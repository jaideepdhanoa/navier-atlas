#!/usr/bin/env python3
"""Emit slim per-cluster sealed-corridor manifests for Tasklet Pass 2 curation."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
OUT_DIR = ROOT / "grok-routing-output" / "sealed-corridors"
REPORT_PATH = ROOT / "grok-routing-output" / "sealed-corridor-manifests-report.json"

MANIFEST_FIELDS = (
    "route_id",
    "from",
    "to",
    "from_city_id",
    "to_city_id",
    "distance_nm",
    "cluster_id",
    "_geometry_land_km",
    "from_label",
    "to_label",
    "traffic_weight",
    "trip_scope",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slim_route(feat: dict) -> dict:
    p = feat.get("properties", feat)
    row = {
        "route_id": p.get("id"),
        "from": p.get("from"),
        "to": p.get("to"),
        "from_city_id": p.get("from_city_id"),
        "to_city_id": p.get("to_city_id"),
        "distance_nm": p.get("distance_nm"),
        "cluster_id": p.get("cluster_id"),
        "_geometry_land_km": p.get("_land_km_interior") or p.get("_geometry_land_km"),
        "from_label": p.get("from_label") or p.get("from"),
        "to_label": p.get("to_label") or p.get("to"),
        "traffic_weight": p.get("traffic_weight"),
        "trip_scope": p.get("trip_scope"),
    }
    return {k: row[k] for k in MANIFEST_FIELDS}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write manifest files")
    args = ap.parse_args()

    routes = json.loads(ROUTES_PATH.read_text())
    if isinstance(routes, dict):
        routes = routes.get("features", [])

    by_cluster: dict[str, list[dict]] = {}
    unstamped: list[dict] = []
    for feat in routes:
        p = feat.get("properties", feat)
        cid = p.get("cluster_id")
        if not cid:
            unstamped.append(slim_route(feat))
            continue
        by_cluster.setdefault(cid, []).append(slim_route(feat))

    # UAE city-level manifests for Tasklet cluster::city grouping
    uae_city_clusters = (
        "abu-dhabi-uae",
        "dubai-uae",
        "fujairah-uae",
        "ras-al-khaimah-uae",
        "sharjah-uae",
    )
    for city_cid in uae_city_clusters:
        rows = []
        for pool in (by_cluster.get("uae", []), by_cluster.get("uae-east-coast", [])):
            for r in pool:
                if r["from_city_id"] == city_cid or r["to_city_id"] == city_cid:
                    row = dict(r)
                    row["cluster_id"] = city_cid
                    rows.append(row)
        if rows:
            by_cluster[city_cid] = rows

    manifest_index: dict[str, int] = {}
    if args.apply:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for cid, rows in sorted(by_cluster.items()):
            out = {
                "generated_at": utc_now(),
                "cluster_id": cid,
                "route_count": len(rows),
                "routes": sorted(rows, key=lambda r: r.get("route_id") or ""),
            }
            path = OUT_DIR / f"{cid}.json"
            path.write_text(json.dumps(out, indent=2) + "\n")
            manifest_index[cid] = len(rows)

    receipt = {
        "generated_at": utc_now(),
        "apply": args.apply,
        "clusters_with_manifest": len(by_cluster),
        "unstamped_routes": len(unstamped),
        "manifest_index": manifest_index if args.apply else {k: len(v) for k, v in by_cluster.items()},
        "total_stamped_routes": sum(len(v) for v in by_cluster.values()),
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())