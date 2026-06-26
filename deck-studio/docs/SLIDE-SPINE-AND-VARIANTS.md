# Deck Slide Spine & Variants — anti-drift manifest

**Purpose.** One canonical slide-by-slide spine per template so a build can never *miss a slide or
an image*. A deck is render-complete only when **every spine slot is present** and **every variant
slot is filled or explicitly null** (null beats confidently-wrong). The generic builder and QA gate
read this file as the checklist; per-deck specifics live in `decks/{deck}/economics-binding.json`
and `ASSET-REGISTRY.json`.

Two slot classes:
- **SPINE** — identical structure/copy across every deck of that template (product, experience,
  problem, appendix divider…). Built once from the gold; partner edits are cosmetic only.
- **VARIANT** — partner/market-specific content and imagery (cover logo, clusters, corridors,
  econ backgrounds). Must be resolved from the partner's sidecar + asset pack; never inherited
  from the gold's market.

A VARIANT slide that ships with the **gold's** market content or imagery is a **drift defect**
(this is the class of bug that left UAE econ backgrounds on the Centara appendix — see LB-262).

---

## Template A — Hospitality (operator-developer), 24 slides
Gold: Minor Hotels `1p5Ntoa…`. Clone-then-edit target example: Centara `1ekpZzZI…`.

| # | Slide | Class | Image role | Economics / data |
|---|---|---|---|---|
| 1 | Cover — "Own the arrival. Own the margin." | **VARIANT** | `cover_hero` (market) + Navier white logo + **partner logo (required)** | — |
| 2 | Executive summary — "Your world, today" | **VARIANT** | `value_prop_bg` — **own distinct image, KPI-FREE**, do NOT borrow the operator-value background | no KPIs |
| 3 | The Problem — "the last mile breaks the spell" | SPINE | problem scene | — |
| 4 | Introducing the N30 | SPINE | N30 product | — |
| 5 | The passenger experience — "Silent. Smooth. Seamless." | SPINE | experience | — |
| 6 | How it works — "Three ways to deploy" | SPINE | operator value (**Cost · Convenience · Comfort** framing) | — |
| 7 | Confidence — "Proven, and trusted" | SPINE | proof | — |
| 8 | Your footprint — "N clusters, ready to connect" | **VARIANT** | footprint/map | cluster count + names |
| 9–14 | Cluster 01–06 deep-dives | **VARIANT** | `cluster_hero` ×6 — **market-specific N30 dusk composite per cluster** | per-cluster narrative |
| 15 | The partnership — "What we bring together" | SPINE (light tailor) | partnership | — |
| 16 | Closing — "Own the arrival. Own the margin." | **VARIANT** | partner logo (white) | — |
| 17 | Appendix divider — "Unit economics, per corridor" | SPINE | — | — |
| 18–24 | Appendix unit-economics cards (7) | **VARIANT** | `econ_market_bg` ×7 — **PAGE-FILL, market-specific, vertical scrim** (LB-262) | per-corridor card from sidecar |

**Hospitality economics rules (do not drift):**
- **$1M / vessel** frame; operator framing **Cost · Convenience · Comfort** (never "Captive · Calm · Clean").
- **NO SOM/SAM/TAM/GMV ladder.** The marquee unit-economics live in the appendix (18–24), one per cluster.
- Appendix card = eyebrow · corridor title · distance line · equation banner (gold "kept") · three value
  columns (gold result line; "kept" gold @15pt; right-aligned) · **CO₂ avoided / yr** (`co2_avoided_tonnes_year`).
- Appendix backgrounds are **page-fills** (`updatePageProperties.pageBackgroundFill.stretchedPictureFill`),
  **never** `navierBg_*` image elements.
- Slide 2 is **KPI-free** with its **own** image — never the operator-value (Three C's) plate.

## Template B — Mobility (super-app), Grab gold lineage
Gold: Grab `…`. See `IMAGE-ROLE-CONTRACT.md` for the canonical image families. Summary:

| Slides | Class | Image role |
|---|---|---|
| 1 | VARIANT | `cover_hero` + Navier + partner logo |
| 2 | VARIANT | `value_prop_bg` (own market image, woman-booking brief) |
| 3 | SPINE | Three C's operator-value background (canonical, keep as-is) |
| 4–6, 14–18 | VARIANT | `atlas_route_screenshot` (**human capture**, not generated) |
| 7–9, 19–23 | VARIANT | `econ_market_bg` (full-bleed landmark, `navierBg_*` **elements**) |
| 10 | SPINE/VARIANT | `tam_bg` + **SOM/SAM/TAM/GMV ladder** (mobility only) |
| 11 | SPINE | `partner_roles_bg` |

**Key cross-template differences (the drift traps):**
1. Mobility econ backgrounds are **`navierBg_*` elements**; hospitality econ backgrounds are **page-fills**.
2. Mobility has a **TAM ladder (slide 10)**; hospitality has **none** (appendix marquee instead).
3. Mobility market side-panels (4–6/14–18) use **human Atlas screenshots**; hospitality cluster slides
   (9–14) use **generated N30 cluster composites**.
4. Mobility slide-3 is the Three C's background (kept); hospitality slide-2 needs its **own** image.

---

## Render-complete gate (both templates)
A deck passes only when, for every row above:
- SPINE slides present and unmodified in structure;
- every VARIANT image slot resolves to an `ASSET-REGISTRY.json` `image_key` with a **stable URL**
  (no embedded-only, no temporary `googleusercontent` contentUrl) **or** is explicitly `null`/`needs_generation`;
- no VARIANT slide carries the **gold deck's** market content or imagery;
- `deck_type` matches the template (hospitality ⇒ no ladder, page-fill econ backgrounds, $1M/vessel, Cost·Convenience·Comfort).
