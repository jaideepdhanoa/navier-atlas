# DiDi × Navier — Ex-China Coverage Audit and Grand-Slam Build Plan

**Date:** 9 July 2026  
**Status:** `research-needed / repair-needed`  
**Scope:** DiDi outside mainland China; direct operations, owned local brands, and the Japan taxi joint venture. Aggregation-only markets are not presented as direct DiDi operations.

## Executive verdict

DiDi is a strong candidate for a Bolt/Grab-depth proposal, but its current Navier proposal is not a safe base to extend. The narrative shell is good; the geography and economics chain are not.

The verified/core ex-China operating footprint is:

- **Latin America:** Mexico, Brazil through **99**, Colombia, Chile, Costa Rica, Panama, Argentina, Ecuador, Peru, Dominican Republic.
- **Asia-Pacific:** Australia, New Zealand, Japan through **DiDi Mobility Japan**, Hong Kong.
- **Africa / MENA:** Egypt.
- **Taiwan:** retained in scope as Jaideep’s confirmed market seed, but current direct-operation evidence still needs to be closed before partner-facing “current footprint” wording or economics.

This produces a target of **16 jurisdictions, 17 full sub-proposals, 14 existing Atlas clusters, 43 canonical member-city IDs in the involved clusters (42 intended plus Macau as a scope-conflict hold), two true registry gaps (Chile and Argentina), 821 active member-touching route records before hygiene, and 2,130 existing POIs to classify into usable boarding points / non-BPs / drops**.

The current DiDi proposal has only **seven full market pages across six countries**. Ecuador, Peru, Australia, New Zealand, Japan, Egypt, Hong Kong, and Taiwan are absent. Chile and Argentina do not yet have canonical Atlas clusters. Mexico, Colombia, and several city briefs are too thin. The current finance chain is stale and contradictory: the durable finance model has no DiDi corridor spine; a recalculation file contains 38 rows but only eight route IDs still resolve; the page still displays a **$5.8M floor and $1.53B journey-spend headline** that current aggregate files cannot reproduce. DiDi’s old growth file also references Grab’s greenfield census, which must be removed.

**Recommendation:** rebuild DiDi from the geography outward, not by extending the current numbers. Mexico is Wave 1 and the calibration market. Latin America is the main commercial story. APAC and Egypt follow on the same exact-ID, shared-corridor, source-backed economics standard.

---

## 1. Operating-footprint audit

### 1.1 Included operating markets

| Region | Market | Operating treatment | Atlas state | Target full sub-proposal |
|---|---|---|---|---|
| Latin America | Mexico | Direct DiDi | Existing `mexico` cluster; deep but needs hygiene and density work | Mexico Pacific; Mexico Caribbean |
| Latin America | Brazil | Owned brand **99** | Existing `brazil` cluster | Brazil / 99 |
| Latin America | Colombia | Direct DiDi | Existing `colombia` cluster; Cartagena strong, Barranquilla thin | Colombia Caribbean |
| Latin America | Chile | Direct DiDi | **True registry gap** | Chile Pacific |
| Latin America | Costa Rica | Direct DiDi | Existing `costa-rica` cluster | Costa Rica |
| Latin America | Panama | Direct DiDi | Existing `panama` cluster | Panama |
| Latin America | Argentina | Direct DiDi | **True registry gap** | Argentina waterways / coast |
| Latin America | Ecuador | Direct DiDi | Existing `galapagos-ecuador`; route stamping is currently corrupted | Ecuador / Galápagos |
| Latin America | Peru | Direct DiDi | Existing `peru` cluster | Peru Pacific |
| Latin America | Dominican Republic | Direct DiDi | Existing `dominican-republic` cluster | Dominican Republic |
| Asia-Pacific | Australia | Direct DiDi | Existing `australia` cluster | Australia |
| Asia-Pacific | New Zealand | Direct DiDi | Existing `new-zealand`; ten foreign routes currently mis-stamped | New Zealand |
| Asia-Pacific | Japan | DiDi Mobility Japan taxi JV | Existing `japan` cluster; strong briefs/geometry | Japan taxi-to-water network |
| Asia-Pacific | Hong Kong SAR | Current taxi operation | Existing `hong-kong-macau`; partner-scope conflict must not overclaim Macau | Hong Kong |
| Asia-Pacific | Taiwan | Scope seed; current-status verification gate | Existing `taiwan` cluster | Taiwan, only after status gate |
| Africa / MENA | Egypt | Direct DiDi | Existing `egypt` cluster | Egypt / Nile and Red Sea |

### 1.2 Explicit exclusions from the direct-operating proposal

