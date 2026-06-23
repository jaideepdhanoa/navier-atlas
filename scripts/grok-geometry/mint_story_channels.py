#!/usr/bin/env python3
"""Batch channel mint for story routes — nudge-first, then hand waypoints + A*."""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from channel_solver import (  # noqa: E402
    densify,
    get_land_checker,
    hand_waypoints_for,
    offset_point,
    solve_endpoints,
    solve_hand,
)
from route_land_qa import evaluate_route  # noqa: E402
from story_registry import collect_story_registry  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "handoff" / "partner-map-model" / "geometry-channel-mint-report.json"
SOLUTIONS_PATH = ROOT / "grok-routing-output" / "route-solutions.jsonl"

_OFFSET_CACHE: dict[tuple[float, float], list[list[float]]] = {}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_routes() -> tuple[list, dict[str, dict]]:
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id = {(f.get("properties") or {}).get("id"): f for f in feats if (f.get("properties") or {}).get("id")}
    return feats, by_id


def quick_offsets(lc, pt: list[float], *, max_pts: int = 14) -> list[list[float]]:
    key = (round(pt[0], 4), round(pt[1], 4))
    if key in _OFFSET_CACHE:
        return _OFFSET_CACHE[key]
    out: list[list[float]] = []
    if not lc.is_land(pt[1], pt[0]):
        out.append(pt)
    for r in (0.001, 0.002, 0.004, 0.008, 0.015, 0.025, 0.04):
        for az in range(0, 360, 45):
            p = [pt[0] + r * math.cos(math.radians(az)), pt[1] + r * math.sin(math.radians(az))]
            if not lc.is_land(p[1], p[0]):
                out.append(p)
    seen = set()
    uniq = []
    for p in out:
        k = (round(p[0], 5), round(p[1], 5))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(p)
    uniq = uniq[:max_pts]
    _OFFSET_CACHE[key] = uniq
    return uniq


def nudge_solve(lc, a: list[float], b: list[float], dist_nm: float | None) -> dict | None:
    """Fast seaward endpoint + midpoint search using canonical land QA."""
    aa = quick_offsets(lc, a)
    bb = quick_offsets(lc, b)
    mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]

    for ca in aa:
        for cb in bb:
            geom = densify([ca, cb])
            ev = evaluate_route(geom, sea_nm=dist_nm)
            if ev["qa_pass"]:
                return {"geometry": geom, "method": "nudge_direct", "qa_pass": True, "interior_land_km": ev["interior_land_km"]}

    for az in range(0, 360, 45):
        for dist_m in (500, 1500, 4000, 10000):
            wp = offset_point(mid, az, dist_m)
            if lc.is_land(wp[1], wp[0]):
                continue
            for ca in aa[:6]:
                for cb in bb[:6]:
                    geom = densify([ca, wp, cb])
                    ev = evaluate_route(geom, sea_nm=dist_nm)
                    if ev["qa_pass"]:
                        return {"geometry": geom, "method": "nudge_mid", "qa_pass": True, "interior_land_km": ev["interior_land_km"]}
    return None


