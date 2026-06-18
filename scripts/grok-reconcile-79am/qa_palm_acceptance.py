#!/usr/bin/env python3
"""Palm/Marina acceptance gate — block reseal on failure."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from reconcile_shared import (
    LAND_THRESHOLD_KM,
    PALM_MARINA_BBOX,
    build_bp_indexes,
    endpoint_survives,
    in_bbox,
    load_json,
    load_qa_module,
    overlay_path,
    route_features,
    route_id_of,
    route_touches_bbox,
    save_json,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    args = ap.parse_args()
    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"

    sem_path = work / "RECONCILE" / "SEM-VERDICTS.json"
    drop_ids = set()
    if sem_path.exists():
        buckets = load_json(work / "RECONCILE" / "SEM-BUCKET-IDS.json")
        drop_ids = set(buckets.get("DROP", []))

    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    bp_by_id, berth_index = build_bp_indexes(fbt)
    city_ids = {
        (c.get("properties") or c).get("id")
        for c in fbt.get("city", []) + fbt.get("priority_city", [])
        if (c.get("properties") or c).get("id")
    }

    failures: list[str] = []
    visible_drop = []
    visible_no_source = []

    for pid, row in bp_by_id.items():
        props = row["props"]
        lon, lat = row["coords"][:2]
        if lon is None or not in_bbox(lon, lat):
            continue
        if props.get("_quarantine") or props.get("relevance") == "hide":
            continue
        if pid in drop_ids:
            visible_drop.append(pid)
        if not props.get("_gazetteer_source"):
            visible_no_source.append({"id": pid, "name": props.get("name")})

    if visible_drop:
        failures.append(f"visible DROP BPs in bbox: {len(visible_drop)}")
    if visible_no_source:
        failures.append(f"surviving BPs without gazetteer source: {len(visible_no_source)}")

    routes = route_features(load_json(dc / "ROUTES.json"))
    orphans = []
    for feat in routes:
        props = feat.get("properties", feat)
        if props.get("_quarantine") or props.get("relevance") == "hide":
            continue
        if not route_touches_bbox(feat, bp_by_id):
            continue
        rid = route_id_of(feat)
        for ep in (props.get("from"), props.get("to")):
            if ep and ep.startswith("bp-"):
                ok, why = endpoint_survives(ep, bp_by_id, berth_index, city_ids)
                if not ok:
                    orphans.append({"route": rid, "endpoint": ep, "why": why})
            elif ep and "__" in ep:
                ok, why = endpoint_survives(ep, bp_by_id, berth_index, city_ids)
                if not ok:
                    orphans.append({"route": rid, "endpoint": ep, "why": why})

    if orphans:
        failures.append(f"orphan routes in bbox: {len(orphans)}")

    qa = load_qa_module(work)
    mask = None
    try:
        from global_land_mask import globe as mask  # noqa: WPS433
    except Exception:
        pass
    overlay_geom, overlay_tree = qa.load_overlay(str(overlay_path(work)))
    land_crossers = []
    for feat in routes:
        props = feat.get("properties", feat)
        if props.get("_quarantine") or props.get("relevance") == "hide":
            continue
        if not route_touches_bbox(feat, bp_by_id):
            continue
        coords = feat.get("geometry", {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        m = qa.evaluate_route(coords, mask, overlay_geom, overlay_tree)
        if m["interior_land_km"] > LAND_THRESHOLD_KM:
            land_crossers.append({"id": route_id_of(feat), "interior_land_km": m["interior_land_km"]})

    if land_crossers:
        failures.append(f"land-crossing routes in bbox: {len(land_crossers)}")

    allowlist_path = dc / "route_water_allowlist.json"
    allow_ids = set()
    if allowlist_path.exists():
        allow_ids = set(load_json(allowlist_path).get("ids", []))

    report = {
        "bbox": PALM_MARINA_BBOX,
        "pass": len(failures) == 0,
        "failures": failures,
        "counts": {
            "visible_bps": sum(
                1
                for row in bp_by_id.values()
                if row["coords"][0] is not None
                and in_bbox(row["coords"][0], row["coords"][1])
                and not row["props"].get("_quarantine")
                and row["props"].get("relevance") != "hide"
            ),
            "visible_drop_violations": len(visible_drop),
            "no_gazetteer_violations": len(visible_no_source),
            "orphan_routes": len(orphans),
            "land_crossers": len(land_crossers),
            "allowlist_ids": len(allow_ids),
        },
        "land_crossing_proof": {
            "threshold_km": LAND_THRESHOLD_KM,
            "flagged_in_bbox": len(land_crossers),
            "sample": land_crossers[:20],
        },
        "orphan_sample": orphans[:20],
        "no_gazetteer_sample": visible_no_source[:20],
    }

    out = work / "grok-routing-output" / "qa-palm-marina-acceptance.json"
    save_json(out, report)

    if failures:
        print("PALM QA FAIL:")
        for f in failures:
            print(f"  - {f}")
        print(f"report: {out}")
        sys.exit(1)

    print(
        f"PALM QA PASS: bps={report['counts']['visible_bps']} "
        f"land_crossers=0 orphans=0"
    )
    print(f"report: {out}")


if __name__ == "__main__":
    main()