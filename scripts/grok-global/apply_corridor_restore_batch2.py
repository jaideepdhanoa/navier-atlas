#!/usr/bin/env python3
"""Restore Q-LR Batch 2 corridors (180–700 nm) from July-3 proven geometry.

Follows a9b5d47e. Copies features from main @ 41cdc35 by jul3_source_route_id.
edge-/gcn-/e__ ids → fresh rn- mint. Assigns Quanta-LR + trunk for cross-border render.
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

from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km,
    load_json,
    load_land_mask,
    mint_route_id,
    route_features,
    save_routes,
)

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
CLUSTERS_PATH = ROOT / "data-clean" / "CLUSTERS.json"
REGISTER_PATH = ROOT / "handoff" / "CORRIDOR-RESTORE-QLR-BATCH2-700nm.json"
REPORT_PATH = ROOT / "grok-routing-output" / "corridor-restore-batch2-report.json"
HANDOFF_REPORT = ROOT / "handoff" / "CORRIDOR-RESTORE-BATCH2-2026-07-06.json"
JUL3_REF = "41cdc35"

# Label QA — register label was wrong; endpoints are Koh Chang ↔ Koh Phangan
LABEL_FIXES: dict[tuple[str, str], dict[str, str]] = {
    ("koh-chang-thailand", "koh-phangan-thailand"): {
        "from_label": "Koh Chang (Ao Sapparot Pier)",
        "to_label": "Koh Phangan (Thong Sala Pier)",
        "label": "Koh Chang → Koh Phangan",
    },
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


def endpoint_index(routes: list) -> set[tuple[str, str]]:
    eps: set[tuple[str, str]] = set()
    for feat in routes:
        ep = endpoints(props(feat))
        if ep:
            eps.add(ep)
            eps.add((ep[1], ep[0]))
    return eps


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


def needs_fresh_rn(old_id: str) -> bool:
    return (
        old_id.startswith("edge-")
        or old_id.startswith("edge__")
        or old_id.startswith("e__")
        or old_id.startswith("gcn-")
        or not old_id.startswith("rn-")
    )


def apply_qlr_tier(p: dict, entry: dict) -> None:
    p["platform"] = "Quanta-LR"
    fc, tc = p.get("from_city_id"), p.get("to_city_id")
    if fc and tc and fc != tc:
        p["edge_class"] = "trunk"
    p["render_tier"] = "trunk"
    p["_assign_tier"] = entry.get("assign_tier", "quanta_lr")
    if entry.get("cross_border"):
        p["_cross_border_qlr"] = True


def restore_feature(
    entry: dict,
    source: dict,
    *,
    city_to_cluster: dict[str, str],
    existing_ids: set[str],
    existing_eps: set[tuple[str, str]],
    report: dict,
) -> dict | None:
    src_p = props(source)
    src_id = src_p.get("id") or entry.get("jul3_source_route_id")

    if src_id in existing_ids:
        report["skipped"].append({**entry, "reason": "source_id_exists"})
        return None

    ep = endpoints(src_p)
    if ep and ep in existing_eps:
        report["skipped"].append({**entry, "reason": "endpoint_pair_exists", "endpoints": ep})
        return None

    feat = copy.deepcopy(source)
    p = props(feat)

    # Normalize node fields for downstream consumers
    if not p.get("from_node") and p.get("from"):
        p["from_node"] = p["from"]
    if not p.get("to_node") and p.get("to"):
        p["to_node"] = p["to"]

    fc, tc = p.get("from_city_id"), p.get("to_city_id")
    fix_key = tuple(sorted([fc, tc])) if fc and tc else None
    for (a, b), fixes in LABEL_FIXES.items():
        if fc and tc and {fc, tc} == {a, b}:
            p.update(fixes)
            report["label_fixes"].append({"pair": [fc, tc], "fixes": fixes})

    stamp = canonical_cluster(fc, tc, city_to_cluster)
    if stamp:
        p["cluster_id"] = stamp

    apply_qlr_tier(p, entry)

    old_id = p.get("id") or src_id
    fn, tn = p.get("from_node") or p.get("from"), p.get("to_node") or p.get("to")
    if needs_fresh_rn(old_id) and fn and tn:
        new_id = mint_route_id(fn, tn, tag="qlr2")
        while new_id in existing_ids:
            new_id = mint_route_id(fn, tn, tag=f"qlr2{len(existing_ids)}")
        p["id"] = new_id
        p["_resealed_from"] = old_id
    elif old_id in existing_ids:
        new_id = mint_route_id(fn or "x", tn or "y", tag="qlr2")
        p["id"] = new_id
        p["_resealed_from"] = old_id
    else:
        p["id"] = old_id

    coords = feat.get("geometry", {}).get("coordinates") or []
    land_km = interior_land_km(coords, load_land_mask()) if coords else 0.0

    p["_corridor_restore_batch2"] = True
    p["_corridor_restore_from_jul3"] = JUL3_REF
    p["_corridor_restore_jul3_source"] = src_id
    p["_corridor_restore_at"] = utc_now()
    p["_land_km_interior"] = round(land_km, 4)

    report["restored"].append(
        {
            "route_id": p["id"],
            "jul3_source": src_id,
            "pair": entry.get("pair"),
            "nm": p.get("distance_nm"),
            "cross_border": entry.get("cross_border"),
            "vertices": len(coords),
            "land_km": round(land_km, 3),
        }
    )
    return feat


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--register", default=str(REGISTER_PATH))
    args = ap.parse_args()

    register = load_json(Path(args.register))
    corridors = register.get("corridors") or []

    jul3 = load_jul3_routes()
    by_id = {props(r).get("id"): r for r in jul3 if props(r).get("id")}

    routes = route_features(load_json(ROUTES_PATH))
    city_to_cluster = load_city_to_cluster()
    existing_ids = {props(r).get("id") for r in routes if props(r).get("id")}
    existing_eps = endpoint_index(routes)

    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "jul3_ref": JUL3_REF,
        "routes_before": len(routes),
        "restored": [],
        "skipped": [],
        "label_fixes": [],
    }

    new_routes: list[dict] = []
    for entry in corridors:
        src_id = entry.get("jul3_source_route_id")
        source = by_id.get(src_id)
        if not source:
            report["skipped"].append({**entry, "reason": "jul3_source_missing"})
            continue

        feat = restore_feature(
            entry,
            source,
            city_to_cluster=city_to_cluster,
            existing_ids=existing_ids | {props(r).get("id") for r in new_routes},
            existing_eps=existing_eps,
            report=report,
        )
        if not feat:
            continue

        p = props(feat)
        rid = p.get("id")
        ep = endpoints(p)
        new_routes.append(feat)
        if rid:
            existing_ids.add(rid)
        if ep:
            existing_eps.add(ep)
            existing_eps.add((ep[1], ep[0]))

    routes.extend(new_routes)
    report["routes_after"] = len(routes)
    report["summary"] = {"restored": len(report["restored"]), "skipped": len(report["skipped"])}

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    HANDOFF_REPORT.write_text(json.dumps(report, indent=2) + "\n")

    print(
        f"  batch2 Q-LR restore: +{len(report['restored'])} · skipped {len(report['skipped'])} "
        f"· routes {report['routes_before']} → {report['routes_after']}"
    )

    if args.apply:
        save_routes(ROUTES_PATH, routes)
        print(f"  wrote {ROUTES_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())