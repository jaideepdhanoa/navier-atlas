#!/usr/bin/env python3
"""FE-2 safe POI dedup — drop orphan-parent copies with zero refs."""
from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKLIST = ROOT / "data-clean" / "_handoff" / "fe2-grok-dedup-worklist.json"
REPORT = ROOT / "handoff" / "partner-map-model" / "fe2-poi-dedup-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hav_km(a: list, b: list) -> float:
    from math import radians, sin, cos, asin, sqrt

    lon1, lat1, lon2, lat2 = map(radians, [a[0], a[1], b[0], b[1]])
    h = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * asin(min(1, sqrt(h)))


def ref_index() -> set[str]:
    refs: set[str] = set()
    for rel in (
        "data-clean/ROUTES.json",
        "data-clean/STORIES.json",
        "data-clean/CLUSTERS.json",
    ):
        p = ROOT / rel
        if not p.exists():
            continue
        txt = p.read_text()
        for token in txt.split('"'):
            if token.startswith("bp-"):
                refs.add(token)
    for p in (ROOT / "data-clean" / "partners").glob("*.json"):
        txt = p.read_text()
        for token in txt.split('"'):
            if token.startswith("bp-"):
                refs.add(token)
    return refs


def city_ids(fbt: dict) -> set[str]:
    return {(c.get("properties") or {}).get("id") for c in fbt.get("city") or []}


def pick_keeper(copies: list[str], pois: dict, cities: set[str]) -> str:
    scored = []
    for pid in copies:
        feat = pois.get(pid)
        if not feat:
            continue
        pr = feat.get("properties") or {}
        coord = feat.get("geometry", {}).get("coordinates") or [0, 0]
        parent = pr.get("parent_city_id")
        in_city = 1 if parent in cities else 0
        scored.append((in_city, -hav_km(coord, coord), pid))
    if not scored:
        return copies[0]
    scored.sort(reverse=True)
    return scored[0][2]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    fbt_path = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
    fbt = json.loads(fbt_path.read_text())
    pois = {(p.get("properties") or {}).get("id"): p for p in fbt.get("poi") or []}
    cities = city_ids(fbt)
    refs = ref_index()
    groups = json.loads(WORKLIST.read_text())

    if args.limit > 0:
        groups = groups[: args.limit]

    drop_ids: set[str] = set()
    kept = 0
    for g in groups:
        copies = g.get("copies") or []
        if len(copies) < 2:
            continue
        keeper = pick_keeper(copies, pois, cities)
        for pid in copies:
            if pid == keeper:
                kept += 1
                continue
            if pid in refs:
                continue
            drop_ids.add(pid)

    report = {
        "at": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "groups_scanned": len(groups),
        "keepers": kept,
        "drops": len(drop_ids),
        "poi_before": len(fbt.get("poi") or []),
    }

    if args.apply and drop_ids:
        fbt["poi"] = [p for p in fbt.get("poi") or [] if (p.get("properties") or {}).get("id") not in drop_ids]
        fbt_path.write_text(json.dumps(fbt, ensure_ascii=False, indent=2) + "\n")

    report["poi_after"] = len(fbt.get("poi") or [])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())