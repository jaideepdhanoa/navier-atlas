#!/usr/bin/env python3
"""Promote 3 held synth rows + Lulu/Reem crosswalk for #79am apply."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--ledger-src", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    ledger = json.loads(Path(args.ledger_src).read_text())

    held = ledger.pop("hold_synthesize_phantom", [])
    ledger["apply_synthesize_phantom_restored"] = held
    ledger.setdefault("_meta", {})["reseal_target"] = "#79am"
    ledger["_meta"]["note"] = "Lulu/Reem restored visible — 3 held synth rows promoted"

    for slug in ("ad-lulu-island", "ad-reem-island"):
        if slug in ledger.get("endpoint_crosswalk_verified", {}):
            ledger["endpoint_crosswalk_verified"][slug]["status"] = "apply"
            ledger["endpoint_crosswalk_verified"][slug]["verified"] = "restored_79ak_visible"

    out = work / "APPLY-LEDGER-79am.json"
    out.write_text(json.dumps(ledger, indent=2) + "\n")
    print(f"wrote {out} with {len(held)} restored synth rows")


if __name__ == "__main__":
    main()