# Hospitality Deck Builder Rules — Minor Gold Baseline

Gold baseline: the live Minor Hotels × Navier deck (`1p5NtoaORRWyBpcsbfqnSB9PLg9yyTpvuzJAyBMjen4o`) is the hospitality deck reference. Do not substitute the mobility/super-app 11-slide sequence.

## Locked deck spine

Use the 24-slide hospitality spine unless a user explicitly asks for a shorter deck:

1. Cover — partner × Navier.
2. Executive thesis — partner-specific, KPI-free, distinct image.
3. Hospitality problem.
4. Navier / N30 answer.
5. Passenger experience / guest journeys.
6. Deployment/value frame using **Cost · Convenience · Comfort**.
7. Proof / confidence.
8. Partner footprint / clusters.
9–14. Six geography or property-cluster slides.
15. Partnership model.
16. Close / phased action.
17. Appendix divider — unit economics.
18–24. Unit-economics appendix using the Minor gold card layout.

## Hospitality rules

- Use **$1M/vessel economics** for hospitality decks.
- Use **Cost · Convenience · Comfort**. Do not use `Captive · Calm · Clean`.
- Do **not** use a SOM/SAM/TAM/GMV ladder in hospitality decks.
- Keep slide 2 KPI-free and give it its own image/prompt; never reuse the Three C’s/value-prop background.
- Keep partner-facing text in plain English. Do not show model/internal words such as `grounded`, `network width`, `route seal`, `capture`, `captive resort mesh`, or `amber-dashed`.
- All unit-economics slides use: Revenue build · Annual run cost · The result, per vessel/year.
- Annual run cost labels must be six flush lines: Energy · Captain & crew · Marina & overhead · Maintenance · Insurance · Shore power & berth.

## Geography and routing rules

Routes should live inside the operator’s property/demand graph:

- gateway → property
- property ↔ property
- property → signature excursion

Any route without a partner-owned endpoint or named partner demand anchor is held/null.

### Urban feeder exception

For an operator with city hotels that are explicitly in scope — e.g., Centara including Bangkok — the deck may include a **hotel-curated city-to-water gateway** even if the water leg uses public/private third-party piers. The partner property must be the demand anchor; the copy must say `hotel-curated river gateway` or similar, not public transit or coastal resort. Pier rights, dock rights, exact endpoints, route IDs, and sealed distances stay null until validated.

## Appendix count rule

The live Minor gold deck has six cluster slides and seven unit-economics appendix slides. For a six-cluster hospitality deck:

- Default to one marquee economics card per grounded cluster.
- If a seventh appendix slot is needed to preserve the gold spine, it may only show a genuinely different operating pattern within an existing cluster.
- Do not invent a seventh cluster.
- Do not pad with a weak route.
- If only six grounded corridors exist, leave slide 24 held/null until a real route earns it.

## Centara-specific application

Centara Thailand uses exactly six clusters:

1. Bangkok river gateway
2. Western Gulf — Hua Hin / Cha-Am
3. Eastern Gulf — Pattaya / Jomtien / Sriracha / Koh Chang
4. Phuket / Andaman north
5. Krabi / Phi Phi
6. Samui / Gulf islands

The seventh economics appendix slot, if used, should split Eastern Gulf into two distinct operating patterns: Pattaya/Koh Larn mainland excursion and Trat/Koh Chang island arrival. This is not a seventh cluster.

## Grok handback requirement

For hospitality deck-builder or partner-page changes, return:

- branch name
- PR link
- commit SHA
- exact files changed
- validation receipt
- explicit nulls/held items
- confirmation that any live Google Slides edits used Slides API only and did not full-replace or round-trip via PPTX
