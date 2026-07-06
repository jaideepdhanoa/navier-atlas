#!/usr/bin/env python3
"""Grok Pass 1 — global corridor reseal across all 116 contested clusters (one batch)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts/grok-global"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    NM_PER_KM,
    build_bp_index,
    build_city_index,
    build_coastal_path,
    hav_nm,
    load_json,
    make_route_feature,
    mint_route_id,
    path_length_km,
    route_features,
    route_id_of,
    save_json,
    save_routes,
)
from bolt_yango_shared import load_land_mask  # noqa: E402
from channel_solver import HAND_WAYPOINTS  # noqa: E402
from route_land_qa import evaluate_route  # noqa: E402

from cluster_scope import (  # noqa: E402
    UAE_PRE_SEALED_CLUSTERS,
    NEVER_MINT_PAIRS,
    load_contention_order,
    min_nm_for_cluster,
    resolve_cluster_city_ids,
)

REPORT = ROOT / "grok-routing-output" / "global-corridor-consolidation-report.json"
SEAL_TAG = "global-corridor-consolidation-2026-07-06"
LAND_THRESH_KM = 0.05
MAX_NM = 70.0
MAX_NM_CROSS_BORDER = 150.0
DEDUPE_KM = 0.4
MAX_BPS_PER_CITY = 10

CROSS_BORDER_LEGIT = re.compile(
    r"batam|bintan|riau|musandam|khasab|langkawi|penang|desaru",
    re.I,
)

DIRTY_RE = re.compile(
    r"jet\s*ski|water\s*sport|diving|divecampus|boat\s*ramp|helipad|seaplane|"
    r"boat\s*yard|shipyard|slipway|parking|dry dock|container port|cargo port|"
    r"under construction|\(planned\)|proposed",
    re.I,
)
CENTROID_NAMES = frozenset(
    {"Abu Dhabi", "Fujairah", "Ras Al Khaimah", "Dubai", "Sharjah", "Bangkok", "Singapore"}
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def load_all_hand_waypoints() -> int:
    added = 0
    dc = ROOT / "data-clean"
    paths = [dc / "uae_hand_waypoints.json", *sorted(dc.glob("pta_hand_waypoints_*.json"))]
    for path in paths:
        if not path.is_file():
            continue
        doc = load_json(path)
        for row in doc.get("pairs") or []:
            fn, tn, wps = row.get("from"), row.get("to"), row.get("waypoints") or []
            if fn and tn and wps:
                key = (fn, tn)
                if key not in HAND_WAYPOINTS:
                    HAND_WAYPOINTS[key] = [[float(w[0]), float(w[1])] for w in wps]
                    added += 1
        for key, wps in (doc.get("waypoints") or {}).items():
            parts = key.split("|", 1)
            if len(parts) == 2 and wps:
                k = (parts[0], parts[1])
                if k not in HAND_WAYPOINTS:
                    HAND_WAYPOINTS[k] = wps
                    added += 1
    return added


def dirty_reason(name: str) -> str | None:
    if not name or not name.strip():
        return "empty_name"
    if name in CENTROID_NAMES:
        return "centroid"
    if DIRTY_RE.search(name):
        return "dirty_endpoint"
    return None


def hub_score(name: str) -> int:
    n = (name or "").lower()
    score = 0
    for token, pts in (
        ("marina", 4),
        ("ferry", 4),
        ("terminal", 4),
        ("harbour", 3),
        ("harbor", 3),
        ("pier", 3),
        ("wharf", 2),
        ("jetty", 2),
        ("island", 2),
    ):
        if token in n:
            score += pts
    return score


def pair_distance_nm(a: str, b: str, bp_idx: dict) -> float:
    return hav_nm(tuple(bp_idx[a]["coords"]), tuple(bp_idx[b]["coords"]))


def blocked_pair(a: str, b: str, bp_idx: dict) -> bool:
    key = frozenset((a, b))
    if key in NEVER_MINT_PAIRS:
        return True
    ac = bp_idx[a].get("parent_city_id") or ""
    bc = bp_idx[b].get("parent_city_id") or ""
    if frozenset((ac, bc)) in NEVER_MINT_PAIRS:
        return True
    return False


def _densify_chain(points: list[tuple[float, float]], steps: int = 16) -> list[list[float]]:
    from bolt_yango_routing_shared import densify  # noqa: WPS433

    out: list[list[float]] = []
    for i in range(len(points) - 1):
        seg = densify(points[i], points[i + 1], n=steps)
        out.extend(seg if not out else seg[1:])
    return out


def _qa_accept(coords: list[list[float]]) -> tuple[bool, float]:
    ev = evaluate_route(coords)
    land = float(ev.get("interior_land_km", 0.0))
    return land <= LAND_THRESH_KM and bool(ev.get("qa_pass")), land


def route_geometry(
    a: str,
    b: str,
    bp_idx: dict,
    mask,
    legacy_geom: dict[tuple[str, str], list],
) -> tuple[list[list[float]], float] | None:
    ac = tuple(bp_idx[a]["coords"])
    bc = tuple(bp_idx[b]["coords"])
    wps: list[tuple[float, float]] = []
    for key in ((a, b), (b, a)):
        if key in HAND_WAYPOINTS and HAND_WAYPOINTS[key]:
            wps = [(float(w[0]), float(w[1])) for w in HAND_WAYPOINTS[key]]
            break

    candidates: list[list[list[float]]] = []
    if wps:
        candidates.append(_densify_chain([ac, *wps, bc]))
        candidates.append(build_coastal_path(ac, bc, mask, manual_waypoints=wps))

    for key in ((a, b), (b, a)):
        old = legacy_geom.get(key)
        if old:
            ok, _ = _qa_accept(old)
            if ok:
                candidates.append(old)
            rev = list(reversed(old))
            ok, _ = _qa_accept(rev)
            if ok:
                candidates.append(rev)

    candidates.append(build_coastal_path(ac, bc, mask))

    for coords in candidates:
        ok, land = _qa_accept(coords)
        if ok:
            return coords, land
    return None


def route_touches_scope(route: dict, scope: set[str], bp_idx: dict) -> bool:
    p = props(route)
    if p.get("cluster_id") and p["cluster_id"] in scope:
        return True
    fc, tc = p.get("from_city_id"), p.get("to_city_id")
    if fc in scope or tc in scope:
        return True
    fn = p.get("from") or p.get("from_node")
    tn = p.get("to") or p.get("to_node")
    for nid in (fn, tn):
        if nid and bp_idx.get(nid, {}).get("parent_city_id") in scope:
            return True
    return False


def select_kept_bps(scope: set[str], bp_idx: dict) -> tuple[dict[str, int], dict[str, str]]:
    kept: dict[str, int] = {}
    dropped: dict[str, str] = {}
    by_city: dict[str, list[str]] = defaultdict(list)

    for pid, row in bp_idx.items():
        city = row.get("parent_city_id")
        if city not in scope:
            continue
        reason = dirty_reason(row.get("name") or "")
        if reason:
            dropped[pid] = reason
            continue
        score = hub_score(row.get("name") or "")
        if score >= 2:
            kept[pid] = score
            by_city[city].append(pid)

    for city, pids in by_city.items():
        pids.sort(key=lambda p: kept[p], reverse=True)
        for pid in pids[MAX_BPS_PER_CITY:]:
            dropped[pid] = "hub_cap"
            kept.pop(pid, None)

    for pids in by_city.values():
        active = [p for p in pids if p in kept]
        remove: set[str] = set()
        for i, a in enumerate(active):
            if a in remove:
                continue
            for b in active[i + 1 :]:
                if b in remove:
                    continue
                if pair_distance_nm(a, b, bp_idx) * 1.852 < DEDUPE_KM:
                    if kept[a] >= kept[b]:
                        remove.add(b)
                    else:
                        remove.add(a)
        for b in remove:
            dropped[b] = "duplicate_proximity"
            kept.pop(b, None)

    return kept, dropped


def build_corridor_pairs(
    kept: dict[str, int],
    bp_idx: dict,
    *,
    min_nm: float,
) -> set[tuple[str, str]]:
    by_city: dict[str, list[str]] = defaultdict(list)
    for pid in kept:
        by_city[bp_idx[pid]["parent_city_id"]].append(pid)

    hubs: list[str] = []
    for pids in by_city.values():
        pids.sort(key=lambda p: kept[p], reverse=True)
        hubs.extend(pids[: min(4, len(pids))])

    pairs: set[tuple[str, str]] = set()
    for a, b in combinations(hubs, 2):
        if blocked_pair(a, b, bp_idx):
            continue
        d = pair_distance_nm(a, b, bp_idx)
        max_nm = MAX_NM_CROSS_BORDER if CROSS_BORDER_LEGIT.search(
            f"{bp_idx[a].get('name','')} {bp_idx[b].get('name','')}"
        ) else MAX_NM
        if min_nm <= d <= max_nm:
            pairs.add(tuple(sorted((a, b))))

    for city, pids in by_city.items():
        pids.sort(key=lambda p: kept[p], reverse=True)
        if len(pids) < 2:
            continue
        hub = pids[0]
        for spoke in pids[1:]:
            if blocked_pair(hub, spoke, bp_idx):
                continue
            d = pair_distance_nm(hub, spoke, bp_idx)
            if min_nm <= d <= MAX_NM:
                pairs.add(tuple(sorted((hub, spoke))))

    return pairs


def vessel_and_render(dist_nm: float) -> tuple[str, str, str]:
    if dist_nm >= 70:
        return "Quanta-LR", "roadmap-amber-dashed", "roadmap"
    return "Pioneer II", "solid", "sealed"


def seal_cluster(
    cluster_id: str,
    scope: set[str],
    *,
    routes: list[dict],
    bp_idx: dict,
    cities: dict,
    mask,
    apply: bool,
) -> dict:
    if cluster_id in UAE_PRE_SEALED_CLUSTERS:
        existing = [
            r
            for r in routes
            if props(r).get("cluster_id") in ("uae", "uae-east-coast", "uae-sir-bani-yas")
            and (
                props(r).get("from_city_id") in scope
                or props(r).get("to_city_id") in scope
            )
        ]
        land_flags = sum(1 for r in existing if props(r).get("_qa_land_flag"))
        return {
            "cluster_id": cluster_id,
            "status": "skipped_pre_sealed_uae",
            "scope_cities": sorted(scope),
            "existing_routes": len(existing),
            "minted": 0,
            "removed": 0,
            "land_flags": land_flags,
            "failed": [],
        }

    min_nm = min_nm_for_cluster(cluster_id, scope)
    kept, dropped = select_kept_bps(scope, bp_idx)
    pairs = build_corridor_pairs(kept, bp_idx, min_nm=min_nm)

    legacy_geom: dict[tuple[str, str], list] = {}
    removed = 0
    kept_routes: list[dict] = []
    for r in routes:
        if route_touches_scope(r, scope, bp_idx):
            p = props(r)
            fn = p.get("from") or p.get("from_node")
            tn = p.get("to") or p.get("to_node")
            coords = r.get("geometry", {}).get("coordinates") or []
            if fn and tn and coords:
                legacy_geom[(fn, tn)] = coords
            removed += 1
        else:
            kept_routes.append(r)

    minted: list[dict] = []
    failed: list[dict] = []
    for a, b in sorted(pairs):
        if a not in bp_idx or b not in bp_idx:
            failed.append({"from": a, "to": b, "reason": "missing_bp"})
            continue
        geom = route_geometry(a, b, bp_idx, mask, legacy_geom)
        if not geom:
            failed.append({"from": a, "to": b, "reason": "no_geometry"})
            continue
        coords, land_km = geom
        ok, land_km = _qa_accept(coords)
        if not ok:
            failed.append(
                {
                    "from": a,
                    "to": b,
                    "reason": "land_crossing",
                    "land_km": land_km,
                }
            )
            continue

        from_city = bp_idx[a].get("parent_city_id")
        to_city = bp_idx[b].get("parent_city_id")
        rid = mint_route_id(a, b, tag="global_consolidation")
        dist_nm = path_length_km(coords) * NM_PER_KM
        platform, render, link_status = vessel_and_render(dist_nm)

        feat = make_route_feature(
            a,
            b,
            bp_idx[a]["name"],
            bp_idx[b]["name"],
            from_city,
            to_city,
            coords,
            cities,
            source="global_consolidation",
            land_km=land_km,
        )
        p = props(feat)
        p["id"] = rid
        p["platform"] = platform
        p["distance_nm"] = round(dist_nm, 1)
        p["_render"] = render
        p["_link_status"] = link_status
        p["cluster_id"] = cluster_id
        p["_global_consolidation_seal"] = utc_now()
        p["_geometry_source"] = "hand_waypoints+coastal"
        p["_qa_land_flag"] = False
        p["_land_km_interior"] = round(land_km, 4)
        minted.append(feat)
        kept_routes.append(feat)

    land_flags = sum(1 for m in minted if props(m).get("_qa_land_flag"))

    if apply:
        routes.clear()
        routes.extend(kept_routes)

    return {
        "cluster_id": cluster_id,
        "status": "resealed",
        "scope_cities": sorted(scope),
        "min_nm": min_nm,
        "bps_kept": len(kept),
        "bps_dropped": len(dropped),
        "candidate_pairs": len(pairs),
        "removed": removed,
        "minted": len(minted),
        "failed_count": len(failed),
        "failed_sample": failed[:8],
        "land_flags": land_flags,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--cluster", nargs="*", help="Limit to cluster_id(s)")
    ap.add_argument("--dry-run", action="store_true", help="Report only (default without --apply)")
    args = ap.parse_args()

    dc = ROOT / "data-clean"
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    routes_raw = load_json(dc / "ROUTES.json")
    routes = route_features(routes_raw)
    mask = load_land_mask()
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    hand_added = load_all_hand_waypoints()

    order = load_contention_order()
    if args.cluster:
        filt = set(args.cluster)
        order = [row for row in order if row["cluster_id"] in filt]

    cluster_reports: list[dict] = []
    total_land = 0
    total_minted = 0
    total_removed = 0

    for row in order:
        cid = row["cluster_id"]
        scope = resolve_cluster_city_ids(cid)
        rep = seal_cluster(
            cid,
            scope,
            routes=routes,
            bp_idx=bp_idx,
            cities=cities,
            mask=mask,
            apply=args.apply,
        )
        cluster_reports.append(rep)
        total_land += rep.get("land_flags", 0)
        total_minted += rep.get("minted", 0)
        total_removed += rep.get("removed", 0)
        print(
            f"  {cid}: {rep.get('status')} "
            f"minted={rep.get('minted',0)} removed={rep.get('removed',0)} "
            f"land={rep.get('land_flags',0)}"
        )

    receipt = {
        "generated_at": utc_now(),
        "seal_tag": SEAL_TAG,
        "apply": args.apply,
        "hand_waypoints_loaded": hand_added,
        "clusters_processed": len(cluster_reports),
        "totals": {
            "minted": total_minted,
            "removed": total_removed,
            "land_flags": total_land,
            "routes_after": len(routes),
        },
        "clusters": cluster_reports,
    }

    if args.apply:
        save_routes(dc / "ROUTES.json", routes)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt["totals"], indent=2))

    if total_land > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())