#!/usr/bin/env python3
"""Backfill from_city_id / to_city_id on routes to gold city registry ids."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import load_json, save_json, resolve_city_id  # noqa: E402

DC = ROOT / "data-clean"
REPORT_PATH = ROOT / "grok-routing-output/route-city-id-backfill-report.json"

DISPLAY_ALIASES = {
    "dubai": "dubai-uae",
    "abu dhabi": "abu-dhabi-uae",
    "manama": "manama-bahrain",
    "doha": "doha-qatar",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gold_cities(fbt: dict) -> tuple[set[str], dict[str, str]]:
    gold: set[str] = set()
    by_name: dict[str, str] = {}
    for layer in ("city", "priority_city"):
        for feat in fbt.get(layer, []):
            props = feat.get("properties", feat)
            cid = props.get("id")
            if not cid:
                continue
            gold.add(cid)
            for key in ("name", "shortName", "fullName"):
                val = props.get(key)
                if val:
                    by_name[val.lower().strip()] = cid
            by_name[cid.replace("-", " ").lower()] = cid
    for alias, cid in DISPLAY_ALIASES.items():
        if cid in gold:
            by_name[alias] = cid
    return gold, by_name


def bp_parents(fbt: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        parent = props.get("parent_city_id")
        if pid and parent:
            out[pid] = parent
    return out


def split_compound(raw: str) -> str | None:
    if "__" in raw:
        head = raw.split("__", 1)[0]
        return head
    if raw.count("-") >= 3:
        # locale-style compound: city-country__locale-slug without separator
        m = re.match(r"^([a-z0-9]+(?:-[a-z0-9]+){1,2}-[a-z]{2,})(?:__|-{2}|__)", raw)
        if m:
            return m.group(1)
    return None


def resolve_endpoint(
    props: dict,
    side: str,
    gold: set[str],
    by_name: dict[str, str],
    bp_idx: dict[str, str],
) -> tuple[str | None, str]:
    field = f"{side}_city_id"
    display_field = f"{side}_city"
    endpoint_field = side if side in ("from", "to") else side

    current = props.get(field)
    if current and current in gold:
        return current, "already_gold"

    display = (props.get(display_field) or "").lower().strip()
    if display and display in by_name:
        return by_name[display], "display_name"

    bp = props.get(endpoint_field)
    if bp and bp in bp_idx:
        parent = bp_idx[bp]
        if parent in gold:
            return parent, "bp_parent"
        resolved = resolve_city_id(parent, gold)
        if resolved in gold:
            return resolved, "bp_parent_resolved"

    if current:
        head = split_compound(current)
        if head and head in gold:
            return head, "compound_head"
        resolved = resolve_city_id(current, gold)
        if resolved in gold:
            return resolved, "resolve_city_id"
        if head:
            resolved = resolve_city_id(head, gold)
            if resolved in gold:
                return resolved, "compound_resolve"

    return None, "unresolved"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--assert-build", action="store_true", help="exit 1 if unresolved rate >= 5%")
    args = ap.parse_args()

    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    gold, by_name = gold_cities(fbt)
    bp_idx = bp_parents(fbt)

    routes_raw = load_json(DC / "ROUTES.json")
    is_list = isinstance(routes_raw, list)
    routes = routes_raw if is_list else routes_raw.get("features", [])

    before_missing = 0
    before_suspect = 0
    fixes: list[dict] = []
    unresolved: list[dict] = []

    for feat in routes:
        props = feat.get("properties") or {}
        rid = props.get("id")
        for side in ("from", "to"):
            field = f"{side}_city_id"
            cur = props.get(field)
            if not cur:
                before_missing += 1
            elif cur not in gold:
                before_suspect += 1

            resolved, method = resolve_endpoint(props, side, gold, by_name, bp_idx)
            if resolved and resolved != cur:
                fixes.append({
                    "route_id": rid,
                    "field": field,
                    "before": cur,
                    "after": resolved,
                    "method": method,
                })
                if args.apply:
                    props[field] = resolved
            elif cur and cur not in gold and not resolved:
                unresolved.append({"route_id": rid, "field": field, "value": cur})

    total_slots = len(routes) * 2
    after_suspect = sum(
        1
        for f in routes
        for side in ("from", "to")
        if (f.get("properties") or {}).get(f"{side}_city_id") not in gold
        and (f.get("properties") or {}).get(f"{side}_city_id")
    )
    after_missing = sum(
        1
        for f in routes
        for side in ("from", "to")
        if not (f.get("properties") or {}).get(f"{side}_city_id")
    )

    mismatch_rate = (after_suspect + after_missing) / total_slots if total_slots else 0.0

    if args.apply:
        if is_list:
            save_json(DC / "ROUTES.json", routes)
        else:
            routes_raw["features"] = routes
            save_json(DC / "ROUTES.json", routes_raw)

    report = {
        "at": utc_now(),
        "apply": args.apply,
        "routes": len(routes),
        "gold_cities": len(gold),
        "before": {
            "missing_city_id": before_missing,
            "suspect_non_gold": before_suspect,
            "mismatch_rate_pct": round(100 * (before_missing + before_suspect) / total_slots, 2),
        },
        "after": {
            "missing_city_id": after_missing,
            "suspect_non_gold": after_suspect,
            "mismatch_rate_pct": round(100 * mismatch_rate, 2),
        },
        "fixes_applied": len(fixes),
        "unresolved": unresolved[:50],
        "unresolved_count": len(unresolved),
        "fix_samples": fixes[:30],
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)

    print(json.dumps({
        "before_mismatch_pct": report["before"]["mismatch_rate_pct"],
        "after_mismatch_pct": report["after"]["mismatch_rate_pct"],
        "fixes": len(fixes),
        "unresolved": len(unresolved),
    }, indent=2))

    if args.assert_build and mismatch_rate >= 0.05:
        print(f"BUILD ASSERTION FAILED: mismatch rate {mismatch_rate:.1%} >= 5%", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())