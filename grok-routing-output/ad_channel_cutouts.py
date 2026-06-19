#!/usr/bin/env python3
"""Abu Dhabi dredged-channel centerlines + cutout polygons (LB-221 / LB-242)."""
from __future__ import annotations

import math
from shapely.geometry import LineString, Point, Polygon

# Channel half-widths (meters) — dredged fairways / marina approaches
WIDTH_M = {
    "hud_offshore_exit": 500,
    "hud_west_approach": 550,
    "lulu_west_channel": 800,
    "lulu_south_approach": 550,
    "saadiyat_reem_gap": 350,
    "saadiyat_lulu_north": 650,
    "khalifa_coast_approach": 650,
    "khalifa_saadiyat_coast": 550,
    "khalifa_south_exit": 700,
    "yas_north_fairway": 550,
    "yas_marina_approach": 450,
    "emirates_palace_approach": 300,
    "ad_coastal_navigation_lane": 1200,
    "khalifa_offshore_lane": 1000,
    "saadiyat_beach_departure": 500,
}


def m_to_deg(lat: float, m_lon: float, m_lat: float) -> tuple[float, float]:
    return m_lon / (111_000 * math.cos(math.radians(lat))), m_lat / 111_000


def channel_lines() -> dict[str, LineString]:
    """Centerlines for dredged navigable channels (satellite / hand-waypoint informed)."""
    return {
        # Hudayriyat offshore exit toward Gulf fairway
        "hud_offshore_exit": LineString(
            [
                (54.285, 24.430),
                (54.310, 24.445),
                (54.330, 24.452),
                (54.380, 24.470),
            ]
        ),
        # Hudayriyat → west/south fairway → Emirates Palace corridor
        "hud_west_approach": LineString(
            [
                (54.327, 24.419),
                (54.302, 24.402),
                (54.284, 24.428),
                (54.292, 24.452),
                (54.311, 24.465),
            ]
        ),
        # Lulu Island west dredged channel → mainland / EP / Saadiyat north
        "lulu_west_channel": LineString(
            [
                (54.428, 24.546),
                (54.400, 24.530),
                (54.370, 24.510),
                (54.340, 24.495),
                (54.328, 24.488),
                (54.308, 24.468),
                (54.298, 24.458),
            ]
        ),
        # Lulu marina mouth (south-west approach)
        "lulu_south_approach": LineString(
            [
                (54.374, 24.510),
                (54.355, 24.502),
                (54.344, 24.501),
            ]
        ),
        # Narrow gap Saadiyat ↔ Reem Island (west of marina jetty)
        "saadiyat_reem_gap": LineString(
            [
                (54.414, 24.518),
                (54.403, 24.502),
                (54.403, 24.492),
                (54.399, 24.484),
            ]
        ),
        # Saadiyat Beach Club → Lulu north fairway (stops short of Lulu jetty)
        "saadiyat_lulu_north": LineString(
            [
                (54.450, 24.558),
                (54.400, 24.530),
                (54.360, 24.508),
                (54.348, 24.504),
            ]
        ),
        # Khalifa Port → south along Taweelah coast (starts offshore S of jetty)
        "khalifa_coast_approach": LineString(
            [
                (54.658, 24.795),
                (54.665, 24.760),
                (54.645, 24.620),
                (54.640, 24.550),
                (54.620, 24.520),
            ]
        ),
        # North of Yas Island fairway (Hud/Khalifa → Yas Marina)
        "yas_north_fairway": LineString(
            [
                (54.520, 24.505),
                (54.555, 24.495),
                (54.585, 24.485),
                (54.609, 24.476),
            ]
        ),
        # Khalifa / Taweelah → Saadiyat north coast fairway
        "khalifa_saadiyat_coast": LineString(
            [
                (54.645, 24.620),
                (54.560, 24.565),
                (54.480, 24.558),
                (54.455, 24.558),
            ]
        ),
        # Emirates Palace marina mouth
        "emirates_palace_approach": LineString(
            [
                (54.298, 24.458),
                (54.305, 24.462),
                (54.311, 24.465),
            ]
        ),
        # Offshore coastal navigation lane (Hud → Yas / Saadiyat fairway)
        "ad_coastal_navigation_lane": LineString(
            [
                (54.285, 24.430),
                (54.330, 24.455),
                (54.400, 24.475),
                (54.480, 24.478),
                (54.550, 24.476),
                (54.600, 24.476),
            ]
        ),
        # Khalifa / Taweelah → Saadiyat offshore descent
        "khalifa_offshore_lane": LineString(
            [
                (54.665, 24.770),
                (54.650, 24.680),
                (54.620, 24.600),
                (54.580, 24.565),
                (54.520, 24.560),
                (54.460, 24.558),
            ]
        ),
        # Khalifa Port jetty → south-east offshore (Taweelah fairway)
        "khalifa_south_exit": LineString(
            [
                (54.651, 24.808),
                (54.648, 24.800),
                (54.642, 24.790),
                (54.634, 24.780),
                (54.634, 24.720),
            ]
        ),
        # Yas Marina north fairway approach
        "yas_marina_approach": LineString(
            [
                (54.570, 24.478),
                (54.590, 24.478),
                (54.606, 24.481),
                (54.609, 24.476),
            ]
        ),
        # Saadiyat Beach Club jetty → north channel
        "saadiyat_beach_departure": LineString(
            [
                (54.450, 24.558),
                (54.448, 24.560),
                (54.440, 24.562),
                (54.422, 24.544),
            ]
        ),
    }


