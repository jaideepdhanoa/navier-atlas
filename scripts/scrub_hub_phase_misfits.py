#!/usr/bin/env python3
"""
Scrub cross-market featured_routes from hub top-level phases (phase-narrative fit).

Per fix-first plan step 5: move to correct market phase or HOLD null on hub carousel.
Records _fidelity_trim on removed items in receipt; does not use placeholders.

Usage:
  python3 scripts/scrub_hub_phase_misfits.py --partner grab --apply
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
RECEIPT = ROOT / "handoff" / "partner-map-model" / "HUB-PHASE-SCRUB-RECEIPT.json"

# Explicit removals: (phase_n, substring in label or from_node_id)
GRAB_HUB_REMOVALS: dict[int, list[str]] = {
    1: ["Manila South Harbor", "Naval Base Cavite", "manila-philippines"],
    2: ["HoiAn Flow", "Da Nang / Hoi An", "vietnam"],
    3: ["Tuan Chau", "Ha Long Bay", "vietnam"],
    4: [
        "Bach Dang",
        "Bến đò Tắc Suất",
        "Desaru Coast",
        "Villa Marina Condominium",
        "desaru-coast-malaysia",
        "vietnam",
    ],
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def item_matches_removal(item: dict, needles: list[str]) -> str | None:
    blob = " ".join(
        str(item.get(k) or "")
        for k in ("label", "from", "to", "from_label", "to_label", "from_node_id", "to_node_id")
    ).lower()
    for needle in needles:
        if needle.lower() in blob:
            return needle
    return None


def scrub_partner(slug: str, removals: dict[int, list[str]], *, apply: bool) -> dict:
    path = ROOT / "data-clean" / "partners" / f"{slug}.json"
    doc = load_json(path)
    removed: list[dict] = []

    for phase in doc.get("phases") or []:
        pn = phase.get("n")
        if pn not in removals:
            continue
        needles = removals[pn]
        kept: list = []
        for fr in phase.get("featured_routes") or []:
            if not isinstance(fr, dict):
                continue
            hit = item_matches_removal(fr, needles)
            if hit:
                entry = copy.deepcopy(fr)
                entry["_fidelity_trim"] = {
                    "at": TS,
                    "reason": "hub_phase_narrative_misfit",
                    "phase": pn,
                    "matched": hit,
                }
                removed.append({"phase": pn, "label": fr.get("label"), "matched": hit})
            else:
                kept.append(fr)
        phase["featured_routes"] = kept

    stats = {"removed": len(removed), "items": removed}
    doc["_hub_phase_scrub"] = {"at": TS, "stats": stats}

    if apply:
        save_json(path, doc)
        pitch = ROOT / "partner-pitch" / "partners" / f"{slug}.json"
        if pitch.parent.exists():
            save_json(pitch, doc)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="+", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    receipt = {"at": TS, "partners": {}}
    for slug in args.partner:
        removals = GRAB_HUB_REMOVALS if slug == "grab" else {}
        stats = scrub_partner(slug, removals, apply=args.apply)
        receipt["partners"][slug] = stats
        print(f"{slug}: removed {stats['removed']}")

    if args.apply:
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())