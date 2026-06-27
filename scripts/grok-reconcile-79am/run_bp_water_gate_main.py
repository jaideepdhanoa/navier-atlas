#!/usr/bin/env python3
"""Run bp_on_water gate on main data-clean and update SEAL.json (#119)."""
from __future__ import annotations

import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
WORK = ROOT / "grok-routing-output"
SEAL = DC / "SEAL.json"
REPORT = WORK / "bp-water-adjacency-report.json"
ALLOWLIST = DC / "bp_water_allowlist.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def route_referenced_ids() -> set[str]:
    routes = json.loads((DC / "ROUTES.json").read_text())
    refs: set[str] = set()
    for f in routes:
        p = f.get("properties") or {}
        for k in ("from", "to"):
            v = p.get(k)
            if isinstance(v, str) and v:
                refs.add(v)
    return refs


def load_allowlist() -> dict:
    if ALLOWLIST.is_file():
        return json.loads(ALLOWLIST.read_text())
    fallback = ROOT / "_ingest/bp-seal-2026-06-20/inputs/bp_water_allowlist.json"
    if fallback.is_file():
        return json.loads(fallback.read_text())
    return {"water_bodies": [], "points": []}


def in_allowlist_bbox(lon: float, lat: float, allowlist: dict) -> bool:
    for body in allowlist.get("water_bodies", []):
        bbox = body.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
        min_lon, max_lon, min_lat, max_lat = bbox
        if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
            return True
    for pt in allowlist.get("points", []):
        if abs(pt.get("lng", 0) - lon) < 0.02 and abs(pt.get("lat", 0) - lat) < 0.02:
            return True
    return False


def build_candidates() -> list[dict]:
    """Gate boarding points (bp-*) referenced as gold route endpoints."""
    fbt = json.loads((DC / "FEATURES_BY_TYPE.json").read_text())
    refs = route_referenced_ids()
    by_id: dict[str, dict] = {}
    for coll in ("poi", "city", "locale"):
        for feat in fbt.get(coll, []):
            pid = (feat.get("properties") or {}).get("id")
            if pid:
                by_id[pid] = feat

    out = []
    for pid in sorted(refs):
        if not pid.startswith("bp-"):
            continue
        feat = by_id.get(pid)
        if not feat:
            continue
        p = feat.get("properties", {})
        if p.get("_quarantine"):
            continue
        coords = feat.get("geometry", {}).get("coordinates")
        if not coords or len(coords) < 2:
            continue
        out.append(
            {
                "id": pid,
                "name": p.get("name") or p.get("fullName"),
                "coords": coords[:2],
                "verdict": "KEEP",
                "reason": "route-endpoint-bp",
            }
        )
    return out


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    (ROOT / "grok-reconcile-79am-work").mkdir(exist_ok=True)
    work = ROOT / "grok-reconcile-79am-work"
    (work / "grok-routing-output").mkdir(parents=True, exist_ok=True)
    (work / "atlas-repo" / "data-clean").mkdir(parents=True, exist_ok=True)

    candidates = build_candidates()
    cand_path = work / "grok-routing-output" / "bp-candidates.json"
    cand_path.write_text(json.dumps(candidates, indent=2) + "\n")

    rc = subprocess.call(
        [
            sys.executable,
            str(ROOT / "scripts/grok-reconcile-79am/gate_bp_water_adjacency.py"),
            "--work",
            str(work),
            "--max-inland-km",
            "0.15",
        ]
    )
    if rc != 0:
        return rc

    report = json.loads((work / "grok-routing-output" / "bp-water-adjacency-report.json").read_text())
    allowlist = load_allowlist()
    candidates_by_id = {c["id"]: c for c in candidates}
    true_fail: list[dict] = []
    allowlisted: list[dict] = []
    for row in report.get("fail", []):
        cand = candidates_by_id.get(row["id"], {})
        coords = cand.get("coords") or [None, None]
        if in_allowlist_bbox(coords[0], coords[1], allowlist):
            allowlisted.append({**row, "allowlist_reason": "named navigable water body"})
        else:
            true_fail.append(row)
    n_pass = len(report.get("pass", [])) + len(allowlisted)
    n_true_fail = len(true_fail)
    verdict = (
        "PASS — 0 true mis-geocodes"
        if n_true_fail == 0
        else f"FAIL {n_true_fail} true mis-geocodes ({n_pass} pass / {len(allowlisted)} allowlisted)"
    )

    enriched = {
        **report,
        "at": utc_now(),
        "verdict": verdict,
        "scope": "bp-* route-endpoint boarding points only",
        "allowlist_size": len(allowlist.get("water_bodies", [])) + len(allowlist.get("points", [])),
        "allowlisted": allowlisted,
        "true_fail": true_fail,
        "summary": {
            "candidates": len(candidates),
            "pass_raw": len(report.get("pass", [])),
            "fail_raw": len(report.get("fail", [])),
            "allowlisted": len(allowlisted),
            "true_misgeocodes": n_true_fail,
        },
    }
    REPORT.write_text(json.dumps(enriched, indent=2) + "\n")

    seal = json.loads(SEAL.read_text())
    seal["gates"]["bp_on_water"] = verdict
    seal["sealed_at"] = utc_now()
    seal.setdefault("meta", {})["bp_on_water_gate_at"] = utc_now()
    SEAL.write_text(json.dumps(seal, indent=1, ensure_ascii=False) + "\n")

    print(f"bp_on_water: {verdict} (candidates={len(candidates)})")
    return 0 if n_true_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())