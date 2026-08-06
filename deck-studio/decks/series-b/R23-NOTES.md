# R23 — Jaideep Aug-6 review fixes (2026-08-06)

Deck: `1g95_1hKvlz8Pfar-fmhoUsONcJyu6-zPPfhvRhPxu4k` · 41 slides (Jaideep inserted new slide 2 + reordered; see SLIDE-MAP-R23.md)

## What changed
1. **Slide 2 rebuilt natively** (`g3f673ef3b6b_2_0`) — was a pasted screenshot. Now house template: cloned title style/geometry from slide 3 (Exo 2 w600, 17pt raw in scaled box), gold underline, `01 · THESIS & TEAM` tracker, © footer, AV logo, dark house field. Chart built from native elements: axis lines, flat gold 20-knot line (1956→2026), labels, gold kick caption "Ships got bigger. They never got faster."
2. **Slide 3 full-bleed** (`st_r19_claim`) — right photo plate deleted (`r22plate_s2`); Maldives-network bg image scaled uniformly to full width (scale 289.37, vertical center-crop); semi-transparent house panel (`r23panel_s3`, alpha 0.68) added behind body text for legibility; z-order panel→back, bg→back.
3. **Slide 21 (cargo gap)** — featured numbers are now the per-kg prices: AIR **$2.50–4.50 /kg** · OCEAN **$0.03–0.50 /kg** (24pt gold + 13pt suffix so they don't wrap). The $8T/$7T goods-value figures REMOVED — side by side they misread as "air carries more than ocean." Air's scale claim kept as context line: "35% of world trade value on under 1% of its tonnage." Sources line reordered (Freightos first).
4. **Slide 22 (islands)** — card 3 was global air-cargo revenue with no label, and nothing evidenced "slowest."
   - Card 2: "$5,563/TEU — what small islands paid per container in H1 2024 — highest freight rates of any country grouping, after a 137% spike" (UNCTAD 2024).
   - Card 3 NEW: "**70% longer** — the wait for a berth in developing-economy ports — 10.9 hours vs 6.4 in developed ones" (UNCTAD RMT 2025, ch. 4: waiting times climbed to 6.4h developed / 10.9h developing, Dec 2023–Mar 2024). This carries the "slowest" claim in the title.
   - $141–157B moved to the band, explicitly labeled "(IATA, global)": premium the world already pays to escape slow ocean freight.
5. **Slide 41 tracker retag** — graveyard slide now sits after appendix (Jaideep reorder) but wore `01 · THESIS & TEAM`; retagged `APPENDIX · WHY PRIOR ATTEMPTS FAILED` in appendix tracker style.

## Sourcing added this round
- UNCTAD Review of Maritime Transport 2025 ch.4: port waiting times 6.4h (developed) vs 10.9h (developing) → "70% longer" card. https://unctad.org/publication/review-maritime-transport-2025

## Gotchas for future rounds
- `createImage` fails on stale lh7 googleusercontent URLs — always fetch a fresh `contentUrl` from a live reference element in the same run (logo ref: `g3f645480738_0_200` on slide `g3f645480738_0_196`).
- Google batchUpdate is atomic: a failed request means nothing in the batch landed; safe to re-run.
- Connector `google_slides_get_presentation` mode:"full" exceeds the tool output cap on this deck — fetch mode:"slides" in chunks of ≤6 indices.
- House title chrome to clone: title box size 3M×3M EMU, transform scale 2.5/0.0872 @ (576075, 457200); gold underline scaleX 0.6672 @ (578425, 868680).
