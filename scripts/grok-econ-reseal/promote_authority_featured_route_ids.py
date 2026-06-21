#!/usr/bin/env python3
"""Promote archetype gold route_id onto authority phase featured cards with null bind."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import proposal_class  # noqa: E402

ARCHETYPE = ROOT / "handoff" / "partner-map-model" / "public-transit-authority-archetype.json"
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff" / "partner-map-model" / "authority-featured-promote-report.json"

DEFAULT_SLUGS = ["dubai-rta", "abu-dhabi-itc", "qatar"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_gold() -> set[str]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    return {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}


def norm_label(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower().strip())


def archetype_index(archetype: dict, slug: str, gold: set[str]) -> dict[str, dict]:
    cfg = (archetype.get("partners") or {}).get(slug) or {}
    idx: dict[str, dict] = {}
    for specs in (cfg.get("supplement_routes") or {}).values():
        for spec in specs:
            rid = spec.get("route_id")
            if rid and rid in gold:
                key = norm_label(spec.get("label", ""))
                idx[key] = spec
    return idx


def bind_fields(dst: dict, src: dict, gold: set[str]) -> bool:
    rid = src.get("route_id")
    rids = src.get("route_ids") or []
    if not rid and rids:
        rid = next((x for x in rids if x in gold), None)
    if not rid or rid not in gold:
        return False
    dst["route_id"] = rid
    dst["route_ids"] = [rid]
    for k in ("from_node_id", "to_node_id", "distance_nm", "platform"):
        if src.get(k) is not None:
            dst[k] = src[k]
    dst["_link_kind"] = src.get("_link_kind", "authority-featured-promote")
    dst["_link_status"] = "linked-grok-scoped"
    dst["_link_source"] = "grok/promote_authority_featured_route_ids"
    dst.pop("_hold_reason", None)
    dst.setdefault("economics_status", "economics_pending")
    return True


def process(slug: str, archetype: dict, gold: set[str]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    if proposal_class(slug, doc) != "authority":
        return {"partner": slug, "skipped": "not authority"}
    idx = archetype_index(archetype, slug, gold)
    from_archetype = from_route_ids = 0
    for j in doc.get("journeys_unlocked") or []:
        if not isinstance(j, dict) or j.get("route_id") in gold:
            continue
        rids = j.get("route_ids") or []
        rid = next((x for x in rids if x in gold), None)
        if rid and bind_fields(j, {**j, "route_id": rid}, gold):
            from_route_ids += 1

    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if fr.get("route_id") in gold:
                continue
            key = norm_label(fr.get("label", ""))
            spec = idx.get(key)
            if spec and bind_fields(fr, spec, gold):
                from_archetype += 1
                continue
            rids = fr.get("route_ids") or []
            rid = next((x for x in rids if x in gold), None)
            if rid and bind_fields(fr, {**fr, "route_id": rid}, gold):
                from_route_ids += 1
    doc.setdefault("_authority_featured_promote", {})["applied_at"] = utc_now()
    doc["_authority_featured_promote"]["from_archetype"] = from_archetype
    doc["_authority_featured_promote"]["from_route_ids"] = from_route_ids
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {
        "partner": slug,
        "from_archetype": from_archetype,
        "from_route_ids": from_route_ids,
    }


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_SLUGS
    gold = load_gold()
    archetype = json.loads(ARCHETYPE.read_text())
    results = [process(s, archetype, gold) for s in slugs]
    out = {"at": utc_now(), "lane": "grok/promote_authority_featured_route_ids", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())