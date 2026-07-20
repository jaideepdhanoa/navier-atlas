#!/usr/bin/env python3
"""
Navier GROWTH-CASE layer (L4) — turns the conservative corridor FLOOR into a
TAM/SAM/SOM ladder + induced-demand + journey-GMV/ecosystem-attach lines.

Design (locked, mirrors the corridor engine):
  - Reads ALL numbers from files. No hardcoded data.
  - The whole ladder hangs off ONE traceable anchor: M_today = sourced
    market_rev / som_capture_rate (= total premium-transfer transport spend on
    the sourced corridors TODAY). Every rung is one multiplication off M_today,
    so the prize traces back to grounded demand.
  - Every multiplier is a low/mid/high BAND (never a single point). MID = headline.
  - NULL-beats-guess: greenfield factor defaults OFF (1.0).
  - Three distinct money units kept explicit: navier_transport_revenue,
    journey_gmv, platform_take. (see growth-config _whose_money_legend)

Usage:
  python3 growth.py [--agg grab-aggregate-results.json] [--json out.json] [--partner grab]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIN  = os.path.dirname(HERE)
cfg  = json.load(open(os.path.join(HERE, "growth-config.json")))

def arg(flag, default):
    return sys.argv[sys.argv.index(flag)+1] if flag in sys.argv else default

partner = arg("--partner", "grab")
agg_path = arg("--agg", os.path.join(FIN, "grab-aggregate-results.json"))
agg = json.load(open(agg_path))
roll = agg["rollup"]

# LB-82: --markets <comma-list> SCOPE FILTER.
# Growth case is a partner-level rollup with no per-market rows, so when --markets is
# passed we recompute the ladder on the (already-scoped) aggregate input, then merge the
# result into a previous growth-<partner>.json carry-forward file. Out-of-scope markets
# are preserved via the prior rollup's market_rev anchor (it stays the published number).
_scope = None
if "--markets" in sys.argv:
    _raw = sys.argv[sys.argv.index("--markets")+1]
    _scope = sorted({t.strip().lower() for t in _raw.split(",") if t.strip()})

M = cfg["multipliers"]
som_capture = cfg["ladder"]["som_capture_rate"]["value"]
take = M["platform_take_rate"]["value"]

# greenfield WIDTH lever — PER-PARTNER (multi-partner safety):
#   --greenfield off            -> force factor 1.0 (e.g. Saudi: purpose-built giga-project
#                                  network; the sourced corridors ARE the addressable network,
#                                  no unsourced density to multiply — null-beats-guess).
#   --greenfield-json <census>  -> read this partner's OWN census-derived factor band.
#   (neither)                   -> fall back to growth-config default (Grab reproduces its number).
BANDS = ["low", "mid", "high"]
_gf = M["greenfield_corridor_factor"]
_gf_mode = None; _gf_src = None
_gf_arg = arg("--greenfield", None)
_gf_json = arg("--greenfield-json", None)
# Auto-discover standardized per-partner census (finance/recal/greenfield-census/<p>.json)
# when --greenfield-json is not passed. Replaces silent Grab-global 4.9× default.
_auto_census = os.path.join(FIN, "recal", "greenfield-census", f"{partner}.json")
if not _gf_json and os.path.exists(_auto_census) and _gf_arg != "off":
    _gf_json = _auto_census

_census_doc = None
if _gf_arg == "off":
    g_green = {b: 1.0 for b in BANDS}; _gf_mode = "off"; _gf_src = "forced off (per-partner)"
elif _gf_json:
    _census_doc = json.load(open(_gf_json))
    _fac = _census_doc["derived_greenfield_factor"]["headline_tier1_plus_tier2"]
    g_green = {b: float(_fac[b]) for b in BANDS}
    _gf_mode = _census_doc.get("mode") or "census"
    if _gf_mode in ("off", "census_empty"):
        g_green = {b: 1.0 for b in BANDS}
    _gf_src = _gf_json
elif partner == "didi" and _gf.get("mode") == "census":
    # Legacy fallback only when no partner census file exists.
    g_green = {b: _gf[b] for b in BANDS}; _gf_mode = "template"; _gf_src = "global template band (not a DiDi or Grab census)"
elif _gf.get("mode") == "census":
    g_green = {b: _gf[b] for b in BANDS}; _gf_mode = "census"; _gf_src = "growth-config default (Grab legacy — prefer greenfield-census/<partner>.json)"
else:
    g_green = {b: _gf.get("off_value", 1.0) for b in BANDS}; _gf_mode = "off"; _gf_src = "growth-config off"

def band(node):  # pull low/mid/high triple
    return {b: node[b] for b in BANDS}

k_ind  = band(M["induced_demand"])
c_mat  = band(M["mature_capture_rate"])
m_att  = band(M["journey_gmv_multiple"])

# ---- ANCHOR: total premium-transfer TRANSPORT spend on sourced corridors TODAY ----
# LB-254 (captive-capture reconciliation, Jaideep 2026-06-19): M_today = the TRUE transport-spend
# pool (demand x fare), emitted by aggregate.py as `transport_spend_pool_yr`. The legacy recovery
# `floor / som_capture` ASSUMED a 10% capture floor — but CAPTIVE markets (Maldives/JIH, Red Sea,
# French Polynesia...) build the floor at ~90% capture, so floor/0.10 inflated the pool (and every
# rung) ~9x. Anchoring on the real pool makes floor/pool == the capture that ACTUALLY built the
# floor (0.90 captive / 0.10 contested / blended for mixed) — there is NO divisor to mismatch.
# THE RULE: the ladder's capture must equal the capture that built the floor. At 90% capture the
# floor already IS ~the whole pool; headroom is induced demand + greenfield WIDTH, not a 10x
# capture-share expansion. Fallback to the legacy divisor only for a pre-LB-254 agg file that
# lacks the pool (contested-only partners, where the floor genuinely IS 10% of the pool).
def m_today_and_capture(node):
    pool = node.get("transport_spend_pool_yr")
    rev  = node.get("market_rev_yr")
    if pool and rev:
        return pool, (rev / pool)              # eff capture = floor / true pool
    return (rev / som_capture if (rev and som_capture) else None), som_capture  # legacy fallback

M_today_grounded, eff_capture_grounded = m_today_and_capture(roll["grounded_floor"])
M_today_total,    eff_capture_total    = m_today_and_capture(roll["estimated_total"])
_fwd = roll.get("forward_sam") or {}
M_today_forward,  eff_capture_forward  = m_today_and_capture({
    "transport_spend_pool_yr": _fwd.get("transport_spend_pool_yr"),
    "market_rev_yr": _fwd.get("market_rev_yr"),
})

# LB-254: capture cannot mature BELOW the rate the floor already operates at.
CAPTIVE_THRESHOLD = 0.5    # blended floor capture above this => CAPTIVE market treatment
CAPTIVE_CEILING   = 0.95   # max defensible lock-up capture (exclusive-deal headroom)

def mature_capture(eff_capture):
    """Captive-aware mature capture band. For CONTESTED markets (eff_capture ~0.10) the config
    ramp (0.15/0.25/0.40) all exceeds the floor => unchanged. For CAPTIVE markets (eff_capture
    ~0.90) the contested ramp is WRONG-SIGNED (would imply maturing DOWN from 90%), so we clamp
    mature capture to the floor capture with a thin high-band lock-up headroom to the ceiling.
    Captive upside therefore lives in induced demand + greenfield WIDTH, not capture-share."""
    if eff_capture and eff_capture >= CAPTIVE_THRESHOLD:
        return {"low": eff_capture, "mid": eff_capture,
                "high": min(CAPTIVE_CEILING, eff_capture + 0.05)}
    return {b: max(c_mat[b], eff_capture or 0.0) for b in BANDS}

def ladder(M_today, eff_capture):
    """Build the full ladder off a single M_today anchor at the floor's actual capture."""
    # LB-256 (Jaideep 2026-06-20): FORWARD-SAM-ONLY guard. Partners whose corridors carry NO
    # grounded/estimated demand yet (e.g. saudi-pif: 0 grounded, all _forward_sam) yield a null
    # M_today on that anchor. Emit an honest null floor (null-beats-guess) instead of crashing on
    # round(None); the headline is then carried by whichever anchor IS populated (see _headline_anchor).
    if M_today is None:
        return {"M_today_transport_spend_yr": None, "_eff_capture_floor": None,
                "_mature_capture_used": None, "_is_captive": None,
                "_forward_sam_only": True,
                "SOM_floor_navier_transport_rev_yr": None}
    out = {"M_today_transport_spend_yr": round(M_today, 0)}
    c_eff = mature_capture(eff_capture)   # LB-254: capture >= floor; captive-aware
    out["_eff_capture_floor"] = round(eff_capture, 4) if eff_capture is not None else None
    out["_mature_capture_used"] = {b: round(c_eff[b], 4) for b in BANDS}
    out["_is_captive"] = bool(eff_capture and eff_capture >= CAPTIVE_THRESHOLD)
    # SOM floor (reproduces the published number) at the capture that BUILT it ----------
    out["SOM_floor_navier_transport_rev_yr"] = round(M_today * eff_capture, 0)
    # SOM full network — same conservative near-term posture (floor capture, today's
    # density-adjusted demand, NO induced, NO maturity ramp) extended across the whole
    # mapped addressable network (sourced + greenfield). The width analog of the floor.
    out["SOM_full_network_navier_transport_rev_yr"] = {
        b: round(M_today * eff_capture * g_green[b], 0) for b in BANDS}
    # SAM capture-ramp — today's (projected) demand at matured capture (>= floor capture),
    # NO induced market growth, NO greenfield. For contested: share rises from the 10% floor
    # toward mature capture; for CAPTIVE: ~flat at the floor (no fictitious capture headroom).
    out["SAM_capture_ramp_navier_transport_rev_yr"] = {
        b: round(M_today * c_eff[b], 0) for b in BANDS}
    # SAM (sourced corridors only) — matured network on the sourced corridors, NO greenfield.
    # This is the "depth" rung: how much the sourced corridors alone yield at maturity.
    out["SAM_sourced_only_navier_transport_rev_yr"] = {
        b: round(M_today * k_ind[b] * c_eff[b], 0) for b in BANDS}
    # SAM = Navier transport revenue at matured network ACROSS THE FULL ADDRESSABLE NETWORK
    # (induced demand + capture ramp + greenfield width). This is the headline SAM.
    out["SAM_navier_transport_rev_yr"] = {
        b: round(M_today * k_ind[b] * c_eff[b] * g_green[b], 0) for b in BANDS}
    # TAM = total journey GMV across the induced crossing market on the full addressable network
    out["TAM_journey_gmv_yr"] = {
        b: round(M_today * k_ind[b] * m_att[b] * g_green[b], 0) for b in BANDS}
    # Journey GMV actually routed through the Navier network (Navier-carried trips)
    out["network_journey_gmv_yr"] = {
        b: round(M_today * k_ind[b] * c_eff[b] * m_att[b] * g_green[b], 0) for b in BANDS}
    # Partner (Grab) platform revenue on that network GMV — the super-app's own take
    out["partner_platform_rev_yr"] = {
        b: round(M_today * k_ind[b] * c_eff[b] * m_att[b] * g_green[b] * take, 0) for b in BANDS}
    # LB-113 alias: explicit "on Navier" naming — partner_platform_rev_on_navier_yr
    out["partner_platform_rev_on_navier_yr"] = out["partner_platform_rev_yr"]
    # ---- ζ1 (LB-122): partner_platform_rev_full_journey — ceiling SIBLING, not 7th rung ----
    # Ceiling = 18% × FULL journey GMV (not Navier-corridor subset). Banded low/mid/high.
    # Use as parallel sibling reference; do NOT promote to ladder rung.
    # Note: TAM_journey_gmv_yr is the same as journey_gmv_yr (LB-111 alias set below).
    out["partner_platform_rev_full_journey_yr"] = {
        b: round(out["TAM_journey_gmv_yr"][b] * take, 0) for b in BANDS}
    # Today's journey GMV (existing demand, NO induced) — a non-induced anchor
    out["today_journey_gmv_yr"] = {
        b: round(M_today * m_att[b], 0) for b in BANDS}
    # ---- LB-110: MARINE MOBILITY TAM (induced marine-transfer market) ----
    # marine_mobility_tam = SAM_full_network / c_mat
    # Interpretation: the inducible water-transfer market at full network width,
    # PRE-capture-constraint. (SAM is the captured share; dividing by c recovers the
    # total addressable spend.) Locked by Jaideep 2026-06-11.
    out["marine_mobility_tam_yr"] = {
        b: round(M_today * k_ind[b] * g_green[b], 0) for b in BANDS}
    # ---- LB-111: rename TAM_journey_gmv_yr -> journey_gmv_yr (one-cycle alias) ----
    out["journey_gmv_yr"] = out["TAM_journey_gmv_yr"]
    return out

