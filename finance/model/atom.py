#!/usr/bin/env python3
"""
Navier partner business-case ATOM engine.
One atom = (corridor x vessel x segment) for one boat, one year.

Two lenses:
  - bottoms-up per-vessel P&L (the believable unit)
  - top-down demand sizing (how many boats the corridor supports at ~10% capture)

Design rules (locked 2026-06-06):
  - per-seat shuttle only; lead with the shuttle number, unforced
  - revenue = comparable_fare x discount(segment 0.5-0.7)
  - demand from BOTH proxies w/ confidence tag; Navier capture ~10%, never 100%
  - NULL beats a wrong number: any missing L3 local -> field returns None + a flag, never fabricated
  - financing stays OUT of this core

Usage:
  python3 atom.py                 # run all corridors in corridors.json, print table
  python3 atom.py --json out.json # also dump full results
"""
import json, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
CONST = json.load(open(os.path.join(HERE, "vessel-constants.json")))
CORR  = json.load(open(os.path.join(HERE, "corridors.json")))

def vget(node, *keys):
    """pull a {'value':..} provenance record's value, or a raw scalar."""
    for k in keys:
        node = node[k]
    return node["value"] if isinstance(node, dict) and "value" in node else node

def compute_atom(corridor, vessel_key="pioneer_ii"):
    flags = []
    v   = CONST["vessels"][vessel_key]
    ops = CONST["operating_defaults"]
    car = CONST["carbon"]
    L3  = corridor["L3_locals"]
    dist = corridor["distance_nm"]
    seg  = corridor.get("archetype", "ridehail")

    # ---- TRIPS / YEAR (L1 geometry + L2 distance) ----
    cruise = vget(v, "cruise_speed_kt")          # kt = nm/hr
    one_way_hr = dist / cruise
    turn_hr = vget(ops, "turnaround_charge_min") / 60.0
    # boarding/scheduling dwell added to every cycle so short hops don't imply
    # an unrealistic sailing every few minutes (Jaideep 2026-06-19).
    dwell_hr = vget(ops, "boarding_dwell_min") / 60.0
    cycle_hr = one_way_hr + turn_hr + dwell_hr     # one revenue leg + turnaround + boarding dwell
    op_capacity = vget(ops, "monthly_operational_capacity")
    # weather/seasonality haircut layered on mechanical uptime (L3 override wins)
    weather = L3.get("weather_uptime_factor")
    if weather is None: weather = vget(ops, "weather_uptime_factor")
    season_days = L3.get("season_days") or round(365 * op_capacity * weather)
    service_hr_per_day = vget(ops, "service_window_hr_per_day")
    # cap revenue sailings/day at a believable on-demand duty cycle, not capacity-max,
    # so a boat is never assumed "full all day" (Jaideep 2026-06-19). L3-overridable.
    # LB-256: high-frequency commuter / water-shuttle archetypes sustain more
    # sailings/day than the premium on-demand default cap. Per-corridor L3 wins;
    # else an archetype-keyed cap; else the global default cap.
    max_tpd = L3.get("max_trips_per_day")
    if max_tpd is None:
        _tpd_map = ops.get("max_trips_per_day_by_archetype") or {}
        if seg in _tpd_map and not str(seg).startswith("_"):
            max_tpd = _tpd_map[seg]
        else:
            max_tpd = vget(ops, "max_trips_per_day")
    trips_per_day_capacity = math.floor(service_hr_per_day / cycle_hr) if cycle_hr > 0 else 0
    trips_per_day = min(trips_per_day_capacity, max_tpd)
    trips_per_day_capped = trips_per_day < trips_per_day_capacity
    # revenue-leg factor: not every theoretical leg earns full fare (deadhead/idle/gaps)
    rev_leg = L3.get("revenue_leg_factor")
    if rev_leg is None: rev_leg = vget(ops, "revenue_leg_factor")
    trips_per_year_theoretical = trips_per_day * season_days
    trips_per_year = round(trips_per_year_theoretical * rev_leg)

    pax_cap = vget(v, "pax_capacity")
    load = L3.get("load_factor")
    if load is None: load = vget(ops, "load_factor_default")
    pax_per_trip = pax_cap * load
    pax_per_year = pax_per_trip * trips_per_year

    # ---- REVENUE (needs L3 comparable fare) ----
    fare = L3.get("comparable_fare_usd_pax")
    # LB-255 (decision B): a subsidized public-transit fare is not the comparable a
    # premium on-demand product prices against. Re-fare such corridors up to the
    # premium on-demand floor; genuine premium scheduled fares above the ceiling are
    # left untouched. Price-parity (disc=1.0) still applies on the corrected comparable.
    refare = ops.get("premium_refare") or {}
    fare_refared = False; fare_original = fare
    if refare.get("enabled") and fare is not None:
        _ceil = vget(refare, "subsidized_fare_ceiling")
        _floor = vget(refare, "premium_ondemand_floor")
        if fare <= _ceil and fare < _floor:
            fare = _floor
            fare_refared = True
            flags.append("PREMIUM_REFARE:subsidized_comparable_lifted")
    # L3 explicit discount_factor wins; else segment default; else 0.6
    if L3.get("discount_factor") is not None:
        disc = L3["discount_factor"]
    elif seg in ops["discount_factor"]:
        disc = vget(ops, "discount_factor", seg)
    else:
        disc = 0.6
    if fare is None:
        flags.append("NULL_revenue:no_comparable_fare")
        navier_fare = None; rev_per_year = None
    else:
        navier_fare = round(fare * disc, 2)
        rev_per_year = round(navier_fare * pax_per_year, 0)

    # ---- COST (L1 + L3 localized opex) ----
    energy_kwh_rate = L3.get("energy_usd_per_kwh")
    battery = vget(v, "battery_kwh")
    # energy per nm: full battery covers ~range_nm; approximate kWh/nm = battery/range
    kwh_per_nm = battery / vget(v, "range_nm")
    annual_kwh = kwh_per_nm * dist * 2 * 0  # placeholder; compute below properly
    annual_nm = dist * trips_per_year
    annual_kwh = kwh_per_nm * annual_nm
    if energy_kwh_rate is None:
        flags.append("NULL_energy_cost:no_local_kwh_rate")
        energy_cost = None
    else:
        energy_cost = round(annual_kwh * energy_kwh_rate, 0)

    captain = L3.get("captain_annual_usd")
    if captain is None: flags.append("NULL_captain_cost:no_local_wage")
    # full crew, not a single captain: a captain can't cover 7 days/wk + relief/leave.
    crew = round(captain * vget(ops, "crew_fte_factor"), 0) if captain is not None else None
    overhead = L3.get("marina_overhead_annual_usd")
    if overhead is None: flags.append("NULL_overhead:no_local_marina_fee")
    maint = vget(v, "annual_maintenance_usd")
    # Regional capex override (e.g. SEA/Grab at $600K vs global $900K). L3 wins.
    capex = L3.get("capex_usd_override") if L3.get("capex_usd_override") is not None else vget(v, "capex_usd")
    dep_years = vget(v, "depreciation_years")
    depreciation = capex / dep_years
    # insurance (H&M+P&I) scales with capex; charging/berth is ADDITIONAL to marina+energy.
    # platform/commission fees are deliberately excluded (Jaideep 2026-06-19).
    insurance = round(capex * vget(ops, "insurance_pct_of_capex"), 0)
    charging_berth = L3.get("charging_berth_annual_usd")
    if charging_berth is None: charging_berth = vget(ops, "charging_berth_annual_usd")

    opex_parts = [energy_cost, crew, overhead, maint, insurance, charging_berth]
    if any(p is None for p in opex_parts):
        annual_opex = None
    else:
        annual_opex = round(sum(opex_parts), 0)

    # ---- P&L ----
    if rev_per_year is None or annual_opex is None:
        ebitda = None; margin = None; payback_yr = None
    else:
        ebitda = round(rev_per_year - annual_opex, 0)
        margin = round(ebitda / rev_per_year, 3) if rev_per_year else None
        net_after_dep = ebitda - depreciation
        payback_yr = round(capex / ebitda, 2) if ebitda > 0 else None

    # ---- CARBON (vs diesel speedboat comparable) ----
    nm_per_gal = vget(v, "diesel_comparable_nm_per_gal")
    diesel_gal = annual_nm / nm_per_gal
    diesel_co2 = diesel_gal * vget(car, "diesel_kg_co2_per_gal")
    grid_rate = L3.get("grid_kg_co2_per_kwh") or vget(car, "grid_kg_co2_per_kwh_default")
    navier_co2 = annual_kwh * grid_rate
    co2_saved_t = round((diesel_co2 - navier_co2) / 1000.0, 1)

    # ---- LENS 2: top-down demand sizing ----
    da = L3.get("demand_arrivals_rides_yr")
    df = L3.get("demand_ferry_rides_yr")
    pool_vals = [x for x in (da, df) if x]
    capture = vget(ops, "navier_capture_rate")
    # --- DORMANT archetype-scoped capture override (default OFF -> byte-identical) ---
    # Captive resort-transfer archetypes (airport->resort) have no competing operator;
    # Navier IS the transfer fleet -> capture ~= 100%, not 10%. Gated by capture_override_enabled
    # (default false in vessel-constants.json) so all current partners are unchanged until
    # Jaideep approves option A. See MALDIVES-JIH-CAPTURE-DECISION.md.
    if ops.get("capture_override_enabled"):
        # A′ (preferred): explicit per-corridor captive flag wins — sole-operator
        # water-access-only transfer. Falls back to archetype map (blanket A) only if
        # no per-corridor flag is set. Both inert until capture_override_enabled=true.
        if corridor.get("captive") is True:
            _cc = ops.get("captive_capture_rate")
            capture = (_cc["value"] if isinstance(_cc, dict) else _cc) if _cc is not None else capture
        elif corridor.get("captive") is False:
            pass  # explicitly contested -> keep global 10%
        else:
            _ovmap = ops.get("navier_capture_rate_by_archetype") or {}
            _arche = corridor.get("_archetype_raw") or corridor.get("archetype")
            if _arche in _ovmap:
                _ov = _ovmap[_arche]
                capture = _ov["value"] if isinstance(_ov, dict) else _ov
    # --- LB-103: pool_basis-aware capture (fixes double/triple discounting) ---
    # "capture_applied": sourced pool ALREADY includes a capture/penetration assumption
    #   (e.g. SG modal-shift rows at documented 0.1-0.25% commuter capture) -> capture=1.0.
    # "addressable": sourced pool already narrowed gross->premium-addressable slice ->
    #   use capture_on_addressable (0.25) instead of the gross-pool 10% default.
    # Untagged rows (gross revealed pools) keep the conservative 10% default.
    _pb = L3.get("pool_basis")
    if _pb == "capture_applied":
        capture = 1.0
    elif _pb == "addressable":
        _ca = ops.get("capture_on_addressable")
        if _ca is not None:
            capture = _ca["value"] if isinstance(_ca, dict) else _ca
    if not pool_vals:
        flags.append("NULL_demand:no_pool")
        vessels_supported = None; market_rev = None; market_co2 = None
        vessels_supported_raw = None; market_rev_raw = None; market_co2_raw = None
    else:
        pool = sum(pool_vals)/len(pool_vals)   # average the two proxies
        navier_rides = pool * capture
        vessels_supported = math.floor(navier_rides / pax_per_year) if pax_per_year else None
        market_rev = round(rev_per_year * vessels_supported, 0) if (rev_per_year and vessels_supported) else None
        market_co2 = round(co2_saved_t * vessels_supported, 1) if vessels_supported else None
        # --- UNFLOORED fractional (R-FLOOR-2): for captive resort/atoll CLUSTERS one
        # Navier fleet is shared across all the cluster's corridors, so the honest fleet
        # is the network-summed fractional need rounded ONCE at market level, not the sum
        # of per-corridor floors (which zeroes thin-but-real resort legs). aggregate.py
        # uses these *_raw fields only for markets flagged fleet_basis="network_sum";
        # contested public-crossing markets keep the conservative per-corridor floor.
        vessels_supported_raw = (navier_rides / pax_per_year) if pax_per_year else None
        market_rev_raw = (rev_per_year * vessels_supported_raw) if (rev_per_year and vessels_supported_raw) else None
        market_co2_raw = (co2_saved_t * vessels_supported_raw) if vessels_supported_raw else None

    return {
        "corridor": f"{corridor['from']} -> {corridor['to']}",
        "route_id": corridor.get("route_id"),
        "distance_nm": dist, "segment": seg, "vessel": v["label"],
        "trips_per_day": trips_per_day, "trips_per_year": trips_per_year,
        "pax_per_trip": round(pax_per_trip,2), "pax_per_year": round(pax_per_year,0),
        "comparable_fare_usd": fare, "discount": disc, "navier_fare_usd": navier_fare,
        "fare_refared": fare_refared, "fare_original_usd": fare_original,
        "revenue_per_boat_yr": rev_per_year,
        "annual_opex": annual_opex, "depreciation": round(depreciation,0),
        "ebitda_per_boat_yr": ebitda, "margin": margin, "payback_years": payback_yr,
        "co2_saved_t_per_boat_yr": co2_saved_t,
        # --- ADDITIVE breakdown components (Gold #47, Claude P2 econ-modal) ---
        # Purely additive: existing fields/values are byte-unchanged. Powers the
        # in-app per-boat breakdown modal (revenue_build / run_cost / result).
        "cost_components": {
            "energy_usd_yr": energy_cost,
            "crew_usd_yr": crew,
            "marina_overhead_usd_yr": overhead,
            "maintenance_usd_yr": maint,
            "insurance_usd_yr": insurance,
            "charging_berth_usd_yr": charging_berth,
            "depreciation_usd_yr": round(depreciation, 0),
        },
        "revenue_inputs": {
            "pax_capacity": pax_cap,
            "load_factor": load,
            "annual_nm": round(annual_nm, 0),
            "annual_kwh": round(annual_kwh, 0),
        },
        # --- ADDITIVE assumptions block (Gold #51, Claude P3 corridor-card transparency) ---
        # Surfaces the operating assumptions ALREADY used above (no re-derivation) so the
        # front end can show we are NOT assuming 100% occupancy 365 days a year.
        "assumptions": {
            "one_way_min": round(one_way_hr * 60, 1),
            "turnaround_min": round(turn_hr * 60, 1),
            "boarding_dwell_min": round(dwell_hr * 60, 1),
            "cycle_min": round(cycle_hr * 60, 1),
            "service_window_h": service_hr_per_day,
            "trips_per_day": trips_per_day,
            "trips_per_day_capacity": trips_per_day_capacity,
            "max_trips_per_day_cap": max_tpd,
            "trips_per_day_capped": trips_per_day_capped,
            "trips_per_day_derivation": (
                (f"min(cap {max_tpd}, " if trips_per_day_capped else "")
                + f"floor({service_hr_per_day}h service window / {round(cycle_hr*60,1)}min cycle "
                f"[{round(one_way_hr*60,1)}min one-way + {round(turn_hr*60,1)}min turnaround "
                f"+ {round(dwell_hr*60,1)}min boarding])"
                + (f") = {trips_per_day}" if trips_per_day_capped else f" = {trips_per_day}")
                + " legs/day"),
            "operating_days_yr": season_days,
            "operating_days_derivation": ("L3 season_days override" if L3.get("season_days")
                                          else f"365 x {op_capacity} mechanical uptime x {weather} weather"),
            "mechanical_uptime": op_capacity,
            "weather_factor": weather,
            "revenue_leg_pct": rev_leg,
            "load_factor": load,
            "pax_capacity": pax_cap,
        },
        "demand_confidence": L3.get("demand_confidence"),
        "vessels_supported_10pct": vessels_supported,
        "market_revenue_yr": market_rev, "market_co2_saved_t_yr": market_co2,
        "vessels_supported_raw": vessels_supported_raw,
        "market_revenue_yr_raw": market_rev_raw, "market_co2_saved_t_yr_raw": market_co2_raw,
        "flags": flags,
    }

