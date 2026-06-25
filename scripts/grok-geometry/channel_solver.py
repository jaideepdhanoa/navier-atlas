#!/usr/bin/env python3
"""A* channel solver — UAE v2 grid + coarse global mask (ported from solve_routes_phase2)."""
from __future__ import annotations

import heapq
import json
import math
from pathlib import Path
from typing import Any

from shapely import wkb
from shapely.geometry import Point
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "grok-routing-output"
WKB_V2 = OUT / "uae_gulf_land_v2.wkb"
SEAWARD = OUT / "seaward-candidates.json"
GRID_CACHE = OUT / "land_grid_0.02.npy"
GRID_META = OUT / "land_grid_meta.json"

R_NM = 3440.065
LAND_TOL_KM = 0.05
LB224_MARINA_APRON_KM = 0.12
UAE_BBOX = (50.0, 21.5, 57.5, 26.8)

def _waypoint_lookup(from_id: str, to_id: str) -> list[list[float]] | None:
    key = (from_id, to_id)
    rev = (to_id, from_id)
    if key in HAND_WAYPOINTS:
        return HAND_WAYPOINTS[key]
    if rev in HAND_WAYPOINTS:
        return list(reversed(HAND_WAYPOINTS[rev]))
    return None


def hand_waypoints_for(
    from_id: str | None,
    to_id: str | None,
    *,
    from_city_id: str | None = None,
    to_city_id: str | None = None,
) -> list[list[float]] | None:
    """Bidirectional lookup — tries POI ids, city ids, and cross pairs."""
    pairs: list[tuple[str, str]] = []
    for a, b in (
        (from_id, to_id),
        (from_city_id, to_city_id),
        (from_id, to_city_id),
        (from_city_id, to_id),
    ):
        if a and b and (a, b) not in pairs:
            pairs.append((a, b))
    for a, b in pairs:
        wps = _waypoint_lookup(a, b)
        if wps:
            return wps
    return None


