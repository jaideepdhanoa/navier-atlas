#!/usr/bin/env python3
"""
Navier corridor-economics AGGREGATOR.
Joins the per-corridor L3 sourcing (corridors.json) with the per-country opex
layer (country-reference.json), runs the atom P&L engine across THIN/MID/FULL
utilization bands for every corridor, runs the estimation cascade for null-demand
corridors (tagged), and rolls up to a partner-regional opportunity.

Design (locked):
  - Reads ALL numbers from files. No hardcoded data.
  - LB-235: default --partner is 'grab'; CLI callers MUST pass --partner explicitly
    for any non-grab refresh. Default-path bug documented; fix candidate = default
    to 'all' + multi-partner mode. Workaround in place: explicit --partner everywhere.
  - Parity pricing (discount 1.0). Per-seat shuttle only.
  - NULL beats a guess: grounded demand and cascade-estimated demand are kept
    SEPARATE so the rollup shows a grounded FLOOR and an estimated TOTAL.
  - Cross-border opex = vessel home-port country (R16) = Singapore default.
  - Duplicates (_dup_of, or label seen in a real market) excluded from rollup.

Usage: python3 aggregate.py [--json out.json] [--partner grab]
"""
import json, os, sys, copy, importlib.util, statistics, math

HERE = os.path.dirname(os.path.abspath(__file__))
const = json.load(open(os.path.join(HERE, "vessel-constants.json")))
# --corridors <path>: override the corridor registry source. Used to feed a SCOPED VIEW of the
# shared global network for inheriting partners (Uber/DiDi/hotels) WITHOUT duplicating corridors
# into the durable corridors.json (the network is shared, not copied). Default = canonical registry.
_CORR_PATH = sys.argv[sys.argv.index("--corridors")+1] if "--corridors" in sys.argv else os.path.join(HERE, "corridors.json")
corr  = json.load(open(_CORR_PATH))
cref  = json.load(open(os.path.join(HERE, "country-reference.json")))["countries"]

# import compute_atom from atom.py
spec = importlib.util.spec_from_file_location("atom", os.path.join(HERE, "atom.py"))
atom = importlib.util.module_from_spec(spec); spec.loader.exec_module(atom)

SCEN = const["operating_defaults"]["_utilization_scenarios"]
CROSS_BORDER_HOMEPORT = "Singapore"   # R16: default home-port opex for cross-border

def cval(country, key):
    row = cref.get(country)
    if not row or key not in row: return None
    v = row[key]
    return v["value"] if isinstance(v, dict) and "value" in v else v

PIONEER_RANGE_NM = const["vessels"]["pioneer_ii"]["range_nm"]
PIONEER_RANGE_NM = PIONEER_RANGE_NM["value"] if isinstance(PIONEER_RANGE_NM, dict) else PIONEER_RANGE_NM

def vessel_for(nm):
    """Hard range gate: Pioneer II commercial-now <=70nm; longer needs roadmap Quanta-LR."""
    return "pioneer_ii" if nm <= PIONEER_RANGE_NM else "quanta_lr"

# LB-177 (Jaideep 2026-06-14): SEA/Grab markets benefit from regional manufacturing/landed-cost
# advantage — capex per vessel = $600K vs $900K global. Applied via L3 override in enrich().
# LB-196 (Jaideep 2026-06-16): UAE/Careem markets (uae-careem, uae-luxury) also use $600K capex.
# LB-243 (Jaideep 2026-06-19): GENERALIZED TO A GLOBAL RULE keyed on COUNTRY, not a market allowlist.
#   capex = $900K for US and EU markets; $600K for every market OUTSIDE US and EU.
#   Rationale: landed-cost / manufacturing advantage applies everywhere except the high-cost
#   US + EU bloc. Keyed on the resolved opex country so it is robust to new markets.
CAPEX_USEU_USD = 900000   # United States + EU member states
CAPEX_ROW_USD  = 600000   # rest of world (outside US/EU)
EU_COUNTRIES = {
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland",
    "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland",
    "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden",
}
US_COUNTRIES = {"United States", "USA", "United States of America"}

def capex_for_country(country):
    """LB-243 global rule: US/EU -> $900K; everywhere else -> $600K."""
    if country in EU_COUNTRIES or country in US_COUNTRIES:
        return CAPEX_USEU_USD
    return CAPEX_ROW_USD

