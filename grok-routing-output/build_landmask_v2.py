#!/usr/bin/env python3
"""
Phase 1 — uae_gulf_land_v2.wkb + seaward-candidates.json + PHASE1-NOTES.md

Builds upgraded UAE/Gulf landmask from v1 WKB:
  - Replace solid Palm Jumeirah blob with trunk + frond polygons + channel gaps
  - Add Abu Dhabi reclamation polygons (Hudayriyat, Khalifa Port, Lulu, Saadiyat, Reem)
  - Optional tight-bbox Overpass coast refinement (Palm + AD); failures logged in notes

Outputs:
  grok-routing-output/uae_gulf_land_v2.wkb
  grok-routing-output/seaward-candidates.json
  grok-routing-output/PHASE1-NOTES.md
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

from shapely import wkb
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, box
from shapely.ops import unary_union
from shapely.validation import make_valid

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "_review/grok-routing-v2/grok-routing-v2"
OUT = ROOT / "grok-routing-output"
sys.path.insert(0, str(OUT))
V1_WKB = PKG / "data/uae_gulf_land.wkb"
REQUESTS = PKG / "failing-cases/route-requests.jsonl"
BPS = PKG / "data/boarding-points-sample.json"

PALM_BBOX = (55.105, 25.090, 55.180, 25.155)
PALM_REMOVE_IDX = {87, 88, 89, 94}

R_NM = 3440.065
KM_PER_DEG_LAT = 111.0


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    R = 6371008.8
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(min(1.0, math.sqrt(h)))


def nm_to_deg_lon(nm: float, lat: float) -> float:
    return (nm * 1.852) / (KM_PER_DEG_LAT * math.cos(math.radians(lat)))


def nm_to_deg_lat(nm: float) -> float:
    return (nm * 1.852) / KM_PER_DEG_LAT


def poly_from_bbox(w: float, s: float, e: float, n: float) -> Polygon:
    return Polygon([(w, s), (e, s), (e, n), (w, n), (w, s)])


def palm_land_polys() -> list[Polygon]:
    """Hand-authored Palm Jumeirah land: trunk strip + fronds + crown + crescent.
    Gaps between polygons are navigable frond channels (water)."""
    polys: list[Polygon] = []

    # Trunk (narrow spine, LB-208-style) — split N/S so mid-trunk channel stays water
    polys.append(poly_from_bbox(55.140, 25.083, 55.143, 25.098))
    polys.append(poly_from_bbox(55.140, 25.104, 55.143, 25.112))

    # West fronds (radial wedges west of trunk)
    polys.append(poly_from_bbox(55.104, 25.109, 55.112, 25.118))   # Kempinski
    polys.append(poly_from_bbox(55.108, 25.103, 55.115, 25.109))   # W Dubai
    polys.append(poly_from_bbox(55.118, 25.094, 55.128, 25.103))   # Zabeel Saray west
    polys.append(poly_from_bbox(55.128, 25.094, 55.137, 25.103))   # One&Only west

    # East fronds
    polys.append(poly_from_bbox(55.137, 25.104, 55.143, 25.110))   # Fairmont / trunk east
    polys.append(poly_from_bbox(55.145, 25.100, 55.151, 25.107))   # FIVE / Palm West Beach
    polys.append(poly_from_bbox(55.149, 25.114, 55.156, 25.124))   # Rixos
    polys.append(poly_from_bbox(55.149, 25.124, 55.156, 25.132))   # Anantara
    polys.append(poly_from_bbox(55.148, 25.130, 55.154, 25.138))   # Waldorf crescent

    # Crown — Atlantis core + Royal block
    polys.append(poly_from_bbox(55.112, 25.124, 55.122, 25.132))   # Atlantis The Palm
    polys.append(poly_from_bbox(55.122, 25.134, 55.130, 25.143))   # Atlantis Royal

    # East breakwater crescent (arc approximated as 3 boxes)
    polys.append(poly_from_bbox(55.155, 25.103, 55.162, 25.111))
    polys.append(poly_from_bbox(55.158, 25.110, 55.165, 25.118))
    polys.append(poly_from_bbox(55.155, 25.117, 55.162, 25.125))

    # Bridge link trunk → crown — split to preserve spine channel at ~25.118
    polys.append(poly_from_bbox(55.140, 25.112, 55.143, 25.116))
    polys.append(poly_from_bbox(55.140, 25.121, 55.143, 25.124))

    return [make_valid(p) for p in polys if not p.is_empty]


def reclamation_polys() -> list[Polygon]:
    """Hand-authored Abu Dhabi reclamation (LB-221) — refined in ad_channel_cutouts."""
    from ad_channel_cutouts import refined_reclamation_polys

    return refined_reclamation_polys()


def try_overpass_land(bbox: tuple[float, float, float, float], label: str) -> tuple[object | None, str]:
    """Tight-bbox Overpass coast fetch via _local_land_solver.fine_osm_land."""
    sys.path.insert(0, str(PKG / "code"))
    try:
        from _local_land_solver import fine_osm_land
        land = fine_osm_land(bbox, pad=0.15)
        if land is None or land.is_empty:
            return None, f"{label}: empty result"
        return land, f"{label}: OK ({land.geom_type})"
    except Exception as e:
        return None, f"{label}: FAIL — {e}"


def build_landmask_v2() -> tuple[MultiPolygon, dict]:
    v1 = wkb.loads(V1_WKB.read_bytes())
    meta: dict = {"v1_polys": len(v1.geoms), "removed_palm_idx": sorted(PALM_REMOVE_IDX)}

    kept = [g for i, g in enumerate(v1.geoms) if i not in PALM_REMOVE_IDX]
    meta["kept_polys"] = len(kept)

    palm = palm_land_polys()
    reclaim = reclamation_polys()
    meta["palm_polys_authored"] = len(palm)
    meta["reclamation_polys"] = len(reclaim)

    overpass_notes: list[str] = []
    overpass_polys: list = []

    palm_bbox = (55.105, 25.080, 55.170, 25.150)
    ad_bbox = (54.30, 24.40, 54.68, 24.83)
    for bbox, label in [(palm_bbox, "Palm Overpass"), (ad_bbox, "AD coast Overpass")]:
        land, note = try_overpass_land(bbox, label)
        overpass_notes.append(note)
        if land is not None:
            palm_box = box(*PALM_BBOX)
            ad_box = box(54.30, 24.40, 54.68, 24.83)
            clip_box = palm_box if "Palm" in label else ad_box
            clipped = land.intersection(clip_box)
            if not clipped.is_empty:
                if clipped.geom_type == "Polygon":
                    overpass_polys.append(clipped)
                elif clipped.geom_type == "MultiPolygon":
                    overpass_polys.extend(clipped.geoms)
                elif clipped.geom_type == "GeometryCollection":
                    overpass_polys.extend(
                        g for g in clipped.geoms if g.geom_type in ("Polygon", "MultiPolygon")
                    )
    meta["overpass"] = overpass_notes
    meta["overpass_polys"] = len(overpass_polys)
    meta["overpass_merged"] = False
    # Overpass faces inside Palm/AD bbox fill frond channels when unioned — log only, do not merge.
    if overpass_polys:
        meta["overpass"] = overpass_notes + [
            "Overpass polygons NOT merged into v2 (would solidify Palm frond channels)."
        ]

    # Union v1 (minus solid Palm blobs) + authored palm fronds + reclamation
    merged = unary_union(kept + palm + reclaim)

    # LB-221 channel holes — subtract dredged fairways (Hud/Lulu/Saadiyat/Reem/Yas)
    from ad_channel_cutouts import channel_cutout_polygons, jetty_core_polys

    cutouts = channel_cutout_polygons()
    if cutouts:
        merged = merged.difference(unary_union(cutouts))
    merged = unary_union([merged] + jetty_core_polys())
    meta["ad_channel_cutouts"] = len(cutouts)
    meta["ad_jetty_cores"] = len(jetty_core_polys())

    if merged.geom_type == "Polygon":
        result = MultiPolygon([merged])
    elif merged.geom_type == "MultiPolygon":
        result = MultiPolygon([g for g in merged.geoms if not g.is_empty])
    else:
        result = MultiPolygon([g for g in merged.geoms if g.geom_type == "Polygon" and not g.is_empty])

    meta["v2_polys"] = len(result.geoms)
    return result, meta


def is_land_pt(geom: MultiPolygon, lon: float, lat: float) -> bool:
    return geom.contains(Point(lon, lat))


def nearest_coast_normal(
    geom: MultiPolygon, lon: float, lat: float, search_m: float = 800.0
) -> tuple[float, float, float, float] | None:
    """Return (seaward_lng, seaward_lat, normal_deg, offshore_m) or None."""
    pt = Point(lon, lat)
    best: tuple[float, tuple[float, float], float, float] | None = None

    for poly in geom.geoms:
        if not poly.boundary.intersects(pt.buffer(0.02)):
            # also consider polys whose boundary is nearest even if BP is in water
            pass
        boundary = poly.boundary
        nearest = boundary.interpolate(boundary.project(pt))
        dx = pt.x - nearest.x
        dy = pt.y - nearest.y
        dist_deg = math.hypot(dx, dy)
        if dist_deg < 1e-9:
            continue
        # outward from land: if point inside land, normal points away from land interior
        inside = poly.contains(pt)
        if inside:
            nx, ny = dx / dist_deg, dy / dist_deg
        else:
            # BP in water: seaward is away from nearest land (same direction from land to pt)
            nx, ny = dx / dist_deg, dy / dist_deg

        normal_deg = (math.degrees(math.atan2(nx, ny)) + 360) % 360

        for offshore_m in (400, 600, 800, 1000, 1200):
            d_lon = nm_to_deg_lon(offshore_m / 1852.0, lat) * nx
            d_lat = nm_to_deg_lat(offshore_m / 1852.0) * ny
            cand = (lon + d_lon, lat + d_lat)
            if not is_land_pt(geom, cand[0], cand[1]):
                score = haversine_m((lon, lat), cand)
                if best is None or score < best[0]:
                    best = (score, cand, normal_deg, float(offshore_m))
                break

    if best is None:
        # Fallback: radial search for open water
        for deg in range(0, 360, 10):
            for dist_m in (300, 500, 700, 900):
                rad = math.radians(deg)
                d_lon = nm_to_deg_lon(dist_m / 1852.0, lat) * math.sin(rad)
                d_lat = nm_to_deg_lat(dist_m / 1852.0) * math.cos(rad)
                cand = (lon + d_lon, lat + d_lat)
                if not is_land_pt(geom, cand[0], cand[1]):
                    return cand[0], cand[1], float(deg), float(dist_m)
        return None

    _, cand, normal_deg, offshore_m = best
    return cand[0], cand[1], normal_deg, offshore_m


def collect_residual_bp_ids() -> set[str]:
    ids: set[str] = set()
    for line in REQUESTS.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("priority_tier") != "densify-residual-LB-211":
            continue
        for key in ("from_id", "to_id"):
            v = row.get(key)
            if v:
                ids.add(v)
    return ids


def build_seaward_candidates(landmask: MultiPolygon) -> dict:
    bp_ids = collect_residual_bp_ids()
    bp_data = {b["id"]: b for b in json.loads(BPS.read_text())["boarding_points"]}

    candidates: dict = {}
    missing: list[str] = []

    for bp_id in sorted(bp_ids):
        bp = bp_data.get(bp_id)
        if not bp:
            # city-level ids (abu-dhabi-uae, doha-qatar) — use request coords
            for line in REQUESTS.read_text().splitlines():
                row = json.loads(line)
                if row.get("from_id") == bp_id:
                    lng, lat = row["from_coord"]
                    name = row.get("from_name") or bp_id
                    break
                if row.get("to_id") == bp_id:
                    lng, lat = row["to_coord"]
                    name = row.get("to_name") or bp_id
                    break
            else:
                missing.append(bp_id)
                continue
        else:
            lng, lat = bp["lng"], bp["lat"]
            name = bp["name"]

        result = nearest_coast_normal(landmask, lng, lat)
        if result is None:
            candidates[bp_id] = {
                "bp_name": name,
                "bp_coord": [lng, lat],
                "seaward_coord": None,
                "coast_normal_deg": None,
                "distance_offshore_m": None,
                "source": "v2_landmask",
                "status": "UNRESOLVED",
            }
            continue

        slng, slat, normal_deg, offshore_m = result
        candidates[bp_id] = {
            "bp_name": name,
            "bp_coord": [round(lng, 6), round(lat, 6)],
            "seaward_coord": [round(slng, 6), round(slat, 6)],
            "coast_normal_deg": round(normal_deg, 1),
            "distance_offshore_m": round(offshore_m, 0),
            "source": "v2_landmask_coast_normal",
            "status": "OK",
        }

    return {
        "_meta": {
            "landmask_version": "uae_gulf_land_v2",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "bp_count": len(bp_ids),
            "resolved": sum(1 for v in candidates.values() if v.get("status") == "OK"),
            "missing_bp_lookup": missing,
            "schema": {
                "bp_id": {
                    "seaward_coord": "[lng, lat]",
                    "coast_normal_deg": "bearing from BP toward open water",
                    "distance_offshore_m": "meters along normal to seaward_coord",
                }
            },
        },
        "candidates": candidates,
    }


def run_sentinels(geom: MultiPolygon) -> list[dict]:
    tests = [
        ("palm_spine_channel", 55.141, 25.118, False),
        ("palm_trunk_mid_channel", 55.142, 25.100, False),
        ("atlantis_jetty", 55.117241, 25.130375, True),
        ("kempinski_jetty", 55.1084, 25.1129, True),
        ("hudayriyat_bp", 54.327324, 24.418703, True),
        ("khalifa_port_bp", 54.651205, 24.808029, True),
        ("lulu_bp", 54.344343, 24.501337, True),
        ("saadiyat_marina", 54.419171, 24.521702, True),
        ("reem_waterfront", 54.401147, 24.484583, True),
        ("open_gulf", 55.05, 25.05, False),
        # AD dredged channels (must be WATER)
        ("hud_channel_mid", 54.284, 24.428, False),
        ("lulu_west_channel_mid", 54.308, 24.468, False),
        ("saadiyat_reem_gap_mid", 54.408, 24.498, False),
        ("yas_north_fairway_mid", 54.555, 24.495, False),
        ("ep_approach_mid", 54.298, 24.458, False),
    ]
    rows = []
    for name, lon, lat, expect_land in tests:
        actual = is_land_pt(geom, lon, lat)
        rows.append({
            "name": name,
            "coord": [lon, lat],
            "expect": "LAND" if expect_land else "WATER",
            "actual": "LAND" if actual else "WATER",
            "pass": actual == expect_land,
        })
    return rows


def write_notes(meta: dict, sentinels: list[dict], seaward: dict) -> None:
    lines = [
        "# Phase 1 Notes — Grok Routing (landmask v2 + seaward candidates)",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Deliverables",
        "",
        "- `uae_gulf_land_v2.wkb` — upgraded landmask",
        "- `seaward-candidates.json` — per-BP coastline-normal seaward points (LB-211)",
        "",
        "## Landmask v2 method",
        "",
        f"- Base: v1 WKB ({meta['v1_polys']} polygons)",
        f"- Removed Palm unified blobs at indices: {meta['removed_palm_idx']}",
        f"- Added {meta['palm_polys_authored']} hand-authored Palm polygons (trunk + fronds + crown + crescent; inter-frond gaps = water)",
        f"- Added {meta['reclamation_polys']} Abu Dhabi reclamation polygons (Hudayriyat, Khalifa Port, Lulu, Saadiyat, Reem)",
        f"- Subtracted {meta.get('ad_channel_cutouts', 0)} dredged-channel cutouts (LB-221 channel holes)",
        f"- Output: {meta['v2_polys']} polygons",
        "",
        "## Overpass (tight-bbox)",
        "",
    ]
    for note in meta.get("overpass", []):
        lines.append(f"- {note}")
    if meta.get("overpass_polys", 0) and not meta.get("overpass_merged"):
        lines.append(
            f"- Fetched {meta['overpass_polys']} Overpass clip polygons; excluded from union (Palm channel safety)"
        )
    lines.extend([
        "",
        "## Sentinel checks",
        "",
        "| Point | Expected | Actual | Pass |",
        "|---|---|---|---|",
    ])
    for s in sentinels:
        ok = "✓" if s["pass"] else "✗"
        lines.append(f"| {s['name']} | {s['expect']} | {s['actual']} | {ok} |")

    lines.extend([
        "",
        "## Seaward candidates (LB-211)",
        "",
        f"- BP ids from densify-residual tier: {seaward['_meta']['bp_count']}",
        f"- Resolved: {seaward['_meta']['resolved']}/{seaward['_meta']['bp_count']}",
    ])
    if seaward["_meta"].get("missing_bp_lookup"):
        lines.append(f"- Missing BP lookup: {seaward['_meta']['missing_bp_lookup']}")

    lines.extend([
        "",
        "## Phase 2 handoff",
        "",
        "- Tasklet wires `seaward-candidates.json` into `_solve_corridor_waypoints.py` / densify pass",
        "- Run `qa_land_crossing.py --overlay uae_gulf_land_v2.wkb` on route-solutions output",
        "- Palm cross-trunk (9): attempt A* with v2 channels; expect 3–5 UNSOLVED needing hand waypoints",
        "",
        "## Kickoff answers (locked)",
        "",
        "1. **Overpass:** tight-bbox first (this build); flag failures above",
        "2. **Seaward JSON shape:** `_meta` + `candidates.{bp_id}` per BRIEF §8",
        "3. **Cross-trunk Palm:** attempt all 9; UNSOLVED where channel selection ambiguous",
    ])

    (OUT / "PHASE1-NOTES.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # Invalidate A* grid cache when landmask geometry changes
    for stale in (OUT / "land_grid_0.02.npy", OUT / "land_grid_meta.json"):
        if stale.exists():
            stale.unlink()

    landmask, meta = build_landmask_v2()
    wkb_path = OUT / "uae_gulf_land_v2.wkb"
    wkb_path.write_bytes(landmask.wkb)

    sentinels = run_sentinels(landmask)
    meta["sentinel_pass"] = sum(1 for s in sentinels if s["pass"])
    meta["sentinel_total"] = len(sentinels)

    seaward = build_seaward_candidates(landmask)
    seaward_path = OUT / "seaward-candidates.json"
    seaward_path.write_text(json.dumps(seaward, indent=2))

    write_notes(meta, sentinels, seaward)

    print(f"Wrote {wkb_path} ({len(landmask.wkb)} bytes, {meta['v2_polys']} polys)")
    print(f"Wrote {seaward_path} ({seaward['_meta']['resolved']}/{seaward['_meta']['bp_count']} resolved)")
    print(f"Sentinels: {meta['sentinel_pass']}/{meta['sentinel_total']} pass")
    for s in sentinels:
        if not s["pass"]:
            print(f"  FAIL {s['name']}: expected {s['expect']} got {s['actual']}")
    return 0 if meta["sentinel_pass"] == meta["sentinel_total"] else 1


if __name__ == "__main__":
    sys.exit(main())