#!/usr/bin/env python3
"""
RE-GROUND proposal surfaces — fix bp_binding by aligning labels to sealed route endpoints.

Decision tree (fix-first):
  1. Has route_id → sync from/to labels from ROUTES.json BP labels
  2. No route_id but from_node_id/to_node_id → attempt strict relink
  3. Phase-narrative misfit → defer to manual receipt

Usage:
  python3 scripts/reground_proposal_surfaces.py --partner grab --apply
  python3 scripts/reground_proposal_surfaces.py --partner bolt rapido careem noon --apply
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_proposal_fidelity import (  # noqa: E402
    audit_item,
    build_indexes,
    iter_proposal_items,
    resolve_route_id,
)
from relink_partner_journeys import (  # noqa: E402
    directional_endpoints_match,
    load_json,
    save_json,
)

TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
RECEIPT = ROOT / "handoff" / "partner-map-model" / "RE-GROUND-RECEIPT.json"


def bp_labels(route_by_id: dict, rid: str) -> tuple[str, str] | None:
    entry = route_by_id.get(rid)
    if not entry:
        return None
    p = entry["props"]
    fn, tn = p.get("from"), p.get("to")
    if not fn or not tn:
        return None
    # Resolve labels via indexes built in audit - use from_label on props if present
    fl = p.get("from_label") or fn
    tl = p.get("to_label") or tn
    # Load from FEATURES if needed
    fbt_path = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
    fbt = load_json(fbt_path)
    node_labels: dict[str, str] = {}
    for bucket in fbt:
        for feat in fbt.get(bucket, []) or []:
            props = feat.get("properties") or {}
            nid = props.get("id")
            if nid:
                node_labels[nid] = (props.get("label") or props.get("name") or nid).strip()

    if fn in node_labels:
        fl = node_labels[fn]
    if tn in node_labels:
        tl = node_labels[tn]
    return fl, tl


def reground_item(item: dict, indexes) -> tuple[dict, str]:
    gold, route_by_id, route_rec, city_of, bp_label_fn = indexes
    item = copy.deepcopy(item)
    rid = resolve_route_id(item)
    action = "unchanged"

    if rid and rid in gold:
        labels = bp_labels(route_by_id, rid)
        if labels:
            fl, tl = labels
            rec = route_rec(rid)
            from_l = item.get("from") or item.get("from_label") or ""
            to_l = item.get("to") or item.get("to_label") or ""
            if item.get("label") is not None or "featured" in str(item.get("_link_kind", "")):
                item["label"] = f"{fl} ↔ {tl}"
                item["from_label"] = fl
                item["to_label"] = tl
                action = "sync_featured_label"
            elif not directional_endpoints_match(from_l, to_l, rec) if rec else True:
                if item.get("from") is not None or "from" in item:
                    item["from"] = fl
                if item.get("to") is not None or "to" in item:
                    item["to"] = tl
                item["from_label"] = fl
                item["to_label"] = tl
                action = "sync_journey_labels"
            if rec:
                if rec.from_node:
                    item["from_node_id"] = rec.from_node
                if rec.to_node:
                    item["to_node_id"] = rec.to_node
                if rec.distance_nm is not None:
                    item["distance_nm"] = rec.distance_nm
            item["_link_source"] = "grok/reground_proposal_surfaces"
            item["_reground_at"] = TS
            for k in ("_inherit_source", "_inherit_at"):
                item.pop(k, None)

    item.pop("_link_source", None) if action == "unchanged" else None
    if action != "unchanged":
        item["_link_source"] = "grok/reground_proposal_surfaces"
    return item, action


def apply_partner(slug: str, *, apply: bool) -> dict:
    path = ROOT / "data-clean" / "partners" / f"{slug}.json"
    doc = load_json(path)
    indexes = build_indexes()
    stats = {"sync_journey_labels": 0, "sync_featured_label": 0, "unchanged": 0}

    def patch_list(items: list) -> list:
        out = []
        for item in items:
            if not isinstance(item, dict):
                continue
            fixed, action = reground_item(item, indexes)
            stats[action] = stats.get(action, 0) + 1
            out.append(fixed)
        return out

    doc["journeys_unlocked"] = patch_list(doc.get("journeys_unlocked") or [])
    for phase in doc.get("phases") or []:
        phase["featured_routes"] = patch_list(phase.get("featured_routes") or [])
    for market in doc.get("markets") or []:
        market["journeys_unlocked"] = patch_list(market.get("journeys_unlocked") or [])
        for phase in market.get("phases") or []:
            phase["featured_routes"] = patch_list(phase.get("featured_routes") or [])

    doc["_reground"] = {"at": TS, "source": "grok/reground_proposal_surfaces", "stats": stats}

    if apply:
        save_json(path, doc)
        pitch = ROOT / "partner-pitch" / "partners" / f"{slug}.json"
        if pitch.parent.exists():
            save_json(pitch, doc)

    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="+", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    receipt = {"at": TS, "partners": {}}
    for slug in args.partner:
        stats = apply_partner(slug, apply=args.apply)
        receipt["partners"][slug] = stats
        print(f"{slug}: {stats}")

    if args.apply:
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())