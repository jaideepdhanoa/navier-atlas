#!/usr/bin/env python3
"""A* channel solve for story routes that fail coastal re-solve."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from channel_solver import solve_endpoints  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402
from story_registry import collect_story_registry  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "handoff" / "partner-map-model" / "geometry-channel-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_routes() -> tuple[list, dict[str, dict]]:
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id = {(f.get("properties") or {}).get("id"): f for f in feats if (f.get("properties") or {}).get("id")}
    return feats, by_id


def endpoints(feat: dict) -> tuple[tuple[float, float], tuple[float, float]] | None:
    coords = (feat.get("geometry") or {}).get("coordinates") or []
    if len(coords) < 2:
        return None
    return (coords[0][0], coords[0][1]), (coords[-1][0], coords[-1][1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--story", action="store_true", help="all story registry routes")
    ap.add_argument("--fail-only", action="store_true", default=True)
    ap.add_argument("--all-fail", action="store_true", help="all QA-failing routes (mesh + story)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--route", nargs="+")
    args = ap.parse_args()

    story = collect_story_registry()
    feats, by_id = load_routes()
    targets: list[str] = []

    if args.route:
        targets = list(args.route)
    else:
        for rid, feat in by_id.items():
            if args.story and rid not in story:
                continue
            if not args.story and not args.all_fail:
                continue
            if args.fail_only:
                coords = (feat.get("geometry") or {}).get("coordinates") or []
                props = feat.get("properties") or {}
                ev = evaluate_route(coords, sea_nm=props.get("distance_nm"))
                if ev["qa_pass"]:
                    continue
            targets.append(rid)

    if args.limit > 0:
        targets = targets[: args.limit]
    else:
        # Easier legs first — more fixes early, better checkpoint cadence.
        def _land_km(rid: str) -> float:
            feat = by_id[rid]
            coords = (feat.get("geometry") or {}).get("coordinates") or []
            props = feat.get("properties") or {}
            return evaluate_route(coords, sea_nm=props.get("distance_nm"))["interior_land_km"]

        targets = sorted(targets, key=_land_km)

    if not targets:
        print("No targets", file=sys.stderr)
        return 2

    fixed = held = 0
    results = []
    pending_save = 0
    for i, rid in enumerate(sorted(targets)):
        feat = by_id[rid]
        props = feat.get("properties") or {}
        ep = endpoints(feat)
        if not ep:
            results.append({"route_id": rid, "action": "no_endpoints"})
            continue
        a, b = ep
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        before = evaluate_route(coords, sea_nm=props.get("distance_nm"))

        solved = solve_endpoints(
            a, b,
            from_id=props.get("from"),
            to_id=props.get("to"),
            dist_nm=props.get("distance_nm"),
            story_mode=True,
        )
        if not solved or not solved.get("qa_pass"):
            held += 1
            results.append({
                "route_id": rid,
                "action": "held",
                "land_km_before": before["interior_land_km"],
            })
            continue

        after = evaluate_route(solved["geometry"], sea_nm=props.get("distance_nm"))
        improved = after["interior_land_km"] < before["interior_land_km"] - 1e-6
        if not after["qa_pass"] and not improved:
            held += 1
            results.append({
                "route_id": rid,
                "action": "held",
                "land_km_before": before["interior_land_km"],
                "land_km_after": after["interior_land_km"],
            })
            continue

        if args.apply:
            feat["geometry"] = {"type": "LineString", "coordinates": solved["geometry"]}
            props["geometry_smooth"] = solved["geometry"]
            props["render_smooth"] = False
            props["_geometry_fix_at"] = utc_now()
            props["_geometry_fix_source"] = f"grok/solve_story_channels:{solved.get('method', 'a_star')}"
            props["_geometry_land_km"] = after["interior_land_km"]
            pending_save += 1
            if pending_save >= 25:
                ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")
                pending_save = 0
                print(f"  checkpoint saved ({i+1}/{len(targets)}) fixed={fixed}", flush=True)

        fixed += 1
        results.append({
            "route_id": rid,
            "action": "fixed" if after["qa_pass"] else "improved",
            "method": solved.get("method"),
            "land_km_before": before["interior_land_km"],
            "land_km_after": after["interior_land_km"],
            "qa_pass": after["qa_pass"],
        })
        if (i + 1) % 25 == 0:
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

    if args.apply and (fixed or pending_save):
        ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")

    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())