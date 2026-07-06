#!/usr/bin/env python3
"""Mint Maghreb BP wishlist piers + candidate corridors (Tasklet 53d03496).

Verify geometry (land QA), mesh coastal paths, mint routes, stamp cluster_id.
Nobody invents a pier — coords are sourced in BP-WISHLIST JSON.

Usage:
  python3 scripts/grok-global/apply_maghreb_bp_wishlist.py --dry-run
  python3 scripts/grok-global/apply_maghreb_bp_wishlist.py --apply
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts"))

from bolt_yango_routing_shared import (  # noqa: E402
    LAND_THRESH_KM,
    build_bp_index,
    build_coastal_path,
    build_city_index,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)
from partner_scope_py import load_clusters  # noqa: E402

WISHLIST = ROOT / "handoff" / "dark-map" / "BP-WISHLIST-yassir-maghreb-2026-07-06.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
FBT_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
CLUSTERS_PATH = ROOT / "data-clean" / "CLUSTERS.json"
REPORT_PATH = ROOT / "grok-routing-output" / "maghreb-bp-wishlist-mint-report.json"

LAND_MAX_KM = 0.4
CITY_META = {
    "annaba-algeria": {"name": "Annaba", "country": "Algeria", "region": "Maghreb", "cluster_id": "algeria"},
    "tangier-morocco": {"name": "Tangier", "country": "Morocco", "region": "Maghreb", "cluster_id": "morocco"},
    "al-hoceima-morocco": {"name": "Al Hoceima", "country": "Morocco", "region": "Maghreb", "cluster_id": "morocco"},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower())
    return s.strip("-")


def bp_id_for(city_id: str, name: str) -> str:
    h = hashlib.md5(f"maghreb-wishlist|{city_id}|{name}".encode()).hexdigest()[:10]
    return f"bp-{h}"


def ensure_city(city_id: str, meta: dict, fbt: dict, report: dict, *, apply: bool) -> None:
    for bucket in ("city", "priority_city"):
        for feat in fbt.get(bucket, []) or []:
            if (feat.get("properties") or {}).get("id") == city_id:
                return
    if city_id not in CITY_META:
        return
    spec = CITY_META[city_id]
    # Use first wishlist BP coord as anchor if city missing
    report["cities_added"].append(city_id)
    if not apply:
        return
    feat = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": meta.get("anchor") or [-1, 0]},
        "properties": {
            "id": city_id,
            "type": "city",
            "name": spec["name"],
            "shortName": spec["name"],
            "fullName": spec["name"],
            "country": spec["country"],
            "region": spec["region"],
            "platform_class": "dual-platform",
            "cluster_id": spec["cluster_id"],
            "_maghreb_wishlist_mint": utc_now(),
        },
    }
    fbt.setdefault("city", []).append(feat)


def ensure_cluster_member(city_id: str, cluster_id: str, clusters_doc: dict, report: dict, *, apply: bool) -> None:
    for c in clusters_doc.get("clusters") or []:
        if c.get("cluster_id") != cluster_id:
            continue
        members = list(c.get("member_city_ids") or [])
        if city_id in members:
            return
        report["cluster_members"].append({"cluster_id": cluster_id, "city_id": city_id})
        if apply:
            members.append(city_id)
            c["member_city_ids"] = members
            c["members_present"] = len(members)
            c["_maghreb_wishlist_mint"] = utc_now()
        return


def mint_bp(bp: dict, city_id: str, fbt: dict, report: dict, *, apply: bool) -> str | None:
    name = bp["name"]
    pid = bp_id_for(city_id, name)
    pois = fbt.get("poi", []) or []
    for poi in pois:
        p = poi.get("properties") or poi
        if p.get("id") == pid:
            return pid
    lon, lat = bp["lon"], bp["lat"]
    report["bps_minted"].append({"bp_id": pid, "city_id": city_id, "name": name})
    if not apply:
        return pid
    pois.append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "id": pid,
                "type": "poi",
                "name": name,
                "shortName": name[:48],
                "fullName": name,
                "parent_city_id": city_id,
                "bp_type": "marina",
                "status": "operational",
                "confidence": "high",
                "source_url": bp.get("source"),
                "_maghreb_wishlist_mint": utc_now(),
            },
        }
    )
    fbt["poi"] = pois
    return pid


def parse_od(od: str) -> tuple[str, str]:
    for sep in (" ↔ ", " ↔", "↔ ", " → ", "->"):
        if sep in od:
            a, b = od.split(sep, 1)
            return a.strip(), b.strip()
    return od.strip(), od.strip()


def match_bp(name: str, bp_map: dict[str, tuple[str, str, str]]) -> str | None:
    nl = name.lower()
    tokens = [t for t in re.split(r"[^a-z0-9]+", nl) if len(t) > 3]
    best: tuple[float, str] | None = None
    for pid, (nm, _city, _cid) in bp_map.items():
        nml = nm.lower()
        if nl in nml or nml in nl:
            return pid
        overlap = sum(1 for t in tokens if t in nml)
        if overlap and (best is None or overlap > best[0]):
            best = (overlap, pid)
    return best[1] if best else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    wishlist = load_json(WISHLIST)
    fbt = load_json(FBT_PATH)
    clusters_doc = load_json(CLUSTERS_PATH)
    routes = route_features(load_json(ROUTES_PATH))
    existing_ids = {(r.get("properties") or r).get("id") for r in routes}
    existing_eps: set[tuple[str, str]] = set()
    for r in routes:
        p = r.get("properties") or r
        fn, tn = p.get("from_node"), p.get("to_node")
        if fn and tn:
            existing_eps.add((fn, tn))
            existing_eps.add((tn, fn))

    mask = load_land_mask()
    cities = build_city_index(fbt)
    _, _, city_to_cluster = load_clusters(ROOT / "data-clean")

    report: dict = {
        "generated": utc_now(),
        "mode": "apply" if apply else "dry-run",
        "cities_added": [],
        "cluster_members": [],
        "bps_minted": [],
        "routes_minted": [],
        "skipped": [],
    }

    for market in wishlist.get("markets") or []:
        city_id = market["city_id"]
        cluster_id = market["cluster_id"]
        anchor = None
        bps = market.get("boarding_points") or []
        if bps:
            anchor = [bps[0]["lon"], bps[0]["lat"]]
        ensure_city(city_id, {"anchor": anchor}, fbt, report, apply=apply)
        ensure_cluster_member(city_id, cluster_id, clusters_doc, report, apply=apply)

        bp_map: dict[str, tuple[str, str, str]] = {}
        for bp in bps:
            pid = mint_bp(bp, city_id, fbt, report, apply=apply)
            if pid:
                bp_map[pid] = (bp["name"], city_id, cluster_id)

        if apply:
            bp_idx = build_bp_index(fbt)
        else:
            bp_idx = {}

        for corr in market.get("candidate_corridors") or []:
            a_name, b_name = parse_od(corr.get("od", ""))
            if apply:
                from_bp = match_bp(a_name, bp_map)
                to_bp = match_bp(b_name, bp_map)
            else:
                from_bp = to_bp = "dry"
            if not from_bp or not to_bp or from_bp == to_bp:
                report["skipped"].append({"od": corr.get("od"), "reason": "bp_unresolved"})
                continue
            if apply:
                ep = (from_bp, to_bp)
                if ep in existing_eps:
                    report["skipped"].append({"od": corr.get("od"), "reason": "endpoint_pair_exists"})
                    continue
                a = bp_idx[from_bp]["coords"]
                b = bp_idx[to_bp]["coords"]
                coords = build_coastal_path(a, b, mask)
                land_km = interior_land_km(coords, mask)
                approx = float(corr.get("approx_nm") or 99)
                if land_km > LAND_MAX_KM and not (approx <= 3 and land_km <= 3.0):
                    report["skipped"].append(
                        {"od": corr.get("od"), "reason": "land_qa", "land_km": land_km, "approx_nm": approx}
                    )
                    continue
                feat = make_route_feature(
                    from_bp,
                    to_bp,
                    bp_idx[from_bp]["name"],
                    bp_idx[to_bp]["name"],
                    city_id,
                    city_id,
                    coords,
                    cities,
                    source="maghreb_bp_wishlist",
                    land_km=land_km,
                )
                p = feat.get("properties") or feat
                rid = mint_route_id(from_bp, to_bp, tag=slugify(city_id)[:8])
                while rid in existing_ids:
                    rid = mint_route_id(from_bp, to_bp, tag=slugify(city_id)[:6] + "x")
                p["id"] = rid
                p["cluster_id"] = cluster_id
                p["cluster_city_id"] = city_id
                p["_maghreb_bp_wishlist_mint"] = utc_now()
                routes.append(feat)
                existing_ids.add(rid)
                existing_eps.add(ep)
                existing_eps.add((ep[1], ep[0]))
                report["routes_minted"].append({"route_id": rid, "od": corr.get("od"), "nm": p.get("distance_nm")})
            else:
                report["routes_minted"].append({"od": corr.get("od"), "city_id": city_id, "dry": True})

    if apply:
        save_routes(ROUTES_PATH, routes)
        save_json(FBT_PATH, fbt)
        save_json(CLUSTERS_PATH, clusters_doc)

    report["summary"] = {
        "bps": len(report["bps_minted"]),
        "routes": len([r for r in report["routes_minted"] if r.get("route_id") or r.get("dry")]),
        "skipped": len(report["skipped"]),
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT_PATH, report)
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())