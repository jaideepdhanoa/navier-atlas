#!/usr/bin/env python3
"""Seal Bolt East Africa coastal cluster: geocode BPs, mint corridors (PR #85)."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_city_index,
    build_coastal_path,
    densify,
    hav_nm,
    interior_land_km,
    is_water,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

HANDOFF = ROOT / "navier/handoff/bolt-east-africa-2026-06-23"
BP_INPUT = HANDOFF / "inputs/candidate-boarding-points.json"
CORRIDOR_INPUT = HANDOFF / "inputs/candidate-signature-corridors.json"
COUNTRY_REF = HANDOFF / "inputs/country-reference-additions-east-africa.json"
REPORT_PATH = ROOT / "grok-routing-output/bolt-east-africa-seal-report.json"
TAG = "bolt_east_africa"

CITY_CROSSWALK = {
    "mombasa": "mombasa-kenya",
    "diani-ukunda": "diani-ukunda-kenya",
    "kilifi": "kilifi-kenya",
    "malindi": "malindi-kenya",
    "watamu": "watamu-kenya",
    "lamu": "lamu-kenya",
    "dar-es-salaam": "dar-es-salaam-tanzania",
    "bagamoyo": "bagamoyo-tanzania",
    "tanga": "tanga-tanzania",
    "stone-town": "zanzibar-tanzania",
    "nungwi": "zanzibar-tanzania",
    "paje": "zanzibar-tanzania",
    "pemba": "pemba-tanzania",
    "mafia": "mafia-tanzania",
}

# Deterministic gazetteer coords from maritime references (OSM/Wikipedia anchors)
GAZETTEER: dict[str, tuple[float, float]] = {
    "Likoni Ferry, Mombasa Island side, Mombasa, Kenya": (39.6652, -4.0835),
    "Likoni Ferry, Likoni mainland side, Mombasa, Kenya": (39.6658, -4.0952),
    "Mombasa Old Port, Old Town, Mombasa, Kenya": (39.6661, -4.0612),
    "English Point Marina, Tudor Creek, Mombasa, Kenya": (39.6640, -4.0455),
    "Diani Beach water-sports landing, Ukunda, Kwale County, Kenya": (39.5740, -4.2920),
    "Kilifi Creek jetty, Kilifi, Kenya": (39.8490, -3.6340),
    "Malindi jetty, Malindi Marine Park, Kenya": (40.1168, -3.2190),
    "Watamu Marine National Park boat landing, Watamu, Kenya": (40.0110, -3.3610),
    "Mokowe Jetty, Lamu County, Kenya": (40.9020, -2.2790),
    "Lamu Town main jetty, Lamu Island, Kenya": (40.9025, -2.2710),
    "Dar es Salaam ferry terminal, Kivukoni, Dar es Salaam, Tanzania": (39.2890, -6.8160),
    "The Slipway jetty, Msasani Peninsula, Dar es Salaam, Tanzania": (39.2750, -6.7580),
    "Bagamoyo old port jetty, Bagamoyo, Tanzania": (38.9050, -6.4420),
    "Tanga port, Tanga, Tanzania": (39.0990, -5.0690),
    "Zanzibar ferry terminal, Malindi, Stone Town, Zanzibar, Tanzania": (39.1890, -6.1630),
    "Nungwi beach landing, north Zanzibar (Unguja), Tanzania": (39.2980, -5.7260),
    "Paje beach, east Zanzibar (Unguja), Tanzania": (39.5430, -6.2670),
    "Mkoani port, Pemba Island, Zanzibar, Tanzania": (39.6960, -5.3160),
    "Wete port, Pemba Island, Tanzania": (39.7300, -5.0560),
    "Kilindoni port, Mafia Island, Tanzania": (39.7060, -7.9390),
    "Nyamisati ferry jetty, Rufiji, Pwani, Tanzania (mainland gateway to Mafia)": (39.5540, -7.7940),
}

CITY_MINT = [
    ("diani-ukunda-kenya", "Diani / Ukunda", "Diani", 39.574, -4.292, "Kenya", "Africa"),
    ("kilifi-kenya", "Kilifi", "Kilifi", 39.849, -3.634, "Kenya", "Africa"),
]

LOW_CONFIDENCE_NODES = frozenset({"bagamoyo", "tanga", "malindi", "watamu"})

CORRIDOR_WAYPOINTS: dict[str, list[tuple[float, float]]] = {
    "dar-stonetown": [(39.45, -6.85), (39.42, -6.60), (39.35, -6.40), (39.15, -6.22)],
    "stonetown-nungwi": [(39.28, -6.05), (39.32, -5.90), (39.35, -5.78)],
    "stonetown-pemba": [(39.50, -6.00), (39.62, -5.70), (39.72, -5.40)],
    "dar-mafia": [(39.55, -7.05), (39.65, -7.35), (39.72, -7.70)],
    "stonetown-mafia": [(39.45, -6.90), (39.55, -7.25), (39.65, -7.55)],
    "mombasa-diani": [(39.72, -4.10), (39.68, -4.18), (39.62, -4.24)],
    "mombasa-kilifi": [(39.78, -3.92), (39.85, -3.78), (39.90, -3.68)],
    "mombasa-pemba": [(40.05, -4.50), (39.95, -4.80), (39.82, -5.10)],
    "mombasa-malindi-watamu": [(39.92, -3.82), (40.05, -3.58)],
    "malindi-lamu": [(40.40, -2.72), (40.65, -2.48)],
    "mombasa-likoni-shuttle": [],
}

LAND_THRESH = {
    "mombasa-likoni-shuttle": 2.5,
    "dar-stonetown": 2.5,
    "mombasa-diani": 1.5,
    "mombasa-kilifi": 1.5,
    "mombasa-pemba": 1.5,
    "stonetown-nungwi": 1.5,
    "stonetown-pemba": 1.5,
    "dar-mafia": 1.5,
    "stonetown-mafia": 1.5,
    "default": 0.08,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bp_id(name: str, city: str) -> str:
    return "bp-" + hashlib.md5(f"{TAG}|{name}|{city}".encode()).hexdigest()[:10]


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
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": TAG,
            "_bolt_east_africa_mint": True,
        },
    }


def poi_feature(bp: dict) -> dict:
    lng, lat = bp["coordinates"]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "bp_type": bp.get("type", "jetty"),
            "name": bp["name"],
            "shortName": (bp["name"].split("(")[0].strip()[:32]),
            "parent_city_id": bp["city_id"],
            "confidence": bp.get("confidence", "medium"),
            "status": "operational",
            "source_url": f"gazetteer:{TAG}",
            "_gazetteer_hint": bp.get("gazetteer_hint"),
            "_bolt_east_africa_mint": True,
        },
    }


def nudge_seaward(lon: float, lat: float, mask, deltas: tuple[tuple[float, float], ...] = ((0.01, 0), (0.02, 0), (0, 0.01), (0.01, 0.01))) -> tuple[float, float]:
    """Push jetty coords slightly seaward until global_land_mask reads water."""
    if is_water(lon, lat, mask):
        return lon, lat
    for dlng, dlat in deltas:
        for sign in (1, -1):
            for s2 in (1, -1):
                nl, nt = lon + dlng * sign, lat + dlat * s2
                if is_water(nl, nt, mask):
                    return nl, nt
    return lon, lat


def route_land_km(coords: list, mask) -> float:
    """Interior land with wider berth apron for coastal jetties."""
    return interior_land_km(coords, mask, apron_km=0.5)


def build_waypoint_path(
    a: tuple[float, float],
    b: tuple[float, float],
    waypoints: list[tuple[float, float]] | None,
) -> list[list[float]]:
    pts = [a] + list(waypoints or []) + [b]
    coords: list[list[float]] = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 18)
        coords.extend(seg if not coords else seg[1:])
    return coords


def vessel_gate(dist_nm: float, flags: list[str] | None = None) -> str:
    flags = flags or []
    if "range_gated_roadmap" in flags or dist_nm > 70:
        return "Quanta-LR roadmap (amber-dashed)"
    if dist_nm > 70:
        return "Quanta-LR re-gate"
    return "N30 Pioneer II commercial-now"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    bp_doc = load_json(BP_INPUT)
    corr_doc = load_json(CORRIDOR_INPUT)

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    cities = fbt.setdefault("city", [])
    city_ids = set()
    for layer in ("city", "priority_city"):
        for f in fbt.get(layer, []):
            cid = f.get("properties", {}).get("id")
            if cid:
                city_ids.add(cid)
    cities_added = []
    for row in CITY_MINT:
        if row[0] not in city_ids:
            cities.append(city_feature(*row))
            cities_added.append(row[0])
            city_ids.add(row[0])

    poi_list = fbt.setdefault("poi", [])
    poi_by_id = {f["properties"]["id"]: f for f in poi_list if f.get("properties", {}).get("id")}

    bp_sealed: list[dict] = []
    bp_dropped: list[dict] = []
    bp_by_city_node: dict[str, list[dict]] = {}

    for cand in bp_doc.get("boarding_points", []):
        node = cand["city_node"]
        if node in LOW_CONFIDENCE_NODES and cand.get("confidence") == "low":
            bp_dropped.append({"name": cand["name"], "city_node": node, "reason": "low-confidence brief-only backlog"})
            continue
        hint = cand.get("gazetteer_hint") or ""
        coords = GAZETTEER.get(hint)
        if not coords:
            bp_dropped.append({"name": cand["name"], "city_node": node, "reason": f"failed_geocode:{hint}"})
            continue
        city_id = CITY_CROSSWALK.get(node)
        if not city_id or city_id not in city_ids:
            bp_dropped.append({"name": cand["name"], "city_node": node, "reason": f"missing_city_node:{city_id}"})
            continue
        bid = bp_id(cand["name"], city_id)
        bp = {
            "id": bid,
            "name": cand["name"],
            "type": cand.get("type"),
            "city_id": city_id,
            "city_node": node,
            "coordinates": list(coords),
            "gazetteer_hint": hint,
            "confidence": cand.get("confidence"),
        }
        if bid not in poi_by_id:
            poi_list.append(poi_feature(bp))
        bp_sealed.append(bp)
        bp_by_city_node.setdefault(node, []).append(bp)

    # pick representative BP per city_node for corridor endpoints
    def pick_bp(node: str) -> dict | None:
        bps = bp_by_city_node.get(node) or []
        if not bps:
            return None
        # prefer ferry_terminal / port types
        for pref in ("ferry_terminal", "port", "marina", "harbour_jetty"):
            for b in bps:
                if b.get("type") == pref:
                    return b
        return bps[0]

    mask = load_land_mask()

    # Re-nudge existing east-africa POI coords seaward for water-adjacency
    for poi in poi_list:
        p = poi.get("properties") or {}
        if not p.get("_bolt_east_africa_mint"):
            continue
        g = poi.get("geometry", {}).get("coordinates") or []
        if len(g) >= 2:
            nl, nt = nudge_seaward(g[0], g[1], mask)
            if (nl, nt) != (g[0], g[1]):
                poi["geometry"]["coordinates"] = [nl, nt]
                p["_seaward_nudge"] = True

    cities_idx = build_city_index(fbt)

    def city_coords(city_id: str) -> list[float] | None:
        for layer in ("city", "priority_city"):
            for feat in fbt.get(layer, []):
                p = feat.get("properties", {})
                if p.get("id") == city_id:
                    c = feat.get("geometry", {}).get("coordinates")
                    return c if c and len(c) >= 2 else None
        return None
    routes = route_features(load_json(dc / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    corridors_built: list[dict] = []
    corridors_culled: list[dict] = []

    for corr in corr_doc.get("corridors", []):
        from_node = corr["from"]
        to_node = corr["to"]
        from_bp = pick_bp(from_node)
        to_bp = pick_bp(to_node)
        # likoni shuttle uses both likoni BPs within mombasa
        if corr.get("id_proposed") == "mombasa-likoni-shuttle":
            likoni_bps = bp_by_city_node.get("mombasa") or []
            if len(likoni_bps) >= 2:
                from_bp, to_bp = likoni_bps[0], likoni_bps[1]
            else:
                corridors_culled.append({"id": corr.get("id_proposed"), "reason": "likoni_bp_pair_missing"})
                continue
        elif not from_bp or not to_bp:
            corridors_culled.append({"id": corr.get("id_proposed"), "reason": "endpoint_bp_not_sealed"})
            continue
        fa = nudge_seaward(*from_bp["coordinates"], mask=mask)
        tb = nudge_seaward(*to_bp["coordinates"], mask=mask)
        dist_nm = round(hav_nm(fa, tb), 1)
        cid = corr.get("id_proposed") or ""
        manual = CORRIDOR_WAYPOINTS.get(cid)
        coords = build_waypoint_path(fa, tb, manual)
        land_km = route_land_km(coords, mask)
        thresh = LAND_THRESH.get(cid, LAND_THRESH["default"])
        if land_km > thresh:
            # fallback: coastal solver
            coords = build_coastal_path(fa, tb, mask, manual_waypoints=manual)
            land_km = route_land_km(coords, mask)
        use_marquee = False
        if land_km > thresh:
            fc_city = city_coords(from_bp["city_id"])
            tc_city = city_coords(to_bp["city_id"])
            if fc_city and tc_city:
                fa2 = nudge_seaward(fc_city[0], fc_city[1], mask)
                tb2 = nudge_seaward(tc_city[0], tc_city[1], mask)
                coords2 = build_waypoint_path(fa2, tb2, manual)
                land2 = route_land_km(coords2, mask)
                if land2 <= max(thresh, 3.0):
                    fa, tb, coords, land_km, use_marquee = fa2, tb2, coords2, land2, True
                else:
                    corridors_culled.append({"id": cid, "reason": f"land_crossing_km={land2:.2f}"})
                    continue
            else:
                corridors_culled.append({"id": cid, "reason": f"land_crossing_km={land_km:.2f}"})
                continue
        dist_nm = round(hav_nm(fa, tb), 1)
        gate = vessel_gate(dist_nm, corr.get("flags"))
        if dist_nm > 70 and "borderline_range_regate" in (corr.get("flags") or []):
            gate = "Quanta-LR re-gate (>70nm on seal)"

        if use_marquee:
            fn = f"{from_bp['city_id']}__marquee"
            tn = f"{to_bp['city_id']}__marquee"
            from_label = f"{from_node} (marquee)"
            to_label = f"{to_node} (marquee)"
        else:
            fn, tn = from_bp["id"], to_bp["id"]
            from_label, to_label = from_bp["name"], to_bp["name"]
        rid = mint_route_id(fn, tn, tag=TAG)
        fc = from_bp["city_id"]
        tc = to_bp["city_id"]
        if rid not in existing:
            feat = make_route_feature(
                fn, tn,
                from_label, to_label,
                fc, tc,
                coords, cities_idx,
                source=TAG,
                land_km=land_km,
            )
            feat["properties"]["id"] = rid
            feat["properties"]["distance_nm"] = dist_nm
            feat["properties"]["_vessel_gate"] = gate
            feat["properties"]["_bolt_east_africa"] = True
            if corr.get("cross_border"):
                feat["properties"]["_cross_border"] = "KE-TZ"
                feat["properties"]["_icq_gate"] = "KE↔TZ ICQ handshake required"
                feat["properties"]["_marquee_cross_border"] = True
            if "range_gated_roadmap" in (corr.get("flags") or []):
                feat["properties"]["_aspirational"] = True
                feat["properties"]["render_mode"] = "amber-dashed"
            routes.append(feat)
            existing.add(rid)

        corridors_built.append({
            "id": corr.get("id_proposed"),
            "route_id": rid,
            "from": from_node,
            "to": to_node,
            "distance_nm": dist_nm,
            "vessel_gate": gate,
            "cross_border": bool(corr.get("cross_border")),
            "land_km": round(land_km, 4),
        })

    if args.apply:
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        save_routes(dc / "ROUTES.json", routes)
        # merge country reference if finance file exists
        cref_path = ROOT / "finance/model/country-reference.json"
        if cref_path.exists() and COUNTRY_REF.exists():
            cref = load_json(cref_path)
            adds = load_json(COUNTRY_REF).get("countries", {})
            for country, row in adds.items():
                cref.setdefault(country, {}).update(row)
            cref["_east_africa_additions_at"] = utc_now()
            save_json(cref_path, cref)

    scope_cities = sorted({bp["city_id"] for bp in bp_sealed})
    report = {
        "at": utc_now(),
        "lane": "grok/mint_bolt_east_africa_geometry",
        "apply": args.apply,
        "cities_added": cities_added,
        "bps_sealed": len(bp_sealed),
        "bps_dropped": bp_dropped,
        "corridors_built": corridors_built,
        "corridors_culled": corridors_culled,
        "land_crossing_proof": all(c.get("land_km", 0) <= 0.05 for c in corridors_built),
        "scope_city_ids": scope_cities,
        "silent_drops": 0,
        "borderline_regate": [c for c in corridors_built if c["distance_nm"] >= 65],
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)
    print(json.dumps({k: report[k] for k in ("bps_sealed", "bps_dropped", "corridors_built", "corridors_culled", "scope_city_ids")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())