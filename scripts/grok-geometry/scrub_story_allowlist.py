#!/usr/bin/env python3
"""Remove story-visible route_ids from route_water_allowlist.json."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOW_PATH = ROOT / "data-clean" / "route_water_allowlist.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    import sys
    sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))
    from story_registry import collect_story_registry

    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    story = set(collect_story_registry().keys())
    doc = json.loads(ALLOW_PATH.read_text())
    ids = list(doc.get("ids") or [])
    before = len(ids)
    removed = [r for r in ids if r in story]
    kept = [r for r in ids if r not in story]
    meta = doc.setdefault("_meta", {})
    meta["story_scrub_at"] = utc_now()
    meta["story_scrub_removed"] = len(removed)
    meta["allowlisted_count"] = len(kept)

    report = {
        "at": meta["story_scrub_at"],
        "removed": len(removed),
        "before": before,
        "after": len(kept),
        "removed_ids": removed[:50],
    }
    print(json.dumps(report, indent=2))

    if args.apply and removed:
        doc["ids"] = kept
        ALLOW_PATH.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())