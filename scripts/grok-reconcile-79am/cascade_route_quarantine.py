#!/usr/bin/env python3
"""Quarantine routes whose endpoints resolve to quarantined BPs (all id schemes)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reconcile_shared import (
    build_bp_indexes,
    endpoint_blocked,
    load_json,
    route_features,
    route_id_of,
    save_routes,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    routes = route_features(load_json(dc / "ROUTES.json"))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    bp_by_id, berth_index = build_bp_indexes(fbt)
    city_ids = {
        (c.get("properties") or c).get("id")
        for c in fbt.get("city", []) + fbt.get("priority_city", [])
        if (c.get("properties") or c).get("id")
    }

    quarantined = []
    for feat in routes:
        props = feat.get("properties", feat)
        rid = route_id_of(feat)
        bad = []
        for ep in (props.get("from"), props.get("to")):
            if not ep:
                continue
            if ep.startswith("bp-") or "__" in ep:
                blocked, why = endpoint_blocked(ep, bp_by_id, berth_index, city_ids)
                if blocked:
                    bad.append(f"{ep}:{why}")
        if bad:
            props["_quarantine"] = True
            props["relevance"] = "hide"
            props["_quarantine_reason"] = f"quarantined_endpoint {bad}"
            quarantined.append({"id": rid, "bad": bad})

    save_routes(dc / "ROUTES.json", routes)
    q_bps = sum(
        1
        for row in bp_by_id.values()
        if row["props"].get("_quarantine") or row["props"].get("relevance") == "hide"
    )
    report = {
        "total": len(routes),
        "quarantined": len(quarantined),
        "active": len(routes) - len(quarantined),
        "quarantined_bps": q_bps,
        "sample": quarantined[:30],
    }
    (work / "grok-routing-output" / "route-cascade-report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(
        f"route cascade: total={report['total']} quarantined={report['quarantined']} "
        f"active={report['active']} (q_bps={q_bps})"
    )


if __name__ == "__main__":
    main()