#!/usr/bin/env python3
"""Audit partner-pitch use-case completeness (PR #56 gate)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTNERS = ROOT / "partner-pitch" / "partners"
MIN_MARKET_USE_CASES = 2

# Hub/sub-proposal partners that require market-level use_cases (PR #56 backfill scope)
MARKET_USE_CASE_PARTNERS = {
    "aman.json",
    "bolt.json",
    "didi.json",
    "discovery-land.json",
    "four-seasons.json",
    "gojek.json",
    "grab.json",
    "indrive.json",
    "kakao-mobility.json",
    "line.json",
    "lyft.json",
    "ola.json",
    "rapido.json",
    "six-senses.json",
    "soneva.json",
    "uber.json",
    "yango.json",
}


def valid_use_case(item) -> bool:
    if isinstance(item, str):
        return bool(item.strip())
    if not isinstance(item, dict):
        return False
    if item.get("label") and item.get("summary"):
        return True
    if item.get("title"):
        return True
    return False


def count_valid(use_cases) -> int:
    if not isinstance(use_cases, list):
        return 0
    return sum(1 for u in use_cases if valid_use_case(u))


def iter_phases(doc: dict, market_id: str | None = None):
    for phase in doc.get("phases") or []:
        yield market_id, phase
    for market in doc.get("markets") or []:
        mid = market.get("id") or market.get("slug") or "?"
        for phase in market.get("phases") or []:
            yield mid, phase


def audit(*, partner_filter: set[str] | None = None) -> int:
    errors: list[str] = []
    empty_phase: list[str] = []
    missing_market_uc: list[str] = []
    gate_failures: list[str] = []

    for path in sorted(PARTNERS.glob("*.json")):
        if path.name.startswith("_"):
            continue
        slug = path.stem
        if partner_filter is not None and slug not in partner_filter:
            continue
        try:
            doc = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: invalid JSON — {exc}")
            continue

        for market_id, phase in iter_phases(doc):
            ucs = phase.get("use_cases")
            if ucs == []:
                label = phase.get("label") or f"phase {phase.get('n', '?')}"
                empty_phase.append(f"{path.name}:{market_id or 'top'}:{label}")

        if path.name in MARKET_USE_CASE_PARTNERS:
            for market in doc.get("markets") or []:
                mid = market.get("id") or market.get("slug") or "?"
                if not market.get("phases"):
                    continue
                ucs = market.get("use_cases")
                n = count_valid(ucs)
                if n == 0:
                    missing_market_uc.append(f"{path.name}:{mid}")
                elif n < MIN_MARKET_USE_CASES:
                    gate_failures.append(
                        f"{path.name}:{mid} ({n} use_cases, need >={MIN_MARKET_USE_CASES})"
                    )

    print("Partner proposal use-case audit")
    print(f"  empty phase use_cases: {len(empty_phase)}")
    print(f"  markets missing market-level use_cases: {len(missing_market_uc)}")
    print(f"  phase 3 market gate failures (<{MIN_MARKET_USE_CASES}): {len(gate_failures)}")

    if empty_phase:
        print("\n  empty phase rows:")
        for row in empty_phase[:20]:
            print(f"    - {row}")
        if len(empty_phase) > 20:
            print(f"    ... +{len(empty_phase) - 20} more")

    if missing_market_uc:
        print("\n  missing market-level use_cases:")
        for row in missing_market_uc[:20]:
            print(f"    - {row}")

    if gate_failures:
        print("\n  gate failures:")
        for row in gate_failures[:20]:
            print(f"    - {row}")

    if errors or empty_phase or missing_market_uc or gate_failures:
        return 1

    print("  ✅ all PR #56 use-case gates pass")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--partner",
        nargs="+",
        default=None,
        help="Limit audit to these partner slugs (e.g. rapido ola noon careem)",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    filt = set(args.partner) if args.partner else None
    sys.exit(audit(partner_filter=filt))