- **Singapore, South Korea, Malaysia, Thailand, Indonesia, Cambodia, Vietnam, Philippines:** DiDi’s overseas-travel aggregation layer, not a direct DiDi operating footprint. They may be mentioned as product reach, but they do not receive direct-operation sub-proposals or partner economics in this build.
- **South Africa and Kazakhstan:** historical exits.
- **Mainland China:** deliberately excluded from this proposal.
- **Macau:** a member of the current Hong Kong–Macau Atlas cluster, but not proven as a current DiDi operating market in this audit. It must not leak into DiDi’s visible footprint merely because Hong Kong is in the same geography cluster.

### 1.3 Source inventory already captured

The source-led pass captured **1,465 DiDi/99 city or service-area rows**: 1,406 city-supported and 59 cleanup-needed. Of these, 179 were classified high marine relevance and 41 medium. This is a discovery inventory, not permission to bulk-add every city.

Strongest sources include:

- DiDi’s [current operating-country help page](https://web.didiglobal.com/au/help-center/how-many-countries-does-didi-operate-in/).
- Official city pages for [Mexico](https://web.didiglobal.com/mx/conductor/ciudades/), Colombia, Chile, Costa Rica, Panama, Argentina, Ecuador, Peru, and the Dominican Republic.
- 99’s [official city index](https://99app.com/cidades/) and [DiDi ownership page](https://99app.com/quem-somos/).
- DiDi Australia’s [28-city availability list](https://web.didiglobal.com/au/help-center/where-is-didi-available/).
- DiDi New Zealand’s current service pages.
- DiDi Mobility Japan’s [service-area page](https://didimobility.co.jp/service/user/) and March 2026 33-prefecture expansion release.
- The live [DiDi Egypt](https://web.didiglobal.com/eg/) passenger and driver flows.
- Current Hong Kong app-store and Google Play listings advertising Hong Kong taxi and cross-border car service.

---

## 2. Atlas coverage audit

### 2.1 Current proposal versus target

| Measure | Current DiDi | Target |
|---|---:|---:|
| Full market/sub-proposal pages | 7 | 17 |
| Jurisdictions represented | 6 | 16 |
| Existing canonical clusters in scope | Partial | 14 |
| Canonical member-city IDs in target clusters | Partial | 43 |
| True registry gaps | Unaddressed | 2: Chile, Argentina |
| Source city/service rows | Not reconciled | 1,465 captured |
| Partner-owned finance spine | Broken | Full route-ID-identical spine for every promoted cluster |
| Reproducible economics | No | Yes, every promoted market |
| Transparent economics sheet | Missing | One live in-place sheet, linked from proposal/deck |
| Deck registration/build artifacts | Missing | Full Deck Studio package after data seal |

### 2.2 Existing cluster coverage

The 14 existing clusters contain **821 active member-touching routes before the required hygiene pass** and **2,130 POIs**. Those are not all automatically valid DiDi corridors or boarding points. Every route must survive cluster stamping, land-crossing, duplicate, range, and endpoint checks; every POI must be classified as a usable BP, a non-BP, or a reasoned drop.

The most important known defects are:

1. **Finance identity is broken.** `finance/model/corridors.json` has no DiDi spine. The old recalculation contains 38 corridors, only eight current route IDs, and 30 stale IDs.
2. **Displayed economics are non-reproducible.** The proposal shows nonzero economics while the current aggregate is zero.
3. **Borrowed census.** The DiDi growth file points to `grab-greenfield-census.json`; this is forbidden. Use a DiDi census or the clearly labelled global template band.
4. **Route stamping defects.** The Galápagos cluster has 46 stamped routes but only three routes actually touch Galápagos member cities. Mexico has 21 foreign-stamped routes. New Zealand has ten Kotor routes mis-stamped into its cluster.
5. **Scope leakage.** Current map scope contains Shanghai, Macau, and non-city Mexico market IDs. Mainland China must be removed; Macau needs an explicit resolution; city and market IDs must not be mixed.
6. **Thin city coverage.** Cozumel, Playa del Carmen, and Barranquilla are already in DiDi scope but lack full sub-proposals. Ecuador and Peru have seven canonical cities absent from DiDi.
7. **Brief gaps.** Pisco/San Andrés, Wellington, and Red Sea Egypt are missing city briefs. Australia, New Zealand, and Hong Kong–Macau lack cluster briefs. Several existing briefs are complete structurally but not mature sales narratives.
8. **Country-cost gaps.** Country-reference rows are missing for multiple promoted markets. No economics cascade can run until every country has a source-tiered row; otherwise the model silently applies Singapore costs.

### 2.3 Coverage-density queue

**Promote to full immediately after hygiene**

- Mexico: Cancún/Riviera Maya, Los Cabos, Puerto Vallarta.
- Brazil: Rio, Angra/Ilha Grande, Florianópolis.
- Colombia: Cartagena.
- Costa Rica: Nicoya/Papagayo.
- Panama: San Blas.
- Dominican Republic: Samaná.

**Thin → full**

- Cozumel.
- Playa del Carmen.
- Barranquilla.

**New display coverage from existing Atlas hierarchy**

- Ecuador: Santa Cruz, Isabela, San Cristóbal, Floreana.
- Peru: Lima, Paracas, Pisco/San Andrés.
- Australia: Brisbane, Gold Coast, Sydney, Whitsundays.
- New Zealand: Auckland, Bay of Islands, Wellington.
- Japan: Tokyo Bay, Setouchi, Okinawa, Izu Peninsula, Izu Islands, Miyako, Yaeyama, Hokkaido/Niseko.
- Egypt: Cairo, Hurghada/El Gouna, Sharm el-Sheikh, Red Sea.
- Hong Kong: Hong Kong city only until Macau treatment is resolved.
- Taiwan: Kaohsiung and Penghu after current-status verification.

**True registry expansion**

- Chile.
- Argentina.

---

## 3. Target proposal architecture

### 3.1 Hub narrative

**Core thesis:** DiDi and 99 already organize the road journey at immense scale. Navier extends that customer relationship across the water, allowing one mobility platform to own the trip from curb to coast, airport to island, and city center to waterfront.

The hub should lead with three region stories:

1. **Latin America — the commercial core:** Mexico and Brazil as anchors; Caribbean, Pacific, island, and urban-water use cases across the region.
2. **Asia-Pacific — localized operating models:** direct DiDi in Australia/New Zealand/Hong Kong, taxi infrastructure through DiDi Mobility Japan, and a separately verified Taiwan lane.
3. **Egypt — the MENA bridge:** urban/Nile access and Red Sea resort mobility, without pretending aggregation-only Asian markets are direct operations.

The deck and site must use plain English. Internal build terminology never appears. The visible economics ladder may use SOM/SAM/TAM/GMV only with plain-English descriptors; the Google Slides convention is **“SOM full network (~XX% capture, today, +greenfield)”**.

### 3.2 Seventeen full sub-proposals

1. Mexico — Pacific.
2. Mexico — Caribbean.
3. Brazil / 99.
4. Colombia Caribbean.
5. Chile Pacific.
6. Costa Rica.
7. Panama.
8. Argentina waterways / coast.
9. Ecuador / Galápagos.
10. Peru Pacific.
11. Dominican Republic.
12. Australia.
13. New Zealand.
14. Japan / DiDi Mobility Japan.
15. Hong Kong.
16. Taiwan — after verification gate.
17. Egypt / Nile and Red Sea.

Every sub-proposal must carry the full Grab/Bolt-quality field set: hero, summary, why now, partner context, multimodal fit, journeys unlocked, proof points, objections, end state, why Navier now, ask, close, three phases, route-bound featured corridors, fleet confidence, and per-market vessel sizing. Roll-up stubs do not count.

### 3.3 Brief and narrative standard

For each of the 14 existing clusters and two new registry markets:

- Read and score the existing canonical cluster and city briefs first.
- Enhance in place field-by-field; do not replace a better canonical paragraph with generic DiDi prose.
- Keep canonical briefs partner-neutral. DiDi-specific positioning lives only in the DiDi partner JSON.
- Each city brief must include source-backed demand signals, waterfront use cases, transfer pain, Navier fit, and real signature routes.
- Each BP record must carry stable ID, coordinates, type, source URL, source date, operator/authority, water adjacency, city/cluster IDs, and keep/drop reason.
- Every accepted BP must either appear in the sealed POI set or in a drop ledger. Acceptance is **zero silent drops**.

---

## 4. Mexico and Latin America economics plan

### 4.1 Mexico is the calibration market

Mexico receives the deepest build and goes first. It remains two complete commercial stories:

- **Pacific:** Los Cabos and Puerto Vallarta/Riviera Nayarit, followed by source-led evaluation of La Paz, Mazatlán, Acapulco, Ensenada, Manzanillo, Guaymas, Puerto Escondido, and other verified DiDi coastal cities.
- **Caribbean:** Cancún/Riviera Maya, Cozumel, Playa del Carmen, with source-led evaluation of Chetumal/Campeche and genuine island-transfer markets.

The current five canonical Mexico city IDs remain the initial geometry base. No new city or pier is added from a name alone. Each promoted city needs real terminals/marinas/public piers, source evidence, clean water geometry, and full demand/fare records.

### 4.2 Economics source hierarchy

For every promoted Latin American corridor, Tasklet must source:

1. Annual passenger trips or a defensible origin/destination demand pool from port authorities, ferry regulators/operators, tourism authorities, airport/visitor flows, or public transport agencies.
2. Current one-way fare or a transparent substitute-cost basis.
3. Seasonality and service-days assumptions.
4. Capture rate specific to DiDi/99’s platform role.
5. Fleet basis and range-gated vessel assignment.
6. Country opex, energy, labor, marina, grid-carbon, and commercial CAPEX reference.

Priority public-source families:

- **Mexico:** APIQROO, ASIPONA/SEMAR, state port administrations, ferry operators, tourism/airport authorities.
- **Brazil:** ANTAQ, state ferry authorities/operators, municipal maritime systems, tourism and airport flows.
- **Colombia:** DIMAR, transport/tourism authorities, Cartagena and Caribbean operators.
- **Chile:** MTT, DIRECTEMAR, port/ferry operators and regional tourism agencies.
- **Costa Rica:** transport/port authorities, ICT, airport and resort-transfer flows.
- **Panama:** Autoridad Marítima de Panamá, ATP, airport and Guna Yala visitor flows.
- **Argentina:** national/provincial port authorities, ferry operators, tourism agencies, river-system data.
- **Ecuador:** Galápagos authorities, ABG/port data, visitor and inter-island transfer flows.
- **Peru:** APN/MTC, port operators and tourism data.
- **Dominican Republic:** APORDOM, tourism ministry, airport/resort/port flows.

No uniform 25K/30K placeholder, no borrowed peer census, and no invented L3 demand. If a route lacks an honest anchor, its economics remain null while the geography can still display.

### 4.3 Finance inheritance and outputs

For every shared market:

- The **route-ID spine must be identical** to the global canonical routes inherited by every partner in that cluster.
- Only the DiDi overlay may vary: `L3_locals`, capture rate, archetype, and fleet basis.
- The durable registry uses real geography keys, never a catch-all `didi` market.
- Mexico’s DiDi spine must match every other partner in `mexico`; the same applies to Colombia, Peru, Ecuador, and all shared geographies.

Required economics outputs:

- Grounded current-network revenue floor.
- Full-network revenue including clearly labelled greenfield template upside until DiDi supplies its own census.
- Addressable journey-spend pool.
- DiDi platform revenue opportunity.
- Phase economics and fleet sizing.
- Route-level economics sidecar keyed to current sealed route IDs.
- One transparent live Google Sheet updated in place.
- Growth-case JSON, partner JSON, data-clean JSON, and master tracker in agreement.

---

## 5. Tasklet ↔ Grok handoff / handback sequence

The work should run as a controlled baton pass. No phase advances without its receipt.

### Pass 0 — Scope freeze

**Tasklet hands off**

- Verified country/status ledger.
- Raw official city inventory and normalized marine-relevance triage.
- Current Atlas coverage matrix.
- Explicit exclusions and holds: mainland China, aggregation-only markets, historical exits, Macau scope issue, Taiwan verification gate.
- Anchor-city crosswalk draft.

**Grok hands back**

- Exact ID reconciliation report.
- Clean DiDi scope with no Shanghai/China leakage and no market IDs in city-ID arrays.
- Proposal/map/full-market roster diff.

**Gate:** 16-jurisdiction scope is explicit; no unsupported country is presented as a direct operation.

### Pass 1 — Global route and cluster hygiene

**Tasklet hands off**

- Defect ledger for Mexico, Galápagos, New Zealand, Hong Kong/Macau, and every target cluster.
- Canonical city/cluster membership list.

**Grok hands back**

- Corrected global route stamping.
- Dedupe, land-crossing, orphan, endpoint, and quarantine report.
- Global inheritance validation.

**Gate:** routes belong to geography once; DiDi does not carry a hand-curated subset.

### Pass 2 — BP and brief deepening

**Tasklet hands off**

- Full BP source manifests for each target city.
- New Chile and Argentina city/BP research.
- Enhanced canonical cluster/city briefs.
- Drop ledger rules.

**Grok hands back**

- Deterministically promoted BPs and city IDs.
- Route candidates with stable IDs or explicit rejects.
- Zero-silent-drop coverage report.

**Gate:** every researched BP is accepted or reasoned; no invented pier; no land crossing.

### Pass 3 — Mexico seal and calibration

**Tasklet hands off**

- Mexico Pacific and Caribbean BP manifests.
- Demand/fare source records for every promoted corridor.
- Country-reference preflight.
- Canonical marquee candidates after route seal.

**Grok hands back**

- Mexico route seal with current route IDs.
- Render QA for all five canonical Mexico cities and any newly accepted cities.
- Partner inheritance and marquee-subset receipts.

**Gate:** Mexico geometry is clean and all partner views in Mexico inherit the identical corridor set.

### Pass 4 — Mexico economics and proposal

**Tasklet executes**

- Build DiDi’s partner overlay on the sealed Mexico spine.
- Run aggregate → growth → frontend block → partner splice.
- Build/update the transparent Sheet and validate both economics engines agree.
- Author the two full Mexico sub-proposals from the sealed routes and sourced economics.

**Grok hands back**

- Route-keyed economics sidecar against the new gold.
- Resealed DiDi partner page and linked economics rungs.
- Render and parity receipt.

**Gate:** Mexico’s numbers reproduce from source records and the site, JSON, sheet, and sidecar agree.

### Pass 5 — Remaining Latin America in waves

Wave A: Brazil, Colombia, Costa Rica, Panama, Dominican Republic.  
Wave B: Ecuador, Peru.  
Wave C: Chile and Argentina after new registry/geometry.

Each wave repeats the BP → seal → demand/fare → finance → sub-proposal → sidecar → render loop. This prevents a giant late-stage merge with untraceable failures.

### Pass 6 — APAC and Egypt

- Australia and New Zealand as direct app markets.
- Japan explicitly framed around DiDi Mobility Japan and local taxi integration.
- Hong Kong direct taxi story, with Macau held unless proven.
- Taiwan activated only after the current-status gate.
- Egypt as direct MENA operation, with Cairo/Nile and Red Sea use cases kept distinct.

### Pass 7 — Hub, sheet, and deck package

After all promoted markets pass geometry and economics:

- Reconcile 17 sub-proposals, network footprint, map scope, and full-market rosters.
- Run Gates A–G and the finance-inheritance gate.
- Register Deck Studio only after opening `deck-studio/decks/didi/deck.config.json` first.
- Grok generates the deterministic model-to-deck package.
- Atlas screenshots remain Jaideep insert slots.
- Live Slides edits are API-only; no PPTX round-trip, no full replacement.
- If a live slide is directly corrected, fix the source JSON without asking Grok to rebuild that deck.

---

## 6. PR / delivery sequence

Recommended small, reviewable PRs:

1. **DiDi scope + operating-status ledger + no-shrink baseline.**
2. **Global route-stamping/hygiene fixes for target clusters.**
3. **Mexico briefs/BPs/source manifests.**
4. **Mexico sealed geometry and canonical marquees.**
5. **Mexico finance spine + partner overlay + two full sub-proposals.**
6. **Latin America Wave A.**
7. **Latin America Wave B.**
8. **Chile/Argentina registry expansion.**
9. **APAC + Egypt coverage and full sub-proposals.**
10. **Full finance cascade, live Sheet, sidecar, master tracker.**
11. **Deck Studio config, slide manifest, asset library, deterministic deck build.**
12. **Final Gates A–G, render QA, deck PDF QA, and delivery receipts.**

Merges remain Jaideep’s call. Partner-facing outreach stays draft-only.

---

## 7. Definition of done

DiDi may be called **proposal-complete** only when:

- All 17 approved sub-proposals are full pages, not stubs.
- Every in-scope anchor city resolves by exact ID.
- Map scope, market pages, and network footprint reconcile.
- Every partner inherits the same canonical corridors in shared markets.
- Every finance route-ID spine matches geography exactly.
- Every promoted corridor has sourced demand/fare or honest-null economics.
- No country uses silent Singapore cost fallback.
- No peer greenfield census is borrowed.
- The live Sheet, growth JSON, partner JSON, data-clean JSON, sidecar, and master tracker agree.
- BP audit shows zero silent drops.
- Global and partner render QA show zero land crossings/orphans.
- Partner-facing copy gate and deck copy lint pass.
- The deck has a committed logo file plus provenance before it is called banked.
- Final render, sheet, sidecar, deck, and delivery receipts exist.

Until then, use exact statuses: `research-needed`, `research-complete / seal-needed`, or `seal-complete / cascade-needed`.

## Immediate next move

Start **Pass 0 + Pass 1**, then run **Mexico Pacific and Caribbean as the calibration build**. Do not touch the old DiDi headline economics except to mark them stale; rebuild them from the sealed Mexico/LatAm route spines and source records. This sequence gives us the fastest credible path to a true Bolt/Grab-quality DiDi proposal without carrying old data debt into the deck.