def channel_cutout_polygons() -> list[Polygon]:
    """Buffered channel corridors to subtract from land union (= water holes)."""
    polys: list[Polygon] = []
    for name, line in channel_lines().items():
        lat = sum(c[1] for c in line.coords) / len(line.coords)
        half_w = WIDTH_M.get(name, 400)
        d_lon, d_lat = m_to_deg(lat, half_w, half_w)
        # buffer in degrees — approximate circle via avg
        buf_deg = (d_lon + d_lat) / 2
        poly = line.buffer(buf_deg, cap_style=2, join_style=2)
        if not poly.is_empty:
            polys.append(poly)
    return polys


def jetty_core_polys() -> list[Polygon]:
    """Small land cores so marina jetties stay LAND after channel subtraction."""
    cores: list[Polygon] = []
    for lon, lat, radius_m in [
        (54.327324, 24.418703, 90),   # Hudayriyat Bab Al Nojoum
        (54.651205, 24.808029, 120),  # Khalifa Port
        (54.344343, 24.501337, 100),  # Lulu Island
        (54.419171, 24.521702, 100),  # Saadiyat Marina
        (54.449803, 24.558459, 90),   # Saadiyat Beach Club
        (54.401147, 24.484583, 90),   # Reem waterfront
        (54.310704, 24.465079, 90),   # Emirates Palace Marina
        (54.609265, 24.475629, 100),  # Yas Marina
    ]:
        d_lon, d_lat = m_to_deg(lat, radius_m, radius_m)
        cores.append(Point(lon, lat).buffer((d_lon + d_lat) / 2))
    return cores


def refined_reclamation_polys():
    """Smaller reclamation footprints — leave room for dredged channels."""
    from shapely.geometry import Polygon
    from shapely.validation import make_valid

    def box(w, s, e, n):
        return make_valid(Polygon([(w, s), (e, s), (e, n), (w, n), (w, s)]))

    return [
        box(54.318, 24.412, 54.342, 24.438),   # Hudayriyat core (west channel open)
        box(54.638, 24.792, 54.668, 24.818),   # Khalifa Port core
        box(54.348, 24.502, 54.355, 24.514),   # Lulu east fill (west channel open)
        box(54.418, 24.528, 54.448, 24.558),   # Saadiyat north / beach club
        box(54.412, 24.518, 54.432, 24.532),   # Saadiyat marina pocket
        box(54.397, 24.480, 54.408, 24.493),   # Reem waterfront (gap west)
    ]