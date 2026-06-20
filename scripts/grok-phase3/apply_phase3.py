#!/usr/bin/env python3
"""Apply Grok Phase-3 geometries per APPLY-LEDGER.json (authoritative)."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def save_routes(path: Path, features: list):
    path.write_text(json.dumps(features, separators=(",", ":")) + "\n")


def route_features(routes_obj) -> list:
    if isinstance(routes_obj, list):
        return routes_obj
    return routes_obj.get("features", [])


def route_id_of(feat: dict) -> str:
    p = feat.get("properties", feat)
    return p.get("id") or p.get("route_id") or ""


def mint_bp_id(payload: dict) -> str:
    seed = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "bp-" + hashlib.sha256(seed.encode()).hexdigest()[:10]


def mint_route_id(from_bp: str, to_bp: str) -> str:
    seed = f"phase3|{from_bp}|{to_bp}"
    return "rn-" + hashlib.md5(seed.encode()).hexdigest()[:12]


def build_bp_index(features_by_type: dict) -> dict:
    idx = {}
    for poi in features_by_type.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        if not pid:
            continue
        coords = poi.get("geometry", {}).get("coordinates", [None, None])
        idx[pid] = {
            "name": props.get("name") or props.get("fullName") or pid,
            "shortName": props.get("shortName"),
            "parent_city_id": props.get("parent_city_id"),
            "coords": coords,
            "bp_type": props.get("bp_type"),
        }
    return idx


def build_city_index(features_by_type: dict) -> dict:
    idx = {}
    for city in features_by_type.get("city", []):
        props = city.get("properties", city)
        cid = props.get("id")
        if cid:
            idx[cid] = props.get("name") or props.get("shortName") or cid
    for pc in features_by_type.get("priority_city", []):
        props = pc.get("properties", pc)
        cid = props.get("id")
        if cid and cid not in idx:
            idx[cid] = props.get("name") or props.get("shortName") or cid
    return idx


def city_display(city_id: str | None, cities: dict) -> str:
    if not city_id:
        return "Unknown"
    return cities.get(city_id, city_id.replace("-uae", "").replace("-", " ").title())


def edge_class_for(from_city: str | None, to_city: str | None, dist_nm: float) -> str:
    if from_city and to_city and from_city == to_city:
        return "local"
    if dist_nm >= 70:
        return "regional"
    return "local"


def trip_scope_for(from_city: str | None, to_city: str | None) -> str:
    if from_city and to_city and from_city == to_city:
        return "intra_city"
    return "inter_city"


def platform_for(dist_nm: float) -> str:
    return "Quanta-LR" if dist_nm >= 70 else "Pioneer II"


def make_bp_feature(bp_id: str, payload: dict) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    name = payload["name"]
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [payload["lng"], payload["lat"]],
        },
        "properties": {
            "id": bp_id,
            "type": "poi",
            "name": name,
            "shortName": name.split("(")[0].strip(),
            "parent_city_id": payload.get("parent_city_id"),
            "bp_type": payload.get("bp_type", "public_pier"),
            "relevance": payload.get("relevance"),
            "coords_resolved": True,
            "confidence": "medium",
            "status": "operational",
            "display_type": payload.get("bp_type", "public_pier"),
            "linked_locale": payload.get("linked_locale"),
            "fullName": name,
            "tier_sort_key": 5,
            "last_enriched": now,
            "_minted_by": "grok-phase3-ci",
        },
    }


def make_synthesize_feature(
    from_bp: str,
    to_bp: str,
    geometry: dict,
    bp_index: dict,
    cities: dict,
    dist_nm: float,
    tier: str,
) -> dict:
    fb, tb = bp_index[from_bp], bp_index[to_bp]
    from_city_id = fb.get("parent_city_id")
    to_city_id = tb.get("parent_city_id")
    from_city = city_display(from_city_id, cities)
    to_city = city_display(to_city_id, cities)
    rid = mint_route_id(from_bp, to_bp)
    label = f"{from_city}: {fb['name']} → {tb['name']}"
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "id": rid,
            "from": from_bp,
            "to": to_bp,
            "from_label": fb["name"],
            "to_label": tb["name"],
            "from_city_id": from_city_id,
            "to_city_id": to_city_id,
            "from_city": from_city,
            "to_city": to_city,
            "label": label,
            "platform": platform_for(dist_nm),
            "distance_nm": round(dist_nm, 1),
            "edge_class": edge_class_for(from_city_id, to_city_id, dist_nm),
            "trip_scope": trip_scope_for(from_city_id, to_city_id),
            "traffic_weight": 0.2,
            "trip_purpose": None,
            "_pending_route_pin": True,
            "_wp_provenance": f"grok-phase3-synthesize ({tier})",
            "_applied_at": datetime.now(timezone.utc).isoformat(),
        },
    }


def slug_to_bp_map(ledger: dict, khalifa_bp: str | None) -> dict:
    m = {}
    for slug, row in ledger["endpoint_crosswalk_verified"].items():
        if row.get("status") == "apply" and row.get("bp_id"):
            m[slug] = row["bp_id"]
        elif row.get("status") == "mint" and khalifa_bp:
            m[slug] = khalifa_bp
    return m


def solutions_index(solutions_path: Path) -> dict:
    idx = {}
    with solutions_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if not row.get("qa_pass") or not row.get("geometry"):
                continue
            key = (row.get("from_id"), row.get("to_id"))
            idx[key] = row
            if row.get("route_id"):
                idx[("route_id", row["route_id"])] = row
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, help="grok-phase3 work tree root")
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    ledger = load_json(work / "APPLY-LEDGER.json")
    solutions = solutions_index(work / "grok-routing-output" / "route-solutions.jsonl")

    fbt_path = dc / "FEATURES_BY_TYPE.json"
    routes_path = dc / "ROUTES.json"
    features_by_type = load_json(fbt_path)
    routes = route_features(load_json(routes_path))
    route_by_id = {route_id_of(f): i for i, f in enumerate(routes)}

    bp_index = build_bp_index(features_by_type)
    cities = build_city_index(features_by_type)

    report = {
        "minted_bps": [],
        "synthesized": [],
        "patched": [],
        "held": [],
        "errors": [],
    }

    # 1. Mint Khalifa Port
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
        report["synthesized"].append(
            {"route_id": rid, "from": from_slug, "to": to_slug, "bucket": bucket}
        )

    for pair in ledger["apply_synthesize_clean"]:
        apply_synthesize_pair(pair["from"], pair["to"], "apply_synthesize_clean")

    for pair in ledger["apply_synthesize_after_khalifa_mint"]:
        apply_synthesize_pair(pair["from"], pair["to"], "apply_synthesize_after_khalifa_mint")

    for pair in ledger["hold_synthesize_phantom"]:
        report["held"].append(pair)

    # 2. Patch resolve / rn-* / ics rows
    for key, row in list(solutions.items()):
        if key[0] != "route_id":
            continue
        rid = key[1]
        if rid not in route_by_id:
            report["errors"].append(f"patch target missing in ROUTES: {rid}")
            continue
        feat = routes[route_by_id[rid]]
        feat["geometry"] = row["geometry"]
        props = feat.setdefault("properties", feat)
        if row.get("distance_nm_geom") is not None:
            props["distance_nm"] = round(float(row["distance_nm_geom"]), 1)
        props["_wp_provenance"] = f"grok-phase3-patch ({row.get('priority_tier', '')})"
        props["_applied_at"] = datetime.now(timezone.utc).isoformat()
        report["patched"].append(rid)

    save_json(fbt_path, features_by_type)
    save_routes(routes_path, routes)

    report_path = work / "grok-routing-output" / "phase3-apply-report.json"
    save_json(report_path, report)

    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(f"apply finished with {len(report['errors'])} error(s)")


if __name__ == "__main__":
    main()