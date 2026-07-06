#!/usr/bin/env python3
"""Apply bucket-A cluster_id restamps from market coverage gap register.

Deterministic hygiene: properties.cluster_id → canonical cluster from endpoint city.
Does not change market-page render (endpoint-city scoping is authoritative).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import load_json, route_features, save_routes  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REGISTER_PATH = ROOT / "handoff" / "MARKET-COVERAGE-GAP-2026-07-06.json"
REPORT_PATH = ROOT / "grok-routing-output" / "market-coverage-restamp-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--register", default=str(REGISTER_PATH))
    args = ap.parse_args()

    register = load_json(Path(args.register))
    restamps = register.get("A_restamp") or []
    routes = route_features(load_json(ROUTES_PATH))
    by_id = {props(r).get("id"): r for r in routes if props(r).get("id")}

    applied = []
    skipped = []
    for entry in restamps:
        rid = entry.get("route_id")
        new = entry.get("new")
        if not rid or not new:
            skipped.append({"route_id": rid, "reason": "missing_fields"})
            continue
        feat = by_id.get(rid)
        if not feat:
            skipped.append({"route_id": rid, "reason": "route_not_found"})
            continue
        p = props(feat)
        old = p.get("cluster_id")
        if old == new:
            skipped.append({"route_id": rid, "reason": "already_correct"})
            continue
        if args.apply:
            p["cluster_id"] = new
            p["_market_coverage_restamp"] = utc_now()
        applied.append({"route_id": rid, "old": old, "new": new, "basis": entry.get("basis")})

    report = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "register": str(args.register),
        "restamp_register_count": len(restamps),
        "applied": len(applied),
        "skipped": len(skipped),
        "samples": applied[:20],
        "skip_reasons": skipped[:20],
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")

    print(f"  A_restamp: {len(applied)} applied · {len(skipped)} skipped")
    if args.apply:
        save_routes(ROUTES_PATH, routes)
        print(f"  wrote {ROUTES_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())