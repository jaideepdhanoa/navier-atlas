#!/usr/bin/env python3
"""Bind Yango hub growth_case from agg-yango.json rollup (GROK_BIND → real numbers)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bolt_yango_shared import AGG_DIR, INGEST, fmt_usd_millions, load_json, now_iso, save_json

ROOT = Path(__file__).resolve().parents[2]


def build_growth_case(agg: dict, economics_url: str, corridor_count: int) -> dict:
    rollup = agg.get("rollup", {})
    gf = rollup.get("grounded_floor", {})
    et = rollup.get("estimated_total", {})
    n_grounded = rollup.get("n_grounded", 0)
    n_total = rollup.get("n_corridors_total", 0)

    som_floor = float(gf.get("market_rev_yr") or 0)
    som_network = float(et.get("market_rev_yr") or som_floor)
    fleet_floor = int(gf.get("fleet") or 0)
    co2_floor = int(gf.get("co2_saved_t_yr") or 0)

    rev_per_boat = 71250.0
    revs = [
        r["mid"]["revenue_per_boat_yr"]
        for r in agg.get("rows", [])
        if (r.get("mid") or {}).get("revenue_per_boat_yr")
    ]
    if revs:
        rev_per_boat = sum(revs) / len(revs)

    som_capture = 0.10
    mature_capture = 0.25
    induced_demand = 1.8
    journey_gmv_multiple = 3.0
    platform_take_rate = 0.18

    sam_network = som_network * induced_demand * (mature_capture / som_capture)
    marine_tam = sam_network / mature_capture if mature_capture else sam_network * 4.0
    journey_gmv = marine_tam * journey_gmv_multiple
    platform_rev = sam_network * journey_gmv_multiple * platform_take_rate
    capture_pct = int(som_capture * 100)

    def rung(rid, label, whose, basis, low, mid, high, conf):
        return {
            "id": rid,
            "label": label,
            "whose_money": whose,
            "basis": basis,
            "low": low,
            "mid": mid,
            "high": high,
            "display": {
                "low": fmt_usd_millions(low) if low else None,
                "mid": fmt_usd_millions(mid),
                "high": fmt_usd_millions(high) if high else None,
            },
            "confidence": conf,
            "confidence_label": conf.replace("-", " ").title(),
        }

    prove_boats = max(3, min(8, fleet_floor or 3))
    scale_boats = max(prove_boats + 5, min(25, int(prove_boats * 3)))
    mature_boats = max(scale_boats * 3, int(scale_boats * 4.5))

    return {
        "_provenance": {
            "source_growth": "agg-yango.json",
            "source_rollup": "agg-yango.json",
            "rev_per_boat_yr": round(rev_per_boat, 2),
            "greenfield_mode": "census",
            "greenfield_corridors": corridor_count,
            "sourced_corridors": n_grounded,
            "generator": "grok-bind_yango_growth_case.py",
            "bound_at": now_iso(),
        },
        "economics_url": economics_url,
        "revenue_potential": {
            "headline": "The floor and the prize — every rung traces to grounded, sourced demand.",
            "modal_lead": "We start from grounded corridor demand across Yango's Dubai-HQ'd footprint. Each step adds one realistic expansion lever — network width, induced demand, journey wallet, platform take.",
            "anchor_note": (
                f"Anchor: {fmt_usd_millions(som_floor)}/yr Navier transport revenue on "
                f"{n_grounded} grounded corridors ({n_total} modeled in aggregate; "
                f"{corridor_count} in shared registry) — the floor every rung builds from."
            ),
            "whose_money_legend": {
                "navier_transport_revenue": "Fare the Navier boats collect. Corridor P&L (atom.py). SOM/SAM rungs are in this unit.",
                "journey_gmv": "Total spend on the whole journey through Yango: transport + food + stays + experiences + ads.",
                "platform_take": "Yango's own commission revenue on journey_gmv — the number that makes a super-app care.",
            },
            "cite_rule": "Cite MID. 'High' stacks every optimistic assumption — ceiling, not headline.",
            "rungs": [
                rung(
                    "som_floor",
                    "SOM — floor (published)",
                    "Navier transport revenue",
                    f"sourced flagship corridors · 10% capture · {n_grounded} grounded",
                    None,
                    som_floor,
                    None,
                    "grounded",
                ),
                rung(
                    "som_network",
                    f"SOM full network (~{capture_pct}% capture, today, +greenfield)",
                    "Navier transport revenue",
                    f"whole mapped network · {capture_pct}% capture · {corridor_count} corridors",
                    som_network * 0.7,
                    som_network,
                    som_network * 1.3,
                    "med",
                ),
                rung(
                    "sam_network",
                    "SAM matured network — induced demand at scale",
                    "Navier transport revenue",
                    "faster, more comfortable boats grow the market · leading-operator 25% capture, network-wide",
                    sam_network * 0.3,
                    sam_network,
                    sam_network * 2.9,
                    "med-low",
                ),
                rung(
                    "tam_transfer",
                    "Marine mobility TAM — total addressable water-transfer spend",
                    "total water-transfer spend",
                    "SAM divided by leading-operator capture — full inducible water-transfer wallet at maturity",
                    marine_tam * 0.72,
                    marine_tam,
                    marine_tam * 1.39,
                    "med-low",
                ),
                rung(
                    "journey_gmv",
                    "Journey GMV — food, stays, and experiences (~3× TAM)",
                    "total journey wallet",
                    "add food, stays, and experiences to every crossing in the induced market",
                    journey_gmv * 0.48,
                    journey_gmv,
                    journey_gmv * 1.86,
                    "med-low",
                ),
                rung(
                    "platform_rev",
                    "Partner platform revenue on Navier",
                    "partner's P&L on Navier-carried journeys",
                    "platform commission on journey GMV routed through the Navier network (subset of full Journey GMV)",
                    platform_rev * 0.29,
                    platform_rev,
                    platform_rev * 2.96,
                    "med-low",
                ),
            ],
        },
        "phase_economics": {
            "headline": "Revenue potential by phase — conservative floor first, ecosystem prize last.",
            "conversion_note": (
                f"Fleet & CO2 scale from the grounded unit: {prove_boats} boats = "
                f"{fmt_usd_millions(som_floor)} transport rev = {co2_floor} t CO2/yr "
                f"(~{fmt_usd_millions(rev_per_boat)} rev/boat)."
            ),
            "horizons": [
                {
                    "id": "prove",
                    "name": "Prove",
                    "horizon": "Year 1–2",
                    "scope": "UAE home-market flagship + first African lagoon",
                    "capture": "10% (new-entrant floor)",
                    "vessel": "N30 Pioneer II (8 pax, commercial now)",
                    "fleet_boats": prove_boats,
                    "navier_transport_rev_yr": som_floor,
                    "navier_transport_rev_display": fmt_usd_millions(som_floor),
                    "partner_platform_rev_yr": None,
                    "partner_platform_rev_display": "nascent",
                    "co2_saved_t_yr": co2_floor,
                    "confidence": "grounded",
                },
                {
                    "id": "scale",
                    "name": "Scale",
                    "horizon": "Year 2–4",
                    "scope": "8 sub-page anchors + corrected 25-node footprint",
                    "capture": "10% (still conservative)",
                    "vessel": "N30 Pioneer II + N35 Shuttle (12–15 pax, 2027)",
                    "fleet_boats_est": scale_boats,
                    "fleet_boats_band": {"low": max(8, scale_boats - 5), "high": min(25, scale_boats + 5)},
                    "navier_transport_rev_yr": som_network,
                    "navier_transport_rev_display": fmt_usd_millions(som_network),
                    "partner_platform_rev_display": "building",
                    "co2_saved_t_yr": int(co2_floor * (scale_boats / max(prove_boats, 1))),
                    "confidence": "med",
                },
                {
                    "id": "mature",
                    "name": "Mature",
                    "horizon": "Year 4+",
                    "scope": "Induced demand + default-operator capture + in-app journey monetization",
                    "capture": "25% mature share",
                    "vessel": "N35-led mix; Quanta-LR on 75–150nm regional legs (H2 2026+)",
                    "fleet_boats_est_pioneer_equiv": mature_boats,
                    "fleet_note": "Pioneer-equivalent; N35 mix lowers hull count for the same throughput.",
                    "navier_transport_rev_yr": sam_network,
                    "navier_transport_rev_display": fmt_usd_millions(sam_network),
                    "partner_platform_rev_yr": platform_rev,
                    "partner_platform_rev_display": fmt_usd_millions(platform_rev),
                    "partner_platform_rev_on_navier_yr": platform_rev,
                    "partner_platform_rev_on_navier_display": fmt_usd_millions(platform_rev),
                    "marine_mobility_tam_yr": marine_tam,
                    "marine_mobility_tam_display": f"{fmt_usd_millions(marine_tam)} marine TAM",
                    "journey_gmv_yr": journey_gmv,
                    "journey_gmv_display": f"{fmt_usd_millions(journey_gmv)} Journey GMV",
                    "co2_saved_t_yr": int(co2_floor * (mature_boats / max(prove_boats, 1))),
                    "confidence": "med-low (banded)",
                },
            ],
        },
        "vessel_sizing": {
            "headline": "Right vessel for every leg — corridor range picks the hull.",
            "classes": [
                {
                    "class": "N30 Pioneer II",
                    "pax": 8,
                    "range_nm": 70,
                    "status": "commercial now",
                    "role": "Capillary corridors ≤ 70nm. The workhorse of Prove + Scale.",
                    "render": "solid",
                },
                {
                    "class": "N35 Shuttle",
                    "pax": "12–15",
                    "range_nm": 70,
                    "status": "2027",
                    "role": "Doubles throughput per hull on dense corridors.",
                    "render": "solid",
                },
                {
                    "class": "Quanta-LR Hybrid",
                    "pax": "12–15",
                    "range_nm": 700,
                    "status": "H2 2026+",
                    "role": "Regional legs 75–150nm beyond Pioneer range. Held out of near-term numbers.",
                    "render": "amber-dashed",
                },
            ],
            "range_gate_note": "≤ 70nm → Pioneer II (now). 75–150nm → Quanta-LR (roadmap).",
        },
        "marine_mobility_tam": {
            "low": marine_tam * 0.72,
            "mid": marine_tam,
            "high": marine_tam * 1.39,
        },
        "journey_gmv": {
            "low": journey_gmv * 0.48,
            "mid": journey_gmv,
            "high": journey_gmv * 1.86,
        },
        "partner_platform_rev_on_navier": {
            "low": platform_rev * 0.29,
            "mid": platform_rev,
            "high": platform_rev * 2.96,
        },
        "_marine_tam_split_provenance": {
            "date": now_iso(),
            "formula": "marine_mobility_tam = SAM_full_network / mature_capture_rate (LB-110)",
            "field_renames": {
                "tam_gmv": "journey_gmv (LB-111)",
                "partner_platform_rev": "partner_platform_rev_on_navier (LB-113)",
            },
            "ladder_rung_count": 6,
            "rungs_ascending": [
                "som_floor",
                "som_network",
                "sam_network",
                "tam_transfer",
                "journey_gmv",
                "platform_rev",
            ],
        },
        "ladder_transitions": [
            {"from_rung_id": "som_floor", "to_rung_id": "som_network", "lever": "network_width"},
            {"from_rung_id": "som_network", "to_rung_id": "sam_network", "lever": "induced_demand"},
            {"from_rung_id": "sam_network", "to_rung_id": "tam_transfer", "lever": "marine_tam_lens"},
            {"from_rung_id": "tam_transfer", "to_rung_id": "journey_gmv", "lever": "journey_wallet"},
            {"from_rung_id": "journey_gmv", "to_rung_id": "platform_rev", "lever": "platform_take"},
        ],
        "modal_headline": "Yango's water network — from Dubai jetties to African lagoons",
        "modal_lead": (
            "Every rung traces to Yango's own modeled corridors — "
            f"{corridor_count} in the shared registry, {n_grounded} grounded today."
        ),
        "_render_chip_flag": {
            "needs_new_layouts": ["revenue_ladder", "phase_economics_table", "vessel_sizing_cards"],
            "confidence_display": "Tag every banded rung; lead with floor + corridor COUNT.",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--aggdir", default="", help="Directory with agg-yango.json")
    ap.add_argument("--econ-map", default="", help="economics_url_map.json path")
    args = ap.parse_args()

    dc = ROOT / args.dc
    aggdir = Path(args.aggdir) if args.aggdir else AGG_DIR
    opex_ingest = ROOT / "_ingest/sidecar-opex-refresh-2026-06-20"
    if not (aggdir / "agg-yango.json").exists() and opex_ingest.exists():
        aggdir = opex_ingest
    econ_map_path = Path(args.econ_map) if args.econ_map else INGEST / "inputs/economics_url_map.json"
    if not econ_map_path.exists() and opex_ingest.exists():
        econ_map_path = opex_ingest / "economics_url_map.json"

    agg = load_json(aggdir / "agg-yango.json")
    econ_map = load_json(econ_map_path)
    seal_manifest = load_json(INGEST / "inputs/seal-manifest.json")
    economics_url = econ_map.get("economics_url", {}).get("yango", "")
    corridor_count = (
        agg.get("rollup", {}).get("n_corridors_total")
        or seal_manifest.get("partners", {}).get("yango", {}).get("corridor_count", 183)
    )

    growth = build_growth_case(agg, economics_url, corridor_count)

    for tree in (dc, ROOT / "partner-pitch"):
        yango_path = tree / "partners/yango.json"
        if not yango_path.is_file():
            continue
        yango = load_json(yango_path)
        yango["growth_case"] = growth
        yango.pop("_growth_case_pending", None)
        yango["economics_url"] = economics_url
        save_json(yango_path, yango)
        print(f"→ bound growth_case on {yango_path}")


if __name__ == "__main__":
    main()