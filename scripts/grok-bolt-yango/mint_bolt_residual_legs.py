#!/usr/bin/env python3
"""Mint + bind residual Bolt kept-market legs with explicit sealed BP pairs."""
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

PARTNER_PATHS = [
    ROOT / "partner-pitch/partners/bolt.json",
    ROOT / "data-clean/partners/bolt.json",
]
REPORT = ROOT / "grok-routing-output/bolt-residual-mint-report.json"

# (from_bp, to_bp, from_city, to_city, journey_from_sub, journey_to_sub)
LEGS = [
    ("bp-9c4dc1bf0b", "bp-a4bab9759a", "venice-italy", "venice-italy", "Venice", "Lido"),
    ("bp-9c4dc1bf0b", "bp-6774b3c63f", "venice-italy", "venice-italy", "San Marco", "Murano"),
    ("bp-st-tropez-vieux-port", "bp-4b8c11f285", "saint-tropez-france", "saint-tropez-france", "St-Tropez", "Pampelonne"),
    ("bp-a1807ad7f6", "bp-st-tropez-vieux-port", "cannes-france", "saint-tropez-france", "Cannes", "St-Tropez"),
    ("__nice_port__", "bp-st-tropez-vieux-port", "nice-france", "saint-tropez-france", "Nice", "St-Tropez"),
    ("bp-dammam-corniche", "bp-ce0d211952", "dammam-khobar-ksa", "eastern-province-ksa", "Dammam", "Tarout"),
]

# Pampelonne beach club cluster (~3nm SE of St-Tropez port) — curated if no BP
PAMPELONNE = [6.67, 43.23]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_pampelonne_bp(fbt: dict, bp_idx: dict) -> str:
    bid = "bp-pampelonne-beach-clubs"
    if bid in bp_idx:
        return bid
    feat = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": PAMPELONNE},
        "properties": {
            "id": bid,
            "type": "poi",
            "name": "Pampelonne beach clubs",
            "shortName": "Pampelonne",
            "parent_city_id": "saint-tropez-france",
            "coords_resolved": True,
            "confidence": "med",
            "precision": "curated_seed",
            "status": "operational",
            "_bolt_residual_mint_at": now_iso(),
        },
    }
    fbt.setdefault("poi", []).append(feat)
    bp_idx[bid] = {"coords": tuple(PAMPELONNE), "name": "Pampelonne beach clubs", "parent_city_id": "saint-tropez-france"}
    return bid


def resolve_nice_port(bp_idx: dict) -> str:
    for bid, v in bp_idx.items():
        if v.get("parent_city_id") == "nice-france" and "nice port" in v.get("name", "").lower():
            return bid
    for bid in ("bp-406604",):
        if bid in bp_idx:
            return bid
    raise KeyError("nice port bp missing")


def mint_and_bind() -> dict:
    fbt = load_json(ROOT / "data-clean/FEATURES_BY_TYPE.json")
    routes = route_features(load_json(ROOT / "data-clean/ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    pamp = ensure_pampelonne_bp(fbt, bp_idx)
    nice_bp = resolve_nice_port(bp_idx)

    existing = {route_id_of(r) for r in routes}
    pair_to_rid: dict[tuple[str, str], str] = {}
    report = {"synthesized": [], "skipped": []}

    leg_specs = []
    for spec in LEGS:
        fb, tb, fc, tc, jf, jt = spec
        if jf == "St-Tropez" and jt == "Pampelonne":
            tb = pamp
        if fb == "__nice_port__":
            fb = nice_bp
        leg_specs.append((fb, tb, fc, tc, jf, jt))

    for from_bp, to_bp, fc, tc, jf, jt in leg_specs:
        if from_bp not in bp_idx or to_bp not in bp_idx:
            report["skipped"].append({"from": jf, "to": jt, "reason": "bp_missing", "from_bp": from_bp, "to_bp": to_bp})
            continue
        a = bp_idx[from_bp]["coords"]
        b = bp_idx[to_bp]["coords"]
        coords = build_coastal_path(a, b, mask)
        land_km = interior_land_km(coords, mask)
        rid = mint_route_id(from_bp, to_bp)
        if rid not in existing:
            feat = make_route_feature(
                from_bp, to_bp,
                bp_idx[from_bp]["name"], bp_idx[to_bp]["name"],
                fc, tc, coords, cities, land_km=land_km, source="bolt_residual_mint",
            )
            feat["properties"]["id"] = rid
            if land_km > LAND_THRESH_KM:
                feat["properties"]["_qa_land_flag"] = True
            routes.append(feat)
            existing.add(rid)
            report["synthesized"].append({"route_id": rid, "from": jf, "to": jt, "land_km": round(land_km, 3)})
        else:
            report["skipped"].append({"route_id": rid, "from": jf, "to": jt, "reason": "already_exists"})
        pair_to_rid[(jf, jt)] = rid

    from bolt_yango_routing_shared import save_json

    save_routes(ROOT / "data-clean/ROUTES.json", routes)
    save_json(ROOT / "data-clean/FEATURES_BY_TYPE.json", fbt)

    bind_stats = {"bound": 0}
    for path in PARTNER_PATHS:
        partner = load_json(path)
        for market in partner.get("markets", []):
            for j in market.get("journeys_unlocked", []):
                for (jf, jt), rid in pair_to_rid.items():
                    if jf in j.get("from", "") and jt in j.get("to", ""):
                        j["route_id"] = rid
                        j["_link_status"] = "linked-grok-scoped"
                        j["_link_source"] = "grok/bolt_residual_mint"
                        j.pop("display", None)
                        if j.get("render", "").startswith("roadmap"):
                            j["render"] = "solid"
                        bind_stats["bound"] += 1
            for ph in market.get("phases", []):
                for fr in ph.get("featured_routes", []) or []:
                    for (jf, jt), rid in pair_to_rid.items():
                        fl, tl = fr.get("from_label", ""), fr.get("to_label", "")
                        if jf in fl and jt in tl:
                            fr["route_id"] = rid
                            fr["_link_status"] = "linked-grok-scoped"
                            fr.pop("display", None)
        path.write_text(json.dumps(partner, indent=2) + "\n")

    return {"mint": report, "bind": bind_stats, "pair_to_rid": {f"{a}->{b}": r for (a, b), r in pair_to_rid.items()}}


def main() -> int:
    out = {"at": now_iso(), **mint_and_bind()}
    REPORT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())