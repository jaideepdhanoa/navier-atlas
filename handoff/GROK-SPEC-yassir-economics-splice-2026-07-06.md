# GROK SPEC — Yassir 4-market economics cascade + splice into partner JSON

**Date:** 2026-07-06
**Owner:** Grok (deterministic model/cascade lane)
**Why:** Registry spine now unified (Morocco 10 · Tunisia 8 · Algeria 7 · Senegal 7) but the partner `growth_case` the deck reads still carries the OLD floor (43 boats / ~$111M pool / 2–3 markets). The Yassir × Navier deck (Noon-parity build) is blocked on this splice. Tasklet owns the deck build; this is the one model-lane gate.

## Scope
Yassir footprint = **Morocco · Tunisia · Algeria · Senegal** (all 4 sub-proposals, super_app archetype).

## Tasks
1. **Preflight — no silent Singapore opex (LB-243):** confirm `model/country-reference.json` has rows for **Morocco, Tunisia, Algeria, Senegal**. Add any missing. CAPEX region rule: all 4 are non-US/EU → **$600K/vessel**.
2. **Cascade over the full 4-market footprint:** `aggregate.py → growth.py → splice_growth_into_partner.py` for `yassir`.
   - Senegal: 7 finance corridors inherited 1:1 from `yango-senegal` L3 (Gorée grounded; Saly/new legs honest-null / estimated — do NOT invent L3).
   - Algeria: 7 corridors; 3 grounded + 4 new legs spine-only (null L3, honest-pending).
   - Morocco / Tunisia: existing L3 unchanged.
3. **Splice the new floor into BOTH partner JSONs** that the deck/microsite read:
   - `data-clean/partners/yassir.json` → `growth_case`
   - `partner-pitch/partners/yassir.json` → `growth_case`
   - Update: `grounded_floor` (fleet, market_rev, transport_spend_pool), `revenue_potential` (SOM floor/full/SAM), `journey_gmv`, `marine_mobility_tam`, `partner_platform_rev_on_navier`, `phase_economics`, `vessel_sizing`, `ladder_transitions`. Per-market boats/TAM populated (estimated flagged where L3 null).
   - Expected direction (from your own 2026-07-06 cascade receipt): hub floor ~**34 boats / ~$116M pool**; Senegal ~1 boat / ~$212K rev; Algeria ~1 boat / ~$169K rev. Recompute authoritatively — these are sanity anchors, not targets.
4. **Cascade provenance (Gate D):** transparent sheet updated **in place** (`fileIdToReplace`, preserve URL); economics sidecar rebuilt; master tracker row refreshed; `yassir-aggregate.json` aggregates all 4 markets.
5. **Gates:** `validate_finance_inheritance.py` PASS (spine identical across yassir markets); model ↔ sheet agree.

## Return receipt
- New `growth_case` numbers: hub floor + per-market (Morocco/Tunisia/Algeria/Senegal) boats · transport rev · SOM/SAM/TAM/GMV · platform take.
- Which per-market legs are grounded vs estimated/null-pending.
- Confirm both yassir.json files spliced + sheet/sidecar/tracker updated.

## Explicitly NOT Grok this batch (Tasklet lane)
- Deck build (all slides, Slides API, in place)
- Market-specific N30 composite image generation
- Route-appendix boxes, copy, logo/cover
- Atlas map screenshots = Jaideep inserts
