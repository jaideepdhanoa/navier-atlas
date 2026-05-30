# Plan — Make the First Markets *Sing*

_Tasklet · 2026-05-30 · for Jaideep's review. Goal: make the partner pages + city briefs bulletproof, partner-specific, and compelling **before** any new-market expansion — in a structured framework that stays cheap to extend._

---

## 0 · UPDATE — Jaideep decisions locked (11:03 PT) → plan v2

**Partner roster changes:**
- **Careem → UAE-only.** Careem is now mainly UAE-focused; re-cut its proposal to a UAE-only phased plan (drop the KSA/Egypt expansion phases).
- **+ Uber (NEW).** Broader MENA partnership angle — Uber is strong in UAE and running AVs there. Uber gets **three stories / market tabs: MENA, US, Global.**
- **+ Qatar proposal (NEW).** Relevant partner TBD by research — candidates Navier already spoke to: **Katara, Qatar Tourism**; also **Ministry of Transport (MOTC/MTT)**. Research who the right convener is.
- **+ Saudi Arabia / PIF proposal (NEW).** A national proposal to bring to **PIF** as target — bundles **NEOM + Red Sea + Jeddah + others** into one sovereign-scale story.
- Net partner set becomes: Grab, Uber (×3 markets), Careem (UAE), Dubai RTA, Abu Dhabi ITC, Qatar, Saudi/PIF, Red Sea Global, Singapore MPA.

**Commercial model — OFF the website.** Economics live in the **proposal deck**, not the page. Website's job: showcase **the need** for Navier marine mobility, **how many amazing journeys** open up when Navier is added to a **multimodal footprint**, and prove **we know their local use cases** so they grasp it instantly. → Schema WS-1 drops `commercial_model` from web-rendered fields; instead emphasizes **use-cases / journeys-unlocked / multimodal-fit**. (Financial model ingested to `/reference/mobility-unit-economics-model.md` for deck use.)

