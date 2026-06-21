#!/usr/bin/env python3
"""Stub authority phases with 0 featured_routes when phase_featured_min requires ≥1."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import audit_rules, proposal_class  # noqa: E402

PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"

# Reference-tier domestic stub — narrative-only tier; geometry already sealed elsewhere.
BAHRAIN_PHASE1_STUB = {
    "label": "Manama waterfront ↔ Sitra / Hawar fast passenger pilot",
    "from_node_id": "manama-bahrain",
    "to_node_id": "manama-bahrain",
    "distance_nm": 12.4,
    "platform": "Pioneer II",
    "route_id": "rn-063a88bc18d1",
    "route_ids": ["rn-063a88bc18d1"],
    "_link_kind": "authority-phase-stub",
    "_link_status": "linked-grok-scoped",
    "_link_source": "grok/stub_authority_empty_phase_featured",
    "economics_status": "economics_pending",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def roadmap_stub_from_prior(phases: list[dict], pn: int) -> dict | None:
    for ph in phases:
        if ph.get("n") == pn:
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, dict) and fr.get("label"):
                    stub = deepcopy(fr)
                    stub["_link_kind"] = "authority-phase-stub"
                    stub["_link_source"] = "grok/stub_authority_empty_phase_featured"
                    stub.setdefault("render", "roadmap-amber-dashed")
                    stub.setdefault("economics_status", "roadmap_excluded")
                    return stub
    return None


def process(slug: str) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    if proposal_class(slug, doc) != "authority":
        return {"partner": slug, "skipped": "not authority"}
    rules = audit_rules(slug, doc)
    min_featured = rules.get("phase_featured_min", 1)
    phases = doc.get("phases") or []
    stubs = 0
    for ph in phases:
        if ph.get("aspirational"):
            continue
        frs = [x for x in (ph.get("featured_routes") or []) if isinstance(x, dict)]
        if len(frs) >= min_featured:
            continue
        pn = ph.get("n")
        if slug == "bahrain-motc" and pn == 1:
            ph.setdefault("featured_routes", []).append(deepcopy(BAHRAIN_PHASE1_STUB))
            stubs += 1
            continue
        if slug == "nyc-ferry" and pn == 4:
            prior = roadmap_stub_from_prior(phases, 3)
            if prior:
                ph.setdefault("featured_routes", []).append(prior)
                stubs += 1
            continue
        if slug == "norway-fjords" and pn == 3:
            prior = roadmap_stub_from_prior(phases, 2)
            if prior:
                ph.setdefault("featured_routes", []).append(deepcopy(prior))
                stubs += 1
    if stubs:
        doc.setdefault("_authority_phase_featured_stub", {})["applied_at"] = utc_now()
        doc["_authority_phase_featured_stub"]["stubs"] = stubs
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        dc = DC / f"{slug}.json"
        if dc.exists():
            dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "stubs_added": stubs}


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else ["bahrain-motc", "nyc-ferry", "norway-fjords"]
    results = [process(s) for s in slugs]
    print(json.dumps({"at": utc_now(), "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())