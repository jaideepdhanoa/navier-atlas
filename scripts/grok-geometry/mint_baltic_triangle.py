#!/usr/bin/env python3
"""Mint Nordic-Baltic triangle cross-border routes: Tallinn↔Helsinki, Helsinki↔Stockholm."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bucketB_shared import hav_nm, interior_land_km, load_land_mask  # noqa: E402
from bolt_yango_routing_shared import (  # noqa: E402
    build_coastal_path,
    load_json,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

TAG = "baltic_triangle"
REPORT_PATH = ROOT / "grok-routing-output/baltic-triangle-seal-report.json"
CORRIDORS_PATH = ROOT / "finance/model/corridors.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
BOLT_PATH = ROOT / "data-clean/partners/bolt.json"
BOLT_PITCH = ROOT / "partner-pitch/partners/bolt.json"

# Pier-exact seeds (lng, lat)
ENDPOINTS = {
    "tallinn-estonia": [24.7647, 59.4431],  # Old City Harbour (Vanasadam)
    "helsinki-finland": [24.9214, 60.1695],  # West Harbour (Lansisatama)
    "stockholm-sweden": [18.1042, 59.3201],  # Varta Terminal
}

ROUTES = [
    {
        "from": "tallinn-estonia",
        "to": "helsinki-finland",
        "platform": "Pioneer II",
        "wps": [(25.0, 59.75), (25.1, 59.95)],
        "trip_scope": "cross_border",
    },
    {
        "from": "helsinki-finland",
        "to": "stockholm-sweden",
        "platform": "Quanta-LR",
        "wps": [(22.0, 59.8), (20.5, 59.5), (19.0, 59.35)],
        "trip_scope": "cross_border",
    },
]

CORRIDOR_FIXES = [
    ("bolt-estonia", "Tallinn", "Helsinki", "helsinki-finland"),
    ("bolt-estonia", "Tallinn", "Stockholm", "stockholm-sweden"),
    ("bolt-finland", "Helsinki", "Tallinn", "tallinn-estonia"),
    ("bolt-finland", "Helsinki", "Stockholm", "stockholm-sweden"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fix_corridor_node_ids(corridors: dict) -> list[dict]:
    actions = []
    markets = corridors.get("markets") or {}
    for mkey, from_city, to_city, to_node in CORRIDOR_FIXES:
        mval = markets.get(mkey)
        if not mval:
            continue
        for corr in mval.get("corridors") or []:
            if corr.get("from") == from_city and corr.get("to") == to_city:
                old = corr.get("to_node_id")
                if old != to_node:
                    corr["to_node_id"] = to_node
                    actions.append({"market": mkey, "corridor": f"{from_city}->{to_city}", "to_node_id": to_node})
    return actions


def bind_bolt_journeys(bolt: dict, route_by_pair: dict) -> dict:
    stats = {"bound": 0, "still_pending": 0}
    pairs = {
        ("tallinn-estonia", "helsinki-finland"),
        ("helsinki-finland", "stockholm-sweden"),
    }

    def bind_j(j: dict) -> None:
        fc = j.get("from_node_id")
        tc = j.get("to_node_id")
        from_lbl = (j.get("from") or j.get("from_label") or "").lower()
        to_lbl = (j.get("to") or j.get("to_label") or "").lower()
        if fc == "tallinn-estonia" and "helsinki" in to_lbl:
            tc = "helsinki-finland"
            j["to_node_id"] = tc
        elif fc == "helsinki-finland" and "stockholm" in to_lbl:
            tc = "stockholm-sweden"
            j["to_node_id"] = tc
        elif fc == "helsinki-finland" and "tallinn" in to_lbl:
            tc = "tallinn-estonia"
            j["to_node_id"] = tc
        elif fc == "tallinn-estonia" and "stockholm" in to_lbl:
            tc = "stockholm-sweden"
            j["to_node_id"] = tc
        if (fc, tc) not in pairs and (tc, fc) not in pairs:
            return
        rid = route_by_pair.get((fc, tc)) or route_by_pair.get((tc, fc))
        if rid:
            j["route_id"] = rid
            j["_link_status"] = "linked-grok-scoped"
            j["_link_source"] = f"grok/{TAG}"
            j.pop("display", None)
            stats["bound"] += 1
        else:
            stats["still_pending"] += 1

    for market in bolt.get("markets", []):
        for j in market.get("journeys_unlocked", []):
            bind_j(j)
        for phase in market.get("phases", []):
            for fr in phase.get("featured_routes", []):
                bind_j(fr)

    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        ap.error("pass --apply or --dry-run")

    corridors = load_json(CORRIDORS_PATH)
    routes = route_features(load_json(ROUTES_PATH))
    bolt = load_json(BOLT_PATH)
    mask = load_land_mask()

    report = {
        "at": now_iso(),
        "lane": f"grok/{TAG}",
        "apply": args.apply,
        "corridor_fixes": fix_corridor_node_ids(corridors),
        "routes_built": [],
    }

    route_by_pair: dict[tuple[str, str], str] = {}
    existing = {(r.get("properties") or r).get("id") for r in routes}

    for spec in ROUTES:
        fc, tc = spec["from"], spec["to"]
        a, b = ENDPOINTS[fc], ENDPOINTS[tc]
        coords = build_coastal_path(tuple(a), tuple(b), mask, spec.get("wps"))
        dist = hav_nm(a, b)
        land_km = interior_land_km(coords, mask)
        rid = mint_route_id(fc, tc, TAG)
        if rid in existing:
            rid = mint_route_id(fc, tc, f"{TAG}|{len(routes)}")
        feat = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "id": rid,
                "platform": spec["platform"],
                "distance_nm": round(dist, 1),
                "edge_class": "inter-city",
                "from": fc,
                "to": tc,
                "from_city_id": fc,
                "to_city_id": tc,
                "from_label": fc.split("-")[0].title(),
                "to_label": tc.split("-")[0].title(),
                "label": f"{fc} → {tc}",
                "trip_scope": spec.get("trip_scope", "cross_border"),
                "traffic_weight": 0.72 if fc == "tallinn-estonia" and tc == "helsinki-finland" else 0.55,
                "interior_land_km": round(land_km, 4),
                f"_{TAG}_applied_at": now_iso(),
                "_geometry_status": "sealed" if land_km <= 2.0 else "pending_channel_authorship",
            },
        }
        routes.append(feat)
        existing.add(rid)
        route_by_pair[(fc, tc)] = rid
        report["routes_built"].append({
            "from": fc, "to": tc, "route_id": rid,
            "distance_nm": round(dist, 1), "platform": spec["platform"],
            "land_km": round(land_km, 3),
        })

    report["journey_bind"] = bind_bolt_journeys(bolt, route_by_pair)

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        save_json(CORRIDORS_PATH, corridors)
        save_json(BOLT_PATH, bolt)
        shutil.copy2(BOLT_PATH, BOLT_PITCH)

    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))
    return 0 if report["journey_bind"]["still_pending"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())