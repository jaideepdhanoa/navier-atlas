# Slide 2 — `value_prop_bg` image brief (Grab deck)

**Role:** `value_prop_bg` (slide 2, exec-summary / "today & proof" hero)
**Status:** `needs_generation` (blocked) — distinct asset not yet composited. Slide 2 currently
shows the borrowed Three C's plate as a **documented interim only**.
**Why this brief exists:** reviewer call 2026-06-22 — the Three C's slide background is correct
as-is; slide 2 must get its **own** image instead of borrowing it. See `IMAGE-ROLE-CONTRACT.md`
→ "Slide 2 vs the Three C's slide (rev-2)".

Obey `docs/IMAGE-RULES.md` in full: canonical **N30 neutral** reference, **no Atlas-generated
images**, deterministic composite, provenance saved, stable URL before any live Slides update.

---

## The scene (literal)

A bright, optimistic **waterfront berth in the deck's anchor market** (Grab → Thai / SEA coastal
marina or river pier — e.g. a Bangkok Chao Phraya / Phuket-style pier). In the foreground, **a woman
stands on the pontoon at the berth, smartphone in hand, mid-booking a ride** — relaxed, confident,
glancing down at her phone as if confirming a pickup. Just off the dock at the berth sits the
**Navier N30** (canonical neutral: light/white hull, glass cabin with the V-mark, foils down,
daylight read), bow-left rear-quarter, ready to board. Calm water, soft natural light.

This is the **"convenience / it's-real-today"** beat: a real person, a real boat, a real booking —
the on-demand electric-boat experience as an everyday act.

## Composition & legibility

- **Aspect:** full-bleed 16:9, used as the slide-2 background behind a navy lower/edge **scrim**.
- **Subject placement:** weight the woman + vessel toward the **lower-left / lower-center third**.
  Keep the **right column and upper band visually calm** — that is where the exec-summary heading,
  subhead, and the 2×2 "Your world" beats sit (no KPI chips anymore). The N30 may extend center-right
  but must not crowd the right-column text zone.
- **Scrim:** navy gradient overlay (market plate sets time-of-day, per IMAGE-RULES "lighting is a
  plate property"). Ensure white copy stays legible over both the sky and the vessel.
- **Distinctness check:** must read as a clearly different photograph/scene from the Three C's plate
  (`…id=1ZyY6gGGWJ9ab4JFQdD2mUsputE70Rytz`) — different framing, subject action, and crop — so
  slides 2 and 3 never look like a repeat.

## Hard constraints (forbidden)

- No Atlas-generated imagery; no fantasy/impossible hull or scale.
- **No watermarks, no logos, no app UI chrome** (imply the booking via gesture/posture, not a visible
  ride-hail screen or brand mark).
- No baked-in other-market sunset on the vessel; lighting comes from the market plate + navy overlay.
- No embedded-only blob: composite → save asset + provenance → publish stable URL → then apply live.

## Provenance to save (in `image-manifest.json` + `ASSET-REGISTRY.json`)

prompt, seed (if available), provider, market-background source file(s), N30 neutral reference used,
mask, `builders/images/n30_composite.py` args, output path, and final stable `source_url`.

## Suggested asset naming (per contract convention)

`backgrounds/decks/grab/grab-slide2-bg-v2-berth-booking-composited.png`
