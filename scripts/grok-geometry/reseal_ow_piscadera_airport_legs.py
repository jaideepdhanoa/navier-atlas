#!/usr/bin/env python3
"""PR #100 — reseal Ocean Whisperer airport legs as short leeward Piscadera embarkations."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from abc_offshore_waypoints import build_offshore_coords  # noqa: E402
from bolt_yango_routing_shared import load_json, mint_route_id, save_routes  # noqa: E402
from bucketB_shared import densify, hav_nm  # noqa: E402
from route_land_qa import evaluate_route, path_detour_ratio, curacao_leeward_bbox_ok  # noqa: E402

TAG = "abc_islands"
BP = {
    "curacao-curacao__piscadera-bay-resort-cluster": (-68.97, 12.12),
    "curacao-curacao__sandals-royal-curacao-spanish-water": (-68.85, 12.067),
    "curacao-curacao__baoase-luxury-resort": (-68.90, 12.094),
}

# Short leeward south-coast runs (Option A — air demand, Piscadera embark).
NEW_LEGS = [
    (
        "curacao-curacao__piscadera-bay-resort-cluster",
        "curacao-curacao__sandals-royal-curacao-spanish-water",
        [(-68.92, 12.10), (-68.88, 12.08)],
    ),
    (
        "curacao-curacao__piscadera-bay-resort-cluster",
        "curacao-curacao__baoase-luxury-resort",
        [(-68.94, 12.11)],
    ),
]

RETIRED_HATO_PAIRS = [
    ("curacao-curacao__hato-airport-waterfront", "curacao-curacao__sandals-royal-curacao-spanish-water"),
    ("curacao-curacao__hato-airport-waterfront", "curacao-curacao__baoase-luxury-resort"),
    ("curacao-curacao__hato-airport-waterfront", "curacao-curacao__spanish-water-jan-thiel"),
]


def pair_key(a: str, b: str) -> str:
    return f"{a}|{b}"


def build_coords(a: tuple[float, float], b: tuple[float, float], wps: list[tuple[float, float]]) -> list[list[float]]:
    pts = [a] + wps + [b]
    coords: list[list[float]] = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 18)
        coords.extend(seg if not coords else seg[1:])
    return coords


def main() -> int:
    routes_path = ROOT / "data-clean/ROUTES.json"
    routes = load_json(routes_path)
    if not isinstance(routes, list):
        routes = routes.get("features", routes)
    by_id = {(r.get("properties") or r).get("id"): r for r in routes}

    built = []
    for from_n, to_n, wps in NEW_LEGS:
        rid = mint_route_id(from_n, to_n, TAG)
        a, b = BP[from_n], BP[to_n]
        coords = build_coords(a, b, wps)
        qa = evaluate_route(coords)
        detour = path_detour_ratio(coords)
        if not qa["qa_pass"]:
            print(f"FAIL land QA {rid}", file=sys.stderr)
            return 1
        if detour > 1.35:
            print(f"FAIL detour ×{detour:.2f} {rid}", file=sys.stderr)
            return 1
        if not curacao_leeward_bbox_ok(coords):
            print(f"FAIL leeward bbox {rid}", file=sys.stderr)
            return 1
        straight = round(hav_nm(a, b), 1)
        path_nm = round(sum(hav_nm((coords[i][0], coords[i][1]), (coords[i + 1][0], coords[i + 1][1])) for i in range(len(coords) - 1)), 1)
        feat = by_id.get(rid) or {
            "type": "Feature",
            "properties": {"id": rid, "tag": TAG},
            "geometry": {"type": "LineString", "coordinates": []},
        }
        feat["geometry"] = {"type": "LineString", "coordinates": coords}
        p = feat.setdefault("properties", {})
        p.update(
            {
                "id": rid,
                "from_node_id": from_n,
                "to_node_id": to_n,
                "distance_nm": path_nm,
                "distance_nm_geom": path_nm,
                "distance_nm_straight": straight,
                "interior_land_km": qa["interior_land_km"],
                "render_smooth": True,
                "shippable": True,
                "_ow_piscadera_reseal_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )
        by_id[rid] = feat
        built.append({"route_id": rid, "from": from_n, "to": to_n, "distance_nm": path_nm, "straight_nm": straight, "detour": round(detour, 2)})

    retired = []
    for from_n, to_n in RETIRED_HATO_PAIRS:
        rid = mint_route_id(from_n, to_n, TAG)
        feat = by_id.get(rid)
        if not feat:
            continue
        p = feat.setdefault("properties", {})
        p["shippable"] = False
        p["_ow_retired_reason"] = "windward circumnavigation — superseded by Piscadera leeward embark (PR #100)"
        p["render"] = "roadmap-amber"
        retired.append(rid)

    save_routes(routes_path, list(by_id.values()))

    report_path = ROOT / "grok-routing-output/abc-islands-seal-report.json"
    report = load_json(report_path)
    rbp = report.setdefault("route_by_pair", {})
    for row in built:
        rbp[pair_key(row["from"], row["to"])] = row["route_id"]
        rbp[pair_key(row["to"], row["from"])] = row["route_id"]
    routes_built = {r.get("route_id"): r for r in (report.get("routes_built") or []) if r.get("route_id")}
    for row in built:
        routes_built[row["route_id"]] = row
    report["routes_built"] = list(routes_built.values())
    report["ow_piscadera_reseal_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report_path.write_text(json.dumps(report, indent=2) + "\n")

    out = ROOT / "grok-routing-output/ow-piscadera-reseal-report.json"
    out.write_text(json.dumps({"built": built, "retired": retired}, indent=2) + "\n")
    print(json.dumps({"built": built, "retired": retired}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())