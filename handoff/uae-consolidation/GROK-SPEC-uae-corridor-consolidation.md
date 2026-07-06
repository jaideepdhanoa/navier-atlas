# GROK SPEC — UAE corridor consolidation & partner unification

**Owner:** Tasklet (diagnosis + target) → Grok (deterministic geometry seal)
**Date:** 2026-07-05
**Trigger:** Jaideep — UAE BPs + routing are a spaghetti disaster; different routes per partner; remove dirty BPs, merge to only significant corridors, route cleanly with no land crossings.
**Companion:** `UAE-SPAGHETTI-DIAGNOSIS-AND-PLAN.md`, `UAE-DIAGNOSIS.json`.

## Goal
Rebuild the **global** UAE view (the master `ROUTES.json` network, not just partner scopes) into a set of corridors where **every corridor is significant, unique (no duplicates/parallels), in-range, and has zero land crossings**. The UAE is a fantastic marine-mobility playground — **there is NO cap of ~45**. Keep **as many corridors as the real geography genuinely supports** (comfortably more than 45), provided each one clears the significance + dedupe + no-land-crossing bar. We are removing spaghetti and dirty BPs, **not** thinning a good network.

Then: the global set is the single source of truth, and **every partner inherits it by cluster/city membership** (see `CORRIDOR-INHERITANCE-CONTRACT.md`) — so the global view and all four partner views are identical for any shared cluster.

Quantitatively: from **~666 rendered / 348 BPs** with 202 land-crossers → a de-duped, land-clean set on **~60–90 real on-water BPs**, corridor count set by geography (significant OD pairs + sensible hub-and-spoke), **0 land flags**.

---
## Step 1 — Drop dirty BPs (deterministic signatures)
Quarantine/drop any UAE BP matching:
1. **Bare city centroids** used as endpoints: `Abu Dhabi`, `Fujairah`, `Ras Al Khaimah`, `Dubai`, `Sharjah` (label == city name; no berth).
2. **Activity operators / non-piers**: names containing `Jet Ski`, `Water Sports`, `Diving`, `DiveCampus`, `MSC`, `Boat ramp`, `Kingfisher Lodge`, dive/kayak/tour operators.
3. **Junk / untranslated placeholders** with no resolvable berth geometry.
4. **Planned/duplicate jetties** — collapse duplicates to one canonical node per landmark (e.g. the multiple Palm-resort jetties → keep the real transfer piers, merge the rest).
Null-beats-wrong: if a BP can't be resolved to a real on-water pier, drop it, don't guess.

## Step 2 — Kill all-pairs meshing; keep every significant corridor (no cap)
Replace full-mesh with **hub-and-spoke + marquee OD pairs**. The enemy is not corridor *count* — it is **duplicates, trivial sub-2 nm hops, redundant parallel edges, and land-crossers**. Delete those. **Keep every corridor that is a genuine, distinct, on-water OD pair**, even if that yields well over 45. The named lists below are the **significance floor / seed, not a ceiling** — add any further real, distinct, in-range, on-water OD pair Grok can source (more resort-island, marina-to-marina, and cross-bay links are welcome as long as they're not duplicates or land-crossers).

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

## Step 4 — Unify via inheritance, not curation (see `CORRIDOR-INHERITANCE-CONTRACT.md`)
Root cause of per-partner divergence: a corridor is treated as a **partner** property — each partner hand-curates its own `_map_scope` subset, so four partners drifted into four UAE maps. Fix the model, not just the data:

1. The **consolidated global corridor set is the single source of truth**; each corridor is stamped with `cluster_id`.
2. **Delete** the four per-partner UAE corridor curations.
3. Each partner's UAE `_map_scope` becomes a **cluster/city membership list + `"inheritance_policy": "inherit_all_cluster_corridors"`** — **no corridor arrays in partner files**.
4. Renderer derives `partner_corridors = global_canonical ∩ partner.clusters`, so every partner in a cluster shows the **identical** corridors (and identical to the global view). Partner **narrative/economics stay partner-specific**; only geometry is inherited.
5. **New seal gate `validate_partner_inheritance.py`:** FAIL if any partner enumerates a corridor not derivable from its clusters, or omits one that is. This is what prevents a future 4-scope split — apply it across **all** partners/markets, not just UAE.

Tasklet stages the membership `_map_scope` blocks post-reseal; Grok wires the derivation + parity gate.

## Step 5 — Then Singapore + roll the gate globally
Apply the same de-mesh + land-QA-to-zero policy to Singapore (tighten its Batam/Johor land-cutters) as the second marquee. Then run `validate_partner_inheritance.py` across **every** partner/market so no other geography can develop a UAE-style 4-scope split. Separate follow-up spec for Singapore.

## Guardrails
- ID-based matching only; null beats confidently-wrong; do not invent BPs, corridors, or coords.
- **No corridor cap** — keep every significant, distinct, in-range, on-water OD pair; only kill duplicates, trivial hops, and land-crossers.
- Every surviving corridor is stamped with `cluster_id` so inheritance can derive partner views.
- No live partner deck is edited by this work.
- East coast (Gulf of Oman) and Gulf coast are permanently separate clusters.
- Report back: new **global** UAE corridor count, BP count, land-flag count (**must be 0**), and inheritance parity — global view == each partner's derived view for every shared cluster.
