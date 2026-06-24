#!/usr/bin/env python3
"""Bind route_ids on bolt/yango partner JSON without splicing handoff markets."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INGEST = ROOT / "_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from apply_bolt_yango import (  # noqa: E402
    RouteIndexes,
    bind_market_routes,
    binding_stats,
    build_corridor_index,
    route_props,
)
from bolt_yango_routing_shared import build_bp_index, load_json, route_features  # noqa: E402

PARTNER_PATHS = {
    "bolt": [
        ROOT / "partner-pitch/partners/bolt.json",
        ROOT / "data-clean/partners/bolt.json",
    ],
    "yango": [
        ROOT / "partner-pitch/partners/yango.json",
        ROOT / "data-clean/partners/yango.json",
    ],
}


def main() -> int:
    corridors = load_json(INGEST / "inputs/corridors.json")
    corridor_idx = build_corridor_index(corridors)
    routes = route_features(load_json(ROOT / "data-clean/ROUTES.json"))
    indexes = RouteIndexes(routes)
    bp_idx = build_bp_index(load_json(ROOT / "data-clean/FEATURES_BY_TYPE.json"))

    report = {}
    for slug, paths in PARTNER_PATHS.items():
        stats_before = None
        for path in paths:
            if not path.exists():
                continue
            doc = load_json(path)
            stats_before = binding_stats(doc)
            for market in doc.get("markets") or []:
                pid = market.get("id") or market.get("slug")
                for key in (f"bolt-{pid}", f"yango-{pid}", pid):
                    if key in corridor_idx:
                        bind_market_routes(
                            market,
                            key,
                            indexes,
                            corridor_idx,
                            doc.get("economics_url"),
                            bp_idx,
                        )
                        break
            path.write_text(json.dumps(doc, indent=2) + "\n")
        report[slug] = {"before": stats_before, "after": binding_stats(load_json(paths[0]))}

    out = ROOT / "grok-routing-output/bolt-yango-bind-report.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())