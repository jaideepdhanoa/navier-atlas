#!/usr/bin/env python3
"""Regional water refinements — override coarse global_land_mask false positives."""
from __future__ import annotations

from functools import lru_cache

# (name, lon_min, lat_min, lon_max, lat_max) — force water inside bbox
WATER_BBOXES: list[tuple[str, float, float, float, float]] = [
    # Upper Gulf of Thailand ferry corridor (Bangkok ↔ Pattaya ↔ Hua Hin)
    ("gulf_thailand_upper", 100.35, 11.15, 101.55, 13.85),
    # Chao Phraya river transit lane (Bangkok ICONSIAM → Gulf mouth)
    ("chao_phraya_bangkok", 100.48, 13.05, 100.62, 13.78),
    # Pattaya ↔ Koh Samet crossing
    ("gulf_thailand_samet", 100.82, 12.45, 101.52, 12.95),
    # Table Bay (V&A ↔ Robben Island)
    ("table_bay_cape_town", 18.25, -33.95, 18.50, -33.75),
    # False Bay north shore channel (Hout Bay ↔ Simon's Town arc)
    ("false_bay_cape_town", 18.15, -34.35, 18.55, -34.05),
    # Ionian protected channel (Corfu ↔ Paxos)
    ("ionian_corfu", 20.45, 38.65, 20.85, 39.25),
    # Hong Kong ↔ Macau ferry lane
    ("hk_macau_channel", 113.75, 22.12, 114.05, 22.35),
    # Victoria Harbour + eastern approaches
    ("hong_kong_harbour", 114.05, 22.24, 114.25, 22.35),
    # Ha Long / Lan Ha / Cat Ba archipelago ferry lanes
    ("ha_long_bay", 106.80, 20.50, 107.60, 21.00),
    # Aegean Cyclades open-water corridor (Mykonos ↔ Santorini arc)
    ("aegean_cyclades", 24.80, 36.30, 26.20, 37.80),
    # Dalmatian coast channels (Split ↔ Dubrovnik)
    ("dalmatia_croatia", 15.80, 42.55, 18.50, 43.85),
    # Puget Sound / San Juan ferry lanes
    ("puget_sound", -123.30, 47.50, -122.25, 48.80),
    # Boston harbour + outer islands
    ("boston_harbour", -71.15, 42.30, -70.05, 42.85),
    # Sydney Harbour approaches
    ("sydney_harbour", 151.15, -33.92, 151.35, -33.78),
    # Bonifacio Strait (Corsica ↔ Sardinia)
    ("bonifacio_strait", 8.65, 41.25, 9.50, 41.95),
    # Douro estuary (Porto ↔ Gaia)
    ("douro_porto", -8.75, 41.10, -8.55, 41.20),
    # Raja Ampat / Ceram passages
    ("raja_ampat", 129.50, -5.00, 131.50, -0.30),
    # Leeward Islands ferry lanes
    ("leeward_caribbean", -65.00, 17.80, -62.80, 18.50),
    # Dutch Caribbean ABC (Aruba · Curaçao · Bonaire) coastal + inter-island lanes
    ("abc_islands", -70.15, 11.85, -68.10, 12.65),
    # Dubai Creek / Palm lagoon approaches
    ("dubai_coast", 54.95, 24.95, 55.35, 25.35),
    # Lagos Lagoon
    ("lagos_lagoon", 3.30, 6.35, 3.55, 6.50),
    # River Thames / estuary ferry lanes
    ("thames_london", -0.30, 51.44, 0.05, 51.58),
    # Krabi / Phang Nga shallow bay corridors
    ("krabi_andaman", 97.60, 7.50, 99.00, 8.95),
    # New York Harbor + East River
    ("ny_harbor", -74.20, 40.60, -73.90, 40.88),
    # Bora Bora / Society lagoon passages
    ("bora_bora_lagoon", -152.30, -17.55, -149.50, -16.40),
    # Nicoya / Papagayo gulf ferry lanes
    ("nicoya_gulf", -86.00, 9.35, -84.10, 10.70),
    # Kerala backwaters / Vembanad
    ("kerala_backwaters", 76.20, 9.40, 76.55, 10.20),
    # Abidjan lagoon
    ("abidjan_lagoon", -4.10, 5.20, -3.85, 5.45),
    # Ras Al Khaimah coast / creek
    ("rak_uae_coast", 55.45, 25.55, 56.10, 26.05),
    # Vancouver inner harbour + Georgia Strait
    ("vancouver_harbour", -123.35, 49.10, -122.85, 49.35),
    # Samaná Bay DR
    ("samana_bay", -69.70, 19.10, -69.05, 19.35),
    # Goa / Mandovi estuary
    ("goa_estuary", 73.75, 15.35, 74.15, 15.55),
    # Andaman shallow channels
    ("andaman_india", 92.50, 10.50, 93.20, 12.00),
    # San Blas archipelago
    ("san_blas_panama", -79.20, 8.80, -77.80, 9.60),
    # Jeju Strait
    ("jeju_strait", 126.10, 33.00, 126.95, 33.60),
    # Tuscan Archipelago ferry lanes
    ("tuscan_archipelago", 9.75, 42.60, 10.35, 43.05),
    # Koh Phangan / Samui crossings
    ("gulf_thailand_samui", 99.70, 9.30, 100.15, 10.15),
    # Rhodes / Dodecanese channels
    ("dodecanese_greece", 27.80, 36.20, 28.45, 36.90),
    # Red Sea NEOM / coastal corridor
    ("red_sea_ksa", 34.50, 25.20, 37.20, 28.20),
]

# Simplified land exclusions inside water bboxes (lon, lat vertices)
LAND_EXCLUSIONS: list[tuple[str, list[tuple[float, float]]]] = [
    (
        "gulf_thailand_upper",
        [
            (100.15, 12.45), (100.45, 12.35), (100.75, 12.55), (100.92, 12.78),
            (100.88, 13.05), (100.55, 13.55), (100.35, 13.35), (100.15, 12.85),
        ],
    ),
    (
        "gulf_thailand_samet",
        [(101.38, 12.48), (101.48, 12.52), (101.46, 12.62), (101.36, 12.58)],
    ),
]


@lru_cache(maxsize=1)
def _land_polys():
    try:
        from shapely.geometry import Polygon

        return {
            name: Polygon(verts)
            for name, verts in LAND_EXCLUSIONS
        }
    except Exception:
        return {}


def in_water_override(lon: float, lat: float) -> bool:
    """True when coarse land should be treated as water (shallow sea / ferry lane)."""
    for name, lo, la, hi, ha in WATER_BBOXES:
        if not (lo <= lon <= hi and la <= lat <= ha):
            continue
        land = _land_polys().get(name)
        if land is not None:
            try:
                from shapely.geometry import Point

                if land.contains(Point(lon, lat)):
                    continue
            except Exception:
                pass
        return True
    return False