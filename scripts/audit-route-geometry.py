#!/usr/bin/env python3
"""Audit ROUTES.json land QA — story registry crosswalk + triage report."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))

from route_land_qa import evaluate_feature  # noqa: E402
from story_registry import collect_story_registry  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
ALLOW_PATH = ROOT / "data-clean" / "route_water_allowlist.json"
OUT_PATH = ROOT / "handoff" / "partner-map-model" / "GEOMETRY-TRIAGE.json"
AUDIT_PATH = ROOT / "handoff" / "partner-map-model" / "GEOMETRY-AUDIT.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_allowlist() -> set[str]:
    if not ALLOW_PATH.exists():
        return set()
    doc = json.loads(ALLOW_PATH.read_text())
    return set(doc.get("ids") or [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit 1 if story routes fail QA")
    ap.add_argument(
        "--strict-severe",
        action="store_true",
        help="exit 1 only if story routes have >1km interior land or are allowlisted",
    )
    ap.add_argument("--story-only", action="store_true")
    args = ap.parse_args()

    story = collect_story_registry()
    allow = load_allowlist()
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])

    rows = []
    story_fail = 0
    story_pass = 0
    mesh_fail = 0
    mesh_pass = 0

    for f in feats:
        props = f.get("properties") or {}
        rid = props.get("id")
        if not rid:
            continue
        is_story = rid in story
        if args.story_only and not is_story:
            continue
        ev = evaluate_feature(f)
        allowlisted = rid in allow
        row = {
            "route_id": rid,
            "story": is_story,
            "story_tags": story.get(rid, []) if is_story else [],
            "qa_pass": ev["qa_pass"],
            "interior_land_km": ev["interior_land_km"],
            "mask": ev["mask"],
            "allowlisted": allowlisted,
            "edge_class": props.get("edge_class"),
            "distance_nm": props.get("distance_nm"),
        }
        rows.append(row)
        if is_story:
            if ev["qa_pass"]:
                story_pass += 1
            else:
                story_fail += 1
        else:
            if ev["qa_pass"]:
                mesh_pass += 1
            else:
                mesh_fail += 1

    story_allowlisted = [r for r in rows if r["story"] and r["allowlisted"]]
    story_fail_rows = [r for r in rows if r["story"] and not r["qa_pass"]]

    out = {
        "generated_at": utc_now(),
        "threshold_km": 0.05,
        "total_routes": len(rows),
        "story_routes": len(story),
        "story_pass": story_pass,
        "story_fail": story_fail,
        "story_allowlisted": len(story_allowlisted),
        "mesh_pass": mesh_pass,
        "mesh_fail": mesh_fail,
        "allowlist_size": len(allow),
        "priority_fix": sorted(
            story_fail_rows,
            key=lambda r: (-r["interior_land_km"], r["route_id"]),
        )[:200],
        "routes": rows if args.story_only else None,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    summary = {
        "generated_at": out["generated_at"],
        "total_routes": out["total_routes"],
        "story_pass": story_pass,
        "story_fail": story_fail,
        "story_allowlisted": len(story_allowlisted),
        "mesh_fail": mesh_fail,
        "allowlist_size": len(allow),
    }
    AUDIT_PATH.write_text(json.dumps(summary, indent=2) + "\n")

    print(f"Geometry audit → {OUT_PATH}")
    print(f"  routes: {len(rows)}")
    print(f"  story: {story_pass} pass / {story_fail} fail ({len(story_allowlisted)} allowlisted)")
    print(f"  mesh:  {mesh_pass} pass / {mesh_fail} fail")
    print(f"  allowlist: {len(allow)}")

    if story_allowlisted:
        print(f"  ✗ story routes on allowlist: {len(story_allowlisted)}")
    if story_fail:
        print(f"  ⚠ story routes failing QA: {story_fail}")

    severe = [r for r in story_fail_rows if r["interior_land_km"] > 1.0]
    out["story_severe_fail"] = len(severe)

    if args.strict_severe and (severe or story_allowlisted):
        print(f"\nGEOMETRY AUDIT FAILED — {len(severe)} severe story fails (>1km), allowlisted={len(story_allowlisted)}")
        return 1
    if args.strict and (story_fail or story_allowlisted):
        print("\nGEOMETRY AUDIT FAILED — story routes must pass QA and not be allowlisted.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())