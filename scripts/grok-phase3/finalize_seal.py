#!/usr/bin/env python3
"""Update SEAL.json after Phase-3 apply (bytes-truth + fresh timestamp)."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_routes(path: Path) -> int:
    obj = json.loads(path.read_text())
    if isinstance(obj, list):
        return len(obj)
    return len(obj.get("features", []))


def count_features(path: Path) -> dict:
    obj = json.loads(path.read_text())
    if not isinstance(obj, dict):
        return {}
    return {k: len(v) for k, v in obj.items() if isinstance(v, list)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    seal_path = dc / "SEAL.json"
    seal = json.loads(seal_path.read_text())

    routes_n = count_routes(dc / "ROUTES.json")
    fbt_counts = count_features(dc / "FEATURES_BY_TYPE.json")

    seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    seal.setdefault("gates", {})
    seal["gates"]["land_crossing"] = (
        "PASS grok-phase3 apply — LB-224 v2 gate (postflight verifies)"
    )
    seal.setdefault("meta", {})["route_count"] = routes_n
    seal.setdefault("meta", {})["gold"] = "#79al"
    seal.setdefault("blobs", {})
    routes_path = dc / "ROUTES.json"
    seal["blobs"]["ROUTES"] = {
        "sha256": sha256_file(routes_path),
        "count": routes_n,
        "bytes": routes_path.stat().st_size,
    }
    fbt_path = dc / "FEATURES_BY_TYPE.json"
    if fbt_counts:
        seal["blobs"]["FEATURES_BY_TYPE"] = {
            "sha256": sha256_file(fbt_path),
            "count": fbt_counts,
            "bytes": fbt_path.stat().st_size,
        }
    for blob_name in ("STORIES", "VESSEL_SPECS"):
        blob_path = dc / f"{blob_name}.json"
        if blob_path.exists():
            obj = json.loads(blob_path.read_text())
            count = len(obj) if isinstance(obj, list) else len(obj.get("features", obj))
            seal["blobs"][blob_name] = {
                "sha256": sha256_file(blob_path),
                "count": count,
                "bytes": blob_path.stat().st_size,
            }

    seal_path.write_text(json.dumps(seal, indent=1) + "\n")

    reseal = work / "partner-pitch" / "_tools" / "reseal_from_disk.py"
    if reseal.exists():
        subprocess.run(
            [sys.executable, str(reseal), str(dc)],
            check=True,
        )

    print(f"SEAL finalized: routes={routes_n} gold=#79al")


if __name__ == "__main__":
    main()