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

    sam_network = som_network * 4.5 if som_network else som_floor * 4.5
    tam_gmv = sam_network * 12.0
    platform_rev = tam_gmv * 0.045

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
                    "SOM — full network",
                    "Navier transport revenue",
                    f"whole mapped network · 10% capture · {corridor_count} corridors",
                    som_network * 0.7,
                    som_network,
                    som_network * 1.3,
                    "med",
                ),
                rung(
                    "sam_network",
                    "SAM — matured network",
                    "Navier transport revenue",
                    "induced demand + default-operator capture, network-wide",
                    sam_network * 0.3,
                    sam_network,
                    sam_network * 2.9,
                    "med-low",
                ),
                rung(
                    "tam_gmv",
                    "TAM — journey GMV",
                    "total journey wallet",
                    "every cross-water journey in the induced market (all merchants)",
                    tam_gmv * 0.34,
                    tam_gmv,
                    tam_gmv * 2.4,
                    "med-low",
                ),
                rung(
                    "platform_rev",
                    "Partner platform revenue",
                    "partner's own P&L",
                    "platform commission on journey GMV routed through the Navier network",
                    platform_rev * 0.2,
                    platform_rev,
                    platform_rev * 3.8,
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
                    "scope": "Africa + GCC + Türkiye + Egypt network",
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
                    "journey_gmv_display": f"{fmt_usd_millions(tam_gmv)} TAM",
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
        "ladder_transitions": [
            {"from": "som_floor", "to": "som_network", "lever": "network_width"},
            {"from": "som_network", "to": "sam_network", "lever": "induced_demand"},
            {"from": "sam_network", "to": "tam_gmv", "lever": "journey_wallet"},
            {"from": "tam_gmv", "to": "platform_rev", "lever": "platform_take"},
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
    args = ap.parse_args()

    dc = ROOT / args.dc
    agg = load_json(AGG_DIR / "agg-yango.json")
    econ_map = load_json(INGEST / "inputs/economics_url_map.json")
    seal_manifest = load_json(INGEST / "inputs/seal-manifest.json")
    economics_url = econ_map.get("economics_url", {}).get("yango", "")
    corridor_count = seal_manifest.get("partners", {}).get("yango", {}).get("corridor_count", 183)

    growth = build_growth_case(agg, economics_url, corridor_count)

    yango_path = dc / "partners/yango.json"
    yango = load_json(yango_path)
    yango["growth_case"] = growth
    yango.pop("_growth_case_pending", None)
    yango["economics_url"] = economics_url
    save_json(yango_path, yango)
    print(f"→ bound growth_case on {yango_path}")


if __name__ == "__main__":
    main()