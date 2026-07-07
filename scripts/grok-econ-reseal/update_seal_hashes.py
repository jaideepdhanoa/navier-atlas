#!/usr/bin/env python3
"""Refresh data-clean/SEAL.json sha256 entries for on-disk blobs (content re-seal)."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
SEAL_PATH = DC / "SEAL.json"

BLOB_FILES = {
    "FEATURES_BY_TYPE": "FEATURES_BY_TYPE.json",
    "ROUTES": "ROUTES.json",
    "STORIES": "STORIES.json",
    "VESSEL_SPECS": "VESSEL_SPECS.json",
    "economics_by_route_id": "economics_by_route_id.json",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_blob(name: str, path: Path) -> int | dict:
    obj = json.loads(path.read_text())
    if name == "ROUTES":
        return len(obj) if isinstance(obj, list) else len(obj.get("features", []))
    if name == "FEATURES_BY_TYPE":
        return {k: len(v) for k, v in obj.items() if isinstance(v, list)}
    if name == "economics_by_route_id":
        return len(obj.get("records", []))
    return len(obj) if isinstance(obj, list) else len(obj)


def main() -> int:
    seal = json.loads(SEAL_PATH.read_text())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seal["sealed_at"] = now
    blobs = seal.setdefault("blobs", {})
    files = seal.setdefault("files", {})
    for blob_name, rel in BLOB_FILES.items():
        path = DC / rel
        if not path.exists():
            print(f"skip {rel}: missing")
            continue
        digest = sha256_file(path)
        blobs[blob_name] = {
            "sha256": digest,
            "count": count_blob(blob_name, path),
            "bytes": path.stat().st_size,
        }
        files[rel] = {"sha256": digest, "updated": now}
        print(f"  {blob_name}: {blobs[blob_name]['sha256'][:16]}… count={blobs[blob_name]['count']}")

    meta = seal.setdefault("meta", {})
    meta["pr58_reseal"] = "grok-india-noon-followup-2026-06-20"
    if isinstance(blobs.get("ROUTES", {}).get("count"), int):
        meta["route_count"] = blobs["ROUTES"]["count"]
    pitch = seal.setdefault("pitch", {})
    partners_dir = DC / "partners"
    if partners_dir.is_dir():
        pitch["partners"] = len(list(partners_dir.glob("*.json")))

    SEAL_PATH.write_text(json.dumps(seal, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {SEAL_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())