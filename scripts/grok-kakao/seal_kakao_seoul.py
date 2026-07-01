#!/usr/bin/env python3
"""Grok seal — Kakao Mobility Seoul–Incheon seed node + Han River corridors."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    save_json,
    save_routes,
)
from channel_solver import HAND_WAYPOINTS  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402

PARTNER = "kakao-mobility"
MARKET = "seoul-han-river"
CITY = "seoul-incheon-korea"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
HAND_PATH = ROOT / "data-clean/kakao_hand_waypoints_seoul.json"
PITCH = ROOT / "partner-pitch/partners" / f"{PARTNER}.json"
DC = ROOT / "data-clean/partners" / f"{PARTNER}.json"
REPORT = ROOT / "handoff/partner-map-model/KAKAO-SEOUL-SEAL-RECEIPT.json"

SEOUL_BPS = [
    ("bp-kakao-gimpo-ara", "Gimpo Ara Marina", [126.817, 37.567]),
    ("bp-kakao-yeouido", "Yeouido Hangang Park Pier", [126.924, 37.521]),
    ("bp-kakao-jamsil", "Jamsil Ttukseom Riverside Pier", [127.082, 37.513]),
    ("bp-kakao-ttukseom", "Ttukseom Hangang Park Pier", [127.098, 37.529]),
    ("bp-kakao-seoul-forest", "Seoul Forest Riverside Pier", [127.044, 37.544]),
    ("bp-kakao-incheon-terminal", "Incheon Coastal Passenger Terminal", [126.597, 37.456]),
    ("bp-kakao-muuido", "Muuido Island Ferry Berth", [126.378, 37.374]),
    ("bp-kakao-yeongjong", "Yeongjong Island Marina", [126.492, 37.492]),
]

ROUTES_SPEC = [
    ("commute_gimpo_jamsil", "bp-kakao-gimpo-ara", "bp-kakao-jamsil", "Gimpo/Yeouido ↔ Jamsil commute"),
    ("commute_yeouido_ttukseom", "bp-kakao-yeouido", "bp-kakao-ttukseom", "Yeouido ↔ Ttukseom leisure + commute"),
    ("incheon_muuido", "bp-kakao-incheon-terminal", "bp-kakao-muuido", "Incheon ↔ Muuido day-trip"),
    ("river_incheon_connector", "bp-kakao-yeouido", "bp-kakao-incheon-terminal", "Han River ↔ Incheon Bay connector"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def load_hand_catalog() -> None:
    if not HAND_PATH.is_file():
        return
    catalog = load_json(HAND_PATH)
    for key, wps in catalog.get("waypoints", {}).items():
        parts = key.split("|", 1)
        if len(parts) == 2:
            HAND_WAYPOINTS[(parts[0], parts[1])] = wps


def route_path(a: tuple[float, float], b: tuple[float, float], fr: str, to: str, mask) -> list:
    manual = HAND_WAYPOINTS.get((fr, to)) or HAND_WAYPOINTS.get((to, fr))
    if manual:
        pts = [a] + [tuple(w) for w in manual] + [b]
        if (fr, to) not in HAND_WAYPOINTS and (to, fr) in HAND_WAYPOINTS:
            pts = [a] + [tuple(w) for w in reversed(manual)] + [b]
        return [[p[0], p[1]] for p in pts]
    return build_coastal_path(a, b, mask)


def ensure_bps(fbt: dict) -> None:
    pois = fbt.setdefault("poi", [])
    existing = {props(p).get("id") for p in pois}
    for bp_id, name, coords in SEOUL_BPS:
        if bp_id in existing:
            for p in pois:
                if props(p).get("id") == bp_id:
                    props(p)["parent_city_id"] = CITY
            continue
        pois.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": coords},
                "properties": {
                    "id": bp_id,
                    "type": "poi",
                    "name": name,
                    "shortName": name[:32],
                    "fullName": name,
                    "parent_city_id": CITY,
                    "bp_type": "ferry_terminal",
                    "status": "operational",
                    "confidence": "high",
                    "_kakao_seoul_sealed": now_iso(),
                },
            }
        )


def patch_city(fbt: dict) -> None:
    for f in fbt.get("city", []):
        p = props(f)
        if p.get("id") == CITY:
            p.pop("_seed_node", None)
            p.pop("_link_status", None)
            p["name"] = "Seoul — Han River + Incheon Bay"
            p["fullName"] = "Seoul — Han River + Incheon Bay"
            p["coords_source"] = "grok/kakao_seoul_seal_2026-07-01"
            p["coords_resolved"] = True
            f["geometry"]["coordinates"] = [126.924, 37.521]
            p["_kakao_seoul_sealed"] = now_iso()


def seal_routes(fbt: dict, routes: list) -> dict:
    load_hand_catalog()
    mask = load_land_mask()
    bp_idx = build_bp_index(fbt)
    cities = {CITY: "Seoul — Han River + Incheon Bay"}
    rids: dict[str, str] = {}
    minted = []
    failed = []

    for key, fr, to, _label in ROUTES_SPEC:
        if fr not in bp_idx or to not in bp_idx:
            failed.append({"key": key, "reason": "bp_missing"})
            continue
        tag = f"kakao_seoul_{key}"
        rid = mint_route_id(fr, to, tag)
        a = tuple(bp_idx[fr]["coords"])
        b = tuple(bp_idx[to]["coords"])
        coords = route_path(a, b, fr, to, mask)
        land_km = interior_land_km(coords, mask)
        qa = evaluate_route(coords)
        if not qa.get("qa_pass"):
            failed.append({"key": key, "land_km": land_km, "qa": qa})
            continue
        feat = make_route_feature(
            fr, to, bp_idx[fr]["name"], bp_idx[to]["name"], CITY, CITY, coords, cities,
            source="kakao_seoul_seal", land_km=land_km,
        )
        p = props(feat)
        p["id"] = rid
        p["platform"] = "Pioneer II"
        p["_kakao_seoul_sealed"] = now_iso()
        routes.append(feat)
        rids[key] = rid
        minted.append(rid)

    return {"minted": minted, "rids": rids, "failed": failed}


JOURNEY_BIND = {
    ("Gimpo / Yeouido", "Jamsil / Ttukseom"): (
        "commute_gimpo_jamsil",
        "bp-kakao-gimpo-ara",
        "bp-kakao-jamsil",
    ),
    ("Yeouido", "Seoul Forest / Ttukseom"): (
        "commute_yeouido_ttukseom",
        "bp-kakao-yeouido",
        "bp-kakao-ttukseom",
    ),
    ("Incheon", "Muuido / Yeongjong (West Sea islands)"): (
        "incheon_muuido",
        "bp-kakao-incheon-terminal",
        "bp-kakao-muuido",
    ),
    ("Han River (Yeouido)", "Incheon Bay"): (
        "river_incheon_connector",
        "bp-kakao-yeouido",
        "bp-kakao-incheon-terminal",
    ),
}

FEATURED_BIND = {
    "Gimpo / Yeouido ↔ Jamsil / Ttukseom": "commute_gimpo_jamsil",
    "Incheon ↔ Muuido / Yeongjong": "incheon_muuido",
    "Han River (Yeouido) ↔ Incheon Bay": "river_incheon_connector",
}


def bind_journey(j: dict, key: str, fr_bp: str, to_bp: str, rid: str, bp_idx: dict) -> None:
    j["from_node_id"] = fr_bp
    j["to_node_id"] = to_bp
    j["route_id"] = rid
    j["route_ids"] = [rid]
    j["_link_status"] = "linked-grok-scoped"
    j["_link_source"] = "grok/kakao_seoul_seal"
    j["economics_status"] = "economics_bound"
    j.pop("display", None)
    j["from"] = bp_idx[fr_bp]["name"]
    j["to"] = bp_idx[to_bp]["name"]
    for r in load_json(ROUTES_PATH):
        p = props(r)
        if p.get("id") == rid and p.get("distance_nm") is not None:
            j["distance_nm"] = p["distance_nm"]
            break


def bind_market(doc: dict, rids: dict[str, str], bp_idx: dict) -> None:
    for m in doc.get("markets", []):
        if m.get("id") != MARKET and m.get("slug") != MARKET:
            continue
        for j in m.get("journeys_unlocked", []):
            pair = (str(j.get("from", "")), str(j.get("to", "")))
            spec = JOURNEY_BIND.get(pair)
            if not spec:
                continue
            key, fr_bp, to_bp = spec
            rid = rids.get(key)
            if rid:
                bind_journey(j, key, fr_bp, to_bp, rid, bp_idx)
        for phase in m.get("phases", []):
            for fr in phase.get("featured_routes", []):
                key = FEATURED_BIND.get(fr.get("label", ""))
                rid = rids.get(key) if key else None
                if not rid:
                    continue
                spec = next(s for s in ROUTES_SPEC if s[0] == key)
                fr_bp, to_bp = spec[1], spec[2]
                fr["from_node_id"] = fr_bp
                fr["to_node_id"] = to_bp
                fr["route_id"] = rid
                fr["route_ids"] = [rid]
                fr["_link_status"] = "linked-grok-scoped"
                fr["_link_source"] = "grok/kakao_seoul_seal"
                fr["economics_status"] = "economics_bound"
                fr.pop("display", None)
                fr["label"] = f"{bp_idx[fr_bp]['name']} ↔ {bp_idx[to_bp]['name']}"
                for r in load_json(ROUTES_PATH):
                    p = props(r)
                    if p.get("id") == rid and p.get("distance_nm") is not None:
                        fr["distance_nm"] = p["distance_nm"]
                        break
        m["_kakao_seoul_sealed"] = {"at": now_iso(), "routes": rids}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    fbt = load_json(FBT_PATH)
    routes = load_json(ROUTES_PATH)
    ensure_bps(fbt)
    patch_city(fbt)
    result = seal_routes(fbt, routes)

    receipt = {
        "partner": PARTNER,
        "market": MARKET,
        "generated_at": now_iso(),
        **result,
        "bp_count": len(SEOUL_BPS),
    }

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        save_json(FBT_PATH, fbt)
        bp_idx = build_bp_index(fbt)
        for path in (PITCH, DC):
            doc = load_json(path)
            bind_market(doc, result["rids"], bp_idx)
            doc.setdefault("_kakao_seoul_sealed", {"at": now_iso(), "routes": result["rids"]})
            save_json(path, doc)

    save_json(REPORT, receipt)
    print(json.dumps(receipt, indent=2))
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())