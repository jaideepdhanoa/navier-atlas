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

def _load_batch5_slugs() -> frozenset[str]:
    gap = HANDOFF / "PTA-PAIR-GAP-TABLE.json"
    if not gap.is_file():
        return frozenset()
    rows = json.loads(gap.read_text()).get("authorities") or []
    return frozenset(r["partner_id"] for r in rows if r.get("partner_id"))


# Batch-5 partners: Tasklet owns presentation fields after #150 scrub.
BATCH5_SLUGS = _load_batch5_slugs()

# Phase B/C partners Grok may fully regen (outside batch-5 guardrail).
PHASE_BC_SLUGS = frozenset(
    {
        "bc-ferries",
        "hawaii",
        "fullers360",
        "maldives-government",
        "norway-fjords",
        "kolkata-wbtc",
        "helsinki-hsl",
        # Batch-7 mint-heavy (Tasklet #163–#168)
        "oslo-ruter",
        "amsterdam-gvb",
        "copenhagen-movia",
        "wellington-metlink",
        "rotterdam-mrdh",
        "gothenburg-vasttrafik",
        # Phase D (Batch-8) Wave 1 + Wave 2
        "manila-pasig-ferry",
        "hcmc-saigon-waterbus",
        "rio-ccr-barcas",
        "mersey-ferries",
        "toronto-island-ferry",
        "calmac",
        "seoul-hangang-bus",
    }
)

PRESERVE_GC_KEYS = frozenset(
    {
        "modal_lead",
        "modal_headline",
        "vessel_sizing",
        "ladder_transitions",
    }
)
PRESERVE_PV_KEYS = frozenset({"levers", "operating_model", "headline", "note"})


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


def bound_routes_in_partner(slug: str) -> int:
    seen: set[str] = set()
    for tree in (DC, PP):
        path = tree / "partners" / f"{slug}.json"
        if not path.is_file():
            continue
        doc = json.loads(path.read_text())
        for kind, _pn, item in _iter_route_items(doc):
            rid = item.get("route_id") or ((item.get("route_ids") or [None])[0])
            if rid:
                seen.add(rid)
    return len(seen)


def _iter_route_items(doc: dict):
    for phase in doc.get("phases", []) or []:
        for fr in phase.get("featured_routes", []) or []:
            if isinstance(fr, dict):
                yield "featured", fr
    for j in doc.get("journeys_unlocked", []) or []:
        if isinstance(j, dict):
            yield "journey", j


def dossier_pairs(slug: str) -> int:
    dossier = HANDOFF / f"PTA-DOSSIER-{slug}.json"
    if not dossier.is_file():
        return 0
    d = json.loads(dossier.read_text())
    pending = d.get("pending_pairs") or []
    if pending:
        return len(pending) + len(d.get("sealed_pairs") or [])
    net = d.get("domestic_network", {})
    sealed = net.get("sealed_pairs")
    if sealed:
        return len(sealed)
    pairs = len(net.get("domestic_pairs") or [])
    links = len(d.get("regional_links", {}).get("links") or [])
    return pairs + links


def sealed_corridors(slug: str) -> int:
    receipt = HANDOFF / f"PTA-SEAL-RECEIPT-{slug}.json"
    if receipt.is_file():
        r = json.loads(receipt.read_text())
        failed = len(r.get("failed") or [])
        minted = len(r.get("minted") or [])
        if minted:
            return minted
        total = dossier_pairs(slug)
        if failed == 0 and total:
            return total
        return max(0, total - failed)
    mint_receipt = HANDOFF / f"GEOMETRY-MINT-RECEIPT-{slug}.json"
    if mint_receipt.is_file():
        r = json.loads(mint_receipt.read_text())
        sealed = [s for s in r.get("sealed_routes") or [] if s.get("status") != "existing"]
        if sealed:
            return len(sealed)
        return len(r.get("sealed_routes") or [])
    return dossier_pairs(slug) or bound_routes_in_partner(slug)


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
    auth = dossier.get("authority")
    authority = (auth.get("display") if isinstance(auth, dict) else auth) or slug
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


