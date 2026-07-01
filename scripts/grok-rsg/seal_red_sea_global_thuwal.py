#!/usr/bin/env python3
"""Grok seal — Red Sea Global Thuwal three-destination corridors (PR #148/#149)."""
from __future__ import annotations

import argparse
import copy
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
    hav_nm,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    save_json,
    save_routes,
)
from channel_solver import HAND_WAYPOINTS  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402

PARTNER = "red-sea-global"
HAND_PATH = ROOT / "data-clean/rsg_hand_waypoints_thuwal.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
PITCH = ROOT / "partner-pitch/partners" / f"{PARTNER}.json"
DC = ROOT / "data-clean/partners" / f"{PARTNER}.json"
REPORT = ROOT / "handoff/partner-map-model/RSG-SEAL-RECEIPT-thuwal.json"

RETIRE_BPS = {
    "bp-w8-shura-marina",
    "bp-w8-amaala-marina",
    "bp-w8-amaala-yacht-club",
    "bp-w8-kaust-harbour",
    "bp-1f65535380",
}

REPARENT = {
    "bp-7760762317": "amaala-triple-bay-ksa",
    "bp-5a67c2e718": "amaala-triple-bay-ksa",
    "bp-7fc32fcaf1": "amaala-triple-bay-ksa",
    "bp-76496878a0": "amaala-triple-bay-ksa",
    "bp-d3708a5d23": "amaala-triple-bay-ksa",
    "bp-7de7f6aab4": "amaala-triple-bay-ksa",
    "bp-5375db25ed": "amaala-triple-bay-ksa",
    "bp-aafc758222": "thuwal-private-retreat-ksa",
    "bp-w8-thuwal-jetty": "thuwal-private-retreat-ksa",
    "bp-w8-sheybarah-jetty": "red-sea-global-ksa",
    "bp-w8-ummahat-jetty": "red-sea-global-ksa",
}

CORRIDORS = [
    {
        "key": "shura_nujuma",
        "from_bp": "bp-b80009b8a5",
        "to_bp": "bp-234d10fa88",
        "from_city": "red-sea-global-ksa",
        "to_city": "red-sea-global-ksa",
        "platform": "Pioneer II",
        "existing": None,
        "economics": {"revenue_usd_yr": 598_707, "margin_pct": 81},
    },
    {
        "key": "shura_turtle",
        "from_bp": "bp-b80009b8a5",
        "to_bp": "bp-917041e2d9",
        "from_city": "red-sea-global-ksa",
        "to_city": "red-sea-global-ksa",
        "platform": "Pioneer II",
        "existing": None,
        "economics": None,
    },
    {
        "key": "redsea_amaala",
        "from_bp": "bp-b80009b8a5",
        "to_bp": "bp-7760762317",
        "from_city": "red-sea-global-ksa",
        "to_city": "amaala-triple-bay-ksa",
        "platform": "Quanta-LR",
        "existing": "gcn-8e16acb312-red-sea-global",
        "economics": None,
    },
    {
        "key": "amaala_marina_yc",
        "from_bp": "bp-5a67c2e718",
        "to_bp": "bp-7760762317",
        "from_city": "amaala-triple-bay-ksa",
        "to_city": "amaala-triple-bay-ksa",
        "platform": "Pioneer II",
        "existing": None,
        "economics": {"revenue_usd_yr": 642_297, "margin_pct": 82},
    },
    {
        "key": "kaust_thuwal",
        "from_bp": "bp-aafc758222",
        "to_bp": "bp-w8-thuwal-jetty",
        "from_city": "thuwal-private-retreat-ksa",
        "to_city": "thuwal-private-retreat-ksa",
        "platform": "Pioneer II",
        "existing": None,
        "economics": {"revenue_usd_yr": 561_018, "margin_pct": 80},
    },
    {
        "key": "thuwal_reef",
        "from_bp": "bp-w8-thuwal-jetty",
        "to_bp": "bp-rsg-thuwal-reef",
        "from_city": "thuwal-private-retreat-ksa",
        "to_city": "thuwal-private-retreat-ksa",
        "platform": "Pioneer II",
        "existing": None,
        "economics": None,
    },
]

