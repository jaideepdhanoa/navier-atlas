# InDrive scope expansion and four-country deck plan

**Prepared for Jaideep review · 13 July 2026**

## Executive diagnosis

Jaideep’s concern is supported by the current source artifacts.

- The InDrive proposal carries **74 footprint rows**, including **58 distinct Atlas-bound keys marked for map promotion**, but its effective `_map_scope` resolves to only **three canonical clusters**: Egypt, India, and Morocco.
- That current scope inherits approximately **342 active canonical routes**. The already-recorded promotion candidates resolve to **22 existing canonical clusters, 101 registered cities, and 2,382 active routes**. This is a candidate ceiling, not an approval to promote all 22: current InDrive operation must be revalidated by country/region first.
- Brazil is already present in InDrive’s footprint as three Atlas-bound markets—Rio de Janeiro, Angra/Ilha Grande, and Florianópolis—but all are outside the effective scope and have no full InDrive Brazil sub-proposal.
- Egypt is already inherited and has a full **Egypt Red Sea** sub-proposal. The canonical Egypt cluster contains four registered cities, but its 179 active routes currently touch the Red Sea cities rather than Cairo. Cairo should remain distribution context unless exact marine routes are validated.
- InDrive economics are not merely stale; they are effectively unusable. The current scoped file has one non-geographic `indrive` bucket, six mixed corridors, an unrelated Saudi resort row, and only partial route binding. Its aggregate has **zero corridors, zero fleet, and zero revenue**; its growth case is null and still names a borrowed Grab census. InDrive has no registered economics Sheet URL.
- DiDi is much further along. Brazil already has one full sub-proposal and four exact, grounded Rio routes. Mexico already has two full sub-proposals—Pacific and Caribbean—with an eight-route exact finance spine and supported values only where evidence exists. There is no reason to duplicate these with a new umbrella proposal.
- No dedicated Deck Studio records currently exist for `didi-brazil`, `didi-mexico`, `indrive-brazil`, or `indrive-egypt`. DiDi’s official logo is banked with provenance; InDrive’s is not.

## Recommended program

### Phase 0 — Freeze the baseline and settle the DiDi dependency

1. Snapshot the current InDrive proposal, rendered partner data, cluster membership, route inheritance, finance artifacts, and deck registry.
2. Preserve every existing InDrive market while revalidating official country/region operation; a partial source scan may add or hold candidates but may not silently shrink the baseline.
3. Obtain Jaideep’s decision on open DiDi PR #256 before deriving the two country decks from its city-deep-dive assets. Do not edit the legacy DiDi deck or fork a second version of the same source package.

**Review gate:** approved InDrive country/region roster and an explicit decision on the DiDi city-deep-dive source branch.

### Phase 1 — Expand InDrive inheritance correctly

1. Revalidate InDrive’s broad operating universe using official country, region, city, help-centre, and corporate sources.
2. Reconcile the 58 existing promotable Atlas keys into four lanes:
   - approved country/region-supported inheritance;
   - exact city-supported inheritance;
   - brief-only candidates;
   - unsupported or unresolved holds.
3. Update InDrive `_map_scope` as **cluster/city membership only**. Corridors must remain geography-owned:

   `InDrive routes = global canonical routes ∩ approved InDrive clusters`

4. Promote Brazil if the operation gate remains supported. The existing Brazil cluster currently provides:
   - 3 registered cities: Rio, Angra/Ilha Grande, Florianópolis;
   - 59 active canonical routes;
   - 11 distinct route endpoints in the current route graph.
5. Preserve Egypt inheritance. Its current cluster provides 179 active routes and 105 distinct route endpoints across the Red Sea route graph. Do not imply that Cairo has active marine routes merely because it is a registered cluster member.
6. Run anchor-city ID matching, route-inheritance identity, hidden/quarantined-route exclusion, zero-silent-drop, and visual render checks.

**Review gate:** accepted scope ledger with exact before/after cluster, city, endpoint, and route counts; all unsupported values remain null.

### Phase 2 — Bring sub-proposals to parity

