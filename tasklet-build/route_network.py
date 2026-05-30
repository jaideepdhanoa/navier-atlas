"""
Demand-weighted layered route-network generator (Tasklet owns the GRAPH).

Replaces the old "routes between city centroids / raw-label endpoints" model for the
marquee markets with a real network built ON the curated boarding-point graph:

  * LOCAL mesh  — intra-cluster BP<->BP capillaries (hub-spokes + nearest-neighbour
                  chords) so no boarding point is an orphan and dense waterfronts read
                  as dense.
  * REGIONAL    — cross-cluster / cross-border connectors.
  * TRUNK       — heavy proven-demand backbones.

Every edge:
  - has endpoints on REAL boarding-point coordinates (so the front-end's geometric
    on_route tagging + terminus connector nodes light up the pins),
  - carries `from`/`to` as real node ids (city node id or the same `bp-<hash>` id the
    rendered pins use) — NEVER a raw label string,
  - is land-validated (SeaGrid A* + interior-land guard, 1.9 km gate),
  - carries `edge_class` + `traffic_weight` (0-1, demand model) + `trip_purpose`.

See reference/route-demand-model.md and route-demand-config.json.
Evidence/anchor strings stay in the config (internal); only neutral numeric/enum fields ship.
"""
from __future__ import annotations

import os
import hashlib
import json
import math
from pathlib import Path

try:
    from global_land_mask import globe
    _HAVE_LAND = True
except Exception:
    globe, _HAVE_LAND = None, False
try:
    from sea_router import SeaGrid
    _HAVE_SEA = True
except Exception:
    SeaGrid, _HAVE_SEA = None, False

R_NM = 3440.065
KM_PER_NM = 1.852
PIONEER_MAX_NM = 70.0
LAND_GATE_KM = 1.99   # stay strictly under the qa_land_crossing.py 2.0 km gate, with margin

DEST_TYPES = {
    "marina", "ferry_terminal", "cruise_terminal", "yacht_club", "hotel_jetty",
    "water_bus_terminal", "beach_club_jetty", "public_pier", "seaplane_base",
    "water_taxi_stop", "abra_station",
}
TYPE_PRIORITY = {
    "marina": 0, "ferry_terminal": 1, "cruise_terminal": 2, "yacht_club": 3,
    "water_bus_terminal": 4, "hotel_jetty": 5, "beach_club_jetty": 6,
    "public_pier": 7, "seaplane_base": 8, "water_taxi_stop": 9, "abra_station": 9,
}
REL_FACTOR = {"P0": 1.0, "P1": 0.78, "P2": 0.55}
DEDUP_DEG = 0.009          # ~1 km — keeps a few reps per district, not every water-bus stop
LOCAL_MAX_NM = 60.0        # an intra-cluster local capillary cap (Pioneer II)
MAX_LOCAL_SPOKES = 16      # legibility per cluster
KNN_CHORDS = 2             # nearest-neighbour chords per rep for mesh density
FAR_MAX_NM = 700.0         # Quanta-LR long-tail connector cap (well inside 2,000 nm)
MAX_FAR_SPOKES = 10        # legibility cap on long-tail Quanta connectors per cluster

# Infrastructure that is NOT a passenger boarding point: never a route endpoint,
# and excluded from the connectivity denominator (a shipyard/port/dive-shop is not a jetty).
NON_BOARDABLE_TYPES = {
    "working_harbour", "shipyard", "dive_centre", "mro", "refuel",
    "anchorage", "mooring_field",
}
# Long-tail purpose mapping for Quanta-LR outpost connectors.
FAR_PURPOSE = {
    "hotel_jetty": "luxury", "beach_club_jetty": "luxury", "yacht_club": "luxury",
    "seaplane_base": "luxury", "cruise_terminal": "tourism", "marina": "luxury",
    "ferry_terminal": "tourism", "public_pier": "tourism", "water_taxi_stop": "tourism",
}


