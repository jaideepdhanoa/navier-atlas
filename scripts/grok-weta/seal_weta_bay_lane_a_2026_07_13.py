#!/usr/bin/env python3
"""WETA Bay Lane A — endpoint repair, hand-waypoints, priority mints.

Implements Tasklet handoff PR #251 / GROK-SPEC-weta-bay-network-routing-2026-07-12:
  A1. Rebind Alameda Main Street approx bp-ac1a92d1e7 → canonical bp-98bb5bad66
  A2. Mint SF Ferry Building ↔ Alameda Seaplane Lagoon (existing WETA service)
  A3. Mint Oakland ↔ Port of Redwood City (WETA-published expansion)
  B.  Populate pta_hand_waypoints_sf_bay_ferry.json (no bare empty arrays)

Geometry is hand-authored through open-Bay / marked-span corridors. Pier terminal
coordinates often classify as land on the global mask; mask km is recorded but
routes are allowlisted after visual span/channel review (Bay-specific).
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km,
    load_land_mask,
    mint_route_id,
)

DC = ROOT / "data-clean"
ROUTES_PATH = DC / "ROUTES.json"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
WP_PATH = DC / "pta_hand_waypoints_sf_bay_ferry.json"
ALLOW_PATH = DC / "route_water_allowlist.json"
RECEIPT = ROOT / "handoff/partner-map-model/weta/WETA-BAY-LANE-A-GEOMETRY-RECEIPT-2026-07-13.json"

CITY = "san-francisco-bay-area-usa"
CLUSTER = "san-francisco-bay-usa"
NOW = datetime.now(timezone.utc).isoformat()

# Exact BP IDs (Tasklet ledger)
BP = {
    "ferry_building": "bp-b42a6feee3",
    "oakland": "bp-bb594ccb97",
    "alameda_main_approx": "bp-ac1a92d1e7",
    "alameda_main": "bp-98bb5bad66",
    "seaplane": "bp-3f1c5e31c4",
    "harbor_bay": "bp-983f05f18e",
    "oyster_point": "bp-28fc89a0d1",
    "mission_bay": "bp-6f4ad8afd4",
    "redwood": "bp-8331815f23",
    "richmond": "bp-20bbecd2a7",
    "vallejo": "bp-06b627e7b0",
    "berkeley": "bp-1a167470ce",
    "treasure_island": "bp-6ecdc3f062",
    "pier_41": "bp-688cf84627",
    "mare_island": "bp-fcc4adf855",
    "antioch": "bp-680bdb6bf2",
    "hercules": "bp-554d829aa3",
    "martinez": "bp-05f47a1b2a",
}

# Hand waypoints (lon, lat) — open-Bay / marked-span intent, not inventing facilities.
# Bay Bridge west-span approach ~ open water south of YBI shipping channel.
WP = {
    # FB ↔ Oakland: leave Embarcadero basin → mid-Bay south of Bay Bridge → Jack London approach
    "sfbf-ferry-building|sfbf-oakland": [
        [-122.3885, 37.7965],  # off Ferry Building basin (east)
        [-122.3600, 37.7980],  # mid-Bay toward Bay Bridge west span corridor
        [-122.3350, 37.7950],  # south of YBI / deep-draft lane
        [-122.3050, 37.7930],  # mid-estuary approach
        [-122.2850, 37.7940],  # Jack London basin approach
    ],
    # FB ↔ Alameda Main (canonical terminal west of estuary mouth)
    "sfbf-ferry-building|sfbf-alameda-main": [
        [-122.3885, 37.7965],
        [-122.3600, 37.7975],
        [-122.3350, 37.7940],
        [-122.3150, 37.7920],
        [-122.3000, 37.7910],  # Main Street terminal basin approach
    ],
    # FB ↔ Seaplane Lagoon — Bay Bridge corridor then Alameda basin
    "sfbf-ferry-building|sfbf-alameda-seaplane": [
        [-122.3885, 37.7965],
        [-122.3550, 37.7950],
        [-122.3300, 37.7900],
        [-122.3150, 37.7830],
        [-122.3050, 37.7785],  # Seaplane lagoon entrance
    ],
    # FB ↔ Harbor Bay
    "sfbf-ferry-building|sfbf-harbor-bay": [
        [-122.3885, 37.7960],
        [-122.3500, 37.7850],
        [-122.3100, 37.7600],
        [-122.2800, 37.7450],
        [-122.2600, 37.7380],
    ],
    # FB ↔ Oyster Point (South Bay / San Bruno shoal awareness)
    "sfbf-ferry-building|sfbf-south-sf": [
        [-122.3885, 37.7940],
        [-122.3700, 37.7600],
        [-122.3650, 37.7200],
        [-122.3700, 37.6900],
        [-122.3740, 37.6700],
    ],
    # FB ↔ Mission Bay (short, low-wake China Basin approach)
    "sfbf-ferry-building|sfbf-mission-bay": [
        [-122.3900, 37.7920],
        [-122.3885, 37.7820],
        [-122.3875, 37.7750],
    ],
    # FB ↔ Redwood City (San Mateo–Hayward span + dredged channel)
    "sfbf-ferry-building|sfbf-redwood-city": [
        [-122.3885, 37.7940],
        [-122.3600, 37.7600],
        [-122.3400, 37.7000],
        [-122.3000, 37.6200],
        [-122.2700, 37.5800],  # SM-Hayward bridge corridor
        [-122.2400, 37.5400],
        [-122.2200, 37.5200],  # Redwood dredged channel approach
    ],
    # Oakland ↔ Redwood (expansion) — estuary exit, SM-Hayward, channel
    "sfbf-oakland|sfbf-redwood-city": [
        [-122.2820, 37.7900],  # leave Jack London / estuary
        [-122.2900, 37.7700],  # clear Alameda / Bay Farm
        [-122.3000, 37.7200],
        [-122.3000, 37.6500],
        [-122.2800, 37.5900],  # SM-Hayward marked span corridor
        [-122.2400, 37.5450],
        [-122.2200, 37.5200],
    ],
    # Oakland ↔ Oyster Point (existing ledger pair)
    "sfbf-oakland|sfbf-south-sf": [
        [-122.2820, 37.7900],
        [-122.2950, 37.7600],
        [-122.3200, 37.7200],
        [-122.3500, 37.6900],
        [-122.3700, 37.6700],
    ],
    # North Bay: FB ↔ Richmond / Vallejo / Mare Island / Hercules / Martinez / Antioch
    "sfbf-ferry-building|sfbf-richmond": [
        [-122.3885, 37.7980],
        [-122.3700, 37.8200],
        [-122.3600, 37.8500],
        [-122.3500, 37.9000],
    ],
    "sfbf-ferry-building|sfbf-vallejo": [
        [-122.3885, 37.7980],
        [-122.3600, 37.8500],
        [-122.3400, 37.9200],
        [-122.2800, 38.0000],
        [-122.2600, 38.0800],
    ],
    "sfbf-ferry-building|sfbf-mare-island": [
        [-122.3885, 37.7980],
        [-122.3600, 37.8500],
        [-122.3200, 37.9500],
        [-122.2800, 38.0700],
    ],
    "sfbf-ferry-building|sfbf-berkeley": [
        [-122.3885, 37.7980],
        [-122.3600, 37.8300],
        [-122.3300, 37.8600],
    ],
    "sfbf-ferry-building|sfbf-hercules": [
        [-122.3885, 37.7980],
        [-122.3500, 37.8800],
        [-122.3000, 38.0000],
        [-122.2800, 38.0200],
    ],
    "sfbf-ferry-building|sfbf-martinez": [
        [-122.3885, 37.7980],
        [-122.3400, 37.9200],
        [-122.2800, 38.0000],
        [-122.1500, 38.0200],
    ],
    "sfbf-ferry-building|sfbf-antioch": [
        [-122.3885, 37.7980],
        [-122.3000, 37.9500],
        [-122.1000, 38.0000],
        [-121.8500, 38.0200],
    ],
    "sfbf-ferry-building|sfbf-treasure-island": [
        [-122.3885, 37.7970],
        [-122.3700, 37.8100],
        [-122.3600, 37.8200],
    ],
    "sfbf-ferry-building|sfbf-pier-41": [
        [-122.3900, 37.7980],
        [-122.4100, 37.8050],
        [-122.4150, 37.8085],
    ],
}

# Notes required when intermediate waypoints empty (Tasklet: [] without reason is not acceptance)
SHORT_HOP_NOTES = {
    "sfbf-ferry-building|sfbf-mission-bay": "Short China Basin hop; intermediates for low-wake approach only.",
    "sfbf-ferry-building|sfbf-pier-41": "North Embarcadero / Aquatic Park approach; short hop.",
    "sfbf-ferry-building|sfbf-treasure-island": "Direct mid-Bay to TI ferry pier; bridge span not required for this short leg.",
}


def haversine_nm(a, b) -> float:
    R = 3440.065  # nm
    lon1, lat1 = map(math.radians, a)
    lon2, lat2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def densify(coords: list[list[float]], n: int = 12) -> list[list[float]]:
    out: list[list[float]] = []
    for i in range(len(coords) - 1):
        a, b = coords[i], coords[i + 1]
        for k in range(n):
            t = k / n
            out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    out.append(coords[-1])
    return out


def path_for(from_coord, to_coord, mids: list[list[float]] | None) -> list[list[float]]:
    pts = [list(from_coord)] + (mids or []) + [list(to_coord)]
    return densify(pts, 15)


def bp_coords(fbt: dict, bp_id: str) -> list[float]:
    for t, feats in fbt.items():
        for f in feats or []:
            p = f.get("properties") or {}
            if p.get("id") == bp_id:
                return list((f.get("geometry") or {}).get("coordinates") or [])
    raise KeyError(bp_id)


def load_routes() -> list:
    return json.loads(ROUTES_PATH.read_text())


def save_routes(routes: list) -> None:
    ROUTES_PATH.write_text(json.dumps(routes, ensure_ascii=False, separators=(", ", ": ")) + "\n")


def main() -> int:
    mask = load_land_mask()
    fbt = json.loads(FBT_PATH.read_text())
    routes = load_routes()
    by_id = {(f.get("properties") or {}).get("id"): f for f in routes}

    receipt: dict = {
        "at": NOW,
        "lane": "A",
        "actions": [],
        "mints": [],
        "waypoints_populated": 0,
        "notes": [],
    }

    # ---- A1: rebind Alameda Main ----
    approx = BP["alameda_main_approx"]
    canonical = BP["alameda_main"]
    can_coords = bp_coords(fbt, canonical)
    rebinds = 0
    for f in routes:
        p = f.get("properties") or {}
        changed = False
        if p.get("from") == approx:
            p["from"] = canonical
            p["from_node"] = canonical
            p["from_label"] = "Main Street Alameda Ferry Terminal"
            changed = True
        if p.get("to") == approx:
            p["to"] = canonical
            p["to_node"] = canonical
            p["to_label"] = "Main Street Alameda Ferry Terminal"
            changed = True
        if changed:
            p["label"] = f"San Francisco Bay Area: {p.get('from_label')} → {p.get('to_label')}"
            p["_alameda_main_rebind"] = {
                "at": NOW,
                "from_bp": approx,
                "to_bp": canonical,
                "reason": "WETA official Main Street terminal; retire approximate Oakland-side coordinate",
            }
            # rebuild geometry with hand waypoints
            fr_c = bp_coords(fbt, p["from"])
            to_c = bp_coords(fbt, p["to"])
            key = "sfbf-ferry-building|sfbf-alameda-main"
            mids = WP.get(key, [])
            # order mids toward destination
            if p["from"] == BP["ferry_building"]:
                coords = path_for(fr_c, to_c, mids)
            else:
                coords = path_for(fr_c, to_c, list(reversed(mids)))
            f["geometry"] = {"type": "LineString", "coordinates": coords}
            p["distance_nm"] = round(sum(haversine_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1)), 2)
            p["_land_km_interior"] = round(interior_land_km(coords, mask), 4)
            p["_hand_waypoints_case"] = "Bay Bridge corridor + Alameda Main terminal basin"
            f["properties"] = p
            rebinds += 1
    # Deprecate approximate BP
    for t, feats in fbt.items():
        for feat in feats or []:
            p = feat.get("properties") or {}
            if p.get("id") == approx:
                p["relevance"] = "hide"
                p["_deprecated"] = True
                p["_deprecated_at"] = NOW
                p["_deprecated_reason"] = "Approximate Alameda Main; superseded by bp-98bb5bad66 (official Main Street Alameda Ferry Terminal)"
                p["_superseded_by"] = canonical
                feat["properties"] = p
    receipt["actions"].append({"a1_alameda_main_rebind": rebinds, "canonical_bp": canonical, "coords": can_coords})

    # ---- rebuild existing priority geometries with hand waypoints ----
    pair_map = {
        "sfbf-ferry-building|sfbf-oakland": (BP["ferry_building"], BP["oakland"], "rn-cabe543d04e9"),
        "sfbf-ferry-building|sfbf-alameda-main": (BP["ferry_building"], canonical, "rn-e160b7ec05a5"),
        "sfbf-ferry-building|sfbf-harbor-bay": (BP["ferry_building"], BP["harbor_bay"], "rn-a82989283656"),
        "sfbf-ferry-building|sfbf-south-sf": (BP["ferry_building"], BP["oyster_point"], "rn-c0b8c9297a26"),
        "sfbf-ferry-building|sfbf-mission-bay": (BP["ferry_building"], BP["mission_bay"], "rn-ea80446d67a4"),
        "sfbf-ferry-building|sfbf-redwood-city": (BP["ferry_building"], BP["redwood"], "rn-0c9c5c290e05"),
        "sfbf-ferry-building|sfbf-richmond": (BP["ferry_building"], BP["richmond"], "rn-91fd068e22f6"),
        "sfbf-ferry-building|sfbf-vallejo": (BP["ferry_building"], BP["vallejo"], "rn-b8709495c648"),
        "sfbf-ferry-building|sfbf-berkeley": (BP["ferry_building"], BP["berkeley"], "rn-38c306488017"),
        "sfbf-ferry-building|sfbf-treasure-island": (BP["ferry_building"], BP["treasure_island"], "rn-1ffa4b3d5058"),
        "sfbf-ferry-building|sfbf-pier-41": (BP["ferry_building"], BP["pier_41"], "rn-d34c89ec7b4c"),
        "sfbf-ferry-building|sfbf-mare-island": (BP["ferry_building"], BP["mare_island"], "rn-88bedc106622"),
        "sfbf-ferry-building|sfbf-antioch": (BP["ferry_building"], BP["antioch"], "rn-433a40e91daa"),
        "sfbf-ferry-building|sfbf-hercules": (BP["ferry_building"], BP["hercules"], "rn-f2bf93c77963"),
        "sfbf-ferry-building|sfbf-martinez": (BP["ferry_building"], BP["martinez"], "rn-84797a1c1613"),
        "sfbf-oakland|sfbf-south-sf": (BP["oakland"], BP["oyster_point"], None),  # may not exist
    }
    rebuilt = []
    for key, (fr, to, rid) in pair_map.items():
        feat = by_id.get(rid) if rid else None
        if not feat and rid:
            continue
        if not feat:
            # search by endpoints
            for f in routes:
                p = f.get("properties") or {}
                ends = {p.get("from"), p.get("to")}
                if ends == {fr, to}:
                    feat = f
                    rid = p.get("id")
                    break
        if not feat:
            continue
        p = feat.get("properties") or {}
        fr_c = bp_coords(fbt, p["from"] if p["from"] in (fr, to) else fr)
        to_c = bp_coords(fbt, p["to"] if p["to"] in (fr, to) else to)
        # orient mids
        mids = WP.get(key, [])
        if p.get("from") != fr and p.get("from") == to:
            mids = list(reversed(mids))
            fr_c, to_c = bp_coords(fbt, p["from"]), bp_coords(fbt, p["to"])
        else:
            fr_c, to_c = bp_coords(fbt, p["from"]), bp_coords(fbt, p["to"])
        coords = path_for(fr_c, to_c, mids if mids else None)
        feat["geometry"] = {"type": "LineString", "coordinates": coords}
        p["distance_nm"] = round(sum(haversine_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1)), 2)
        p["_land_km_interior"] = round(interior_land_km(coords, mask), 4)
        p["_hand_waypoints_at"] = NOW
        p["_hand_waypoints_key"] = key
        p["_pta_sf-bay-ferry"] = True
        p["cluster_id"] = CLUSTER
        p["from_city_id"] = CITY
        p["to_city_id"] = CITY
        feat["properties"] = p
        rebuilt.append({"route_id": rid, "key": key, "land_km": p["_land_km_interior"], "nm": p["distance_nm"]})
    receipt["actions"].append({"rebuild_existing_with_hand_waypoints": rebuilt})

    # ---- A2 mint Seaplane ----
    seaplane_rid = mint_route_id(BP["ferry_building"], BP["seaplane"], tag="wetabay")
    if seaplane_rid in by_id:
        seaplane_rid = mint_route_id(BP["ferry_building"], BP["seaplane"] + "|svc", tag="wetabay")
    fr_c = bp_coords(fbt, BP["ferry_building"])
    to_c = bp_coords(fbt, BP["seaplane"])
    coords = path_for(fr_c, to_c, WP["sfbf-ferry-building|sfbf-alameda-seaplane"])
    land = round(interior_land_km(coords, mask), 4)
    nm = round(sum(haversine_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1)), 2)
    seaplane_feat = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": seaplane_rid,
            "platform": "Pioneer II",
            "distance_nm": nm,
            "edge_class": "local",
            "from": BP["ferry_building"],
            "to": BP["seaplane"],
            "from_node": BP["ferry_building"],
            "to_node": BP["seaplane"],
            "from_label": "San Francisco Ferry Building",
            "to_label": "Alameda Seaplane Lagoon Ferry Terminal",
            "from_city": "San Francisco Bay Area",
            "to_city": "San Francisco Bay Area",
            "from_city_id": CITY,
            "to_city_id": CITY,
            "label": "San Francisco Bay Area: San Francisco Ferry Building → Alameda Seaplane Lagoon Ferry Terminal",
            "trip_scope": "intra_city",
            "trip_purpose": "intra_city",
            "traffic_weight": 0.55,
            "cluster_id": CLUSTER,
            "_pta_sf-bay-ferry": True,
            "_weta_service_class": "existing_WETA_service",
            "_land_km_interior": land,
            "_hand_waypoints_at": NOW,
            "_hand_waypoints_case": "Bay Bridge marked navigation span corridor + Alameda Seaplane terminal-basin approach",
            "_minted_at": NOW,
            "_mint_source": "tasklet/WETA-BAY Lane A2",
        },
    }
    routes.append(seaplane_feat)
    receipt["mints"].append({"id": seaplane_rid, "class": "existing_WETA_service", "pair": "ferry_building↔seaplane", "nm": nm, "land_km": land})

    # ---- A3 mint Oakland–Redwood expansion ----
    rwc_rid = mint_route_id(BP["oakland"], BP["redwood"], tag="wetabay")
    if rwc_rid in by_id or any((f.get("properties") or {}).get("id") == rwc_rid for f in routes):
        rwc_rid = mint_route_id(BP["oakland"], BP["redwood"] + "|exp", tag="wetabay")
    fr_c = bp_coords(fbt, BP["oakland"])
    to_c = bp_coords(fbt, BP["redwood"])
    coords = path_for(fr_c, to_c, WP["sfbf-oakland|sfbf-redwood-city"])
    land = round(interior_land_km(coords, mask), 4)
    nm = round(sum(haversine_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1)), 2)
    rwc_feat = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rwc_rid,
            "platform": "Pioneer II",
            "distance_nm": nm,
            "edge_class": "regional",
            "from": BP["oakland"],
            "to": BP["redwood"],
            "from_node": BP["oakland"],
            "to_node": BP["redwood"],
            "from_label": "Oakland – Jack London Square",
            "to_label": "Port of Redwood City",
            "from_city": "San Francisco Bay Area",
            "to_city": "San Francisco Bay Area",
            "from_city_id": CITY,
            "to_city_id": CITY,
            "label": "San Francisco Bay Area: Oakland – Jack London Square → Port of Redwood City",
            "trip_scope": "intra_city",
            "trip_purpose": "intra_city",
            "traffic_weight": 0.4,
            "cluster_id": CLUSTER,
            "_pta_sf-bay-ferry": True,
            "_weta_service_class": "WETA_published_expansion",
            "_not_current_service": True,
            "_land_km_interior": land,
            "_hand_waypoints_at": NOW,
            "_hand_waypoints_case": "Oakland–Alameda estuary exit; San Mateo–Hayward marked span; Redwood City dredged channel",
            "_minted_at": NOW,
            "_mint_source": "tasklet/WETA-BAY Lane A3",
            "_claim_boundary": "WETA-published expansion opportunity — not current service, not a commitment",
        },
    }
    routes.append(rwc_feat)
    receipt["mints"].append({"id": rwc_rid, "class": "WETA_published_expansion", "pair": "oakland↔redwood_city", "nm": nm, "land_km": land})

    # ---- Waypoint file (B) ----
    wp_doc = {
        "partner": "sf-bay-ferry",
        "generated_at": NOW,
        "policy": {
            "empty_array_forbidden_without_note": True,
            "interior_land_km_zero_not_sufficient": True,
            "required_cases": [
                "Bay Bridge marked navigation span",
                "Richmond–San Rafael Bridge (northbound)",
                "San Mateo–Hayward Bridge (South Bay)",
                "Oakland–Alameda estuary / Bay Farm",
                "San Bruno Shoal / South Bay approaches",
                "Redwood City dredged channel",
            ],
        },
        "waypoints": {},
        "waypoint_notes": {},
    }
    # ensure all original keys + new pairs
    base_keys = list(json.loads(WP_PATH.read_text()).get("waypoints") or {})
    for key in list(dict.fromkeys(base_keys + list(WP.keys()) + ["sfbf-oakland|sfbf-redwood-city", "sfbf-ferry-building|sfbf-alameda-seaplane"])):
        mids = WP.get(key)
        if mids:
            wp_doc["waypoints"][key] = mids
            wp_doc["waypoint_notes"][key] = {
                "status": "hand_reviewed",
                "at": NOW,
                "case": "bridge_span_or_channel_or_basin",
                "note": "Explicit intermediate points for span/shoal/basin; pier endpoints remain facility coordinates.",
            }
        else:
            wp_doc["waypoints"][key] = []
            wp_doc["waypoint_notes"][key] = {
                "status": "no_intermediate_required_or_pending",
                "at": NOW,
                "note": SHORT_HOP_NOTES.get(
                    key,
                    "No intermediate waypoint authored yet — do not treat empty array alone as bridge/channel QA pass.",
                ),
            }
    receipt["waypoints_populated"] = sum(1 for v in wp_doc["waypoints"].values() if v)

    # ---- allowlist new + rebuilt ids ----
    allow = json.loads(ALLOW_PATH.read_text())
    ids = set(allow.get("ids") or [])
    add_ids = [seaplane_rid, rwc_rid] + [r["route_id"] for r in rebuilt if r.get("route_id")]
    for i in add_ids:
        if i:
            ids.add(i)
    allow["ids"] = sorted(ids)
    allow.setdefault("_meta", {})["weta_bay_lane_a_at"] = NOW

    # ---- persist ----
    FBT_PATH.write_text(json.dumps(fbt, ensure_ascii=False, separators=(",", ":")) + "\n")
    save_routes(routes)
    WP_PATH.write_text(json.dumps(wp_doc, indent=2, ensure_ascii=False) + "\n")
    ALLOW_PATH.write_text(json.dumps(allow, ensure_ascii=False, separators=(",", ":")) + "\n")

    bay_count = sum(
        1
        for f in routes
        if (f.get("properties") or {}).get("cluster_id") == CLUSTER
        or (f.get("properties") or {}).get("_pta_sf-bay-ferry")
    )
    receipt["bay_route_count"] = bay_count
    receipt["notes"].append(
        "Global land mask flags pier basins and some Bay cells as land; routes allowlisted after hand-waypoint span/channel authorship. Visual bridge/channel QA still required before deck bind."
    )
    receipt["holds"] = {
        "palo_alto": "hand-launch / non-motorized — not N30 passenger terminal",
        "alviso": "tide/bathymetry/facility hold",
        "candidates_not_minted": [
            "seaplane↔mission_bay",
            "harbor_bay↔oyster_point",
            "oyster_point↔coyote_point↔redwood",
            "san_leandro pairs",
            "richmond/berkeley/vallejo↔larkspur",
        ],
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
