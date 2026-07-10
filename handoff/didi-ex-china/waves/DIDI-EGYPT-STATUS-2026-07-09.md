# DiDi × Navier Egypt deepening — status

**As of:** 2026-07-09  
**Lane:** Boarding points + brief maturity + demand/fare research  
**Status:** Research complete with canonical-repository, geocoding, and route-demand blockers

## What is now defensible

### Cairo / Nile
- A current seasonal river-bus example is verified: **Happy Land berth at Al-Mazallat → Al-Qanater al-Khayriyya**, daily during the reported Eid al-Fitr 2026 program.
- Published fare: **EGP 120 per person return**. Reported sailing time is about four hours return, with about three hours at Al-Qanater.
- Maspero, University Bridge, and Zoo river-bus stations are **revalidation candidates only**; the evidence found is from 2023 and does not prove July 2026 operation.
- Cairo Airport handled **30.94 million passengers in 2025**, but this is contextual throughput, not Nile-route demand.
- The amphibious “Swim Bus” was described as a trial and tourist-only, not public passenger transport.

### Red Sea
- AD Ports Group says cruise services commenced at **Sharm El Sheikh, Hurghada, and Safaga** terminals by 19 May 2026; Hurghada and Safaga passenger services and a **Safaga–NEOM Hajj-worker ferry** operation are specifically described.
- Egypt’s official tourism portal says special **Hurghada–Mahmeya/Giftun boats run daily**, leaving in the morning and returning at sunset. Exact origin berth, fare, capacity, and annual riders remain unknown.
- El Gouna boat rentals are verified as leisure activity, **not scheduled passenger transit**.
- Ras Muhammad and Nabq are marine/protected-area POIs, **not boarding points**. No scheduled Sharm excursion route was verified.

## DiDi evidence boundary
- Cairo is supported by a 2025 DiDi Express launch report and official DiDi Egypt/Cairo organizational evidence.
- This research does **not** prove live DiDi coverage in Hurghada, El Gouna, Safaga, or Sharm. Partner copy must say service-area validation is required.

## Artifact counts
- 14 sources
- 4 existing Atlas city IDs reviewed
- 13 BP/POI records: 5 verified existing BPs, 6 confirmation candidates, 2 non-BP POIs
- 6 candidate corridors: 3 with current-operation evidence, 1 historical reactivation candidate, 2 future opportunities
- 7 demand/fare records
- 0 route IDs assigned
- 0 route-level annual passenger values; all `annual_one_way_pax` fields remain null
- 1 current route-specific fare captured

## Finance / geometry handoff
- **No Egypt corridor is finance-ready.** National tourism and airport totals must not be converted into route demand.
- **No route ID is stamped.** `/tmp/navier-atlas` and canonical `ROUTES.json` were unavailable; the fallback audit reports zero Egypt routes.
- Obtain authority/operator coordinates before stamping Cairo berths, Red Sea passenger gates, the Hurghada excursion berth, or island landings.
- Marine geometry needs human-reviewed waypoints for port approaches, reefs/protected waters, lagoons, and the international Safaga–NEOM crossing.

## Canonical brief recommendation
Enhance rather than replace once the canonical briefs are mounted. Keep them partner-neutral and visibly separate:
1. **Cairo/Nile:** existing seasonal leisure river bus, historical urban stations needing revalidation, airport-to-river first/last mile.
2. **Red Sea:** operating cruise/ferry gateways, daily fee-bearing island excursion, protected-area opportunities not yet evidenced as scheduled routes.

Put all DiDi-specific framing in a separate partner narrative block.

## Blockers / next actions
1. Mount `/tmp/navier-atlas`; exact-match `CLUSTERS.json`, `ROUTES.json`, canonical briefs, and existing BP files.
2. Obtain a 2026 Cairo authority station list, timetable, fares, ridership, and coordinates.
3. Get authoritative passenger-gate coordinates for Hurghada, Safaga, and Sharm.
4. Request Mahmeya operator tariff, exact quay, vessel capacity, annual bookings, and operating/cancellation calendar.
5. Source EEAA/protectorate rules and named authorized Sharm excursion terminals.
6. Obtain DiDi’s official July 2026 service-area list for the Red Sea cities.

## Outputs
- JSON: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-EGYPT-DEEPENING-2026-07-09.json`
- Markdown: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-EGYPT-STATUS-2026-07-09.md`
