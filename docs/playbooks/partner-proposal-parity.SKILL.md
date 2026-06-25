---
name: partner-proposal-parity
description: Definition-of-done for a Navier partner proposal to reach Grab/Careem completeness. Use when building, auditing, or fixing any partner proposal (Bolt, Yango, etc.). Covers the anchor-city ID-match render check and full growth_case/TAM economics.
---

# Partner Proposal Parity — the Grab/Careem standard

Use this before declaring any partner proposal "done." Grab and Careem are the reference implementations. A new partner (Bolt, Yango, …) is **only at par** when it passes every gate below. This skill exists because Bolt/Yango shipped the map half but not the economics half, and several marquee markets rendered nothing due to an ID mismatch — a discovery that cost real time. Do not rediscover it.

## The two failure modes that look like "incomplete"
1. **Render gap (map looks empty / only a handful of markets):** usually an **anchor-city ID mismatch**, not missing data. The microsite joins `markets[].anchor_cities` ids to the sealed atlas `city_id` (the render join key is the internal `city_id`, NOT the filename). A country-suffixed id like `dubai-uae` will not resolve to atlas `dubai` and renders nothing even though geometry is fully minted. Real-world hits: `dubai-uae→dubai`, `abu-dhabi-uae→abu-dhabi`, `doha-qatar→doha`, `bodrum-turkey→bodrum`.
2. **Economics gap (TAM tiny or missing):** the finance chain never ran over the full footprint, so there is no `*-aggregate.json` and the `growth_case` block is partial or absent.

## Gate A — Market render parity (check FIRST; cheapest, highest impact)
For every market in `partners/{partner}.json`:
- [ ] Each `anchor_cities` id resolves to an existing atlas `city_id`. Verify by reading the internal `city_id` of the boarding-point file, not the filename.
- [ ] Build/refresh an **anchor-city crosswalk** (`{partner}-ANCHOR-CITY-CROSSWALK.json`) with verdicts: `OK` / `ID_MISMATCH` (geometry exists, rename the id) / `MISSING_GEOMETRY` (mint it).
- [ ] All `ID_MISMATCH` entries renamed (Grok) and re-rendered. Trivial fix, do before economics.
- [ ] All `MISSING_GEOMETRY` entries either minted (Grok geometry lane) or explicitly demoted to Tier-B roll-up / held.
- [ ] The three market rosters reconcile: **geometry chips == `.markets` sub-pages == `roll_up_markets`** (minus explicitly-held markets). No market on the map without a sub-page; no sub-page referencing an unminted market.

## Gate B — Economics / TAM ladder parity
- [ ] `finance/{partner}-aggregate.json` exists and aggregates **all in-scope markets** (not a single market). Compare size/shape to `grab-aggregate-results.json` and `careem-aggregate.json`.
- [ ] `partners/{partner}.json` has a **complete `growth_case`** matching Grab's shape:
  - `revenue_potential` (SOM floor / full / SAM)
  - `journey_gmv` (journey-GMV TAM rung)
  - `marine_mobility_tam` (marine TAM rung)
  - `partner_platform_rev_on_navier`
  - `phase_economics`
  - `vessel_sizing`
  - `ladder_transitions` (the inter-rung "SHOW MATH" explanations) — **this is what makes the TAM legible; never skip it**
  - `modal_headline` / `modal_lead` (narrative headers)
  - provenance / source fields
- [ ] TAM is anchored on **sourced demand**, never the uniform `30,000/yr` placeholder (which rounds to ~0 boats / $0 at default capture). Anchor + Tier-A + Tier-B should have real `*-DEMAND-ANCHORS-*.json`.
- [ ] Magnitudes sanity-check against footprint (no trivial SOM floor under a large route network).
- [ ] **Captive markets: TAM-ladder capture = floor capture, NOT 10% (LB-254).** For captive/luxury partners
  (Maldives/JIH, Red Sea, French Polynesia, resort transfers) the floor is built at ~90% capture, so the ladder must
  anchor `M_today` on the true `transport_spend_pool_yr` (= floor/`effective_capture`), never `floor/0.10` — the
  latter inflates every rung ~9×. **Sanity gate:** a captive market whose journey-GMV TAM exceeds its country's whole
  tourism economy is the tell (JIH read $23B vs ~$5–6B). The SOM floor itself never changes. Full rule + engine
  details in `partner-model-cascade` golden rule #11.
- [ ] **Greenfield labelled honestly (LB-250):** if greenfield is in the headline, it's either the partner's *own* census or the **global template band labelled as a template assumption** — never a peer's census file borrowed silently. A new partner that matches a reference partner's TAM almost exactly is a red flag for a borrowed census; confirm it's the labelled template band and say so. The grounded SOM floor (greenfield-independent) is the invariant to check against.
- [ ] **No silent Singapore opex (LB-243):** every country in the partner's footprint has a `model/country-reference.json` row. Missing countries silently inherit Singapore costs in *both* `aggregate.py` and the transparent sheet. Run the §B.0 preflight in the partner-model-cascade skill.
- [ ] **CAPEX region rule applied (LB-243):** US + EU = $900K/vessel, everywhere else = $600K, keyed by country and rendered as a per-country column on the sheet (not one global cell).

