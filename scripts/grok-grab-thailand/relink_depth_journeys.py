#!/usr/bin/env python3
"""Bind upper-Gulf depth route_ids on grab-thailand partner JSON (post-seal handback)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNER_PATHS = [
    ROOT / "partner-pitch/partners/grab-thailand.json",
    ROOT / "data-clean/partners/grab-thailand.json",
]

# (from_node_id, to_node_id) -> route_id from grab-thailand-depth-seal-report.json
DEPTH_BIND = {
    ("bangkok-thailand", "pattaya-thailand"): "rn-dcbcbe8bfb4f",
    ("koh-samet-thailand", "koh-samet-thailand"): "rn-3b647e2d663d",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def relink(partner: dict) -> dict:
    stats = {"bound": 0, "already": 0}
    for market in partner.get("markets", []):
        for j in market.get("journeys_unlocked", []):
            fc, tc = j.get("from_node_id"), j.get("to_node_id")
            rid = DEPTH_BIND.get((fc, tc))
            if not rid:
                continue
            if j.get("route_id") == rid:
                stats["already"] += 1
                continue
            j["route_id"] = rid
            j["_link_status"] = "linked-grok-scoped"
            j["_link_source"] = "grok/grab_thailand_depth_relink"
            j["economics_status"] = "pending-seal"
            j.pop("display", None)
            stats["bound"] += 1
        for mesh in market.get("connected_city_mesh", []) or []:
            fc, tc = mesh.get("from_node_id"), mesh.get("to_node_id")
            rid = DEPTH_BIND.get((fc, tc))
            if rid and not mesh.get("route_id"):
                mesh["route_id"] = rid
                mesh["_link_status"] = "linked-grok-scoped"
                stats["bound"] += 1
    partner.setdefault("economics_status", {})["depth_relink_at"] = now_iso()
    return stats


def main() -> int:
    stats = None
    for path in PARTNER_PATHS:
        doc = json.loads(path.read_text())
        stats = relink(doc)
        path.write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())