JOURNEY_KEYS = [
    "shura_nujuma",
    "redsea_amaala",
    "amaala_marina_yc",
    "kaust_thuwal",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def route_by_id(routes: list) -> dict[str, dict]:
    return {props(r).get("id"): r for r in routes if props(r).get("id")}


def bp_coords(bp_idx: dict, bp_id: str) -> tuple[float, float]:
    return tuple(bp_idx[bp_id]["coords"])


def load_hand_catalog() -> None:
    if not HAND_PATH.is_file():
        return
    catalog = load_json(HAND_PATH)
    for key, wps in catalog.get("waypoints", {}).items():
        parts = key.split("|", 1)
        if len(parts) == 2:
            HAND_WAYPOINTS[(parts[0], parts[1])] = wps


def route_coords(a: tuple[float, float], b: tuple[float, float], fr: str, to: str, mask) -> list:
    manual = HAND_WAYPOINTS.get((fr, to)) or HAND_WAYPOINTS.get((to, fr))
    if manual:
        pts = [a] + [tuple(w) for w in manual] + [b]
        if (fr, to) not in HAND_WAYPOINTS and (to, fr) in HAND_WAYPOINTS:
            pts = [a] + [tuple(w) for w in reversed(manual)] + [b]
        return [[p[0], p[1]] for p in pts]
    return build_coastal_path(a, b, mask)


def ensure_priority_city(fbt: dict, city_id: str, name: str, coords: list[float], country: str = "Saudi Arabia") -> None:
    feat = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": coords},
        "properties": {
            "id": city_id,
            "type": "priority_city",
            "name": name,
            "shortName": name.split("(")[0].strip()[:24],
            "fullName": name,
            "country": country,
            "region": "MENA",
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "grok/rsg_thuwal_seal_2026-07-01",
            "cluster_id": "saudi-arabia",
            "tier_sort_key": 1,
            "priority": "high",
            "_rsg_thuwal_sealed": now_iso(),
        },
    }
    for bucket in ("priority_city", "city"):
        arr = fbt.setdefault(bucket, [])
        for i, f in enumerate(arr):
            if props(f).get("id") == city_id:
                if bucket == "city":
                    arr.pop(i)
                else:
                    arr[i] = feat
                    return
        if bucket == "priority_city":
            arr.append(feat)


def patch_surface(fbt: dict, routes: list, apply: bool) -> dict:
    pois = fbt.setdefault("poi", [])
    kept_pois = []
    retired = []
    for poi in pois:
        pid = props(poi).get("id")
        if pid in RETIRE_BPS:
            retired.append(pid)
            continue
        if pid in REPARENT:
            props(poi)["parent_city_id"] = REPARENT[pid]
        kept_pois.append(poi)
    fbt["poi"] = kept_pois

    # Thuwal reef anchorage BP
    if not any(props(p).get("id") == "bp-rsg-thuwal-reef" for p in fbt["poi"]):
        fbt["poi"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [39.075, 22.265]},
                "properties": {
                    "id": "bp-rsg-thuwal-reef",
                    "type": "poi",
                    "name": "Thuwal coral-archipelago snorkel anchorage",
                    "shortName": "Thuwal reef anchorage",
                    "fullName": "Thuwal coral-archipelago snorkel anchorage",
                    "parent_city_id": "thuwal-private-retreat-ksa",
                    "bp_type": "anchorage",
                    "status": "operational",
                    "confidence": "high",
                    "_rsg_thuwal_sealed": now_iso(),
                },
            }
        )

    for f in fbt.get("city", []):
        p = props(f)
        if p.get("id") == "red-sea-global-ksa":
            p["name"] = "The Red Sea"
            p["shortName"] = "The Red Sea"
            p["fullName"] = "The Red Sea"
            p["coords_source"] = "grok/rsg_thuwal_seal_2026-07-01"
            f["geometry"]["coordinates"] = [36.93, 25.46]

    ensure_priority_city(fbt, "amaala-triple-bay-ksa", "AMAALA (Triple Bay)", [36.216, 26.644])
    ensure_priority_city(fbt, "thuwal-private-retreat-ksa", "Thuwal (Private Retreat)", [39.0972, 22.305])

    load_hand_catalog()
    mask = load_land_mask()
    bp_idx = build_bp_index(fbt)
    cities = {
        "red-sea-global-ksa": "The Red Sea",
        "amaala-triple-bay-ksa": "AMAALA (Triple Bay)",
        "thuwal-private-retreat-ksa": "Thuwal (Private Retreat)",
    }
    ridx = route_by_id(routes)
    bound: dict[str, str] = {}
    minted = []
    failed = []

    for spec in CORRIDORS:
        rid = spec.get("existing")
        if rid and rid in ridx:
            bound[spec["key"]] = rid
            continue
        fr, to = spec["from_bp"], spec["to_bp"]
        if fr not in bp_idx or to not in bp_idx:
            failed.append({"key": spec["key"], "reason": "missing_bp"})
            continue
        tag = f"rsg_thuwal_{spec['key']}"
        rid = mint_route_id(fr, to, tag)
        if rid in ridx:
            bound[spec["key"]] = rid
            continue
        a = bp_coords(bp_idx, fr)
        b = bp_coords(bp_idx, to)
        coords = route_coords(a, b, fr, to, mask)
        land_km = interior_land_km(coords, mask)
        qa = evaluate_route(coords)
        if not qa.get("qa_pass"):
            failed.append({"key": spec["key"], "land_km": land_km, "qa": qa})
            continue
        feat = make_route_feature(
            fr,
            to,
            bp_idx[fr]["name"],
            bp_idx[to]["name"],
            spec["from_city"],
            spec["to_city"],
            coords,
            cities,
            source="rsg_thuwal_seal",
            land_km=land_km,
        )
        p = props(feat)
        p["platform"] = spec["platform"]
        p["id"] = rid
        p["_rsg_thuwal_sealed"] = now_iso()
        routes.append(feat)
        bound[spec["key"]] = rid
        minted.append(rid)

    receipt = {
        "partner": PARTNER,
        "generated_at": now_iso(),
        "retired_bps": retired,
        "minted_routes": minted,
        "bound": bound,
        "failed": failed,
    }

    if apply:
        save_routes(ROUTES_PATH, routes)
        save_json(FBT_PATH, fbt)
    return receipt


