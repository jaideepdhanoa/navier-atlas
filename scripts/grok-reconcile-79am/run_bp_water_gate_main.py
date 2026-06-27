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


def build_candidates() -> list[dict]:
    """Gate POIs referenced as gold route endpoints (story/mesh operational set)."""
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
                "reason": "route-endpoint-referenced",
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
    n_pass = len(report.get("pass", []))
    n_fail = len(report.get("fail", []))
    verdict = "PASS" if n_fail == 0 else f"FAIL {n_pass} pass / {n_fail} fail"

    REPORT.write_text(json.dumps({**report, "at": utc_now(), "verdict": verdict}, indent=2) + "\n")

    seal = json.loads(SEAL.read_text())
    seal["gates"]["bp_on_water"] = verdict
    seal["sealed_at"] = utc_now()
    seal.setdefault("meta", {})["bp_on_water_gate_at"] = utc_now()
    SEAL.write_text(json.dumps(seal, indent=1, ensure_ascii=False) + "\n")

    print(f"bp_on_water: {verdict} (candidates={len(candidates)})")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())