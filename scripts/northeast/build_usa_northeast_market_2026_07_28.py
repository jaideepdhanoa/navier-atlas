#!/usr/bin/env python3
"""Northeast USA Phase 2 — country row + market entries (Jaideep-approved anchors 2026-07-27).

Adds to a navier-atlas checkout (arg1, default /tmp/na):
  1. country-reference.json: "United States" row (T1/T2 evidence; berth = Jaideep-approved
     flagged estimate pending written quotes).
  2. corridors.json: markets `usa-ny-harbor` + `usa-new-england` (partner: uber = canonical
     owner; Lyft/Blade/Hornblower/authority decks inherit scoped views, corridor-inheritance rule).
Evidence: /tasklet/agent/home/northeast-program/census/*.md
Run: python3 build_usa_northeast_market_2026_07_28.py [repo] [--apply]
"""
import json, sys, shutil

REPO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '/tmp/na'
APPLY = '--apply' in sys.argv

CEN = '/tasklet/agent/home/northeast-program/census'

US_ROW = {
  "captain_usd_yr": {
    "value": 203000, "source_tier": "T2", "confidence": "med",
    "source": ("BLS OEWS May-2023: 53-5021 Captains/Mates/Pilots mean annual NY-Newark-Jersey City "
      "$102,500, Boston-Cambridge-Nashua $69,240; 53-5011 Sailors/Marine Oilers NY $65,510, Boston "
      "$43,030 (bls.gov/oes/2023/may/oes_35620.htm, oes_71650.htm). Formula: 1 captain + 1 deckhand, "
      "50/50 NY/Boston market blend = wages $140,140/vessel/yr x 1.4521 BLS ECEC benefits load "
      "(private transportation/material-moving: total comp $35.81/hr vs wages $24.66/hr, Mar-2026 "
      "release) = $203,497 -> anchored $203,000. Highest-wage market in the reference (US Northeast "
      "unionized marine labor). Evidence: COST-POLICY-CENSUS.md + COST-GAPFILL-PASS2.md."),
  },
  "energy_usd_kwh": {
    "value": 0.21, "source_tier": "T1", "confidence": "med-high",
    "source": ("Con Edison small-business TOU observed Jul-2026: off-peak energy $0.0199/kWh + "
      "delivery $0.2038 (summer) / $0.1719 (other) per kWh + $34/mo customer charge "
      "(coned.com time-of-use). Overnight off-peak charging basis: 0.0199 + blended delivery "
      "~0.19 = ~$0.21/kWh EXCLUDING demand charges (marina tariff class/demand charges unquoted "
      "- flagged). Eversource MA commercial tariff not verified this pass; Con Ed basis applied "
      "as the conservative Northeast anchor. Evidence: COST-POLICY-CENSUS.md S9/S10."),
  },
  "grid_co2_kg_kwh": {
    "value": 0.32, "source_tier": "T1", "confidence": "high",
    "source": ("EPA eGRID 2023 subregion total output CO2 rates: NYCW (NYC/Westchester) 864.469 "
      "lb/MWh = 0.392 kg/kWh; NEWE (New England) 539.275 lb/MWh = 0.245 kg/kWh (epa.gov/egrid "
      "summary data). Fleet-weighted 50/50 NY/New England blend = 0.318 -> anchored 0.32. "
      "Upstate NY (NYUP 242 lb/MWh) not used - fleet charges downstate. Evidence: COST-GAPFILL-PASS2.md."),
  },
  "marina_overhead_usd_yr": {
    "value": 36000, "source_tier": "T5", "confidence": "low",
    "source": ("FLAGGED ESTIMATE - Jaideep-approved flagged estimate line 2026-07-27 pending written "
      "commercial berth quotes (dockage tariffs fail-closed across NYC/Boston premium facilities). "
      "Published bounds: Town of Barnstable 2026 rate card (T1 municipal) 30-ft commercial "
      "$1.75/ft/day May-Oct + $8/ft/mo Nov-Apr = $11,100/yr floor; Nantucket Boat Basin published "
      "high-season transient $12.00-13.25/ft/night = $34,440-38,028 for 82 nights (seasonal only). "
      "NYC/Boston premium commercial berth + insurance + admin modeled $36,000/vessel/yr between "
      "these bounds; above UAE $22k - US Northeast is the most expensive berth market in the "
      "reference. Replace with quotes before any operating commitment. Evidence: COST-GAPFILL-PASS2.md."),
  },
  "cost_index": {
    "value": 1.95, "confidence": "med-low",
    "source": ("Relative to Singapore=1.00. R7 two-sided: crew ~4.2x SG nominal (blended loaded crew "
      "$203k vs SG $48k captain-anchor - basis mismatch noted, SG row is captain-lean); commercial "
      "electricity ~1.0x SG ($0.21 vs $0.21); World Bank 2025 US price level ~1.5x SG. Wage-dominant "
      "blend (50% crew / 25% energy / 25% price level) = 1.95. Highest cost index in the reference - "
      "US Northeast is the most expensive operating environment modeled. T3 modeled; evidence: "
      "COST-GAPFILL-PASS2.md section 4."),
  },
}

