#!/usr/bin/env python3
"""BP mint-path city_id stamp — spatial nearest city, never batch context.

Hard-won rule (BP hygiene 2026-07-08/09): RETAG churn regrows when new boarding
points inherit the *partner/market batch* city_id instead of the city nearest
their coordinates. Call `stamp_city_id_from_coords` whenever minting a BP.

Usage:
  from bp_mint_city_id import CityIndex, stamp_city_id_from_coords
  idx = CityIndex.from_routes("data-clean/ROUTES.json")
  city_id = idx.nearest([lng, lat])  # or None if no confident match
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


def haversine_km(a: list[float], b: list[float]) -> float:
    R = 6371.0
    la1, lo1 = math.radians(a[1]), math.radians(a[0])
    la2, lo2 = math.radians(b[1]), math.radians(b[0])
    d = (
        math.sin((la2 - la1) / 2) ** 2
        + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    )
    return 2 * R * math.asin(min(1.0, math.sqrt(d)))


def _median(xs: list[float]) -> float:
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


class CityIndex:
    """Centroid index built from route endpoint city_ids + coordinates."""

    def __init__(self, centroids: dict[str, list[float]], min_members: int = 3):
        self.centroids = centroids
        self.min_members = min_members

    @classmethod
    def from_routes(cls, routes_path: str | Path, min_members: int = 3) -> "CityIndex":
        routes = json.loads(Path(routes_path).read_text())
        if isinstance(routes, dict) and "features" in routes:
            routes = routes["features"]
        by_city: dict[str, list[list[float]]] = defaultdict(list)
        for r in routes:
            p = r.get("properties") or {}
            co = (r.get("geometry") or {}).get("coordinates") or []
            if len(co) < 2:
                continue
            for end, cid_field, coord in (
                ("from", "from_city_id", co[0]),
                ("to", "to_city_id", co[-1]),
            ):
                cid = p.get(cid_field)
                if not cid and p.get(end) and "__" in str(p.get(end)):
                    cid = str(p.get(end)).split("__", 1)[0]
                if cid and isinstance(coord, (list, tuple)) and len(coord) >= 2:
                    by_city[cid].append([float(coord[0]), float(coord[1])])
        centroids = {
            c: [_median([p[0] for p in pts]), _median([p[1] for p in pts])]
            for c, pts in by_city.items()
            if len(pts) >= min_members
        }
        return cls(centroids, min_members=min_members)

    @classmethod
    def from_features(cls, features_path: str | Path) -> "CityIndex":
        """Prefer priority_city / city anchors from FEATURES_BY_TYPE when available."""
        fbt = json.loads(Path(features_path).read_text())
        centroids: dict[str, list[float]] = {}
        for key in ("priority_city", "city"):
            for feat in fbt.get(key) or []:
                p = feat.get("properties") or feat
                cid = p.get("id") or p.get("city_id")
                g = feat.get("geometry") or {}
                co = g.get("coordinates")
                if cid and isinstance(co, (list, tuple)) and len(co) >= 2:
                    centroids[str(cid)] = [float(co[0]), float(co[1])]
        return cls(centroids, min_members=1)

    def nearest(
        self,
        coord: list[float],
        *,
        max_km: float = 60.0,
        forbid_batch_city: str | None = None,
    ) -> str | None:
        """Return nearest city_id within max_km, or None (null beats wrong).

        If forbid_batch_city is set and it is *not* the spatial nearest, it is
        never returned — this is the anti-WS-4 rule.
        """
        if not coord or len(coord) < 2 or not self.centroids:
            return None
        ranked = sorted(
            ((c, haversine_km(coord, ce)) for c, ce in self.centroids.items()),
            key=lambda t: t[1],
        )
        best_c, best_d = ranked[0]
        if best_d > max_km:
            return None
        if forbid_batch_city and best_c != forbid_batch_city:
            # Explicitly reject batch context when spatial disagrees
            return best_c
        return best_c


def stamp_city_id_from_coords(
    bp: dict[str, Any],
    coord: list[float],
    index: CityIndex,
    *,
    batch_city_id: str | None = None,
    max_km: float = 60.0,
) -> dict[str, Any]:
    """Stamp bp['city_id'] / parent_city_id from spatial nearest city.

    Never uses batch_city_id unless it matches the spatial nearest (within max_km).
    """
    nearest = index.nearest(coord, max_km=max_km, forbid_batch_city=batch_city_id)
    if nearest is None:
        bp["city_id"] = None
        bp["_city_id_stamp"] = "null_no_confident_spatial_match"
        bp["_city_id_batch_rejected"] = batch_city_id
    else:
        bp["city_id"] = nearest
        if "parent_city_id" in bp or "parent_city_id" not in bp:
            bp["parent_city_id"] = nearest
        bp["_city_id_stamp"] = "spatial_nearest"
        if batch_city_id and batch_city_id != nearest:
            bp["_city_id_batch_rejected"] = batch_city_id
    return bp


if __name__ == "__main__":
    import sys

    root = Path(__file__).resolve().parents[1]
    idx = CityIndex.from_routes(root / "data-clean/ROUTES.json")
    print(f"centroids: {len(idx.centroids)}")
    if len(sys.argv) >= 3:
        lng, lat = float(sys.argv[1]), float(sys.argv[2])
        batch = sys.argv[3] if len(sys.argv) > 3 else None
        print(idx.nearest([lng, lat], forbid_batch_city=batch))
