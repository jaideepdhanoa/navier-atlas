# Hospitality deck builder — GOLD spec (for Grok deterministic build)

Canonical, deterministic recipe for an operator-developer (hotel/resort) partner deck. Gold reference: **Minor Hotels × Navier v2** (24-slide live deck, Jaideep-edited 2026-06-25). This is the input contract any future Grok build reads — the corrected data lives in the JSON sources below, so a rebuild reproduces the gold without re-deriving anything.

**Live gold deck:** https://docs.google.com/presentation/d/1p5NtoaORRWyBpcsbfqnSB9PLg9yyTpvuzJAyBMjen4o/edit
**Build the unit-econ slides via Slides API in place** — no full-replace, no PPTX round-trip. The deck was directly edited; do not rebuild it from scratch — read the fixed inputs and apply deltas only.

## Slide taxonomy — spine vs partner vs market

Three classes. SPINE = reusable verbatim (product/Navier copy). PARTNER = copy + data swap per operator. MARKET = one per cluster/corridor, each needs its own market-specific N30 image.

| # | Slide | Class | Image | Per-partner change |
|---|---|---|---|---|
| 1 | Cover "Own the arrival. Own the margin." | PARTNER | `{partner}-cover-n30.png` | partner logo co-brand + wordmark |
| 2 | Exec "Your world, today" | PARTNER | **own distinct** `{partner}-exec-n30.png` | operator world; **KPI-FREE**; never reuse another slide's bg |
| 3 | Problem "The last mile breaks the spell" | SPINE | interior N30 | — |
| 4 | Introducing the N30 Pioneer | SPINE | N30 intro hero | — |
| 5 | Passenger experience "Silent. Smooth. Seamless." | SPINE | N30/market hero | — |
| 6 | "Three ways to deploy" | SPINE | N30 scenery | — |
| 7 | Confidence "Proven, and trusted" | PARTNER | proof plate | partner precedents |
| 8 | Footprint "N clusters, ready to connect" | PARTNER | footprint aerial | cluster count + map |
| 9–14 | Cluster 01–06 (one per market) | MARKET | `{partner}-{market}-n30.png` | per-market properties + plate |
| 15 | Partnership "What we bring together" | PARTNER | together plate | partner value exchange |
| 16 | Close "Own the arrival. Own the margin." | SPINE | cover hero | — |
| 17 | Appendix divider "Unit economics, per corridor" | SPINE | appendix plate | — |
| 18–24 | Unit-econ, one marquee corridor per grounded cluster | MARKET | `econ-bg-{market}-n30.jpg` (scrimmed) | corridor economics + market bg |

**Optional spine** (trimmed from the Minor gold; add only if earned): standalone **Cost · Convenience · Comfort** value slide; specs "Built for the resort transfer"; precedents "This is already real."

## Narrative rule
Value-prop framing is **Cost · Convenience · Comfort**. ⛔ Never "Captive · Calm · Clean." Plain English only; no internal model/finance taxonomy in any rendered text. SOM/SAM/TAM/GMV may appear only as labels with plain-English descriptors — but hospitality decks carry **no ladder**.

## Economics rule
- $1M/vessel CAPEX (LB-260, `capex_tier: "hospitality"`). No SOM/SAM/TAM/GMV ladder — one **marquee-corridor unit-econ card per cluster at the end** instead.
- Numbers come from the grounded engine `econ_engine.py` (validated to the dollar), never typed by hand.
- **Realism basis (LB-261):** captive short transfers run at 50–60% load / 50–60% revenue legs and distance-scaled fares (a 10-min hop is not $150 at 70% full). Premium fares only on genuine 2+ hour crossings. Encoded as per-corridor `_realism_override` in the **scoped** view (`minor-hotels-realism.override.json`) and honored by `aggregate.py:run_scenarios`. Never edit the shared durable markets (other partners inherit them — LB-260).

## Unit-econ slide format (matches mobility gold)
3 columns on a scrimmed market N30 background:
1. **Revenue build:** seats/transfer (`8 × load%`), paid transfers/day, op-days/yr, revenue legs, paid seats/yr, fare/seat, **revenue/vessel·yr**.
2. **Annual run cost (6 flush OPEX lines):** Energy · Captain & crew · Marina & overhead · Maintenance · Insurance · Shore power & berth · **Total**.
3. **The result:** kept/vessel·yr, operating margin, vessel investment ($1.0M), paid back in, CO₂ avoided/yr.
Equation band on top; footnote: "Every line ties to Navier's corridor model … No blended averages." Background scrim = vertical `rgba(0,0,0,0.42)→rgba(0,0,0,0.86)`.

## Gold economics (Minor, realism-rebased 2026-06-25)
Source: `finance/model/minor-hotels-econ-gold-2026-06-25.json`.

| Corridor | nm | fare | load/legs | rev/vessel | kept | margin | payback |
|---|---|---|---|---|---|---|---|
| Anantara Palm → Bluewaters | 5.0 | $50 | 60/60 | $591,840 | $453,133 | 77% | 2.2y |
| Sir Bani Yas → Jebel Dhanna | 7.9 | $50 | 60/60 | $512,880 | $373,543 | 73% | 2.7y |
| Mina Al Arab → Anantara Palm | 46.5 | $150 | 50/50 | $328,800 | $188,273 | 57% | 5.3y |
| Anantara Palm → Yas Marina | 49.6 | $150 | 50/50 | $328,800 | $188,038 | 57% | 5.3y |
| Dharavandhoo → Anantara Kihavah | 11.8 | $100 | 50/50 | $602,800 | $447,318 | 74% | 2.2y |
| Ao Po → Anantara Layan | 9.6 | $85 | 50/50 | $558,960 | $457,779 | 82% | 2.2y |
| Avani Seminyak ↔ Anantara Uluwatu | 9.3 | $85 | 50/50 | $558,960 | $482,617 | 86% | 2.1y |

## Image map & hosting
Repo assets: `decks/minor-hotels-v2/assets/`, served raw-GitHub. Cluster plates `minor-{market}-n30.png`; econ backgrounds `econ-bg-{market}-n30.jpg` (UAE/Maldives/Thailand/Bali present). No Atlas-generated images; minimal gold accents; no inaccessible embeds.

## Cascade after any economics change
Run §B of the `partner-model-cascade` skill for the partner (aggregate → growth → frontend → splice → transparent sheet → master tracker) so agg/sheet reproduce the deck-gold. Include the economics sidecar in the gold export. Do **not** rebuild the directly-edited deck.
