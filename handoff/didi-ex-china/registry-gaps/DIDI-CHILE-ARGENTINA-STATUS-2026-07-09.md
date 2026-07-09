# DiDi × Navier — Chile & Argentina registry-gap status

**As of:** 2026-07-09  
**Lane:** true-registry-gap city / boarding-point / brief discovery  
**Status:** **research-complete / registry-and-seal-needed; economics not ready**

## Baseline

- `CLUSTERS.json`: **0 Chile clusters, 0 Argentina clusters**; no canonical city IDs for either country.
- `ROUTES.json`: **0 exact matches** for the researched endpoint pairs; every proposed `route_id` remains `null`.
- DiDi partner JSON: neither country is in current `network_footprint` or `_map_scope`.
- External BP registry: only Singapore and Riau Islands files exist; no matching Chile/Argentina BP file.
- Canonical briefs: no matching Chile/Argentina city or cluster brief.

## Source-backed operating-city anchors

Official DiDi city inventory supports these nine prioritized anchors:

- **Chile:** Punta Arenas, Valdivia, Puerto Montt, Concepción, Valparaíso, Viña del Mar.
- **Argentina:** Buenos Aires, Rosario, Bariloche.

Nearby terminal municipalities and islands are **not** assumed to be inside DiDi service polygons.

The broad-footprint pass also retains, but does **not** promote, official DiDi labels for Antofagasta, Arica, Iquique, La Serena–Coquimbo, Magallanes, Mar del Plata, La Plata, Paraná, Santa Fe, and a secondary Concordia/Formosa/Posadas/Resistencia river queue. These need a current high-value passenger-water endpoint pair and operator/authority evidence before registry promotion.

## Highest-value route evidence

### P0

1. **Punta Arenas — Embarcadero Tres Puentes ↔ Porvenir**  
   TABSA verifies the ferry terminal/route. Exact Porvenir ramp label, fare, fixed frequency, coordinates and water geometry remain open.
2. **Valdivia regional — Terminal Portuario Niebla ↔ Corral**  
   Operator route and fare evidence; adult CLP 500 one-way. Requires a hand-routed estuary/channel path.
3. **Puerto Montt/Chiloé regional — Calbuco ↔ Isla Puluqui**  
   30 minutes, Mon–Sun, eight listed departures each direction for 1 Apr–31 Aug 2026; adult CLP 600.
4. **Puerto Montt/Chiloé regional — Pargua ↔ Chacao**  
   Official multi-vessel schedule runs across the day/night; 2026 vehicle fares are published, but no standalone passenger fare was captured.
5. **Buenos Aires/Tigre regional — Estación Fluvial Tigre ↔ Arroyo Cruz Colorada/Casa Bellini**  
   Official Line 452 timetable and river sequence; about 1.5 hours. Mandatory multi-waypoint routing through the Paraná Delta; do not draw a straight chord.

### P1 / qualification needed

- **El Pasaje ↔ Coyumbe (Canal Dalcahue):** 10 minutes, approximately every 10 minutes, 24/7; passengers free.
- **Lota (Pueblo Hundido) ↔ Isla Santa María (Puerto Sur):** 3 hours; national-adult CLP 4,470; broader Concepción bind only until DiDi polygon confirmation.
- **Rosario Terminal Fluvial ↔ Isla Sabino Corsi:** official summer hourly service; rest-of-year service suspended until notice.
- **Puerto Pañuelo ↔ Puerto Blest:** official Bariloche excursion evidence; route fare, service days, operator counts and coordinates remain missing.

### Separate legal/technical lane

- **Puerto Madero, Buenos Aires ↔ Colonia, Uruguay:** verified daily international ferry connection. Do not promote as a domestic/deployment-ready corridor without customs, immigration, cabotage, certification, distance and range review.

## Boarding-point triage

- **22 records total**
- **8 verified existing points** (count includes excursion-only Muelle Prat and foreign Colonia terminal)
- **14 candidates needing coordinate, terminal-name, service-boundary or passenger-operation confirmation**
- **Muelle Prat, Valparaíso:** verified tourism-launch pier, not a sourced scheduled point-to-point corridor.
- **Muelle Blanco, Talcahuano:** operational pier evidence only; current scheduled passenger use remains unverified.

## Economics discipline

- **10 demand records; annual one-way passenger count is null for all 10.**
- **5 records contain a route-specific fare or published fare category.**
- No tourism, airport, metro or citywide count was converted into route demand.
- All corridor economics remain **not model ready** pending operator/regulator passenger counts, coordinate seal, water distance and vessel-range review.

## Brief maturity

No canonical brief exists for any researched market. All standard fields score **0 / absent**. Recommended sequence:

1. approve registry hierarchy and partner-neutral market labels;
2. seal at least one source-backed BP/corridor per promoted market;
3. add official demand, regulator, seasonality and competitive-service evidence;
4. create partner-neutral canonical briefs;
5. keep DiDi-specific first/last-mile and in-app framing only in the partner narrative.

## Critical blockers

- Final cluster/city/BP IDs and route IDs must be assigned only through registry review and Grok seal.
- Authoritative ramp coordinates and hand-routed water geometry are missing.
- DiDi app/service polygons must be checked for Niebla, Calbuco/Pargua/Chacao/Dalcahue, Lota/Talcahuano and Tigre.
- Annual route passenger counts are unavailable in captured sources.
- Muelle Blanco needs current passenger operator/timetable/destination evidence.
- Rosario needs next-summer reactivation, fare and landing confirmation.

## Artifacts

- Research JSON: `DIDI-CHILE-ARGENTINA-REGISTRY-RESEARCH-2026-07-09.json`
- This status: `DIDI-CHILE-ARGENTINA-STATUS-2026-07-09.md`
