# India + GCC Partner Proposal Build Plan

## Objective

Build eight partner proposals to **Grab / Careem parity**, using the latest user decisions from 20 Jun 2026:

1. **Uber India**
2. **Rapido India**
3. **Ola India**
4. **Reliance**
5. **Adani**
6. **Ras Al Khaimah Transport Authority**
7. **Bahrain Ministry of Transportation and Communication**
8. **Noon**

The common standard is: grounded Atlas coverage, partner-specific route logic, two local use cases per promoted market, complete TAM/economics ladder, transparent Sheets, sidecar economics, and full proposal rendering rather than stub pages.

Important operating constraints:

- Use existing Atlas hierarchy and shared corridors first; additions should go through registry / geometry / economics gates.
- Display can lead economics where geometry exists, but proposal-ready Phase 3 markets need at least **two local use cases**.
- No invented geography; null beats confidently wrong.
- Authority proposals may be built normally; do not include special outreach-blocker language in this plan.

---

## Executive plan

This should be one coordinated build, not eight isolated decks.

The core idea:

- **Uber India, Rapido India, Ola India, Reliance, and Adani** should reuse the **same India corridor spine** where possible, with partner-specific positioning and selected additions.
- **Ola** should be India-focused for this pass unless fresh source evidence shows active non-India ride-hailing operations. Public reporting indicates Ola exited the UK, Australia, and New Zealand ride-hailing markets in 2024, so no international overlay should be promoted by default.
- **Noon** should mirror the **Careem UAE + cross-border operating logic**, framed as another super-app mobility service with full-journey GMV.
- **RAKTA** should be a compact public-authority proposal focused on **RAK domestic mobility**, then inter-emirate and selected Gulf cross-border corridors.
- **Bahrain MOTC** should be a compact sovereign/public-transport proposal focused on **Bahrain domestic mobility**, then KSA Eastern Province, Qatar, Dubai, and Abu Dhabi connectivity.

Recommended build sequence:

1. **Shared corridor inventory and source-of-truth audit**
2. **India corridor spine** for Uber India / Rapido India / Ola India / Reliance / Adani
3. **UAE + Gulf cross-border spine** for Noon / RAKTA / Bahrain MOTC
4. Partner-specific coverage binding
5. Local use-case matrix
6. Economics cascade
7. Proposal pages + render QA
8. Grok sealing / sidecar / gold export package

---

## Workstream A — Shared corridor audit

### A1. Inventory existing reusable corridors

Create two reusable corridor workbooks / JSON ledgers:

#### India shared corridor spine

For Uber India, Rapido India, Ola India, Reliance, and Adani.

Fields:

- `corridor_id`
- `market_key`
- `country`
- `state_or_region`
- `from_node_id`
- `to_node_id`
- `from_label`
- `to_label`
- `route_nm`
- `vessel_gate`
- `current_geometry_status`
- `current_economics_status`
- `usable_by_uber_india`
- `usable_by_rapido_india`
- `usable_by_ola_india`
- `usable_by_reliance`
- `usable_by_adani`
- `evidence_notes`
- `addition_needed`

#### UAE / Gulf shared corridor spine

For Noon, RAKTA, and Bahrain MOTC.

Fields:

- `corridor_id`
- `market_key`
- `country_or_cross_border_pair`
- `from_node_id`
- `to_node_id`
- `from_label`
- `to_label`
- `route_nm`
- `vessel_gate`
- `domestic_or_cross_border`
- `usable_by_noon`
- `usable_by_rakta`
- `usable_by_bahrain_motc`
- `authority_or_platform_relevance`
- `economics_status`
- `regulatory_note`

### A2. Do not duplicate routes

The shared network should remain shared. Partner files should reference the same registry corridors rather than creating partner-specific duplicates unless the route is truly new or asset-specific.

### A3. Re-gate vessels before phasing

Every route must be range-gated:

- **≤ 70nm** → N30 Pioneer II now; N35 Shuttle may appear in Scale for dense corridors.
- **75–150nm** → Quanta-LR roadmap / amber-dashed.
- **>150nm** → Quanta-LR flagged for review; do not pretend it is an N30 route.