def solve_route(
    lc,
    a: list[float],
    b: list[float],
    *,
    from_id: str | None,
    to_id: str | None,
    dist_nm: float | None,
    land_before: float,
    nudge_only: bool = False,
) -> dict | None:
    res = nudge_solve(lc, a, b, dist_nm)
    if res:
        return res

    if nudge_only:
        return None

    wps = hand_waypoints_for(from_id, to_id)
    if wps:
        solved = solve_hand(lc, a, b, wps)
        if solved and solved.get("qa_pass"):
            return solved

    res = solve_endpoints(
        a, b,
        from_id=from_id,
        to_id=to_id,
        dist_nm=dist_nm,
        lc=lc,
        story_mode=True,
    )
    if res and res.get("qa_pass"):
        return res

    if land_before <= 5.0:
        return None

    # Two-midpoint grid for medium crossings
    for frac_a in (0.33, 0.5):
        for frac_b in (0.5, 0.66):
            if frac_b <= frac_a:
                continue
            p1 = [a[0] + frac_a * (b[0] - a[0]), a[1] + frac_a * (b[1] - a[1])]
            p2 = [a[0] + frac_b * (b[0] - a[0]), a[1] + frac_b * (b[1] - a[1])]
            for az in range(0, 360, 60):
                for dist_m in (3000, 8000, 20000):
                    w1 = offset_point(p1, az, dist_m)
                    w2 = offset_point(p2, (az + 120) % 360, dist_m)
                    if lc.is_land(w1[1], w1[0]) or lc.is_land(w2[1], w2[0]):
                        continue
                    for ca in quick_offsets(lc, a, max_pts=6)[:4]:
                        for cb in quick_offsets(lc, b, max_pts=6)[:4]:
                            geom = densify([ca, w1, w2, cb])
                            ev = evaluate_route(geom, sea_nm=dist_nm)
                            if ev["qa_pass"]:
                                return {
                                    "geometry": geom,
                                    "method": "grid_2mid",
                                    "qa_pass": True,
                                    "interior_land_km": ev["interior_land_km"],
                                }
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--story", action="store_true", default=True)
    ap.add_argument("--fail-only", action="store_true", default=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--route", nargs="+")
    ap.add_argument("--min-land-km", type=float, default=0.0)
    ap.add_argument("--max-land-km", type=float, default=0.0, help="0 = no cap")
    ap.add_argument("--nudge-only", action="store_true", help="fast seaward nudge; skip A* channel solver")
    args = ap.parse_args()

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
            if args.fail_only and ev["qa_pass"]:
                continue
            targets.append((rid, ev["interior_land_km"]))
    else:
        for rid in story:
            feat = by_id.get(rid)
            if not feat:
                continue
            props = feat.get("properties") or {}
            coords = (feat.get("geometry") or {}).get("coordinates") or []
            ev = evaluate_route(coords, sea_nm=props.get("distance_nm"))
            if args.fail_only and ev["qa_pass"]:
                continue
            lk = ev["interior_land_km"]
            if lk < args.min_land_km:
                continue
            if args.max_land_km > 0 and lk > args.max_land_km:
                continue
            targets.append((rid, lk))

    targets.sort(key=lambda x: x[1])
    if args.limit > 0:
        targets = targets[: args.limit]

    if not targets:
        print("No targets", file=sys.stderr)
        return 2

    fixed = held = 0
    results = []
    solutions = []
    pending_save = 0

    for i, (rid, land_before) in enumerate(targets):
        feat = by_id[rid]
        props = feat.get("properties") or {}
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            results.append({"route_id": rid, "action": "no_endpoints"})
            held += 1
            continue

        a, b = coords[0], coords[-1]
        solved = solve_route(
            lc, a, b,
            from_id=props.get("from"),
            to_id=props.get("to"),
            dist_nm=props.get("distance_nm"),
            land_before=land_before,
            nudge_only=args.nudge_only,
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
            props["_geometry_fix_at"] = utc_now()
            props["_geometry_fix_source"] = f"grok/mint_story_channels:{solved.get('method', 'channel')}"
            props["_geometry_land_km"] = after["interior_land_km"]
            pending_save += 1
            if pending_save >= 25:
                ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")
                pending_save = 0
                print(f"  checkpoint saved ({i+1}/{len(targets)}) fixed={fixed}", flush=True)

        fixed += 1
        row = {
            "route_id": rid,
            "action": "fixed",
            "method": solved.get("method"),
            "land_km_before": land_before,
            "land_km_after": after["interior_land_km"],
            "qa_pass": after["qa_pass"],
        }
        results.append(row)
        solutions.append({
            "route_id": rid,
            "from_id": props.get("from"),
            "to_id": props.get("to"),
            "qa_pass": True,
            "geometry": {"type": "LineString", "coordinates": solved["geometry"]},
            "method": solved.get("method"),
        })

        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(targets)}] fixed={fixed} held={held}", flush=True)

    report = {
        "at": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "targets": len(targets),
        "fixed": fixed,
        "held": held,
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    if solutions:
        existing = SOLUTIONS_PATH.read_text().splitlines() if SOLUTIONS_PATH.exists() else []
        seen = set()
        for line in existing:
            if line.strip():
                seen.add(json.loads(line).get("route_id"))
        with SOLUTIONS_PATH.open("a") as fh:
            for row in solutions:
                if row["route_id"] not in seen:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    if args.apply and (fixed or pending_save):
        ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")

    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())