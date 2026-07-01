#!/usr/bin/env python3
"""Regenerate PTA growth_case economics from sealed corridors (PTA-ECONOMICS-CONVENTION)."""
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff/partner-map-model"
DC = ROOT / "data-clean"
PP = ROOT / "partner-pitch"

REV_PER_BOAT_YR = 126_000
CO2_PER_BOAT_YR = 68
CAPTURE_FLOOR = 0.10
CAPTURE_MATURE_MID = 0.25
INDUCED_MID = 1.8


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fmt_money(n: float) -> str:
    if n >= 1_000_000:
        return f"${round(n / 1_000_000)}M"
    if n >= 1_000:
        return f"${round(n / 1_000)}K"
    return f"${round(n)}"


def money_band(mid: float, *, low_factor: float = 0.7, high_factor: float = 1.3) -> dict:
    return {
        "low": fmt_money(mid * low_factor),
        "mid": fmt_money(mid),
        "high": fmt_money(mid * high_factor),
    }


def sealed_corridors(slug: str) -> int:
    total = dossier_pairs(slug)
    receipt = HANDOFF / f"PTA-SEAL-RECEIPT-{slug}.json"
    if receipt.is_file():
        r = json.loads(receipt.read_text())
        failed = len(r.get("failed") or [])
        if failed == 0 and total:
            return total
        minted = len(r.get("minted") or [])
        if minted:
            return minted
        return max(0, total - failed)
    return total


def dossier_pairs(slug: str) -> int:
    dossier = HANDOFF / f"PTA-DOSSIER-{slug}.json"
    if not dossier.is_file():
        return 0
    d = json.loads(dossier.read_text())
    pairs = len(d.get("domestic_network", {}).get("domestic_pairs") or [])
    links = len(d.get("regional_links", {}).get("links") or [])
    return pairs + links


def net_zero_label(dossier: dict) -> str:
    pt = dossier.get("policy_targets") or {}
    yr = pt.get("net_zero_year")
    dec = pt.get("decarb_note") or pt.get("vision") or ""
    if yr:
        return f"net-zero {yr}"
    m = re.search(r"20\d{2}", dec)
    return m.group(0) if m else "published decarbonization targets"


def build_public_value(slug: str, dossier: dict, corridors: int, fleet_mature: int) -> dict:
    co2 = CO2_PER_BOAT_YR * max(1, fleet_mature)
    trips = int(corridors * 120 * 250 * CAPTURE_MATURE_MID)  # corridors × daily trips × days × share
    minutes = corridors * 8 * 120  # ~8 min saved × daily riders proxy
    nz = net_zero_label(dossier)
    authority = (dossier.get("authority") or {}).get("display") or slug
    return {
        "headline": "What it returns to the public",
        "note": f"Quantified public-value outputs for {authority}, tied to sealed domestic corridors and {nz}.",
        "metrics": [
            {
                "label": "Emissions avoided",
                "value": f"{co2:,} t CO₂/yr",
                "basis": f"Zero-emission foiling vs diesel/road alternative at mature fleet ({fleet_mature} Pioneer-equiv boats)",
            },
            {
                "label": "Congestion relieved",
                "value": f"{trips:,} peak trips/yr shifted to water",
                "basis": "Conservative share of road/bridge trips moved to the public network",
            },
            {
                "label": "Time saved",
                "value": f"{minutes:,} passenger-minutes/yr",
                "basis": "Faster crossings than congested road or legacy ferry alternatives",
            },
            {
                "label": "Access widened",
                "value": f"{corridors} corridors on the public network",
                "basis": "Islands, waterfront and cross-harbour communities brought onto the authority network",
            },
        ],
        "levers": [
            x.strip()
            for x in [
                dossier.get("interpretation_for_navier") or "",
                (dossier.get("policy_targets") or {}).get("relevance") or "",
            ]
            if x and x.strip()
        ][:3],
        "operating_model": [
            {"label": "Fare integration", "value": "Rides on the authority's existing fare system — set with the authority"},
            {"label": "Operating cost", "value": "Benchmarked against bus/ferry service-hours the authority already runs"},
            {
                "label": "Cost-recovery band",
                "value": "Farebox vs operating cost — agreed with the authority (not fabricated here)",
            },
        ],
        "_grok_regen": "Regenerated from sealed PTA corridors — refine with authority-specific fare data when available.",
    }


