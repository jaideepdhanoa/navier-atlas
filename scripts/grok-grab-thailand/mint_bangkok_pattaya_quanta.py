#!/usr/bin/env python3
"""Restore Bangkok ↔ Pattaya as a Quanta-LR cross-Gulf gateway corridor."""
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
REPORT_PATH = ROOT / "grok-routing-output/grab-thailand-bkk-pattaya-quanta-report.json"

TAG = "grab_thailand_bkk_pattaya_quanta"
CANONICAL_ID = "rn-dcbcbe8bfb4f"

ENDPOINTS = {
    "bangkok-thailand": [100.5118, 13.7276],  # ICONSIAM / river gateway
    "pattaya-thailand": [100.8674, 12.9233],   # Bali Hai
}

# Chao Phraya mouth → upper Gulf → Pattaya (cross-Gulf Quanta-LR lane)
WAYPOINTS = [
    (100.62, 13.15),
    (100.78, 13.02),
    (100.86, 12.96),
]

JOURNEY_SPEC = {
    "from": "Bangkok (Gulf mouth)",
    "to": "Pattaya (Bali Hai Pier)",
    "today": "A 2hr-plus drive on the congested Bangkok-Pattaya highway.",
    "with_navier": "A premium ~75 nm Quanta-LR foiling gateway hop across the upper Gulf — booked in-app.",
    "distance_nm": 75.0,
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
            "platform": "Quanta-LR",
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
            "traffic_weight": 0.72,
            "interior_land_km": round(land_km, 4),
            f"_{TAG}_applied_at": now_iso(),
            "_geometry_status": "pending_channel_authorship",
            "_marquee": True,
            "_grab_thailand_depth_route_fix": "bangkok-pattaya-quanta-lr",
        },
    }
    for i, r in enumerate(routes):
        if props(r).get("id") == CANONICAL_ID:
            routes[i] = feat
            return
    routes.append(feat)


def bind_journey(j: dict, dist_nm: float) -> bool:
    fc, tc = j.get("from_node_id"), j.get("to_node_id")
    if {fc, tc} != {"bangkok-thailand", "pattaya-thailand"}:
        return False
    j.update(
        {
            **JOURNEY_SPEC,
            "distance_nm": round(dist_nm, 1),
            "platform": "Quanta-LR",
            "render": "amber-dashed",
            "range_status": "now",
            "route_id": CANONICAL_ID,
            "_link_status": "linked-grok-scoped",
            "_link_source": f"grok/{TAG}",
            "_link_kind": "corridor-label",
            "economics_status": j.get("economics_status") or "bound",
        }
    )
    return True


def bind_partner(partner: dict, dist_nm: float) -> dict:
    stats = {"journeys_bound": 0, "featured_bound": 0}
    for market in partner.get("markets", []):
        for j in market.get("journeys_unlocked", []):
            if bind_journey(j, dist_nm):
                stats["journeys_bound"] += 1
        for phase in market.get("phases", []):
            for fr in phase.get("featured_routes", []) or []:
                fc, tc = fr.get("from_node_id"), fr.get("to_node_id")
                if {fc, tc} == {"bangkok-thailand", "pattaya-thailand"}:
                    fr["route_id"] = CANONICAL_ID
                    fr["platform"] = "Quanta-LR"
                    fr["distance_nm"] = round(dist_nm, 1)
                    fr["render"] = "amber-dashed"
                    fr["_link_status"] = "linked-grok-scoped"
                    fr["_link_source"] = f"grok/{TAG}"
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
                c["vessel"] = "Quanta-LR"
                c["distance_nm"] = round(dist_nm, 1)
                c["platform"] = "Quanta-LR"
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
        "platform": "Quanta-LR",
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
        # keep pitch + data-clean grab in sync
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
    ok = props(feat).get("platform") == "Quanta-LR" and land_km <= 0.05
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())