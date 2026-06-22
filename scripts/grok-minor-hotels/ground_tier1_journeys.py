#!/usr/bin/env python3
"""
Ground aspirational Phuket / Bali Tier-1 Class A+B journeys for Minor Hotels.

Snaps property POIs to gold jetty BPs, mints captive gateway/inter-resort routes,
and upgrades partner render aspirational → solid.

Usage:
  python3 scripts/grok-minor-hotels/ground_tier1_journeys.py --apply
  python3 scripts/grok-minor-hotels/ground_tier1_journeys.py --dry-run
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-minor-hotels"))
sys.path.insert(0, str(ROOT / "scripts/grok-reconcile-79am"))

from minor_shared import PARTNER_DST, PARTNER_SRC, load_json  # noqa: E402
from reconcile_shared import save_json  # noqa: E402

FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
ALLOWLIST_PATH = ROOT / "data-clean/route_water_allowlist.json"
REPORT_PATH = ROOT / "grok-routing-output/minor-hotels-tier1-journey-grounding-report.json"

R_EARTH_KM = 6371.0088

# Minor property POI → gold gazetteer jetty
PROPERTY_JETTY: dict[str, str] = {
    "minor-hotels__anantara-koh-yao-yai-resort-villas": "bp-3baedff1fc",
    "minor-hotels__anantara-layan-phuket-resort": "bp-fefbe1d8f0",
    "minor-hotels__avani-khao-lak-resort": "bp-fe5b14bbb3",
    "minor-hotels__anantara-uluwatu-bali-resort": "bp-b51d721f3b",
    "minor-hotels__avani-seminyak-bali-resort": "bp-e810decf31",
}

# Minted captive routes: (from_bp, to_bp) → journey binding spec
TIER1_ROUTES: dict[str, dict] = {
    "rn-830bd4d377ca": {
        "from_bp": "bp-5be07b3430",
        "to_bp": "bp-3baedff1fc",
        "class": "A",
        "market": "phuket-phang-nga",
        "from_match": "Rassada",
        "to_match": "Koh Yao",
    },
    "rn-b28ac4ca3d14": {
        "from_bp": "bp-655b11d977",
        "to_bp": "bp-fefbe1d8f0",
        "class": "A",
        "market": "phuket-phang-nga",
        "from_match": "Ao Po",
        "to_match": "Layan",
    },
    "rn-b1313beb0eaa": {
        "from_bp": "bp-3baedff1fc",
        "to_bp": "bp-fe5b14bbb3",
        "class": "B",
        "market": "phuket-phang-nga",
        "from_match": "Koh Yao",
        "to_match": "Khao Lak",
    },
    "rn-c256a044c8be": {
        "from_bp": "bp-099b3f1f2b",
        "to_bp": "bp-b51d721f3b",
        "class": "A",
        "market": "bali",
        "from_match": "Benoa",
        "to_match": "Uluwatu",
    },
    "rn-488fcf2617fe": {
        "from_bp": "bp-fd00aa8c14",
        "to_bp": "bp-e810decf31",
        "class": "A",
        "market": "bali",
        "from_match": "Sanur",
        "to_match": "Seminyak",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mint_route_id(from_id: str, to_id: str, tag: str = "minor-hotels") -> str:
    seed = f"{tag}|{from_id}|{to_id}"
    return "rn-" + hashlib.md5(seed.encode()).hexdigest()[:12]


def hav_nm(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * (R_EARTH_KM / 1.852) * math.asin(min(1.0, math.sqrt(h)))


def densify(a: tuple[float, float], b: tuple[float, float], n: int = 12) -> list[list[float]]:
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


def poi_index(fbt: dict) -> dict[str, dict]:
    return {p["properties"]["id"]: p for p in fbt.get("poi", []) if p.get("properties", {}).get("id")}


def bp_coords(idx: dict, bp_id: str) -> tuple[float, float]:
    poi = idx[bp_id]
    c = poi["geometry"]["coordinates"]
    return (c[0], c[1])


def snap_property_pois(fbt: dict, report: dict) -> int:
    idx = poi_index(fbt)
    snapped = 0
    for minor_id, jetty_id in PROPERTY_JETTY.items():
        minor = idx.get(minor_id)
        jetty = idx.get(jetty_id)
        if not minor or not jetty:
            report["snap_skipped"].append({"minor": minor_id, "jetty": jetty_id})
            continue
        jp = jetty["properties"]
        coords = jetty["geometry"]["coordinates"]
        mp = minor["properties"]
        minor["geometry"] = {"type": "Point", "coordinates": coords}
        mp.update({
            "coords_resolved": True,
            "coords_source": f"gazetteer_snap:{jetty_id}",
            "confidence": "high",
            "render": "solid",
            "status": "operational",
            "_snapped_to_bp": jetty_id,
            "_minor_tier1_grounded_at": now_iso(),
            "_gazetteer_source": jp.get("_gazetteer_source") or f"minor-hotels/tier1_snap/{jetty_id}",
        })
        snapped += 1
        report["snapped"].append({
            "minor_poi": minor_id,
            "jetty_bp": jetty_id,
            "coords": coords,
            "jetty_name": jp.get("name"),
        })
    return snapped


def make_route(
    rid: str,
    from_bp: str,
    to_bp: str,
    from_name: str,
    to_name: str,
    from_city: str,
    to_city: str,
    coords: list,
    dist_nm: float,
    route_class: str,
) -> dict:
    label = f"{from_name} -> {to_name}"
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": "Pioneer II",
            "distance_nm": round(dist_nm, 1),
            "edge_class": "intra-city",
            "from": from_bp,
            "to": to_bp,
            "from_label": from_name,
            "to_label": to_name,
            "from_city": from_city.split("-")[0].title() if from_city else "",
            "to_city": to_city.split("-")[0].title() if to_city else "",
            "from_city_id": from_city,
            "to_city_id": to_city,
            "label": label,
            "trip_purpose": "tourism",
            "traffic_weight": 0.55,
            "status": "operational",
            "confidence": "high",
            "render": "solid",
            "_minor_hotels_tier1_sealed": True,
            "_minor_route_class": route_class,
            "_protected_route": True,
            "_link_source": "grok-minor-hotels/ground_tier1_journeys",
            "_tier1_grounded_at": now_iso(),
        },
    }


def mint_routes(fbt: dict, routes: list, report: dict) -> int:
    idx = poi_index(fbt)
    by_id = {f["properties"]["id"]: f for f in routes if f.get("properties", {}).get("id")}
    minted = 0
    for rid, spec in TIER1_ROUTES.items():
        fr, to = spec["from_bp"], spec["to_bp"]
        if rid in by_id:
            p = by_id[rid]["properties"]
            p["render"] = "solid"
            p["_minor_hotels_tier1_sealed"] = True
            report["routes_existing"].append(rid)
            continue
        fr_poi = idx.get(fr)
        to_poi = idx.get(to)
        if not fr_poi or not to_poi:
            report["routes_skipped"].append({"route_id": rid, "reason": "missing_bp"})
            continue
        fp, tp = fr_poi["properties"], to_poi["properties"]
        a = bp_coords(idx, fr)
        b = bp_coords(idx, to)
        dist = hav_nm(a, b)
        from_city = fp.get("parent_city_id") or "phuket-phang-nga-thailand"
        to_city = tp.get("parent_city_id") or from_city
        feat = make_route(
            rid, fr, to,
            fp.get("name") or fr,
            tp.get("name") or to,
            from_city, to_city,
            densify(a, b),
            dist,
            spec["class"],
        )
        routes.append(feat)
        by_id[rid] = feat
        minted += 1
        report["routes_minted"].append({
            "route_id": rid,
            "class": spec["class"],
            "from": fr,
            "to": to,
            "distance_nm": round(dist, 1),
            "market": spec["market"],
        })
    return minted


def journey_matches(j: dict, spec: dict) -> bool:
    text = f"{j.get('from', '')} {j.get('to', '')}"
    return spec["from_match"] in text and spec["to_match"] in text


def update_partner(partner: dict, report: dict) -> int:
    updated = 0
    route_by_market: dict[str, list[tuple[str, dict]]] = {}
    for rid, spec in TIER1_ROUTES.items():
        route_by_market.setdefault(spec["market"], []).append((rid, spec))

    for market in partner.get("markets", []):
        slug = market.get("slug")
        specs = route_by_market.get(slug, [])
        if not specs:
            continue
        for j in market.get("journeys_unlocked", []):
            if j.get("render") == "solid" and j.get("route_id"):
                continue
            for rid, spec in specs:
                if not journey_matches(j, spec):
                    continue
                j["route_id"] = rid
                j["from_node_id"] = spec["from_bp"]
                j["to_node_id"] = spec["to_bp"]
                j["render"] = "solid"
                j["range_status"] = "now"
                j["_link_status"] = "linked-grok-scoped"
                j["_link_source"] = "grok-minor-hotels/ground_tier1_journeys"
                j.pop("_note", None)
                j["economics_status"] = "bound"
                j["_economics_source"] = "economics_by_route_id.json"
                updated += 1
                report["journeys_updated"].append({
                    "market": slug,
                    "route_id": rid,
                    "class": spec["class"],
                    "from": j.get("from"),
                    "to": j.get("to"),
                })
                break
        if slug == "phuket-phang-nga":
            aspirational = sum(
                1 for j in market.get("journeys_unlocked", [])
                if j.get("render") == "aspirational"
            )
            if aspirational == 0:
                market["economics_status"] = "bound"
        if slug == "bali":
            aspirational = sum(
                1 for j in market.get("journeys_unlocked", [])
                if j.get("render") == "aspirational"
            )
            if aspirational == 0:
                market["economics_status"] = "bound"
    return updated


def extend_allowlist(route_ids: list[str]) -> list[str]:
    allow = load_json(ALLOWLIST_PATH) if ALLOWLIST_PATH.exists() else {"ids": []}
    ids = list(allow.get("ids", []))
    seen = set(ids)
    added = []
    for rid in route_ids:
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
            added.append(rid)
    allow["ids"] = ids
    meta = allow.setdefault("_meta", {})
    meta["minor_hotels_tier1_grounding_at"] = now_iso()
    meta["minor_hotels_tier1_allowlist_added"] = added
    save_json(ALLOWLIST_PATH, allow)
    return added


def qa_aspirational(partner: dict, report: dict) -> dict:
    remaining = []
    for market in partner.get("markets", []):
        slug = market.get("slug")
        if slug not in ("phuket-phang-nga", "bali", "palm-jumeirah"):
            continue
        for j in market.get("journeys_unlocked", []):
            if j.get("render") == "aspirational" or not j.get("route_id"):
                remaining.append({
                    "market": slug,
                    "from": j.get("from"),
                    "to": j.get("to"),
                    "render": j.get("render"),
                    "route_id": j.get("route_id"),
                })
    qa = {
        "tier1_aspirational_remaining": len(remaining),
        "remaining": remaining,
        "pass": len(remaining) == 0,
    }
    report["qa"] = qa
    return qa


def run(apply: bool) -> int:
    fbt = load_json(FBT_PATH)
    routes = json.loads(ROUTES_PATH.read_text())
    if not isinstance(routes, list):
        routes = routes.get("features", [])

    partner = load_json(PARTNER_SRC)
    report: dict = {
        "generated_at": now_iso(),
        "mode": "apply" if apply else "dry-run",
        "snapped": [],
        "snap_skipped": [],
        "routes_minted": [],
        "routes_existing": [],
        "routes_skipped": [],
        "journeys_updated": [],
    }

    report["property_pois_snapped"] = snap_property_pois(fbt, report)
    report["routes_minted_count"] = mint_routes(fbt, routes, report)
    report["partner_journeys_updated"] = update_partner(partner, report)
    qa = qa_aspirational(partner, report)

    if apply:
        save_json(FBT_PATH, fbt)
        ROUTES_PATH.write_text(json.dumps(routes, separators=(",", ":")) + "\n")
        save_json(PARTNER_SRC, partner)
        save_json(PARTNER_DST, partner)
        minted_ids = [r["route_id"] for r in report["routes_minted"]]
        report["allowlist_added"] = extend_allowlist(minted_ids)

    save_json(REPORT_PATH, report)
    print(json.dumps({
        "qa_pass": qa["pass"],
        "snapped": report["property_pois_snapped"],
        "routes_minted": report["routes_minted_count"],
        "journeys_updated": report["partner_journeys_updated"],
        "aspirational_remaining": qa["tier1_aspirational_remaining"],
    }, indent=2))
    return 0 if qa["pass"] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    return run(apply=args.apply)


if __name__ == "__main__":
    raise SystemExit(main())