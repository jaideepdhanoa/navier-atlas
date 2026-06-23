#!/usr/bin/env python3
"""Grok seal — Grab Thailand upper-Gulf depth pass (PR #88).

Mints hua-hin / cha-am / koh-samet cities + BPs, builds 5 Pioneer II corridors,
binds route_ids on partner-pitch/partners/grab-thailand.json, promotes to data-clean.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bucketB_shared import densify, hav_nm, interior_land_km, load_land_mask  # noqa: E402
from bolt_yango_routing_shared import (  # noqa: E402
    build_coastal_path,
    load_json,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

DEPTH = ROOT / "partner-pitch/proposals/grab-thailand/depth-2026-06-23"
BP_DIR = DEPTH / "boarding-points"
BINDSET = DEPTH / "GRAB-THAILAND-DEPTH-BINDSET.json"
PARTNER_SRC = ROOT / "partner-pitch/partners/grab-thailand.json"
PARTNER_DST = ROOT / "data-clean/partners/grab-thailand.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean/CLUSTERS.json"
REPORT_PATH = ROOT / "grok-routing-output/grab-thailand-depth-seal-report.json"
TAG = "grab_thailand_depth"

CITY_SEEDS = {
    "hua-hin-thailand": ("Hua Hin", "Thailand", "SEA", [99.9577, 12.5707]),
    "cha-am-thailand": ("Cha-Am", "Thailand", "SEA", [99.955, 12.795]),
    "koh-samet-thailand": ("Koh Samet", "Thailand", "SEA", [101.45, 12.565]),
}

# Pier-exact endpoints (city_id keys preserved for partner bind)
ROUTE_ENDPOINTS: dict[tuple[str, str], tuple[list[float], list[float]]] = {
    ("bangkok-thailand", "pattaya-thailand"): (
        [100.5118, 13.7276],  # ICONSIAM / river gateway
        [100.8674, 12.9233],  # Bali Hai, Pattaya
    ),
    ("pattaya-thailand", "koh-samet-thailand"): (
        [100.8807, 12.8304],  # Ocean Marina
        [101.454, 12.5715],   # Na Dan, Koh Samet
    ),
    ("koh-samet-thailand", "koh-samet-thailand"): (
        [101.4407, 12.6248],  # Ban Phe mainland
        [101.454, 12.5715],   # Na Dan island
    ),
    ("hua-hin-thailand", "pattaya-thailand"): (
        [99.959, 12.5712],    # Hua Hin pier
        [100.8674, 12.9233],  # Pattaya
    ),
    ("hua-hin-thailand", "cha-am-thailand"): (
        [99.959, 12.5712],
        [99.955, 12.795],
    ),
}

# (from_city, to_city, waypoints[(lng,lat)], marquee?)
DEPTH_ROUTES = [
    ("bangkok-thailand", "pattaya-thailand", [
        (100.62, 13.15), (100.78, 13.02), (100.86, 12.96),
    ], False),
    ("pattaya-thailand", "koh-samet-thailand", [
        (100.98, 12.72), (101.18, 12.62), (101.35, 12.58),
    ], False),
    ("koh-samet-thailand", "koh-samet-thailand", [], False),
    ("hua-hin-thailand", "pattaya-thailand", [
        (100.15, 12.05), (100.45, 11.92), (100.72, 12.35),
    ], True),
    ("hua-hin-thailand", "cha-am-thailand", [(99.956, 12.68)], False),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def city_coord(fbt: dict, city_id: str) -> list[float] | None:
    for t in ("city", "priority_city"):
        for f in fbt.get(t, []):
            p = f.get("properties", {})
            if p.get("id") == city_id:
                return f["geometry"]["coordinates"]
    seed = CITY_SEEDS.get(city_id)
    return seed[3] if seed else None


def make_city(city_id: str, coords: list[float]) -> dict:
    name, country, region, _ = CITY_SEEDS.get(
        city_id, (city_id.replace("-thailand", "").title(), "Thailand", "SEA", coords)
    )
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": coords},
        "properties": {
            "id": city_id,
            "type": "city",
            "name": name,
            "shortName": name,
            "fullName": name,
            "country": country,
            "region": region,
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "grab_thailand_depth_seal_2026-06-23",
            "confidence": "medium",
            "status": "operational",
            "tier_sort_key": 2,
            f"_{TAG}_applied_at": now_iso(),
        },
    }


def make_poi(city_id: str, bp: dict) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [bp["lng"], bp["lat"]]},
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "name": bp["name"],
            "shortName": bp["name"].split("(")[0].strip(),
            "parent_city_id": city_id,
            "bp_type": bp.get("type", "pier"),
            "coords_resolved": True,
            "confidence": bp.get("confidence", "med"),
            "precision": bp.get("precision", "curated_seed"),
            "_gazetteer_source": f"grab_thailand_depth:{city_id}",
            f"_{TAG}_applied_at": now_iso(),
            "status": "operational",
        },
    }


def route_id_of(feat: dict) -> str:
    return (feat.get("properties") or feat).get("id", "")


def build_path(a: list[float], b: list[float], wps: list[tuple[float, float]] | None) -> list:
    pts = [a]
    if wps:
        pts.extend([list(w) for w in wps])
    pts.append(b)
    coords = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 18)
        coords.extend(seg if not coords else seg[1:])
    return coords


def bind_partner_journeys(partner: dict, route_by_pair: dict) -> dict:
    stats = {"bound": 0, "roadmap": 0, "still_pending": 0}
    for market in partner.get("markets", []):
        for j in market.get("journeys_unlocked", []):
            st = j.get("_link_status", "")
            if st == "roadmap-quanta-lr":
                j["route_id"] = None
                j["render"] = "amber-dashed"
                stats["roadmap"] += 1
                continue
            if st != "pending-seal-thailand-depth":
                continue
            fc, tc = j.get("from_node_id"), j.get("to_node_id")
            rid = route_by_pair.get((fc, tc)) or route_by_pair.get((tc, fc))
            if rid:
                j["route_id"] = rid
                j["_link_status"] = "linked-grok-scoped"
                j["_link_source"] = f"grok/{TAG}"
                j["economics_status"] = "pending-seal"
                stats["bound"] += 1
            else:
                stats["still_pending"] += 1
    return stats


def ensure_thailand_cluster(clusters: dict, city_ids: list[str]) -> None:
    for c in clusters.get("clusters", []):
        if c.get("cluster_id") == "thailand":
            members = set(c.get("member_city_ids") or c.get("city_ids") or [])
            members.update(city_ids)
            c["member_city_ids"] = sorted(members)
            if "city_ids" in c:
                c["city_ids"] = sorted(members)
            return


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        ap.error("pass --apply or --dry-run")

    fbt = load_json(FBT_PATH)
    routes = route_features(load_json(ROUTES_PATH))
    partner = load_json(PARTNER_SRC)
    clusters = load_json(CLUSTERS_PATH)
    mask = load_land_mask()

    report = {
        "at": now_iso(),
        "lane": f"grok/{TAG}",
        "apply": args.apply,
        "cities_minted": [],
        "bps_sealed": [],
        "routes_built": [],
        "routes_culled": [],
    }

    city_ids = list(CITY_SEEDS)
    existing_city = {f["properties"]["id"] for f in fbt.get("city", [])}
    for cid, (_, _, _, coords) in CITY_SEEDS.items():
        if cid not in existing_city:
            fbt.setdefault("city", []).append(make_city(cid, coords))
            report["cities_minted"].append(cid)

    poi_by_id = {p["properties"]["id"]: p for p in fbt.get("poi", [])}
    for bp_file in sorted(BP_DIR.glob("*.json")):
        data = json.loads(bp_file.read_text())
        cid = data["city_id"]
        for bp in data.get("boarding_points", []):
            bid = bp.get("id")
            if not bid:
                continue
            feat = make_poi(cid, bp)
            poi_by_id[bid] = feat
            report["bps_sealed"].append(bid)
    fbt["poi"] = list(poi_by_id.values())

    route_by_pair: dict[tuple[str, str], str] = {}
    existing_ids = {route_id_of(r) for r in routes}

    for fc, tc, wps, marquee in DEPTH_ROUTES:
        ep = ROUTE_ENDPOINTS.get((fc, tc))
        ac = ep[0] if ep else city_coord(fbt, fc)
        bc = ep[1] if ep else city_coord(fbt, tc)
        if not ac or not bc:
            report["routes_culled"].append({"from": fc, "to": tc, "reason": "missing_city_coord"})
            continue
        coords = build_coastal_path(tuple(ac), tuple(bc), mask, wps)
        dist = hav_nm(ac, bc)
        land_km = interior_land_km(coords, mask)
        geom_status = "sealed"
        if land_km > 2.0:
            geom_status = "pending_channel_authorship"
            report.setdefault("routes_borderline", []).append(
                {"from": fc, "to": tc, "land_km": round(land_km, 2), "note": "bound for proposal; G1 channel solver backlog"}
            )
        rid = mint_route_id(fc, tc, TAG)
        if rid in existing_ids:
            rid = mint_route_id(fc, tc, f"{TAG}|{len(routes)}")
        feat = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "id": rid,
                "platform": "Pioneer II",
                "distance_nm": round(dist, 1),
                "edge_class": "inter-city" if fc != tc else "intra-city",
                "from": fc,
                "to": tc,
                "from_city": fc,
                "to_city": tc,
                "from_city_id": fc,
                "to_city_id": tc,
                "label": f"{fc} → {tc}" if fc != tc else f"{fc}: gateway shuttle",
                "trip_purpose": "tourism" if marquee else "mixed",
                "traffic_weight": 0.72 if marquee else 0.55,
                "interior_land_km": round(land_km, 4),
                f"_{TAG}_applied_at": now_iso(),
                "_geometry_status": geom_status,
            },
        }
        routes.append(feat)
        existing_ids.add(rid)
        route_by_pair[(fc, tc)] = rid
        report["routes_built"].append(
            {"from": fc, "to": tc, "route_id": rid, "distance_nm": round(dist, 1), "land_km": round(land_km, 3)}
        )

    bind_stats = bind_partner_journeys(partner, route_by_pair)
    report["journey_bind"] = bind_stats

    nt = partner.setdefault("network_thesis", {})
    if nt.get("stats"):
        for s in nt["stats"]:
            if s.get("label") == "Clusters":
                s["value"] = "5"
                s["sub"] = "Gulf, Andaman, Bangkok river, Eastern Seaboard, Royal Coast"
            if s.get("label") == "Sealed corridors":
                bound = sum(
                    1 for m in partner.get("markets", [])
                    for j in m.get("journeys_unlocked", [])
                    if j.get("route_id") and j.get("_link_status") == "linked-grok-scoped"
                )
                s["value"] = str(bound)
                s["sub"] = "Samui + Andaman + Bangkok + upper-Gulf depth (Grok seal 2026-06-23)"

    ensure_thailand_cluster(clusters, city_ids)

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        save_json(FBT_PATH, fbt)
        save_json(CLUSTERS_PATH, clusters)
        save_json(PARTNER_SRC, partner)
        shutil.copy2(PARTNER_SRC, PARTNER_DST)
        for brief in (ROOT / "data-clean/city_briefs").glob("*-thailand.json"):
            pass  # briefs already on main from PR88
    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))
    ok = bind_stats["still_pending"] == 0 and len(report["routes_built"]) >= 5
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())