## Gate C — Sub-page parity (this is where "incomplete" hides)
**A hub partner page is NOT the deliverable — Grab (13) and Uber (17) carry a full per-market sub-proposal beyond the hub.** Parity means *every in-scope market is its own complete pitch*, not a dot on the map.
- [ ] Every in-scope market has a sub-page at Grab parity: `anchor_cities, hero, summary, why_now, multimodal_fit, journeys_unlocked, proof_points, objections, phases, the_ask, close, why_navier_now, partner_context, end_state` populated (≈22–25 fields/market — compare to a live Grab/Uber market).
- [ ] **`roll_up_markets` stubs are NOT parity.** A market with only `{id,label,region,one_liner,status}` is a stub, not a sub-proposal. The three rosters must reconcile (Gate A), but reconciling ≠ done: a market that has economics + corridors must be **promoted from roll-up to a full sub-page**, not left as a stub. (LB-251: Bolt shipped 8 full sub-pages + 10 roll-up stubs while the model already covered all 18 — the stubs were mistaken for parity.)
- [ ] **Every sub-page has `phases`** (Prove → Scale → Mature), each phase with: `n, label, boats, cities, route_scope, narrative, timeline, rationale, featured_routes[], use_cases[], fleet_confidence`. `featured_routes` reference **real `*_node_id`s**; `route_id` is bound by Grok during the seal (null until bound — never fabricate a route_id). `model_link` on each featured route = the partner economics Sheet URL (the `economics_url` binding).
- [ ] **Hub-only is valid for single-country opportunities** (e.g., Careem = hub-only because it is a single-country play). A multi-market partner (Bolt, Yango, Grab, Uber) is *not* allowed to be hub-only.

## Gate C.1 — Vessel sizing per phase (Grab methodology, range-gated)
- [ ] **Every corridor is range-gated by hull**, no exceptions: **≤ 70nm → N30 Pioneer II** (commercial now; N35 Shuttle adds throughput on dense legs in the Scale phase); **75–150nm → Quanta-LR** (roadmap, render `amber-dashed`); **> 150nm → Quanta-LR flagged for review**, never a 70nm boat. "Long legs never faked on a 70nm boat."
- [ ] **Re-gate the corridor registry before phasing** — `corridors.json` `vessel` fields drift (long legs mislabelled `Pioneer II`, casing like `pioneer-ii`/`quanta-lr`). Run the scaffold generator (`partner-pitch/subproposals/build_scaffold.py`) which re-gates every leg and emits a `VESSEL-REGATE-LEDGER`. (LB-252: 27 legs across Bolt/Yango were mis-vesselled, e.g. Palma↔Ibiza 75nm and Spain Balearic legs tagged Pioneer.)
- [ ] **Per-phase fleet sizing is grounded**, not invented: scale boats from the model's `phase_economics` grounding rule (e.g. *3 boats = $2M transport rev = 546 t CO₂/yr ≈ $513K rev/boat*), tier-weighted; mark `fleet_confidence` (`grounded`/`med`/`roadmap`); final counts reconcile to `aggregate.py`/`phase_economics` (model is source of truth).
- [ ] **`vessel_sizing` block present on each sub-page** (the three hull classes + `range_gate_note`), identical methodology to Grab.

