#!/usr/bin/env python3
"""Cascade economics from economics_by_route_id.json onto sealed partner cards.

For authority + hub partners: when a card has a sealed route_id that exists in the
registry (any authored_for), set model_link, economics_status=cascaded, and provenance
fields. Does not create new economics rows — inherits existing registry only.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import load_classes, proposal_class  # noqa: E402

PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
ECON = ROOT / "data-clean" / "economics_by_route_id.json"
REPORT = ROOT / "handoff" / "partner-map-model" / "economics-cascade-by-route-id-report.json"

TARGET_CLASSES = frozenset({"authority", "hub"})
DEFAULT_SLUGS = [
    "dubai-rta", "abu-dhabi-itc", "qatar", "singapore-mpa",
    "gojek", "line", "didi", "lyft", "kakao-mobility",
    "noon", "careem", "grab", "bolt", "yango", "uber",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_registry() -> dict[str, dict]:
    doc = json.loads(ECON.read_text())
    by_id: dict[str, dict] = {}
    for rec in doc.get("records") or []:
        rid = rec.get("route_id")
        if rid and rid not in by_id:
            by_id[rid] = rec
    return by_id


def iter_cards(doc: dict):
    for j in doc.get("journeys_unlocked") or []:
        if isinstance(j, dict):
            yield j
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, dict):
                yield fr
        for j in ph.get("journeys_unlocked") or []:
            if isinstance(j, dict):
                yield j
    for m in doc.get("markets") or []:
        for j in m.get("journeys_unlocked") or []:
            if isinstance(j, dict):
                yield j
        for ph in m.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, dict):
                    yield fr


def cascade_card(card: dict, registry: dict[str, dict]) -> bool:
    if card.get("economics_status") == "cascaded":
        return False
    if card.get("economics_status") == "roadmap_excluded":
        return False
    if card.get("render") == "roadmap-amber-dashed":
        return False
    rid = card.get("route_id")
    if not rid:
        rids = card.get("route_ids") or []
        rid = next((x for x in rids if x in registry), None)
    if not rid or rid not in registry:
        return False
    rec = registry[rid]
    card["route_id"] = rid
    card["model_link"] = rid
    card["economics_status"] = "cascaded"
    card["_economics_source"] = "economics_by_route_id.json"
    card["_economics_authored_for"] = rec.get("authored_for")
    card["_economics_cascade_at"] = utc_now()
    return True


def process(slug: str, registry: dict[str, dict]) -> dict:
    path = PARTNERS / f"{slug}.json"
    if not path.is_file():
        return {"partner": slug, "skipped": "missing"}
    doc = json.loads(path.read_text())
    pclass = proposal_class(slug, doc)
    if pclass not in TARGET_CLASSES:
        return {"partner": slug, "skipped": f"class={pclass}"}
    cascaded = 0
    for card in iter_cards(doc):
        if cascade_card(card, registry):
            cascaded += 1
    if cascaded:
        doc.setdefault("_economics_cascade", {})["applied_at"] = utc_now()
        doc["_economics_cascade"]["cards"] = cascaded
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        dc = DC / f"{slug}.json"
        if dc.exists():
            dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "proposal_class": pclass, "cascaded": cascaded}


def main() -> int:
    data = load_classes()
    slugs = sys.argv[1:] if len(sys.argv) > 1 else [
        s for s in DEFAULT_SLUGS if data["by_partner"].get(s) in TARGET_CLASSES
    ]
    registry = load_registry()
    results = [process(s, registry) for s in slugs]
    out = {
        "at": utc_now(),
        "lane": "grok/wire_economics_cascade_by_route_id",
        "registry_rows": len(registry),
        "results": results,
        "total_cascaded": sum(r.get("cascaded", 0) for r in results),
    }
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())