# WETA × Navier deck refinement status — 2026-07-12

## Current state

- Live deck: `1frwn6G6NrGdzxbJEqlO_EZ6M-vWF2dLYN8PWhGwHRpw`
- Slides: **15**
- Live revision: `4TonRLaYt4ERpg` (Drive version 66)
- Status: **PTA/RTA-standard refinement and Marin access narrative QA-passed for internal partner review**
- External release clearance: **not granted**
- Outreach authorization: **not granted**

## What changed

- Normalized all 15 slides to the authority-deck typography system: Playfair Display headlines, Exo 2 labels/metric emphasis, and Poppins body copy.
- Tightened the narrative from Bay context and public-service need through product, operating logic, passenger experience, bounded demonstration, WETA-selected pilot, evidence-led scale, governance, and next step.
- Rebuilt slide 9 around a banked Navier Atlas Bay render and a visible distinction between **existing WETA service**, **WETA-published expansion**, **Golden Gate Ferry / Marin inter-agency context**, and other candidate access pockets.
- Added the network-access thesis to slide 8: more—and closer—start and end points can reduce first/last-mile friction and make water transit useful to demand pockets below large-ferry scale.
- Added Larkspur, Sausalito and Tiburon as Marin gateways, with Richmond/Berkeley/Vallejo ↔ Larkspur retained as candidate inter-agency links rather than current WETA service.
- Synchronized the same qualified narrative to both proposal-source mirrors at commit `f3ed57b0e37de5ce3863600ecbb34ad11d8d7222`.
- Added explicit language that map lines are screening geometry only and do not imply a WETA or Golden Gate Ferry route, terminal, facility, or commitment.

## QA evidence

- 15/15 slides exported and visually inspected.
- 30/30 live image objects mapped to the image ledger.
- 12 Bay-specific N30 applications across 8 banked N30 plates, plus one banked Atlas network render.
- Partner-facing copy audit: zero banned internal-language hits.
- No visible overflow, overlap, or contrast defect observed in the final export.

## Routing handoff

Prepared, not sealed:

- `WETA-BAY-NETWORK-EXACT-ID-LEDGER-2026-07-12.json`
- `WETA-BAY-SHUTTLE-CANDIDATES-AND-WAYPOINT-GATE-2026-07-12.json`
- `GROK-SPEC-weta-bay-network-routing-2026-07-12.md`

The routing handoff now identifies three explicit lanes: repair/mint current and WETA-published routes, populate hand-waypoints for bridge/channel/shoal cases, and screen additional North/East/South Bay shuttle sites. The current canonical WETA waypoint file contains 17 route keys but every waypoint array is empty; zero recorded interior-land distance is therefore not treated as sufficient bridge/channel evidence.

Priority repairs are the Alameda Main Street endpoint conflict, the missing exact-ID Alameda Seaplane Lagoon current-service route, and the WETA-published Oakland–Redwood City route. Additional candidate pairs are classified separately from current WETA service, including Golden Gate Ferry inter-agency opportunities and facility-conversion holds. Palo Alto is held because official material describes a small/non-motorized hand-launch facility; San Leandro and Alviso remain site/facility screens rather than passenger terminals.

Exact existing IDs are recorded where present. Unsupported boarding-point and route bindings remain `null`. Any accepted geometry must be added globally under the corridor-inheritance contract and must pass zero-land-crossing, bridge-span/channel, and rendered-map QA before the live Atlas or deck can treat it as bound.

## Approval boundary

This package does **not** establish WETA commitment, external clearance, cargo demand, grant eligibility, application readiness, procurement, route selection, or outreach approval. Jaideep controls PR merge. Any warm leadership outreach requires explicit Sampriti/Jaideep approval.
