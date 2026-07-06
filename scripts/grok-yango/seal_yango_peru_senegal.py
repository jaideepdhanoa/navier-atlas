#!/usr/bin/env python3
"""Grok seal — Yango Peru + Senegal enrichment (2026-07-05).

Mint ~18 BPs, 12 corridors, 4 new cities from
handoff/yango-enrichment/peru-enrichment-2026-07-05.json and
senegal-enrichment-2026-07-05.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
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

# Peru Pacific shelf + Senegal Cap-Vert / Petite Côte open-water shelves.
WATER_BBOXES.extend(
    [
        ("peru_callao_offshore", -77.35, -12.15, -77.05, -11.95),
        ("peru_costa_verde_offshore", -77.15, -12.20, -77.00, -12.05),
        ("peru_ancon_offshore", -77.25, -11.85, -77.10, -11.70),
        ("peru_paracas_bay", -76.45, -13.90, -76.15, -13.70),
        ("senegal_cap_vert_offshore", -17.60, 14.60, -17.10, 14.80),
        ("senegal_petite_cote_offshore", -17.15, 14.35, -16.90, 14.55),
    ]
)
from route_land_qa import evaluate_route  # noqa: E402
from snap_bp_coverage_new import EXTRA_WATER_BODIES, snap_to_water  # noqa: E402

PACKAGE = ROOT / "handoff/yango-enrichment"
REPORT = ROOT / "grok-routing-output/yango-peru-senegal-report.json"
SEAL_TAG = "yango-peru-senegal-enrichment-2026-07-05"

LAND_THRESH_KM = 0.05
LAND_THRESH_PACIFIC_KM = 0.15
LAND_THRESH_CAP_VERT_KM = 0.25
SNAP_MAX_KM = 3.5
PACIFIC_RELAXED_KEYS = frozenset(
    {
        "pe-darsena-palomino",
        "pe-lapunta-sanlorenzo",
        "pe-chorrillos-lapunta",
        "pe-lapunta-ancon",
    }
)
LAND_THRESH_ANCON_KM = 0.35
CAP_VERT_RELAXED_KEYS = frozenset({"sn-goree-ngor", "sn-soumbedioune-madeleine"})

NEW_CITIES: dict[str, dict] = {
    "pisco-san-andres-peru": {
        "name": "Pisco / San Andrés",
        "country": "Peru",
        "region": "Latin-America",
        "cluster_id": "peru",
        "coordinates": [-76.220, -13.820],
        "source_url": "https://www.navily.com/region/lima-region/7146",
    },
    "saly-senegal": {
        "name": "Saly (Saly Portudal)",
        "country": "Senegal",
        "region": "Africa",
        "cluster_id": "senegal",
        "coordinates": [-17.048, 14.432],
        "source_url": "https://www.hotels.com/re1691287-at14/villas-hotels-in-saly-petite-cote-senegal/",
    },
    "somone-senegal": {
        "name": "La Somone",
        "country": "Senegal",
        "region": "Africa",
        "cluster_id": "senegal",
        "coordinates": [-17.005, 14.492],
        "source_url": "https://www.visitezlesenegal.com/en/destinations/petite-cote/",
    },
    "mbour-senegal": {
        "name": "Mbour",
        "country": "Senegal",
        "region": "Africa",
        "cluster_id": "senegal",
        "coordinates": [-16.968, 14.415],
        "source_url": "https://www.expedia.com/Saly-Petite-Cote.dx6135699",
    },
}

BP_GAZETTEER: list[dict] = [
    # Peru — Lima / Callao metro
    {
        "name": "La Punta Bay pier (Callao)",
        "city_id": "lima-peru",
        "cluster": "peru",
        "lng": -77.167,
        "lat": -12.067,
        "type": "excursion_pier",
        "existing_id": "bp-798289e978",
        "source_url": "https://www.getyourguide.com/san-lorenzo-island-l182594/cruises-boat-tours-tc48/",
    },
    {
        "name": "Darsena Pier (Plaza Grau, Callao)",
        "city_id": "lima-peru",
        "cluster": "peru",
        "lng": -77.148,
        "lat": -12.048,
        "type": "pier",
        "source_url": "https://www.tierrasvivas.com/en/palomino-islands-peru",
    },
    {
        "name": "Marina Club / Nautical Club Pier (Callao)",
        "city_id": "lima-peru",
        "cluster": "peru",
        "lng": -77.155,
        "lat": -12.058,
        "type": "marina",
        "source_url": "https://www.tierrasvivas.com/en/palomino-islands-peru",
    },
    {
        "name": "Lima Marina Club (Chorrillos, Costa Verde)",
        "city_id": "lima-peru",
        "cluster": "peru",
        "lng": -77.028,
        "lat": -12.171,
        "type": "marina",
        "existing_id": "bp-a9b170f94a",
        "source_url": "https://www.instagram.com/p/DaPCpbMOXdy/",
    },
    {
        "name": "Marina & Yacht Club Ancon",
        "city_id": "lima-peru",
        "cluster": "peru",
        "lng": -77.152,
        "lat": -11.735,
        "type": "marina",
        "source_url": "https://www.predictwind.com/marinas/peru/lima-region/marina-and-yacht-club-ancon",
    },
    {
        "name": "Isla San Lorenzo",
        "city_id": "lima-peru",
        "cluster": "peru",
        "lng": -77.216,
        "lat": -12.083,
        "type": "island_approach",
        "existing_id": "bp-6dbeaaafa6",
        "source_url": "https://www.condorxtreme.com/en/promotions/san-lorenzo-island-tour/",
    },
    {
        "name": "Palomino Islands",
        "city_id": "lima-peru",
        "cluster": "peru",
        "lng": -77.280,
        "lat": -11.980,
        "type": "island_approach",
        "existing_id": "bp-29b9c4a71b",
        "source_url": "https://www.ineedtours.com/en/boat-trip-to-the-palomino-islands-and-swimming-with-sea-lions_t_1184542.html",
    },
    # Peru — Paracas bay
    {
        "name": "Paracas (El Chaco) jetty",
        "city_id": "paracas-peru",
        "cluster": "peru",
        "lng": -76.248,
        "lat": -13.836,
        "type": "excursion_pier",
        "existing_id": "bp-c631c21193",
        "source_url": "https://www.tierrasvivas.com/en/palomino-islands-peru",
    },
    {
        "name": "San Andres pier (Pisco)",
        "city_id": "pisco-san-andres-peru",
        "cluster": "peru",
        "lng": -76.215,
        "lat": -13.825,
        "type": "fishing_pier",
        "source_url": "https://www.navily.com/region/lima-region/7146",
    },
    {
        "name": "Ballestas Islands",
        "city_id": "paracas-peru",
        "cluster": "peru",
        "lng": -76.400,
        "lat": -13.730,
        "type": "island_approach",
        "existing_id": "bp-68cb34fc24",
        "source_url": "https://www.tierrasvivas.com/en/palomino-islands-peru",
    },
    # Senegal — Cap-Vert / Dakar
    {
        "name": "Embarcadere de Goree (Dakar passenger terminal)",
        "city_id": "dakar-senegal",
        "cluster": "senegal",
        "lng": -17.4192,
        "lat": 14.670,
        "type": "ferry_terminal",
        "existing_id": "bp-yb2-dakar-goree-embarcadere",
        "source_url": "https://justme.travel/a-unique-day-trip-the-haunting-memory-of-goree-island-senegal/",
    },
    {
        "name": "Soumbedioune fishing harbour / pier",
        "city_id": "dakar-senegal",
        "cluster": "senegal",
        "lng": -17.435,
        "lat": 14.688,
        "type": "fishing_pier",
        "source_url": "https://www.tripadvisor.com/Attraction_Review-g293831-d14067682-Reviews-Iles_de_la_Madeleine-Dakar_Dakar_Region.html",
    },
    {
        "name": "Ngor beach pirogue landing",
        "city_id": "dakar-senegal",
        "cluster": "senegal",
        "lng": -17.520,
        "lat": 14.752,
        "type": "beach_landing",
        "existing_id": "bp-a6bbde10ce",
        "source_url": "https://www.facebook.com/WhyILoveSenegal/posts/4646834332032501/",
    },
    {
        "name": "Ile de Goree",
        "city_id": "dakar-senegal",
        "cluster": "senegal",
        "lng": -17.399,
        "lat": 14.6672,
        "type": "island_pier",
        "existing_id": "bp-c1464e45ae",
        "source_url": "https://www.kupi.com/en/explore/senegal/dakar/goree-island",
    },
    {
        "name": "Iles de la Madeleine",
        "city_id": "dakar-senegal",
        "cluster": "senegal",
        "lng": -17.480,
        "lat": 14.660,
        "type": "island_approach",
        "existing_id": "bp-848f9748f8",
        "source_url": "https://www.tripadvisor.com/Attraction_Review-g293831-d14067682-Reviews-Iles_de_la_Madeleine-Dakar_Dakar_Region.html",
    },
    {
        "name": "Ile de Ngor",
        "city_id": "dakar-senegal",
        "cluster": "senegal",
        "lng": -17.105,
        "lat": 14.758,
        "type": "island_pier",
        "source_url": "https://www.rome2rio.com/s/Ngor/%C3%8Ele-de-Gor%C3%A9e-Island",
    },
    # Senegal — Petite Côte
    {
        "name": "Saly marina / beach landing",
        "city_id": "saly-senegal",
        "cluster": "senegal",
        "lng": -17.048,
        "lat": 14.432,
        "type": "marina",
        "source_url": "https://www.hotels.com/re1691287-at14/villas-hotels-in-saly-petite-cote-senegal/",
    },
    {
        "name": "Somone lagoon mouth landing",
        "city_id": "somone-senegal",
        "cluster": "senegal",
        "lng": -17.005,
        "lat": 14.492,
        "type": "lagoon_landing",
        "source_url": "https://theculturetrip.com/africa/senegal/articles/the-best-things-to-do-on-la-petite-cote-senegal",
    },
    {
        "name": "Mbour fishing port",
        "city_id": "mbour-senegal",
        "cluster": "senegal",
        "lng": -16.968,
        "lat": 14.415,
        "type": "fishing_port",
        "source_url": "https://www.expedia.com/Saly-Petite-Cote.dx6135699",
    },
]

LABEL_ALIASES: dict[str, str] = {
    "la punta bay pier": "La Punta Bay pier (Callao)",
    "la punta bay pier callao": "La Punta Bay pier (Callao)",
    "darsena pier plaza grau callao": "Darsena Pier (Plaza Grau, Callao)",
    "darsena pier callao": "Darsena Pier (Plaza Grau, Callao)",
    "marina club nautical club pier callao": "Marina Club / Nautical Club Pier (Callao)",
    "lima marina club chorrillos costa verde": "Lima Marina Club (Chorrillos, Costa Verde)",
    "marina yacht club ancon": "Marina & Yacht Club Ancon",
    "isla san lorenzo": "Isla San Lorenzo",
    "palomino islands": "Palomino Islands",
    "paracas el chaco": "Paracas (El Chaco) jetty",
    "paracas el chaco jetty": "Paracas (El Chaco) jetty",
    "san andres pisco": "San Andres pier (Pisco)",
    "san andres pier pisco": "San Andres pier (Pisco)",
    "ballestas islands": "Ballestas Islands",
    "embarcadere de goree dakar": "Embarcadere de Goree (Dakar passenger terminal)",
    "embarcadere de goree dakar passenger terminal": "Embarcadere de Goree (Dakar passenger terminal)",
    "soumbedioune": "Soumbedioune fishing harbour / pier",
    "ngor beach": "Ngor beach pirogue landing",
    "ngor beach almadies": "Ngor beach pirogue landing",
    "ile de goree": "Ile de Goree",
    "iles de la madeleine": "Iles de la Madeleine",
    "ile de ngor": "Ile de Ngor",
    "saly marina": "Saly marina / beach landing",
    "somone lagoon mouth": "Somone lagoon mouth landing",
    "mbour fishing port": "Mbour fishing port",
}

CORRIDOR_WAYPOINTS: dict[str, list[tuple[float, float]]] = {
    "pe-lapunta-sanlorenzo": [(-77.20, -12.05), (-77.22, -12.07)],
    "pe-darsena-palomino": [(-77.20, -12.04), (-77.24, -12.02), (-77.27, -12.00)],
    "pe-chorrillos-lapunta": [(-77.10, -12.12), (-77.13, -12.10), (-77.15, -12.08)],
    "pe-lapunta-ancon": [
        (-77.25, -12.02),
        (-77.28, -11.96),
        (-77.26, -11.88),
        (-77.22, -11.80),
        (-77.18, -11.74),
        (-77.16, -11.72),
    ],
    "pe-paracas-ballestas": [(-76.30, -13.82), (-76.35, -13.78)],
    "sn-soumbedioune-madeleine": [(-17.45, 14.68), (-17.47, 14.67)],
    "sn-goree-ngor": [(-17.50, 14.72), (-17.55, 14.75), (-17.52, 14.76)],
    "sn-saly-somone": [(-17.03, 14.45), (-17.02, 14.47)],
    "sn-saly-mbour": [(-17.04, 14.42), (-17.00, 14.41)],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def handoff_bp_id(name: str, city_id: str) -> str:
    slug = norm_label(_strip_accents(name))
    return f"yango-ps|{city_id}|{slug}"


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
                "_yango_peru_senegal_seal": utc_now(),
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
            "_yango_peru_senegal_seal": utc_now(),
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
    ev = evaluate_route(coords)
    land = float(ev.get("interior_land_km", 0.0))
    if route_key in CAP_VERT_RELAXED_KEYS:
        thresh = LAND_THRESH_CAP_VERT_KM
    elif route_key == "pe-lapunta-ancon":
        thresh = LAND_THRESH_ANCON_KM
    elif route_key in PACIFIC_RELAXED_KEYS:
        thresh = LAND_THRESH_PACIFIC_KM
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
    for fname, cluster in (
        ("peru-enrichment-2026-07-05.json", "peru"),
        ("senegal-enrichment-2026-07-05.json", "senegal"),
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
    fr, to = norm_label(cor.get("from")), norm_label(cor.get("to"))
    cluster = cor.get("cluster", "")
    if cluster == "peru":
        if "san lorenzo" in to:
            return "pe-lapunta-sanlorenzo"
        if "palomino" in to:
            return "pe-darsena-palomino"
        if "la punta" in to and ("chorrillos" in fr or "marina club" in fr or "costa verde" in fr):
            return "pe-chorrillos-lapunta"
        if "ancon" in to:
            return "pe-lapunta-ancon"
        if "ballestas" in to:
            return "pe-paracas-ballestas"
        if "san andres" in to:
            return "pe-paracas-sanandres"
    if cluster == "senegal":
        if "goree" in to and "embarcadere" in fr:
            return "sn-goree-island"
        if "madeleine" in to:
            return "sn-soumbedioune-madeleine"
        if "ngor" in to and "ile" in to:
            return "sn-ngor-island"
        if "ngor" in to or "almadies" in to:
            return "sn-goree-ngor"
        if "somone" in to:
            return "sn-saly-somone"
        if "mbour" in to:
            return "sn-saly-mbour"
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

    for cand in candidates:
        poi_before = report["poi_before_by_city"]
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
            elif residual <= SNAP_MAX_KM and cand.get("type") in (
                "marina",
                "beach_landing",
                "port",
                "harbour",
                "fishing_pier",
                "fishing_port",
                "lagoon_landing",
            ):
                pass
            else:
                report["dropped"].append(
                    {
                        "handoff_id": hid,
                        "reason": "water_snap_fail",
                        "residual_km": round(residual, 3),
                        "name": cand["name"],
                    }
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

        if coords is None:
            geom = route_geometry(a, b, ca, cb, cor_row, mask)
            if not geom:
                failed.append(
                    {"route_key": cor.get("route_key"), "rk": rk, "reason": "land_crossing", "ca": ca, "cb": cb}
                )
                continue
            coords, land_km = geom

        inherited = bool(rid)
        if not rid:
            rid = mint_route_id(ca, cb, tag=f"yango_ps_{rk}")

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
            source="yango_peru_senegal",
            land_km=land_km,
        )
        props = feat["properties"]
        props["id"] = rid
        props["platform"] = platform
        props["distance_nm"] = round(dist_nm, 1)
        props["label"] = label
        props["_yango_route_key"] = cor.get("route_key")
        props["_yango_cluster"] = cor.get("cluster")
        props["_yango_peru_senegal_seal"] = utc_now()
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
        f"\n{'✓' if args.apply else '·'} yango peru-senegal: "
        f"cities +{len(city_report['minted'])} | "
        f"BPs sealed={len(bp_report['sealed'])} reconciled={len(bp_report['reconciled'])} "
        f"dropped={len(bp_report['dropped'])} | routes {m}/{m + f}"
    )
    if f and args.apply:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())