def main():
    results=[]
    for mid, mk in CORR["markets"].items():
        for c in mk["corridors"]:
            if not c.get("in_phase1_shuttle"): continue
            r = compute_atom(c)
            r["market"]=mid
            results.append(r)
    # print compact
    print(f"{'market':9} {'corridor':46} {'nm':>3} {'rev/boat':>10} {'margin':>7} {'payback':>8} {'CO2t':>6} {'flags'}")
    for r in results:
        rev = f"${r['revenue_per_boat_yr']:,.0f}" if r['revenue_per_boat_yr'] else "—"
        mg  = f"{r['margin']*100:.0f}%" if r['margin'] is not None else "—"
        pb  = f"{r['payback_years']}y" if r['payback_years'] else "—"
        nf  = "" if not r['flags'] else f"[{len(r['flags'])} null]"
        print(f"{r['market']:9} {r['corridor'][:46]:46} {r['distance_nm']:>3} {rev:>10} {mg:>7} {pb:>8} {r['co2_saved_t_per_boat_yr']:>6} {nf}")
    if "--json" in sys.argv:
        path = sys.argv[sys.argv.index("--json")+1]
        json.dump(results, open(path,"w"), indent=2, ensure_ascii=False)
        print("wrote", path)

if __name__=="__main__":
    main()
