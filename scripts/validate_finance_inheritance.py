#!/usr/bin/env python3
"""Gate: finance corridor spine (route_id sets) identical per shared geography.

Contract: handoff/uae-consolidation/FINANCE-CORRIDOR-INHERITANCE-CONTRACT.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORRIDORS_PATH = ROOT / "finance" / "model" / "corridors.json"
REPORT_PATH = ROOT / "grok-routing-output" / "finance-inheritance-report.json"

# Explicit market-key → geography (finance twin of geometry cluster)
MARKET_GEO_OVERRIDES: dict[str, str] = {
    "uae-careem": "uae",
    "uae-noon": "uae",
    "uae-luxury": "uae",
    "bolt-uae": "uae",
    "yango-uae": "uae",
    "gulf-authority-bahrain-motc": "gulf-authority",
    "gulf-authority-rakta": "gulf-authority",
    "ola-mumbai": "mumbai",
    "rapido-mumbai": "mumbai",
    "uber-mumbai": "mumbai",
    "bolt-qatar": "qatar",
    "yango-qatar": "qatar",
    "bolt-egypt": "egypt",
    "yango-egypt": "egypt",
    "yassir-morocco": "morocco",
    "yango-morocco": "morocco",
    "yassir-tunisia": "tunisia",
    "yango-tunisia": "tunisia",
}

PARTNER_PREFIXES = (
    "uber-india",
    "uber",
    "rapido",
    "ola",
    "bolt",
    "yango",
    "yassir",
    "careem",
    "noon",
    "india",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def market_to_geography(market_key: str) -> str:
    if market_key in MARKET_GEO_OVERRIDES:
        return MARKET_GEO_OVERRIDES[market_key]

    # india-{region}-{partner}
    m = re.match(r"^(india-[a-z]+)-(?:ola|rapido|uber-india)$", market_key)
    if m:
        return m.group(1)

    for prefix in ("bolt-", "yango-", "yassir-"):
        if market_key.startswith(prefix):
            return market_key[len(prefix) :]

    return market_key


def market_to_partner(market_key: str) -> str:
    if market_key in MARKET_GEO_OVERRIDES:
        # uae-careem → careem; bolt-uae → bolt
        if market_key.startswith("uae-"):
            return market_key[4:]
        if market_key.endswith("-uae"):
            return market_key[:-4]
        if market_key.startswith("gulf-authority-"):
            return market_key[len("gulf-authority-") :]
    m = re.match(r"^india-[a-z]+-(ola|rapido|uber-india)$", market_key)
    if m:
        return m.group(1)
    for prefix in ("bolt-", "yango-", "yassir-"):
        if market_key.startswith(prefix):
            return prefix.rstrip("-")
    if market_key.startswith("ola-"):
        return "ola"
    if market_key.startswith("rapido-"):
        return "rapido"
    if market_key.startswith("uber-"):
        return "uber"
    return market_key


def spine_route_ids(market: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for c in market.get("corridors") or []:
        rid = c.get("route_id")
        if rid:
            out.add(rid)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--geography", nargs="*", help="Limit divergence check to geography slug(s)")
    ap.add_argument("--json", action="store_true", help=f"Write report to {REPORT_PATH.relative_to(ROOT)}")
    args = ap.parse_args()

    doc = json.loads(CORRIDORS_PATH.read_text())
    markets: dict[str, dict[str, Any]] = doc.get("markets") or {}

    by_geo: dict[str, list[dict[str, Any]]] = {}
    for key, market in markets.items():
        geo = market_to_geography(key)
        partner = market_to_partner(key)
        by_geo.setdefault(geo, []).append(
            {
                "market_key": key,
                "partner": partner,
                "route_ids": sorted(spine_route_ids(market)),
                "route_count": len(spine_route_ids(market)),
            }
        )

    geo_filter = set(args.geography) if args.geography else None
    divergent: list[dict[str, Any]] = []
    checked = 0

    for geo in sorted(by_geo):
        if geo_filter and geo not in geo_filter:
            continue
        rows = by_geo[geo]
        partners = sorted({r["partner"] for r in rows})
        if len(partners) < 2:
            continue
        checked += 1
        sets = {r["market_key"]: set(r["route_ids"]) for r in rows}
        ref_key, ref_set = next(iter(sets.items()))
        identical = all(s == ref_set for s in sets.values())
        union = set().union(*sets.values())
        common = set.intersection(*sets.values()) if sets else set()
        if not identical:
            divergent.append(
                {
                    "geography": geo,
                    "partners": partners,
                    "market_keys": [r["market_key"] for r in rows],
                    "route_id_union": len(union),
                    "common_to_all": len(common),
                    "identical_sets": False,
                    "per_market_counts": {k: len(v) for k, v in sets.items()},
                    "only_in": {
                        k: sorted(v - ref_set) for k, v in sets.items() if v != ref_set
                    },
                    "reference_market": ref_key,
                }
            )

    print("Finance corridor spine inheritance gate")
    print(f"  multi-partner geographies checked: {checked}")
    print(f"  divergent: {len(divergent)}")

    priority = ["uae", "qatar", "gulf-authority", "egypt", "morocco", "tunisia"]
    ordered = sorted(
        divergent,
        key=lambda d: (priority.index(d["geography"]) if d["geography"] in priority else 99, d["geography"]),
    )

    for d in ordered:
        print(f"\n  ✗ {d['geography']} — partners {', '.join(d['partners'])}")
        print(f"    markets: {', '.join(d['market_keys'])}")
        print(
            f"    union {d['route_id_union']} · common {d['common_to_all']} · "
            f"counts {d['per_market_counts']}"
        )

    report = {
        "generated": utc_now(),
        "summary": {
            "market_keys_total": len(markets),
            "geographies_total": len(by_geo),
            "multi_partner_geographies_checked": checked,
            "divergent_geographies": len(divergent),
        },
        "divergent": ordered,
        "all_geographies": {
            geo: rows for geo, rows in sorted(by_geo.items())
        },
    }

    if args.json:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
        print(f"\nReport → {REPORT_PATH.relative_to(ROOT)}")

    if divergent:
        return 1
    print("\n  ✅ all multi-partner geographies share identical finance spines")
    return 0


if __name__ == "__main__":
    sys.exit(main())