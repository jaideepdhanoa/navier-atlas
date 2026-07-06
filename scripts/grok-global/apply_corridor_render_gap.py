#!/usr/bin/env python3
"""Repair corridor render gaps — mis-stamps, null clusters, Colombia seal, finance bind.

Lane: geometry/seal integrity per GROK-SPEC-corridor-render-gap-2026-07-06.
Guardrail: nobody invents a pier — unsourceable pairs stay null and get flagged.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

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
    resolve_corridor_endpoints,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)

HANDOFF = ROOT / "handoff" / "yango-program" / "gulf-and-restamp"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean" / "CLUSTERS.json"
CORRIDORS_PATH = ROOT / "finance" / "model" / "corridors.json"
FBT_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
REGISTER_PATH = HANDOFF / "CORRIDOR-RENDER-GAP-2026-07-06.json"
REPORT_PATH = ROOT / "grok-routing-output" / "corridor-render-gap-repair-report.json"

# WS-4 spatial-anchor collision tells (route_id → correct cluster_id)
ROUTE_OVERRIDES: dict[str, str] = {
    "rn-58b8735df336": "bahrain",
    "rn-6cf8e35fa53b": "oman",
    "rn-375e648be08e": "oman",
    "rn-38d01ae6b0a1": "ksa-commercial",
}

# Cluster-pair collision patterns: wrong_cluster → (city_substring, correct_cluster)
CLUSTER_COLLISION_RULES: list[tuple[str, str, str]] = [
    ("morocco", "oman", "oman"),
    ("morocco", "bahrain", "bahrain"),
    ("morocco", "ksa", "ksa-commercial"),
    ("morocco", "eastern-province", "ksa-commercial"),
    ("morocco", "manama", "bahrain"),
    ("morocco", "muscat", "oman"),
    ("amalfi-coast-italy", "florida", "florida-usa"),
    ("bay-of-naples-amalfi-coast-italy", "florida", "florida-usa"),
    ("cambodia", "vietnam", "vietnam"),
    ("indonesia", "geneva", "switzerland"),
    ("tunisia", "mauritius", "tunisia"),  # sousse/monastir mis-stamp
]

MINT_MARKETS = (
    "yango-colombia",
    "yango-tunisia",
    "yango-mozambique",
    "yango-pakistan",
    "yango-senegal",
    "yango-caspian-az",
    "yango-caspian-kz",
    "yango-israel",
)

# Markets with zero drawable geometry at audit time (finance knows them; geometry dark)
DARK_MARKETS_AUDIT = (
    "colombia",
    "morocco",
    "tunisia",
    "caspian",
    "cote-divoire",
    "senegal",
    "peru",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def load_city_to_cluster() -> dict[str, str]:
    clusters = load_json(CLUSTERS_PATH).get("clusters") or []
    out: dict[str, str] = {}
    for c in clusters:
        cid = c["cluster_id"]
        for city in c.get("member_city_ids") or []:
            out[city] = cid
    return out


def cluster_from_cities(fc: str | None, tc: str | None, city_to_cluster: dict[str, str]) -> str | None:
    clusters = {city_to_cluster.get(c) for c in (fc, tc) if c and city_to_cluster.get(c)}
    clusters.discard(None)
    if len(clusters) == 1:
        return next(iter(clusters))
    if fc and tc and fc == tc:
        return city_to_cluster.get(fc)
    return None


def apply_collision_rules(p: dict) -> str | None:
    cid = p.get("cluster_id")
    if not cid:
        return None
    blob = f"{p.get('from_city_id','')} {p.get('to_city_id','')} {p.get('from_label','')} {p.get('to_label','')}".lower()
    for wrong, needle, correct in CLUSTER_COLLISION_RULES:
        if cid == wrong and needle in blob:
            return correct
    return None


def correct_misstamps(routes: list, city_to_cluster: dict[str, str], report: dict) -> None:
    """Fix WS-4 spatial-anchor collisions + stamp null cluster_id on real corridors.

    Does NOT blanket-overwrite existing cluster_id (sub-cluster vs parent stays intact).
    """
    for feat in routes:
        p = props(feat)
        rid = p.get("id") or route_id_of(feat)
        old = p.get("cluster_id")

        new = ROUTE_OVERRIDES.get(rid)
        if not new:
            new = apply_collision_rules(p)
        if not new and not old:
            new = cluster_from_cities(p.get("from_city_id"), p.get("to_city_id"), city_to_cluster)

        if new and new != old:
            p["cluster_id"] = new
            p["_corridor_render_gap_repair"] = utc_now()
            report["restamps"].append({"route_id": rid, "from": old, "to": new})


def ensure_colombia_cluster_member(clusters_doc: dict) -> bool:
    changed = False
    for c in clusters_doc.get("clusters") or []:
        if c.get("cluster_id") != "colombia":
            continue
        members = list(c.get("member_city_ids") or [])
        if "barranquilla-colombia" not in members:
            members.append("barranquilla-colombia")
            c["member_city_ids"] = members
            c["members_present"] = len(members)
            c["_corridor_render_gap"] = utc_now()
            changed = True
        break
    return changed


def mint_market_routes(
    market_key: str,
    market: dict,
    routes: list,
    bp_idx: dict,
    cities: dict,
    mask,
    city_to_cluster: dict[str, str],
    report: dict,
) -> list[dict]:
    existing = {route_id_of(r) for r in routes}
    added: list[dict] = []
    cluster_id = market_key.replace("yango-", "").replace("bolt-", "")
    if cluster_id.startswith("caspian"):
        cluster_id = "azerbaijan-caspian" if "az" in cluster_id else "kazakhstan-caspian"

    for corr in market.get("corridors") or []:
        from_bp, to_bp, from_city, to_city = resolve_corridor_endpoints(corr, bp_idx)
        if not from_bp or not to_bp or from_bp == to_bp:
            report["mint_skipped"].append(
                {
                    "market": market_key,
                    "from": corr.get("from"),
                    "to": corr.get("to"),
                    "reason": "unresolved_bp",
                }
            )
            continue

        rid = mint_route_id(from_bp, to_bp, tag=market_key.replace("-", "")[:12])
        if rid in existing:
            report["mint_skipped"].append({"market": market_key, "route_id": rid, "reason": "exists"})
            continue

        a = bp_idx[from_bp]["coords"]
        b = bp_idx[to_bp]["coords"]
        coords = build_coastal_path(a, b, mask)
        land_km = interior_land_km(coords, mask)
        if land_km > LAND_THRESH_KM:
            report["flags"].append(
                {
                    "type": "land_qa_warn",
                    "market": market_key,
                    "from": corr.get("from"),
                    "to": corr.get("to"),
                    "land_km": land_km,
                }
            )

        feat = make_route_feature(
            from_bp,
            to_bp,
            bp_idx[from_bp]["name"],
            bp_idx[to_bp]["name"],
            from_city,
            to_city,
            coords,
            cities,
            source="corridor_render_gap",
            land_km=land_km,
        )
        p = props(feat)
        p["id"] = rid
        stamp = cluster_from_cities(from_city, to_city, city_to_cluster) or cluster_id
        if from_city and city_to_cluster.get(from_city):
            stamp = city_to_cluster[from_city]
        p["cluster_id"] = stamp
        p["_corridor_render_gap_mint"] = utc_now()

        added.append(feat)
        existing.add(rid)
        report["minted"].append(
            {
                "route_id": rid,
                "market": market_key,
                "cluster_id": stamp,
                "from_bp": from_bp,
                "to_bp": to_bp,
                "nm": p.get("distance_nm"),
            }
        )
        corr["route_id"] = rid
        corr["_atlas_status"] = "bound"
        corr.pop("_aspirational", None)

    return added


def bind_corridor_route_ids(corridors_doc: dict, routes: list, report: dict) -> int:
    by_pair: dict[tuple[str, str], str] = {}
    for feat in routes:
        p = props(feat)
        fn = p.get("from_node") or p.get("from")
        tn = p.get("to_node") or p.get("to")
        rid = p.get("id")
        if fn and tn and rid:
            by_pair[(fn, tn)] = rid
            by_pair[(tn, fn)] = rid

    bound = 0
    for market_key, market in (corridors_doc.get("markets") or {}).items():
        for corr in market.get("corridors") or []:
            if corr.get("route_id"):
                continue
            eps = corr.get("endpoint_boarding_points") or {}
            fn = eps.get("from_bp") or corr.get("from_bp")
            tn = eps.get("to_bp") or corr.get("to_bp")
            if fn and tn:
                rid = by_pair.get((fn, tn))
                if rid:
                    corr["route_id"] = rid
                    corr["_atlas_status"] = "bound"
                    bound += 1
                    report["finance_bound"].append({"market": market_key, "route_id": rid})
    return bound


def build_register(report: dict) -> dict:
    return {
        "generated": utc_now(),
        "lane": "corridor-render-gap",
        "guardrail": "nobody_invents_a_pier",
        "modes": ["missing", "cross_country_misstamp", "null_cluster_id", "finance_geometry_unbound"],
        "dark_markets_yango": list(DARK_MARKETS_AUDIT),
        "summary": {
            "misstamps_corrected": len(report.get("restamps", [])),
            "routes_minted": len(report.get("minted", [])),
            "mint_skipped": len(report.get("mint_skipped", [])),
            "finance_bound": len(report.get("finance_bound", [])),
            "flags": len(report.get("flags", [])),
        },
        "restamps": report.get("restamps", [])[:120],
        "minted": report.get("minted", []),
        "mint_skipped": report.get("mint_skipped", []),
        "finance_bound": report.get("finance_bound", []),
        "flags": report.get("flags", []),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--mint-markets", nargs="*", default=list(MINT_MARKETS))
    args = ap.parse_args()

    city_to_cluster = load_city_to_cluster()
    routes = route_features(load_json(ROUTES_PATH))
    corridors_doc = load_json(CORRIDORS_PATH)
    fbt = load_json(FBT_PATH)
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()

    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "routes_before": len(routes),
        "restamps": [],
        "minted": [],
        "mint_skipped": [],
        "finance_bound": [],
        "flags": [],
    }

    correct_misstamps(routes, city_to_cluster, report)

    new_routes: list[dict] = []
    for market_key in args.mint_markets:
        market = (corridors_doc.get("markets") or {}).get(market_key)
        if not market:
            continue
        new_routes.extend(
            mint_market_routes(market_key, market, routes + new_routes, bp_idx, cities, mask, city_to_cluster, report)
        )

    routes.extend(new_routes)
    report["routes_after"] = len(routes)

    bind_corridor_route_ids(corridors_doc, routes, report)

    clusters_doc = load_json(CLUSTERS_PATH)
    cluster_patch = ensure_colombia_cluster_member(clusters_doc)

    # Post-repair counts for dark markets
    by_cluster = defaultdict(int)
    for r in routes:
        cid = props(r).get("cluster_id")
        if cid:
            by_cluster[cid] += 1
    report["post_counts"] = {m: by_cluster.get(m, 0) for m in DARK_MARKETS_AUDIT}
    report["colombia_routes"] = by_cluster.get("colombia", 0)

    print(
        f"  misstamps fixed: {len(report['restamps'])} · minted: {len(report['minted'])} "
        f"· finance bound: {len(report['finance_bound'])} · flags: {len(report['flags'])}"
    )
    print(f"  colombia routes: {report['colombia_routes']} · morocco: {by_cluster.get('morocco',0)} · tunisia: {by_cluster.get('tunisia',0)}")

    register = build_register(report)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    REGISTER_PATH.write_text(json.dumps(register, indent=2) + "\n")

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        save_json(CORRIDORS_PATH, corridors_doc)
        if cluster_patch:
            CLUSTERS_PATH.write_text(json.dumps(clusters_doc, indent=2, ensure_ascii=False) + "\n")
        print(f"  wrote {ROUTES_PATH} · {CORRIDORS_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())