PREMIUM_BASIS = ("Premium-substitute benchmarking (Jaideep override Jul-2026; anchors approved "
  "2026-07-27): Uber Black computed/flat fares, Blade by-the-seat air, and incumbent premium fast-ferry "
  "tariffs per corridor _fare_record. Evidence: FARE-ANCHOR-PROPOSAL.md + census/FARES-*.md.")

def corr(frm, to, nm, vessel, rid, bps, fare, fare_src, pool, dem, floor=True, phase1=True, extra=None):
    d = {
      "from": frm, "to": to, "distance_nm": nm, "vessel": vessel, "route_id": rid,
      "country": "United States",
      "archetype": "ridehail",
      "service_status": "current_scheduled",
      "in_phase1_shuttle": phase1, "_in_grounded_floor": floor,
      "_source": "usa-northeast-t1-2026-07-28",
      "L3_locals": {
        "corridor_annual_oneway_pax": pool,
        "comparable_fare_usd_pax": fare,
        "pool_basis": "gross",
        "_demand_record": dem,
        "_fare_record": fare_src,
      },
    }
    if bps: d["endpoint_boarding_points"] = bps
    if extra: d.update(extra)
    return d

def dem(value, year, tier, conf, source, method):
    return {"value": value, "unit": "one-way passenger-trips/year (pool basis per method)",
            "year": year, "source_tier": tier, "confidence": conf, "source": source, "method": method}

def fare(value, source, method):
    return {"value": value, "unit": "USD/pax/one-way premium anchor (Jaideep-approved 2026-07-27)",
            "year": 2026, "source_tier": "T2", "confidence": "med", "source": source, "method": method}

