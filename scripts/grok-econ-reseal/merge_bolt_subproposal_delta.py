#!/usr/bin/env python3
"""Merge PR #83 bolt subproposal deltas + france-riviera + east-africa stand-up."""
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import load_json, save_json  # noqa: E402

BATCH = ROOT / "navier/handoff/bolt-batch-2026-06-23"
DELTA = BATCH / "inputs/bolt-subproposals-delta.json"
ENRICHED = BATCH / "inputs/subproposals-enriched-2026-06-20.json"
SCOPE_MAP = BATCH / "inputs/bolt-scope-map.json"
RIVIERA = ROOT / "navier/handoff/cote-dazur-debundle/bolt-france-riviera.subproposal.json"
EA_REPORT = ROOT / "grok-routing-output/bolt-east-africa-seal-report.json"
OUT = ROOT / "grok-routing-output/merged-bolt-subproposals-pr81-86.json"
REPORT = ROOT / "grok-routing-output/bolt-subproposal-merge-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def east_africa_subproposal(scope_cities: list[str]) -> dict:
    return {
        "id": "east-africa",
        "slug": "east-africa",
        "label": "East Africa — Kenya coast & Tanzania archipelago",
        "region": "Africa",
        "tier": "A",
        "summary": (
            "Bolt's East African coastal cluster — Mombasa/Diani on the Kenyan coast, Dar es Salaam on the mainland, "
            "and the Zanzibar/Pemba/Mafia archipelago — is a dense ferry-dependent water market where Navier fast-electric "
            "craft shortcut slow diesel crossings. Marquee legs: Dar↔Stone Town (~41nm) and Mombasa↔Diani (~16nm); "
            "first-class KE↔TZ cross-border Mombasa↔Pemba (~54nm)."
        ),
        "anchor_cities": scope_cities,
        "hero": {
            "title": "Bolt × Navier — East Africa coastal cluster",
            "subtitle": "Foil the Kenyan coast and the Zanzibar archipelago, booked in the Bolt app.",
            "what_we_do_together": (
                "A Bolt-branded foiling tier across Kenya's south coast and Tanzania's island gateway — "
                "Dar↔Stone Town, Mombasa↔Diani, and the cross-border Pemba hop."
            ),
        },
        "why_now": (
            "Bolt is Tanzania's fastest-growing rides market (+68% YoY) and is licensed in Zanzibar; "
            "the Kenyan coast (Mombasa, Diani) is live. The water graph is ferry-dependent and underserved by in-app premium craft."
        ),
        "multimodal_fit": "Same Bolt app: car to the jetty, foiling hop, car on arrival — the premium chain on Africa's busiest coastal corridors.",
        "capture_rate": 0.18,
        "journeys_unlocked": [],
        "phases": [],
        "_seal_status": "geometry_sealed_pending_economics_cascade",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    authored = deepcopy(load_json(ENRICHED))
    delta = load_json(DELTA)
    scope_map = load_json(SCOPE_MAP) if SCOPE_MAP.exists() else {}

    changes: list[dict] = []

    # Full narrative + anchor replacements from bolt-subproposals-delta.json
    for market_key, replacement in delta.items():
        if not market_key.startswith("bolt-"):
            continue
        old_anchors = (authored.get(market_key) or {}).get("anchor_cities")
        authored[market_key] = deepcopy(replacement)
        changes.append({
            "market": market_key,
            "action": "replace_from_delta",
            "anchor_cities": replacement.get("anchor_cities"),
            "prior_anchors": old_anchors,
        })

    # france-riviera from de-bundle package
    if RIVIERA.exists():
        riv = load_json(RIVIERA)
        key = "bolt-france-riviera"
        authored[key] = riv
        changes.append({"market": key, "action": "replace_from_cote_dazur_debundle"})

    # east africa stand-up
    scope_cities: list[str] = []
    if EA_REPORT.exists():
        scope_cities = load_json(EA_REPORT).get("scope_city_ids", [])
    roster_scope = [
        "mombasa-kenya", "diani-ukunda-kenya", "dar-es-salaam-tanzania",
        "zanzibar-tanzania", "pemba-tanzania", "mafia-tanzania", "lamu-kenya", "kilifi-kenya",
    ]
    scope_cities = sorted(set(scope_cities or roster_scope))
    authored["bolt-east-africa"] = east_africa_subproposal(scope_cities)
    changes.append({"market": "bolt-east-africa", "action": "net_new_standup", "anchor_cities": scope_cities})

    # apply scope_map view bindings
    for market_key, scope in scope_map.items():
        if market_key in authored and scope.get("scope_city_ids"):
            authored[market_key]["anchor_cities"] = scope["scope_city_ids"]

    out_path = Path(args.out)
    save_json(out_path, authored)

    report = {
        "at": utc_now(),
        "lane": "grok/merge_bolt_subproposal_delta",
        "out": str(out_path.relative_to(ROOT)),
        "markets_total": len([k for k in authored if k.startswith("bolt-")]),
        "new_or_rescoped": [
            "bolt-ksa-commercial", "bolt-estonia", "bolt-thailand", "bolt-nigeria",
            "bolt-south-africa", "bolt-east-africa", "bolt-france-riviera",
        ],
        "changes": changes,
    }
    save_json(REPORT, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())