# Grok task — create the LINE MAN Wongnai × Navier deck (mirror of Grab Thailand)

**Owner:** Grok (deterministic create/bind/apply/render). **Author of inputs:** Tasklet.
**Editing mode:** Google Slides API only. No PPTX round-trip, no full-replace, no manual visual drift.

## Mandate
Create a new live Google Slides deck for **LINE MAN Wongnai × Navier** by mirroring the **Grab Thailand**
gold deck (`11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo`), changing **only** partner-facing narrative and
the cover logo. This is the same `create-from-grab-…-template` path used to build Grab Thailand itself.

## Inputs (all in this package / repo)
- `deck-studio/decks/line-man-wongnai/deck.config.json` — deck identity, scope decision, cover-logo binding.
- `deck-studio/decks/line-man-wongnai/SLIDE-COPY-DIFF.md` — **the authoritative slide-by-slide copy map**
  (global token swaps + per-slide bespoke rewrites + the Thailand-scope drop list).
- `partner-pitch/partners/line-man-wongnai-derivative.json` — the partner proposal (narrative source of truth).
- `assets/logos/partners/line-man-wongnai/logo-lmwn.png` (+ `LOGO-SOURCE.json`) — banked cover logo.
- Grab Thailand gold sources (read-only reference): `partner-pitch/partners/grab-thailand.json`,
  `deck-studio/decks/grab-thailand/*`, `finance/recal/agg-grab-thailand.json`,
  `finance/recal/growth-grab-thailand.json`.

## Steps
1. Create the new presentation; record `deck_id` + `live_deck_url` back into `deck.config.json`.
2. Build the Thailand-scoped slide sequence (16 slides) by mirroring Grab Thailand and **dropping the 8
   regional slides** (Manila, Boracay, Langkawi, Penghu — example + unit-econ). Honor `full_mirror` if set.
3. Apply `SLIDE-COPY-DIFF.md` via style-preserving `deleteText`+`insertText` ops. **Numbers never change.**
4. Replace the cover partner logo with the banked LINE MAN Wongnai wordmark (registry-resolved URL; no re-embed).
   Reuse all Thai market backgrounds from the grab-thailand registry — do **not** regenerate images.
5. Run `deck-studio/qa/partner_copy_lint.py line-man-wongnai` (blocking). Zero `Grab` tokens; no internal
   taxonomy; SOM/SAM/TAM/GMV only as labels with plain-English descriptors.
6. Export PDF QA; verify the four KPI tiles, the TAM ladder, and one unit-econ slide are byte-identical to Grab Thailand.

## Return a QA receipt
deck_id, slide count, copy-lint result, zero-`Grab` proof, cover-logo provenance, image-reuse ledger (no
re-embed), number-parity spot-check, and any unresolved gaps.

## Notes / holds
- Economics `economics_url` is null until the Thailand cascade is re-run under `partner_id=line-man-wongnai`
  (the deck currently reuses Grab Thailand's numbers verbatim, which is correct for a mirror). If/when a
  LINE MAN Wongnai sheet exists, wire `economics_url` and the TAM-ladder rung deep-links.
- Do not rebuild or re-seal the Grab Thailand deck; this is a brand-new sibling deck.
