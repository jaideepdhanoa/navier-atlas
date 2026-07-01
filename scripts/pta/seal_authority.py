#!/usr/bin/env python3
"""Seal one PTA authority: mint BPs, route pairs, bind partner JSON."""
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
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from channel_solver import HAND_WAYPOINTS, get_land_checker, hand_waypoints_for, solve_hand  # noqa: E402

HANDOFF = ROOT / "handoff/partner-map-model"
DC = ROOT / "data-clean"
PP = ROOT / "partner-pitch"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bp_id_for(node: str) -> str:
    if node.startswith("bp-"):
        return node
    h = hashlib.md5(f"pta|{node}".encode()).hexdigest()[:10]
    return f"bp-{h}"


def load_hand_catalog(slug: str) -> None:
    path = DC / f"pta_hand_waypoints_{slug.replace('-', '_')}.json"
    if not path.is_file():
        return
    catalog = load_json(path)
    for key, wps in catalog.get("waypoints", {}).items():
        parts = key.split("|", 1) if "|" in key else key.split(",", 1)
        if len(parts) == 2 and parts[0] and parts[1]:
            HAND_WAYPOINTS[(parts[0], parts[1])] = wps


def mint_bp_poi(bp: dict, city_id: str, slug: str, fbt: dict) -> str:
    node = bp["node"]
    pid = bp_id_for(node)
    pois = fbt.setdefault("poi", [])
    for poi in pois:
        props = poi.get("properties", poi)
        if props.get("id") == pid or props.get("_pta_node") == node:
            return pid

    lng, lat = bp["anchor_lnglat"]
    name = bp.get("name") or node.replace("-", " ").title()
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
            "bp_type": bp.get("type", "ferry_terminal"),
            "bp_type_label": "Ferry Terminal",
            "status": "operational",
            "confidence": "high",
            "_pta_node": node,
            "_pta_authority": slug,
            "_pta_sealed_at": utc_now(),
        },
    }
    pois.append(feat)
    return pid


def _qa_accept(coords: list) -> tuple[bool, float]:
    """Regional land QA (matches channel_solver + deploy geometry gate)."""
    from route_land_qa import evaluate_route  # noqa: WPS433

    ev = evaluate_route(coords)
    return bool(ev.get("qa_pass")), float(ev.get("interior_land_km", 0.0))


def route_geometry(
    from_node: str,
    to_node: str,
    a: tuple[float, float],
    b: tuple[float, float],
    mask,
    lc,
) -> tuple[list[list[float]], float] | None:
    from channel_solver import connect_chain, densify  # noqa: WPS433

    manual = hand_waypoints_for(from_node, to_node) or hand_waypoints_for(
        from_node, to_node, from_city_id=from_node, to_city_id=to_node
    )
    mid_lists: list[list[tuple[float, float]]] = []
    if manual:
        mid_lists.append([(w[0], w[1]) for w in manual])
    if lc:
        chain = connect_chain(lc, [a, b])
        if chain:
            geom = densify(chain)
            ok, land = _qa_accept(geom)
            if ok and land <= LAND_THRESH_KM:
                return geom, land
            if chain and len(chain) > 2:
                mid_lists.append([tuple(p) for p in chain[1:-1]])
        mid_lists.append([])

    for mids in mid_lists:
        if lc:
            solved = solve_hand(lc, a, b, mids)
            if solved and solved.get("qa_pass") and solved.get("geometry"):
                coords = solved["geometry"]
                land = float(solved.get("interior_land_km", 0.0))
                ok, land2 = _qa_accept(coords)
                if ok and min(land, land2) <= LAND_THRESH_KM:
                    return coords, min(land, land2) if land > 0 else land2
        if mids:
            coords = build_coastal_path(a, b, mask, manual_waypoints=mids)
            ok, land = _qa_accept(coords)
            if ok and land <= LAND_THRESH_KM:
                return coords, land

    coords = build_coastal_path(a, b, mask)
    ok, land = _qa_accept(coords)
    if ok and land <= LAND_THRESH_KM:
        return coords, land
    return None