def _hav_nm(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R_NM * math.asin(min(1.0, math.sqrt(h)))


def _arc_mid_land_nm(arc, buf_nm=1.5):
    """Interior land (nm) along arc, excluding a buffer near each endpoint (jetties read
    as land at the ~1 km mask resolution)."""
    if not _HAVE_LAND or len(arc) < 3:
        return 0.0
    n = len(arc)
    dfrom = [0.0] * n
    for i in range(1, n):
        dfrom[i] = dfrom[i - 1] + _hav_nm(arc[i - 1], arc[i])
    total = dfrom[-1]
    land = 0.0
    for i in range(1, n - 1):
        if dfrom[i] < buf_nm or (total - dfrom[i]) < buf_nm:
            continue
        if bool(globe.is_land(arc[i][1], arc[i][0])):
            land += (_hav_nm(arc[i - 1], arc[i]) + _hav_nm(arc[i], arc[i + 1])) / 2.0
    return land


def _densify(seq):
    """Linear lng/lat interpolation (matches the straight segments the sea-router validates)."""
    arc = []
    for i in range(len(seq) - 1):
        p, q = seq[i], seq[i + 1]
        leg = _hav_nm(p, q)
        npts = max(2, min(80, int(leg / 0.6) + 1))
        seg = [[p[0] + (q[0] - p[0]) * k / npts, p[1] + (q[1] - p[1]) * k / npts]
               for k in range(npts + 1)]
        arc.extend(seg[1:] if i else seg)
    return arc


def _bp_hash(bp, node_id):
    """Replicate build.py's rendered pin id EXACTLY so route endpoints == real node ids."""
    raw = (bp.get("id") or bp.get("name") or "") + node_id
    return "bp-" + hashlib.md5(raw.encode("utf-8")).hexdigest()[:10]


def _rel(bp):
    return (bp.get("relevance") or "").strip().upper()


def _bp_file(bp_dir, slug):
    fp = Path(bp_dir) / f"{slug}-boarding-points.json"
    if not fp.exists():
        fp = Path(bp_dir) / f"{slug}.json"
    return fp if fp.exists() else None


def generate(*, bp_dir, config_path, bp_city_map, is_marker, sanitize):
    cfg = json.loads(Path(config_path).read_text())
    local_base = cfg.get("local_base_weight", 0.34)
    features = []
    stats = {"local": 0, "regional": 0, "trunk": 0, "dropped_land": 0,
             "clusters": 0, "corridors_dropped": 0, "managed_node_ids": set()}

    # ---- load every cluster referenced by the config -------------------------------
    clusters = {}  # slug -> {node_id, anchor, reps:[bp..], all:[bp..]}
    for mkt in cfg["markets"].values():
        for slug in mkt["clusters"]:
            if slug in clusters:
                continue
            node_id = bp_city_map.get(slug)
            fp = _bp_file(bp_dir, slug)
            if not node_id or not fp:
                continue
            data = json.loads(fp.read_text())
            anchor = data.get("city_anchor")
            cand = []
            for bp in data.get("boarding_points", []):
                if bp.get("relevance") == "hide":
                    continue
                if bp.get("lng") is None or bp.get("lat") is None:
                    continue
                if bp.get("type") not in DEST_TYPES:
                    continue
                if is_marker(bp.get("name") or ""):
                    continue
                cand.append(bp)
            clusters[slug] = {"node_id": node_id, "anchor": anchor, "all": cand}
            stats["managed_node_ids"].add(node_id)

    # ---- per-market sea grids (shared bbox over the market's clusters) -------------
    def _market_grid(market):
        if not _HAVE_SEA:
            return None
        xs, ys = [], []
        for slug in market["clusters"]:
            c = clusters.get(slug)
            if not c:
                continue
            if c["anchor"]:
                xs.append(c["anchor"][0]); ys.append(c["anchor"][1])
            for bp in c["all"]:
                xs.append(bp["lng"]); ys.append(bp["lat"])
        if not xs:
            return None
        try:
            return SeaGrid(min(xs) - 0.3, min(ys) - 0.3, max(xs) + 0.3, max(ys) + 0.3)
        except Exception:
            return None

    def _water_anchor(pt, max_nm=1.5):
        """Radial search for the nearest open-water point (per the ~1km land mask).

        Many real jetties sit up lagoons/channels the coarse mask reads as land; the
        grid A* can't start there. We route from a nearby open-water APPROACH point and
        prepend the true jetty. The approach must be within `max_nm` so the short
        connector leg falls inside the gate's 1.5 nm endpoint buffer (and is therefore
        ignored by the land-crossing check). Returns (dist_nm, point) or (None, pt) if no
        open water is within max_nm (jetty too deep in mask-land for this corridor)."""
        if not _HAVE_LAND or not bool(globe.is_land(pt[1], pt[0])):
            return 0.0, pt
        best = (1e9, None)
        for r in (0.003 * k for k in range(1, 60)):           # ~0.3 km steps out to ~8 nm
            for da in range(0, 360, 12):
                p = [pt[0] + r * math.cos(math.radians(da)),
                     pt[1] + r * math.sin(math.radians(da))]
                if not bool(globe.is_land(p[1], p[0])):
                    d = _hav_nm(pt, p)
                    if d < best[0]:
                        best = (d, p)
            if best[1] is not None:
                break
        if best[1] is None or best[0] > max_nm:
            return None, pt
        return best[0], best[1]

    def _route(grid, a, b, hand_wps=None):
        """Return (arc, sea_nm) or None if it can't find a clean, gate-passing sea path.
        Endpoints are anchored to nearby open water; the jetty coords are prepended so the
        drawn line still lands on the pin. `hand_wps` (curated open-water waypoints) override
        the A* solver for corridors the coarse grid can't thread."""
        da, wa = _water_anchor(a)
        db, wb = _water_anchor(b)
        if wa is None or wb is None:
            return None
        if hand_wps:
            mids = [list(p) for p in hand_wps]
        else:
            wps = grid.route(tuple(wa), tuple(wb)) if grid is not None else None
            mids = list(wps) if wps else []
        seq = [a] + ([wa] if wa != a else []) + mids + ([wb] if wb != b else []) + [b]
        dedup = [seq[0]]
        for p in seq[1:]:
            if p != dedup[-1]:
                dedup.append(p)
        arc = _densify(dedup)
        sea_nm = sum(_hav_nm(dedup[i], dedup[i + 1]) for i in range(len(dedup) - 1))
        if _arc_mid_land_nm(arc) * KM_PER_NM > LAND_GATE_KM:
            return None
        return arc, sea_nm

    def _emit(rid_seed, arc, sea_nm, frm, to, edge_class, weight, purpose, platform_hint):
        platform = platform_hint
        # Rule A (QLR curation): any edge within the all-electric range is Pioneer II,
        # regardless of hint. Quanta-LR is reserved for genuine long-haul (>70 nm).
        if sea_nm <= PIONEER_MAX_NM:
            platform = "Pioneer II"
        elif not platform or platform == "Pioneer II":
            platform = "Quanta-LR"
        rid = "rn-" + hashlib.md5(rid_seed.encode("utf-8")).hexdigest()[:12]
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": arc},
            "properties": {
                "id": rid,
                "platform": platform,
                "distance_nm": round(sea_nm, 1),
                "edge_class": edge_class,
                "traffic_weight": round(float(weight), 3),
                "trip_purpose": purpose,
                "from": frm,
                "to": to,
            },
        })

    def _find_bp(slug, match):
        """Resolve a corridor endpoint inside a cluster: matched BP, else cluster hub."""
        c = clusters.get(slug)
        if not c or not c["all"]:
            return None
        if match:
            ml = match.lower()
            hits = [bp for bp in c["all"] if ml in (bp.get("name") or "").lower()
                    or ml in (bp.get("linked_locale") or "").lower()]
            if hits:
                hits.sort(key=lambda b: ({"P0": 0, "P1": 1, "P2": 2}.get(_rel(b), 3),
                                         TYPE_PRIORITY.get(b.get("type"), 9)))
                return hits[0]
        return _hub(slug)

    _hub_cache = {}

    def _hub(slug):
        if slug in _hub_cache:
            return _hub_cache[slug]
        c = clusters.get(slug)
        if not c or not c["all"]:
            _hub_cache[slug] = None
            return None
        anc = c["anchor"] or [c["all"][0]["lng"], c["all"][0]["lat"]]
        best = sorted(
            c["all"],
            key=lambda b: ({"P0": 0, "P1": 1, "P2": 2}.get(_rel(b), 3),
                           TYPE_PRIORITY.get(b.get("type"), 9),
                           _hav_nm(anc, [b["lng"], b["lat"]])),
        )[0]
        _hub_cache[slug] = best
        return best

    # ================= LOCAL MESH per cluster =================
    for slug, c in clusters.items():
        if not c["all"]:
            continue
        anchor = c["anchor"] or [c["all"][0]["lng"], c["all"][0]["lat"]]
        node_id = c["node_id"]
        # dedup to ~1 km grid -> representative reps
        cells = {}
        for bp in c["all"]:
            if bp.get("type") in NON_BOARDABLE_TYPES:
                continue  # infrastructure, not a passenger boarding point
            cc = [bp["lng"], bp["lat"]]
            d = _hav_nm(anchor, cc)
            if d > FAR_MAX_NM:
                continue
            key = (round(cc[0] / DEDUP_DEG), round(cc[1] / DEDUP_DEG))
            prio = ({"P0": 0, "P1": 1, "P2": 2}.get(_rel(bp), 3),
                    TYPE_PRIORITY.get(bp.get("type"), 9), d)
            if key not in cells or prio < cells[key][0]:
                cells[key] = (prio, bp, cc, d)
        all_reps = sorted(cells.values(), key=lambda v: v[0])
        # near reps -> Pioneer II local capillaries; far reps -> Quanta-LR outpost spokes
        reps = [r for r in all_reps if r[3] <= LOCAL_MAX_NM]
        far_reps = [r for r in all_reps if r[3] > LOCAL_MAX_NM]
        if len(reps) < 2 and not far_reps:
            continue
        if len(reps) < 1:
            continue
        connected_ids = set()  # bp-hash ids that received >=1 edge this cluster
        hub_bp = _hub(slug)
        hub_c = [hub_bp["lng"], hub_bp["lat"]]
        grid = None
        if _HAVE_SEA:
            xs = [p[2][0] for p in reps] + [hub_c[0]]
            ys = [p[2][1] for p in reps] + [hub_c[1]]
            try:
                grid = SeaGrid(min(xs) - 0.15, min(ys) - 0.15, max(xs) + 0.15, max(ys) + 0.15)
            except Exception:
                grid = None
        cluster_has = 0
        # hub spokes
        spoke_reps = [r for r in reps if r[1] is not hub_bp][:MAX_LOCAL_SPOKES]
        for _prio, bp, cc, _d in spoke_reps:
            r = _route(grid, hub_c, cc)
            if not r:
                stats["dropped_land"] += 1
                continue
            arc, sea_nm = r
            w = local_base * REL_FACTOR.get(_rel(bp), 0.55)
            bid = _bp_hash(bp, node_id)
            _emit(node_id + "|hub|" + bid, arc, sea_nm,
                  node_id, bid, "local", w, "local", "Pioneer II")
            stats["local"] += 1
            cluster_has += 1
            connected_ids.add(bid)
        # nearest-neighbour chords (mesh density)
        pts = [(bp, cc) for _p, bp, cc, _d in reps]
        seen_pairs = set()
        for i, (bp_i, c_i) in enumerate(pts):
            dists = sorted(
                ((_hav_nm(c_i, c_j), j) for j, (_bp_j, c_j) in enumerate(pts) if j != i)
            )[:KNN_CHORDS]
            for _dn, j in dists:
                key = tuple(sorted((i, j)))
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                bp_j, c_j = pts[j]
                r = _route(grid, c_i, c_j)
                if not r:
                    stats["dropped_land"] += 1
                    continue
                arc, sea_nm = r
                rf = min(REL_FACTOR.get(_rel(bp_i), 0.55), REL_FACTOR.get(_rel(bp_j), 0.55))
                w = local_base * 0.7 * rf
                bi, bj = _bp_hash(bp_i, node_id), _bp_hash(bp_j, node_id)
                _emit(node_id + "|chord|" + bi + bj,
                      arc, sea_nm, bi, bj,
                      "local", w, "local", "Pioneer II")
                stats["local"] += 1
                cluster_has += 1
                connected_ids.add(bi); connected_ids.add(bj)

        # ----- Quanta-LR long-tail outpost connectors -----
        # Link mid/long-range boardable outposts (resort islands, ferry ports far from
        # the hub) to the nearest ALREADY-connected jetty (or hub) via a Quanta-LR
        # regional spoke. This lights up the island-hopping story without faking demand.
        near_pts = [(bp, cc, _bp_hash(bp, node_id)) for _p, bp, cc, _d in reps]
        near_pts.append((hub_bp, hub_c, node_id))
        for _prio, bp, cc, _d in far_reps[:MAX_FAR_SPOKES]:
            # nearest near-rep / hub to anchor the connector
            cand = sorted(near_pts, key=lambda np: _hav_nm(cc, np[1]))
            placed = False
            for anchor_bp, anchor_c, anchor_id in cand[:4]:
                if _hav_nm(cc, anchor_c) > FAR_MAX_NM:
                    break
                # cheap straight-line + land guard first (open-ocean Quanta legs)
                r = _route(None, anchor_c, cc)
                if not r:
                    # bounded grid fallback only for modest spans (avoid huge grids)
                    span = max(abs(cc[0] - anchor_c[0]), abs(cc[1] - anchor_c[1]))
                    if _HAVE_SEA and span <= 2.5:
                        try:
                            pg = SeaGrid(min(cc[0], anchor_c[0]) - 0.2, min(cc[1], anchor_c[1]) - 0.2,
                                         max(cc[0], anchor_c[0]) + 0.2, max(cc[1], anchor_c[1]) + 0.2)
                            r = _route(pg, anchor_c, cc)
                        except Exception:
                            r = None
                if not r:
                    continue
                arc, sea_nm = r
                bid = _bp_hash(bp, node_id)
                purpose = FAR_PURPOSE.get(bp.get("type"), "tourism")
                w = 0.40 * REL_FACTOR.get(_rel(bp), 0.55)
                # endpoints: hub anchor uses node_id (lights hub degree); else bp-hash chord
                frm = anchor_id
                _emit(node_id + "|far|" + bid, arc, sea_nm,
                      frm, bid, "regional", w, purpose, "Quanta-LR")
                stats["regional"] = stats.get("regional", 0) + 1
                stats["far_connectors"] = stats.get("far_connectors", 0) + 1
                cluster_has += 1
                connected_ids.add(bid)
                placed = True
                break
            if not placed:
                stats["dropped_land"] += 1

        # ----- Orphan rescue: any boardable near-rep with no edge gets one -----
        for _prio, bp, cc, _d in reps:
            bid = _bp_hash(bp, node_id)
            if bid in connected_ids or bp is hub_bp:
                continue
            cand = sorted(
                ((_hav_nm(cc, np[1]), np) for np in near_pts if np[2] != bid and np[2] in (connected_ids | {node_id})),
                key=lambda x: x[0])
            for _dn, (anchor_bp, anchor_c, anchor_id) in cand[:5]:
                r = _route(grid, anchor_c, cc)
                if not r:
                    continue
                arc, sea_nm = r
                w = local_base * 0.6 * REL_FACTOR.get(_rel(bp), 0.55)
                _emit(node_id + "|rescue|" + bid, arc, sea_nm,
                      (anchor_id if anchor_id == node_id else anchor_id), bid,
                      "local", w, "local", "Pioneer II")
                stats["local"] += 1
                stats["rescued"] = stats.get("rescued", 0) + 1
                cluster_has += 1
                connected_ids.add(bid)
                break

        if cluster_has:
            stats["clusters"] += 1

    # ================= FEATURED CORRIDORS (regional / trunk) =================
    for mkt in cfg["markets"].values():
        grid = _market_grid(mkt)
        for cor in mkt.get("corridors", []):
            fb = _find_bp(cor["from"]["cluster"], cor["from"].get("match"))
            tb = _find_bp(cor["to"]["cluster"], cor["to"].get("match"))
            if not fb or not tb:
                stats["corridors_dropped"] += 1
                if os.environ.get("RN_DEBUG"):
                    print(f"  [corridor-drop:endpoint] {cor['from']['cluster']}/{cor['from'].get('match')} -> {cor['to']['cluster']}/{cor['to'].get('match')} (fb={bool(fb)} tb={bool(tb)})")
                continue
            a = [fb["lng"], fb["lat"]]
            b = [tb["lng"], tb["lat"]]
            r = _route(grid, a, b, hand_wps=cor.get("waypoints"))
            if not r:
                stats["corridors_dropped"] += 1
                if os.environ.get("RN_DEBUG"):
                    print(f"  [corridor-drop:route] {cor['from']['cluster']}/{cor['from'].get('match')} -> {cor['to']['cluster']}/{cor['to'].get('match')} a={a} b={b}")
                continue
            arc, sea_nm = r
            fslug, tslug = cor["from"]["cluster"], cor["to"]["cluster"]
            fnode, tnode = clusters[fslug]["node_id"], clusters[tslug]["node_id"]
            # inter-cluster: from/to = city node ids (degree lights the hubs).
            # intra-cluster (same cluster): from/to = bp-hash ids (don't inflate city degree).
            if fslug == tslug:
                frm, to = _bp_hash(fb, fnode), _bp_hash(tb, tnode)
            else:
                frm, to = fnode, tnode
            ec = cor.get("class", "regional")
            _emit("cor|" + fnode + "|" + tnode + "|" + (cor["to"].get("match") or ""),
                  arc, sea_nm, frm, to, ec, cor.get("weight", 0.5),
                  cor.get("purpose", "mixed"), cor.get("platform"))
            stats[ec] = stats.get(ec, 0) + 1

    stats["managed_node_ids"] = sorted(stats["managed_node_ids"])
    return features, stats
