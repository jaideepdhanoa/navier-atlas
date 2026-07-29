#!/usr/bin/env python3
"""SSA authority deck — mint Woods Hole <-> Oak Bluffs (SSA published route, geometry gap).

Endpoints reuse sealed anchors:
  - Woods Hole terminal: exact endpoint coordinate of sealed route ics-c7c6e76d27
    (node bp-ssa-woods-hole)
  - Oak Bluffs: bp-83a62832de (Steamship Authority Oak Bluffs Terminal, operational)

Validation: hand waypoints (around Nobska Point, across Vineyard Sound, east of
East Chop) + high-zoom visual QA (northeast/Singapore standard); coarse land-mask
backstop via interior_land_km.
Run: python3 mint_wh_oakbluffs_2026_07_29.py /tmp/na [--apply]
"""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "/tmp/na")
APPLY = "--apply" in sys.argv
sys.path.insert(0, str(REPO / "scripts/grok-bolt-yango"))
from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km, load_json, load_land_mask, path_length_km, save_routes,
)

DC = REPO / "data-clean"
SEAL_LANE = "ssa-authority-2026-07-29"
NOW = datetime.now(timezone.utc).isoformat()

WH = (-70.671325, 41.522835)      # sealed endpoint of ics-c7c6e76d27 (bp-ssa-woods-hole)
OB = (-70.5559054, 41.4579385)    # bp-83a62832de

PATH = [
    WH,
    (-70.6690, 41.5140),   # clear Great Harbor, south
    (-70.6560, 41.5070),   # round Nobska Point (stay offshore)
    (-70.6180, 41.4890),   # mid Vineyard Sound
    (-70.5840, 41.4760),   # off West Chop, standing east
    (-70.5590, 41.4690),   # east of East Chop
    (-70.5545, 41.4620),   # Oak Bluffs approach
    OB,
]

def main() -> int:
    routes_raw = load_json(DC / "ROUTES.json")
    # duplicate guard
    for r in routes_raw if isinstance(routes_raw, list) else routes_raw.get("features", []):
        p = r.get("properties", {})
        ns = {p.get("from_node"), p.get("to_node")}
        if ns == {"bp-ssa-woods-hole", "bp-83a62832de"}:
            print("ALREADY EXISTS:", p.get("id")); return 1
    km = path_length_km(PATH)
    nm = km / 1.852
    mask = load_land_mask()
    land_km = interior_land_km(PATH, mask)
    print(f"path {len(PATH)} pts · {km:.2f} km · {nm:.2f} nm · interior land {land_km:.3f} km (coarse backstop)")
    # route feature built explicitly to match sealed northeast mints
    rid = "rn-ssa-wh-oakbluffs"
    feat = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": [list(c) for c in PATH]},
        "properties": {
            "id": rid,
            "route_key": rid,
            "from": "Woods Hole (Falmouth) — Vineyard mainland gateway",
            "from_label": "Woods Hole",
            "from_node": "bp-ssa-woods-hole",
            "from_city_id": "cape-cod-islands-usa",
            "to": "Steamship Authority Oak Bluffs Terminal",
            "to_label": "Oak Bluffs",
            "to_node": "bp-83a62832de",
            "to_city_id": "cape-cod-islands-usa",
            "cluster_city_id": "cape-cod-islands-usa",
            "edge_class": "island-hop",
            "distance_nm": round(nm, 1),
            "service_status": "current_scheduled",
            "operator_note": "Steamship Authority published seasonal passenger route (see SSA schedules)",
            "_seal_lane": SEAL_LANE,
            "_geometry_method": "hand-waypoints+visual-qa",
            "_minted_at": NOW,
        },
    }
    if APPLY:
        (routes_raw if isinstance(routes_raw, list) else routes_raw["features"]).append(feat)
        save_routes(DC / "ROUTES.json", routes_raw)
        print("APPLIED", rid)
    else:
        print("DRY RUN — pass --apply to write", rid)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
