#!/usr/bin/env python3
"""
Mint full intra-city boarding-point mesh routes (all BP pairs within a city).

Shared lane step — NOT Bolt/Yango exclusive. Used by:
  - scripts/grok-bolt-yango/route_bolt_yango_markets.py (all POIs in anchor cities)
  - scripts/run-abc-islands-seal-lane.sh (canonical ABC node endpoints)
  - future seal lanes (see handoff/MESH-BACKLOG.md)

Contract:
  - Skip pairs that already exist (by mint_route_id).
  - Coastal / offshore-aware geometry (never straight chords over land when avoidable).
  - Routes failing land QA are still minted with _qa_land_flag (allowlist at deploy).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from abc_offshore_waypoints import build_offshore_coords, manual_waypoints  # noqa: E402
from bolt_yango_routing_shared import (  # noqa: E402
    BOLT_YANGO_ANCHORS,
    LAND_THRESH_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    hav_nm,
    interior_land_km,
    load_json,
    load_land_mask,
    mint_route_id,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from route_land_qa import interior_land_km as qa_interior_land_km  # noqa: E402

# Cities that always get a full mesh pass when this script runs without --cities.
DEFAULT_MESH_CITIES: dict[str, dict] = {
    "curacao-curacao": {
        "tag": "abc_islands",
        "endpoint_mode": "canonical_nodes",
        "max_nm": 40,
        "max_pairs": 64,
        "land_thresh_km": 0.08,
        "traffic_weight": 0.35,
    },
    "aruba-aruba": {
        "tag": "abc_islands",
        "endpoint_mode": "canonical_nodes",
        "max_nm": 40,
        "max_pairs": 40,
        "land_thresh_km": 0.08,
        "traffic_weight": 0.35,
    },
    "bonaire-bonaire": {
        "tag": "abc_islands",
        "endpoint_mode": "canonical_nodes",
        "max_nm": 40,
        "max_pairs": 40,
        "land_thresh_km": 0.08,
        "traffic_weight": 0.35,
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_node_ids(city_id: str) -> set[str]:
    """ABC sealed nodes: parent_city__suffix (from mint_abc_islands_geometry BP_DEFS)."""
    return {pid for pid, row in _BP_INDEX_CACHE.items() if row.get("parent_city_id") == city_id and "__" in pid}


_BP_INDEX_CACHE: dict = {}


def endpoints_for_city(city_id: str, bp_idx: dict, mode: str) -> list[str]:
    if mode == "canonical_nodes":
        return sorted(pid for pid, row in bp_idx.items() if row.get("parent_city_id") == city_id and "__" in pid)
    if mode == "all_pois":
        return sorted(pid for pid, row in bp_idx.items() if row.get("parent_city_id") == city_id)
    raise ValueError(f"unknown endpoint_mode: {mode}")


def build_mesh_coords(
    from_id: str,
    to_id: str,
    a: tuple[float, float],
    b: tuple[float, float],
    mask,
) -> tuple[list, float]:
    manual = manual_waypoints(from_id, to_id)
    if manual is not None:
        coords = build_offshore_coords(a, b, manual)
        land_km = qa_interior_land_km(coords, apron_km=0.25)
        if land_km <= 0.08:
            return coords, land_km
    coords = build_coastal_path(a, b, mask, manual_waypoints=manual)
    land_km = interior_land_km(coords, mask)
    if land_km > LAND_THRESH_KM and manual:
        coords = build_offshore_coords(a, b, manual)
        land_km = qa_interior_land_km(coords, apron_km=0.25)
    return coords, land_km


def make_mesh_feature(
    from_id: str,
    to_id: str,
    from_row: dict,
    to_row: dict,
    city_id: str,
    coords: list,
    land_km: float,
    *,
    tag: str,
    cities: dict,
    traffic_weight: float,
    source: str,
) -> dict:
    from_name = from_row.get("name") or from_id
    to_name = to_row.get("name") or to_id
    dist_nm = round(hav_nm(from_row["coords"], to_row["coords"]), 1)
    rid = mint_route_id(from_id, to_id, tag)
    offshore = manual_waypoints(from_id, to_id) is not None
    props = {
        "id": rid,
        "platform": "Pioneer II",
        "distance_nm": dist_nm,
        "edge_class": "intra-city",
        "from": from_id,
        "to": to_id,
        "from_node": from_id,
        "to_node": to_id,
        "from_label": from_name,
        "to_label": to_name,
        "from_city": city_id,
        "to_city": city_id,
        "from_city_id": city_id,
        "to_city_id": city_id,
        "label": f"{from_name} → {to_name}",
        "trip_scope": "intra_island",
        "traffic_weight": traffic_weight,
        "interior_land_km": round(land_km, 4),
        "_mesh": True,
        "_mesh_source": source,
        "_mesh_at": utc_now(),
        "_geometry_status": "sealed",
    }
    if offshore:
        props["render_smooth"] = False
        props["render_no_bundle"] = True
        props["_abc_offshore_mesh"] = True
    if land_km > LAND_THRESH_KM:
        props["_qa_land_flag"] = True
    return {"type": "Feature", "geometry": {"type": "LineString", "coordinates": coords}, "properties": props}


def mint_mesh_for_cities(
    routes: list,
    fbt: dict,
    *,
    city_configs: dict[str, dict],
    source: str,
    extra_cities: list[str] | None = None,
) -> dict:
    bp_idx = build_bp_index(fbt)
    global _BP_INDEX_CACHE
    _BP_INDEX_CACHE = bp_idx
    cities = build_city_index(fbt)
    mask = load_land_mask()
    existing_ids = {route_id_of(r) for r in routes}
    existing_pairs: set[tuple[str, str]] = set()
    for feat in routes:
        p = feat.get("properties", feat)
        fn = p.get("from_node") or p.get("from")
        tn = p.get("to_node") or p.get("to")
        if fn and tn:
            existing_pairs.add((fn, tn))
            existing_pairs.add((tn, fn))

    report = {"source": source, "cities": {}, "synthesized": [], "skipped": [], "allowlisted": []}
    new_routes: list = []

    city_list = sorted(set(city_configs) | set(extra_cities or []))
    for city_id in city_list:
        cfg = city_configs.get(city_id, {})
        if not cfg and city_id in BOLT_YANGO_ANCHORS:
            cfg = {
                "tag": "boltyango",
                "endpoint_mode": "all_pois",
                "max_nm": 40,
                "max_pairs": 40,
                "land_thresh_km": LAND_THRESH_KM,
                "traffic_weight": 0.28,
            }
        if not cfg:
            continue

        tag = cfg.get("tag", "mesh")
        mode = cfg.get("endpoint_mode", "all_pois")
        max_nm = float(cfg.get("max_nm", 40))
        max_pairs = int(cfg.get("max_pairs", 40))
        tw = float(cfg.get("traffic_weight", 0.28))

        endpoints = endpoints_for_city(city_id, bp_idx, mode)
        city_report = {"endpoints": len(endpoints), "added": 0, "skipped_existing": 0}
        pairs_done = 0

        for i, from_id in enumerate(endpoints):
            for to_id in endpoints[i + 1 :]:
                if pairs_done >= max_pairs:
                    break
                if (from_id, to_id) in existing_pairs:
                    city_report["skipped_existing"] += 1
                    report["skipped"].append({"city": city_id, "from": from_id, "to": to_id, "reason": "pair_exists"})
                    continue
                from_row = bp_idx[from_id]
                to_row = bp_idx[to_id]
                a, b = from_row["coords"], to_row["coords"]
                if hav_nm(a, b) > max_nm:
                    report["skipped"].append({"city": city_id, "from": from_id, "to": to_id, "reason": "distance"})
                    continue
                rid = mint_route_id(from_id, to_id, tag)
                if rid in existing_ids:
                    city_report["skipped_existing"] += 1
                    continue

                coords, land_km = build_mesh_coords(from_id, to_id, a, b, mask)
                feat = make_mesh_feature(
                    from_id,
                    to_id,
                    from_row,
                    to_row,
                    city_id,
                    coords,
                    land_km,
                    tag=tag,
                    cities=cities,
                    traffic_weight=tw,
                    source=source,
                )
                if land_km > cfg.get("land_thresh_km", LAND_THRESH_KM):
                    report["allowlisted"].append({"route_id": rid, "land_km": land_km, "city": city_id})

                new_routes.append(feat)
                existing_ids.add(rid)
                existing_pairs.add((from_id, to_id))
                existing_pairs.add((to_id, from_id))
                pairs_done += 1
                city_report["added"] += 1
                report["synthesized"].append(
                    {"route_id": rid, "city": city_id, "from": from_id, "to": to_id, "nm": feat["properties"]["distance_nm"], "land_km": land_km}
                )

        report["cities"][city_id] = city_report

    routes.extend(new_routes)
    report["mesh_added"] = len(new_routes)
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Mint intra-city BP mesh routes")
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument(
        "--cities",
        default="",
        help="Comma-separated city_ids (default: ABC trio + Bolt/Yango anchors)",
    )
    ap.add_argument("--abc-only", action="store_true", help="Only mesh curacao/aruba/bonaire canonical nodes")
    ap.add_argument("--boltyango-anchors", action="store_true", help="Also mesh Bolt/Yango anchor cities (all POIs)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))

    city_configs = dict(DEFAULT_MESH_CITIES)
    extra: list[str] = []

    if args.cities:
        for cid in args.cities.split(","):
            cid = cid.strip()
            if cid and cid not in city_configs:
                city_configs[cid] = {
                    "tag": "mesh",
                    "endpoint_mode": "all_pois",
                    "max_nm": 40,
                    "max_pairs": 40,
                    "land_thresh_km": LAND_THRESH_KM,
                    "traffic_weight": 0.28,
                }

    if args.abc_only:
        city_configs = {k: v for k, v in DEFAULT_MESH_CITIES.items() if k in args.cities.split(",") or not args.cities}
        if not args.cities:
            city_configs = dict(DEFAULT_MESH_CITIES)

    if args.boltyango_anchors or (not args.abc_only and not args.cities):
        for cid in BOLT_YANGO_ANCHORS:
            if cid not in city_configs:
                extra.append(cid)

    source = "grok/mint_intra_city_mesh"
    if args.abc_only:
        source = "grok/abc_islands_mesh"

    report = mint_mesh_for_cities(routes, fbt, city_configs=city_configs, source=source, extra_cities=extra)

    out = ROOT / "grok-routing-output" / "intra-city-mesh-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")

    if not args.dry_run:
        save_routes(dc / "ROUTES.json", routes)

    print(json.dumps({"mesh_added": report["mesh_added"], "cities": report["cities"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())