#!/usr/bin/env python3
"""
Trim excess _pending_mesh routes while keeping useful capillary coverage.

Policy:
1. Drop mesh routes that duplicate an existing non-mesh BP pair (same from_node/to_node).
2. Drop mesh routes with failed land QA (_qa_land_flag) when a clean alternative exists.
3. Per showcase city, keep the top N mesh routes by usefulness score (default 35).
   - Referenced by partner journeys / economics / corridor binds score highest.
   - Prefer moderate hop lengths (0.4–18 nm); penalize ultra-short hotel-adjacent pairs.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MESH_CITIES = (
    "dubai-uae",
    "abu-dhabi-uae",
    "istanbul-turkey",
    "bodrum-turkey",
    "antalya-turkey",
    "cesme-izmir-turkey",
    "singapore",
)


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def route_features(obj):
    return obj if isinstance(obj, list) else obj.get("features", [])


def props(r: dict) -> dict:
    return r.get("properties", r)


def bp_pair_key(p: dict) -> frozenset[str] | None:
    fn, tn = p.get("from_node"), p.get("to_node")
    if fn and tn:
        return frozenset((fn, tn))
    return None


def collect_referenced_route_ids(dc: Path) -> set[str]:
    refs: set[str] = set()
    econ_path = dc / "economics_by_route_id.json"
    if econ_path.exists():
        econ = load_json(econ_path)
        for rec in econ.get("records", []):
            if rec.get("route_id"):
                refs.add(rec["route_id"])

    for partner in ("bolt", "yango"):
        p_path = dc / "partners" / f"{partner}.json"
        if not p_path.exists():
            continue

        def walk(o):
            if isinstance(o, dict):
                rid = o.get("route_id")
                if rid:
                    refs.add(rid)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for i in o:
                    walk(i)

        walk(load_json(p_path))
    return refs


def mesh_score(p: dict, referenced: set[str]) -> float:
    rid = p.get("id")
    score = 0.0
    if rid in referenced:
        score += 200.0
    if p.get("_corridor_market") or p.get("_pending_bind"):
        score += 120.0
    tw = p.get("traffic_weight")
    if isinstance(tw, (int, float)):
        score += float(tw) * 100.0
    nm = p.get("distance_nm") or p.get("distance_nm_geom")
    if isinstance(nm, (int, float)):
        if 0.4 <= nm <= 18:
            score += 30.0
        elif nm < 0.3:
            score -= 40.0
        elif nm > 30:
            score -= 10.0
    if p.get("_qa_land_flag"):
        score -= 80.0
    return score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--cap-per-city", type=int, default=35)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    routes_path = dc / "ROUTES.json"
    routes_obj = load_json(routes_path)
    feats = route_features(routes_obj)
    referenced = collect_referenced_route_ids(dc)

    pair_routes: dict[frozenset[str], list[tuple[int, dict]]] = defaultdict(list)
    for i, f in enumerate(feats):
        p = props(f)
        key = bp_pair_key(p)
        if key:
            pair_routes[key].append((i, p))

    drop_idxs: set[int] = set()
    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "cap_per_city": args.cap_per_city,
        "dropped": [],
        "kept_mesh_by_city": {},
        "before_mesh": 0,
        "after_mesh": 0,
    }

    mesh_by_idx: list[tuple[int, dict]] = []
    for i, f in enumerate(feats):
        p = props(f)
        if p.get("_pending_mesh"):
            report["before_mesh"] += 1
            mesh_by_idx.append((i, p))

    # Phase 1: duplicate BP-pair mesh (non-mesh route already exists)
    for i, p in mesh_by_idx:
        key = bp_pair_key(p)
        if not key:
            continue
        siblings = pair_routes.get(key, [])
        if any(props(feats[j]).get("_pending_mesh") is not True for j, _ in siblings):
            drop_idxs.add(i)
            report["dropped"].append(
                {"route_id": p.get("id"), "reason": "duplicate_bp_pair", "city": p.get("from_city_id")}
            )

    # Phase 2: per-city cap on remaining mesh
    remaining = [(i, p) for i, p in mesh_by_idx if i not in drop_idxs]
    by_city: dict[str, list[tuple[int, dict, float]]] = defaultdict(list)
    for i, p in remaining:
        city = p.get("from_city_id") or p.get("to_city_id") or "?"
        if city not in MESH_CITIES:
            continue
        by_city[city].append((i, p, mesh_score(p, referenced)))

    for city, rows in by_city.items():
        rows.sort(key=lambda x: -x[2])
        keep = rows[: args.cap_per_city]
        report["kept_mesh_by_city"][city] = len(keep)
        for i, p, sc in rows[args.cap_per_city :]:
            drop_idxs.add(i)
            report["dropped"].append(
                {
                    "route_id": p.get("id"),
                    "reason": "city_cap",
                    "city": city,
                    "score": round(sc, 2),
                }
            )

    kept_feats = [f for i, f in enumerate(feats) if i not in drop_idxs]
    report["after_mesh"] = sum(1 for f in kept_feats if props(f).get("_pending_mesh"))
    report["dropped_total"] = len(drop_idxs)
    report["routes_before"] = len(feats)
    report["routes_after"] = len(kept_feats)

    out_report = ROOT / "grok-routing-output/trim-excess-mesh-report.json"
    out_report.parent.mkdir(parents=True, exist_ok=True)
    save_json(out_report, report)

    if args.dry_run:
        print(f"DRY RUN: would drop {len(drop_idxs)} mesh routes")
        print(f"mesh {report['before_mesh']} -> {report['after_mesh']}")
        print(f"report: {out_report}")
        return

    if isinstance(routes_obj, dict) and "features" in routes_obj:
        routes_obj["features"] = kept_feats
    else:
        routes_obj = kept_feats
    save_json(routes_path, routes_obj)

    dropped_ids = {props(feats[i]).get("id") for i in drop_idxs if props(feats[i]).get("id")}
    allow_path = dc / "route_water_allowlist.json"
    if allow_path.exists() and dropped_ids:
        allow = load_json(allow_path)
        ids = [rid for rid in allow.get("ids", []) if rid not in dropped_ids]
        allow["ids"] = ids
        save_json(allow_path, allow)

    print(f"trimmed {len(drop_idxs)} routes | mesh {report['before_mesh']} -> {report['after_mesh']}")
    print(f"routes {report['routes_before']} -> {report['routes_after']}")
    print(f"report: {out_report}")


if __name__ == "__main__":
    main()