# Deck image-spec changeset — 2026-07-23  ·  SINGLE SOURCE OF TRUTH
*Point Grok here. Locks the image contract for all four country decks so backgrounds can't drift again.
No images were generated (no image-gen in this environment) — generation + live-deck apply stay with Grok.*

## Why
DiDi Brazil slides 8/9/10 shared one image (should be per-city) and slide 12 was identical across every deck
(should be per-deck). Root cause (Tasklet audit + our cascade): **no deck had a `slide-image-bindings.json`,
and manifests didn't declare the econ/narrative background roles**, so every non-cover background fell back to
a template plate. Fixed structurally below, plus a playbook gate so it can't recur.

## Read order for Grok
1. This changeset (overview + per-deck status).
2. `handoff/partner-map-model/MX-EG-IMAGE-BIND-RESYNC-2026-07-23.md` — the live-resync procedure for the three
   stale decks (DiDi Mexico, inDrive Egypt, inDrive Brazil).
3. `deck-studio/decks/didi-brazil/IMAGE-SPEC-HANDOFF-2026-07-23.md` — the Brazil generation worklist.
4. Each deck's `deck.config.json → image_bind_precondition` (machine-readable gate) + `image-manifest.json`
   (`object_inventory.status`) + `slide-image-bindings.json`.

## Per-deck status
| Deck | Repo slide-manifest | Image spec | Object ids | Generation needed |
|---|---|---|---|---|
| **didi-brazil** | current | rebuilt 24-role manifest + bindings | **slide ids real**, element ids pending | **12 composites** + register cover |
| **didi-mexico** | **STALE** (hedged, pre-expansion) | rebuilt 19-role manifest + bindings | **all null — live sync req'd** | 11 composites + register three_c |
| **indrive-egypt** | **STALE** (hedged, 2-city) | rebuilt 17-role manifest + bindings | **all null — live sync req'd** | 10 composites + register three_c |
| **indrive-brazil** | **STALE** (hedged spine) | new 23-role manifest + bindings | **all null — live sync req'd** | **0 — inherits from didi-brazil** |

## Files changed (all under `deck-studio/` and `handoff/`)

### Playbook — the recurrence fix
- **`deck-studio/docs/PARTNER-DECK-GROK-HANDOFF-PLAYBOOK.md`** *(modified)* — added an **image-completeness**
  non-negotiable + **QA gate 13**: every background role must be declared and bound to a live object id,
  `slide-image-bindings.json` must exist, per-deck backgrounds (`partner_roles_bg`/`tam_bg`/`value_prop_bg`/
  `close_bg`) and per-city `econ_market_bg` may not be shared across slides, and no background may resolve to
  the gold/template chassis or a sibling deck. (Also carries the 2026-07-23 copy/tone gates.)

### DiDi Brazil — READY TO BIND (repo manifest was current)
- **`decks/didi-brazil/image-manifest.json`** *(rebuilt 4 → 24 roles)* — real live slide ids; stale
  `role_contract` pointer fixed. 12 backgrounds `needs_generation`, cover `needs_registration`, three_c
  `checked_in`, 9 human Atlas slots.
- **`decks/didi-brazil/slide-image-bindings.json`** *(created)* — 23 bindings.
- **`decks/didi-brazil/IMAGE-SPEC-HANDOFF-2026-07-23.md`** *(created)* — 12-image worklist, ready-to-paste
  cover registry entry, apply sequence. Only image-**element** ids pending (resolve from live inventory).

### DiDi Mexico + inDrive Egypt — SPEC LOCKED, LIVE SYNC REQUIRED
- **`decks/didi-mexico/image-manifest.json`** *(rebuilt, 19 roles)* + **`slide-image-bindings.json`** *(created)*
- **`decks/indrive-egypt/image-manifest.json`** *(rebuilt, 17 roles)* + **`slide-image-bindings.json`** *(created)*
- **`decks/didi-mexico/deck.config.json`** + **`decks/indrive-egypt/deck.config.json`** *(modified)* — added the
  machine-readable **`image_bind_precondition`** gate (`status: live_resync_required`) so an automated run
  trips before binding.
- **Why:** the committed `slide-manifest.json` for both is **stale** — old hedged spine ("PHASED REVIEW",
  "joint route review") + pre-expansion city set, slide ids **absent** from the live decks. So **every** target
  id is `null` (`object_inventory.status: STALE_REPO_MANIFEST__REQUIRES_LIVE_SYNC`); roles bind by
  `expected_slide_title`.
- **City sets** (reconstructed from the corrected `.pptx` + finance corridors — reconcile against live):
  Mexico (6 econ): Cancún–Isla Mujeres, Playa del Carmen–Cozumel, Puerto Vallarta, Los Cabos, Isla Holbox,
  Bahías de Huatulco · Egypt (5 econ): Cairo, Hurghada, Sharm El Sheikh, El Gouna, Marsa Alam.

### inDrive Brazil — INHERITS FROM DIDI BRAZIL, LIVE SYNC REQUIRED
- **`decks/indrive-brazil/image-manifest.json`** *(new, 23 roles)* + **`slide-image-bindings.json`** *(created)*
  + **`decks/indrive-brazil/deck.config.json`** *(modified — `image_bind_precondition` gate)*.
- **Zero net-new generation.** inDrive Brazil = DiDi Brazil with a different partner narrative, so every
  background is inherited: 6 deck-scoped roles **copy DiDi Brazil's asset**, 8 econ roles **bind the same
  shared city-keyed plate**. Exceptions: the cover uses the **inDrive** logo (banked in its `deck.config`),
  and the partner-roles / cover on-slide **text** is inDrive-specific (already in the deck).
- Repo manifest is stale (hedged), so ids are null pending the same live sync; roles bind by
  `expected_slide_title`.

### Handoff instruction (the three stale decks)
- **`handoff/partner-map-model/MX-EG-IMAGE-BIND-RESYNC-2026-07-23.md`** *(created)* — the live-sync-first
  procedure, phrased as a direct instruction to Grok; referenced by all three `image_bind_precondition` gates.

## What Grok does next
1. **DiDi Brazil (no re-sync):** resolve the per-slide image-element ids from the live deck → generate the 12
   composites (Brazil handoff worklist) → register + publish stable URLs → `replaceImage` → QA gate 13.
2. **DiDi Mexico / inDrive Egypt:** `presentations.get` → overwrite `slide-manifest.json` → reconcile the city
   set → re-key the specs by `expected_slide_title` → generate → register → apply → QA gate 13.
3. **inDrive Brazil:** `presentations.get` → reconcile to the de-hedged DiDi-Brazil structure → **copy DiDi
   Brazil's finished assets** (deck-scoped) + **bind the shared city plates** (econ) + keep the inDrive cover
   logo → apply → QA gate 13. No generation of its own.

## On-disk assets already available (register/copy, don't regenerate)
- Brazil cover `assets/didi/didi-cover-rio-n30.png`; Brazil three_c (registered).
- Mexico three_c `assets/didi/didi-mexico-three_c_bg.png` (unregistered); market plates for Isla Mujeres /
  Holbox / Huatulco (Holbox + Huatulco half-registered, `status: null` — fix).
- Egypt three_c `assets/indrive/indrive-egypt/indrive-egypt-three_c_bg.png` (unregistered).

## Not done here (needs Grok / image-gen / git / Slides API)
Generating composites · publishing stable `source_url`s (git) · resolving live object ids · `replaceImage` on
the live decks. The repo now carries the enforceable spec + gates; those steps consume it.
