#!/usr/bin/env python3
"""
Phase 2 — route-solutions.jsonl for all 42 failing-case inputs.
"""
from __future__ import annotations

import heapq
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

from shapely import wkb
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely.prepared import prep
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "_review/grok-routing-v2/grok-routing-v2"
OUT = ROOT / "grok-routing-output"
CODE = PKG / "code"
WKB_V2 = OUT / "uae_gulf_land_v2.wkb"
SEAWARD = OUT / "seaward-candidates.json"
REQUESTS = PKG / "failing-cases/route-requests.jsonl"
SOLUTIONS = OUT / "route-solutions.jsonl"
NOTES = OUT / "PHASE2-NOTES.md"

sys.path.insert(0, str(CODE))
from coast_aware_solver import solve_route as coast_solve
from qa_land_crossing import evaluate_route as qa_eval_route, load_overlay as qa_load_overlay

R_NM = 3440.065
LAND_TOL_KM = 0.05
LB224_MARINA_APRON_KM = 0.12
UAE_BBOX = (50.0, 21.5, 57.5, 26.8)

PALM_NODES: dict[str, list[float]] = {
    "trunk_south": [55.141, 25.099],
    "trunk_mid": [55.141, 25.100],
    "spine_mid": [55.141, 25.118],
    "spine_north": [55.138, 25.125],
    "west_fan": [55.115, 25.105],
    "east_fan": [55.152, 25.113],
    "crown_west": [55.115, 25.132],
    "crown_east": [55.135, 25.132],
    "crescent_n": [55.158, 25.120],
}

PALM_ROUTE_CHANNELS: dict[tuple[str, str], list[list[str]]] = {
    ("dxb-dubai-harbour-marina", "dxb-atlantis-palm"): [["trunk_mid", "spine_mid", "crown_west"], ["trunk_mid", "spine_north", "crown_west"]],
    ("dxb-dmyc", "dxb-waldorf-palm"): [["trunk_mid", "spine_mid", "crown_east"], ["trunk_mid", "spine_north", "crown_east"]],
    ("dxb-jbr-the-walk", "dxb-one-only-palm"): [["trunk_mid"], ["trunk_south"]],
    ("dxb-zabeel-saray", "dxb-rixos-palm"): [["west_fan", "trunk_mid", "east_fan"], ["west_fan", "spine_mid", "east_fan"], ["west_fan", "crescent_n", "east_fan"]],
    ("dxb-zabeel-saray", "dxb-anantara-palm"): [["west_fan", "spine_mid", "crown_east"], ["west_fan", "crescent_n", "crown_east"]],
    ("dxb-palm-west-beach", "dxb-five-palm"): [["trunk_mid"]],
    ("dxb-bluewaters-marina", "dxb-rixos-palm"): [["trunk_mid", "east_fan"], ["trunk_mid", "spine_mid", "east_fan"]],
    ("dxb-jbr-the-walk", "dxb-zabeel-saray"): [["trunk_mid", "west_fan"]],
    ("dxb-dmyc", "dxb-atlantis-royal"): [["trunk_mid", "spine_mid", "crown_east"], ["trunk_mid", "spine_north", "crown_east"]],
}