## Gate D — Cascade & provenance
- [ ] Transparent partner sheet updated **in place** (don't create new sheets, use `fileIdToReplace` to preserve the URL); economics sidecar built into the gold zip; master tracker row refreshed. Numbers cascade end-to-end.
- [ ] **Model and sheet agree.** The deck/partner-JSON numbers (from `aggregate.py`/`growth.py`) and the standalone transparent sheet (`build_transparent_sheet.py`) are computed independently and each has its own override maps. Confirm they tell the same greenfield/opex/CAPEX story — a contradiction ships a deck that disagrees with its own backing sheet. See the partner-model-cascade skill for the full mechanics.
- [ ] Re-sealed and committed/tagged to the GitHub source of truth (`jaideepdhanoa/navier-atlas`); no zip hand-back.

## Gate E — Partner-specific framing
- [ ] Sovereign/sanctions framing applied where needed (e.g., **Yango = the Dubai-HQ'd Yango**; lead with the Dubai-HQ split). Held markets (sovereign coordination) flagged, not silently dropped.

## Gate F — Slide-2 exec-summary / narrative readiness (so the deck is more than numbers)
The deck's **slide 2** is an exec-summary/thesis distilled from the proposal by `gen_deck_narrative.py`
and painted via `narrative-binding.json` (one-time gold-created slide; see `deck-studio/docs/SPEC-narrative-binding.md`).
The slide can only render if the proposal carries its **five source fields** — otherwise it renders partial/null.
This gate exists because the slide-2 layer shipped while ~5 deck-eligible proposals silently lacked a field
(LB-255). **Do not rediscover it.**
- [ ] For every **deck-eligible** partner (archetypes `ridehail`, `super_app`, `corporate` — i.e. the consumer
  partner decks that carry the exec-summary slide), all five fields are present and non-empty:
  `partner_context`, `hero`, `why_now`, `network_thesis`, `proof_points`.
- [ ] **Authority/transit (`public_transit`, `sovereign`) and captive `hospitality` cover-cases are exempt** —
  they do not carry the consumer exec-summary slide. Null beats confidently-wrong; do not back-fill a
  `network_thesis` onto an authority proposal just to clear the gate.
- [ ] `network_thesis` matches the reference shape: `headline`, `body`, and a `stats[]` array of
  `{label, value, sub}` (these become the slide-2 proof chips). `proof_points` is the `{claim, evidence}[]`
  array (sourced — feeds the proof strip; numbers must trace to evidence or they FLAG at render).
- [ ] **Run the guard:** `python3 scripts/validate_partner_proposals.py --strict-narrative`. It reports
  deck-eligible readiness and **exits non-zero** if any deck-eligible partner is missing a field. Wire this
  into the proposal-prep preflight so the gap is caught at authoring time, not at deck-build time.
- [ ] After adding the fields, regenerate: `gen_deck_narrative.py <partner>` → `gen_narrative_binding.py <partner>`,
  then paint via the per-deck `deleteText`+`insertText` ops (style-preserving), exactly like economics.
- [ ] **No internal taxonomy in ANY rendered slide text (not just slide 2).** Titles, subtitles, eyebrows,
  KPI/ladder captions and route descriptors must be plain partner-facing English — never SOM/SAM/TAM/GMV,
  "captive resort mesh", "grounded", "network width", "amber-dashed", "scale vision", "N% capture", vessel
  codenames, "on these lanes". Builders must map model labels → display captions; do not f-string a finance
  `meaning`/`kpi_frame` onto a slide. **Run the gate:** `python3 deck-studio/qa/partner_copy_lint.py <deck>`
  must be green before seal/apply. Full rule: `deck-studio/docs/PARTNER-COPY-RULES.md`. (LB-256: OW shipped
  "captive resort mesh (grounded)" / "ABC scale vision (roadmap)" / "SOM floor ~46% capture" titles that
  survived several reviews because nothing linted the words a partner reads; bolt/grab-thailand/minor-hotels still carry it.)

> Forward queue at time of writing (deck-eligible, one field each): `cabify`, `freenow`,
> `uber-india-derivative` need `proof_points`; `careem`, `noon` need `network_thesis`. Author each from the
> partner's **own** existing proposal prose (distillation, not invention) before declaring its deck slide-2 ready.

## Tasklet / Grok split (keep Tasklet on research)
- **Tasklet:** anchor-city crosswalk + ID-matching, roster reconciliation, demand-anchor sourcing, build spec, parity QA, the share. No code/seal/render.
- **Grok CI (deterministic):** id renames, geometry mint, `aggregate.py → growth.py → splice_growth_into_partner.py`, sub-page build, sheet/sidecar/master, reseal, commit.

## Completeness language gate
Do not call a partner proposal, market, country, or package **complete**, **ready**, **done**, or **at parity** unless every Tasklet-owned upstream artifact and every downstream seal/cascade artifact required by Gates A–E is actually present and validated.

Use precise status labels instead:
- **research-needed** — Tasklet has not finished source-backed country/city/BP/demand/fare evidence.
- **research-complete / seal-needed** — Tasklet has finished source-backed city/BP/demand/fare evidence; Grok still needs deterministic route geometry, route IDs, and render QA.
- **seal-complete / cascade-needed** — route geometry/IDs/render QA are sealed; Tasklet still needs country-reference/model/growth/sheet/sidecar cascade.
- **proposal-complete** — Gates A–E all pass, data-clean exists, economics sidecar exists, render receipt exists, and the delivery links/posts are done.

A handoff checklist is not a completion receipt. If a required file is absent, say **held** or **missing**, name the file, and state the owner/next action. Never let a partial geography packet sound finished because deck scaffolding or a prompt exists.

## Definition of done
All gates A–E pass; both maps render every in-scope market; the TAM ladder renders with explanations for every partner (including the previously-dark ones); `data-clean/partners/{partner}.json`, economics sidecar, and render/QA receipt exist; links posted to `#tasklet-jaideep`; external outreach left as drafts.

## References
- `partner-pitch/BOLT-YANGO-PARITY-FIX-PLAN-2026-06-18.md` — worked example of this skill end to end.
- `partner-pitch/BOLT-YANGO-ANCHOR-CITY-CROSSWALK.json` — crosswalk example.
- `partner-pitch/PARTNER-DECK-CREATION-PLAYBOOK.md`, `PARTNER-RECAL-PLAYBOOK.md` — adjacent deck/recal playbooks.
- `finance/TAM-METHODOLOGY-DIAGNOSIS-2026-06-17.md` — the 30K-placeholder hazard.
