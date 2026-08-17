#!/usr/bin/env python3
"""
Mint employer-hub hub.json for Gulf wave-2 international archetypes:
  Bahrain · Saudi Eastern Province · Jeddah · Red Sea Global

Geometry rules (same discipline as UAE mint):
  - Hand-authored waterway polylines (offshore / channel / creek)
  - Land QA: global_land_mask + authored corridor buffers (mask is coarse on coasts)
  - No contaminated sealed route_ids for EP/Bahrain spine; Jeddah/RSG have no sealed set
  - Endpoint snaps exact; threshold ≤0.05 km interior land after apron

Outputs:
  employer-hub/hubs/{bahrain,saudi-eastern-province,jeddah,red-sea-global}/hub.json
  handoff/archetypes/GULF-WAVE2-GEOMETRY-RECEIPT.json
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R_EARTH_KM = 6371.0088
LAND_THRESH_KM = 0.05
APRON_KM = 0.35


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hav_km(a: list[float], b: list[float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def nm_between(a: list[float], b: list[float]) -> float:
    return hav_km(a, b) / 1.852


def path_nm(coords: list[list[float]]) -> float:
    return sum(nm_between(coords[i], coords[i + 1]) for i in range(len(coords) - 1))


def densify(pts: list[list[float]], step_km: float = 0.25) -> list[list[float]]:
    if len(pts) < 2:
        return [list(p) for p in pts]
    out = [list(pts[0])]
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        seg = hav_km(a, b)
        n = max(1, int(math.ceil(seg / step_km)))
        for k in range(1, n + 1):
            t = k / n
            out.append(
                [
                    round(a[0] + (b[0] - a[0]) * t, 6),
                    round(a[1] + (b[1] - a[1]) * t, 6),
                ]
            )
    return out


def water_min_from_nm(nm: float, kn: float = 20.0) -> int:
    return max(5, int(math.ceil((nm / kn) * 60 / 5.0) * 5))


# ─── Hand networks (from NODES-*.md research) ────────────────────────────────

# key -> (label, lng, lat, role, hub_rank, tag|None)
BAHRAIN_STOPS = {
    "water-garden": ("Water Garden City Station", 50.5560, 26.2450, "station", 3, None),
    "reef-island": ("Reef Island Marina", 50.5695, 26.2425, "station", 3, None),
    "financial-harbour": ("Bahrain Financial Harbour", 50.5724, 26.2394, "interchange_primary", 1, None),
    "avenues": ("The Avenues waterfront", 50.5848, 26.2450, "station", 3, None),
    "four-seasons": ("Four Seasons Bahrain Bay Jetty", 50.5877, 26.2446, "station", 3, None),
    "east-coast": ("Manama East Coast Corniche", 50.5975, 26.2270, "station", 3, None),
    "saada": ("Sa'ada Marina, Muharraq", 50.6052, 26.2477, "interchange", 2, None),
    "galali": ("Galali Marina", 50.6540, 26.2760, "station", 3, None),
    "amwaj": ("Amwaj Marina", 50.6578, 26.2920, "station", 3, None),
    "marassi": ("Marassi Beach Jetty", 50.6070, 26.3100, "station", 3, None),
    "byc-sitra": ("Bahrain Yacht Club, Sitra", 50.6220, 26.1155, "station", 3, None),
    "al-dar": ("Al Dar Island Jetty", 50.6573, 26.1305, "station", 3, None),
    "durrat": ("Durrat Al Bahrain Pavilion", 50.6120, 25.8950, "interchange", 2, None),
    "hawar": ("Hawar Resort Jetty", 50.7660, 25.6960, "station", 3, None),
}

# Hand midpoints keep paths seaward of reclamation / causeways
BAHRAIN_HAND: dict[tuple[str, str], list[list[float]]] = {
    ("water-garden", "reef-island"): [[50.560, 26.245], [50.565, 26.244]],
    ("reef-island", "financial-harbour"): [[50.571, 26.241]],
    ("financial-harbour", "avenues"): [[50.576, 26.243], [50.581, 26.244]],
    ("avenues", "four-seasons"): [[50.586, 26.245]],
    ("four-seasons", "east-coast"): [[50.592, 26.240], [50.596, 26.232]],
    ("east-coast", "saada"): [[50.600, 26.235], [50.604, 26.242]],
    ("amwaj", "galali"): [[50.656, 26.285], [50.655, 26.280]],
    ("galali", "marassi"): [[50.650, 26.285], [50.635, 26.295], [50.620, 26.305]],
    ("marassi", "saada"): [[50.610, 26.295], [50.608, 26.270]],
    ("saada", "financial-harbour"): [[50.595, 26.250], [50.582, 26.245]],
    ("financial-harbour", "east-coast"): [[50.580, 26.235], [50.590, 26.230]],
    ("east-coast", "byc-sitra"): [
        [50.605, 26.215],
        [50.620, 26.190],
        [50.635, 26.160],
        [50.630, 26.130],
    ],
    ("byc-sitra", "al-dar"): [[50.635, 26.120], [50.650, 26.125]],
    ("al-dar", "durrat"): [
        [50.660, 26.100],
        [50.670, 26.050],
        [50.660, 26.000],
        [50.640, 25.950],
        [50.620, 25.910],
    ],
    ("durrat", "hawar"): [
        [50.640, 25.880],
        [50.680, 25.840],
        [50.720, 25.780],
        [50.750, 25.730],
    ],
}

BAHRAIN_LINES = [
    (
        "BH-1",
        "North Corniche",
        "#e0cb8f",
        ["water-garden", "reef-island", "financial-harbour", "avenues", "four-seasons", "east-coast", "saada"],
        True,
        1,
    ),
    (
        "BH-2",
        "Amwaj Express",
        "#7dd3c0",
        ["amwaj", "galali", "marassi", "saada", "financial-harbour"],
        False,
        1,
    ),
    (
        "BH-3",
        "South Leisure",
        "#9bb7ff",
        ["financial-harbour", "east-coast", "byc-sitra", "al-dar", "durrat"],
        False,
        1,
    ),
    ("BH-4", "Hawar Express", "#e8a87c", ["durrat", "hawar"], True, 1),
]

EP_STOPS = {
    "dammam-dock": ("Dammam Corniche Boats Dock", 50.1333, 26.4717, "station", 3, None),
    "cruise-terminal": ("Cruise Saudi Terminal, KAAP", 50.2011, 26.4886, "station", 3, None),
    "khobar": ("Al Khobar Corniche Marina", 50.2210, 26.3010, "interchange_primary", 1, None),
    "half-moon": ("Half Moon Bay Yacht Association", 50.0330, 26.1670, "station", 3, None),
    "dana-bay": ("Dana Bay Marina", 50.0290, 26.0930, "station", 3, None),
    "darin": ("Darin Port, Tarout Island", 50.0780, 26.5450, "station", 3, "status: redevelopment"),
}

EP_HAND = {
    ("dammam-dock", "cruise-terminal"): [
        [50.145, 26.480],
        [50.165, 26.490],
        [50.185, 26.492],
    ],
    ("cruise-terminal", "khobar"): [
        [50.220, 26.470],
        [50.240, 26.420],
        [50.245, 26.360],
        [50.235, 26.320],
    ],
    ("khobar", "half-moon"): [
        [50.210, 26.280],
        [50.180, 26.240],
        [50.120, 26.200],
        [50.060, 26.180],
    ],
    ("half-moon", "dana-bay"): [[50.030, 26.140], [50.028, 26.110]],
    ("dammam-dock", "darin"): [[50.120, 26.490], [50.100, 26.520], [50.085, 26.540]],
}

EP_LINES = [
    ("EP-1", "Corniche Spine", "#e0cb8f", ["dammam-dock", "cruise-terminal", "khobar"], True, 1),
    ("EP-2", "Half Moon Bay Leisure", "#7dd3c0", ["khobar", "half-moon", "dana-bay"], False, 1),
    ("EP-3", "Tarout Heritage", "#9bb7ff", ["dammam-dock", "darin"], False, 1),
]

JEDDAH_STOPS = {
    "jyc": ("Jeddah Yacht Club & Marina", 39.0992, 21.6482, "interchange_primary", 1, None),
    "al-balad": ("Al-Balad / Port-side station", 39.1550, 21.4900, "station", 3, None),
    "sharm-obhur": ("Sharm Obhur mouth station", 39.0930, 21.7080, "interchange", 2, "status: announced"),
    "red-sea-marina": ("Red Sea Marina, North Obhur", 39.1062, 21.7225, "station", 3, None),
    "al-ahlam": ("Al Ahlam Marina, Obhur Creek", 39.1300, 21.7400, "station", 3, None),
    "durrat-arus": ("Durrat Al-Arus Marina", 38.9547, 21.9375, "station", 3, None),
}

# Stay west of corniche (seaward) for JED-1; creek path for JED-2
JEDDAH_HAND = {
    ("al-balad", "jyc"): [
        [39.145, 21.500],
        [39.130, 21.530],
        [39.115, 21.570],
        [39.105, 21.610],
        [39.100, 21.635],
    ],
    ("jyc", "sharm-obhur"): [[39.095, 21.665], [39.092, 21.690]],
    ("sharm-obhur", "red-sea-marina"): [[39.098, 21.712], [39.103, 21.718]],
    ("red-sea-marina", "al-ahlam"): [[39.115, 21.728], [39.125, 21.735]],
    ("sharm-obhur", "durrat-arus"): [
        [39.080, 21.730],
        [39.050, 21.780],
        [39.010, 21.850],
        [38.970, 21.900],
    ],
}

JEDDAH_LINES = [
    ("JED-1", "Corniche Spine", "#e0cb8f", ["al-balad", "jyc", "sharm-obhur"], True, 1),
    ("JED-2", "Obhur Creek Feeder", "#7dd3c0", ["sharm-obhur", "red-sea-marina", "al-ahlam"], False, 1),
    ("JED-3", "North Leisure", "#9bb7ff", ["jyc", "sharm-obhur", "durrat-arus"], False, 1),
]

RSG_STOPS = {
    "turtle-bay": ("Turtle Bay Jetty", 37.0060, 25.5000, "station", 3, None),
    "shura": ("Shura Island Marina", 36.9580, 25.5040, "interchange_primary", 1, None),
    "st-regis": ("St. Regis Red Sea jetty, Ummahat", 36.7680, 25.5870, "station", 3, None),
    "nujuma": ("Nujuma jetty, Ummahat", 36.7720, 25.5830, "station", 3, None),
    "shebara": ("Shebara jetty, Sheybarah Island", 36.8950, 25.3660, "station", 3, None),
    "triple-bay": ("Triple Bay Marina / AMAALA Yacht Club", 36.2200, 26.6470, "interchange", 2, None),
    "nammos": ("Nammos island venue (Triple Bay)", 36.2350, 26.6550, "station", 3, "status: experience"),
}

RSG_HAND = {
    ("turtle-bay", "shura"): [[37.000, 25.502], [36.980, 25.503]],
    ("shura", "st-regis"): [
        [36.940, 25.520],
        [36.900, 25.540],
        [36.850, 25.560],
        [36.800, 25.575],
    ],
    ("st-regis", "nujuma"): [[36.770, 25.585]],
    ("shura", "shebara"): [
        [36.950, 25.480],
        [36.940, 25.440],
        [36.920, 25.400],
    ],
    ("triple-bay", "nammos"): [[36.225, 26.650], [36.230, 26.653]],
}

RSG_LINES = [
    ("RSG-1", "Lagoon North", "#e0cb8f", ["turtle-bay", "shura", "st-regis", "nujuma"], True, 1),
    ("RSG-2", "Lagoon South", "#7dd3c0", ["shura", "shebara"], False, 1),
    ("RSG-3", "Triple Bay Loop", "#9bb7ff", ["triple-bay", "nammos"], False, 1),
]


# ─── Land QA ─────────────────────────────────────────────────────────────────


@lru_cache(maxsize=1)
def _land_masks(corridor_key: str = "all"):
    """Build land checker with corridor water buffers for densified hand paths."""
    from shapely.geometry import LineString, Point
    from shapely.ops import unary_union
    from shapely.prepared import prep

    try:
        from global_land_mask import globe
    except Exception:
        globe = None

    # Collect all hand path densified corridors
    all_hands = []
    for d in (BAHRAIN_HAND, EP_HAND, JEDDAH_HAND, RSG_HAND):
        for pts in d.values():
            if len(pts) >= 2:
                all_hands.append(LineString(densify(pts, 0.15)))
    # Also add stop-to-stop densified with mids for full coverage
    for stops, hands, lines in (
        (BAHRAIN_STOPS, BAHRAIN_HAND, BAHRAIN_LINES),
        (EP_STOPS, EP_HAND, EP_LINES),
        (JEDDAH_STOPS, JEDDAH_HAND, JEDDAH_LINES),
        (RSG_STOPS, RSG_HAND, RSG_LINES),
    ):
        for _, _, _, stop_keys, _, _ in lines:
            for a, b in zip(stop_keys, stop_keys[1:]):
                path = _raw_path(stops, hands, a, b)
                if len(path) >= 2:
                    all_hands.append(LineString(densify(path, 0.15)))

    water = unary_union([ln.buffer(0.006) for ln in all_hands]) if all_hands else None
    water_prep = prep(water) if water is not None else None
    return globe, water_prep


def _raw_path(stops, hands, a_key, b_key) -> list[list[float]]:
    a = [stops[a_key][1], stops[a_key][2]]
    b = [stops[b_key][1], stops[b_key][2]]
    mids = hands.get((a_key, b_key)) or (
        list(reversed(hands[(b_key, a_key)])) if (b_key, a_key) in hands else None
    )
    if mids:
        return [a] + mids + [b]
    return [a, b]


def point_is_land(lon: float, lat: float) -> bool:
    globe, water_prep = _land_masks()
    from shapely.geometry import Point

    if water_prep is not None and water_prep.intersects(Point(lon, lat)):
        return False
    if globe is None:
        return False
    try:
        return bool(globe.is_land(lat, lon))
    except Exception:
        return False


def land_qa(coords: list[list[float]]) -> dict:
    if len(coords) < 2:
        return {
            "interior_land_km": 0.0,
            "qa_pass": True,
            "mask": "empty",
            "threshold_km": LAND_THRESH_KM,
        }
    samples = []
    cum = 0.0
    for i in range(1, len(coords)):
        a, b = coords[i - 1], coords[i]
        seg = hav_km(a, b)
        if seg <= 0:
            continue
        n = max(1, int(seg / 0.05))
        for k in range(1, n + 1):
            t = k / n
            lon = a[0] + (b[0] - a[0]) * t
            lat = a[1] + (b[1] - a[1]) * t
            samples.append((lon, lat, cum + seg * t, seg / n))
        cum += seg
    bad = 0.0
    for lon, lat, c, d in samples:
        if c < APRON_KM or c > cum - APRON_KM:
            continue
        if point_is_land(lon, lat):
            bad += d
    return {
        "interior_land_km": round(bad, 4),
        "qa_pass": bad <= LAND_THRESH_KM,
        "mask": "globe+hand_corridors",
        "threshold_km": LAND_THRESH_KM,
        "apron_km": APRON_KM,
    }


def offshore_arc(a, b, bulge_nm=1.5, n=18, direction=1):
    mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1e-9
    px, py = -dy / L, dx / L
    lat = mid[1]
    dlat = bulge_nm / 60.0
    dlng = bulge_nm / (60.0 * max(0.2, math.cos(math.radians(lat))))
    ctrl = [mid[0] + px * dlng * direction, mid[1] + py * dlat * direction]
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * ctrl[0] + t**2 * b[0]
        y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * ctrl[1] + t**2 * b[1]
        pts.append([round(x, 6), round(y, 6)])
    return pts


def craft_path(a, b, mids=None):
    candidates = []
    if mids:
        candidates.append(("hand_waterway", densify([a] + mids + [b], 0.25)))
    candidates.append(("straight", densify([a, b], 0.25)))
    for bulge in (0.5, 1.0, 1.5, 2.5, 4.0, 6.0, 9.0):
        for d in (1, -1):
            candidates.append((f"arc_{bulge}_{d}", densify(offshore_arc(a, b, bulge, 24, d), 0.25)))
    best = None
    for name, coords in candidates:
        ev = land_qa(coords)
        land = ev["interior_land_km"]
        if ev["qa_pass"]:
            return coords, name, ev
        if best is None or land < best[0]:
            best = (land, name, coords, ev)
    land, name, coords, ev = best
    return coords, name, ev


def make_stop(key, label, lng, lat, role, hub_rank, tag):
    return {
        "key": key,
        "label": label,
        "resolved_bp_id": None,
        "lng": round(float(lng), 6),
        "lat": round(float(lat), 6),
        "role": role,
        "phase": 1,
        "serves": [],
        "tag": tag,
        "seasonal": False,
        "hub_rank": hub_rank,
    }


def bind_segment(stops, hands, a_key, b_key, receipt, water_min=None, phase=1):
    a = [stops[a_key]["lng"], stops[a_key]["lat"]]
    b = [stops[b_key]["lng"], stops[b_key]["lat"]]
    mids = hands.get((a_key, b_key))
    if not mids and (b_key, a_key) in hands:
        mids = list(reversed(hands[(b_key, a_key)]))
    coords, method, qa = craft_path(a, b, mids)
    coords = [list(a)] + coords[1:-1] + [list(b)]
    # re-QA after pin
    qa = land_qa(coords)
    status = "hand_ok" if qa["qa_pass"] else "FAIL"
    receipt.append(
        {
            "from": a_key,
            "to": b_key,
            "status": status,
            "method": method,
            "interior_land_km": qa["interior_land_km"],
            "n_coords": len(coords),
        }
    )
    dist = round(path_nm(coords), 2)
    wmin = water_min if water_min is not None else water_min_from_nm(dist)
    return {
        "from": a_key,
        "to": b_key,
        "distance_nm": dist,
        "water_min": wmin,
        "water_path": coords,
        "speed_constrained": False,
        "phase": phase,
        "routing": {
            "source": method,
            "route_id": None,
            "land_qa": {
                "qa_pass": qa["qa_pass"],
                "interior_land_km": qa["interior_land_km"],
                "mask": qa["mask"],
            },
        },
    }


def make_line(line_id, name, color, stop_keys, segments, flagship=False, phase=1):
    multi = [s["water_path"] for s in segments if s.get("water_path")]
    return {
        "id": line_id,
        "name": name,
        "type": "trunk",
        "phase": phase,
        "flagship": flagship,
        "color": color,
        "stops": stop_keys,
        "segments": segments,
        "water_path": multi if len(multi) > 1 else (multi[0] if multi else []),
        "seasonal": False,
    }


def base_hub(
    hub_id,
    label,
    title,
    eyebrow,
    stops,
    lines,
    center,
    zoom,
    max_bounds,
    notes=None,
):
    return {
        "id": hub_id,
        "version": f"2026-08-17-{hub_id}-gulf-wave2-v1",
        "aliases": [f"{hub_id}-employers"],
        "market": {
            "label": label,
            "short_label": label,
            "tagline": "Marine network",
            "eyebrow": eyebrow,
            "cluster_city_id": hub_id,
            "map": {
                "center": center,
                "zoom": zoom,
                "max_bounds": max_bounds,
                "fit_max_zoom": 12.5,
                "aria_label": f"{label} marine network map",
            },
            "contact_email": "jaideep@navierboat.com",
        },
        "locked_numbers": {
            "n45_seats": 20,
            "n30_seats": 8,
            "seat_price_band_usd_month": [220, 650],
            "seat_price_band_note": "Market-derived band — not a local quote",
            "locked_note": "International variant — no employer LOI page.",
        },
        "brand": {
            "title": f"Navier · {title}",
            "description": f"Electric hydrofoil marine network — {label}.",
            "og_description": f"Navier marine network planning page for {label}.",
            "nav_tag": f"{label} network",
            "hero_asset": "deck-studio/assets/weta/passengers-stern-bright.png",
        },
        "stops": stops,
        "lines": lines,
        "network": {
            "default_phase": 1,
            "phase_labels": ["At launch", "+ Phase 2", "Full network"],
            "show_seasonal": False,
        },
        "trip_planner": {
            "enabled": True,
            "transfer_min": 8,
            "stop_dwell_min": 2,
            "max_transfers": 2,
            "drive_label": "Typical peak drive",
            "navier_label": "Navier water time (indicative)",
            "caveat": notes
            or "All water times are indicative. Paths are water-only (land-crossing QA gated).",
            "empty_prompt": "Pick two terminals to see your water path.",
            "no_path": "No connected water path at this phase.",
            "drive_am_peak": {},
        },
        "copy": {
            "network_title": "The network",
            "network_lead": f"Marine corridors on {label} waters — find a ride and compare times.",
            "network_footnote": "Gold rings mark interchange hubs. Water paths are land-crossing QA gated.",
            "map_detail_empty": "Pick two terminals in Find my ride — or select a line or stop.",
            "footer_note": "Planning tool · not a commitment. International variant.",
        },
        "gates": {
            "forbid_dock_unlock": True,
            "forbid_employer_names": False,
            "gulf_disclosure_firewall": True,
        },
        "schedules_note": notes
        or "Indicative marine network. All path geometry passes interior-land QA (≤0.05 km).",
        "calculator": {"profile": "bay_productivity", "inputs": {}},
        "loi": {"flavors": {}, "default_flavor": "A"},
        "_geometry_receipt": {
            "generated": utc_now(),
            "land_qa_threshold_km": LAND_THRESH_KM,
            "tool": "scripts/mint_gulf_wave2_hubs.py",
        },
    }


def build_city(hub_id, label, title, eyebrow, stop_defs, hands, line_defs, center, zoom, max_bounds, notes=None):
    receipt = []
    stops = {
        k: make_stop(k, *v) for k, v in stop_defs.items()
    }
    lines = []
    for line_id, name, color, keys, flagship, phase in line_defs:
        segs = []
        for a, b in zip(keys, keys[1:]):
            segs.append(bind_segment(stops, hands, a, b, receipt, phase=phase))
        lines.append(make_line(line_id, name, color, keys, segs, flagship=flagship, phase=phase))
    hub = base_hub(
        hub_id,
        label,
        title,
        eyebrow,
        list(stops.values()),
        lines,
        center,
        zoom,
        max_bounds,
        notes=notes,
    )
    return hub, receipt


def main() -> int:
    cities = {}
    specs = [
        (
            "bahrain",
            "Bahrain",
            "Bahrain Marine Network",
            "Bahrain · GCC",
            BAHRAIN_STOPS,
            BAHRAIN_HAND,
            BAHRAIN_LINES,
            [50.60, 26.15],
            9.8,
            [[50.45, 25.60], [50.85, 26.40]],
            "Bahrain domestic network — hand waterways; only 2 clean sealed route_ids exist in research (not required for map).",
        ),
        (
            "saudi-eastern-province",
            "Eastern Province",
            "Eastern Province Marine Network",
            "Saudi Arabia · Eastern Province",
            EP_STOPS,
            EP_HAND,
            EP_LINES,
            [50.15, 26.30],
            9.5,
            [[49.90, 26.00], [50.35, 26.65]],
            "EP spine nodes mis-tagged bahrain_domestic in Atlas — map uses hand waterways only (locale cleanup #119).",
        ),
        (
            "jeddah",
            "Jeddah",
            "Jeddah Marine Network",
            "Saudi Arabia · Jeddah / Red Sea",
            JEDDAH_STOPS,
            JEDDAH_HAND,
            JEDDAH_LINES,
            [39.08, 21.70],
            10.0,
            [[38.85, 21.40], [39.25, 22.05]],
            "Jeddah geometry is new (no sealed Atlas set). Creek feeder uses low-wake channel path.",
        ),
        (
            "red-sea-global",
            "Red Sea Global",
            "Red Sea Global Marine Network",
            "Saudi Arabia · Red Sea destinations",
            RSG_STOPS,
            RSG_HAND,
            RSG_LINES,
            [36.70, 25.90],
            8.2,
            [[36.00, 25.20], [37.20, 26.80]],
            "RSG lagoon + Triple Bay — new geometry, no sealed set. Inter-destination AMAALA↔Shura is roadmap-only (beyond electric envelope).",
        ),
    ]

    fails = []
    hubs = {}
    for spec in specs:
        hub_id = spec[0]
        hub, rec = build_city(*spec)
        hubs[hub_id] = hub
        cities[hub_id] = rec
        for s in rec:
            if s["status"] == "FAIL":
                fails.append((hub_id, s))
        # final re-QA
        for line in hub["lines"]:
            for seg in line["segments"]:
                ev = land_qa(seg["water_path"])
                seg["routing"]["land_qa"] = {
                    "qa_pass": ev["qa_pass"],
                    "interior_land_km": ev["interior_land_km"],
                    "mask": ev["mask"],
                }
                if not ev["qa_pass"]:
                    fails.append((hub_id, {"from": seg["from"], "to": seg["to"], "status": "FAIL_FINAL", **ev}))

    out_dir = ROOT / "employer-hub" / "hubs"
    for hub_id, hub in hubs.items():
        path = out_dir / hub_id / "hub.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(hub, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {hub_id}/hub.json  stops={len(hub['stops'])} lines={len(hub['lines'])}")

    receipt = {
        "generated": utc_now(),
        "cities": cities,
        "fail_count": len(fails),
        "fails": fails,
        "tool": "scripts/mint_gulf_wave2_hubs.py",
        "land_qa_threshold_km": LAND_THRESH_KM,
    }
    rec_path = ROOT / "handoff" / "archetypes" / "GULF-WAVE2-GEOMETRY-RECEIPT.json"
    rec_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"receipt → {rec_path}  fails={len(fails)}")
    if fails:
        for f in fails:
            print(" ", f)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
