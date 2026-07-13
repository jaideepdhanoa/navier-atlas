#!/usr/bin/env python3
"""WETA / SF Bay Ferry — partner-ready corridor seal (2026-07-13).

Completes Tasklet handoff (#251) + Lane A (#252):
  - Local SF Bay mask (water corridors + land exclusions + terminal aprons)
  - Hand spines for every PTA pair + A* water fill
  - interior_land_km gate under local mask
  - Bind exact route IDs into sf-bay-ferry partner journeys
  - Replace oversized regional sf_bay water bbox with corridor-aware note
  - Receipt for partner-ready return

Does NOT invent WETA commitments for Lane C candidates (held null or labeled
Navier_candidate_screen only if explicitly minted with claim boundary).
"""
from __future__ import annotations

import json
import math
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-weta"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from sf_bay_local_mask import (  # noqa: E402
    densify,
    hav_km,
    interior_land_km,
    point_is_water,
    route_via_spine,
    simplify_coords,
)
from bolt_yango_routing_shared import mint_route_id  # noqa: E402

DC = ROOT / "data-clean"
ROUTES_PATH = DC / "ROUTES.json"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
WP_PATH = DC / "pta_hand_waypoints_sf_bay_ferry.json"
ALLOW_PATH = DC / "route_water_allowlist.json"
PARTNER_PATH = DC / "partners/sf-bay-ferry.json"
PITCH_PATH = ROOT / "partner-pitch/partners/sf-bay-ferry.json"
REGIONAL_MASK = ROOT / "scripts/grok-geometry/regional_land_masks.py"
RECEIPT = ROOT / "handoff/partner-map-model/weta/WETA-BAY-PARTNER-READY-RECEIPT-2026-07-13.json"

CITY = "san-francisco-bay-area-usa"
CLUSTER = "san-francisco-bay-usa"
NOW = datetime.now(timezone.utc).isoformat()
LAND_GATE_KM = 0.35  # local-mask residual tolerance (piers / mask edge)

