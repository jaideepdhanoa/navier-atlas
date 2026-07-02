#!/usr/bin/env python3
"""Mint Phase D greenfield seed cities + boarding points for Wave 2 authorities."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    LAND_THRESH_KM,
    build_city_index,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from channel_solver import get_land_checker, solve_hand  # noqa: E402
from mint_authority_city import register_cluster, route_geometry  # noqa: E402

HANDOFF = ROOT / "handoff/partner-map-model"
DC = ROOT / "data-clean"

# Shared kakao pier nodes (Seoul Hangang reconciliation)
KAKAO_SHARED_BPS = {
    "hangang-yeouido": {"bp_id": "bp-kakao-yeouido", "name": "Yeouido Hangang Park Pier", "anchor_lnglat": [126.924, 37.521]},
    "hangang-ttukseom": {"bp_id": "bp-kakao-ttukseom", "name": "Ttukseom Hangang Park Pier", "anchor_lnglat": [127.098, 37.529]},
    "hangang-jamsil": {"bp_id": "bp-kakao-jamsil", "name": "Jamsil Ttukseom Riverside Pier", "anchor_lnglat": [127.082, 37.513]},
}

PHASE_D_SPECS: dict[str, dict] = {
    "mersey-ferries": {
        "partner": "mersey-ferries",
        "city_id": "liverpool-mersey-uk",
        "name": "Liverpool — Mersey",
        "country": "United Kingdom",
        "region": "Europe",
        "cluster_id": "uk",
        "coordinates": [-3.0120, 53.4080],
        "boarding_points": [
            {"node": "mersey-pier-head", "name": "Gerry Marsden Terminal (Pier Head)", "anchor_lnglat": [-3.0065, 53.4048]},
            {"node": "mersey-seacombe", "name": "Seacombe Terminal (Wallasey)", "anchor_lnglat": [-3.0180, 53.4105]},
            {"node": "mersey-woodside", "name": "Woodside Ferry Terminal (Birkenhead)", "anchor_lnglat": [-3.0240, 53.3930]},
        ],
        "starter_pairs": [
            ("mersey-pier-head", "mersey-seacombe"),
            ("mersey-pier-head", "mersey-woodside"),
            ("mersey-seacombe", "mersey-woodside"),
        ],
    },
    "toronto-island-ferry": {
        "partner": "toronto-island-ferry",
        "city_id": "toronto-island-canada",
        "name": "Toronto Island",
        "country": "Canada",
        "region": "North America",
        "cluster_id": "great-lakes-usa",
        "coordinates": [-79.3775, 43.6300],
        "boarding_points": [
            {"node": "tor-jack-layton", "name": "Jack Layton Ferry Terminal", "anchor_lnglat": [-79.3745, 43.6395]},
            {"node": "tor-centre-island", "name": "Centre Island Dock", "anchor_lnglat": [-79.3640, 43.6200]},
            {"node": "tor-hanlans-point", "name": "Hanlan's Point Dock", "anchor_lnglat": [-79.4150, 43.6270]},
            {"node": "tor-wards-island", "name": "Ward's Island Dock", "anchor_lnglat": [-79.3500, 43.6300]},
        ],
        "starter_pairs": [
            ("tor-jack-layton", "tor-centre-island"),
            ("tor-jack-layton", "tor-hanlans-point"),
            ("tor-jack-layton", "tor-wards-island"),
        ],
    },
    "calmac": {
        "partner": "calmac",
        "city_id": "firth-of-clyde-scotland",
        "name": "Firth of Clyde",
        "country": "Scotland",
        "region": "Europe",
        "cluster_id": "uk",
        "coordinates": [-4.9500, 55.7000],
        "boarding_points": [
            {"node": "cal-ardrossan", "name": "Ardrossan Harbour", "anchor_lnglat": [-4.8400, 55.6410]},
            {"node": "cal-brodick", "name": "Brodick (Isle of Arran)", "anchor_lnglat": [-5.1380, 55.5770]},
            {"node": "cal-wemyss-bay", "name": "Wemyss Bay", "anchor_lnglat": [-4.8880, 55.8760]},
            {"node": "cal-rothesay", "name": "Rothesay (Isle of Bute)", "anchor_lnglat": [-5.0570, 55.8360]},
            {"node": "cal-gourock", "name": "Gourock", "anchor_lnglat": [-4.8150, 55.9610]},
            {"node": "cal-dunoon", "name": "Dunoon (Cowal)", "anchor_lnglat": [-4.9230, 55.9510]},
        ],
        "starter_pairs": [
            ("cal-ardrossan", "cal-brodick"),
            ("cal-wemyss-bay", "cal-rothesay"),
            ("cal-gourock", "cal-dunoon"),
        ],
    },
    "seoul-hangang-bus": {
        "partner": "seoul-hangang-bus",
        "city_id": "seoul-incheon-korea",
        "reuse_city": True,
        "cluster_id": "korea",
        "boarding_points": [
            {"node": "hangang-magok", "name": "Magok Pier", "anchor_lnglat": [126.827, 37.566]},
            {"node": "hangang-mangwon", "name": "Mangwon Pier", "anchor_lnglat": [126.895, 37.545]},
            {"node": "hangang-yeouido", "name": "Yeouido Pier", "bp_id": "bp-kakao-yeouido", "anchor_lnglat": [126.924, 37.521]},
            {"node": "hangang-oksu", "name": "Oksu Pier", "anchor_lnglat": [127.022, 37.545]},
            {"node": "hangang-apgujeong", "name": "Apgujeong Pier", "anchor_lnglat": [127.058, 37.530]},
            {"node": "hangang-ttukseom", "name": "Ttukseom Pier", "bp_id": "bp-kakao-ttukseom", "anchor_lnglat": [127.098, 37.529]},
            {"node": "hangang-jamsil", "name": "Jamsil Pier", "bp_id": "bp-kakao-jamsil", "anchor_lnglat": [127.082, 37.513]},
        ],
        "starter_pairs": [
            ("hangang-jamsil", "hangang-yeouido"),
            ("hangang-magok", "hangang-yeouido"),
            ("hangang-yeouido", "hangang-ttukseom"),
            ("hangang-magok", "hangang-jamsil"),
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bp_id_for(node: str, city_id: str) -> str:
    h = hashlib.md5(f"pta-mint|{city_id}|{node}".encode()).hexdigest()[:10]
    return f"bp-{h}"


def mint_bp_poi(bp: dict, city_id: str, fbt: dict) -> str:
    node = bp["node"]
    pid = bp.get("bp_id") or bp_id_for(node, city_id)
    pois = fbt.setdefault("poi", [])
    for poi in pois:
        props = poi.get("properties", poi)
        if props.get("id") == pid or props.get("_pta_node") == node:
            return pid
    lng, lat = bp["anchor_lnglat"]
    name = bp["name"]
    feat = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": pid,
            "type": "poi",
            "name": name,
            "shortName": name[:40],
            "fullName": name,
            "parent_city_id": city_id,
            "bp_type": "ferry_terminal",
            "bp_type_label": "Ferry Terminal",
            "status": "operational",
            "confidence": "high",
            "_pta_node": node,
            "_pta_mint_city": city_id,
            "_pta_minted_at": utc_now(),
        },
    }
    pois.append(feat)
    return pid


def mint_city_feature(city_id: str, spec: dict) -> dict:
    lng, lat = spec["coordinates"]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": city_id,
            "type": "priority_city",
            "name": spec["name"],
            "shortName": spec["name"],
            "fullName": spec["name"],
            "country": spec["country"],
            "region": spec["region"],
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "pta_mint_phase_d",
            "confidence": "high",
            "status": "operational",
            "tier_sort_key": 2,
            "cluster_id": spec["cluster_id"],
            "_seed_node": True,
            "_link_status": "geometry_seal_pending",
            "_pta_minted_at": utc_now(),
        },
    }


def mint_partner(slug: str, apply: bool) -> dict:
    spec = PHASE_D_SPECS[slug]
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(DC / "ROUTES.json")
    routes = route_features(routes_raw)
    existing = {route_id_of(r) for r in routes}

    city_id = spec["city_id"]
    if not spec.get("reuse_city"):
        cities_bucket = fbt.setdefault("priority_city", [])
        if not any((c.get("properties", c).get("id") == city_id) for c in cities_bucket):
            cities_bucket.append(mint_city_feature(city_id, spec))

    mask = load_land_mask()
    lc = get_land_checker()
    cities = build_city_index(fbt)

    node_meta = {b["node"]: b for b in spec["boarding_points"]}
    node_to_bp: dict[str, str] = {}
    boarding_points_out = []

    for bp in spec["boarding_points"]:
        pid = mint_bp_poi(bp, city_id, fbt)
        node_to_bp[bp["node"]] = pid
        boarding_points_out.append(
            {
                "node": bp["node"],
                "bp_id": pid,
                "name": bp["name"],
                "anchor_lnglat": bp["anchor_lnglat"],
            }
        )

    sealed_routes = []
    failed = []
    anchor_bp = boarding_points_out[0]["bp_id"] if boarding_points_out else None
    tag = f"pta-{slug}"

    for fn, tn in spec["starter_pairs"]:
        from_bp = node_to_bp[fn]
        to_bp = node_to_bp[tn]
        rid = mint_route_id(from_bp, to_bp, tag=tag)
        if rid in existing:
            sealed_routes.append({"route_id": rid, "from_bp": from_bp, "to_bp": to_bp, "status": "existing"})
            continue
        a = tuple(node_meta[fn]["anchor_lnglat"])
        b = tuple(node_meta[tn]["anchor_lnglat"])
        geom = route_geometry(fn, tn, a, b, mask, lc)
        if not geom:
            failed.append({"from": fn, "to": tn, "reason": "land_crossing"})
            continue
        coords, land_km = geom
        feat = make_route_feature(
            from_bp,
            to_bp,
            node_meta[fn]["name"],
            node_meta[tn]["name"],
            city_id,
            city_id,
            coords,
            cities,
            source=f"pta_{slug}",
            land_km=land_km,
        )
        feat["properties"]["id"] = rid
        feat["properties"]["_pta_partner"] = slug
        feat["properties"]["_pta_node_from"] = fn
        feat["properties"]["_pta_node_to"] = tn
        routes.append(feat)
        existing.add(rid)
        sealed_routes.append(
            {
                "route_id": rid,
                "from_bp": from_bp,
                "to_bp": to_bp,
                "from_node": fn,
                "to_node": tn,
                "land_km": land_km,
            }
        )

    receipt = {
        "partner": slug,
        "generated_at": utc_now(),
        "city_feature_id": city_id,
        "boarding_points": boarding_points_out,
        "sealed_routes": sealed_routes,
        "routes_failed": failed,
        "generator": "scripts/pta/mint_phase_d.py",
    }

    if apply:
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)
        save_routes(DC / "ROUTES.json", routes)
        if not spec.get("reuse_city"):
            register_cluster(city_id, spec, anchor_bp)
        out = HANDOFF / f"GEOMETRY-MINT-RECEIPT-{slug}.json"
        out.write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"✓ minted {slug}: {len(boarding_points_out)} BPs, {len(sealed_routes)} routes → {out}")
    else:
        print(json.dumps(receipt, indent=2))
        print("(dry-run — pass --apply to write)")

    return receipt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", action="append", dest="partners")
    ap.add_argument("--all-wave2", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    targets = list(PHASE_D_SPECS.keys()) if args.all_wave2 else (args.partners or [])
    if not targets:
        ap.error("pass --partner <slug> or --all-wave2")

    failed_any = False
    for slug in targets:
        if slug not in PHASE_D_SPECS:
            print(f"✗ unknown partner: {slug}", file=sys.stderr)
            failed_any = True
            continue
        r = mint_partner(slug, args.apply)
        if r.get("routes_failed"):
            failed_any = True
    return 2 if failed_any else 0


if __name__ == "__main__":
    raise SystemExit(main())