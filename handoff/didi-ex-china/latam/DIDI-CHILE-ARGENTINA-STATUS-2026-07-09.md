# DiDi × Navier Wave C — Chile & Argentina status

**As of:** 2026-07-09  
**Overall:** **research-complete for source-led registry handoff; research-needed for live-repo seal, geometry and economics**

## What is complete

- Current DiDi operation is established city by city from DiDi's official local operating-city indexes: **23 Chile source labels** and **20 Argentina source labels** (43 total; 48 normalized rows because combined Chile service-area labels split only as proposed normalization rows).
- Same-day Atlas audit baseline remains a true registry gap for both countries: **0 canonical clusters, cities, matching briefs, BPs and exact candidate route matches** at commit `ae1b96917eaed901a84302b856ce53f6efd767ae`.
- **22** BP records and **10** source-backed corridor candidates are typed with endpoint names, all unresolved coordinates left null, waypoint/land-crossing risks, and **all route IDs null**.
- Grok-ready expansion ledger includes proposed normalized names, source/proof, endpoint pairs, rejects, gap owners and acceptance criteria.
- P0 marine anchors retained: Puerto Montt, Punta Arenas, Valdivia, Buenos Aires.

## Important holds

- No proposed label or candidate key is a canonical ID. Do not publish or mint IDs from this file.
- No annual one-way route passenger count was found; broad tourism/metro counts were not converted into route demand.
- Exact DiDi coverage remains unproven for nearby municipalities such as Niebla, Calbuco/Pargua/Chacao/Dalcahue, Lota/Talcahuano and Tigre.
- Rosario–Isla Sabino Corsi is seasonal; Muelle Prat is excursion-only; Muelle Blanco still lacks current passenger-service proof; Buenos Aires–Colonia requires cross-border review.
- `/tmp/navier-atlas` was unavailable in this worker. Exact-match baseline is inherited from the same-day audit and copied DiDi partner staging file; the live repo must be rechecked at seal time (G9).

## Next acceptance gates

1. Registry owner approves Chile/Argentina hierarchy and normalized labels.
2. Geometry owner confirms authoritative BP coordinates and seals water-only waypoint paths.
3. Demand owner obtains annual one-way route counts and current fare tables.
4. DiDi coverage owner verifies app/service polygons outside exact named cities.
5. Legal/regulatory owner clears domestic and cross-border operating constraints.
6. Build partner-neutral briefs, then run model cascade and Grok seal handoff.

## Artifacts

- JSON: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-CHILE-ARGENTINA-REGISTRY-DEEPENING-2026-07-09.json`
- This status: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-CHILE-ARGENTINA-STATUS-2026-07-09.md`

Repository was not edited.
