# Grok handoff — Dott/Voi market coverage and route inheritance

**Source commit audited:** `8adf384da2214629b8b672b897fcd91011d3040d`  
**Owner split:** Tasklet evidence complete; Grok deterministic scope/render seal needed.

## P0: restore corridor inheritance

Partner hub pages must emit exactly:

`global canonical ROUTES.json ∩ partner._map_scope.clusters`

Current `scripts/route-display.mjs` drops routes twice on large hub pages: inherited hub intra-city culling, then automatic legacy filtering when route count exceeds 40. For hub pages using live cluster inheritance:

- select by canonical `properties.cluster_id` membership;
- do not delete canonical routes for density;
- use lane styling/opacity/zoom for legibility;
- retain sovereign commercial suppression only where contractually required and account for it explicitly in validation.

## P0: replace stale source scope

Do not union the old `cluster_city_ids` leftovers into the authoritative hub scope. Re-derive city membership from canonical clusters.

### Dott — evidence-supported existing Atlas clusters

`balearic-islands-spain`, `bay-of-naples-amalfi-coast-italy`, `cote-dazur-france-archipelago`, `denmark`, `finland`, `france`, `germany`, `greece`, `israel`, `italy`, `netherlands`, `norway`, `saudi-arabia`, `spain`, `switzerland`, `uae`, `uk`

Remove stale clusters: `bahrain`, `cyprus`, `dalmatia-croatia`, `egypt`, `estonia`, `ireland`, `lebanon`, `monaco`, `morocco`, `portugal`, `qatar`, `romania`, `sweden`.

Dott’s FY2025 report explicitly says Qatar and Sweden were exited in 2025.

### Voi — current-operation existing Atlas clusters

`balearic-islands-spain`, `bay-of-naples-amalfi-coast-italy`, `cote-dazur-france-archipelago`, `denmark`, `finland`, `france`, `germany`, `italy`, `netherlands`, `norway`, `spain`, `sweden`, `switzerland`, `uk`

Keep `uae` only as a visibly labelled **expansion opportunity**, not current Voi operation.

Remove stale current-operation clusters: `cyprus`, `dalmatia-croatia`, `egypt`, `estonia`, `greece`, `ireland`, `israel`, `lebanon`, `monaco`, `morocco`, `portugal`, `romania`, `saudi-arabia`.

## Current and expected receipts

- Current emitted totals: Dott **430**, Voi **374**.
- Supported routes currently emitted: Dott **268 / 1,430**; Voi **184 / 427**.
- Current Lebanon leakage: **4 routes each**; expected after repair: **0 each**.
- Netherlands currently: **0 / 8** routes for each; expected after scope repair: **8 / 8**.
- Voi UAE currently emits 45 routes under the expansion case. Retain expansion wording and do not convert it into an operating-footprint claim.

## P1 registry queue — null until globally sealed

Do not mint partner-specific corridors. Source/create geography once, then inherit it.

1. Belgium for both partners.
2. Le Havre / Seine estuary for Voi; no current northern-France Dott claim.
3. UK depth: Solent/Isle of Wight, Scottish and Severn opportunities according to exact partner evidence.
4. Germany beyond Hamburg: coastal/Baltic nodes and relevant river cities.
5. Norway and broader Nordic exact-city depth.
6. Poland for Dott.
7. Switzerland routes; current cluster has zero canonical corridors.
8. Austria/Hungary water-network candidates.

The source ledger contains every current official service-area row. `atlas_city_id`, `boarding_point_ids` and `route_ids` are intentionally null in the gap queue until exact binding.

## Required validation receipts

1. `validate_partner_inheritance.py` passes for Dott and Voi.
2. Output route-ID set equals the canonical route-ID set for every included cluster.
3. Shared clusters have identical route-ID sets across Dott/Voi and all other partners.
4. No Lebanon routes.
5. No Dott Qatar or Sweden routes.
6. Voi UAE is expansion-only in partner-facing copy.
7. Gate G partner-copy audit passes.
8. Provide rebuilt Dott/Voi route counts by cluster and screenshot/render receipt.

## Evidence files

- `DOTT-VOI-MARKET-COVERAGE-AUDIT-2026-07-10.md`
- `DOTT-VOI-ROUTE-SCOPE-PARITY-2026-07-10.json`
- `DOTT-VOI-COVERAGE-GAP-QUEUE-2026-07-10.json`
- `dott-official-footprint-2026-07-10.json`
- `voi-official-footprint-2026-07-10.json`

No economics promotion is authorized by this packet.