HAND_WAYPOINTS: dict[tuple[str, str], list[list[float]]] = {
    ("dxb-zabeel-saray", "dxb-rixos-palm"): [[55.115, 25.105], [55.141, 25.100], [55.141, 25.118], [55.158, 25.120], [55.152, 25.113]],
    ("dxb-palm-west-beach", "dxb-five-palm"): [[55.145, 25.103]],
    ("ad-hudayriyat-bab-al-nojoum", "ad-emirates-palace-marina"): [[54.300, 24.405], [54.285, 24.430], [54.295, 24.455]],
    ("ad-hudayriyat-bab-al-nojoum", "ad-yas-marina"): [
        [54.300, 24.405], [54.285, 24.430], [54.308, 24.432], [54.336, 24.448],
        [54.372, 24.460], [54.426, 24.472], [54.498, 24.478], [54.570, 24.478],
        [54.6063, 24.4808],
    ],
    ("ad-khalifa-port", "ad-yas-marina"): [[54.639, 24.730], [54.657, 24.516], [54.627, 24.480]],
    ("ad-khalifa-port", "ad-saadiyat-beach-club"): [
        [54.630, 24.780], [54.564, 24.714], [54.492, 24.618], [54.474, 24.594],
        [54.490, 24.602], [54.462, 24.582],
    ],
    ("ad-lulu-island", "ad-emirates-palace-marina"): [[54.330, 24.490], [54.305, 24.470], [54.300, 24.460]],
    ("ad-saadiyat-marina", "ad-reem-island"): [[54.414, 24.518], [54.403, 24.502], [54.403, 24.492]],
    ("ad-saadiyat-beach-club", "ad-lulu-island"): [[54.428, 24.546], [54.3413, 24.5013]],
    ("abu-dhabi-uae", "doha-qatar"): [[54.85, 25.60], [53.85, 25.60], [52.85, 25.55], [52.05, 25.45], [51.62, 25.33]],
    ("bp-2f3e3c22fa", "bp-80adfa36b4"): [[51.52, 25.55], [51.53, 25.45]],
    ("bp-08b9b97bec", "bp-b10aba6c16"): [[56.275, 25.68], [56.270, 25.665]],
    ("abu-dhabi-uae", "bp-ed4ac4b266"): [[54.335, 24.452]],
    ("bp-2d105c5127", "bp-f377aadba6"): [[56.366, 25.516]],
    ("bp-8e8a497a21", "bp-e22806d1fa"): [[54.460, 24.538]],
    ("bp-ed4ac4b266", "bp-6846d27fcc"): [[54.329, 24.454]],
    ("bp-f377aadba6", "bp-3d9055c24e"): [[56.365, 25.514]],
    ("bp-7e3e3ac47c", "bp-7c9cd1a243"): [[55.842, 25.720]],
    # Cape Town lagoon mesh (Table Bay + False Bay arcs)
    ("bp-41c1d22c88", "bp-c07f712484"): [[18.40, -33.84]],
    ("bp-41c1d22c88", "bp-6572ae8691"): [[18.43, -33.91], [18.39, -33.96], [18.36, -34.01]],
    ("bp-6572ae8691", "bp-0682568ae1"): [[18.349, -34.052]],
    ("bp-6572ae8691", "bp-17cbbdad38"): [[18.32, -34.12], [18.38, -34.22], [18.44, -34.20]],
    ("bp-41c1d22c88", "bp-5fa23ee16d"): [[18.50, -33.90], [18.58, -33.98], [18.68, -34.06], [18.78, -34.12], [18.86, -34.15]],
    # East Africa channel corridors (v2)
    ("dar-es-salaam-tanzania", "zanzibar-tanzania"): [[39.45, -6.85], [39.35, -6.55], [39.20, -6.25]],
    ("mombasa-kenya", "diani-ukunda-kenya"): [[39.72, -4.10], [39.65, -4.18], [39.60, -4.24]],
    ("mombasa-kenya", "kilifi-kenya"): [[39.78, -3.92], [39.85, -3.78], [39.88, -3.68]],
    ("zanzibar-tanzania", "pemba-tanzania"): [[39.50, -5.95], [39.62, -5.65], [39.72, -5.38]],
    ("dar-es-salaam-tanzania", "mafia-tanzania"): [[39.55, -7.05], [39.65, -7.35], [39.72, -7.70]],
    # Portugal Tagus → Algarve (offshore Atlantic shelf; excl. inland Algarve)
    ("bp-terreiro-do-paco-lisbon", "bp-ponta-da-piedade"): [
        [-9.25, 38.72], [-9.10, 38.55], [-8.95, 38.35], [-8.82, 38.10],
        [-8.75, 37.85], [-8.72, 37.55], [-8.71, 37.25], [-8.72, 37.10],
    ],
    # Chicago Lake Michigan ferry
    ("chicago-lake-michigan-usa__dusable-harbor-chicago", "chicago-lake-michigan-usa__new-buffalo-municipal-marina"): [
        [-87.55, 41.85], [-87.20, 41.95], [-86.85, 42.05], [-86.55, 42.15],
    ],
    # Komodo ↔ Lombok open Flores Sea
    ("bp-fa2c2875fa", "bp-3497837a7b"): [
        [119.40, -8.55], [118.80, -8.45], [118.20, -8.40], [117.60, -8.42],
        [117.00, -8.48], [116.50, -8.55],
    ],
    # Istanbul Bosphorus long arc (Sea of Marmara offshore)
    ("bp-5654d9cdd3", "bp-84f50d4224"): [
        [29.00, 41.05], [29.50, 41.10], [30.20, 41.05], [31.00, 40.95],
        [32.00, 40.85], [33.50, 40.75], [35.00, 40.65],
    ],
    # Andaman India coastal shelf
    ("bp-7f1d145a12", "bp-87802f7406"): [
        [92.80, 11.20], [92.95, 11.00], [93.05, 10.75], [93.10, 10.55],
    ],
}

_lc_singleton: "LandChecker | None" = None
_seaward_cache: dict | None = None


def hav_nm(a, b) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_NM * math.asin(min(1.0, math.sqrt(h)))


def hav_km(a, b) -> float:
    return hav_nm(a, b) * 1.852


