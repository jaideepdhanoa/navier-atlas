# Grok prompt — Bolt/Yango new-market seal + corrected economics (deterministic, Grok-owned)

## Context
Source of truth: GitHub `navier-atlas` `main` (zip hand-back retired). Tasklet has landed, in the
finance world only, a large expansion: new countries, clusters, cities, boarding points, and
shared-network economic corridors for **Bolt** and **Yango**, plus a corrected economics base
(greenfield template band, per-country opex, region-keyed CAPEX). The **atlas front-end surface is
stale** and must be resealed. Target reseal: **#<NEXT-TAG>**.

Inputs (in `grok-bolt-yango-seal.zip`, posted to `#tasklet-jaideep`):
- New/edited `boarding-points/*.json` (Greece, Croatia, Spain/Ibiza/Mallorca, Portugal/Lisbon,
  Senegal/Dakar, Kenya, Tanzania, Mozambique, Nigeria, …).
- `SEAL-MANIFEST.json` — new cities, cluster tags, **country tags**, and corridors to fold into the
  **shared global corridor network** (must inherit correct country tags + overlap across partners).
- `route_water_allowlist.json` (LB-242) — fold into the routing/mask lane.
- `econ-sidecar-bolt.json`, `econ-sidecar-yango.json` — corrected rung ladder + published Sheet URL.

## ⚑ Coverage mandate — INCLUDE ALL BOARDING POINTS (hours of research at stake)
Current sealed surface drops **786 BPs** vs. what's on disk (`atlas-external/boarding-points/*.json`).
Audit: `atlas-external/BP-COVERAGE-GAP-2026-06-19.json`. Acceptance is that every researched BP is
either **sealed as a POI marker** or **listed in a drop-ledger with an explicit reason** (junk-POI
repoint, failed water-adjacency, unresolved coords). Silent drops are not allowed.
- **A) 35 cities with ZERO sealed POIs (148 BPs)** — fold in fully. Worst: `sabah-kk` (61),
  `lisbon-tagus-portugal` (10), `abidjan-cote-divoire` (5), `dammam-khobar-ksa`, `shanghai-china`,
  `neom-ksa`, `amaala-ksa`, `dakar-senegal`, `baku-azerbaijan`, `beirut-lebanon`, plus Cyprus,
  Egypt (El Gouna/Hurghada), Kazakhstan, Tangier, Tel Aviv, Tunis, Maputo, Karachi, etc.
- **A-bis) routed-but-no-markers** — `mombasa-kenya`, `lamu-kenya`, `belize-city-cayes-belize`,
  `ambergris-caye-belize`, `placencia-belize`, Galápagos (`santa-cruz`/`isabela`/`san-cristobal`):
  routes exist but **0 BP markers sealed** — seal the markers so they aren't ghost endpoints.
- **B) 56 partially-sealed cities (489 BP gap)** — reconcile each; keep real BPs, ledger the drops.

## What to do (deterministic; null > confidently-wrong; exactness over coverage)

### 1. Ingest + ID-match the new boarding points
- Add the new BPs. **Promote only** BPs with a real gazetteer/source id (ferry/water-bus terminals,
  licensed marina berths, OSM `amenity=ferry_terminal` / `leisure=marina` / harbour nodes). No
  name-only promotions. Inland/junk POIs die regardless of name — **but record each drop in the ledger.**
- Reconcile against `BP-COVERAGE-GAP-2026-06-19.json`: target 0 silent drops.

### 2. Build the graph for the new markets (geometry-first)
- Real boarding-point endpoints only — **no raw-label endpoints**; bidirectional ↔ corridors.
- Enrich the **existing** registry corridors where they already exist; do not recreate shared routes.
- Every featured / inter-city route must **render real water-following geometry or be visibly aspirational**.
- Turkey beyond Istanbul must include **Bodrum** and other coastal/Aegean-Med markets.

### 3. Water + land gates (hard, block reseal on failure)
- Apply the water allowlist; **0 route polylines crossing land** after allowlist.
- Water-adjacency disqualifies inland BPs.

### 4. Cascade + de-spaghetti
- Drop orph
### 6. Sub-proposals: full per-market pages with range-gated phases (Grab/Uber parity)
- Each Bolt/Yango market is a **full sub-proposal**, not a roll-up stub — the Grab (13) / Uber (17) pattern.
  Careem is hub-only ONLY because it is a single-country play; multi-market partners cannot be hub-only.
- `subproposals/SCAFFOLD-ALL.json` supplies, per market: `journeys_unlocked` + `phases` (Prove→Scale→Mature),
  each phase with **range-gated vessel sizing** (≤70nm Pioneer II / 75–150nm Quanta-LR / >150nm flagged),
  grounded per-phase boats, and `featured_routes` referencing **real `*_node_id`s** with `route_id: null`.
- **Bind during seal:** set each featured route's `route_id` to the sealed route, set `model_link` to the
  partner economics Sheet, and **reconcile per-phase boat counts to `phase_economics`** (model is source of truth).
- `subproposals/AUTHORED-batch1-*.json` = complete narrative for Bolt Spain/Egypt/Sweden — splice as-is.
  Remaining markets' narrative follows from Tasklet in batches; splice each as it lands.
- `subproposals/VESSEL-REGATE-LEDGER.json` lists 27 corridors whose hull was corrected — apply the corrected vessels.

### 6b. Sub-proposals — COMPLETE SET (supersedes §6 batch-1 note)
All 33 sub-proposals are now authored and QA-clean in `subproposals/AUTHORED-ALL-33-markets.json`
(18 Bolt + 15 Yango) plus the Yango hub in `subproposals/AUTHORED-yango-hub.json`. For EACH market:
- Splice the full sub-page (`hero, why_now, why_navier_now, journeys_unlocked, proof_points, objections,
  phases, the_ask, close, summary, end_state`) into `partners/{partner}.json` markets[].
- **Bind `route_id` + `model_link`** in every `phases[].featured_routes[]` — these are null in the authored
  files BY DESIGN (null beats confidently-wrong). ID-match `from_node_id`/`to_node_id` to sealed corridors.
- **Reconcile per-phase `boats`** against the model output (aggregate.py → growth.py); the authored counts
  are grounded estimates from the $513K/boat rule — replace with model truth where they differ.
- **Bind the Yango hub growth_case** (revenue_potential / phase_economics / vessel_sizing / ladder_transitions /
  modal_headline) from the Yango model + economics_url. Do NOT borrow another partner's census (LB-250).
- **Held markets** (`bolt-israel`, `bolt-lebanon`, `yango-israel`): keep DATA-ONLY/held framing; do not wire
  active outreach CTAs. They carry parity for network integrity (shared corridors).
- **Turkey/Bodrum + Aegean-Med:** narrative flags these as committed expansion but corridors need minting —
  render aspirational until your geometry lane enriches them. Do not fake placeholder geometry.
