#!/usr/bin/env python3
"""FE-2 Grok handoff — rebind route-bound junk POIs, fix Hua Hin pier, drop junk pins."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Curated junk → nearest legitimate marine endpoint (same market context).
REBIND_MAP: dict[str, str] = {
    "bp-0a02b5083e": "bp-e54c85e611",  # Seahawk Yacht → Marina Promenade Water Bus
    "bp-2683f97998": "bp-a7a2a607a2",  # Brilions yacht ad → Kaleiçi Old Harbour
    "bp-3b0efa4fcc": "bp-644376be1d",  # Marina Garden Café → Cebu-Mactan Ferry
    "bp-4098845649": "bp-2c19bec2d4",  # Morning Bakery (Harbour Bay SG) → Harbour Bay pier
    "bp-4ae4740171": "bp-3dbf93456b",  # Gading Marina Wedding → Tanjung Priok Cruise
    "bp-4eea23de3f": "bp-73c2ac95b0",  # Yolo Yacht RAK → Dubai Ferry Station
    "bp-5144c5f7fe": "bp-60d0f1022c",  # Victoria Harbour Café → Harbor Star Shipping
    "bp-541a9469dc": "bp-0424f0138f",  # Yolo Yacht Sharjah → Dubai Int'l Marine Club
    "bp-9282a838ef": "bp-3ad5195431",  # Japanos Creek Harbour → Al Jaddaf Marine
    "bp-a293fa98dd": "bp-kabatas-iskelesi",  # Mega Lüfer dinner cruise → Kabataş iskelesi
    "bp-c11e8c29a7": "bp-90d0392e3c",  # Yacht Charter Split → ACI Marina Trogir
    "bp-e3cba3ab10": "bp-f245e138b7",  # Harbour Coffee Jakarta → Ancol public pier
    "bp-e6f1000592": "bp-3c14f6ef5b",  # Morning Bakery Desaru → Harbour Bay
    "bp-eac3c86c8f": "bp-73c2ac95b0",  # Osteria Mario RAK → Dubai Ferry Station
    "bp-eb77aab37d": "bp-fcd2b28e14",  # Terra Pizza Çeşme → Çeşme Cruise Port
}

# Zero-ref junk — drop without rebind.
DROP_ONLY = frozenset({"bp-c3c09a9cbd"})

HUA_HIN_PIER = "bp-cd5ab934c8"
HUA_HIN_COORD = [99.959, 12.5712]

JUNK_IDS = set(REBIND_MAP) | DROP_ONLY


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def poi_index(fbt: dict) -> dict[str, dict]:
    idx = {}
    for feat in fbt.get("poi") or []:
        pid = (feat.get("properties") or {}).get("id")
        if pid:
            idx[pid] = feat
    return idx


def poi_label(feat: dict) -> str:
    return (feat.get("properties") or {}).get("name") or ""


def rebind_value(val: str | None, old_bp: str, new_bp: str, labels: dict[str, str]) -> str | None:
    if not val or val != old_bp:
        return val
    return new_bp


def walk_rebind(obj, old_bp: str, new_bp: str, labels: dict[str, str]) -> int:
    n = 0
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k in ("from", "to", "bp_id", "pier_id", "endpoint_id") and v == old_bp:
                obj[k] = new_bp
                n += 1
            elif k in ("from_label", "to_label") and isinstance(v, str):
                pass
            else:
                n += walk_rebind(v, old_bp, new_bp, labels)
        if obj.get("from") == new_bp and "from_label" in obj:
            obj["from_label"] = labels.get(new_bp, obj.get("from_label"))
        if obj.get("to") == new_bp and "to_label" in obj:
            obj["to_label"] = labels.get(new_bp, obj.get("to_label"))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if item == old_bp:
                obj[i] = new_bp
                n += 1
            else:
                n += walk_rebind(item, old_bp, new_bp, labels)
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    fbt_path = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
    routes_path = ROOT / "data-clean" / "ROUTES.json"
    clusters_path = ROOT / "data-clean" / "CLUSTERS.json"
    report_path = ROOT / "handoff" / "partner-map-model" / "fe2-routebound-cleanup-report.json"

    fbt = load_json(fbt_path)
    pois = poi_index(fbt)
    routes = load_json(routes_path)
    clusters = load_json(clusters_path) if clusters_path.exists() else {}

    # Build labels for replacements
    labels: dict[str, str] = {}
    for old_bp, new_bp in REBIND_MAP.items():
        if new_bp in pois:
            labels[new_bp] = poi_label(pois[new_bp])

    report = {
        "at": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "rebinds": [],
        "drops": [],
        "hua_hin": {},
        "partner_hits": 0,
        "route_hits": 0,
        "cluster_hits": 0,
    }

    # Hua Hin coord fix
    if HUA_HIN_PIER in pois:
        feat = pois[HUA_HIN_PIER]
        old_coord = feat.get("geometry", {}).get("coordinates")
        report["hua_hin"] = {
            "id": HUA_HIN_PIER,
            "old_coord": old_coord,
            "new_coord": HUA_HIN_COORD,
        }
        if args.apply:
            feat.setdefault("geometry", {})["type"] = "Point"
            feat["geometry"]["coordinates"] = HUA_HIN_COORD
            props = feat.setdefault("properties", {})
            props["_fe2_coord_fix_at"] = report["at"]
            props["_fe2_coord_fix_source"] = "grok/fe2-hua-hin-pier"

    # Rebind routes
    for f in routes:
        props = f.get("properties") or {}
        rid = props.get("id")
        for old_bp, new_bp in REBIND_MAP.items():
            changed = False
            for side in ("from", "to"):
                if props.get(side) == old_bp:
                    props[side] = new_bp
                    label_key = f"{side}_label"
                    if label_key in props and new_bp in labels:
                        props[label_key] = labels[new_bp]
                    changed = True
            if changed:
                props["_fe2_rebind_at"] = report["at"]
                report["route_hits"] += 1
                report["rebinds"].append({"route_id": rid, "old": old_bp, "new": new_bp})

    # Partners
    partners_dir = ROOT / "data-clean" / "partners"
    for ppath in sorted(partners_dir.glob("*.json")):
        doc = load_json(ppath)
        hits = 0
        for old_bp, new_bp in REBIND_MAP.items():
            hits += walk_rebind(doc, old_bp, new_bp, labels)
        if hits:
            report["partner_hits"] += hits
            if args.apply:
                save_json(ppath, doc)

    # Clusters
    if clusters:
        hits = 0
        for old_bp, new_bp in REBIND_MAP.items():
            hits += walk_rebind(clusters, old_bp, new_bp, labels)
        report["cluster_hits"] = hits
        if args.apply and hits:
            save_json(clusters_path, clusters)

    # Drop junk POIs from poi layer
    drop_ids = set(JUNK_IDS)
    kept_poi = []
    for feat in fbt.get("poi") or []:
        pid = (feat.get("properties") or {}).get("id")
        if pid in drop_ids:
            report["drops"].append({"id": pid, "name": poi_label(feat)})
            continue
        kept_poi.append(feat)
    report["poi_before"] = len(fbt.get("poi") or [])
    report["poi_after"] = len(kept_poi)

    if args.apply:
        fbt["poi"] = kept_poi
        save_json(fbt_path, fbt)
        save_json(routes_path, routes)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(report_path, report)
    print(json.dumps({k: v for k, v in report.items() if k not in ("rebinds", "drops")}, indent=2))
    print(f"  rebinds={len(report['rebinds'])} drops={len(report['drops'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())