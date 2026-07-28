#!/usr/bin/env python3
"""Northeast Phase 2 follow-up (Jaideep directives 2026-07-28, second round).

1. Quanta LR hybrid = N30 hull + hybrid engine ('capacity & cruise speed same as N30;
   only the engine changes; ready now; $1.5M capex US/EU premium').
2. Sag Harbor + Montauk -> quanta_lr, capex_usd_override=1500000 (enrich() defaults US
   to N30 $900K), holds released, fares re-anchored vs BLADE $795/seat
   (blade.com/hamptons 2026 Summer Pass): Sag $625 (3.00yr MID), Montauk $645 (2.83yr).
3. Nantucket $85 -> $99 (Cape Air top-of-band; 'shift to $99') -> 3.03yr MID.
4. ROUTES.json: _quarantine + render_hidden on the 11 junk ICS ids.

Cascade: scoped view -> aggregate.py --partner uber --corridors <scoped> --json
finance/recal/agg-uber-usa.json -> greenfield_census.census_partner(agg_path=...,
country='United States') -> growth.py -> build_transparent_sheet.py.
Rule-7 verified 2026-07-28: sheet MID == engine on all 8 corridors.
NOTE: aggregate.py output flag is --json (NOT --out); always pass --partner uber.
Usage: python3 apply_quanta_reanchor_2026_07_28.py <repo_root> --apply
"""
import json, copy, sys

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    apply = '--apply' in sys.argv

    vp = f'{root}/finance/model/vessel-constants.json'
    v = json.load(open(vp))
    q = copy.deepcopy(v['vessels']['pioneer_ii'])
    q['label'] = 'N30 Quanta LR (hybrid)'; q['status'] = 'commercial_now'
    q['_note'] = ("N30 hull with hybrid powertrain — Jaideep 2026-07-28: capacity & cruise speed "
                  "same as Pioneer II N30; only the engine changes; ready now; $1.5M capex US/EU "
                  "premium. Range & energy intensity are LABELLED modelling values pending locked spec.")
    q['capex_usd'] = {"value": 1500000, "unit": "USD", "source_tier": "T1",
        "source": "Jaideep directive 2026-07-28: hybrid Quanta $1.5M capex US/EU premium markets",
        "confidence": "high", "notes": "Non-US/EU pricing NOT set — explicit override or fail closed."}
    q['range_nm'] = {"value": 110, "unit": "nm", "source_tier": "T3",
        "source": "MODELLED: hybrid long-range per Jaideep 2026-07-28 (max modeled corridor 104.7nm)",
        "confidence": "low", "notes": "Replace with locked Quanta LR range."}
    q['battery_kwh'] = {"value": 179, "unit": "kWh", "source_tier": "T3",
        "source": "MODELLED: preserves N30 energy intensity (1.629 kWh/nm) at 110nm modelled range",
        "confidence": "low", "notes": "Energy-cost math only; replace with locked hybrid basis."}
    v['vessels']['quanta_lr'] = q

    cp = f'{root}/finance/model/corridors.json'
    c = json.load(open(cp))
    FB = {"rn-e2c8f0d3fe0d": (625.0, "Sag Harbor"), "rn-1119113a9806": (645.0, "Montauk")}
    for cor in c['markets']['usa-ny-harbor']['corridors']:
        rid = cor['route_id']
        if rid in FB:
            fare, name = FB[rid]
            L = cor['L3_locals']; old = L.get('comparable_fare_usd_pax')
            cor['vessel_key'] = 'quanta_lr'
            L['capex_usd_override'] = 1500000
            L['comparable_fare_usd_pax'] = fare
            L['_fare_record'] = {"value": fare, "unit": "USD/pax/one-way premium anchor", "year": 2026,
                "source_tier": "T2", "confidence": "med",
                "source": f"BLADE Hamptons 2026 Summer Pass $795/seat Manhattan-{name} (blade.com/hamptons)",
                "method": "Premium-substitute benchmarking; anchored ~20% under the Blade seat."}
            cor.pop('_economics_hold_reason', None)
            cor['_hold_released'] = 'released 2026-07-28: Quanta LR hybrid clears the 70nm range gate'
            print(f're-anchored {name}: {old} -> {fare}')
    for cor in c['markets']['usa-new-england']['corridors']:
        if cor['route_id'] == 'e__boston-new-england-usa__hyannis-terminal__nantucket-steamship-wharf':
            L = cor['L3_locals']; L['comparable_fare_usd_pax'] = 99
            L['_fare_record'] = {"value": 99.0, "unit": "USD/pax/one-way premium anchor", "year": 2026,
                "source_tier": "T2", "confidence": "med",
                "source": "Cape Air HYA-ACK band $69-99/seat; Jaideep 2026-07-28: shift to $99",
                "method": "Top of sourced premium-substitute band."}
            cor.pop('_economics_hold_reason', None)
            cor['_hold_released'] = 'released 2026-07-28: $99 top-of-band clears ~3yr (3.03 MID)'
            print('Nantucket -> $99')

    rp = f'{root}/data-clean/ROUTES.json'
    qf = json.load(open(f'{root}/data-clean/QUARANTINE-ics-junk-endpoints-2026-07-28.json'))
    qr = qf['routes'] if isinstance(qf, dict) and 'routes' in qf else qf
    ids = {r['route_id']: r.get('reason', 'geocoding junk endpoint') for r in qr}
    R = json.load(open(rp)); n = 0
    for f in R:
        p = f.get('properties', {})
        if p.get('id') in ids:
            p['_quarantine'] = True; p['render_hidden'] = True
            p['_quarantine_reason'] = f"ICS geocoding junk endpoint (2026-07-28 Northeast hygiene): {ids[p['id']]}"
            n += 1
    print('quarantined', n)

    if not apply:
        print('DRY RUN — pass --apply'); return
    json.dump(v, open(vp, 'w'), indent=1, ensure_ascii=False)
    json.dump(c, open(cp, 'w'), indent=2, ensure_ascii=False)
    json.dump(R, open(rp, 'w'), indent=2, ensure_ascii=False)
    print('APPLIED')

if __name__ == '__main__':
    main()
