#!/usr/bin/env python3
"""Mint PTA authority city nodes, boarding points, and starter sealed routes."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    LAND_THRESH_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from channel_solver import get_land_checker, hand_waypoints_for, solve_hand  # noqa: E402

HANDOFF = ROOT / "handoff/partner-map-model"
DC = ROOT / "data-clean"

# Junk POIs to quarantine so relink/bind lanes cannot pick them for these cities.
JUNK_POI_IDS = frozenset(
    {
        "bp-bcfc48aae1",  # Oslo Road Boat Ramp (Florida)
        "bp-b718f46797",  # Fort Amsterdam (Caribbean)
        "bp-71155e0dbe",  # Wellington Point Boat Ramp (Australia)
        "bp-6825d03a00",  # Mystic Wellington Yacht Club (US)
    }
)

CITY_SPECS: dict[str, dict] = {
    "oslo-norway": {
        "name": "Oslo",
        "country": "Norway",
        "region": "Europe",
        "cluster_id": "norway",
        "coordinates": [10.7522, 59.9139],
        "boarding_points": [
            {"node": "oslo-aker-brygge", "name": "Aker Brygge Ferry Terminal", "anchor_lnglat": [10.732, 59.908]},
            {"node": "oslo-nesoddtangen", "name": "Nesoddtangen Ferry Terminal", "anchor_lnglat": [10.665, 59.862]},
            {"node": "oslo-hovedoya", "name": "Hovedøya Island Pier", "anchor_lnglat": [10.768, 59.894]},
            {"node": "oslo-bygdoy", "name": "Bygdøy Ferry Pier", "anchor_lnglat": [10.688, 59.901]},
        ],
        "starter_pairs": [
            ("oslo-aker-brygge", "oslo-nesoddtangen"),
            ("oslo-aker-brygge", "oslo-hovedoya"),
            ("oslo-aker-brygge", "oslo-bygdoy"),
            ("oslo-hovedoya", "oslo-bygdoy"),
        ],
    },
    "amsterdam-netherlands": {
        "name": "Amsterdam",
        "country": "Netherlands",
        "region": "Europe",
        "cluster_id": "netherlands",
        "coordinates": [4.9041, 52.3676],
        "boarding_points": [
            {"node": "ams-centraal-ij", "name": "Centraal Station IJ Pontoon", "anchor_lnglat": [4.897, 52.383]},
            {"node": "ams-buiksloterweg", "name": "Buiksloterweg Ferry Pontoon", "anchor_lnglat": [4.920, 52.400]},
            {"node": "ams-ijplein", "name": "IJplein Ferry Pontoon", "anchor_lnglat": [4.910, 52.388]},
            {"node": "ams-ndsm", "name": "NDSM Ferry Pontoon", "anchor_lnglat": [4.892, 52.405]},
        ],
        "starter_pairs": [
            ("ams-centraal-ij", "ams-buiksloterweg"),
            ("ams-centraal-ij", "ams-ijplein"),
            ("ams-centraal-ij", "ams-ndsm"),
            ("ams-buiksloterweg", "ams-ndsm"),
        ],
    },
    "wellington-new-zealand": {
        "name": "Wellington",
        "country": "New Zealand",
        "region": "Oceania",
        "cluster_id": "new-zealand",
        "coordinates": [174.7762, -41.2865],
        "boarding_points": [
            {"node": "wlg-queens-wharf", "name": "Queens Wharf Ferry Terminal", "anchor_lnglat": [174.778, -41.286]},
            {"node": "wlg-days-bay", "name": "Days Bay Wharf", "anchor_lnglat": [174.917, -41.212]},
            {"node": "wlg-seatoun", "name": "Seatoun Wharf", "anchor_lnglat": [174.833, -41.320]},
            {"node": "wlg-somes-island", "name": "Somes Island (Matiu) Pier", "anchor_lnglat": [174.857, -41.257]},
        ],
        "starter_pairs": [
            ("wlg-queens-wharf", "wlg-days-bay"),
            ("wlg-queens-wharf", "wlg-seatoun"),
            ("wlg-queens-wharf", "wlg-somes-island"),
            ("wlg-seatoun", "wlg-somes-island"),
        ],
    },
    "copenhagen-denmark": {
        "name": "Copenhagen",
        "country": "Denmark",
        "region": "Europe",
        "cluster_id": "denmark",
        "coordinates": [12.5683, 55.6761],
        "boarding_points": [
            {"node": "cph-nyhavn", "name": "Nyhavn Harbour Bus Stop", "anchor_lnglat": [12.590, 55.680]},
            {"node": "cph-refshaleoen", "name": "Refshaleøen Ferry Stop", "anchor_lnglat": [12.610, 55.693]},
            {"node": "cph-opera", "name": "Opera House Ferry Stop", "anchor_lnglat": [12.602, 55.682]},
            {"node": "cph-nordre-toldbod", "name": "Nordre Toldbod Ferry Stop", "anchor_lnglat": [12.595, 55.685]},
        ],
        "starter_pairs": [
            ("cph-nyhavn", "cph-opera"),
            ("cph-nyhavn", "cph-refshaleoen"),
            ("cph-opera", "cph-nordre-toldbod"),
            ("cph-nordre-toldbod", "cph-refshaleoen"),
        ],
    },
    "gothenburg-sweden": {
        "name": "Gothenburg",
        "country": "Sweden",
        "region": "Europe",
        "cluster_id": "sweden",
        "coordinates": [11.9746, 57.7089],
        "boarding_points": [
            {"node": "got-saltholmen", "name": "Saltholmen Ferry Terminal", "anchor_lnglat": [11.870, 57.665]},
            {"node": "got-styrso-bratten", "name": "Styrsö Bratten Pier", "anchor_lnglat": [11.810, 57.638]},
            {"node": "got-vrango", "name": "Vrångö Pier", "anchor_lnglat": [11.760, 57.600]},
            {"node": "got-fiskebackskil", "name": "Fiskebäckskil Pier", "anchor_lnglat": [11.920, 57.680]},
        ],
        "starter_pairs": [
            ("got-saltholmen", "got-styrso-bratten"),
            ("got-saltholmen", "got-vrango"),
            ("got-styrso-bratten", "got-vrango"),
            ("got-saltholmen", "got-fiskebackskil"),
        ],
    },
    "rotterdam-netherlands": {
        "name": "Rotterdam",
        "country": "Netherlands",
        "region": "Europe",
        "cluster_id": "netherlands",
        "coordinates": [4.4777, 51.9244],
        "boarding_points": [
            {"node": "rtd-erasmusbrug", "name": "Erasmusbrug (Willemsplein) Waterbus", "anchor_lnglat": [4.482, 51.916]},
            {"node": "rtd-dordrecht", "name": "Dordrecht Merwekade Waterbus", "anchor_lnglat": [4.668, 51.808]},
            {"node": "rtd-kinderdijk", "name": "Kinderdijk Waterbus Stop", "anchor_lnglat": [4.635, 51.883]},
            {"node": "rtd-hoek-van-holland", "name": "Hoek van Holland Haven", "anchor_lnglat": [4.133, 51.977]},
        ],
        "starter_pairs": [
            ("rtd-erasmusbrug", "rtd-dordrecht"),
            ("rtd-erasmusbrug", "rtd-kinderdijk"),
            ("rtd-dordrecht", "rtd-kinderdijk"),
            ("rtd-erasmusbrug", "rtd-hoek-van-holland"),
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bp_id_for(node: str, city_id: str) -> str:
    h = hashlib.md5(f"pta-mint|{city_id}|{node}".encode()).hexdigest()[:10]
    return f"bp-{h}"


def quarantine_junk_pois(fbt: dict) -> list[str]:
    quarantined = []
    for poi in fbt.get("poi", []) or []:
        props = poi.get("properties", poi)
        pid = props.get("id")
        if pid in JUNK_POI_IDS and not props.get("_quarantine"):
            props["_quarantine"] = True
            props["_quarantine_reason"] = "pta_mint_heavy_misgeocode"
            props["_quarantine_at"] = utc_now()
            quarantined.append(pid)
    return quarantined


def mint_city_feature(city_id: str, spec: dict) -> dict:
    lng, lat = spec["coordinates"]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": city_id,
            "type": "priority_city",
            "name": spec["name"],
            "shortName": spec["name"],
            "fullName": spec["name"],
            "country": spec["country"],
            "region": spec["region"],
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "pta_mint_authority_city",
            "confidence": "high",
            "status": "operational",
            "tier_sort_key": 2,
            "cluster_id": spec["cluster_id"],
            "_pta_minted_at": utc_now(),
        },
    }


def mint_bp_poi(bp: dict, city_id: str, fbt: dict) -> str:
    node = bp["node"]
    pid = bp_id_for(node, city_id)
    pois = fbt.setdefault("poi", [])
    for poi in pois:
        props = poi.get("properties", poi)
        if props.get("id") == pid or props.get("_pta_node") == node:
            return pid
    lng, lat = bp["anchor_lnglat"]
    name = bp["name"]
    feat = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": pid,
            "type": "poi",
            "name": name,
            "shortName": name[:40],
            "fullName": name,
            "parent_city_id": city_id,
            "bp_type": "ferry_terminal",
            "bp_type_label": "Ferry Terminal",
            "status": "operational",
            "confidence": "high",
            "_pta_node": node,
            "_pta_mint_city": city_id,
            "_pta_minted_at": utc_now(),
        },
    }
    pois.append(feat)
    return pid


PAIR_WAYPOINTS: dict[str, list[list[float]]] = {
    # Oslo — Oslofjord ferry lanes (mid-fjord)
    "oslo-aker-brygge|oslo-nesoddtangen": [[10.71, 59.885], [10.68, 59.872], [10.665, 59.866]],
    "oslo-aker-brygge|oslo-hovedoya": [[10.745, 59.904], [10.758, 59.899]],
    "oslo-aker-brygge|oslo-bygdoy": [[10.705, 59.907], [10.692, 59.904]],
    "oslo-hovedoya|oslo-bygdoy": [[10.725, 59.899], [10.698, 59.901]],
    # Amsterdam — IJ (centreline, mid-channel)
    "ams-centraal-ij|ams-buiksloterweg": [[4.905, 52.388], [4.912, 52.394], [4.916, 52.398]],
    "ams-centraal-ij|ams-ijplein": [[4.903, 52.385], [4.906, 52.386]],
    "ams-centraal-ij|ams-ndsm": [[4.900, 52.388], [4.896, 52.395], [4.894, 52.402]],
    "ams-buiksloterweg|ams-ndsm": [[4.906, 52.402], [4.899, 52.403]],
    # Wellington — harbour
    "wlg-queens-wharf|wlg-days-bay": [[174.82, -41.27], [174.87, -41.24], [174.9, -41.22]],
    "wlg-queens-wharf|wlg-seatoun": [[174.8, -41.3], [174.82, -41.31]],
    "wlg-queens-wharf|wlg-somes-island": [[174.81, -41.28], [174.84, -41.265]],
    # Copenhagen — harbour bus lanes
    "cph-nyhavn|cph-opera": [[12.596, 55.681]],
    "cph-nyhavn|cph-refshaleoen": [[12.6, 55.688], [12.605, 55.692]],
    "cph-opera|cph-nordre-toldbod": [[12.598, 55.684]],
    "cph-nordre-toldbod|cph-refshaleoen": [[12.602, 55.69]],
    # Gothenburg — archipelago
    "got-saltholmen|got-styrso-bratten": [[11.84, 57.65], [11.82, 57.64]],
    "got-saltholmen|got-vrango": [[11.82, 57.63], [11.78, 57.61]],
    "got-styrso-bratten|got-vrango": [[11.78, 57.62]],
    "got-saltholmen|got-fiskebackskil": [[11.89, 57.67], [11.91, 57.68]],
    # Rotterdam — Nieuwe Maas / Waterbus (river centreline)
    "rtd-erasmusbrug|rtd-dordrecht": [[4.52, 51.915], [4.58, 51.895], [4.63, 51.865], [4.66, 51.815]],
    "rtd-erasmusbrug|rtd-kinderdijk": [[4.53, 51.912], [4.58, 51.895], [4.63, 51.885]],
    "rtd-dordrecht|rtd-kinderdijk": [[4.655, 51.845], [4.64, 51.875]],
    "rtd-erasmusbrug|rtd-hoek-van-holland": [[4.40, 51.925], [4.30, 51.945], [4.18, 51.965]],
}


def route_geometry(
    fn: str,
    tn: str,
    a: tuple[float, float],
    b: tuple[float, float],
    mask,
    lc,
) -> tuple[list, float] | None:
    from route_land_qa import evaluate_route  # noqa: WPS433

    key = f"{fn}|{tn}"
    manual = PAIR_WAYPOINTS.get(key) or PAIR_WAYPOINTS.get(f"{tn}|{fn}") or []
    mids = [(w[0], w[1]) for w in manual]

    attempts: list[list[tuple[float, float]]] = []
    if mids:
        attempts.append(mids)
    attempts.append([])

    for mid_list in attempts:
        if lc:
            solved = solve_hand(lc, a, b, mid_list)
            if solved and solved.get("qa_pass") and solved.get("geometry"):
                coords = solved["geometry"]
                ev = evaluate_route(coords)
                if ev.get("qa_pass") and float(ev.get("interior_land_km", 0)) <= LAND_THRESH_KM:
                    return coords, float(ev.get("interior_land_km", 0))
        if mid_list:
            coords = build_coastal_path(a, b, mask, manual_waypoints=mid_list)
            ev = evaluate_route(coords)
            if ev.get("qa_pass") and float(ev.get("interior_land_km", 0)) <= LAND_THRESH_KM:
                return coords, float(ev.get("interior_land_km", 0))

    if mids:
        from channel_solver import densify  # noqa: WPS433

        chain = densify([a] + mids + [b])
        ev = evaluate_route(chain)
        if ev.get("qa_pass") and float(ev.get("interior_land_km", 0)) <= LAND_THRESH_KM:
            return chain, float(ev.get("interior_land_km", 0))

    coords = build_coastal_path(a, b, mask)
    ev = evaluate_route(coords)
    if ev.get("qa_pass") and float(ev.get("interior_land_km", 0)) <= LAND_THRESH_KM:
        return coords, float(ev.get("interior_land_km", 0))
    return None


def register_cluster(city_id: str, spec: dict, anchor_bp: str | None) -> None:
    clusters_path = DC / "CLUSTERS.json"
    doc = load_json(clusters_path)
    cluster_id = spec["cluster_id"]
    found = None
    for cl in doc.get("clusters", []):
        if cl.get("cluster_id") == cluster_id:
            found = cl
            break
    if not found:
        found = {
            "cluster_id": cluster_id,
            "cluster_label": spec["country"] if cluster_id in ("denmark", "netherlands") else spec["name"],
            "region": spec["region"],
            "type": "coastal",
            "anchor": spec["coordinates"],
            "member_city_ids": [],
            "members_present": 0,
            "members_missing": [],
            "anchor_source": anchor_bp or city_id,
            "_pta_minted_at": utc_now(),
        }
        doc.setdefault("clusters", []).append(found)
    members = found.setdefault("member_city_ids", [])
    if city_id not in members:
        members.append(city_id)
    found["members_present"] = len(members)
    if anchor_bp:
        found["anchor_source"] = anchor_bp
    save_json(clusters_path, doc)


def mint_city(city_id: str, apply: bool) -> dict:
    spec = CITY_SPECS[city_id]
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(DC / "ROUTES.json")
    routes = route_features(routes_raw)
    existing = {route_id_of(r) for r in routes}

    quarantined = quarantine_junk_pois(fbt)

    cities_bucket = fbt.setdefault("priority_city", [])
    city_exists = any(
        (c.get("properties", c).get("id") == city_id) for c in cities_bucket
    )
    if not city_exists:
        cities_bucket.append(mint_city_feature(city_id, spec))

    mask = load_land_mask()
    lc = get_land_checker()
    cities = build_city_index(fbt)

    node_meta = {b["node"]: b for b in spec["boarding_points"]}
    node_to_bp: dict[str, str] = {}
    boarding_points_out = []
    for bp in spec["boarding_points"]:
        pid = mint_bp_poi(bp, city_id, fbt)
        node_to_bp[bp["node"]] = pid
        boarding_points_out.append(
            {
                "node": bp["node"],
                "bp_id": pid,
                "name": bp["name"],
                "anchor_lnglat": bp["anchor_lnglat"],
            }
        )

    sealed_routes = []
    failed = []
    anchor_bp = boarding_points_out[0]["bp_id"] if boarding_points_out else None

    for fn, tn in spec["starter_pairs"]:
        if fn not in node_meta or tn not in node_meta:
            failed.append({"from": fn, "to": tn, "reason": "missing_node"})
            continue
        from_bp = node_to_bp[fn]
        to_bp = node_to_bp[tn]
        tag = f"pta-mint-{city_id}"
        rid = mint_route_id(from_bp, to_bp, tag=tag)
        if rid in existing:
            sealed_routes.append({"route_id": rid, "from_bp": from_bp, "to_bp": to_bp, "status": "existing"})
            continue
        a = tuple(node_meta[fn]["anchor_lnglat"])
        b = tuple(node_meta[tn]["anchor_lnglat"])
        geom = route_geometry(fn, tn, a, b, mask, lc)
        if not geom:
            failed.append({"from": fn, "to": tn, "reason": "land_crossing"})
            continue
        coords, land_km = geom
        feat = make_route_feature(
            from_bp,
            to_bp,
            node_meta[fn]["name"],
            node_meta[tn]["name"],
            city_id,
            city_id,
            coords,
            cities,
            source=f"pta_mint_{city_id}",
            land_km=land_km,
        )
        feat["properties"]["id"] = rid
        feat["properties"]["_pta_mint_city"] = city_id
        routes.append(feat)
        existing.add(rid)
        sealed_routes.append(
            {
                "route_id": rid,
                "from_bp": from_bp,
                "to_bp": to_bp,
                "from_node": fn,
                "to_node": tn,
                "distance_nm": feat["properties"].get("distance_nm"),
                "land_km": land_km,
            }
        )

    receipt = {
        "city_id": city_id,
        "generated_at": utc_now(),
        "city_feature_id": city_id,
        "coordinates": spec["coordinates"],
        "cluster_id": spec["cluster_id"],
        "boarding_points": boarding_points_out,
        "sealed_routes": sealed_routes,
        "routes_failed": failed,
        "junk_quarantined": quarantined,
        "generator": "scripts/pta/mint_authority_city.py",
    }

    if apply:
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)
        save_routes(DC / "ROUTES.json", routes)
        register_cluster(city_id, spec, anchor_bp)
        out = HANDOFF / f"GEOMETRY-MINT-RECEIPT-{city_id}.json"
        out.write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"✓ minted {city_id}: {len(boarding_points_out)} BPs, {len(sealed_routes)} routes → {out}")
    else:
        print(json.dumps(receipt, indent=2))
        print("(dry-run — pass --apply to write)")

    return receipt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", action="append", dest="cities")
    ap.add_argument("--all-mint-heavy", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    targets = list(CITY_SPECS.keys()) if args.all_mint_heavy else (args.cities or [])
    if not targets:
        ap.error("pass --city <id> or --all-mint-heavy")

    failed_any = False
    for cid in targets:
        if cid not in CITY_SPECS:
            print(f"✗ unknown city: {cid}", file=sys.stderr)
            failed_any = True
            continue
        r = mint_city(cid, args.apply)
        if r.get("routes_failed"):
            failed_any = True
    return 2 if failed_any else 0


if __name__ == "__main__":
    raise SystemExit(main())