#!/usr/bin/env python3
"""WS-8 — Re-mint Dubai Creek/Canal water-bus spine with creek-following waypoints."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    densify,
    load_json,
    make_route_feature,
    mint_route_id,
    route_features,
    route_id_of,
    save_routes,
)
from route_land_qa import interior_land_km as qa_land  # noqa: E402

REGISTER_PATH = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "DUBAI-DESPAGHETTI.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
FBT_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
REPORT_PATH = ROOT / "grok-routing-output" / "dubai-creek-spine-report.json"

CITY_ID = "dubai-uae"
CLUSTER_ID = "dubai-uae"
TAG = "dubai-creek-spine"
LAND_MAX_KM = 0.12

NODE_BP: dict[str, str] = {
    "Dubai Festival City Marina": "bp-5c7aaead40",
    "Al Seef Marine Transport Station (Dubai Creek)": "bp-a27aa3915d",
    "Dubai Old Souq Marine Transport Station": "bp-00a6462e28",
    "Al Fahidi Marine Transport Station": "bp-f0c3eca1bd",
    "Al Ghubaiba Marine Transport Station (Ferry + Water Bus + Abra)": "bp-01beccf900",
    "Baniyas Marine Transport Station 1": "bp-cfa4872726",
    "Business Bay Marine Transport Station": "bp-42a15eb6e1",
    "Marasi Business Bay Marina": "bp-4609de30c5",
    "Dubai Canal Marine Transport Station 1": "bp-f3f4b807f2",
}

# Full creek/canal chains per segment (lng, lat) — endpoints included
SEGMENT_CHAINS: dict[tuple[str, str], list[tuple[float, float]]] = {
    ("Dubai Festival City Marina", "Al Seef Marine Transport Station (Dubai Creek)"): [
        (55.34928, 25.22223),
        (55.346, 25.225),
        (55.343, 25.228),
        (55.340, 25.231),
        (55.337, 25.234),
        (55.334, 25.237),
        (55.331, 25.240),
        (55.328, 25.243),
        (55.325, 25.246),
        (55.322, 25.249),
        (55.319, 25.252),
        (55.316, 25.255),
        (55.313, 25.257),
        (55.310, 25.258),
        (55.307, 25.259),
        (55.304, 25.259),
        (55.3005, 25.2585),
    ],
    ("Al Seef Marine Transport Station (Dubai Creek)", "Dubai Old Souq Marine Transport Station"): [
        (55.3005, 25.2585),
        (55.298, 25.260),
        (55.296, 25.262),
        (55.29519, 25.26489),
    ],
    ("Dubai Old Souq Marine Transport Station", "Al Fahidi Marine Transport Station"): [
        (55.29519, 25.26489),
        (55.297, 25.265),
        (55.30074, 25.26544),
    ],
    ("Al Fahidi Marine Transport Station", "Al Ghubaiba Marine Transport Station (Ferry + Water Bus + Abra)"): [
        (55.30074, 25.26544),
        (55.296, 25.265),
        (55.29112, 25.26508),
    ],
    ("Al Ghubaiba Marine Transport Station (Ferry + Water Bus + Abra)", "Baniyas Marine Transport Station 1"): [
        (55.29112, 25.26508),
        (55.296, 25.264),
        (55.302, 25.263),
        (55.31158, 25.26252),
    ],
    ("Baniyas Marine Transport Station 1", "Business Bay Marine Transport Station"): [
        (55.31158, 25.26252),
        (55.310, 25.260),
        (55.305, 25.255),
        (55.298, 25.248),
        (55.290, 25.240),
        (55.280, 25.225),
        (55.270, 25.205),
        (55.262, 25.190),
        (55.26014, 25.18342),
    ],
    ("Business Bay Marine Transport Station", "Marasi Business Bay Marina"): [
        (55.26014, 25.18342),
        (55.268, 25.185),
        (55.276, 25.186),
        (55.284, 25.187),
        (55.2874, 25.18793),
    ],
    ("Marasi Business Bay Marina", "Dubai Canal Marine Transport Station 1"): [
        (55.2874, 25.18793),
        (55.280, 25.189),
        (55.270, 25.191),
        (55.260, 25.193),
        (55.250, 25.195),
        (55.240, 25.197),
        (55.2334, 25.19799),
    ],
}

CHAIN = [
    "Dubai Festival City Marina",
    "Al Seef Marine Transport Station (Dubai Creek)",
    "Dubai Old Souq Marine Transport Station",
    "Al Fahidi Marine Transport Station",
    "Al Ghubaiba Marine Transport Station (Ferry + Water Bus + Abra)",
    "Baniyas Marine Transport Station 1",
    "Business Bay Marine Transport Station",
    "Marasi Business Bay Marina",
    "Dubai Canal Marine Transport Station 1",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def chain_coords(points: list[tuple[float, float]], n: int = 10) -> list[list[float]]:
    out: list[list[float]] = []
    for i in range(len(points) - 1):
        seg = densify(points[i], points[i + 1], n)
        out.extend(seg if not out else seg[1:])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    fbt = load_json(FBT_PATH)
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    routes = route_features(load_json(ROUTES_PATH))
    existing = {route_id_of(f) for f in routes}

    minted: list[dict] = []
    errors: list[str] = []

    for i in range(len(CHAIN) - 1):
        from_name = CHAIN[i]
        to_name = CHAIN[i + 1]
        from_bp = NODE_BP.get(from_name)
        to_bp = NODE_BP.get(to_name)
        if not from_bp or not to_bp:
            errors.append(f"missing bp: {from_name} -> {to_name}")
            continue

        chain_pts = SEGMENT_CHAINS.get((from_name, to_name))
        if not chain_pts:
            errors.append(f"no chain: {from_name} -> {to_name}")
            continue

        coords = chain_coords(chain_pts, n=10)
        land_km = qa_land(coords)
        if land_km > LAND_MAX_KM:
            errors.append(f"land {land_km:.2f}km: {from_name} -> {to_name}")
            continue

        rid = mint_route_id(from_bp, to_bp, TAG)
        if rid in existing:
            continue

        from_row = bp_idx[from_bp]
        to_row = bp_idx[to_bp]
        feat = make_route_feature(
            from_bp,
            to_bp,
            from_row["name"],
            to_row["name"],
            CITY_ID,
            CITY_ID,
            coords,
            cities,
            source=TAG,
            land_km=land_km,
        )
        props = feat["properties"]
        props["id"] = rid
        props["cluster_id"] = CLUSTER_ID
        props["edge_class"] = "intra-city"
        minted.append(feat)
        existing.add(rid)

    report = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "segments_attempted": len(CHAIN) - 1,
        "minted": len(minted),
        "route_ids": [route_id_of(f) for f in minted],
        "errors": errors,
    }
    print(f"  Dubai creek spine: {len(minted)} routes minted · {len(errors)} errors")

    if args.apply and minted:
        save_routes(ROUTES_PATH, routes + minted)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 1 if errors and not minted else 0


if __name__ == "__main__":
    raise SystemExit(main())