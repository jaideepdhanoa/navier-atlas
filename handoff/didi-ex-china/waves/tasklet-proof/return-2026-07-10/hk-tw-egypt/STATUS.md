# HK + Taiwan + Egypt P2 — Status

**As of:** 2026-07-10  
**Asks:** T9, T10, T11, T12  
**Records:** 14 (benchmark_only: 4, not_publicly_supported: 8, usable_for_base_case: 2)

## Conclusions

- **T9 / `rn-d7294a3ddd04`:** official exact-route historical patronage exists: **1.250 million passenger journeys in 2017**, direction-combined. It is `benchmark_only`, not a 2026 base-case input.
- **T10 / `rn-5085d4e1f498`:** Taiwan Navigation currently proves Kaohsiung–Penghu ferry operation and gives authoritative boarding-place names/addresses (Kaohsiung Port Pier 1 and Magong Port passenger facilities). No current local Taiwan DiDi passenger-operation proof was found. Keep quarantine/hard hold; **do not promote 95,705**.
- **T11 / Cairo:** Happy Land, Qanater, Maspero, University Bridge, and Zoo all remain coordinate-null. Current secondary or historical official mentions do not supply current authoritative berth coordinates.
- **T11 / Red Sea cruise terminals:** current names for Hurghada, Safaga, and Sharm El Sheikh are confirmed. Ministry coordinates are published only as **port coordinates**, not named cruise-berth coordinates; names can be used for research repair, coordinates stay held.
- **T11 / Giftun–Mahmeya:** official tourism evidence supports daily boat access/context, but neither the Hurghada departure berth nor island landing identity/coordinate is authoritatively published. Both remain null.
- **T12 / El Gouna:** DiDi’s directory supports Hurghada but not El Gouna. Do not inherit Hurghada operation proof to El Gouna. The current combined city ID `hurghada-el-gouna-egypt` is a structural leakage risk, so the exclusion is not guaranteed by Atlas geography alone.
- **T12 / NEOM:** NEOM is unambiguously Saudi Arabia (`neom-sindalah-ksa` in the Saudi cluster). Safaga–NEOM is cross-border; reject every NEOM-as-Egypt claim.

## What can materialize

1. Historical HK benchmark: 1,250,000 passenger journeys for 2017, with explicit stale-period label.
2. Taiwan endpoint **names/addresses only** for a repair queue; no route promotion or coordinate guessing.
3. Current Egyptian cruise-terminal names; no berth coordinate materialization yet.
4. Partner-scope gates: El Gouna held separately from Hurghada; NEOM excluded from Egypt attribution.

## What stays null / held

- Current HK route annual demand.
- Taiwan local DiDi operation, exact authoritative berth coordinates, and candidate demand 95,705.
- Exact berth coordinates for all five Cairo facilities, all three cruise terminals, and both Giftun/Mahmeya landings.

## Exact next action

1. Obtain a current Transport Department route-patronage extract for North Point–Hung Hom before using demand in a base case.
2. Run a controlled Taiwan DiDi Rider app service-area/ride-availability check and retain timestamped city/geofence evidence; separately request Taiwan Navigation/TIPC berth GIS or berth-plan coordinates for Kaohsiung Pier 1 and Magong.
3. Request berth GIS/as-built plans from Cairo Public Transport Authority and Egypt Red Sea Ports Authority/AD Ports; request EEAA/authorized operator landing permits for Giftun/Mahmeya.
4. Enforce a component-level El Gouna hold (or split the combined city ID) before any DiDi inheritance; update Egypt filters so `neom-sindalah-ksa` can appear only as a Saudi endpoint on an explicitly international corridor.
