# Grok instruction — DiDi Mexico & inDrive Egypt: live-resync REQUIRED before any image bind
*2026-07-23 · gate referenced by each deck's `deck.config.json → image_bind_precondition`*

**Grok: read this before you touch backgrounds on these two decks. It changes how you treat them versus DiDi Brazil.**

## The flag
The repo's `slide-manifest.json` for **DiDi Mexico** (`1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c`) and
**inDrive Egypt** (`1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk`) is **stale**. It still shows the old hedged
spine ("PHASED REVIEW", "A joint route review is the next step") and the pre-expansion city set, and **none
of its slide IDs exist in the live decks**. The de-hedge rebuilds happened at the `.pptx` level and the
further corrections happened live in Google Slides — neither flowed back into the repo records.

So, **unlike DiDi Brazil** (whose repo manifest was current, which let the slide object IDs be filled in),
**every object ID was deliberately left `null`** in the Mexico and Egypt image specs, and each role binds by
**`expected_slide_title`** instead. Your **first step for these two must be a fresh live sync + city
reconciliation before you bind anything** — this is called out at the top of both `image-manifest.json`
files (`object_inventory.status: STALE_REPO_MANIFEST__REQUIRES_LIVE_SYNC`) and in
`deck-studio/docs/IMAGE-SPEC-CHANGESET-2026-07-23.md`.

## Do this, in order (both decks)
1. **Live sync.** `presentations.get` the live deck → overwrite `deck-studio/decks/{deck}/slide-manifest.json`
   with the true current slides + object IDs. Update the `notes` / slide count (they currently claim 18 / 12).
2. **Reconcile the city set** against the live econ (`WHAT ONE BOAT EARNS · …`) slides. The specs were
   reconstructed from the corrected `.pptx` + finance corridors, **not** read from the live deck:
   - **DiDi Mexico — 6 econ cities:** Cancún–Isla Mujeres, Playa del Carmen–Cozumel, Puerto Vallarta,
     Los Cabos, Isla Holbox, Bahías de Huatulco.
   - **inDrive Egypt — 5 econ cities:** Cairo, Hurghada, Sharm El Sheikh, El Gouna, Marsa Alam.
   Add or drop `econ_market_bg` roles so the manifest matches the live deck exactly.
3. **Re-key** `image-manifest.json` + `slide-image-bindings.json` to the live slide + image-element object
   IDs — match each role to its live slide by `expected_slide_title`, then resolve the full-bleed background
   element ID from the live inventory. **Never guess an ID or reuse a sibling deck's.**
4. **Generate → register (stable `source_url`) → `replaceImage` → QA gate 13** (image-completeness). Do not
   touch the Three C's slide or the human Atlas route-map slots.

## Assets already on disk (register, don't regenerate)
- Mexico `three_c`: `deck-studio/assets/didi/didi-mexico-three_c_bg.png` (unregistered). Market plates on disk
  for Isla Mujeres / Holbox / Huatulco — Holbox + Huatulco are half-registered (`status: null`); fix those.
- Egypt `three_c`: `deck-studio/assets/indrive/indrive-egypt/indrive-egypt-three_c_bg.png` (unregistered).

## Contrast: DiDi Brazil is different
DiDi Brazil's `image-manifest.json` already carries **real live slide IDs** (its repo manifest was current);
only the image-**element** IDs are pending. Follow `deck-studio/decks/didi-brazil/IMAGE-SPEC-HANDOFF-2026-07-23.md`
for Brazil — no full re-sync needed there.
