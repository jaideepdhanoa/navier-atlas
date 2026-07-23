# GROK HANDOFF — DiDi Mexico +2 & inDrive Egypt +3 city expansion (2026-07-23)

**From:** Tasklet (research + sourcing complete)
**To:** Grok (economics rebuild + slide build)
**Owner of merge:** Jaideep

## Mandate
Add **five** new city deep-dives (+ one `WHAT ONE BOAT EARNS · {CITY}` unit-econ slide each) to two live decks. Tasklet has sourced the four required inputs per corridor and reconciled every corridor against sealed `data-clean/ROUTES.json`. Grok rebuilds economics and builds/places the slides deterministically.

- **DiDi Mexico** (`1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c`): **Puerto Vallarta**, **Los Cabos**
- **inDrive Egypt** (`1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk`): **Cairo / The Nile**, **El Gouna**, **Marsa Alam**

## Inputs in this package
- `CORRIDOR-EVIDENCE-2026-07-23.json` — the four-input sourcing evidence (route, distance, premium fare $/seat OW, demand anchor + demand basis + source URLs + confidence) per corridor.
- `GEOMETRY-STATUS-2026-07-23.json` — exact sealed route IDs / BP IDs per corridor; the one `NEEDS_MINT` flag.

## Four-input gate result (Jaideep's city-coverage rule)
A city earns a full slide (map + unit-econ P&L) only when all four are sourced for ≥1 corridor: (1) named pier-to-pier route, (2) distance (nm), (3) benchmarked premium fare ($/seat OW), (4) anchored demand.

| City | Route | nm (sealed) | Premium fare $/seat OW | Demand anchor | Geometry | Gate |
|---|---|---|---|---|---|---|
| Puerto Vallarta | PV → Yelapa `ics-89a8844858` | 14.5 | $25 | ~22,000 captive pax/yr (boat-only village; bottoms-up on scheduled Los Muertos–Yelapa co-op service) | SEALED | ✅ PASS |
| Los Cabos | Cabo San Lucas → San José del Cabo `rn-d206da44c580` | 13.8 | $30 | 3.86M Los Cabos visitors/yr; 257K Cabo marina cruise pax (2024) | SEALED | ✅ PASS |
| Cairo / The Nile | Zamalek ↔ Maadi `rn-c37df5916b71` | 6.26 | $20 | ~180,000 riders/yr (Nile Taxi operates this exact route today, 10 boats) | SEALED | ✅ PASS |
| El Gouna | Marina El Gouna ↔ Hurghada `rn-bb533d525e01` | 14.2 | $25 | >1M visitors/yr + 25,000 residents (Orascom resort town) | SEALED | ✅ PASS |
| Marsa Alam | Port Ghalib → Sha'ab Samadai | ~12.5 | $30 | ~1.09M airport pax/yr; Samadai managed reef-excursion program | **NEEDS_MINT** | ⚠️ HOLD until reef jetty minted |

**Marsa Alam:** all four data inputs are sourced, but the Samadai reef jetty is absent from the graph. **Mint the Port Ghalib → Sha'ab Samadai corridor first** (or bind an alternate Marsa Alam signature route), then it clears the gate. Until minted, hold the Marsa Alam economics/slide — fail closed, do not borrow another route.

## Economics rebuild (per partner-model-cascade)
Fares are **premium-substitute benchmarked** (Uber Black equivalent), **MID** scenario, Voi multiplicative revenue structure — consistent with confirmed anchors ($30 Playa–Cozumel, $20 Huatulco, $12 Holbox).

