#!/usr/bin/env python3
"""Apply high-confidence POI junk drops by exact id (Lagos + Cape Town, PR #84)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import load_json, save_json  # noqa: E402

DEFAULT_TRIM = ROOT / "navier/handoff/bolt-narrative-refresh-2026-06-23/inputs/lagos-capetown-junk-trim.json"
REPORT_PATH = ROOT / "grok-routing-output/lagos-capetown-junk-trim-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--trim", default=str(DEFAULT_TRIM))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    trim = load_json(Path(args.trim))
    drop_by_id: dict[str, dict] = {}
    for city, block in (trim.get("drops") or {}).items():
        for row in block.get("drop_ids", []):
            drop_by_id[row["id"]] = {**row, "parent_city_id": city}

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    actions: list[dict] = []
    counts_before: dict[str, int] = {}
    counts_after: dict[str, int] = {}

    for city in ("lagos-nigeria", "cape-town-south-africa"):
        counts_before[city] = sum(
            1 for p in fbt.get("poi", [])
            if (p.get("properties") or {}).get("parent_city_id") == city
        )

    new_pois = []
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        if pid in drop_by_id:
            actions.append({"id": pid, "action": "drop", "reason": drop_by_id[pid]["reason"], "name": drop_by_id[pid]["name"]})
            continue
        if pid in drop_by_id:
            pass
        new_pois.append(poi)

    # verify every ledger id resolved
    found = {a["id"] for a in actions if a["action"] == "drop"}
    missing = sorted(set(drop_by_id) - found)
    kept_notes = []
    for pid in sorted(drop_by_id):
        if pid not in found:
            kept_notes.append({"id": pid, "action": "not_found", "note": "id absent from gold — already dropped or never sealed"})

    if args.apply:
        fbt["poi"] = new_pois
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
    if missing:
        print("NOTE: ids already absent from gold (prior drop):", missing)

    for city in ("lagos-nigeria", "cape-town-south-africa"):
        counts_after[city] = counts_before[city] - sum(
            1 for a in actions if a["action"] == "drop" and drop_by_id[a["id"]]["parent_city_id"] == city
        )

    report = {
        "at": utc_now(),
        "lane": "grok/apply_poi_junk_drops",
        "apply": args.apply,
        "drop_count_expected": len(drop_by_id),
        "drop_count_applied": len(found),
        "missing_ids": missing,
        "silent_drops": 0,
        "already_absent": len(missing),
        "before": counts_before,
        "after": counts_after if args.apply else counts_before,
        "actions": actions + kept_notes,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())