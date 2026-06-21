#!/usr/bin/env python3
"""Roll up partner-page QA + spine parity into a review queue (like authority coverage)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import audit_rules, proposal_class  # noqa: E402
HANDOFF = ROOT / "handoff" / "partner-map-model"
QA_LEDGER = HANDOFF / "partner-page-qa-ledger.json"
SPINE_LEDGER = HANDOFF / "spine-parity-ledger.json"
OUT = HANDOFF / "partner-coverage-review-rollup.json"

GEOMETRY_FLAG_CHECKS = frozenset({
    "featured_geometry_ratio",
    "journey_geometry_ratio",
    "featured_link_ratio",
    "journey_link_ratio",
    "featured_unlinked",
    "journey_unlinked",
})
COSMETIC_FLAG_CHECKS = frozenset({
    "phase_narrative",
    "phase_rationale",
    "phase_featured",
    "narrative",
    "partner_context",
    "network_chip_empty",
})


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> int:
    qa = load(QA_LEDGER)
    spine = load(SPINE_LEDGER) if SPINE_LEDGER.is_file() else None
    spine_by = {r["partner"]: r for r in (spine or {}).get("partners", [])}

    review: dict[str, list] = {
        "authority_reference": [],
        "geometry_gaps": [],
        "spine_parity_fail": [],
        "thin_map": [],
        "tasklet_queue": [],
    }

    partners_pitch = ROOT / "partner-pitch" / "partners"
    qa_pass_with_flags_hospitality = 0
    qa_pass_with_flags_hub_authority = 0
    qa_flags_featured_geometry = 0
    qa_flags_journey_only = 0
    qa_flags_cosmetic = 0
    spine_pass_with_flags = 0

    for r in qa.get("partners", []):
        p = r["partner"]
        c = r.get("counts", {})
        fr, fg = c.get("featured_routes", 0), c.get("featured_geometry_linked", 0)
        mr = c.get("map_routes_in_scope", 0)
        doc_path = partners_pitch / f"{p}.json"
        doc = json.loads(doc_path.read_text()) if doc_path.exists() else {}
        pclass = proposal_class(p, doc)
        rules = audit_rules(p, doc)
        geom_floor = rules.get("featured_geometry_floor", 0.85)

        if p in ("rakta", "bahrain-motc"):
            review["authority_reference"].append({
                "partner": p,
                "verdict": r["verdict"],
                "featured_sealed_geom": f"{fg}/{fr}",
                "map_routes_in_scope": mr,
            })
            continue

        sp = spine_by.get(p, {})
        if sp.get("verdict") == "FAIL":
            review["spine_parity_fail"].append({
                "partner": p,
                "geometry_linked": sp.get("geometry_linked"),
                "card_gaps": sp.get("card_gaps"),
            })

        if fr and fg < fr * geom_floor:
            review["geometry_gaps"].append({
                "partner": p,
                "proposal_class": pclass,
                "featured_geom": f"{fg}/{fr}",
                "journey_geom": f"{c.get('journeys_geometry_linked', 0)}/{c.get('journeys', 0)}",
                "map_routes": mr,
                "verdict": r["verdict"],
            })

        thin_thresh = rules.get("thin_map_threshold", 80)
        if mr < thin_thresh and p not in {
            "maldives-government", "norway-fjords", "thames-clippers",
            "transport-nsw", "hong-kong", "universal-enterprises", "villa-hotels",
        }:
            review["thin_map"].append({"partner": p, "proposal_class": pclass, "map_routes": mr})

        for t in r.get("tasklet_actions", []):
            review["tasklet_queue"].append({"partner": p, "action": t})

        if r.get("verdict") == "PASS_WITH_FLAGS":
            if pclass == "hospitality":
                qa_pass_with_flags_hospitality += 1
            elif pclass in ("hub", "authority"):
                qa_pass_with_flags_hub_authority += 1
            checks = {f.get("check") for f in r.get("flags", [])}
            has_feat = "featured_geometry_ratio" in checks or "featured_unlinked" in checks
            has_journey = bool(checks & {"journey_geometry_ratio", "journey_unlinked"})
            has_cosmetic = bool(checks & COSMETIC_FLAG_CHECKS)
            if has_feat:
                qa_flags_featured_geometry += 1
            elif has_journey and not has_cosmetic:
                qa_flags_journey_only += 1
            elif has_cosmetic and not has_feat and not has_journey:
                qa_flags_cosmetic += 1

        if sp.get("verdict") == "PASS_WITH_FLAGS":
            spine_pass_with_flags += 1

    out = {
        "at": datetime.now(timezone.utc).isoformat(),
        "sources": [str(QA_LEDGER.relative_to(ROOT)), str(SPINE_LEDGER.relative_to(ROOT))],
        "summary": {
            "qa_total": qa.get("summary", {}).get("total"),
            "qa_pass": qa.get("summary", {}).get("pass"),
            "qa_pass_with_flags": qa.get("summary", {}).get("pass_with_flags"),
            "qa_pass_with_flags_hospitality": qa_pass_with_flags_hospitality,
            "qa_pass_with_flags_hub_authority": qa_pass_with_flags_hub_authority,
            "qa_pass_with_flags_hospitality_target": 5,
            "qa_pass_with_flags_featured_geometry": qa_flags_featured_geometry,
            "qa_pass_with_flags_journey_only": qa_flags_journey_only,
            "qa_pass_with_flags_cosmetic": qa_flags_cosmetic,
            "qa_fail": qa.get("summary", {}).get("fail"),
            "geometry_gap_partners": len(review["geometry_gaps"]),
            "spine_pass_with_flags": spine_pass_with_flags,
            "spine_pass_with_flags_target": 10,
            "spine_parity_fail": len(review["spine_parity_fail"]),
            "thin_map": len(review["thin_map"]),
            "tasklet_actions": len(review["tasklet_queue"]),
        },
        "review": review,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())