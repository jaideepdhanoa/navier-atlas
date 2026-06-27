# Gojek × Navier — Indonesia deck · BUILD-LOG

**Deck (live):** https://docs.google.com/presentation/d/13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs/edit
**Status:** ✅ 14 / 14 slides complete and verified.
**Method:** Duplicate of the live Grab Thailand deck, then **edited in place via the Slides API**. No full-replace, no PPTX round-trip. Imagery and the gold/navy visual system inherited from the Grab gold deck and preserved throughout.

## What was edited this round (Tasklet lane)

### Slides 8–10 — "What one boat earns" (unit economics)
Filled the three marquee unit-economics tables, replacing the inherited Thailand/Phuket placeholders with Indonesia-grounded numbers. Source: `data-clean/economics_by_route_id.json` (market-tagged, physics-grounded, partner-agnostic records). Each table's lines tie internally (revenue = seats × fare × legs; opex sums; EBITDA; payback = capex ÷ EBITDA). Run-cost basis is the sealed model stack (crew $21.6k, marina $10k, maintenance $10k, insurance $15k, charging $18k, $600k capex, 274 operating days). Full breakdowns captured in `ECONOMICS-SIDECAR.json`.

| slide | cluster | marquee corridor | route_id | rev/boat/yr | margin | payback |
|---|---|---|---|---|---|---|
| 8 | Bali | Benoa → Six Senses Uluwatu | `rn-c256a044c8be` | $865,810 | 91% | 0.76 yr |
| 9 | Singapore | ONE°15 Sentosa Cove → Harbour Bay | `rn-76264638fa6b` | $430,980 | 82% | 1.7 yr |
| 10 | Riau ↔ Singapore | Riau Islands → ONE°15 Sentosa | `rn-2568d40ee060` | $391,820 | 80% | 1.9 yr |

> Slide 10 marquee was switched from Jakarta's own intra-city water economics (honest but weak — ~14-yr payback) to the **Riau ↔ Singapore cross-border** corridor, a flagship-strength example that still sits inside the deck's footprint. Decision: Jaideep, 2026-06-27.

Style preservation verified on the live deck after a delete+insert edit (title gold Exo2, headline white 22pt, corridor sand Poppins, summary centered, value cells END-aligned) — runs retain color/font/weight/alignment.

### Slide 1 (cover) — partner logo
Swapped the inherited Grab mark for the **Gojek white wordmark** in the top-right partner-logo slot (`p1_i5`), re-fit to the wordmark's 4.2:1 aspect, anchored top-right opposite the Navier wordmark. Rendered cover logo verified byte-identical to the banked asset. Logo provenance + banking: `assets/logos/partners/gojek/LOGO-SOURCE.json`.

## Held / null (honest)
- 20 shared/unbound corridors on the partner page carry `-shared` or `null` `route_id` — left null for Grok seal-bind (not invented).
- No model derivation performed here; economics are deck-application of already-sealed per-corridor records.

## Provenance
- Partner page: `partner-pitch/partners/gojek.json` (27 → 60 journeys; existing journeys byte-for-byte intact; route_id discipline clean; archetype chips plain English).
- Economics sidecar: `decks/gojek-indonesia/ECONOMICS-SIDECAR.json`.
- Logo: `assets/logos/partners/gojek/logo-gojek.png` + `LOGO-SOURCE.json`.
