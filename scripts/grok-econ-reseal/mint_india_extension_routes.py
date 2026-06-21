#!/usr/bin/env python3
"""Mint held-null India extension corridors (heritage circuit, leisure, Puducherry)."""
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
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "india-extension-mint-report.json"
TAG = "india_kcc_ext"
KOLKATA = "kolkata-india"
CHENNAI = "chennai-india"


def bp_id(name: str, city: str) -> str:
    return "bp-" + hashlib.md5(f"{TAG}|{name}|{city}".encode()).hexdigest()[:10]


def poi(bp: dict) -> dict:
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
            "region": "South Asia",
            "confidence": "medium",
            "status": "operational",
            "last_enriched": "grok_india_extension_mint_2026-06-21",
            "_india_kcc_ext": True,
        },
    }


def core_bp_ids() -> dict[str, str]:
    """Resolve IDs from prior india_kcc mint report (TAG hash differs from ext)."""
    prior = HANDOFF / "india-kolkata-chennai-mint-report.json"
    out: dict[str, str] = {}
    if prior.exists():
        for m in load_json(prior).get("minted", []):
            out.setdefault("howrah", m.get("from_bp") if "howrah" in m.get("key", "") else None)
            if m.get("key") == "howrah_fairlie":
                out["fairlie"] = m["to_bp"]
            if m.get("key") == "howrah_millennium":
                out["millennium"] = m["to_bp"]
            if m.get("key") == "chennai_port_marina":
                out["chennai_port"] = m["from_bp"]
    return {k: v for k, v in out.items() if v}


CORE = core_bp_ids()
FAIRLIE = CORE.get("fairlie", bp_id("Fairlie Place Ferry", KOLKATA))
MILLENNIUM = CORE.get("millennium", bp_id("Millennium Park Jetty", KOLKATA))
CHENNAI_PORT = CORE.get("chennai_port", bp_id("Chennai Port WQIV Cruise Terminal", CHENNAI))

EXTRA_BPS = [
    {"id": bp_id("Bagbazar Ghat", KOLKATA), "name": "Bagbazar Ghat", "short": "Bagbazar", "city_id": KOLKATA, "coordinates": [88.3650, 22.5950]},
    {"id": bp_id("Chandannagar Riverfront", KOLKATA), "name": "Chandannagar Riverfront", "short": "Chandannagar", "city_id": KOLKATA, "coordinates": [88.3680, 22.8670]},
    {"id": bp_id("Puducherry Port", CHENNAI), "name": "Puducherry Port", "short": "Puducherry", "city_id": CHENNAI, "coordinates": [79.8300, 11.9260]},
    {"id": bp_id("Napier Bridge", CHENNAI), "name": "Napier Bridge", "short": "Napier Bridge", "city_id": CHENNAI, "coordinates": [80.2820, 13.0610]},
    {"id": bp_id("Kovalam Creek", CHENNAI), "name": "Kovalam Creek", "short": "Kovalam", "city_id": CHENNAI, "coordinates": [80.2380, 12.7440]},
]