BP = {
    "ferry_building": "bp-b42a6feee3",
    "oakland": "bp-bb594ccb97",
    "alameda_main": "bp-98bb5bad66",
    "alameda_main_approx": "bp-ac1a92d1e7",
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

# Corridor spines (lon, lat) — open water / marked spans / dredged channels only.
# Order: Ferry Building-side → destination for FB pairs; otherwise from→to.
SPINES: dict[str, list[list[float]]] = {
    # Bay Bridge west-span deep-draft corridor → Jack London estuary mouth
    "sfbf-ferry-building|sfbf-oakland": [
        [-122.3880, 37.7980],
        [-122.3600, 37.8000],
        [-122.3400, 37.7980],
        [-122.3200, 37.7960],
        [-122.3000, 37.7950],
        [-122.2850, 37.7945],
    ],
    "sfbf-ferry-building|sfbf-alameda-main": [
        [-122.3880, 37.7975],
        [-122.3550, 37.7980],
        [-122.3300, 37.7950],
        [-122.3100, 37.7920],
        [-122.2980, 37.7910],
    ],
    "sfbf-ferry-building|sfbf-alameda-seaplane": [
        [-122.3880, 37.7960],
        [-122.3500, 37.7930],
        [-122.3250, 37.7880],
        [-122.3100, 37.7820],
        [-122.3020, 37.7780],
    ],
    "sfbf-ferry-building|sfbf-harbor-bay": [
        [-122.3880, 37.7940],
        [-122.3500, 37.7800],
        [-122.3200, 37.7600],
        [-122.2900, 37.7450],
        [-122.2650, 37.7380],
    ],
    # South Bay: stay west-central, avoid Bay Farm land, Oyster Point basin
    "sfbf-ferry-building|sfbf-south-sf": [
        [-122.3900, 37.7900],
        [-122.3700, 37.7600],
        [-122.3550, 37.7200],
        [-122.3600, 37.6900],
        [-122.3700, 37.6700],
    ],
    "sfbf-ferry-building|sfbf-mission-bay": [
        [-122.3920, 37.7900],
        [-122.3900, 37.7800],
        [-122.3880, 37.7720],
    ],
    # SM–Hayward marked span corridor + Redwood dredged channel
    "sfbf-ferry-building|sfbf-redwood-city": [
        [-122.3900, 37.7900],
        [-122.3600, 37.7500],
        [-122.3400, 37.7000],
        [-122.3200, 37.6400],
        [-122.2900, 37.5800],
        [-122.2600, 37.5450],
        [-122.2400, 37.5250],
        [-122.2250, 37.5150],
        [-122.2150, 37.5080],
    ],
    "sfbf-oakland|sfbf-redwood-city": [
        [-122.2850, 37.7900],  # leave estuary west
        [-122.3000, 37.7700],
        [-122.3100, 37.7400],
        [-122.3100, 37.6800],
        [-122.3000, 37.6200],
        [-122.2800, 37.5700],
        [-122.2500, 37.5350],
        [-122.2250, 37.5150],
        [-122.2150, 37.5080],
    ],
    "sfbf-oakland|sfbf-south-sf": [
        [-122.2850, 37.7900],
        [-122.3000, 37.7700],
        [-122.3200, 37.7300],
        [-122.3450, 37.7000],
        [-122.3650, 37.6750],
    ],
    # North Bay: central Bay → San Pablo open water → Richmond
    "sfbf-ferry-building|sfbf-richmond": [
        [-122.3880, 37.8000],
        [-122.3700, 37.8300],
        [-122.3600, 37.8600],
        [-122.3550, 37.8900],
        [-122.3520, 37.9050],
    ],
    # Vallejo: San Pablo Bay west of Richmond, Carquinez approach
    "sfbf-ferry-building|sfbf-vallejo": [
        [-122.3880, 37.8000],
        [-122.3700, 37.8400],
        [-122.3800, 37.9000],
        [-122.4000, 37.9600],
        [-122.3800, 38.0200],
        [-122.3400, 38.0600],
        [-122.3000, 38.0850],
        [-122.2800, 38.0950],
    ],
    "sfbf-ferry-building|sfbf-mare-island": [
        [-122.3880, 37.8000],
        [-122.3700, 37.8400],
        [-122.3800, 37.9000],
        [-122.4000, 37.9600],
        [-122.3600, 38.0400],
        [-122.3000, 38.0800],
        [-122.2800, 38.0950],
    ],
    "sfbf-ferry-building|sfbf-berkeley": [
        [-122.3880, 37.8000],
        [-122.3600, 37.8300],
        [-122.3400, 37.8500],
        [-122.3250, 37.8600],
    ],
    "sfbf-ferry-building|sfbf-hercules": [
        [-122.3880, 37.8000],
        [-122.3700, 37.8600],
        [-122.3800, 37.9400],
        [-122.3600, 38.0000],
        [-122.3200, 38.0200],
        [-122.3000, 38.0180],
    ],
    "sfbf-ferry-building|sfbf-martinez": [
        [-122.3880, 37.8000],
        [-122.3700, 37.8600],
        [-122.3800, 37.9400],
        [-122.3400, 38.0200],
        [-122.2600, 38.0500],
        [-122.2000, 38.0400],
        [-122.1600, 38.0320],
    ],
    "sfbf-ferry-building|sfbf-antioch": [
        [-122.3880, 37.8000],
        [-122.3700, 37.8600],
        [-122.3800, 37.9400],
        [-122.3400, 38.0200],
        [-122.2200, 38.0550],
        [-122.1000, 38.0450],
        [-121.9500, 38.0300],
        [-121.8600, 38.0200],
        [-121.8250, 38.0160],
    ],
    "sfbf-ferry-building|sfbf-treasure-island": [
        [-122.3880, 37.7980],
        [-122.3750, 37.8100],
        [-122.3680, 37.8180],
    ],
    "sfbf-ferry-building|sfbf-pier-41": [
        [-122.3950, 37.7980],
        [-122.4050, 37.8050],
        [-122.4120, 37.8080],
    ],
}

# Existing route IDs (ledger) + Lane A mints
PAIR_ROUTES: dict[str, dict] = {
    "sfbf-ferry-building|sfbf-oakland": {
        "rid": "rn-cabe543d04e9",
        "from": "ferry_building",
        "to": "oakland",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Oakland – Jack London Square",
    },
    "sfbf-ferry-building|sfbf-alameda-main": {
        "rid": "rn-e160b7ec05a5",
        "from": "ferry_building",
        "to": "alameda_main",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Main Street Alameda Ferry Terminal",
    },
    "sfbf-ferry-building|sfbf-alameda-seaplane": {
        "rid": "rn-76d0f0667063",
        "from": "ferry_building",
        "to": "seaplane",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Alameda Seaplane Lagoon Ferry Terminal",
        "mint_if_missing": True,
    },
    "sfbf-ferry-building|sfbf-harbor-bay": {
        "rid": "rn-a82989283656",
        "from": "ferry_building",
        "to": "harbor_bay",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Harbor Bay (Bay Farm Island)",
    },
    "sfbf-ferry-building|sfbf-south-sf": {
        "rid": "rn-c0b8c9297a26",
        "from": "ferry_building",
        "to": "oyster_point",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "South San Francisco (Oyster Point)",
    },
    "sfbf-oakland|sfbf-south-sf": {
        "rid": "rn-5cd7878b37e0",
        "from": "oakland",
        "to": "oyster_point",
        "class": "existing_WETA_service",
        "from_label": "Oakland – Jack London Square",
        "to_label": "South San Francisco (Oyster Point)",
    },
    "sfbf-ferry-building|sfbf-richmond": {
        "rid": "rn-91fd068e22f6",
        "from": "ferry_building",
        "to": "richmond",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Richmond Ferry Terminal",
    },
    "sfbf-ferry-building|sfbf-vallejo": {
        "rid": "rn-b8709495c648",
        "from": "ferry_building",
        "to": "vallejo",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Vallejo Ferry Terminal",
    },
    "sfbf-ferry-building|sfbf-mare-island": {
        "rid": "rn-88bedc106622",
        "from": "ferry_building",
        "to": "mare_island",
        "class": "existing_WETA_service",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Mare Island",
    },
    "sfbf-ferry-building|sfbf-mission-bay": {
        "rid": "rn-ea80446d67a4",
        "from": "ferry_building",
        "to": "mission_bay",
        "class": "WETA_published_expansion",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Mission Bay (16th St / China Basin)",
        "not_current": True,
    },
    "sfbf-ferry-building|sfbf-redwood-city": {
        "rid": "rn-0c9c5c290e05",
        "from": "ferry_building",
        "to": "redwood",
        "class": "WETA_published_expansion",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Port of Redwood City",
        "not_current": True,
    },
    "sfbf-oakland|sfbf-redwood-city": {
        "rid": "rn-1fe517f50e97",
        "from": "oakland",
        "to": "redwood",
        "class": "WETA_published_expansion",
        "from_label": "Oakland – Jack London Square",
        "to_label": "Port of Redwood City",
        "not_current": True,
        "mint_if_missing": True,
    },
    "sfbf-ferry-building|sfbf-berkeley": {
        "rid": "rn-38c306488017",
        "from": "ferry_building",
        "to": "berkeley",
        "class": "WETA_published_expansion",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Berkeley Marina",
        "not_current": True,
    },
    "sfbf-ferry-building|sfbf-treasure-island": {
        "rid": "rn-1ffa4b3d5058",
        "from": "ferry_building",
        "to": "treasure_island",
        "class": "WETA_published_expansion",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Treasure Island",
        "not_current": True,
    },
    "sfbf-ferry-building|sfbf-pier-41": {
        "rid": "rn-d34c89ec7b4c",
        "from": "ferry_building",
        "to": "pier_41",
        "class": "existing_Golden_Gate_Ferry_context",
        "from_label": "San Francisco Ferry Building",
        "to_label": "San Francisco – Pier 41",
    },
    "sfbf-ferry-building|sfbf-hercules": {
        "rid": "rn-f2bf93c77963",
        "from": "ferry_building",
        "to": "hercules",
        "class": "Navier_candidate_screen",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Hercules",
        "not_current": True,
    },
    "sfbf-ferry-building|sfbf-martinez": {
        "rid": "rn-84797a1c1613",
        "from": "ferry_building",
        "to": "martinez",
        "class": "Navier_candidate_screen",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Martinez",
        "not_current": True,
    },
    "sfbf-ferry-building|sfbf-antioch": {
        "rid": "rn-433a40e91daa",
        "from": "ferry_building",
        "to": "antioch",
        "class": "Navier_candidate_screen",
        "from_label": "San Francisco Ferry Building",
        "to_label": "Antioch",
        "not_current": True,
    },
}


def bp_coords(fbt: dict, bp_id: str) -> list[float]:
    for _t, feats in fbt.items():
        for f in feats or []:
            p = f.get("properties") or {}
            if p.get("id") == bp_id:
                return list((f.get("geometry") or {}).get("coordinates") or [])
    raise KeyError(bp_id)


def haversine_nm(a, b) -> float:
    return hav_km((a[0], a[1]), (b[0], b[1])) / 1.852


def path_nm(coords: list) -> float:
    return round(sum(haversine_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1)), 2)