def bind_link(item: dict, spec: dict, rid: str, bp_idx: dict) -> None:
    item["from_node_id"] = spec["from_bp"]
    item["to_node_id"] = spec["to_bp"]
    item["route_id"] = rid
    item["route_ids"] = [rid]
    item["_link_status"] = "linked-grok-scoped"
    item["_link_source"] = "grok/rsg_thuwal_seal"
    item["economics_status"] = "economics_bound"
    item.pop("display", None)
    r = route_by_id(load_json(ROUTES_PATH)).get(rid)
    if r:
        item["distance_nm"] = props(r).get("distance_nm")
    if spec.get("economics"):
        item["_economics"] = spec["economics"]


FEATURED_KEY_BY_LABEL = {
    "Ummahat": "shura_nujuma",
    "Turtle Bay": "shura_turtle",
    "AMAALA Triple Bay": "redsea_amaala",
    "AMAALA Marina": "amaala_marina_yc",
    "Thuwal Private Retreat island": "kaust_thuwal",
    "coral-archipelago": "thuwal_reef",
}


def bind_partner(receipt: dict, apply: bool) -> None:
    key_to_spec = {c["key"]: c for c in CORRIDORS}
    routes = load_json(ROUTES_PATH)
    fbt = load_json(FBT_PATH)
    bp_idx = build_bp_index(fbt)

    for path in (PITCH, DC):
        doc = load_json(path)
        for phase in doc.get("phases", []):
            for fr_item in phase.get("featured_routes", []):
                label = fr_item.get("label", "")
                key = next((k for token, k in FEATURED_KEY_BY_LABEL.items() if token in label), None)
                if not key:
                    if "Triple Bay" in label and "AMAALA Marina" not in label:
                        key = "redsea_amaala"
                spec = key_to_spec.get(key) if key else None
                rid = receipt["bound"].get(key) if key else None
                if spec and rid:
                    bind_link(fr_item, spec, rid, bp_idx)

        journey_map = {
            "Shura Island hub": "shura_nujuma",
            "The Red Sea (Shura)": "redsea_amaala",
            "AMAALA Marina": "amaala_marina_yc",
            "KAUST Harbour": "kaust_thuwal",
        }
        for j in doc.get("journeys_unlocked", []):
            for prefix, key in journey_map.items():
                if str(j.get("from", "")).startswith(prefix):
                    spec = key_to_spec.get(key)
                    rid = receipt["bound"].get(key)
                    if spec and rid:
                        bind_link(j, spec, rid, bp_idx)
                        j["render"] = "solid"

        doc["_rsg_thuwal_sealed"] = {"at": now_iso(), "by": "grok", "routes": receipt["bound"]}
        if apply:
            save_json(path, doc)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    fbt = load_json(FBT_PATH)
    routes = load_json(ROUTES_PATH)
    receipt = patch_surface(fbt, routes, apply=args.apply)
    if args.apply:
        bind_partner(receipt, apply=True)
    save_json(REPORT, receipt)
    print(json.dumps(receipt, indent=2))
    return 1 if receipt["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())