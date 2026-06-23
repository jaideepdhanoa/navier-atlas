#!/usr/bin/env python3
"""Document story routes that fail QA after coastal fix — pending channel authorship."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))
from route_land_qa import evaluate_feature  # noqa: E402
from story_registry import collect_story_registry  # noqa: E402

OUT = ROOT / "handoff" / "partner-map-model" / "GEOMETRY-STORY-HOLD.json"
TRIAGE = ROOT / "handoff" / "partner-map-model" / "GEOMETRY-TRIAGE.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    story = collect_story_registry()
    triage = json.loads(TRIAGE.read_text()) if TRIAGE.exists() else {}
    fail_by_id = {r["route_id"]: r for r in triage.get("priority_fix", [])}

    raw = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    hold = []
    for f in feats:
        props = f.get("properties") or {}
        rid = props.get("id")
        if not rid or rid not in story:
            continue
        ev = evaluate_feature(f)
        if ev["qa_pass"]:
            continue
        hold.append({
            "route_id": rid,
            "story_tags": story[rid],
            "interior_land_km": ev["interior_land_km"],
            "distance_nm": props.get("distance_nm"),
            "edge_class": props.get("edge_class"),
            "reason": "pending_channel_authorship",
            "next_lane": "grok/solve_routes_phase2_or_hand_waypoints",
        })

    doc = {
        "generated_at": utc_now(),
        "count": len(hold),
        "routes": hold,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"hold_count": len(hold), "path": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())