def build_growth_case(slug: str, dossier: dict, corridors: int) -> dict:
    floor = REV_PER_BOAT_YR
    network_mid = floor * max(1.0, math.sqrt(corridors / 8.0)) * INDUCED_MID
    mature_mid = network_mid * (CAPTURE_MATURE_MID / CAPTURE_FLOOR)
    fleet_starter = 1
    fleet_network = max(2, min(12, int(math.ceil(corridors / 4))))
    fleet_mature = max(fleet_network, min(30, int(math.ceil(corridors / 2))))

    rungs = [
        {
            "id": "operating_floor",
            "label": "Operating revenue — starter corridors (today's demand)",
            "basis": f"One Pioneer-equiv boat on the busiest sealed corridors ({corridors} mapped).",
            "whose_money": "operating_revenue",
            "display": money_band(floor),
            "confidence": "grounded",
            "confidence_label": "Grounded",
        },
        {
            "id": "operating_network",
            "label": "Operating revenue — full network",
            "basis": "Same conservative ridership, extended across all sealed domestic corridors.",
            "whose_money": "operating_revenue",
            "display": money_band(network_mid),
            "confidence": "med",
            "confidence_label": "Modeled",
        },
        {
            "id": "operating_mature",
            "label": "Operating revenue — mature network",
            "basis": "Better boats grow ridership; a well-run network carries a larger share.",
            "whose_money": "operating_revenue",
            "display": money_band(mature_mid),
            "confidence": "med-low",
            "confidence_label": "Projected",
        },
    ]

    horizons = [
        {
            "id": "starter",
            "name": "Starter service",
            "horizon": "Year 1–2",
            "scope": "Live corridors, foiling-upgraded",
            "capture": f"{int(CAPTURE_FLOOR * 100)}% (new-entrant floor)",
            "vessel": "N30 Pioneer II (8 pax, commercial now)",
            "fleet_boats": fleet_starter,
            "navier_transport_rev_yr": floor,
            "navier_transport_rev_display": fmt_money(floor),
            "co2_saved_t_yr": CO2_PER_BOAT_YR * fleet_starter,
            "confidence": "grounded",
            "confidence_label": "Grounded",
        },
        {
            "id": "network",
            "name": "Full network",
            "horizon": "Year 2–4",
            "scope": "Extended across the authority's sealed domestic network",
            "capture": f"{int(CAPTURE_FLOOR * 100)}% (still conservative)",
            "vessel": "N30 Pioneer II + N35 Shuttle (12–15 pax, 2027) on dense legs",
            "fleet_boats_est": fleet_network,
            "fleet_boats_band": {"low": max(1, fleet_network - 1), "high": fleet_network + 2},
            "navier_transport_rev_yr": network_mid,
            "navier_transport_rev_display": fmt_money(network_mid),
            "co2_saved_t_yr": CO2_PER_BOAT_YR * fleet_network,
            "confidence": "med",
            "confidence_label": "Modeled",
        },
        {
            "id": "mature",
            "name": "Mature network",
            "horizon": "Year 4+",
            "scope": "A well-used network as ridership grows",
            "capture": f"{int(CAPTURE_MATURE_MID * 100)}% mature share",
            "vessel": "N35-led mix; Quanta-LR on 75–150nm regional legs (H2 2026+)",
            "fleet_boats_est_pioneer_equiv": fleet_mature,
            "navier_transport_rev_yr": mature_mid,
            "navier_transport_rev_display": fmt_money(mature_mid),
            "co2_saved_t_yr": CO2_PER_BOAT_YR * fleet_mature,
            "confidence": "med-low (banded)",
            "confidence_label": "Projected",
        },
    ]

    pv = build_public_value(slug, dossier, corridors, fleet_mature)

    return {
        "revenue_potential": {
            "headline": "Operating revenue as the network grows — with the public value set out alongside.",
            "anchor_note": f"Grounded in {corridors} sealed domestic corridors. Operating figures use the PTA public-value convention; fares and cost-recovery are set with the authority.",
            "whose_money_legend": {
                "operating_revenue": "Fare revenue the service collects — the operating P&L for the route network.",
            },
            "rungs": rungs,
        },
        "phase_economics": {
            "headline": "Operating revenue by phase — conservative first, mature last.",
            "conversion_note": "Each vessel delivers public value as well as revenue: zero-emission foiling removes road trips and avoids diesel emissions.",
            "horizons": horizons,
        },
        "public_value": pv,
        "ladder_transitions": [
            {
                "from_rung_id": "operating_floor",
                "to_rung_id": "operating_network",
                "headline": "Same conservative ridership, across the full sealed network",
                "basis": "Hold ridership steady and extend from starter corridors to all mapped domestic pairs.",
                "confidence": "med",
            },
            {
                "from_rung_id": "operating_network",
                "to_rung_id": "operating_mature",
                "headline": "A maturing network as faster boats grow ridership",
                "basis": "Better, quicker boats grow how many people choose the water.",
                "confidence": "med-low",
            },
        ],
        "modal_headline": "What it returns to the public",
        "modal_lead": "Start from corridors the authority already serves. Each maturity stage widens access and deepens public value — emissions avoided, congestion relieved, and time saved — on a fare-integrated operating model set with the authority.",
        "_provenance": {
            "generator": "scripts/pta/regen_pta_economics.py",
            "regenerated_at": utc_now(),
            "sealed_corridors": corridors,
            "rev_per_boat_yr": REV_PER_BOAT_YR,
            "economics_status": "pta_regenerated",
        },
        "_economics_status": "pta_regenerated",
        "_platform_rev_excluded": True,
    }


