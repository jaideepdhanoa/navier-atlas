#!/usr/bin/env python3
"""Bind validated cross-border Bolt journeys to sealed route_ids."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNER_PATHS = [
    ROOT / "partner-pitch/partners/bolt.json",
    ROOT / "data-clean/partners/bolt.json",
]

# journey (from_substr, to_substr) -> route_id
CROSS_BIND = {
    ("Dubrovnik", "Kotor"): "rn-933f14e08a33",
}

# Fix node IDs + clear text_only when route exists
NODE_FIX = {
    ("Rhodes", "Marmaris"): {
        "route_id": "rn-a95f11ef9a7e",
        "from_node_id": "rhodes-dodecanese-greece",
        "to_node_id": "bodrum-turkey",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def patch_journey(j: dict, extra: dict) -> bool:
    changed = False
    for k, v in extra.items():
        if j.get(k) != v:
            j[k] = v
            changed = True
    if j.get("display") == "text_only":
        j.pop("display", None)
        changed = True
    if extra.get("route_id"):
        j["_link_status"] = "linked-grok-scoped"
        j["_link_source"] = "grok/bolt_crossborder_bind"
        j.pop("economics_status", None)
        changed = True
    return changed


def bind(partner: dict) -> dict:
    stats = {"cross_bound": 0, "node_fixed": 0}
    for market in partner.get("markets", []):
        mid = market.get("id")
        for j in market.get("journeys_unlocked", []):
            f, t = j.get("from", ""), j.get("to", "")
            for (fs, ts), rid in CROSS_BIND.items():
                if fs in f and ts in t:
                    if patch_journey(j, {"route_id": rid, "render": "solid"}):
                        stats["cross_bound"] += 1
            for (fs, ts), fix in NODE_FIX.items():
                if fs in f and ts in t:
                    if patch_journey(j, fix):
                        stats["node_fixed"] += 1
        for ph in market.get("phases", []):
            for fr in ph.get("featured_routes", []) or []:
                fl, tl = fr.get("from_label", ""), fr.get("to_label", "")
                for (fs, ts), rid in CROSS_BIND.items():
                    if fs in fl and ts in tl:
                        patch_journey(fr, {"route_id": rid, "render": "solid"})
                for (fs, ts), fix in NODE_FIX.items():
                    if fs in fl and ts in tl:
                        patch_journey(fr, fix)
    partner.setdefault("economics_status", {})["crossborder_bind_at"] = now_iso()
    return stats


def main() -> int:
    stats = None
    for path in PARTNER_PATHS:
        doc = json.loads(path.read_text())
        stats = bind(doc)
        path.write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())