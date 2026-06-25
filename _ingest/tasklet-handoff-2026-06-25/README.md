# tasklet-handoff-2026-06-25 — Bolt/Yango corridor pins + BP research (Tasklet → Grok)

**Type:** corridor registry edits + new second-endpoint BPs. Pairs with the next econ reseal.
**Division of labor:** Tasklet ships `corridors.json` + BP research; **Grok** seals BPs, mints `route_id`s, binds, and reseals economics. Tasklet does not run the model cascade.

## 1. `corridors.json` edits (10 rows; same row set, valid JSON)

### A. Cross-border / out-of-scope holds → `aspirational: true` (5)
Clears these from `actionable_pending` (resolver rule 5 → `aspirational_declared`). Targets the ≤5 acceptance gate (was 6 actionable).
- `bolt-spain` Tarifa → Tangier — cross-strait excluded (Gibraltar)
- `yango-morocco` Tangier Marina Bay → Tarifa — cross-strait excluded
- `yango-morocco` Tanger Med → Algeciras (Spain) — cross-strait international
- `yango-turkey` Kuşadası → Samos (Greece) — cross-border Aegean (`no_endpoints`)
- `bolt-ireland` Dublin Port → Holyhead (Wales) — 67 nm open Irish Sea, international; beyond Pioneer II urban scope

### B. Node-chip corrections (5)
**Safe (chip already in gold, proven by sibling corridor):**
- `bolt-italy` San Marco → Murano/Burano: `amalfi-coast-italy` → `venice-italy`
- `bolt-italy` Venice → Lido: `amalfi-coast-italy` → `venice-italy`

**NEW node chips — Grok please mint these gold cities (flagged `_new_node_chip: true`):**
- `bolt-portugal` Porto → Gaia: `beira-mozambique` (wrong continent!) → **`porto-portugal`**
- `bolt-spain` L'Estartit → Illes Medes: `palma-mallorca-spain` → **`costa-brava-spain`**
- `yango-morocco` Rabat → Salé: `tangier-morocco` → **`rabat-sale-morocco`**

> The Porto row was keyed to a Mozambique node (`beira-mozambique`, a pruned market) with `country: Portugal` — a confidently-wrong binding now corrected. If a `porto-portugal`/`costa-brava-spain`/`rabat-sale-morocco` city is not minted, those corridors will pin via BP-pair (rule 3) but cluster on the new chip — please mint.

## 2. New boarding points (`boarding-points/*.json` + `inputs/BP-COVERAGE-NEW-2026-06-25.json`)
22 new second-endpoint BPs across 11 cities for active `one_bp` corridors. **Validate / snap-to-water before seal. 0 silent drops.** 16 high / 6 medium-confidence (medium = snap-check):
- **Croatia (Elaphiti — named blocker):** Lopud, Suđurađ (Šipan), Koločep quays
- **Estonia (Aegna — named blocker):** Aegna Sadam
- **Italy/Venice:** San Zaccaria, Murano (Colonna), Burano, Lido S.M.E.
- **Portugal:** Cascais marina; Porto (Cais da Ribeira) + Gaia
- **Ireland:** Docklands (Sir John Rogerson's Quay), Coliemore (Dalkey), Ireland's Eye, Dalkey Island
- **Sweden:** Drottningholm slottsbrygga
- **Spain (Costa Brava):** Port de l'Estartit, Illes Medes
- **Turkey:** Kabataş iskelesi
- **Morocco:** Rabat Marina Bouregreg, Salé Bab Lamrissa
- **Nigeria:** Osborne Foreshore Jetty (Ikoyi)

## 3. Grok next steps
1. Mint the 3 new gold city chips (porto / costa-brava / rabat-salé).
2. Seal the 22 BPs (snap-to-water; honor confidence flags).
3. Re-run route-linkage lane for bolt + yango; mint `route_id`s for the now-pairable corridors.
4. Phase-5 econ reseal; refresh `PENDING-ECONOMICS-TRIAGE`.

## 4. Still parked (not in this drop)
- East Africa 8 culled corridors — separate BP/geometry research (v2 mint).
- `mint_gcn` intra-city loops (Bali Benoa, Phuket Chalong, Bangkok ICONSIAM) — Grok mints declared `gcn-*` into gold.
- `mint_rn` Dubrovnik → Kotor — both endpoints present; Grok routes the edge.
