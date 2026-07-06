#!/usr/bin/env python3
"""Restore lost corridors from peak-vs-current OD-pair diff (Tasklet register).

Primary strategy: copy water-validated geometry from peak ROUTES @ 9c85d855 by
canonical city-pair key (51/51 register entries match peak). Re-stamp cluster_id
to canonical. Minting gaps (Hua Hin) built fresh when no peak OD exists.

Guardrail: nobody invents a pier — null beats wrong.
"""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-bucketC-thailand"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    build_coastal_path,
    densify,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    resolve_bp_by_label,
    route_features,
    save_routes,
)

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean" / "CLUSTERS.json"
FBT_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
REGISTER_PATH = ROOT / "handoff" / "LOST-CORRIDORS-CLASSIFIED-2026-07-06.json"
REPORT_PATH = ROOT / "grok-routing-output" / "corridor-restore-report.json"
HANDOFF_REPORT = ROOT / "handoff" / "CORRIDOR-RESTORE-2026-07-06.json"
PEAK_REF = "9c85d855"

B_DIST_MIN_NM = 60.0
B_DIST_MAX_NM = 180.0

# Minting gaps — BPs exist; never sealed in current ROUTES.json
MINTING_GAPS = [
    {
        "from_city_id": "bangkok-thailand",
        "to_city_id": "hua-hin-thailand",
        "from_bp": "bp-778dc1efd0",
        "to_bp": "hua-hin-cross-gulf-ferry-pier",
        "waypoints": [(100.15, 12.05), (100.45, 11.92), (100.72, 12.35)],
    },
    {
        "from_city_id": "pattaya-thailand",
        "to_city_id": "hua-hin-thailand",
        "from_bp": None,
        "to_bp": "hua-hin-pier",
        "from_label": "Bali Hai Pier",
        "waypoints": [(100.15, 12.05), (100.45, 11.92), (100.72, 12.35)],
    },
    {
        "from_city_id": "hua-hin-thailand",
        "to_city_id": "cha-am-thailand",
        "from_bp": "hua-hin-pier",
        "to_bp": None,
        "to_label": "Cha-Am Beach Pier",
        "waypoints": [(99.956, 12.68)],
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def load_peak_routes() -> list[dict]:
    raw = subprocess.check_output(["git", "show", f"{PEAK_REF}:data-clean/ROUTES.json"], cwd=ROOT)
    obj = json.loads(raw)
    return obj if isinstance(obj, list) else obj.get("features", [])


def load_city_to_cluster() -> dict[str, str]:
    out: dict[str, str] = {}
    for c in load_json(CLUSTERS_PATH).get("clusters") or []:
        for city in c.get("member_city_ids") or []:
            out[city] = c["cluster_id"]
    return out


def city_pair_key(a: str | None, b: str | None) -> tuple[str, str] | None:
    if not a or not b:
        return None
    return tuple(sorted([a, b]))


def existing_city_pairs(routes: list) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for feat in routes:
        p = props(feat)
        key = city_pair_key(p.get("from_city_id"), p.get("to_city_id"))
        if key:
            pairs.add(key)
    return pairs


def canonical_cluster(
    from_city: str | None,
    to_city: str | None,
    city_to_cluster: dict[str, str],
) -> str | None:
    clusters = {city_to_cluster.get(c) for c in (from_city, to_city) if c and city_to_cluster.get(c)}
    clusters.discard(None)
    if len(clusters) == 1:
        return next(iter(clusters))
    if from_city and city_to_cluster.get(from_city):
        return city_to_cluster[from_city]
    if to_city and city_to_cluster.get(to_city):
        return city_to_cluster[to_city]
    return None


def index_peak_by_pair(peak: list[dict]) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    for feat in peak:
        p = props(feat)
        key = city_pair_key(p.get("from_city_id"), p.get("to_city_id"))
        if key:
            out[key] = feat
    return out


def restore_peak_feature(
    entry: dict,
    peak_feat: dict,
    *,
    bucket: str,
    city_to_cluster: dict[str, str],
    mask,
    existing_ids: set[str],
    report: dict,
) -> dict | None:
    feat = copy.deepcopy(peak_feat)
    p = props(feat)
    coords = feat.get("geometry", {}).get("coordinates") or []
    land_km = interior_land_km(coords, mask) if coords else 999.0

    stamp = canonical_cluster(p.get("from_city_id"), p.get("to_city_id"), city_to_cluster)
    if stamp:
        p["cluster_id"] = stamp

    dist = p.get("distance_nm") or 0
    if bucket == "REVIEW_midrange_qlr_candidate" and B_DIST_MIN_NM <= dist <= B_DIST_MAX_NM:
        p["platform"] = "Quanta-LR"
        p["edge_class"] = "trunk"

    rid = p.get("id")
    if not rid or rid in existing_ids:
        fn = p.get("from_node") or p.get("from")
        tn = p.get("to_node") or p.get("to")
        if fn and tn:
            rid = mint_route_id(fn, tn, tag="restore")
            p["id"] = rid

    if rid in existing_ids:
        report["skipped"].append({**entry, "reason": "route_id_exists", "route_id": rid, "bucket": bucket})
        return None

    p["_corridor_restore_from_peak"] = PEAK_REF
    p["_corridor_restore_bucket"] = bucket
    p["_corridor_restore_at"] = utc_now()
    p["_land_km_interior"] = round(land_km, 4)

    report["minted"].append(
        {
            "route_id": rid,
            "bucket": bucket,
            "source": "peak",
            "from_city_id": p.get("from_city_id"),
            "to_city_id": p.get("to_city_id"),
            "distance_nm": dist,
            "land_km": round(land_km, 3),
            "platform": p.get("platform"),
        }
    )
    if land_km > 5.0:
        report["flags"].append({"route_id": rid, "land_km": round(land_km, 3), "note": "peak_geometry_land_advisory"})
    return feat


def mint_gap(
    gap: dict,
    *,
    bp_idx: dict,
    cities: dict,
    mask,
    city_to_cluster: dict[str, str],
    existing_ids: set[str],
    report: dict,
) -> dict | None:
    fc, tc = gap["from_city_id"], gap["to_city_id"]
    from_bp = gap.get("from_bp") or resolve_bp_by_label(fc, gap.get("from_label"), bp_idx)
    to_bp = gap.get("to_bp") or resolve_bp_by_label(tc, gap.get("to_label"), bp_idx)
    if not from_bp or not to_bp or from_bp == to_bp:
        report["skipped"].append({**gap, "reason": "unresolved_bp", "from_bp": from_bp, "to_bp": to_bp})
        return None

    a = bp_idx[from_bp]["coords"]
    b = bp_idx[to_bp]["coords"]
    wps = [tuple(w) for w in gap.get("waypoints") or []]
    if wps:
        pts = [a, *wps, b]
        coords: list = []
        for i in range(len(pts) - 1):
            seg = densify(pts[i], pts[i + 1], 18)
            coords.extend(seg if not coords else seg[1:])
    else:
        coords = build_coastal_path(a, b, mask)
    land_km = interior_land_km(coords, mask)

    feat = make_route_feature(
        from_bp,
        to_bp,
        bp_idx[from_bp]["name"],
        bp_idx[to_bp]["name"],
        fc,
        tc,
        coords,
        cities,
        source="corridor_restore_minting_gap",
        land_km=land_km,
    )
    p = props(feat)
    rid = mint_route_id(from_bp, to_bp, tag="thgulf")
    if rid in existing_ids:
        report["skipped"].append({**gap, "reason": "route_id_exists", "route_id": rid})
        return None
    p["id"] = rid
    stamp = canonical_cluster(fc, tc, city_to_cluster)
    if stamp:
        p["cluster_id"] = stamp
    p["_corridor_restore_bucket"] = "minting_gap"
    p["_corridor_restore_at"] = utc_now()

    report["minted"].append(
        {
            "route_id": rid,
            "bucket": "minting_gap",
            "source": "fresh_mint",
            "from_city_id": fc,
            "to_city_id": tc,
            "distance_nm": p.get("distance_nm"),
            "land_km": round(land_km, 3),
        }
    )
    return feat


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--register", default=str(REGISTER_PATH))
    ap.add_argument("--skip-b", action="store_true")
    args = ap.parse_args()

    register = load_json(Path(args.register))
    buckets = register.get("buckets") or {}

    routes = route_features(load_json(ROUTES_PATH))
    peak = load_peak_routes()
    peak_by_pair = index_peak_by_pair(peak)
    pairs = existing_city_pairs(routes)
    existing_ids = {props(r).get("id") for r in routes if props(r).get("id")}

    fbt = load_json(FBT_PATH)
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    mask = load_land_mask()
    city_to_cluster = load_city_to_cluster()

    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "peak_ref": PEAK_REF,
        "routes_before": len(routes),
        "minted": [],
        "skipped": [],
        "flags": [],
    }

    new_routes: list[dict] = []

    for bucket_name in ("RESTORE_in_range", "REVIEW_midrange_qlr_candidate"):
        if bucket_name == "REVIEW_midrange_qlr_candidate" and args.skip_b:
            continue
        for entry in buckets.get(bucket_name) or []:
            key = city_pair_key(entry.get("from_city_id"), entry.get("to_city_id"))
            if not key:
                report["skipped"].append({**entry, "reason": "missing_city_ids", "bucket": bucket_name})
                continue
            if key in pairs:
                report["skipped"].append({**entry, "reason": "city_pair_exists", "bucket": bucket_name})
                continue
            peak_feat = peak_by_pair.get(key)
            if not peak_feat:
                report["skipped"].append({**entry, "reason": "no_peak_match", "bucket": bucket_name})
                continue
            feat = restore_peak_feature(
                entry,
                peak_feat,
                bucket=bucket_name,
                city_to_cluster=city_to_cluster,
                mask=mask,
                existing_ids=existing_ids | {props(r).get("id") for r in new_routes},
                report=report,
            )
            if feat:
                new_routes.append(feat)
                pairs.add(key)
                rid = props(feat).get("id")
                if rid:
                    existing_ids.add(rid)

    for gap in MINTING_GAPS:
        key = city_pair_key(gap["from_city_id"], gap["to_city_id"])
        if key and key in pairs:
            report["skipped"].append({**gap, "reason": "city_pair_exists"})
            continue
        feat = mint_gap(
            gap,
            bp_idx=bp_idx,
            cities=cities,
            mask=mask,
            city_to_cluster=city_to_cluster,
            existing_ids=existing_ids | {props(r).get("id") for r in new_routes},
            report=report,
        )
        if feat:
            new_routes.append(feat)
            if key:
                pairs.add(key)
            rid = props(feat).get("id")
            if rid:
                existing_ids.add(rid)

    routes.extend(new_routes)
    report["routes_after"] = len(routes)
    report["summary"] = {
        "minted": len(report["minted"]),
        "skipped": len(report["skipped"]),
        "flags": len(report["flags"]),
        "by_bucket": {},
    }
    for m in report["minted"]:
        b = m.get("bucket", "unknown")
        report["summary"]["by_bucket"][b] = report["summary"]["by_bucket"].get(b, 0) + 1

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    HANDOFF_REPORT.write_text(json.dumps({"generated": report["generated"], "lane": "corridor-restore", **report["summary"], "minted": report["minted"], "skipped_sample": report["skipped"][:30], "flags": report["flags"]}, indent=2) + "\n")

    print(
        f"  corridor restore: +{len(report['minted'])} from peak/gaps · skipped {len(report['skipped'])} "
        f"· routes {report['routes_before']} → {report['routes_after']}"
    )
    for b, n in sorted(report["summary"]["by_bucket"].items()):
        print(f"    {b}: {n}")

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        print(f"  wrote {ROUTES_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())