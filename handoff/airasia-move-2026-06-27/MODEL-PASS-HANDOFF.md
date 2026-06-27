# AirAsia MOVE — model-pass handoff (capture band)

Per Jaideep's decision (2026-06-27): **anchor TAM on arriving-seat distribution-capture**, source the demand anchors (done), and **hand the capture band to the model pass.**

## What's handed over
- **Demand anchors:** `AIRASIA-DEMAND-ANCHORS.json` — sourced inbound passenger/seat pools for the Phase 1 coastal gateways (Phuket 17.4M+, Bali 21.8M+, Kota Kinabalu / Penang / Langkawi from Malaysia Airports, Samui, Lombok, Labuan Bajo), plus Capital A load factors (82–90%). Sourced facts are separated from flagged assumptions (island-bound share, premium-transfer take-rate).
- **Anchor basis:** arriving-seat distribution-capture (NOT contested city-mobility).
- **Footprint:** `airasia-move-seal-manifest.json` — 15 markets across TH/ID/MY.

## What the model pass owns (not Tasklet, not the seal)
1. Set the **capture band** (floor / full-network / SAM) on arriving-seat → onward-water-transfer conversion.
2. Produce `finance/airasia-move-aggregate.json` over the full Phase 1 footprint.
3. Run `aggregate.py → growth.py → splice_growth_into_partner.py` to fill the `growth_case` numeric bands (currently `null`, `model-pass-pending`).
4. Build the transparent sheet (in place), wire `economics_url`, refresh the master tracker.

## Guardrails carried from the parity skill
- **Captive sanity (LB-254):** AirAsia is a distributor, not a captive resort — use the arriving-seat pool, not a captive floor/0.10 inflation. Sanity-check: no rung should exceed the destination country's whole tourism economy.
- **Greenfield honesty (LB-250):** if greenfield is in the headline, label it as the template band, not a borrowed peer census.
- **No silent Singapore opex (LB-243):** ensure MY/TH/ID all have `model/country-reference.json` rows before aggregate.
- **CAPEX region rule:** non-US/EU → $600K/vessel.

Until the model runs, all numeric bands stay `null` — **null beats confidently-wrong.**
