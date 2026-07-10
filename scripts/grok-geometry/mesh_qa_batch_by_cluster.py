#!/usr/bin/env python3
"""Mesh land-QA burn-down: process failing non-story routes by cluster.

Runs mint_story_channels nudge-only per cluster with a per-cluster limit to
avoid global hangs. Emits a receipt.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from route_land_qa import evaluate_feature  # noqa: E402
from story_registry import collect_story_registry  # noqa: E402

ROUTES = ROOT / "data-clean/ROUTES.json"
RECEIPT = ROOT / "handoff/partner-map-model/MESH-QA-BATCH-RECEIPT.json"
MINT = ROOT / "scripts/grok-geometry/mint_story_channels.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect_mesh_fails() -> dict[str, list[str]]:
    story = collect_story_registry()
    raw = json.loads(ROUTES.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features") or []
    by_cluster: dict[str, list[str]] = defaultdict(list)
    for f in feats:
        p = f.get("properties") or {}
        rid = p.get("id")
        if not rid or rid in story:
            continue
        ev = evaluate_feature(f)
        if not ev.get("qa_pass"):
            cid = p.get("cluster_id") or "_none"
            by_cluster[cid].append(rid)
    return dict(by_cluster)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--top-clusters", type=int, default=8, help="clusters by fail count")
    ap.add_argument("--per-cluster", type=int, default=25, help="max routes per cluster")
    ap.add_argument("--max-land-km", type=float, default=5.0)
    args = ap.parse_args()

    print("→ scanning mesh fails (coarse mask)…")
    by_c = collect_mesh_fails()
    ranked = sorted(by_c.items(), key=lambda kv: -len(kv[1]))
    print("top clusters:", [(c, len(ids)) for c, ids in ranked[:15]])

    targets = ranked[: args.top_clusters]
    all_route_ids: list[str] = []
    plan = []
    for cid, ids in targets:
        take = ids[: args.per_cluster]
        plan.append({"cluster_id": cid, "fails": len(ids), "batch": len(take), "route_ids": take})
        all_route_ids.extend(take)

    receipt = {
        "at": utc_now(),
        "total_mesh_fail_clusters": len(by_c),
        "total_mesh_fails": sum(len(v) for v in by_c.values()),
        "plan": [{k: v for k, v in p.items() if k != "route_ids"} | {"n_routes": p["batch"]} for p in plan],
        "route_ids": all_route_ids,
    }

    if not args.apply:
        print(json.dumps(receipt, indent=2)[:2000])
        return 0

    if not all_route_ids:
        print("nothing to fix")
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
        return 0

    # One mint invocation with explicit route list (nudge-only, capped land)
    cmd = [
        sys.executable,
        str(MINT),
        "--mesh-fails",  # still ok with --route override of targets
        "--nudge-only",
        f"--max-land-km={args.max_land_km}",
        "--apply",
        "--route",
        *all_route_ids,
    ]
    # mint_story_channels: --route alone should target those routes; --mesh-fails may re-scan.
    # Prefer --route without mesh-fails if supported
    cmd = [
        sys.executable,
        str(MINT),
        "--nudge-only",
        f"--max-land-km={args.max_land_km}",
        "--apply",
        "--route",
        *all_route_ids,
    ]
    print("→ mint_story_channels", len(all_route_ids), "routes…")
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=900)
    receipt["mint_returncode"] = proc.returncode
    receipt["mint_stdout_tail"] = (proc.stdout or "")[-2000:]
    receipt["mint_stderr_tail"] = (proc.stderr or "")[-1000:]
    print(proc.stdout[-1500:] if proc.stdout else proc.stderr)

    # re-count fails in batched ids
    raw = json.loads(ROUTES.read_text())
    feats = { (f.get("properties") or {}).get("id"): f for f in (raw if isinstance(raw, list) else raw.get("features") or []) }
    still = 0
    fixed = 0
    for rid in all_route_ids:
        f = feats.get(rid)
        if not f:
            continue
        if evaluate_feature(f).get("qa_pass"):
            fixed += 1
        else:
            still += 1
    receipt["batch_fixed"] = fixed
    receipt["batch_still_fail"] = still

    # global mesh fail recount (story excluded) — sample count only via full scan optional
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"batch_fixed": fixed, "batch_still_fail": still, "receipt": str(RECEIPT)}, indent=2))
    return 0 if proc.returncode == 0 else proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
