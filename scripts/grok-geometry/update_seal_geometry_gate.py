#!/usr/bin/env python3
"""Write honest geometry gate stats into SEAL.json."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEAL_PATH = ROOT / "data-clean" / "SEAL.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    audit_path = ROOT / "handoff" / "partner-map-model" / "GEOMETRY-AUDIT.json"
    if not audit_path.exists():
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "audit-route-geometry.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0 and not audit_path.exists():
            print(r.stdout, r.stderr, file=sys.stderr)
            return 1

    audit = json.loads(audit_path.read_text())
    seal = json.loads(SEAL_PATH.read_text())
    gates = seal.setdefault("gates", {})
    gates["geometry_story"] = (
        f"{'PASS' if audit.get('story_fail', 1) == 0 else 'FAIL'} — "
        f"story {audit.get('story_pass', 0)} pass / {audit.get('story_fail', 0)} fail"
    )
    gates["geometry_story_allowlisted"] = (
        f"{'PASS' if audit.get('story_allowlisted', 1) == 0 else 'FAIL'} — "
        f"{audit.get('story_allowlisted', 0)} story routes on allowlist"
    )
    gates["geometry_mesh_fail"] = str(audit.get("mesh_fail", "?"))
    gates["geometry_allowlist_size"] = str(audit.get("allowlist_size", "?"))
    seal["geometry_audit_at"] = utc_now()
    seal["geometry_audit"] = audit

    print(json.dumps(audit, indent=2))
    if args.apply:
        SEAL_PATH.write_text(json.dumps(seal, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {SEAL_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())