---

## Workstream B — India corridor spine

### Partners covered

- Uber India
- Rapido India
- Ola India
- Reliance
- Adani

### Shared assumption

These five should use the **same India corridors already in Atlas**, plus selective additions only where the partner has a credible route/use-case reason. The India spine should be broad enough to support mobility-platform proposals and asset-origin proposals without duplicating route geometry.

### Accepted India corridor baseline

The accepted India baseline for this pass is:

1. **Mumbai / Maharashtra waterfront corridors**
2. **Kerala corridors**
3. **Andaman Islands corridors**
4. **Goa corridors**

These are the initial shared spine for Uber India, Rapido India, Ola India, Reliance, and Adani. Partner files should inherit these corridors first before any new India geography is added.

### Allowed India extensions for this pass

Extensions are allowed only if they make sense against the existing Atlas hierarchy, can be grounded to real coastal/waterfront use cases, and pass the ID/registry/economics gates. Recommended additions to evaluate, in priority order:

1. **Gujarat port/coastal spine** — especially where Adani ports/coastal assets create a strong asset-origin reason; use for Adani first, then consider platform inheritance only where city/region evidence supports it.
2. **Tamil Nadu / Chennai coast** — large urban coastal market, airport/waterfront transfer logic, commuter bypass potential; useful for mobility platforms if Atlas nodes exist or can be cleanly added.
3. **Andhra Pradesh / Visakhapatnam coast** — port/city/tourism gateway logic; prioritize if it links to Adani or existing Atlas coastal hierarchy.
4. **West Bengal / Kolkata-Haldia-Sundarbans edge** — evaluate carefully for waterfront/riverine mobility and tourism; keep exact-bind only.
5. **Lakshadweep** — only if already grounded or explicitly green-lit; otherwise keep as backlog because of access/regulatory sensitivity.

Do **not** bulk-add India coastal states. The rule is: accepted baseline first, then partner-specific additions with local use cases and stable IDs.

### B1. Uber India

#### Archetype

Mobility-platform partner.

#### Coverage logic

Use Uber India as a broad mobility platform and inherit existing Atlas coastal/waterfront India markets where Uber India presence supports the country/city/region.

#### Proposal shape

Uber India should look closest to Grab/Uber-style platform proposals:

- hub page,
- full subpages for promoted India markets,
- ride-hail + marine first/last-mile integration,
- airport/waterfront/resort/business routes,
- partner platform revenue from Navier journeys.

#### Required work

1. Confirm Uber India market presence at country and key-city level.
2. Bind to existing India Atlas corridors.
3. Promote only markets with at least two local use cases.
4. Build India-specific TAM ladder and platform-revenue case.
5. Add full subpages for promoted markets.

#### Likely use-case families

- airport ↔ waterfront / CBD transfer,
- coastal business district ↔ tourism district,
- island / ferry-adjacent premium mobility,
- event and hospitality transfers,
- premium commuter bypass where road congestion is severe.

---

### B2. Reliance

#### Archetype

Conglomerate / platform / real-estate / energy / consumer ecosystem partner.

#### Coverage logic

Reliance should not be treated as “all India.” It should inherit the India corridor spine where Reliance has a credible asset, customer, real-estate, retail, telecom, event, or energy ecosystem reason.

#### Proposal shape

Reliance should be an **asset + platform-origin** proposal:

- **Jio / consumer reach as the lead wedge**,
- premium customer mobility,
- waterfront real estate / event / retail corridors,
- energy / charging / infrastructure as supporting thesis,
- corporate and captive mobility where assets support it.

#### Required work

1. Map Reliance-relevant coastal/waterfront assets and platform hooks.
2. Overlay those onto the existing India corridor spine.
3. Mark each corridor as:
   - direct asset-supported,
   - platform-supported,
   - speculative / brief-only,
   - exclude.
4. Add local use cases per promoted market.
5. Build economics around the combined Jio-led consumer platform + asset/infrastructure value, not generic ride-hail revenue only.

#### Likely use-case families

