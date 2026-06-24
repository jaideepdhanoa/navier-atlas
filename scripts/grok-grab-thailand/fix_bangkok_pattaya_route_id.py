#!/usr/bin/env python3
"""Repair rn-dcbcbe8bfb4f: must be bangkok-thailand → pattaya-thailand, not koh-chang."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
CANONICAL_ID = "rn-dcbcbe8bfb4f"
SOURCE_PAIRS = ("bangkok-thailand", "pattaya-thailand")

# Duplicate depth-seal runs (2026-06-24) — drop after canonical fix
DUP_IDS = {
    "rn-71d469bfdfe4",
    "rn-ee55739721e4",
    "rn-4e437a8e1965",
    "rn-3b51a7741677",
    "rn-af9a746d0f79",
    "rn-3249b47197b1",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def main() -> int:
    routes = json.loads(ROUTES_PATH.read_text())
    by_id = {props(r).get("id"): r for r in routes}

    donor = None
    for rid, feat in by_id.items():
        p = props(feat)
        if (p.get("from_city_id"), p.get("to_city_id")) == SOURCE_PAIRS and rid != CANONICAL_ID:
            donor = feat
            break
    if not donor:
        print("no bangkok→pattaya donor route found", file=sys.stderr)
        return 1

    wrong = by_id.get(CANONICAL_ID)
    if not wrong:
        print(f"{CANONICAL_ID} missing", file=sys.stderr)
        return 1

    dp = props(donor)
    wp = props(wrong)
    report = {
        "at": now_iso(),
        "canonical_id": CANONICAL_ID,
        "before": {
            "from": wp.get("from_city_id"),
            "to": wp.get("to_city_id"),
        },
        "donor_id": dp.get("id"),
        "removed_dupes": [],
    }

    wrong["geometry"] = donor["geometry"]
    wp.update(
        {
            "from": "bangkok-thailand",
            "to": "pattaya-thailand",
            "from_city": "bangkok-thailand",
            "to_city": "pattaya-thailand",
            "from_city_id": "bangkok-thailand",
            "to_city_id": "pattaya-thailand",
            "label": "bangkok-thailand → pattaya-thailand",
            "distance_nm": dp.get("distance_nm"),
            "interior_land_km": dp.get("interior_land_km"),
            "_geometry_status": dp.get("_geometry_status", "pending_channel_authorship"),
            "_grab_thailand_depth_applied_at": now_iso(),
            "_grab_thailand_depth_route_fix": "bangkok-pattaya canonical",
        }
    )

    out = []
    for feat in routes:
        rid = props(feat).get("id")
        if rid in DUP_IDS:
            report["removed_dupes"].append(rid)
            continue
        out.append(feat)

    ROUTES_PATH.write_text(json.dumps(out) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())