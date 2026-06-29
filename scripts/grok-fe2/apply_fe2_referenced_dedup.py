#!/usr/bin/env python3
"""FE-2 referenced POI dedup — remap duplicate bp-* ids to keeper, then drop extras."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKLIST = ROOT / "data-clean" / "_handoff" / "fe2-grok-dedup-worklist.json"
REPORT = ROOT / "handoff" / "partner-map-model" / "fe2-referenced-dedup-report.json"

REMAP_PATHS = [
    ROOT / "data-clean" / "ROUTES.json",
    ROOT / "data-clean" / "STORIES.json",
    ROOT / "data-clean" / "CLUSTERS.json",
    ROOT / "data-clean" / "FEATURES_BY_TYPE.json",
    ROOT / "data-clean" / "BP_DEFS.json",
]
PARTNER_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hav_km(a: list, b: list) -> float:
    from math import radians, sin, cos, asin, sqrt

    lon1, lat1, lon2, lat2 = map(radians, [a[0], a[1], b[0], b[1]])
    h = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * asin(min(1, sqrt(h)))


def ref_index() -> set[str]:
    refs: set[str] = set()
    for rel in ("data-clean/ROUTES.json", "data-clean/STORIES.json", "data-clean/CLUSTERS.json"):
        p = ROOT / rel
        if p.exists():
            for token in p.read_text().split('"'):
                if token.startswith("bp-"):
                    refs.add(token)
    if PARTNER_DIR.exists():
        for p in PARTNER_DIR.glob("*.json"):
            for token in p.read_text().split('"'):
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


def remap_text(text: str, rename: dict[str, str]) -> tuple[str, int]:
    hits = 0
    out = text
    for old, new in sorted(rename.items(), key=lambda x: -len(x[0])):
        if old not in out:
            continue
        n = out.count(old)
        if n:
            hits += n
            out = out.replace(old, new)
    return out, hits


def collect_targets() -> list[Path]:
    paths = [p for p in REMAP_PATHS if p.exists()]
    if PARTNER_DIR.exists():
        paths.extend(sorted(PARTNER_DIR.glob("*.json")))
    if PITCH_DIR.exists():
        paths.extend(sorted(PITCH_DIR.rglob("*.json")))
    return paths


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--min-refs", type=int, default=2, help="only groups with N+ referenced copies")
    args = ap.parse_args()

    fbt_path = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
    fbt = json.loads(fbt_path.read_text())
    pois = {(p.get("properties") or {}).get("id"): p for p in fbt.get("poi") or []}
    cities = city_ids(fbt)
    refs = ref_index()
    groups = json.loads(WORKLIST.read_text())
    if args.limit > 0:
        groups = groups[: args.limit]

    rename: dict[str, str] = {}
    drop_ids: set[str] = set()
    merged_groups = 0

    for g in groups:
        copies = g.get("copies") or []
        if len(copies) < 2:
            continue
        referenced = [c for c in copies if c in refs]
        if len(referenced) < args.min_refs:
            continue
        keeper = pick_keeper(copies, pois, cities)
        merged_groups += 1
        for pid in copies:
            if pid == keeper:
                continue
            rename[pid] = keeper
            drop_ids.add(pid)

    # Collapse rename chains
    for old in list(rename):
        target = rename[old]
        while target in rename:
            target = rename[target]
        rename[old] = target

    path_hits: dict[str, int] = {}
    for path in collect_targets():
        text = path.read_text()
        new_text, hits = remap_text(text, rename)
        if hits:
            path_hits[str(path.relative_to(ROOT))] = hits
            if args.apply:
                path.write_text(new_text)

    if args.apply and drop_ids:
        fbt["poi"] = [p for p in fbt.get("poi") or [] if (p.get("properties") or {}).get("id") not in drop_ids]
        fbt_path.write_text(json.dumps(fbt, ensure_ascii=False, indent=2) + "\n")

    report = {
        "at": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "groups_merged": merged_groups,
        "rename_pairs": len(rename),
        "drops": len(drop_ids),
        "path_hits": path_hits,
        "poi_before": len(pois),
        "poi_after": len(pois) - len(drop_ids) if args.apply else len(pois) - len(drop_ids),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())