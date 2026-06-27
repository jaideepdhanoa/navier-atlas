#!/usr/bin/env python3
"""
GROWTH -> FRONT-END BLOCK generator.

Reads a partner's growth-case JSON + aggregate rollup and emits a front-end-ready
`growth_case` block for the Atlas partner page (content lane, NOT geometry/gold).

Three render-ready sub-blocks:
  1. revenue_potential  -> the floor-and-prize ladder (banded, MID headline, whose-money legend)
  2. phase_economics    -> 3 economic horizons (Prove / Scale / Mature) wired to fleet+rev+CO2+vessel
  3. vessel_sizing      -> N30 / N35 / Quanta-LR mapped to corridor range + phase role

Nothing hardcoded: all magnitudes derive from the input JSONs + one conversion key
(transport rev per boat) read from the grounded floor.

Usage:
  python3 growth_frontend_block.py --partner grab \
      --growth ../grab-growth-case.json --rollup ../grab-aggregate-results.json \
      --out ../../partner-pitch/partners/_growth-draft/grab.growth.json
"""
import json, argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(HERE)
sys.path.insert(0, FIN)
from partner_platform_rev import shows_platform_revenue, strip_frontend_block  # noqa: E402

def band(d):
    if isinstance(d, dict):
        return {"low": d.get("low"), "mid": d.get("mid"), "high": d.get("high")}
    return {"low": None, "mid": d, "high": None}

def m(x):  # -> "$Xm" / "$X.Yb" display
    # One decimal below $10M so a grounded floor never rounds UP across a whole-million
    # boundary (e.g. $1.54M -> "$1.5M", not "$2M"); whole millions / $B at/above $10M.
    if x is None: return None
    if x >= 1e9: return f"${x/1e9:,.2f}B"
    v = x / 1e6
    return f"${v:,.1f}M" if abs(v) < 10 else f"${v:,.0f}M"

