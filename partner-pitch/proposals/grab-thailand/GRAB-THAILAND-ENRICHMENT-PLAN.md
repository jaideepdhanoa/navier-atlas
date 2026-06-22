# Grab × Navier — Thailand Enrichment Plan
**Trigger:** Dominic Ong (Grab) pinged the Grab **Thailand team**; called out **Phuket, Koh Samui, and Bangkok** as strong fits. Jaideep in **Bangkok end-of-week / early next**, can reach Phuket/Samui.
**Goal:** Turn a Singapore-anchored Grab pitch into a **Thailand-forward** pitch with **two flagship Thai sub-proposals (Phuket/Andaman + Koh Samui/Gulf)**, a strengthened **Bangkok** gateway, and the connected-city briefs that make them credible — all at Grab/Careem parity.

---

## 0. Where we actually stand (grounded, not assumed — verified against the live model)
- **Grab partner JSON has 6 markets:** `singapore, cross-border, bali, phuket, philippines, vietnam`. Only **`phuket`** touches Thailand — and it bundles `phuket-phang-nga-thailand + langkawi-malaysia + penang-malaysia` (half Malaysian).
- **Koh Samui** and **Bangkok** = **city briefs only, no sub-proposal** in the partner JSON. Samui's brief is our richest Thai brief (7.5 KB); Bangkok's is the thinnest.
- **GOOD NEWS — sealed corridor geometry already exists** in `finance/model/corridors.json` for all three:
  - **`koh-samui` — 7 sealed corridors** (Samui↔Phangan 10.2nm, Samui↔Koh Tao 35.3nm, Donsak ferry crossings, Four Seasons↔Ang Thong Marine Park). Flagship-ready.
  - **`phuket` — 8 sealed corridors** (Phang Nga/James Bond 20nm, Krabi/Ao Nang 40nm, Phi Phi 25nm, Similan 55nm Quanta-LR, Langkawi 107nm Quanta-LR cross-border). Andaman cluster already bound.
  - **`bangkok` — only 2 corridors** (intra-river Chao Phraya: ICONSIAM 5.3nm, Sathorn↔Phra Arthit 2.9nm). **This is the real geometry gap** — no gulf gateway.
- **Genuinely missing geometry (need mint):** **Pattaya = 0, Koh Chang = 0, Hua Hin = 0.** Krabi/Phi Phi/Koh Tao present but thin.
- **The opportunity:** Samui + Phuket/Andaman can be bound to *real* sealed geometry today; only Bangkok's gulf gateway and the eastern-gulf islands need minting.

---