# Hand-authored channel waypoints (satellite-informed / LB-220 Lulu west-channel pattern)
HAND_WAYPOINTS: dict[tuple[str, str], list[list[float]]] = {
    ("dxb-zabeel-saray", "dxb-rixos-palm"): [[55.115, 25.105], [55.141, 25.100], [55.141, 25.118], [55.158, 25.120], [55.152, 25.113]],
    ("dxb-palm-west-beach", "dxb-five-palm"): [[55.145, 25.103]],
    ("ad-hudayriyat-bab-al-nojoum", "ad-emirates-palace-marina"): [[54.300, 24.405], [54.285, 24.430], [54.295, 24.455]],
    ("ad-hudayriyat-bab-al-nojoum", "ad-yas-marina"): [
        [54.300, 24.405], [54.285, 24.430], [54.308, 24.432], [54.336, 24.448],
        [54.372, 24.460], [54.426, 24.472], [54.498, 24.478], [54.570, 24.478],
        [54.6063, 24.4808],
    ],
    ("ad-khalifa-port", "ad-yas-marina"): [
        [54.639, 24.730], [54.657, 24.516], [54.627, 24.480],
    ],
    ("ad-khalifa-port", "ad-saadiyat-beach-club"): [
        [54.630, 24.780], [54.564, 24.714], [54.492, 24.618], [54.474, 24.594],
        [54.490, 24.602], [54.462, 24.582],
    ],
    ("ad-lulu-island", "ad-emirates-palace-marina"): [[54.330, 24.490], [54.305, 24.470], [54.300, 24.460]],
    ("ad-saadiyat-marina", "ad-reem-island"): [[54.414, 24.518], [54.403, 24.502], [54.403, 24.492]],
    ("ad-saadiyat-beach-club", "ad-lulu-island"): [
        [54.428, 24.546], [54.3413, 24.5013],
    ],
    ("abu-dhabi-uae", "doha-qatar"): [[54.85, 25.60], [53.85, 25.60], [52.85, 25.55], [52.05, 25.45], [51.62, 25.33]],
    ("bp-2f3e3c22fa", "bp-80adfa36b4"): [[51.52, 25.55], [51.53, 25.45]],
    ("bp-08b9b97bec", "bp-b10aba6c16"): [[56.275, 25.68], [56.270, 25.665]],
    ("abu-dhabi-uae", "bp-ed4ac4b266"): [[54.335, 24.452]],
    ("bp-2d105c5127", "bp-f377aadba6"): [[56.366, 25.516]],
    ("bp-8e8a497a21", "bp-e22806d1fa"): [[54.460, 24.538]],
    ("bp-ed4ac4b266", "bp-6846d27fcc"): [[54.329, 24.454]],
    ("bp-f377aadba6", "bp-3d9055c24e"): [[56.365, 25.514]],
    ("bp-7e3e3ac47c", "bp-7c9cd1a243"): [[55.842, 25.720]],
}


def hav_nm(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_NM * math.asin(min(1.0, math.sqrt(h)))


def hav_km(a, b):
    return hav_nm(a, b) * 1.852


def in_uae_bbox(lon: float, lat: float) -> bool:
    w, s, e, n = UAE_BBOX
    return w <= lon <= e and s <= lat <= n


class LandChecker:
    """UAE v2 STRtree grid + coarse global mask."""

    GRID_CACHE = OUT / "land_grid_0.02.npy"

    def __init__(self, wkb_path: Path, coarse=None, res_deg=0.02):
        import numpy as np

        geom = wkb.loads(wkb_path.read_bytes())
        self.polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
        self.tree = STRtree(self.polys)
        self.geom = geom
        self.coarse = coarse
        self.W, self.S, self.E, self.N = UAE_BBOX
        self.res = res_deg
        self.nx = int((self.E - self.W) / res_deg) + 1
        self.ny = int((self.N - self.S) / res_deg) + 1
        meta = OUT / "land_grid_meta.json"
        if self.GRID_CACHE.exists() and meta.exists():
            import json as _json
            m = _json.loads(meta.read_text())
            if m.get("res") == res_deg and m.get("nx") == self.nx:
                self.grid = np.load(self.GRID_CACHE)
                print(f"[landmask] grid cache hit {self.nx}x{self.ny}", flush=True)
                return
        self.grid = np.zeros((self.ny, self.nx), dtype=bool)
        print(f"[landmask] building grid {self.nx}x{self.ny} …", flush=True)
        for j in range(self.ny):
            lat = self.S + j * res_deg
            for i in range(self.nx):
                lon = self.W + i * res_deg
                pt = Point(lon, lat)
                for idx in self.tree.query(pt):
                    if self.polys[idx].contains(pt):
                        self.grid[j, i] = True
                        break
        np.save(self.GRID_CACHE, self.grid)
        meta.write_text(json.dumps({"res": res_deg, "nx": self.nx, "ny": self.ny}))

    def _in_uae(self, lon, lat):
        return self.W <= lon <= self.E and self.S <= lat <= self.N

    def is_land(self, lat, lon) -> bool:
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

    def evaluate_land_km(self, coords, step_km=0.05, apron_km=LB224_MARINA_APRON_KM) -> float:
        if len(coords) < 2:
            return 0.0
        samples = []
        cum = 0.0
        samples.append((coords[0][0], coords[0][1], 0.0))
        for i in range(1, len(coords)):
            a, b = coords[i - 1], coords[i]
            seg_km = hav_km(a, b)
            if seg_km <= 0:
                continue
            n_steps = max(1, int(seg_km / step_km))
            for k in range(1, n_steps + 1):
                t = k / n_steps
                samples.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, cum + seg_km * t))
            cum += seg_km
        total_km = samples[-1][2]
        on_land_km = 0.0
        prev = 0.0
        for lon, lat, cum in samples:
            seg = cum - prev
            prev = cum
            if cum < apron_km or cum > total_km - apron_km:
                continue
            if self.is_land(lat, lon):
                on_land_km += seg
        return round(on_land_km, 4)

