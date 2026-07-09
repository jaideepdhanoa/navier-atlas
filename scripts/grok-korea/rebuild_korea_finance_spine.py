#!/usr/bin/env python3
"""#209 W1–W2+W5: rebuild Korea finance spine on 39 canonical rn- corridors.

- Identical spine for kakao-mobility · swing · naver (finance-corridor inheritance)
- L3 attach with level discipline (port_total / market pools allocated; never 1:1)
- Greenfield factor for remaining null route-level ODs (null beats invented route demand)
- Writes finance/recal/corridors-{partner}.json; optional model market seed
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CANON = ROOT / "handoff/korea-deepening/korea-corridors-canonical.json"
L3 = ROOT / "handoff/korea-deepening/KOREA-L3-SOURCING-2026-07-09.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
RECAL = ROOT / "finance/recal"
MODEL = ROOT / "finance/model/corridors.json"
RECEIPT = ROOT / "handoff/korea-deepening/KOREA-FINANCE-SPINE-REBUILD-2026-07-09.json"

PARTNERS = ("kakao-mobility", "swing", "naver")
# Greenfield factor vs median allocated route pax (Grab-style width lever; thin)
GREENFIELD_FACTOR = 0.22
# Hangang Bus run-rate (spec headline table) — market pool for Hangang local hops
HANGANG_RUNRATE_PAX = 1_050_000


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(p: Path) -> Any:
    return json.loads(p.read_text())


def save_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def route_index() -> dict[str, dict]:
    raw = load_json(ROUTES)
    feats = raw if isinstance(raw, list) else raw.get("features") or []
    out: dict[str, dict] = {}
    for f in feats:
        p = f.get("properties") or {}
        rid = p.get("id")
        if rid:
            out[rid] = p
    return out


def l3_record(value: float | None, *, tier: str, conf: str, source: str, method: str, unit: str) -> dict | None:
    if value is None:
        return None
    return {
        "value": value,
        "unit": unit,
        "source_tier": tier,
        "confidence": conf,
        "source": source,
        "method": method,
    }


def build_spine() -> tuple[list[dict], dict]:
    canon = load_json(CANON)["korea_canonical_corridors"]
    l3doc = load_json(L3)
    rows = l3doc["corridor_rows"]
    ridx = route_index()

    # Index fare/pax by route_id (prefer non-null pax; prefer route-level fare)
    by_rid: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if r.get("route_id"):
            by_rid[r["route_id"]].append(r)

    fare_by: dict[str, float] = {}
    for rid, rs in by_rid.items():
        for r in rs:
            if r.get("fare_usd") is not None:
                fare_by[rid] = float(r["fare_usd"])
                break

    # Direct bindable: port_pair / route with pax on a real route_id
    direct_pax: dict[str, tuple[float, dict]] = {}
    for r in rows:
        rid = r.get("route_id")
        pax = r.get("annual_oneway_pax")
        if not rid or pax is None:
            continue
        level = r.get("level")
        if level in ("route", "port_pair"):
            direct_pax[rid] = (float(pax), r)
        # port_total never 1:1 — handled as pools below

    # Pools
    tongyeong_pool = 1_745_223.0  # KOMSA Tongyeong district — port_total
    incheon_pool = 1_081_234.0  # ICPA coastal terminal
    oedo_pool = 1_000_000.0  # Geoje Oedo cruise boardings (customers/yr ≈ boardings)

    # Classify routes into allocation buckets
    hangang_ids: list[str] = []
    incheon_ids: list[str] = []
    tongyeong_ids: list[str] = []
    oedo_geoje_ids: list[str] = []
    jeju_ids: list[str] = []

    HANGANG_RE = re.compile(
        r"oks u|oks u|apgujeong|seoul forest|ttukseom|jamsil|yeouido|magok|mangwon|hangang",
        re.I,
    )
    # fix typo pattern
    HANGANG_RE = re.compile(
        r"oksu|apgujeong|seoul forest|ttukseom|jamsil|yeouido|magok|mangwon|hangang",
        re.I,
    )
    INCHEON_RE = re.compile(r"incheon|muuido|yeongjong|gimpo ara|ara marina", re.I)
    TONG_RE = re.compile(
        r"tongyeong|yokjido|saryang|geumodo|gaochi|samdeok|yeosu passenger|samcheonpo",
        re.I,
    )
    OEDO_RE = re.compile(r"geoje|busan coastal|jangseungpo|oedo", re.I)
    JEJU_RE = re.compile(r"jeju|seongsan|hallim|jongdal|seopjikoji|seogwipo|udo", re.I)

    for c in canon:
        rid = c["route_id"]
        od = c.get("od") or ""
        cities = f"{c.get('from_city_id','')} {c.get('to_city_id','')}"
        blob = f"{od} {cities}"
        if "hangang" in cities or HANGANG_RE.search(od):
            hangang_ids.append(rid)
        if INCHEON_RE.search(blob) and "hangang" not in cities:
            incheon_ids.append(rid)
        if TONG_RE.search(blob):
            tongyeong_ids.append(rid)
        if c.get("from_city_id") == "busan-geoje-korea" or c.get("to_city_id") == "busan-geoje-korea":
            if rid not in ("rn-e44147de575d", "rn-6786317ef18f"):  # not Fukuoka / Busan-Jeju trunk
                oedo_geoje_ids.append(rid)
        if "jeju" in cities or JEJU_RE.search(od):
            jeju_ids.append(rid)

    # Dedupe allocation membership (prefer more specific first later)
    def unique(seq: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for x in seq:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    hangang_ids = unique(hangang_ids)
    incheon_ids = unique(incheon_ids)
    tongyeong_ids = unique(tongyeong_ids)
    oedo_geoje_ids = unique(oedo_geoje_ids)
    jeju_ids = unique(jeju_ids)

    alloc: dict[str, dict] = {}

    def allocate(ids: list[str], pool: float, *, tag: str, tier: str, conf: str, source: str) -> None:
        if not ids or pool <= 0:
            return
        share = pool / len(ids)
        for rid in ids:
            prev = alloc.get(rid)
            # Prefer higher-confidence direct over pool; if already direct, skip pool
            if prev and prev.get("kind") == "direct":
                continue
            # If already pooled, keep the larger pool share (don't double-count across pools)
            if prev and prev.get("kind") == "pool":
                continue
            alloc[rid] = {
                "kind": "pool",
                "pax": share,
                "tag": tag,
                "tier": tier,
                "conf": conf,
                "source": source,
                "pool_total": pool,
                "pool_n": len(ids),
            }

    # Direct first
    for rid, (pax, r) in direct_pax.items():
        alloc[rid] = {
            "kind": "direct",
            "pax": pax,
            "tag": r.get("level"),
            "tier": (r.get("sources") or [{}])[0].get("tier") or "T2",
            "conf": (r.get("sources") or [{}])[0].get("confidence") or "med",
            "source": (r.get("sources") or [{}])[0].get("url") or "KOREA-L3-SOURCING",
            "level": r.get("level"),
        }

    allocate(
        hangang_ids,
        float(HANGANG_RUNRATE_PAX),
        tag="hangang_runrate_pool",
        tier="T1",
        conf="med",
        source="Seoul City Hangang Bus run-rate (~1.05M/yr; spec headline)",
    )
    allocate(
        incheon_ids,
        incheon_pool,
        tag="incheon_coastal_terminal_pool",
        tier="T1",
        conf="high",
        source="https://www.icpa.or.kr/icferry/mobile/main.do?menuKey=779",
    )
    allocate(
        tongyeong_ids,
        tongyeong_pool,
        tag="tongyeong_district_pool",
        tier="T1",
        conf="high",
        source="KOMSA Tongyeong district coastal 2025",
    )
    allocate(
        oedo_geoje_ids,
        oedo_pool,
        tag="oedo_geoje_cruise_pool",
        tier="T2",
        conf="med",
        source="Geoje Oedo cruise piers ~1M customers/yr (allocation pool)",
    )

    # Median for greenfield
    grounded = [a["pax"] for a in alloc.values() if a.get("pax")]
    median_pax = sorted(grounded)[len(grounded) // 2] if grounded else 25_000.0
    greenfield_pax = max(8_000.0, median_pax * GREENFIELD_FACTOR)

    corridors: list[dict] = []
    stats = {
        "canonical": len(canon),
        "direct": 0,
        "pool": 0,
        "greenfield": 0,
        "fare_only": 0,
        "total_pax_sum": 0.0,
    }

    for c in canon:
        rid = c["route_id"]
        props = ridx.get(rid) or {}
        from_l = props.get("from_label") or (c["od"].split("->")[0].strip() if "->" in c["od"] else c["od"])
        to_l = props.get("to_label") or (
            c["od"].split("->", 1)[1].strip() if "->" in c["od"] else c["od"]
        )
        nm = float(props.get("distance_nm") or c.get("distance_nm") or 10)
        platform = props.get("platform") or ("Quanta-LR" if nm > 70 else "Pioneer II")
        vkey = "quanta_lr" if "quanta" in platform.lower() or nm > 70 else "pioneer_ii"

        a = alloc.get(rid)
        fare = fare_by.get(rid)
        if fare is None and props.get("fare_usd"):
            fare = float(props["fare_usd"])
        # default fares by band if still missing
        if fare is None:
            if nm <= 5:
                fare = 4.0
            elif nm <= 30:
                fare = 8.0
            elif nm <= 80:
                fare = 22.0
            else:
                fare = 45.0

        if a and a["kind"] == "direct":
            pax = a["pax"]
            method = f"korea_l3/direct_{a.get('level')}"
            tier, conf, source = a["tier"], a["conf"], a["source"]
            stats["direct"] += 1
        elif a and a["kind"] == "pool":
            pax = a["pax"]
            method = f"korea_l3/pool_alloc:{a['tag']} (pool={a['pool_total']:.0f}/n={a['pool_n']})"
            tier, conf, source = a["tier"], a["conf"], a["source"]
            stats["pool"] += 1
        else:
            pax = greenfield_pax
            method = f"korea_l3/greenfield_factor={GREENFIELD_FACTOR}×median_allocated"
            tier, conf, source = "T3", "low", "greenfield_convention"
            stats["greenfield"] += 1

        stats["total_pax_sum"] += float(pax)

        l3 = {
            "comparable_fare_usd_pax": fare,
            "corridor_annual_oneway_pax": int(round(pax)),
            "_demand_record": l3_record(
                int(round(pax)),
                tier=tier,
                conf=conf,
                source=source,
                method=method,
                unit="pax/yr one-way",
            ),
            "_fare_record": l3_record(
                fare,
                tier="T1" if rid in fare_by else "T3",
                conf="high" if rid in fare_by else "low",
                source="KOREA-L3-SOURCING" if rid in fare_by else "band_default",
                method="korea_l3/fare",
                unit="USD/pax/one-way",
            ),
            "demand_confidence": conf,
        }

        corridors.append(
            {
                "route_id": rid,
                "from": from_l,
                "to": to_l,
                "distance_nm": nm,
                "vessel": platform,
                "archetype": "local" if nm <= 30 else ("regional" if nm <= 120 else "intercity"),
                "from_node_id": c.get("from_city_id"),
                "to_node_id": c.get("to_city_id"),
                "country": "South Korea",
                "pool_basis": "addressable",
                "L3_locals": l3,
                "_vessel_key": vkey,
                "_korea_spine": True,
                "_edge_class": c.get("edge_class"),
            }
        )

    stats["median_allocated_pax"] = median_pax
    stats["greenfield_pax"] = greenfield_pax
    stats["hangang_n"] = len(hangang_ids)
    stats["incheon_n"] = len(incheon_ids)
    stats["tongyeong_n"] = len(tongyeong_ids)
    stats["oedo_n"] = len(oedo_geoje_ids)
    return corridors, stats


def market_block(partner: str, corridors: list[dict]) -> dict:
    labels = {
        "kakao-mobility": "Kakao Mobility — Korea network",
        "swing": "Swing — Korea network",
        "naver": "NAVER — Korea network",
    }
    return {
        "partner": partner,
        "region": "Korea",
        "label": labels.get(partner, partner),
        "fleet_basis": "network_sum",
        "fleet_rounding": "ceil",
        "_scope": "korea-canonical-39",
        "_partner_market_keys": [f"korea-{partner}"],
        "_route_ids_requested": len(corridors),
        "_corridors_bound": len(corridors),
        "_provenance": {
            "spec": "handoff/korea-deepening/GROK-SPEC-korea-tam-deepening-2026-07-09.md",
            "at": utc_now(),
            "w": "W1-W2 spine rebuild + L3 attach",
        },
        "corridors": copy.deepcopy(corridors),
    }


def write_recal(partner: str, corridors: list[dict]) -> Path:
    doc = {
        "_doc": f"Korea finance spine (39 rn-) for {partner} — #209 W1 rebuild",
        "_source": "handoff/korea-deepening/korea-corridors-canonical.json",
        "_built_at": utc_now(),
        "capture_rate": 0.1,
        "markets": {partner: market_block(partner, corridors)},
    }
    out = RECAL / f"corridors-{partner}.json"
    save_json(out, doc)
    return out


def seed_model(corridors: list[dict]) -> None:
    """Seed finance/model/corridors.json korea-* markets for inheritance visibility."""
    model = load_json(MODEL)
    mkts = model.setdefault("markets", {})
    for partner in PARTNERS:
        key = f"korea-{partner}"
        block = market_block(partner, corridors)
        block["capture_rate"] = 0.1
        mkts[key] = block
    model.setdefault("_meta", {})["korea_spine_rebuild_at"] = utc_now()
    save_json(MODEL, model)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--seed-model", action="store_true", help="also write korea-* into model/corridors.json")
    args = ap.parse_args()

    corridors, stats = build_spine()
    receipt = {
        "at": utc_now(),
        "stats": stats,
        "partners": list(PARTNERS),
        "sample": [
            {
                "route_id": c["route_id"],
                "pax": c["L3_locals"]["corridor_annual_oneway_pax"],
                "fare": c["L3_locals"]["comparable_fare_usd_pax"],
                "method": c["L3_locals"]["_demand_record"]["method"],
            }
            for c in corridors[:8]
        ],
    }

    if not args.apply:
        print(json.dumps(receipt, indent=2))
        print(f"(dry-run) spine={len(corridors)} total_pax≈{stats['total_pax_sum']:.0f}")
        return 0

    paths = []
    for partner in PARTNERS:
        paths.append(str(write_recal(partner, corridors)))
    if args.seed_model:
        seed_model(corridors)
        paths.append(str(MODEL))
    save_json(RECEIPT, receipt)
    print(json.dumps({"wrote": paths, **receipt}, indent=2, default=str)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
