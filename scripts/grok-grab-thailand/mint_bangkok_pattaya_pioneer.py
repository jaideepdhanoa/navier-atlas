#!/usr/bin/env python3
"""Restore Bangkok ↔ Pattaya as Pioneer II with cross-market map visibility."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bucketB_shared import hav_nm, interior_land_km, load_land_mask  # noqa: E402
from bolt_yango_routing_shared import load_json, route_features, save_json, save_routes  # noqa: E402
from channel_solver import get_land_checker, solve_hand  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402

ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
PARTNERS = [
    ROOT / "partner-pitch/partners/grab-thailand.json",
    ROOT / "data-clean/partners/grab-thailand.json",
    ROOT / "partner-pitch/partners/line-man-wongnai.json",
    ROOT / "data-clean/partners/line-man-wongnai.json",
]
CORRIDORS = [
    ROOT / "finance/recal/corridors-grab-thailand.json",
    ROOT / "finance/recal/corridors-line-man-wongnai.json",
]
REPORT_PATH = ROOT / "grok-routing-output/grab-thailand-bkk-pattaya-pioneer-report.json"

TAG = "grab_thailand_bkk_pattaya_pioneer"
CANONICAL_ID = "rn-dcbcbe8bfb4f"
GATEWAY_CITIES = ("bangkok-thailand", "pattaya-thailand")

ENDPOINTS = {
    "bangkok-thailand": [100.5118, 13.7276],
    "pattaya-thailand": [100.8674, 12.9233],
}

WAYPOINTS = [
    (100.62, 13.15),
    (100.78, 13.02),
    (100.86, 12.96),
]

JOURNEY_SPEC = {
    "from": "Bangkok (Gulf mouth)",
    "to": "Pattaya (Bali Hai Pier)",
    "today": "A 2hr-plus drive on the congested Bangkok-Pattaya highway.",
    "with_navier": "A premium ~46 nm foiling gateway hop across the upper Gulf — booked in-app.",
    "platform": "Pioneer II",
    "render": "solid",
    "range_status": "now",
    "_marquee": True,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def path_length_nm(coords: list) -> float:
    return sum(hav_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1))


def build_geometry() -> tuple[list, float, float, dict]:
    a, b = ENDPOINTS["bangkok-thailand"], ENDPOINTS["pattaya-thailand"]
    lc = get_land_checker()
    wps = [[lon, lat] for lon, lat in WAYPOINTS]
    solved = solve_hand(lc, a, b, wps)
    if solved and solved.get("qa_pass"):
        coords = solved["geometry"]
        ev = evaluate_route(coords)
        return coords, path_length_nm(coords), ev["interior_land_km"], {"method": solved.get("method", "hand")}

    mask = load_land_mask()
    from bolt_yango_routing_shared import build_coastal_path  # noqa: WPS433

    coords = build_coastal_path(tuple(a), tuple(b), mask, WAYPOINTS)
    land_km = interior_land_km(coords, mask)
    ev = evaluate_route(coords)
    return coords, path_length_nm(coords), land_km, {"method": "coastal", "qa_pass": ev["qa_pass"]}


def upsert_route(routes: list, coords: list, dist_nm: float, land_km: float) -> None:
    feat = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": CANONICAL_ID,
            "platform": "Pioneer II",
            "distance_nm": round(dist_nm, 1),
            "edge_class": "inter-city",
            "from": "bangkok-thailand",
            "to": "pattaya-thailand",
            "from_city": "bangkok-thailand",
            "to_city": "pattaya-thailand",
            "from_city_id": "bangkok-thailand",
            "to_city_id": "pattaya-thailand",
            "label": "bangkok-thailand → pattaya-thailand",
            "trip_purpose": "mixed",
            "traffic_weight": 0.82,
            "interior_land_km": round(land_km, 4),
            f"_{TAG}_applied_at": now_iso(),
            "_geometry_status": "channel_authored",
            "_marquee": True,
            "_grab_thailand_depth_route_fix": "bangkok-pattaya-pioneer-ii",
        },
    }
    for i, r in enumerate(routes):
        if props(r).get("id") == CANONICAL_ID:
            routes[i] = feat
            return
    routes.append(feat)


def bind_journey(j: dict, dist_nm: float) -> bool:
    fc, tc = j.get("from_node_id"), j.get("to_node_id")
    if {fc, tc} != set(GATEWAY_CITIES):
        return False
    j.update(
        {
            **JOURNEY_SPEC,
            "distance_nm": round(dist_nm, 1),
            "route_id": CANONICAL_ID,
            "_link_status": "linked-grok-scoped",
            "_link_source": f"grok/{TAG}",
            "_link_kind": "corridor-label",
            "economics_status": j.get("economics_status") or "bound",
            "_economics_source": "economics_by_route_id.json",
        }
    )
    return True


def bind_featured(fr: dict, dist_nm: float) -> bool:
    fc, tc = fr.get("from_node_id"), fr.get("to_node_id")
    if {fc, tc} != set(GATEWAY_CITIES):
        return False
    fr.update(
        {
            "route_id": CANONICAL_ID,
            "platform": "Pioneer II",
            "distance_nm": round(dist_nm, 1),
            "render": "solid",
            "_link_status": "linked-grok-scoped",
            "_link_source": f"grok/{TAG}",
            "_link_kind": "corridor-label",
        }
    )
    fr.pop("display", None)
    return True


def _normalize_phase_cities(cities: list) -> list:
    resolved = set()
    for c in cities or []:
        cl = str(c).lower()
        if cl in ("bangkok", "bangkok-thailand"):
            resolved.add("bangkok-thailand")
        elif cl in ("pattaya", "pattaya-thailand"):
            resolved.add("pattaya-thailand")
        elif cl in ("koh larn", "koh-larn-thailand"):
            resolved.add("koh-larn-thailand")
        elif cl in ("koh samet", "koh-samet-thailand"):
            resolved.add("koh-samet-thailand")
        elif cl in ("koh chang", "koh-chang-thailand"):
            resolved.add("koh-chang-thailand")
        else:
            resolved.add(c)
    return sorted(resolved)


def ensure_market_scope(partner: dict) -> dict:
    """Both gateway cities must sit in each market's rollout scope (build-site marketCities)."""
    stats = {"bangkok_scope": False, "eastern_scope": False, "promote": False}
    md = partner.setdefault("map_display", {})
    promote = set(md.get("promote_route_ids") or [])
    if CANONICAL_ID not in promote:
        promote.add(CANONICAL_ID)
        md["promote_route_ids"] = sorted(promote)
        stats["promote"] = True

    for market in partner.get("markets", []):
        mid = market.get("id") or market.get("slug")
        if mid == "bangkok":
            anchors = list(market.get("anchor_cities") or [])
            if "pattaya-thailand" not in anchors:
                anchors.append("pattaya-thailand")
                market["anchor_cities"] = anchors
                stats["bangkok_scope"] = True
            for phase in market.get("phases", []):
                cities = _normalize_phase_cities(phase.get("cities"))
                if phase.get("n") in (2, 3) and "pattaya-thailand" not in cities:
                    cities.append("pattaya-thailand")
                    stats["bangkok_scope"] = True
                phase["cities"] = sorted(set(cities))
                # Replace aspirational text-only placeholder with the built gateway leg.
                for fr in phase.get("featured_routes", []) or []:
                    if fr.get("_link_status") == "aspirational-no-built-route":
                        if "pattaya" in str(fr.get("label", "")).lower():
                            fr.clear()
                            fr.update(
                                {
                                    "label": "Bangkok (Gulf mouth) ↔ Pattaya (Bali Hai Pier)",
                                    "from_node_id": "bangkok-thailand",
                                    "to_node_id": "pattaya-thailand",
                                    "route_id": CANONICAL_ID,
                                    "platform": "Pioneer II",
                                    "render": "solid",
                                    "_link_status": "linked-grok-scoped",
                                    "_link_source": f"grok/{TAG}",
                                    "_link_kind": "corridor-label",
                                    "economics_status": "bound",
                                }
                            )
                            stats["bangkok_scope"] = True
        if mid == "eastern_seaboard":
            anchors = list(market.get("anchor_cities") or [])
            if "bangkok-thailand" not in anchors:
                anchors.insert(0, "bangkok-thailand")
                market["anchor_cities"] = anchors
                stats["eastern_scope"] = True
            for phase in market.get("phases", []):
                norm = _normalize_phase_cities(phase.get("cities"))
                if "bangkok-thailand" not in norm:
                    norm.append("bangkok-thailand")
                    stats["eastern_scope"] = True
                phase["cities"] = norm
    return stats