- premium retail / destination access,
- event mobility,
- waterfront real-estate access,
- employee / campus / corporate shuttle,
- Jio-enabled booking / loyalty / distribution,
- energy / charging partnership narrative where grounded.

---

### B3. Adani

#### Archetype

Infrastructure / ports / airports / logistics / real-estate partner.

#### Coverage logic

Adani should be built from **asset-origin routes**, not a general India map. Reuse the India corridor spine where it overlaps with Adani ports, airports, coastal infrastructure, tourism gateways, or real-estate assets.

#### Proposal shape

Adani should lead with **ports and coastal real estate**, not airports as the primary wedge. Airports can support specific local corridors where relevant, but the headline should be coastal infrastructure and destination access:

- port / waterfront-city mobility,
- coastal real-estate access and destination unlocks,
- port-city / cruise / ferry-adjacent use cases,
- passenger transfer and tourism unlocks,
- potential low-emission maritime infrastructure narrative,
- asset-level phased deployment.

#### Required work

1. Build Adani coastal asset inventory.
2. Bind assets to existing India corridors.
3. Identify additions only where a major Adani asset lacks a currently usable Atlas corridor.
4. Split routes into:
   - ready shared corridors,
   - asset-specific additions,
   - future registry gaps.
5. Build economics around asset throughput, airport/port transfer demand, tourism, and premium mobility.

#### Likely use-case families

- port / cruise terminal ↔ city / airport,
- port-campus employee shuttle,
- coastal real-estate access,
- tourist gateway transfer,
- strategic low-emission maritime corridor pilot.

---

### B4. Rapido India

#### Archetype

Mobility-platform partner focused on two-wheeler, auto, taxi, and urban mobility distribution. Rapido stays in the normal mobility lane, not the hotel/property-origin lane.

#### Coverage logic

Rapido India should reuse the India corridor spine where Rapido has credible India operating presence and where Atlas already supports coastal/waterfront markets. Because Rapido is mass-market and city-mobility oriented, its Navier story should focus less on premium chauffeur-style journeys and more on **last-mile distribution, commuter bypass, urban congestion relief, and app-based demand aggregation**.

#### Proposal shape

Rapido should be a platform-mobility proposal with India-market subpages where promoted:

- app distribution for ferry/marine legs,
- first/last-mile completion around waterfront nodes,
- commuter and airport/waterfront use cases,
- integration with bike/auto/taxi modes,
- lower-friction adoption narrative versus luxury-only positioning.

#### Required work

1. Confirm Rapido India operating footprint at country/key-city level.
2. Bind Rapido to the existing India corridor spine by city/region evidence or country-supported inheritance where appropriate.
3. Promote only Atlas-backed coastal/waterfront markets with at least two local use cases.
4. Inherit the standard mobility-platform economics initially. Do **not** lower average ticket or take-rate for Rapido in this pass because the current instruction is to use standard mobility-platform assumptions.
5. Build subpages for promoted India markets; leave unsupported coastal candidates as brief-only/backlog.

#### Likely use-case families

- commuter first/last-mile to marine nodes,
- waterfront congestion bypass,
- airport/rail/bus ↔ waterfront transfer,
- event and tourism access,
- app-distributed short marine legs paired with bike/auto/taxi completion.

---

### B5. Ola India

#### Archetype

Mobility-platform partner with an India core. International markets are **not in scope by default** for this pass.

#### Current international-scope finding

Ola previously operated in the **UK, Australia, and New Zealand**, but public reporting from 2024 says Ola exited those international ride-hailing markets to focus on India. Source check: Reuters and TechCrunch both reported the UK/Australia/New Zealand exit in April 2024. Therefore:

- Focus the proposal on **India**.
- Do not promote UK / Australia / New Zealand markets.
- Do not build an international overlay unless fresh evidence shows active non-India Ola operations.
- If any non-India footprint evidence emerges later, keep it **display-only / validation-pending** until exact city/region validation and Atlas grounding are complete.

#### Coverage logic

Ola should reuse the India corridor spine for India. Treat it like Uber/Rapido: inherit accepted India corridors first, then consider only grounded extensions with two local use cases.

#### Proposal shape

