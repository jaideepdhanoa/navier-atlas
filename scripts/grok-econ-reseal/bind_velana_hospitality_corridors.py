#!/usr/bin/env python3
"""Bind Velana→resort e__velana__* gold routes onto hospitality partner cards."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff" / "partner-map-model" / "velana-hospitality-bind-report.json"

# Partner → primary Velana airport-to-resort leg (property-specific mint)
VELANA_BY_PARTNER: dict[str, str] = {
    "constance": "e__velana__constance-halaveli-jetty",
    "crown-champa": "e__velana__kuredu-jetty",
    "sun-siyam": "e__velana__iru-fushi-jetty",
    "villa-hotels": "e__velana__sun-island-jetty",
    "universal-enterprises": "e__velana__kurumba-jetty",
    "maldives": "e__velana__kurumba-jetty",
    "four-seasons": "e__velana__ritz-fari-jetty",
    "aman": "e__velana__patina-fari-jetty",
    "six-senses": "e__velana__six-senses-laamu-jetty",
    "soneva": "e__velana__soneva-fushi-jetty",
    "jih-global": "e__velana__kurumba-jetty",
}

VELANA_JOURNEY_KEYS = (
    ("velana international airport (malé)", "north & south malé atoll resorts"),
    ("velana international airport", "greater malé / hulhumalé urban waterfront"),
    ("velana international", "north & south malé atoll resorts"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower().strip())


def load_gold_props() -> tuple[set[str], dict[str, dict]]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    gold: set[str] = set()
    props: dict[str, dict] = {}
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id")
        if rid:
            gold.add(rid)
            props[rid] = p
    return gold, props


def journey_key(item: dict) -> tuple[str, str] | None:
    fr, to = norm(item.get("from", "")), norm(item.get("to", ""))
    for a, b in VELANA_JOURNEY_KEYS:
        if a in fr and b in to:
            return (a, b)
    if "velana" in fr and ("malé" in to or "male" in to or "resort" in to):
        return (fr[:40], to[:40])
    return None


def bind_item(item: dict, rid: str, route_props: dict, gold: set[str]) -> bool:
    if rid not in gold:
        return False
    p = route_props.get(rid, {})
    item["route_id"] = rid
    item["route_ids"] = [rid]
    if p.get("distance_nm") is not None:
        item["distance_nm"] = p["distance_nm"]
    if p.get("from"):
        item["from_node_id"] = p["from"]
    if p.get("to"):
        item["to_node_id"] = p["to"]
    item["_link_kind"] = "velana-resort"
    item["_link_status"] = "linked-grok-scoped"
    item["_link_source"] = "grok/bind_velana_hospitality_corridors"
    item.pop("_hold_reason", None)
    item.setdefault("economics_status", "economics_pending")
    return True


def bind_partner(slug: str, gold: set[str], route_props: dict[str, dict]) -> dict:
    rid = VELANA_BY_PARTNER.get(slug)
    if not rid:
        return {"partner": slug, "skipped": "no velana mapping"}
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    bound_j = bound_f = 0

    for j in doc.get("journeys_unlocked") or []:
        if not isinstance(j, dict) or not journey_key(j):
            continue
        if bind_item(j, rid, route_props, gold):
            bound_j += 1

    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if not isinstance(fr, dict):
                continue
            label = norm(fr.get("label", ""))
            if "velana" not in label:
                continue
            if bind_item(fr, rid, route_props, gold):
                bound_f += 1

    doc.setdefault("_velana_hospitality_bind", {})["applied_at"] = utc_now()
    doc["_velana_hospitality_bind"]["route_id"] = rid
    doc["_velana_hospitality_bind"]["journeys"] = bound_j
    doc["_velana_hospitality_bind"]["featured"] = bound_f
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "route_id": rid, "journeys_bound": bound_j, "featured_bound": bound_f}


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else list(VELANA_BY_PARTNER)
    gold, route_props = load_gold_props()
    results = [bind_partner(s, gold, route_props) for s in slugs]
    out = {"at": utc_now(), "lane": "grok/bind_velana_hospitality_corridors", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())