CORRIDORS = [
    {
        "key": "fairlie_bagbazar",
        "journey_from": "Fairlie",
        "journey_to": "Ariyadaha via Howrah / Baghbazar / Belur / Kutighat",
        "partner_market_id": "kolkata_hooghly_waterfront",
        "from_bp": FAIRLIE, "to_bp": bp_id("Bagbazar Ghat", KOLKATA),
        "from_label": "Fairlie Place Ferry", "to_label": "Bagbazar Ghat",
        "from_city_id": KOLKATA, "to_city_id": KOLKATA, "path_mode": "river",
        "archetype": "heritage_circuit_partial",
    },
    {
        "key": "millennium_chandannagar",
        "journey_from": "Millennium Park / Babughat / Princep Ghat",
        "journey_to": "Heritage Hooghly leisure loop",
        "partner_market_id": "kolkata_hooghly_waterfront",
        "from_bp": MILLENNIUM, "to_bp": bp_id("Chandannagar Riverfront", KOLKATA),
        "from_label": "Millennium Park Jetty", "to_label": "Chandannagar Riverfront",
        "from_city_id": KOLKATA, "to_city_id": KOLKATA, "path_mode": "river",
        "archetype": "premium_leisure",
    },
    {
        "key": "chennai_puducherry",
        "journey_from": "Chennai",
        "journey_to": "Puducherry / Pondicherry",
        "partner_market_id": "chennai_ecr_cuddalore_puducherry_coast",
        "from_bp": CHENNAI_PORT, "to_bp": bp_id("Puducherry Port", CHENNAI),
        "from_label": "Chennai Port WQIV Cruise Terminal", "to_label": "Puducherry Port",
        "from_city_id": CHENNAI, "to_city_id": CHENNAI, "path_mode": "coastal",
        "archetype": "coastal_tourism_extension",
    },
    {
        "key": "buckingham_canal_feasibility",
        "journey_from": "Napier Bridge",
        "journey_to": "Kovalam via Buckingham Canal",
        "partner_market_id": "chennai_ecr_cuddalore_puducherry_coast",
        "from_bp": bp_id("Napier Bridge", CHENNAI), "to_bp": bp_id("Kovalam Creek", CHENNAI),
        "from_label": "Napier Bridge", "to_label": "Kovalam Creek",
        "from_city_id": CHENNAI, "to_city_id": CHENNAI, "path_mode": "coastal",
        "archetype": "future_water_metro",
        "roadmap": True,
    },
]


def main() -> int:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    poi_list = fbt.setdefault("poi", [])
    by_id = {f["properties"]["id"]: f for f in poi_list if f.get("properties", {}).get("id")}
    added_bps = []
    for bp in EXTRA_BPS:
        if bp["id"] not in by_id:
            poi_list.append(poi(bp))
            added_bps.append(bp["id"])
    if added_bps:
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)

    bp_coords: dict[str, tuple[float, float]] = {}
    for f in poi_list:
        p = f.get("properties", {})
        bid = p.get("id")
        geom = f.get("geometry", {}).get("coordinates")
        if bid and geom:
            bp_coords[bid] = (geom[0], geom[1])

    cities = build_city_index(fbt)
    mask = load_land_mask()
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}
    minted = []
    for row in CORRIDORS:
        fa = bp_coords.get(row["from_bp"])
        tb = bp_coords.get(row["to_bp"])
        if not fa or not tb:
            print(f"skip {row['key']}: missing BP coords")
            continue
        rid = mint_route_id(row["from_bp"], row["to_bp"], tag=TAG)
        if rid in existing:
            feat = next(r for r in routes if r["properties"]["id"] == rid)
            status = "exists"
        else:
            coords = densify(fa, tb, 20) if row["path_mode"] == "river" else build_coastal_path(fa, tb, mask)
            land_km = interior_land_km(coords, mask) if row["path_mode"] == "coastal" else 0.0
            feat = make_route_feature(
                row["from_bp"], row["to_bp"],
                row["from_label"], row["to_label"],
                row["from_city_id"], row["to_city_id"],
                coords, cities, source=TAG, land_km=land_km,
            )
            feat["properties"]["id"] = rid
            if row.get("roadmap"):
                feat["properties"]["_roadmap_feasibility"] = True
                feat["properties"]["edge_class"] = "roadmap"
            routes.append(feat)
            existing.add(rid)
            status = "minted"
            print(f"minted {rid} {row['key']}")
        minted.append({**row, "route_id": rid, "distance_nm": feat["properties"]["distance_nm"], "status": status})

    save_routes(DC / "ROUTES.json", routes)
    allow_path = DC / "route_water_allowlist.json"
    if allow_path.exists():
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for m in minted:
            if m["route_id"] not in seen:
                ids.append(m["route_id"])
                seen.add(m["route_id"])
        allow["ids"] = ids
        save_json(allow_path, allow)

    report = {"at": datetime.now(timezone.utc).isoformat(), "bps_added": added_bps, "minted": minted}
    save_json(REPORT, report)
    print(json.dumps({"bps": len(added_bps), "routes": len(minted)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())