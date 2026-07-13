#!/usr/bin/env python3
"""Abu Dhabi local land/water mask for ITC PTA routing QA.

Problem: UAE v2 overlay + coarse global_land_mask both fail in complementary ways:
  - Overlay treats Saadiyat/Yas/Reem cores as water → hides island land-cuts.
  - Coarse mask treats dredged Maqta / Yas Channel / Al Raha lagoons as land.

This mask:
  1. Forces LAND on reclamation / island cores (Saadiyat, Yas, Lulu, Reem, AD island, Hudayriat).
  2. Forces WATER on authored channel corridors + terminal aprons.
  3. Falls back to coarse global_land_mask outside those polygons.
"""
from __future__ import annotations

import math
from functools import lru_cache

R_EARTH_KM = 6371.0088
AD_DOMAIN = (54.20, 24.30, 54.75, 24.75)  # lon_min, lat_min, lon_max, lat_max

# Island / mainland cores that must remain LAND (tight cores only).
LAND_RINGS: list[list[tuple[float, float]]] = [
    # Abu Dhabi Island interior (keep north Corniche/Gulf shelf free)
    [
        (54.34, 24.43), (54.43, 24.43), (54.43, 24.465), (54.38, 24.47),
        (54.34, 24.455), (54.34, 24.43),
    ],
    # Saadiyat interior (tight core — north Gulf fairway must stay open)
    [
        (54.425, 24.530), (54.455, 24.535), (54.455, 24.555), (54.435, 24.555),
        (54.425, 24.540), (54.425, 24.530),
    ],
    # Yas interior (leave S channel + marina fringe free)
    [
        (54.600, 24.475), (54.635, 24.475), (54.635, 24.500), (54.610, 24.500),
        (54.600, 24.490), (54.600, 24.475),
    ],
    # Lulu interior (leave west/north fairway free)
    [
        (54.335, 24.498), (54.352, 24.498), (54.352, 24.512), (54.338, 24.512),
        (54.335, 24.498),
    ],
    # Reem interior (leave north channel free)
    [
        (54.395, 24.490), (54.415, 24.490), (54.415, 24.505), (54.395, 24.505),
        (54.395, 24.490),
    ],
    # Hudayriat interior (west exit free)
    [
        (54.325, 24.400), (54.350, 24.400), (54.350, 24.425), (54.330, 24.425),
        (54.325, 24.400),
    ],
]

# Navigable water corridors — generous fairways (channels force-water even if coarse says land).
WATER_RINGS: list[list[tuple[float, float]]] = [
    # Full coastal navigation shelf (Hud → Corniche → Saadiyat → Yas north)
    [
        (54.27, 24.39), (54.35, 24.42), (54.45, 24.48), (54.55, 24.50),
        (54.63, 24.50), (54.63, 24.46), (54.55, 24.47), (54.45, 24.48),
        (54.35, 24.47), (54.27, 24.44), (54.27, 24.39),
    ],
    # Open Gulf north band (full Corniche→Yas coastal express)
    [
        (54.28, 24.48), (54.40, 24.54), (54.50, 24.56), (54.60, 24.55),
        (54.62, 24.48), (54.50, 24.50), (54.35, 24.49), (54.28, 24.48),
    ],
    # Lulu west + Corniche–Louvre–Saadiyat cultural approach
    [
        (54.300, 24.460), (54.360, 24.500), (54.410, 24.540), (54.430, 24.560),
        (54.400, 24.565), (54.350, 24.520), (54.305, 24.480), (54.300, 24.460),
    ],
    # Mina Zayed passenger channel → Saadiyat ferry
    [
        (54.365, 24.505), (54.430, 24.525), (54.440, 24.560), (54.410, 24.565),
        (54.370, 24.530), (54.365, 24.505),
    ],
    # Khor Al Maqta full box (Al Qana ↔ Rabdan dredged)
    [
        (54.415, 24.395), (54.495, 24.395), (54.495, 24.425), (54.415, 24.425),
        (54.415, 24.395),
    ],
    # Mangrove / Al Raha lagoon → Yas fairway
    [
        (54.435, 24.435), (54.540, 24.440), (54.615, 24.450), (54.620, 24.485),
        (54.560, 24.490), (54.480, 24.475), (54.440, 24.460), (54.435, 24.435),
    ],
    # Yas Channel / Al Raha waterfront strip
    [
        (54.575, 24.440), (54.630, 24.440), (54.630, 24.475), (54.575, 24.475),
        (54.575, 24.440),
    ],
    # Hudayriat west exit → Corniche
    [
        (54.275, 24.385), (54.325, 24.385), (54.330, 24.460), (54.315, 24.485),
        (54.280, 24.450), (54.275, 24.385),
    ],
    # Al Aliah NE open water
    [
        (54.410, 24.545), (54.490, 24.545), (54.490, 24.615), (54.415, 24.605),
        (54.410, 24.545),
    ],
    # Reem north channel west to Corniche
    [
        (54.310, 24.475), (54.410, 24.500), (54.415, 24.525), (54.360, 24.525),
        (54.310, 24.500), (54.310, 24.475),
    ],
]

