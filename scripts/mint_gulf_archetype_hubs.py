#!/usr/bin/env python3
"""
Mint employer-hub hub.json for UAE international archetypes (Dubai, Abu Dhabi, RAK).

Geometry rules (hard):
  - Prefer HAND-authored waterway polylines (canal / creek / offshore / island channels)
  - Never bind contaminated RAK sealed route_ids
  - Sealed ROUTES.json only if endpoints snap to both stops AND corridor land-QA passes
  - Land QA uses UAE WKB land mask WITHOUT the regional dubai_coast water override
    (that override force-waters the whole UAE and hides land crossings)
  - Known canal/creek/channel centerlines are buffered as water corridors (mask has
    false-land on Dubai Water Canal / parts of Creek)
  - Threshold: ≤0.05 km interior land (after apron + corridor buffer)
  - Every rendered stop must have real coordinates (POI catalog or research hand coords)

Outputs:
  employer-hub/hubs/{dubai,abu-dhabi,ras-al-khaimah}/hub.json
  handoff/archetypes/GULF-HUB-GEOMETRY-RECEIPT.json
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROUTES = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
FEATS = ROUTES if isinstance(ROUTES, list) else ROUTES.get("features", [])
BY_ID = {f["properties"]["id"]: f for f in FEATS if (f.get("properties") or {}).get("id")}

POIS = json.loads((ROOT / "data-clean" / "FEATURES_BY_TYPE.json").read_text())["poi"]
POI_BY_ID: dict[str, dict] = {}
POI_BY_NAME: dict[str, dict] = {}
for f in POIS:
    p = f["properties"]
    coords = f["geometry"]["coordinates"]
    rec = {
        "id": p.get("id"),
        "name": p.get("name") or p.get("fullName"),
        "lng": coords[0],
        "lat": coords[1],
        "city": p.get("parent_city_id"),
    }
    if rec["id"]:
        POI_BY_ID[rec["id"]] = rec
    if rec["name"]:
        POI_BY_NAME[rec["name"].lower()] = rec

R_EARTH_KM = 6371.0088
LAND_THRESH_KM = 0.05
END_SNAP_NM = 0.55  # ~1 km max endpoint error for sealed binds
APRON_KM = 0.30


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hav_km(a: list[float], b: list[float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


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


# Sparse hand waterway centerlines — buffered as water (mask false-land on canal/creek)
WATERWAY_CENTERLINES: list[list[list[float]]] = [
    # Dubai Water Canal mouth → Business Bay → Creek connector → Al Seef
    [
        [55.2334, 25.198],
        [55.240, 25.1965],
        [55.248, 25.1935],
        [55.255, 25.1885],
        [55.2585, 25.185],
        [55.2601, 25.1834],
        [55.265, 25.1795],
        [55.272, 25.179],
        [55.280, 25.188],
        [55.290, 25.210],
        [55.297, 25.235],
        [55.3005, 25.2585],
    ],
    # Dubai Creek Al Seef / Old Souq → Festival City
    [
        [55.3005, 25.2585],
        [55.298, 25.2615],
        [55.2952, 25.2649],
        [55.305, 25.257],
        [55.315, 25.250],
        [55.325, 25.242],
        [55.335, 25.232],
        [55.3493, 25.2222],
    ],
    # Jumeirah offshore Bluewaters → Canal mouth
    [
        [55.1251, 25.0767],
        [55.115, 25.082],
        [55.108, 25.095],
        [55.108, 25.115],
        [55.115, 25.135],
        [55.130, 25.155],
        [55.155, 25.172],
        [55.185, 25.188],
        [55.210, 25.196],
        [55.2334, 25.198],
    ],
    # Palm outer gulf (Harbour / Atlantis / Bluewaters)
    [
        [55.1289, 25.0934],
        [55.118, 25.095],
        [55.105, 25.100],
        [55.098, 25.110],
        [55.098, 25.120],
        [55.105, 25.128],
        [55.1172, 25.1304],
        [55.105, 25.125],
        [55.100, 25.115],
        [55.100, 25.100],
        [55.105, 25.090],
        [55.115, 25.080],
        [55.1251, 25.0767],
    ],
    # Atlantis → Mina Rashid far-offshore
    [
        [55.1172, 25.1304],
        [55.100, 25.140],
        [55.095, 25.160],
        [55.110, 25.190],
        [55.140, 25.220],
        [55.180, 25.245],
        [55.220, 25.265],
        [55.250, 25.275],
        [55.2861, 25.2771],
    ],
    # World Islands apron
    [
        [55.1251, 25.0767],
        [55.120, 25.095],
        [55.130, 25.130],
        [55.150, 25.170],
        [55.165, 25.200],
        [55.180, 25.230],
        [55.145, 25.155],
        [55.1289, 25.0934],
    ],
    # AD north island shelf
    [
        [54.3107, 24.4651],
        [54.320, 24.480],
        [54.340, 24.510],
        [54.380, 24.550],
        [54.420, 24.555],
        [54.480, 24.560],
        [54.540, 24.555],
        [54.600, 24.530],
        [54.620, 24.490],
        [54.6093, 24.4756],
    ],
    # AD Lulu → Rabdan via north shelf
    [
        [54.3443, 24.5013],
        [54.35, 24.52],
        [54.38, 24.55],
        [54.45, 24.555],
        [54.50, 24.53],
        [54.50, 24.48],
        [54.49, 24.44],
        [54.4874, 24.4197],
    ],
    # AD Yas approaches / Al Raha
    [
        [54.6093, 24.4756],
        [54.600, 24.460],
        [54.580, 24.450],
        [54.550, 24.440],
        [54.520, 24.430],
        [54.4874, 24.4197],
        [54.6009, 24.4498],
        [54.618, 24.455],
        [54.620, 24.465],
        [54.4948, 24.4033],
    ],
    # RAK seaward Gulf shelf (Al Marjan → Al Hamra → Mina mouth → Corniche approaches)
    [
        [55.735, 25.705],
        [55.745, 25.712],
        [55.760, 25.712],
        [55.770, 25.710],
        [55.780, 25.725],
        [55.800, 25.740],
        [55.825, 25.745],
        [55.830, 25.760],
        [55.820, 25.790],
        [55.840, 25.820],
        [55.880, 25.830],
        [55.920, 25.820],
        [55.940, 25.800],
    ],
]

# Per-segment hand waypoints (from → to). Ends are snapped to stop coords at bind time.
HAND_PATHS: dict[tuple[str, str], list[list[float]]] = {
    ("bluewaters", "canal-1"): [
        [55.125084, 25.076721],
        [55.115, 25.082],
        [55.108, 25.095],
        [55.108, 25.115],
        [55.115, 25.135],
        [55.130, 25.155],
        [55.155, 25.172],
        [55.185, 25.188],
        [55.210, 25.196],
        [55.233398, 25.197992],
    ],
    ("canal-1", "business-bay"): [
        [55.233398, 25.197992],
        [55.240, 25.1965],
        [55.248, 25.1935],
        [55.255, 25.1885],
        [55.2585, 25.185],
        [55.260143, 25.183423],
    ],
    ("al-seef", "old-souq"): [
        [55.3005, 25.2585],
        [55.298, 25.2615],
        [55.295195, 25.264891],
    ],
    ("old-souq", "festival-city"): [
        [55.295195, 25.264891],
        [55.298, 25.262],
        [55.305, 25.257],
        [55.315, 25.250],
        [55.325, 25.242],
        [55.335, 25.232],
        [55.345, 25.225],
        [55.349277, 25.222234],
    ],
    ("harbour", "atlantis"): [
        [55.128935, 25.093374],
        [55.118, 25.095],
        [55.105, 25.100],
        [55.098, 25.110],
        [55.098, 25.120],
        [55.105, 25.128],
        [55.117241, 25.130375],
    ],
    ("atlantis", "bluewaters"): [
        [55.117241, 25.130375],
        [55.105, 25.125],
        [55.100, 25.115],
        [55.100, 25.100],
        [55.105, 25.090],
        [55.115, 25.080],
        [55.125084, 25.076721],
    ],
    ("bluewaters", "world-islands"): [
        [55.125084, 25.076721],
        [55.120, 25.095],
        [55.130, 25.130],
        [55.150, 25.170],
        [55.165, 25.200],
        [55.18, 25.23],
    ],
    ("world-islands", "harbour"): [
        [55.18, 25.23],
        [55.165, 25.195],
        [55.145, 25.155],
        [55.130, 25.120],
        [55.128935, 25.093374],
    ],
    ("atlantis", "mina-rashid"): [
        [55.117241, 25.130375],
        [55.100, 25.140],
        [55.095, 25.160],
        [55.110, 25.190],
        [55.140, 25.220],
        [55.180, 25.245],
        [55.220, 25.265],
        [55.250, 25.275],
        [55.28611, 25.277064],
    ],
    ("business-bay", "al-seef"): [
        [55.260143, 25.183423],
        [55.265, 25.1795],
        [55.272, 25.179],
        [55.280, 25.188],
        [55.290, 25.210],
        [55.297, 25.235],
        [55.3005, 25.2585],
    ],
    ("mina-rashid", "al-seef"): [
        [55.28611, 25.277064],
        [55.290, 25.270],
        [55.295, 25.265],
        [55.3005, 25.2585],
    ],
    ("emirates-palace", "lulu"): [
        [54.310704, 24.465079],
        [54.320, 24.480],
        [54.330, 24.495],
        [54.344343, 24.501337],
    ],
    ("lulu", "rabdan"): [
        [54.344343, 24.501337],
        [54.35, 24.52],
        [54.38, 24.55],
        [54.45, 24.555],
        [54.50, 24.53],
        [54.50, 24.48],
        [54.49, 24.44],
        [54.487426, 24.41968],
    ],
    ("emirates-palace", "saadiyat"): [
        [54.310704, 24.465079],
        [54.315, 24.480],
        [54.325, 24.500],
        [54.350, 24.530],
        [54.380, 24.550],
        [54.405, 24.555],
        [54.422, 24.553],
    ],
    ("saadiyat", "hidd-saadiyat"): [
        [54.422, 24.553],
        [54.430, 24.560],
        [54.445, 24.562],
        [54.45912, 24.56046],
    ],
    ("yas", "saadiyat"): [
        # North shelf into open water, then west to Saadiyat (avoid island land bridges)
        [54.609265, 24.475629],
        [54.630, 24.480],
        [54.640, 24.500],
        [54.640, 24.530],
        [54.600, 24.560],
        [54.540, 24.570],
        [54.480, 24.570],
        [54.440, 24.560],
        [54.422, 24.553],
    ],
    ("yas", "rabdan"): [
        [54.609265, 24.475629],
        [54.600, 24.460],
        [54.580, 24.450],
        [54.550, 24.440],
        [54.520, 24.430],
        [54.500, 24.425],
        [54.487426, 24.41968],
    ],
    ("emirates-palace", "yas"): [
        # North into open Gulf shelf, then east — never cut AD island land bridges
        [54.310704, 24.465079],
        [54.318, 24.490],
        [54.340, 24.530],
        [54.380, 24.560],
        [54.450, 24.570],
        [54.520, 24.565],
        [54.580, 24.540],
        [54.620, 24.500],
        [54.609265, 24.475629],
    ],
    ("nurai", "saadiyat"): [
        [54.47619, 24.61462],
        [54.470, 24.600],
        [54.450, 24.575],
        [54.435, 24.560],
        [54.422, 24.553],
    ],
    ("al-qana", "rabdan"): [
        [54.494847, 24.403286],
        [54.492, 24.408],
        [54.488, 24.415],
        [54.487426, 24.41968],
    ],
    ("al-bandar", "yas"): [
        [54.600854, 24.44978],
        [54.610, 24.450],
        [54.618, 24.455],
        [54.620, 24.465],
        [54.615, 24.472],
        [54.609265, 24.475629],
    ],
    # RAK Coastal Spine only (v1): Al Marjan → Al Hamra RYC → Mina Al Arab → Corniche.
    # Paths stay on the Gulf shelf — north around Al Marjan breakwaters; seaward of lagoons.
    ("al-marjan", "royal-yacht-club"): [
        [55.7392, 25.6915],
        [55.735, 25.705],
        [55.745, 25.712],
        [55.760, 25.712],
        [55.772, 25.705],
        [55.778509, 25.695935],
    ],
    ("royal-yacht-club", "mina-al-arab"): [
        [55.778509, 25.695935],
        [55.770, 25.710],
        [55.780, 25.725],
        [55.800, 25.740],
        [55.825, 25.745],
        [55.8475, 25.732],
    ],
    ("mina-al-arab", "qawasim-1"): [
        # Exit Mina NW into Gulf shelf, run east in open water, drop south to Corniche berth
        [55.8475, 25.732],
        [55.835, 25.750],
        [55.820, 25.770],
        [55.815, 25.800],
        [55.830, 25.825],
        [55.860, 25.845],
        [55.900, 25.850],
        [55.920, 25.845],
        [55.944, 25.845],
        [55.956, 25.845],
        [55.960, 25.835],
        [55.960, 25.823],
        [55.956, 25.815],
        [55.952, 25.807],
        [55.950, 25.797],
        [55.944, 25.788],
    ],
}


@lru_cache(maxsize=1)
def _land_masks():
    from shapely import wkb
    from shapely.geometry import LineString
    from shapely.ops import unary_union
    from shapely.prepared import prep

    land = wkb.loads((ROOT / "grok-routing-output" / "uae_gulf_land_v2.wkb").read_bytes())
    land_prep = prep(land)
    corridors = []
    # Buffer only known false-land waterway centerlines (Dubai Canal / Creek, etc.).
    # Do NOT buffer HAND_PATHS — that self-certified coarse chords that visually crossed land.
    for cl in WATERWAY_CENTERLINES:
        if len(cl) >= 2:
            corridors.append(LineString(densify(cl, 0.15)))
    # ~500 m buffer around authored waterways
    water_buf = unary_union([ln.buffer(0.005) for ln in corridors]) if corridors else None
    water_prep = prep(water_buf) if water_buf is not None else None
    return land_prep, water_prep


def _point_is_land_gated(lon: float, lat: float) -> bool:
    """WKB land, minus authored waterway corridors. No regional water-override."""
    from shapely.geometry import Point

    land_prep, water_prep = _land_masks()
    pt = Point(lon, lat)
    if water_prep is not None and water_prep.intersects(pt):
        return False
    return bool(land_prep.intersects(pt))


def _point_is_land_pure(lon: float, lat: float) -> bool:
    from shapely.geometry import Point

    land_prep, _ = _land_masks()
    return bool(land_prep.intersects(Point(lon, lat)))


def _interior_land_km(
    coords: list[list[float]],
    *,
    gated: bool = True,
    step_km: float = 0.05,
    apron_km: float = APRON_KM,
) -> float:
    if len(coords) < 2:
        return 0.0
    checker = _point_is_land_gated if gated else _point_is_land_pure
    samples: list[tuple[float, float, float, float]] = []
    cum = 0.0
    for i in range(1, len(coords)):
        a, b = coords[i - 1], coords[i]
        seg = hav_km(a, b)
        if seg <= 0:
            continue
        n = max(1, int(seg / step_km))
        for k in range(1, n + 1):
            t = k / n
            lon = a[0] + (b[0] - a[0]) * t
            lat = a[1] + (b[1] - a[1]) * t
            samples.append((lon, lat, cum + seg * t, seg / n))
        cum += seg
    bad = 0.0
    for lon, lat, c, d in samples:
        if c < apron_km or c > cum - apron_km:
            continue
        if checker(lon, lat):
            bad += d
    return bad


def land_qa(coords: list[list[float]]) -> dict:
    """Land QA for Gulf hubs.

    Gated mask = WKB land minus WATERWAY_CENTERLINES buffers (Dubai Canal/Creek false-land).
    HAND_PATHS are intentionally NOT buffered — coastal hand chords must sit in real water.
    """
    land = _interior_land_km(coords, gated=True)
    pure = _interior_land_km(coords, gated=False)
    return {
        "interior_land_km": round(land, 4),
        "pure_wkb_land_km": round(pure, 4),
        "qa_pass": land <= LAND_THRESH_KM,
        "mask": "uae_wkb_v2+waterway_centerlines_only",
        "threshold_km": LAND_THRESH_KM,
        "apron_km": APRON_KM,
    }


def route_coords(route_id: str) -> list[list[float]] | None:
    f = BY_ID.get(route_id)
    if not f:
        return None
    g = f["geometry"]
    if g["type"] == "LineString":
        return [[float(x), float(y)] for x, y in g["coordinates"]]
    if g["type"] == "MultiLineString":
        parts = g["coordinates"]
        best = max(parts, key=len)
        return [[float(x), float(y)] for x, y in best]
    return None


def endpoints_snap_ok(
    coords: list[list[float]],
    a: list[float],
    b: list[float],
    max_nm: float = END_SNAP_NM,
) -> tuple[bool, list[list[float]]]:
    """Orient path and require both ends near stops."""
    if not coords or len(coords) < 2:
        return False, coords
    d0a = nm_between(coords[0], a)
    d1a = nm_between(coords[-1], a)
    if d1a < d0a:
        coords = list(reversed(coords))
    ok = nm_between(coords[0], a) <= max_nm and nm_between(coords[-1], b) <= max_nm
    return ok, coords


def route_ok(
    route_id: str,
    a: list[float] | None = None,
    b: list[float] | None = None,
    max_land_km: float = LAND_THRESH_KM,
) -> tuple[bool, dict | None, list | None]:
    coords = route_coords(route_id)
    if not coords or len(coords) < 2:
        return False, None, None
    if a is not None and b is not None:
        snap_ok, coords = endpoints_snap_ok(coords, a, b)
        if not snap_ok:
            return False, {"qa_pass": False, "reason": "endpoint_snap_fail"}, None
    ev = land_qa(coords)
    ok = bool(ev.get("qa_pass")) and (ev.get("interior_land_km") or 0) <= max_land_km
    return ok, ev, coords


def offshore_arc(
    a: list[float],
    b: list[float],
    bulge_nm: float = 1.5,
    n: int = 18,
    direction: int = 1,
) -> list[list[float]]:
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


def craft_water_path(
    a: list[float],
    b: list[float],
    *,
    prefer_offshore: bool = False,
    mids: list[list[float]] | None = None,
) -> tuple[list[list[float]], dict]:
    """Hand mids first, then offshore arcs until corridor land-QA passes."""
    candidates: list[tuple[str, list[list[float]]]] = []
    if mids:
        candidates.append(("hand_waypoints", densify([a] + mids + [b], 0.25)))
    if not prefer_offshore:
        candidates.append(("straight", densify([a, b], 0.25)))
    for bulge in (0.4, 0.8, 1.2, 1.8, 2.5, 3.5, 5.0, 7.0, 10.0, 14.0):
        for d in (1, -1):
            candidates.append((f"arc_{bulge}_{d}", densify(offshore_arc(a, b, bulge, 24, d), 0.25)))
    for bulge in (2.0, 4.0, 6.0, 9.0):
        for d in (1, -1):
            mid_off = offshore_arc(a, b, bulge, 2, d)[1]
            p1 = offshore_arc(a, mid_off, max(0.5, bulge / 3), 12, d)
            p2 = offshore_arc(mid_off, b, max(0.5, bulge / 3), 12, d)
            candidates.append((f"twohop_{bulge}_{d}", densify(p1[:-1] + p2, 0.25)))
    if prefer_offshore:
        candidates.append(("straight", densify([a, b], 0.25)))

    best = None
    for name, coords in candidates:
        ev = land_qa(coords)
        land = ev.get("interior_land_km") or 0
        if ev.get("qa_pass") and land <= LAND_THRESH_KM:
            return coords, {"method": name, **ev}
        if best is None or land < best[0]:
            best = (land, name, coords, ev)
    land, name, coords, ev = best
    return coords, {
        "method": name,
        "qa_pass": False,
        "interior_land_km": land,
        "pure_wkb_land_km": ev.get("pure_wkb_land_km"),
        "mask": ev.get("mask"),
        "warning": "best-effort path still fails corridor land QA — review manually",
    }


def hand_path_for(from_key: str, to_key: str) -> list[list[float]] | None:
    if (from_key, to_key) in HAND_PATHS:
        return densify(HAND_PATHS[(from_key, to_key)], 0.25)
    if (to_key, from_key) in HAND_PATHS:
        return list(reversed(densify(HAND_PATHS[(to_key, from_key)], 0.25)))
    return None


def nm_between(a: list[float], b: list[float]) -> float:
    R = 3440.065
    lat1, lon1 = math.radians(a[1]), math.radians(a[0])
    lat2, lon2 = math.radians(b[1]), math.radians(b[0])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(min(1.0, h)))


def path_nm(coords: list[list[float]]) -> float:
    return sum(nm_between(coords[i], coords[i + 1]) for i in range(len(coords) - 1))


def water_min_from_nm(nm: float, kn: float = 20.0) -> int:
    return max(5, int(math.ceil((nm / kn) * 60 / 5.0) * 5))


def resolve_stop(key: str, label: str, lng: float | None, lat: float | None, bp_id: str | None = None) -> dict:
    if bp_id and bp_id in POI_BY_ID:
        r = POI_BY_ID[bp_id]
        lng, lat = r["lng"], r["lat"]
    elif label.lower() in POI_BY_NAME:
        r = POI_BY_NAME[label.lower()]
        lng, lat = r["lng"], r["lat"]
        bp_id = bp_id or r.get("id")
    if lng is None or lat is None:
        raise ValueError(f"No coordinates for stop {key} ({label})")
    return {
        "key": key,
        "label": label,
        "resolved_bp_id": bp_id,
        "lng": round(float(lng), 6),
        "lat": round(float(lat), 6),
        "role": "station",
        "phase": 1,
        "serves": [],
        "tag": None,
        "seasonal": False,
        "hub_rank": 3,
    }


def bind_segment(
    from_stop: dict,
    to_stop: dict,
    preferred_ids: list[str],
    receipt: list,
    phase: int = 1,
    water_min: int | None = None,
    speed_constrained: bool = False,
    water_min_label: str | None = None,
    prefer_offshore: bool = False,
    force_craft: bool = False,
) -> dict:
    """Bind a water segment: hand path → snap-checked sealed → craft fallback."""
    a = [from_stop["lng"], from_stop["lat"]]
    b = [to_stop["lng"], to_stop["lat"]]
    coords = None
    used_id = None
    method = None
    qa: dict | None = None

    # 1) Prefer hand-authored waterway polyline (primary for Gulf visual QA)
    hand = hand_path_for(from_stop["key"], to_stop["key"])
    if hand and len(hand) >= 2:
        # Snap endpoints to exact stop coords
        path = [list(a)] + hand[1:-1] + [list(b)]
        path = densify(path, 0.25)
        ev = land_qa(path)
        if ev.get("qa_pass"):
            coords, method, qa = path, "hand_waterway", ev
        # else: fall through to sealed / craft — do not ship a failing hand chord

    # 2) Optional sealed bind — only if endpoints snap AND corridor QA passes
    if coords is None and not force_craft:
        for rid in preferred_ids:
            ok, ev, c = route_ok(rid, a, b)
            if ok and c:
                # pin ends
                c = [list(a)] + c[1:-1] + [list(b)]
                coords, used_id, method, qa = c, rid, "sealed_route", ev
                break

    # 3) Craft fallback (arcs + optional hand mids as soft guidance)
    if coords is None:
        mids = None
        hand_soft = hand_path_for(from_stop["key"], to_stop["key"])
        if hand_soft and len(hand_soft) > 2:
            mids = hand_soft[1:-1]
        dist_guess = nm_between(a, b)
        prefer = prefer_offshore or dist_guess >= 6.0 or force_craft
        coords, meta = craft_water_path(a, b, prefer_offshore=prefer, mids=mids)
        method = meta.get("method")
        qa = meta
        used_id = None

    # Final pin ends
    if coords and len(coords) >= 2:
        coords = [list(a)] + coords[1:-1] + [list(b)]

    status = "FAIL"
    if qa and qa.get("qa_pass"):
        status = "hand_ok" if method == "hand_waterway" else ("bound_ok" if used_id else "crafted_ok")
    elif method == "hand_waterway" and (qa or {}).get("interior_land_km", 99) <= LAND_THRESH_KM:
        status = "hand_ok"
    receipt.append(
        {
            "from": from_stop["key"],
            "to": to_stop["key"],
            "status": status,
            "route_id": used_id,
            "method": method,
            "interior_land_km": (qa or {}).get("interior_land_km", 0),
            "pure_wkb_land_km": (qa or {}).get("pure_wkb_land_km"),
            "n_coords": len(coords or []),
        }
    )

    dist = round(path_nm(coords), 2)
    wmin = water_min if water_min is not None else water_min_from_nm(dist)
    seg = {
        "from": from_stop["key"],
        "to": to_stop["key"],
        "distance_nm": dist,
        "water_min": wmin,
        "water_path": coords,
        "speed_constrained": speed_constrained,
        "phase": phase,
        "routing": {
            "source": method,
            "route_id": used_id,
            "land_qa": {
                "qa_pass": (qa or {}).get("qa_pass"),
                "interior_land_km": (qa or {}).get("interior_land_km"),
                "pure_wkb_land_km": (qa or {}).get("pure_wkb_land_km"),
                "mask": (qa or {}).get("mask"),
            },
        },
    }
    if water_min_label:
        seg["water_min_label"] = water_min_label
    return seg


def make_line(line_id: str, name: str, color: str, stops: list[str], segments: list[dict], phase: int = 1, flagship: bool = False) -> dict:
    # multi water_path for whole line
    multi = []
    for s in segments:
        if s.get("water_path"):
            multi.append(s["water_path"])
    return {
        "id": line_id,
        "name": name,
        "type": "trunk",
        "phase": phase,
        "flagship": flagship,
        "color": color,
        "stops": stops,
        "segments": segments,
        "water_path": multi if len(multi) > 1 else (multi[0] if multi else []),
        "seasonal": False,
    }


def write_hub(hub: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(hub, indent=2, ensure_ascii=False) + "\n")


# ─── City definitions ───────────────────────────────────────────────────────

DUBAI_STOPS = [
    ("bluewaters", "Bluewaters Ferry Station", "bp-711cf44b60"),
    ("canal-1", "Dubai Canal Marine Transport Station 1", None),
    ("business-bay", "Business Bay Marine Transport Station", None),
    ("atlantis", "Atlantis The Palm Jetty", "bp-55aa98c7fb"),
    ("harbour", "Dubai Harbour Cruise Terminal", "bp-1982dfd974"),
    ("mina-rashid", "Mina Rashid Cruise Terminal", "bp-5f767488d3"),
    ("al-seef", "Al Seef Marine Transport Station (Dubai Creek)", None),
    ("old-souq", "Dubai Old Souq Marine Transport Station", None),
    ("festival-city", "Dubai Festival City Marina", None),
    ("world-islands", "The World Islands", "bp-8c7fcc1977"),
]

AD_STOPS = [
    ("emirates-palace", "Emirates Palace Marina", "bp-14c19a643c"),
    ("saadiyat", "Saadiyat Marina & Ferry Terminal", "bp-8cb3366589"),
    ("yas", "Yas Marina", "bp-3b66a8ce1d"),
    ("rabdan", "Rabdan Marina", "bp-5ca878cc7e"),
    ("hidd-saadiyat", "Hidd Al Saadiyat Marina", None),
    ("nurai", "Zaya Nurai Island Jetty", None),
    ("lulu", "Lulu Island", None),
    ("al-qana", "Al Qana Marina", None),
    ("al-bandar", "Al Bandar Marina (Al Raha Beach)", None),
]

# Research / verified coords for RAK (Atlas POI catalog is contaminated for RAK tags)
# v1 foiling network: 4 stops only — one Coastal Spine (no heritage spur, no Corniche micro-tram)
RAK_HAND_COORDS = {
    # Al Hamra Marina & Royal Yacht Club RAK (catalog bp-6ec9d9d298 — verified)
    "royal-yacht-club": (55.778509, 25.695935, "bp-6ec9d9d298"),
    # Al Marjan Island west shore (public island centroid-ish landing)
    "al-marjan": (55.7392, 25.6915, None),
    # Mina Al Arab lagoon mouth (developer marina basin — research approx)
    "mina-al-arab": (55.8475, 25.7320, None),
    # Single Corniche foiling hub (collapse of Qawasim 1/2 + Hilton abra stops).
    # Snapped ~75 m seaward of the research pier coord so the berth sits in WKB water.
    "qawasim-1": (55.9440, 25.7880, None),
}


def build_dubai(receipt: dict) -> dict:
    rec = []
    stops = {}
    for key, label, bp in DUBAI_STOPS:
        stops[key] = resolve_stop(key, label, None, None, bp)

    # promote hubs
    for k in ("bluewaters", "mina-rashid", "harbour", "atlantis"):
        stops[k]["role"] = "interchange"
        stops[k]["hub_rank"] = 2
    stops["bluewaters"]["role"] = "interchange_primary"
    stops["bluewaters"]["hub_rank"] = 1

    lines = []
    # MAR-1 Marina–Canal: Bluewaters → Canal → Business Bay
    segs = [
        bind_segment(stops["bluewaters"], stops["canal-1"], ["rn-02b2927692e0"], rec, water_min=30),
        bind_segment(
            stops["canal-1"],
            stops["business-bay"],
            ["rn-9d23e412de22", "rn-2327c9838e1d"],
            rec,
            water_min=12,
        ),
    ]
    lines.append(
        make_line(
            "MAR-1",
            "Marina–Canal",
            "#e0cb8f",
            ["bluewaters", "canal-1", "business-bay"],
            segs,
            flagship=True,
        )
    )

    # CRK-1 Creek Heritage: Al Seef → Old Souq → Festival City
    segs = [
        bind_segment(stops["al-seef"], stops["old-souq"], ["rn-bfa9c0d8ba7b", "rn-da7538ae363d"], rec, water_min=8),
        bind_segment(
            stops["old-souq"],
            stops["festival-city"],
            ["rn-2f0bb0572ec4", "rn-343edeabf362", "rn-15c6fdffe852"],
            rec,
            water_min=15,
        ),
    ]
    lines.append(make_line("CRK-1", "Creek Heritage", "#7dd3c0", ["al-seef", "old-souq", "festival-city"], segs))

    # PLM-1 Palm & Harbour: Harbour → Atlantis → Bluewaters
    segs = [
        bind_segment(stops["harbour"], stops["atlantis"], ["rn-c6db0ce8b6a6"], rec, water_min=12),
        bind_segment(stops["atlantis"], stops["bluewaters"], ["rn-d3a88461a5ed", "rn-f314996e94b7"], rec, water_min=15),
    ]
    lines.append(make_line("PLM-1", "Palm & Harbour", "#9bb7ff", ["harbour", "atlantis", "bluewaters"], segs))

    # ISL-1 World Islands: Bluewaters → World → Harbour
    segs = [
        bind_segment(stops["bluewaters"], stops["world-islands"], ["rn-200157a4d545", "rn-fb4ca86ddc17"], rec, water_min=30),
        bind_segment(stops["world-islands"], stops["harbour"], ["rn-f4c2f161324c"], rec, water_min=28),
    ]
    lines.append(make_line("ISL-1", "World Islands", "#e8a87c", ["bluewaters", "world-islands", "harbour"], segs))

    # SIG-1 Palm–Mina Rashid: Atlantis → Mina Rashid (marquee)
    segs = [
        bind_segment(stops["atlantis"], stops["mina-rashid"], ["rn-b7ac6238165d"], rec, water_min=40),
    ]
    lines.append(make_line("SIG-1", "Palm–Mina Rashid", "#c4b5fd", ["atlantis", "mina-rashid"], segs, flagship=True))

    # XFR-1 Creek connector — joins Creek Heritage to the marina/canal mesh for trip planner
    segs = [
        bind_segment(
            stops["business-bay"],
            stops["al-seef"],
            ["rn-1623544e6d4a"],
            rec,
            water_min=18,
            prefer_offshore=True,
        ),
        bind_segment(
            stops["mina-rashid"],
            stops["al-seef"],
            [],
            rec,
            water_min=15,
            prefer_offshore=True,
            force_craft=True,
        ),
    ]
    lines.append(
        make_line(
            "XFR-1",
            "Creek Connector",
            "#94a3b8",
            ["business-bay", "al-seef", "mina-rashid"],
            segs,
            phase=1,
        )
    )

    receipt["dubai"] = rec
    return base_hub(
        "dubai",
        "Dubai",
        "Dubai Marine Network",
        "UAE · Dubai",
        list(stops.values()),
        lines,
        center=[55.20, 25.18],
        zoom=10.2,
        max_bounds=[[54.95, 24.95], [55.45, 25.40]],
        contact="jaideep@navierboat.com",
    )


def build_abu_dhabi(receipt: dict) -> dict:
    rec = []
    stops = {}
    for key, label, bp in AD_STOPS:
        stops[key] = resolve_stop(key, label, None, None, bp)

    for k in ("emirates-palace", "saadiyat", "yas"):
        stops[k]["role"] = "interchange"
        stops[k]["hub_rank"] = 2
    stops["emirates-palace"]["role"] = "interchange_primary"
    stops["emirates-palace"]["hub_rank"] = 1
    stops["nurai"]["tag"] = "status: renovation"
    stops["nurai"]["phase"] = 2

    lines = []
    # COR-1 Corniche: Emirates Palace → Lulu → Rabdan
    segs = [
        bind_segment(stops["emirates-palace"], stops["lulu"], ["rn-544c3f7471c1", "rn-7c69dd29a122"], rec, water_min=15),
        # No sealed bind: rn-881a8cdb6576 is Emirates Palace→Rabdan (skips Lulu)
        bind_segment(stops["lulu"], stops["rabdan"], [], rec, water_min=20, force_craft=True, prefer_offshore=True),
    ]
    lines.append(
        make_line(
            "COR-1",
            "Corniche",
            "#e0cb8f",
            ["emirates-palace", "lulu", "rabdan"],
            segs,
            flagship=True,
        )
    )

    # SDY-1 Saadiyat Culture: Emirates Palace → Saadiyat → Hidd
    segs = [
        bind_segment(
            stops["emirates-palace"],
            stops["saadiyat"],
            ["rn-60483e41e97f"],
            rec,
            water_min=30,
            water_min_label="~30 min day · ~34 min after sunset (20 kn night cap)",
        ),
        bind_segment(stops["saadiyat"], stops["hidd-saadiyat"], ["rn-b56442e5125a"], rec, water_min=12),
    ]
    lines.append(make_line("SDY-1", "Saadiyat Culture", "#7dd3c0", ["emirates-palace", "saadiyat", "hidd-saadiyat"], segs))

    # YAS-1 Yas: Yas → Saadiyat → Rabdan; also Yas → Emirates Palace
    segs = [
        bind_segment(stops["yas"], stops["saadiyat"], ["rn-b58e6dc0d928"], rec, water_min=35),
        bind_segment(stops["yas"], stops["rabdan"], ["rn-94858c712852"], rec, water_min=25),
        bind_segment(stops["emirates-palace"], stops["yas"], ["rn-b89451fb7867"], rec, water_min=40),
    ]
    lines.append(make_line("YAS-1", "Yas", "#9bb7ff", ["yas", "saadiyat", "rabdan", "emirates-palace"], segs))

    # NRI-1 Nurai Shuttle
    segs = [
        bind_segment(stops["nurai"], stops["saadiyat"], ["rn-cedce441d25a"], rec, phase=2, water_min=20),
    ]
    lines.append(make_line("NRI-1", "Nurai Shuttle", "#e8a87c", ["nurai", "saadiyat"], segs, phase=2))

    # Optional label-only stops for Al Qana / Al Bandar — seaward paths only
    segs_extra = [
        bind_segment(
            stops["al-qana"],
            stops["rabdan"],
            [],
            rec,
            phase=2,
            water_min=15,
            prefer_offshore=True,
            force_craft=True,
        ),
        bind_segment(
            stops["al-bandar"],
            stops["yas"],
            [],
            rec,
            phase=2,
            water_min=18,
            prefer_offshore=True,
            force_craft=True,
        ),
    ]
    lines.append(
        make_line(
            "RAH-1",
            "Al Raha Link",
            "#c4b5fd",
            ["al-bandar", "al-qana", "rabdan", "yas"],
            segs_extra,
            phase=2,
        )
    )

    receipt["abu-dhabi"] = rec
    return base_hub(
        "abu-dhabi",
        "Abu Dhabi",
        "Abu Dhabi Marine Network",
        "UAE · Abu Dhabi",
        list(stops.values()),
        lines,
        center=[54.45, 24.50],
        zoom=10.0,
        max_bounds=[[54.20, 24.30], [54.75, 24.70]],
        contact="jaideep@navierboat.com",
    )


def build_rak(receipt: dict) -> dict:
    rec = []
    stops = {}
    labels = {
        "royal-yacht-club": "Royal Yacht Club of Ras Al Khaimah",
        "al-marjan": "Al Marjan Island",
        "mina-al-arab": "Mina Al Arab / Hayat Island",
        "qawasim-1": "Al Qawasim Corniche",
    }
    for key, (lng, lat, bp) in RAK_HAND_COORDS.items():
        stops[key] = resolve_stop(key, labels[key], lng, lat, bp)
        if key in ("al-marjan", "mina-al-arab"):
            stops[key]["tag"] = "status: verify facility"

    stops["royal-yacht-club"]["role"] = "interchange_primary"
    stops["royal-yacht-club"]["hub_rank"] = 1
    stops["qawasim-1"]["role"] = "interchange"
    stops["qawasim-1"]["hub_rank"] = 2

    # All RAK segments hand-crafted — no contaminated route_ids
    def seg(a, b, wmin, label=None):
        return bind_segment(
            stops[a],
            stops[b],
            [],
            rec,
            water_min=wmin,
            water_min_label=label or "indicative — no published numeric RAK speed rules; conservative basis",
            prefer_offshore=True,
            force_craft=True,
        )

    # v1: ONE Coastal Spine only — Al Marjan → Al Hamra → Mina Al Arab → Corniche.
    # No overlapping Resort/City/Heritage products; no Corniche micro-tram; no heritage spur.
    lines = [
        make_line(
            "SPN-1",
            "Coastal Spine",
            "#e0cb8f",
            ["al-marjan", "royal-yacht-club", "mina-al-arab", "qawasim-1"],
            [
                seg("al-marjan", "royal-yacht-club", 15),
                seg("royal-yacht-club", "mina-al-arab", 25),
                seg(
                    "mina-al-arab",
                    "qawasim-1",
                    55,
                    "≈55 min day · ≈65 min after dark (20 kn night planning basis)",
                ),
            ],
            flagship=True,
        )
    ]

    receipt["ras-al-khaimah"] = rec
    return base_hub(
        "ras-al-khaimah",
        "Ras Al Khaimah",
        "Ras Al Khaimah Marine Network",
        "UAE · Ras Al Khaimah",
        list(stops.values()),
        lines,
        center=[55.86, 25.75],
        zoom=10.4,
        max_bounds=[[55.65, 25.62], [56.05, 25.90]],
        contact="jaideep@navierboat.com",
        notes="RAK v1: single Coastal Spine (4 stops). Hand waterways; pure-WKB land QA. Existing Corniche abra stops are local heritage feeders — not separate foiling stations.",
    )


def base_hub(hub_id, label, title, eyebrow, stops, lines, center, zoom, max_bounds, contact, notes=None):
    return {
        "id": hub_id,
        "version": f"2026-08-16-{hub_id}-gulf-v1",
        "aliases": [f"{hub_id}-employers"],
        "market": {
            "label": label,
            "short_label": label,
            "tagline": "Marine network",
            "eyebrow": eyebrow,
            "cluster_city_id": f"{hub_id}-uae" if hub_id != "ras-al-khaimah" else "ras-al-khaimah-uae",
            "map": {
                "center": center,
                "zoom": zoom,
                "max_bounds": max_bounds,
                "fit_max_zoom": 12.5,
                "aria_label": f"{label} marine network map",
            },
            "contact_email": contact,
        },
        "locked_numbers": {
            "n45_seats": 20,
            "n30_seats": 8,
            "seat_price_band_usd_month": [400, 900],
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
            "land_qa_threshold_km": 0.05,
            "tool": "scripts/mint_gulf_archetype_hubs.py",
        },
    }


def main() -> int:
    receipt: dict = {"generated": utc_now(), "cities": {}}
    hubs = {
        "dubai": build_dubai(receipt["cities"]),
        "abu-dhabi": build_abu_dhabi(receipt["cities"]),
        "ras-al-khaimah": build_rak(receipt["cities"]),
    }

    fails = []
    for city, segs in receipt["cities"].items():
        for s in segs:
            if s.get("status") == "FAIL":
                fails.append((city, s))

    # Final re-QA every segment path (corridor-gated)
    for city, hub in hubs.items():
        for line in hub["lines"]:
            for seg in line.get("segments") or []:
                ev = land_qa(seg["water_path"])
                seg["routing"]["land_qa"] = {
                    "qa_pass": ev.get("qa_pass"),
                    "interior_land_km": ev.get("interior_land_km"),
                    "pure_wkb_land_km": ev.get("pure_wkb_land_km"),
                    "mask": ev.get("mask"),
                }
                if not ev.get("qa_pass") or (ev.get("interior_land_km") or 0) > LAND_THRESH_KM:
                    fails.append(
                        (
                            city,
                            {
                                "from": seg["from"],
                                "to": seg["to"],
                                "status": "FAIL_FINAL",
                                "interior_land_km": ev.get("interior_land_km"),
                                "pure_wkb_land_km": ev.get("pure_wkb_land_km"),
                            },
                        )
                    )

    out_dir = ROOT / "employer-hub" / "hubs"
    for city, hub in hubs.items():
        write_hub(hub, out_dir / city / "hub.json")
        print(f"wrote {city}/hub.json  stops={len(hub['stops'])} lines={len(hub['lines'])}")

    receipt["fail_count"] = len(fails)
    receipt["fails"] = fails
    rec_path = ROOT / "handoff" / "archetypes" / "GULF-HUB-GEOMETRY-RECEIPT.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"receipt → {rec_path}  fails={len(fails)}")
    if fails:
        print("FAILURES:")
        for f in fails:
            print(" ", f)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
