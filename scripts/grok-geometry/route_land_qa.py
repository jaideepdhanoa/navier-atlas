#!/usr/bin/env python3
"""Canonical Grok land QA — coarse global_land_mask + regional overlays (UAE v2)."""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
UAE_WKB = ROOT / "grok-routing-output" / "uae_gulf_land_v2.wkb"
UAE_BBOX = (50.0, 21.5, 57.5, 26.8)  # lon min, lat min, lon max, lat max
THRESH_KM = 0.05
APRON_KM = 0.12
R_EARTH_KM = 6371.0088

_overlay = None
_coarse = None


def _hav_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def load_coarse_mask():
    global _coarse
    if _coarse is not None:
        return _coarse
    try:
        from global_land_mask import globe
        _coarse = globe
    except Exception:
        _coarse = None
    return _coarse


def load_uae_overlay():
    global _overlay
    if _overlay is not None:
        return _overlay
    if not UAE_WKB.exists():
        _overlay = None
        return None
    try:
        from shapely import wkb
        from shapely.geometry import Point
        from shapely.prepared import prep

        geom = wkb.loads(UAE_WKB.read_bytes())
        _overlay = prep(geom)
        _overlay._point_cls = Point  # type: ignore[attr-defined]
    except Exception:
        _overlay = None
    return _overlay


def in_uae_bbox(lon: float, lat: float) -> bool:
    return UAE_BBOX[0] <= lon <= UAE_BBOX[2] and UAE_BBOX[1] <= lat <= UAE_BBOX[3]


def point_is_land(lon: float, lat: float, *, coarse=None, uae=None) -> bool:
    if uae is not None and in_uae_bbox(lon, lat):
        try:
            from shapely.geometry import Point
            return bool(uae.intersects(Point(lon, lat)))
        except Exception:
            pass
    if coarse is None:
        coarse = load_coarse_mask()
    if coarse is None:
        return False
    try:
        return bool(coarse.is_land(lat, lon))
    except Exception:
        return False


def coords_of(feature: dict) -> list[list[float]]:
    g = feature.get("geometry") or {}
    if g.get("type") != "LineString":
        return []
    return g.get("coordinates") or []


def interior_land_km(
    coords: list,
    *,
    coarse=None,
    uae=None,
    step_km: float = 0.05,
    apron_km: float = APRON_KM,
    thresh_bbox: tuple | None = None,
) -> float:
    if len(coords) < 2:
        return 0.0
    if coarse is None:
        coarse = load_coarse_mask()
    if uae is None:
        uae = load_uae_overlay()
    cum = 0.0
    samples: list[tuple[float, float, float, float]] = []
    for i in range(1, len(coords)):
        a = (coords[i - 1][0], coords[i - 1][1])
        b = (coords[i][0], coords[i][1])
        seg_km = _hav_km(a, b)
        if seg_km <= 0:
            continue
        n = max(1, int(seg_km / step_km))
        for k in range(1, n + 1):
            t = k / n
            lon = a[0] + (b[0] - a[0]) * t
            lat = a[1] + (b[1] - a[1]) * t
            if thresh_bbox:
                lo, la, hi, ha = thresh_bbox
                if not (lo <= lon <= hi and la <= lat <= ha):
                    continue
            samples.append((lon, lat, cum + seg_km * t, seg_km / n))
        cum += seg_km
    total = cum
    bad = 0.0
    for lon, lat, c, d in samples:
        if c < apron_km or c > total - apron_km:
            continue
        if point_is_land(lon, lat, coarse=coarse, uae=uae):
            bad += d
    return bad


def evaluate_route(
    coords: list,
    *,
    sea_nm: float | None = None,
    step_km: float | None = None,
) -> dict[str, Any]:
    if not coords or len(coords) < 2:
        return {"interior_land_km": 0.0, "qa_pass": True, "mask": "none"}
    if step_km is None:
        if sea_nm is None:
            sea_nm = sum(
                _hav_km((coords[i - 1][0], coords[i - 1][1]), (coords[i][0], coords[i][1]))
                for i in range(1, len(coords))
            ) / 1.852
        step_km = 0.15 if sea_nm > 30 else 0.05
    land_km = interior_land_km(coords, step_km=step_km)
    uae_used = any(in_uae_bbox(c[0], c[1]) for c in coords)
    return {
        "interior_land_km": round(land_km, 4),
        "qa_pass": land_km <= THRESH_KM,
        "mask": "uae_v2+coarse" if uae_used and load_uae_overlay() else "coarse",
        "threshold_km": THRESH_KM,
    }


def evaluate_feature(feature: dict) -> dict[str, Any]:
    coords = coords_of(feature)
    props = feature.get("properties") or {}
    sea_nm = props.get("distance_nm_geom") or props.get("distance_nm")
    return evaluate_route(coords, sea_nm=sea_nm)


def qa_pass(coords: list, *, sea_nm: float | None = None) -> bool:
    return evaluate_route(coords, sea_nm=sea_nm)["qa_pass"]