class LandChecker:
    """UAE v2 STRtree grid + coarse global mask."""

    def __init__(self, wkb_path: Path, coarse=None, res_deg: float = 0.02):
        import numpy as np

        geom = wkb.loads(wkb_path.read_bytes())
        self.polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
        self.tree = STRtree(self.polys)
        self.coarse = coarse
        self.W, self.S, self.E, self.N = UAE_BBOX
        self.res = res_deg
        self.nx = int((self.E - self.W) / res_deg) + 1
        self.ny = int((self.N - self.S) / res_deg) + 1
        if GRID_CACHE.exists() and GRID_META.exists():
            m = json.loads(GRID_META.read_text())
            if m.get("res") == res_deg and m.get("nx") == self.nx:
                self.grid = np.load(GRID_CACHE)
                return
        self.grid = np.zeros((self.ny, self.nx), dtype=bool)
        for j in range(self.ny):
            lat = self.S + j * res_deg
            for i in range(self.nx):
                lon = self.W + i * res_deg
                pt = Point(lon, lat)
                for idx in self.tree.query(pt):
                    if self.polys[idx].contains(pt):
                        self.grid[j, i] = True
                        break
        np.save(GRID_CACHE, self.grid)
        GRID_META.write_text(json.dumps({"res": res_deg, "nx": self.nx, "ny": self.ny}))

    def _in_uae(self, lon: float, lat: float) -> bool:
        return self.W <= lon <= self.E and self.S <= lat <= self.N

    def is_land(self, lat: float, lon: float) -> bool:
        try:
            from regional_land_masks import in_water_override

            if in_water_override(lon, lat):
                return False
        except Exception:
            pass
        if self._in_uae(lon, lat):
            i = int((lon - self.W) / self.res)
            j = int((lat - self.S) / self.res)
            i = min(self.nx - 1, max(0, i))
            j = min(self.ny - 1, max(0, j))
            return bool(self.grid[j, i])
        if self.coarse is not None:
            try:
                return bool(self.coarse.is_land(lat, lon))
            except Exception:
                pass
        return False


def get_land_checker() -> LandChecker:
    global _lc_singleton
    if _lc_singleton is None:
        try:
            from global_land_mask import globe as coarse
        except Exception:
            coarse = None
        _lc_singleton = LandChecker(WKB_V2, coarse=coarse)
    return _lc_singleton


def load_seaward() -> dict:
    global _seaward_cache
    if _seaward_cache is None:
        _seaward_cache = json.loads(SEAWARD.read_text()) if SEAWARD.exists() else {}
    return _seaward_cache


def densify(seq: list, step_nm: float = 0.25) -> list[list[float]]:
    arc: list[list[float]] = []
    for i in range(len(seq) - 1):
        p, q = seq[i], seq[i + 1]
        leg = hav_nm(p, q)
        n = max(2, min(300, int(leg / step_nm) + 1))
        seg = [[p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n] for k in range(n + 1)]
        arc.extend(seg[1:] if i else seg)
    return arc


def leg_clear(lc: LandChecker, p, q, step_nm: float = 0.2) -> bool:
    leg = hav_nm(p, q)
    n = max(2, int(leg / step_nm) + 1)
    for k in range(1, n):
        x = p[0] + (q[0] - p[0]) * k / n
        y = p[1] + (q[1] - p[1]) * k / n
        if lc.is_land(y, x):
            return False
    return True


def astar(lc: LandChecker, wa, wb, res: float = 0.003, pad: float = 0.2) -> list | None:
    minx = min(wa[0], wb[0]) - pad
    maxx = max(wa[0], wb[0]) + pad
    miny = min(wa[1], wb[1]) - pad
    maxy = max(wa[1], wb[1]) + pad
    span = max(maxx - minx, maxy - miny)
    if span > 3.0:
        res = max(res, span / 200)
    nx = min(350, int((maxx - minx) / res) + 1)
    ny = min(350, int((maxy - miny) / res) + 1)
    res_x = (maxx - minx) / max(1, nx - 1)
    res_y = (maxy - miny) / max(1, ny - 1)

    def to_pt(c):
        return [minx + c[0] * res_x, miny + c[1] * res_y]

    def to_cell(p):
        return (
            min(nx - 1, max(0, int((p[0] - minx) / res_x))),
            min(ny - 1, max(0, int((p[1] - miny) / res_y))),
        )

    def ocean(c):
        x, y = to_pt(c)
        return not lc.is_land(y, x)

    def nearest_ocean(c):
        if ocean(c):
            return c
        for rad in range(1, 50):
            for dx in range(-rad, rad + 1):
                for dy in range(-rad, rad + 1):
                    if max(abs(dx), abs(dy)) != rad:
                        continue
                    cc = (c[0] + dx, c[1] + dy)
                    if 0 <= cc[0] < nx and 0 <= cc[1] < ny and ocean(cc):
                        return cc
        return None

    start = nearest_ocean(to_cell(wa))
    goal = nearest_ocean(to_cell(wb))
    if not start or not goal:
        return None

    def h(c):
        return math.hypot(c[0] - goal[0], c[1] - goal[1])

    openh = [(h(start), 0.0, start)]
    came: dict = {}
    g = {start: 0.0}
    nbrs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    while openh:
        _, gc, c = heapq.heappop(openh)
        if c == goal:
            path = [c]
            while c in came:
                c = came[c]
                path.append(c)
            return [to_pt(cc) for cc in reversed(path)]
        if gc > g.get(c, 1e18):
            continue
        for dx, dy in nbrs:
            nc = (c[0] + dx, c[1] + dy)
            if not (0 <= nc[0] < nx and 0 <= nc[1] < ny) or not ocean(nc):
                continue
            ng = gc + math.hypot(dx, dy)
            if ng < g.get(nc, 1e18):
                g[nc] = ng
                came[nc] = c
                heapq.heappush(openh, (ng + h(nc), ng, nc))
    return None