result = {
    "partner": partner,
    "_as_of": cfg["_as_of"],
    "anchor_note": "LB-254: M_today = transport_spend_pool_yr (demand x fare); the ladder's capture = floor/pool (the capture that actually built the floor: ~0.90 captive / ~0.10 contested / blended). Replaces the legacy floor/0.10 divisor that inflated captive markets ~9x.",
    "parameters_used": {
        "som_capture_rate_legacy_fallback": som_capture,
        "effective_capture_floor_grounded": round(eff_capture_grounded, 4) if eff_capture_grounded is not None else None,
        "effective_capture_floor_estimated_total": round(eff_capture_total, 4) if eff_capture_total is not None else None,
        "induced_demand": k_ind, "mature_capture_rate_config_band": c_mat,
        "captive_threshold": CAPTIVE_THRESHOLD, "captive_ceiling": CAPTIVE_CEILING,
        "journey_gmv_multiple": m_att, "platform_take_rate": take,
        "greenfield_corridor_factor": g_green,
    },
    "grounded": ladder(M_today_grounded, eff_capture_grounded),
    "estimated_total": ladder(M_today_total, eff_capture_total),
    "forward_sam": ladder(M_today_forward, eff_capture_forward),
    "source_rollup": {
        "n_corridors": roll["n_corridors_total"],
        "som_floor_grounded_rev_yr": roll["grounded_floor"]["market_rev_yr"],
        "som_floor_grounded_fleet": roll["grounded_floor"]["fleet"],
        "som_estimated_total_rev_yr": roll["estimated_total"]["market_rev_yr"],
    },
    # The shared config historically named Grab in what is otherwise a generic legend.
    # Keep partner output neutral so inheriting partners never carry peer-specific prose.
    "_whose_money_legend": {k: (v.replace("The partner's (Grab's) own", "The partner's own") if isinstance(v, str) else v)
                             for k, v in cfg["_whose_money_legend"].items()},
    "greenfield": {
        "mode": _gf_mode,
        "source": _gf_src,
        "factor_band": g_green,
        "_census": (
            {
                "source": _gf_src,
                "n_sourced": (_census_doc or {}).get("n_sourced"),
                "n_greenfield_headline": (_census_doc or {}).get("n_greenfield_headline"),
                "count_ratio": (_census_doc or {}).get("count_ratio"),
                "alpha_density": (_census_doc or {}).get("alpha_density"),
                "methodology": (_census_doc or {}).get("methodology"),
                "note": (_census_doc or {}).get("note"),
            }
            if _census_doc
            else (_gf.get("_census") if _gf_mode == "census" and "growth-config" in str(_gf_src) else None)
        ),
        "_doc": "WIDTH lever. SAM_sourced_only = depth on the sourced corridors (no greenfield). "
                "SAM/TAM/network/platform = full addressable network (sourced + greenfield). "
                "SOM floor is unaffected (it is the sourced corridors). "
                "Prefer finance/recal/greenfield-census/<partner>.json over Grab-global template.",
    },
}

