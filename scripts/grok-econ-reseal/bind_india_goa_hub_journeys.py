#!/usr/bin/env python3
"""Bind Adani / Reliance Goa unlinked journeys (Grande Island + North/South Goa bundle)."""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff" / "partner-map-model" / "india-goa-hub-bind-report.json"

GOA_GRANDE = {
    "route_id": "rn-8e3cd84b9293",
    "from_node_id": "bp-0d6e4cc1d5",
    "to_node_id": "bp-61a48743ff",
    "distance_nm": 4.3,
    "platform": "Pioneer II",
}

GOA_NORTH_SOUTH_BUNDLE = [
    "ics-894d34e14d",
    "ics-a53a6e7900",
    "ics-b61d127eb2",
    "ics-f8ba590813",
    "ics-d1d96f8e7c",
    "ics-16c8b53ed0",
    "ics-2ada641ba1",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(s: str) -> str:
    return (s or "").strip().lower()


def load_gold() -> set[str]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    return {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}


def is_grande_journey(j: dict) -> bool:
    fr, to = norm(j.get("from")), norm(j.get("to"))
    return "grande" in to or "bat island" in to


def is_north_south_journey(j: dict) -> bool:
    fr, to = norm(j.get("from")), norm(j.get("to"))
    return "north goa" in fr and ("south goa" in to or "palolem" in to or "cavelossim" in to)


def bind_grande(j: dict, gold: set[str]) -> bool:
    if GOA_GRANDE["route_id"] not in gold:
        return False
    j.update(GOA_GRANDE)
    j["route_ids"] = [GOA_GRANDE["route_id"]]
    j["_link_status"] = "linked-grok-scoped"
    j["_link_source"] = "grok/bind_india_goa_hub_journeys"
    j["_link_kind"] = "corridor-label"
    j.pop("_hold_reason", None)
    j.pop("_bind_status", None)
    return True


def bind_north_south(j: dict, gold: set[str]) -> bool:
    rids = [r for r in GOA_NORTH_SOUTH_BUNDLE if r in gold]
    if not rids:
        return False
    j["route_ids"] = rids
    j["route_id"] = rids[0]
    j["_link_status"] = "linked-grok-scoped"
    j["_link_source"] = "grok/bind_india_goa_hub_journeys"
    j["_link_kind"] = "network-bundle"
    j.pop("_hold_reason", None)
    j.pop("_bind_status", None)
    return True


def process_partner(slug: str, gold: set[str]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    grande = north_south = 0
    for market in doc.get("markets") or []:
        if market.get("id") != "goa":
            continue
        for j in market.get("journeys_unlocked") or []:
            if not isinstance(j, dict) or j.get("route_id") in gold:
                continue
            if is_grande_journey(j) and bind_grande(j, gold):
                grande += 1
            elif is_north_south_journey(j) and bind_north_south(j, gold):
                north_south += 1
        for ph in market.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                if not isinstance(fr, dict):
                    continue
                label = norm(fr.get("label", ""))
                if "grande" in label and not fr.get("route_id"):
                    bind_grande(fr, gold)
                elif "north goa" in label and "south goa" in label and not fr.get("route_id"):
                    bind_north_south(fr, gold)
    doc.setdefault("_india_goa_hub_bind", {})["applied_at"] = utc_now()
    doc["_india_goa_hub_bind"]["grande"] = grande
    doc["_india_goa_hub_bind"]["north_south"] = north_south
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "grande_journeys": grande, "north_south_journeys": north_south}


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else ["adani-ports", "reliance-industries"]
    gold = load_gold()
    results = [process_partner(s, gold) for s in slugs]
    out = {"at": utc_now(), "lane": "grok/bind_india_goa_hub_journeys", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())