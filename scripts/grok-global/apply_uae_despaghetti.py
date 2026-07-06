#!/usr/bin/env python3
"""WS-7 — UAE over-dense cluster de-spaghetti per UAE-DESPAGHETTI-REGISTER.json."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import load_json, route_features, route_id_of, save_routes  # noqa: E402

REGISTER_PATH = ROOT / "handoff" / "yango-program" / "gulf-and-restamp" / "UAE-DESPAGHETTI-REGISTER.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "grok-routing-output" / "uae-despaghetti-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    reg = load_json(REGISTER_PATH)
    drop_ids: set[str] = set()
    drop_ids.update(reg.get("drop_exact_parallel_dupes") or [])
    drop_ids.update(reg.get("drop_musandam_land_crossers") or [])
    drop_ids.update(reg.get("collapse_interemirate_longhaul_fan") or [])
    keep = set(reg.get("keep_2_canonical_longhaul") or [])

    routes = route_features(load_json(ROUTES_PATH))
    before = len(routes)
    kept = []
    dropped = 0
    for feat in routes:
        rid = route_id_of(feat)
        if rid in drop_ids and rid not in keep:
            dropped += 1
            continue
        kept.append(feat)

    report = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "routes_before": before,
        "routes_after": len(kept),
        "dropped": dropped,
        "keep_canonical": sorted(keep),
    }
    print(f"  UAE de-spaghetti: {before} → {len(kept)} routes (dropped {dropped})")

    if args.apply:
        save_routes(ROUTES_PATH, kept)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())