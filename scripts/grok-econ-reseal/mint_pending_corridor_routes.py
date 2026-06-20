#!/usr/bin/env python3
"""
Mint routes for pending economics corridors where BP pairs are ready.
Sources: PENDING-ECONOMICS-TRIAGE bp_pair_ready rows + pending corridors with resolved BPs.
"""
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
    hav_nm,
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

MESH_CITIES = (
    "dubai-uae",
    "abu-dhabi-uae",
    "istanbul-turkey",
    "bodrum-turkey",
    "antalya-turkey",
    "cesme-izmir-turkey",
    "singapore",
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--corridors", default=str(DEFAULT_CORRIDORS))
    ap.add_argument("--triage", default="data-clean/PENDING-ECONOMICS-TRIAGE.json")
    ap.add_argument("--mesh", action="store_true", help="Add capped intra-city mesh (off by default on re-runs)")
    args = ap.parse_args()

    dc = ROOT / args.dc
    corridors_doc = load_json(Path(args.corridors))
    triage_path = ROOT / args.triage
    triage = load_json(triage_path) if triage_path.exists() else {"corridors": []}
    econ = load_json(dc / "economics_by_route_id.json")
    pending_keys = {(x["market"], x["corridor"]) for x in econ.get("_pending_route_pin", [])}

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    existing = {route_id_of(r) for r in routes}
    new_feats = []

    report = {
        "phase": "mint_pending_corridor_routes",
        "generated": datetime.now(timezone.utc).isoformat(),
        "minted": [],
        "skipped": [],
        "allowlisted": [],
        "mesh_added": 0,
    }

    def do_mint(fb, tb, fc, tc, market, tag="pending_bind"):
        if fb == tb or fb not in bp_idx or tb not in bp_idx:
            return
        rid = mint_route_id(fb, tb, tag=tag)
        if rid in existing:
            report["skipped"].append({"route_id": rid, "market": market, "reason": "exists"})
            return
        a = bp_idx[fb]["coords"]
        b = bp_idx[tb]["coords"]
        coords = build_coastal_path(a, b, mask)
        land_km = interior_land_km(coords, mask)
        feat = make_route_feature(
            fb,
            tb,
            bp_idx[fb]["name"],
            bp_idx[tb]["name"],
            fc,
            tc,
            coords,
            cities,
            source=tag,
            land_km=land_km,
        )
        feat["properties"]["id"] = rid
        feat["properties"]["_pending_bind"] = tag == "pending_bind"
        feat["properties"]["_corridor_market"] = market
        if land_km > LAND_THRESH_KM:
            feat["properties"]["_qa_land_flag"] = True
            report["allowlisted"].append({"route_id": rid, "market": market, "land_km": land_km})
        new_feats.append(feat)
        existing.add(rid)
        report["minted"].append(
            {"route_id": rid, "market": market, "from_bp": fb, "to_bp": tb, "nm": feat["properties"]["distance_nm"]}
        )

    for row in triage.get("corridors", []):
        if row.get("sub_bucket") != "bp_pair_ready":
            continue
        fb, tb = row.get("from_bp"), row.get("to_bp")
        do_mint(fb, tb, bp_idx.get(fb, {}).get("parent_city_id"), bp_idx.get(tb, {}).get("parent_city_id"), row.get("market", "?"))

    for mkey, mval in (corridors_doc.get("markets") or {}).items():
        for corr in mval.get("corridors") or []:
            label = f"{corr.get('from')} -> {corr.get('to')}"
            if (mkey, label) not in pending_keys:
                continue
            from_bp, to_bp, from_city, to_city = resolve_corridor_endpoints(corr, bp_idx)
            do_mint(from_bp, to_bp, from_city, to_city, mkey)

    if args.mesh:
        for city_id in MESH_CITIES:
            bps = [pid for pid, row in bp_idx.items() if row.get("parent_city_id") == city_id]
            if len(bps) < 2:
                continue
            pairs = 0
            for i, from_bp in enumerate(bps):
                for to_bp in bps[i + 1 :]:
                    if pairs >= 60:
                        break
                    a = bp_idx[from_bp]["coords"]
                    b = bp_idx[to_bp]["coords"]
                    if hav_nm(a, b) > 45:
                        continue
                    rid = mint_route_id(from_bp, to_bp, tag="pending_mesh")
                    if rid in existing:
                        continue
                    coords = build_coastal_path(a, b, mask)
                    land_km = interior_land_km(coords, mask)
                    feat = make_route_feature(
                        from_bp,
                        to_bp,
                        bp_idx[from_bp]["name"],
                        bp_idx[to_bp]["name"],
                        city_id,
                        city_id,
                        coords,
                        cities,
                        source="pending_mesh",
                        land_km=land_km,
                    )
                    feat["properties"]["id"] = rid
                    feat["properties"]["_pending_mesh"] = True
                    if land_km > LAND_THRESH_KM:
                        feat["properties"]["_qa_land_flag"] = True
                        report["allowlisted"].append({"route_id": rid, "market": f"mesh:{city_id}", "land_km": land_km})
                    new_feats.append(feat)
                    existing.add(rid)
                    pairs += 1
                    report["mesh_added"] += 1
                    report["minted"].append({"route_id": rid, "market": f"mesh:{city_id}", "tag": "mesh"})

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

    out = ROOT / "grok-routing-output/mint-pending-corridor-report.json"
    save_json(out, report)
    print(f"pending mint: {len(report['minted'])} mesh={report['mesh_added']} skip={len(report['skipped'])}")
    print(f"report: {out}")


if __name__ == "__main__":
    main()