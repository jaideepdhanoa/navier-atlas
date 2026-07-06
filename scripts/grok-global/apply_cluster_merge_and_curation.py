#!/usr/bin/env python3
"""Cluster merge cascade + render curation (Tasklet 9fbab02f / 443816a5 / 46bc2714).

1. Rebind retired cluster_ids in ROUTES + live data
2. Berth-pair redundancy dedupe (exact label+city duplicates)
3. Tag sovereign intra-giga corridors for commercial-partner render suppression
4. Partner scope key cleanup (stale cluster ids)
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import load_json, route_features, save_routes  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
REPORT_PATH = ROOT / "grok-routing-output" / "cluster-merge-curation-report.json"
HANDOFF_REPORT = ROOT / "handoff" / "CLUSTER-MERGE-CURATION-2026-07-06.json"

CLUSTER_MERGE = {
    "uae-east-coast": "uae",
    "dammam-eastern-province-ksa": "saudi-arabia",
    "ksa-commercial": "saudi-arabia",
}
RETIRED_CLUSTERS = frozenset(CLUSTER_MERGE.keys())

SOVEREIGN_CITY_IDS = frozenset(
    {
        "neom-sindalah-ksa",
        "red-sea-global-ksa",
        "the-red-sea-archipelago-ksa",
        "amaala-triple-bay-ksa",
        "thuwal-private-retreat-ksa",
    }
)

COMMERCIAL_PARTNERS = frozenset({"bolt", "yango", "uber", "careem", "noon", "indrive", "cabify"})

ROUTE_CLUSTER_FIELDS = ("cluster_id", "from_cluster_id", "to_cluster_id")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def props(feat: dict) -> dict:
    return feat.get("properties") or feat


def rebind_value(val: Any, counts: Counter) -> Any:
    if isinstance(val, str) and val in CLUSTER_MERGE:
        counts[val] += 1
        return CLUSTER_MERGE[val]
    if isinstance(val, list):
        out = []
        changed = False
        for x in val:
            if isinstance(x, str) and x in CLUSTER_MERGE:
                counts[x] += 1
                out.append(CLUSTER_MERGE[x])
                changed = True
            else:
                out.append(x)
        return sorted(set(out)) if changed else val
    return val


def rebind_routes(routes: list[dict]) -> tuple[list[dict], Counter]:
    counts: Counter = Counter()
    for feat in routes:
        p = props(feat)
        for field in ROUTE_CLUSTER_FIELDS:
            if field in p:
                p[field] = rebind_value(p[field], counts)
        if "cluster_ids" in p:
            p["cluster_ids"] = rebind_value(p.get("cluster_ids"), counts)
    return routes, counts


def canonical_score(feat: dict) -> tuple:
    p = props(feat)
    rid = p.get("id") or ""
    coords = feat.get("geometry", {}).get("coordinates") or []
    pref = 0
    if rid.startswith("rn-"):
        pref += 4
    elif rid.startswith("edge-"):
        pref += 2
    elif rid.startswith("e__"):
        pref += 1
    if rid.startswith("ics-"):
        pref -= 2
    land = float(p.get("_land_km_interior") or p.get("_geometry_land_km") or 0)
    return (pref, len(coords), -land, rid)


def dedupe_berth_pairs(routes: list[dict], report: dict) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    drop_ids: set[str] = set()

    for feat in routes:
        p = props(feat)
        fl, tl = p.get("from_label"), p.get("to_label")
        if fl and tl and fl == tl:
            drop_ids.add(p.get("id"))
            report["self_berth_dropped"].append(p.get("id"))
            continue
        key = (p.get("from_city_id"), p.get("to_city_id"), fl, tl)
        groups[key].append(feat)

    for key, feats in groups.items():
        if len(feats) <= 1:
            continue
        feats.sort(key=canonical_score, reverse=True)
        keep = feats[0]
        for dup in feats[1:]:
            rid = props(dup).get("id")
            if rid:
                drop_ids.add(rid)
        report["dedupe_groups"].append(
            {
                "key": key,
                "kept": props(keep).get("id"),
                "dropped": [props(d).get("id") for d in feats[1:]],
                "count": len(feats),
            }
        )

    out = [f for f in routes if props(f).get("id") not in drop_ids]
    report["summary"]["deduped"] = len(drop_ids) - len(report["self_berth_dropped"])
    report["summary"]["dedupe_pairs"] = len(report["dedupe_groups"])
    return out


def tag_sovereign_suppression(routes: list[dict], report: dict) -> None:
    tagged = 0
    kept_trunk = 0
    for feat in routes:
        p = props(feat)
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if fc in SOVEREIGN_CITY_IDS and tc in SOVEREIGN_CITY_IDS:
            p["_commercial_suppress_sovereign"] = True
            p["_suppress_reason"] = "intra_giga_project"
            tagged += 1
        elif (fc in SOVEREIGN_CITY_IDS) ^ (tc in SOVEREIGN_CITY_IDS):
            p.pop("_commercial_suppress_sovereign", None)
            kept_trunk += 1
        else:
            p.pop("_commercial_suppress_sovereign", None)
    report["summary"]["sovereign_suppressed"] = tagged
    report["summary"]["sovereign_trunk_kept"] = kept_trunk


def walk_rebind_json(obj: Any, counts: Counter) -> Any:
    if isinstance(obj, dict):
        return {k: walk_rebind_json(v, counts) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_rebind_json(x, counts) for x in obj]
    if isinstance(obj, str) and obj in CLUSTER_MERGE:
        counts[obj] += 1
        return CLUSTER_MERGE[obj]
    return obj


def clean_partner_scope(partner: dict, partner_id: str, report: dict) -> dict:
    doc = copy.deepcopy(partner)
    scope = dict(doc.get("_map_scope") or {})
    changes: list[str] = []

    def clean_list(key: str) -> None:
        nonlocal changes
        items = list(scope.get(key) or [])
        new: list[str] = []
        for x in items:
            if x in RETIRED_CLUSTERS:
                merged = CLUSTER_MERGE[x]
                if merged not in new:
                    new.append(merged)
                changes.append(f"{key}: {x}→{merged}")
            elif x == "bolt-ksa-commercial" and partner_id == "bolt":
                if "saudi-arabia" not in new:
                    new.append("saudi-arabia")
                changes.append(f"{key}: bolt-ksa-commercial→saudi-arabia")
            elif x not in new:
                new.append(x)
        scope[key] = sorted(new)

    for k in ("registry_keys", "cluster_city_ids", "contested_cluster_ids"):
        clean_list(k)

    # Remove Norway from Yango scope surfaces (correction 46bc2714 — geography stays on atlas/Uber)
    if partner_id == "yango":
        for k in ("registry_keys", "cluster_city_ids", "contested_cluster_ids"):
            before = len(scope.get(k) or [])
            scope[k] = [x for x in (scope.get(k) or []) if "norway" not in x.lower()]
            if len(scope[k]) < before:
                changes.append(f"{k}: removed norway refs")

    if changes:
        scope["generated"] = utc_now()
        scope["source"] = "cluster_merge_cascade_2026-07-06"
        doc["_map_scope"] = scope
        report["partner_scope"][partner_id] = changes
    return doc


def rebind_file(path: Path, counts: Counter, apply: bool) -> int:
    if not path.is_file():
        return 0
    text = path.read_text()
    n_before = sum(text.count(k) for k in RETIRED_CLUSTERS)
    if not n_before:
        return 0
    obj = json.loads(text)
    obj = walk_rebind_json(obj, counts)
    if apply:
        path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    return n_before


def residual_scan() -> dict[str, int]:
    out: dict[str, int] = {}
    for path in (ROOT / "data-clean").rglob("*"):
        if not path.is_file() or path.suffix not in (".json", ".md"):
            continue
        if path.name == "SEAL.json":
            continue
        try:
            text = path.read_text()
        except OSError:
            continue
        for k in RETIRED_CLUSTERS:
            c = len(re.findall(re.escape(k), text))
            if c:
                out[str(path.relative_to(ROOT))] = out.get(str(path.relative_to(ROOT)), 0) + c
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    routes = route_features(load_json(ROUTES_PATH))
    before = len(routes)

    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "routes_before": before,
        "cluster_rebind": {},
        "self_berth_dropped": [],
        "dedupe_groups": [],
        "partner_scope": {},
        "summary": {},
    }

    routes, rebind_counts = rebind_routes(routes)
    report["cluster_rebind"] = dict(rebind_counts)

    routes = dedupe_berth_pairs(routes, report)
    tag_sovereign_suppression(routes, report)

    report["routes_after"] = len(routes)
    report["summary"]["routes_dropped"] = before - len(routes)
    report["summary"]["net_after_dedupe"] = len(routes)

    if args.apply:
        save_routes(ROUTES_PATH, routes)

        file_counts: Counter = Counter()
        for rel in (
            "data-clean/economics_by_route_id.json",
            "data-clean/PENDING-ECONOMICS-TRIAGE.json",
            "handoff/global-marquee-pass2/CANONICAL-MARQUEES.json",
        ):
            rebind_file(ROOT / rel, file_counts, True)

        for path in sorted(PARTNERS_DIR.glob("*.json")):
            partner = json.loads(path.read_text())
            pid = path.stem
            updated = clean_partner_scope(partner, pid, report)
            text = json.dumps(updated, indent=2) + "\n"
            path.write_text(text)
            pitch = PITCH_DIR / path.name
            if pitch.parent.is_dir():
                pitch.write_text(text)

        report["file_rebind"] = dict(file_counts)

    report["residual_refs"] = residual_scan()

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    HANDOFF_REPORT.write_text(json.dumps(report, indent=2) + "\n")

    s = report["summary"]
    print(
        f"  cluster-merge+curation: routes {before} → {report['routes_after']} "
        f"(rebind {sum(rebind_counts.values())}, deduped {s.get('deduped',0)}, "
        f"sovereign-suppress {s.get('sovereign_suppressed',0)})"
    )
    if report["residual_refs"]:
        print(f"  residual retired-cluster refs: {sum(report['residual_refs'].values())} in {len(report['residual_refs'])} files")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())