Ola should be an India mobility proposal:

- India as the anchor and only active market scope for this pass,
- platform distribution and multimodal integration,
- full subpages for promoted India markets,
- brief-only treatment for unsupported India candidates that lack geometry or local use-case depth.

#### Required work

1. Confirm Ola India coverage and source-led operating footprint.
2. Bind Ola to the accepted India corridor baseline: Mumbai, Kerala, Andaman Islands.
3. Evaluate allowed extensions: Goa, Gujarat port/coastal spine, Tamil Nadu/Chennai, Andhra Pradesh/Visakhapatnam, West Bengal/Kolkata-Haldia-Sundarbans edge, and possibly Lakshadweep only if grounded/green-lit.
4. Promote only markets with Atlas grounding and at least two local use cases.
5. Build economics under standard mobility-platform assumptions.
6. Keep any future international markets separated to avoid blended-cost or silent-country-reference errors.

#### Likely use-case families

- India airport/waterfront and commuter bypass corridors,
- marine legs distributed through Ola app demand,
- tourism and event mobility,
- multimodal transfer between road ride-hail and Navier marine service.

---

## Workstream C — UAE / Gulf spine

### Partners covered

- Noon
- Ras Al Khaimah Transport Authority
- Bahrain MOTC

### Shared assumption

Noon should mirror **Careem** geographically: domestic UAE plus cross-border from UAE. RAKTA and Bahrain MOTC are authority proposals with narrower domestic cores and selective cross-border routes.

---

### C1. Noon

#### Archetype

Consumer platform / e-commerce / delivery / super-app-adjacent partner.

#### Coverage logic

Noon should mirror Careem’s UAE-first logic:

1. Domestic UAE marine mobility,
2. UAE inter-emirate corridors,
3. Cross-border Gulf expansion from UAE.

#### Proposal shape

Noon should be a Careem-style UAE proposal, framed as a super-app service that Noon can offer to its consumer base:

- consumer app distribution,
- premium passenger booking,
- full-journey GMV logic like Careem,
- possible logistics / light parcel / concierge adjacency only if grounded,
- UAE-first mobility corridors,
- cross-border Gulf routes as expansion narrative.

#### Required work

1. Clone Careem-style UAE market structure as the starting geography pattern.
2. Replace Careem mobility narrative with Noon consumer-platform narrative.
3. Reuse domestic UAE and cross-border corridors where Atlas/economics already support them.
4. Build Noon-specific objections/responses: consumer trust, regulatory scope, operational fit, fulfillment vs passenger focus.
5. Run economics like Careem / mobility booking platform economics with full-journey GMV. Do **not** create a separate lower take-rate or e-commerce-only economics logic for Noon in this pass.

#### Likely route families

- Dubai ↔ Abu Dhabi,
- Dubai ↔ Sharjah / Ajman / RAK,
- Abu Dhabi ↔ islands / waterfront districts,
- UAE ↔ Musandam,
- UAE ↔ Doha,
- UAE ↔ Bahrain,
- UAE ↔ Muscat where range-gated correctly.

---

### C2. Ras Al Khaimah Transport Authority

#### Archetype

Emirate transport authority.

#### Coverage logic

RAKTA should focus on:

1. **RAK only** domestic / intra-emirate routes,
2. **RAK ↔ other UAE emirates**,
3. Cross-border from RAK / UAE to:
   - Musandam,
   - Muscat,
   - Doha,
   - Bahrain.

#### Proposal shape

RAKTA should be a public-authority proposal, not a generic mobility-platform deck.

It should emphasize:

- tourism and resort access,
- public transport modernization,
- low-emission maritime mobility,
- connectivity to UAE emirates,
- RAK as a northern Gulf mobility gateway,
- phased authority pilot.

#### Required work

1. Identify existing Atlas RAK nodes and domestic RAK corridors.
2. Bind RAK ↔ UAE emirate routes.
3. Bind or backlog RAK/UAE ↔ Musandam, Muscat, Doha, Bahrain routes.
4. Clearly separate commercial-now routes from Quanta-LR roadmap routes. For this plan, assume RAK cross-border routes to Musandam, Muscat, Doha, and Bahrain are **Quanta-LR roadmap**, not commercial-now.
5. Build public-value economics in addition to fare revenue:
   - tourism lift,
   - congestion relief,
   - airport/resort accessibility,
   - public transport coverage.
