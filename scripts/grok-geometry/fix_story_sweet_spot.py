#!/usr/bin/env python3
"""Wave 5 — fix story routes in the 0.05–1.5 km land band via masks + A* / nudge."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from channel_solver import astar, fast_nudge_solve, get_land_checker, pack_result  # noqa: E402
from mint_hand_waypoints import ocean_chain_solve, solve_route  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402
from story_registry import collect_story_registry  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
TRIAGE_PATH = ROOT / "handoff" / "partner-map-model" / "GEOMETRY-TRIAGE.json"
REPORT_PATH = ROOT / "handoff" / "partner-map-model" / "geometry-sweet-spot-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_routes() -> tuple[list, dict[str, dict]]:
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id = {(f.get("properties") or {}).get("id"): f for f in feats if (f.get("properties") or {}).get("id")}
    return feats, by_id


def try_solvers(lc, a, b, props: dict) -> dict | None:
    sea_nm = props.get("distance_nm")
    from_id = props.get("from")
    to_id = props.get("to")

    res = solve_route(
        lc, a, b,
        from_id=from_id,
        to_id=to_id,
        from_city_id=props.get("from_city_id"),
        to_city_id=props.get("to_city_id"),
        dist_nm=sea_nm,
    )
    if res and res.get("qa_pass"):
        return res

    res = fast_nudge_solve(lc, a, b)
    if res and res.get("qa_pass"):
        return res

    res = ocean_chain_solve(lc, a, b, sea_nm)
    if res and res.get("qa_pass"):
        return res

    span = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
    pad = min(0.5, max(0.15, span * 0.15))
    for res_deg in (0.001, 0.0015, 0.002, 0.003):
        path = astar(lc, a, b, res=res_deg, pad=pad)
        if not path:
            continue
        dd = [a] + path + [b]
        packed = pack_result(lc, dd, "astar_sweet_spot", max_sinuosity=1.35)
        if packed and packed.get("qa_pass"):
            return packed
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-land-km", type=float, default=0.05)
    ap.add_argument("--max-land-km", type=float, default=1.5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--route", nargs="+")
    args = ap.parse_args()

    story = collect_story_registry()
    feats, by_id = load_routes()
    lc = get_land_checker()
    now = utc_now()

    targets: list[tuple[str, float, str]] = []
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
            targets.append((rid, ev["interior_land_km"], "cli"))
    else:
        triage = json.loads(TRIAGE_PATH.read_text()) if TRIAGE_PATH.exists() else {}
        for item in triage.get("priority_fix", []):
            if not item.get("story") or item.get("qa_pass"):
                continue
            rid = item["route_id"]
            if rid not in story:
                continue
            land = item.get("interior_land_km", 0)
            if land < args.min_land_km or land > args.max_land_km:
                continue
            feat = by_id.get(rid)
            if not feat:
                continue
            props = feat.get("properties") or {}
            coords = (feat.get("geometry") or {}).get("coordinates") or []
            ev = evaluate_route(coords, sea_nm=props.get("distance_nm"))
            if ev["qa_pass"]:
                targets.append((rid, land, "mask_only"))
            else:
                targets.append((rid, land, "solve"))

    if args.limit > 0:
        targets = targets[: args.limit]

    fixed = held = mask_only = 0
    results = []
    pending = 0

    for i, (rid, land_before, mode_hint) in enumerate(targets):
        feat = by_id[rid]
        props = feat.get("properties") or {}
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            held += 1
            continue

        before = evaluate_route(coords, sea_nm=props.get("distance_nm"))
        if before["qa_pass"]:
            mask_only += 1
            results.append({"route_id": rid, "action": "mask_only", "land_km_before": land_before})
            continue

        a, b = coords[0], coords[-1]
        solved = try_solvers(lc, a, b, props)
        if not solved or not solved.get("qa_pass"):
            held += 1
            after_land = evaluate_route(coords, sea_nm=props.get("distance_nm"))["interior_land_km"]
            results.append({
                "route_id": rid,
                "action": "held",
                "land_km_before": land_before,
                "land_km_after_eval": after_land,
                "detour": before.get("detour_ratio"),
            })
            continue

        after = evaluate_route(solved["geometry"], sea_nm=props.get("distance_nm"))
        if args.apply:
            feat["geometry"] = {"type": "LineString", "coordinates": solved["geometry"]}
            props["geometry_smooth"] = solved["geometry"]
            props["render_smooth"] = False
            props["_geometry_fix_at"] = now
            props["_geometry_fix_source"] = f"grok/fix_story_sweet_spot:{solved.get('method', 'solver')}"
            props["_geometry_land_km"] = after["interior_land_km"]
            pending += 1
            if pending >= 20:
                ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")
                pending = 0

        fixed += 1
        results.append({
            "route_id": rid,
            "action": "fixed",
            "method": solved.get("method"),
            "land_km_before": land_before,
            "land_km_after": after["interior_land_km"],
            "detour_after": after.get("detour_ratio"),
        })
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(targets)}] fixed={fixed} mask_only={mask_only} held={held}", flush=True)

    report = {
        "at": now,
        "mode": "apply" if args.apply else "dry-run",
        "band_km": [args.min_land_km, args.max_land_km],
        "targets": len(targets),
        "fixed": fixed,
        "mask_only": mask_only,
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