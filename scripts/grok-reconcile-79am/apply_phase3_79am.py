#!/usr/bin/env python3
"""Phase-3 apply for #79am — includes restored Lulu/Reem synth rows."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Reuse phase3 helpers
PHASE3 = Path(__file__).resolve().parents[1] / "grok-phase3"
sys.path.insert(0, str(PHASE3))
from apply_phase3 import (  # noqa: E402
    build_bp_index,
    build_city_index,
    load_json,
    make_bp_feature,
    make_synthesize_feature,
    mint_bp_id,
    save_json,
    save_routes,
    route_features,
    route_id_of,
    slug_to_bp_map,
    solutions_index,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    ledger = load_json(work / "APPLY-LEDGER-79am.json")
    solutions = solutions_index(work / "grok-routing-output" / "route-solutions.jsonl")

    fbt_path = dc / "FEATURES_BY_TYPE.json"
    routes_path = dc / "ROUTES.json"
    features_by_type = load_json(fbt_path)
    routes = route_features(load_json(routes_path))
    route_by_id = {route_id_of(f): i for i, f in enumerate(routes)}

    bp_index = build_bp_index(features_by_type)
    cities = build_city_index(features_by_type)

    report = {"minted_bps": [], "synthesized": [], "patched": [], "held": [], "errors": []}

    khalifa_payload = ledger["khalifa_mint_payload"]
    khalifa_bp = mint_bp_id(khalifa_payload)
    if khalifa_bp not in bp_index:
        feat = make_bp_feature(khalifa_bp, khalifa_payload)
        features_by_type.setdefault("poi", []).append(feat)
        bp_index[khalifa_bp] = {
            "name": khalifa_payload["name"],
            "parent_city_id": khalifa_payload["parent_city_id"],
            "coords": [khalifa_payload["lng"], khalifa_payload["lat"]],
        }
        report["minted_bps"].append(khalifa_bp)

    slug_bp = slug_to_bp_map(ledger, khalifa_bp)

    def apply_synthesize_pair(from_slug: str, to_slug: str, bucket: str):
        row = solutions.get((from_slug, to_slug))
        if not row:
            report["errors"].append(f"missing solution for {from_slug} -> {to_slug}")
            return
        from_bp = slug_bp.get(from_slug)
        to_bp = slug_bp.get(to_slug)
        if not from_bp or not to_bp:
            report["errors"].append(f"missing bp map for {from_slug} -> {to_slug}")
            return
        if from_bp not in bp_index or to_bp not in bp_index:
            report["errors"].append(f"bp not in graph: {from_bp} / {to_bp}")
            return
        dist = float(row.get("distance_nm_geom") or row.get("distance_nm") or 0)
        feat = make_synthesize_feature(
            from_bp, to_bp, row["geometry"], bp_index, cities, dist, row.get("priority_tier", "")
        )
        rid = feat["properties"]["id"]
        if rid in route_by_id:
            routes[route_by_id[rid]] = feat
        else:
            routes.append(feat)
            route_by_id[rid] = len(routes) - 1
        report["synthesized"].append({"route_id": rid, "from": from_slug, "to": to_slug, "bucket": bucket})

    for pair in ledger["apply_synthesize_clean"]:
        apply_synthesize_pair(pair["from"], pair["to"], "apply_synthesize_clean")
    for pair in ledger["apply_synthesize_after_khalifa_mint"]:
        apply_synthesize_pair(pair["from"], pair["to"], "apply_synthesize_after_khalifa_mint")
    for pair in ledger.get("apply_synthesize_phantom_restored", []):
        apply_synthesize_pair(pair["from"], pair["to"], "apply_synthesize_phantom_restored")

    for key, row in list(solutions.items()):
        if key[0] != "route_id":
            continue
        rid = key[1]
        if rid not in route_by_id:
            report["errors"].append(f"patch target missing in ROUTES: {rid}")
            continue
        feat = routes[route_by_id[rid]]
        if feat.get("properties", feat).get("_quarantine"):
            continue
        feat["geometry"] = row["geometry"]
        props = feat.setdefault("properties", feat)
        if row.get("distance_nm_geom") is not None:
            props["distance_nm"] = round(float(row["distance_nm_geom"]), 1)
        props["_wp_provenance"] = f"grok-79am-patch ({row.get('priority_tier', '')})"
        props["_applied_at"] = datetime.now(timezone.utc).isoformat()
        report["patched"].append(rid)

    save_json(fbt_path, features_by_type)
    save_routes(routes_path, routes)
    save_json(work / "grok-routing-output" / "phase3-apply-report-79am.json", report)
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(f"apply finished with {len(report['errors'])} error(s)")


if __name__ == "__main__":
    main()