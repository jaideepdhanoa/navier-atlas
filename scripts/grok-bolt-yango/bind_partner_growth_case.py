#!/usr/bin/env python3
"""Bind partner hub growth_case from agg-{partner}.json rollup."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bind_yango_growth_case import build_growth_case
from bolt_yango_shared import INGEST, load_json, now_iso, save_json

ROOT = Path(__file__).resolve().parents[2]

PARTNER_META = {
    "bolt": {
        "capture_note": "10%",
        "modal_headline": "Bolt's water network — from the Aegean to the Gulf",
        "modal_lead": (
            "Every rung traces to Bolt's own modeled corridors across Europe and MENA — "
            "captive-aware, starting from grounded transport spend."
        ),
        "corridor_key": "bolt",
    },
    "yango": {
        "capture_note": "11%",
        "modal_headline": "Yango's water network — from Dubai jetties to African lagoons",
        "modal_lead": (
            "Every rung traces to Yango's Dubai-HQ'd footprint — "
            "Egypt, Turkey, Lagos, Pakistan and beyond."
        ),
        "corridor_key": "yango",
    },
    "grab": {
        "capture_note": "11%",
        "modal_headline": "Grab's SEA water mesh — harbour hops to island corridors",
        "modal_lead": (
            "Every rung traces to Grab's de-duplicated SEA registry — "
            "one geography per bucket, no double-counting."
        ),
        "corridor_key": "grab",
    },
}


def patch_partner_growth(growth: dict, partner: str) -> dict:
    meta = PARTNER_META[partner]
    growth["revenue_potential"]["modal_headline"] = meta["modal_headline"]
    growth["revenue_potential"]["modal_lead"] = meta["modal_lead"]
    growth["_provenance"]["generator"] = "grok-bind_partner_growth_case.py"
    growth["_provenance"]["bound_at"] = now_iso()
    growth["_provenance"]["partner"] = partner
    return growth


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", required=True, choices=sorted(PARTNER_META))
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--aggdir", default="")
    ap.add_argument("--econ-map", default="")
    args = ap.parse_args()

    dc = ROOT / args.dc
    aggdir = Path(args.aggdir) if args.aggdir else ROOT / "_ingest/sidecar-opex-refresh-2026-06-20"
    econ_map_path = Path(args.econ_map) if args.econ_map else INGEST / "inputs/economics_url_map.json"
    if not econ_map_path.exists():
        econ_map_path = aggdir / "economics_url_map.json"

    agg = load_json(aggdir / f"agg-{args.partner}.json")
    econ_map = load_json(econ_map_path)
    seal_manifest = load_json(INGEST / "inputs/seal-manifest.json")
    economics_url = econ_map.get("economics_url", {}).get(args.partner, "")
    corridor_count = seal_manifest.get("partners", {}).get(args.partner, {}).get("corridor_count", 0)

    growth = patch_partner_growth(build_growth_case(agg, economics_url, corridor_count), args.partner)

    partner_path = dc / f"partners/{args.partner}.json"
    partner = load_json(partner_path)
    partner["growth_case"] = growth
    partner.pop("_growth_case_pending", None)
    if economics_url:
        partner["economics_url"] = economics_url
    save_json(partner_path, partner)
    print(f"→ bound growth_case on {partner_path}")


if __name__ == "__main__":
    main()