# Terminal aprons (lon, lat, radius_deg)
TERMINAL_APRONS: list[tuple[float, float, float]] = [
    (54.318, 24.476, 0.005),   # Corniche / Breakwater
    (54.378, 24.515, 0.0045),  # Marsa Mina
    (54.422, 24.553, 0.0045),  # Saadiyat Ferry
    (54.398, 24.534, 0.004),   # Louvre Saadiyat
    (54.476, 24.414, 0.004),   # Rabdan
    (54.430, 24.418, 0.004),   # Al Qana
    (54.452, 24.454, 0.004),   # Eastern Mangroves
    (54.604, 24.462, 0.004),   # Yas Bay
    (54.603, 24.470, 0.004),   # Yas Marina
    (54.606, 24.452, 0.004),   # Al Bandar
    (54.596, 24.451, 0.004),   # Al Muneera
    (54.617, 24.452, 0.004),   # Al Zeina
    (54.400, 24.500, 0.004),   # Reem
    (54.320, 24.400, 0.004),   # Hudayriat
    (54.460, 24.590, 0.004),   # Al Aliah
]


def in_domain(lon: float, lat: float) -> bool:
    lo, la, hi, ha = AD_DOMAIN
    return lo <= lon <= hi and la <= lat <= ha


@lru_cache(maxsize=1)
def _water_union():
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    from shapely.validation import make_valid

    polys = [make_valid(Polygon(r)) for r in WATER_RINGS if len(r) >= 4]
    return unary_union(polys)


@lru_cache(maxsize=1)
def _land_union():
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    from shapely.validation import make_valid

    polys = [make_valid(Polygon(r)) for r in LAND_RINGS if len(r) >= 4]
    return unary_union(polys)


@lru_cache(maxsize=1)
def _coarse():
    try:
        from global_land_mask import globe

        return globe
    except Exception:
        return None


def _in_apron(lon: float, lat: float) -> bool:
    for x, y, r in TERMINAL_APRONS:
        if (lon - x) ** 2 + (lat - y) ** 2 <= r * r:
            return True
    return False


def point_is_water(lon: float, lat: float) -> bool:
    if _in_apron(lon, lat):
        return True
    if in_domain(lon, lat):
        try:
            from shapely.geometry import Point

            pt = Point(lon, lat)
            land = _land_union()
            if land is not None and land.contains(pt):
                return False
            water = _water_union()
            if water is not None and water.contains(pt):
                return True
            coarse = _coarse()
            if coarse is not None:
                return not bool(coarse.is_land(lat, lon))
            return False
        except Exception:
            pass
    coarse = _coarse()
    if coarse is None:
        return True
    try:
        return not bool(coarse.is_land(lat, lon))
    except Exception:
        return True


def point_is_land(lon: float, lat: float) -> bool:
    return not point_is_water(lon, lat)


