#!/usr/bin/env python3
"""
Route-seal kept Bolt/Yango markets: Spain, Sweden, Portugal, Finland, Estonia, Egypt, Morocco, Abidjan.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORRIDORS = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"

KEPT_MARKETS = (
    "bolt-spain",
    "bolt-sweden",
    "bolt-portugal",
    "bolt-finland",
    "bolt-estonia",
    "bolt-egypt",
    "yango-egypt",
    "yango-morocco",
    "yango-cote-divoire",
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bolt_yango_routing_shared import (
    BOLT_YANGO_ANCHORS,
    LAND_THRESH_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    resolve_corridor_endpoints,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)

SIGNATURE_WAYPOINTS: dict[tuple[str, str], list[tuple[float, float]]] = {
    ("bp-porto-ribeira", "bp-porto-gaia"): [(-8.612, 41.14)],
    ("bp-lagos-marina", "bp-ponta-da-piedade"): [(-8.671, 37.093)],
    ("bp-vila-real-santo-antonio", "bp-ayamonte-spain"): [(-7.41, 37.198)],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--corridors", default=str(DEFAULT_CORRIDORS))
    ap.add_argument("--markets", default=",".join(KEPT_MARKETS))
    args = ap.parse_args()

    dc = ROOT / args.dc
    markets = [m.strip() for m in args.markets.split(",") if m.strip()]
    corridors_doc = load_json(Path(args.corridors))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    existing = {route_id_of(r) for r in routes}

    report = {"synthesized": [], "skipped": [], "allowlisted": [], "markets": {}}

    for mkey in markets:
        mval = (corridors_doc.get("markets") or {}).get(mkey)
        if not mval:
            report["skipped"].append({"market": mkey, "reason": "missing_market"})
            continue
        m_stats = {"synth": 0, "skip": 0}
        for corr in mval.get("corridors") or []:
            from_bp, to_bp, from_city, to_city = resolve_corridor_endpoints(corr, bp_idx)
            if not from_bp or not to_bp or from_bp == to_bp:
                m_stats["skip"] += 1
                report["skipped"].append(
                    {
                        "market": mkey,
                        "from": corr.get("from"),
                        "to": corr.get("to"),
                        "reason": "unresolved_bp",
                    }
                )
                continue

            rid = mint_route_id(from_bp, to_bp, tag=mkey)
            if rid in existing:
                m_stats["skip"] += 1
                report["skipped"].append({"route_id": rid, "market": mkey, "reason": "exists"})
                continue

            a = bp_idx[from_bp]["coords"]
            b = bp_idx[to_bp]["coords"]
            manual = SIGNATURE_WAYPOINTS.get((from_bp, to_bp)) or SIGNATURE_WAYPOINTS.get((to_bp, from_bp))
            coords = build_coastal_path(a, b, mask, manual_waypoints=manual)
            land_km = interior_land_km(coords, mask)
            feat = make_route_feature(
                from_bp,
                to_bp,
                bp_idx[from_bp]["name"],
                bp_idx[to_bp]["name"],
                from_city,
                to_city,
                coords,
                cities,
                source="kept_market",
                land_km=land_km,
            )
            feat["properties"]["id"] = rid
            feat["properties"]["_kept_market"] = mkey
            if land_km > LAND_THRESH_KM:
                feat["properties"]["_qa_land_flag"] = True
                report["allowlisted"].append({"route_id": rid, "market": mkey, "land_km": land_km})

            routes.append(feat)
            existing.add(rid)
            m_stats["synth"] += 1
            report["synthesized"].append(
                {
                    "route_id": rid,
                    "market": mkey,
                    "from_bp": from_bp,
                    "to_bp": to_bp,
                    "nm": feat["properties"]["distance_nm"],
                }
            )
        report["markets"][mkey] = m_stats

    save_routes(dc / "ROUTES.json", routes)
    out = ROOT / "grok-routing-output/route-kept-markets-report.json"
    save_json(out, report)
    print(f"kept markets: synth={len(report['synthesized'])} skip={len(report['skipped'])}")
    for mk, st in report["markets"].items():
        print(f"  {mk}: +{st['synth']} skip={st['skip']}")
    print(f"report: {out}")


if __name__ == "__main__":
    main()