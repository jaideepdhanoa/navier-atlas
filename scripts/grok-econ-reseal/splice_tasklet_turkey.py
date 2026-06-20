#!/usr/bin/env python3
"""Splice PR #49 Yango Turkey market + re-bind nulled featured routes."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from apply_bolt_yango import (  # noqa: E402
    RouteIndexes,
    bind_route_refs,
    binding_stats,
    build_corridor_index,
    load_json,
    route_features,
    save_json,
)
from bolt_yango_routing_shared import build_bp_index  # noqa: E402

PRESERVE_KEYS = ("growth_case", "economics_url", "_growth_case_pending", "_ingest")


def splice_turkey_market(handoff_market: dict, current: dict, indexes, corridor_idx, url: str, bp_idx) -> dict:
    out = json.loads(json.dumps(handoff_market))
    for key in PRESERVE_KEYS:
        if current.get(key):
            out[key] = current[key]
    market_key = "yango-turkey"
    bind_route_refs(out, indexes, corridor_idx, url, market_key, bp_idx)
    for ph in out.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if fr.get("_prev_route_id") and not fr.get("route_id"):
                prev = fr["_prev_route_id"]
                if prev in indexes.by_id:
                    fr["route_id"] = prev
                    fr["_link_status"] = "linked-node-retag"
                    fr["_link_kind"] = "node-retag-reuse"
            if fr.get("route_id") and not fr.get("render"):
                fr["render"] = "geometry" if fr.get("_link_status", "").startswith("linked") else fr.get("render")
            if fr.get("from_label") and "rhodes" in (fr.get("to_label") or "").lower():
                fr["render"] = fr.get("render") or "aspirational"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--handoff", default=str(ROOT / "_ingest/tasklet-turkey-split-2026-06-20"))
    ap.add_argument("--corridors", default=str(ROOT / "finance/model/corridors.json"))
    ap.add_argument("--econ-map", default=str(ROOT / "finance/economics_url_map.json"))
    args = ap.parse_args()

    dc = ROOT / args.dc
    handoff_yango = load_json(Path(args.handoff) / "yango.json") if (Path(args.handoff) / "yango.json").exists() else None
    if not handoff_yango:
        handoff_yango = load_json(dc / "partners/yango.json")

    yango = load_json(dc / "partners/yango.json")
    handoff_market = next((m for m in handoff_yango.get("markets", []) if m.get("id") == "turkey"), None)
    if not handoff_market:
        raise SystemExit("missing turkey market in handoff")

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    indexes = RouteIndexes(routes)
    corridor_idx = build_corridor_index(load_json(Path(args.corridors)))
    bp_idx = build_bp_index(fbt)
    econ_map = load_json(Path(args.econ_map))
    url = econ_map.get("economics_url", {}).get("yango", "")

    for i, m in enumerate(yango.get("markets") or []):
        if m.get("id") == "turkey":
            yango["markets"][i] = splice_turkey_market(handoff_market, m, indexes, corridor_idx, url, bp_idx)
            break
    else:
        raise SystemExit("turkey market not found in data-clean yango.json")

    save_json(dc / "partners/yango.json", yango)
    stats = binding_stats(yango)
    print(f"→ yango: linked={stats['linked']} unlinked={stats['unlinked']}")

    report = []
    turkey = next(m for m in yango["markets"] if m["id"] == "turkey")
    for ph in turkey.get("phases", []):
        for fr in ph.get("featured_routes", []):
            if fr.get("_node_retag") or fr.get("_prev_route_id"):
                report.append({
                    "phase": ph.get("id"),
                    "from": fr.get("from_label"),
                    "to": fr.get("to_label"),
                    "route_id": fr.get("route_id"),
                    "status": fr.get("_link_status"),
                    "render": fr.get("render"),
                    "nodes": f"{fr.get('from_node_id')} → {fr.get('to_node_id')}",
                })
                print(f"  {fr.get('from_label')} → {fr.get('to_label')}: {fr.get('route_id') or fr.get('_link_status')} render={fr.get('render')}")

    out = ROOT / "grok-routing-output/turkey-coast-splice-report.json"
    save_json(out, {"featured_route_rebinds": report})


if __name__ == "__main__":
    main()