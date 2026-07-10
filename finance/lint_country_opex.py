#!/usr/bin/env python3
"""
Lint: corridor countries vs finance/model/country-reference.json.

Exits:
  0 — no R16/home-port fallbacks required (or --report-only)
  1 — one or more true missing countries (need Tasklet rates)
  2 — usage / load error

Usage:
  python3 finance/lint_country_opex.py
  python3 finance/lint_country_opex.py --json
  python3 finance/lint_country_opex.py --partner swing
  python3 finance/lint_country_opex.py --report-only   # always exit 0
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "model")
sys.path.insert(0, MODEL)

from country_opex_resolve import (  # noqa: E402
    resolve_opex_country,
    scan_corridors_missing,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corridors", default=os.path.join(MODEL, "corridors.json"))
    ap.add_argument(
        "--partner",
        default=None,
        help="Only lint corridors for this partner key",
    )
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument(
        "--report-only",
        action="store_true",
        help="Print findings but always exit 0",
    )
    args = ap.parse_args()

    cref = json.load(open(os.path.join(MODEL, "country-reference.json")))["countries"]
    corr = json.load(open(args.corridors))
    markets = corr.get("markets") or {}
    if args.partner:
        markets = {
            mid: mk
            for mid, mk in markets.items()
            if isinstance(mk, dict) and mk.get("partner") == args.partner
        }
        if not markets:
            print(f"No markets for partner={args.partner!r}", file=sys.stderr)
            return 2

    hits = scan_corridors_missing(markets, cref)
    # True missing = used_fallback with r16 policy (not dual-leg alias that resolved cleanly)
    true_missing = [
        h
        for h in hits
        if h.get("used_fallback")
        or (
            h.get("policy") == "r16_homeport_fallback"
            or str(h.get("policy", "")).startswith("alias_target_missing")
        )
    ]

    payload = {
        "corridors_path": args.corridors,
        "partner_filter": args.partner,
        "n_cref_countries": len(cref),
        "fallback_hits": hits,
        "true_missing_countries": sorted(
            {h.get("raw_country") for h in true_missing if h.get("raw_country")}
        ),
        "n_fallback_corridor_rows": sum(h.get("n_corridors", 0) for h in true_missing),
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"country-reference countries: {payload['n_cref_countries']}")
        print(f"corridors: {args.corridors}")
        if args.partner:
            print(f"partner filter: {args.partner}")
        if not true_missing:
            print("OK — no R16/home-port country-opex fallbacks required.")
        else:
            print(
                f"MISSING / FALLBACK — {payload['n_fallback_corridor_rows']} corridor-row(s), "
                f"countries: {payload['true_missing_countries']}"
            )
            for h in true_missing:
                print(
                    f"  • {h.get('raw_country')!r} → opex={h.get('opex_country')!r} "
                    f"policy={h.get('policy')} n={h.get('n_corridors')} "
                    f"partners={h.get('partners')} markets={h.get('markets')[:6]}"
                )
            print(
                "\nSeal rates in finance/model/country-reference.json then rebuild sheets "
                "(finance/REBUILD-AFTER-COUNTRY-OPEX.md)."
            )

    if args.report_only:
        return 0
    return 1 if true_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
