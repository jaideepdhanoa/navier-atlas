#!/usr/bin/env python3
"""
Mint declared gcn-* corridor route_ids into ROUTES.json (preserve IDs).
Resolves endpoints via BP labels; coastal geometry via bolt_yango_routing_shared.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORRIDORS = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
DEFAULT_INGEST = ROOT / "_ingest/bp-seal-2026-06-20"

sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_routing_shared import (  # noqa: E402
    LAND_THRESH_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    make_route_feature,
    resolve_corridor_endpoints,
    route_features,
    route_id_of,
    save_json,
    save_routes,
    load_land_mask,
)


def iter_corridors(corridors_doc: dict, prefixes: tuple[str, ...]) -> list[tuple[str, dict, dict]]:
    rows = []
    for key, val in (corridors_doc.get("markets") or {}).items():
        if not isinstance(val, dict):
            continue
        if prefixes and not any(key.startswith(p) or key == p for p in prefixes):
            continue
        for corr in val.get("corridors") or []:
            rows.append((key, val, corr))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--corridors", default=str(DEFAULT_CORRIDORS))
    ap.add_argument(
        "--markets",
        default="",
        help="Comma-separated market prefixes (default: all gcn corridors)",
    )
    ap.add_argument("--out-report", default="grok-routing-output/gcn-mint-report.json")
    args = ap.parse_args()

    dc = ROOT / args.dc
    prefixes = tuple(p.strip() for p in args.markets.split(",") if p.strip()) or ()

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    corridors_doc = load_json(Path(args.corridors))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()

    existing = {route_id_of(r) for r in routes}
    report = {
        "phase": "mint_gcn_corridor_routes",
        "generated": datetime.now(timezone.utc).isoformat(),
        "minted": [],
        "skipped": [],
        "allowlisted": [],
    }

    candidates = []
    for mkey, mval, corr in iter_corridors(corridors_doc, prefixes):
        rid = corr.get("route_id")
        if not rid or not str(rid).startswith("gcn-"):
            continue
        if rid in existing:
            report["skipped"].append({"route_id": rid, "market": mkey, "reason": "already_in_gold"})
            continue
        candidates.append((mkey, mval, corr, rid))

    for mkey, mval, corr, rid in candidates:
        from_bp, to_bp, from_city, to_city = resolve_corridor_endpoints(corr, bp_idx)
        if not from_bp or not to_bp:
            report["skipped"].append(
                {
                    "route_id": rid,
                    "market": mkey,
                    "from": corr.get("from"),
                    "to": corr.get("to"),
                    "reason": "unresolved_bp",
                }
            )
            continue
        if from_bp == to_bp:
            report["skipped"].append({"route_id": rid, "market": mkey, "reason": "same_bp"})
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
            source="gcn_mint",
            land_km=land_km,
        )
        feat["properties"]["id"] = rid
        feat["properties"]["_gcn_corridor"] = True
        feat["properties"]["_corridor_market"] = mkey
        if land_km > LAND_THRESH_KM:
            feat["properties"]["_qa_land_flag"] = True
            report["allowlisted"].append({"route_id": rid, "land_km": land_km, "market": mkey})

        routes.append(feat)
        existing.add(rid)
        report["minted"].append(
            {
                "route_id": rid,
                "market": mkey,
                "from_bp": from_bp,
                "to_bp": to_bp,
                "nm": feat["properties"]["distance_nm"],
            }
        )

    save_routes(dc / "ROUTES.json", routes)

    allow_path = dc / "route_water_allowlist.json"
    if allow_path.exists():
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for row in report["allowlisted"]:
            rid = row["route_id"]
            if rid not in seen:
                ids.append(rid)
                seen.add(rid)
        allow["ids"] = ids
        allow.setdefault("_meta", {})["gcn_mint_at"] = datetime.now(timezone.utc).isoformat()
        save_json(allow_path, allow)

    out = ROOT / args.out_report
    out.parent.mkdir(parents=True, exist_ok=True)
    save_json(out, report)

    print(
        f"gcn mint: candidates={len(candidates)} minted={len(report['minted'])} "
        f"skipped={len(report['skipped'])} allowlisted={len(report['allowlisted'])}"
    )
    print(f"report: {out}")


if __name__ == "__main__":
    main()