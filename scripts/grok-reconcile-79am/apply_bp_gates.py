#!/usr/bin/env python3
"""Apply gate #3/#4 results to FEATURES_BY_TYPE — quarantine non-promoted candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    candidates = json.loads((work / "grok-routing-output" / "bp-candidates.json").read_text())
    fbt = json.loads((dc / "FEATURES_BY_TYPE.json").read_text())
    pois = fbt.get("poi", [])

    promoted = set()
    quarantined = []
    for row in candidates:
        pid = row["id"]
        if row.get("promoted"):
            promoted.add(pid)
        else:
            quarantined.append(pid)

    cand_by_id = {r["id"]: r for r in candidates}
    for poi in pois:
        props = poi.get("properties", poi)
        pid = props.get("id")
        row = cand_by_id.get(pid)
        if not row:
            continue
        if pid in promoted:
            props.pop("_quarantine", None)
            props.pop("relevance", None)
            props["status"] = "operational"
            props["_gate4_promoted"] = True
        else:
            props["relevance"] = "hide"
            props["_quarantine"] = True
            props["_quarantine_bucket"] = row.get("verdict", "HOLD") + "_UNCONFIRMED"
            props["_quarantine_reason"] = row.get("gate4_reason") or row.get("reason")

    (dc / "FEATURES_BY_TYPE.json").write_text(json.dumps(fbt, indent=2) + "\n")
    out = {
        "promoted": len(promoted),
        "quarantined": len(quarantined),
        "promoted_ids": sorted(promoted),
    }
    (work / "grok-routing-output" / "bp-gate-final.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"bp gates applied: promoted={len(promoted)} quarantined={len(quarantined)}")


if __name__ == "__main__":
    main()