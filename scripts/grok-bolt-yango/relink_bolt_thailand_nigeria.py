#!/usr/bin/env python3
"""Bind Bolt Thailand journeys to minted Andaman routes (inherit Grab/Phuket geometry)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNER_PATHS = [
    ROOT / "partner-pitch/partners/bolt.json",
    ROOT / "data-clean/partners/bolt.json",
]

# journey `to` substring -> route_id (Pioneer II legs with sealed geometry)
THAILAND_BIND = {
    "Phang Nga": "gcn-f1b2ff834e-shared",
    "Koh Yao": "rn-830bd4d377ca",
    "Phi Phi": "gcn-9ae16d4c34-shared",
    "Krabi": "gcn-e927fe8958-shared",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def match_route(journey: dict) -> str | None:
    to_text = journey.get("to", "")
    for needle, rid in THAILAND_BIND.items():
        if needle in to_text:
            return rid
    return None


def relink(partner: dict) -> dict:
    stats = {"thailand_bound": 0, "thailand_skipped": 0, "thailand_already": 0}
    for market in partner.get("markets", []):
        if market.get("id") != "thailand":
            continue
        for j in market.get("journeys_unlocked", []):
            if j.get("route_id"):
                stats["thailand_already"] += 1
                continue
            if "Koh Samui" in j.get("to", ""):
                j["_link_status"] = "aspirational-quanta-lr"
                j["display"] = "text_only"
                stats["thailand_skipped"] += 1
                continue
            rid = match_route(j)
            if not rid:
                stats["thailand_skipped"] += 1
                continue
            j["route_id"] = rid
            j["_link_status"] = "linked-grok-scoped"
            j["_link_source"] = "grok/bolt_thailand_andaman_relink"
            j["economics_status"] = "bound"
            j.pop("display", None)
            stats["thailand_bound"] += 1
    partner.setdefault("economics_status", {})["bolt_thailand_relink_at"] = now_iso()
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