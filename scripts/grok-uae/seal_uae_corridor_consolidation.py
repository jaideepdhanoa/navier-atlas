#!/usr/bin/env python3
"""Grok seal — UAE corridor consolidation (2026-07-05).

Drop dirty UAE BPs, remove all UAE-touching routes, rebuild significant
hub-spoke corridors (Gulf vs east-coast separate), route with hand-waypoints,
stamp cluster_id, target 0 land flags.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    NM_PER_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    hav_nm,
    load_json,
    make_route_feature,
    mint_route_id,
    path_length_km,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from bolt_yango_shared import load_land_mask  # noqa: E402
from channel_solver import HAND_WAYPOINTS  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402

REPORT = ROOT / "grok-routing-output/uae-corridor-consolidation-report.json"
HAND_PATH = ROOT / "data-clean/uae_hand_waypoints.json"
SEAL_TAG = "uae-corridor-consolidation-2026-07-05"

UAE_CITIES = frozenset(
    {
        "dubai-uae",
        "abu-dhabi-uae",
        "sharjah-uae",
        "ras-al-khaimah-uae",
        "fujairah-uae",
        "ajman-uae",
        "umm-al-quwain-uae",
    }
)

CENTROID_NAMES = frozenset({"Abu Dhabi", "Fujairah", "Ras Al Khaimah", "Dubai", "Sharjah"})

DIRTY_RE = re.compile(
    r"jet\s*ski|water\s*sport|diving|divecampus|msc|boat\s*ramp|kingfisher\s*lodge|kayak|tour\s*operator",
    re.I,
)
JUNK_RE = re.compile(
    r"helipad|seaplane|parking|dry dock|boat yard|container port|cargo port|crude|"
    r"industrial channel|kizad|mussafah|viewpoint|non stop|waves marine|"
    r"home interiors|photos kodak|restaurant|retail|shop|mall interior",
    re.I,
)
PLANNED_RE = re.compile(r"\(planned\)|planned/|proposed|under construction", re.I)
EAST_RE = re.compile(r"khorfakkan|khor fakkan|kalba|dibba|aqah|murbah|dadna", re.I)
MUSANDAM_RE = re.compile(r"zighy|khasab|musandam", re.I)
SIR_BANI_RE = re.compile(r"sir bani yas|desert island|jebel dhanna|delma|dalma", re.I)
ISLAND_RE = re.compile(
    r"world island|heart of europe|lulu island|nurai|zaya|atlantis|one&only the palm|bluewaters",
    re.I,
)
QB_RE = re.compile(r"qatar|bahrain|doha|manama", re.I)

LAND_THRESH_KM = 0.05
MIN_NM = 2.0
MAX_NM = 70.0
DEDUPE_KM = 0.4

CLUSTER_GULF = "uae"
CLUSTER_EAST = "uae-east-coast"
CLUSTER_SIR = "uae-sir-bani-yas"

MUSANDAM_BP_HINTS = (
    "bp-ecd6f8e183",
    "bp-8f6140f2d4",
    "bp-121822",
)

# Spec / canonical marquee OD seeds (significance floor — not a ceiling).
MARQUEE_SEED_PAIRS: tuple[tuple[str, str], ...] = (
    ("bp-fadfae552e", "bp-55aa98c7fb"),  # Dubai Marina ↔ Atlantis Palm
    ("bp-fadfae552e", "bp-26eff0c4b6"),  # Dubai Marina ↔ Dubai Harbour
    ("bp-26eff0c4b6", "bp-55aa98c7fb"),  # Dubai Harbour ↔ Atlantis
    ("bp-26eff0c4b6", "bp-8c7fcc1977"),  # Dubai Harbour ↔ World Islands
    ("bp-00a6462e28", "bp-5c7aaead40"),  # Old Souq ↔ Festival City Marina (creek)
    ("bp-f53314647f", "bp-fadfae552e"),  # One&Only Palm ↔ Dubai Marina
    ("bp-56d5f5bd8d", "bp-1982dfd974"),  # Yas Marina ↔ Saadiyat Ferry
    ("bp-44685987bc", "bp-8b8245f21b"),  # Khorfakkan ↔ Fujairah/Dibba chain anchor
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def coast_kind(pid: str, bp_idx: dict) -> str:
    row = bp_idx[pid]
    name = row.get("name") or ""
    city = row.get("parent_city_id") or ""
    if SIR_BANI_RE.search(name):
        return "sir"
    if city == "fujairah-uae" or EAST_RE.search(name):
        return "east"
    return "gulf"


def dirty_reason(name: str) -> str | None:
    if not name or not name.strip():
        return "empty_name"
    if name in CENTROID_NAMES:
        return "centroid"
    if DIRTY_RE.search(name):
        return "dirty_activity"
    if JUNK_RE.search(name):
        return "junk_endpoint"
    if PLANNED_RE.search(name):
        return "planned_jetty"
    return None


def hub_score(name: str) -> int:
    n = name.lower()
    score = 0
    if "marina" in n:
        score += 4
    if "ferry" in n or "terminal" in n:
        score += 4
    if "marine station" in n or "marine transport" in n:
        score += 3
    if "corniche pier" in n:
        score += 3
    if "harbour" in n or "harbor" in n:
        score += 2
    if ISLAND_RE.search(name):
        score += 3
    if MUSANDAM_RE.search(name):
        score += 2
    return score


def classify_locale(pid: str, bp_idx: dict) -> tuple[str, str]:
    row = bp_idx[pid]
    name = (row.get("name") or "").lower()
    city = row.get("parent_city_id") or ""
    ck = coast_kind(pid, bp_idx)

    if ck == "sir":
        return ("sir", city)
    if ck == "east":
        if city == "fujairah-uae" or "fujairah" in name:
            return ("east", "fujairah")
        if "khorfakkan" in name or "khor fakkan" in name:
            return ("east", "khorfakkan")
        if "kalba" in name:
            return ("east", "kalba")
        if "dibba" in name:
            return ("east", "dibba")
        if "aqah" in name:
            return ("east", "aqah")
        return ("east", city)

    if city == "dubai-uae":
        if any(x in name for x in ("creek", "deira", "festival", "souq", "jaddaf", "bur dubai")):
            return ("gulf", "dubai-creek")
        if "marina" in name and "palm" not in name:
            return ("gulf", "dubai-marina")
        if "harbour" in name or "ain dubai" in name:
            return ("gulf", "dubai-harbour")
        if "palm" in name or "atlantis" in name or "zabeel" in name:
            return ("gulf", "dubai-palm")
        if "world" in name or "heart" in name:
            return ("gulf", "dubai-world")
        if "bulgari" in name or "mina rashid" in name:
            return ("gulf", "dubai-bulgari")
        return ("gulf", "dubai-metro")

    if city == "abu-dhabi-uae":
        if "yas" in name:
            return ("gulf", "ad-yas")
        if any(x in name for x in ("saadiyat", "nurai", "zaya")):
            return ("gulf", "ad-saadiyat")
        if any(x in name for x in ("maryah", "corniche", "palace", "lulu", "breakwater", "marina mall")):
            return ("gulf", "ad-cbd")
        if "rabdan" in name:
            return ("gulf", "ad-rabdan")
        return ("gulf", "ad-metro")

    if city == "sharjah-uae":
        if EAST_RE.search(row.get("name") or ""):
            return ("east", "shj-east")
        if any(x in name for x in ("majaz", "khalid", "lagoon", "ajman", "zorah")):
            return ("gulf", "shj-lagoon")
        return ("gulf", "shj-metro")

    if city == "ras-al-khaimah-uae":
        if any(x in name for x in ("ajman", "zorah")):
            return ("gulf", "shj-lagoon")
        if "marjan" in name or "wynn" in name:
            return ("gulf", "rak-marjan")
        if any(x in name for x in ("hamra", "mina al arab", "anantara")):
            return ("gulf", "rak-hamra")
        if "corniche" in name:
            return ("gulf", "rak-corniche")
        return ("gulf", "rak-metro")

    return (ck, city)


def cluster_for_pair(a: str, b: str, bp_idx: dict) -> str:
    kinds = {coast_kind(x, bp_idx) for x in (a, b)}
    if kinds == {"sir"}:
        return CLUSTER_SIR
    if "east" in kinds:
        return CLUSTER_EAST
    return CLUSTER_GULF


def pair_distance_nm(a: str, b: str, bp_idx: dict) -> float:
    ac = bp_idx[a]["coords"]
    bc = bp_idx[b]["coords"]
    return hav_nm(tuple(ac), tuple(bc))


def load_hand_waypoint_catalog() -> int:
    if not HAND_PATH.is_file():
        return 0
    doc = load_json(HAND_PATH)
    added = 0
    for row in doc.get("pairs") or []:
        fn = row.get("from")
        tn = row.get("to")
        wps = row.get("waypoints") or []
        if not fn or not tn or not wps:
            continue
        key = (fn, tn)
        if key not in HAND_WAYPOINTS:
            HAND_WAYPOINTS[key] = [[float(w[0]), float(w[1])] for w in wps]
            added += 1
    return added


def _densify_chain(points: list[tuple[float, float]], steps: int = 16) -> list[list[float]]:
    from bolt_yango_routing_shared import densify  # noqa: WPS433

    out: list[list[float]] = []
    for i in range(len(points) - 1):
        seg = densify(points[i], points[i + 1], n=steps)
        out.extend(seg if not out else seg[1:])
    return out


def _qa_accept(coords: list[list[float]]) -> tuple[bool, float]:
    ev = evaluate_route(coords)
    land = float(ev.get("interior_land_km", 0.0))
    return land <= LAND_THRESH_KM and bool(ev.get("qa_pass")), land


def route_geometry(
    a: str,
    b: str,
    bp_idx: dict,
    mask,
    legacy_geom: dict[tuple[str, str], list],
) -> tuple[list[list[float]], float] | None:
    ac = tuple(bp_idx[a]["coords"])
    bc = tuple(bp_idx[b]["coords"])

    wps: list[tuple[float, float]] = []
    for key in ((a, b), (b, a)):
        if key in HAND_WAYPOINTS and HAND_WAYPOINTS[key]:
            wps = [(float(w[0]), float(w[1])) for w in HAND_WAYPOINTS[key]]
            break

    candidates: list[list[list[float]]] = []
    if wps:
        candidates.append(_densify_chain([ac, *wps, bc]))
        candidates.append(build_coastal_path(ac, bc, mask, manual_waypoints=wps))

    for key in ((a, b), (b, a)):
        old = legacy_geom.get(key)
        if old:
            ok, _ = _qa_accept(old)
            if ok:
                candidates.append(old)
            rev = list(reversed(old))
            ok, _ = _qa_accept(rev)
            if ok:
                candidates.append(rev)

    candidates.append(build_coastal_path(ac, bc, mask))

    for coords in candidates:
        ok, land = _qa_accept(coords)
        if ok:
            return coords, land
    return None


def select_kept_bps(bp_idx: dict) -> tuple[dict[str, int], dict[str, str]]:
    """Return kept bp_id -> hub_score, dropped bp_id -> reason."""
    kept: dict[str, int] = {}
    dropped: dict[str, str] = {}

    for pid, row in bp_idx.items():
        city = row.get("parent_city_id")
        if city not in UAE_CITIES:
            continue
        reason = dirty_reason(row.get("name") or "")
        if reason:
            dropped[pid] = reason
            continue
        score = hub_score(row.get("name") or "")
        if score >= 3 or ISLAND_RE.search(row.get("name") or ""):
            kept[pid] = score
            continue
        if coast_kind(pid, bp_idx) == "east" and score >= 2:
            kept[pid] = score

    by_city: dict[str, list[str]] = defaultdict(list)
    for pid in kept:
        by_city[bp_idx[pid]["parent_city_id"]].append(pid)

    for pids in by_city.values():
        pids.sort(key=lambda p: kept[p], reverse=True)
        remove: set[str] = set()
        for i, a in enumerate(pids):
            if a in remove:
                continue
            ac = bp_idx[a]["coords"]
            for b in pids[i + 1 :]:
                if b in remove:
                    continue
                if pair_distance_nm(a, b, bp_idx) * 1.852 < DEDUPE_KM:
                    remove.add(b)
                    dropped[b] = "duplicate_proximity"
        for b in remove:
            kept.pop(b, None)

    return kept, dropped


def build_locale_hubs(kept: dict[str, int], bp_idx: dict) -> dict[tuple[str, str], str]:
    locale_hubs: dict[tuple[str, str], str] = {}
    for pid in kept:
        loc = classify_locale(pid, bp_idx)
        if loc not in locale_hubs or kept[pid] > kept[locale_hubs[loc]]:
            locale_hubs[loc] = pid
    return locale_hubs


def build_corridor_pairs(kept: dict[str, int], bp_idx: dict) -> set[tuple[str, str]]:
    locale_hubs = build_locale_hubs(kept, bp_idx)
    pairs: set[tuple[str, str]] = set()

    by_cc: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    for loc, pid in locale_hubs.items():
        city = bp_idx[pid]["parent_city_id"]
        by_cc[(loc[0], city)].append((loc[1], pid))

    for (_coast, _city), locs in by_cc.items():
        for (_, a), (_, b) in combinations(locs, 2):
            if a == b:
                continue
            if coast_kind(a, bp_idx) != coast_kind(b, bp_idx):
                continue
            d = pair_distance_nm(a, b, bp_idx)
            if MIN_NM <= d <= MAX_NM:
                pairs.add(tuple(sorted((a, b))))

    east_hubs = [pid for loc, pid in locale_hubs.items() if loc[0] == "east"]
    for i, a in enumerate(east_hubs):
        for b in east_hubs[i + 1 :]:
            d = pair_distance_nm(a, b, bp_idx)
            if MIN_NM <= d <= MAX_NM:
                pairs.add(tuple(sorted((a, b))))

    sir_hubs = [pid for loc, pid in locale_hubs.items() if loc[0] == "sir"]
    for i, a in enumerate(sir_hubs):
        for b in sir_hubs[i + 1 :]:
            d = pair_distance_nm(a, b, bp_idx)
            if MIN_NM <= d <= MAX_NM:
                pairs.add(tuple(sorted((a, b))))

    hub_ids = set(locale_hubs.values())
    for pid in kept:
        if pid in hub_ids:
            continue
        loc = classify_locale(pid, bp_idx)
        hub = locale_hubs.get(loc)
        if not hub or hub == pid:
            continue
        d = pair_distance_nm(pid, hub, bp_idx)
        if MIN_NM <= d <= MAX_NM:
            pairs.add(tuple(sorted((pid, hub))))

    for a, b in MARQUEE_SEED_PAIRS:
        if a not in kept or b not in kept:
            continue
        if coast_kind(a, bp_idx) != coast_kind(b, bp_idx):
            continue
        d = pair_distance_nm(a, b, bp_idx)
        if MIN_NM <= d <= MAX_NM:
            pairs.add(tuple(sorted((a, b))))

    return pairs


def musandam_marquee_pair(kept: dict[str, int], bp_idx: dict) -> tuple[str, str] | None:
    east_ids = [p for p in kept if coast_kind(p, bp_idx) == "east"]
    if not east_ids:
        return None
    musandam = [
        pid
        for pid, row in bp_idx.items()
        if MUSANDAM_RE.search(row.get("name") or "") or pid in MUSANDAM_BP_HINTS
    ]
    if not musandam:
        return None
    best: tuple[str, str, float] | None = None
    for eu in east_ids:
        for mo in musandam:
            d = pair_distance_nm(eu, mo, bp_idx)
            if MIN_NM <= d <= MAX_NM and (best is None or d < best[2]):
                best = (eu, mo, d)
    if not best:
        return None
    return tuple(sorted((best[0], best[1])))


def route_touches_uae(route: dict, bp_idx: dict) -> bool:
    p = props(route)
    fc = p.get("from_city_id")
    tc = p.get("to_city_id")
    if fc in UAE_CITIES or tc in UAE_CITIES:
        return True
    fn = p.get("from") or p.get("from_node")
    tn = p.get("to") or p.get("to_node")
    for nid in (fn, tn):
        if nid and bp_idx.get(nid, {}).get("parent_city_id") in UAE_CITIES:
            return True
    return False


def is_qb_cross_border(route: dict) -> bool:
    p = props(route)
    fc, tc = p.get("from_city_id"), p.get("to_city_id")
    other = tc if fc in UAE_CITIES else fc if tc in UAE_CITIES else None
    return bool(other and QB_RE.search(other))


def drop_dirty_pois(fbt: dict, dropped: dict[str, str], apply: bool) -> int:
    new_pois = []
    n_drop = 0
    for poi in fbt.get("poi", []):
        pid = props(poi).get("id")
        if pid in dropped:
            n_drop += 1
            continue
        new_pois.append(poi)
    if apply:
        fbt["poi"] = new_pois
    return n_drop


def drop_orphan_pois(fbt: dict, used_bp_ids: set[str], apply: bool) -> int:
    new_pois = []
    n_drop = 0
    for poi in fbt.get("poi", []):
        p = props(poi)
        pid = p.get("id")
        city = p.get("parent_city_id")
        if city in UAE_CITIES and pid not in used_bp_ids:
            n_drop += 1
            continue
        new_pois.append(poi)
    if apply:
        fbt["poi"] = new_pois
    return n_drop


def stamp_bp_clusters(fbt: dict, bp_idx: dict, apply: bool) -> dict[str, int]:
    counts = defaultdict(int)
    for poi in fbt.get("poi", []):
        p = props(poi)
        pid = p.get("id")
        if pid not in bp_idx or p.get("parent_city_id") not in UAE_CITIES:
            continue
        ck = coast_kind(pid, bp_idx)
        if ck == "east":
            cid = CLUSTER_EAST
        elif ck == "sir":
            cid = CLUSTER_SIR
        else:
            cid = CLUSTER_GULF
        if apply:
            p["cluster_id"] = cid
            p["_uae_consolidation_seal"] = utc_now()
        counts[cid] += 1
    return dict(counts)


def update_clusters(clusters_doc: dict, apply: bool) -> dict:
    clusters = clusters_doc.get("clusters") or []
    by_id = {c.get("cluster_id"): c for c in clusters}

    uae = by_id.get(CLUSTER_GULF)
    if uae:
        members = list(uae.get("member_city_ids") or [])
        if "fujairah-uae" in members:
            members = [m for m in members if m != "fujairah-uae"]
        uae["member_city_ids"] = members
        uae["_uae_consolidation_seal"] = utc_now()

    east = by_id.get(CLUSTER_EAST)
    if not east:
        east = {
            "cluster_id": CLUSTER_EAST,
            "cluster_label": "UAE East Coast (Gulf of Oman)",
            "region": "MENA",
            "type": "coastal",
            "anchor": [56.358394, 25.352343],
            "member_city_ids": ["fujairah-uae", "sharjah-uae"],
            "members_present": 2,
            "members_missing": [],
            "anchor_source": "bp-44685987bc",
            "_uae_consolidation_seal": utc_now(),
        }
        clusters.append(east)
        by_id[CLUSTER_EAST] = east
    else:
        east["member_city_ids"] = ["fujairah-uae", "sharjah-uae"]
        east["_uae_consolidation_seal"] = utc_now()

    if apply:
        clusters_doc["clusters"] = clusters
    return {
        "uae_members": uae.get("member_city_ids") if uae else [],
        "east_members": east.get("member_city_ids"),
        "east_added": CLUSTER_EAST not in by_id or east is by_id[CLUSTER_EAST],
    }


def vessel_and_render(dist_nm: float) -> tuple[str, str, str]:
    if dist_nm >= 70:
        return "Quanta-LR", "roadmap-amber-dashed", "roadmap"
    return "Pioneer II", "solid", "sealed"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write FEATURES_BY_TYPE, ROUTES, CLUSTERS")
    args = ap.parse_args()

    dc = ROOT / "data-clean"
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(dc / "ROUTES.json")
    routes = route_features(routes_raw)
    clusters_doc = load_json(dc / "CLUSTERS.json")
    mask = load_land_mask()

    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    hand_added = load_hand_waypoint_catalog()

    kept_scores, dropped = select_kept_bps(bp_idx)
    pairs = build_corridor_pairs(kept_scores, bp_idx)

    musandam = musandam_marquee_pair(kept_scores, bp_idx)
    if musandam:
        pairs.add(musandam)
        for pid in musandam:
            if pid not in kept_scores:
                kept_scores[pid] = hub_score(bp_idx[pid].get("name") or "")

    legacy_geom: dict[tuple[str, str], list] = {}
    removed_routes: list[dict] = []
    kept_routes: list[dict] = []
    for r in routes:
        if route_touches_uae(r, bp_idx):
            p = props(r)
            fn = p.get("from") or p.get("from_node")
            tn = p.get("to") or p.get("to_node")
            coords = r.get("geometry", {}).get("coordinates") or []
            if fn and tn and coords:
                legacy_geom[(fn, tn)] = coords
            removed_routes.append(
                {
                    "route_id": route_id_of(r),
                    "from": fn,
                    "to": tn,
                    "from_city_id": p.get("from_city_id"),
                    "to_city_id": p.get("to_city_id"),
                    "qb": is_qb_cross_border(r),
                }
            )
        else:
            kept_routes.append(r)

    minted: list[dict] = []
    failed: list[dict] = []
    land_flagged: list[dict] = []

    for a, b in sorted(pairs):
        if a not in bp_idx or b not in bp_idx:
            failed.append({"from": a, "to": b, "reason": "missing_bp"})
            continue
        geom = route_geometry(a, b, bp_idx, mask, legacy_geom)
        if not geom:
            failed.append({"from": a, "to": b, "reason": "no_geometry"})
            continue
        coords, land_km = geom
        ok, land_km = _qa_accept(coords)
        if not ok:
            failed.append(
                {
                    "from": a,
                    "to": b,
                    "reason": "land_crossing",
                    "land_km": land_km,
                    "from_label": bp_idx[a]["name"],
                    "to_label": bp_idx[b]["name"],
                }
            )
            continue

        from_city = bp_idx[a].get("parent_city_id")
        to_city = bp_idx[b].get("parent_city_id")
        rid = mint_route_id(a, b, tag="uae_consolidation")
        dist_nm = path_length_km(coords) * NM_PER_KM
        platform, render, link_status = vessel_and_render(dist_nm)
        cluster_id = cluster_for_pair(a, b, bp_idx)

        feat = make_route_feature(
            a,
            b,
            bp_idx[a]["name"],
            bp_idx[b]["name"],
            from_city,
            to_city,
            coords,
            cities,
            source="uae_consolidation",
            land_km=land_km,
        )
        p = props(feat)
        p["id"] = rid
        p["platform"] = platform
        p["distance_nm"] = round(dist_nm, 1)
        p["_render"] = render
        p["_link_status"] = link_status
        p["cluster_id"] = cluster_id
        p["_uae_consolidation_seal"] = utc_now()
        p["_geometry_source"] = "uae_hand_waypoints+coastal"
        p["_qa_land_flag"] = False
        p["_land_km_interior"] = round(land_km, 4)

        minted.append(feat)
        kept_routes.append(feat)

    used_bp_ids = set()
    for m in minted:
        p = props(m)
        used_bp_ids.add(p["from"])
        used_bp_ids.add(p["to"])

    poi_dropped = drop_dirty_pois(fbt, dropped, args.apply)
    orphan_dropped = drop_orphan_pois(fbt, used_bp_ids, args.apply)
    bp_cluster_counts = stamp_bp_clusters(fbt, bp_idx, args.apply)
    cluster_report = update_clusters(clusters_doc, args.apply)

    uae_route_land_flags = sum(1 for m in minted if props(m).get("_qa_land_flag"))

    receipt = {
        "generated_at": utc_now(),
        "seal_tag": SEAL_TAG,
        "apply": args.apply,
        "hand_waypoints_loaded": hand_added,
        "bp": {
            "before_uae": sum(1 for p in bp_idx.values() if p.get("parent_city_id") in UAE_CITIES),
            "kept_scores": len(kept_scores),
            "used_in_routes": len(used_bp_ids),
            "dropped_dirty": len(dropped),
            "dropped_from_fbt": poi_dropped,
            "orphan_dropped": orphan_dropped,
            "drop_reasons": dict(sorted(((v, sum(1 for x in dropped.values() if x == v)) for v in set(dropped.values())))),
            "cluster_assignment": bp_cluster_counts,
        },
        "routes": {
            "removed_uae_touching": len(removed_routes),
            "candidate_pairs": len(pairs),
            "minted": len(minted),
            "failed": failed,
            "failed_count": len(failed),
            "land_flags": uae_route_land_flags,
            "musandam_marquee": musandam,
        },
        "clusters": cluster_report,
    }

    if args.apply:
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        save_routes(dc / "ROUTES.json", kept_routes)
        save_json(dc / "CLUSTERS.json", clusters_doc)
        receipt["routes_after_total"] = len(kept_routes)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))

    print(
        f"\n{'✓' if args.apply else '·'} UAE consolidation: "
        f"BPs used={len(used_bp_ids)} routes={len(minted)} "
        f"land_flags={uae_route_land_flags} failed={len(failed)}"
    )

    if uae_route_land_flags > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())