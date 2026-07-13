#!/usr/bin/env python3
"""SF Bay local land/water mask for WETA / sf-bay-ferry routing QA.

Replaces the oversized regional `sf_bay` WATER_BBOX (which treated whole islands
as water) with:
  1. Navigable-water polygons (open Bay + channels + terminal aprons)
  2. Explicit land exclusions for islands/peninsulas inside those water hulls
  3. Optional coarse global_land_mask only *outside* the local Bay domain

Use `point_is_land` / `interior_land_km` from this module for Bay corridor QA.
"""
from __future__ import annotations

import math
from functools import lru_cache
from typing import Iterable

R_EARTH_KM = 6371.0088
BAY_DOMAIN = (-122.65, 37.40, -121.70, 38.20)  # lon_min, lat_min, lon_max, lat_max

# Navigable-water hulls — generous open Bay + channels. Land exclusions carve islands.
WATER_RINGS: list[list[tuple[float, float]]] = [
    # Entire open Central + South Bay water body (SF–Oakland–South Bay main pool)
    [
        (-122.52, 37.78), (-122.48, 37.74), (-122.42, 37.70), (-122.38, 37.66),
        (-122.40, 37.64), (-122.38, 37.60), (-122.34, 37.55), (-122.30, 37.52),
        (-122.26, 37.50), (-122.20, 37.485), (-122.185, 37.50), (-122.20, 37.52),
        (-122.24, 37.55), (-122.28, 37.60), (-122.30, 37.68), (-122.28, 37.74),
        (-122.25, 37.76), (-122.26, 37.79), (-122.28, 37.80), (-122.27, 37.82),
        (-122.28, 37.86), (-122.30, 37.90), (-122.34, 37.92), (-122.40, 37.92),
        (-122.46, 37.90), (-122.50, 37.88), (-122.53, 37.84), (-122.54, 37.80),
        (-122.52, 37.78),
    ],
    # Oyster Point basin + San Bruno channel (explicit)
    [
        (-122.395, 37.655), (-122.360, 37.655), (-122.355, 37.680), (-122.370, 37.685),
        (-122.395, 37.675), (-122.395, 37.655),
    ],
    # SM–Hayward span + Redwood dredged channel
    [
        (-122.30, 37.52), (-122.22, 37.50), (-122.195, 37.495), (-122.195, 37.515),
        (-122.22, 37.535), (-122.28, 37.56), (-122.30, 37.54), (-122.30, 37.52),
    ],
    # Oakland–Alameda estuary throat (Jack London + Main Street approaches)
    [
        (-122.32, 37.785), (-122.275, 37.785), (-122.270, 37.795), (-122.275, 37.805),
        (-122.30, 37.805), (-122.32, 37.795), (-122.32, 37.785),
    ],
    # Seaplane Lagoon + west Alameda basin entrance
    [
        (-122.325, 37.770), (-122.290, 37.770), (-122.290, 37.785), (-122.320, 37.785),
        (-122.325, 37.770),
    ],
    # Harbor Bay south approach (water south of Bay Farm)
    [
        (-122.30, 37.72), (-122.24, 37.72), (-122.24, 37.745), (-122.28, 37.755),
        (-122.30, 37.74), (-122.30, 37.72),
    ],
    # San Pablo Bay full open water
    [
        (-122.52, 37.90), (-122.40, 37.90), (-122.32, 37.94), (-122.28, 38.00),
        (-122.28, 38.08), (-122.34, 38.12), (-122.42, 38.13), (-122.50, 38.10),
        (-122.54, 38.04), (-122.54, 37.94), (-122.52, 37.90),
    ],
    # Carquinez + Vallejo / Mare Island
    [
        (-122.34, 38.04), (-122.20, 38.04), (-122.18, 38.06), (-122.22, 38.10),
        (-122.28, 38.12), (-122.32, 38.10), (-122.34, 38.06), (-122.34, 38.04),
    ],
    # Suisun → Antioch main channel
    [
        (-122.20, 38.04), (-121.78, 38.00), (-121.78, 38.04), (-122.05, 38.08),
        (-122.20, 38.07), (-122.20, 38.04),
    ],
    # Mission Bay / China Basin channel
    [
        (-122.400, 37.760), (-122.380, 37.760), (-122.380, 37.795), (-122.398, 37.798),
        (-122.400, 37.760),
    ],
    # Treasure Island south/west pier water
    [
        (-122.385, 37.810), (-122.360, 37.810), (-122.358, 37.830), (-122.380, 37.832),
        (-122.385, 37.810),
    ],
    # Pier 41 / north Embarcadero water
    [
        (-122.430, 37.800), (-122.405, 37.800), (-122.405, 37.820), (-122.430, 37.820),
        (-122.430, 37.800),
    ],
    # Martinez / Hercules shoreline water fringe
    [
        (-122.32, 38.00), (-122.12, 38.01), (-122.12, 38.04), (-122.32, 38.05),
        (-122.32, 38.00),
    ],
]

