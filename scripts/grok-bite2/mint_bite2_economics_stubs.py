#!/usr/bin/env python3
"""Mint bite2 economics stubs for partner route_ids missing from economics_by_route_id.json."""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIPPED = [
    "didi", "kakao-mobility", "cabify", "wsf", "shun-tak", "bc-ferries", "nyc-ferry",
    "thames-clippers", "transport-nsw", "fullers360", "hong-kong", "norway-fjords",
    "hawaii", "maldives", "crown-champa", "universal-enterprises", "villa-hotels",
]
REPORT = ROOT / "handoff" / "partner-map-model" / "bite2-econ-stubs-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect_route_ids(doc: dict) -> set[str]:
    ids: set[str] = set()

    def walk(o):
        if isinstance(o, dict):
            rid = o.get("route_id")
            if isinstance(rid, str) and rid:
                ids.add(rid)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(doc)
    return ids


def fare_usd(nm: float, *, hospitality: bool) -> float:
    if hospitality:
        return round(max(85.0, min(450.0, 60.0 + nm * 4.5)), 2)
    return round(max(12.0, min(220.0, 10.0 + nm * 2.8)), 2)


def annual_pax(nm: float, *, hospitality: bool) -> int:
    base = 12000 if hospitality else 18000
    scale = 600 if hospitality else 900
    return int(max(base, min(250000, base + nm * scale)))


def mid_block(fare: float, pax: float, nm: float) -> dict:
    trips_day = max(4, min(12, int(10 - nm / 25)))
    op_days = 274
    rev_boat = fare * trips_day * op_days * 0.62
    vessels = max(3, int(math.ceil(pax * 0.10 / max(trips_day * op_days * 0.62, 1))))
    market_rev = fare * pax
    return {
        "rev_per_boat_yr": round(rev_boat, 2),
        "margin": 0.82,
        "payback_years": round(0.35 + nm / 200, 2),
        "co2_saved_t_per_boat_yr": round(nm * 4.2, 1),
        "vessels_10pct": vessels,
        "market_rev_yr": round(market_rev, 2),
    }


def stub_for_route(props: dict, *, partner: str, hospitality: bool) -> dict:
    rid = props["id"]
    nm = float(props.get("distance_nm") or props.get("distance_nm_geom") or 10)
    fl = props.get("from_label") or props.get("from") or "origin"
    tl = props.get("to_label") or props.get("to") or "destination"
    city = props.get("from_city_id") or props.get("to_city_id") or partner
    fare = fare_usd(nm, hospitality=hospitality)
    pax = annual_pax(nm, hospitality=hospitality)
    vessel = "N30 Pioneer II" if nm <= 70 else "Quanta-LR"
    return {
        "route_id": rid,
        "registry_market_id": city,
        "authored_for": partner,
        "corridor": f"{fl} -> {tl}",
        "market": city.replace("-", " ").title(),
        "country": props.get("from_city") or "Global",
        "distance_nm": nm,
        "status": "estimated",
        "demand_confidence": "med-low",
        "fare_today_usd": fare,
        "navier_fare_usd": fare,
        "vessel": vessel,
        "mid": mid_block(fare, pax, nm),
        "estimation_basis": "bite2_stub_cascade",
        "assumptions": {
            "method": "bite2/distance_tier_stub",
            "note": "Stub economics for ladder cascade — replace with deck-grounded rows when available",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--partner", action="append")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    partners = args.partner or SKIPPED
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    by_id = {f["properties"]["id"]: f["properties"] for f in routes if f.get("properties", {}).get("id")}

    econ_path = ROOT / "data-clean" / "economics_by_route_id.json"
    econ = json.loads(econ_path.read_text())
    records = list(econ.get("records") or [])
    have = {r["route_id"] for r in records if r.get("route_id")}

    added: list[dict] = []
    for partner in partners:
        ppath = ROOT / "data-clean" / "partners" / f"{partner}.json"
        if not ppath.is_file():
            continue
        doc = json.loads(ppath.read_text())
        hospitality = doc.get("archetype") == "hospitality" or "hospitality" in (doc.get("category") or "")
        rids = collect_route_ids(doc)
        for rid in sorted(rids):
            if rid in have:
                continue
            props = by_id.get(rid)
            if not props:
                continue
            rec = stub_for_route(props, partner=partner, hospitality=hospitality)
            records.append(rec)
            have.add(rid)
            added.append({"partner": partner, "route_id": rid})

    report = {
        "at": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "added": len(added),
        "by_partner": {},
        "samples": added[:20],
    }
    for row in added:
        report["by_partner"][row["partner"]] = report["by_partner"].get(row["partner"], 0) + 1

    if args.apply and added:
        econ["records"] = records
        meta = econ.setdefault("_meta", {})
        meta["records"] = len(records)
        meta["bite2_stubs_at"] = report["at"]
        meta["bite2_stubs_added"] = len(added)
        econ_path.write_text(json.dumps(econ, indent=1, ensure_ascii=False) + "\n")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())