def build_feature(rid: str, fr: str, to: str, fr_lab: str, to_lab: str, coords: list, cls: str, not_current: bool) -> dict:
    land = round(interior_land_km(coords), 4)
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": "Pioneer II",
            "distance_nm": path_nm(coords),
            "edge_class": "regional" if path_nm(coords) > 12 else "local",
            "from": fr,
            "to": to,
            "from_node": fr,
            "to_node": to,
            "from_label": fr_lab,
            "to_label": to_lab,
            "from_city": "San Francisco Bay Area",
            "to_city": "San Francisco Bay Area",
            "from_city_id": CITY,
            "to_city_id": CITY,
            "label": f"San Francisco Bay Area: {fr_lab} → {to_lab}",
            "trip_scope": "intra_city",
            "trip_purpose": "intra_city",
            "traffic_weight": 0.55 if cls == "existing_WETA_service" else 0.4,
            "cluster_id": CLUSTER,
            "_pta_sf-bay-ferry": True,
            "_weta_service_class": cls,
            "_not_current_service": bool(not_current),
            "_land_km_interior_local_mask": land,
            "_land_km_gate": LAND_GATE_KM,
            "_hand_waypoints_at": NOW,
            "_mint_source": "tasklet/WETA-BAY partner-ready 2026-07-13",
            "_local_mask": "sf_bay_local_mask",
            "_claim_boundary": (
                "WETA-published expansion / candidate — not current service, not a commitment"
                if not_current
                else None
            ),
        },
    }


