#!/usr/bin/env python3
"""Apply SEM-VERDICTS: DROP→quarantine, KEEP/HOLD→candidate pool for gates #3/#4."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    sem = load_json(work / "RECONCILE" / "SEM-VERDICTS.json")
    buckets = load_json(work / "RECONCILE" / "SEM-BUCKET-IDS.json")
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    pois = fbt.get("poi", [])

    sem_by_id = {r["id"]: r for r in sem}
    drop_ids = set(buckets.get("DROP", []))
    keep_hold_ids = set(buckets.get("KEEP", [])) | set(buckets.get("HOLD", []))

    report = {"drop_quarantined": 0, "candidates": 0, "missing": []}
    candidates = []

    for poi in pois:
        props = poi.get("properties", poi)
        pid = props.get("id")
        if pid not in sem_by_id:
            continue
        row = sem_by_id[pid]
        if pid in drop_ids:
            props["relevance"] = "hide"
            props["_quarantine"] = True
            props["_quarantine_bucket"] = "DROP"
            props["_quarantine_reason"] = row.get("reason", "semantic_DROP")
            report["drop_quarantined"] += 1
        elif pid in keep_hold_ids:
            candidates.append(
                {
                    "id": pid,
                    "name": row.get("name") or props.get("name"),
                    "coords": poi.get("geometry", {}).get("coordinates", [None, None]),
                    "verdict": row.get("verdict"),
                    "reason": row.get("reason"),
                }
            )
            report["candidates"] += 1
        else:
            report["missing"].append(pid)

    save_json(dc / "FEATURES_BY_TYPE.json", fbt)
    save_json(work / "grok-routing-output" / "bp-candidates.json", candidates)
    save_json(work / "grok-routing-output" / "sem-apply-report.json", report)
    print(f"sem: drop={report['drop_quarantined']} candidates={report['candidates']}")


if __name__ == "__main__":
    main()