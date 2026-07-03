#!/usr/bin/env python3
"""Program-wide PTA land QA gate — evaluate _pta_* tagged routes in ROUTES.json."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from route_land_qa import evaluate_feature  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
META_PTA_KEYS = frozenset(
    {
        "_pta_node_from",
        "_pta_node_to",
        "_pta_pair_id",
        "_pta_bound_at",
        "_pta_sealed_at",
        "_pta_minted_at",
        "_pta_mint_city",
        "_pta_authority",
        "_pta_partner",
        "_pta_resealed_at",
    }
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pta_authority_tags(props: dict) -> list[str]:
    tags: list[str] = []
    for key, val in props.items():
        if not key.startswith("_pta_") or key in META_PTA_KEYS:
            continue
        if val is True:
            tags.append(key.removeprefix("_pta_"))
    return tags


def route_features(raw) -> list[dict]:
    if isinstance(raw, list):
        return raw
    return raw.get("features") or []


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit PTA-tagged routes for land QA")
    ap.add_argument(
        "--partner",
        help="Optional comma-separated partner slugs (e.g. dubai-rta,wsf)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any evaluated route fails land QA",
    )
    args = ap.parse_args()

    partner_filter: set[str] | None = None
    if args.partner:
        partner_filter = {p.strip() for p in args.partner.split(",") if p.strip()}

    raw = json.loads(ROUTES_PATH.read_text())
    feats = route_features(raw)

    rows: list[dict] = []
    pass_n = 0
    fail_n = 0
    skipped = 0

    for feat in feats:
        props = feat.get("properties") or {}
        rid = props.get("id")
        if not rid:
            continue
        tags = pta_authority_tags(props)
        if not tags:
            continue
        if partner_filter and not any(t in partner_filter for t in tags):
            skipped += 1
            continue

        ev = evaluate_feature(feat)
        row = {
            "route_id": rid,
            "pta_authorities": tags,
            "qa_pass": ev["qa_pass"],
            "interior_land_km": ev["interior_land_km"],
            "detour_ratio": ev.get("detour_ratio"),
            "mask": ev["mask"],
            "distance_nm": props.get("distance_nm"),
        }
        rows.append(row)
        if ev["qa_pass"]:
            pass_n += 1
        else:
            fail_n += 1

    report = {
        "generated_at": utc_now(),
        "routes_path": str(ROUTES_PATH.relative_to(ROOT)),
        "partner_filter": sorted(partner_filter) if partner_filter else None,
        "evaluated": len(rows),
        "skipped_unmatched": skipped,
        "pass": pass_n,
        "fail": fail_n,
        "failures": [r for r in rows if not r["qa_pass"]],
    }

    print(json.dumps(report, indent=2))
    print(
        f"\n✓ PTA land QA: {pass_n} pass, {fail_n} fail"
        + (f" ({skipped} routes skipped by --partner filter)" if partner_filter else "")
    )

    if fail_n:
        print("✗ failures:", file=sys.stderr)
        for r in report["failures"]:
            print(
                f"  {r['route_id']} [{','.join(r['pta_authorities'])}] "
                f"land={r['interior_land_km']}km detour={r.get('detour_ratio')}",
                file=sys.stderr,
            )

    if args.strict and fail_n:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())