#!/usr/bin/env python3
"""Build a source-backed South Korea 65% midpoint scenario from retained evidence.

This is an audit/scenario builder, not a production cascade. It reads the live Swing
workbook, the retained aggregate (for exact route IDs), and the fare evidence ledger.
"""
from __future__ import annotations
import json, math, re
from pathlib import Path
import pandas as pd

ROOT = Path('/tasklet/agent/home')
WORKBOOK = ROOT / 'post-224-verification/swing-live.xlsx'
AGG = ROOT / 'six-deck-refresh/source/agg-swing.json'
EVIDENCE = ROOT / 'south-korea-economics-review/KOREA-PREMIUM-FARE-EVIDENCE-2026-07-11.json'
OUT = ROOT / 'south-korea-economics-review'

SERVICE_MIN = 12 * 60
TURNAROUND_MIN = 20
BOARDING_DWELL_MIN = 10
OPERATING_DAYS = 274
REVENUE_LEG_PCT = 0.65
LOAD_FACTOR = 0.65
PAX_CAPACITY = 8
SPEED_KT = 20
PUBLISHED_RANGE_NM = 70
PUBLISHED_DC_FAST_CHARGE_MIN = 45
CAPEX_USD = 600_000


def norm(s: str) -> str:
    s = str(s).replace('→', '->').replace('—', '-').lower()
    return re.sub(r'[^a-z0-9]+', '', s)


def market_for(corridor: str) -> str:
    s = corridor.lower()
    if 'busan' in s and 'geoje' in s:
        return 'geoje'
    if 'busan' in s:
        return 'busan'
    if any(x in s for x in ('incheon', 'yeongjong', 'muuido', 'gimpo')):
        return 'incheon'
    if any(x in s for x in ('seoul', 'yeouido', 'jamsil', 'ttukseom', 'oksu', 'apgujeong')):
        return 'seoul'
    if any(x in s for x in ('jeju', 'udo', 'seogwipo', 'seongsan', 'jongdal')):
        return 'jeju'
    if 'yeosu' in s:
        return 'yeosu'
    return 'tongyeong'


def charter_price_krw(evidence: dict, market: str, one_way_min: float) -> float:
    rec = evidence['markets'][market]
    if market == 'jeju':
        minimum_price = rec['normalized_eight_rider_whole_vessel_krw']
    else:
        minimum_price = rec['whole_vessel_krw']
    minimum_min = rec['minimum_minutes']
    if 'higher_block_whole_vessel_krw' in rec:
        if one_way_min <= minimum_min:
            return minimum_price
        higher_price = rec['higher_block_whole_vessel_krw']
        higher_min = rec['higher_block_minutes']
        if one_way_min <= higher_min:
            return higher_price
        return higher_price * one_way_min / higher_min
    return minimum_price * max(1.0, one_way_min / minimum_min)


