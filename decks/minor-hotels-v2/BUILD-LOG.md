# Hospitality Deck v2 — Build Log & Asset Map (reference instance: Minor Hotels × Navier)

**Live deck:** https://docs.google.com/presentation/d/1p5NtoaORRWyBpcsbfqnSB9PLg9yyTpvuzJAyBMjen4o/edit
**Source of truth (for any future Grok generator):**
- `deck_spec_minor.json` — all partner-facing copy + image bindings (plain English, zero internal jargon)
- `build_deck.py` — spec-driven 16:9 PPTX builder (scrim baking + layout renderers)

## Method
1. Author copy + bindings in `deck_spec_minor.json`. Every line is plain guest-and-margin English.
   None of the model/finance taxonomy (grounded floor, WIDTH, captive band, route ids, downweights)
   reaches a slide.
2. `build_deck.py` bakes legibility scrims over the hero images and lays out the slides, emits PPTX.
3. Upload-convert to Google Slides (fresh reference build — not a live-deck round-trip).
4. QA by exporting to PDF and reading Google's own render. Fix in the spec/builder, rebuild, replace
   the *same* fileId so the URL is stable.

## Spine (23 slides — simplified hospitality v2)
Cover · Exec "your world" (KPI-free, own hero) · Problem · Three C's (Cost·Convenience·Comfort) ·
Passenger experience (N30 hero) · Specs that matter · Proven & trusted · Footprint · 5 cluster
slides (UAE / Maldives / Thailand / Mediterranean Europe / Australia coastal) · Close ·
Appendix divider · 5 marquee-corridor unit-economics backup slides (one per cluster).

Dropped vs old Minor deck: deep technology-stack slide and charging-infrastructure slide.
No SOM/SAM/TAM/GMV ladder anywhere — replaced by one example corridor per cluster at the end.

## Canonical image asset map (stable raw-GitHub URLs)
Repo path: `decks/minor-hotels-v2/assets/`
Base: `https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/main/decks/minor-hotels-v2/assets/`
| Slide | Asset | Origin |
|---|---|---|
| Cover | `minor-cover-n30.png` | generated, N30-composited |
| Exec / slide 2 | `minor-slide2-exec-n30.png` | generated, distinct high-aerial, own prompt |
| Passenger experience | `minor-interior-n30.png` + N30 hero | generated |
| UAE cluster | `minor-uae-palm-n30.png` | canonical Drive asset (Palm/Burj) |
| Maldives cluster | `minor-maldives-n30.png` | generated |
| Thailand cluster | `minor-thailand-andaman-n30.png` | canonical Drive asset (Andaman) |
| Mediterranean Europe | `minor-medeurope-n30.png` | generated |
| Australia coastal | `minor-australia-n30.png` | generated |

All images keep the canonical N30 (compositing reference), market-specific backgrounds, no
Atlas-generated map images, minimal gold accents. Hosting is public raw-GitHub so the Slides
renderer fetches+embeds once at insert time (stable, no inaccessible embeds).

## QA fixes applied
- Gold rule moved *above* the title on bullets slides (two-line titles no longer struck through).
- Specs stat "All-weather" → "Any sea" (fit the 38pt serif column cleanly).

## For Grok codification
`build_deck.py` + `deck_spec_minor.json` are the deterministic generator seed. Future hospitality
decks: clone the spec, swap copy + the 8 image bindings per partner, keep the renderers. Hospitality
rules baked in: $1M/vessel economics, Cost·Convenience·Comfort, KPI-free slide 2 with its own image,
no ladder, marquee-corridor backups at the end.
