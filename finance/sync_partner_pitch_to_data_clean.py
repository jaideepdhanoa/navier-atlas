#!/usr/bin/env python3
"""Sync partner-pitch/partners → data-clean/partners (public-stripped)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PITCH = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
STRIP_KEYS = frozenset({"deck_only", "reviewer_notes", "internal"})


def strip_obj(obj):
    if isinstance(obj, dict):
        return {k: strip_obj(v) for k, v in obj.items() if k not in STRIP_KEYS}
    if isinstance(obj, list):
        return [strip_obj(x) for x in obj]
    return obj


def main() -> int:
    import sys
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["rapido", "ola", "noon"]
    DC.mkdir(parents=True, exist_ok=True)
    for slug in targets:
        src = PITCH / f"{slug}.json"
        if not src.exists():
            print(f"skip {slug}: missing {src}")
            continue
        doc = strip_obj(json.loads(src.read_text()))
        out = DC / f"{slug}.json"
        out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"{slug}: {src} → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())