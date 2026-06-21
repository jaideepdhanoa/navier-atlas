#!/usr/bin/env python3
"""Wave 4 — expand partner map scope by unioning cities from gold routes touching anchor cities."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import audit_rules, proposal_class  # noqa: E402

PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff" / "partner-map-model" / "expand-map-scope-report.json"

THIN_HUBS = ["kakao-mobility", "lyft", "cabify", "freenow", "fullers360"]
HUB_PACK_CITIES = {
    "kakao-mobility": [
        "seoul-incheon-korea", "busan-geoje-korea", "jeju-korea",
        "yeosu-tongyeong-korea",
    ],
    "lyft": ["san-francisco-usa", "los-angeles-usa", "new-york-harbor-usa", "seattle-usa"],
    "cabify": ["madrid-spain", "barcelona-spain", "lisbon-tagus-portugal"],
    "freenow": ["berlin-germany", "hamburg-germany", "munich-germany"],
    "fullers360": ["auckland-new-zealand"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def city_id_of(props: dict) -> str | None:
    return props.get("from_city_id") or props.get("from")


def anchor_cities(doc: dict) -> set[str]:
    cities: set[str] = set()
    for ph in doc.get("phases") or []:
        cities.update(ph.get("cities") or [])
    for m in doc.get("markets") or []:
        cities.update(m.get("anchor_cities") or m.get("cities") or [])
    for j in doc.get("journeys_unlocked") or []:
        for k in ("from_node_id", "to_node_id"):
            v = j.get(k)
            if v and not str(v).startswith("bp-"):
                cities.add(v.split("__")[0] if "__" in str(v) else v)
    return cities


def routes_touching(cities: set[str], routes: list) -> set[str]:
    expanded = set(cities)
    for f in routes:
        p = f.get("properties") or {}
        fr, to = city_id_of(p), p.get("to_city_id") or p.get("to")
        if fr in cities or to in cities:
            if fr:
                expanded.add(fr)
            if to:
                expanded.add(to)
    return expanded


def expand_phases(doc: dict, extra: set[str]) -> int:
    added = 0
    phases = doc.get("phases") or []
    if not phases:
        phases = [{"n": 1, "label": "Phase 1", "cities": [], "featured_routes": []}]
        doc["phases"] = phases
    for ph in phases:
        cur = set(ph.get("cities") or [])
        for c in sorted(extra - cur):
            ph.setdefault("cities", []).append(c)
            added += 1
    return added


def process(slug: str, routes: list) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    rules = audit_rules(slug, doc)
    thresh = rules.get("thin_map_threshold", 80)
    anchors = anchor_cities(doc)
    if slug in HUB_PACK_CITIES:
        anchors.update(HUB_PACK_CITIES[slug])
    expanded = routes_touching(anchors, routes)
    added = expand_phases(doc, expanded)
    doc.setdefault("_map_scope_expand", {})["applied_at"] = utc_now()
    doc["_map_scope_expand"]["cities_added"] = added
    doc["_map_scope_expand"]["city_union"] = sorted(expanded)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "thin_threshold": thresh, "cities_added": added, "city_count": len(expanded)}


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else THIN_HUBS
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    results = [process(s, routes) for s in slugs]
    out = {"at": utc_now(), "lane": "grok/expand_partner_map_scope", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())