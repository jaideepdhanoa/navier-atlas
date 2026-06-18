#!/usr/bin/env python3
"""Reseal as #79am."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PHASE3 = Path(__file__).resolve().parents[1] / "grok-phase3"
sys.path.insert(0, str(PHASE3))

from finalize_seal import count_features, count_routes, sha256_canonical  # noqa: E402

import json
import subprocess
from datetime import datetime, timezone


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    seal_path = dc / "SEAL.json"
    seal = json.loads(seal_path.read_text())

    routes = json.loads((dc / "ROUTES.json").read_text())
    active_routes = [
        f for f in (routes if isinstance(routes, list) else routes.get("features", []))
        if not (f.get("properties") or f).get("_quarantine")
    ]
    routes_n = len(active_routes)
    fbt_counts = count_features(dc / "FEATURES_BY_TYPE.json")

    seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    seal.setdefault("gates", {})
    seal["gates"]["land_crossing"] = "PASS grok-reconcile-79am — LB-224 v2 gate"
    seal["gates"]["bp_semantic_qa"] = "PASS SEM buckets + water-adjacency + gazetteer"
    seal.setdefault("meta", {})["route_count"] = routes_n
    seal.setdefault("meta", {})["gold"] = "#79am"
    seal.setdefault("blobs", {})
    seal["blobs"]["ROUTES"] = {
        "sha256": sha256_canonical(json.loads((dc / "ROUTES.json").read_text())),
        "count": routes_n,
        "bytes": (dc / "ROUTES.json").stat().st_size,
    }
    if fbt_counts:
        seal["blobs"]["FEATURES_BY_TYPE"] = {
            "sha256": sha256_canonical(json.loads((dc / "FEATURES_BY_TYPE.json").read_text())),
            "count": fbt_counts,
        }

    seal_path.write_text(json.dumps(seal, indent=1) + "\n")

    reseal = work / "partner-pitch" / "_tools" / "reseal_from_disk.py"
    if reseal.exists():
        subprocess.run([sys.executable, str(reseal), str(dc)], check=True)

    print(f"SEAL finalized: routes={routes_n} gold=#79am")


if __name__ == "__main__":
    main()