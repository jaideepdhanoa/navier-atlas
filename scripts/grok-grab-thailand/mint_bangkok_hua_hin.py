#!/usr/bin/env python3
"""Mint marquee Bangkok ↔ Hua Hin corridor — Chao Phraya river then west-coast fold."""
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

from bucketB_shared import hav_nm, interior_land_km, load_land_mask  # noqa: E402
from bolt_yango_routing_shared import (  # noqa: E402
    build_coastal_path,
    load_json,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)

ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
PARTNER_SRC = ROOT / "partner-pitch/partners/grab-thailand.json"
PARTNER_DST = ROOT / "data-clean/partners/grab-thailand.json"
REPORT_PATH = ROOT / "grok-routing-output/grab-thailand-bkk-hua-hin-mint-report.json"

TAG = "grab_thailand_bkk_hua_hin"
CANONICAL_ID = mint_route_id("bangkok-thailand", "hua-hin-thailand", TAG)

# ICONSIAM river gateway → Hua Hin pier
ENDPOINTS = {
    "bangkok-thailand": [100.5118, 13.7276],
    "hua-hin-thailand": [99.959, 12.5712],
}

# River south through Chao Phraya, Gulf mouth exit, then fold along western coast to Hua Hin
WAYPOINTS = [
    (100.52, 13.62),
    (100.54, 13.48),
    (100.57, 13.32),
    (100.58, 13.12),
    (100.52, 12.95),
    (100.28, 12.82),
    (100.05, 12.68),
    (99.97, 12.60),
]

JOURNEY_BIND = {
    ("bangkok-thailand", "hua-hin-thailand"): {
        "from": "Bangkok (ICONSIAM / Chao Phraya)",
        "to": "Hua Hin (pier)",
        "today": "A 2.5–3hr drive on congested Phetkasem Road to the royal coast — no premium water option.",
        "with_navier": "A premium ~88 nm foiling run down the Chao Phraya and along the upper Gulf — river gateway to the royal coast, booked in Grab.",
        "distance_nm": 88.0,
        "_marquee": True,
    },
    ("hua-hin-thailand", "bangkok-thailand"): {
        "from": "Hua Hin (pier)",
        "to": "Bangkok (ICONSIAM / Chao Phraya)",
        "today": "A 2.5–3hr drive north to Bangkok — no premium water return.",
        "with_navier": "A premium foiling return up the Gulf and into the Chao Phraya — the royal-coast gateway to Bangkok, booked in Grab.",
        "distance_nm": 88.0,
        "_marquee": True,
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def path_length_nm(coords: list) -> float:
    return sum(hav_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1))


def upsert_route(routes: list, rid: str, coords: list, dist_nm: float, land_km: float) -> None:
    feat = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": "Pioneer II",
            "distance_nm": round(dist_nm, 1),
            "edge_class": "inter-city",
            "from": "bangkok-thailand",
            "to": "hua-hin-thailand",
            "from_city": "bangkok-thailand",
            "to_city": "hua-hin-thailand",
            "from_city_id": "bangkok-thailand",
            "to_city_id": "hua-hin-thailand",
            "label": "bangkok-thailand → hua-hin-thailand",
            "trip_purpose": "tourism",
            "traffic_weight": 0.78,
            "interior_land_km": round(land_km, 4),
            f"_{TAG}_applied_at": now_iso(),
            "_geometry_status": "pending_channel_authorship",
            "_marquee": True,
        },
    }
    for i, r in enumerate(routes):
        p = props(r)
        if p.get("id") == rid:
            routes[i] = feat
            return
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if {fc, tc} == {"bangkok-thailand", "hua-hin-thailand"} and rid != p.get("id"):
            routes[i] = feat
            return
    routes.append(feat)


def journey_exists(journeys: list, fc: str, tc: str) -> bool:
    return any(j.get("from_node_id") == fc and j.get("to_node_id") == tc for j in journeys)


def append_journey(journeys: list, fc: str, tc: str, rid: str, spec: dict) -> bool:
    if journey_exists(journeys, fc, tc):
        return False
    journeys.append(
        {
            **spec,
            "platform": "Pioneer II",
            "render": "solid",
            "range_status": "now",
            "from_node_id": fc,
            "to_node_id": tc,
            "route_id": rid,
            "_link_status": "linked-grok-scoped",
            "_link_source": f"grok/{TAG}",
            "_link_kind": "corridor-label",
            "economics_status": "pending-seal",
        }
    )
    return True


