#!/usr/bin/env python3
"""WS-8 — Dubai intra-city OD-level de-spaghetti per DUBAI-DESPAGHETTI.json."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import load_json, route_features, route_id_of, save_routes  # noqa: E402

REGISTER_PATH = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "DUBAI-DESPAGHETTI.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "grok-routing-output" / "dubai-despaghetti-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    reg = load_json(REGISTER_PATH)
    drop_ids: set[str] = set()
    for section in ("cut_land_crossers", "cut_miscity"):
        for row in reg.get(section) or []:
            if row.get("id"):
                drop_ids.add(row["id"])

    hold_ids = {r.get("id") for r in (reg.get("penalty_planned_hold") or []) if r.get("id")}
    keep_ids = {r.get("id") for r in (reg.get("keep_onwater") or []) if r.get("id")}

    routes = route_features(load_json(ROUTES_PATH))
    before = len(routes)
    kept = []
    dropped = 0
    for feat in routes:
        rid = route_id_of(feat)
        if rid in drop_ids and rid not in keep_ids:
            dropped += 1
            continue
        kept.append(feat)

    report = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "routes_before": before,
        "routes_after": len(kept),
        "dropped": dropped,
        "held_planned": sorted(hold_ids),
        "keep_onwater": len(keep_ids),
        "creek_remint_pending": bool(reg.get("creek_remint_gap")),
    }
    print(f"  Dubai de-spaghetti: {before} → {len(kept)} routes (dropped {dropped})")

    if args.apply:
        save_routes(ROUTES_PATH, kept)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())