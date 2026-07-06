#!/usr/bin/env python3
"""Apply BP-CLEANUP-REGISTER.json before global reseal (Pass 1 precondition)."""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER_PATH = ROOT / "handoff" / "uae-consolidation" / "BP-CLEANUP-REGISTER.json"
FBT_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "grok-routing-output" / "bp-cleanup-apply-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def hub_score(name: str) -> int:
    n = (name or "").lower()
    score = 0
    for token, pts in (
        ("marina", 4),
        ("ferry", 4),
        ("terminal", 4),
        ("harbour", 2),
        ("harbor", 2),
        ("pier", 2),
        ("marine station", 3),
    ):
        if token in n:
            score += pts
    return score


def apply_register(register: dict, fbt: dict, routes: list, *, apply: bool) -> dict:
    drop_ids = {row["bp"] for row in register.get("DROP_junk") or []}
    retag = {row["bp"]: row["nearest"] for row in register.get("RETAG_city_mismatch") or []}
    relabel = {row["bp"]: row["suggest"] for row in register.get("RELABEL_aggregate") or []}

    dup_canonical: dict[str, str] = {}
    dup_groups: list[dict] = []
    for row in register.get("DUP_coord") or []:
        bps = row.get("bps") or []
        if len(bps) < 2:
            continue
        scores: list[tuple[int, str]] = []
        for bid in bps:
            name = bid
            for poi in fbt.get("poi") or []:
                if props(poi).get("id") == bid:
                    name = props(poi).get("name") or bid
                    break
            scores.append((hub_score(name), bid))
        scores.sort(reverse=True)
        keep = scores[0][1]
        for _, bid in scores[1:]:
            dup_canonical[bid] = keep
        dup_groups.append({"keep": keep, "merge": [b for b in bps if b != keep]})

    report = {
        "generated_at": utc_now(),
        "apply": apply,
        "drop_junk": len(drop_ids),
        "retag_city": 0,
        "relabel": 0,
        "dup_merge": len(dup_canonical),
        "routes_removed": 0,
        "routes_repointed": 0,
        "flagged_doubtful": [],
    }

    work_fbt = copy.deepcopy(fbt) if apply else fbt
    work_routes = copy.deepcopy(routes) if apply else routes

    new_pois = []
    for poi in work_fbt.get("poi") or []:
        p = props(poi)
        pid = p.get("id")
        if pid in drop_ids:
            continue
        if pid in dup_canonical:
            continue
        if pid in retag:
            if apply:
                p["parent_city_id"] = retag[pid]
                p["_bp_cleanup_retag"] = utc_now()
            report["retag_city"] += 1
        if pid in relabel:
            clean = relabel[pid]
            if apply:
                for field in ("name", "shortName", "fullName"):
                    if field in p:
                        p[field] = clean
                p["_bp_cleanup_relabel"] = utc_now()
            report["relabel"] += 1
        new_pois.append(poi)
    if apply:
        work_fbt["poi"] = new_pois

    repoint = {**dup_canonical}
    kept_routes = []
    for r in work_routes:
        p = props(r)
        fn = p.get("from") or p.get("from_node")
        tn = p.get("to") or p.get("to_node")
        if fn in drop_ids or tn in drop_ids:
            report["routes_removed"] += 1
            continue
        changed = False
        if fn in repoint:
            if apply:
                p["from"] = repoint[fn]
            changed = True
        if tn in repoint:
            if apply:
                p["to"] = repoint[tn]
            changed = True
        if changed:
            report["routes_repointed"] += 1
        kept_routes.append(r)

    if apply:
        return {
            **report,
            "fbt": work_fbt,
            "routes": kept_routes,
            "dup_groups": dup_groups,
        }
    return {**report, "dup_groups": dup_groups}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    register = json.loads(REGISTER_PATH.read_text())
    fbt = json.loads(FBT_PATH.read_text())
    routes = json.loads(ROUTES_PATH.read_text())
    if isinstance(routes, dict):
        routes = routes.get("features", [])

    result = apply_register(register, fbt, routes, apply=args.apply)
    receipt = {k: v for k, v in result.items() if k not in ("fbt", "routes")}

    if args.apply:
        FBT_PATH.write_text(json.dumps(result["fbt"], indent=2) + "\n")
        ROUTES_PATH.write_text(json.dumps(result["routes"], indent=2) + "\n")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    print(
        f"\n{'✓' if args.apply else '·'} BP cleanup: "
        f"drop={receipt['drop_junk']} retag={receipt['retag_city']} "
        f"dup={receipt['dup_merge']} routes_removed={receipt['routes_removed']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())