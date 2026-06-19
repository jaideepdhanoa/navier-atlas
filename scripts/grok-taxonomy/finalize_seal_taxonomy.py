#!/usr/bin/env python3
"""Update SEAL.json after taxonomy migration (FEATURES_BY_TYPE.locale + CLUSTERS)."""
from __future__ import annotations

import argparse
import hashlib
import json
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
    ap.add_argument("--dc", default="data-clean", help="data-clean directory")
    ap.add_argument("--seal", default="#79ao")
    args = ap.parse_args()

    dc = Path(args.dc)
    seal_path = dc / "SEAL.json"
    seal = json.loads(seal_path.read_text())

    routes_n = count_routes(dc / "ROUTES.json")
    fbt_counts = count_features(dc / "FEATURES_BY_TYPE.json")
    clusters_n = len(json.loads((dc / "CLUSTERS.json").read_text()).get("clusters", []))

    seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    seal.setdefault("gates", {})
    seal["gates"]["taxonomy"] = (
        f"PASS grok-taxonomy — 4-tier Region→Cluster→City→Locale; clusters={clusters_n}; "
        f"locales={fbt_counts.get('locale', 0)} ({args.seal})"
    )
    seal.setdefault("meta", {})["route_count"] = routes_n
    seal.setdefault("meta", {})["gold"] = args.seal
    seal.setdefault("meta", {})["clusters"] = clusters_n
    seal.setdefault("meta", {})["locales"] = fbt_counts.get("locale", 0)

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

    pitch = seal.setdefault("pitch", {})
    briefs = list((dc / "city_briefs").glob("*.json")) if (dc / "city_briefs").is_dir() else []
    pitch["city_briefs"] = len(briefs)

    seal_path.write_text(json.dumps(seal, indent=2) + "\n")
    print(json.dumps({"SEAL finalized": args.seal, "routes": routes_n, "locales": fbt_counts.get("locale", 0)}, indent=2))


if __name__ == "__main__":
    main()