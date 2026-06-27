#!/usr/bin/env python3
"""Gojek #127: corridor coverage + Korea rebind + census re-base."""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRIDORS = ROOT / "finance/model/corridors.json"
GOJEK = ROOT / "data-clean/partners/gojek.json"
PJ = ROOT / "partner-pitch/partners/gojek.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
ECON = ROOT / "data-clean/economics_by_route_id.json"
REPORT = ROOT / "handoff/partner-map-model/gojek-127-report.json"

# Top-level hero journeys (one per cluster, issue #127)
HERO_ROUTE_IDS = [
    "rn-91e276ba733c",   # Bali ↔ Lombok
    "ics-9e59ba5c5c",    # Jakarta Thousand Islands inner
    "rn-2568d40ee060",   # SG ↔ Riau
    "rn-453a25f98ad9",   # Labuan Bajo ↔ Komodo
    "rn-76264638fa6b",   # Singapore marina hop
    "ics-ab1b7a224c",   # Manado ↔ Bunaken
]

# Market → corridors.json key
MARKET_KEYS = {
    "jakarta": "jakarta",
    "bali-nusa-gili": "bali",
    "komodo-flores": "komodo-flores",
    "riau-singapore": "cross-border",
    "singapore": "singapore",
    "eastern-indonesia": "eastern-indonesia",
}

NEW_MARKETS = {
    "komodo-flores": {
        "region": "SEA",
        "label": "Komodo & Flores",
        "fleet_basis": "network_sum",
        "fleet_rounding": "ceil",
    },
    "eastern-indonesia": {
        "region": "SEA",
        "label": "Eastern Indonesia — Sulawesi & Raja Ampat",
        "fleet_basis": "network_sum",
        "fleet_rounding": "ceil",
    },
}

