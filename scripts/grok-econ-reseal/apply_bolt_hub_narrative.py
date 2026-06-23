#!/usr/bin/env python3
"""Refresh Bolt hub-level narrative copy only (PR #86) — no per-market geometry edits."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import load_json, save_json  # noqa: E402

ROSTER = ROOT / "navier/handoff/bolt-hub-narrative-2026-06-23/inputs/bolt-hub-market-roster.json"
REPORT = ROOT / "grok-routing-output/bolt-hub-narrative-refresh-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dc = ROOT / args.dc
    bolt_path = dc / "partners/bolt.json"
    bolt = load_json(bolt_path)
    roster = load_json(ROSTER) if ROSTER.exists() else {}

    total = roster.get("total_subproposals", 22)
    newly = roster.get("newly_added_or_rescoped", [])

    old_stats = bolt.get("network_thesis", {}).get("stats", [])
    new_stats = [
        {"label": "Footprint", "value": "45+ countries", "sub": "Bolt's existing demand base"},
        {"label": "Sub-proposals", "value": str(total), "sub": "water-bound markets across 8 regions"},
        {"label": "Proof", "value": "~100 vessels", "sub": "live Maldives network"},
    ]

    changes = []
    if args.apply:
        nt = bolt.setdefault("network_thesis", {})
        nt["stats"] = new_stats
        nt["coverage_note"] = (
            "Bolt operates in 45+ countries; these sub-proposals are the coastlines where foiling water routes "
            "change the journey most — from the Tallinn triangle to the Gulf, Lagos lagoon, Phuket, Cape Town, "
            "and the East Africa coastal cluster."
        )
        nt["how_to_read"] = (
            "Each market below is a complete phased proposal. The refreshed roster folds in Estonia (Tallinn triangle), "
            "rescoped KSA-commercial (Jeddah + Eastern Province), Thailand, Nigeria, South Africa, and net-new East Africa."
        )
        gc = bolt.setdefault("growth_case", {})
        if isinstance(gc, dict):
            gc["addressable_market_count"] = total
            gc["scale"] = f"{total} sub-proposals · multi-region footprint · 60+ vessels at steady state"
            gc["narrative"] = (
                "Steady state is a Bolt water tier from the Baltic triangle through the Med, Gulf, and African coasts: "
                "book a foiling vessel the same way you book a car."
            )
        bolt["_hub_narrative_refresh"] = {
            "at": utc_now(),
            "source": "navier/handoff/bolt-hub-narrative-2026-06-23",
            "newly_added_or_rescoped": newly,
        }
        save_json(bolt_path, bolt)
        pitch = ROOT / "partner-pitch/partners/bolt.json"
        if pitch.parent.exists():
            save_json(pitch, bolt)

    report = {
        "at": utc_now(),
        "lane": "grok/apply_bolt_hub_narrative",
        "apply": args.apply,
        "hub_only": True,
        "stats_before": old_stats,
        "stats_after": new_stats,
        "newly_added_or_rescoped": newly,
    }
    save_json(REPORT, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())