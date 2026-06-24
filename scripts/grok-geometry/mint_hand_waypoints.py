#!/usr/bin/env python3
"""Tier 5 — apply merged HAND_WAYPOINTS + ocean-chain search to story QA failures."""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))
sys.path.insert(0, str(ROOT / "scripts" / "grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts" / "grok-bucketC-thailand"))

from channel_solver import (  # noqa: E402
    HAND_WAYPOINTS,
    connect_chain,
    densify,
    get_land_checker,
    hand_waypoints_for,
    pack_result,
    solve_hand,
)
from route_land_qa import evaluate_route  # noqa: E402
from story_registry import collect_story_registry  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
TRIAGE_PATH = ROOT / "handoff" / "partner-map-model" / "GEOMETRY-TRIAGE.json"
REPORT_PATH = ROOT / "handoff" / "partner-map-model" / "geometry-hand-waypoints-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def merge_waypoint_catalogs() -> int:
    """Extend HAND_WAYPOINTS from routing-lane scripts (idempotent)."""
    added = 0

    def put(a: str, b: str, wps: list) -> None:
        nonlocal added
        key = (a, b)
        if key not in HAND_WAYPOINTS and wps:
            HAND_WAYPOINTS[key] = [[float(x), float(y)] for x, y in wps]
            added += 1

    try:
        from route_bolt_yango_markets import SIGNATURE_WAYPOINTS as YANGO  # noqa: WPS433

        for (a, b), wps in YANGO.items():
            put(a, b, wps)
    except Exception:
        pass

    try:
        from route_kept_markets import SIGNATURE_WAYPOINTS as KEPT  # noqa: WPS433

        for (a, b), wps in KEPT.items():
            put(a, b, wps)
    except Exception:
        pass

    try:
        from route_bucketC_thailand import SIGNATURE_ROUTES  # noqa: WPS433

        for _city, a, b, wps in SIGNATURE_ROUTES:
            if wps:
                put(a, b, wps)
    except Exception:
        pass

    # City-level Gulf / Andaman corridors (grab-thailand depth)
    city_wps = {
        ("bangkok-thailand", "pattaya-thailand"): [
            [100.75, 13.55], [100.88, 13.25], [100.90, 12.98],
        ],
        ("pattaya-thailand", "koh-samet-thailand"): [
            [100.95, 12.75], [101.15, 12.65], [101.32, 12.58],
        ],
        ("hua-hin-thailand", "pattaya-thailand"): [
            [100.05, 11.85], [100.40, 11.75], [100.72, 12.35],
        ],
        ("hua-hin-thailand", "cha-am-thailand"): [[99.956, 12.68]],
        # Portugal Tagus / Algarve
        ("bp-terreiro-do-paco-lisbon", "bp-ponta-da-piedade"): [
            [-9.20, 38.72], [-9.05, 38.50], [-8.85, 38.30], [-8.72, 37.15],
        ],
        # Hong Kong ↔ Macau
        ("hong-kong__hk-macau-ferry-terminal-sheung-wan", "macau-china__macau-outer-harbour-ferry-terminal"): [
            [113.98, 22.22], [113.88, 22.18], [113.78, 22.16],
        ],
        # Corfu channel hops
        ("corfu-ionian-greece__nidri", "corfu-ionian-greece__gaios"): [
            [20.65, 38.72], [20.58, 38.68],
        ],
        ("corfu-ionian-greece__gouvia-marina", "corfu-ionian-greece__gaios"): [
            [20.62, 39.02], [20.55, 38.85], [20.52, 38.72],
        ],
        # Dubai Harbour / Palm lagoon offshore arc
        ("bp-56d5f5bd8d", "bp-29c2c81221"): [[55.12, 25.08], [55.10, 25.06], [55.08, 25.04]],
        ("bp-56d5f5bd8d", "bp-f0fde14967"): [[55.12, 25.08], [55.08, 25.05], [55.05, 25.02]],
        ("bp-56d5f5bd8d", "bp-d6496ac4e8"): [[55.12, 25.08], [55.14, 25.10], [55.16, 25.12]],
        ("bp-df8901f3ae", "bp-e981496917"): [[55.18, 25.22], [55.20, 25.18], [55.22, 25.14]],
        ("dubai-uae", "sharjah-uae"): [[55.30, 25.20], [55.38, 25.22], [55.42, 25.24]],
        ("dubai-uae", "ras-al-khaimah-uae"): [[55.20, 25.30], [55.45, 25.55], [55.75, 25.72]],
        # Cape Town — wider Atlantic arc
        ("bp-41c1d22c88", "bp-c07f712484"): [[18.28, -33.84], [18.32, -33.80]],
        ("bp-41c1d22c88", "bp-6572ae8691"): [
            [18.22, -33.98], [18.18, -34.08], [18.25, -34.12],
        ],
        ("bp-6572ae8691", "bp-17cbbdad38"): [
            [18.20, -34.18], [18.30, -34.28], [18.42, -34.22],
        ],
    }
    for key, wps in city_wps.items():
        put(key[0], key[1], wps)

    return added