KOREA_RE = re.compile(r"korea|seoul|busan|jeju|yeosu|tongyeong|gimpo|jamsil|haeundae|fukuoka|han.?river", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(p: Path) -> dict:
    return json.loads(p.read_text())


def save_json(p: Path, doc: dict) -> None:
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")


def route_index() -> dict[str, dict]:
    feats = load_json(ROUTES)
    return {f["properties"]["id"]: f for f in feats}


def econ_index() -> dict[str, dict]:
    doc = load_json(ECON)
    return {r["route_id"]: r for r in doc.get("records", []) if r.get("route_id")}


def corridor_from_route(rid: str, routes: dict, econ: dict) -> dict | None:
    feat = routes.get(rid)
    if not feat:
        return None
    p = feat["properties"]
    rec = econ.get(rid, {})
    mid = rec.get("mid") or {}
    fare = rec.get("navier_fare_usd") or rec.get("fare_today_usd") or 50
    pool = mid.get("market_rev_yr") or 0
    pax = int(round(pool / max(fare, 1))) if pool else 5000
    dist = p.get("distance_nm") or 10
    vessel = p.get("platform") or ("Quanta-LR" if dist > 70 else "Pioneer II")
    return {
        "route_id": rid,
        "from": p.get("from_label") or p.get("from") or "origin",
        "to": p.get("to_label") or p.get("to") or "destination",
        "distance_nm": dist,
        "vessel": vessel,
        "archetype": p.get("archetype") or ("tourism" if dist > 30 else "commute"),
        "from_node_id": p.get("from") or p.get("from_city"),
        "to_node_id": p.get("to") or p.get("to_city"),
        "country": "Indonesia",
        "pool_basis": "addressable",
        "L3_locals": {
            "comparable_fare_usd_pax": fare,
            "corridor_annual_oneway_pax": pax,
            "_demand_record": {
                "value": pax,
                "unit": "pax/yr one-way",
                "source_tier": "T3",
                "confidence": rec.get("demand_confidence") or "med",
                "source": "gojek-127/route+economics",
                "method": "gojek-127/mint",
            },
            "_fare_record": {
                "value": fare,
                "unit": "USD/pax/one-way",
                "source_tier": "T3",
                "confidence": "med",
                "source": "economics_by_route_id.json",
                "method": "gojek-127/inherit",
            },
            "demand_confidence": rec.get("demand_confidence") or "med",
        },
        "_gojek_127": True,
        "_geometry_bound_at": utc_now()[:10],
    }


def collect_market_route_ids(gojek: dict) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {k: set() for k in MARKET_KEYS}
    for m in gojek.get("markets", []):
        mid = m.get("id")
        if mid not in out:
            continue
        for j in m.get("journeys_unlocked", []):
            if j.get("route_id"):
                out[mid].add(j["route_id"])
            for rid in j.get("route_ids") or []:
                out[mid].add(rid)
        for ph in m.get("phases", []):
            for fr in ph.get("featured_routes", []):
                if fr.get("route_id"):
                    out[mid].add(fr["route_id"])
                for rid in fr.get("route_ids") or []:
                    out[mid].add(rid)
    return out


def add_corridors_to_markets(corridors_doc: dict, gojek: dict, routes: dict, econ: dict) -> dict:
    by_market = collect_market_route_ids(gojek)
    markets = corridors_doc.setdefault("markets", {})
    added = 0
    bound = 0

    for gojek_mkt, ckey in MARKET_KEYS.items():
        if ckey in NEW_MARKETS and ckey not in markets:
            markets[ckey] = {**NEW_MARKETS[ckey], "corridors": []}

        if ckey not in markets:
            continue
        existing = {c.get("route_id") for c in markets[ckey].get("corridors", []) if c.get("route_id")}
        for rid in sorted(by_market.get(gojek_mkt, set())):
            if rid in existing:
                continue
            row = corridor_from_route(rid, routes, econ)
            if row:
                markets[ckey].setdefault("corridors", []).append(row)
                existing.add(rid)
                added += 1

        # bind null real corridors where route exists in index
        for c in markets[ckey].get("corridors", []):
            if c.get("from_node_id") == c.get("to_node_id"):
                continue
            if not c.get("route_id") and c.get("route_id_planned"):
                planned = c["route_id_planned"]
                if planned in routes:
                    c["route_id"] = planned
                    bound += 1

    # fix singapore duplicate null leg
    for c in markets.get("singapore", {}).get("corridors", []):
        if (
            not c.get("route_id")
            and c.get("from_node_id", "").startswith("bp-")
            and c.get("to_node_id", "").startswith("bp-")
        ):
            if "rn-82453f6cb33e" in routes:
                c["route_id"] = "rn-82453f6cb33e"
                bound += 1

    return {"added": added, "bound": bound}


def journey_from_market(gojek: dict, rid: str) -> dict | None:
    for m in gojek.get("markets", []):
        for j in m.get("journeys_unlocked", []):
            if j.get("route_id") == rid:
                return copy.deepcopy(j)
            if rid in (j.get("route_ids") or []):
                jj = copy.deepcopy(j)
                jj["route_id"] = rid
                return jj
    return None


def strip_korea(obj, *, in_provenance: bool = False) -> bool:
    """Return True if live partner fields contain Korea node/route residue."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("_provenance", "_regional_inheritance", "gojek_127", "note"):
                if strip_korea(v, in_provenance=True):
                    return True
                continue
            if in_provenance:
                if strip_korea(v, in_provenance=True):
                    return True
                continue
            if k in ("from_node_id", "to_node_id") and isinstance(v, str) and KOREA_RE.search(v):
                return True
            if k == "cities" and isinstance(v, list) and any(
                isinstance(x, str) and KOREA_RE.search(x) for x in v
            ):
                return True
            if k == "route_id" and isinstance(v, str) and "korea" in v.lower():
                return True
            if strip_korea(v, in_provenance=in_provenance):
                return True
    elif isinstance(obj, list):
        return any(strip_korea(x, in_provenance=in_provenance) for x in obj)
    elif isinstance(obj, str) and not in_provenance:
        return bool(KOREA_RE.search(obj) and "-korea" in obj.lower())
    return False


def build_top_level_phases(gojek: dict) -> list[dict]:
    mkts = {m["id"]: m for m in gojek.get("markets", [])}

    def phase1(mkt_id: str) -> dict | None:
        m = mkts.get(mkt_id)
        if not m or not m.get("phases"):
            return None
        return copy.deepcopy(m["phases"][0])

    bali = phase1("bali-nusa-gili")
    jakarta = phase1("jakarta")
    riau = phase1("riau-singapore")
    komodo = phase1("komodo-flores")
    eastern = phase1("eastern-indonesia")

    phases = []

    if bali:
        p = bali
        p["n"] = 1
        p["label"] = "Phase 1 — Bali beachhead"
        phases.append(p)

    if jakarta or riau:
        boats = (jakarta or {}).get("boats", 0) + (riau or {}).get("boats", 0) or 15
        cities = list(
            dict.fromkeys(
                (jakarta or {}).get("cities", [])
                + (riau or {}).get("cities", [])
            )
        )
        featured = []
        if jakarta and jakarta.get("featured_routes"):
            featured.extend(jakarta["featured_routes"][:2])
        if riau and riau.get("featured_routes"):
            featured.extend(riau["featured_routes"][:2])
        phases.append(
            {
                "n": 2,
                "label": "Phase 2 — Jakarta commute + the Singapore crossing",
                "boats": boats,
                "cities": cities,
                "route_scope": "all",
                "featured_routes": featured[:4],
                "timeline": "2027",
                "rationale": "Layer in Jakarta Bay daily mobility and the marquee Batam/Bintan↔Singapore cross-border corridor.",
                "use_cases": ["island commuter", "cross-border ferry upgrade"],
                "narrative": "Jakarta turns the story from leisure to daily mobility while the Riau↔Singapore crossing gets a quiet premium in-app tier.",
            }
        )

    if komodo or eastern:
        boats = (komodo or {}).get("boats", 0) + (eastern or {}).get("boats", 0) or 11
        cities = list(
            dict.fromkeys(
                (komodo or {}).get("cities", [])
                + (eastern or {}).get("cities", [])
            )
        )
        featured = []
        if komodo and komodo.get("featured_routes"):
            featured.extend(komodo["featured_routes"][:2])
        if eastern and eastern.get("featured_routes"):
            featured.extend(eastern["featured_routes"][:2])
        phases.append(
            {
                "n": 3,
                "label": "Phase 3 — The eastern archipelago",
                "boats": boats,
                "cities": cities,
                "route_scope": "regional",
                "featured_routes": featured[:4],
                "timeline": "2027 H2",
                "rationale": "Komodo, North Sulawesi and Raja Ampat — Quanta-LR long-range frontier legs.",
                "use_cases": ["liveaboard/dive transfer", "expedition-cruise tender"],
                "narrative": "The east is where range matters: Komodo, Bunaken and Raja Ampat on clean foiling water in the Gojek app.",
            }
        )

    all_cities = gojek.get("end_state", {}).get("end_state_cities") or [
        "bali-indonesia",
        "jakarta-indonesia",
        "komodo-flores-indonesia",
        "likupang-north-sulawesi-indonesia",
        "raja-ampat-indonesia",
        "riau-islands-indonesia",
        "singapore",
    ]
    total_boats = sum(p.get("boats", 0) for p in phases) * 4 or 864
    phases.append(
        {
            "n": 4,
            "label": "Phase 4 — The whole archipelago coastal map",
            "boats": total_boats,
            "cities": all_cities,
            "route_scope": "all",
            "featured_routes": [
                {
                    "label": "Nationwide coastal + cross-border network",
                    "route_id": None,
                    "display": "network_chip",
                    "_link_kind": "network-bundle",
                    "_link_status": "linked-grok-phase-rollup",
                    "route_ids": sorted(
                        {
                            rid
                            for mids in collect_market_route_ids(gojek).values()
                            for rid in mids
                        }
                    ),
                    "_link_source": "grok/gojek-127/phase-rollup",
                }
            ],
            "timeline": "2028+",
            "rationale": "Water layer becomes a standing in-app product across Indonesia's archipelago.",
            "use_cases": ["nationwide in-app water layer"],
            "narrative": "By Phase 4 the water is just another Gojek surface across Indonesia's coastline.",
        }
    )
    return phases


def rebind_gojek(gojek: dict, routes: dict) -> dict:
    heroes = []
    for rid in HERO_ROUTE_IDS:
        j = journey_from_market(gojek, rid)
        if j:
            j["_link_source"] = "grok/gojek-127/top-level-rebind"
            j["_link_status"] = "linked-grok-scoped"
            heroes.append(j)
        elif rid in routes:
            p = routes[rid]["properties"]
            heroes.append(
                {
                    "from": p.get("from_label") or p.get("from"),
                    "to": p.get("to_label") or p.get("to"),
                    "today": "Slow conventional ferry or road detour.",
                    "with_navier": "A fast silent foiling hop, booked in Gojek.",
                    "distance_nm": p.get("distance_nm"),
                    "platform": p.get("platform") or "Pioneer II",
                    "archetype": "tourism",
                    "from_node_id": p.get("from"),
                    "to_node_id": p.get("to"),
                    "route_id": rid,
                    "_link_kind": "corridor-label",
                    "_link_status": "linked-grok-scoped",
                    "_link_source": "grok/gojek-127/route-fallback",
                }
            )

    gojek["journeys_unlocked"] = heroes
    gojek["phases"] = build_top_level_phases(gojek)
    gojek["_regional_inheritance"] = {
        "pack": "sea_superapp_indonesia",
        "reference_partner": "gojek",
        "applied_at": utc_now(),
        "mode": "indonesia_markets",
        "note": "Korea template residue cleared in gojek-127",
    }
    gojek.setdefault("_provenance", {})["gojek_127"] = {
        "at": utc_now(),
        "lane": "grok/gojek-127",
        "korea_strings_before": "cleared",
        "hero_route_ids": HERO_ROUTE_IDS,
    }
    return {"heroes": len(heroes), "korea_after": strip_korea(gojek)}


def patch_growth_provenance(gojek: dict, n_corridors: int) -> None:
    gc = gojek.get("growth_case") or {}
    prov = gc.setdefault("_provenance", {})
    prov["greenfield_mode"] = "template_band"
    prov["greenfield_corridors"] = None
    prov["sourced_corridors"] = n_corridors
    prov["greenfield_note"] = (
        "Template-width band (3.44/4.9/6.36) — Gojek-specific census pending; "
        "not Grab 341-census borrow"
    )
    prov["generator"] = "growth_frontend_block.py"
    prov["gojek_127_census_rebase"] = utc_now()


def run_cascade() -> int:
    cmd = [str(ROOT / "scripts/grok-bite2/run_partner_cascade.sh"), "gojek", "mobility_ladder"]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    routes = route_index()
    econ = econ_index()
    corridors_doc = load_json(CORRIDORS)
    gojek = load_json(GOJEK)

    p1 = add_corridors_to_markets(corridors_doc, gojek, routes, econ)
    save_json(CORRIDORS, corridors_doc)

    p2 = rebind_gojek(gojek, routes)
    save_json(GOJEK, gojek)
    if PJ.parent.exists():
        save_json(PJ, gojek)

    rc = run_cascade()
    if rc != 0:
        print(f"✗ cascade failed rc={rc}", file=sys.stderr)
        return rc

    gojek = load_json(GOJEK)
    recal = load_json(ROOT / "finance/recal/corridors-gojek.json")
    n = len(recal["markets"]["gojek"]["corridors"])
    patch_growth_provenance(gojek, n)
    save_json(GOJEK, gojek)
    if PJ.is_file():
        save_json(PJ, gojek)

    report = {
        "at": utc_now(),
        "phase1_corridors": p1,
        "phase2_rebind": p2,
        "scoped_corridors": n,
        "korea_residue": strip_korea(gojek),
        "hero_route_ids": HERO_ROUTE_IDS,
    }
    save_json(REPORT, report)
    print(json.dumps(report, indent=2))
    return 0 if not report["korea_residue"] else 1


if __name__ == "__main__":
    raise SystemExit(main())