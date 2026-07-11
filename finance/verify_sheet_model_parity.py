#!/usr/bin/env python3
"""Verify transparent-sheet formula semantics match aggregate.py (Python half-even).

Checks:
  - trips/year half-even vs agg mid for every engine route
  - revenue/boat and market_rev for grounded rows
  - rollup SOM floor equals agg rollup.grounded_floor.market_rev_yr

Does NOT mutate sources. Use after patching build_transparent_sheet.py.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE / "model"
RECAL = HERE / "recal"


def v(n):
    return n["value"] if isinstance(n, dict) and "value" in n else n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", required=True)
    ap.add_argument("--corridors", default=None)
    ap.add_argument("--agg", default=None)
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args()

    partner = args.partner
    corr_path = Path(args.corridors or RECAL / f"corridors-{partner}.json")
    if not corr_path.is_file():
        corr_path = MODEL / "corridors.json"
    agg_path = Path(args.agg or RECAL / f"agg-{partner}.json")

    const = json.loads((MODEL / "vessel-constants.json").read_text())
    OPS = const["operating_defaults"]
    P2 = const["vessels"]["pioneer_ii"]
    range_nm = v(P2["range_nm"])
    cruise = v(P2["cruise_speed_kt"])
    service_hr = v(OPS["service_window_hr_per_day"])
    turn_min = v(OPS["turnaround_charge_min"])
    dwell = v(OPS["boarding_dwell_min"])
    max_tpd = v(OPS["max_trips_per_day"])
    tpd_map = OPS.get("max_trips_per_day_by_archetype") or {}
    mech = v(OPS["monthly_operational_capacity"])
    pax_cap = v(P2["pax_capacity"])
    load = OPS["_utilization_scenarios"]["mid"]["load_factor"]
    revleg = OPS["_utilization_scenarios"]["mid"]["revenue_leg_factor"]
    disc_map = OPS.get("discount_factor") or {}
    capt_rate = v(OPS["navier_capture_rate"])
    capt_on_addr = OPS.get("capture_on_addressable")
    capt_on_addr = v(capt_on_addr) if capt_on_addr is not None else capt_rate

    # LB-255 premium re-fare (mirror build_transparent_sheet / atom)
    REFARE_ON = True
    REFARE_CEIL = 8.0
    REFARE_FLOOR = 18.0

    corr = json.loads(corr_path.read_text())
    agg = json.loads(agg_path.read_text())
    agg_by = {}
    for r in agg.get("rows") or []:
        if r.get("is_dup"):
            continue
        rid = r.get("route_id")
        if rid:
            agg_by[rid] = r

    rows_checked = []
    mismatches = []
    sim_floor = 0.0
    sim_pool = 0.0

    for mid, mk in (corr.get("markets") or {}).items():
        if mk.get("partner", "grab") != partner and partner != "global":
            # scoped file is partner-only; canonical filters
            if Path(corr_path).name == "corridors.json" and mk.get("partner") != partner:
                continue
        for c in mk.get("corridors") or []:
            if c.get("_economics_hold_reason") or c.get("_premium_cascade") or c.get("_dup_of"):
                continue
            rid = c.get("route_id")
            nm = c.get("distance_nm")
            if nm is None or nm > range_nm:
                continue
            L3 = c.get("L3_locals") or {}
            arche = c.get("archetype") or "intercity"
            disc = disc_map.get(arche, disc_map.get("intercity", 1.0))
            if isinstance(disc, dict):
                disc = v(disc)
            if disc is None:
                disc = 1.0
            eff_cap = (
                tpd_map[arche]
                if arche in tpd_map and not str(arche).startswith("_")
                else max_tpd
            )
            ow = 60 * nm / cruise
            cyc = ow + turn_min + dwell
            tpd = min(eff_cap, math.floor(60 * service_hr / cyc) if cyc else 0)
            season = L3.get("season_days")
            if season is None:
                w = L3.get("weather_uptime_factor")
                w = 1.0 if w is None else w
                od = round(365 * mech * w)
            else:
                od = season
            tpy = round(tpd * od * revleg)

            fare = L3.get("comparable_fare_usd_pax")
            if fare is not None and REFARE_ON and fare <= REFARE_CEIL and fare < REFARE_FLOOR:
                fare = REFARE_FLOOR
            nf = (fare or 0) * disc
            ppt = pax_cap * load
            ppy = ppt * tpy
            rev = round(nf * ppy, 0)

            # demand pool
            da = L3.get("demand_arrivals_rides_yr")
            df = L3.get("demand_ferry_rides_yr")
            pool_vals = [x for x in (da, df) if x]
            demand = (
                sum(pool_vals) / len(pool_vals)
                if pool_vals
                else L3.get("corridor_annual_oneway_pax")
            )
            # capture mirror (simplified)
            cap = capt_rate
            pb = L3.get("pool_basis")
            if pb == "capture_applied":
                cap = 1.0
            elif pb == "addressable":
                cap = capt_on_addr
            if L3.get("navier_capture_override") is not None:
                cap = L3["navier_capture_override"]
            if c.get("captive") is True and OPS.get("capture_override_enabled"):
                cc = OPS.get("captive_capture_rate")
                if cc is not None:
                    cap = v(cc)

            nrd = (demand or 0) * cap if demand is not None else None
            vessels = math.floor(nrd / ppy) if (nrd is not None and ppy) else 0
            mrev = round(rev * vessels, 0) if vessels else 0
            vraw = (nrd / ppy) if (nrd is not None and ppy) else 0
            mrev_raw = vraw * (nf * ppy)  # unrounded per-boat revenue

            ar = agg_by.get(rid) or {}
            midr = ar.get("mid") or {}
            rec = {
                "route_id": rid,
                "corridor": f"{c.get('from')} → {c.get('to')}",
                "sim": {
                    "trips_per_year": tpy,
                    "revenue_per_boat_yr": rev,
                    "vessels_supported": vessels,
                    "market_revenue_yr": mrev,
                    "market_revenue_raw": mrev_raw,
                },
                "model": {
                    "trips_per_year": midr.get("trips_per_year"),
                    "revenue_per_boat_yr": midr.get("revenue_per_boat_yr"),
                    "vessels_supported": midr.get("vessels_supported"),
                    "market_revenue_yr": midr.get("market_revenue_yr")
                    or midr.get("market_rev_yr"),
                },
                "status": ar.get("status"),
            }
            for field in (
                "trips_per_year",
                "revenue_per_boat_yr",
                "vessels_supported",
                "market_revenue_yr",
            ):
                a = rec["sim"][field]
                b = rec["model"][field]
                if b is None:
                    continue
                if a != b and abs(float(a or 0) - float(b or 0)) > 0.51:
                    mismatches.append(
                        {"route_id": rid, "field": field, "sim": a, "model": b}
                    )
            if ar.get("status") == "grounded":
                sim_floor += mrev
                if demand is not None and fare is not None:
                    # pool uses comparable fare (pre-discount) × demand one-way
                    # match growth: demand * fare (model comparable)
                    base_fare = L3.get("comparable_fare_usd_pax")
                    if base_fare is not None and REFARE_ON and base_fare <= REFARE_CEIL and base_fare < REFARE_FLOOR:
                        base_fare = REFARE_FLOOR
                    sim_pool += demand * (base_fare or 0)
            rows_checked.append(rec)

    model_floor = agg["rollup"]["grounded_floor"]["market_rev_yr"]
    model_pool = agg["rollup"]["grounded_floor"]["transport_spend_pool_yr"]
    report = {
        "partner": partner,
        "n_routes_checked": len(rows_checked),
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:50],
        "sim_grounded_floor": sim_floor,
        "model_grounded_floor": model_floor,
        "floor_delta": sim_floor - model_floor,
        "model_pool": model_pool,
        "four_tie_routes_tpy": {
            rid: next(
                (
                    r["sim"]["trips_per_year"]
                    for r in rows_checked
                    if r["route_id"] == rid
                ),
                None,
            )
            for rid in (
                "rn-79388bf546a1",
                "rn-b93989547df9",
                "rn-649a78c56f95",
                "rn-ba28d38bee02",
            )
        },
        "pass": len(mismatches) == 0
        and abs(sim_floor - model_floor) < 0.51
        and all(
            rows_checked
            and any(
                r["route_id"] == rid and r["sim"]["trips_per_year"] == 890
                for r in rows_checked
            )
            for rid in (
                "rn-79388bf546a1",
                "rn-b93989547df9",
                "rn-649a78c56f95",
                "rn-ba28d38bee02",
            )
            if partner == "swing"
        ),
    }
    # For non-swing, don't require four-tie routes
    if partner != "swing":
        report["pass"] = len(mismatches) == 0 and abs(sim_floor - model_floor) < 0.51

    text = json.dumps(report, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n")
    print(text)
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