NY = {
  "display_name": "USA \u00b7 New York Harbor + East End",
  "partner": "uber", "country": "United States", "country_slug": "united-states",
  "currency": "USD", "scope": "NY Harbor T1 corridors + Manhattan\u2194East End long-haul (approved anchor table 2026-07-27)",
  "archetype": "ridehail", "_tier": "T1_grounded",
  "_source": "Northeast USA program Phase 0 census 2026-07-27 (/tasklet/agent/home/northeast-program/census/)",
  "_premium_fare_basis": PREMIUM_BASIS,
  "corridors": [
    corr("East 34th Street (Manhattan)", "LGA Marine Air Terminal (Bowery Bay)", 5.9, "Pioneer II",
      "rn-0e2b916d3b8d", {"from": "bp-5f0981ff77", "to": "bp-lga-marine-air"}, 75.0,
      fare(75.0, "Uber Black JFK\u2194Manhattan flat $85; NYC black-car guides $100-150 (FARES-PASS2)",
        "Anchored below the JFK Uber Black flat for the shorter LGA run; premium door-to-door substitute."),
      1387826,
      dem(1387826, 2023, "T1", "med-high",
        "NYC TLC trip records CY2023 (Yellow+Green+non-HVFHV FHV), LGA zone 138 \u2194 Manhattan filter (DEMAND-GAPFILL-PASS3.md)",
        "Count of licensed taxi/FHV trips between LGA and Manhattan. UNDERSTATED: excludes Uber/Lyft "
        "(HVFHV) trips - the majority of the for-hire market - plus all private-car access. 1 trip "
        "counted as 1 passenger (occupancy >1 uncounted). Airport context: LGA 33.63M pax 2024, 85% car-based access (PANYNJ ATR)."),
    ),
    corr("Wall Street / Pier 11 (Manhattan)", "North Williamsburg (Brooklyn)", 2.4, "Pioneer II",
      "rn-5c8ceecea4d9", {"from": "bp-58a56df431", "to": "bp-1c4d49ace6"}, 25.0,
      fare(25.0, "Uber Black computed ~$44/car Manhattan\u2194N Williamsburg (FARES-PASS2)",
        "Anchored below the per-car Uber Black quote; per-seat premium water substitute."),
      2792467,
      dem(2792467, 2024, "T1", "high",
        "NYCEDC NYC Ferry Open Data, East River (ER) route hourly boardings aggregated to CY2024 (DEMAND-GAPFILL-PASS3.md)",
        "Direct route-level sum of published ER-route boardings; East River is NYC Ferry's highest-ridership route (FY24 annual report)."),
    ),
    corr("Wall Street / Pier 11 (Manhattan)", "Paulus Hook (Jersey City)", 1.41, "Pioneer II",
      "ics-bdacfbafa1", None, 20.0,
      fare(20.0, "Uber Black computed ~$35/car Manhattan\u2194Paulus Hook (FARES-PASS2)",
        "Anchored below the per-car Uber Black quote; per-seat premium water substitute."),
      213380,
      dem(213380, 2024, "T4", "low",
        "NTD 2024: NY Waterway 4,694,357 UPT network-wide; operator publishes 22 distinct commuter routes (CAPACITY-GAPFILL.md)",
        "MODELED equal-share allocation: 4,694,357 / 22 routes = 213,380. UNDERSTATED for Paulus Hook "
        "- a flagship trans-Hudson crossing; route-level count not published. Flagged per fail-closed policy."),
    ),
    corr("Wall Street / Pier 11 (Manhattan)", "Long Wharf (Sag Harbor Village Dock)", 101.2, "Quanta-LR",
      "rn-e2c8f0d3fe0d", {"from": "bp-58a56df431", "to": "bp-505629a487"}, 295.0,
      fare(295.0, "Blade helicopter by-the-seat Manhattan\u2194Hamptons $795; Uber Black flat $400 (FARES-PASS2; Blade 10-K)",
        "Anchored between the premium ground flat ($400/car) and premium air ($795/seat)."),
      47366,
      dem(47366, 2024, "T4", "low",
        "Blade Air Mobility 2024 10-K: 94,733 Short Distance seats flown + $72.2M Short Distance revenue (RIDERSHIP-PASS3)",
        "MODELED 50% split of Blade's demonstrated premium by-the-seat air demand across the two "
        "Manhattan\u2194East End corridors (Hamptons-only split not disclosed). UNDERSTATED: excludes "
        "Hampton Jitney, LIRR premium, and private-car East End travel."),
      floor=True, phase1=False,
      extra={"_roadmap_note": "101nm leg - Quanta-LR (75-150nm gate); held from Pioneer II near-term floor by range."},
    ),
    corr("Wall Street / Pier 11 (Manhattan)", "Viking Fleet Dock \u2014 Montauk Harbor", 104.7, "Quanta-LR",
      "rn-1119113a9806", {"from": "bp-58a56df431", "to": "bp-55f162ae8f"}, 345.0,
      fare(345.0, "Blade Montauk Sky Pass $495/seat (FARES-PASS2)",
        "Anchored below the published premium air seat for the same corridor."),
      47367,
      dem(47367, 2024, "T4", "low",
        "Blade Air Mobility 2024 10-K: 94,733 Short Distance seats flown (RIDERSHIP-PASS3)",
        "MODELED 50% split of Blade premium air seats across the two East End corridors; same caveats as Sag Harbor."),
      floor=True, phase1=False,
      extra={"_roadmap_note": "105nm leg - Quanta-LR (75-150nm gate); held from Pioneer II near-term floor by range."},
    ),
  ],
}

