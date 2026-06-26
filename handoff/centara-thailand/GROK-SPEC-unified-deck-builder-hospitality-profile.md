# GROK SPEC — Unified deck builder: hospitality profile + page-fill backgrounds + retire bespoke scripts

**Owner:** Grok (deterministic model-to-deck generation lane).
**Author:** Tasklet. **Date:** 2026-06-26.
**Goal:** One config-driven deck builder that works consistently for **mobility** (Grab, Bolt, Careem…)
and **hospitality** (Minor, Centara…) templates, with **no drift** — no missed slides, no missed imagery.

> **Do NOT rebuild any live-edited deck** (Centara `1ekpZzZI…`, Minor `1p5Ntoa…`, LINE MAN `1wT1_t2H…`).
> Those were edited in place via Slides API; the corrected inputs are already in the JSON/source files.
> This spec is about the **generic engine + bindings + QA** so the *next* build reads the fixed inputs.

## Background — why this is needed
Two generations of tooling coexist in `deck-studio/builders/`:
- **Gen-1 (legacy):** one bespoke `deck_{partner}.py` per deck (`deck_minor_hotels.py`,
  `deck_grab_thailand.py`, `deck_bolt_*`, `deck_ocean_whisperer.py`…). Each hardcodes that deck.
  `deck_minor_hotels.py` was forked from the **Grab mobility** lineage (3 econ slides, background as an
  **element**), which is why nothing applied the hospitality **7 appendix page-fill** backgrounds.
- **Gen-2 (target):** config-driven — `decks/{deck}/deck.config.json` + `economics-binding.json` +
  generic `gen_deck_*` generators + the `deck_studio` CLI (`plan`/`apply`/`qa`). Mobility-shaped only.

Converge on Gen-2; branch it on `deck_type`.

## Required changes

### 1. Read `deck_type` everywhere
`deck.config.json` and `economics-binding.json` now carry `deck_type: "mobility" | "hospitality"`.
The generator + applier + QA must branch on it. (Centara + Minor already set it.)

### 2. Hospitality branch in the economics generator (`gen_deck_economics.py` or sibling)
When `deck_type == hospitality`:
- **Value source = the sealed hospitality sidecar**, not the mobility `agg-/growth-` model.
  Centara: `handoff/centara-thailand/centara-thailand-economics-sidecar.json` (7 corridors, `$1M/vessel`,
  6 OPEX lines, `co2_avoided_tonnes_year` sealed).
- **Emit the 7 appendix cards** (slides 18–24): eyebrow · corridor title · distance line · equation banner
  (gold "kept") · three value columns (gold result line, "kept" gold @15pt, right-aligned END,
  spaceBelow 5.5pt / c3v 10pt) · **CO₂ avoided / yr**. Object-ID map per card is in
  `decks/centara-thailand/economics-binding.json → appendix_cards[]`.
- **Do NOT emit** the mobility `slide_10` SOM/SAM/TAM/GMV ladder or the slide-3 network-KPI block.
- Honor `economics_frame`: `$1,000,000/vessel`, operator framing **Cost · Convenience · Comfort**
  (never "Captive · Calm · Clean").

### 3. Background binding schema (NEW) + applier
`economics-binding.json` now declares backgrounds explicitly:
- `appendix_backgrounds[]` — `{slide_index, page_object_id, asset_ref, source_url, apply:
  "updatePageProperties.pageBackgroundFill.stretchedPictureFill.contentUrl"}`. **Hospitality applier
  must apply these as PAGE-FILLS** (LB-262), not `navierBg_*` element swaps.
- `cluster_deepdive_backgrounds[]` — `{slide_index, asset_ref, apply: "replaceImage"}` for slides 9–14.
- `asset_ref` resolves to `ASSET-REGISTRY.json` → stable `source_url` (no embedded-only, no temporary
  `googleusercontent` URLs).

### 4. Retire Gen-1 bespoke builders
Mark `deck_{partner}.py` legacy; converge on `deck_studio` CLI reading `deck.config + economics-binding +
ASSET-REGISTRY + SLIDE-SPINE-AND-VARIANTS`. At minimum, **`deck_minor_hotels.py` must not be the build
path** for hospitality — replace with the generic hospitality branch.

### 5. Re-pull stale bindings against live gold
`decks/minor-hotels/economics-binding.json` still describes the **old 3-econ-slide** deck and carries the
ladder. Re-pull it against the **24-slide** gold: fill `appendix_cards[]` (7) + `appendix_backgrounds[]`
(7, page-fill). Extract the live Minor appendix **page object IDs** and **register each Minor market plate**
in `ASSET-REGISTRY.json` (currently `audit_pending` — do not fabricate IDs/URLs).

### 6. QA gate = render-complete checklist
Implement the gate in `deck-studio/docs/SLIDE-SPINE-AND-VARIANTS.md`:
- every SPINE slot present; every VARIANT image slot resolves to a stable registry URL or explicit null;
- **no VARIANT slide carries the gold deck's market content/imagery** (the Centara-appendix drift class);
- hospitality asserts: **no ladder**, econ backgrounds are **page-fills**, `co2` present, `$1M/vessel`,
  Cost·Convenience·Comfort. Mobility asserts its existing families unchanged.

## Inputs already laid down by Tasklet (read these; do not rebuild)
- `decks/centara-thailand/deck.config.json` + `economics-binding.json` — hospitality profile, 7 cards +
  7 page-fill backgrounds, object-ID map, applied-state source-of-truth. (commit `511a0c26`)
- `handoff/centara-thailand/centara-thailand-economics-sidecar.json` — now includes `co2_avoided_tonnes_year`.
- `ASSET-REGISTRY.json` — 16 Centara assets (`centara-cluster-*`, `centara-econ-*`, `centara-*-logo`) +
  `centara-thailand` & `minor-hotels` deck_coverage.
- `deck-studio/assets/IMAGE-ROLE-CONTRACT.md` — hospitality addendum (cluster_hero, page-fill econ, no ladder).
- `deck-studio/docs/SLIDE-SPINE-AND-VARIANTS.md` — Template A (hospitality 24-slide) + Template B (mobility).
- `decks/minor-hotels/economics-binding.json` — patched: `deck_type: hospitality`, ladder deprecated,
  `appendix_backgrounds_policy: audit_pending`.

## Handback requirements (MANDATORY — no self-certified completion)
Return: **branch name · PR link · commit SHA · exact files changed · validation receipt** (actual QA-gate
run output, not a line-range audit) · **explicit list of nulls/held items**. No "done" without the receipt.
