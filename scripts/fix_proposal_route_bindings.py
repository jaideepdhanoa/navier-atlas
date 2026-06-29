#!/usr/bin/env python3
"""
Apply known-correct route_id bindings from sealed ROUTES.json labels.

Clears poisoned bindings (wrong route on right label) and promotes route_ids[] → route_id.

Usage:
  python3 scripts/fix_proposal_route_bindings.py --partner grab bolt --apply
"""
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
RECEIPT = ROOT / "handoff" / "partner-map-model" / "ROUTE-BINDING-FIX-RECEIPT.json"

# (from_label_substr, to_label_substr) -> route_id
LABEL_BINDINGS: dict[tuple[str, str], str] = {
    ("Ao Po Grand Marina", "Anantara Layan"): "rn-b28ac4ca3d14",
    ("Royal Phuket Marina", "Similan"): "gcn-0cc5f4e157-shared",
    ("Manoh Pier", "Thap Lamu"): "rn-b1313beb0eaa",
    ("Bach Dang Speed Ferry Terminal", "Bến đò Tắc Suất"): "rn-a0654d43e7e4",
    ("Cebu Port Pier 1", "Tagbilaran"): "rn-66e9451f405f",
    ("HoiAn Flow", "Cù lao Chàm"): "ics-1312999652",
    ("Tuan Chau International Marina", "Cat Ba"): "ics-f21c5d7e8d",
    ("Port de Cannes, Jetée Albert Edouard", "Voiles de Lérins"): "ics-529325c5eb",
    ("Ushuaïa Dubai Harbour Experience", "Marina Mall"): "gcn-4ae479b872-bolt",
}

POISONED_ROUTES = frozenset({"rn-eb5758aeba2a", "ics-c142307006"})


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def item_labels(item: dict) -> tuple[str, str]:
    fl = item.get("from") or item.get("from_label") or ""
    tl = item.get("to") or item.get("to_label") or ""
    lab = item.get("label") or ""
    if not fl and lab:
        for sep in ("↔", "→", "->"):
            if sep in lab:
                parts = lab.split(sep, 1)
                fl, tl = parts[0].strip(), parts[1].strip()
                break
    return fl, tl


def match_binding(fl: str, tl: str) -> str | None:
    pair = f"{fl} {tl}".lower()
    for (a, b), rid in LABEL_BINDINGS.items():
        if a.lower() in pair and b.lower() in pair:
            return rid
    return None


def fix_item(item: dict, partner: str) -> tuple[dict, str]:
    item = copy.deepcopy(item)
    action = "unchanged"
    fl, tl = item_labels(item)
    rid = item.get("route_id") or ((item.get("route_ids") or [None])[0])

    if rid in POISONED_ROUTES:
        item["route_id"] = None
        item["route_ids"] = None
        item["_link_status"] = "unlinked-poison-cleared"
        action = "cleared_poison"

    new_rid = match_binding(fl, tl)
    if new_rid:
        partner_rid = new_rid
        if new_rid.startswith("gcn-") and partner in ("bolt", "careem", "yango"):
            alt = new_rid.replace("-shared", f"-{partner}")
            routes = load_json(ROOT / "data-clean" / "ROUTES.json")
            ids = {r["properties"]["id"] for r in routes}
            if alt in ids:
                partner_rid = alt
        if item.get("route_id") != partner_rid:
            item["route_id"] = partner_rid
            item["route_ids"] = [partner_rid]
            item["_link_status"] = "linked-binding-fix"
            item["_link_source"] = "grok/fix_proposal_route_bindings"
            item["_binding_fix_at"] = TS
            action = "bound" if action == "unchanged" else action + "+bound"

    elif rid and not item.get("route_id") and item.get("route_ids"):
        item["route_id"] = rid
        item["_link_source"] = "grok/fix_proposal_route_bindings"
        item["_binding_fix_at"] = TS
        action = "promoted_route_id"

    if fl == "Manado" and "Lembeh" in tl and item.get("route_id") in POISONED_ROUTES | {None}:
        item["route_id"] = None
        item["route_ids"] = None
        item["_link_status"] = "unlinked-no-gold-route"
        item["_fidelity_trim"] = {"at": TS, "reason": "hold_null_manado_lembeh"}
        action = "hold_null"

    return item, action


def walk_items(doc: dict, partner: str) -> tuple[dict, dict]:
    stats: dict[str, int] = {}

    def patch_list(items: list) -> list:
        out = []
        for item in items:
            if not isinstance(item, dict):
                continue
            fixed, action = fix_item(item, partner)
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
    return doc, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="+", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    receipt = {"at": TS, "partners": {}}
    for slug in args.partner:
        path = ROOT / "data-clean" / "partners" / f"{slug}.json"
        doc = load_json(path)
        doc, stats = walk_items(doc, slug)
        doc["_route_binding_fix"] = {"at": TS, "stats": stats}
        receipt["partners"][slug] = stats
        print(f"{slug}: {stats}")
        if args.apply:
            save_json(path, doc)
            pitch = ROOT / "partner-pitch" / "partners" / f"{slug}.json"
            if pitch.parent.exists():
                save_json(pitch, doc)

    if args.apply:
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())