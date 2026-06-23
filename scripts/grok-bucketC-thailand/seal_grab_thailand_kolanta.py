#!/usr/bin/env python3
"""Grok seal — Grab Thailand Ko Lanta Andaman addition (PR #89 kolanta pass)."""
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

from bucketB_shared import densify, hav_nm, interior_land_km, load_land_mask  # noqa: E402
from bolt_yango_routing_shared import (  # noqa: E402
    build_coastal_path,
    load_json,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

KOLANTA = ROOT / "partner-pitch/proposals/grab-thailand/kolanta-2026-06-23"
BP_FILE = KOLANTA / "boarding-points/koh-lanta-thailand.json"
PARTNER_SRC = ROOT / "partner-pitch/partners/grab-thailand.json"
PARTNER_DST = ROOT / "data-clean/partners/grab-thailand.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean/CLUSTERS.json"
REPORT_PATH = ROOT / "grok-routing-output/grab-thailand-kolanta-seal-report.json"
TAG = "grab_thailand_kolanta"
CITY_ID = "koh-lanta-thailand"

ROUTE_ENDPOINTS: dict[tuple[str, str], tuple[list[float], list[float]]] = {
    ("koh-lanta-thailand", "koh-phi-phi-thailand"): (
        [99.041, 7.6386],
        [98.778, 7.7405],
    ),
    ("koh-lanta-thailand", "krabi-thailand"): (
        [99.041, 7.6386],
        [98.965, 8.086],
    ),
    ("phuket-phang-nga-thailand", "koh-lanta-thailand"): (
        [98.354, 7.828],
        [99.041, 7.6386],
    ),
}

KOLANTA_ROUTES = [
    ("koh-lanta-thailand", "koh-phi-phi-thailand", [(98.91, 7.69)]),
    ("koh-lanta-thailand", "krabi-thailand", [(99.0, 7.86)]),
    ("phuket-phang-nga-thailand", "koh-lanta-thailand", [(98.7, 7.75), (98.85, 7.68)]),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_city(coords: list[float]) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": coords},
        "properties": {
            "id": CITY_ID,
            "type": "city",
            "name": "Ko Lanta",
            "shortName": "Ko Lanta",
            "fullName": "Ko Lanta",
            "country": "Thailand",
            "region": "SEA",
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "grab_thailand_kolanta_seal_2026-06-23",
            "confidence": "medium",
            "status": "operational",
            f"_{TAG}_applied_at": now_iso(),
        },
    }


def make_poi(bp: dict) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [bp["lng"], bp["lat"]]},
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "name": bp["name"],
            "shortName": bp["name"].split("(")[0].strip(),
            "parent_city_id": CITY_ID,
            "bp_type": bp.get("type", "pier"),
            "coords_resolved": True,
            "confidence": bp.get("confidence", "med"),
            "precision": bp.get("precision", "curated_seed"),
            "_gazetteer_source": f"grab_thailand_kolanta:{bp['id']}",
            f"_{TAG}_applied_at": now_iso(),
            "status": "operational",
        },
    }


def route_id_of(feat: dict) -> str:
    return (feat.get("properties") or feat).get("id", "")


def bind_partner(partner: dict, route_by_pair: dict) -> dict:
    stats = {"bound": 0, "still_pending": 0}
    for market in partner.get("markets", []):
        for j in market.get("journeys_unlocked", []):
            if j.get("_link_status") != "pending-seal-thailand-kolanta":
                continue
            fc, tc = j.get("from_node_id"), j.get("to_node_id")
            rid = route_by_pair.get((fc, tc)) or route_by_pair.get((tc, fc))
            if rid:
                j["route_id"] = rid
                j["_link_status"] = "linked-grok-scoped"
                j["_link_source"] = f"grok/{TAG}"
                stats["bound"] += 1
            else:
                stats["still_pending"] += 1
    mesh = partner.setdefault("connected_city_mesh", [])
    for j in mesh:
        if j.get("_link_status") != "pending-seal-thailand-kolanta":
            continue
        fc, tc = j.get("from_node_id"), j.get("to_node_id")
        rid = route_by_pair.get((fc, tc)) or route_by_pair.get((tc, fc))
        if rid:
            j["route_id"] = rid
            j["_link_status"] = "linked-grok-scoped"
            j["_link_source"] = f"grok/{TAG}"
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        ap.error("pass --apply or --dry-run")

    fbt = load_json(FBT_PATH)
    routes = route_features(load_json(ROUTES_PATH))
    partner = load_json(PARTNER_SRC)
    clusters = load_json(CLUSTERS_PATH)
    mask = load_land_mask()
    bp_data = json.loads(BP_FILE.read_text())

    report = {"at": now_iso(), "lane": f"grok/{TAG}", "apply": args.apply, "bps_sealed": [], "routes_built": []}

    existing_city = {f["properties"]["id"] for f in fbt.get("city", [])}
    anchor = bp_data.get("city_anchor", [99.041, 7.6386])
    if CITY_ID not in existing_city:
        fbt.setdefault("city", []).append(make_city(anchor))

    poi_by_id = {p["properties"]["id"]: p for p in fbt.get("poi", [])}
    for bp in bp_data.get("boarding_points", []):
        bid = bp.get("id")
        if not bid:
            continue
        poi_by_id[bid] = make_poi(bp)
        report["bps_sealed"].append(bid)
    fbt["poi"] = list(poi_by_id.values())

    route_by_pair: dict[tuple[str, str], str] = {}
    existing_ids = {route_id_of(r) for r in routes}

    for fc, tc, wps in KOLANTA_ROUTES:
        ep = ROUTE_ENDPOINTS[(fc, tc)]
        coords = build_coastal_path(tuple(ep[0]), tuple(ep[1]), mask, wps)
        dist = hav_nm(ep[0], ep[1])
        land_km = interior_land_km(coords, mask)
        rid = mint_route_id(fc, tc, TAG)
        if rid in existing_ids:
            rid = mint_route_id(fc, tc, f"{TAG}|{len(routes)}")
        feat = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "id": rid,
                "platform": "Pioneer II",
                "distance_nm": round(dist, 1),
                "edge_class": "inter-city",
                "from": f"{fc}__{fc.split('-')[0]}",
                "to": f"{tc}__{tc.split('-')[0]}",
                "from_city_id": fc,
                "to_city_id": tc,
                "label": f"{fc} → {tc}",
                "traffic_weight": 0.65,
                "interior_land_km": round(land_km, 4),
                f"_{TAG}_applied_at": now_iso(),
                "_geometry_status": "sealed" if land_km <= 2.0 else "pending_channel_authorship",
            },
        }
        routes.append(feat)
        existing_ids.add(rid)
        route_by_pair[(fc, tc)] = rid
        report["routes_built"].append({"from": fc, "to": tc, "route_id": rid, "land_km": round(land_km, 3)})

    report["journey_bind"] = bind_partner(partner, route_by_pair)

    for c in clusters.get("clusters", []):
        if c.get("cluster_id") in ("thailand", "thailand_andaman"):
            members = set(c.get("member_city_ids") or c.get("city_ids") or [])
            members.add(CITY_ID)
            c["member_city_ids"] = sorted(members)
            if "city_ids" in c:
                c["city_ids"] = sorted(members)

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        save_json(FBT_PATH, fbt)
        save_json(CLUSTERS_PATH, clusters)
        save_json(PARTNER_SRC, partner)
        shutil.copy2(PARTNER_SRC, PARTNER_DST)

    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))
    return 0 if report["journey_bind"]["still_pending"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())