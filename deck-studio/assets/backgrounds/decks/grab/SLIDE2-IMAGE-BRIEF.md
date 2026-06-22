# Slide 2 — `value_prop_bg` image brief + per-market process (deck-builder canonical)

**Role:** `value_prop_bg` (slide 2, exec-summary / "today & proof" hero)
**Status:** ✅ **SEALED for Grab (SE Asia)** — distinct composite generated, locked in the asset pack,
and applied live (`replaceImage` on `narr2_bg_img`). Interim borrowed Three C's plate **retired**.
**Rule (definitive, rev-3 — 2026-06-22):** `value_prop_bg` is **market-specific**. Every deck's
slide-2 image is generated for that deck's **anchor market**. There is **one variant per market** —
never a shared cross-market plate, never the Three C's plate.

Obey `docs/IMAGE-RULES.md` in full: canonical **N30 neutral** reference, **no Atlas-generated
images**, deterministic scrim, provenance saved, **stable URL before any live Slides update**.

---

## Sealed reference — SE Asia (Grab)

| field | value |
|---|---|
| asset | `backgrounds/decks/grab/grab-value_prop_bg-southeast_asia.png` (1536×864) |
| drive_file_id | `1OiOsLLNSdzR9P0vwZ7S_sQr42RWd5EFe` |
| source_url | `https://drive.google.com/uc?export=download&id=1OiOsLLNSdzR9P0vwZ7S_sQr42RWd5EFe` |
| live target | presentation `18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs`, slide `narr2_page`, image `narr2_bg_img` |
| provenance | `grab-value_prop_bg-southeast_asia.provenance.json` |
| market read | modern city riverfront skyline (Bangkok-style), on-demand commuter mood |

This is the **gold reference** for the scene/composition. Other markets re-shoot the *same beat* with
their own locale (see "Market-specific rule" below).

## The scene (literal, market-agnostic beat)

A bright, optimistic **waterfront berth in the deck's anchor market**. In the **lower-left**
foreground, a **professional woman stands/walks on the dock, smartphone in hand, mid-booking a ride**
— relaxed, confident, glancing at her phone as she steps toward the boat to board. At the berth sits
the **Navier N30** (canonical neutral: light/white hull, glass cabin with the V-mullion, foils down,
daylight read), bow toward the dock with a low boarding step/gangway. Calm water, natural light.

This is the **"convenience / it's-real-today"** beat: a real person, a real boat, a real booking.

## Market-specific rule (how variants differ)

Keep the **beat identical** (woman + phone + booking + N30 at the dock + lower-left weighting + navy
scrim). Change the **locale plate** to the deck's anchor market, and keep it **distinct from that
deck's Three C's plate** (different framing/crop/action):

| market | locale read (example) |
|---|---|
| **SE Asia (Grab)** — SEALED | modern city riverfront skyline (Bangkok-style), morning commuter energy |
| Gulf / UAE (Careem) | modern Gulf marina / corniche, contemporary towers |
| Mediterranean (Bolt · Aegean) | Aegean harbour town, whitewashed waterfront |
| *(other)* | the anchor market's signature working waterfront — never a generic/duplicate bay |

> Lighting is a **plate property** (per IMAGE-RULES): generate the N30 **neutral**; the market plate
> + navy overlay set time-of-day. Never bake another market's sunset onto the vessel.

## Composition & legibility

- **Aspect:** full-bleed 16:9, used as the slide-2 background behind a navy lower/edge **scrim**.
- **Subject placement:** weight the woman + vessel to the **lower-left / lower-center third**. Keep the
  **right column and upper band visually calm** — that is where the exec-summary heading, subhead, and
  the 2×2 "Your world" beats sit (no KPI chips). The N30 may extend center-right but must not crowd the
  right-column text zone.
- **Scrim:** navy lower-third gradient overlay; white copy must stay legible over sky and vessel.

## Hard constraints (forbidden)