def bind_partner(partner: dict, rid: str) -> dict:
    stats = {"journeys_added": 0, "journeys_bound": 0, "featured_bound": 0}
    market_targets = {
        "bangkok": ("bangkok-thailand", "hua-hin-thailand"),
        "royal_coast": ("hua-hin-thailand", "bangkok-thailand"),
    }
    for market in partner.get("markets", []):
        mid = market.get("id")
        pair = market_targets.get(mid)
        journeys = market.setdefault("journeys_unlocked", [])
        if pair:
            fc, tc = pair
            spec = JOURNEY_BIND[(fc, tc)]
            if append_journey(journeys, fc, tc, rid, spec):
                stats["journeys_added"] += 1
        for j in journeys:
            fc, tc = j.get("from_node_id"), j.get("to_node_id")
            if {fc, tc} == {"bangkok-thailand", "hua-hin-thailand"}:
                if j.get("route_id") != rid:
                    j["route_id"] = rid
                    j["_link_status"] = "linked-grok-scoped"
                    j["_link_source"] = f"grok/{TAG}"
                    j["economics_status"] = "pending-seal"
                    stats["journeys_bound"] += 1
        for phase in market.get("phases", []):
            for fr in phase.get("featured_routes", []) or []:
                fc, tc = fr.get("from_node_id"), fr.get("to_node_id")
                if {fc, tc} == {"bangkok-thailand", "hua-hin-thailand"}:
                    fr["route_id"] = rid
                    fr["_link_status"] = "linked-grok-scoped"
                    fr["_link_source"] = f"grok/{TAG}"
                    stats["featured_bound"] += 1

    if "bangkok" in {m.get("id") for m in partner.get("markets", [])}:
        note = partner["markets"][[m["id"] for m in partner["markets"]].index("bangkok")].get(
            "corridors_note", ""
        )
        if "Hua Hin" not in note:
            partner["markets"][[m["id"] for m in partner["markets"]].index("bangkok")][
                "corridors_note"
            ] = (
                note.rstrip()
                + " Bangkok↔Hua Hin marquee (~88 nm) sealed: Chao Phraya river gateway then west-coast fold to the royal coast."
            )

    nt = partner.setdefault("network_thesis", {})
    if nt.get("stats"):
        for s in nt["stats"]:
            if s.get("label") == "Sealed corridors":
                bound = sum(
                    1
                    for m in partner.get("markets", [])
                    for j in m.get("journeys_unlocked", [])
                    if j.get("route_id") and j.get("_link_status", "").startswith("linked")
                )
                s["value"] = str(bound)
                s["sub"] = "Samui + Andaman + Bangkok river + upper-Gulf depth + BKK↔Hua Hin marquee"
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        ap.error("pass --apply or --dry-run")

    a = ENDPOINTS["bangkok-thailand"]
    b = ENDPOINTS["hua-hin-thailand"]
    mask = load_land_mask()
    coords = build_coastal_path(tuple(a), tuple(b), mask, WAYPOINTS)
    land_km = interior_land_km(coords, mask)
    path_nm = path_length_nm(coords)

    routes = route_features(load_json(ROUTES_PATH))
    partner = load_json(PARTNER_SRC)

    report = {
        "at": now_iso(),
        "lane": f"grok/{TAG}",
        "apply": args.apply,
        "canonical_id": CANONICAL_ID,
        "from_city_id": "bangkok-thailand",
        "to_city_id": "hua-hin-thailand",
        "straight_nm": round(hav_nm(a, b), 1),
        "path_nm": round(path_nm, 1),
        "land_km": round(land_km, 3),
        "waypoints": WAYPOINTS,
        "geometry_status": "pending_channel_authorship",
    }

    upsert_route(routes, CANONICAL_ID, coords, path_nm, land_km)
    report["bind"] = bind_partner(partner, CANONICAL_ID)

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        save_json(PARTNER_SRC, partner)
        shutil.copy2(PARTNER_SRC, PARTNER_DST)

    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))

    p = props(routes[-1])
    for r in routes:
        pr = props(r)
        if pr.get("id") == CANONICAL_ID:
            p = pr
            break
    ok = (
        p.get("from_city_id") == "bangkok-thailand"
        and p.get("to_city_id") == "hua-hin-thailand"
        and report["bind"]["journeys_added"] + report["bind"]["journeys_bound"] >= 1
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())