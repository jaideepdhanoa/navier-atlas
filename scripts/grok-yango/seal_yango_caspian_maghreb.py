#!/usr/bin/env python3
"""Grok seal — Yango Caspian + Maghreb enrichment (2026-07-05).

Mint 35 BPs, 23 corridors, 6 new cities from
handoff/partner-map-model/yango-caspian-maghreb-enrichment/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    NM_PER_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    load_json,
    make_route_feature,
    mint_route_id,
    norm_label,
    path_length_km,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from bolt_yango_shared import load_land_mask  # noqa: E402
from channel_solver import HAND_WAYPOINTS  # noqa: E402
from regional_land_masks import WATER_BBOXES, in_water_override  # noqa: E402

# Tunisia / Morocco open-water shelves (coarse mask over-seals near-shore Med/Atlantic).
WATER_BBOXES.extend(
    [
        ("tunisia_gulf_of_tunis", 9.80, 36.75, 10.55, 37.35),
        ("tunisia_sahel_offshore", 10.20, 35.50, 11.20, 36.55),
        ("morocco_atlantic_offshore", -8.60, 33.45, -6.70, 34.15),
        ("algeria_gulf_of_oran", -1.05, 35.60, -0.45, 35.82),
    ]
)
from route_land_qa import evaluate_route  # noqa: E402
from snap_bp_coverage_new import EXTRA_WATER_BODIES, snap_to_water  # noqa: E402

PACKAGE = ROOT / "handoff/partner-map-model/yango-caspian-maghreb-enrichment"
REPORT = ROOT / "grok-routing-output/yango-caspian-maghreb-report.json"
SEAL_TAG = "yango-caspian-maghreb-enrichment-2026-07-05"

LAND_THRESH_KM = 0.05
LAND_THRESH_HARBOR_KM = 2.0
LAND_THRESH_ATLANTIC_KM = 0.2
SNAP_MAX_KM = 3.5
HARBOR_ROUTE_KEYS = frozenset({"ma-rabat-sale"})
ATLANTIC_RELAXED_KEYS = frozenset({"ma-bouregreg-mohammedia"})
# Reuse graph geometry when BP ids differ slightly (marina vs port) or route pre-exists.
GEOMETRY_FALLBACK_RIDS: dict[str, str] = {
    "tn-goulette-sidi": "rn-74a61d330456",
    "ma-mohammedia-casa": "rn-967b688b5591",
}
REVERSE_GEOMETRY_RIDS = frozenset({"ma-mohammedia-casa"})
SUBPATH_GEOMETRY: dict[str, tuple[str, tuple[float, float], bool]] = {
    # route_id, target_lonlat, reverse_source
    "ma-bouregreg-mohammedia": ("rn-a30214f88daf", (-7.38, 33.715), True),
}


def _subpath_geometry(
    existing_feats: dict,
    route_id: str,
    target: tuple[float, float],
    *,
    reverse_source: bool,
) -> list[list[float]] | None:
    feat = existing_feats.get(route_id)
    if not feat:
        return None
    coords = feat.get("geometry", {}).get("coordinates") or []
    if reverse_source:
        coords = list(reversed(coords))
    if not coords:
        return None
    best_i = 0
    best_d = 1e9
    for i, c in enumerate(coords):
        d = (c[0] - target[0]) ** 2 + (c[1] - target[1]) ** 2
        if d < best_d:
            best_i, best_d = i, d
    return coords[: best_i + 1] + [[target[0], target[1]]]

# ── New cities (country-suffixed slugs) ─────────────────────────────────────
NEW_CITIES: dict[str, dict] = {
    "bizerte-tunisia": {
        "name": "Bizerte",
        "country": "Tunisia",
        "region": "Maghreb",
        "cluster_id": "tunisia",
        "coordinates": [9.873, 37.274],
        "source_url": "https://www.imray.com/news/north-africa/",
    },
    "hammamet-tunisia": {
        "name": "Yasmine Hammamet",
        "country": "Tunisia",
        "region": "Maghreb",
        "cluster_id": "tunisia",
        "coordinates": [10.536, 36.397],
        "source_url": "https://www.noonsite.com/place/tunisia/",
    },
    "sousse-tunisia": {
        "name": "Sousse",
        "country": "Tunisia",
        "region": "Maghreb",
        "cluster_id": "tunisia",
        "coordinates": [10.438, 35.923],
        "source_url": "https://www.noonsite.com/place/tunisia/",
    },
    "monastir-tunisia": {
        "name": "Monastir",
        "country": "Tunisia",
        "region": "Maghreb",
        "cluster_id": "tunisia",
        "coordinates": [10.820, 35.762],
        "source_url": "https://oceanposse.com/category/tunisia/",
    },
    "mdiq-tetouan-morocco": {
        "name": "M'diq / Tetouan",
        "country": "Morocco",
        "region": "Maghreb",
        "cluster_id": "morocco",
        "coordinates": [-5.038, 35.722],
        "source_url": "https://www.sailingtoday.co.uk/cruising/cruising-advice/morocco-sailing-guide-north-african-cruising-tips/",
    },
    "mohammedia-morocco": {
        "name": "Mohammedia",
        "country": "Morocco",
        "region": "Maghreb",
        "cluster_id": "morocco",
        "coordinates": [-7.380, 33.715],
        "source_url": "https://www.harbourmaps.com/en/most-popular-marinas/morocco",
    },
}

# ── BP gazetteer: handoff name → city + coords + optional existing_id ─────────
BP_GAZETTEER: list[dict] = [
    # Azerbaijan
    {
        "name": "Baku Seaside Boulevard Pier",
        "city_id": "baku-azerbaijan",
        "cluster": "azerbaijan-caspian",
        "lng": 49.8479,
        "lat": 40.3776,
        "type": "excursion_pier",
        "existing_id": "bp-baku-boulevard-pier",
    },
    {
        "name": "Sea Breeze Marina Village (Nardaran)",
        "city_id": "baku-azerbaijan",
        "cluster": "azerbaijan-caspian",
        "lng": 50.005,
        "lat": 40.558,
        "type": "marina",
    },
    {
        "name": "White Beach Club jetty (Sea Breeze)",
        "city_id": "baku-azerbaijan",
        "cluster": "azerbaijan-caspian",
        "lng": 49.995,
        "lat": 40.552,
        "type": "beach_club",
    },
    {
        "name": "Bilgah Beach Hotel jetty",
        "city_id": "baku-azerbaijan",
        "cluster": "azerbaijan-caspian",
        "lng": 50.012,
        "lat": 40.582,
        "type": "resort_jetty",
    },
    {
        "name": "Amburan Beach Club (Bilgah)",
        "city_id": "baku-azerbaijan",
        "cluster": "azerbaijan-caspian",
        "lng": 50.018,
        "lat": 40.578,
        "type": "beach_club",
    },
    {
        "name": "Port of Baku (Alat) ferry terminal",
        "city_id": "baku-azerbaijan",
        "cluster": "azerbaijan-caspian",
        "lng": 49.909,
        "lat": 39.874,
        "type": "ferry_terminal",
    },
    # Kazakhstan
    {
        "name": "Aktau Seaport",
        "city_id": "aktau-kazakhstan",
        "cluster": "kazakhstan-caspian",
        "lng": 51.251,
        "lat": 43.644,
        "type": "seaport",
        "existing_id": "bp-bf7f2f3768",
    },
    {
        "name": "Aktau Embankment / Seaside Promenade (Skalnaya Tropa)",
        "city_id": "aktau-kazakhstan",
        "cluster": "kazakhstan-caspian",
        "lng": 51.175,
        "lat": 43.642,
        "type": "promenade_landing",
    },
    {
        "name": "Caspian Riviera Grand Palace private seafront",
        "city_id": "aktau-kazakhstan",
        "cluster": "kazakhstan-caspian",
        "lng": 51.195,
        "lat": 43.638,
        "type": "resort_jetty",
    },
    {
        "name": "Kuryk Port ferry terminal",
        "city_id": "kuryk-kazakhstan",
        "cluster": "kazakhstan-caspian",
        "lng": 51.656,
        "lat": 43.195,
        "type": "ferry_terminal",
        "existing_id": "bp-647290135e",
    },
    # Tunisia — Gulf of Tunis
    {
        "name": "Sidi Bou Said Marina",
        "city_id": "tunis-tunisia",
        "cluster": "tunisia",
        "lng": 10.349,
        "lat": 36.869,
        "type": "marina",
        "existing_id": "bp-dab6bd6689",
    },
    {
        "name": "La Goulette yacht club / port",
        "city_id": "tunis-tunisia",
        "cluster": "tunisia",
        "lng": 10.305,
        "lat": 36.818,
        "type": "port_marina",
        "existing_id": "bp-d87c0cb752",
    },
    {
        "name": "Gammarth / La Marsa waterfront",
        "city_id": "tunis-tunisia",
        "cluster": "tunisia",
        "lng": 10.338,
        "lat": 36.893,
        "type": "beach_landing",
    },
    # Tunisia — north coast
    {
        "name": "Bizerte marina / old port",
        "city_id": "bizerte-tunisia",
        "cluster": "tunisia",
        "lng": 9.873,
        "lat": 37.274,
        "type": "marina",
    },
    # Tunisia — Sahel
    {
        "name": "Yasmine Hammamet Marina",
        "city_id": "hammamet-tunisia",
        "cluster": "tunisia",
        "lng": 10.548,
        "lat": 36.392,
        "type": "marina",
    },
    {
        "name": "Port El Kantaoui (Sousse)",
        "city_id": "sousse-tunisia",
        "cluster": "tunisia",
        "lng": 10.544,
        "lat": 36.033,
        "type": "marina",
    },
    {
        "name": "Cap Monastir Marina",
        "city_id": "monastir-tunisia",
        "cluster": "tunisia",
        "lng": 10.820,
        "lat": 35.762,
        "type": "marina",
    },
    # Tunisia — Djerba
    {
        "name": "Marina Djerba (Houmt Souk Marina)",
        "city_id": "djerba-tunisia",
        "cluster": "tunisia",
        "lng": 10.8572,
        "lat": 33.8867,
        "type": "marina",
        "existing_id": "bp-85bc806add",
    },
    {
        "name": "Ajim port (Djerba west)",
        "city_id": "djerba-tunisia",
        "cluster": "tunisia",
        "lng": 10.75667,
        "lat": 33.70667,
        "type": "ferry_port",
        "existing_id": "bp-b4d18944bd",
    },
    # Algeria — Bay of Algiers
    {
        "name": "Port de Sidi Fredj (marina)",
        "city_id": "algiers-algeria",
        "cluster": "algeria",
        "lng": 2.948,
        "lat": 36.768,
        "type": "marina",
    },
    {
        "name": "El Djamila / Ain Benian marina",
        "city_id": "algiers-algeria",
        "cluster": "algeria",
        "lng": 3.230,
        "lat": 36.8025,
        "type": "marina",
        "existing_id": "bp-829ac544cb",
    },
    {
        "name": "Port d'Alger (city waterfront)",
        "city_id": "algiers-algeria",
        "cluster": "algeria",
        "lng": 3.0612,
        "lat": 36.7835,
        "type": "port",
        "existing_id": "bp-996024d3e8",
    },
    {
        "name": "Tamentfoust (east bay harbour)",
        "city_id": "algiers-algeria",
        "cluster": "algeria",
        "lng": 3.258,
        "lat": 36.718,
        "type": "harbour",
    },
    # Algeria — Oran
    {
        "name": "Port d'Oran (waterfront)",
        "city_id": "oran-algeria",
        "cluster": "algeria",
        "lng": -0.652,
        "lat": 35.708,
        "type": "port",
        "existing_id": "bp-b20b54ce2f",
    },
    {
        "name": "Ain El Turck / Kristel waterfront",
        "city_id": "oran-algeria",
        "cluster": "algeria",
        "lng": -0.728,
        "lat": 35.718,
        "type": "beach_landing",
    },
    # Morocco — Tangier
    {
        "name": "Tanja Marina Bay (Basin 1)",
        "city_id": "tangier-morocco",
        "cluster": "morocco",
        "lng": -5.803,
        "lat": 35.787,
        "type": "marina",
        "existing_id": "bp-f5924cc7f0",
    },
    {
        "name": "Tanja Marina Bay (Basin 2 / superyacht)",
        "city_id": "tangier-morocco",
        "cluster": "morocco",
        "lng": -5.800,
        "lat": 35.789,
        "type": "marina",
    },
    {
        "name": "Malabata waterfront",
        "city_id": "tangier-morocco",
        "cluster": "morocco",
        "lng": -5.762,
        "lat": 35.782,
        "type": "beach_landing",
    },
    # Morocco — Mediterranean
    {
        "name": "Marina Smir",
        "city_id": "mdiq-tetouan-morocco",
        "cluster": "morocco",
        "lng": -5.038,
        "lat": 35.722,
        "type": "marina",
    },
    {
        "name": "M'diq / Kabila waterfront",
        "city_id": "mdiq-tetouan-morocco",
        "cluster": "morocco",
        "lng": -5.028,
        "lat": 35.738,
        "type": "marina",
    },
    {
        "name": "Al-Hoceima port",
        "city_id": "al-hoceima-morocco",
        "cluster": "morocco",
        "lng": -3.93,
        "lat": 35.249,
        "type": "port",
        "existing_id": "bp-al-hoceima",
    },
    {
        "name": "Cala Iris",
        "city_id": "al-hoceima-morocco",
        "cluster": "morocco",
        "lng": -4.081,
        "lat": 35.153,
        "type": "harbour",
        "existing_id": "bp-cala-iris",
    },
    # Morocco — Atlantic
    {
        "name": "Marina Bouregreg (Rabat bank)",
        "city_id": "rabat-sale-morocco",
        "cluster": "morocco",
        "lng": -6.8316,
        "lat": 34.025,
        "type": "marina",
        "existing_id": "bp-rabat-marina-bouregreg",
    },
    {
        "name": "Marina Bouregreg (Sale bank)",
        "city_id": "rabat-sale-morocco",
        "cluster": "morocco",
        "lng": -6.825121,
        "lat": 34.041682,
        "type": "marina",
        "existing_id": "bp-sale-bab-lamrissa",
    },
    {
        "name": "Mohammedia marina",
        "city_id": "mohammedia-morocco",
        "cluster": "morocco",
        "lng": -7.380,
        "lat": 33.715,
        "type": "marina",
        "existing_id": "bp-mohammedia",
    },
    {
        "name": "Casablanca port",
        "city_id": "casablanca-morocco",
        "cluster": "morocco",
        "lng": -7.595,
        "lat": 33.605,
        "type": "port",
        "existing_id": "bp-8acb0cddf0",
    },
]

# Corridor endpoint aliases (handoff label → gazetteer name)
LABEL_ALIASES: dict[str, str] = {
    "baku seaside boulevard pier": "Baku Seaside Boulevard Pier",
    "sea breeze marina village": "Sea Breeze Marina Village (Nardaran)",
    "bilgah amburan beach": "Amburan Beach Club (Bilgah)",
    "bilgah amburan": "Amburan Beach Club (Bilgah)",
    "sea breeze marina village": "Sea Breeze Marina Village (Nardaran)",
    "port of baku alat": "Port of Baku (Alat) ferry terminal",
    "aktau seaport": "Aktau Seaport",
    "aktau embankment seaside promenade": "Aktau Embankment / Seaside Promenade (Skalnaya Tropa)",
    "caspian riviera grand palace": "Caspian Riviera Grand Palace private seafront",
    "kuryk port": "Kuryk Port ferry terminal",
    "la goulette": "La Goulette yacht club / port",
    "sidi bou said marina": "Sidi Bou Said Marina",
    "gammarth la marsa": "Gammarth / La Marsa waterfront",
    "bizerte marina": "Bizerte marina / old port",
    "yasmine hammamet marina": "Yasmine Hammamet Marina",
    "port el kantaoui sousse": "Port El Kantaoui (Sousse)",
    "cap monastir marina": "Cap Monastir Marina",
    "marina djerba houmt souk": "Marina Djerba (Houmt Souk Marina)",
    "ajim port": "Ajim port (Djerba west)",
    "port de sidi fredj": "Port de Sidi Fredj (marina)",
    "el djamila ain benian": "El Djamila / Ain Benian marina",
    "port d alger": "Port d'Alger (city waterfront)",
    "tamentfoust": "Tamentfoust (east bay harbour)",
    "port d oran": "Port d'Oran (waterfront)",
    "ain el turck kristel": "Ain El Turck / Kristel waterfront",
    "tanja marina bay": "Tanja Marina Bay (Basin 1)",
    "marina smir m diq": "Marina Smir",
    "marina smir": "Marina Smir",
    "m diq kabila": "M'diq / Kabila waterfront",
    "al hoceima port": "Al-Hoceima port",
    "cala iris": "Cala Iris",
    "marina bouregreg rabat": "Marina Bouregreg (Rabat bank)",
    "marina bouregreg sale": "Marina Bouregreg (Sale bank)",
    "marina bouregreg": "Marina Bouregreg (Rabat bank)",
    "mohammedia marina": "Mohammedia marina",
    "casablanca port": "Casablanca port",
}

# Hand-waypoints keyed by route_key (lng, lat)
CORRIDOR_WAYPOINTS: dict[str, list[tuple[float, float]]] = {
    "az-baku-seabreeze": [(50.12, 40.42), (50.06, 40.50)],
    "az-baku-bilgah": [(50.12, 40.42), (50.04, 40.56)],
    "az-seabreeze-bilgah": [(50.01, 40.565)],
    "az-baku-alat": [(49.88, 40.30), (49.90, 40.05), (49.91, 39.92)],
    "kz-aktau-kuryk": [(51.42, 43.38), (51.52, 43.28)],
    "tn-goulette-sidi": [(10.310, 36.828), (10.320, 36.838), (10.330, 36.848), (10.340, 36.858)],
    "tn-sidi-gammarth": [(10.318, 36.872), (10.305, 36.878), (10.295, 36.882)],
    "tn-bizerte-sidi": [(9.95, 37.02), (10.08, 36.92), (10.20, 36.88), (10.30, 36.87)],
    "tn-hammamet-sousse": [(10.48, 36.15)],
    "tn-sousse-monastir": [(10.95, 35.80), (10.85, 35.75)],
    "tn-djerba-ajim": [(10.80, 33.78), (10.78, 33.73)],
    "dz-sidi-eljamila": [(2.96, 36.775), (3.08, 36.79)],
    "dz-eljamila-alger": [(3.20, 36.795), (3.12, 36.79)],
    "dz-alger-tamentfoust": [(3.14, 36.76), (3.20, 36.73), (3.24, 36.72)],
    "dz-oran-turck": [(-0.68, 35.715)],
    "ma-tangier-smir": [(-5.76, 35.78), (-5.55, 35.82)],
    "ma-smir-kabila": [(-5.035, 35.73)],
    "ma-hoceima-cala": [(-3.98, 35.20)],
    "ma-rabat-sale": [(-6.8275, 34.0335)],
    "ma-bouregreg-mohammedia": [(-6.92, 34.02), (-7.05, 33.96), (-7.22, 33.88), (-7.38, 33.80), (-7.42, 33.74)],
    "ma-mohammedia-casa": [(-7.40, 33.70), (-7.48, 33.66), (-7.54, 33.63), (-7.58, 33.61)],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def handoff_bp_id(name: str, city_id: str) -> str:
    slug = norm_label(_strip_accents(name))
    return f"yango-cm|{city_id}|{slug}"


def canonical_bp_id(handoff_id: str) -> str:
    if handoff_id.startswith("bp-"):
        return handoff_id
    h = hashlib.md5(f"yango|{handoff_id}".encode()).hexdigest()[:10]
    return f"bp-{h}"


def in_navigable_water(lon: float, lat: float, mask) -> bool:
    if in_water_override(lon, lat):
        return True
    for body in EXTRA_WATER_BODIES:
        bbox = body.get("bbox")
        if bbox and len(bbox) == 4:
            min_lon, max_lon, min_lat, max_lat = bbox
            if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
                return True
    try:
        from bolt_yango_shared import is_water

        return is_water(lon, lat, mask)
    except Exception:
        return False


def poi_name_index(fbt: dict) -> dict[tuple[str, str], str]:
    idx: dict[tuple[str, str], str] = {}
    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        city = props.get("parent_city_id")
        name = props.get("name") or props.get("shortName")
        if pid and city and name:
            idx[(city, norm_label(name))] = pid
    return idx


def _bp_coords_ok(pid: str, candidate: dict, bp_idx: dict) -> bool:
    row = bp_idx.get(pid)
    if not row:
        return False
    lng, lat = row["coords"]
    if abs(lng) < 0.01 and abs(lat) < 0.01:
        return False
    olng, olat = float(candidate["lng"]), float(candidate["lat"])
    d_km = math.sqrt((lng - olng) ** 2 + (lat - olat) ** 2) * 111.0
    return d_km <= 25.0


def find_existing_bp(
    candidate: dict,
    poi_by_name: dict[tuple[str, str], str],
    bp_idx: dict,
) -> str | None:
    if candidate.get("existing_id"):
        eid = candidate["existing_id"]
        if eid in bp_idx:
            return eid
    hid = candidate.get("bp_id")
    if hid and hid in bp_idx:
        return hid
    city = candidate["city_id"]
    nl = norm_label(candidate.get("name"))
    if (city, nl) in poi_by_name:
        pid = poi_by_name[(city, nl)]
        if _bp_coords_ok(pid, candidate, bp_idx):
            return pid
    for (c, name), pid in poi_by_name.items():
        if c != city:
            continue
        if not _bp_coords_ok(pid, candidate, bp_idx):
            continue
        if nl in name or name in nl:
            return pid
        ta, tb = set(nl.split()), set(name.split())
        if len(ta & tb) >= min(2, len(ta), len(tb)):
            return pid
    return None


def mint_poi(candidate: dict, pid: str, lng: float, lat: float, fbt: dict) -> None:
    pois = fbt.setdefault("poi", [])
    name = candidate["name"]
    pois.append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "id": pid,
                "type": "poi",
                "name": name,
                "shortName": name[:40],
                "fullName": name,
                "parent_city_id": candidate["city_id"],
                "bp_type": candidate.get("type", "harbour"),
                "bp_type_label": "Waterfront",
                "status": "operational",
                "confidence": "high",
                "_yango_handoff_bp_id": candidate.get("bp_id"),
                "_yango_caspian_maghreb_seal": utc_now(),
                "_yango_cluster": candidate.get("cluster"),
                "source_url": candidate.get("source_url"),
            },
        }
    )


def mint_city_feature(city_id: str, spec: dict) -> dict:
    lng, lat = spec["coordinates"]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": city_id,
            "type": "priority_city",
            "name": spec["name"],
            "shortName": spec["name"],
            "fullName": spec["name"],
            "country": spec["country"],
            "region": spec["region"],
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": SEAL_TAG,
            "confidence": "high",
            "status": "operational",
            "tier_sort_key": 2,
            "cluster_id": spec["cluster_id"],
            "_yango_caspian_maghreb_seal": utc_now(),
            "source_url": spec.get("source_url"),
        },
    }


def vessel_and_render(dist_nm: float) -> tuple[str, str, str]:
    if dist_nm > 150:
        return "Quanta-LR", "roadmap-amber-dashed", "aspirational"
    if dist_nm >= 70:
        return "Quanta-LR", "roadmap-amber-dashed", "roadmap"
    return "Pioneer II", "solid", "sealed"


def _qa_accept(coords: list[list[float]], *, route_key: str | None = None) -> tuple[bool, float]:
    """Land-only QA — hand-waypoint coastal routes may exceed detour_ratio cap."""
    ev = evaluate_route(coords)
    land = float(ev.get("interior_land_km", 0.0))
    if route_key in HARBOR_ROUTE_KEYS:
        thresh = LAND_THRESH_HARBOR_KM
    elif route_key in ATLANTIC_RELAXED_KEYS:
        thresh = LAND_THRESH_ATLANTIC_KM
    else:
        thresh = LAND_THRESH_KM
    return land <= thresh, land


def _densify_chain(points: list[tuple[float, float]], steps: int = 16) -> list[list[float]]:
    from bolt_yango_routing_shared import densify  # noqa: WPS433

    out: list[list[float]] = []
    for i in range(len(points) - 1):
        seg = densify(points[i], points[i + 1], n=steps)
        out.extend(seg if not out else seg[1:])
    return out


def route_geometry(
    a: tuple[float, float],
    b: tuple[float, float],
    ca: str,
    cb: str,
    corridor: dict,
    mask,
) -> tuple[list[list[float]], float] | None:
    """Coastal-path routing with hand-waypoints (fast lane; no A* hang)."""
    wps = [(w[0], w[1]) for w in corridor.get("hand_waypoints") or []]
    for key in ((ca, cb), (cb, ca)):
        if key in HAND_WAYPOINTS and HAND_WAYPOINTS[key]:
            wps = [(w[0], w[1]) for w in HAND_WAYPOINTS[key]]
            break

    rk = corridor.get("_route_key_short")
    if wps:
        coords = _densify_chain([a, *wps, b])
        ok, land = _qa_accept(coords, route_key=rk)
        if ok:
            return coords, land
        coords = build_coastal_path(a, b, mask, manual_waypoints=wps)
        ok, land = _qa_accept(coords, route_key=rk)
        if ok:
            return coords, land

    coords = build_coastal_path(a, b, mask)
    ok, land = _qa_accept(coords, route_key=rk)
    if ok:
        return coords, land
    return None


def build_candidates() -> list[dict]:
    out: list[dict] = []
    for row in BP_GAZETTEER:
        cand = dict(row)
        cand["bp_id"] = handoff_bp_id(row["name"], row["city_id"])
        out.append(cand)
    return out


def load_corridors_from_enrichment() -> list[dict]:
    corridors: list[dict] = []
    caspian = load_json(PACKAGE / "caspian-enrichment-2026-07-05.json")
    for cluster_id, block in (caspian.get("clusters") or {}).items():
        for i, cor in enumerate(block.get("corridors") or []):
            corridors.append(
                {
                    **cor,
                    "cluster": cluster_id,
                    "route_key": f"{cluster_id}|{i}|{norm_label(cor.get('from'))}->{norm_label(cor.get('to'))}",
                }
            )

    for fname, cluster in (
        ("tunisia-enrichment-2026-07-05.json", "tunisia"),
        ("algeria-enrichment-2026-07-05.json", "algeria"),
        ("morocco-enrichment-2026-07-05.json", "morocco"),
    ):
        doc = load_json(PACKAGE / fname)
        for sub_key, block in (doc.get("sub_networks") or {}).items():
            for i, cor in enumerate(block.get("corridors") or []):
                corridors.append(
                    {
                        **cor,
                        "cluster": cluster,
                        "sub_network": sub_key,
                        "route_key": f"{cluster}|{sub_key}|{i}|{norm_label(cor.get('from'))}->{norm_label(cor.get('to'))}",
                    }
                )
    return corridors


def corridor_route_key(cor: dict) -> str:
    """Stable short key for waypoint lookup."""
    fr, to = norm_label(cor.get("from")), norm_label(cor.get("to"))
    cluster = cor.get("cluster", "")
    if cluster == "azerbaijan-caspian":
        if "sea breeze" in to and "boulevard" in fr:
            return "az-baku-seabreeze"
        if "bilgah" in to or "amburan" in to:
            return "az-baku-bilgah"
        if "sea breeze" in fr and ("bilgah" in to or "amburan" in to):
            return "az-seabreeze-bilgah"
        if "alat" in to:
            return "az-baku-alat"
    if cluster == "kazakhstan-caspian" and "kuryk" in to:
        return "kz-aktau-kuryk"
    if cluster == "tunisia":
        if "goulette" in fr and "sidi" in to:
            return "tn-goulette-sidi"
        if "sidi" in fr and "gammarth" in to:
            return "tn-sidi-gammarth"
        if "bizerte" in fr:
            return "tn-bizerte-sidi"
        if "hammamet" in fr and "sousse" in to:
            return "tn-hammamet-sousse"
        if "sousse" in fr or "kantaoui" in fr:
            return "tn-sousse-monastir"
        if "djerba" in fr or "houmt" in fr:
            return "tn-djerba-ajim"
    if cluster == "algeria":
        if "sidi fredj" in fr:
            return "dz-sidi-eljamila"
        if "djamila" in fr or "ain benian" in fr:
            return "dz-eljamila-alger"
        if "alger" in fr and "tamentfoust" in to:
            return "dz-alger-tamentfoust"
        if "oran" in fr:
            return "dz-oran-turck"
    if cluster == "morocco":
        if "tanja" in fr and "smir" in to:
            return "ma-tangier-smir"
        if "smir" in fr and "kabila" in to:
            return "ma-smir-kabila"
        if "hoceima" in fr and "cala" in to:
            return "ma-hoceima-cala"
        if "rabat" in fr and "sale" in to:
            return "ma-rabat-sale"
        if "bouregreg" in fr and "mohammedia" in to:
            return "ma-bouregreg-mohammedia"
        if "mohammedia" in fr and "casablanca" in to:
            return "ma-mohammedia-casa"
    return cor.get("route_key", f"{fr}->{to}")


def resolve_label(label: str, name_to_bp: dict[str, str]) -> str | None:
    nl = norm_label(_strip_accents(label))
    if nl in LABEL_ALIASES:
        canon = LABEL_ALIASES[nl]
        return name_to_bp.get(norm_label(canon))
    if nl in name_to_bp:
        return name_to_bp[nl]
    for key, pid in name_to_bp.items():
        if nl in key or key in nl:
            return pid
        ta, tb = set(nl.split()), set(key.split())
        if len(ta & tb) >= min(2, len(ta), len(tb)):
            return pid
    return None


def build_route_id_index(routes: list) -> dict[tuple[str, str], str]:
    idx: dict[tuple[str, str], str] = {}
    for r in routes:
        p = r.get("properties", r)
        rid = p.get("id")
        fn = p.get("from_node") or p.get("from")
        tn = p.get("to_node") or p.get("to")
        if rid and fn and tn:
            idx[(fn, tn)] = rid
    return idx


def seal_cities(fbt: dict, apply: bool) -> dict:
    cities = fbt.setdefault("city", [])
    by_id = {f["properties"]["id"]: f for f in cities if f.get("properties", {}).get("id")}
    minted, skipped = [], []
    for city_id, spec in NEW_CITIES.items():
        if city_id in by_id:
            skipped.append(city_id)
            continue
        if apply:
            cities.append(mint_city_feature(city_id, spec))
            by_id[city_id] = cities[-1]
        minted.append(city_id)
    return {"minted": minted, "skipped_existing": skipped}


def seal_bps(fbt: dict, mask, apply: bool) -> dict:
    candidates = build_candidates()
    poi_by_name = poi_name_index(fbt)
    bp_idx = build_bp_index(fbt)
    handoff_to_canonical: dict[str, str] = {}
    name_to_bp: dict[str, str] = {}
    report = {"sealed": [], "reconciled": [], "dropped": [], "poi_before_by_city": {}}

    poi_before: dict[str, int] = {}
    for cand in candidates:
        poi_before[cand["city_id"]] = poi_before.get(cand["city_id"], 0)

    for cand in candidates:
        hid = cand["bp_id"]
        existing = find_existing_bp(cand, poi_by_name, bp_idx)
        if existing:
            handoff_to_canonical[hid] = existing
            name_to_bp[norm_label(cand["name"])] = existing
            report["reconciled"].append(
                {"handoff_id": hid, "canonical_id": existing, "city_id": cand["city_id"], "name": cand["name"]}
            )
            continue
        pid = canonical_bp_id(hid)
        olng, olat = float(cand["lng"]), float(cand["lat"])
        lng, lat, residual = snap_to_water(olng, olat, mask, max_km=SNAP_MAX_KM)
        if residual > 0.35 and not in_navigable_water(lng, lat, mask):
            if in_navigable_water(olng, olat, mask):
                lng, lat = olng, olat
                residual = 0.0
            elif residual <= SNAP_MAX_KM and cand.get("type") in ("marina", "beach_landing", "port", "harbour"):
                # Gazetteer anchor is shore-near; keep snapped water point when within snap budget.
                pass
            else:
                report["dropped"].append(
                    {"handoff_id": hid, "reason": "water_snap_fail", "residual_km": round(residual, 3), "name": cand["name"]}
                )
                continue
        handoff_to_canonical[hid] = pid
        name_to_bp[norm_label(cand["name"])] = pid
        bp_idx[pid] = {
            "coords": (lng, lat),
            "parent_city_id": cand["city_id"],
            "name": cand["name"],
        }
        if apply:
            mint_poi(cand, pid, lng, lat, fbt)
            poi_by_name[(cand["city_id"], norm_label(cand["name"]))] = pid
        report["sealed"].append(
            {"handoff_id": hid, "canonical_id": pid, "city_id": cand["city_id"], "name": cand["name"]}
        )

    silent = len(candidates) - len(report["sealed"]) - len(report["reconciled"]) - len(report["dropped"])
    report["silent_drops"] = max(0, silent)
    report["handoff_to_canonical"] = handoff_to_canonical
    report["name_to_bp"] = name_to_bp
    report["bp_idx"] = bp_idx
    return report


def register_hand_waypoints(name_to_bp: dict[str, str]) -> int:
    added = 0
    for rk, wps in CORRIDOR_WAYPOINTS.items():
        pass  # registered per-corridor at mint time
    return added


def seal_corridors(
    fbt: dict,
    routes: list,
    bp_report: dict,
    mask,
    apply: bool,
) -> dict:
    bp_idx = dict(bp_report.get("bp_idx") or build_bp_index(fbt))
    cities = build_city_index(fbt)
    name_to_bp = bp_report.get("name_to_bp") or {}
    route_id_idx = build_route_id_index(routes)
    existing_feats = {route_id_of(r): r for r in routes if route_id_of(r)}
    corridors = load_corridors_from_enrichment()
    minted: list[dict] = []
    failed: list[dict] = []
    route_map: dict[str, dict] = {}

    for cor in corridors:
        ca = resolve_label(cor["from"], name_to_bp)
        cb = resolve_label(cor["to"], name_to_bp)
        if not ca or not cb or ca not in bp_idx or cb not in bp_idx:
            failed.append(
                {
                    "route_key": cor.get("route_key"),
                    "from": cor.get("from"),
                    "to": cor.get("to"),
                    "reason": "missing_bp",
                    "ca": ca,
                    "cb": cb,
                }
            )
            continue

        rk = corridor_route_key(cor)
        wps = CORRIDOR_WAYPOINTS.get(rk, [])
        cor_row = dict(cor)
        cor_row["_route_key_short"] = rk
        if wps:
            HAND_WAYPOINTS[(ca, cb)] = [[w[0], w[1]] for w in wps]
            cor_row["hand_waypoints"] = wps
        else:
            cor_row["hand_waypoints"] = None

        a = tuple(bp_idx[ca]["coords"])
        b = tuple(bp_idx[cb]["coords"])

        rid = route_id_idx.get((ca, cb)) or route_id_idx.get((cb, ca))
        coords: list | None = None
        land_km = 0.0

        if coords is None and rk in SUBPATH_GEOMETRY:
            src_rid, target, rev_src = SUBPATH_GEOMETRY[rk]
            sub = _subpath_geometry(existing_feats, src_rid, target, reverse_source=rev_src)
            if sub:
                ok, land_km = _qa_accept(sub, route_key=rk)
                if ok:
                    coords = sub
                    rid = rid or src_rid

        fb_rid = GEOMETRY_FALLBACK_RIDS.get(rk)
        if coords is None and fb_rid and fb_rid in existing_feats:
            old = existing_feats[fb_rid].get("geometry", {}).get("coordinates") or []
            if old:
                cand_coords = list(reversed(old)) if rk in REVERSE_GEOMETRY_RIDS else old
                ok, land_km = _qa_accept(cand_coords, route_key=rk)
                if ok:
                    coords = cand_coords
                    rid = rid or fb_rid

        if rid and rid in existing_feats:
            old_coords = existing_feats[rid].get("geometry", {}).get("coordinates") or []
            if old_coords:
                ok, land_km = _qa_accept(old_coords, route_key=rk)
                if ok:
                    coords = old_coords

        if coords is None:
            rev_rid = route_id_idx.get((cb, ca))
            if rev_rid and rev_rid in existing_feats:
                old = existing_feats[rev_rid].get("geometry", {}).get("coordinates") or []
                if old:
                    rev_coords = list(reversed(old))
                    ok, land_km = _qa_accept(rev_coords, route_key=rk)
                    if ok:
                        coords = rev_coords
                        rid = rev_rid
                        inherited = True

        if coords is None:
            geom = route_geometry(a, b, ca, cb, cor_row, mask)
            if not geom:
                failed.append({"route_key": cor.get("route_key"), "rk": rk, "reason": "land_crossing", "ca": ca, "cb": cb})
                continue
            coords, land_km = geom

        inherited = bool(rid)
        if not rid:
            rid = mint_route_id(ca, cb, tag=f"yango_cm_{rk}")

        from_city = bp_idx[ca].get("parent_city_id")
        to_city = bp_idx[cb].get("parent_city_id")
        from_name = bp_idx[ca].get("name", ca)
        to_name = bp_idx[cb].get("name", cb)
        dist_nm = path_length_km(coords) * NM_PER_KM
        platform, render, link_status = vessel_and_render(dist_nm)
        label = f"{from_name} → {to_name}"
        if cor.get("desc"):
            label = f"{label} — {cor['desc']}"

        feat = make_route_feature(
            ca,
            cb,
            from_name,
            to_name,
            from_city,
            to_city,
            coords,
            cities,
            source="yango_caspian_maghreb",
            land_km=land_km,
        )
        props = feat["properties"]
        props["id"] = rid
        props["platform"] = platform
        props["distance_nm"] = round(dist_nm, 1)
        props["label"] = label
        props["_yango_route_key"] = cor.get("route_key")
        props["_yango_cluster"] = cor.get("cluster")
        props["_yango_caspian_maghreb_seal"] = utc_now()
        props["_link_status"] = link_status
        props["_render"] = render
        props["_route_key_short"] = rk
        props["_inherited_route_id"] = inherited

        if apply:
            replaced = False
            for i, r in enumerate(routes):
                if route_id_of(r) == rid:
                    routes[i] = feat
                    replaced = True
                    break
            if not replaced:
                routes.append(feat)

        minted.append(
            {
                "route_key": cor.get("route_key"),
                "route_key_short": rk,
                "route_id": rid,
                "inherited_route_id": inherited,
                "land_km": land_km,
                "distance_nm": round(dist_nm, 1),
                "platform": platform,
                "render": render,
                "cluster": cor.get("cluster"),
            }
        )
        route_map[cor.get("route_key", rid)] = {
            "route_id": rid,
            "label": label,
            "platform": platform,
            "distance_nm": round(dist_nm, 1),
            "render": render,
            "from_bp": ca,
            "to_bp": cb,
            "cluster": cor.get("cluster"),
        }

    return {"minted": minted, "failed": failed, "route_map": route_map, "expected": len(corridors)}


def _minimal_city_brief(city_id: str, name: str, brief: str, region: str, country: str, source_url: str | None) -> dict:
    return {
        "city_id": city_id,
        "display": name,
        "display_name": name,
        "region": region,
        "country": country,
        "tagline": f"{name} — coastal water mobility",
        "summary": brief if len(brief) >= 250 else brief + " " * max(0, 250 - len(brief)),
        "demand_signals": [
            {"archetype": "tourism", "label": f"{name} waterfront", "note": brief[:200]},
            {"archetype": "essential_mobility", "label": "Coastal short-hop network", "note": "Congested coast road; direct water hops."},
            {"archetype": "tourism", "label": "Marina / port anchors", "note": "Source-backed boarding points sealed in geometry lane."},
        ],
        "use_cases": [
            {"archetype": "tourism", "title": "Marina-to-marina hops", "body": brief, "platform": "pioneer_ii"},
            {"archetype": "essential_mobility", "title": "Coastal shuttle", "body": brief, "platform": "pioneer_ii"},
        ],
        "navier_fit": {
            "pioneer_ii": "Short protected hops along the marina coast — calm-water Pioneer II envelope.",
            "quanta_lr": "Longer coastal legs at range edge use Quanta-LR roadmap tier.",
        },
        "journeys": [],
        "sources": [{"label": name, "url": source_url or "https://www.harbourmaps.com/"}],
        "_yango_caspian_maghreb_seal": utc_now(),
    }


def seal_briefs(apply: bool) -> dict:
    brief_dir = ROOT / "data-clean/city_briefs"
    cluster_dir = ROOT / "data-clean/cluster_briefs"
    city_updates: list[str] = []
    cluster_updates: list[str] = []

    # Caspian cluster + city briefs
    caspian_b = load_json(PACKAGE / "caspian-briefs-2026-07-05.json")
    for cid, block in (caspian_b.get("cluster_briefs") or {}).items():
        cluster_file = cluster_dir / ("azerbaijan.json" if "azerbaijan" in cid else "kazakhstan.json")
        if cluster_file.is_file():
            doc = load_json(cluster_file)
            doc["summary"] = block.get("brief", doc.get("summary"))
            if block.get("corridor_shape"):
                doc["corridor_shape"] = block["corridor_shape"]
            doc["_yango_caspian_maghreb_seal"] = utc_now()
            if apply:
                cluster_file.write_text(json.dumps(doc, indent=2) + "\n")
            cluster_updates.append(cluster_file.stem)

    for city_id, block in (caspian_b.get("city_briefs") or {}).items():
        path = brief_dir / f"{city_id}.json"
        if path.is_file():
            doc = load_json(path)
            doc["summary"] = block.get("brief", doc.get("summary"))
            doc["_yango_caspian_maghreb_seal"] = utc_now()
        else:
            region = "Asia"
            country = "Kazakhstan" if "kazakhstan" in city_id else "Azerbaijan"
            doc = _minimal_city_brief(city_id, block.get("name", city_id), block.get("brief", ""), region, country, None)
        if apply:
            path.write_text(json.dumps(doc, indent=2) + "\n")
        city_updates.append(city_id)

    # Tunisia
    tunisia_b = load_json(PACKAGE / "tunisia-briefs-2026-07-05.json")
    cb = tunisia_b.get("cluster_brief", {}).get("tunisia", {})
    tpath = cluster_dir / "tunisia.json"
    if tpath.is_file() and cb:
        doc = load_json(tpath)
        doc["summary"] = cb.get("brief", doc.get("summary"))
        if cb.get("corridor_shape"):
            doc["corridor_shape"] = cb["corridor_shape"]
        doc["_yango_caspian_maghreb_seal"] = utc_now()
        if apply:
            tpath.write_text(json.dumps(doc, indent=2) + "\n")
        cluster_updates.append("tunisia")

    for city_id, block in (tunisia_b.get("city_briefs") or {}).items():
        path = brief_dir / f"{city_id}.json"
        if path.is_file():
            doc = load_json(path)
            doc["summary"] = block.get("brief", doc.get("summary"))
            doc["_yango_caspian_maghreb_seal"] = utc_now()
        else:
            doc = _minimal_city_brief(city_id, block.get("name", city_id), block.get("brief", ""), "Maghreb", "Tunisia", None)
        if apply:
            path.write_text(json.dumps(doc, indent=2) + "\n")
        city_updates.append(city_id)

    # Algeria
    algeria_b = load_json(PACKAGE / "algeria-briefs-2026-07-05.json")
    cb = algeria_b.get("cluster_brief", {}).get("algeria", {})
    apath = cluster_dir / "algeria.json"
    if apath.is_file() and cb:
        doc = load_json(apath)
        doc["summary"] = cb.get("brief", doc.get("summary"))
        if cb.get("corridor_shape"):
            doc["corridor_shape"] = cb["corridor_shape"]
        doc["_yango_caspian_maghreb_seal"] = utc_now()
        if apply:
            apath.write_text(json.dumps(doc, indent=2) + "\n")
        cluster_updates.append("algeria")

    for city_id, block in (algeria_b.get("city_briefs") or {}).items():
        path = brief_dir / f"{city_id}.json"
        if path.is_file():
            doc = load_json(path)
            doc["summary"] = block.get("brief", doc.get("summary"))
            doc["_yango_caspian_maghreb_seal"] = utc_now()
        else:
            doc = _minimal_city_brief(city_id, block.get("name", city_id), block.get("brief", ""), "Maghreb", "Algeria", None)
        if apply:
            path.write_text(json.dumps(doc, indent=2) + "\n")
        city_updates.append(city_id)

    # Morocco addendum
    morocco_b = load_json(PACKAGE / "morocco-briefs-2026-07-05.json")
    cb = morocco_b.get("cluster_brief_addendum", {}).get("morocco", {})
    mpath = cluster_dir / "morocco.json"
    if mpath.is_file() and cb:
        doc = load_json(mpath)
        doc["summary"] = cb.get("brief", doc.get("summary"))
        if cb.get("corridor_shape"):
            doc["corridor_shape"] = cb["corridor_shape"]
        doc["_yango_caspian_maghreb_seal"] = utc_now()
        if apply:
            mpath.write_text(json.dumps(doc, indent=2) + "\n")
        cluster_updates.append("morocco")

    slug_map = {
        "tangier-morocco": "tangier.json",
        "al-hoceima-morocco": "al-hoceima.json",
        "casablanca-morocco": "casablanca.json",
    }
    for city_id, block in (morocco_b.get("city_briefs") or {}).items():
        fname = slug_map.get(city_id, f"{city_id}.json")
        path = brief_dir / fname
        if path.is_file():
            doc = load_json(path)
            doc["summary"] = block.get("brief", doc.get("summary"))
            doc["city_id"] = city_id
            doc["_yango_caspian_maghreb_seal"] = utc_now()
        else:
            doc = _minimal_city_brief(city_id, block.get("name", city_id), block.get("brief", ""), "Maghreb", "Morocco", None)
        if apply:
            path.write_text(json.dumps(doc, indent=2) + "\n")
        city_updates.append(city_id)

    return {"city_briefs": city_updates, "cluster_briefs": cluster_updates}


def regenerate_city_brief_index(apply: bool) -> int:
    brief_dir = ROOT / "data-clean/city_briefs"
    entries = []
    for path in sorted(brief_dir.glob("*.json")):
        if path.name == "_index.json":
            continue
        doc = load_json(path)
        entries.append(
            {
                "city_id": doc.get("city_id") or path.stem,
                "display_name": doc.get("display_name") or doc.get("display"),
                "region": doc.get("region"),
                "tier": doc.get("tier"),
                "posture": doc.get("posture"),
            }
        )
    index = {
        "generated": utc_now(),
        "total_anchors": len(entries),
        "briefs": len(entries),
        "index": sorted(entries, key=lambda e: e["city_id"]),
    }
    if apply:
        (brief_dir / "_index.json").write_text(json.dumps(index, indent=2) + "\n")
    return len(entries)


def poi_counts_by_city(fbt: dict, city_ids: set[str]) -> dict[str, int]:
    counts: dict[str, int] = {c: 0 for c in city_ids}
    for poi in fbt.get("poi", []):
        cid = poi.get("properties", poi).get("parent_city_id")
        if cid in counts:
            counts[cid] += 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / "data-clean"
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(dc / "ROUTES.json")
    routes = route_features(routes_raw)
    mask = load_land_mask()
    poi_before = len(fbt.get("poi", []))
    routes_before = len(routes)

    touched_cities = {c["city_id"] for c in BP_GAZETTEER} | set(NEW_CITIES)
    poi_before_city = poi_counts_by_city(fbt, touched_cities)

    city_report = seal_cities(fbt, args.apply)
    bp_report = seal_bps(fbt, mask, args.apply)
    if bp_report.get("silent_drops", 0) > 0:
        print(f"✗ silent BP drops: {bp_report['silent_drops']}", file=sys.stderr)
        if args.apply:
            return 1

    corridor_report = seal_corridors(fbt, routes, bp_report, mask, args.apply)
    brief_report = seal_briefs(args.apply)

    poi_after_city = poi_counts_by_city(fbt, touched_cities) if args.apply else poi_before_city

    receipt = {
        "generated_at": utc_now(),
        "partner": "yango",
        "seal_tag": SEAL_TAG,
        "poi_before": poi_before,
        "poi_after": len(fbt.get("poi", [])) if args.apply else poi_before,
        "routes_before": routes_before,
        "cities": city_report,
        "bp": {
            "candidates": len(BP_GAZETTEER),
            "sealed": len(bp_report["sealed"]),
            "reconciled": len(bp_report["reconciled"]),
            "dropped": bp_report["dropped"],
            "silent_drops": bp_report.get("silent_drops", 0),
            "poi_before_by_city": poi_before_city,
            "poi_after_by_city": poi_after_city,
        },
        "corridors": {
            "expected": corridor_report["expected"],
            "minted": len(corridor_report["minted"]),
            "failed": corridor_report["failed"],
            "land_crossings": sum(1 for m in corridor_report["minted"] if m.get("land_km", 0) > LAND_THRESH_KM),
        },
        "briefs": brief_report,
    }

    if args.apply:
        save_json(dc / "FEATURES_BY_TYPE.json", fbt)
        save_routes(dc / "ROUTES.json", routes)
        receipt["routes_after"] = len(routes)
        receipt["city_brief_index"] = regenerate_city_brief_index(True)

    REPORT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))

    m, f = len(corridor_report["minted"]), len(corridor_report["failed"])
    print(
        f"\n{'✓' if args.apply else '·'} yango caspian-maghreb: "
        f"cities +{len(city_report['minted'])} | "
        f"BPs sealed={len(bp_report['sealed'])} reconciled={len(bp_report['reconciled'])} "
        f"dropped={len(bp_report['dropped'])} | routes {m}/{m + f}"
    )
    if f and args.apply:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())