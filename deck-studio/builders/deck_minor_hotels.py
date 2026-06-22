#!/usr/bin/env python3
"""Minor Hotels operator-developer deck builder (captive economics, WIDTH KPIs)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "builders"
sys.path.insert(0, str(BUILDERS))

from deck_bolt_pilot import load_json, utc_now, write_json  # noqa: E402

DECK = "minor-hotels"
KPI_PATH = ROOT / "decks/minor-hotels/slide3-kpis-minor-hotels.json"
BINDING_PATH = ROOT / "decks/minor-hotels/economics-binding.json"
AGG_PATH = ROOT.parent / "finance/recal/agg-minor-hotels.json"
GROWTH_PATH = ROOT.parent / "finance/recal/growth-minor-hotels.json"
PARTNER_PATH = ROOT.parent / "partner-pitch/partners/minor-hotels.json"


def build_editplan_stub() -> dict:
    """Emit deterministic editplan stub for Slides API apply (full apply needs live deck copy)."""
    kpi = load_json(KPI_PATH)
    binding = load_json(BINDING_PATH)
    partner = load_json(PARTNER_PATH)
    width = kpi["slide3_width_kpis"]
    return {
        "deck_key": DECK,
        "presentation_id": "pending-grok-create-or-bind",
        "mode": "slides_api_batch_update",
        "archetype_variant": "operator-developer",
        "request_summary": (
            "Minor Hotels: captive thesis slide 2 (KPI-free), slide 3 WIDTH KPIs, "
            "3 grounded cluster slides, 3 flagship econ slides, 13 cluster WIDTH slides, TAM captive frame"
        ),
        "safety": {
            "no_pptx_roundtrip": True,
            "no_full_deck_replace": True,
            "preserve_object_ids": True,
            "human_review_required_for_external_send": True,
        },
        "slide_overrides": {
            "slide_2": {
                "frame": "Why a hotel operator now — Captive · Calm · Clean · Continuity",
                "kpi_free": True,
                "headline": partner.get("network_thesis", {}).get("headline"),
            },
            "slide_3": {
                "frame": "Portfolio WIDTH KPIs",
                "cards": width,
            },
            "slide_10": {
                "frame": "Captive LB-254 ladder — headroom = WIDTH not capture share",
                "tam": kpi["slide10_tam"],
            },
        },
        "flagship_econ_slides": binding["flagship_econ_slides"],
        "qa": {
            "leak_denylist": binding["leak_denylist"],
            "G1_archetype_purity": 0,
        },
        "qa_gates": ["drift_gate", "leak_scan", "render_export", "G1_archetype_purity"],
        "operations": [],
        "created_at": utc_now(),
        "_note": "Run copy_gold_deck + apply_plan after sourcing Minor Hotels logo",
    }


def main() -> int:
    plan = build_editplan_stub()
    out = ROOT / f"decks/{DECK}/deck.editplan.json"
    write_json(out, plan)
    print(json.dumps({
        "deck": DECK,
        "editplan": str(out),
        "flagship_slides": len(plan["flagship_econ_slides"]),
        "partner_logo": "needs_sourcing",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())