# Islands / land that must remain land inside water hulls.
LAND_RINGS: list[list[tuple[float, float]]] = [
    # Alameda Island core (leave west/north shore for terminals)
    [
        (-122.295, 37.765), (-122.245, 37.765), (-122.240, 37.775), (-122.250, 37.795),
        (-122.285, 37.798), (-122.295, 37.780), (-122.295, 37.765),
    ],
    # Bay Farm Island core
    [
        (-122.255, 37.725), (-122.225, 37.725), (-122.220, 37.740), (-122.235, 37.748),
        (-122.255, 37.745), (-122.255, 37.725),
    ],
    # Treasure Island / YBI land mass (keep south pier apron out)
    [
        (-122.375, 37.818), (-122.358, 37.818), (-122.355, 37.832), (-122.365, 37.838),
        (-122.375, 37.830), (-122.375, 37.818),
    ],
    # Angel Island
    [
        (-122.442, 37.852), (-122.422, 37.852), (-122.418, 37.868), (-122.432, 37.872),
        (-122.442, 37.860), (-122.442, 37.852),
    ],
    # SF mainland interior (west of Embarcadero apron — keep pier water free)
    [
        (-122.430, 37.760), (-122.400, 37.760), (-122.398, 37.785), (-122.405, 37.805),
        (-122.430, 37.805), (-122.430, 37.760),
    ],
    # East Bay mainland east of estuary (do not swallow Jack London apron)
    [
        (-122.265, 37.80), (-122.15, 37.80), (-122.15, 38.00), (-122.28, 38.00),
        (-122.30, 37.90), (-122.28, 37.84), (-122.265, 37.80),
    ],
    # Peninsula mainland — strictly inland of Bay shoreline / channels
    # (west of US-101 corridor approx; do NOT include Oyster Point basin or SM–Hayward water)
    [
        (-122.48, 37.45), (-122.30, 37.45), (-122.28, 37.50), (-122.32, 37.58),
        (-122.40, 37.65), (-122.45, 37.68), (-122.48, 37.60), (-122.48, 37.45),
    ],
    # Marin / Tiburon / Sausalito land
    [
        (-122.55, 37.83), (-122.46, 37.83), (-122.45, 37.90), (-122.48, 37.96),
        (-122.55, 37.93), (-122.55, 37.83),
    ],
]

# Terminal aprons forced water (lon, lat, radius_deg)
TERMINAL_APRONS: list[tuple[float, float, float]] = [
    (-122.3933, 37.7955, 0.006),    # Ferry Building
    (-122.2776, 37.7945, 0.006),    # Oakland JL
    (-122.293984, 37.790723, 0.005),  # Alameda Main
    (-122.29832, 37.77717, 0.005),  # Seaplane
    (-122.253, 37.735, 0.005),      # Harbor Bay
    (-122.376, 37.665, 0.005),      # Oyster Point
    (-122.387, 37.77, 0.005),       # Mission Bay
    (-122.21, 37.505, 0.005),       # Redwood
    (-122.354, 37.911, 0.005),      # Richmond
    (-122.273, 38.099, 0.005),      # Vallejo
    (-122.269, 38.096, 0.005),      # Mare Island
    (-122.318, 37.865, 0.0045),     # Berkeley
    (-122.37, 37.82, 0.0045),       # Treasure Island
    (-122.4169, 37.8088, 0.0045),   # Pier 41
    (-122.29, 38.017, 0.0045),      # Hercules
    (-122.141, 38.029, 0.0045),     # Martinez
    (-121.815, 38.015, 0.005),      # Antioch
]


def in_domain(lon: float, lat: float) -> bool:
    lo, la, hi, ha = BAY_DOMAIN
    return lo <= lon <= hi and la <= lat <= ha


@lru_cache(maxsize=1)
def _water_polys():
    from shapely.geometry import Polygon
    from shapely.ops import unary_union

    polys = [Polygon(r) for r in WATER_RINGS if len(r) >= 4]
    return unary_union(polys) if polys else None


@lru_cache(maxsize=1)
def _land_polys():
    from shapely.geometry import Polygon
    from shapely.ops import unary_union

    polys = [Polygon(r) for r in LAND_RINGS if len(r) >= 4]
    return unary_union(polys) if polys else None


@lru_cache(maxsize=1)
def _coarse():
    try:
        from global_land_mask import globe

        return globe
    except Exception:
        return None


def _in_apron(lon: float, lat: float) -> bool:
    for x, y, r in TERMINAL_APRONS:
        if abs(lon - x) <= r and abs(lat - y) <= r:
            if (lon - x) ** 2 + (lat - y) ** 2 <= r * r:
                return True
    return False