def nearest_ocean(lc, lon: float, lat: float, *, max_deg: float = 0.35) -> list[float] | None:
    if not lc.is_land(lat, lon):
        return [lon, lat]
    for r in [0.002, 0.005, 0.01, 0.02, 0.04, 0.08, 0.12, 0.18, 0.25, 0.35]:
        if r > max_deg:
            break
        for az in range(0, 360, 20):
            p = [
                lon + r * math.cos(math.radians(az)),
                lat + r * math.sin(math.radians(az)),
            ]
            if not lc.is_land(p[1], p[0]):
                return [p[0], p[1]]
    return None


def ocean_chain_solve(lc, a: list[float], b: list[float], dist_nm: float | None) -> dict | None:
    """Place ocean anchors along the chord and A*-connect."""
    mids = []
    for frac in (0.25, 0.5, 0.75):
        mid = [a[0] + frac * (b[0] - a[0]), a[1] + frac * (b[1] - a[1])]
        span = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
        oc = nearest_ocean(lc, mid[0], mid[1], max_deg=min(0.5, 0.15 + span * 0.15))
        if oc:
            mids.append(oc)

    if not mids:
        return None

    pts = [a] + mids + [b]
    path = connect_chain(lc, pts)
    if not path:
        # direct hand chain through ocean mids
        dd = [a]
        for m in mids:
            if m != dd[-1]:
                dd.append(m)
        dd.append(b)
        res = pack_result(lc, dd, "ocean_chain", max_sinuosity=4.0)
        return res if res and res.get("qa_pass") else None

    full = [a] + [p for p in path if p != a and p != b] + [b]
    dd = [full[0]]
    for p in full[1:]:
        if p != dd[-1]:
            dd.append(p)
    res = pack_result(lc, dd, "ocean_chain", max_sinuosity=4.0)
    return res if res and res.get("qa_pass") else None


def solve_route(
    lc,
    a: list[float],
    b: list[float],
    *,
    from_id: str | None,
    to_id: str | None,
    from_city_id: str | None = None,
    to_city_id: str | None = None,
    dist_nm: float | None,
) -> dict | None:
    wps = hand_waypoints_for(from_id, to_id, from_city_id=from_city_id, to_city_id=to_city_id)
    if wps:
        res = solve_hand(lc, a, b, wps)
        if res and res.get("qa_pass"):
            return res

    res = ocean_chain_solve(lc, a, b, dist_nm)
    if res:
        return res

    # brute 2-mid perpendicular offsets for island-hops
    for frac_a, frac_b in ((0.33, 0.66), (0.4, 0.6)):
        p1 = [a[0] + frac_a * (b[0] - a[0]), a[1] + frac_a * (b[1] - a[1])]
        p2 = [a[0] + frac_b * (b[0] - a[0]), a[1] + frac_b * (b[1] - a[1])]
        o1 = nearest_ocean(lc, p1[0], p1[1])
        o2 = nearest_ocean(lc, p2[0], p2[1])
        if not o1 or not o2:
            continue
        dd = [a, o1, o2, b]
        res = pack_result(lc, dd, "ocean_pair", max_sinuosity=4.5)
        if res and res.get("qa_pass"):
            return res
    return None