def fm(x):
    if x is None: return "—"
    return f"${x/1e6:,.0f}M" if x < 1e9 else f"${x/1e9:,.2f}B"

def band_str(d): return " / ".join(fm(d[b]) for b in BANDS)

# LB-256: forward-SAM-only partners (no grounded demand sourced yet) carry the headline on the
# forward_sam rollup bucket (held OUT of estimated_total by aggregate.py); record which anchor is
# authoritative so the frontend splice reads the populated rung, not the null grounded floor.
FORWARD_SAM_ONLY = (result["grounded"].get("M_today_transport_spend_yr") is None
                    and result["estimated_total"].get("M_today_transport_spend_yr") is None
                    and result["forward_sam"].get("M_today_transport_spend_yr") is not None)
result["_forward_sam_only"] = FORWARD_SAM_ONLY
result["_headline_anchor"] = "forward_sam" if FORWARD_SAM_ONLY else "grounded"
g = result["forward_sam"] if FORWARD_SAM_ONLY else result["grounded"]
_anchor_lbl = "forward-SAM (2030+ mapped network)" if FORWARD_SAM_ONLY else "grounded"
_nsrc = roll.get("n_grounded") or roll.get("n_corridors_total") or roll.get("n_corridors_near_term") or "the sourced"
_gflabel = ("+measured greenfield" if _gf_mode == "census" else
            "+global-template greenfield" if _gf_mode == "template" else
            "greenfield OFF")

