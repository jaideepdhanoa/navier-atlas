#!/usr/bin/env python3
"""
Route Bolt/Yango markets from corridors.json + signature BP pairs.
Geometry uses seaward mid-channel waypoints (not straight chords over land).
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from bolt_yango_routing_shared import (
    BOLT_YANGO_ANCHORS,
    LAND_THRESH_KM,
    NM_PER_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    hav_nm,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    path_length_km,
    resolve_corridor_endpoints,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)

ROOT = Path(__file__).resolve().parents[2]
INGEST = ROOT / "_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19"

# Manual mid-channel waypoints where auto-offset is insufficient
SIGNATURE_WAYPOINTS: dict[tuple[str, str], list[tuple[float, float]]] = {
    ("bp-cais-do-sodre-lisbon", "bp-cacilhas-almada"): [(-9.147, 38.696)],
    ("bp-terreiro-do-paco-lisbon", "bp-barreiro"): [(-9.055, 38.68)],
    ("bp-cais-do-sodre-lisbon", "bp-seixal"): [(-9.125, 38.673)],
    ("bp-belem-lisbon", "bp-trafaria-porto-brandao"): [(-9.22, 38.684)],
    ("bp-porto-ribeira", "bp-porto-gaia"): [(-8.612, 41.14)],
    ("bp-lagos-marina", "bp-ponta-da-piedade"): [(-8.671, 37.093)],
    ("bp-vila-real-santo-antonio", "bp-ayamonte-spain"): [(-7.41, 37.198)],
    ("bp-limassol-marina", "bp-larnaca-marina"): [(33.2, 34.85)],
    ("bp-dublin-port", "bp-dun-laoghaire-harbour"): [(-6.18, 53.32)],
    ("bp-dammam-corniche", "bp-alkhobar-corniche"): [(50.17, 26.42)],
}

BOLT_YANGO_MARKET_PREFIXES = ("bolt-", "yango-")


def partner_markets(corridors_doc: dict) -> dict[str, dict]:
    out = {}
    for key, val in (corridors_doc.get("markets") or {}).items():
        if any(key.startswith(p) for p in BOLT_YANGO_MARKET_PREFIXES):
            out[key] = val
    return out


def refresh_coastal_geometry(routes: list, mask, report: dict) -> int:
    """Re-densify routes that are straight chords or have high interior land crossing."""
    updated = 0
    for feat in routes:
        p = feat.get("properties", feat)
        coords = feat.get("geometry", {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        land_km = float(p.get("_land_km_interior") or 0)
        needs_refresh = (
            not p.get("_coastal_geometry")
            or land_km > LAND_THRESH_KM * 4
            or (len(coords) <= 24 and land_km > LAND_THRESH_KM)
        )
        if not needs_refresh:
            continue
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if fc not in BOLT_YANGO_ANCHORS and tc not in BOLT_YANGO_ANCHORS:
            continue
        a = (coords[0][0], coords[0][1])
        b = (coords[-1][0], coords[-1][1])
        pair = (p.get("from_node") or p.get("from"), p.get("to_node") or p.get("to"))
        manual = SIGNATURE_WAYPOINTS.get(pair) if pair[0] and pair[1] else None
        new_coords = build_coastal_path(a, b, mask, manual_waypoints=manual)
        land_km = interior_land_km(new_coords, mask)
        feat["geometry"]["coordinates"] = new_coords
        p["distance_nm"] = round(path_length_km(new_coords) * NM_PER_KM, 1)
        p["_coastal_geometry"] = True
        p["_land_km_interior"] = round(land_km, 4)
        if land_km > LAND_THRESH_KM:
            p["_qa_land_flag"] = True
            report["allowlisted"].append({"route_id": route_id_of(feat), "land_km": land_km, "action": "refresh"})
        report["refreshed"].append({"route_id": route_id_of(feat), "pts": len(new_coords)})
        updated += 1
    return updated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--ingest", default=str(INGEST))
    ap.add_argument("--refresh-existing", action="store_true", default=True)
    args = ap.parse_args()

    dc = ROOT / args.dc
    ingest = Path(args.ingest)
    corridors_path = ingest / "inputs/corridors.json"
    if not corridors_path.exists():
        print(f"missing {corridors_path}", file=sys.stderr)
        sys.exit(1)

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    corridors_doc = load_json(corridors_path)
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()

    existing_ids = {route_id_of(r) for r in routes}
    report = {
        "phase": "route_bolt_yango_markets",
        "synthesized": [],
        "skipped": [],
        "allowlisted": [],
        "refreshed": [],
        "errors": [],
    }

    if args.refresh_existing:
        n = refresh_coastal_geometry(routes, mask, report)
        print(f"refreshed coastal geometry on {n} existing routes")

    new_routes = []
    for market_key, market in partner_markets(corridors_doc).items():
        for corr in market.get("corridors") or []:
            from_bp, to_bp, from_city, to_city = resolve_corridor_endpoints(corr, bp_idx)
            if not from_bp or not to_bp or from_bp == to_bp:
                report["skipped"].append(
                    {"market": market_key, "from": corr.get("from"), "to": corr.get("to"), "reason": "unresolved_bp"}
                )
                continue

            a = bp_idx[from_bp]["coords"]
            b = bp_idx[to_bp]["coords"]
            manual = SIGNATURE_WAYPOINTS.get((from_bp, to_bp)) or SIGNATURE_WAYPOINTS.get((to_bp, from_bp))
            coords = build_coastal_path(a, b, mask, manual_waypoints=manual)
            land_km = interior_land_km(coords, mask)
            rid = mint_route_id(from_bp, to_bp)
            if rid in existing_ids:
                report["skipped"].append({"route_id": rid, "market": market_key, "reason": "already_exists"})
                continue

            feat = make_route_feature(
                from_bp,
                to_bp,
                bp_idx[from_bp]["name"],
                bp_idx[to_bp]["name"],
                from_city,
                to_city,
                coords,
                cities,
                land_km=land_km,
            )
            feat["properties"]["id"] = rid
            if land_km > LAND_THRESH_KM:
                feat["properties"]["_qa_land_flag"] = True
                report["allowlisted"].append({"route_id": rid, "land_km": land_km, "market": market_key})

            new_routes.append(feat)
            existing_ids.add(rid)
            report["synthesized"].append(
                {
                    "route_id": rid,
                    "market": market_key,
                    "from_bp": from_bp,
                    "to_bp": to_bp,
                    "nm": feat["properties"]["distance_nm"],
                    "land_km": land_km,
                }
            )

    routes.extend(new_routes)
    # Intra-city BP mesh — shared lane (scripts/grok-geometry/mint_intra_city_mesh.py)
    sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))
    from mint_intra_city_mesh import mint_mesh_for_cities  # noqa: E402

    mesh_report = mint_mesh_for_cities(
        routes,
        fbt,
        city_configs={},
        source="grok/boltyango_mesh",
        extra_cities=list(BOLT_YANGO_ANCHORS),
    )
    mesh_added = mesh_report.get("mesh_added", 0)
    for row in mesh_report.get("allowlisted", []):
        report["allowlisted"].append({**row, "market": f"mesh:{row.get('city')}"})
    for row in mesh_report.get("synthesized", []):
        report["synthesized"].append(
            {
                "route_id": row["route_id"],
                "market": f"mesh:{row['city']}",
                "from_bp": row["from"],
                "to_bp": row["to"],
                "tag": "mesh",
            }
        )
    save_routes(dc / "ROUTES.json", routes)
    print(f"intra-city mesh routes added: {mesh_added}")

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
    meta["boltyango_routing_at"] = datetime.now(timezone.utc).isoformat()
    meta["boltyango_allowlist_added"] = added
    save_json(allow_path, allow)

    out = ROOT / "grok-routing-output" / "bolt-yango-route-report.json"
    save_json(out, report)

    print(
        f"boltyango route: synthesized={len(report['synthesized'])} "
        f"refreshed={len(report['refreshed'])} skipped={len(report['skipped'])} "
        f"allowlisted={len(added)} errors={len(report['errors'])}"
    )
    print(f"report: {out}")


if __name__ == "__main__":
    main()