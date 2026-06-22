#!/usr/bin/env python3
"""Route Thailand Bucket-C connected-city BP↔BP corridors + land-crossing gate."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
from bucketB_shared import (  # noqa: E402
    LAND_THRESH_KM,
    build_bp_index,
    build_city_index,
    city_display,
    densify,
    hav_nm,
    interior_land_km,
    load_json,
    load_land_mask,
    route_features,
    route_id_of,
    save_json,
    save_routes,
    platform_for,
    edge_class_for,
    trip_scope_for,
)

# (report_city, from_bp, to_bp, optional_waypoints[(lon,lat),...])
SIGNATURE_ROUTES = [
    # Gulf inter-island mesh
    ("koh-samui-thailand", "bp-bangrak-pier", "bp-thong-sala-pier", None),
    ("koh-samui-thailand", "bp-maenam-pier", "bp-thong-sala-pier", None),
    ("koh-samui-thailand", "bp-bangrak-pier", "bp-mae-haad-pier", [(100.02, 9.82)]),
    ("koh-phangan-thailand", "bp-thong-sala-pier", "bp-mae-haad-pier", [(100.01, 9.89)]),
    ("koh-phangan-thailand", "bp-thong-sala-pier", "bp-haad-rin-pier", None),
    # Pattaya ↔ Koh Larn
    ("pattaya-thailand", "bp-bali-hai-pier", "bp-koh-larn-na-ban-pier", None),
    ("pattaya-thailand", "bp-ocean-marina-yacht-club", "bp-bali-hai-pier", [(100.875, 12.875)]),
    # Koh Chang intra
    ("koh-chang-thailand", "bp-ao-sapparot-pier", "bp-bang-bao-pier", None),
    # Krabi river + peninsula water-only hops
    ("krabi-thailand", "bp-khong-kha-pier", "bp-klong-jilad-pier", [(98.9195, 8.052)]),
    ("krabi-thailand", "bp-klong-jilad-pier", "bp-ao-nang-pier", [(98.865, 8.038)]),
    ("krabi-thailand", "bp-ao-nang-pier", "bp-railay-east-pier", [(98.828, 8.018)]),
    # Phi Phi intra
    ("koh-phi-phi-thailand", "bp-tonsai-pier", "bp-laem-tong-pier", None),
    # Andaman cross-cluster (Krabi ↔ Phi Phi)
    ("krabi-thailand", "bp-klong-jilad-pier", "bp-tonsai-pier", [(98.75, 7.85)]),
]


def mint_route_id(from_id: str, to_id: str) -> str:
    seed = f"bucketC-thailand|{from_id}|{to_id}"
    return "rn-" + hashlib.md5(seed.encode()).hexdigest()[:12]


def endpoint_meta(endpoint: str, bp_idx: dict, cities: dict):
    row = bp_idx[endpoint]
    return endpoint, row["name"], row["coords"], row["parent_city_id"]


def build_path(a, b, waypoints):
    pts = [a]
    if waypoints:
        pts.extend(waypoints)
    pts.append(b)
    coords = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 12)
        coords.extend(seg if not coords else seg[1:])
    return coords


def make_route(from_id, to_id, from_name, to_name, from_city, to_city, coords, dist_nm, land_km, cities):
    rid = mint_route_id(from_id, to_id)
    fc = city_display(from_city, cities)
    tc = city_display(to_city, cities)
    label = f"{from_name} → {to_name}"
    city_label = f"{fc} → {tc}" if from_city and to_city and from_city != to_city else (
        f"{fc}: {label}" if from_city else label
    )
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": platform_for(dist_nm),
            "distance_nm": round(dist_nm, 1),
            "edge_class": edge_class_for(from_city, to_city, dist_nm),
            "from": from_id,
            "to": to_id,
            "from_label": from_name,
            "to_label": to_name,
            "from_city": fc,
            "to_city": tc,
            "from_city_id": from_city,
            "to_city_id": to_city,
            "label": city_label,
            "trip_purpose": trip_scope_for(from_city, to_city),
            "traffic_weight": 0.55,
            "_bucketC_thailand": True,
            "_land_km_interior": round(land_km, 4),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(ROOT))
    args = ap.parse_args()

    dc = Path(args.repo) / "data-clean"
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()

    existing_ids = {route_id_of(r) for r in routes}
    report = {"phase": "bucketC_thailand_route", "synthesized": [], "skipped": [], "land_flagged": [], "errors": []}
    new_routes = []

    for entry in SIGNATURE_ROUTES:
        city_scope, from_ep, to_ep = entry[0], entry[1], entry[2]
        waypoints = entry[3] if len(entry) > 3 else None
        if from_ep not in bp_idx or to_ep not in bp_idx:
            report["errors"].append({"pair": [from_ep, to_ep], "error": "bp_not_sealed"})
            continue
        a = bp_idx[from_ep]["coords"]
        b = bp_idx[to_ep]["coords"]
        _, from_name, _, from_city = endpoint_meta(from_ep, bp_idx, cities)
        _, to_name, _, to_city = endpoint_meta(to_ep, bp_idx, cities)
        coords = build_path(a, b, waypoints)
        land_km = interior_land_km(coords, mask)
        dist_nm = hav_nm(a, b)
        rid = mint_route_id(from_ep, to_ep)
        if rid in existing_ids:
            report["skipped"].append({"route_id": rid, "reason": "already_exists"})
            continue
        feat = make_route(from_ep, to_ep, from_name, to_name, from_city, to_city, coords, dist_nm, land_km, cities)
        if land_km > LAND_THRESH_KM:
            feat["properties"]["_qa_land_flag"] = True
            report["land_flagged"].append({"route_id": rid, "land_km": land_km, "pair": [from_ep, to_ep]})
        new_routes.append(feat)
        report["synthesized"].append({
            "route_id": rid, "from": from_ep, "to": to_ep,
            "city": city_scope, "land_km": round(land_km, 4), "distance_nm": round(dist_nm, 1),
        })

    routes.extend(new_routes)
    save_routes(dc / "ROUTES.json", routes)

    allow_path = dc / "route_water_allowlist.json"
    allow = load_json(allow_path)
    ids = list(allow.get("ids", []))
    seen = set(ids)
    added = []
    for row in report["land_flagged"]:
        rid = row["route_id"]
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
            added.append(rid)
    allow["ids"] = ids
    meta = allow.setdefault("_meta", {})
    meta["bucketC_thailand_applied_at"] = datetime.now(timezone.utc).isoformat()
    meta["bucketC_thailand_allowlist_added"] = added
    save_json(allow_path, allow)

    out = ROOT / "grok-routing-output/grab-thailand-route-report.json"
    report["acceptance"] = {
        "routes_built": len(report["synthesized"]),
        "land_crossings": len(report["land_flagged"]),
        "errors": len(report["errors"]),
        "zero_errors": len(report["errors"]) == 0,
    }
    save_json(out, report)
    print(
        f"bucketC-thailand route: synthesized={len(report['synthesized'])} "
        f"land_flagged={len(report['land_flagged'])} errors={len(report['errors'])}"
    )
    if report["errors"]:
        for e in report["errors"]:
            print(f"  error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"report: {out}")


if __name__ == "__main__":
    main()