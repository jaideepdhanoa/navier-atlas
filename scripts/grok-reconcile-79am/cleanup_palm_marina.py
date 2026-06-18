#!/usr/bin/env python3
"""Palm Jumeirah / Dubai Marina bbox cleanup — deterministic Grok-owned lane."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from reconcile_shared import (
    JUNK_NAME,
    LAND_THRESHOLD_KM,
    PALM_MARINA_BBOX,
    WATER_THRESHOLD_KM,
    build_bp_indexes,
    build_crosswalk_index,
    endpoint_survives,
    gazetteer_promote,
    in_bbox,
    load_json,
    load_land_mask,
    load_qa_module,
    overlay_path,
    resolve_endpoint,
    route_features,
    route_id_of,
    route_touches_bbox,
    save_json,
    save_routes,
    water_distance_km,
)


def quarantine_bp(props: dict, reason: str, bucket: str = "PALM_CLEANUP"):
    props["relevance"] = "hide"
    props["_quarantine"] = True
    props["_quarantine_bucket"] = bucket
    props["_quarantine_reason"] = reason


def load_sem(work: Path) -> tuple[dict, set, set, set]:
    sem_path = work / "RECONCILE" / "SEM-VERDICTS.json"
    buckets_path = work / "RECONCILE" / "SEM-BUCKET-IDS.json"
    if not sem_path.exists():
        return {}, set(), set(), set()
    sem = {r["id"]: r for r in load_json(sem_path)}
    buckets = load_json(buckets_path)
    return (
        sem,
        set(buckets.get("DROP", [])),
        set(buckets.get("KEEP", [])),
        set(buckets.get("HOLD", [])),
    )


def load_protected_bps(work: Path) -> set[str]:
    protected: set[str] = set()
    manifest = work / "RECONCILE" / "RESTORE-MANIFEST.json"
    if manifest.exists():
        for entry in load_json(manifest).get("restore_bp_ids", []):
            protected.add(entry["id"])
    protected.update({"bp-31b06c534d", "bp-f47f75836a"})
    for ledger_name in ("APPLY-LEDGER-79am.json", "RECONCILE/APPLY-LEDGER-src.json"):
        lp = work / ledger_name
        if not lp.exists():
            continue
        ledger = load_json(lp)
        for slug, row in ledger.get("endpoint_crosswalk_verified", {}).items():
            if row.get("bp_id"):
                protected.add(row["bp_id"])
    return protected


def load_keep_routes(work: Path) -> set[str]:
    keep: set[str] = set()
    manifest = work / "RECONCILE" / "RESTORE-MANIFEST.json"
    if manifest.exists():
        for entry in load_json(manifest).get("restore_route_ids", []):
            rid = entry["id"] if isinstance(entry, dict) else entry
            keep.add(rid)
    solutions = work / "grok-routing-output" / "route-solutions.jsonl"
    if solutions.exists():
        for line in solutions.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("route_id"):
                keep.add(row["route_id"])
    return keep


def slug_bp_pairs(work: Path) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for ledger_name in ("APPLY-LEDGER-79am.json", "RECONCILE/APPLY-LEDGER-src.json"):
        lp = work / ledger_name
        if not lp.exists():
            continue
        ledger = load_json(lp)
        slug_map = {
            slug: row["bp_id"]
            for slug, row in ledger.get("endpoint_crosswalk_verified", {}).items()
            if row.get("bp_id")
        }
        for section in (
            "apply_synthesize_clean",
            "apply_synthesize_after_khalifa_mint",
            "apply_synthesize_phantom_restored",
        ):
            for pair in ledger.get(section, []):
                fr = slug_map.get(pair["from"], pair["from"])
                to = slug_map.get(pair["to"], pair["to"])
                pairs.add((fr, to))
                pairs.add((to, fr))
    return pairs


def cleanup_bbox_bps(work: Path, report: dict) -> set[str]:
    dc = work / "atlas-repo" / "data-clean"
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    sem, drop_ids, keep_ids, hold_ids = load_sem(work)
    protected = load_protected_bps(work)

    crosswalk_path = work / "atlas-external" / "pier-slug-bp-crosswalk.json"
    if not crosswalk_path.exists():
        crosswalk_path = Path(__file__).resolve().parents[2] / "atlas-external/pier-slug-bp-crosswalk.json"
    crosswalk_keys = build_crosswalk_index(load_json(crosswalk_path))
    mask = load_land_mask()

    promoted: set[str] = set()
    dropped: list[dict] = []

    for poi in fbt.get("poi", []):
        props = poi.get("properties", poi)
        pid = props.get("id")
        coords = poi.get("geometry", {}).get("coordinates", [None, None])
        lon, lat = coords[0], coords[1]
        if lon is None or not in_bbox(lon, lat):
            continue

        name = props.get("name") or ""
        verdict = (sem.get(pid) or {}).get("verdict")
        if pid in protected and pid not in drop_ids:
            props.pop("_quarantine", None)
            props.pop("relevance", None)
            props["_gazetteer_source"] = props.get("_gazetteer_source") or "protected_restore"
            props["_gate4_promoted"] = True
            promoted.add(pid)
            continue

        if pid in drop_ids or verdict == "DROP":
            quarantine_bp(props, (sem.get(pid) or {}).get("reason", "semantic_DROP"), "DROP")
            dropped.append({"id": pid, "reason": "DROP"})
            continue

        dist = water_distance_km(lon, lat, mask)
        if dist > WATER_THRESHOLD_KM:
            quarantine_bp(props, f"water_adjacency_{dist}km", "GATE3")
            dropped.append({"id": pid, "name": name, "reason": f"inland_{dist}km"})
            continue

        if JUNK_NAME.search(name):
            quarantine_bp(props, "junk_poi_name", "JUNK")
            dropped.append({"id": pid, "name": name, "reason": "junk_name"})
            continue

        ok, source = gazetteer_promote(pid, name, crosswalk_keys, verdict)
        if not ok:
            bucket = verdict or "LEGACY"
            quarantine_bp(props, f"no_terminal_gazetteer ({bucket})", f"{bucket}_UNCONFIRMED")
            dropped.append({"id": pid, "name": name, "reason": "no_gazetteer"})
            continue

        props.pop("_quarantine", None)
        props.pop("relevance", None)
        props["status"] = "operational"
        props["_gate4_promoted"] = True
        props["_gazetteer_source"] = source
        promoted.add(pid)

    save_json(dc / "FEATURES_BY_TYPE.json", fbt)
    report["bps_dropped"] = len(dropped)
    report["bps_promoted"] = len(promoted)
    report["bp_drop_sample"] = dropped[:40]
    print(f"palm bbox BPs: promoted={len(promoted)} dropped={len(dropped)}")
    return promoted


def cascade_routes(work: Path, report: dict):
    dc = work / "atlas-repo" / "data-clean"
    routes = route_features(load_json(dc / "ROUTES.json"))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    bp_by_id, berth_index = build_bp_indexes(fbt)
    city_ids = {
        (c.get("properties") or c).get("id")
        for c in fbt.get("city", []) + fbt.get("priority_city", [])
        if (c.get("properties") or c).get("id")
    }

    quarantined = []
    for feat in routes:
        if not route_touches_bbox(feat, bp_by_id):
            continue
        props = feat.get("properties", feat)
        rid = route_id_of(feat)
        reasons = []
        for ep in (props.get("from"), props.get("to")):
            ok, why = endpoint_survives(ep, bp_by_id, berth_index, city_ids)
            if not ok:
                reasons.append(f"{ep}:{why}")
        if reasons:
            quarantine_bp(props, f"endpoint_cascade {reasons}", "ROUTE_CASCADE")
            quarantined.append({"id": rid, "reasons": reasons})
        elif props.get("_quarantine_reason", "").startswith("endpoint_cascade"):
            props.pop("_quarantine", None)
            props.pop("relevance", None)
            props.pop("_quarantine_reason", None)

    save_routes(dc / "ROUTES.json", routes)
    report["routes_cascade_quarantined"] = len(quarantined)
    report["route_cascade_sample"] = quarantined[:30]
    print(f"palm cascade: quarantined={len(quarantined)}")


def dedupe_spaghetti(work: Path, report: dict):
    dc = work / "atlas-repo" / "data-clean"
    routes = route_features(load_json(dc / "ROUTES.json"))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    bp_by_id, _ = build_bp_indexes(fbt)
    keep_routes = load_keep_routes(work)
    slug_pairs = slug_bp_pairs(work)

    culled = []
    seen_pairs: dict[tuple[str, str], str] = {}

    for feat in routes:
        props = feat.get("properties", feat)
        if props.get("_quarantine") or props.get("relevance") == "hide":
            continue
        if not route_touches_bbox(feat, bp_by_id):
            continue
        rid = route_id_of(feat)
        if rid in keep_routes:
            continue
        fr, to = props.get("from"), props.get("to")
        if not (fr and to and fr.startswith("bp-") and to.startswith("bp-")):
            continue
        pair = tuple(sorted((fr, to)))
        if pair in slug_pairs or (fr, to) in slug_pairs:
            seen_pairs.setdefault(pair, rid)
            continue
        if pair in seen_pairs:
            quarantine_bp(props, f"dedupe_spaghetti duplicate_of={seen_pairs[pair]}", "SPAGHETTI")
            culled.append({"id": rid, "reason": "duplicate_od"})
            continue
        quarantine_bp(props, "marina_mesh_not_operator_service", "SPAGHETTI")
        culled.append({"id": rid, "from": fr, "to": to})

    save_routes(dc / "ROUTES.json", routes)
    report["routes_spaghetti_culled"] = len(culled)
    report["spaghetti_sample"] = culled[:30]
    print(f"palm spaghetti: culled={len(culled)}")


def repair_geometry(work: Path, report: dict):
    dc = work / "atlas-repo" / "data-clean"
    routes = route_features(load_json(dc / "ROUTES.json"))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    bp_by_id, berth_index = build_bp_indexes(fbt)
    city_ids = {
        (c.get("properties") or c).get("id")
        for c in fbt.get("city", []) + fbt.get("priority_city", [])
        if (c.get("properties") or c).get("id")
    }

    qa = load_qa_module(work)
    mask = None
    try:
        from global_land_mask import globe as mask  # noqa: WPS433
    except Exception:
        pass
    overlay_geom, overlay_tree = qa.load_overlay(str(overlay_path(work)))

    solutions_path = work / "grok-routing-output" / "route-solutions.jsonl"
    by_rid: dict[str, dict] = {}
    by_bp_pair: dict[tuple[str, str], dict] = {}
    if solutions_path.exists():
        for line in solutions_path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if not row.get("qa_pass") or not row.get("geometry"):
                continue
            if row.get("route_id"):
                by_rid[row["route_id"]] = row
            fr = row.get("from_id")
            to = row.get("to_id")
            if fr and to:
                by_bp_pair[(fr, to)] = row
                by_bp_pair[(to, fr)] = row

    ledger_slug_bp: dict[str, str] = {}
    for ledger_name in ("APPLY-LEDGER-79am.json", "RECONCILE/APPLY-LEDGER-src.json"):
        lp = work / ledger_name
        if not lp.exists():
            continue
        for slug, row in load_json(lp).get("endpoint_crosswalk_verified", {}).items():
            if row.get("bp_id"):
                ledger_slug_bp[slug] = row["bp_id"]

    rerouted = []
    culled = []

    for feat in routes:
        props = feat.get("properties", feat)
        if props.get("_quarantine") or props.get("relevance") == "hide":
            continue
        if not route_touches_bbox(feat, bp_by_id):
            continue
        coords = feat.get("geometry", {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        rid = route_id_of(feat)
        m = qa.evaluate_route(coords, mask, overlay_geom, overlay_tree)
        if m["interior_land_km"] <= LAND_THRESHOLD_KM:
            continue

        patch = by_rid.get(rid)
        fr_res, _ = resolve_endpoint(props.get("from"), bp_by_id, berth_index, city_ids)
        to_res, _ = resolve_endpoint(props.get("to"), bp_by_id, berth_index, city_ids)
        if not patch and fr_res and to_res:
            patch = by_bp_pair.get((fr_res, to_res))
        if not patch and fr_res and to_res:
            inv = {v: k for k, v in ledger_slug_bp.items()}
            fr_slug = inv.get(fr_res)
            to_slug = inv.get(to_res)
            if fr_slug and to_slug:
                patch = by_bp_pair.get((fr_slug, to_slug))

        if patch and patch.get("geometry"):
            feat["geometry"] = patch["geometry"]
            props["_wp_provenance"] = "palm-marina-geometry-repair"
            props["_repaired_at"] = datetime.now(timezone.utc).isoformat()
            m2 = qa.evaluate_route(patch["geometry"]["coordinates"], mask, overlay_geom, overlay_tree)
            if m2["interior_land_km"] <= LAND_THRESHOLD_KM:
                rerouted.append({"id": rid, "was_km": m["interior_land_km"], "now_km": m2["interior_land_km"]})
                continue

        quarantine_bp(props, f"land_crossing_{m['interior_land_km']}km_no_repair", "LAND_GEOM")
        culled.append({"id": rid, "interior_land_km": m["interior_land_km"]})

    save_routes(dc / "ROUTES.json", routes)
    report["routes_rerouted"] = len(rerouted)
    report["routes_geom_culled"] = len(culled)
    report["reroute_sample"] = rerouted[:20]
    report["geom_cull_sample"] = culled[:20]
    print(f"palm geometry: rerouted={len(rerouted)} culled={len(culled)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument(
        "--phase",
        choices=("bps", "cascade", "spaghetti", "geometry", "all"),
        default="all",
    )
    args = ap.parse_args()
    work = Path(args.work)
    report = {
        "bbox": PALM_MARINA_BBOX,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": args.phase,
    }

    if args.phase in ("bps", "all"):
        cleanup_bbox_bps(work, report)
    if args.phase in ("cascade", "all"):
        cascade_routes(work, report)
    if args.phase in ("spaghetti", "all"):
        dedupe_spaghetti(work, report)
    if args.phase in ("geometry", "all"):
        repair_geometry(work, report)

    out = work / "grok-routing-output" / "palm-marina-cleanup-report.json"
    save_json(out, report)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()