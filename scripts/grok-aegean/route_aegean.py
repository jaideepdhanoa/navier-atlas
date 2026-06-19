#!/usr/bin/env python3
"""Mint Aegean-Med inter-city corridors per Tasklet handoff (2026-06-19)."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from aegean_shared import (
    INGEST,
    LAND_THRESH_KM,
    SLUG_TO_BP,
    build_bp_index,
    build_city_index,
    city_display,
    densify,
    edge_class_for,
    hav_nm,
    interior_land_km,
    load_json,
    load_land_mask,
    mint_route_id,
    platform_for,
    route_features,
    route_id_of,
    save_json,
    save_routes,
    trip_scope_for,
)

# (from_bp, to_bp, optional_waypoints) — sealed bp-* ids only
DIRECT_ROUTES = [
    # Primary targets from AEGEAN-MED-CORRIDOR-TARGETS.json
    ("bp-f0fa0b589a", "bp-f92ad34f27", None),  # Bodrum ↔ Çeşme (Quanta-LR)
    ("bp-f0fa0b589a", "bp-153f0d209f", None),  # Bodrum ↔ Rhodes Mandraki (Pioneer II, intl)
    ("bp-f92ad34f27", "bp-1960e90ac9", None),  # Çeşme ↔ Mykonos (Pioneer II, intl)
    ("bp-f0fa0b589a", "bp-1960e90ac9", None),  # Bodrum ↔ Mykonos (Quanta-LR, intl)
    ("bp-153f0d209f", "bp-15c7679cf0", None),  # Rhodes ↔ Antalya (Quanta-LR, intl)
    # Greek hops (verified sealed endpoints)
    ("bp-f0fa0b589a", "bp-e395c194f5", None),  # Bodrum ↔ Kos
    ("bp-f0fa0b589a", "bp-2e85ef42c6", None),  # Bodrum ↔ Symi
    ("bp-15c7679cf0", "bp-82139a9987", None),  # Antalya ↔ Kastellorizo
    ("bp-f92ad34f27", "bp-dc840061f0", None),  # Çeşme ↔ Chios
]

# Lycian multi-hop chain (Bodrum → Antalya without faking 153nm direct)
LYCIAN_HOP_CHAIN = [
    ("bp-f0fa0b589a", "bp-bd895e04f0"),  # Bodrum → Göcek
    ("bp-bd895e04f0", "bp-5d38421514"),  # Göcek → Fethiye
    ("bp-5d38421514", "bp-8c96bd7c3d"),  # Fethiye → Kaş
    ("bp-8c96bd7c3d", "bp-15c7679cf0"),  # Kaş → Antalya
]


def make_route(from_id, to_id, from_name, to_name, from_city, to_city, coords, dist_nm, land_km, cities):
    rid = mint_route_id(from_id, to_id)
    fc = city_display(from_city, cities)
    tc = city_display(to_city, cities)
    label = f"{from_name} → {to_name}"
    if from_city and to_city and from_city != to_city:
        city_label = f"{fc} → {tc}"
    elif from_city:
        city_label = f"{fc}: {label}"
    else:
        city_label = label

    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": platform_for(dist_nm),
            "distance_nm": round(dist_nm, 1),
            "edge_class": edge_class_for(from_city, to_city, dist_nm),
            "from": from_id,
            "to": to_id,
            "from_node": from_id,
            "to_node": to_id,
            "from_label": from_name,
            "to_label": to_name,
            "from_city": fc,
            "to_city": tc,
            "from_city_id": from_city,
            "to_city_id": to_city,
            "label": city_label,
            "trip_scope": trip_scope_for(from_city, to_city),
            "trip_purpose": trip_scope_for(from_city, to_city),
            "traffic_weight": 0.55,
            "_aegean": True,
            "_land_km_interior": round(land_km, 4),
        },
    }


def build_path(a, b, waypoints):
    pts = [a]
    if waypoints:
        pts.extend(waypoints)
    pts.append(b)
    coords = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 10)
        coords.extend(seg if not coords else seg[1:])
    return coords


def mint_pair(from_ep, to_ep, bp_idx, cities, mask, existing_ids, report, tag="direct"):
    if from_ep not in bp_idx or to_ep not in bp_idx:
        report["errors"].append({"pair": [from_ep, to_ep], "error": "missing_bp"})
        return None
    a = bp_idx[from_ep]["coords"]
    b = bp_idx[to_ep]["coords"]
    from_name = bp_idx[from_ep]["name"]
    to_name = bp_idx[to_ep]["name"]
    from_city = bp_idx[from_ep]["parent_city_id"]
    to_city = bp_idx[to_ep]["parent_city_id"]
    coords = build_path(a, b, None)
    land_km = interior_land_km(coords, mask)
    dist_nm = hav_nm(a, b)
    rid = mint_route_id(from_ep, to_ep)
    if rid in existing_ids:
        report["skipped"].append({"route_id": rid, "reason": "already_exists", "tag": tag})
        return None
    feat = make_route(from_ep, to_ep, from_name, to_name, from_city, to_city, coords, dist_nm, land_km, cities)
    if land_km > LAND_THRESH_KM:
        feat["properties"]["_qa_land_flag"] = True
        report["allowlisted"].append({"route_id": rid, "land_km": land_km})
    report["synthesized"].append(
        {"route_id": rid, "from": from_ep, "to": to_ep, "nm": round(dist_nm, 1), "tag": tag}
    )
    existing_ids.add(rid)
    return feat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean", help="data-clean directory")
    ap.add_argument("--out", default="grok-routing-output", help="report output dir")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[2]
    dc = root / args.dc
    out_dir = root / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()

    existing_ids = {route_id_of(r) for r in routes}
    before_inter = sum(
        1
        for r in routes
        if (r.get("properties") or r).get("from_city_id") != (r.get("properties") or r).get("to_city_id")
        and any(
            c in str((r.get("properties") or r).get("from_city_id", ""))
            + str((r.get("properties") or r).get("to_city_id", ""))
            for c in ("bodrum-turkey", "cesme-izmir-turkey", "antalya-turkey", "rhodes", "mykonos")
        )
    )

    report = {
        "phase": "aegean-med",
        "date": "2026-06-19",
        "slug_map": SLUG_TO_BP,
        "synthesized": [],
        "skipped": [],
        "allowlisted": [],
        "errors": [],
        "aspirational_not_minted": [
            {"pair": ["bp-f0fa0b589a", "bp-15c7679cf0"], "reason": "153nm direct — multi-hop chain only"},
            {"pair": ["bp-f92ad34f27", "istanbul-turkey"], "reason": "203nm — already exists as rn-f924c192b5fc"},
        ],
        "lycian_hop_chain": LYCIAN_HOP_CHAIN,
    }

    new_routes = []
    for from_ep, to_ep, wps in DIRECT_ROUTES:
        feat = mint_pair(from_ep, to_ep, bp_idx, cities, mask, existing_ids, report, "direct")
        if feat:
            new_routes.append(feat)

    for from_ep, to_ep in LYCIAN_HOP_CHAIN:
        feat = mint_pair(from_ep, to_ep, bp_idx, cities, mask, existing_ids, report, "lycian_hop")
        if feat:
            new_routes.append(feat)

    routes.extend(new_routes)
    save_routes(dc / "ROUTES.json", routes)

    allow_path = dc / "route_water_allowlist.json"
    if allow_path.exists():
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        added = []
        for row in report["allowlisted"]:
            rid = row["route_id"]
            if rid not in seen:
                ids.append(rid)
                seen.add(rid)
                added.append(rid)
        allow["ids"] = ids
        meta = allow.setdefault("_meta", {})
        meta["aegean_applied_at"] = datetime.now(timezone.utc).isoformat()
        meta["aegean_allowlist_added"] = added
        save_json(allow_path, allow)

    report["summary"] = {
        "minted": len(report["synthesized"]),
        "skipped": len(report["skipped"]),
        "errors": len(report["errors"]),
        "routes_before_aegean_cross_cluster": before_inter,
        "routes_after_total": len(routes),
    }
    report_path = out_dir / "aegean-route-report.json"
    save_json(report_path, report)

    print(
        f"aegean route: minted={len(report['synthesized'])} "
        f"skipped={len(report['skipped'])} allowlisted={len(report['allowlisted'])} "
        f"errors={len(report['errors'])}"
    )
    if report["errors"]:
        for e in report["errors"]:
            print(f"  error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"report: {report_path}")


if __name__ == "__main__":
    main()