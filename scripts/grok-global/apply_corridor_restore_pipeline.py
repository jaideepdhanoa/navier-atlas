#!/usr/bin/env python3
"""Corridor restore pipeline — Taiwan, Batch 2b, global intra-metro on-water restore.

Sequence (Tasklet bf35af7e + bp-wishlist spec):
  1. Taiwan — 5 real OD corridors (regression fix)
  2. Batch 2b — 5 isolated-city corridors (Koh Lanta + Riviera)
  3. Intra-metro — RESTORE-REGISTER-intra-metro-onwater (Jul-3 copy-proven)

Copy July-3 geometry; re-seal edge-/gcn-/e__/ics- → fresh rn-; dedupe by endpoint pair.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-global"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_coastal_path,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    route_features,
    save_routes,
)
from cluster_scope import UAE_PRE_SEALED_CLUSTERS, min_nm_for_cluster  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean" / "CLUSTERS.json"
FBT_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
BATCH2B_PATH = ROOT / "handoff" / "CORRIDOR-RESTORE-QLR-BATCH2B-ISOLATED-CITY.json"
INTRA_PATH = ROOT / "handoff" / "corridor-restore" / "RESTORE-REGISTER-intra-metro-onwater-2026-07-06.json"
REPORT_PATH = ROOT / "grok-routing-output" / "corridor-restore-pipeline-report.json"
HANDOFF_REPORT = ROOT / "handoff" / "CORRIDOR-RESTORE-PIPELINE-2026-07-06.json"
JUL3_REF = "41cdc35"
LAND_MAX_KM = 0.25

DISPLAY_NAME_ENDPOINTS = frozenset(
    {
        "Penghu",
        "Jakarta",
        "Singapore",
        "Donggang",
        "Kaohsiung, Taiwan",
        "Liuqiu (Xiaoliuqiu), Taiwan",
    }
)

TAIWAN_RESTORE = [
    {"jul3_source_route_id": "e__kaohsiung-taiwan__4205637c19ed", "tier": "coastal", "cluster_id": "taiwan"},
    {"jul3_source_route_id": "e__kaohsiung-taiwan__7b7e1b0cbd32", "tier": "coastal", "cluster_id": "taiwan"},
    {"jul3_source_route_id": "e__penghu-taiwan__5a588c1b1f9d", "tier": "coastal", "cluster_id": "taiwan",
     "label_override": "Magong → Wang An (Penghu inter-island)"},
    {"jul3_source_route_id": "e__kaohsiung-taiwan__kaohsiung-port__penghu-taiwan__magong-harbor",
     "tier": "quanta_lr", "cluster_id": "taiwan"},
]

TAIWAN_MINT = {
    "from_bp": "bp-9ef4971a1b",
    "to_bp": "bp-42b7325105",
    "from_city_id": "penghu-taiwan",
    "to_city_id": "penghu-taiwan",
    "cluster_id": "taiwan",
    "tier": "coastal",
    "label": "Budai (Chiayi) → Magong (Penghu)",
    # Taiwan Strait — hand waypoints keep to open water (land mask over-aggressive near coast)
    "waypoints": [(120.0, 23.18), (119.82, 23.28), (119.64, 23.40), (119.54, 23.50)],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def load_jul3_routes() -> list[dict]:
    raw = subprocess.check_output(["git", "show", f"{JUL3_REF}:data-clean/ROUTES.json"], cwd=ROOT)
    obj = json.loads(raw)
    return obj if isinstance(obj, list) else obj.get("features", [])


def load_city_to_cluster() -> dict[str, str]:
    out: dict[str, str] = {}
    for c in load_json(CLUSTERS_PATH).get("clusters") or []:
        for city in c.get("member_city_ids") or []:
            out[city] = c["cluster_id"]
    return out


def endpoints(p: dict) -> tuple[str, str] | None:
    fn = p.get("from_node") or p.get("from")
    tn = p.get("to_node") or p.get("to")
    if fn and tn:
        return (fn, tn)
    return None


def ep_key(ep: tuple[str, str]) -> tuple[str, str]:
    return (ep[0], ep[1]) if ep[0] <= ep[1] else (ep[1], ep[0])


def endpoint_index(routes: list) -> set[tuple[str, str]]:
    eps: set[tuple[str, str]] = set()
    for feat in routes:
        ep = endpoints(props(feat))
        if ep:
            eps.add(ep_key(ep))
    return eps


def id_index(routes: list) -> set[str]:
    return {props(r).get("id") for r in routes if props(r).get("id")}


def needs_fresh_rn(old_id: str) -> bool:
    if not old_id:
        return True
    return (
        old_id.startswith("edge-")
        or old_id.startswith("edge__")
        or old_id.startswith("e__")
        or old_id.startswith("gcn-")
        or old_id.startswith("ics-")
        or not old_id.startswith("rn-")
    )


def is_junk_endpoint(bp: str, p: dict) -> bool:
    if not bp or bp == "None":
        return True
    if bp in DISPLAY_NAME_ENDPOINTS:
        return True
    if ", " in bp and not bp.startswith("bp-"):
        return True
    cid = p.get("from_city_id") or p.get("to_city_id")
    if bp == cid and not bp.startswith("bp-") and "__" not in bp:
        return True
    if re.match(r"^[A-Z][a-z].*\s", bp) and not bp.startswith("bp-"):
        return True
    return False


def apply_tier(p: dict, tier: str) -> None:
    if tier == "quanta_lr":
        p["platform"] = "Quanta-LR"
        if p.get("from_city_id") and p.get("to_city_id") and p["from_city_id"] != p["to_city_id"]:
            p["edge_class"] = "trunk"
        p["render_tier"] = "trunk"
        p["_assign_tier"] = "quanta_lr"
    else:
        dist = float(p.get("distance_nm") or 0)
        if dist > 70:
            p["platform"] = "Quanta-LR"
            p["edge_class"] = "trunk"
        else:
            p["platform"] = "Pioneer II"
            p["edge_class"] = "coastal" if dist >= 3 else "local"
        p["render_tier"] = p.get("edge_class")


def canonical_cluster(fc: str | None, tc: str | None, city_to_cluster: dict[str, str]) -> str | None:
    clusters = {city_to_cluster.get(c) for c in (fc, tc) if c and city_to_cluster.get(c)}
    clusters.discard(None)
    if len(clusters) == 1:
        return next(iter(clusters))
    if fc and city_to_cluster.get(fc):
        return city_to_cluster[fc]
    if tc and city_to_cluster.get(tc):
        return city_to_cluster[tc]
    return None


def restore_from_source(
    source: dict,
    *,
    entry: dict,
    city_to_cluster: dict[str, str],
    existing_ids: set[str],
    existing_eps: set[tuple[str, str]],
    report: dict,
    phase: str,
) -> dict | None:
    src_p = props(source)
    src_id = src_p.get("id") or entry.get("jul3_source_route_id")

    ep = endpoints(src_p)
    if not ep or ep[0] == ep[1]:
        report["skipped"].append({"phase": phase, "src_id": src_id, "reason": "same_endpoint"})
        return None
    if is_junk_endpoint(ep[0], src_p) or is_junk_endpoint(ep[1], src_p):
        report["skipped"].append({"phase": phase, "src_id": src_id, "reason": "junk_endpoint", "ep": ep})
        return None

    ek = ep_key(ep)
    if ek in existing_eps:
        report["skipped"].append({"phase": phase, "src_id": src_id, "reason": "endpoint_pair_exists", "ep": ep})
        return None

    coords = source.get("geometry", {}).get("coordinates") or []
    land_km = interior_land_km(coords, load_land_mask()) if coords else 0.0
    # Jul-3 copy-proven: Tasklet verified water-following; record land_km, do not re-cull.
    if entry.get("enforce_land_gate") and land_km > LAND_MAX_KM:
        report["skipped"].append({"phase": phase, "src_id": src_id, "reason": "land_crossing", "land_km": land_km})
        return None
    if land_km > LAND_MAX_KM:
        report.setdefault("land_advisory", []).append(
            {"phase": phase, "src_id": src_id, "land_km": round(land_km, 3)}
        )

    feat = copy.deepcopy(source)
    p = props(feat)

    if not p.get("from_node") and p.get("from"):
        p["from_node"] = p["from"]
    if not p.get("to_node") and p.get("to"):
        p["to_node"] = p["to"]

    tier = entry.get("tier") or entry.get("assign_tier") or "coastal"
    apply_tier(p, tier)

    stamp = entry.get("cluster_id") or canonical_cluster(p.get("from_city_id"), p.get("to_city_id"), city_to_cluster)
    if stamp:
        p["cluster_id"] = stamp

    if entry.get("label_override"):
        p["label"] = entry["label_override"]

    old_id = p.get("id") or src_id
    fn, tn = p.get("from_node") or p.get("from"), p.get("to_node") or p.get("to")
    if needs_fresh_rn(old_id) and fn and tn:
        tag = f"{phase}{len(report['restored'])}"
        new_id = mint_route_id(fn, tn, tag=tag)
        while new_id in existing_ids:
            new_id = mint_route_id(fn, tn, tag=f"{tag}x")
        p["id"] = new_id
        p["_resealed_from"] = old_id
    elif old_id in existing_ids:
        new_id = mint_route_id(fn or "x", tn or "y", tag=phase)
        p["id"] = new_id
        p["_resealed_from"] = old_id
    else:
        p["id"] = old_id

    p["_corridor_restore_pipeline"] = phase
    p["_corridor_restore_from_jul3"] = JUL3_REF
    p["_corridor_restore_jul3_source"] = src_id
    p["_corridor_restore_at"] = utc_now()
    p["_land_km_interior"] = round(land_km, 4)

    report["restored"].append(
        {
            "phase": phase,
            "route_id": p["id"],
            "jul3_source": src_id,
            "endpoints": list(ep),
            "nm": p.get("distance_nm"),
            "land_km": round(land_km, 3),
            "city_id": entry.get("city_id"),
        }
    )
    return feat


def mint_taiwan_budai_magong(
    bp_idx: dict,
    cities: dict[str, str],
    existing_ids: set[str],
    existing_eps: set[tuple[str, str]],
    report: dict,
) -> dict | None:
    spec = TAIWAN_MINT
    ep = (spec["from_bp"], spec["to_bp"])
    if ep_key(ep) in existing_eps:
        report["skipped"].append({"phase": "taiwan", "reason": "endpoint_pair_exists", "ep": ep})
        return None

    fb, tb = bp_idx.get(spec["from_bp"]), bp_idx.get(spec["to_bp"])
    if not fb or not tb:
        report["skipped"].append({"phase": "taiwan", "reason": "bp_missing", "spec": spec})
        return None

    mask = load_land_mask()
    coords = build_coastal_path(
        fb["coords"], tb["coords"], mask, manual_waypoints=spec.get("waypoints")
    )
    land_km = interior_land_km(coords, mask)
    if land_km > LAND_MAX_KM:
        report.setdefault("land_advisory", []).append(
            {"phase": "taiwan", "mint": "budai_magong", "land_km": round(land_km, 3)}
        )

    feat = make_route_feature(  # fresh mint — land gate enforced above
        spec["from_bp"],
        spec["to_bp"],
        fb["name"],
        tb["name"],
        spec["from_city_id"],
        spec["to_city_id"],
        coords,
        cities,
        source="taiwan_restore",
        land_km=land_km,
    )
    p = props(feat)
    p["cluster_id"] = spec["cluster_id"]
    p["label"] = spec["label"]
    apply_tier(p, spec["tier"])
    p["_corridor_restore_pipeline"] = "taiwan"
    p["_corridor_restore_at"] = utc_now()
    p["_taiwan_budai_mint"] = True

    rid = p["id"]
    while rid in existing_ids:
        rid = mint_route_id(spec["from_bp"], spec["to_bp"], tag=f"taiwan{len(existing_ids)}")
    p["id"] = rid

    report["restored"].append(
        {
            "phase": "taiwan",
            "route_id": p["id"],
            "jul3_source": None,
            "endpoints": list(ep),
            "nm": p.get("distance_nm"),
            "land_km": round(land_km, 3),
            "minted": "budai_magong",
        }
    )
    return feat


def dedupe_register(corridors: list[dict]) -> list[dict]:
    """One register row per metro endpoint-pair; prefer non-ics, more vertices."""
    best: dict[tuple[str, str, str], dict] = {}
    for entry in corridors:
        fb, tb = entry.get("from_bp"), entry.get("to_bp")
        if not fb or not tb or fb == tb:
            continue
        key = (entry.get("city_id") or "", fb, tb) if fb <= tb else (entry.get("city_id") or "", tb, fb)
        cur = best.get(key)
        if not cur:
            best[key] = entry
            continue
        score = lambda e: (  # noqa: E731
            (0 if str(e.get("src_id", "")).startswith("ics-") else 2)
            + (1 if str(e.get("src_id", "")).startswith("e__") else 0)
            + min(int(e.get("n_vertices") or 0), 500) / 500.0
        )
        if score(entry) > score(cur):
            best[key] = entry
    return list(best.values())


def metro_route_counts(routes: list, city_to_cluster: dict[str, str]) -> Counter:
    counts: Counter = Counter()
    for feat in routes:
        p = props(feat)
        for cid in {p.get("from_city_id"), p.get("to_city_id")}:
            if cid:
                counts[cid] += 1
    return counts


def run_phase(
    phase: str,
    routes: list[dict],
    jul3_by_id: dict[str, dict],
    city_to_cluster: dict[str, str],
    report: dict,
    *,
    corridors: list[dict] | None = None,
    bp_idx: dict | None = None,
    cities: dict | None = None,
) -> list[dict]:
    existing_ids = id_index(routes)
    existing_eps = endpoint_index(routes)
    new_routes: list[dict] = []

    if phase == "taiwan":
        for entry in TAIWAN_RESTORE:
            src = jul3_by_id.get(entry["jul3_source_route_id"])
            if not src:
                report["skipped"].append({**entry, "phase": "taiwan", "reason": "jul3_source_missing"})
                continue
            feat = restore_from_source(
                src,
                entry=entry,
                city_to_cluster=city_to_cluster,
                existing_ids=existing_ids | {props(r).get("id") for r in new_routes},
                existing_eps=existing_eps,
                report=report,
                phase="taiwan",
            )
            if not feat:
                continue
            new_routes.append(feat)
            ep = endpoints(props(feat))
            if ep:
                existing_eps.add(ep_key(ep))
            rid = props(feat).get("id")
            if rid:
                existing_ids.add(rid)

        if bp_idx and cities:
            feat = mint_taiwan_budai_magong(bp_idx, cities, existing_ids, existing_eps, report)
            if feat:
                new_routes.append(feat)

    elif phase == "batch2b":
        for entry in corridors or []:
            src_id = entry.get("jul3_source_route_id")
            src = jul3_by_id.get(src_id)
            if not src:
                report["skipped"].append({**entry, "phase": "batch2b", "reason": "jul3_source_missing"})
                continue
            enriched = {**entry, "tier": entry.get("tier") or "coastal_short", "cluster_id": entry.get("cluster")}
            feat = restore_from_source(
                src,
                entry=enriched,
                city_to_cluster=city_to_cluster,
                existing_ids=existing_ids | {props(r).get("id") for r in new_routes},
                existing_eps=existing_eps,
                report=report,
                phase="batch2b",
            )
            if not feat:
                continue
            new_routes.append(feat)
            ep = endpoints(props(feat))
            if ep:
                existing_eps.add(ep_key(ep))
            rid = props(feat).get("id")
            if rid:
                existing_ids.add(rid)

    elif phase == "intra_metro":
        deduped = dedupe_register(corridors or [])
        report["intra_register_deduped"] = len(corridors or []) - len(deduped)
        for entry in deduped:
            src_id = entry.get("src_id")
            src = jul3_by_id.get(src_id)
            if not src:
                report["skipped"].append({"phase": "intra_metro", "src_id": src_id, "reason": "jul3_source_missing"})
                continue

            src_p = props(src)
            metro = entry.get("city_id") or ""
            if metro in UAE_PRE_SEALED_CLUSTERS:
                entry = {**entry, "_uae_conservative": True}

            feat = restore_from_source(
                src,
                entry={"tier": "coastal", "city_id": metro, "cluster_id": city_to_cluster.get(metro)},
                city_to_cluster=city_to_cluster,
                existing_ids=existing_ids | {props(r).get("id") for r in new_routes},
                existing_eps=existing_eps,
                report=report,
                phase="intra_metro",
            )
            if not feat:
                continue
            new_routes.append(feat)
            ep = endpoints(props(feat))
            if ep:
                existing_eps.add(ep_key(ep))
            rid = props(feat).get("id")
            if rid:
                existing_ids.add(rid)

    return new_routes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument(
        "--phase",
        choices=["all", "taiwan", "batch2b", "intra_metro"],
        default="all",
    )
    args = ap.parse_args()

    jul3 = load_jul3_routes()
    jul3_by_id = {props(r).get("id"): r for r in jul3 if props(r).get("id")}

    routes = route_features(load_json(ROUTES_PATH))
    city_to_cluster = load_city_to_cluster()
    fbt = load_json(FBT_PATH)
    bp_idx = build_bp_index(fbt)
    cities = {}
    for key in ("city", "priority_city"):
        for feat in fbt.get(key, []):
            pr = props(feat)
            if pr.get("id"):
                cities[pr["id"]] = pr.get("name") or pr["id"]

    before_count = len(routes)
    before_metro = metro_route_counts(routes, city_to_cluster)

    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "jul3_ref": JUL3_REF,
        "routes_before": before_count,
        "phases": [],
        "restored": [],
        "skipped": [],
    }

    phases = ["taiwan", "batch2b", "intra_metro"] if args.phase == "all" else [args.phase]
    batch2b = load_json(BATCH2B_PATH).get("corridors") or []
    intra_reg = load_json(INTRA_PATH).get("corridors") or []

    for phase in phases:
        phase_before = len(routes)
        corridors = batch2b if phase == "batch2b" else intra_reg if phase == "intra_metro" else None
        new_feats = run_phase(
            phase,
            routes,
            jul3_by_id,
            city_to_cluster,
            report,
            corridors=corridors,
            bp_idx=bp_idx if phase == "taiwan" else None,
            cities=cities if phase == "taiwan" else None,
        )
        routes.extend(new_feats)
        report["phases"].append(
            {
                "phase": phase,
                "added": len(new_feats),
                "routes_after": len(routes),
                "routes_before": phase_before,
            }
        )

    after_metro = metro_route_counts(routes, city_to_cluster)
    top_cities = [c for c, _ in load_json(INTRA_PATH).get("top_cities") or []][:25]
    deltas = []
    for city in top_cities:
        deltas.append(
            {
                "city_id": city,
                "before": before_metro.get(city, 0),
                "after": after_metro.get(city, 0),
                "delta": after_metro.get(city, 0) - before_metro.get(city, 0),
            }
        )
    deltas.sort(key=lambda x: -abs(x["delta"]))

    report["routes_after"] = len(routes)
    report["summary"] = {
        "restored": len(report["restored"]),
        "skipped": len(report["skipped"]),
        "net_added": len(routes) - before_count,
    }
    report["top25_metro_deltas"] = deltas

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    HANDOFF_REPORT.write_text(json.dumps(report, indent=2) + "\n")

    print(
        f"  corridor-restore pipeline: +{report['summary']['net_added']} "
        f"(restored {report['summary']['restored']}, skipped {report['summary']['skipped']}) "
        f"· routes {before_count} → {len(routes)}"
    )
    for ph in report["phases"]:
        print(f"    {ph['phase']}: +{ph['added']}")

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        print(f"  wrote {ROUTES_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())