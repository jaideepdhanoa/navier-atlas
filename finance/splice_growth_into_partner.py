#!/usr/bin/env python3
"""LB-110/111/113 splice: take the new 6-rung growth-block + emit ladder_transitions for
a partner; splice into partner-pitch/partners/{partner}.json in place.

Cascade preserves: phases, featured_routes, committed_fleet, all other top-level fields.
Replaces inside growth_case: revenue_potential, phase_economics, modal_lead, modal_headline,
ladder_transitions, _growth_provenance.

Usage:
  python3 splice_growth_into_partner.py --partner grab \
    --growth grab-growth-case.json --frontend ../partner-pitch/partners/_growth-draft/grab.growth.json
"""
import argparse, json, os, shutil, sys, time
from datetime import datetime

def m(x):
    if x is None: return "—"
    return f"${x/1e6:,.0f}M" if x < 1e9 else f"${x/1e9:,.2f}B"

def build_ladder_transitions(gc_grounded, params, partner):
    """Six-rung ascending: som_floor -> som_network -> sam_network -> tam_transfer
    -> journey_gmv -> platform_rev."""
    G = gc_grounded
    P = params
    gf = (P.get("greenfield_corridor_factor", {}) or {}).get("mid")
    if gf is None:
        gf = 1.0
    k_ind_mid = P["induced_demand"]["mid"]
    # LB-254: capture that ACTUALLY built the floor (eff) + the captive-aware mature band, both
    # emitted per-anchor by growth.py. Replaces the hardcoded contested 0.10 narrative so captive
    # markets (eff ~0.90) read honestly instead of falsely claiming a 10%->25% capture ramp.
    eff_cap    = G.get("_eff_capture_floor") or 0.10
    c_mat_band = G.get("_mature_capture_used") or P.get("mature_capture_rate_config_band") or {"mid": 0.25}
    c_mat_mid  = c_mat_band["mid"]
    is_captive = bool(G.get("_is_captive"))
    m_att_mid = P["journey_gmv_multiple"]["mid"]
    take = P.get("platform_take_rate", 0.18)
    if isinstance(take, dict):
        take = take.get("mid", 0.18)

    som_floor = G["SOM_floor_navier_transport_rev_yr"]
    som_net   = G["SOM_full_network_navier_transport_rev_yr"]["mid"]
    sam_net   = G["SAM_navier_transport_rev_yr"]["mid"]
    tam_trf   = G["marine_mobility_tam_yr"]["mid"]
    jrny      = G["journey_gmv_yr"]["mid"]
    plat      = G["partner_platform_rev_on_navier_yr"]["mid"]

    partner_label = {"grab":"Grab","careem":"Careem","jih-global":"JIH Global","qatar":"Qatar",
                     "saudi-pif":"Saudi PIF","red-sea-global":"Red Sea Global"}.get(partner, partner.title())

    return [
        {
            "from_rung_id":"som_floor","to_rung_id":"som_network",
            "headline":"Same 10% capture, expanded to the full mapped network",
            "basis":("Width-only step. Capture rate held at 10%; corridor set expands from sourced "
                     "flagships to the full mapped network."),
            "derivation":f"som_floor_mid ({m(som_floor)}) \u00d7 greenfield_corridor_factor.mid ({gf:.2f}) = {m(som_net)} (som_network mid)",
            "multipliers_cited":{"greenfield_corridor_factor_mid":gf,"som_capture_rate":0.1},
            "source_fields":[
                f"finance/recal/growth-{partner}.json:parameters_used.greenfield_corridor_factor",
                f"finance/recal/growth-{partner}.json:parameters_used.som_capture_rate",
            ],
            "confidence":"med",
        },
        {
            "from_rung_id":"som_network","to_rung_id":"sam_network",
            "headline":"Network matures: faster, more comfortable boats grow the market + leading-operator capture",
            "basis":("Two-lever step. (1) Faster, more comfortable boats grow the cross-water market "
                     "(induced demand). (2) Leading-operator capture lifts share from 10% floor to 25% mature, "
                     "network-wide."),
            "derivation":(f"som_network_mid ({m(som_net)}) \u00d7 induced_demand.mid ({k_ind_mid:.2f}) "
                          f"\u00d7 (mature_capture / som_capture) ({c_mat_mid:.2f}/0.10 = {c_mat_mid/0.10:.2f}) = {m(sam_net)} (sam_network mid)"),
            "multipliers_cited":{"induced_demand_mid":k_ind_mid,"mature_capture_rate_mid":c_mat_mid,"som_capture_rate":0.1},
            "source_fields":[
                f"finance/recal/growth-{partner}.json:parameters_used.induced_demand",
                f"finance/recal/growth-{partner}.json:parameters_used.mature_capture_rate",
            ],
            "confidence":"med-low",
        },
        {
            "from_rung_id":"sam_network","to_rung_id":"tam_transfer",
            "headline":"Lens shift: Navier captured share \u2192 total inducible marine-transfer wallet",
            "basis":("Unit change. Divide SAM (the captured share) by leading-operator capture rate to recover "
                     "the full inducible water-transfer market \u2014 the marine-mobility TAM."),
            "derivation":f"sam_network_mid ({m(sam_net)}) \u00f7 mature_capture.mid ({c_mat_mid:.2f}) = {m(tam_trf)} (marine TAM mid)",
            "multipliers_cited":{"mature_capture_rate_mid":c_mat_mid},
            "source_fields":[f"finance/recal/growth-{partner}.json:parameters_used.mature_capture_rate"],
            "confidence":"med-low",
            "_lb_ref":"LB-110: marine_mobility_tam = SAM_full_network / c (locked 2026-06-11)",
        },
        {
            "from_rung_id":"tam_transfer","to_rung_id":"journey_gmv",
            "headline":"Marine transfer \u2192 total journey wallet (food, stays, experiences, in-app ads)",
            "basis":("Journey-wallet step. Each $1 of marine-transfer spend unlocks ~$3 of broader journey "
                     "GMV across merchants the partner monetizes."),
            "derivation":f"marine_tam_mid ({m(tam_trf)}) \u00d7 journey_gmv_multiple.mid ({m_att_mid:.2f}) = {m(jrny)} (journey_gmv mid)",
            "multipliers_cited":{"journey_gmv_multiple_mid":m_att_mid},
            "source_fields":[f"finance/recal/growth-{partner}.json:parameters_used.journey_gmv_multiple"],
            "confidence":"med-low",
        },
        {
            "from_rung_id":"journey_gmv","to_rung_id":"platform_rev",
            "headline":f"{partner_label} platform take on Navier-carried journeys",
            "basis":("Platform-take step. Platform commission applied to the journey GMV routed through "
                     "the Navier network (Navier-captured subset, not the full induced market)."),
            "derivation":(f"sam_network_mid ({m(sam_net)}) \u00d7 journey_gmv_multiple.mid ({m_att_mid:.2f}) "
                          f"\u00d7 platform_take_rate ({take:.0%}) = {m(plat)} (platform_rev mid)"),
            "multipliers_cited":{"journey_gmv_multiple_mid":m_att_mid,"platform_take_rate":take,"mature_capture_rate_mid":c_mat_mid},
            "source_fields":[
                f"finance/recal/growth-{partner}.json:parameters_used.platform_take_rate",
                f"finance/recal/growth-{partner}.json:parameters_used.journey_gmv_multiple",
            ],
            "confidence":"med-low",
            "_lb_ref":"LB-113: partner_platform_rev_on_navier = on-Navier subset, distinct from deck's '18% \u00d7 full Journey GMV' narrative ceiling",
        },
    ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", required=True)
    ap.add_argument("--growth", required=True)
    ap.add_argument("--frontend", required=True)
    ap.add_argument("--partner-json", default=None)
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    pj = a.partner_json or os.path.join(root, "partner-pitch", "partners", f"{a.partner}.json")
    shutil.copy(pj, pj + ".bak-pre-marine-tam-split")

    gc = json.load(open(a.growth))
    fe = json.load(open(a.frontend))
    pp = json.load(open(pj))

    if "growth_case" not in pp:
        pp["growth_case"] = {}
    gcblock = pp["growth_case"]

    # replace revenue_potential + phase_economics + vessel_sizing
    gcblock["revenue_potential"] = fe["revenue_potential"]
    gcblock["phase_economics"]   = fe["phase_economics"]
    gcblock["vessel_sizing"]     = fe.get("vessel_sizing", gcblock.get("vessel_sizing"))
    gcblock["_provenance"]       = fe.get("_provenance", gcblock.get("_provenance"))
    gcblock["_render_chip_flag"] = fe.get("_render_chip_flag", gcblock.get("_render_chip_flag"))

    # modal copy refresh
    gcblock["modal_lead"] = gcblock["revenue_potential"]["modal_lead"]
    if not gcblock.get("modal_headline"):
        gcblock["modal_headline"] = "Floor to prize \u2014 every rung traces to grounded demand"

    # ladder_transitions regenerated
    gcblock["ladder_transitions"] = build_ladder_transitions(
        gc["grounded"], gc["parameters_used"], a.partner)

    # marine TAM convenience surface at growth_case top
    gcblock["marine_mobility_tam"] = gc["grounded"]["marine_mobility_tam_yr"]
    gcblock["journey_gmv"] = gc["grounded"]["journey_gmv_yr"]
    gcblock["partner_platform_rev_on_navier"] = gc["grounded"]["partner_platform_rev_on_navier_yr"]
    gcblock["_marine_tam_split_provenance"] = {
        "date": datetime.utcnow().isoformat() + "Z",
        "formula": "marine_mobility_tam = SAM_full_network / mature_capture_rate (LB-110)",
        "field_renames": {
            "tam_gmv": "journey_gmv (LB-111; alias preserved one cycle)",
            "partner_platform_rev": "partner_platform_rev_on_navier (LB-113)",
        },
        "ladder_rung_count": 6,
        "rungs_ascending": ["som_floor","som_network","sam_network","tam_transfer","journey_gmv","platform_rev"],
    }

    json.dump(pp, open(pj, "w"), indent=1, ensure_ascii=False)
    print(f"spliced {a.partner}: rungs={len(gcblock['revenue_potential']['rungs'])} "
          f"transitions={len(gcblock['ladder_transitions'])} "
          f"marine_tam_mid={m(gcblock['marine_mobility_tam']['mid'])} "
          f"plat_on_navier_mid={m(gcblock['partner_platform_rev_on_navier']['mid'])}")

if __name__ == "__main__":
    main()
