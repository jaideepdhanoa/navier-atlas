# GROK SPEC — inDrive Egypt TAM-ladder correction (2026-07-14)

**Owner split:** Tasklet has done the sourcing (this spec + `EGYPT-MARINE-TAM-LADDER-2026-07-14.json`). Grok owns the deterministic `growth_case` bind / cascade.

## Problem
The prior Egypt view presented **~$8.5M** as the Egypt TAM. That figure is the **journey-GMV pool of the two sealed captive corridors only** (Giftun + Ras Mohammed) — i.e. the grounded floor. Presenting it as the market TAM drastically **undercounts** the addressable Egypt marine-mobility opportunity, and the previous "~$8.5M is far below Egypt's tourism economy, so no inflation" note used backwards logic (being below the economy is the *symptom* of a floor, not proof of a correct TAM).

## Fix — bind a three-rung ladder from the sidecar
Source of numbers: `EGYPT-MARINE-TAM-LADDER-2026-07-14.json` (this handoff dir). Cascade into the inDrive `growth_case` Egypt contribution with the same shape as Grab/Bolt (`revenue_potential` {floor/full/SAM}, `journey_gmv`, `marine_mobility_tam`, `ladder_transitions`).

| Rung | Internal | Value | Basis |
|---|---|---|---|
| 1 | SOM grounded floor | **$8.50M pool / $7.65M Navier rev** | 2 sealed captive routes, sourced visitor pools × observed fares, 90% floor capture (LB-254) |
| 2 | SAM — Red Sea day-trips | **$21.3M–$33.4M (Hurghada alone)** | Hurghada 1.9M arrivals 2023 (UNWTO) × labelled 35–55% boat-trip participation × $32; Sharm + other resorts = held upside |
| 3 | TAM — Egypt marine | Red Sea slice (rung 2 + held resorts); **Nile + Alexandria HELD NULL** | Egypt 15.78M arrivals / $15.3B spend 2024 (UNWTO) is context ceiling |

## Hard rules
1. **Captive floor unchanged (LB-254):** rung-1 anchors on `transport_spend_pool_yr` ($8.5M). Do **NOT** recover any rung by `floor / 0.10`.
2. **Rung 2 participation (35–55%) is a labelled ASSUMPTION band** — render as an assumption, never as a sourced datum. Base (1.9M Hurghada arrivals) is sourced.
3. **Rungs held null stay null:** Nile Luxor–Aswan transit and Alexandria waterfront have no route-level boardings — do not synthesize. They are candidate rungs.
4. **Sanity gate:** rung-3 marine slice must stay well below Egypt's $15.3B tourism economy. (The old inverted note is deleted — do not reproduce it.)
5. **Plain-English deck copy only.** Slide captions map to `ladder_transitions_plain_english` in the sidecar — no SOM/SAM/TAM/GMV/"grounded floor"/"captive" strings on any rendered slide. `deck-studio/qa/partner_copy_lint.py` + `scripts/audit_partner_copy.py` must pass.

## Cascade
`aggregate.py` (Egypt uses ride-hail region CAPEX $600K, NOT hospitality $1M) → `growth.py` (bind rungs above) → `splice_growth_into_partner.py` → transparent sheet in place (`fileIdToReplace`) → economics sidecar → master tracker. Model and sheet must agree.

## Deck
inDrive Egypt deck `1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk` — TAM slide reflects the ladder (floor + Red Sea day-trip rung + Egypt marine rung with null Nile/Alexandria shown as roadmap). Dual unit-economics anchor selection (Giftun/Ras Mohammed) still `pending_jaideep` per PR #266. Atlas screenshot slots remain for Jaideep's human insertion — no placeholder text.
