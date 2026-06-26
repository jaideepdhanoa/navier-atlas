# Deck archetype: hotel/resort operator-developer (HOSPITALITY GOLD)

Reusable deck structure + narrative for partners that are **hotel developers/operators**, not mobility/ride-hail/super-app distributors. Gold reference instance: **Minor Hotels × Navier v2** (24-slide live deck, Jaideep-edited 2026-06-25). Reuse for **Aman, Four Seasons, Constance, Six Senses, Banyan Tree**, and similar portfolio operators.

Use this variant **in addition to** the base playbook in `SKILL.md` (Slides-API-only, image discipline, N30/N35 compositing, partner-logo-on-cover, 6-line OPEX rule, validation gate, reporting language all still apply). This file overrides **deck structure, the route rule, the economics frame, the unit-economics slide format, and the narrative**.

**Gold artifacts (source of truth — read before building):**
- Live gold deck: `https://docs.google.com/presentation/d/1p5NtoaORRWyBpcsbfqnSB9PLg9yyTpvuzJAyBMjen4o/edit`
- Deck spec + builder: `agent/home/hospitality-template-2026-06-25/deck_spec_minor.json`, `build_deck.py`, `build_econ_v2.py`
- Grounded econ engine (reproduces unit-econ to the dollar): `agent/home/hospitality-template-2026-06-25/econ_engine.py`
- Gold economics + realism override: `decks/minor-hotels-v2/HOSPITALITY-DECK-GOLD.md`, `finance/model/minor-hotels-econ-gold-2026-06-25.json`, `minor-hotels-realism.override.json`

## When to use this archetype

Pick the operator-developer variant when **all** hold:
- the named partner **owns/operates physical destinations** (hotels, resorts, branded residences), and
- the value to Navier is **captive guest throughput at those properties**, not city-wide consumer mobility, and
- headroom comes from the partner **opening more properties** (keys/clusters/pipeline), not from winning a larger share of an open mobility market.

If the partner is a mobility/super-app/ride-hail distributor (Grab, Bolt, Careem, Yango), use the **base** standard sequence in `SKILL.md`, not this variant.

## Governing route rule (hardest eval gate)

Routes exist **only inside the partner's own property graph**. Three captive route classes only:
- **(A) gateway → property** (airport/city gateway ↔ a partner hotel)
- **(B) property ↔ property** (intra-portfolio, same operator)
- **(C) property → signature excursion** (operator-owned/partnered destination experience)

Any leg with **no partner-owned endpoint is forbidden**. Carry it into the Grok seal prompt as a numeric eval — **archetype purity: 0 non-partner-endpoint routes** (Minor's `G1`).

## The 24-slide hospitality gold spine

The gold deck is **24 slides** in three editorial blocks. Classify every slide as **SPINE** (reusable verbatim — product/Navier copy), **PARTNER** (copy + data swap per operator), or **MARKET** (one per cluster/corridor, needs a market-specific N30 image).

| # | Slide | Class | What changes per partner |
|---|---|---|---|
| 1 | Cover — "Own the arrival. Own the margin." | **PARTNER** | partner wordmark + logo co-brand, market-anchored N30 cover hero |
| 2 | Executive summary — "Your world, today" | **PARTNER** | the operator's own world; **KPI-FREE**; its **own distinct image/prompt** (never borrow another slide's background) |
| 3 | The problem — "The last mile breaks the spell" | SPINE | — (interior N30) |
| 4 | Introducing the N30 Pioneer | SPINE | — (N30 intro hero) |
| 5 | The passenger experience — "Silent. Smooth. Seamless." | SPINE | — (N30 / market hero) |
| 6 | How it works — "Three ways to deploy" | SPINE | — |
| 7 | Confidence — "Proven, and trusted" | **PARTNER** | partner-relevant precedents/proof |
| 8 | Your footprint — "N clusters, ready to connect" | **PARTNER** | partner cluster count + footprint map |
| 9–14 | Cluster 01–06 (one per market) | **MARKET** | one slide per market; market-specific N30 composite + that market's partner properties |
| 15 | The partnership — "What we bring together" | **PARTNER** | partner-specific value exchange |
| 16 | Close — "Own the arrival. Own the margin." | SPINE | — |
| 17 | Appendix divider — "Unit economics, per corridor" | SPINE | — |
| 18–24 | Unit-economics, one marquee corridor per grounded cluster | **MARKET** | corridor-specific grounded economics + market-specific N30 background |

**Optional spine slides** (canonical, but Jaideep trimmed them from the Minor gold — include only when they earn their place): a standalone value-prop slide (**Cost · Convenience · Comfort**, see narrative), a specs slide ("Built for the resort transfer"), and a precedents slide ("This is already real"). Trimming is an editorial choice; never pad.

## Narrative / USP framing — Cost · Convenience · Comfort

Hospitality decks use the operator framing **Cost · Convenience · Comfort** (Jaideep, locked). This is the value-prop language wherever a value slide, exec summary, or proof strip needs operator props.

> ⛔ **Do NOT use "Captive · Calm · Clean(· Continuity)."** That earlier set is retired for hospitality decks. Do not switch Minor or any other hospitality deck to it.

