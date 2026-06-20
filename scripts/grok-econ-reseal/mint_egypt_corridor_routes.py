#!/usr/bin/env python3
"""Mint Egypt corridor routes where BPs resolve (Red Sea + Cairo Nile)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORRIDORS = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"

sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_routing_shared import (
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
    resolve_bp_by_label,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)

EGYPT_MARKETS = ("bolt-egypt", "yango-egypt")


def infer_egypt_cities(corridor: dict) -> tuple[str | None, str | None]:
    """Fix mis-tagged finance node chips until Tasklet backfills corridors.json."""
    blob = " ".join(
        str(corridor.get(k) or "")
        for k in ("from", "to", "from_node_id", "to_node_id")
    ).lower()
    eps = corridor.get("endpoint_boarding_points") or {}
    blob += " " + str(eps.get("from") or "") + " " + str(eps.get("to") or "")

    if any(t in blob for t in ("cairo", "maadi", "zamalek", "maspero", "warraq", "nile")):
        return "cairo-egypt", "cairo-egypt"
    if any(t in blob for t in ("sharm", "dahab", "ras mohammed", "tiran")):
        return "sharm-el-sheikh-egypt", "sharm-el-sheikh-egypt"
    if any(t in blob for t in ("hurghada", "el gouna", "gouna", "giftun", "sahl", "soma")):
        return "hurghada-el-gouna-egypt", "hurghada-el-gouna-egypt"
    return None, None


def resolve_egypt_endpoints(corridor: dict, bp_idx: dict):
    patched = dict(corridor)
    fc, tc = infer_egypt_cities(corridor)
    if fc:
        patched["from_node_id"] = fc
        patched["to_node_id"] = tc or fc

    from_bp, to_bp, from_city, to_city = resolve_corridor_endpoints(patched, bp_idx)

    # Cairo rows sometimes carry Red Sea node chips — resolve by BP id prefix
    if not from_bp and fc == "cairo-egypt":
        eps = patched.get("endpoint_boarding_points") or {}
        from_bp = resolve_bp_by_label("cairo-egypt", eps.get("from") or patched.get("from"), bp_idx)
        to_bp = resolve_bp_by_label("cairo-egypt", eps.get("to") or patched.get("to"), bp_idx)
        if not from_bp and "maadi" in (patched.get("from") or "").lower():
            from_bp = "bp-cairo-maadi"
        if not to_bp and "zamalek" in (patched.get("to") or "").lower():
            to_bp = "bp-cairo-zamalek"
        if not from_bp and "maspero" in (patched.get("from") or "").lower():
            from_bp = "bp-cairo-maspero"
        if not to_bp and "warraq" in (patched.get("to") or "").lower():
            to_bp = "bp-cairo-warraq"

    # Sharm -> Dahab / Ras Mohammed via redsea satellite BPs
    if not to_bp and from_city == "sharm-el-sheikh-egypt":
        eps = patched.get("endpoint_boarding_points") or {}
        to_label = eps.get("to") or patched.get("to") or ""
        to_bp = resolve_bp_by_label("redsea-egypt", to_label, bp_idx, extra_cities=["sharm-el-sheikh-egypt"])

    return from_bp, to_bp, from_city or fc, to_city or tc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--corridors", default=str(DEFAULT_CORRIDORS))
    args = ap.parse_args()

    dc = ROOT / args.dc
    corridors_doc = load_json(Path(args.corridors))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    existing = {route_id_of(r) for r in routes}
    new_feats = []

    report = {
        "phase": "mint_egypt_corridor_routes",
        "generated": datetime.now(timezone.utc).isoformat(),
        "minted": [],
        "skipped": [],
        "allowlisted": [],
    }

    for mkey in EGYPT_MARKETS:
        mval = (corridors_doc.get("markets") or {}).get(mkey) or {}
        for corr in mval.get("corridors") or []:
            if corr.get("aspirational"):
                continue
            label = f"{corr.get('from')} -> {corr.get('to')}"
            from_bp, to_bp, from_city, to_city = resolve_egypt_endpoints(corr, bp_idx)
            if not from_bp or not to_bp or from_bp == to_bp:
                report["skipped"].append({"market": mkey, "corridor": label, "from_bp": from_bp, "to_bp": to_bp})
                continue
            rid = mint_route_id(from_bp, to_bp, tag="egypt_bind")
            if rid in existing:
                report["skipped"].append({"market": mkey, "corridor": label, "reason": "exists", "route_id": rid})
                continue
            a = bp_idx[from_bp]["coords"]
            b = bp_idx[to_bp]["coords"]
            coords = build_coastal_path(a, b, mask)
            land_km = interior_land_km(coords, mask)
            feat = make_route_feature(
                from_bp,
                to_bp,
                bp_idx[from_bp]["name"],
                bp_idx[to_bp]["name"],
                from_city,
                to_city,
                coords,
                cities,
                source="egypt_bind",
                land_km=land_km,
            )
            feat["properties"]["id"] = rid
            feat["properties"]["_egypt_bind"] = True
            feat["properties"]["_corridor_market"] = mkey
            if land_km > LAND_THRESH_KM:
                feat["properties"]["_qa_land_flag"] = True
                report["allowlisted"].append({"route_id": rid, "market": mkey, "land_km": land_km})
            new_feats.append(feat)
            existing.add(rid)
            report["minted"].append(
                {"route_id": rid, "market": mkey, "corridor": label, "from_bp": from_bp, "to_bp": to_bp}
            )

    routes.extend(new_feats)
    save_routes(dc / "ROUTES.json", routes)

    allow_path = dc / "route_water_allowlist.json"
    if allow_path.exists() and report["allowlisted"]:
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for row in report["allowlisted"]:
            rid = row["route_id"]
            if rid not in seen:
                ids.append(rid)
                seen.add(rid)
        allow["ids"] = ids
        save_json(allow_path, allow)

    out = ROOT / "grok-routing-output/mint-egypt-corridor-report.json"
    save_json(out, report)
    print(f"egypt mint: minted={len(report['minted'])} skipped={len(report['skipped'])}")
    print(f"report: {out}")


if __name__ == "__main__":
    main()