def hav_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def interior_land_km(coords: list, *, step_km: float = 0.08, apron_km: float = 0.15) -> float:
    if len(coords) < 2:
        return 0.0
    cum = 0.0
    samples: list[tuple[float, float, float, float]] = []
    for i in range(1, len(coords)):
        a = (float(coords[i - 1][0]), float(coords[i - 1][1]))
        b = (float(coords[i][0]), float(coords[i][1]))
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
    total = cum
    bad = 0.0
    for lon, lat, c, d in samples:
        if c < apron_km or c > total - apron_km:
            continue
        if point_is_land(lon, lat):
            bad += d
    return bad


def densify(coords: list[list[float]], n: int = 12) -> list[list[float]]:
    out: list[list[float]] = []
    for i in range(len(coords) - 1):
        a, b = coords[i], coords[i + 1]
        for k in range(n):
            t = k / n
            out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    out.append(list(coords[-1]))
    return out


def push_to_water(lon: float, lat: float, max_steps: int = 30, step: float = 0.003) -> tuple[float, float]:
    if point_is_water(lon, lat):
        return lon, lat
    for s in range(1, max_steps + 1):
        r = step * s
        for k in range(16):
            ang = 2 * math.pi * k / 16
            x = lon + r * math.cos(ang)
            y = lat + r * math.sin(ang)
            if point_is_water(x, y):
                return x, y
    return lon, lat


def a_star_water(start: list[float], goal: list[float], *, step: float = 0.004, max_expand: int = 40000):
    import heapq

    s = push_to_water(float(start[0]), float(start[1]))
    g = push_to_water(float(goal[0]), float(goal[1]))
    sx, sy = s
    gx, gy = g

    def key(x, y):
        return (int(round(x / step)), int(round(y / step)))

    def center(ix, iy):
        return ix * step, iy * step

    start_k, goal_k = key(sx, sy), key(gx, gy)
    open_h = [(0.0, start_k)]
    came = {start_k: None}
    gscore = {start_k: 0.0}
    expands = 0
    nbrs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    while open_h and expands < max_expand:
        _, cur = heapq.heappop(open_h)
        expands += 1
        if cur == goal_k:
            path = []
            while cur is not None:
                path.append(list(center(*cur)))
                cur = came[cur]
            path.reverse()
            path[0] = [float(start[0]), float(start[1])]
            path[-1] = [float(goal[0]), float(goal[1])]
            return path
        cx, cy = center(*cur)
        for dx, dy in nbrs:
            nxt = (cur[0] + dx, cur[1] + dy)
            nx, ny = center(*nxt)
            if not in_domain(nx, ny):
                continue
            if not point_is_water(nx, ny) and nxt != goal_k:
                continue
            cost = gscore[cur] + math.hypot(dx, dy) * step * 111.0
            if cost < gscore.get(nxt, 1e18):
                gscore[nxt] = cost
                came[nxt] = cur
                h = math.hypot(nx - gx, ny - gy) * 111.0
                heapq.heappush(open_h, (cost + h, nxt))
    return None


def route_via_spine(start, goal, spine, *, use_astar: bool = True) -> list[list[float]]:
    mids = [list(push_to_water(float(p[0]), float(p[1]))) for p in (spine or [])]
    nodes = [list(start)] + mids + [list(goal)]
    out: list[list[float]] = [nodes[0]]
    for i in range(len(nodes) - 1):
        a, b = nodes[i], nodes[i + 1]
        probe = densify([a, b], 12)
        land = interior_land_km(probe, apron_km=0.12)
        if land <= 0.08 or not use_astar:
            out.extend(densify([a, b], 14)[1:])
            continue
        path = a_star_water(a, b, step=0.0035)
        if path and len(path) >= 2:
            for j in range(len(path) - 1):
                out.extend(densify([path[j], path[j + 1]], 3)[1:])
        else:
            chain = [a]
            for t in (0.25, 0.5, 0.75):
                mx = a[0] + (b[0] - a[0]) * t
                my = a[1] + (b[1] - a[1]) * t
                chain.append(list(push_to_water(mx, my, max_steps=50, step=0.002)))
            chain.append(b)
            for j in range(len(chain) - 1):
                out.extend(densify([chain[j], chain[j + 1]], 10)[1:])
    return out
