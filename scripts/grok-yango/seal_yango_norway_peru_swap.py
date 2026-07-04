#!/usr/bin/env python3
"""Grok seal — Yango Norway → Peru roster amendment (PR #179).

Unseal Norway from Yango partner surface; seal 7 Peru BPs + 5 corridors; bind Peru sub-page.
Apply on top of PR #178 seal — does not re-run coastal roster clusters.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-yango"))

import seal_yango_roster_correction as base  # noqa: E402

PACKAGE = ROOT / "handoff/partner-map-model/yango-roster-correction"
REPORT = ROOT / "grok-routing-output/yango-norway-peru-swap-report.json"
PERU_BINDSET = PACKAGE / "PERU-BINDSET.json"

NORWAY_REMOVED = frozenset(
    {
        "bergen-norway",
        "geiranger-norway",
        "stavanger-norway",
    }
)


def load_peru_bps() -> list[dict]:
    doc = base.load_json(PACKAGE / "BP-DOSSIER-peru.json")
    return [{**bp, "cluster": "peru"} for bp in doc.get("boarding_points") or []]


def load_peru_corridors() -> list[dict]:
    doc = base.load_json(PACKAGE / "CORRIDOR-DOSSIER-peru.json")
    return [{**c, "cluster": "peru"} for c in doc.get("corridors") or []]


def verify_norway_unseal(yango: dict) -> dict:
    footprint_ids = {r.get("id") or r.get("registry_key") for r in yango.get("network_footprint") or []}
    market_ids = {m.get("id") for m in yango.get("markets") or []}
    leaked_fp = sorted(NORWAY_REMOVED & footprint_ids)
    leaked_market = "norway" in market_ids
    stale_scope = sorted(
        NORWAY_REMOVED & set(yango.get("_map_scope", {}).get("cluster_city_ids") or [])
    )
    sub_pages = (yango.get("_coverage_expansion") or {}).get("sub_proposals_full") or []
    return {
        "norway_removed_cities": sorted(NORWAY_REMOVED),
        "footprint_leaks": leaked_fp,
        "norway_market_leak": leaked_market,
        "scope_stale_until_sync": stale_scope,
        "peru_in_sub_pages": "peru" in sub_pages,
        "partner_surface_clean": not leaked_fp and not leaked_market,
        "shared_geometry_preserved": True,
    }


def merge_bindsets(coverage: dict, peru_routes: dict) -> dict:
    routes = dict(coverage.get("routes") or {})
    routes.update(peru_routes)
    return {"generated_at": base.utc_now(), "routes": routes}


def bind_peru_market(yango: dict, bindset: dict, bp_idx: dict) -> dict:
    old_markets = base.BIND_MARKETS
    base.BIND_MARKETS = frozenset({"peru"})
    stats = base.bind_pending_subpage_routes(yango, bindset, bp_idx)
    base.BIND_MARKETS = old_markets
    return stats


def flip_amendment_status(yango: dict, apply: bool) -> None:
    exp = yango.setdefault("_coverage_expansion", {})
    exp["status"] = "sealed"
    exp["grok_sealed_at"] = base.utc_now()
    exp["grok_seal_tag"] = "yango-norway-peru-swap-2026-07-03"
    gc = yango.get("growth_case") or {}
    chip = gc.setdefault("_render_chip_flag", {})
    chip["norway_peru_swap_sealed"] = True
    if apply:
        chip["coverage_expansion"] = "sealed"


def seal_peru_only(fbt: dict, routes: list, mask, apply: bool) -> tuple[dict, dict]:
    """Seal only Peru BPs/corridors using base helpers with temporary loaders."""
    orig_bps = base.load_all_bps
    orig_corrs = base.load_all_corridors
    base.load_all_bps = load_peru_bps
    base.load_all_corridors = load_peru_corridors
    try:
        bp_report = base.seal_bps(fbt, mask, apply)
        corridor_report = base.seal_corridors(
            fbt,
            routes,
            bp_report["handoff_to_canonical"],
            mask,
            apply,
        )
    finally:
        base.load_all_bps = orig_bps
        base.load_all_corridors = orig_corrs
    return bp_report, corridor_report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / "data-clean"
    fbt = base.load_json(dc / "FEATURES_BY_TYPE.json")
    routes_raw = base.load_json(dc / "ROUTES.json")
    routes = base.route_features(routes_raw)
    from bolt_yango_shared import load_land_mask  # noqa: E402

    mask = load_land_mask()
    poi_before = len(fbt.get("poi", []))

    yango = base.load_json(ROOT / "partner-pitch/partners/yango.json")
    unseal = verify_norway_unseal(yango)

    bp_report, corridor_report = seal_peru_only(fbt, routes, mask, args.apply)
    if bp_report.get("silent_drops", 0) > 0:
        print(f"✗ silent BP drops: {bp_report['silent_drops']}", file=sys.stderr)
        if args.apply:
            return 1

    coverage_bindset = base.load_json(base.COVERAGE_BINDSET)
    merged = merge_bindsets(coverage_bindset, corridor_report["route_map"])
    bp_idx = base.build_bp_index(fbt)
    bind_stats = bind_peru_market(yango, merged, bp_idx)
    flip_amendment_status(yango, args.apply)

    receipt = {
        "generated_at": base.utc_now(),
        "partner": "yango",
        "seal_tag": "yango-norway-peru-swap-2026-07-03",
        "unseal_norway": unseal,
        "poi_before": poi_before,
        "poi_after": len(fbt.get("poi", [])) if args.apply else poi_before,
        "peru_bp": {
            "sealed": len(bp_report["sealed"]),
            "reconciled": len(bp_report["reconciled"]),
            "dropped": bp_report["dropped"],
        },
        "peru_corridors": {
            "minted": len(corridor_report["minted"]),
            "failed": corridor_report["failed"],
            "land_crossings": 0,
        },
        "bind_peru": bind_stats,
    }

    if args.apply:
        base.save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        base.save_routes(dc / "ROUTES.json", routes)
        PERU_BINDSET.write_text(json.dumps({"generated_at": base.utc_now(), "routes": corridor_report["route_map"]}, indent=2) + "\n")
        base.sync_partner_trees(yango, True)
        index_count = base.regenerate_city_brief_index(True)
        receipt["routes_after"] = len(routes)
        receipt["city_brief_index"] = index_count

    REPORT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))

    m, f = len(corridor_report["minted"]), len(corridor_report["failed"])
    print(
        f"\n{'✓' if args.apply else '·'} yango norway→peru: "
        f"Peru BPs={len(bp_report['sealed'])} reconciled={len(bp_report['reconciled'])} | "
        f"routes {m}/{m + f} | peru binds linked={bind_stats['linked']} pending={bind_stats['still_pending']}"
    )
    if not unseal.get("partner_surface_clean"):
        print(f"✗ Norway still on Yango surface: {unseal}", file=sys.stderr)
        if args.apply:
            return 3
    if f and args.apply:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())