if g.get("SOM_full_network_navier_transport_rev_yr") is None:
    # Both anchors null: nothing sourced or estimated yet. Honest no-op (null-beats-guess).
    print(f"\n=== {partner.upper()} GROWTH CASE — FORWARD-SAM-ONLY (no grounded/estimated demand) ===")
    print("Both grounded and estimated_total floors are null; ladder rungs are null (null-beats-guess).")
    print("Source demand on >=1 corridor, or confirm forward-SAM intent, to populate the ladder.")
else:
    _cappct = f"{g['_eff_capture_floor']*100:.0f}%" if g.get('_eff_capture_floor') is not None else "—"
    _captag = "CAPTIVE" if g.get('_is_captive') else "contested"
    print(f"\n=== {partner.upper()} GROWTH CASE — {_anchor_lbl} anchor (low / MID / high) ===")
    print(f"Anchor  M_today transport-spend POOL (demand x fare, sourced corridors, today): {fm(g['M_today_transport_spend_yr'])}/yr")
    print(f"        floor capture = {_cappct} ({_captag}); ladder capture cannot mature below the floor (LB-254)\n")
    print(f"  SOM  (floor, {_cappct} capture, today's demand, sourced {_nsrc})  {fm(g['SOM_floor_navier_transport_rev_yr'])}/yr   [PUBLISHED]")
    print(f"  SOM  full network ({_cappct} capture, today, {_gflabel})    {band_str(g['SOM_full_network_navier_transport_rev_yr'])}/yr")
    print(f"  SAM* sourced corridors only (depth, no greenfield)     {band_str(g['SAM_sourced_only_navier_transport_rev_yr'])}/yr")
    print(f"  SAM  Navier transport rev @ FULL network ({_gflabel}) {band_str(g['SAM_navier_transport_rev_yr'])}/yr")
    print(f"  TAM  total journey GMV (induced crossing market)       {band_str(g['TAM_journey_gmv_yr'])}/yr")
    print(f"  ---  journey GMV routed through Navier network         {band_str(g['network_journey_gmv_yr'])}/yr")
    print(f"  ---  PARTNER platform revenue on Navier network        {band_str(g['partner_platform_rev_yr'])}/yr")
    print(f"  ---  today's journey GMV (existing demand, no induced) {band_str(g['today_journey_gmv_yr'])}/yr")
    print(f"\nMID headline: floor {fm(g['SOM_floor_navier_transport_rev_yr'])} boat-fare  ->  SAM {fm(g['SAM_navier_transport_rev_yr']['mid'])} Navier transport, "
          f"{fm(g['network_journey_gmv_yr']['mid'])} journey GMV through the network, "
          f"{fm(g['partner_platform_rev_yr']['mid'])} partner platform revenue.")
    print("\n(estimated-total anchor adds the cascade-estimated corridors; see JSON.)")

if _scope is not None:
    result["_scope"] = _scope
    # carry-forward from recal/growth-<partner>.json if present (LB-82)
    _prev = os.path.join(FIN, "recal", f"growth-{partner}.json")
    if os.path.exists(_prev):
        try:
            _p = json.load(open(_prev))
            result["_carry_forward"] = {
                "prev_source": _prev,
                "_doc": "Growth output has no per-market rows; full ladder recomputed from the scoped aggregate. Prev anchor preserved below for diffing.",
                "prev_source_rollup": _p.get("source_rollup"),
            }
        except Exception as _e:
            print(f"[LB-82] growth carry-forward warn: {_e}", file=sys.stderr)

if "--json" in sys.argv or _scope is not None:
    _default = os.path.join(FIN, "recal", f"growth-{partner}.json") if _scope is not None else os.path.join(FIN, "grab-growth-case.json")
    p = arg("--json", _default)
    json.dump(result, open(p, "w"), indent=2, ensure_ascii=False)
    print("\nwrote", p)