| Requested deck | Current proposal state | Required action |
|---|---|---|
| DiDi Brazil | Full `brazil` sub-proposal exists | Audit and reuse; no duplicate wrapper. |
| DiDi Mexico | Full `mexico-caribbean` and `mexico-pacific` sub-proposals exist | Audit and use both as the country-deck source; no duplicate wrapper. |
| InDrive Brazil | Missing | Create a full Brazil sub-proposal with Rio, Angra/Ilha Grande, and Florianópolis anchors, phases, supported journeys, exact featured routes, and partner-facing copy. |
| InDrive Egypt | Full `egypt-red-sea` sub-proposal exists | Audit and deepen the Red Sea proposal. Keep Cairo as distribution context unless exact marine binding supports a separate page. |

Every promoted sub-proposal must pass roster reconciliation, vessel range-gating, route-ID subset checks, and the partner-copy audit. `roll_up_markets` stubs do not count as full sub-proposals.

### Phase 3 — Rebuild InDrive financials from the geography spine

1. Retire the current pseudo-market scoped build; do not repair it by layering more rows onto `markets.indrive`.
2. Materialize explicit market keys, beginning with `indrive-brazil` and `indrive-egypt`, then the rest of the accepted scope.
3. Reuse route demand and fare records only when they are geography facts bound to the same exact route ID:
   - Brazil can start from DiDi’s four exact Rio demand/fare records, with an InDrive-specific commercial overlay.
   - Egypt has ten existing finance candidates, but route binding and demand support are incomplete. Bind exact canonical IDs first; unsupported annual demand remains null and outside the grounded floor.
4. Apply exact country cost rows for Brazil and Egypt, commercial regional CAPEX, range-gated vessels, and labelled global-template upside only if no InDrive census exists. Never reuse the Grab census.
5. Cascade model → growth case → InDrive partner JSON → transparent workbook → master tracker → route-keyed sidecar.
6. Because InDrive has no existing Sheet, create one stable workbook once, register its ID, and use that same link everywhere thereafter.
7. Establish model-to-Sheet parity before any deck economics are applied.
8. Preserve the published DiDi workbook. Produce country-scoped Brazil and Mexico deck outputs from the existing source model/workbook rather than forking the underlying economics.

**Review gate:** exact route ledger, country-reference pass, model/Sheet parity receipt, registered InDrive economics URL, and explicit hold list.

### Phase 4 — Build four distinct country decks

Create four new Deck Studio records and four new live Slides review drafts:

1. `didi-brazil`
2. `didi-mexico`
3. `indrive-brazil`
4. `indrive-egypt`

Use the mobility-partner chassis, but retain the city-deep-dive treatment rather than broad regional maps.

- **DiDi Brazil:** Rio operating case first; Costa Verde and Florianópolis as supported network context. Economics must visibly distinguish the four grounded Rio routes from broader display geography.
- **DiDi Mexico:** Cancún–Isla Mujeres, Playa del Carmen–Cozumel, Puerto Vallarta, and Los Cabos pages; show economics only for supported route rows.
- **InDrive Brazil:** Rio first, then Costa Verde and Florianópolis; use InDrive-specific integration and rollout copy rather than cloning DiDi language.
- **InDrive Egypt:** Hurghada/El Gouna and Sharm El Sheikh deep dives; Cairo may explain onward distribution but must not be drawn as a marine route without exact support.

For each deck: unique config, slide manifest, content-source map, image manifest, economics binding, route ledger, QA receipt, and live deck ID. Use market-specific N30 composites, Slides API only, and plain partner-facing English. DiDi can reuse its banked official logo; InDrive requires an official logo file plus `LOGO-SOURCE.json` before a branded cover can be approved.

### Phase 5 — Review and merge sequence

Use three controlled review surfaces:

1. **PR A — InDrive scope and sub-proposals**
2. **PR B — InDrive economics, Sheet binding, and sidecar inputs**
3. **PR C — four Deck Studio packages and live review-draft receipts**

PR C should consume accepted outputs from A and B; it should not manually override them. Jaideep retains merge and external-release control.

## Definition of success

- InDrive’s approved Atlas scope reflects source-supported country/region operation and inherits the complete canonical corridor set for every accepted cluster.
- InDrive Brazil exists as a full sub-proposal; InDrive Egypt’s existing Red Sea proposal is complete enough to source a country deck without unsupported Cairo routing.
- InDrive economics no longer resolve to zero because of a broken pseudo-market build, and every modeled value has an exact route and country-cost basis.
- The four country decks have independent live IDs and manifests, while sharing canonical geography and finance sources rather than duplicating them.
- All four remain review drafts until Jaideep approves merge and external use.
