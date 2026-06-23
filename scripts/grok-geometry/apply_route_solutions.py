#!/usr/bin/env python3
"""Apply grok-routing-output/route-solutions.jsonl geometries into ROUTES.json."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))
from route_land_qa import evaluate_route  # noqa: E402

ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
SOLUTIONS = ROOT / "grok-routing-output" / "route-solutions.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    if not SOLUTIONS.exists():
        print("no route-solutions.jsonl")
        return 0
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id = {(f.get("properties") or {}).get("id"): f for f in feats if (f.get("properties") or {}).get("id")}
    by_ft = {}
    for f in feats:
        p = f.get("properties") or {}
        key = (p.get("from"), p.get("to"))
        if key[0] and key not in by_ft:
            by_ft[key] = f

    applied = 0
    for line in SOLUTIONS.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if not row.get("qa_pass") or not row.get("geometry"):
            continue
        rid = row.get("route_id")
        feat = by_id.get(rid) if rid else None
        if not feat:
            feat = by_ft.get((row.get("from_id"), row.get("to_id")))
        if not feat:
            continue
        coords = row["geometry"]["coordinates"]
        ev = evaluate_route(coords)
        if not ev["qa_pass"]:
            continue
        rid = (feat.get("properties") or {}).get("id")
        feat["geometry"] = row["geometry"]
        props = feat.setdefault("properties", {})
        props["geometry_smooth"] = coords
        props["render_smooth"] = False
        props["_geometry_fix_at"] = utc_now()
        props["_geometry_fix_source"] = "grok/apply_route_solutions"
        applied += 1

    ROUTES_PATH.write_text(json.dumps(feats, ensure_ascii=False) + "\n")
    print(json.dumps({"applied": applied}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())