#!/usr/bin/env python3
"""Seal ABC islands geometry: split lumped node, mint BPs, build corridors (PR #93)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bucketB_shared import densify, hav_nm, load_land_mask  # noqa: E402
from route_land_qa import interior_land_km as qa_interior_land_km  # noqa: E402
from bolt_yango_routing_shared import (  # noqa: E402
    build_city_index,
    build_coastal_path,
    load_json,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

STAGING = ROOT / "partner-pitch/seal-staging/curacao-caribbean-2026-06-24"
REPORT_PATH = ROOT / "grok-routing-output/abc-islands-seal-report.json"
COUNTRY_REF = STAGING / "caribbean/caribbean-country-reference-rows.json"
TAG = "abc_islands"
LUMP = "aruba-curacao-bonaire"

NODE_ALIASES = {
    "curacao-curacao__spanish-water-caracasbaai": "curacao-curacao__spanish-water-jan-thiel",
}

CITY_DEFS = [
    ("aruba-aruba", "Aruba", "Aruba", -70.035, 12.519, "Aruba", "Caribbean"),
    ("curacao-curacao", "Curaçao", "Curaçao", -68.935, 12.108, "Curaçao", "Caribbean"),
    ("bonaire-bonaire", "Bonaire", "Bonaire", -68.277, 12.150, "Bonaire", "Caribbean"),
]

# Canonical BPs: (city_id, node_suffix, name, lng, lat, bp_type, source_ids_to_retire)
BP_DEFS: list[tuple] = [
    ("aruba-aruba", "oranjestad-cruise-terminal", "Oranjestad Cruise Terminal", -70.042605, 12.519636, "cruise_terminal", ("bp-b50d68b868",)),
    ("aruba-aruba", "oranjestad-renaissance-marina", "Renaissance Marina (Oranjestad)", -70.038813, 12.518219, "marina", ("bp-a83d4c5ed1",)),
    ("aruba-aruba", "palm-beach-resort-strip", "Palm Beach resort strip", -70.058, 12.572, "resort_jetty", ()),
    ("aruba-aruba", "queen-beatrix-airport-waterfront", "Queen Beatrix Airport waterfront", -70.013, 12.503, "airport_waterfront", ()),
    ("aruba-aruba", "spanish-lagoon-savaneta", "Spanish Lagoon / Savaneta", -69.945, 12.452, "marina", ()),
    ("curacao-curacao", "willemstad-sint-anna-bay", "Willemstad / Sint Anna Bay (Otrobanda mega-pier)", -68.935, 12.108, "cruise_terminal", ("bp-1acf06c512", "bp-722adaba93", "bp-a37e547625")),
    ("curacao-curacao", "spanish-water-jan-thiel", "Spanish Water / Caracasbaai (Jan Thiel)", -68.855, 12.078, "marina", ()),
    ("curacao-curacao", "hato-airport-waterfront", "Hato (Curaçao Int'l) airport waterfront", -68.958, 12.183, "airport_waterfront", ()),
    ("curacao-curacao", "klein-curacao-day-trip", "Klein Curaçao day-trip jetty", -68.645, 11.984, "day_trip_island", ("bp-klein-curacao-pier",)),
    ("curacao-curacao", "sandals-royal-curacao-spanish-water", "Sandals Royal Curaçao (Spanish Water)", -68.85, 12.067, "resort_jetty", ()),
    ("curacao-curacao", "baoase-luxury-resort", "Baoase Luxury Resort", -68.90, 12.094, "resort_jetty", ()),
    ("curacao-curacao", "piscadera-bay-resort-cluster", "Piscadera Bay (Marriott / JW cluster)", -68.97, 12.12, "resort_jetty", ()),
    ("bonaire-bonaire", "kralendijk-town-pier", "Kralendijk Town Pier", -68.277, 12.150, "town_pier", ("bp-546c2641aa", "bp-221c50831b")),
    ("bonaire-bonaire", "klein-bonaire-dive-transfer", "Klein Bonaire dive transfer", -68.305, 12.162, "dive_transfer", ("bp-klein-bonaire-pier",)),
    ("bonaire-bonaire", "harbour-village-marina", "Harbour Village Marina", -68.285, 12.169, "marina", ("bp-7e72884496",)),
]

CORRIDORS = [
    # (from_suffix, to_suffix, tier, waypoints[(lng,lat)])
    (
        "curacao-curacao__spanish-water-jan-thiel",
        "bonaire-bonaire__kralendijk-town-pier",
        "grounded",
        [(-68.78, 12.02), (-68.58, 11.98), (-68.38, 12.00), (-68.30, 12.08)],
    ),
    (
        "curacao-curacao__spanish-water-jan-thiel",
        "curacao-curacao__klein-curacao-day-trip",
        "seasonal",
        [(-68.78, 12.02), (-68.70, 11.99), (-68.66, 11.985)],
    ),
    ("bonaire-bonaire__kralendijk-town-pier", "bonaire-bonaire__klein-bonaire-dive-transfer", "grounded", [(-68.29, 12.155)]),
    ("bonaire-bonaire__kralendijk-town-pier", "bonaire-bonaire__harbour-village-marina", "grounded", [(-68.28, 12.158)]),
    (
        "aruba-aruba__oranjestad-cruise-terminal",
        "aruba-aruba__palm-beach-resort-strip",
        "grounded",
        [(-70.04, 12.52), (-70.05, 12.545), (-70.055, 12.56)],
    ),
    (
        "aruba-aruba__queen-beatrix-airport-waterfront",
        "aruba-aruba__palm-beach-resort-strip",
        "grounded",
        [(-70.02, 12.51), (-70.03, 12.53), (-70.04, 12.555), (-70.055, 12.568)],
    ),
    (
        "curacao-curacao__willemstad-sint-anna-bay",
        "curacao-curacao__spanish-water-jan-thiel",
        "grounded",
        [(-68.92, 12.095), (-68.89, 12.085), (-68.87, 12.08)],
    ),
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__spanish-water-jan-thiel",
        "grounded",
        [(-69.02, 12.16), (-69.08, 12.10), (-69.10, 12.02), (-69.00, 11.98), (-68.88, 12.06), (-68.86, 12.082)],
    ),
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__sandals-royal-curacao-spanish-water",
        "grounded",
        [(-69.02, 12.16), (-69.08, 12.10), (-69.10, 12.02), (-69.00, 11.98), (-68.87, 12.05), (-68.85, 12.067)],
    ),
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__baoase-luxury-resort",
        "grounded",
        [(-69.02, 12.16), (-69.08, 12.10), (-69.10, 12.02), (-69.00, 11.98), (-68.92, 12.06), (-68.90, 12.094)],
    ),
    (
        "curacao-curacao__willemstad-sint-anna-bay",
        "curacao-curacao__sandals-royal-curacao-spanish-water",
        "grounded",
        [(-68.92, 12.095), (-68.88, 12.08), (-68.86, 12.072)],
    ),
    ("curacao-curacao__willemstad-sint-anna-bay", "curacao-curacao__piscadera-bay-resort-cluster", "grounded", [(-68.95, 12.11)]),
    (
        "curacao-curacao__spanish-water-jan-thiel",
        "curacao-curacao__baoase-luxury-resort",
        "grounded",
        [(-68.87, 12.085), (-68.88, 12.09)],
    ),
    (
        "aruba-aruba__oranjestad-renaissance-marina",
        "curacao-curacao__spanish-water-jan-thiel",
        "roadmap",
        [(-69.85, 12.30), (-69.45, 12.18), (-69.05, 12.10), (-68.88, 12.082)],
    ),
    (
        "aruba-aruba__oranjestad-renaissance-marina",
        "bonaire-bonaire__kralendijk-town-pier",
        "roadmap",
        [(-69.70, 12.25), (-69.20, 12.08), (-68.65, 12.02), (-68.35, 12.06)],
    ),
]

LAND_THRESH = {"inter_island": 1.5, "intra_island": 0.08, "roadmap": 12.0, "default": 0.08}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def node_id(city_id: str, suffix: str) -> str:
    return f"{city_id}__{suffix}" if "__" not in suffix else suffix


def classify_island(lon: float, lat: float) -> str:
    if lon < -69.5:
        return "aruba-aruba"
    if lat < 12.0 and lon > -68.7:
        return "curacao-curacao"
    if lon > -68.45:
        return "bonaire-bonaire"
    return "curacao-curacao"


def city_feature(cid: str, name: str, short: str, lng: float, lat: float, country: str, region: str) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": cid,
            "type": "city",
            "name": name,
            "shortName": short,
            "fullName": name,
            "country": country,
            "region": region,
            "parent_cluster": "abc-islands",
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": f"grok_{TAG}_2026-06-24",
            "confidence": "high",
            "status": "operational",
            f"_{TAG}_mint": True,
        },
    }


def poi_feature(node: str, name: str, lng: float, lat: float, city_id: str, bp_type: str, *, retired_from: tuple[str, ...] = ()) -> dict:
    props = {
        "id": node,
        "type": "poi",
        "name": name,
        "shortName": name.split("(")[0].strip()[:40],
        "parent_city_id": city_id,
        "bp_type": bp_type,
        "coords_resolved": True,
        "confidence": "high",
        "status": "operational",
        "source_url": f"seal:{TAG}",
        f"_{TAG}_mint": True,
        f"_{TAG}_applied_at": utc_now(),
    }
    if retired_from:
        props["_id_matched_from"] = list(retired_from)
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": props,
    }


def nudge_seaward(lon: float, lat: float, mask) -> tuple[float, float]:
    from bolt_yango_routing_shared import is_water  # noqa: WPS433

    if is_water(lon, lat, mask):
        return lon, lat
    for dlng, dlat in ((0.008, 0), (0.015, 0), (0, 0.008), (0.01, 0.01)):
        for sx in (1, -1):
            for sy in (1, -1):
                nl, nt = lon + dlng * sx, lat + dlat * sy
                if is_water(nl, nt, mask):
                    return nl, nt
    return lon, lat


def land_threshold(tier: str, from_city: str, to_city: str) -> float:
    if tier == "roadmap":
        return LAND_THRESH["roadmap"]
    if from_city != to_city:
        return LAND_THRESH["inter_island"]
    return LAND_THRESH["intra_island"]


def build_path(
    a: tuple[float, float],
    b: tuple[float, float],
    wps: list[tuple[float, float]] | None,
    mask,
    *,
    tier: str,
    from_city: str,
    to_city: str,
) -> tuple[list, float, float]:
    thresh = land_threshold(tier, from_city, to_city)
    pts = [a] + list(wps or []) + [b]
    coords: list[list[float]] = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 22)
        coords.extend(seg if not coords else seg[1:])
    land_km = qa_interior_land_km(coords, apron_km=0.25)
    if land_km > thresh:
        coords = build_coastal_path(a, b, mask, wps)
        land_km = qa_interior_land_km(coords, apron_km=0.25)
    return coords, land_km, hav_nm(a, b)


def replace_lump(val: str | None) -> str | None:
    if val == LUMP:
        return "aruba-aruba"
    if val and LUMP in val:
        return val.replace(LUMP, "curacao-curacao")
    return val


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes = route_features(load_json(dc / "ROUTES.json"))
    clusters = load_json(dc / "CLUSTERS.json")
    mask = load_land_mask()

    poi_before = len(fbt.get("poi", []))
    routes_before = len(routes)

    report: dict = {
        "at": utc_now(),
        "lane": f"grok/{TAG}",
        "apply": args.apply,
        "nodes_minted": [],
        "bps_sealed": [],
        "bps_dropped": [],
        "poi_rekeyed": 0,
        "routes_built": [],
        "routes_culled": [],
        "routes_repointed": 0,
        "silent_drops": 0,
    }

    cities = fbt.setdefault("city", [])
    city_ids = {f["properties"]["id"] for f in cities if f.get("properties", {}).get("id")}
    for row in CITY_DEFS:
        if row[0] not in city_ids:
            cities.append(city_feature(*row))
            report["nodes_minted"].append(row[0])
            city_ids.add(row[0])

    for layer in ("city", "priority_city"):
        kept = []
        for feat in fbt.get(layer, []):
            p = feat.get("properties", {})
            if p.get("id") == LUMP:
                p["_retired"] = True
                p["_superseded_by"] = ["aruba-aruba", "curacao-curacao", "bonaire-bonaire"]
                p["_retired_at"] = utc_now()
                p["status"] = "retired"
                if layer == "city":
                    continue
            kept.append(feat)
        if layer == "city":
            fbt["city"] = kept + [f for f in cities if f["properties"]["id"] != LUMP or f["properties"].get("_retired")]

    retire_ids: set[str] = set()
    for _city, _suffix, _name, _lng, _lat, _typ, src_ids in BP_DEFS:
        retire_ids.update(src_ids)

    bp_coords: dict[str, tuple[float, float]] = {}
    bp_meta: dict[str, dict] = {}
    for city_id, suffix, name, lng, lat, bp_type, src_ids in BP_DEFS:
        nid = node_id(city_id, suffix)
        bp_coords[nid] = (lng, lat)
        bp_meta[nid] = {"name": name, "city_id": city_id, "bp_type": bp_type, "src_ids": src_ids}

    poi_by_id: dict[str, dict] = {}
    for poi in fbt.get("poi", []):
        pid = (poi.get("properties") or {}).get("id")
        if pid:
            poi_by_id[pid] = poi

    for nid, meta in bp_meta.items():
        lng, lat = bp_coords[nid]
        lng, lat = nudge_seaward(lng, lat, mask)
        bp_coords[nid] = (lng, lat)
        feat = poi_feature(nid, meta["name"], lng, lat, meta["city_id"], meta["bp_type"], retired_from=meta["src_ids"])
        poi_by_id[nid] = feat
        report["bps_sealed"].append(nid)

    rekeyed = 0
    supplemental = []
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        if pid in poi_by_id and pid in bp_meta:
            continue
        if pid in retire_ids:
            report["bps_dropped"].append({"id": pid, "reason": "superseded_by_canonical_bp"})
            continue
        if props.get("parent_city_id") == LUMP:
            coords = poi.get("geometry", {}).get("coordinates") or [0, 0]
            new_parent = classify_island(coords[0], coords[1])
            props["parent_city_id"] = new_parent
            props["_rekey_from"] = LUMP
            props["_rekey_at"] = utc_now()
            rekeyed += 1
            supplemental.append(poi)
        elif props.get("parent_city_id") not in (None, "") and pid not in poi_by_id:
            supplemental.append(poi)
        elif pid not in poi_by_id:
            supplemental.append(poi)

    fbt["poi"] = list(poi_by_id.values()) + supplemental
    report["poi_rekeyed"] = rekeyed
    report["poi_after"] = len(fbt["poi"])

    cities_idx = build_city_index(fbt)
    existing_ids = {(r.get("properties") or r).get("id") for r in routes}
    route_by_pair: dict[tuple[str, str], str] = {}
    pair_to_feat: dict[tuple[str, str], dict] = {}
    for feat in routes:
        p = feat.get("properties", feat)
        fn = p.get("from_node") or p.get("from")
        tn = p.get("to_node") or p.get("to")
        if fn and tn:
            pair_to_feat[(fn, tn)] = feat
            pair_to_feat[(tn, fn)] = feat

    def endpoint_coords(node: str) -> tuple[float, float] | None:
        node = NODE_ALIASES.get(node, node)
        if node in bp_coords:
            return bp_coords[node]
        return None

    for from_n, to_n, tier, wps in CORRIDORS:
        from_n = NODE_ALIASES.get(from_n, from_n)
        to_n = NODE_ALIASES.get(to_n, to_n)
        fa = endpoint_coords(from_n)
        tb = endpoint_coords(to_n)
        if not fa or not tb:
            report["routes_culled"].append({"from": from_n, "to": to_n, "reason": "endpoint_missing"})
            continue
        from_city = from_n.split("__", 1)[0]
        to_city = to_n.split("__", 1)[0]
        thresh = land_threshold(tier, from_city, to_city)
        coords, land_km, dist_nm = build_path(fa, tb, wps, mask, tier=tier, from_city=from_city, to_city=to_city)
        if land_km > thresh and tier != "roadmap":
            report["routes_culled"].append({"from": from_n, "to": to_n, "reason": f"land_km={land_km:.3f}"})
            continue
        if tier == "grounded" and dist_nm > 70:
            report["routes_culled"].append({"from": from_n, "to": to_n, "reason": f"pioneer_ii_gate_dist={dist_nm:.1f}"})
            continue

        from_name = bp_meta.get(from_n, {}).get("name", from_n)
        to_name = bp_meta.get(to_n, {}).get("name", to_n)
        rid = mint_route_id(from_n, to_n, TAG)
        existing_feat = pair_to_feat.get((from_n, to_n))
        if existing_feat:
            rid = (existing_feat.get("properties") or existing_feat).get("id") or rid

        feat = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "id": rid,
                "platform": "Quanta-LR" if tier == "roadmap" or dist_nm > 70 else "Pioneer II",
                "distance_nm": round(dist_nm, 1),
                "edge_class": "inter-island" if from_city != to_city else "intra-city",
                "from": from_n,
                "to": to_n,
                "from_node": from_n,
                "to_node": to_n,
                "from_label": from_name,
                "to_label": to_name,
                "from_city": from_city,
                "to_city": to_city,
                "from_city_id": from_city,
                "to_city_id": to_city,
                "label": f"{from_name} → {to_name}",
                "trip_scope": "inter_island" if from_city != to_city else "intra_island",
                "traffic_weight": 0.72 if from_n.endswith("spanish-water-jan-thiel") and to_n.startswith("bonaire") else 0.55,
                "interior_land_km": round(land_km, 4),
                f"_{TAG}_applied_at": utc_now(),
                "_geometry_status": "sealed",
                "_tier": tier,
            },
        }
        if tier == "seasonal":
            feat["properties"]["render_mode"] = "seasonal-amber"
            feat["properties"]["_seasonal"] = True
        if tier == "roadmap":
            feat["properties"]["_aspirational"] = True
            feat["properties"]["render_mode"] = "amber-dashed"
            feat["properties"]["_vessel_gate"] = "Quanta-LR roadmap (amber-dashed)"

        if existing_feat:
            existing_feat["geometry"] = feat["geometry"]
            existing_feat["properties"].update(feat["properties"])
            feat = existing_feat
        else:
            routes.append(feat)
            existing_ids.add(rid)
        pair_to_feat[(from_n, to_n)] = feat
        pair_to_feat[(to_n, from_n)] = feat
        route_by_pair[(from_n, to_n)] = rid
        route_by_pair[(to_n, from_n)] = rid
        report["routes_built"].append({
            "from": from_n,
            "to": to_n,
            "route_id": rid,
            "distance_nm": round(dist_nm, 1),
            "tier": tier,
            "land_km": round(land_km, 4),
        })

    canonical_pairs: set[tuple[str, str]] = set()
    for from_n, to_n, *_ in CORRIDORS:
        from_n = NODE_ALIASES.get(from_n, from_n)
        to_n = NODE_ALIASES.get(to_n, to_n)
        canonical_pairs.add((from_n, to_n))
        canonical_pairs.add((to_n, from_n))

    culled = []
    kept = []
    seen_canonical: set[tuple[str, str]] = set()
    for feat in routes:
        p = feat.get("properties", feat)
        rid = p.get("id", "")
        fn = p.get("from_node") or p.get("from")
        tn = p.get("to_node") or p.get("to")
        pair_key = (fn, tn) if fn and tn else None
        if pair_key in canonical_pairs:
            want_rid = mint_route_id(fn, tn, TAG)
            if rid != want_rid and pair_key in seen_canonical:
                culled.append({"id": rid, "reason": "abc_duplicate_pair"})
                continue
            if rid == want_rid or pair_key not in seen_canonical:
                seen_canonical.add(pair_key)
                seen_canonical.add((tn, fn))
        fc = p.get("from_city_id") or p.get("from_city")
        tc = p.get("to_city_id") or p.get("to_city")
        if fc == LUMP or tc == LUMP or p.get("cluster_city_id") == LUMP:
            if str(rid).startswith("ics-"):
                culled.append({"id": rid, "reason": "lump_ics_self_loop"})
                continue
            p["from_city_id"] = replace_lump(fc) or "aruba-aruba"
            p["to_city_id"] = replace_lump(tc) or "aruba-aruba"
            p["from_city"] = p["from_city_id"]
            p["to_city"] = p["to_city_id"]
            if p.get("to") == LUMP:
                p["to"] = "aruba-aruba"
            if p.get("from") == LUMP:
                p["from"] = "aruba-aruba"
            p[f"_{TAG}_repoint"] = utc_now()
            report["routes_repointed"] += 1
        if str(rid).startswith("ics-") and (fc == LUMP or tc == LUMP):
            culled.append({"id": rid, "reason": "lump_ics"})
            continue
        kept.append(feat)
    routes = kept
    report["routes_culled"].extend(culled)
    report["routes_after"] = len(routes)

    for cl in clusters.get("clusters") or []:
        if cl.get("cluster_id") == "abc-islands":
            cl["member_city_ids"] = ["aruba-aruba", "curacao-curacao", "bonaire-bonaire"]
            cl["members_present"] = 3
            cl["members_missing"] = []
            cl["anchor"] = [-68.935, 12.108]
            cl["anchor_source"] = "curacao-curacao__willemstad-sint-anna-bay"
            cl["_abc_debundle_at"] = utc_now()

    expected_bps = {node_id(c, s) for c, s, *_ in BP_DEFS}
    sealed_set = set(report["bps_sealed"])
    if expected_bps - sealed_set:
        report["silent_drops"] = len(expected_bps - sealed_set)
        report["bps_missing"] = sorted(expected_bps - sealed_set)

    def _within_land_gate(c: dict) -> bool:
        if c.get("tier") == "roadmap":
            return True
        fc = c["from"].split("__", 1)[0]
        tc = c["to"].split("__", 1)[0]
        return c.get("land_km", 0) <= land_threshold(c.get("tier", "grounded"), fc, tc)

    report["land_crossing_proof"] = all(_within_land_gate(c) for c in report["routes_built"])
    report["route_by_pair"] = {f"{a}|{b}": rid for (a, b), rid in route_by_pair.items()}

    if args.apply:
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        save_routes(dc / "ROUTES.json", routes)
        save_json(dc / "CLUSTERS.json", clusters)
        cref_path = ROOT / "finance/model/country-reference.json"
        if cref_path.exists() and COUNTRY_REF.exists():
            cref = load_json(cref_path)
            for country, row in load_json(COUNTRY_REF).get("rows", {}).items():
                cref.setdefault(country, {}).update(row)
            cref["_abc_islands_additions_at"] = utc_now()
            save_json(cref_path, cref)

        brief_idx = load_json(dc / "city_briefs/_index.json")
        if isinstance(brief_idx, list):
            brief_idx = [b for b in brief_idx if b.get("city_id") != LUMP]
            for cid, name, *_ in CITY_DEFS:
                if not any(b.get("city_id") == cid for b in brief_idx):
                    brief_idx.append({"city_id": cid, "name": name, "region": "Caribbean"})
            save_json(dc / "city_briefs/_index.json", brief_idx)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)
    print(json.dumps({
        "nodes_minted": report["nodes_minted"],
        "bps_sealed": len(report["bps_sealed"]),
        "bps_dropped": len(report["bps_dropped"]),
        "poi_rekeyed": report["poi_rekeyed"],
        "routes_built": len(report["routes_built"]),
        "routes_culled": len(report["routes_culled"]),
        "routes_repointed": report["routes_repointed"],
        "silent_drops": report["silent_drops"],
        "poi_before": poi_before,
        "poi_after": report.get("poi_after"),
        "routes_before": routes_before,
        "routes_after": report.get("routes_after"),
    }, indent=2))
    return 0 if report["silent_drops"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())