# Slide-2 exec-summary — the render/paint path (binding + one-time gold create)

This closes the loop that `SPEC-deck-narrative.md` opened. That spec produces the **content**
(`narrative-slide2-<partner>.json`, distilled from the proposal). This spec **paints it onto the deck**.

It deliberately mirrors the **economics** layer so there is one mental model:

| Layer | Content (WHAT) | Binding (WHERE) | Paint |
|---|---|---|---|
| Economics | transparent sheet / `agg-*.json` | `economics-binding.json` | `deleteText(ALL)`+`insertText` into gold object_ids |
| **Narrative (this)** | `narrative-slide2-<partner>.json` | `narrative-binding.json` | same — into the **same** object_ids on every gold copy |

## Why a one-time gold create (not per-build slide creation)
Every partner deck is a **copy of the Grab gold deck** — that is why Bolt's economics object_ids
are identical to Grab's. So we create the exec-summary slide **once, in gold**, with
**pre-assigned object_ids**, and it propagates to every future copy for free. Benefits:
- **Determinism** — IDs are chosen by us (Slides API allows `objectId` on `createSlide`/`createShape`), known ahead of time, pinned in `narrative-binding.json`.
- **Quality** — the layout is hand-tuned once to the bar, not re-synthesized programmatically each build (no per-build geometry drift).
- **Simplicity** — after the one-time create, painting any partner is pure style-preserving `deleteText`+`insertText`, exactly like economics. No slide creation at paint time.

## The three steps

### Step 1 — ONE-TIME: create the slide in gold
Apply `decks/grab/narrative-slide2.gold-create.editplan.json` **once** to the gold deck
(`18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs`) via `slides_api_batch_update`.
- `createSlide` at `insertionIndex: 1` → lands as **slide 2**, pushing Cost·Comfort·Convenience to slide 3.
- `createShape` per slot with the fixed `narr2_*` IDs + geometry + styling + Grab seed text.
- 69 requests, 25 object_ids, all charset/length-valid.
- **Additive, single-slide insert** — never a full-deck replace, never a PPTX round-trip.
- After applying: re-capture the realized slide into `golden-template-map.json` (a `pending_slide_inserts`
  descriptor is already there), and wire `narr2_image` via `image-manifest.json` (N30 archetype **A2**).

> **Replay caveat:** any deck **already forked** from gold before this ran will NOT have the slide —
> replay the same editplan against those presentation_ids. Decks still `scaffold_pending_gold_copy`
> (e.g. Bolt) inherit it automatically on copy. This is the only non-automatic consequence of one-time create.

### Step 2 — Pin (already done, deterministic)
`narrative-binding.json` maps every narrative field → its `narr2_*` object_id. Regenerate with
`python3 gen_narrative_binding.py grab` (`--validate` reproduces field-for-field). The binding is the
contract; the IDs never change.

### Step 3 — Per-deck paint (every partner, repeatable)
For partner P:
1. `python3 gen_deck_narrative.py P` → `narrative-slide2-P.json` (content, distilled from `partners/P.json`).
2. For each **present** pin in `narrative-binding.json`: `deleteText{objectId, textRange:ALL}` then
   `insertText{objectId, insertionIndex:0}` with the value from the narrative JSON.
3. Skip pins where `present:false` — **null beats confidently-wrong**; never insert invented prose.
4. Run QA gates (below). Image slot is filled by the image layer, not here.

## Field → object_id map (the contract)
| Field (narrative JSON) | object_id | Notes |
|---|---|---|
| *static* | `narr2_kicker` | "PARTNER PROPOSAL" eyebrow |
| `partner_lockup` | `narr2_lockup` | e.g. "Grab × Navier" |
| `positioning` | `narr2_positioning` | e.g. "the black-car network, on the water" |
| `thesis` | `narr2_thesis` | the one-line thesis (keeps its punchline) |
| `the_deal` | `narr2_deal` | one-sentence deal |
| *static* | `narr2_world_label` | "Your world" |
| `your_world[0..3].label/.text` | `narr2_wN_h` / `narr2_wN_b` | today / up-against / where-Navier-fits / why-now |
| `proof_strip[0..3].value` / `.label·.sub` | `narr2_chipN_v` / `narr2_chipN_c` | proof chips |
| *(image layer)* | `narr2_image` | N30 archetype A2; never embedded here |
| *(accent)* | `narr2_rule` | thin gold rule |

