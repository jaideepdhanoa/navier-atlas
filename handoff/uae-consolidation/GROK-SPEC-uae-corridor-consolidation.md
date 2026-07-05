# GROK SPEC — UAE corridor consolidation & partner unification

**Owner:** Tasklet (diagnosis + target) → Grok (deterministic geometry seal)
**Date:** 2026-07-05
**Trigger:** Jaideep — UAE BPs + routing are a spaghetti disaster; different routes per partner; remove dirty BPs, merge to only significant corridors, route cleanly with no land crossings.
**Companion:** `UAE-SPAGHETTI-DIAGNOSIS-AND-PLAN.md`, `UAE-DIAGNOSIS.json`.

## Goal
Reduce the UAE from **~666 rendered routes / 348 BPs** to **~35–45 significant, clean, in-range, no-land-crossing corridors** on **~60–80 real on-water BPs**, and render the **same** UAE network for every partner.

---
## Step 1 — Drop dirty BPs (deterministic signatures)
Quarantine/drop any UAE BP matching:
1. **Bare city centroids** used as endpoints: `Abu Dhabi`, `Fujairah`, `Ras Al Khaimah`, `Dubai`, `Sharjah` (label == city name; no berth).
2. **Activity operators / non-piers**: names containing `Jet Ski`, `Water Sports`, `Diving`, `DiveCampus`, `MSC`, `Boat ramp`, `Kingfisher Lodge`, dive/kayak/tour operators.
3. **Junk / untranslated placeholders** with no resolvable berth geometry.
4. **Planned/duplicate jetties** — collapse duplicates to one canonical node per landmark (e.g. the multiple Palm-resort jetties → keep the real transfer piers, merge the rest).
Null-beats-wrong: if a BP can't be resolved to a real on-water pier, drop it, don't guess.

## Step 2 — Kill all-pairs meshing; keep only significant corridors
Replace full-mesh with **hub-and-spoke + marquee OD pairs**. Delete: trivial sub-2 nm hops, redundant parallel edges, and any edge whose both endpoints are better served by a hub. Target named set below.

### Dubai (Gulf coast) — ~8 corridors
- Dubai Marina ↔ Palm Jumeirah (Atlantis / One&Only jetties)
- Dubai Marina ↔ Dubai Harbour (Bluewaters / Ain Dubai)
- Dubai Harbour ↔ Palm Jumeirah (Atlantis)
- Palm Jumeirah ↔ World Islands (Heart of Europe / Côte d'Azur Marina)
- Dubai Harbour ↔ World Islands
- Bulgari Yacht Club & Marina (Jumeirah Bay) ↔ Dubai Harbour
- Dubai Creek: Old Souq Marine Station (Deira/Bur Dubai) ↔ Dubai Festival City Marina *(creek routing)*
- Jumeirah Zabeel Saray Jetty (Palm) ↔ Dubai Marina

### Abu Dhabi — ~7 corridors
- Yas Marina ↔ Saadiyat Ferry Terminal
- Saadiyat ↔ Corniche (Emirates Palace Marina / Al Maryah CBD)
- Emirates Palace Marina ↔ Lulu Island
- Marina Mall / Breakwater ↔ Lulu Island
- Yas Marina ↔ Al Maryah / CBD
- Saadiyat ↔ Zaya Nurai Island
- Al Maryah ↔ Rabdan Marina
- **Sir Bani Yas / Desert Islands = SEPARATE far-west local sub-cluster** (~150 nm from AD city) near Jebel Dhanna — never connect to AD-city BPs.

### Sharjah + Ajman — ~3 corridors
- Al Majaz Waterfront ↔ Khalid Lagoon Marina (intra-lagoon)
- Sharjah (Khalid Lagoon) ↔ Ajman Marina / Corniche
- Ajman Marina ↔ Al Zorah Beach Resort
- *(Sharjah's Khorfakkan/Kalba enclaves are on the Gulf of Oman — move them to the East-Coast cluster.)*

### Ras Al Khaimah — ~3 corridors
- Al Marjan Island ↔ RAK Corniche
- Al Marjan (Wynn) ↔ Al Hamra / Mina Al Arab (Anantara)
- RAK Corniche ↔ Al Hamra

### East coast (Gulf of Oman) — SEPARATE cluster, ~5 corridors
Never mesh to the Gulf-side emirates (that's the mountain-crossing bug).
- Fujairah Marina (Corniche) ↔ Khorfakkan
- Khorfakkan ↔ Dibba
- Dibba ↔ Al Aqah resorts (Iberotel Miramar / Fairmont)
- Fujairah ↔ Kalba
- *(Cross-border marquee, keep 1: Dibba/Khorfakkan ↔ Zighy Bay / Khasab, Musandam Oman — coastal, in-range.)*

### Cross-border policy
Drop all UAE↔Qatar/Bahrain edges (over-range, quarantined). Keep at most the one east-coast UAE↔Oman Musandam coastal marquee.

## Step 3 — Route cleanly (zero land crossings)
- Apply the **788 existing pairs** in `data-clean/uae_hand_waypoints.json` at seal, and author waypoints for any surviving corridor still flagged.
- **Acceptance gate: 0 rendered UAE routes with `_qa_land_flag=true`.** Every Palm/island/creek corridor rounds the breakwater/land offshore.
- Enforce range: drop/keep-null any surviving corridor > 70 nm.

## Step 4 — Unify the partners (one shared UAE scope)
Root cause of per-partner divergence: routes are **not** partner-tagged; the front-end renders each partner's own `_map_scope`. Bolt, Yango, Noon, and Careem(mirror) each carry a different UAE scope.

**Action:** define ONE canonical UAE `_map_scope` block (identical `registry_keys` + `cluster_city_ids` + `inheritance_policy`, pointing at the consolidated corridor set) and write it identically into `careem.json`, `bolt.json`, `yango.json`, `noon.json`. Partner **narrative/economics stay partner-specific**; only the UAE geometry scope is unified. Tasklet will stage the shared `_map_scope` block; Grok confirms the registry_keys resolve post-reseal.

## Step 5 — Then Singapore
Apply the same de-mesh + land-QA-to-zero policy to Singapore (tighten its Batam/Johor land-cutters) as the second marquee. Separate follow-up spec.

## Guardrails
- ID-based matching only; null beats confidently-wrong; do not invent BPs, corridors, or coords.
- No live partner deck is edited by this work.
- East coast and Gulf coast are permanently separate clusters.
- Report back: new UAE route count, BP count, land-flag count (must be 0), and per-partner render parity (all four identical).
