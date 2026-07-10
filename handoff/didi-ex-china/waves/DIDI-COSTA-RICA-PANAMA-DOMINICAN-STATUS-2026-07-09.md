# DiDi × Navier Costa Rica / Panama / Dominican Republic — status

**As of:** 2026-07-09  
**Status:** research-complete / seal-needed / finance-inputs-incomplete  
**JSON:** `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-COSTA-RICA-PANAMA-DOMINICAN-DEEPENING-2026-07-09.json`

## Baseline audited

- Canonical markets: `nicoya-papagayo-costa-rica`, `san-blas-panama`, `samana-dominican-republic`.
- 123 Atlas boarding-point records classified: 39 Costa Rica, 48 Panama, 36 Dominican Republic.
- Conservative BP classes: candidate_needing_boarding_confirmation=10, candidate_needing_coordinate_and_primary_source_confirmation=75, future_opportunity=5, non_bp_poi=11, reject_drop=3, verified_existing_boarding_point=19.
- 11 priority corridors reviewed; 10 have exact existing ROUTES.json IDs; the speculative Cartí–Colón concept correctly remains `route_id: null`.

## Strongest evidence added

- **Costa Rica:** official DiDi city list names Liberia; ICT reports 881,289 tourist entries via Daniel Oduber airport in 2024; regulated adult fares effective 1 July 2026 are CRC 810 to Paquera and CRC 1,000 to Playa Naranjo; Naviera Tambor lists eight Paquera departures per direction.
- **Panama:** official DiDi evidence is exact only for Panama City, not Cartí/Gunayala. Visit Panamá confirms 365+ islands; a licensed Guna-owned operator documents advance coordination, three official ports and local control. No annual visitor or route-pax series was found.
- **Samaná:** official government evidence records 61,558 whale-observation visitors in Q1 2024 and a 15 Jan–31 Mar 2025 season. Official tourism supply is ~2.6K rooms/46 hotels; El Catey handled 101,555 passengers in 2024. Public-ferry seller evidence shows a one-hour, US$16 crossing and indexed Samaná times of 09:00/11:00/15:00/16:20, but primary confirmation remains required.

## Brief maturity

- Nicoya/Papagayo: **76/100** — strong structure and segmentation; add official fare/schedule/catchment evidence and route pax when available.
- San Blas: **68/100** — governance framing is strong; demand claims, timing language and BP verification need correction.
- Samaná: **74/100** — strong whale-sensitive fit; explicitly add public ferry and official seasonal demand while keeping it separate from route demand.

Canonical briefs should remain partner-neutral. DiDi-specific framing is isolated in `partner_narrative_notes`.

## Finance and geometry blockers

1. **No verified route-level annual passenger counts** for any priority corridor. Every `annual_one_way_pax` remains null.
2. Guna Yala community docks and permissions need Guna authority/operator validation; OSM links are not authority-grade.
3. Cartí–Colón is future-only and needs coast-following hand waypoints, range/weather/restricted-water checks, and authority approval.
4. Samaná ferry fare/timetable needs primary operator or transport-authority confirmation.
5. Exact local DiDi service remains unproven in Samaná and Guna Yala.

## Publication guardrails

Do not convert broad tourism/airport/whale counts into route demand; do not claim exact DiDi coverage outside official city evidence; do not present excursion/resort/Guna panga activity as scheduled public transport; and do not publish OSM-only BP coordinates as verified.
