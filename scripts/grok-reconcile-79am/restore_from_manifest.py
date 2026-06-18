#!/usr/bin/env python3
"""Restore 440 routes + 213 BPs from #79ak (gold-trusted manifest)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2) + "\n")


def save_routes(p: Path, features: list):
    p.write_text(json.dumps(features, separators=(",", ":")) + "\n")


def route_features(obj) -> list:
    return obj if isinstance(obj, list) else obj.get("features", [])


def route_id_of(f: dict) -> str:
    p = f.get("properties", f)
    return p.get("id") or p.get("route_id") or ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--restore-src", required=True)
    args = ap.parse_args()

    work = Path(args.work)
    dc = work / "atlas-repo" / "data-clean"
    src = Path(args.restore_src)
    manifest = load_json(work / "RECONCILE" / "RESTORE-MANIFEST.json")

    routes = route_features(load_json(dc / "ROUTES.json"))
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    pois = fbt.setdefault("poi", [])

    src_routes = {route_id_of(f): f for f in route_features(load_json(src / "ROUTES.json"))}
    src_pois = {(p.get("properties") or p).get("id"): p for p in load_json(src / "FEATURES_BY_TYPE.json").get("poi", [])}

    route_by_id = {route_id_of(f): i for i, f in enumerate(routes)}
    poi_by_id = {(p.get("properties") or p).get("id"): i for i, p in enumerate(pois)}

    visible_restore = {"bp-31b06c534d", "bp-f47f75836a"}
    report = {
        "routes_restored": [],
        "routes_missing_src": [],
        "bps_restored": [],
        "bps_updated_visible": [],
        "bps_missing_src": [],
    }

    for entry in manifest["restore_route_ids"]:
        rid = entry["id"] if isinstance(entry, dict) else entry
        feat = src_routes.get(rid)
        if not feat:
            report["routes_missing_src"].append(rid)
            continue
        if rid in route_by_id:
            routes[route_by_id[rid]] = feat
        else:
            routes.append(feat)
            route_by_id[rid] = len(routes) - 1
        report["routes_restored"].append(rid)

    for entry in manifest["restore_bp_ids"]:
        bid = entry["id"]
        feat = src_pois.get(bid)
        if not feat:
            report["bps_missing_src"].append(bid)
            continue
        props = feat.setdefault("properties", feat)
        if bid in visible_restore:
            props.pop("relevance", None)
            props["status"] = "operational"
            props["_restored_visible"] = True
        if bid in poi_by_id:
            pois[poi_by_id[bid]] = feat
            if bid in visible_restore:
                report["bps_updated_visible"].append(bid)
        else:
            pois.append(feat)
            poi_by_id[bid] = len(pois) - 1
            report["bps_restored"].append(bid)

    save_routes(dc / "ROUTES.json", routes)
    save_json(dc / "FEATURES_BY_TYPE.json", fbt)
    save_json(work / "grok-routing-output" / "restore-report.json", report)
    print(json.dumps({k: len(v) for k, v in report.items()}, indent=2))


if __name__ == "__main__":
    main()