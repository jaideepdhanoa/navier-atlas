#!/usr/bin/env python3
"""Lane #4 — operator/terminal gazetteer ID-match for water-adjacent survivors."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

MARINE_STRONG = re.compile(
    r"\b(ferry\s+terminal|ferry\s+port|cruise\s+terminal|marina|harbour|harbor|"
    r"harbor|pier|jetty|wharf|dock|port|ferry|water\s+taxi|boat\s+ramp|yacht\s+club|"
    r"shipyard|seaport|waterfront)\b",
    re.I,
)
MARINE_WEAK = re.compile(r"\b(marina|harbour|harbor|pier|jetty|wharf|dock|port|ferry)\b", re.I)
NOISE = re.compile(
    r"\b(gym|fitness|restaurant|bar\b|hotel|mall|clinic|church|school|residence|"
    r"apartment|coffee|spa|salon|shop|store|market|gym)\b",
    re.I,
)


def build_crosswalk_index(crosswalk: dict) -> set[str]:
    ids = set()
    for _key, vals in crosswalk.get("crosswalk", {}).items():
        for v in vals:
            ids.add(v)
    return ids


def gazetteer_match(bp_id: str, name: str, in_crosswalk: set[str]) -> tuple[bool, str]:
    if bp_id in in_crosswalk:
        return True, "pier_slug_crosswalk"
    if NOISE.search(name or ""):
        return False, "noise_name"
    if MARINE_STRONG.search(name or ""):
        return True, "marine_name_strong"
    if MARINE_WEAK.search(name or ""):
        return True, "marine_name_weak"
    return False, "no_gazetteer_match"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    cand_path = work / "grok-routing-output" / "bp-candidates.json"
    candidates = json.loads(cand_path.read_text())

    crosswalk_path = work / "atlas-external" / "pier-slug-bp-crosswalk.json"
    if not crosswalk_path.exists():
        crosswalk_path = Path(__file__).resolve().parents[2] / "atlas-external" / "pier-slug-bp-crosswalk.json"
    crosswalk = json.loads(crosswalk_path.read_text())
    in_crosswalk = build_crosswalk_index(crosswalk)

    promoted = []
    quarantined = []
    for row in candidates:
        if not row.get("water_adjacency_pass"):
            row["promoted"] = False
            row["gate4_reason"] = "failed_water_adjacency"
            quarantined.append(row["id"])
            continue
        matched, reason = gazetteer_match(row["id"], row.get("name", ""), in_crosswalk)
        if row.get("verdict") == "KEEP":
            ok = matched or reason.startswith("marine_name")
            row["promoted"] = ok
            row["gate4_reason"] = reason if ok else f"KEEP_unconfirmed:{reason}"
        else:  # HOLD
            ok = matched and reason == "pier_slug_crosswalk"
            row["promoted"] = ok
            row["gate4_reason"] = reason if ok else f"HOLD_unconfirmed:{reason}"
        (promoted if row["promoted"] else quarantined).append(row["id"])

    promoted_path = work / "grok-routing-output" / "bp-promoted-ids.json"
    promoted_path.write_text(json.dumps({"promoted": promoted, "count": len(promoted)}, indent=2) + "\n")
    cand_path.write_text(json.dumps(candidates, indent=2) + "\n")

    report = {
        "promoted": len(promoted),
        "quarantined_after_gate4": len(quarantined),
        "promoted_ids": promoted,
    }
    (work / "grok-routing-output" / "bp-gazetteer-report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(f"gazetteer gate: promoted={len(promoted)} quarantined={len(quarantined)}")


if __name__ == "__main__":
    main()