#!/usr/bin/env python3
"""LB-257: build a scoped corridors.json for inheritance partners (uber, etc.).

Reads finance/model/inheritance_spec.json + the global registry and emits a
partner-scoped view: listed registry markets copied with partner re-tagged.
Does NOT edit finance/model/corridors.json.

Usage:
  python3 build_scoped_corridors.py --partner uber --out finance/recal/corridors-uber.json
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "model")
SPEC_PATH = os.path.join(MODEL, "inheritance_spec.json")
REGISTRY_PATH = os.path.join(MODEL, "corridors.json")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", required=True, help="inheritance_spec partners key (e.g. uber)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--registry", default=REGISTRY_PATH)
    ap.add_argument("--spec", default=SPEC_PATH)
    args = ap.parse_args()

    spec = json.load(open(args.spec))
    entry = spec["partners"].get(args.partner)
    if not entry:
        sys.exit(f"unknown partner in inheritance_spec: {args.partner}")
    if not entry.get("ready_to_cascade"):
        sys.exit(f"{args.partner} is run-blocked: {entry.get('run_blocked_pending', 'ready_to_cascade=false')}")

    registry = json.load(open(args.registry))
    inherit = entry.get("inherit_markets") or {}
    market_keys = sorted({mk for keys in inherit.values() for mk in keys})
    missing = [k for k in market_keys if k not in registry["markets"]]
    if missing:
        sys.exit(f"registry missing inherited markets: {missing}")

    partner_tag = entry.get("partner_tag", args.partner)
    scoped_markets = {}
    for mk in market_keys:
        m = copy.deepcopy(registry["markets"][mk])
        m["partner"] = partner_tag
        scoped_markets[mk] = m

    out_doc = {
        "_doc": f"LB-257 scoped corridor view for {args.partner} — inherited from global registry; partner re-tagged.",
        "_source": os.path.basename(args.registry),
        "_inheritance_spec": os.path.basename(args.spec),
        "capture_rate": registry.get("capture_rate"),
        "markets": scoped_markets,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out_doc, open(args.out, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {args.out} ({len(scoped_markets)} markets: {', '.join(market_keys)})")


if __name__ == "__main__":
    main()