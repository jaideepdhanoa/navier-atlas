#!/usr/bin/env python3
"""Mint gold routes for India held-null marquee corridors (PR #58).

Targets POI pairs that exist in FEATURES_BY_TYPE but lack ROUTES.json geometry:
  - Goa ↔ Grande Island / Bat Island
  - Port Blair ↔ Ross Island / North Bay
  - Port Blair ↔ Diglipur (North Andaman) — synthesises Diglipur jetty POI first
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
    build_bp_index,
    build_city_index,
    build_coastal_path,
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
REPORT = ROOT / "handoff/partner-map-model/india-held-null-mint-report.json"

# Existing boarding points (verified in gold)
MORMAGAO = "bp-0d6e4cc1d5"
GRANDE = "bp-61a48743ff"
HADDO = "bp-7f1d145a12"
ROSS = "bp-619284c9e7"
NORTH_BAY = "bp-dbd5433377"
DIGLIPUR_ID = "bp-" + hashlib.md5(b"pr58|Diglipur Aerial Bay Jetty|andaman-india").hexdigest()[:10]

CORRIDORS = [
    {
        "key": "goa_grande",
        "from_node": MORMAGAO,
        "to_node": GRANDE,
        "from_label": "Mormugao Harbour",
        "to_label": "Grande Island (Bat Island)",
        "from_city_id": "goa-india",
        "to_city_id": "goa-india",
        "marquee": "Goa ↔ Grande Island / Bat Island",
    },
    {
        "key": "port_blair_ross",
        "from_node": HADDO,
        "to_node": ROSS,
        "from_label": "Port Blair (Haddo Wharf / Phoenix Bay Jetty)",
        "to_label": "Ross Island (Netaji Subhas)",
        "from_city_id": "andaman-india",
        "to_city_id": "andaman-india",
        "marquee": "Port Blair ↔ Ross Island / North Bay",
    },
    {
        "key": "port_blair_north_bay",
        "from_node": HADDO,
        "to_node": NORTH_BAY,
        "from_label": "Port Blair (Haddo Wharf / Phoenix Bay Jetty)",
        "to_label": "North Bay Island",
        "from_city_id": "andaman-india",
        "to_city_id": "andaman-india",
        "marquee": "Port Blair ↔ Ross Island / North Bay",
    },
    {
        "key": "port_blair_diglipur",
        "from_node": HADDO,
        "to_node": DIGLIPUR_ID,
        "from_label": "Port Blair (Haddo Wharf / Phoenix Bay Jetty)",
        "to_label": "Diglipur Aerial Bay Jetty",
        "from_city_id": "andaman-india",
        "to_city_id": "andaman-india",
        "marquee": "Port Blair ↔ Diglipur (North Andaman)",
        "synth_poi": {
            "id": DIGLIPUR_ID,
            "name": "Diglipur Aerial Bay Jetty",
            "coordinates": [92.978, 13.268],
            "parent_city_id": "andaman-india",
        },
    },
]


def ensure_diglipur_poi(fbt: dict) -> bool:
    poi_list = fbt.setdefault("poi", [])
    by_id = {f["properties"]["id"]: f for f in poi_list if f.get("properties", {}).get("id")}
    spec = CORRIDORS[-1]["synth_poi"]
    if spec["id"] in by_id:
        return False
    lng, lat = spec["coordinates"]
    poi_list.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": spec["id"],
            "type": "poi",
            "bp_type": "marina_or_jetty",
            "bp_type_label": "marina_or_jetty",
            "name": spec["name"],
            "fullName": spec["name"],
            "shortName": spec["name"],
            "parent_city_id": spec["parent_city_id"],
            "region": "South Asia",
            "confidence": "low",
            "status": "operational",
            "last_enriched": "pr58_held_null_mint",
            "source_url": None,
            "_pr58_synth": True,
            "_registry_note": "Diglipur ferry jetty — synthesised for Quanta-LR line-haul bind; refine coords at BP build",
        },
    })
    return True


def main() -> int:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    poi_added = ensure_diglipur_poi(fbt)
    if poi_added:
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)

    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    minted: list[dict] = []
    marquee_map: dict[str, list[str]] = {}
    single_map: dict[str, str] = {}

    for row in CORRIDORS:
        fn, tn = row["from_node"], row["to_node"]
        a = bp_idx.get(fn, {}).get("coords")
        b = bp_idx.get(tn, {}).get("coords")
        if not a or not b:
            print(f"skip {row['key']}: missing coords for {fn} or {tn}")
            continue
        rid = mint_route_id(fn, tn, tag="pr58india")
        if rid in existing:
            print(f"skip {row['key']}: {rid} already exists")
            minted.append({"route_id": rid, "key": row["key"], "status": "exists"})
        else:
            coords = build_coastal_path(a, b, mask)
            land_km = interior_land_km(coords, mask)
            feat = make_route_feature(
                fn, tn,
                row["from_label"], row["to_label"],
                row["from_city_id"], row["to_city_id"],
                coords, cities,
                source="pr58_india_held_null",
                land_km=land_km,
            )
            feat["properties"]["id"] = rid
            routes.append(feat)
            existing.add(rid)
            minted.append({
                "route_id": rid,
                "key": row["key"],
                "distance_nm": feat["properties"]["distance_nm"],
                "marquee": row["marquee"],
                "status": "minted",
            })
            print(f"minted {rid} {row['key']} ({feat['properties']['distance_nm']} nm)")

        marquee = row["marquee"]
        if row["key"] in ("port_blair_ross", "port_blair_north_bay"):
            marquee_map.setdefault(marquee, []).append(rid)
        else:
            single_map[marquee] = rid

    save_routes(DC / "ROUTES.json", routes)

    allow_path = DC / "route_water_allowlist.json"
    allow = load_json(allow_path)
    ids = list(allow.get("ids", []))
    seen = set(ids)
    added = []
    for m in minted:
        rid = m["route_id"]
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
            added.append(rid)
    allow["ids"] = ids
    allow.setdefault("_meta", {})["pr58_india_held_null_mint_at"] = datetime.now(timezone.utc).isoformat()
    save_json(allow_path, allow)

    report = {
        "at": datetime.now(timezone.utc).isoformat(),
        "poi_added": poi_added,
        "diglipur_poi_id": DIGLIPUR_ID if poi_added else None,
        "minted": minted,
        "allowlist_added": added,
        "marquee_static_route_ids": marquee_map,
        "marquee_single_route_id": single_map,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())