def apply_partner(path: Path, gc_patch: dict, apply: bool) -> bool:
    if not path.is_file():
        return False
    doc = json.loads(path.read_text())
    gc = doc.setdefault("growth_case", {})
    vessel_sizing = gc.get("vessel_sizing")
    gc.update(gc_patch)
    if vessel_sizing:
        gc["vessel_sizing"] = vessel_sizing
    doc["economics_status"] = "authority_economics_regenerated"
    if apply:
        path.write_text(json.dumps(doc, indent=2) + "\n")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    slugs = []
    if args.all:
        gap = json.loads((HANDOFF / "PTA-PAIR-GAP-TABLE.json").read_text())
        slugs = [r["partner_id"] for r in gap["authorities"]]
    elif args.partner:
        slugs = [args.partner]
    else:
        ap.error("pass --partner or --all")

    report = {"generated_at": utc_now(), "partners": []}
    for slug in slugs:
        dossier_path = HANDOFF / f"PTA-DOSSIER-{slug}.json"
        if not dossier_path.is_file():
            continue
        dossier = json.loads(dossier_path.read_text())
        corridors = sealed_corridors(slug)
        gc_patch = build_growth_case(slug, dossier, corridors)
        for p in (DC / "partners" / f"{slug}.json", PP / "partners" / f"{slug}.json"):
            apply_partner(p, gc_patch, args.apply)
        report["partners"].append({"partner": slug, "corridors": corridors, "floor": REV_PER_BOAT_YR})
        print(f"{'✓' if args.apply else '·'} {slug}: {corridors} corridors → floor {fmt_money(REV_PER_BOAT_YR)}")

    receipt = HANDOFF / "PTA-ECONOMICS-REGEN.json"
    if args.apply:
        receipt.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())