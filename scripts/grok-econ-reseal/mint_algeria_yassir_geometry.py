#!/usr/bin/env python3
"""Mint Algeria cities, boarding points, and sealable routes for Yassir batch 1.

Sources: handoff/partner-map-model/caribbean-yassir-gold-2026-06-21/
  yassir-algeria-tasklet-research-completion-2026-06-21.json
  yassir-algeria-route-source-hardening-batch-1.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_city_index,
    build_coastal_path,
    densify,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff" / "partner-map-model" / "caribbean-yassir-gold-2026-06-21"
REPORT = ROOT / "handoff" / "partner-map-model" / "algeria-yassir-mint-report.json"
TAG = "yassir_algeria"

ALGIERS = "algiers-algeria"
BEJAIA = "bejaia-algeria"
ORAN = "oran-algeria"
MOSTAGANEM = "mostaganem-algeria"


def bp_id(name: str, city_id: str) -> str:
    return "bp-" + hashlib.md5(f"{TAG}|{name}|{city_id}".encode()).hexdigest()[:10]


def city_feature(city_id: str, name: str, short: str, lng: float, lat: float) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": city_id,
            "type": "city",
            "name": name,
            "shortName": short,
            "fullName": name,
            "region": "Maghreb",
            "country": "Algeria",
            "platform_class": "dual-platform",
            "priority": 1,
            "tier_sort_key": 1,
            "coords_resolved": True,
            "coords_source": "grok_yassir_algeria_mint_2026-06-21",
        },
    }


def poi_feature(bp: dict) -> dict:
    lng, lat = bp["coordinates"]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "bp_type": "ferry_terminal",
            "bp_type_label": "Ferry Terminal",
            "name": bp["name"],
            "fullName": bp["name"],
            "shortName": bp["short"],
            "parent_city_id": bp["city_id"],
            "region": "Maghreb",
            "confidence": "medium",
            "status": "operational",
            "last_enriched": "grok_yassir_algeria_mint_2026-06-21",
            "source_url": bp.get("source_url"),
            "_yassir_algeria_mint": True,
            "_registry_note": bp.get("note", "Tasklet ENTMV / port evidence"),
        },
    }


CITIES = [
    (ALGIERS, "Algiers / Alger Centre", "Algiers", 3.0588, 36.7538),
    (BEJAIA, "Béjaïa", "Béjaïa", 5.0833, 36.7525),
    (ORAN, "Oran", "Oran", -0.6417, 35.6969),
    (MOSTAGANEM, "Mostaganem", "Mostaganem", 0.0889, 35.9311),
]

BOARDING_POINTS = [
    {
        "id": bp_id("La Pêcherie Port d'Alger", ALGIERS),
        "name": "La Pêcherie / Port d'Alger / Gare Maritime",
        "short": "La Pêcherie",
        "city_id": ALGIERS,
        "coordinates": [3.0612, 36.7835],
        "source_url": "https://radioalgerie.dz/news/fr/article/20140805/9131.html",
    },
    {
        "id": bp_id("El Djamila Ain Benian", ALGIERS),
        "name": "El Djamila / Aïn Bénian",
        "short": "El Djamila",
        "city_id": ALGIERS,
        "coordinates": [3.2300, 36.8025],
        "source_url": "https://radioalgerie.dz/news/fr/article/20140805/9131.html",
    },
    {
        "id": bp_id("Port de Bejaia", BEJAIA),
        "name": "Port de Béjaïa passenger terminal",
        "short": "Béjaïa Port",
        "city_id": BEJAIA,
        "coordinates": [5.0680, 36.7480],
        "source_url": "https://www.portdebejaia.dz/",
    },
    {
        "id": bp_id("Gare Maritime Oran", ORAN),
        "name": "Gare Maritime / Port d'Oran",
        "short": "Oran Port",
        "city_id": ORAN,
        "coordinates": [-0.6520, 35.7080],
        "source_url": "https://ca.directferries.com/oran_ferry.htm",
    },
    {
        "id": bp_id("Port Mostaganem", MOSTAGANEM),
        "name": "Gare Maritime / Port de Mostaganem",
        "short": "Mostaganem Port",
        "city_id": MOSTAGANEM,
        "coordinates": [0.0820, 35.9380],
        "source_url": "http://news.radioalgerie.dz/fr/node/27221",
    },
]

CORRIDORS = [
    {
        "candidate_id": "dz-algiers-bay-pecherie-el-djamila",
        "from_bp": bp_id("La Pêcherie Port d'Alger", ALGIERS),
        "to_bp": bp_id("El Djamila Ain Benian", ALGIERS),
        "from_label": "La Pêcherie / Port d'Alger",
        "to_label": "El Djamila / Aïn Bénian",
        "from_city_id": ALGIERS,
        "to_city_id": ALGIERS,
        "vessel_gate": "N30 Pioneer II commercial-now",
        "economics_status": "commercial_now",
        "path_mode": "bay",
    },
    {
        "candidate_id": "dz-oran-mostaganem-summer",
        "from_bp": bp_id("Gare Maritime Oran", ORAN),
        "to_bp": bp_id("Port Mostaganem", MOSTAGANEM),
        "from_label": "Port d'Oran",
        "to_label": "Mostaganem port",
        "from_city_id": ORAN,
        "to_city_id": MOSTAGANEM,
        "vessel_gate": "N30 Pioneer II commercial-now",
        "economics_status": "commercial_now",
        "path_mode": "coastal_waypoints",
        "waypoints": [(-1.05, 35.72), (-0.55, 35.82), (-0.2, 35.9)],
    },
    {
        "candidate_id": "dz-bejaia-algiers-hsc",
        "from_bp": bp_id("Port de Bejaia", BEJAIA),
        "to_bp": bp_id("La Pêcherie Port d'Alger", ALGIERS),
        "from_label": "Port de Béjaïa",
        "to_label": "Port d'Alger",
        "from_city_id": BEJAIA,
        "to_city_id": ALGIERS,
        "vessel_gate": "Quanta-LR roadmap",
        "economics_status": "roadmap_excluded",
        "path_mode": "coastal_waypoints",
        "waypoints": [(4.8, 36.9), (4.1, 37.05), (3.4, 37.0), (3.0, 36.92)],
    },
]


def build_path_for_row(row: dict, fa: tuple[float, float], tb: tuple[float, float], mask) -> list:
    mode = row.get("path_mode", "coastal")
    if mode == "bay":
        return densify(fa, tb, n=20)
    if mode == "coastal_waypoints":
        pts = [fa]
        for wp in row.get("waypoints", []):
            pts.append(tuple(wp))
        pts.append(tb)
        coords: list = []
        for i in range(len(pts) - 1):
            seg = build_coastal_path(pts[i], pts[i + 1], mask)
            coords.extend(seg if not coords else seg[1:])
        return coords
    return build_coastal_path(fa, tb, mask)


def vessel_gate_for(dist_nm: float) -> str:
    if dist_nm <= 70:
        return "N30 Pioneer II commercial-now"
    if dist_nm <= 150:
        return "Quanta-LR roadmap"
    return "Quanta-LR review"


def ensure_cities(fbt: dict) -> list[str]:
    cities = fbt.setdefault("city", [])
    by_id = {f["properties"]["id"]: f for f in cities if f.get("properties", {}).get("id")}
    added = []
    for cid, name, short, lng, lat in CITIES:
        if cid in by_id:
            continue
        cities.append(city_feature(cid, name, short, lng, lat))
        added.append(cid)
    return added


def ensure_bps(fbt: dict) -> list[str]:
    poi_list = fbt.setdefault("poi", [])
    by_id = {f["properties"]["id"]: f for f in poi_list if f.get("properties", {}).get("id")}
    added = []
    for bp in BOARDING_POINTS:
        if bp["id"] in by_id:
            continue
        poi_list.append(poi_feature(bp))
        added.append(bp["id"])
    return added


def main() -> int:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    cities_added = ensure_cities(fbt)
    bps_added = ensure_bps(fbt)
    if cities_added or bps_added:
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)

    bp_idx = {bp["id"]: bp for bp in BOARDING_POINTS}
    cities = build_city_index(fbt)
    mask = load_land_mask()
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    minted: list[dict] = []
    held: list[dict] = []

    for row in CORRIDORS:
        fn, tn = row["from_bp"], row["to_bp"]
        fa = tuple(bp_idx[fn]["coordinates"])
        tb = tuple(bp_idx[tn]["coordinates"])
        rid = mint_route_id(fn, tn, tag=TAG)
        if rid in existing:
            feat = next(r for r in routes if r["properties"]["id"] == rid)
            dist = feat["properties"]["distance_nm"]
            status = "exists"
        else:
            coords = build_path_for_row(row, fa, tb, mask)
            land_km = interior_land_km(coords, mask)
            feat = make_route_feature(
                fn, tn,
                row["from_label"], row["to_label"],
                row["from_city_id"], row["to_city_id"],
                coords, cities,
                source=TAG,
                land_km=land_km,
            )
            feat["properties"]["id"] = rid
            feat["properties"]["_yassir_algeria_mint"] = True
            if land_km > 2.0:
                feat["properties"]["_land_km_interior"] = round(land_km, 2)
                feat["properties"]["_land_crossing_review"] = True
            routes.append(feat)
            existing.add(rid)
            dist = feat["properties"]["distance_nm"]
            status = "minted"
            print(f"minted {rid} {row['candidate_id']} ({dist} nm)")

        gate = vessel_gate_for(dist)
        minted.append({
            **row,
            "route_id": rid,
            "distance_nm": dist,
            "vessel_gate": gate,
            "status": status,
        })

    save_routes(DC / "ROUTES.json", routes)

    report = {
        "at": datetime.now(timezone.utc).isoformat(),
        "lane": "grok/mint_algeria_yassir_geometry",
        "cities_added": cities_added,
        "bps_added": bps_added,
        "minted": minted,
        "held": held,
    }
    save_json(REPORT, report)
    print(json.dumps({"cities": cities_added, "bps": bps_added, "routes": len(minted), "held": len(held)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())