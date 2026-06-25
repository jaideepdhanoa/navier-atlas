# Bolt — partner-proposal parity status (grounded re-audit)

**Date:** 2026-06-25
**Method:** full-structure parse of `partner-pitch/partners/bolt.json` (395 KB, 33 top-level keys) against the live render-join source `data-clean/FEATURES_BY_TYPE.json` (1,661 `city` + 37 `priority_city` features → 212 distinct render-join `city_id`s). No line-range slicing — the whole JSON is loaded and every referenced id is matched by exact `city_id`.
**Reference standard:** `partner-proposal-parity` skill, gates A–F.

## Verdict
**Bolt is broadly at parity — fix-list, not a restart.** Render parity and the economics ladder are solid. The real gaps are a stale roster/market-count, one underbuilt sub-page (`east-africa`), one distance/geocode bug, and a small, contained copy-lint carryover. All are surgical.

---

## Gate A — Market render parity → **PASS**
- 55 distinct city ids are referenced across `markets[].anchor_cities`, market & top-level `phases[].cities`, and `end_state_cities`. **55/55 resolve** to atlas render-join ids. **0 ID_MISMATCH, 0 MISSING_GEOMETRY.**
- All 42 journey `from_node_id`/`to_node_id`s also resolve.
- Note: the atlas now carries **country-suffixed** ids (`dubai-uae`, `abu-dhabi-uae`, `jeddah-ksa` are the real `city_id`s), so the historical `dubai-uae→dubai` class of mismatch is already resolved. Evidence: `BOLT-ANCHOR-CITY-CROSSWALK.json` (this PR).

## Gate A.1 — Roster / count reconciliation → **FLAG (fix)**
The market count is stated three different ways and the end-state roster is stale:
- `markets[]` array = **18** · `end_state.addressable_market_count` = **17** · `growth_case.addressable_market_count` = **22** · `network_thesis.stats` "Sub-proposals" = **22**.
- `end_state.end_state_cities` (28) does not reconcile with the 47 distinct market anchor ids: **8** cities are in `end_state_cities` with no market sub-page (`beirut-lebanon, constanta-romania, dubrovnik-croatia, eastern-province-ksa, limassol-cyprus, santorini-greece, sharm-el-sheikh-egypt, tel-aviv-israel`); **27** market anchor ids are absent from `end_state_cities`.
- **Action:** pick one canonical market count, refresh `end_state_cities` to match the live 18-market / 47-anchor roster (less explicitly-held markets), and align `addressable_market_count` + the slide-2 stat.

## Gate B — Economics / TAM ladder → **PASS**
- All nine `growth_case` fields present: `revenue_potential, journey_gmv, marine_mobility_tam, partner_platform_rev_on_navier, phase_economics, vessel_sizing, ladder_transitions, modal_headline, modal_lead`.
- Six-rung ladder intact (`som_floor → som_network → sam_network → tam_transfer → journey_gmv → platform_rev`) with `ladder_transitions` SHOW-MATH for every step.
- Provenance grounded: `greenfield_mode=census`, 35 sourced + 341 greenfield corridors, `rev_per_boat_yr=$266,202` — **not** the 30K placeholder. SOM floor $104M / SOM network $507M / SAM $2.20B.

## Gate C — Sub-page parity → **MOSTLY PASS (1 fix)**
- 17 of 18 markets are at full depth (14/14 core fields + `phases`).
- **`east-africa` is underbuilt: 7/14** — missing `proof_points, objections, the_ask, close, why_navier_now, partner_context, end_state`. It is the net-new market and needs to be brought to Grab parity or explicitly demoted to roll-up.
- 43 of 167 sub-page `featured_routes` are unbound (`route_id: null`). Allowed pre-seal, but the `east-africa` + newer minted legs need Grok seal-binding.

## Gate C.1 — Vessel range-gating → **FLAG (1 data bug, not a vessel error)**
- One leg trips the gate: `portugal` › **Lagos → Ponta da Piedade, 100.9 nm, "Pioneer II"** (>70 nm on a 70 nm hull).
- On inspection this is a **distance/geocode bug**, not a hull mistake: Lagos (Algarve) ↔ Ponta da Piedade is ~1 nm (Ponta da Piedade is the cliff formation at Lagos). The 100.9 nm reads like a Lagos-Nigeria coordinate mismatch. **Fix the distance (~1–2 nm); Pioneer II is correct.**
- Every other leg is correctly gated.

## Gate F — Copy lint (no internal taxonomy in partner-facing text) → **FLAG (small, contained)**
Genuine taxonomy leaks (product names Pioneer II / Quanta-LR are legitimate and excluded):
- **Sub-page prose (partner reads as narrative):**
  - `markets[france-riviera].phases[0].narrative` — "the **captive** Lérins island shuttle…"
  - `markets[8].phases[2].narrative` & `markets[11].phases[2].narrative` — "Mature into **induced demand**, … in-app **capture**."
- **Economics modal:** `revenue_potential.headline` ("every **rung** traces to **grounded**, sourced demand"), `ladder_transitions[4].headline` ("Bolt **platform take**…").
- Matches the known LB-256 carryover ("bolt/grab-thailand/minor-hotels still carry it"). **Action:** plain-English these few strings; keep SOM/SAM/TAM/GMV as labels-with-descriptors per house rule.

---

## Fix list (surgical — hand to Grok build for the seal/cascade items)
1. Reconcile market count + refresh `end_state_cities` (Gate A.1).
2. Bring `east-africa` sub-page to parity or demote to roll-up; bind its `featured_routes` (Gate C).
3. Correct the Lagos→Ponta da Piedade distance (~1 nm) (Gate C.1).
4. Plain-English the ~5 taxonomy strings (Gate F).

No render-join breakage, no missing geometry, no placeholder economics — so **no full rebuild is warranted.**
