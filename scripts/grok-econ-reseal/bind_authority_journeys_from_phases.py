#!/usr/bin/env python3
"""Wave 2 — bind authority journeys + featured from archetype supplements and phase cards."""
from __future__ import annotations

import copy
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
REPORT = ROOT / "handoff" / "partner-map-model" / "authority-journey-bind-report.json"

DEFAULT_SLUGS = [
    "dubai-rta", "abu-dhabi-itc", "singapore-mpa", "hong-kong",
    "transport-nsw", "thames-clippers",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_gold() -> set[str]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    return {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower().strip())


def norm_tokens(*parts: str) -> set[str]:
    blob = " ".join(p for p in parts if p).lower()
    for ch in ("↔", "—", "–", "/", "(", ")", ",", "&"):
        blob = blob.replace(ch, " ")
    return {t for t in blob.split() if len(t) > 2}


def overlap(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


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
    dst["_link_kind"] = src.get("_link_kind", "authority-phase-sync")
    dst["_link_status"] = "linked-grok-scoped"
    dst["_link_source"] = "grok/bind_authority_journeys_from_phases"
    dst.pop("_hold_reason", None)
    dst.setdefault("economics_status", "economics_pending")
    return True


def archetype_label_index(archetype: dict, slug: str, gold: set[str]) -> dict[str, dict]:
    cfg = (archetype.get("partners") or {}).get(slug) or {}
    idx: dict[str, dict] = {}
    for tier_specs in (cfg.get("supplement_routes") or {}).values():
        for spec in tier_specs:
            rid = spec.get("route_id")
            if rid and rid in gold:
                key = re.sub(r"\s+", " ", (spec.get("label") or "").lower().strip())
                idx[key] = spec
    return idx


def promote_route_ids_on_featured(doc: dict, gold: set[str]) -> int:
    n = 0
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if fr.get("route_id") in gold:
                continue
            rids = fr.get("route_ids") or []
            rid = next((x for x in rids if x in gold), None)
            if rid:
                bind_fields(fr, {**fr, "route_id": rid}, gold)
                n += 1
    return n


def apply_archetype_supplements(doc: dict, slug: str, archetype: dict, gold: set[str]) -> int:
    idx = archetype_label_index(archetype, slug, gold)
    n = 0
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            key = re.sub(r"\s+", " ", (fr.get("label") or "").lower().strip())
            spec = idx.get(key)
            if spec and bind_fields(fr, spec, gold):
                n += 1
    return n


def sync_journeys(doc: dict, gold: set[str]) -> int:
    pool: list[dict] = []
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            rid = fr.get("route_id") or next((x for x in (fr.get("route_ids") or []) if x in gold), None)
            if rid in gold:
                pool.append({**fr, "route_id": rid})
    if not pool:
        return 0
    bound = 0
    for j in doc.get("journeys_unlocked") or []:
        if j.get("route_id") in gold:
            continue
        jt = norm_tokens(j.get("from", ""), j.get("to", ""))
        best = None
        best_score = 0.25
        for fr in pool:
            lt = norm_tokens(fr.get("label", ""))
            ft = norm_tokens(fr.get("from_label", ""), fr.get("to_label", ""))
            score = max(overlap(jt, lt), overlap(jt, ft))
            if fr.get("from_node_id") == j.get("from_node_id") and fr.get("to_node_id") == j.get("to_node_id"):
                score = max(score, 0.85)
            for a, b in ((j.get("from", ""), j.get("to", "")),):
                for part in (a, b):
                    if part and norm(part)[:12] in norm(fr.get("label", "")):
                        score = max(score, 0.5)
            if score > best_score:
                best_score = score
                best = fr
        if best and bind_fields(j, best, gold):
            bound += 1
    return bound


def process(slug: str, archetype: dict, gold: set[str]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    if proposal_class(slug, doc) != "authority":
        return {"partner": slug, "skipped": "not authority"}
    featured = apply_archetype_supplements(doc, slug, archetype, gold)
    promoted = promote_route_ids_on_featured(doc, gold)
    journeys = sync_journeys(doc, gold)
    doc.setdefault("_authority_journey_bind", {})["applied_at"] = utc_now()
    doc["_authority_journey_bind"]["featured_from_archetype"] = featured
    doc["_authority_journey_bind"]["featured_promoted_route_ids"] = promoted
    doc["_authority_journey_bind"]["journeys_synced"] = journeys
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "featured_archetype": featured, "featured_promoted": promoted, "journeys": journeys}


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_SLUGS
    gold = load_gold()
    archetype = json.loads(ARCHETYPE.read_text())
    results = [process(s, archetype, gold) for s in slugs]
    out = {"at": utc_now(), "lane": "grok/bind_authority_journeys_from_phases", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())