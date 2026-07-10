#!/usr/bin/env python3
"""Korea W3 — mint Udo gateway ferries (Seongsan↔Udo, Jongdal↔Udo).

BPs already sealed. Demand from KOREA-L3-SOURCING (~3.19M one-way pax/yr
Seongsan/Jongdal ↔ Udo) allocated across the two ferry links (not double-counted).
Then patch finance spines for kakao-mobility / swing / naver.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys_path_geo = ROOT / "scripts/grok-geometry"
import sys

sys.path.insert(0, str(sys_path_geo))
from route_land_qa import evaluate_feature  # noqa: E402

ROUTES = ROOT / "data-clean/ROUTES.json"
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
RECAL = ROOT / "finance/recal"
CANON = ROOT / "handoff/korea-deepening/korea-corridors-canonical.json"
MODEL = ROOT / "finance/model/corridors.json"
RECEIPT = ROOT / "handoff/korea-deepening/KOREA-W3-UDO-GATEWAY-MINT-2026-07-09.json"

PARTNERS = ("kakao-mobility", "swing", "naver")

# Existing sealed BPs
SEONGSAN = "bp-cac137da7d"
UDO = "bp-fd2840f8b6"
JONGDAL = "bp-5556ff6aee"

# L3: 3,188,200 one-way Seongsan/Jongdal ↔ Udo (JTO T2)
# Allocate by relative ferry role: Seongsan primary gateway ~65%, Jongdal secondary ~35%
UDO_POOL_PAX = 3_188_200
SEONGSAN_SHARE = 0.65
FARE_USD = 3.75


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def mint_route_id(a: str, b: str, tag: str) -> str:
    lo, hi = sorted([a, b])
    return "rn-" + hashlib.md5(f"{tag}|{lo}|{hi}".encode()).hexdigest()[:12]


def hav_nm(a: list[float], b: list[float]) -> float:
    R = 6371.0
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(min(1.0, math.sqrt(h))) / 1.852


def densify(a: list[float], b: list[float], n: int = 16) -> list[list[float]]:
    out = []
    for i in range(n + 1):
        t = i / n
        out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


def bp_index(fbt: dict) -> dict[str, dict]:
    out = {}
    for f in fbt.get("poi") or []:
        p = f.get("properties") or {}
        pid = p.get("id")
        if pid:
            out[pid] = {
                "props": p,
                "coords": (f.get("geometry") or {}).get("coordinates"),
                "name": p.get("name") or pid,
            }
    return out


def make_route(
    rid: str,
    from_bp: str,
    to_bp: str,
    from_name: str,
    to_name: str,
    from_xy: list[float],
    to_xy: list[float],
) -> dict:
    coords = densify(from_xy, to_xy, 18)
    nm = round(hav_nm(from_xy, to_xy), 2)
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": "Pioneer II",
            "distance_nm": nm,
            "edge_class": "local",
            "from": from_bp,
            "to": to_bp,
            "from_node": from_bp,
            "to_node": to_bp,
            "from_label": from_name,
            "to_label": to_name,
            "from_city": "Jeju",
            "to_city": "Jeju",
            "from_city_id": "jeju-korea",
            "to_city_id": "jeju-korea",
            "label": f"Jeju: {from_name} → {to_name}",
            "trip_scope": "intra_city",
            "trip_purpose": "intra_city",
            "traffic_weight": 0.75,
            "cluster_id": "korea",
            "_korea_w3_udo": True,
            "_minted_at": utc_now(),
            "_mint_source": "handoff/korea-deepening KOREA-L3 Udo gateway",
        },
    }


def corridor_row(feat: dict, pax: int, fare: float, method: str) -> dict:
    p = feat["properties"]
    return {
        "route_id": p["id"],
        "from": p["from_label"],
        "to": p["to_label"],
        "distance_nm": p["distance_nm"],
        "vessel": "Pioneer II",
        "archetype": "local",
        "from_node_id": "jeju-korea",
        "to_node_id": "jeju-korea",
        "country": "South Korea",
        "pool_basis": "addressable",
        "L3_locals": {
            "comparable_fare_usd_pax": fare,
            "corridor_annual_oneway_pax": pax,
            "_demand_record": {
                "value": pax,
                "unit": "pax/yr one-way",
                "source_tier": "T2",
                "confidence": "high",
                "source": "JTO / KOREA-L3-SOURCING Seongsan-Jongdal↔Udo 3.188M pool",
                "method": method,
            },
            "_fare_record": {
                "value": fare,
                "unit": "USD/pax/one-way",
                "source_tier": "T2",
                "confidence": "med",
                "source": "KOREA-L3-SOURCING fare_usd 3.75",
                "method": "korea_w3_udo_fare",
            },
            "demand_confidence": "high",
        },
        "_vessel_key": "pioneer_ii",
        "_korea_spine": True,
        "_korea_w3_udo": True,
        "_edge_class": "local",
    }


def patch_finance(new_corridors: list[dict]) -> dict:
    """Append Udo corridors to recal + model korea-* markets if missing."""
    stats = {}
    new_ids = {c["route_id"] for c in new_corridors}

    for partner in PARTNERS:
        path = RECAL / f"corridors-{partner}.json"
        doc = load(path)
        mkt = doc["markets"][partner]
        existing = {c.get("route_id") for c in mkt.get("corridors") or []}
        added = 0
        for c in new_corridors:
            if c["route_id"] not in existing:
                mkt["corridors"].append(deepcopy(c))
                added += 1
        mkt["_corridors_bound"] = len(mkt["corridors"])
        mkt["_korea_w3_udo_at"] = utc_now()
        save(path, doc)
        stats[partner] = {"added": added, "total": len(mkt["corridors"])}

    # model markets
    model = load(MODEL)
    for partner in PARTNERS:
        key = f"korea-{partner}"
        m = model.setdefault("markets", {}).get(key)
        if not m:
            continue
        existing = {c.get("route_id") for c in m.get("corridors") or []}
        for c in new_corridors:
            if c["route_id"] not in existing:
                m.setdefault("corridors", []).append(deepcopy(c))
        m["_corridors_bound"] = len(m.get("corridors") or [])
    save(MODEL, model)

    # canonical inventory
    if CANON.exists():
        can = load(CANON)
        rows = can.setdefault("korea_canonical_corridors", [])
        have = {r.get("route_id") for r in rows}
        for c in new_corridors:
            rid = c["route_id"]
            if rid in have:
                continue
            rows.append(
                {
                    "route_id": rid,
                    "od": f"{c['from']} -> {c['to']}",
                    "distance_nm": c["distance_nm"],
                    "from_city_id": "jeju-korea",
                    "to_city_id": "jeju-korea",
                    "trip_purpose": "intra_city",
                    "edge_class": "local",
                    "_korea_w3_udo": True,
                }
            )
        save(CANON, can)

    stats["new_ids"] = sorted(new_ids)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    fbt = load(FBT)
    bps = bp_index(fbt)
    for need in (SEONGSAN, UDO, JONGDAL):
        if need not in bps or not bps[need]["coords"]:
            print(f"✗ missing BP {need}")
            return 2

    pairs = [
        (
            SEONGSAN,
            UDO,
            int(round(UDO_POOL_PAX * SEONGSAN_SHARE)),
            f"korea_w3/udo_pool_alloc share={SEONGSAN_SHARE} of {UDO_POOL_PAX}",
        ),
        (
            JONGDAL,
            UDO,
            int(round(UDO_POOL_PAX * (1 - SEONGSAN_SHARE))),
            f"korea_w3/udo_pool_alloc share={1-SEONGSAN_SHARE} of {UDO_POOL_PAX}",
        ),
    ]

    raw = load(ROUTES)
    feats = raw if isinstance(raw, list) else raw.get("features") or []
    existing = {(f.get("properties") or {}).get("id") for f in feats}

    minted_feats = []
    finance_rows = []
    qa = []

    for a, b, pax, method in pairs:
        rid = mint_route_id(a, b, "korea-w3-udo")
        if rid in existing:
            # still rebuild finance row from existing geometry
            feat = next(f for f in feats if (f.get("properties") or {}).get("id") == rid)
        else:
            feat = make_route(
                rid,
                a,
                b,
                bps[a]["name"],
                bps[b]["name"],
                bps[a]["coords"],
                bps[b]["coords"],
            )
            ev = evaluate_feature(feat)
            qa.append({"route_id": rid, **ev})
            if not ev.get("qa_pass"):
                print(f"⚠ QA fail {rid}: {ev}")
            minted_feats.append(feat)
        finance_rows.append(corridor_row(feat if rid not in existing else feat, pax, FARE_USD, method))
        if rid in existing:
            finance_rows[-1]["_already_in_routes"] = True

    receipt = {
        "at": utc_now(),
        "pool_pax": UDO_POOL_PAX,
        "allocation": {
            "seongsan_udo_share": SEONGSAN_SHARE,
            "jongdal_udo_share": 1 - SEONGSAN_SHARE,
        },
        "fare_usd": FARE_USD,
        "minted_route_ids": [f["properties"]["id"] for f in minted_feats],
        "finance_rows": [
            {
                "route_id": r["route_id"],
                "pax": r["L3_locals"]["corridor_annual_oneway_pax"],
                "fare": r["L3_locals"]["comparable_fare_usd_pax"],
                "nm": r["distance_nm"],
            }
            for r in finance_rows
        ],
        "qa": qa,
        "bps": {k: bps[k]["coords"] for k in (SEONGSAN, UDO, JONGDAL)},
    }

    if not args.apply:
        print(json.dumps(receipt, indent=2))
        return 0

    for feat in minted_feats:
        feats.append(feat)
    if isinstance(raw, list):
        save(ROUTES, feats)
    else:
        raw["features"] = feats
        save(ROUTES, raw)

    fin = patch_finance(finance_rows)
    receipt["finance"] = fin
    save(RECEIPT, receipt)
    print(json.dumps(receipt, indent=2, default=str)[:2500])
    print(f"wrote {RECEIPT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
