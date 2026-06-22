# Slide 2 — Executive-summary / thesis (deterministic build spec, Grok-owned)

**Owner:** Grok build loop. Tasklet supplies this spec + the distillation guardrails; Grok runs the generator.
**Why this slide exists:** the proposal prose is the sharpest asset we have and it was absent from the deck. This slide carries the *strategic story* so a partner deck is **more than numbers** — without dumping the proposal onto a slide.

## The principle: distillation, not paste
The partner proposal (`partner-pitch/partners/<partner>.json`) is the **source of truth** for narrative — exactly as `agg-*.json` / `growth-*.json` are for numbers. The slide is a **distillation** of it. We never paste paragraphs; we extract the skeleton and let the full prose keep living in the proposal. Discipline is enforced by **hard word caps** and a **no-orphan-numbers** check, both in the generator.

## Run it
```
python3 deck-studio/decks/gen_deck_narrative.py <partner>
python3 deck-studio/decks/gen_deck_narrative.py grab --validate   # reproduces the bar-setter
```
Reads `partner-pitch/partners/<partner>.json` → writes `deck-studio/decks/<partner>/narrative-slide2-<partner>.json`.

## Field mapping (source → slide field, with cap)
| Slide field | Source (proposal JSON) | Cap | Treatment |
|---|---|---|---|
| `partner_lockup` | `hero.title` (before em-dash) | — | small kicker, e.g. "Grab × Navier" |
| `positioning` | `hero.title` (after em-dash) | ≤ 8 w | big headline, e.g. "the black-car network, on the water" |
| `thesis` | `hero.subtitle` | ≤ 25 w | sub-headline (keeps multiple sentences if under cap) |
| `the_deal` | `hero.what_we_do_together` | ≤ 40 w | one tight line |
| `your_world[0] today` | `partner_context.their_ambition` | ≤ 25 w | block |
| `your_world[1] up_against` | `partner_context.their_pressure` | ≤ 25 w | block |
| `your_world[2] navier_fits` | `partner_context.where_navier_fits` | ≤ 25 w | block |
| `your_world[3] why_now` | `why_now` | ≤ 25 w | block |
| `proof_strip[≤4]` | `network_thesis.stats` | — | stat chips (label / value / sub) |
| `proof_sources` | `proof_points[].source` | — | provenance for the stat strip |

## Distillation rule (deterministic)
`distill(text, cap)` fills **whole leading sentences up to the word cap**. It never truncates mid-sentence. If even the first sentence exceeds the cap, it emits that sentence **unmangled** and adds a `_warnings` entry telling the author to tighten the *proposal* — **null/flag beats confidently-wrong**. Sentence splitting protects `$1.22B`-style decimals and known abbreviations.

## Eight hard rules (anti-misinterpretation)
1. **Never author prose here** — every field is extracted from the proposal JSON. A hand-written string = bug.
2. **The proposal is the only place to edit narrative.** To change what the slide says, edit `partner-pitch/partners/<partner>.json`, then regenerate. Do not edit the sidecar by hand.
3. **Caps flag, never truncate.** An overflow sentence ships whole + a `_warnings` entry; a human tightens the source.
4. **No orphan numbers.** Any figure shown in `thesis`/`the_deal`/`your_world` must be backed by `proof_sources`; the generator's `_orphan_number_check` FLAGs otherwise. External facts (partner financials, regulator dates) are **sourced**, not model outputs.
5. **Model numbers do NOT live here.** Pax/revenue/TAM belong to the economics sidecar (`gen_deck_economics.py`). This slide is strategy; that slide is numbers.
6. **Keep `_provenance_note` and `proof_sources`.** They mark the stat strip as sourced external facts.
7. **Missing source field → emit `null`**, never invent. A partner with no `hero.subtitle` gets `thesis: null`, not a fabricated thesis.
8. **`--validate` stays green** — it reproduces the committed bar-setter field-for-field. Run after any change.

## Sequencing / insertion (low blast radius)
New order: **1 cover → 2 exec-summary (this) → 3 cost·comfort·convenience (booking-moment) → 4 market KPIs → econ slides → TAM → roles.**
- Bindings are **object_id-based** and the economics slides read their indices from `economics-binding.json` — so inserting slide 2 only requires **re-keying the binding's slide indices**; `gen_deck_economics.py` and `gen_deck_narrative.py` do not hardcode positions.
- After inserting, re-pull the slide manifest so object inventory is fresh before any text op.

## Fallback for unusually rich narratives
If a partner's story can't sit in one slide without breaking caps repeatedly (many `_warnings`), split into two: **thesis slide** (lockup + positioning + thesis + the_deal + proof_strip) and a **"Why you / why now" slide** (the four `your_world` blocks). Prefer the split over overstuffing one slide.

## Wire the trigger
Whenever the proposal narrative changes (or a new partner is onboarded), rerun `gen_deck_narrative.py <partner>` and the renderer re-reads the sidecar — the slide tracks the proposal with no manual refresh. Same pattern as the economics regeneration.