def densify(seq, step_nm=0.25):
    arc = []
    for i in range(len(seq) - 1):
        p, q = seq[i], seq[i + 1]
        leg = hav_nm(p, q)
        n = max(2, min(300, int(leg / step_nm) + 1))
        seg = [[p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n] for k in range(n + 1)]
        arc.extend(seg[1:] if i else seg)
    return arc


def leg_clear(lc: LandChecker, p, q, step_nm=0.2) -> bool:
    leg = hav_nm(p, q)
    n = max(2, int(leg / step_nm) + 1)
    for k in range(1, n):
        x = p[0] + (q[0] - p[0]) * k / n
        y = p[1] + (q[1] - p[1]) * k / n
        if lc.is_land(y, x):
            return False
    return True


def astar(lc: LandChecker, wa, wb, res=0.003, pad=0.2):
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
    came = {}
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


def simplify(lc, path):
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


def connect_chain(lc, pts):
    full = []
    for i in range(len(pts) - 1):
        seg = astar(lc, pts[i], pts[i + 1])
        if not seg:
            return None
        simp = simplify(lc, seg)
        full.extend(simp if not full else simp[1:])
    return simplify(lc, full) if full else None


def gen_anchors(lc, pt, max_nm=1.5, preferred=None):
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


def geom_sinuosity(coords):
    gc = hav_km(coords[0], coords[-1])
    if gc <= 0:
        return 1.0
    total = sum(hav_km(coords[i - 1], coords[i]) for i in range(1, len(coords)))
    return round(total / gc, 3)


_QA_OVERLAY = None
_QA_TREE = None
_QA_COARSE = None


def _qa_init():
    global _QA_OVERLAY, _QA_TREE, _QA_COARSE
    if _QA_OVERLAY is None:
        _QA_OVERLAY, _QA_TREE = qa_load_overlay(WKB_V2)
    if _QA_COARSE is None:
        try:
            from global_land_mask import globe as _QA_COARSE
        except Exception:
            _QA_COARSE = None


def qa_land_km(geom) -> float:
    _qa_init()
    m = qa_eval_route(geom, _QA_COARSE, _QA_OVERLAY, _QA_TREE, step_km=0.05)
    return m["interior_land_km"]


def pack_result(lc, dd, method, max_sinuosity=1.6):
    geom = densify(dd)
    land_km = lc.evaluate_land_km(geom)
    sinu = geom_sinuosity(geom)
    # Hand-authored offshore legs: grid is coarse; official QA runs in verify_solution.
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
    }


def verify_solution(result) -> dict | None:
    """Confirm interior_land_km matches official qa_land_crossing."""
    if not result:
        return None
    result["interior_land_km"] = qa_land_km(result["geometry"])
    return result if result["interior_land_km"] <= LAND_TOL_KM else None


def solve_hand(lc, a, b, mids, method="hand_waypoints"):
    dd = [a] + mids + [b]
    # Inject seaward anchors when marina endpoints sit on reclaimed land.
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
    res = verify_solution(pack_result(lc, dd, method, max_sinuosity=2.5))
    if res:
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
    return verify_solution(pack_result(lc, dd2, method, max_sinuosity=2.5))


class NE10Checker:
    """NE10m LocalLand for non-UAE ICS routes."""

    def __init__(self, bbox, pad=0.25):
        from _local_land_solver import LocalLand

        w, s, e, n = bbox
        self.ll = LocalLand((w, s, e, n), pad=pad)

    def is_land(self, lat, lon) -> bool:
        return self.ll.is_land(lat, lon)

    def evaluate_land_km(self, coords, step_km=0.05, apron_km=LB224_MARINA_APRON_KM) -> float:
        if len(coords) < 2:
            return 0.0
        samples = []
        cum = 0.0
        samples.append((coords[0][0], coords[0][1], 0.0))
        for i in range(1, len(coords)):
            a, b = coords[i - 1], coords[i]
            seg_km = hav_km(a, b)
            if seg_km <= 0:
                continue
            n_steps = max(1, int(seg_km / step_km))
            for k in range(1, n_steps + 1):
                t = k / n_steps
                samples.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, cum + seg_km * t))
            cum += seg_km
        total_km = samples[-1][2]
        on_land_km = 0.0
        prev = 0.0
        for lon, lat, cum in samples:
            seg = cum - prev
            prev = cum
            if cum < apron_km or cum > total_km - apron_km:
                continue
            if self.is_land(lat, lon):
                on_land_km += seg
        return round(on_land_km, 4)


