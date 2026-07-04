# GROK SPEC — Yango roster amendment: Norway → Peru swap (2026-07-03)

**Stacked on PR #178** (`tasklet/yango-roster-correction`). This is an *amendment* to that roster correction — apply on top of the #178 seal, do not re-run from scratch.

## Why
Jaideep: **Yango exited Norway ridehail** (operations shut down Oct 2025; Dutch DPA €100M GDPR data-transfer ruling, May 2026). Norway is no longer a Yango market. Remove it entirely and backfill its sub-proposal slot with **Peru** (second LATAM market — the strongest clean Yango LatAm market after Colombia).

Sub-proposal total held at **8**. Required spread still satisfied: UAE + Qatar + Kazakhstan; LATAM ×2 (Colombia, Peru); Africa ×2 (Côte d'Ivoire, Senegal).

## What changed in this PR (Tasklet lane — already applied to `partner-pitch/partners/yango.json`)
1. **Removed Norway sub-page** (`markets[].id == "norway"`).
2. **Removed 3 Norway footprint entries:** `bergen-norway`, `geiranger-norway`, `stavanger-norway`.
3. **Added Peru sub-page** (`peru`, 21-field parity with UAE gold; region `LatAm-Pacific`; anchors `lima-peru`, `paracas-peru`; 4 journeys, 6 featured routes, 3 phases). All routes `route_id: null`, `_link_status: pending-grok-bind`.
4. **Added 2 Peru footprint entries:** `lima-peru`, `paracas-peru` (region `LatAm-Pacific`, `map_promote: true`).
5. **`_coverage_expansion`** updated — `sub_proposals_full` now includes `peru` not `norway`; `roster_amendments[]` logs the swap; `norway_briefs_retained` note added.
6. **New Peru briefs** (`data-clean/`, partner-neutral, mature bar): `city_briefs/lima-peru.json`, `city_briefs/paracas-peru.json`, `cluster_briefs/peru.json`.
7. **New Peru geometry dossiers:** `BP-DOSSIER-peru.json` (7 BPs), `CORRIDOR-DOSSIER-peru.json` (5 corridors, all hand-waypointed, no land crossings).

**No brief deletions.** Norway city/cluster briefs are partner-neutral shared assets (other partners may serve Oslo/Bergen) — retained as harmless orphans. Only Yango's partner surface is corrected.

## Grok lane (deterministic seal)
Apply **on top of the #178 seal**:

### 1. Unseal Norway from the Yango view
- Drop `bergen-norway`, `geiranger-norway`, `stavanger-norway` from any Yango `_map_scope` / cluster-id derivation.
- Do **not** delete the shared Norway briefs or any non-Yango partner's Norway geometry.

### 2. Seal Peru (net-new)
- Promote the 7 Peru BPs and 5 corridors from the dossiers into the gazetteer / registry (ID-match; refine approx coords on promotion).
- **BPs:** `yg-pe-lapunta`, `yg-pe-callao`, `yg-pe-costaverde`, `yg-pe-sanlorenzo`, `yg-pe-palomino`, `yg-pe-elchaco`, `yg-pe-ballestas`.
- **Corridors:** Costa Verde↔Callao (9nm), La Punta↔San Lorenzo (4nm), Callao↔Palominos (8nm), El Chaco↔Ballestas (9nm) → Pioneer II solid; Lima↔Paracas (~112nm) → Quanta-LR amber-dashed.
- All corridors carry explicit hand-waypoints (no land crossings) — honor them; do not re-route through land.
- Add `lima-peru`, `paracas-peru` to Yango `_map_scope` cluster-id derivation.

### 3. TAM ladder (Gap 1) over corrected footprint
- Extend the TAM-ladder regen to include Peru; recompute over the amended footprint (Norway out, Peru in). Same convention as #178.

### 4. Route bind (Gap 2)
- Bind `route_id` for the 6 Peru featured routes + 4 journeys once corridors are minted. Peru is currently 0/6 bound (`pending-grok-bind`), same pattern as the other 4 new sub-pages in #178.

### 5. Status flag (Gap 5)
- Same cosmetic status flip as #178.

## Guardrails
- ID-based matching only; null beats wrong.
- Never invent `route_id`s — leave null if a corridor isn't minted.
- Peru long leg (Lima↔Paracas ~112nm) is Quanta-LR roadmap — never fake it on a 70nm Pioneer II.
- Hand-waypoints are authoritative — no land crossings on any Peru corridor.

## QA gate
- Yango sub-pages == 8: `uae, qatar, egypt, cote-divoire, senegal, colombia, peru, kazakhstan`.
- No `norway`/`bergen`/`stavanger`/`geiranger` tokens in any live Yango surface (markets, footprint, `_map_scope`) — audit log in `_coverage_expansion` is documentation only.
- Peru field parity with UAE == PASS.
- All Peru corridors hand-waypointed; land-QA 0 fail.
