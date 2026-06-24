#!/usr/bin/env python3
"""Re-seal intra-Curaçao north→south legs with offshore waypoints (no overland cut)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bucketB_shared import densify, hav_nm, load_land_mask  # noqa: E402
from bolt_yango_routing_shared import load_json, mint_route_id, save_routes  # noqa: E402
from route_land_qa import interior_land_km as qa_interior_land_km  # noqa: E402

TAG = "abc_islands"
BP_COORDS = {
    "curacao-curacao__hato-airport-waterfront": (-68.958, 12.183),
    "curacao-curacao__sandals-royal-curacao-spanish-water": (-68.85, 12.067),
    "curacao-curacao__baoase-luxury-resort": (-68.90, 12.094),
    "curacao-curacao__spanish-water-jan-thiel": (-68.855, 12.078),
}

OFFSHORE = {
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__sandals-royal-curacao-spanish-water",
    ): [(-69.02, 12.16), (-69.08, 12.10), (-69.10, 12.02), (-69.00, 11.98), (-68.87, 12.05), (-68.85, 12.067)],
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__baoase-luxury-resort",
    ): [(-69.02, 12.16), (-69.08, 12.10), (-69.10, 12.02), (-69.00, 11.98), (-68.92, 12.06), (-68.90, 12.094)],
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__spanish-water-jan-thiel",
    ): [(-69.02, 12.16), (-69.08, 12.10), (-69.10, 12.02), (-69.00, 11.98), (-68.88, 12.06), (-68.86, 12.082)],
}


def build_coords(a, b, wps):
    pts = [a] + list(wps) + [b]
    coords: list[list[float]] = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 22)
        coords.extend(seg if not coords else seg[1:])
    return coords


def main() -> int:
    routes_path = ROOT / "data-clean/ROUTES.json"
    routes = load_json(routes_path)
    if not isinstance(routes, list):
        routes = routes.get("features", routes)

    by_id = {(r.get("properties") or r).get("id"): r for r in routes}
    updated = []

    for (from_n, to_n), wps in OFFSHORE.items():
        rid = mint_route_id(from_n, to_n, TAG)
        feat = by_id.get(rid)
        if not feat:
            print(f"missing route {rid} for {from_n} -> {to_n}", file=sys.stderr)
            continue
        a, b = BP_COORDS[from_n], BP_COORDS[to_n]
        coords = build_coords(a, b, wps)
        land_km = qa_interior_land_km(coords, apron_km=0.25)
        if land_km > 0.08:
            print(f"FAIL land_km={land_km} for {rid}", file=sys.stderr)
            return 1
        dist_nm = round(hav_nm(a, b), 1)
        feat["geometry"] = {"type": "LineString", "coordinates": coords}
        p = feat["properties"]
        p["distance_nm"] = dist_nm
        p["interior_land_km"] = round(land_km, 4)
        p["_abc_offshore_fix_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        updated.append({"route_id": rid, "from": from_n, "to": to_n, "distance_nm": dist_nm, "land_km": land_km})

    save_routes(routes_path, routes)
    report = ROOT / "grok-routing-output/abc-curacao-offshore-fix.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"updated": updated}, indent=2) + "\n")
    print(json.dumps({"updated": len(updated), "routes": updated}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())