NE = {
  "display_name": "USA \u00b7 Boston Harbor + Cape & Islands",
  "partner": "uber", "country": "United States", "country_slug": "united-states",
  "currency": "USD", "scope": "Boston Harbor + Cape Cod & Islands T1 corridors (approved anchor table 2026-07-27)",
  "archetype": "ridehail", "_tier": "T1_grounded",
  "_source": "Northeast USA program Phase 0 census 2026-07-27 (/tasklet/agent/home/northeast-program/census/)",
  "_premium_fare_basis": PREMIUM_BASIS,
  "corridors": [
    corr("Long Wharf (Boston)", "Hingham Shipyard", 9.2, "Pioneer II",
      "rn-6e97c92755a8", {"from": "bp-98fe0af19b", "to": "bp-cb7113ff22"}, 35.0,
      fare(35.0, "Uber Black computed ~$78/car Boston\u2194Hingham (FARES-PASS2); MBTA std $9.75",
        "Anchored well below the per-car Uber Black quote; per-seat premium water substitute."),
      169875,
      dem(169875, 2024, "T4", "low",
        "NTD 2024: MBTA ferry 1,359,001 UPT systemwide; MBTA lists 8 ferry routes (CAPACITY-GAPFILL.md)",
        "MODELED equal-share allocation: 1,359,001 / 8 routes = 169,875. UNDERSTATED for Hingham - "
        "the F1 Hingham run is the system's dominant route; per-route split not published. Flagged."),
    ),
    corr("Long Wharf (Boston)", "Salem Ferry Wharf", 12.34, "Pioneer II",
      "ics-3b05a4e262", None, 45.0,
      fare(45.0, "BHCC Salem fast ferry published fare ~$43 one-way (FARES-PASS2)",
        "Anchored at the incumbent premium fast-ferry tariff."),
      194296,
      dem(194296, 2026, "T2", "med-low",
        "BHCC Salem Ferry 2026: vessel Nathaniel Bowditch 149 pax (T1 operator); 4 departures/direction/day baseline; season May 22 - Oct 31 = 163 days (CAPACITY-GAPFILL.md)",
        "CAPACITY BASIS (Jaideep-approved 2026-07-27): 149 x 4 x 2 directions x 163 days = 194,296 "
        "seat-capacity/yr. Conservative: excludes the published 5th Thu-Sat sailing. Route ridership unpublished."),
    ),
    corr("Long Wharf (Boston)", "Provincetown (MacMillan Pier)", 42.86, "Pioneer II",
      "ics-4df4cecf34", None, 95.0,
      fare(95.0, "Bay State fast ferry $87-102 one-way + $5 fuel surcharge, 2026 published (BOSTON-CAPE-CENSUS S4)",
        "Anchored inside the incumbent premium fast-ferry band."),
      139464,
      dem(139464, 2026, "T2", "med-low",
        "Bay State Cruise Co 2026: Provincetown III certified 149 pax (T1); 3 departures/direction/day; season May 16 - Oct 18 = 156 days (CAPACITY-GAPFILL.md)",
        "CAPACITY BASIS (Jaideep-approved 2026-07-27): 149 x 3 x 2 x 156 = 139,464 seat-capacity/yr. "
        "Conservative: excludes BHCC's competing Provincetown service (Salacia, 600 pax) entirely."),
    ),
    corr("Long Wharf (Boston)", "Logan Airport ferry dock", 1.1, "Pioneer II",
      "rn-b1104ed2e1eb", {"from": "bp-98fe0af19b", "to": "bp-c324600173"}, 20.0,
      fare(20.0, "MBTA std $9.75; Uber Black Logan run with tolls substantially higher (FARES-PASS2)",
        "Premium anchored at ~2x the public tariff, below the premium ground substitute."),
      169875,
      dem(169875, 2024, "T4", "low",
        "NTD 2024: MBTA ferry 1,359,001 UPT systemwide across 8 published routes; Massport confirms the Logan Water Transportation Dock year-round link (BOSTON-CAPE-CENSUS S2)",
        "MODELED equal-share allocation: 1,359,001 / 8 = 169,875. Logan-route split unpublished; "
        "no double-count - each MBTA route share used at most once across this market. Flagged."),
    ),
    corr("Hyannis Terminal", "Nantucket (Steamship Wharf)", 24.1, "Pioneer II",
      "e__boston-new-england-usa__hyannis-terminal__nantucket-steamship-wharf", None, 65.0,
      fare(65.0, "Hy-Line Captain's View premium cabin $61 one-way (FARES-PASS2)",
        "Anchored just above the incumbent premium-cabin tariff."),
      544425,
      dem(544425, 2024, "T1", "high",
        "Steamship Authority 2024 traffic statistics: Nantucket route 544,425 one-way passenger passages (steamshipauthority.com/about/traffic-statistics)",
        "Route-level published figure, SSA only. UNDERSTATED: excludes Hy-Line's 928,922 operator-wide "
        "UPT (route split unpublished - flagged additional pool, not counted)."),
    ),
    corr("Woods Hole", "Vineyard Haven (Tisbury), Martha's Vineyard", 6.1, "Pioneer II",
      "ics-c7c6e76d27", None, 40.0,
      fare(40.0, "Falmouth\u2194Edgartown premium passenger boat $35-45 one-way, primary-sourced (FARES-GAPFILL)",
        "Anchored inside the premium small-boat band for the same island pair."),
      2396540,
      dem(2396540, 2024, "T1", "high",
        "Steamship Authority 2024 traffic statistics: Vineyard route 2,396,540 one-way passenger passages",
        "Route-level published figure; excludes 492,473 one-way autos (vehicle passages not counted as pax)."),
    ),
    corr("Seastreak Ferry Terminal at New Bedford", "Steamship Authority Oak Bluffs Terminal", 27.3, "Pioneer II",
      "rn-ba49e90cdbec", {"from": "bp-41b26f2bfc", "to": "bp-83a62832de"}, 50.0,
      fare(50.0, "Seastreak New Bedford\u2194Vineyard express $49 one-way (FARES-PASS2)",
        "Anchored at the incumbent premium fast-ferry tariff."),
      143040,
      dem(143040, 2026, "T4", "low",
        "Seastreak: MV Express + Whaling City Express certified 149 pax each (T1, CAPACITY-GAPFILL.md); published pattern 4 departures/direction/day, 55-min crossing (BOSTON-CAPE-CENSUS S9)",
        "CAPACITY BASIS: 149 x 4 x 2 x 120-day conservative season assumption = 143,040 seat-capacity/yr. "
        "Season dates not primary-sourced - 120 days is deliberately below the visible May-Oct pattern; "
        "route-level ridership unpublished (network NTD 1.31M includes NYC commuter runs). Flagged."),
    ),
  ],
}