def bind_partner(partner: dict, route_map: dict[tuple[str, str], str]) -> int:
    bound = 0

    def bind_item(item: dict) -> bool:
        fn = item.get("from_node_id")
        tn = item.get("to_node_id")
        if not fn or not tn:
            return False
        rid = route_map.get((fn, tn)) or route_map.get((tn, fn))
        if not rid:
            return False
        item["route_id"] = rid
        item["route_ids"] = [rid]
        item.pop("_link_status", None)
        item["_link_source"] = "grok/pta_seal_authority"
        item["_pta_bound_at"] = utc_now()
        return True

    for phase in partner.get("phases", []):
        for fr in phase.get("featured_routes", []):
            if bind_item(fr):
                bound += 1
    for j in partner.get("journeys_unlocked", []):
        if bind_item(j):
            bound += 1
    return bound


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dc", default="data-clean")
    args = ap.parse_args()

    slug = args.partner
    dossier_path = HANDOFF / f"PTA-DOSSIER-{slug}.json"
    if not dossier_path.is_file():
        print(f"✗ no dossier: {dossier_path}", file=sys.stderr)
        return 1

    dossier = load_json(dossier_path)
    dc = ROOT / args.dc
    partner_paths = [dc / "partners" / f"{slug}.json", PP / "partners" / f"{slug}.json"]

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(dc / "ROUTES.json")
    routes = route_features(routes_raw)
    existing = {route_id_of(r) for r in routes}

    load_hand_catalog(slug)
    mask = load_land_mask()
    lc = get_land_checker()
    cities = build_city_index(fbt)

    bps = dossier["domestic_network"]["boarding_points"]
    node_meta: dict[str, dict] = {b["node"]: b for b in bps}
    pairs = list(dossier["domestic_network"].get("domestic_pairs", []))
    for link in dossier.get("regional_links", {}).get("links", []):
        if link.get("from") in node_meta and link.get("to") in node_meta:
            pairs.append(link)

    node_to_bp: dict[str, str] = {}

    for bp in bps:
        city_id = bp.get("city") or dossier.get("authority", {}).get("home_city")
        if not city_id and partner_paths[0].is_file():
            p = load_json(partner_paths[0])
            hc = (p.get("_public_transit_authority") or {}).get("home_cities") or p.get("cities") or []
            city_id = hc[0] if hc else None
        if not city_id:
            city_id = slug
        pid = mint_bp_poi(bp, city_id, slug, fbt)
        node_to_bp[bp["node"]] = pid

    route_map: dict[tuple[str, str], str] = {}
    minted: list[dict] = []
    failed: list[dict] = []

    for pair in pairs:
        fn, tn = pair["from"], pair["to"]
        if fn not in node_meta or tn not in node_meta:
            failed.append({"pair": pair.get("pair_id"), "reason": "missing_bp"})
            continue
        from_bp = node_to_bp[fn]
        to_bp = node_to_bp[tn]
        tag = f"pta-{slug}"
        rid = mint_route_id(from_bp, to_bp, tag=tag)
        if rid in existing:
            route_map[(fn, tn)] = rid
            continue

        a = tuple(node_meta[fn]["anchor_lnglat"])
        b = tuple(node_meta[tn]["anchor_lnglat"])
        geom = route_geometry(fn, tn, a, b, mask, lc)
        if not geom:
            failed.append({"pair": pair.get("pair_id"), "from": fn, "to": tn, "reason": "land_crossing"})
            continue
        coords, land_km = geom
        from_city = node_meta[fn].get("city")
        to_city = node_meta[tn].get("city")
        feat = make_route_feature(
            from_bp,
            to_bp,
            node_meta[fn].get("name", fn),
            node_meta[tn].get("name", tn),
            from_city,
            to_city,
            coords,
            cities,
            source=f"pta_{slug}",
            land_km=land_km,
        )
        feat["properties"]["id"] = rid
        feat["properties"]["_pta_pair_id"] = pair.get("pair_id")
        feat["properties"]["_pta_node_from"] = fn
        feat["properties"]["_pta_node_to"] = tn
        routes.append(feat)
        existing.add(rid)
        route_map[(fn, tn)] = rid
        minted.append({"pair_id": pair.get("pair_id"), "route_id": rid, "land_km": land_km})

    bound_total = 0
    for ppath in partner_paths:
        if not ppath.is_file():
            continue
        partner = load_json(ppath)
        bound_total = max(bound_total, bind_partner(partner, route_map))
        if args.apply:
            save_json(ppath, partner)

    report = {
        "partner": slug,
        "generated_at": utc_now(),
        "bps_minted": len(node_to_bp),
        "routes_minted": len(minted),
        "routes_failed": len(failed),
        "partner_bindings": bound_total,
        "minted": minted,
        "failed": failed,
    }

    receipt = HANDOFF / f"PTA-SEAL-RECEIPT-{slug}.json"
    print(json.dumps(report, indent=2))

    if args.apply:
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        save_routes(dc / "ROUTES.json", routes)
        receipt.write_text(json.dumps(report, indent=2) + "\n")
        print(f"✓ sealed {slug}: {len(minted)} routes, {bound_total} bindings → {receipt}")
    else:
        print("(dry-run — pass --apply to write)")

    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())