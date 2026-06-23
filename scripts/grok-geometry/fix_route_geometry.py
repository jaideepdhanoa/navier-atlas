#!/usr/bin/env python3
"""Re-solve route LineStrings with coastal path builder + land QA."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_coastal_path,
    coastal_waypoints,
    hav_nm,
    load_land_mask,
    push_seaward,
)
from route_land_qa import evaluate_route, interior_land_km  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "handoff" / "partner-map-model" / "geometry-fix-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_routes() -> tuple[list, dict[str, dict]]:
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id = {}
    for f in feats:
        pid = (f.get("properties") or {}).get("id")
        if pid:
            by_id[pid] = f
    return feats, by_id


def endpoints(coords: list) -> tuple[tuple[float, float], tuple[float, float]] | None:
    if len(coords) < 2:
        return None
    a = coords[0]
    b = coords[-1]
    return (a[0], a[1]), (b[0], b[1])


def try_rebuild(
    a: tuple[float, float],
    b: tuple[float, float],
    mask,
    *,
    extra_mid: int = 0,
) -> list[list[float]]:
    dist_nm = hav_nm(a, b)
    best = build_coastal_path(a, b, mask)
    best_land = interior_land_km(best)
    for bump in range(1, 4 + extra_mid):
        n_mid = min(8, 1 + bump + extra_mid)
        manual = coastal_waypoints(a, b, mask, n_mid=n_mid, dist_nm=dist_nm)
        coords = build_coastal_path(a, b, mask, manual_waypoints=manual)
        land = interior_land_km(coords)
        if land < best_land:
            best, best_land = coords, land
        if land <= 0.05:
            break
    if best_land > 0.05:
        for scale in (0.02, 0.04, 0.06, 0.1, 0.15):
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            wp = push_seaward(mid, a, b, mask)
            if wp:
                trial = build_coastal_path(a, b, mask, manual_waypoints=[wp])
                land = interior_land_km(trial)
                if land < best_land:
                    best, best_land = trial, land
    return best


def fix_feature(feat: dict, mask, *, force: bool = False) -> dict | None:
    props = feat.setdefault("properties", {})
    coords = (feat.get("geometry") or {}).get("coordinates") or []
    if len(coords) < 2:
        return None
    ep = endpoints(coords)
    if not ep:
        return None
    a, b = ep
    before = evaluate_route(coords, sea_nm=props.get("distance_nm"))
    if before["qa_pass"] and not force:
        return {"route_id": props.get("id"), "action": "skip_pass", "land_km": before["interior_land_km"]}

    rebuilt = try_rebuild(a, b, mask)
    after = evaluate_route(rebuilt, sea_nm=props.get("distance_nm"))
    improved = after["interior_land_km"] < before["interior_land_km"] - 1e-6
    if not after["qa_pass"] and not improved:
        return {
            "route_id": props.get("id"),
            "action": "held",
            "land_km_before": before["interior_land_km"],
            "land_km_after": after["interior_land_km"],
        }

    feat["geometry"] = {"type": "LineString", "coordinates": rebuilt}
    props["geometry_smooth"] = rebuilt
    props["_geometry_fix_at"] = utc_now()
    props["_geometry_fix_source"] = "grok/fix_route_geometry"
    props["_geometry_land_km"] = after["interior_land_km"]
    props["render_smooth"] = False
    return {
        "route_id": props.get("id"),
        "action": "fixed" if after["qa_pass"] else "improved",
        "land_km_before": before["interior_land_km"],
        "land_km_after": after["interior_land_km"],
        "qa_pass": after["qa_pass"],
    }


def save_routes(feats: list) -> None:
    ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--route", nargs="+", help="specific route ids")
    ap.add_argument("--story", action="store_true", help="all story registry routes")
    ap.add_argument("--allowlisted", action="store_true", help="routes on water allowlist")
    ap.add_argument("--fail-only", action="store_true", default=True)
    ap.add_argument("--all", dest="all_routes", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    from story_registry import collect_story_registry  # noqa: E402

    feats, by_id = load_routes()
    mask = load_land_mask()
    targets: set[str] = set()

    if args.route:
        targets.update(args.route)
    if args.story:
        targets.update(collect_story_registry().keys())
    if args.allowlisted:
        allow_path = ROOT / "data-clean" / "route_water_allowlist.json"
        if allow_path.exists():
            doc = json.loads(allow_path.read_text())
            targets.update(doc.get("ids") or [])
    if args.all_routes:
        targets.update(by_id.keys())

    if not targets:
        print("No targets — use --story, --route, --allowlisted, or --all", file=sys.stderr)
        return 2

    results = []
    fixed = held = skipped = 0
    for rid in sorted(targets):
        feat = by_id.get(rid)
        if not feat:
            results.append({"route_id": rid, "action": "missing"})
            continue
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        if args.fail_only and not args.force:
            ev = evaluate_route(coords, sea_nm=(feat.get("properties") or {}).get("distance_nm"))
            if ev["qa_pass"]:
                skipped += 1
                continue
        row = fix_feature(feat, mask, force=args.force)
        if not row:
            continue
        results.append(row)
        if row["action"] in ("fixed", "improved"):
            fixed += 1
        elif row["action"] == "held":
            held += 1
        elif row["action"] == "skip_pass":
            skipped += 1

    report = {
        "at": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "targets": len(targets),
        "fixed": fixed,
        "held": held,
        "skipped": skipped,
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    if args.apply and fixed:
        save_routes(feats)

    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())