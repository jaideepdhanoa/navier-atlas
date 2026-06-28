# AirAsia MOVE × Navier — Deck Build Receipt

**Built:** 2026-06-28
**Live deck:** https://docs.google.com/presentation/d/1PAs3wvHcUB6ykiG3jbx_-XmzveXmI1K9HIJPLKbYkyI/edit
**deck_id:** `1PAs3wvHcUB6ykiG3jbx_-XmzveXmI1K9HIJPLKbYkyI`
**Branch:** `airasia-deck-build-2026-06-28`
**Build method:** Slides API only (create + batchUpdate). No PPTX round-trip, no full-replace.

## Visual system (gold, inherited from live Grab Thailand deck)
- Headlines: Exo 2 bold white (33/27/23/22pt)
- Body: Poppins 13.5pt near-white
- Gold eyebrow accent: RGB (0.773, 0.616, 0.373)
- Page: 9144000 × 5143500 EMU
- Imagery: canonical N30 destination-cinematic composites, market-specific full-bleed backgrounds, navy scrim, minimal gold accents. No Atlas-generated images.

## Asset hosting (no inaccessible embeds)
- **Destination plates:** public Google Drive `uc?export=download&id=...` URLs (all resolve as image/png — verified).
- **Logos:** public `raw.githubusercontent.com` URLs (repo is public).
  - Navier wordmark: `assets/logos/navier/navier-wordmark-white.png` (committed this branch).
  - AirAsia MOVE consumer mark: `deck-studio/decks/airasia-move/logo-bank/logo-airasia-move.png`.
  - Note: the Navier logo Drive file is private (sign-in interstitial), so raw URL hosting was used instead of Drive `uc` for logos.

## 11-slide structure
1. Cover — Navier × AirAsia MOVE, Andaman plate
2. The opportunity / thesis
3. Footprint (Atlas map placeholder — **Jaideep adds screenshots**)
4. Launch markets
5. Use-cases / arriving-seat distribution
6. Vessel tiers
7. Economics — 6-rung ladder
8. How it works / integration
9. 3-phase rollout (Phase 1 TH+ID+MY, Phase 2 PH+SG)
10. Marquee corridors
11. The ask / close

## Economics (model-pass-complete)
6-rung ladder: floor ~$18M (10% cap) → SOM full network ~$87M → SAM $356M → Marine TAM $1.42B → Journey GMV $4.27B → Platform rev $192M.
Grounded→projected tags applied; no internal acronyms leaked into partner-facing copy (SOM/SAM/TAM/GMV shown with plain-English descriptors only).

## Open dependency
- **Atlas map screenshots** on slide 3 — Jaideep adds (Atlas behind HTTP basic auth; Tasklet cannot capture renders).

## Notes
- PP↔El Nido (rn-81f865bba3ac) stays Quanta-LR roadmap — out of floor.
- Full PDF QA passed across all 11 slides.