def load_routes() -> tuple[list, dict[str, dict]]:
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id = {(f.get("properties") or {}).get("id"): f for f in feats if (f.get("properties") or {}).get("id")}
    return feats, by_id


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-land-km", type=float, default=2.0)
    ap.add_argument("--max-land-km", type=float, default=20.0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--route", nargs="+")
    args = ap.parse_args()

    added = merge_waypoint_catalogs()
    print(f"merged {added} new HAND_WAYPOINTS entries (total={len(HAND_WAYPOINTS)})", flush=True)

    story = collect_story_registry()
    feats, by_id = load_routes()
    lc = get_land_checker()

    targets: list[tuple[str, float]] = []
    if args.route:
        for rid in args.route:
            feat = by_id.get(rid)
            if not feat:
                continue
            props = feat.get("properties") or {}
            coords = (feat.get("geometry") or {}).get("coordinates") or []
            ev = evaluate_route(coords, sea_nm=props.get("distance_nm"))
            if ev["qa_pass"]:
                continue
            targets.append((rid, ev["interior_land_km"]))
    else:
        for rid in story:
            if rid not in story:
                continue
            feat = by_id.get(rid)
            if not feat:
                continue
            props = feat.get("properties") or {}
            coords = (feat.get("geometry") or {}).get("coordinates") or []
            ev = evaluate_route(coords, sea_nm=props.get("distance_nm"))
            if ev["qa_pass"]:
                continue
            lk = ev["interior_land_km"]
            if lk < args.min_land_km or lk > args.max_land_km:
                continue
            targets.append((rid, lk))

    targets.sort(key=lambda x: x[1])
    if args.limit > 0:
        targets = targets[: args.limit]

    print(f"targets={len(targets)} land=[{args.min_land_km},{args.max_land_km}]", flush=True)

    fixed = held = 0
    results = []
    pending = 0
    now = utc_now()

    for i, (rid, land_before) in enumerate(targets):
        feat = by_id[rid]
        props = feat.get("properties") or {}
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            held += 1
            continue
        a, b = coords[0], coords[-1]
        solved = solve_route(
            lc, a, b,
            from_id=props.get("from"),
            to_id=props.get("to"),
            from_city_id=props.get("from_city_id"),
            to_city_id=props.get("to_city_id"),
            dist_nm=props.get("distance_nm"),
        )
        if not solved or not solved.get("qa_pass"):
            held += 1
            results.append({"route_id": rid, "action": "held", "land_km_before": land_before})
            continue

        after = evaluate_route(solved["geometry"], sea_nm=props.get("distance_nm"))
        if args.apply:
            feat["geometry"] = {"type": "LineString", "coordinates": solved["geometry"]}
            props["geometry_smooth"] = solved["geometry"]
            props["render_smooth"] = False
            props["_geometry_fix_at"] = now
            props["_geometry_fix_source"] = f"grok/mint_hand_waypoints:{solved.get('method', 'hand')}"
            props["_geometry_land_km"] = after["interior_land_km"]
            pending += 1
            if pending >= 20:
                ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")
                pending = 0
                print(f"  checkpoint ({i+1}/{len(targets)}) fixed={fixed}", flush=True)

        fixed += 1
        results.append({
            "route_id": rid,
            "action": "fixed",
            "method": solved.get("method"),
            "land_km_before": land_before,
            "land_km_after": after["interior_land_km"],
        })
        if (i + 1) % 25 == 0:
            print(f"  [{i+1}/{len(targets)}] fixed={fixed} held={held}", flush=True)

    report = {
        "at": now,
        "mode": "apply" if args.apply else "dry-run",
        "waypoints_merged": added,
        "targets": len(targets),
        "fixed": fixed,
        "held": held,
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    if args.apply and (fixed or pending):
        ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")

    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())