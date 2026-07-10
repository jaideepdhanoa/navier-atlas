# Grok post-G4 handoff — DiDi ex-China regional waves

**As of:** 2026-07-09  
**PR:** #211  
**State:** research banked / exact registry and geometry seal needed  
**Boundary:** Mexico G4 comes first. This document sequences the remaining ex-China program; it does not declare any new region publish- or finance-ready.

## Operating rules

1. Exact ID matching only. `null` beats a plausible but unsealed city, BP, route ID, coordinate, fare, or demand value.
2. Canonical geography owns corridors. Partner corridors are `global_canonical ∩ partner.clusters`; never mint DiDi-only geometry.
3. Canonical briefs remain partner-neutral. Put DiDi/99 positioning only in DiDi partner JSON.
4. Current-operation evidence must be city-specific when copy names a city. Country-level or app-store evidence is not city proof.
5. Broad airport, tourism, visitor, port, terminal, or excursion counts are context—not route demand—unless the source is route/direction specific and transferability is explicit.
6. Preserve gross directional one-way passenger semantics. Never silently halve or double a published crossing count.
7. No economics before route IDs are sealed. No Sheet/deck claims before aggregate → growth → splice → route-keyed sidecar.
8. Gate G and strict partner/finance inheritance must pass before any seal/complete claim.

## Wave order

### 0. Mexico G4 — now

Consume `handoff/didi-ex-china/mexico/GROK-G4-HANDOFF-2026-07-09.md` and return the route-keyed economics sidecar, strict featured-route schema repair, reseal, linkage, and render receipt. Preserve the exact eight-route T3 spine.

### 1. Latin America registry + geometry

#### Brazil / Colombia

Input: `handoff/didi-ex-china/waves/DIDI-BRAZIL-COLOMBIA-DEEPENING-2026-07-09.json`

- Exact existing geometry is available for four Rio public-ferry routes and one Cartagena route; verify endpoint/BP parentage before inheritance.
- 99 city proof is exact for Rio and Florianópolis; Angra is not exact-city proven.
- DiDi city proof is exact for Cartagena and Barranquilla.
- Every annual route-pax value remains null. Do not annualize Rio record-day observations or convert Cartagena terminal entries into one route.
- Treat Barranquilla Río-Bus as project/future until current scheduled operation is proven.

#### Costa Rica / Panama / Dominican Republic

Input: `handoff/didi-ex-china/waves/DIDI-COSTA-RICA-PANAMA-DOMINICAN-DEEPENING-2026-07-09.json`

- Ten priority corridors have existing route IDs to re-check exactly; Cartí–Colón remains future-only and `route_id: null`.
- DiDi exact city proof exists for Liberia and Panama City—not Cartí/Gunayala or Samaná.
- Guna governance/permissions and community docks require authority/operator confirmation.
- All annual route-pax values remain null; do not convert tourist, airport, whale-season, or island counts.

#### Ecuador / Peru

Input: `handoff/didi-ex-china/waves/DIDI-ECUADOR-PERU-DEEPENING-2026-07-09.json`

- First remove 46 foreign Galápagos route stamps and restore the three real populated-island member routes.
- Confirm exact BP IDs for Gus Angermeyer, Puerto Villamil, Tiburón Martillo, and Puerto Velasco Ibarra.
- Create/enhance a partner-neutral Pisco/San Andrés brief only after the current canonical checkout confirms the city/BP record.
- Keep all annual route-pax values null. Galápagos tourist arrivals and Ica visits are TAM context only.
- DiDi evidence is country-level only; do not claim local pier/city availability.

#### Chile / Argentina

Input already on main: `handoff/didi-ex-china/registry-gaps/DIDI-CHILE-ARGENTINA-REGISTRY-RESEARCH-2026-07-09.json`

- Reconcile real city IDs, BPs, and supported operating footprint before any sub-proposal is made full.
- No partner-only routes; source and seal geometry canonically first.

#### La Paz / Mazatlán / Acapulco

Input: `handoff/didi-ex-china/mexico/DIDI-MEXICO-LA-PAZ-MAZATLAN-ACAPULCO-REGISTRY-2026-07-09.json`

- All three have exact city-level DiDi evidence but zero current canonical city/alias matches.
- Create canonical city/brief/BP records only from the sourced facilities; unresolved coordinates and opposite island landings stay null.
- All five candidate corridors remain `route_id: null` until sealed.
- Preserve 2025 La Paz→Mazatlán 49,714 and Mazatlán→La Paz 52,544 as incumbent long-distance ferry observations only. Do not transfer them to Navier economics without a documented product/range/geometry decision.

### 2. APAC registry + geometry

#### Australia / New Zealand

Input: `handoff/didi-ex-china/waves/DIDI-AUSTRALIA-NEW-ZEALAND-DEEPENING-2026-07-09.json`

- Purge the ten Kotor/Montenegro stamps from New Zealand first.
- Add partner-neutral cluster briefs for Australia and New Zealand and a missing Wellington brief after exact checkout reconciliation.
- Exact DiDi city proof: Brisbane, Gold Coast, Sydney, Auckland, Wellington. Whitsundays and Bay of Islands are not exact-city proven.
- Candidate route IDs and annual route pax remain null until exact matching and sourcing.

#### Japan / Hong Kong / Taiwan

Input: `handoff/didi-ex-china/waves/DIDI-JAPAN-HONG-KONG-TAIWAN-DEEPENING-2026-07-09.json`

- Preserve DiDi Mobility Japan's DiDi–SoftBank JV framing and exact supported-city roster.
- Exact-match existing Atlas routes/BPs before assigning any IDs; all research candidates currently hold `route_id: null`.
- Hong Kong DiDi current-service status remains verification-needed; an app-store listing is not enough.
- Taiwan is a hard operation-status gate. Current Kaohsiung–Penghu ferry evidence does not prove current DiDi Taiwan operation.
- Macau remains held from current-operation claims absent an exact receipt.
- Route-level annual pax remain null.

### 3. Egypt registry + geometry

Input: `handoff/didi-ex-china/waves/DIDI-EGYPT-DEEPENING-2026-07-09.json`

- Cairo exact DiDi evidence exists. Hurghada, El Gouna, Safaga, and Sharm local DiDi coverage is not proven.
- Validate Cairo river-bus stations and Red Sea passenger gates with current authority/operator coordinates.
- Keep Red Sea cruise/ferry gateways separate from daily tourism excursions and protected-area POIs.
- All route IDs and annual route pax remain null. Airport/national tourism totals do not enter finance.
- Marine geometry requires human-reviewed port, reef, protected-water, lagoon, and international-crossing waypoints.

## Per-wave return receipt

Return one receipt per wave containing:

- canonical city IDs added/retained/held, with source and exact operation-status class;
- BP IDs added/retained/held/dropped, with parent city and authority source;
- route IDs added/retained/removed, with exact endpoints and duplicate/stamp audit;
- cluster inheritance deltas and no-shrink result;
- all demand/fare rows joined by route ID, with null count and excluded-context ledger;
- full sub-proposal/page status by jurisdiction;
- Gate G, strict partner inheritance, finance inheritance, linkage, and render outcomes;
- commit hash and explicit remaining blockers.

Do not edit the live deck directly. Source JSON and route-keyed economics feed deterministic deck generation after Jaideep's merge decision.