def main():
    cr_p = f'{REPO}/finance/model/country-reference.json'
    co_p = f'{REPO}/finance/model/corridors.json'
    cr = json.load(open(cr_p)); co = json.load(open(co_p))
    allc = dict(cr.get('countries', {}));
    for k, v in cr.items():
        if not k.startswith('_') and k != 'countries' and isinstance(v, dict) and 'captain_usd_yr' in v:
            allc[k] = v
    assert 'United States' not in allc, 'US row already exists'
    for mk in ('usa-ny-harbor', 'usa-new-england'):
        assert mk not in co['markets'], f'{mk} already exists'
    n_ny, n_ne = len(NY['corridors']), len(NE['corridors'])
    print(f'US row fields: {list(US_ROW.keys())}')
    print(f'usa-ny-harbor: {n_ny} corridors; usa-new-england: {n_ne} corridors')
    for m in (NY, NE):
        for c in m['corridors']:
            L = c['L3_locals']
            print(f"  {c['route_id'][:40]:42s} {c['distance_nm']:6.1f}nm ${L['comparable_fare_usd_pax']:5.0f} pool {L['corridor_annual_oneway_pax']:>9,} [{L['_demand_record']['source_tier']}] {c['vessel']}")
    if not APPLY:
        print('\nDRY RUN - pass --apply to write'); return
    shutil.copy(co_p, '/tmp/corridors.pre-usa-northeast.bak.json')
    cr['countries']['United States'] = US_ROW  # engines read only ['countries']
    cr['_usa_northeast_additions_at'] = '2026-07-28 Northeast USA program Phase 2 (anchors approved by Jaideep 2026-07-27)'
    co['markets']['usa-ny-harbor'] = NY
    co['markets']['usa-new-england'] = NE
    co['_usa_northeast_t1'] = {
      "date": "2026-07-28",
      "approved": "Jaideep fare-anchor table + 3 flags, 2026-07-27 ('Okay approved')",
      "evidence": "/tasklet/agent/home/northeast-program/census/ (COST-POLICY, RIDERSHIP-PASS2, DEMAND-GAPFILL-PASS3, COST-GAPFILL-PASS2, CAPACITY-GAPFILL, FARES-*)",
      "held_display_tier": {
        "sag-harbor-local-mesh": "geometry exists; no premium fare substitute + no local demand anchor",
        "newport-block-island": "display tier per plan", "casco-bay": "display tier per plan (Casco Bay Lines 1.09M UPT sourced if promoted)"
      },
      "berth_note": "US marina_overhead is a Jaideep-approved FLAGGED ESTIMATE pending written quotes; see country-reference row.",
    }
    json.dump(cr, open(cr_p, 'w'), indent=1, ensure_ascii=False)
    json.dump(co, open(co_p, 'w'), indent=2, ensure_ascii=False)
    # scoped view for per-partner-country agg (didi-mexico precedent)
    scoped = dict(co); scoped = {k: v for k, v in co.items() if k != 'markets'}
    scoped['markets'] = {k: co['markets'][k] for k in ('usa-ny-harbor', 'usa-new-england')}
    json.dump(scoped, open('/tmp/corridors-uber-usa.json', 'w'), indent=1, ensure_ascii=False)
    print('APPLIED: country row + 2 markets; scoped view at /tmp/corridors-uber-usa.json')

if __name__ == '__main__':
    main()