def simplify(lc: LandChecker, path: list) -> list:
    if len(path) <= 2:
        return path
    out = [path[0]]
    i = 0
    while i < len(path) - 1:
        j = len(path) - 1
        while j > i + 1 and not leg_clear(lc, out[-1], path[j]):
            j -= 1
        out.append(path[j])
        i = j
    return out


def connect_chain(lc: LandChecker, pts: list) -> list | None:
    full: list = []
    for i in range(len(pts) - 1):
        seg = astar(lc, pts[i], pts[i + 1])
        if not seg:
            return None
        simp = simplify(lc, seg)
        full.extend(simp if not full else simp[1:])
    return simplify(lc, full) if full else None


def gen_anchors(lc: LandChecker, pt, max_nm: float = 1.5, preferred=None) -> list:
    cands = []
    if preferred and not lc.is_land(preferred[1], preferred[0]):
        cands.append((hav_nm(pt, preferred), preferred))
    if not lc.is_land(pt[1], pt[0]):
        cands.append((0.0, pt))
    for r in (0.003 * k for k in range(1, 40)):
        for da in range(0, 360, 15):
            p = [pt[0] + r * math.cos(math.radians(da)), pt[1] + r * math.sin(math.radians(da))]
            if not lc.is_land(p[1], p[0]):
                d = hav_nm(pt, p)
                if d <= max_nm:
                    cands.append((d, p))
    seen = set()
    uniq = []
    for _, p in sorted(cands):
        key = (round(p[0], 4), round(p[1], 4))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(p)
    return uniq[:8]


def offset_point(origin, az_deg: float, dist_m: float) -> list[float]:
    r = 6378137.0
    az = math.radians(az_deg)
    lat = math.radians(origin[1])
    lon = math.radians(origin[0])
    ang = dist_m / r
    lat2 = math.asin(math.sin(lat) * math.cos(ang) + math.cos(lat) * math.sin(ang) * math.cos(az))
    lon2 = lon + math.atan2(
        math.sin(az) * math.sin(ang) * math.cos(lat),
        math.cos(ang) - math.sin(lat) * math.sin(lat2),
    )
    return [math.degrees(lon2), math.degrees(lat2)]


def pack_result(lc: LandChecker, dd: list, method: str, max_sinuosity: float = 1.6) -> dict | None:
    from route_land_qa import evaluate_route

    geom = densify(dd)
    ev = evaluate_route(geom)
    land_km = ev["interior_land_km"]
    gc = hav_km(dd[0], dd[-1])
    total = sum(hav_km(dd[i - 1], dd[i]) for i in range(1, len(dd)))
    sinu = round(total / gc, 3) if gc > 0 else 1.0
    if method != "hand_waypoints" and land_km > LAND_TOL_KM:
        return None
    if sinu > max_sinuosity and method != "hand_waypoints":
        return None
    sea_nm = sum(hav_nm(dd[i], dd[i + 1]) for i in range(len(dd) - 1))
    return {
        "waypoints": [[round(p[0], 5), round(p[1], 5)] for p in dd[1:-1]],
        "geometry": geom,
        "interior_land_km": land_km,
        "sinuosity": sinu,
        "sea_nm": round(sea_nm, 2),
        "method": method,
        "qa_pass": ev["qa_pass"],
    }


def solve_hand(lc: LandChecker, a, b, mids: list, method: str = "hand_waypoints") -> dict | None:
    dd = [a] + mids + [b]
    if mids:
        if not leg_clear(lc, a, mids[0]):
            for p in gen_anchors(lc, a, max_nm=2.0)[:6]:
                if leg_clear(lc, a, p) and leg_clear(lc, p, mids[0]):
                    dd = [a, p] + mids + [b]
                    break
        if not leg_clear(lc, dd[-2], b):
            for p in gen_anchors(lc, b, max_nm=2.0)[:6]:
                if leg_clear(lc, p, b) and leg_clear(lc, dd[-2], p):
                    dd = dd[:-1] + [p, b]
                    break
    res = pack_result(lc, dd, method, max_sinuosity=2.5)
    if res and res["qa_pass"]:
        return res
    path = connect_chain(lc, dd)
    if not path:
        return None
    full = [a] + [p for p in path if p != a and p != b] + [b]
    dd2 = [full[0]]
    for p in full[1:]:
        if p != dd2[-1]:
            dd2.append(p)
    dd2 = [[round(p[0], 5), round(p[1], 5)] for p in dd2]
    res = pack_result(lc, dd2, method, max_sinuosity=2.5)
    return res if res and res["qa_pass"] else None