def enrich(c, market):
    """Return a deep copy with L3 opex injected from country layer + demand mapped."""
    c = copy.deepcopy(c)
    L3 = c.setdefault("L3_locals", {})
    # --- country selection (R16: cross-border or any non-cref country -> home-port) ---
    country = c.get("country")
    if country not in cref:               # 'CrossBorder' or missing -> home-port opex (R16)
        country = CROSS_BORDER_HOMEPORT
    c["_opex_country"] = country
    # LB-243: global region-based capex rule, keyed on resolved opex country.
    if L3.get("capex_usd_override") is None:
        L3["capex_usd_override"] = capex_for_country(country)
    # --- inject opex if the corridor didn't already carry atom-native fields ---
    if L3.get("energy_usd_per_kwh") is None:
        L3["energy_usd_per_kwh"] = cval(country, "energy_usd_kwh")
    if L3.get("captain_annual_usd") is None:
        L3["captain_annual_usd"] = cval(country, "captain_usd_yr")
    if L3.get("marina_overhead_annual_usd") is None:
        L3["marina_overhead_annual_usd"] = cval(country, "marina_overhead_usd_yr")
    if L3.get("grid_kg_co2_per_kwh") is None:
        L3["grid_kg_co2_per_kwh"] = cval(country, "grid_co2_kg_kwh")
    # --- demand mapping: atom reads demand_arrivals_rides_yr / demand_ferry_rides_yr ---
    if L3.get("demand_arrivals_rides_yr") is None and L3.get("demand_ferry_rides_yr") is None:
        pax = L3.get("corridor_annual_oneway_pax")
        if pax is not None:
            L3["demand_ferry_rides_yr"] = pax   # crossing pool proxy
    # archetype must map to a discount segment (all 1.0)
    # preserve the raw archetype first (capture-override keys on it; default-OFF so no effect)
    c["_archetype_raw"] = c.get("archetype")
    if c.get("archetype") not in const["operating_defaults"]["discount_factor"]:
        c["archetype"] = "intercity"
    return c

def run_scenarios(c, vessel_key):
    out = {}
    for name, band in SCEN.items():
        if name.startswith("_"): continue
        cc = copy.deepcopy(c)
        cc["L3_locals"]["load_factor"] = band["load_factor"]
        cc["L3_locals"]["revenue_leg_factor"] = band["revenue_leg_factor"]
        out[name] = atom.compute_atom(cc, vessel_key=vessel_key)
    return out