def bind_partner(partner: dict, dist_nm: float) -> dict:
    stats = {"journeys_bound": 0, "featured_bound": 0, **ensure_market_scope(partner)}
    for market in partner.get("markets", []):
        for j in market.get("journeys_unlocked", []):
            if bind_journey(j, dist_nm):
                stats["journeys_bound"] += 1
        for phase in market.get("phases", []):
            for fr in phase.get("featured_routes", []) or []:
                if bind_featured(fr, dist_nm):
                    stats["featured_bound"] += 1
    return stats


def bind_corridors(path: Path, dist_nm: float) -> bool:
    if not path.is_file():
        return False
    doc = json.loads(path.read_text())
    changed = False
    for market in (doc.get("markets") or {}).values():
        for c in market.get("corridors", []):
            if c.get("route_id") == CANONICAL_ID:
                c["vessel"] = "N30 Pioneer II"
                c["distance_nm"] = round(dist_nm, 1)
                c.pop("platform", None)
                changed = True
    if changed:
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    coords, dist_nm, land_km, geom_meta = build_geometry()
    routes = route_features(load_json(ROUTES_PATH))

    report = {
        "at": now_iso(),
        "lane": f"grok/{TAG}",
        "apply": args.apply,
        "canonical_id": CANONICAL_ID,
        "platform": "Pioneer II",
        "path_nm": round(dist_nm, 1),
        "land_km": round(land_km, 4),
        "geometry": geom_meta,
        "partner_binds": {},
        "corridors_updated": [],
    }

    upsert_route(routes, coords, dist_nm, land_km)

    for ppath in PARTNERS:
        if not ppath.is_file():
            continue
        partner = load_json(ppath)
        report["partner_binds"][str(ppath.relative_to(ROOT))] = bind_partner(partner, dist_nm)
        if args.apply:
            save_json(ppath, partner)

    for cpath in CORRIDORS:
        if bind_corridors(cpath, dist_nm):
            report["corridors_updated"].append(str(cpath.relative_to(ROOT)))

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        src = ROOT / "partner-pitch/partners/grab-thailand.json"
        dst = ROOT / "data-clean/partners/grab-thailand.json"
        if src.is_file() and dst.parent.exists():
            shutil.copy2(src, dst)
        src2 = ROOT / "partner-pitch/partners/line-man-wongnai.json"
        dst2 = ROOT / "data-clean/partners/line-man-wongnai.json"
        if src2.is_file() and dst2.parent.exists():
            shutil.copy2(src2, dst2)

    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))

    feat = next(r for r in routes if props(r).get("id") == CANONICAL_ID)
    ok = props(feat).get("platform") == "Pioneer II" and land_km <= 0.05
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())