# DiDi × Navier — Mexico Pacific status (2026-07-09)

**Status:** research-complete for source triage; registry/BP grounding, Grok seal, and economics still required.

## Baseline
- Canonical hierarchy preserved: `mexico` → `los-cabos-mexico`, `puerto-vallarta-mexico`.
- DiDi partner scope already inherits both cities at country-supported tier; Mexico Pacific remains aspirational at market-card level.
- `ROUTES.json` contains 16 Los Cabos + 16 Puerto Vallarta routes.
- No matching Mexico file exists under `atlas-external/boarding-points/`.

## Source-backed DiDi coastal candidates
Official DiDi Mexico inventory explicitly lists **Puerto Vallarta, La Paz, Mazatlán, Acapulco, Ensenada, Manzanillo, Guaymas, and Puerto Escondido**. It does **not** list Los Cabos/Cabo San Lucas; preserve Los Cabos only as country-supported inherited coverage unless DiDi supplies city proof.

## Priority opportunities
1. **Puerto Vallarta deepening:** bind Los Muertos Pier and Boca de Tomatlán; ground Yelapa/Las Ánimas landings.
2. **Mazatlán + La Paz registry pair:** public ferry terminals and current Baja Ferries routes are verified; route-specific directional pax/service days remain missing.
3. **Mazatlán local crossing:** Gabriel Leyva ↔ Isla de la Piedra has five-minute lancha evidence but needs authority confirmation.
4. **Acapulco:** Caleta ↔ La Roqueta has daily operator evidence; exact public dock, fare, pax and permits are unresolved.
5. **Cruise transfer nodes:** Ensenada, Acapulco and Manzanillo have official passenger-terminal evidence; these are transfer origins, not yet water corridors.
6. **Guaymas:** historic official ferry launch exists, but current 2026 status is unconfirmed—hold.

## Critical QA blockers
- Many existing endpoints are generic/non-BP POIs (e.g., Harbor 171, Bistro Marina, beach clubs, “Water Taxi,” “Los Cabos, Baja Sur”).
- Routes `ics-3b1885b0e5` and `ics-c1f5deb1fa` are Los Cabos records incorrectly stamped `cluster_id=galapagos-ecuador`.
- Reconcile Marina Puerto Los Cabos / San José del Cabo Marina aliases and duplicate nodes.
- Ensenada official plan conflicts internally: repeated 2024 series says **272 calls / 949,287 passengers**, another fragment says **353 / 744.2k**. Do not publish until reconciled.
- All route `annual_one_way_pax` values remain null; broad cruise/tourism totals were not converted to route demand.

## Files
- JSON: `/tasklet/agent/home/didi-ex-china-audit/mexico/DIDI-MEXICO-PACIFIC-BP-BRIEF-RESEARCH-2026-07-09.json`
- Markdown: `/tasklet/agent/home/didi-ex-china-audit/mexico/DIDI-MEXICO-PACIFIC-STATUS-2026-07-09.md`