def merge_growth_case(existing: dict, patch: dict) -> dict:
    """Patch metrics/numbers only — preserve Tasklet presentation on batch-5."""
    out = dict(existing)
    for key, val in patch.items():
        if key in PRESERVE_GC_KEYS and key in existing:
            continue
        if key == "public_value" and isinstance(val, dict):
            pv_old = existing.get("public_value") or {}
            pv_new = dict(val)
            for pk in PRESERVE_PV_KEYS:
                if pk in pv_old:
                    pv_new[pk] = pv_old[pk]
            if pv_old.get("metrics") and isinstance(pv_new.get("metrics"), list):
                # Refresh metric values but keep labels/basis wording when customized.
                old_by_label = {m.get("label"): m for m in pv_old["metrics"] if isinstance(m, dict)}
                merged_metrics = []
                for m in pv_new["metrics"]:
                    lbl = m.get("label")
                    if lbl in old_by_label and old_by_label[lbl].get("basis"):
                        keep = dict(old_by_label[lbl])
                        keep["value"] = m.get("value", keep.get("value"))
                        merged_metrics.append(keep)
                    else:
                        merged_metrics.append(m)
                pv_new["metrics"] = merged_metrics
            out["public_value"] = pv_new
            continue
        if key in ("revenue_potential", "phase_economics") and isinstance(val, dict) and isinstance(existing.get(key), dict):
            sub = dict(existing[key])
            for sk, sv in val.items():
                if sk in ("headline", "anchor_note", "whose_money_legend", "conversion_note") and sk in sub:
                    continue
                sub[sk] = sv
            out[key] = sub
            continue
        out[key] = val
    return out


def apply_partner(path: Path, gc_patch: dict, apply: bool, slug: str, *, full_apply: bool) -> bool:
    if not path.is_file():
        return False
    doc = json.loads(path.read_text())
    gc = doc.setdefault("growth_case", {})
    if full_apply:
        vessel_sizing = gc.get("vessel_sizing")
        gc.clear()
        gc.update(gc_patch)
        if vessel_sizing:
            gc["vessel_sizing"] = vessel_sizing
        doc["archetype"] = "public_transit"
        doc["economics_status"] = "pta_regenerated"
        doc["_economics_status"] = "pta_regenerated"
        if not doc.get("_public_transit_authority"):
            dossier_path = HANDOFF / f"PTA-DOSSIER-{slug}.json"
            home_cities: list[str] = []
            if dossier_path.is_file():
                d = json.loads(dossier_path.read_text())
                auth = d.get("authority")
                anchor = (
                    (auth.get("anchor_city_id") if isinstance(auth, dict) else None)
                    or d.get("city_feature_id")
                )
                if anchor:
                    home_cities = [anchor]
            if not home_cities:
                home_cities = list(doc.get("cities") or doc.get("end_state", {}).get("end_state_cities") or [])[:1]
            doc["_public_transit_authority"] = {
                "archetype_id": "public_transit_authority",
                "applied_at": utc_now(),
                "home_cities": home_cities,
            }
    else:
        doc["growth_case"] = merge_growth_case(gc, gc_patch)
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
        if slug in BATCH5_SLUGS and slug not in PHASE_BC_SLUGS:
            print(f"⊘ {slug}: skipped (batch-5 presentation guard — not Phase B/C)")
            continue
        dossier_path = HANDOFF / f"PTA-DOSSIER-{slug}.json"
        if not dossier_path.is_file():
            continue
        dossier = json.loads(dossier_path.read_text())
        corridors = sealed_corridors(slug)
        gc_patch = build_growth_case(slug, dossier, corridors)
        full_apply = slug in PHASE_BC_SLUGS
        for p in (DC / "partners" / f"{slug}.json", PP / "partners" / f"{slug}.json"):
            apply_partner(p, gc_patch, args.apply, slug, full_apply=full_apply)
        report["partners"].append(
            {"partner": slug, "corridors": corridors, "floor": REV_PER_BOAT_YR, "mode": "full" if full_apply else "metrics_only"}
        )
        print(f"{'✓' if args.apply else '·'} {slug}: {corridors} corridors → floor {fmt_money(REV_PER_BOAT_YR)}")

    receipt = HANDOFF / "PTA-ECONOMICS-REGEN.json"
    if args.apply:
        receipt.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())