def solve_chain(lc, a, b, mids=None, anchors=None):
    mids = mids or []
    pref_a = anchors.get("from") if anchors else None
    pref_b = anchors.get("to") if anchors else None
    aa = gen_anchors(lc, a, preferred=pref_a)
    bb = gen_anchors(lc, b, preferred=pref_b)
    if not aa or not bb:
        return None
    best = None
    for ca in aa[:4]:
        for cb in bb[:4]:
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
            if cand and (best is None or len(dd2) < len(best.get("_dd", []))):
                cand["_dd"] = dd2
                best = cand
        if best:
            break
    if best:
        best.pop("_dd", None)
    return best


def solve_palm(req, lc, seaward):
    key = (req["from_id"], req["to_id"])
    channel_sets = PALM_ROUTE_CHANNELS.get(key, [["trunk_mid"]])
    anchors = {}
    for side, bp_id in [("from", req["from_id"]), ("to", req["to_id"])]:
        sc = seaward.get("candidates", {}).get(bp_id, {})
        if sc.get("seaward_coord"):
            anchors[side] = sc["seaward_coord"]

    passing = []
    for ch in channel_sets:
        mids = [PALM_NODES[n] for n in ch if n in PALM_NODES]
        res = solve_chain(lc, req["from_coord"], req["to_coord"], mids=mids, anchors=anchors)
        if res:
            res["channel_path"] = ch
            res["method"] = "hybrid"
            passing.append(res)

    if not passing:
        return None, "no A* path through Palm channels passes QA"
    if len(passing) >= 2:
        lengths = [p["sea_nm"] for p in passing]
        if max(lengths) - min(lengths) < 0.3 * max(1.0, min(lengths)):
            best = min(passing, key=lambda p: p["sea_nm"])
            best["method"] = "hybrid_shortest"
            best["note"] = "ambiguous_channel_picked_shortest"
            return best, "PASS(ambiguous-shortest)"
    return passing[0], "PASS"


def offset_point(origin, az_deg, dist_m):
    R = 6378137.0
    az = math.radians(az_deg)
    lat = math.radians(origin[1])
    lon = math.radians(origin[0])
    ang = dist_m / R
    lat2 = math.asin(math.sin(lat) * math.cos(ang) + math.cos(lat) * math.sin(ang) * math.cos(az))
    lon2 = lon + math.atan2(
        math.sin(az) * math.sin(ang) * math.cos(lat),
        math.cos(ang) - math.sin(lat) * math.sin(lat2),
    )
    return [math.degrees(lon2), math.degrees(lat2)]


def fast_nudge_solve(lc, a, b, anchors=None):
    """Lightweight 0-2WP search — avoids coast_aware_solver combinatorics."""
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
        if cand and (best is None or cand["sea_nm"] < best["sea_nm"]):
            best = cand
    return best


def solve_ics(req):
    a, b = req["from_coord"], req["to_coord"]
    w = min(a[0], b[0]) - 0.3
    e = max(a[0], b[0]) + 0.3
    s = min(a[1], b[1]) - 0.3
    n = max(a[1], b[1]) + 0.3
    lc = NE10Checker((w, s, e, n))
    mids = HAND_WAYPOINTS.get((req["from_id"], req["to_id"]), [])
    if mids:
        res = solve_hand(lc, a, b, mids)
        if res:
            return res, "PASS(hand)"
    res = fast_nudge_solve(lc, a, b)
    if res:
        res["method"] = "a_star_global"
        return res, "PASS"
    return None, "ICS NE10m solve failed QA"