6. Create a hub-led proposal with phase detail rather than many country subpages.

#### Likely phases

- **Phase 1 — RAK proof:** short domestic / resort / waterfront pilots.
- **Phase 2 — UAE integration:** RAK ↔ Dubai / Sharjah / Abu Dhabi where viable.
- **Phase 3 — Gulf gateway:** Musandam, Muscat, Doha, Bahrain as range-gated expansion.

---

### C3. Bahrain Ministry of Transportation and Communication

#### Archetype

National transport ministry / sovereign public-mobility partner.

#### Coverage logic

Bahrain MOTC should focus on:

1. Bahrain domestic / island-country mobility,
2. Bahrain ↔ KSA Eastern Province,
3. Bahrain ↔ Doha,
4. Bahrain ↔ Dubai,
5. Bahrain ↔ Abu Dhabi.

#### Proposal shape

Bahrain MOTC should be a national transport modernization proposal.

It should emphasize:

- island-country marine mobility,
- integration with national transport policy,
- cross-border Gulf connectivity,
- tourism and business travel,
- alternative to congested/long road paths where applicable,
- staged regulatory and operational pathway.

#### Required work

1. Identify existing Atlas Bahrain nodes/corridors.
2. Bind Bahrain domestic opportunities.
3. Bind Bahrain ↔ KSA Eastern Province corridors.
4. Range-gate Bahrain ↔ Doha / Dubai / Abu Dhabi correctly. For this plan, assume **Manama ↔ KSA Eastern Province** is the only commercial-now cross-border candidate; Doha, Dubai, and Abu Dhabi are **Quanta-LR roadmap** unless later range/ops evidence says otherwise.
5. Build authority-facing economics:
   - direct fare revenue,
   - national mobility value,
   - tourism/business connectivity,
   - public-sector decarbonization narrative.
6. Create hub-led proposal with route/phase depth.

#### Likely phases

- **Phase 1 — Bahrain domestic proof:** high-confidence, short-range routes.
- **Phase 2 — KSA Eastern Province connection:** regional business/tourism corridor.
- **Phase 3 — Gulf capital connectivity:** Doha, Dubai, Abu Dhabi with correct vessel/range treatment.

---

## Workstream D — Partner-specific proposal parity gates

Each partner must pass the same gates before being called Grab/Careem-level.

### D1. Coverage and binding

For every promoted market/corridor:

- existing Atlas hierarchy or explicit registry addition,
- stable node IDs,
- no filename/anchor-city ID mismatch,
- map renders correctly,
- no silent drops.

### D2. Local use cases

Every proposal-ready market must have at least **two local use cases**.

If not:

- keep it as display-only,
- economics-pending,
- or brief-only backlog.

### D3. Economics

Each partner needs:

- aggregate model output,
- growth case,
- transparent Sheet,
- market/phase economics,
- vessel sizing,
- ladder transitions / show-math explanations,
- economics sidecar for gold export.

### D4. Subpage / hub parity

- Multi-market/platform partners need full subpages.
- Compact authority proposals can be hub-led, but must have deep route/phase sections.
- Roll-up stubs are not parity.

### D5. QA

Run:

- JSON parse,
- schema validation,
- renderer syntax check,
- anchor-city crosswalk,
- vessel re-gate ledger,
- economics model vs transparent Sheet consistency,
- live render check.

---

## Recommended execution order

### Step 1 — Build two shared spines

1. India shared corridor spine.
2. UAE / Gulf shared corridor spine.

Output:

- `india-shared-corridor-spine.json`
- `uae-gulf-shared-corridor-spine.json`
- status memo with ready / needs-addition / backlog counts.

### Step 2 — Build Noon first in the GCC batch

Reason: Noon can mirror Careem, so it is the fastest way to create a reusable UAE + cross-border template.

Output:

- Noon partner JSON draft,
- Noon growth/economics plan,
- Noon route/use-case matrix.

### Step 3 — Build RAKTA and Bahrain MOTC from the GCC spine

Reason: after Noon/Careem geography is reconciled, RAKTA and Bahrain MOTC can reuse the same UAE/Gulf corridor ledger but with authority-specific framing.

Output:

- RAKTA proposal draft,
- Bahrain MOTC proposal draft,
- cross-border route QA table.

### Step 4 — Build Uber India, Rapido India, and Ola India from the India spine

Reason: the three mobility-platform partners should share one India corridor foundation, while preserving partner-specific coverage and use-case logic. Rapido and Ola should inherit standard mobility-platform economics initially.

Output:

- Uber India coverage binding,
- Rapido India coverage binding,
- Ola India-only coverage binding,
- promoted market subpages,
- India TAM/economics ladders by partner.

### Step 5 — Build Adani and Reliance from the India spine

Reason: they need additional asset inventory discipline. Build them after the India route base is clean.

Output:

- Adani asset-to-corridor map,
- Reliance asset/platform-to-corridor map,
- partner-specific proposal drafts.

---

## Proposed file / PR structure

### Handoff artifacts

Under `handoff/partner-map-model/`:

- `partner-proposals-india-gcc-build-plan-2026-06-20.md`
- `india-shared-corridor-spine.json`
- `uae-gulf-shared-corridor-spine.json`
- `india-partner-use-case-matrix.json`
- `gcc-partner-use-case-matrix.json`
- `partner-proposal-build-status-india-gcc.md`

### Partner files

Under `partner-pitch/partners/`:

- `uber-india.json`
- `rapido-india.json`
- `ola-india.json`
- `reliance.json`
- `adani.json`
- `noon.json`
- `rakta.json`
- `bahrain-motc.json`

Naming can be adjusted to match existing repo conventions.

### Finance outputs

Under finance/recal or partner growth outputs:

- `agg-uber-india.json`
- `agg-rapido-india.json`
- `agg-ola-india.json`
- `agg-reliance.json`
- `agg-adani.json`
- `agg-noon.json`
- `agg-rakta.json`
- `agg-bahrain-motc.json`

Transparent Sheets should be created/updated in place once sheet IDs exist.

---

## Decisions now resolved

1. **India corridor baseline:** accepted baseline is **Mumbai**, **Kerala**, **Andaman Islands**, and **Goa**.
2. **India corridor additions allowed this pass:** evaluate **Gujarat port/coastal spine**, **Tamil Nadu/Chennai**, **Andhra Pradesh/Visakhapatnam**, **West Bengal/Kolkata-Haldia-Sundarbans edge**, and **Lakshadweep only if grounded/green-lit**. Additions must pass registry/ID/economics gates.
3. **Rapido economics:** inherit standard mobility-platform assumptions initially.
4. **Ola international scope:** focus on India. Public reporting says Ola exited UK, Australia, and New Zealand in 2024; no international markets should be promoted unless fresh active-operations evidence appears.
5. **Reliance wedge:** combined thesis, but lead with **Jio / consumer platform**.
6. **Adani wedge:** lead with **ports and coastal real estate**.
7. **Noon economics:** model like Careem: a super-app mobility service with full-journey GMV, not a distinct e-commerce-only economics model.
8. **Cross-border treatment:** assume all RAK/Bahrain/Gulf cross-border routes are **Quanta-LR roadmap** except **Manama ↔ KSA Eastern Province**, which can be commercial-now if range/ops checks support it.
9. **Authority/outreach handling:** omitted from this build plan; the plan should focus only on proposal construction, route/economics grounding, and render/export readiness.

---

## Immediate next action

Start with a repo-backed audit, not prose drafting:

1. Pull current Atlas repo.
2. Extract existing India corridors and UAE/Gulf corridors.
3. Produce the two shared spine JSON files.
4. Mark each route as reusable by each partner.
5. Identify additions/backlog separately.
6. Then build the partner JSONs and economics from those spines.

That keeps the proposals grounded, avoids duplicating corridors, and lets the eight partner decks share one clean route foundation.