**MENA coverage add:** **Eastern Province — Dammam + Khobar**, anchored on the busy **Eastern Province ↔ Bahrain corridor** (marine mobility is exciting here; today it's the King Fahd Causeway).

**Fill order (revised):** **Malaysia + Manila FIRST.** Bodrum/Turkey → lower priority (defer).

**Rewrite sequence:** **Grab first** (confirmed).

**Riau / Singapore note (research + validate, then act):**
- Emphasize / reclassify **Bintan** (where the resorts are — the recognizable tourism node) rather than the less-familiar "Riau Islands" label.
- Strategic point = **start going cross-border from Singapore**: SG→Indonesia (Bintan) **and** SG→**Malaysia** (Johor/Desaru/Tioman — *even more important, more traffic*).
- Check we've captured **Singapore East Coast** berthing/harbor points — there's a domestic **East Coast → CBD** transport use case to pitch to Singapore authorities (landlocked, proactively investing in efficient transport infra).

---

## 1 · Diagnosis — where we are today

**What's already strong:** clean, partner-facing prose; archetype-aware; phased with KPIs + camera; strict platform discipline (Pioneer II ≤70 nm vs Quanta-LR long-haul); a clean extensible schema; node-id integrity fixed.

**What's missing to make a partner's BD/strategy team lean in (gap themes):**

| # | Gap | Why it matters to the partner |
|---|-----|-------------------------------|
| G1 | **No commercial model / unit economics** | Grab/Careem/RTA will ask in the first meeting: who owns the boats, capex, price/trip, revenue split, payback. We have none. |
| G2 | **We lead with Navier's product, not the partner's strategy** | The page should open with *their* ambition/problem (Grab's premium-tier margin push; RTA's 2040 marine modal-share target) and show Navier as the unlock. Today it opens with "foiling lifts the hull…". |
| G3 | **No competitive differentiation — esp. Candela** | A foiling-vessel partner *will* ask "why not Candela P-12?" (already in Stockholm transit + courting Saudi). We have zero rebuttal on the page. |
| G4 | **No proof/evidence layer with sources** | Claims ("millions/yr cross to Riau", "100 vessels Maldives") are unsourced. BD teams fact-check. We *have* the WSJ/Bloomberg refs in `/reference` — not wired in. |
| G5 | **No explicit "the ask" / division of labour** | Each page should state what Navier does vs what the partner does, plus the concrete next step (pilot MOU, exclusivity, co-marketing). |
| G6 | **Phases are marketing, not an operating plan** | Round boat numbers, no timeline, no per-phase economics, no go/no-go gate criteria, no risk + mitigation. (Directly answers your "think through phases more thoughtfully?" — **yes**.) |
| G7 | **No objection-handling / FAQ** | Range, sea-state/weather, safety & first-of-class certification, charging infra, monsoon/winter downtime. Partners raise these every time. |
| G8 | **Credibility moat under-used** | Founders Fund / Brin / Altman / Hoffman cap table, Turkey factory, software-defined + autonomy-ready, Maldives at-scale proof — barely surfaced. |

---

## 2 · Coverage answer (you asked directly)

**Grab — partial.** Grab operates in 8 countries. Covered as briefs: Singapore ✅, Indonesia (Bali, Jakarta/Batam, Lombok, Komodo ✅), Thailand (Phuket, Bangkok ✅). **Missing Grab heartlands:** 🔴 **Malaysia** (Penang/Langkawi/KL-Klang), 🔴 **Philippines** (Manila/Cebu/Palawan — map has nodes, no brief), 🔴 **Vietnam** (Hạ Long/HCMC/Da Nang), Cambodia (Sihanoukville). _Myanmar correctly excluded (politically active)._ The Grab **proposal** only sequences SG → Bali → Phuket — it skips Malaysia (despite the Langkawi↔Phuket featured route) and the Philippines/Vietnam entirely.

**MENA — strong but two real holes.** Covered: Dubai, Abu Dhabi, Doha, Manama, Muscat, Jeddah, RSG, Sharm, NEOM-Sindalah ✅. **Missing:** 🔴 **Bodrum / Turkey** (this is the **factory market** — strategically embarrassing to omit; also on the data-fix list for coords), 🟡 Kuwait, 🟡 Aqaba (Jordan — also a Careem market). Male = South Asia (covered).

**Careem — reasonable, could extend.** Covers Dubai, Abu Dhabi, Jeddah, Sharm. Careem's other water-relevant heartlands: 🟡 Bahrain (Manama brief exists), 🟡 Qatar (Doha brief exists), 🟡 Jordan/Aqaba, Pakistan (Karachi — low Navier-fit). Low lift to add Manama/Doha phases since briefs exist.

---

## 3 · Proposed work — 5 workstreams

### WS-1 · Upgrade the schema (foundation; do first, ~½ day)
Extend `partner_proposal.schema.json` and `city_brief.schema.json` with **optional** fields (backward-compatible — existing files stay valid) so the framework carries the missing dimensions and every future partner/city inherits them:

**Partner proposal — add:**
- `partner_context` — their strategy/ambition/pressure in their words (drives the new hero open). _(G2)_
- `commercial_model` — ownership, capex/opex split, pricing tier, revenue model, indicative unit economics, payback. _(G1)_
- `differentiation` — vs incumbent fast-ferry **and vs Candela**, + the software-defined/autonomy moat. _(G3)_
- `proof_points[]` — `{claim, evidence, source}` (wire WSJ/Bloomberg/Maldives refs). _(G4)_
- `the_ask` — Navier-does / partner-does / next step. _(G5)_
- `objections[]` — `{concern, response}` FAQ. _(G7)_
- per-phase: `timeline`, `gate_criteria` (go/no-go to next phase), `economics`, `risks[]`. _(G6)_

**City brief — add:** `sources[]` on demand_signals (cite the numbers), `competitive_landscape` (who runs the water today), `regulatory_note`, `seasonality` (monsoon/sea-state windows).

### WS-2 · Research pass (the real value-add; ~1 day, sourced)
A focused, **sourced** research sprint per partner — output saved to `/agent/home/navier/partner-pitch/research/<partner>.md`:
- **Their strategy & numbers:** stated goals, recent moves, footprint, relevant execs/decision path (cross-ref `humans.json`), what pressure they're under.
- **RTA / ITC / MPA:** their *published* marine modal-share & decarbonization targets, station build-outs, tender mechanisms.
- **Grab / Careem:** premium-tier strategy, margin pressure, regional exclusivity logic, super-app monetization.
- **RSG:** Red Sea destination phasing, fleet/jetty plans, sustainability mandates.
- **Competitive:** Candela P-12 status (Stockholm, Saudi interest), Damen/incumbent fast-ferry — crisp rebuttal lines.
- **Proof:** lock the Maldives/JIH deal specifics + WSJ/Bloomberg citations for reuse.

_(I'll use the web research capability; everything sourced and dated. Sensitive contact intel stays internal-only, never shipped to the page.)_

### WS-3 · Rewrite the 6 partner pages against the upgraded schema (~1 day)
Re-author each to: open with `partner_context`, embed economics + differentiation + proof + the ask + objections, and **sharpen phases** into an operating plan (timeline, gate criteria, economics, risk). One at a time, reviewed before moving on (your sequential rule).

**Phase rethink per partner (the substance of "think through phases"):**
- **Grab:** decide whether SG → Bali → Phuket is the right order vs SG → **Riau (own phase)** → Phuket+Langkawi (Andaman cross-border) → Bali-Lombok-Komodo (hero luxury) → Manila/Vietnam. Sequence by Grab's real demand + cross-border defensibility, not just geography.
- **Careem:** Dubai → UAE+Gulf → KSA (Jeddah/RSG) + Egypt — add gate criteria + the AD/KSA royal-channel reality.
- **RTA / ITC / MPA:** tie phases to their *published* targets + tender cycles; gate on first-of-class certification.
- **RSG:** tie to destination opening phases.

### WS-4 · City-brief deepening + coverage fill (~1 day)
- **Deepen** the 19 existing briefs: add sources, competitive landscape, seasonality, regulatory note.
- **Fill priority gaps** (briefs only — routes already in graph, no code): 🔴 **Bodrum/Turkey** (factory), 🔴 **Malaysia (Langkawi/Penang)**, 🔴 **Manila**, then 🟡 Vietnam (Hạ Long), 🟡 Kuwait/Aqaba. This extends Grab + MENA coverage to match the proposals.

### WS-5 · QA & integrity sweep (~½ day)
- Every partner phase-city has a brief (automated check).
- Every numeric claim has a source.
- Node-id integrity (the bug class we just fixed) + schema validation in the build.
- Optional: a `check_pitch_quality.py` lint (required fields present, no unsourced numbers, platform/range discipline) wired into dev pre-flight.

---

## 4 · Sequence & checkpoints
1. **WS-1 schema** (unblocks everything) → show you the new schema.
2. **WS-2 research** → share research notes per partner before rewriting.
3. **WS-3 rewrite**, one partner at a time, **Grab first** (your direct relationship + most coverage gaps) → you review each.
4. **WS-4 deepen + fill** city briefs.
5. **WS-5 QA**, then deploy + push.

Then return to the held data-quality TODOs (Bodrum/Setouchi coords, Penghu phantom, garbage POIs, `bp-*` naming) — note **Bodrum coords fix dovetails with the Bodrum brief in WS-4**, so I'd fold that in.

---

## 5 · Decisions I need from you
1. **Approve the schema upgrade** (WS-1) as the foundation? Any field you'd add/drop?
2. **Research depth:** web-research sprint OK? Anything you already know about each partner you want me to bake in (or avoid)?
3. **Coverage priority:** agree on the fill order — **Bodrum/Turkey + Malaysia + Manila first**? Add Vietnam now or defer?
4. **Grab phase re-sequence:** do you want Riau as its own phase and Malaysia/Andaman folded in — or keep the 3-phase SG→Bali→Phuket arc?
5. **Commercial model:** can you share the real numbers (ownership/pricing/revenue split, Maldives deal economics) so the unit-economics are credible — or should I frame them as illustrative ranges, clearly labelled?
6. **Sequence check:** Grab first for the rewrite?
