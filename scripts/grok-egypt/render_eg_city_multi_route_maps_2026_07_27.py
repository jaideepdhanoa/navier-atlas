#!/usr/bin/env python3
"""Re-render inDrive Egypt city map plates as MULTI-ROUTE city networks.

Jaideep 2026-07-26: city slides must match the Brazil city-slide format —
an Atlas-style map with several example routes per city, not a single
corridor. This re-renders the five Egypt city plates with every sourced,
geometry-backed route shown on the matching slide's route list.

Reuses the fail-closed renderer from render_mx_eg_exact_route_maps_2026_07_23.py
(same basemap, style, plate size, discipline: geometry from data-clean/ROUTES.json
only; fail closed if a route_id is missing geometry).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "scripts/grok-egypt/render_mx_eg_exact_route_maps_2026_07_23.py"
spec = importlib.util.spec_from_file_location("base_renderer", BASE_PATH)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

OUT_EG = ROOT / "deck-studio/assets/indrive-egypt/city-maps"
RECEIPT = (
    ROOT
    / "handoff/partner-map-model/mx-eg-expansion-2026-07-20"
    / "EG-CITY-MULTI-ROUTE-RECEIPT-2026-07-27.json"
)

MAPS = {
    "indrive-hurghada": {
        "out": OUT_EG / "indrive-hurghada-exact-route-map.png",
        "route_ids": [
            "rn-b06f6971ed47",  # Hurghada Marina → Giftun Island (Orange Bay/Mahmya) 6.6nm
            "rn-3d161664de08",  # Hurghada Marina → Sahl Hasheesh Marina 9.5nm
            "rn-bb533d525e01",  # Hurghada Marina → Marina El Gouna 14.2nm
        ],
        "pad": 0.10,
        "left_clear": 0.30,
        "min_span_deg": 0.45,
    },
    "indrive-sharm": {
        "out": OUT_EG / "indrive-sharm-exact-route-map.png",
        "route_ids": [
            "rn-c16a1627130f",  # Sharm Marina → Ras Mohammed (reef jetty) 11.7nm
            "rn-285fc16b29dc",  # Sharm Marina → Sharks Bay Marina 5.4nm
            "rn-42cf3b291895",  # Sharks Bay Marina → Ras Mohammed 15.3nm
        ],
        "pad": 0.10,
        "left_clear": 0.30,
        "min_span_deg": 0.45,
    },
    "indrive-el-gouna": {
        "out": OUT_EG / "indrive-el-gouna-exact-route-map.png",
        "route_ids": [
            "rn-bb533d525e01",  # Hurghada Marina → Marina El Gouna 14.2nm
            "rn-38903e094a00",  # Abu Tig Marina → El Gouna Downtown Marina 1.55nm
        ],
        "pad": 0.08,
        "left_clear": 0.30,
        "min_span_deg": 0.35,
    },
    "indrive-cairo-zamalek-maadi": {
        "out": OUT_EG / "indrive-cairo-zamalek-maadi-exact-route-map.png",
        "route_ids": [
            "rn-c37df5916b71",  # Maadi Corniche → Zamalek 6.26nm
            "rn-df422f98bbae",  # Zamalek → Maspero (Downtown) 0.74nm
        ],
        "pad": 0.04,
        "left_clear": 0.30,
        "min_span_deg": 0.16,
    },
    "indrive-marsa-alam-samadai": {
        "out": OUT_EG / "indrive-marsa-alam-samadai-exact-route-map.png",
        "route_ids": [
            "rn-c28e0cdf10f6",  # Divino Port Ghalib Marina → Sha'ab Samadai 38.7nm
            "rn-732413fb4542",  # Hamata Marina → Qulaan Islands 1.3nm
        ],
        "pad": 0.22,
        "left_clear": 0.30,
        "min_span_deg": 1.0,
    },
}


def main() -> int:
    by_id = base.load_routes()
    results = []
    fail = False
    for key, cfg in MAPS.items():
        print(f"=== {key} ===")
        r = base.render_one(key, cfg, by_id)
        results.append(r)
        n = len(r.get("route_ids_resolved") or [])
        print(" ", r.get("status"), r.get("file") or r.get("reason"), "routes", n)
        if r.get("status") != "ok" or n != len(cfg["route_ids"]):
            fail = True
            print("  FAIL-CLOSED: missing:", r.get("route_ids_missing_skipped") or r.get("missing"))
    receipt = {
        "at": datetime.now(timezone.utc).isoformat(),
        "reason": "Jaideep 2026-07-26 — Egypt city slides must show multi-route city networks (Brazil city-slide format parity)",
        "base_renderer": str(BASE_PATH.relative_to(ROOT)),
        "geometry_source": "data-clean/ROUTES.json",
        "basemap": "CartoDB Dark Matter No Labels",
        "maps": results,
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2))
    print("receipt ->", RECEIPT.relative_to(ROOT))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
