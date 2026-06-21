#!/usr/bin/env python3
"""Audit RAKTA / Bahrain MOTC: featured-card seal vs full Gulf spine coverage."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff" / "partner-map-model"
PARTNERS = ROOT / "partner-pitch" / "partners"
OUT = HANDOFF / "authority-coverage-report.json"


def load(path: Path):
    return json.loads(path.read_text())


def featured_with_spine(doc: dict) -> list[dict]:
    out = []
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if fr.get("_spine_corridor_id"):
                out.append({**fr, "_phase": ph.get("n")})
    return out


def main() -> int:
    report = {"at": datetime.now(timezone.utc).isoformat(), "partners": {}}
    specs = {
        "rakta": {
            "seal_ledger": HANDOFF / "rakta-route-seal-ledger-2026-06-21.json",
            "grok_ledger": HANDOFF / "rakta-grok-seal-ledger.json",
            "qa": HANDOFF / "partner-page-qa-rakta.json",
        },
        "bahrain-motc": {
            "seal_ledger": HANDOFF / "bahrain-motc-route-seal-ledger-2026-06-21.json",
            "grok_ledger": HANDOFF / "bahrain-motc-grok-seal-ledger.json",
            "qa": HANDOFF / "partner-page-qa-bahrain-motc.json",
        },
    }
    for slug, paths in specs.items():
        doc = load(PARTNERS / f"{slug}.json")
        seal = load(paths["seal_ledger"])
        grok = load(paths["grok_ledger"])
        qa = load(paths["qa"]) if paths["qa"].exists() else {}
        featured = featured_with_spine(doc)
        spine_rows = seal.get("routes") or []
        sealed_cards = [f for f in featured if f.get("route_id")]
        held_cards = [f for f in featured if not f.get("route_id")]
        report["partners"][slug] = {
            "interpretation": (
                "Fastlane sealed/held counts apply to featured_routes cards in partner JSON only — "
                "not the full Tasklet spine ledger."
            ),
            "featured_cards_with_spine_id": len(featured),
            "featured_cards_sealed_route_id": len(sealed_cards),
            "featured_cards_held_null": len(held_cards),
            "fastlane_summary": grok.get("summary"),
            "spine_geometry_present_total": seal.get("summary", {}).get(
                "total_geometry_present_spine_rows"
            ),
            "spine_by_classification": seal.get("summary", {}).get("by_classification"),
            "spine_sealable_domestic": sum(
                v for k, v in (seal.get("summary", {}).get("by_classification") or {}).items()
                if k.startswith("proposal_active")
            ),
            "spine_not_in_partner_json": max(
                0,
                (seal.get("summary", {}).get("total_geometry_present_spine_rows") or 0)
                - len(featured),
            ),
            "qa_map_routes_in_scope": qa.get("counts", {}).get("map_routes_in_scope"),
            "qa_featured_geometry_linked": qa.get("counts", {}).get("featured_geometry_linked"),
            "verdict": (
                "ROBUST_MAP_THIN_PROPOSAL_CARDS"
                if (qa.get("counts", {}).get("map_routes_in_scope") or 0) > 500
                else "THIN"
            ),
        }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())