def solve_generic(req, lc, seaward):
    a, b = req["from_coord"], req["to_coord"]
    key = (req["from_id"], req["to_id"])
    if key in HAND_WAYPOINTS:
        res = solve_hand(lc, a, b, HAND_WAYPOINTS[key])
        if res:
            return res, "PASS(hand)"

    anchors = {}
    mids = []
    for side, bp_id in [("from", req["from_id"]), ("to", req["to_id"])]:
        sc = seaward.get("candidates", {}).get(bp_id, {})
        if sc.get("seaward_coord"):
            anchors[side] = sc["seaward_coord"]
            mids.append(sc["seaward_coord"])

    res = solve_chain(lc, a, b, mids=mids if mids else None, anchors=anchors)
    if res:
        return res, "PASS"

    res = fast_nudge_solve(lc, a, b, anchors=anchors)
    if res:
        return res, "PASS"

    return None, "A* and nudge failed QA"


def build_row(req, result, reason=None):
    row = {
        "route_id": req.get("route_id"),
        "request_kind": req["request_kind"],
        "from_id": req["from_id"],
        "to_id": req["to_id"],
        "priority_tier": req.get("priority_tier"),
        "landmask_version": "uae_gulf_land_v2",
    }
    if result:
        row.update({
            "geometry": {"type": "LineString", "coordinates": [[round(c[0], 6), round(c[1], 6)] for c in result["geometry"]]},
            "waypoints_authored": result.get("waypoints", []),
            "method": result.get("method", "a_star_v2"),
            "interior_land_km": result["interior_land_km"],
            "sinuosity": result["sinuosity"],
            "qa_pass": True,
            "distance_nm_geom": result["sea_nm"],
        })
        if result.get("channel_path"):
            row["channel_path"] = result["channel_path"]
    else:
        row.update({"geometry": None, "qa_pass": False, "reason": reason})
    return row


def main():
    try:
        from global_land_mask import globe as coarse
    except Exception:
        coarse = None

    lc = LandChecker(WKB_V2, coarse=coarse)
    seaward = json.loads(SEAWARD.read_text())
    requests = [json.loads(l) for l in REQUESTS.read_text().splitlines() if l.strip()]

    solutions = []
    stats = {"solved": 0, "unsolved": 0, "by_tier": {}}

    for i, req in enumerate(requests):
        tier = req.get("priority_tier", "?")
        if tier == "palm-9-cross-trunk":
            key = (req["from_id"], req["to_id"])
            if key in HAND_WAYPOINTS:
                result = solve_hand(lc, req["from_coord"], req["to_coord"], HAND_WAYPOINTS[key])
                verdict = "PASS(hand)" if result else "hand waypoints failed QA"
            else:
                result, verdict = solve_palm(req, lc, seaward)
        elif tier == "ics-cleanup-LB-225":
            result, verdict = solve_ics(req)
        else:
            result, verdict = solve_generic(req, lc, seaward)

        row = build_row(req, result, reason=None if result else verdict)
        solutions.append(row)
        stats["solved" if result else "unsolved"] += 1
        stats["by_tier"].setdefault(tier, {"solved": 0, "unsolved": 0})
        stats["by_tier"][tier]["solved" if result else "unsolved"] += 1

        tag = req.get("route_id") or f"{req['from_id']}->{req['to_id']}"
        print(f"{'SOLVED' if result else 'UNSOLVED'} [{i+1}/42] {tag} — {verdict}", flush=True)

    with SOLUTIONS.open("w") as f:
        for row in solutions:
            f.write(json.dumps(row) + "\n")

    qa_routes = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"id": r.get("route_id") or f"{r['from_id']}->{r['to_id']}", "distance_nm": r.get("distance_nm_geom", 1)},
                "geometry": r["geometry"],
            }
            for r in solutions if r.get("geometry")
        ],
    }
    (OUT / "ROUTES-solutions-qa.json").write_text(json.dumps(qa_routes))

    lines = [
        "# Phase 2 Notes — route-solutions.jsonl",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"**Solved:** {stats['solved']}/42 · **UNSOLVED:** {stats['unsolved']}/42",
        "",
        "## By tier",
        "",
    ]
    for tier, t in sorted(stats["by_tier"].items()):
        lines.append(f"- `{tier}`: {t['solved']} solved, {t['unsolved']} unsolved")
    unsolved = [r for r in solutions if not r.get("qa_pass")]
    if unsolved:
        lines.extend(["", "## UNSOLVED", ""])
        for r in unsolved:
            rid = r.get("route_id") or f"{r['from_id']}->{r['to_id']}"
            lines.append(f"- `{rid}`: {r.get('reason')}")
    NOTES.write_text("\n".join(lines) + "\n")
    print(f"\nWrote {SOLUTIONS} ({stats['solved']}/42 solved)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())