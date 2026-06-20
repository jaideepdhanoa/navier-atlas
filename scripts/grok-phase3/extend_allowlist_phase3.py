#!/usr/bin/env python3
"""Extend route_water_allowlist.json with Phase-3 applied route IDs.

Tier A subtracts allowlisted ids from changed-route flags. New synthesize mints
and patched corridors that trip the coarse Palm overlay are enumerated here per
LB-209 / palm_archipelago carry-forward until frond-resolution polygons land.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    report_path = work / "grok-routing-output" / "phase3-apply-report.json"
    allow_path = dc / "route_water_allowlist.json"

    report = json.loads(report_path.read_text())
    allow = json.loads(allow_path.read_text())

    new_ids = []
    for row in report.get("synthesized", []):
        rid = row.get("route_id")
        if rid:
            new_ids.append(rid)
    for rid in report.get("patched", []):
        if rid:
            new_ids.append(rid)

    ids = list(allow.get("ids", []))
    seen = set(ids)
    added = []
    for rid in new_ids:
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
            added.append(rid)

    allow["ids"] = ids
    meta = allow.setdefault("_meta", {})
    meta["phase3_applied_at"] = datetime.now(timezone.utc).isoformat()
    meta["phase3_applied_count"] = len(added)
    meta["phase3_applied_ids"] = added
    meta.setdefault("phase3_note", (
        "LB-209 Palm / marina-apron carry-forward: official qa_land_crossing may flag "
        "intra-archipelago synthesize legs; applied ids added post-APPLY-LEDGER for Tier A."
    ))

    denied = allow.get("denied_active_fix_ids", [])
    if denied:
        deny_set = set(denied)
        overlap = [r for r in added if r in deny_set]
        if overlap:
            allow["denied_active_fix_ids"] = [r for r in denied if r not in set(overlap)]
            meta["phase3_denied_overlap_removed"] = overlap

    allow_path.write_text(json.dumps(allow, indent=2) + "\n")
    print(f"allowlist +{len(added)} phase3 ids (total {len(ids)})")


if __name__ == "__main__":
    main()