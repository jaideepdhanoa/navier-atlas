#!/usr/bin/env python3
"""Mint Lagos lagoon Pioneer-II corridors and bind bolt.json nigeria journeys."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from bolt_yango_routing_shared import (  # noqa: E402
    LAND_THRESH_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    route_id_of,
    save_routes,
)

ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
PARTNER_PATHS = [
    ROOT / "partner-pitch/partners/bolt.json",
    ROOT / "data-clean/partners/bolt.json",
]
REPORT_PATH = ROOT / "grok-routing-output/bolt-nigeria-lagos-mint-report.json"

# Sealed BP IDs (from bolt-yango-bp-apply-report reconciled_existing)
LAGOS_BPS = {
    "cms": "bp-3a23a75e85",
    "osborne": "bp-0a23376ed0",
    "vi": "bp-801ab11946",
    "apapa": "bp-19cb381d59",
    "ikorodu": "bp-aaff4858f0",
}

# (from_key, to_key) -> journey `from`/`to` substring match
CORRIDORS = [
    (("cms", "vi"), ("CMS", "Victoria Island")),
    (("osborne", "cms"), ("Osborne", "CMS")),
    (("cms", "apapa"), ("CMS", "Apapa")),
    (("cms", "ikorodu"), ("CMS", "Ikorodu")),
]

JOURNEY_ROADMAP = ("Lekki", "Epe")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mint_lagos_routes(routes: list, bp_idx: dict, cities: dict, mask) -> tuple[dict, list]:
    existing = {route_id_of(r) for r in routes}
    pair_to_rid: dict[tuple[str, str], str] = {}
    report = {"synthesized": [], "skipped": []}

    for (fk, tk), _ in CORRIDORS:
        from_bp, to_bp = LAGOS_BPS[fk], LAGOS_BPS[tk]
        if from_bp not in bp_idx or to_bp not in bp_idx:
            report["skipped"].append({"from": from_bp, "to": to_bp, "reason": "bp_missing"})
            continue
        a = bp_idx[from_bp]["coords"]
        b = bp_idx[to_bp]["coords"]
        coords = build_coastal_path(a, b, mask)
        land_km = interior_land_km(coords, mask)
        rid = mint_route_id(from_bp, to_bp)
        if rid in existing:
            pair_to_rid[(fk, tk)] = rid
            report["skipped"].append({"route_id": rid, "reason": "already_exists"})
            continue
        feat = make_route_feature(
            from_bp,
            to_bp,
            bp_idx[from_bp]["name"],
            bp_idx[to_bp]["name"],
            "lagos-nigeria",
            "lagos-nigeria",
            coords,
            cities,
            source="bolt_nigeria_lagos",
            land_km=land_km,
        )
        feat["properties"]["id"] = rid
        if land_km > LAND_THRESH_KM:
            feat["properties"]["_qa_land_flag"] = True
        routes.append(feat)
        existing.add(rid)
        pair_to_rid[(fk, tk)] = rid
        report["synthesized"].append(
            {"route_id": rid, "from_bp": from_bp, "to_bp": to_bp, "land_km": round(land_km, 3)}
        )
    return pair_to_rid, report


def bind_journeys(partner: dict, pair_to_rid: dict) -> dict:
    stats = {"bound": 0, "roadmap": 0, "skipped": 0}
    for market in partner.get("markets", []):
        if market.get("id") != "nigeria":
            continue
        for j in market.get("journeys_unlocked", []):
            if JOURNEY_ROADMAP[0] in j.get("from", "") and JOURNEY_ROADMAP[1] in j.get("to", ""):
                j["route_id"] = None
                j["_link_status"] = "roadmap-quanta-lr"
                j["render"] = "amber-dashed"
                j.pop("display", None)
                stats["roadmap"] += 1
                continue
            matched = None
            for (fk, tk), (fsub, tsub) in CORRIDORS:
                if fsub in j.get("from", "") and tsub in j.get("to", ""):
                    matched = pair_to_rid.get((fk, tk))
                    break
            if not matched:
                stats["skipped"] += 1
                continue
            j["route_id"] = matched
            j["_link_status"] = "linked-grok-scoped"
            j["_link_source"] = "grok/bolt_nigeria_lagos_mint"
            j["economics_status"] = "pending-seal"
            j.pop("display", None)
            stats["bound"] += 1
        for fr in market.get("phases", [{}])[0].get("featured_routes", []) or []:
            for (fk, tk), (fsub, tsub) in CORRIDORS:
                if fsub in fr.get("from_label", "") and tsub in fr.get("to_label", ""):
                    rid = pair_to_rid.get((fk, tk))
                    if rid:
                        fr["route_id"] = rid
                        fr["_link_status"] = "linked-grok-scoped"
                        fr.pop("display", None)
    partner.setdefault("economics_status", {})["nigeria_lagos_mint_at"] = now_iso()
    return stats


def main() -> int:
    fbt = load_json(FBT_PATH)
    routes = route_features(load_json(ROUTES_PATH))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()

    pair_to_rid, mint_report = mint_lagos_routes(routes, bp_idx, cities, mask)
    save_routes(ROUTES_PATH, routes)

    bind_stats = None
    for path in PARTNER_PATHS:
        partner = load_json(path)
        bind_stats = bind_journeys(partner, pair_to_rid)
        path.write_text(json.dumps(partner, indent=2) + "\n")

    out = {
        "at": now_iso(),
        "mint": mint_report,
        "bind": bind_stats,
        "pair_to_rid": {f"{a}->{b}": rid for (a, b), rid in pair_to_rid.items()},
    }
    REPORT_PATH.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())