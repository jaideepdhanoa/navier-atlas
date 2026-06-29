#!/usr/bin/env python3
"""Sync partner card distance_nm to gold ROUTES.json distance_nm_geom for linked route_ids."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "data-clean" / "ROUTES.json"
PARTNERS = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff/partner-map-model" / "distance-honesty-sync-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def route_distances() -> dict[str, float]:
    raw = json.loads(ROUTES.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    out: dict[str, float] = {}
    for f in feats:
        p = f.get("properties") or {}
        rid = p.get("id")
        if not rid:
            continue
        d = p.get("distance_nm_geom") or p.get("distance_nm")
        if d is not None:
            out[rid] = float(d)
    return out


def walk(obj, distances: dict[str, float], fixes: list) -> None:
    if isinstance(obj, dict):
        rid = obj.get("route_id")
        if rid and rid in distances:
            card = obj.get("distance_nm")
            route_d = distances[rid]
            if card is not None and abs(float(card) - route_d) > 0.5:
                fixes.append({
                    "route_id": rid,
                    "was": card,
                    "now": route_d,
                    "label": obj.get("label") or obj.get("from") or obj.get("from_label"),
                })
                obj["distance_nm"] = round(route_d, 2)
        for v in obj.values():
            walk(v, distances, fixes)
    elif isinstance(obj, list):
        for item in obj:
            walk(item, distances, fixes)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", nargs="*")
    args = ap.parse_args()

    distances = route_distances()
    slugs = args.partner or sorted(p.stem for p in PARTNERS.glob("*.json"))
    all_fixes: dict[str, list] = {}

    for slug in slugs:
        path = PARTNERS / f"{slug}.json"
        if not path.is_file():
            continue
        doc = json.loads(path.read_text())
        fixes: list = []
        walk(doc, distances, fixes)
        if fixes:
            all_fixes[slug] = fixes
            if args.apply:
                path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")

    report = {"at": utc_now(), "mode": "apply" if args.apply else "dry-run", "fixes": all_fixes}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    total = sum(len(v) for v in all_fixes.values())
    print(json.dumps({"partners": len(all_fixes), "fixes": total}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())