- **Census — per-partner-country (Jaideep 2026-07-21):** Mexico corridors use `finance/recal/greenfield-census/didi-mexico.json`; Egypt corridors use `finance/recal/greenfield-census/indrive-egypt.json`. Never cross a country census.
- **FX (locked):** MXN ≈ 17.50; EGP sell 51.1728.
- **Add corridors** to the scoped `finance/recal/corridors-didi-mexico.json` / `corridors-indrive-egypt.json` (PV→Yelapa and Cabo→San José already exist with **null economics** — fill demand/fare from the evidence file; Cairo/El Gouna corridors exist in ROUTES.json and need finance rows; Marsa Alam after mint).
- **Cascade:** `aggregate.py → growth.py → growth_frontend_block.py → splice_growth_into_partner.py → build_transparent_sheet.py` per partner. Use each market's local per-partner-country census in the transparent sheet (fix at `finance/build_transparent_sheet.py`).
- **Country-reference fail-closed gate (§B.0):** every new corridor's country (Mexico, Egypt) must resolve a complete `country-reference.json` row (both already exist for the current cities — reuse). Hold any corridor whose row is incomplete.
- **Refresh TAM ladders** on **SOM Full Mapped Network** (not floor). DiDi Mexico keeps the journey-GMV rung **and** the 6th platform-take rung (18%). inDrive Egypt stops at Journey GMV (no platform rung).
- **Update the Drive financial-model sheets in place** (preserve URLs): DiDi Mexico `1AtoSyNtAZtYiW-duU0oxZTgdtpWW4Al3xuUAHnqlFg0`; inDrive Egypt workbook per `finance/COUNTRY-SHEET-IDS.json`.
- **Two-engine agreement (golden rule #7):** partner JSON and transparent sheet must tell the same greenfield/opex/CAPEX story.

## Slide build (per partner-deck-grok-handoff — LOCKED country spine)
Duplicate the existing city deep-dive + econ chassis in each deck; substitute only source-backed fields. **Slides API only; no PPTX; no wholesale replacement.**

Per new city, add **two** slides after the existing marquee cities (main deck stays lean; these can sit in the deep-dive block):
1. **City deep-dive** — marquee route(s) in the canonical route-list box format (amber `▸`, white-bold `{From} → {To}`, white-normal `~XX nm · plain-English description`, blank line between routes, **no vessel names**), plus the text-free Atlas map plate (human-inserted slot / banked plate — never generate a map).
2. **`WHAT ONE BOAT EARNS · {CITY}`** — MID unit-econ, six flush OPEX lines (Energy · Captain/crew · Marina+overhead · Maintenance · Insurance · Charging berth · Total), premium-fare revenue build.

Also update, per deck:
- **Market-overview slide (S4)** — must cover **all** cities now in scope (add the new cities to the roster/KPIs).
- **Slide-2 deal quadrant** — name the new cities in the "what's in scope" quadrant.
- **THE PRIZE / TAM slide** — refreshed ladder values from the cascade.
- **Map plates** — render text-free CartoDB Dark Matter exact-route plates for the 5 new corridors (renderer: `scripts/grok-egypt/render_mx_eg_exact_route_maps_2026_07_23.py`), bank under `deck-studio/assets/{didi/city-maps,indrive-egypt/city-maps}/`, register in `ASSET-REGISTRY.json`.

## Gates (blocking)
- `python3 scripts/audit_partner_copy.py` must PASS on both partner JSONs.
- `python3 deck-studio/qa/partner_copy_lint.py <deck>` must be green before apply — zero internal taxonomy in rendered slide text (plain partner English).
- Vessel gate: all 5 corridors are ≤70nm → **N30 (8 pax)**. Never other capacity figures.
- Shared-basis note: these two decks do **not** share a canonical basis with each other, so no cross-cascade between them (Brazil is the shared-basis pair, not MX/EG).

## Fail-closed / holds
- **Marsa Alam** — HOLD economics + slide until the Port Ghalib → Sha'ab Samadai reef corridor is minted.
- Fares for the Egypt corridors are Tasklet-**sourced/recommended** premium-substitute benchmarks (not yet Jaideep-approved like the MX/Brazil anchors). Flag for Jaideep confirmation on merge.

## Acceptance receipt (return to #tasklet-jaideep)
Deck IDs, slide counts before→after, per-corridor economics (cost/margin/payback/fleet, MID), refreshed TAM ladders, map-plate provenance ledger, copy-lint green, and the Marsa Alam mint result (minted route ID or still-held).