def solve_chain(lc: LandChecker, a, b, mids=None, anchors=None) -> dict | None:
    mids = mids or []
    pref_a = anchors.get("from") if anchors else None
    pref_b = anchors.get("to") if anchors else None
    aa = gen_anchors(lc, a, preferred=pref_a)
    bb = gen_anchors(lc, b, preferred=pref_b)
    if not aa or not bb:
        return None
    best = None
    for ca in aa[:2]:
        for cb in bb[:2]:
            pts = [a]
            if ca != a:
                pts.append(ca)
            pts.extend(mids)
            if cb != b:
                pts.append(cb)
            pts.append(b)
            dd = [pts[0]]
            for p in pts[1:]:
                if [round(p[0], 5), round(p[1], 5)] != [round(dd[-1][0], 5), round(dd[-1][1], 5)]:
                    dd.append(p)
            path = connect_chain(lc, dd)
            if not path:
                continue
            full = [a] + [p for p in path if p != a and p != b] + [b]
            dd2 = [full[0]]
            for p in full[1:]:
                if p != dd2[-1]:
                    dd2.append(p)
            cand = pack_result(lc, dd2, "a_star_v2")
            if cand and cand["qa_pass"] and (best is None or len(dd2) < len(best.get("_dd", []))):
                cand["_dd"] = dd2
                best = cand
        if best:
            break
    if best:
        best.pop("_dd", None)
    return best


def fast_nudge_solve(lc: LandChecker, a, b, anchors=None) -> dict | None:
    anchors = anchors or {}
    trials = [[a, b]]
    mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
    for az in range(0, 360, 30):
        for dist_m in (800, 1500, 3000, 5000, 8000):
            wp = offset_point(mid, az, dist_m)
            trials.append([a, wp, b])
            if anchors.get("from"):
                trials.append([a, anchors["from"], wp, b])
            if anchors.get("to"):
                trials.append([a, wp, anchors["to"], b])
    leg_nm = hav_nm(a, b)
    if leg_nm > 30:
        for frac in (0.33, 0.66):
            p = [a[0] + frac * (b[0] - a[0]), a[1] + frac * (b[1] - a[1])]
            for az in range(0, 360, 45):
                wp = offset_point(p, az, 5000)
                trials.append([a, wp, b])
    best = None
    for dd in trials:
        dd2 = [dd[0]]
        for p in dd[1:]:
            if p != dd2[-1]:
                dd2.append(p)
        cand = pack_result(lc, dd2, "coast_normal")
        if cand and cand["qa_pass"] and (best is None or cand["sea_nm"] < best["sea_nm"]):
            best = cand
    return best


def solve_endpoints(
    a: list[float],
    b: list[float],
    *,
    from_id: str | None = None,
    to_id: str | None = None,
    lc: LandChecker | None = None,
    dist_nm: float | None = None,
    story_mode: bool = False,
) -> dict[str, Any] | None:
    """Solve water path between two lon/lat endpoints."""
    lc = lc or get_land_checker()
    if dist_nm is None:
        dist_nm = hav_nm(a, b)

    wps = hand_waypoints_for(from_id, to_id)
    if wps:
        res = solve_hand(lc, a, b, wps)
        if res:
            return res

    seaward = load_seaward()
    anchors: dict[str, list] = {}
    mids: list = []
    for side, bp_id in [("from", from_id), ("to", to_id)]:
        if not bp_id:
            continue
        sc = seaward.get("candidates", {}).get(bp_id, {})
        if sc.get("seaward_coord"):
            anchors[side] = sc["seaward_coord"]
            mids.append(sc["seaward_coord"])

    # Fast nudge first — cheap; catches most short coastal legs.
    res = fast_nudge_solve(lc, a, b, anchors=anchors or None)
    if res:
        return res

    max_nm = 250 if story_mode else 120
    if dist_nm > max_nm:
        return None

    return solve_chain(lc, a, b, mids=mids if mids else None, anchors=anchors or None)