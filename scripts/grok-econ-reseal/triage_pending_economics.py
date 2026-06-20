#!/usr/bin/env python3
"""Honest pending-economics triage: actionable vs structural buckets."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORRIDORS = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"


def load_json(p: Path):
    return json.loads(p.read_text())


def route_features(obj):
    return obj if isinstance(obj, list) else obj.get("features", [])


def fix_hint(corr: dict, rid_in_gold: bool, from_bp: str | None, to_bp: str | None) -> str:
    rid = corr.get("route_id")
    a, b = corr.get("from_node_id"), corr.get("to_node_id")
    if corr.get("aspirational"):
        return "hold"
    if rid and str(rid).startswith("gcn-") and not rid_in_gold:
        return "mint_gcn"
    if a and b and a == b and not rid:
        if from_bp and to_bp and from_bp != to_bp:
            return "mint_rn"
        return "seal_bp"
    if a and b and a != b and not from_bp:
        return "seal_bp"
    if a and b and a != b and from_bp and to_bp and not rid_in_gold:
        return "mint_rn"
    if not a or not b:
        return "hold"
    if rid and not rid_in_gold:
        return "mint_gcn"
    return "hold"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--corridors", default=str(DEFAULT_CORRIDORS))
    ap.add_argument("--out", default="data-clean/PENDING-ECONOMICS-TRIAGE.json")
    args = ap.parse_args()

    dc = ROOT / args.dc
    econ = load_json(dc / "economics_by_route_id.json")
    pending = econ.get("_pending_route_pin", [])
    records_n = len(econ.get("records", []))
    pending_n = len(pending)

    routes = route_features(load_json(dc / "ROUTES.json"))
    gold = {r.get("properties", r).get("id") for r in routes}
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")

    sys_path = ROOT / "scripts/grok-bolt-yango"
    import sys

    sys.path.insert(0, str(sys_path))
    from bolt_yango_routing_shared import build_bp_index, resolve_corridor_endpoints

    bp_idx = build_bp_index(fbt)
    corr_doc = load_json(Path(args.corridors))
    pending_keys = {(x["market"], x["corridor"]) for x in pending}

    sub_buckets = Counter()
    per_corridor = []
    for mkey, mval in (corr_doc.get("markets") or {}).items():
        partner = mval.get("partner", "?")
        for c in mval.get("corridors") or []:
            label = f"{c.get('from')} -> {c.get('to')}"
            key = (mkey, label)
            if key not in pending_keys:
                continue
            rid = c.get("route_id")
            rid_in_gold = bool(rid and rid in gold)
            from_bp, to_bp, _, _ = resolve_corridor_endpoints(c, bp_idx)
            a, b = c.get("from_node_id"), c.get("to_node_id")
            if rid and str(rid).startswith("gcn-") and not rid_in_gold:
                bucket = "gcn_declared_not_in_gold"
            elif a and b and a == b and not rid:
                if from_bp and to_bp and from_bp != to_bp:
                    bucket = "bp_pair_ready"
                elif from_bp or to_bp:
                    bucket = "one_bp"
                else:
                    bucket = "same_node_no_route_id"
            elif not from_bp and not to_bp:
                bucket = "no_bp"
            elif c.get("aspirational"):
                bucket = "intentional_hold"
            else:
                bucket = "other_actionable"
            sub_buckets[bucket] += 1
            pend_row = next((x for x in pending if x["market"] == mkey and x["corridor"] == label), {})
            per_corridor.append(
                {
                    "partner": partner,
                    "market": mkey,
                    "corridor": label,
                    "reason": pend_row.get("reason"),
                    "sub_bucket": bucket,
                    "fix_hint": fix_hint(c, rid_in_gold, from_bp, to_bp),
                    "route_id": rid,
                    "from_bp": from_bp,
                    "to_bp": to_bp,
                }
            )

    by_reason = Counter(x.get("reason") for x in pending)
    by_partner = defaultdict(Counter)
    for x in pending:
        by_partner[x.get("authored_for") or x.get("partner") or "?"][x.get("reason", "?")] += 1

    actionable = (
        sub_buckets["gcn_declared_not_in_gold"]
        + sub_buckets["bp_pair_ready"]
        + sub_buckets["other_actionable"]
    )
    structural = sub_buckets["same_node_no_route_id"] + sub_buckets["intentional_hold"]
    pin_rate_raw = records_n / (records_n + pending_n) if (records_n + pending_n) else 0
    pin_rate_actionable = (
        records_n / (records_n + actionable) if (records_n + actionable) else 1.0
    )

    payload = {
        "_meta": {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "records": records_n,
            "pending_total": pending_n,
            "pin_rate_raw": round(pin_rate_raw, 4),
            "pin_rate_actionable": round(pin_rate_actionable, 4),
            "actionable_pending": actionable,
            "structural_holds": structural,
        },
        "by_reason": dict(by_reason),
        "by_partner": {k: dict(v) for k, v in sorted(by_partner.items())},
        "sub_buckets": dict(sub_buckets),
        "corridors": per_corridor,
    }

    out = ROOT / args.out
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload["_meta"], indent=2))
    print(f"→ {out}")


if __name__ == "__main__":
    main()