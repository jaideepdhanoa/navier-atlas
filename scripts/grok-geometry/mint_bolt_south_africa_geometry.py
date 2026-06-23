#!/usr/bin/env python3
"""Mint Bolt South Africa Cape Town lagoon mesh from sealed boarding points."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    build_coastal_path,
    hav_nm,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)
from channel_solver import hand_waypoints_for, solve_hand, get_land_checker  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402

REPORT_PATH = ROOT / "grok-routing-output/bolt-south-africa-seal-report.json"
TAG = "bolt_south_africa"

# Primary lagoon mesh (V&A anchor)
MESH_CORRIDORS: list[tuple[str, str, str, str]] = [
    ("bp-41c1d22c88", "bp-c07f712484", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-41c1d22c88", "bp-6572ae8691", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-6572ae8691", "bp-17cbbdad38", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-41c1d22c88", "bp-5fa23ee16d", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-41c1d22c88", "bp-d327e6ccc7", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-c07f712484", "bp-97c63623ac", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-6572ae8691", "bp-0682568ae1", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-17cbbdad38", "bp-924f18dd1b", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-5fa23ee16d", "bp-706671bf99", "cape-town-south-africa", "cape-town-south-africa"),
    ("bp-41c1d22c88", "bp-92ac8746e3", "cape-town-south-africa", "cape-town-south-africa"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_geometry(from_bp: str, to_bp: str, a: tuple[float, float], b: tuple[float, float], mask, lc) -> tuple[list, float, bool]:
    wps = hand_waypoints_for(from_bp, to_bp)
    if wps:
        solved = solve_hand(lc, a, b, wps)
        if solved and solved.get("qa_pass"):
            return solved["geometry"], solved["interior_land_km"], True
    coords = build_coastal_path(a, b, mask, manual_waypoints=[(w[0], w[1]) for w in wps] if wps else None)
    ev = evaluate_route(coords)
    return coords, ev["interior_land_km"], ev["qa_pass"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dc", default="data-clean")
    args = ap.parse_args()

    dc = ROOT / args.dc
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    lc = get_land_checker()
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    report = {
        "at": utc_now(),
        "lane": f"grok/{TAG}",
        "apply": args.apply,
        "routes_built": [],
        "routes_skipped": [],
        "routes_culled": [],
    }

    for from_bp, to_bp, from_city, to_city in MESH_CORRIDORS:
        if from_bp not in bp_idx or to_bp not in bp_idx:
            report["routes_culled"].append({"from_bp": from_bp, "to_bp": to_bp, "reason": "bp_missing"})
            continue
        rid = mint_route_id(from_bp, to_bp, tag=TAG)
        if rid in existing:
            report["routes_skipped"].append({"route_id": rid, "reason": "exists"})
            continue
        a = bp_idx[from_bp]["coords"]
        b = bp_idx[to_bp]["coords"]
        coords, land_km, qa_pass = build_geometry(from_bp, to_bp, a, b, mask, lc)
        dist_nm = round(hav_nm(a, b), 1)
        feat = make_route_feature(
            from_bp, to_bp,
            bp_idx[from_bp]["name"], bp_idx[to_bp]["name"],
            from_city, to_city,
            coords, cities,
            source=TAG,
            land_km=land_km,
        )
        feat["properties"]["id"] = rid
        feat["properties"]["distance_nm"] = dist_nm
        feat["properties"]["_bolt_south_africa"] = True
        feat["properties"]["_geometry_land_km"] = round(land_km, 4)
        if not qa_pass:
            feat["properties"]["_qa_land_flag"] = True
        routes.append(feat)
        existing.add(rid)
        report["routes_built"].append({
            "route_id": rid,
            "from_bp": from_bp,
            "to_bp": to_bp,
            "distance_nm": dist_nm,
            "land_km": round(land_km, 3),
            "qa_pass": qa_pass,
        })

    save_json(REPORT_PATH, report)
    if args.apply and report["routes_built"]:
        save_routes(dc / "ROUTES.json", routes)

    print(json.dumps({k: v for k, v in report.items() if k != "routes_built"}, indent=2))
    print(f"built={len(report['routes_built'])} culled={len(report['routes_culled'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())