def point_is_water(lon: float, lat: float) -> bool:
    """Local SF Bay water test."""
    if _in_apron(lon, lat):
        return True
    if in_domain(lon, lat):
        try:
            from shapely.geometry import Point

            pt = Point(lon, lat)
            land = _land_polys()
            if land is not None and land.contains(pt):
                return False
            water = _water_polys()
            if water is not None and water.contains(pt):
                return True
            # Outside authored water hull but in domain: fall back to coarse ocean
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


def interior_land_km(
    coords: list,
    *,
    step_km: float = 0.08,
    apron_km: float = 0.15,
) -> float:
    """Land distance along path using local Bay mask. Endpoint aprons excluded."""
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


def push_to_water(lon: float, lat: float, max_steps: int = 24, step: float = 0.004) -> tuple[float, float]:
    """Nudge a point to nearest local water (search ring)."""
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


def a_star_water(
    start: list[float],
    goal: list[float],
    *,
    step: float = 0.008,
    max_expand: int = 25000,
) -> list[list[float]] | None:
    """Coarse A* on local water grid between two points."""
    import heapq

    s = push_to_water(float(start[0]), float(start[1]))
    g = push_to_water(float(goal[0]), float(goal[1]))
    sx, sy = s
    gx, gy = g

    def key(x: float, y: float) -> tuple[int, int]:
        return (int(round(x / step)), int(round(y / step)))

    def cell_center(ix: int, iy: int) -> tuple[float, float]:
        return ix * step, iy * step

    start_k = key(sx, sy)
    goal_k = key(gx, gy)
    open_h: list[tuple[float, tuple[int, int]]] = []
    heapq.heappush(open_h, (0.0, start_k))
    came: dict[tuple[int, int], tuple[int, int] | None] = {start_k: None}
    gscore = {start_k: 0.0}
    expands = 0
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while open_h and expands < max_expand:
        _, cur = heapq.heappop(open_h)
        expands += 1
        if cur == goal_k:
            path = []
            while cur is not None:
                path.append(list(cell_center(*cur)))
                cur = came[cur]
            path.reverse()
            # snap ends to true endpoints
            path[0] = [float(start[0]), float(start[1])]
            path[-1] = [float(goal[0]), float(goal[1])]
            return path
        cx, cy = cell_center(*cur)
        for dx, dy in neighbors:
            nxt = (cur[0] + dx, cur[1] + dy)
            nx, ny = cell_center(*nxt)
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


def route_via_spine(
    start: list[float],
    goal: list[float],
    spine: list[list[float]] | None,
    *,
    use_astar: bool = True,
) -> list[list[float]]:
    """Build densified path start → spine → goal, A* filling land segments."""
    mids = [list(push_to_water(float(p[0]), float(p[1]), max_steps=30, step=0.003)) for p in (spine or [])]
    nodes = [list(start)] + mids + [list(goal)]
    out: list[list[float]] = [nodes[0]]
    for i in range(len(nodes) - 1):
        a, b = nodes[i], nodes[i + 1]
        probe = densify([a, b], 12)
        land = interior_land_km(probe, apron_km=0.12)
        if land <= 0.08 or not use_astar:
            out.extend(densify([a, b], 14)[1:])
            continue
        path = a_star_water(a, b, step=0.005, max_expand=40000)
        if path and len(path) >= 2:
            # keep A* path densified lightly
            for j in range(len(path) - 1):
                out.extend(densify([path[j], path[j + 1]], 3)[1:])
        else:
            # multi-midpoint lateral nudges
            mids2 = []
            for t in (0.25, 0.5, 0.75):
                mx = a[0] + (b[0] - a[0]) * t
                my = a[1] + (b[1] - a[1]) * t
                mids2.append(list(push_to_water(mx, my, max_steps=50, step=0.0025)))
            chain = [a] + mids2 + [b]
            for j in range(len(chain) - 1):
                out.extend(densify([chain[j], chain[j + 1]], 10)[1:])
    return out


def simplify_coords(coords: list[list[float]], tol_deg: float = 0.0008) -> list[list[float]]:
    """Douglas-Peucker reduce — re-check land after simplify; fall back if worse."""
    if len(coords) <= 6:
        return coords
    try:
        from shapely.geometry import LineString

        before = interior_land_km(coords)
        ls = LineString(coords)
        simp = ls.simplify(tol_deg, preserve_topology=True)
        out = [list(c) for c in simp.coords]
        if len(out) < 2:
            return coords
        out[0] = list(coords[0])
        out[-1] = list(coords[-1])
        after = interior_land_km(out)
        if after > before + 0.05:
            return coords  # simplify created land cuts
        return out
    except Exception:
        return coords