## QA gates (same family as economics)
- **leak_denylist** — no other partner's place-names/values.
- **char_budget_scan** — caps enforced upstream by the generator (flag, not truncate).
- **orphan_number_check** — any number on the slide must trace to `proof_sources`, else FLAG.
- **style_reset_scan** — `deleteText`+`insertText` preserves box style; verify no font/colour reset.
- **drift_gate** + **render_thumbnails** — visual confirm post-paint.

## What is Grok-owned now
Generation **and** render. Grok runs `gen_deck_narrative.py` → `gen_narrative_binding.py` (once per gold
structural change) → emits the per-deck `deleteText`/`insertText` ops from `narrative-binding.json`.
Tasklet supplies the contract (IDs, geometry, styles, gates), not hand-typed slides.

## Beat distillation (LB-256)
Beats are **2-line teasers**, not full sentences — the 2×2 grid box physically holds ~14 words.
`gen_deck_narrative.py` therefore runs a **clause-aware beat distiller** (`distill_beat`) on
`your_world[*].text` only — it trims at a clause/conjunction boundary and appends an ellipsis,
preserving the lead idea. **thesis/the_deal/positioning are never beat-trimmed** (they keep their
full punchline). Caps: beat ≤ 14 words. The full thought still lives in the proposal + the later
"why-now" slide; the beat only has to *open the loop*.

## Geometry note (LB-256)
Slides does **not** clip text to the text-box height — only the **page edge** clips. The lower block
(beats + proof-chip strip) is tuned so a **2-line chip caption clears the 5143500 EMU page bottom**:
beat row2 body ends 4525000, chip values at 4585000, captions at 4780000 (2-line end ≈ 5060000).
If you re-tune, keep the chip-caption bottom inside the page edge or captions will silently truncate.

## Live execution log
- **2026-06-22** — One-time gold-create **executed** against the live Grab deck
  (`18yDAgO0…NCdSs`) via additive single-slide insert (`createSlide @ insertionIndex 1`,
  **no full-replace**). Slide 2 is now the exec-summary; the original three-C's slide shifted to 3.
  Applied as 7 ordered `batchUpdate` chunks (page+dark-background first, then style-preserving
  shape groups). A dark page background (`#0a0a0c`) is set on create because the deck's dark look
  comes from a full-bleed background, and the text styles assume a dark base. `narr2_image`
  (right ~35%) is **reserved empty** for the N30 archetype-A2 image (the woman-on-phone-at-berth
  booking moment) — to be filled by the image layer, never embedded here.
- **2026-06-22 (slide-2 v2, partner-comment pass)** — three reviewer comments resolved on the
  live deck, surgically (no re-mint, manual reviewer edits preserved):
  1. **Image (was plain black).** Wired `grab-value_prop_bg` (existing N30 market composite,
     stable Drive URL) **full-bleed** behind the text + a navy scrim rectangle (`alpha 0.5`),
     text brought to front; `narr2_image` placeholder deleted. The boat sits in the clear
     right third where there is no text; the woman-at-berth reads in the scrimmed left.
     This was the never-executed `post_create_action`. Manifest → `applied_live`.
  2. **"Why now" was incomplete/overflowing.** The long `why_now` proposal lead cannot be
     clause-trimmed into a complete beat (it left a mid-thought ellipsis). Added a
     deterministic **`your_world_beats.<key>` override** in the generator: a short COMPLETE
     beat is used verbatim (still cap-flagged). `grab.your_world_beats.why_now` set; regen is
     warning-free and 2-line clean above the chips.
  3. **KPI overlap between slide 2 and slide 4 (250 vs 1,000+ vessels).** Division of labor:
     **slide 2 = today/proof, slide 4 = scale/TAM.** Removed the confusing middle
     "250+ vessels / 120+ booked corridors" chip. New slide-2 quartet (today ladder):
     `30+ clusters · ~100 vessels (live, Maldives $100M) · 2026 (proof, WSJ & Bloomberg) ·
     2030 (regulator)`. The only vessel numbers are now ~100 (live, slide 2) → 1,000+
     (maturity, slide 4): a progression, not a contradiction. Slide 4 left untouched; each
     metric now appears exactly once.