def boats(rev, key):
    if rev is None or not key: return None
    return round(rev / key)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", required=True)
    ap.add_argument("--growth", required=True)
    ap.add_argument("--rollup", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--partner-json", default=None, help="partner proposal JSON (archetype gate for platform rev)")
    a = ap.parse_args()

    show_plat = True
    if a.partner_json:
        pp = json.load(open(a.partner_json))
        show_plat = shows_platform_revenue(pp)

    gc = json.load(open(a.growth)); P = gc["parameters_used"]; gf = gc["greenfield"]
    rl = json.load(open(a.rollup))["rollup"]
    anchor = gc.get("_headline_anchor", "grounded")
    G = gc.get(anchor) or gc["grounded"]
    if anchor == "forward_sam":
        floor_fleet = rl["forward_sam"]["fleet"]
        floor_rev   = rl["forward_sam"]["market_rev_yr"]
        floor_co2   = rl["forward_sam"]["co2_saved_t_yr"]
    elif anchor == "estimated_total":
        floor_fleet = rl["estimated_total"]["fleet"]
        floor_rev   = rl["estimated_total"]["market_rev_yr"]
        floor_co2   = (rl["grounded_floor"]["co2_saved_t_yr"]
                       + (rl.get("estimated_upside", {}).get("co2_saved_t_yr") or 0))
    else:
        floor_fleet = rl["grounded_floor"]["fleet"]
        floor_rev   = rl["grounded_floor"]["market_rev_yr"]
        floor_co2   = rl["grounded_floor"]["co2_saved_t_yr"]
    # LB-254: capture that ACTUALLY built the floor (eff) + captive-aware mature band (both emitted
    # per-anchor by growth.py). Replaces hardcoded contested 10%/25% display copy.
    eff_cap = G.get("_eff_capture_floor") or 0.10
    cmat = (G.get("_mature_capture_used") or P.get("mature_capture_rate_config_band") or {"mid": 0.25})
    cmat_mid = cmat["mid"]
    is_captive = bool(G.get("_is_captive"))
    cappct = f"{eff_cap:.0%}"; maturepct = f"{cmat_mid:.0%}"
    REVPERBOAT  = (floor_rev / floor_fleet if floor_fleet else None)  # conversion key (~$257K)
    if REVPERBOAT is None and G.get("SOM_floor_navier_transport_rev_yr"):
        _sam_fleet = rl.get("forward_sam", {}).get("fleet") or rl["estimated_total"].get("fleet") or 1
        REVPERBOAT = G["SOM_floor_navier_transport_rev_yr"] / _sam_fleet
    CO2PERREV   = (floor_co2 / floor_rev if floor_rev else 0)       # CO2 t per $ transport rev

    def co2(rev):
        return None if rev is None else round(rev * CO2PERREV)

    # LB-256: Quanta-LR / forward-SAM-only partners (no Pioneer-II near-term floor yet).
    forward_only = bool(
        gc.get("_forward_sam_only")
        or G.get("_forward_sam_only")
        or G.get("SOM_full_network_navier_transport_rev_yr") is None
    )
    roadmap = (rl.get("roadmap_quanta_lr_2026plus") or {})
    if forward_only:
        n_roadmap = roadmap.get("n_corridors") or len(roadmap.get("corridors") or [])
        block = {
            "_provenance": {
                "source_growth": os.path.basename(a.growth),
                "source_rollup": os.path.basename(a.rollup),
                "generator": "growth_frontend_block.py",
                "forward_sam_only": True,
                "headline_anchor": anchor,
                "roadmap_quanta_lr_corridors": n_roadmap,
            },
            "revenue_potential": {
                "headline": "Forward-SAM network — Quanta-LR corridors held until H2 2026+ economics lock.",
                "modal_lead": (
                    "Near-term Pioneer-II floor is null (null-beats-guess). "
                    "Mapped inter-island / long-haul corridors sit in the Quanta-LR roadmap bucket."
                ),
                "anchor_note": (
                    f"{n_roadmap} corridor(s) mapped beyond 70 nm Pioneer range — "
                    "economics held for Quanta-LR hybrid (H2 2026+)."
                ),
                "whose_money_legend": gc.get("_whose_money_legend", {}),
                "cite_rule": "No headline until a near-term floor is sourced or forward-SAM demand is published.",
                "rungs": [],
            },
            "phase_economics": {
                "headline": "Phased rollout — prove on sheltered Pioneer legs, scale on Quanta-LR line-hauls.",
                "conversion_note": "Fleet & revenue conversion deferred until first near-term corridor is grounded.",
                "horizons": [
                    {
                        "id": "prove", "name": "Prove", "horizon": "Year 1–2",
                        "scope": "Sheltered ≤70 nm Pioneer-II beachhead (if sourced)",
                        "capture": "10% new-entrant floor",
                        "vessel": "N30 Pioneer II (8 pax, commercial now)",
                        "fleet_boats": floor_fleet or 0,
                        "navier_transport_rev_yr": floor_rev, "navier_transport_rev_display": m(floor_rev) if floor_rev else "—",
                        "co2_saved_t_yr": round(floor_co2) if floor_co2 else 0,
                        "confidence": "held",
                        "confidence_label": "Held",
                    },
                    {
                        "id": "scale", "name": "Scale", "horizon": "Year 2–4",
                        "scope": f"Quanta-LR roadmap — {n_roadmap} long-haul corridor(s) mapped",
                        "capture": "forward-SAM",
                        "vessel": "Quanta-LR Hybrid (12–15 pax, H2 2026+)",
                        "fleet_boats_est": None,
                        "navier_transport_rev_yr": None, "navier_transport_rev_display": "roadmap",
                        "co2_saved_t_yr": None,
                        "confidence": "med-low",
                        "confidence_label": "Roadmap",
                    },
                ],
            },
            "vessel_sizing": {
                "headline": "Quanta-LR owns the long-haul network; Pioneer-II proves sheltered legs.",
                "classes": [
                    {"class": "N30 Pioneer II", "pax": 8, "range_nm": 70, "status": "commercial now",
                     "role": "Sheltered channels ≤70 nm — beachhead only.", "render": "solid"},
                    {"class": "Quanta-LR Hybrid", "pax": "12–15", "range_nm": 700, "status": "H2 2026+",
                     "role": "Inter-island / regional line-hauls beyond Pioneer range — headline fleet class.",
                     "render": "amber-dashed"},
                ],
                "range_gate_note": "Long legs never faked on a 70 nm boat. Roadmap corridors listed in aggregate rollup.",
            },
            "_render_chip_flag": {
                "needs_new_layouts": ["forward_sam_roadmap_banner", "vessel_sizing_cards"],
                "confidence_display": "Lead with roadmap corridor count; do not invent a floor.",
            },
        }
        if roadmap.get("corridors"):
            block["roadmap_quanta_lr_2026plus"] = roadmap
        strip_frontend_block(block)
        os.makedirs(os.path.dirname(a.out), exist_ok=True)
        json.dump(block, open(a.out, "w"), indent=1, ensure_ascii=False)
        print("wrote", a.out, "(forward_sam_only)")
        return

    # ---- 1. revenue_potential ladder (LB-110/111/113 — 6 rungs ascending) ----
    # Order: SOM floor -> SOM network -> SAM network -> TAM transfer (NEW) -> Journey GMV (renamed) -> Platform Rev on Navier
    rungs = [
        ("som_floor",     f"SOM floor (published) \u2014 sourced corridors today", "Navier transport revenue",
         f"sourced flagship corridors \u00b7 {cappct} capture \u00b7 today's demand",
         band(G["SOM_floor_navier_transport_rev_yr"]), "grounded"),
        ("som_network",   f"SOM full network (~{cappct} capture, today, +greenfield)", "Navier transport revenue",
         f"whole mapped network \u00b7 {cappct} capture \u00b7 today's demand (no growth assumed)",
         band(G["SOM_full_network_navier_transport_rev_yr"]), "med"),
        ("sam_network",   "SAM matured network \u2014 induced demand at scale", "Navier transport revenue",
         (f"faster, more comfortable boats grow the market (induced demand); we already capture ~{cappct} \u2014 growth is demand + width, not a capture ramp"
          if is_captive else
          f"faster, more comfortable boats grow the market \u00b7 leading-operator {maturepct} capture, network-wide"),
         band(G["SAM_navier_transport_rev_yr"]), "med-low"),
        ("tam_transfer",  "Marine mobility TAM \u2014 total addressable water-transfer spend", "total water-transfer spend",
         "SAM divided by leading-operator capture \u2014 the full inducible water-transfer wallet at network maturity",
         band(G["marine_mobility_tam_yr"]), "med-low"),
        ("journey_gmv",   "Journey GMV \u2014 food, stays, and experiences (~3\u00d7 TAM)", "total journey wallet",
         "add food, stays, and experiences to every crossing in the induced market",
         band(G["journey_gmv_yr"]), "med-low"),
    ]
    if show_plat:
        rungs.append(
            ("platform_rev",  "Partner platform revenue on Navier", "partner's P&L on Navier-carried journeys",
             "platform commission on journey GMV routed through the Navier network (subset of full Journey GMV)",
             band(G["partner_platform_rev_on_navier_yr"]), "med-low"),
        )
    revenue_potential = {
        "headline": "The floor and the prize \u2014 every rung traces to grounded, sourced demand.",
        "modal_lead": (
            "We start from grounded corridor demand. Each step adds one realistic expansion "
            "lever \u2014 network width, induced demand, journey wallet"
            + (", platform take." if show_plat else ".")
        ),
        "anchor_note": (f"{m(G['M_today_transport_spend_yr'])}/yr premium sea-transfer spend on sourced corridors today "
                        "\u2014 the anchor every rung builds from."),
        "whose_money_legend": gc.get("_whose_money_legend", {}),
        "cite_rule": "Cite MID. 'High' stacks every optimistic assumption \u2014 ceiling, not headline.",
        "rungs": [
            {"id": rid, "label": lbl, "whose_money": wm, "basis": basis,
             "low": bd["low"], "mid": bd["mid"], "high": bd["high"],
             "display": {"low": m(bd["low"]), "mid": m(bd["mid"]), "high": m(bd["high"])},
             "confidence": conf,
             # ζ3 (LB-122): human-readable confidence label
             "confidence_label": {"grounded": "Grounded", "med": "Modeled",
                                  "med-low": "Projected", "med-low (banded)": "Projected"}.get(conf, "Projected")}
            for rid, lbl, wm, basis, bd, conf in rungs
        ],
    }
    if show_plat:
        revenue_potential["ceiling_sibling"] = {
            "id": "platform_rev_full_journey",
            "label": "Platform revenue ceiling \u2014 18% \u00d7 full Journey GMV",
            "low": band(G["partner_platform_rev_full_journey_yr"])["low"],
            "mid": band(G["partner_platform_rev_full_journey_yr"])["mid"],
            "high": band(G["partner_platform_rev_full_journey_yr"])["high"],
            "display": {
                "low":  m(band(G["partner_platform_rev_full_journey_yr"])["low"]),
                "mid":  m(band(G["partner_platform_rev_full_journey_yr"])["mid"]),
                "high": m(band(G["partner_platform_rev_full_journey_yr"])["high"]),
            },
            "derivation": "journey_gmv.mid \u00d7 0.18 (full GMV ceiling, not Navier-corridor subset)",
            "confidence_label": "Projected",
            "_doc": "Sibling reference. Do NOT promote to a 7th ladder rung. "
                    "Platform_rev rung remains the Navier-subset Interpretation-A value.",
        }

    # ---- 2. phase_economics (3 horizons) ---------------------------------
    som_net = band(G["SOM_full_network_navier_transport_rev_yr"])
    sam_net = band(G["SAM_navier_transport_rev_yr"])
    plat    = band(G["partner_platform_rev_yr"])
    # WIDTH vs DEPTH partner: greenfield census ON => Scale = geographic width (SOM_full_network).
    # greenfield OFF (e.g. purpose-built giga-project networks) => Scale = DEPTH: the sourced
    # flagship corridors ramping to project capacity (matured capture), no new geography assumed.
    gf_mode = gf.get("mode")
    if gf_mode == "census":
        scale_rev   = som_net
        scale_scope = "Extend to the full mapped greenfield network"
        scale_cap   = f"{cappct} (still conservative)"
        scale_vessel= "N30 Pioneer II + N35 Shuttle (12\u201315 pax, 2027) on dense legs"
    else:
        scale_rev   = band(G["SAM_capture_ramp_navier_transport_rev_yr"])
        scale_scope = "Flagship corridors ramp to project capacity \u2014 depth, not new geography"
        scale_cap   = (f"already ~{cappct} captive capture; corridors ramp to project capacity (depth), today's demand"
                       if is_captive else
                       f"matured default-operator capture as giga-projects fill (~{maturepct}), today's demand")
        scale_vessel= "N30 Pioneer II + N35 Shuttle (12\u201315 pax, 2027) on dense resort/transit legs"
    phase_economics = {
        "headline": "Revenue potential by phase \u2014 conservative floor first, ecosystem prize last.",
        "conversion_note": f"Fleet & CO2 scale from the grounded unit: {floor_fleet} boats = {m(floor_rev)} "
                           f"transport rev = {floor_co2:,.0f} t CO2/yr (~${REVPERBOAT/1e3:,.0f}K rev/boat).",
        "horizons": [
            {
                "id": "prove", "name": "Prove", "horizon": "Year 1\u20132",
                "scope": "Sourced flagship corridors go live",
                "capture": "10% (new-entrant floor)",
                "vessel": "N30 Pioneer II (8 pax, commercial now)",
                "fleet_boats": floor_fleet,
                "navier_transport_rev_yr": floor_rev, "navier_transport_rev_display": m(floor_rev),
                **({"partner_platform_rev_yr": None, "partner_platform_rev_display": "nascent"} if show_plat else {}),
                "co2_saved_t_yr": round(floor_co2),
                "confidence": "grounded",
                "confidence_label": "Grounded",
            },
            {
                "id": "scale", "name": "Scale", "horizon": "Year 2\u20134",
                "scope": scale_scope,
                "capture": scale_cap,
                "vessel": scale_vessel,
                "fleet_boats_est": boats(scale_rev["mid"], REVPERBOAT),
                "fleet_boats_band": {"low": boats(scale_rev["low"], REVPERBOAT), "high": boats(scale_rev["high"], REVPERBOAT)},
                "navier_transport_rev_yr": scale_rev["mid"], "navier_transport_rev_display": m(scale_rev["mid"]),
                **({"partner_platform_rev_display": "building"} if show_plat else {}),
                "co2_saved_t_yr": co2(scale_rev["mid"]),
                "confidence": "med",
                "confidence_label": "Modeled",
            },
            {
                "id": "mature", "name": "Mature", "horizon": "Year 4+",
                "scope": ("Induced marine-transfer demand across the captive network (capture already ~max)"
                          if is_captive else
                          "Induced marine-transfer demand + leading-operator capture across the network"),
                "capture": f"{maturepct} mature share",
                "vessel": "N35-led mix; Quanta-LR on 75\u2013150nm regional legs (H2 2026+)",
                "fleet_boats_est_pioneer_equiv": boats(sam_net["mid"], REVPERBOAT),
                "fleet_note": "Pioneer-equivalent; N35 mix lowers hull count for the same throughput.",
                "navier_transport_rev_yr": sam_net["mid"], "navier_transport_rev_display": m(sam_net["mid"]),
                **(
                    {
                        "partner_platform_rev_yr": plat["mid"],
                        "partner_platform_rev_display": m(plat["mid"]),
                        "partner_platform_rev_on_navier_yr": plat["mid"],
                        "partner_platform_rev_on_navier_display": m(plat["mid"]),
                    }
                    if show_plat
                    else {}
                ),
                "marine_mobility_tam_yr": band(G["marine_mobility_tam_yr"])["mid"],
                "marine_mobility_tam_display": m(band(G["marine_mobility_tam_yr"])["mid"]) + " marine TAM",
                "journey_gmv_yr": band(G["journey_gmv_yr"])["mid"],
                "journey_gmv_display": m(band(G["journey_gmv_yr"])["mid"]) + " Journey GMV",
                "co2_saved_t_yr": co2(sam_net["mid"]),
                "confidence": "med-low (banded)",
                "confidence_label": "Projected",
            },
        ],
    }

    # ---- 3. vessel_sizing -------------------------------------------------
    vessel_sizing = {
        "headline": "Right vessel for every leg \u2014 corridor range picks the hull.",
        "classes": [
            {"class": "N30 Pioneer II", "pax": 8, "range_nm": 70, "status": "commercial now",
             "role": "Capillary corridors \u2264 70nm. The workhorse of Prove + Scale.", "render": "solid"},
            {"class": "N35 Shuttle", "pax": "12\u201315", "range_nm": 70, "status": "2027",
             "role": "Doubles throughput per hull on dense corridors; roughly halves payback. Scale-phase workhorse.",
             "render": "solid"},
            {"class": "Quanta-LR Hybrid", "pax": "12\u201315", "range_nm": 700, "status": "H2 2026+",
             "role": "Regional legs 75\u2013150nm beyond Pioneer range. Held out of near-term numbers.",
             "render": "amber-dashed"},
        ],
        "range_gate_note": "\u2264 70nm \u2192 Pioneer II (now). 75\u2013150nm \u2192 Quanta-LR (roadmap). "
                           "Long legs never faked on a 70nm boat.",
    }

    if not show_plat:
        block = {
            "_provenance": {},
            "revenue_potential": revenue_potential,
            "phase_economics": phase_economics,
            "vessel_sizing": vessel_sizing,
        }
        strip_frontend_block(block)
        block["_provenance"] = {
            "source_growth": os.path.basename(a.growth),
            "source_rollup": os.path.basename(a.rollup),
            "rev_per_boat_yr": round(REVPERBOAT) if REVPERBOAT else None,
            "greenfield_mode": gf_mode,
            "greenfield_corridors": (gf.get("_census") or {}).get("n_greenfield_headline"),
            "sourced_corridors": (gf.get("_census") or {}).get("n_sourced")
                                  or json.load(open(a.rollup)).get("rollup", {}).get("n_corridors_total"),
            "generator": "growth_frontend_block.py",
            "platform_rev_excluded": True,
        }
        block["_render_chip_flag"] = {
            "needs_new_layouts": ["revenue_ladder", "phase_economics_table", "vessel_sizing_cards"],
            "confidence_display": "Tag every banded rung; lead with floor + corridor COUNT (ID-traceable). "
                                  "Never headline the 'high' band.",
        }
    else:
        block = {
        "_provenance": {
            "source_growth": os.path.basename(a.growth),
            "source_rollup": os.path.basename(a.rollup),
            "rev_per_boat_yr": round(REVPERBOAT),
            "greenfield_mode": gf_mode,
            "greenfield_corridors": (gf.get("_census") or {}).get("n_greenfield_headline"),
            "sourced_corridors": (gf.get("_census") or {}).get("n_sourced")
                                  or json.load(open(a.rollup)).get("rollup", {}).get("n_corridors_total"),
            "generator": "growth_frontend_block.py",
        },
        "revenue_potential": revenue_potential,
        "phase_economics": phase_economics,
        "vessel_sizing": vessel_sizing,
        "_render_chip_flag": {
            "needs_new_layouts": ["revenue_ladder", "phase_economics_table", "vessel_sizing_cards"],
            "confidence_display": "Tag every banded rung; lead with floor + corridor COUNT (ID-traceable). "
                                  "Never headline the 'high' band.",
        },
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(block, open(a.out, "w"), indent=1, ensure_ascii=False)
    print("wrote", a.out)
    # console summary
    print(f"\nrev/boat = ${REVPERBOAT/1e3:,.0f}K | co2/$ = {CO2PERREV*1e6:.1f} t per $M")
    for h in phase_economics["horizons"]:
        fl = h.get("fleet_boats") or h.get("fleet_boats_est") or h.get("fleet_boats_est_pioneer_equiv")
        print(f"  {h['name']:7s} {h['horizon']:10s} fleet~{fl:>5} | "
              f"Navier {h['navier_transport_rev_display']:>7} | "
              f"platform {str(h.get('partner_platform_rev_display')):>8} | CO2 {h['co2_saved_t_yr']:>8,} t")

if __name__ == "__main__":
    main()