def main() -> None:
    evidence = json.loads(EVIDENCE.read_text())
    fx = evidence['normalization']['fx_krw_per_usd']
    average_riders = PAX_CAPACITY * LOAD_FACTOR
    raw = pd.read_excel(WORKBOOK, sheet_name='Corridor economics', header=None)
    headers = raw.iloc[2].tolist()
    wb = raw.iloc[3:].copy()
    wb.columns = headers
    wb = wb[(wb['Corridor'].notna()) & (wb['Country'] == 'South Korea')].reset_index(drop=True)

    agg = json.loads(AGG.read_text())
    id_by_corridor = {norm(r['corridor']): r['route_id'] for r in agg['rows']}

    # Preserve current Korean production-cost inputs from the live workbook.
    base = wb.iloc[0]
    crew = float(base['Crew/yr'])
    port = float(base['Berth & port admin/yr'])
    maint = float(base['Maint/yr'])
    insurance = float(base['Vessel insurance/yr'])
    charge_berth = float(base['Fast-charge berth/yr'])
    energy_usd_per_nm = float(base['Energy/yr']) / (float(base['Distance']) * float(base['Trips/yr']))

    rows = []
    for _, r in wb.iterrows():
        corridor = str(r['Corridor'])
        nm = float(r['Distance'])
        one_way_min = nm / SPEED_KT * 60
        # Energy-proportional charging proxy: recover each leg's fraction of the
        # published 70-nm range at the published 45-minute DC fast-charge rate.
        # This keeps charging visible without charging a full 45 minutes per leg.
        charge_recovery_min = nm / PUBLISHED_RANGE_NM * PUBLISHED_DC_FAST_CHARGE_MIN
        cycle_min = one_way_min + TURNAROUND_MIN + BOARDING_DWELL_MIN + charge_recovery_min
        gross_legs_day = math.floor(SERVICE_MIN / cycle_min)
        revenue_legs_year = round(gross_legs_day * OPERATING_DAYS * REVENUE_LEG_PCT)
        market = market_for(corridor)
        charter_krw = charter_price_krw(evidence, market, one_way_min)
        fare = charter_krw / average_riders / fx
        pax_year = revenue_legs_year * average_riders
        revenue = pax_year * fare
        annual_nm = revenue_legs_year * nm
        energy = annual_nm * energy_usd_per_nm
        opex = crew + port + maint + insurance + charge_berth + energy
        ebitda = revenue - opex
        payback = CAPEX_USD / ebitda if ebitda > 0 else None
        target_fare = (opex + CAPEX_USD / 3) / pax_year if pax_year else None
        rows.append({
            'route_id': id_by_corridor.get(norm(corridor)),
            'corridor': corridor,
            'market_benchmark': market,
            'distance_nm': nm,
            'one_way_min': round(one_way_min, 1),
            'cycle_min': round(cycle_min, 1),
            'gross_legs_per_day': gross_legs_day,
            'revenue_leg_utilization': REVENUE_LEG_PCT,
            'revenue_legs_per_year': revenue_legs_year,
            'seat_occupancy': LOAD_FACTOR,
            'pax_per_revenue_leg': average_riders,
            'charter_benchmark_krw': round(charter_krw),
            'fare_equivalent_usd_per_rider': round(fare, 2),
            'annual_revenue_usd': round(revenue),
            'annual_opex_usd': round(opex),
            'ebitda_usd': round(ebitda),
            'payback_years': round(payback, 2) if payback is not None else None,
            'fare_needed_for_3yr_payback_usd': round(target_fare, 2) if target_fare is not None else None,
            'under_3yr_payback': bool(payback is not None and payback < 3),
            'production_status': 'candidate' if payback is not None and payback < 3 else 'held',
        })
    out = pd.DataFrame(rows)
    if out['route_id'].isna().any():
        missing = out.loc[out['route_id'].isna(), 'corridor'].tolist()
        raise SystemExit(f'Exact route-ID match failed: {missing}')

    csv_path = OUT / 'KOREA-ROUTE-SCHEDULE-SCENARIO-2026-07-11.csv'
    json_path = OUT / 'KOREA-ROUTE-SCHEDULE-SCENARIO-2026-07-11.json'
    out.to_csv(csv_path, index=False)
    summary = {
        'as_of': '2026-07-11',
        'scenario_status': 'source-backed audit scenario; not production-cascaded',
        'route_count': len(out),
        'profitable_route_count': int((out['ebitda_usd'] > 0).sum()),
        'under_3yr_route_count': int(out['under_3yr_payback'].sum()),
        'held_route_count': int((~out['under_3yr_payback']).sum()),
        'gross_legs_per_day_min': int(out['gross_legs_per_day'].min()),
        'gross_legs_per_day_max': int(out['gross_legs_per_day'].max()),
        'gross_legs_per_day_median': float(out['gross_legs_per_day'].median()),
        'inputs': {
            'service_window_h': 12,
            'speed_kt': SPEED_KT,
            'turnaround_min': TURNAROUND_MIN,
            'boarding_dwell_min': BOARDING_DWELL_MIN,
            'revenue_leg_utilization': REVENUE_LEG_PCT,
            'seat_occupancy': LOAD_FACTOR,
            'operating_days': OPERATING_DAYS,
            'capex_usd': CAPEX_USD,
            'crew_usd_yr': crew,
            'port_usd_yr': port,
            'maintenance_usd_yr': maint,
            'insurance_usd_yr': insurance,
            'fast_charge_berth_usd_yr': charge_berth,
            'energy_usd_per_nm': energy_usd_per_nm,
        },
        'important_limits': [
            'The 15-leg cap is removed; gross legs/day are floor(720 / (one-way run time + 20-minute turnaround + 10-minute boarding dwell + energy-proportional charge recovery)).',
            'Revenue-leg utilization remains separately visible at 65%; it is not merged into seat occupancy.',
            '65% seat occupancy means 5.2 riders per revenue leg on an eight-seat N30.',
            'Port, Korean wages, maintenance, insurance, charge-berth cost and energy inputs are retained from the live workbook.',
            'Fare inputs are premium local whole-vessel marine analogs normalized to the modeled 5.2 riders, not exact canonical-OD fares; even sub-three-year rows require route-level pricing validation before production.',
            'Charging is not yet a route-cycle time penalty. Energy feasibility and charger availability require engineering confirmation before production.',
            'Only rows with payback under three years are production candidates; other rows remain held rather than forced through unsupported assumptions.'
        ],
        'routes': rows,
    }
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k not in ('routes', 'inputs', 'important_limits')}, indent=2))


if __name__ == '__main__':
    main()
