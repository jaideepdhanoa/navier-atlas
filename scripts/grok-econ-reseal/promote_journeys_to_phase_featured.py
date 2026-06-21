#!/usr/bin/env python3
"""Promote top market/hub journeys into hub-phase featured_routes for map UI."""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import proposal_class  # noqa: E402

PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff" / "partner-map-model" / "promote-journeys-to-featured-report.json"

PER_PHASE = 3


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def journey_to_featured(j: dict) -> dict:
    label = f"{j.get('from', '')} ↔ {j.get('to', '')}".strip(" ↔")
    return {
        "label": label,
        "from_node_id": j.get("from_node_id"),
        "to_node_id": j.get("to_node_id"),
        "distance_nm": j.get("distance_nm"),
        "platform": j.get("platform", "Pioneer II"),
        "route_id": j.get("route_id"),
        "route_ids": [j["route_id"]] if j.get("route_id") else None,
        "_link_kind": "promoted-from-journey",
        "_link_status": j.get("_link_status", "linked-grok-scoped"),
        "_link_source": "grok/promote_journeys_to_phase_featured",
        "economics_status": j.get("economics_status", "economics_pending"),
    }


def promote_hub(doc: dict) -> int:
    added = 0
    phases = doc.get("phases") or []
    if not phases:
        return 0
    pool: list[dict] = []
    for m in doc.get("markets") or []:
        for j in m.get("journeys_unlocked") or []:
            if isinstance(j, dict) and j.get("route_id"):
                pool.append(j)
    if not pool:
        for j in doc.get("journeys_unlocked") or []:
            if isinstance(j, dict) and j.get("route_id"):
                pool.append(j)
    pool.sort(key=lambda x: x.get("distance_nm") or 999)
    seen: set[str] = set()
    for ph in phases:
        if ph.get("aspirational"):
            continue
        frs = [fr for fr in (ph.get("featured_routes") or []) if isinstance(fr, dict)]
        existing = {fr.get("route_id") for fr in frs if fr.get("route_id")}
        for j in pool:
            if len(frs) >= PER_PHASE:
                break
            rid = j.get("route_id")
            if not rid or rid in existing or rid in seen:
                continue
            frs.append(journey_to_featured(j))
            seen.add(rid)
            added += 1
        ph["featured_routes"] = frs
    return added


def promote_single(doc: dict) -> int:
    """Fill empty authority/single-layout phases from journeys_unlocked."""
    added = 0
    journeys = [j for j in doc.get("journeys_unlocked") or [] if isinstance(j, dict)]
    if not journeys:
        return 0
    phases = doc.get("phases") or []
    ji = 0
    for ph in phases:
        if ph.get("aspirational"):
            continue
        frs = list(ph.get("featured_routes") or [])
        if frs:
            continue
        while ji < len(journeys) and len(frs) < PER_PHASE:
            frs.append(journey_to_featured(journeys[ji]))
            ji += 1
            added += 1
        ph["featured_routes"] = frs
    return added


def main() -> int:
    targets = sys.argv[1:] if len(sys.argv) > 1 else [
        p.stem for p in PARTNERS.glob("*.json") if p.stem != "_draft"
    ]
    results = {"at": utc_now(), "lane": "grok/promote_journeys_to_phase_featured", "partners": []}
    for slug in targets:
        path = PARTNERS / f"{slug}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        cls = proposal_class(slug, doc)
        if cls == "hub":
            n = promote_hub(doc)
        elif cls in ("authority", "standalone"):
            n = promote_single(doc)
        else:
            n = 0
        if n:
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
            dc = DC / f"{slug}.json"
            if dc.exists():
                dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        results["partners"].append({"partner": slug, "class": cls, "promoted": n})
    REPORT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())