- **2026-06-22 (slide-2 v3, partner-comment pass #2)** — two further reviewer comments:
  1. **Remove the bottom KPI chips entirely; give the copy room.** The whole proof-chip strip
     was creating more risk/uncertainty than value (and still echoed slide-4 numbers). Removed
     all four chips (`narr2_chip{1..4}_{v,c}` → **retired**) on the live deck *and* in the
     playbook. The 2x2 "Your world" beats were enlarged (head 10→**11pt**, body 8.5→**10pt**)
     and spread into the freed lower third. `gen_narrative_binding.py` no longer paints chips;
     `network_thesis.stats` is retained in the narrative JSON for the **economics sidecar +
     slide 4 only** (`_proof_strip_painted_on_slide2: false`). Slide 2 now carries **no
     numbers** — quantified proof lives on slide 4 (THE REGION). The one-time gold-create
     editplan was regenerated to the new design (scrim + full-bleed bg, no chips, no
     right-zone image box) so future gold copies inherit it; `--validate` reproduces.
  2. **Same image on slides 2 and 3 — intentional?** No. See
     `assets/IMAGE-ROLE-CONTRACT.md` → "Slide 2 vs the Three C's slide". The contract assigns
     `value_prop_bg` to slide 2 and treats slide 3 as a **data/KPI** role; there is no
     same-image rule. They matched only because `value_prop_bg` was banked from the *same* N30
     composite the Three C's slide already used. **Definitive policy: distinct backgrounds.**
     Added role `three_cs_bg` (status `needs_sourcing`, documented interim share) and repointed
     `value_prop_bg` to the real slide-2 image (`narr2_bg_img`).
  - **rev-2 (same day, reviewer follow-up):** direction reversed — the **Three C's slide
     background is correct as-is**; the new image belongs on **slide 2**, not slide 3.
     `three_cs_bg` is now the **canonical** Three C's plate (`applied_live`, no sourcing open),
     and **`value_prop_bg` (slide 2) is `needs_generation`** with a literal brief at
     `assets/backgrounds/decks/grab/SLIDE2-IMAGE-BRIEF.md` (woman on a phone at the berth booking
     a ride, N30 at the dock, market plate + navy scrim, distinct from the Three C's plate). The
     borrowed Three C's plate stays on live slide 2 as a **documented interim only** until the
     distinct composite is sourced (N30 neutral, no Atlas-generated images, provenance + stable URL).
  - **rev-3 (same day, image SEALED):** generated the distinct slide-2 composite and **locked it**.
     Scene: modern city riverfront skyline, woman lower-left on her phone walking the dock to board,
     canonical N30 bow-to-dock with gangway, navy lower-third scrim — reference-guided on the **N30
     neutral only** (the Three C's plate was deliberately *not* used as a composition reference; that
     incidental reuse caused the earlier echo). Published to the public deck-assets Drive folder
     (`id=1OiOsLLNSdzR9P0vwZ7S_sQr42RWd5EFe`), registered, and applied live via **`replaceImage`** on
     `narr2_bg_img` (in place; transform/scrim/z-order preserved). Interim Three C's plate **retired**.
     `value_prop_bg` is now declared **market-specific** (one variant per anchor market); the
     deterministic per-market process + literal prompt template live in `SLIDE2-IMAGE-BRIEF.md`.
  - **Live geometry fix (same pass):** the four "Your world" beats were inconsistent — the bottom row
     (`narr2_w3/w4`) was full-width (scaleX 1.0) and overran into the right column. Narrowed to match
     the top row (effective width ~2,480,000 EMU) so the 2×2 grid is collision-free. The generator
     (`gen_narrative_binding.py`) already emits the uniform width, so new decks are unaffected.
