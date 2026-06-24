#!/usr/bin/env python3
"""Strip partner platform-revenue ladder from non–super-app proposals (in place).

Hospitality, destination-region, sovereign, transit, and corporate partners show
Navier transport + journey wallet only — never Grab-style platform take.

Usage:
  python3 finance/apply_platform_rev_strip.py              # all partner JSON dirs
  python3 finance/apply_platform_rev_strip.py ocean-whisperer caribbean
  python3 finance/apply_platform_rev_strip.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from partner_platform_rev import shows_platform_revenue, strip_growth_case_platform  # noqa: E402

PARTNER_DIRS = [
    ROOT / "partner-pitch" / "partners",
    ROOT / "data-clean" / "partners",
]


def strip_partner(path: Path, *, dry_run: bool) -> bool:
    data = json.loads(path.read_text())
    if shows_platform_revenue(data):
        return False
    gc = data.get("growth_case")
    if not isinstance(gc, dict):
        return False
    rungs = (gc.get("revenue_potential") or {}).get("rungs") or []
    had_plat = any(r.get("id") == "platform_rev" for r in rungs)
    had_top = "partner_platform_rev_on_navier" in gc
    ci = gc.get("_cascade_inputs") or data.get("_cascade_inputs") or {}
    ci_rungs = ci.get("rungs_expected_ascending") or ci.get("rung_ids_expected") or []
    had_ci_plat = "platform_rev" in ci_rungs
    had_ci_shape = "platform" in str(ci.get("ladder_shape") or "").lower()
    if not had_plat and not had_top and not had_ci_plat and not had_ci_shape and gc.get("_platform_rev_excluded"):
        return False
    strip_growth_case_platform(gc)
    if not dry_run:
        path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("partners", nargs="*", help="optional partner ids (default: scan all)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets: list[Path] = []
    for d in PARTNER_DIRS:
        if not d.is_dir():
            continue
        if args.partners:
            for pid in args.partners:
                p = d / f"{pid}.json"
                if p.is_file():
                    targets.append(p)
        else:
            targets.extend(sorted(p for p in d.glob("*.json") if "_growth" not in p.name))

    changed = 0
    for path in targets:
        if strip_partner(path, dry_run=args.dry_run):
            changed += 1
            tag = "would strip" if args.dry_run else "stripped"
            print(f"{tag}: {path.relative_to(ROOT)}")

    print(f"done: {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())