## 1. The Thailand narrative (lead the meeting with this)
Three clusters, one country story — **"the water layer for Thailand's two coasts + its river megacity."**
1. **Andaman / Phuket** — resort + island-hop premium (Phuket ↔ Phang Nga ↔ Krabi ↔ Phi Phi), cross-border reach to Langkawi/Penang.
2. **Gulf / Koh Samui** — the flagship island cluster (Samui ↔ Koh Phangan ↔ Koh Tao), today reached by slow ferry/air; Quanta-LR opens single-leg gulf runs.
3. **Bangkok** — Chao Phraya premium river tier (congestion relief, demand already in-app) + the gulf gateway to Pattaya/Koh Chang/Samui.
**Framing for Grab:** lead with **autonomy-ready** (Dominic's AV lens), **super-app water tier** (demand already in-app), **congestion + island connectivity**. Thailand-first, region-next.

---

## 1b. Standalone Grab Thailand proposal (NEW — mirrors Uber India)
Build a dedicated **`grab-thailand-derivative.json`** partner, exactly patterned on **`uber-india-derivative.json`**: a standalone hub-layout proposal whose `markets[]` array *is* the set of Thai sub-proposals. This gives the TH team a single, self-contained Thailand pitch — not a Thai slice buried inside a SEA-wide Grab deck.
- **Pattern source (verified):** `uber-india-derivative.json` = `partner_id` + `display` + `archetype/category/region/layout:"hub"` + `coverage_note` + `hero/why_now/network_thesis/why_navier_now` + **`markets[]`** (each a full sub-proposal: hero, partner_context, why_now, why_navier_now, journeys_unlocked, proof_points, objections, phases, the_ask, end_state, close, vessel sizing) + `phases` + `economics_status` + `growth_case` + `_provenance` + a `*_seal` block. It has **6 India markets**; ours gets the Thai markets.
- **Reuse:** the `growth_case` TAM template already references **Grab's commission / super-app journey_gmv** (it was authored *from* the Grab model) → economics inherit cleanly.
- **Derivative markets (initial):** `phuket_andaman` (flagship), `koh_samui_gulf` (flagship), `bangkok` (river + gulf gateway). Expansion-ready for the gulf/Andaman connected cities.
- **Scaffold:** reuse `partner-pitch/subproposals/build_scaffold.py` (deterministic phases + range-gated vessel sizing off real corridors; prose left empty for Tasklet to author).
- **Crosswalk + seal:** ship `GRAB-THAILAND-DERIVATIVE-ANCHOR-CITY-CROSSWALK.json` (ID-match only) → Grok mints missing geometry + binds route_ids → reseal.

---

## 2. Workstreams (mapped to the parity gates A–E)

### WS1 — City briefs: enrich + extend *(Tasklet, research)*
- **Enrich Bangkok** (thinnest): add Chao Phraya pier-level journey legs, Pattaya/Koh Chang gulf corridors, ridership/congestion sources, regulatory (Marine Dept / BMA clean-river agenda), fare/demand signals.
- **Deepen Koh Samui**: lock the Samui↔Phangan↔Tao triangle + Samui↔mainland (Donsak/Surat) + Samui↔Bangkok long-haul.
- **New connected-city briefs (cover/connect to the anchors):**
  - **Gulf cluster:** Koh Phangan, Koh Tao, Pattaya, Koh Chang *(+ optional Hua Hin/Cha-am)*
  - **Andaman cluster:** Krabi, Phi Phi, Phang Nga *(deepens the existing Phuket market)*
  - **Keep:** Langkawi, Penang (cross-border, already in the phuket market)
- Every brief: source-backed demand signals, journeys (from/to/today/with_navier/distance_nm/platform), `partner_overlays.grab`, seasonality, regulatory, precedents.

### WS2 — Sub-proposal build to Grab parity *(Tasklet spec → Grok seal)*
- **Promote Koh Samui → full market sub-page** (~22–25 fields: hero, summary, why_now, multimodal_fit, journeys_unlocked, proof_points, objections, **phases**, the_ask, close, why_navier_now, partner_context, end_state, **vessel_sizing**).
- **Add Bangkok → full market sub-page** (river tier + gulf gateway).
- **Re-cut the "phuket" market into a Thailand-clean "Phuket / Andaman"** sub-proposal; move Langkawi/Penang into the existing `cross-border` logic so the Thai story reads clean. (Decision point — see §5.)
- Result: **two flagship Thai sub-proposals + Bangkok** = the "two compelling sub-proposals to go through" the meeting needs, with room to expand.

### WS3 — Render readiness / Gate A *(Tasklet crosswalk → Grok mint)*
- Build **`grab-thailand-anchor-city-crosswalk.json`**: verify each anchor id resolves to an atlas `city_id` (ID-match only; null beats wrong).
- Flag `MISSING_GEOMETRY`: Krabi, Phi Phi, Pattaya, Koh Chang, Koh Larn (+ thin Koh Phangan/Koh Tao) → Grok geometry lane mints BPs + corridors; **route_ids null until Grok binds.**
- Reconcile rosters: geometry chips == market sub-pages == roll_up — no map dot without a sub-page.

### WS4 — Economics / TAM / Gate B *(Tasklet demand anchors → Grok cascade)*
- **Thailand `model/country-reference.json` row** — critical: no silent Singapore opex (LB-243). Thai crew/marina/energy/CAPEX ($600K non-US/EU).
- **Demand anchors** (`*-DEMAND-ANCHORS-*.json`) for Phuket, Samui, Bangkok off sourced tourism/ferry/ridership data — never the 30K placeholder.
- Run `aggregate.py → growth.py` over the expanded Thai footprint; refresh `growth_case` (revenue_potential, journey_gmv, marine_mobility_tam, partner_platform_rev, phase_economics, **ladder_transitions**).

### WS5 — Vessel sizing / range gating / Gate C.1 *(Tasklet spec → Grok regate)*
- Range-gate every Thai leg: **≤70nm → N30 Pioneer II; 75–150nm → Quanta-LR; >150nm → Quanta-LR (review).**
- Bangkok↔Samui (~205nm) and gulf island long-legs = **Quanta-LR, render amber-dashed** — never a 70nm boat on a long leg.

### WS6 — Cascade + deck / Gate D *(Grok deterministic; Tasklet QA)*
- Transparent Grab sheet updated **in place** (preserve URL); economics **sidecar** rebuilt; master tracker row refreshed.
- Live Grab deck via Slides API: add/refresh **slide 3 KPI**, market slides for Samui + Bangkok, **slide 10 TAM**, **6-line flush-left OPEX**. No PPTX round-trip; reuse approved image assets; no Atlas-generated images.

### WS7 — Meeting collateral *(Tasklet draft → human review, FAST track)*
- **One-page Thailand brief** for the Grab TH team: the three clusters, signature routes, the autonomy + super-app framing, "what a low-friction pilot looks like." No full deck unless asked.
- Talking-points card for Jaideep (Phuket / Samui / Bangkok, 3 lines each).
- Any email/intro text stays a **draft for review**; c