- **Cost** — premium transfer revenue the operator keeps, on a low fixed-cost electric hull; honest unit economics, no blended averages.
- **Convenience** — wake-free, on-demand arrival inside the operator's own graph (gateway → property → excursion).
- **Comfort** — silent, smooth, first-class guest experience that extends the brand to the water.

Keep all partner-facing copy in **plain English**. No internal model/finance taxonomy (grounded floor, WIDTH, captive band, route ids, downweights) in any title, subtitle, caption, or label. The only recognized labels that may stay visible are **SOM / SAM / TAM / GMV**, each with a plain-English descriptor alongside — **but hospitality decks do NOT use a SOM/SAM/TAM/GMV ladder at all** (see economics frame).

## Economics frame (captive, throughput-bounded)

- **Capture is high and bounded** (captive resort throughput, not a contested mobility market). Inherits **LB-254** (no 9× ladder inflation).
- **Headroom = WIDTH** (more keys / openings / clusters / pipeline) — never a rising share of an open market.
- **CAPEX = $1M / vessel** (LB-260, N30 luxury hull list price; region-independent; `capex_tier: "hospitality"`). Never the mobility region-keyed $600K/$900K.
- **No SOM/SAM/TAM/GMV ladder.** Replace the ladder with **one marquee-corridor unit-economics example per cluster, placed at the end** (appendix), as backup. The body of the deck stays geography + experience; the dollars live in the appendix.

### Unit-economics slide format (the gold upgrade)

Each appendix unit-econ slide (one per grounded marquee corridor) matches the **mobility unit-economics gold**: a 3-column build on a **market-specific N30 background** with a legibility scrim. Object/layout recipe is in `build_econ_v2.py`; numbers come from the grounded `econ_engine.py` (validated to the dollar — never typed by hand).

- **Equation band** (top): `$X revenue − $Y to run = $Z kept per vessel each year` (the "kept" figure in gold).
- **Column 1 — Revenue build:** Seats per transfer (`8 × load% = n`) · Paid transfers/day · Operating days/yr · Revenue legs · Paid seats/yr · Fare per seat · **Revenue / vessel·yr** (gold total).
- **Column 2 — Annual run cost (6 flush OPEX lines):** Energy · Captain & crew · Marina & overhead · Maintenance · **Insurance** · **Shore power & berth** · **Total run cost/yr** (gold). Insurance + berth flush-left, never indented (base-playbook 6-line OPEX rule).
- **Column 3 — The result, per vessel·year:** Kept per vessel·yr (gold) · Operating margin · Vessel investment ($1.0M) · Vessel paid back in · CO₂ avoided/yr.
- **Footnote:** "Every line ties to Navier's corridor model — real route distance, conservative load, and the $1M N30 vessel. No blended averages."
- **Background:** market N30 composite → `econ-bg-{market}-n30.jpg` (scrim = vertical `rgba(0,0,0,0.42)`→`rgba(0,0,0,0.86)`, top→bottom). Hosted at the stable raw-GitHub assets path; bound via `updatePageProperties.stretchedPictureFill.contentUrl`. If a market has no N30 composite, **commission one** (canonical N30 on a market-specific background) rather than leaving navy or borrowing a wrong-market plate.

### Realism basis (LB-261)

Captive resort transfers run at a **lower, honest basis than the global scenario band** — a 10-minute hotel transfer cannot run 70% full all day on 75% revenue legs, nor command a long-crossing fare. Use defensible, distance-scaled fares and **50–60% load / 50–60% revenue legs** for short captive transfers; retain premium fares only on genuine 2+ hour crossings. These are encoded as per-corridor `_realism_override` (load/revenue-leg/trips) in the Minor-scoped view and honored by `aggregate.py:run_scenarios` (additive, default-off). **Do not** write realism overrides into the shared durable markets — they are inherited by other partners (LB-260: tag the scoped view, not the shared market).

## Image rules (hospitality specifics on top of base)

- Canonical **N30 compositing**, **market-specific backgrounds**, **minimal gold accents**, **no Atlas-generated images**, stable raw-GitHub hosting, no inaccessible embeds, **no full-replace / PPTX round-trip** on the live deck.
- **Slide 2 (exec) gets its own distinct image** — never the value-prop / Three C's background.
- Cluster slides + unit-econ slides each carry their own **market** N30 plate.
- Partner logo on cover required where supported; null/no-logo (Navier-only cover) for unsupported territory rather than guessing.

## Validation-gate additions (on top of the base gate)

Before reporting deck-prep complete for an operator-developer partner, also confirm:
- the seal prompt carries the **archetype-purity numeric gate** (0 non-partner-endpoint routes);
- the value-prop framing is **Cost · Convenience · Comfort**, never Captive·Calm·Clean;
- slide 2 is **KPI-free** with its **own** image;
- there is **no SOM/SAM/TAM/GMV ladder** — economics are appendix marquee-corridor cards, one per cluster;
- CAPEX is **$1M/vessel**; unit-econ numbers come from the grounded engine (reproduced to the dollar), with **6 flush OPEX lines** and a market N30 background;
- realism overrides live in the **scoped** view, not the shared markets;
- single-property markets with no corridor partner are **logged as explicit holds**, never seeded.
