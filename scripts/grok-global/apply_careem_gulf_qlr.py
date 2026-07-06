#!/usr/bin/env python3
"""WS-3 — Careem Gulf Q-LR aspirational overlay (Careem only, not inherited by Noon)."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_coastal_path,
    load_json,
    make_route_feature,
    mint_route_id,
    route_features,
    route_id_of,
    save_routes,
)
from bolt_yango_shared import load_land_mask  # noqa: E402

GULF_PATH = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "GULF-AND-GROUPS.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "careem-gulf-qlr-report.json"

# Offshore hand-waypoints — route around Qatar peninsula (open Gulf, no land crossing)
GULF_WAYPOINTS: dict[tuple[str, str], list[tuple[float, float]]] = {
    ("uae-dubai-alghubaiba", "qatar-lusail"): [(55.8, 25.0), (54.5, 24.8), (52.5, 25.0)],
    ("uae-abudhabi-irshad", "qatar-lusail"): [(54.8, 24.7), (53.0, 24.5), (52.0, 25.0)],
    ("uae-dubai-alghubaiba", "bahrain-manama"): [(55.5, 25.2), (53.5, 25.5), (51.5, 26.0)],
    ("uae-abudhabi-irshad", "bahrain-manama"): [(54.5, 24.8), (53.0, 25.5), (51.0, 26.0)],
    ("uae-dubai-alghubaiba", "ksa-dammam"): [(55.5, 25.0), (53.5, 25.8), (51.5, 26.2)],
}

EDGE_SPECS = [
    ("uae-dubai-alghubaiba", "qatar-lusail", "UAE Dubai Al Ghubaiba → Qatar Lusail", "dubai-uae", None),
    ("uae-abudhabi-irshad", "qatar-lusail", "UAE Abu Dhabi Irshad → Qatar Lusail", "abu-dhabi-uae", None),
    ("uae-dubai-alghubaiba", "bahrain-manama", "UAE Dubai Al Ghubaiba → Bahrain Manama", "dubai-uae", None),
    ("uae-abudhabi-irshad", "bahrain-manama", "UAE Abu Dhabi Irshad → Bahrain Manama", "abu-dhabi-uae", None),
    ("uae-dubai-alghubaiba", "ksa-dammam", "UAE Dubai Al Ghubaiba → KSA Dammam", "dubai-uae", None),
]

ANCHOR_COORDS = {
    "uae-dubai-alghubaiba": (55.291, 25.265),
    "uae-abudhabi-irshad": (54.359, 24.536),
    "qatar-lusail": (51.526, 25.422),
    "bahrain-manama": (50.585, 26.248),
    "ksa-dammam": (50.202, 26.474),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def anchor_bp_id(name: str) -> str:
    return "bp-careem-gulf-" + name.lower().replace(" ", "-").replace("_", "-")


def mint_qlr_edge(
    from_id: str,
    from_label: str,
    from_city: str,
    to_id: str,
    to_label: str,
    to_city: str | None,
    coords: list,
    cities: dict[str, str],
) -> dict:
    feat = make_route_feature(
        from_id,
        to_id,
        from_label,
        to_label,
        from_city,
        to_city,
        coords,
        cities,
        source="careem-gulf-qlr",
    )
    p = feat["properties"]
    p["platform"] = "Quanta-LR"
    p["aspirational"] = True
    p["_render"] = "roadmap-amber-dashed"
    p["_link_status"] = "roadmap"
    p["_careem_gulf_qlr"] = True
    p["cluster_id"] = None  # NOT stamped into uae — overlay only
    p["id"] = mint_route_id(from_id, to_id, tag="careem-gulf-qlr")
    return feat


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    anchors_doc = load_json(GULF_PATH).get("careem_gulf_anchors") or {}
    routes = route_features(load_json(ROUTES_PATH))
    existing_ids = {route_id_of(r) for r in routes}
    mask = load_land_mask()
    cities: dict[str, str] = {}

    minted: list[dict] = []
    overlay_entries: list[dict] = []
    for from_key, to_key, label, from_city, to_city in EDGE_SPECS:
        from_id = anchor_bp_id(from_key)
        to_id = anchor_bp_id(to_key)
        wps = GULF_WAYPOINTS.get((from_key, to_key))
        fa = ANCHOR_COORDS[from_key]
        tb = ANCHOR_COORDS[to_key]
        manual = [(w[0], w[1]) for w in wps] if wps else None
        coords = build_coastal_path(fa, tb, mask, manual_waypoints=manual)
        parts = label.split(" → ")
        from_label, to_label = parts[0], parts[1]
        feat = mint_qlr_edge(from_id, from_label, from_city, to_id, to_label, to_city, coords, cities)
        rid = feat["properties"]["id"]
        if rid not in existing_ids:
            minted.append(feat)
            existing_ids.add(rid)
        overlay_entries.append(
            {
                "route_id": rid,
                "from_label": from_label,
                "to_label": to_label,
                "cluster_id": None,
                "class": "careem-gulf-qlr",
            }
        )

    report = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "minted": len(minted),
        "overlay_entries": overlay_entries,
    }
    print(f"  Careem Gulf Q-LR: {len(minted)} routes minted · {len(overlay_entries)} overlay entries")

    if args.apply:
        routes.extend(minted)
        save_routes(ROUTES_PATH, routes)
        for pid in ("careem",):
            path = PARTNERS_DIR / f"{pid}.json"
            doc = json.loads(path.read_text())
            scope = dict(doc.get("_map_scope") or {})
            scope["aspirational_gulf_qlr"] = overlay_entries
            scope["aspirational_gulf_qlr_note"] = "Careem-only Q-LR overlay; excluded from operational inheritance"
            doc["_map_scope"] = scope
            text = json.dumps(doc, indent=2) + "\n"
            path.write_text(text)
            pitch = PITCH_DIR / f"{pid}.json"
            if pitch.parent.is_dir():
                pitch.write_text(text)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())