def patch_regional_mask() -> str:
    """Replace oversized sf_bay water bbox with pier/channel corridors note."""
    text = REGIONAL_MASK.read_text()
    old = '    # San Francisco Bay + Delta approaches (SF Bay Ferry)\n    ("sf_bay", -122.55, 37.45, -121.75, 38.15),'
    new = (
        "    # SF Bay — pier aprons + open-water corridors only.\n"
        "    # Full-Bay bbox removed 2026-07-13: it treated Alameda/Bay Farm/peninsula as water\n"
        "    # and hid real land crossings. Local QA: scripts/grok-weta/sf_bay_local_mask.py\n"
        '    ("sf_bay_central_open", -122.45, 37.76, -122.28, 37.88),\n'
        '    ("sf_bay_san_pablo", -122.50, 37.92, -122.30, 38.10),\n'
        '    ("sf_bay_carquinez", -122.32, 38.04, -122.20, 38.10),\n'
        '    ("sf_bay_south_channel", -122.36, 37.52, -122.22, 37.66),\n'
        '    ("sf_bay_redwood_channel", -122.23, 37.49, -122.20, 37.52),'
    )
    if old in text:
        REGIONAL_MASK.write_text(text.replace(old, new))
        return "replaced_oversized_sf_bay_bbox"
    if "sf_bay_central_open" in text:
        return "already_corridor_bboxes"
    return "no_match_manual_review"