def main():
    partner = "grab"
    if "--partner" in sys.argv: partner = sys.argv[sys.argv.index("--partner")+1]

    # LB-82: --markets <comma-list> SCOPE FILTER.
    # Only recompute rows for in-scope markets; carry forward out-of-scope rows
    # from a previous output JSON (default: /tasklet/.../recal/agg-<partner>.json),
    # merged by route_id. Backward compat: no flag = full behavior.
    scope = None
    if "--markets" in sys.argv:
        raw = sys.argv[sys.argv.index("--markets")+1]
        scope = {t.strip().lower() for t in raw.split(",") if t.strip()}
    def in_scope(mid):
        if scope is None: return True
        mlow = mid.lower()
        return any(tok in mlow or mlow in tok for tok in scope)

    # dedupe: collect (from,to) labels seen in "real" markets to drop cross-listed dups
    seen_labels = {}
    rows = []; roadmap = []
    # PARTNER SCOPING (multi-partner safety): only aggregate markets owned by this partner.
    # --partner global: process ALL markets (route physics are partner-independent); market.partner
    # is provenance only. Output defaults to finance/recal/agg-global.json.
    global_mode = partner == "global"
    for mid, mk in corr["markets"].items():
        if not global_mode and mk.get("partner", "grab") != partner:
            continue
        if not in_scope(mid):
            continue
        for c in mk["corridors"]:
            if c.get("_premium_cascade"): continue  # R5-EXT: public-transit/no-premium-tier — excluded from floor & estimation
            key = (c.get("from","").strip().lower(), c.get("to","").strip().lower())
            is_dup = c.get("_dup_of") is not None or (key in seen_labels and seen_labels[key] != mid)
            seen_labels.setdefault(key, mid)
            nm = c["distance_nm"]
            vk = vessel_for(nm)
            ec = enrich(c, mid)
            # --- RANGE GATE: corridors beyond Pioneer II range need roadmap Quanta-LR ---
            if vk != "pioneer_ii":
                roadmap.append({"market": mid, "corridor": f"{c['from']} -> {c['to']}",
                                "nm": nm, "fare": (ec.get("L3_locals") or {}).get("comparable_fare_usd_pax"),
                                "country": ec.get("_opex_country"), "vessel": "Quanta-LR (roadmap 2026+)"})
                continue
            scen = run_scenarios(ec, vk)
            mid_r = scen["mid"]
            # LB-87: captive_resort ceiling — cap vessels at ceil(villas / 25).
            if c.get("captive_resort") and c.get("villas"):
                cap_fleet = math.ceil(c["villas"] / 25)
                for sc_name in ("thin","mid","full"):
                    sc = scen[sc_name]
                    for k in ("vessels_supported_10pct","vessels_supported_raw"):
                        v = sc.get(k)
                        if v is not None and v > cap_fleet:
                            sc[f"{k}_uncapped"] = v
                            sc[k] = cap_fleet if k=="vessels_supported_10pct" else float(cap_fleet)
                    # scale market_revenue & co2 to capped fleet
                    if sc.get("revenue_per_boat_yr") and sc.get("vessels_supported_10pct") is not None:
                        sc["market_revenue_yr_uncapped"] = sc.get("market_revenue_yr")
                        sc["market_revenue_yr"] = round(sc["revenue_per_boat_yr"] * sc["vessels_supported_10pct"], 0)
                        sc["market_revenue_yr_raw"] = sc["revenue_per_boat_yr"] * sc["vessels_supported_raw"]
                    sc["_captive_ceiling_applied"] = {"villas": c["villas"], "ceiling": cap_fleet}
            mid_r = scen["mid"]
            # LB-254: transport-spend POOL (demand x fare) = the TRUE addressable market for this
            # corridor, INDEPENDENT of capture. Captive corridors capture ~90% of this pool;
            # contested ~10%. The growth ladder anchors on pool (not floor/0.10), so captive
            # markets are no longer inflated 9x. Pool is NOT fleet/ceiling-capped (it is total spend).
            _dem = (ec.get("L3_locals") or {}).get("corridor_annual_oneway_pax") \
                   or (ec.get("L3_locals") or {}).get("demand_ferry_rides_yr") or 0
            _pool_yr = (_dem or 0) * (mid_r.get("comparable_fare_usd") or 0)
            rows.append({
                "market": mid, "country": ec.get("_opex_country"),
                "pool_yr": _pool_yr,
                "corridor": mid_r["corridor"], "nm": mid_r["distance_nm"],
                "fare": mid_r["comparable_fare_usd"],
                "is_dup": is_dup,
                # R-SUBSET (G51): pier-exact mint slice of a parent crossing. Carries its own
                # economics (sidecar/card) but is EXCLUDED from market fleet/revenue sums —
                # the parent crossing already pools the full demand.
                "_subset_of": c.get("_subset_of"),
                "_forward_sam": bool(c.get("_forward_sam")),
                # LB-97/LB-98 sourced greenfield tiers — must ride along for status routing
                "_tier": c.get("_tier"),
                "_in_grounded_floor": c.get("_in_grounded_floor"),
                "route_id": c.get("route_id"),
                # ceiling/base pool ratio for LB-97 P3 "scaled modal-shift" ladder step
                "_ceiling_ratio": (lambda dr: (dr.get("addressable_pax_yr_ceiling")/dr.get("addressable_pax_yr"))
                                   if (dr.get("addressable_pax_yr") and dr.get("addressable_pax_yr_ceiling")) else 1.0
                                  )(c.get("_demand_record") or (c.get("L3_locals") or {}).get("_demand_record") or {}),
                "thin": scen["thin"], "mid": mid_r, "full": scen["full"],
                "demand_conf": (c.get("L3_locals") or {}).get("demand_confidence")
                               or (c.get("L3_locals",{}).get("_demand_record") or {}).get("confidence"),
            })

    # ---- ESTIMATION CASCADE for null demand (tagged) ----
    # grounded demand pool per country, then global median, used only to estimate nulls.
    def demand_of(r): return r["mid"].get("market_revenue_yr")  # proxy presence
    grounded = [r for r in rows if not r["is_dup"] and r["mid"]["vessels_supported_10pct"]]
    # build per-country median corridor demand (one-way pax) from grounded rows
    bycountry = {}
    for r in grounded:
        pool = []
        L = None
        # recover demand pool from pax used: vessels*pax_per_year/capture — simpler: re-read source
        bycountry.setdefault(r["country"], [])
    # simpler cascade: use grounded corridor demand pools directly from corridors.json
    pools_by_country = {}; all_pools = []
    for mid, mk in corr["markets"].items():
        for c in mk["corridors"]:
            if c.get("_dup_of") or c.get("_premium_cascade") or c.get("_forward_sam") or c.get("_subset_of"): continue
            L3 = c.get("L3_locals") or {}
            pax = L3.get("corridor_annual_oneway_pax")
            if pax is None:
                pax = L3.get("demand_ferry_rides_yr") or L3.get("demand_arrivals_rides_yr")
            cty = c.get("country") or (CROSS_BORDER_HOMEPORT if mid=="cross-border" else None)
            if pax:
                pools_by_country.setdefault(cty, []).append(pax)
                all_pools.append(pax)
    global_med = statistics.median(all_pools) if all_pools else None

    def cascade_demand(country):
        if country in pools_by_country and pools_by_country[country]:
            return statistics.median(pools_by_country[country]), "country-median"
        return global_med, "region-median"

    # R-FLOOR-2: a market can opt into network-sum fleet basis (captive resort/atoll
    # clusters share one fleet across all their corridors). For those, a corridor is
    # "grounded" if it carries any real demand pool (unfloored fractional not None),
    # even when its per-corridor floor is 0. Contested markets keep the floored test.
    def market_basis(mid): return corr["markets"][mid].get("fleet_basis", "per_corridor_floor")
    def is_grounded(r):
        if market_basis(r["market"]) == "network_sum":
            return r["mid"].get("vessels_supported_raw") is not None
        return bool(r["mid"]["vessels_supported_10pct"])

    # attach estimated demand + estimated fleet to null-demand rows
    for r in rows:
        if r["is_dup"]:
            r["status"]="duplicate"; continue
        if r.get("_forward_sam"):
            # Forward/SAM: demand is low-confidence / 2030-dated (e.g. Saudi-Red Sea
            # destination caps). Computed but held OUT of the near-term grounded floor;
            # reported as a separate forward-SAM bucket so it never sits next to a hard anchor.
            r["status"]="forward_sam"; continue
        if r.get("_in_grounded_floor") is False or r.get("_tier") in ("modal_shift_greenfield","experience_upside"):
            # LB-97/LB-98: sourced greenfield tiers (modal-shift, experience attach-upside).
            # These carry their OWN sourced demand pools (not country-median cascade) but are
            # held OUT of the grounded floor by design: grounded = today's observable water
            # ridership only. Reported in estimated_upside with basis=sourced_greenfield_tier.
            r["status"]="estimated"
            r["est_basis"]="sourced_greenfield_tier"
            r["est_demand_oneway"]=None  # pool lives in the corridor's own _demand_record
            _raw = r["mid"].get("vessels_supported_raw")
            r["est_vessels"]= int(_raw) if _raw else None  # floor; thin legs stay honest 0
            r["est_vessels_raw"]= _raw  # unfloored, for P3 ceiling scaling
            r["est_market_rev"]= round(r["mid"]["revenue_per_boat_yr"]*r["est_vessels"],0) if (r["mid"].get("revenue_per_boat_yr") and r.get("est_vessels")) else None
            continue
        if is_grounded(r):
            r["status"]="grounded"
        else:
            est, basis = cascade_demand(r["country"])
            r["status"]="estimated"
            r["est_basis"]=basis
            # estimate fleet at 10% capture / pax_per_year(mid)
            ppy = r["mid"]["pax_per_year"]
            cap = const["operating_defaults"]["navier_capture_rate"]
            capv = cap["value"] if isinstance(cap,dict) else cap
            r["est_demand_oneway"]=est
            r["est_vessels"]= int((est*capv)//ppy) if (est and ppy) else None
            r["est_market_rev"]= round(r["mid"]["revenue_per_boat_yr"]*r["est_vessels"],0) if (r["mid"]["revenue_per_boat_yr"] and r.get("est_vessels")) else None
            # LB-254: cascade-estimated corridors carry no real demand; pool = est_demand x fare.
            r["pool_yr"] = (est or 0) * (r.get("fare") or 0)

    # ---- ROLLUP ----
    uniq = [r for r in rows if not r["is_dup"]]
    grounded = [r for r in uniq if r["status"]=="grounded"]
    estimated = [r for r in uniq if r["status"]=="estimated"]
    forward_sam = [r for r in uniq if r["status"]=="forward_sam"]
    def s(lst, f): return sum(x for x in (f(r) for r in lst) if x)
    # ---- grounded floor with per-market fleet basis (R-FLOOR-2) ----
    # network_sum markets: sum unfloored fractional vessels per market, round ONCE;
    # revenue/CO2 scale with the fractional need. per_corridor_floor markets: unchanged.
    g_by_mkt = {}
    for r in grounded: g_by_mkt.setdefault(r["market"], []).append(r)
    floor_fleet = 0; floor_rev = 0.0; floor_co2 = 0.0; floor_pool = 0.0
    floor_by_market = {}  # LB-103: per-market breakdown so scoped runs can merge honestly
    for mid, rs in g_by_mkt.items():
        # R-SUBSET (G51): mint-slice corridors never sum with their parent crossing.
        rs_sum = [r for r in rs if not r.get("_subset_of")]
        mp = sum((r.get("pool_yr") or 0) for r in rs_sum)  # LB-254: transport-spend pool
        if market_basis(mid) == "network_sum":
            raw_v = sum((r["mid"].get("vessels_supported_raw") or 0) for r in rs_sum)
            # market-level rounding: fleet_rounding="ceil" (G51 locked ruling for grab) vs
            # legacy round (R-FLOOR-2, e.g. maldives-jih — unchanged).
            _rnd = math.ceil if corr["markets"][mid].get("fleet_rounding") == "ceil" else round
            mf = int(_rnd(raw_v))
            mr = sum((r["mid"].get("market_revenue_yr_raw") or 0) for r in rs_sum)
            mc = sum((r["mid"].get("market_co2_saved_t_yr_raw") or 0) for r in rs_sum)
        else:
            mf = sum((r["mid"]["vessels_supported_10pct"] or 0) for r in rs_sum)
            mr = sum((r["mid"]["market_revenue_yr"] or 0) for r in rs_sum)
            mc = sum((r["mid"]["market_co2_saved_t_yr"] or 0) for r in rs_sum)
        floor_by_market[mid] = {"fleet": mf, "market_rev_yr": round(mr, 0), "co2_saved_t_yr": round(mc, 1),
                                "transport_spend_pool_yr": round(mp, 0)}
        floor_fleet += mf; floor_rev += mr; floor_co2 += mc; floor_pool += mp
    # LB-89: per-market phase caps. Phase 1 ≤ 8, Phase 2 ≤ 25, Phase 3 = network-sum.
    phase_caps_per_market = {}
    for mid, rs in g_by_mkt.items():
        rs_sum = [r for r in rs if not r.get("_subset_of")]
        if market_basis(mid) == "network_sum":
            raw_v = sum((r["mid"].get("vessels_supported_raw") or 0) for r in rs_sum)
            _rnd = math.ceil if corr["markets"][mid].get("fleet_rounding") == "ceil" else round
            net = int(_rnd(raw_v))
        else:
            net = sum((r["mid"]["vessels_supported_10pct"] or 0) for r in rs_sum)
        # LB-97 ladder: sourced greenfield tiers (modal-shift, experience attach-upside)
        # are OUT of Phase 1 (grounded-only pilot) but phase IN at P2/P3 — they carry
        # their own sourced pools, unlike country-median cascade estimates which never
        # enter the ladder.
        sgf_rows = [r for r in estimated
                    if r["market"] == mid and r.get("est_basis") == "sourced_greenfield_tier"
                    and not r.get("_subset_of")]
        sgf = sum((r.get("est_vessels") or 0) for r in sgf_rows)             # base capture
        sgf_p3 = int(sum((r.get("est_vessels_raw") or 0) * (r.get("_ceiling_ratio") or 1.0)
                         for r in sgf_rows))                                  # ceiling capture, network-summed
        phase_caps_per_market[mid] = {
            "phase_1_fleet": min(net, 8),
            "phase_2_fleet": min(net + sgf, 25),
            "phase_3_fleet": net + max(sgf, sgf_p3),
        }
    rollup = {
        "partner": "global" if global_mode else partner,
        "phase_caps_per_market_LB89": phase_caps_per_market,
        "phase_caps_LB89_doc": "Per-market caps: Phase 1 ≤ 8 boats, Phase 2 ≤ 25 boats, Phase 3 = network-sum (unchanged). Prevents single-market dominance in near-term phase economics.",
        "n_corridors_total": len(uniq), "n_grounded": len(grounded), "n_estimated": len(estimated),
        "n_forward_sam": len(forward_sam),
        "n_duplicates_excluded": sum(1 for r in rows if r["is_dup"]),
        "grounded_floor": {
            "fleet": floor_fleet,
            "market_rev_yr": round(floor_rev, 0),
            "co2_saved_t_yr": round(floor_co2, 1),
            # LB-254: true addressable transport spend (demand x fare) + the capture that
            # actually built this floor (floor/pool). Captive ~0.90, contested ~0.10, blended
            # for mixed markets. growth.py anchors on the pool, not floor/0.10.
            "transport_spend_pool_yr": round(floor_pool, 0),
            "effective_capture": round(floor_rev / floor_pool, 4) if floor_pool else None,
        },
        "grounded_floor_by_market": floor_by_market,  # LB-103: enables honest scoped-run merge
        "estimated_upside": {
            "fleet": s(estimated, lambda r: r.get("est_vessels")),
            "market_rev_yr": s(estimated, lambda r: r.get("est_market_rev")),
            "transport_spend_pool_yr": s(estimated, lambda r: r.get("pool_yr")),  # LB-254
        },
        "forward_sam": {
            "_doc": "Low-confidence / future-dated demand (e.g. Saudi-Red Sea 2030 destination caps). Computed at MID but held OUT of the near-term grounded floor and estimated_total; reported as forward-looking SAM only.",
            "fleet": s(forward_sam, lambda r: r["mid"]["vessels_supported_10pct"]),
            "market_rev_yr": s(forward_sam, lambda r: r["mid"]["market_revenue_yr"]),
            "co2_saved_t_yr": s(forward_sam, lambda r: r["mid"]["market_co2_saved_t_yr"]),
        },
    }
    rollup["estimated_total"] = {
        "fleet": rollup["grounded_floor"]["fleet"] + rollup["estimated_upside"]["fleet"],
        "market_rev_yr": rollup["grounded_floor"]["market_rev_yr"] + rollup["estimated_upside"]["market_rev_yr"],
    }
    # LB-254: estimated-total pool + its blended effective capture.
    _et_pool = (rollup["grounded_floor"]["transport_spend_pool_yr"]
                + (rollup["estimated_upside"]["transport_spend_pool_yr"] or 0))
    rollup["estimated_total"]["transport_spend_pool_yr"] = round(_et_pool, 0)
    rollup["estimated_total"]["effective_capture"] = (
        round(rollup["estimated_total"]["market_rev_yr"] / _et_pool, 4) if _et_pool else None)
    rollup["roadmap_quanta_lr_2026plus"] = {
        "n_corridors": len(roadmap),
        "note": "Beyond Pioneer II 70nm range; need Quanta-LR (H2 2026+, capacity/capex not locked). Economics held out of near-term number per null-beats-guess.",
        "corridors": [f"{r['market']}: {r['corridor']} ({r['nm']}nm)" for r in roadmap],
    }

    # ---- PRINT ----
    print(f"\n=== {partner.upper()} NEAR-TERM (Pioneer II, <=70nm) — {len(uniq)} corridors; {len(roadmap)} long-haul held for Quanta-LR ===\n")
    print(f"{'market':11} {'corridor':40} {'nm':>3} {'fare':>5} {'pay(t/m/f)':>14} {'mgn':>4} {'fleet':>6} {'status':>9}")
    for r in sorted(uniq, key=lambda x:(x['mid']['payback_years'] or 99)):
        pb=lambda s: (f"{r[s]['payback_years']}" if r[s]['payback_years'] else "—")
        mg=f"{r['mid']['margin']*100:.0f}%" if r['mid']['margin'] is not None else "—"
        fleet = r["mid"]["vessels_supported_10pct"] or (f"~{r['est_vessels']}*" if r.get("est_vessels") else "—")
        print(f"{r['market'][:11]:11} {r['corridor'][:40]:40} {r['nm']:>3} ${str(r['fare'] or '—'):>4} {pb('thin')+'/'+pb('mid')+'/'+pb('full'):>14} {mg:>4} {str(fleet):>6} {r['status']:>9}")
    print(f"\n--- ROLLUP ({partner}) ---")
    print(json.dumps(rollup, indent=2))
    print("\n* = fleet estimated via cascade (country/region median demand); grounded floor excludes these.")

    # ---- LB-82 CARRY-FORWARD: merge prev rows for unscoped markets ----
    out_obj = {"rows": rows, "rollup": rollup}
    default_recal = os.path.join(os.path.dirname(HERE), "recal",
                                 "agg-global.json" if global_mode else f"agg-{partner}.json")
    out_path = sys.argv[sys.argv.index("--json")+1] if "--json" in sys.argv else None
    if scope is not None:
        prev_path = out_path if (out_path and os.path.exists(out_path)) else default_recal
        if os.path.exists(prev_path):
            try:
                prev = json.load(open(prev_path))
                prev_rows = prev.get("rows", [])
                # carry forward rows whose market is OUT of scope (preserve original ordering)
                carry = [r for r in prev_rows if not in_scope(r.get("market",""))]
                # merge by route_id: refreshed in-scope rows win, others carried forward
                fresh_ids = {(r.get("mid") or {}).get("route_id") for r in rows}
                merged = [r for r in carry if (r.get("mid") or {}).get("route_id") not in fresh_ids] + rows
                rows = merged
                out_obj["rows"] = rows
                out_obj["_carry_forward"] = {
                    "scope": sorted(scope),
                    "prev_source": prev_path,
                    "n_rows_carried": len(carry),
                    "n_rows_refreshed": len(fresh_ids),
                }
                # LB-101: phase caps must NOT lose out-of-scope markets on a scoped run.
                prev_caps = (prev.get("rollup") or {}).get("phase_caps_per_market_LB89") or {}
                merged_caps = {k: v for k, v in prev_caps.items() if not in_scope(k)}
                merged_caps.update(out_obj["rollup"]["phase_caps_per_market_LB89"])
                out_obj["rollup"]["phase_caps_per_market_LB89"] = merged_caps
                # LB-103: merge grounded_floor_by_market the same way, then recompute the
                # network grounded_floor headline from the merged per-market breakdown.
                prev_fbm = (prev.get("rollup") or {}).get("grounded_floor_by_market") or {}
                merged_fbm = {k: v for k, v in prev_fbm.items() if not in_scope(k)}
                merged_fbm.update(out_obj["rollup"].get("grounded_floor_by_market") or {})
                out_obj["rollup"]["grounded_floor_by_market"] = merged_fbm
                if prev_fbm:
                    _m_rev  = round(sum(v["market_rev_yr"] for v in merged_fbm.values()), 0)
                    _m_pool = round(sum(v.get("transport_spend_pool_yr", 0) for v in merged_fbm.values()), 0)
                    out_obj["rollup"]["grounded_floor"] = {
                        "fleet": sum(v["fleet"] for v in merged_fbm.values()),
                        "market_rev_yr": _m_rev,
                        "co2_saved_t_yr": round(sum(v["co2_saved_t_yr"] for v in merged_fbm.values()), 1),
                        "transport_spend_pool_yr": _m_pool,  # LB-254
                        "effective_capture": round(_m_rev / _m_pool, 4) if _m_pool else None,
                    }
                    out_obj["rollup"]["_scope_only"] = False
                    out_obj["rollup"]["_scoped_merge_note"] = "grounded_floor + caps merged across scoped run (LB-101/103); other rollup fields (estimated_upside, counts) remain scope-only."
                else:
                    # prev file predates by-market breakdown -> cannot merge honestly
                    out_obj["rollup"]["_scope_only"] = True
                print(f"[LB-82] carry-forward: scope={sorted(scope)}; carried {len(carry)} prev rows from {prev_path}; refreshed {len(fresh_ids)} in-scope rows.")
            except Exception as e:
                print(f"[LB-82] warn: carry-forward failed ({e}); emitting scope-only rows.", file=sys.stderr)
        if out_path is None:
            out_path = default_recal

    if out_path:
        json.dump(out_obj, open(out_path,"w"), indent=2, ensure_ascii=False, default=str)
        print("wrote", out_path)

if __name__=="__main__":
    main()
