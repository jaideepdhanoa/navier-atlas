#!/usr/bin/env python3
"""Route Bucket B Tier 1+2 signature corridors + extend LB-242 allowlist."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from bucketB_shared import (
    LAND_THRESH_KM,
    build_bp_index,
    build_city_index,
    city_display,
    densify,
    edge_class_for,
    hav_nm,
    interior_land_km,
    load_json,
    load_land_mask,
    mint_route_id,
    platform_for,
    route_features,
    route_id_of,
    save_json,
    save_routes,
    trip_scope_for,
)

# Marquee / signature routes: (city_scope, from, to, optional_waypoints[(lon,lat),...])
SIGNATURE_ROUTES = [
    # Lisbon — Transtejo/Soflusa estuary (mid-channel waypoints on Tagus)
    ("lisbon-tagus-portugal", "bp-cais-do-sodre-lisbon", "bp-cacilhas-almada", [(-9.147, 38.696)]),
    ("lisbon-tagus-portugal", "bp-terreiro-do-paco-lisbon", "bp-barreiro", [(-9.055, 38.68)]),
    ("lisbon-tagus-portugal", "bp-cais-do-sodre-lisbon", "bp-seixal", [(-9.125, 38.673)]),
    ("lisbon-tagus-portugal", "bp-cais-do-sodre-lisbon", "bp-montijo", [(-9.05, 38.69), (-9.02, 38.7)]),
    ("lisbon-tagus-portugal", "bp-belem-lisbon", "bp-trafaria-porto-brandao", [(-9.22, 38.684)]),
    # Al Wakrah — coastal via Gulf (not over peninsula)
    ("al-wakrah-qatar", "doha-qatar", "bp-port-al-wakrah-marina", [(51.55, 25.28)]),
    ("al-wakrah-qatar", "bp-port-al-wakrah-marina", "bp-al-wakrah-dhow-harbour", None),
    # Abidjan — Ébrié lagoon (lagoon-center waypoints)
    ("abidjan-cote-divoire", "bp-gare-plateau-abidjan", "bp-gare-treichville-abidjan", [(-4.015, 5.314)]),
    ("abidjan-cote-divoire", "bp-gare-plateau-abidjan", "bp-gare-blockauss-abidjan", [(-4.012, 5.322)]),
    ("abidjan-cote-divoire", "bp-gare-plateau-abidjan", "bp-gare-abobo-doume-yopougon", [(-4.03, 5.32)]),
    # Dammam–Khobar — offshore Arabian Gulf waypoints
    ("dammam-khobar-ksa", "bp-dammam-corniche", "bp-alkhobar-corniche", [(50.17, 26.42)]),
    ("dammam-khobar-ksa", "bp-alkhobar-corniche", "bp-half-moon-bay-ksa", [(50.2, 26.18)]),
]

SKIP_LOW_CONFIDENCE_BPS = {"bp-dammam-marina-yacht", "bp-cocody-riviera-citrans"}


def endpoint_meta(endpoint: str, bp_idx: dict, cities: dict) -> tuple[str, str, tuple[float, float], str | None]:
    if endpoint in bp_idx:
        row = bp_idx[endpoint]
        return endpoint, row["name"], row["coords"], row["parent_city_id"]
    if endpoint in cities:
        # city node — use city pin coords from FEATURES
        return endpoint, cities[endpoint], None, endpoint
    raise KeyError(endpoint)


def resolve_coords(endpoint: str, bp_idx: dict, fbt: dict) -> tuple[float, float]:
    if endpoint in bp_idx:
        return bp_idx[endpoint]["coords"]
    for key in ("city", "priority_city"):
        for feat in fbt.get(key, []):
            props = feat.get("properties", feat)
            if props.get("id") == endpoint:
                c = feat["geometry"]["coordinates"]
                return (c[0], c[1])
    raise KeyError(endpoint)


def make_route(
    from_id: str,
    to_id: str,
    from_name: str,
    to_name: str,
    from_city: str | None,
    to_city: str | None,
    coords: list,
    dist_nm: float,
    land_km: float,
    cities: dict[str, str],
) -> dict:
    rid = mint_route_id(from_id, to_id)
    fc = city_display(from_city, cities)
    tc = city_display(to_city, cities)
    label = f"{from_name} → {to_name}"
    if from_city and to_city and from_city != to_city:
        city_label = f"{fc} → {tc}"
    elif from_city:
        city_label = f"{fc}: {label}"
    else:
        city_label = label

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
            "_bucketB": True,
            "_land_km_interior": round(land_km, 4),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()

    existing_ids = {route_id_of(r) for r in routes}
    report = {
        "phase": "route",
        "synthesized": [],
        "skipped": [],
        "allowlisted": [],
        "errors": [],
    }

    def build_path(a, b, waypoints):
        pts = [a]
        if waypoints:
            pts.extend(waypoints)
        pts.append(b)
        coords = []
        for i in range(len(pts) - 1):
            seg = densify(pts[i], pts[i + 1], 8)
            coords.extend(seg if not coords else seg[1:])
        return coords

    new_routes = []
    for entry in SIGNATURE_ROUTES:
        city_scope, from_ep, to_ep = entry[0], entry[1], entry[2]
        waypoints = entry[3] if len(entry) > 3 else None
        if from_ep in SKIP_LOW_CONFIDENCE_BPS or to_ep in SKIP_LOW_CONFIDENCE_BPS:
            report["skipped"].append({"pair": [from_ep, to_ep], "reason": "low_confidence_bp"})
            continue
        try:
            a = resolve_coords(from_ep, bp_idx, fbt)
            b = resolve_coords(to_ep, bp_idx, fbt)
            _, from_name, _, from_city = endpoint_meta(from_ep, bp_idx, cities)
            _, to_name, _, to_city = endpoint_meta(to_ep, bp_idx, cities)
        except KeyError as e:
            report["errors"].append({"pair": [from_ep, to_ep], "error": str(e)})
            continue

        coords = build_path(a, b, waypoints)
        land_km = interior_land_km(coords, mask)
        dist_nm = hav_nm(a, b)
        rid = mint_route_id(from_ep, to_ep)
        if rid in existing_ids:
            report["skipped"].append({"route_id": rid, "reason": "already_exists"})
            continue

        feat = make_route(
            from_ep, to_ep, from_name, to_name, from_city, to_city, coords, dist_nm, land_km, cities
        )
        if land_km > LAND_THRESH_KM:
            feat["properties"]["_qa_land_flag"] = True
            report["allowlisted"].append({"route_id": rid, "land_km": land_km})

        new_routes.append(feat)
        report["synthesized"].append(
            {"route_id": rid, "from": from_ep, "to": to_ep, "city": city_scope, "land_km": land_km}
        )

    routes.extend(new_routes)
    save_routes(dc / "ROUTES.json", routes)

    allow_path = dc / "route_water_allowlist.json"
    allow = load_json(allow_path)
    ids = list(allow.get("ids", []))
    seen = set(ids)
    added = []
    for row in report["allowlisted"]:
        rid = row["route_id"]
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
            added.append(rid)
    allow["ids"] = ids
    meta = allow.setdefault("_meta", {})
    meta["bucketB_applied_at"] = datetime.now(timezone.utc).isoformat()
    meta["bucketB_allowlist_added"] = added
    save_json(allow_path, allow)

    out = work / "grok-routing-output" / "bucketB-route-report.json"
    save_json(out, report)

    print(
        f"bucketB route: synthesized={len(report['synthesized'])} "
        f"skipped={len(report['skipped'])} allowlisted={len(added)} errors={len(report['errors'])}"
    )
    if report["errors"]:
        for e in report["errors"]:
            print(f"  error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"report: {out}")


if __name__ == "__main__":
    main()