- No Atlas-generated imagery; no fantasy/impossible hull or scale.
- **No watermarks, no logos, no app UI chrome** (imply the booking via gesture/posture, not a visible
  ride-hail screen or brand mark).
- No baked-in other-market sunset on the vessel.
- No embedded-only blob: composite → save asset + provenance → publish stable URL → then apply live.

---

## Deterministic per-market process (Grok-runnable)

Inputs: `{deck}`, `{anchor_market}`, `{locale_read}` (from the market table above), `{n30_neutral_ref}`
= `assets/n30/n30-reference-neutral.png`, `{three_cs_plate_id}` (that deck's slide-3 background).

1. **Generate** (reference-guided; pass **only** `{n30_neutral_ref}` — never the Three C's plate):
   size `1536x864`, with the literal prompt template below.
2. **Scrim** (deterministic, reproducible): navy `rgb(11,22,46)` lower-third gradient, start at 0.42·H,
   max alpha 150, ease `t**1.6`. Save raw + composited PNG.
3. **Provenance:** write `…-{market_slug}.provenance.json` (prompt, provider, references, scrim params,
   sha16, supersedes, forbidden-check).
4. **Publish stable URL:** upload the composited PNG to the public deck-assets Drive folder
   `14PFDM6Z-I9j4gDzJpt6yYiizojTUr0FF` (inherits link-sharing) → record `drive_file_id` + `source_url`.
   Verify the `uc?export=download` URL returns HTTP 200 + a PNG before proceeding.
5. **Register:** update `ASSET-REGISTRY.json` (`{deck}-value_prop_bg`, `market_slug`, `status:checked_in`,
   `delivery.stable_url_status:ready`) and `decks/{deck}/image-manifest.json` (`status:applied_live`).
6. **Apply live (in place):** Slides `replaceImage` on the deck's slide-2 background object
   (`imageReplaceMethod: CENTER_CROP`) using `source_url`. Do **not** delete/recreate; keep transform,
   scrim, and text z-order.
7. **QA gate (export → render slide 2):** all must pass, else revert:
   - background is the new market plate (not the Three C's plate; pass distinctness check);
   - woman lower-left with phone, N30 at the dock, gangway visible;
   - right-column heading + 2×2 beats legible, **no text collision** (the four "Your world" beats are
     equal-width, ~2,480,000 EMU; bottom row must not overrun into the right column);
   - no logos/UI/watermark; vessel matches the N30 neutral reference.

### Literal prompt template

> Photorealistic wide 16:9 marketing background for a pitch-deck slide. CONCEPT: an everyday on-demand
> mobility moment at a **{locale_read}** waterfront — deliberately NOT a wild tropical/karst bay.
> FRAMING intimate and human-first: in the LOWER-LEFT foreground, a close three-quarter view of a
> professional woman in smart business-casual, smartphone in one hand as she finishes booking her ride
> and steps toward the boat to board — candid, confident, in-motion. NO visible phone screen, NO logos,
> NO brand marks, NO watermarks, NO app UI. The boat is pulled up to a modern floating dock at
> center-right, bow angled toward the dock as if just arrived, a low boarding step/gangway near the
> woman. Match the vessel EXACTLY to the reference image: light/white hull, dark glass cabin with a
> V-shaped mullion, sleek low modern profile, twin outboard pods, hydrofoils at dock level; daylight-
> neutral read on the vessel. Keep the UPPER band and the RIGHT THIRD calm and uncluttered (open sky /
> soft skyline) for overlaid headline and body copy. Realistic photography, shallow depth of field on
> the background, sharp on the woman and boat, no text anywhere in the image.

### Field mappings (no interpretation drift)

| placeholder | source |
|---|---|
| `{locale_read}` | market table in this brief, keyed by `{anchor_market}` |
| reference image | `assets/n30/n30-reference-neutral.png` (only) |
| output size | `1536x864` |
| scrim params | navy `(11,22,46)`, start `0.42·H`, max alpha `150`, ease `t**1.6` |
| live target object | deck `image-manifest.json` → `value_prop_bg.target_object_id` |