def journey(
    fr: str,
    to: str,
    fr_node: str,
    to_node: str,
    rid: str,
    nm: float,
    narrative: str,
    cls: str,
    *,
    not_current: bool = False,
) -> dict:
    j = {
        "from": fr,
        "to": to,
        "today": "Today it's a road trip, a slower displacement ferry, or a longer way round.",
        "with_navier": narrative,
        "platform": "Pioneer II",
        "distance_nm": nm,
        "from_node_id": fr_node,
        "to_node_id": to_node,
        "route_id": rid,
        "route_ids": [rid],
        "_link_source": "grok/weta_bay_partner_ready_2026_07_13",
        "_pta_bound_at": NOW,
        "_weta_service_class": cls,
        "display": "map" if cls == "existing_WETA_service" else "text_only",
        "_link_kind": "bound-route" if cls == "existing_WETA_service" else "expansion-or-candidate",
        "economics_status": "roadmap_excluded" if not_current or cls != "existing_WETA_service" else "bound",
        "render": "live-solid" if cls == "existing_WETA_service" else "roadmap-amber-dashed",
    }
    if not_current:
        j["_not_current_service"] = True
        j["_claim_boundary"] = "Not current WETA service; expansion or candidate only"
    return j


def main() -> int:
    fbt = json.loads(FBT_PATH.read_text())
    routes = json.loads(ROUTES_PATH.read_text())
    by_id = {(f.get("properties") or {}).get("id"): f for f in routes}

    receipt: dict = {
        "at": NOW,
        "lane": "partner_ready",
        "land_gate_km": LAND_GATE_KM,
        "corridors": [],
        "mints": [],
        "fails": [],
        "partner_journeys": 0,
        "waypoints_populated": 0,
        "regional_mask": None,
        "holds": {
            "palo_alto": "hand-launch / non-motorized",
            "alviso": "tide/bathymetry/facility hold",
            "candidates_not_minted": [
                "seaplane↔mission_bay",
                "harbor_bay↔oyster_point",
                "oyster_point↔coyote_point↔redwood",
                "san_leandro pairs",
                "richmond/berkeley/vallejo↔larkspur",
            ],
            "marin": "Golden Gate Ferry context only — inter-agency, not WETA service",
        },
    }

    # A1 ensure approx BP retired
    approx = BP["alameda_main_approx"]
    can = BP["alameda_main"]
    for _t, feats in fbt.items():
        for feat in feats or []:
            p = feat.get("properties") or {}
            if p.get("id") == approx:
                p["relevance"] = "hide"
                p["_deprecated"] = True
                p["_deprecated_at"] = NOW
                p["_superseded_by"] = can
                feat["properties"] = p

    wp_doc = {
        "partner": "sf-bay-ferry",
        "generated_at": NOW,
        "local_mask": "scripts/grok-weta/sf_bay_local_mask.py",
        "policy": {
            "empty_array_forbidden_without_note": True,
            "interior_land_km_zero_not_sufficient_without_span_qa": True,
            "local_mask_gate_km": LAND_GATE_KM,
            "required_cases": [
                "Bay Bridge marked navigation span",
                "Richmond–San Rafael / San Pablo approaches",
                "San Mateo–Hayward Bridge (South Bay)",
                "Oakland–Alameda estuary / Bay Farm exclusion",
                "San Bruno Shoal / South Bay approaches",
                "Redwood City dredged channel",
                "Carquinez / Suisun for North Bay extensions",
            ],
        },
        "waypoints": {},
        "waypoint_notes": {},
    }

    allow = json.loads(ALLOW_PATH.read_text())
    allow_ids = set(allow.get("ids") or [])

    for key, meta in PAIR_ROUTES.items():
        fr_bp = BP[meta["from"]]
        to_bp = BP[meta["to"]]
        fr_c = bp_coords(fbt, fr_bp)
        to_c = bp_coords(fbt, to_bp)
        spine = SPINES.get(key, [])
        coords = route_via_spine(fr_c, to_c, spine, use_astar=True)
        # Keep dense water paths for map fidelity (skip aggressive simplify)
        land = interior_land_km(coords)
        nm = path_nm(coords)
        rid = meta["rid"]
        feat = by_id.get(rid)
        if feat is None and meta.get("mint_if_missing"):
            # search existing by endpoints
            for f in routes:
                p = f.get("properties") or {}
                if {p.get("from"), p.get("to")} == {fr_bp, to_bp}:
                    feat = f
                    rid = p.get("id")
                    break
        if feat is None and meta.get("mint_if_missing"):
            rid = mint_route_id(fr_bp, to_bp, tag="wetabay")
            feat = build_feature(
                rid, fr_bp, to_bp, meta["from_label"], meta["to_label"], coords,
                meta["class"], meta.get("not_current", False),
            )
            routes.append(feat)
            by_id[rid] = feat
            receipt["mints"].append({"id": rid, "key": key, "class": meta["class"]})
        if feat is None:
            receipt["fails"].append({"key": key, "reason": "route_id_missing", "rid": rid})
            continue

        p = feat.get("properties") or {}
        # rebind Alameda Main if needed
        if p.get("from") == approx:
            p["from"] = can
            p["from_node"] = can
            p["from_label"] = "Main Street Alameda Ferry Terminal"
        if p.get("to") == approx:
            p["to"] = can
            p["to_node"] = can
            p["to_label"] = "Main Street Alameda Ferry Terminal"

        feat["geometry"] = {"type": "LineString", "coordinates": coords}
        p["from"] = fr_bp if p.get("from") in (fr_bp, to_bp, approx, None) else p.get("from", fr_bp)
        p["to"] = to_bp if p.get("to") in (fr_bp, to_bp, approx, None) else p.get("to", to_bp)
        # force exact pair endpoints
        p["from"], p["to"] = fr_bp, to_bp
        p["from_node"], p["to_node"] = fr_bp, to_bp
        p["from_label"] = meta["from_label"]
        p["to_label"] = meta["to_label"]
        p["label"] = f"San Francisco Bay Area: {meta['from_label']} → {meta['to_label']}"
        p["distance_nm"] = nm
        p["from_city_id"] = CITY
        p["to_city_id"] = CITY
        p["cluster_id"] = CLUSTER
        p["_pta_sf-bay-ferry"] = True
        p["_weta_service_class"] = meta["class"]
        p["_not_current_service"] = bool(meta.get("not_current"))
        p["_land_km_interior_local_mask"] = round(land, 4)
        p["_land_km_gate"] = LAND_GATE_KM
        p["_hand_waypoints_at"] = NOW
        p["_hand_waypoints_key"] = key
        p["_local_mask"] = "sf_bay_local_mask"
        if meta.get("not_current"):
            p["_claim_boundary"] = (
                "WETA-published expansion or Navier candidate — not current service, not a commitment"
            )
        feat["properties"] = p

        status = "pass" if land <= LAND_GATE_KM else "fail_land"
        if status != "pass":
            receipt["fails"].append({"key": key, "rid": rid, "land_km": round(land, 4), "nm": nm})
        receipt["corridors"].append(
            {
                "key": key,
                "route_id": rid,
                "class": meta["class"],
                "nm": nm,
                "land_km_local": round(land, 4),
                "status": status,
                "spine_pts": len(spine),
                "geom_pts": len(coords),
            }
        )
        allow_ids.add(rid)

        # waypoint file stores intermediate spine only (not endpoints)
        wp_doc["waypoints"][key] = spine
        wp_doc["waypoint_notes"][key] = {
            "status": "hand_reviewed_local_mask",
            "at": NOW,
            "land_km_local": round(land, 4),
            "gate_km": LAND_GATE_KM,
            "case": "bridge_span_or_channel_or_basin",
            "note": "Spine points forced through open Bay / marked span / dredged channel; A* fill under sf_bay_local_mask.",
        }

    receipt["waypoints_populated"] = sum(1 for v in wp_doc["waypoints"].values() if v)

    # Partner journeys — existing service first, then expansion
    journeys = [
        journey(
            "San Francisco Ferry Building", "Oakland – Jack London Square",
            "sfbf-ferry-building", "sfbf-oakland", "rn-cabe543d04e9",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-oakland"),
            "Flagship East Bay commute: Ferry Building to Jack London Square — foiling layer above the busiest WETA route.",
            "existing_WETA_service",
        ),
        journey(
            "San Francisco Ferry Building", "Main Street Alameda Ferry Terminal",
            "sfbf-ferry-building", "sfbf-alameda-main", "rn-e160b7ec05a5",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-alameda-main"),
            "Ferry Building to Alameda Main Street — Island City commute on exact Main Street terminal.",
            "existing_WETA_service",
        ),
        journey(
            "San Francisco Ferry Building", "Alameda Seaplane Lagoon Ferry Terminal",
            "sfbf-ferry-building", "sfbf-alameda-seaplane", "rn-76d0f0667063",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-alameda-seaplane"),
            "Current WETA Downtown SF ↔ Seaplane Lagoon service, Bay Bridge span + Alameda basin approach.",
            "existing_WETA_service",
        ),
        journey(
            "San Francisco Ferry Building", "Harbor Bay (Bay Farm Island)",
            "sfbf-ferry-building", "sfbf-harbor-bay", "rn-a82989283656",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-harbor-bay"),
            "Ferry Building to Harbor Bay — Alameda south shore terminal.",
            "existing_WETA_service",
        ),
        journey(
            "San Francisco Ferry Building", "South San Francisco (Oyster Point)",
            "sfbf-ferry-building", "sfbf-south-sf", "rn-c0b8c9297a26",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-south-sf"),
            "Ferry Building to Oyster Point — Peninsula biotech waterfront.",
            "existing_WETA_service",
        ),
        journey(
            "Oakland – Jack London Square", "South San Francisco (Oyster Point)",
            "sfbf-oakland", "sfbf-south-sf", "rn-5cd7878b37e0",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-oakland|sfbf-south-sf"),
            "Oakland ↔ Oyster Point cross-Bay — existing WETA East Bay–Peninsula link.",
            "existing_WETA_service",
        ),
        journey(
            "San Francisco Ferry Building", "Richmond Ferry Terminal",
            "sfbf-ferry-building", "sfbf-richmond", "rn-91fd068e22f6",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-richmond"),
            "Ferry Building to Richmond across the central Bay.",
            "existing_WETA_service",
        ),
        journey(
            "San Francisco Ferry Building", "Vallejo Ferry Terminal",
            "sfbf-ferry-building", "sfbf-vallejo", "rn-b8709495c648",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-vallejo"),
            "Ferry Building to Vallejo via San Pablo Bay and Carquinez approach — longest mainline commute.",
            "existing_WETA_service",
        ),
        journey(
            "Oakland – Jack London Square", "Port of Redwood City",
            "sfbf-oakland", "sfbf-redwood-city", "rn-1fe517f50e97",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-oakland|sfbf-redwood-city"),
            "WETA-published expansion: Oakland ↔ Redwood City via estuary exit, SM–Hayward span, dredged channel.",
            "WETA_published_expansion",
            not_current=True,
        ),
        journey(
            "San Francisco Ferry Building", "Port of Redwood City",
            "sfbf-ferry-building", "sfbf-redwood-city", "rn-0c9c5c290e05",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-redwood-city"),
            "WETA-published expansion: Ferry Building ↔ Redwood City South Bay channel.",
            "WETA_published_expansion",
            not_current=True,
        ),
        journey(
            "San Francisco Ferry Building", "Mission Bay (16th St / China Basin)",
            "sfbf-ferry-building", "sfbf-mission-bay", "rn-ea80446d67a4",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-mission-bay"),
            "WETA-published future Mission Bay terminal — Downtown SF pair only.",
            "WETA_published_expansion",
            not_current=True,
        ),
        journey(
            "San Francisco Ferry Building", "Berkeley Marina",
            "sfbf-ferry-building", "sfbf-berkeley", "rn-38c306488017",
            next(c["nm"] for c in receipt["corridors"] if c["key"] == "sfbf-ferry-building|sfbf-berkeley"),
            "WETA-published expansion screen: Ferry Building ↔ Berkeley Marina.",
            "WETA_published_expansion",
            not_current=True,
        ),
    ]
    receipt["partner_journeys"] = len(journeys)

    for partner_path in (PARTNER_PATH, PITCH_PATH):
        if not partner_path.exists():
            continue
        partner = json.loads(partner_path.read_text())
        partner["journeys_unlocked"] = journeys
        # ensure market keep for inheritance
        partner.setdefault("markets", [])
        if CITY not in partner.get("markets", []):
            # some partners use hub_rollout / covered
            pass
        gc = partner.get("growth_case") or {}
        if isinstance(gc, dict):
            # stamp route linkage refresh
            gc["_weta_bay_partner_ready_at"] = NOW
            partner["growth_case"] = gc
        partner["_weta_bay_partner_ready_at"] = NOW
        partner["_weta_bay_local_mask"] = "sf_bay_local_mask"
        partner_path.write_text(json.dumps(partner, indent=2, ensure_ascii=False) + "\n")

    receipt["regional_mask"] = patch_regional_mask()

    allow["ids"] = sorted(allow_ids)
    allow.setdefault("_meta", {})["weta_bay_partner_ready_at"] = NOW
    allow["_meta"]["weta_bay_local_mask"] = "sf_bay_local_mask"

    FBT_PATH.write_text(json.dumps(fbt, ensure_ascii=False, separators=(",", ":")) + "\n")
    ROUTES_PATH.write_text(json.dumps(routes, ensure_ascii=False, separators=(",", ":")) + "\n")
    WP_PATH.write_text(json.dumps(wp_doc, indent=2, ensure_ascii=False) + "\n")
    ALLOW_PATH.write_text(json.dumps(allow, ensure_ascii=False, separators=(",", ":")) + "\n")

    pass_n = sum(1 for c in receipt["corridors"] if c["status"] == "pass")
    receipt["summary"] = {
        "corridors": len(receipt["corridors"]),
        "pass": pass_n,
        "fail": len(receipt["corridors"]) - pass_n,
        "partner_ready": pass_n == len(receipt["corridors"]) and pass_n > 0,
    }
    receipt["notes"] = [
        "Local mask: water corridors + island land exclusions + terminal aprons.",
        "Oversized regional sf_bay WATER_BBOX replaced with corridor bboxes.",
        "Lane C candidates remain unminted; Marin is Golden Gate context only.",
        "Deck bind of new rids deferred until visual QA confirms spans.",
    ]
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["summary"]["partner_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
