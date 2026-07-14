# GROK SPEC — inDrive Egypt economics cascade + deck seal (2026-07-14)

**Goal:** light up the `indrive-egypt` deck's unit-economics + market-overview from held to
grounded for the two promoted Red Sea luxury-belt routes, deterministically, without
inventing anything and without disturbing the three held routes.

## Inputs already in this PR

1. `finance/recal/corridors-indrive.json` — the two promoted routes now carry
   `L3_locals.corridor_annual_oneway_pax` + `comparable_fare_usd_pax`, provenance in
   `_demand_basis` / `_fare_basis`, and their `_economics_hold_reason` removed. The three held
   routes are unchanged (still carry `_economics_hold_reason`, null L3_locals).
2. `deck-studio/decks/indrive-egypt/economics-binding.json` + `market-scope.json` — the two
   `city_route_pairs` now bind exact `route_id`s with plain-English theses; three held
   `route_id`s recorded under `country_total.held_route_ids`.
3. `INDRIVE-EGYPT-UNIT-ECONOMICS-RECEIPT-2026-07-14.json` — expected per-boat outputs (use as QA).

## Deterministic steps

Run the standard partner-model cascade for `indrive` against the scoped view:

```
# §B.0 gate — must PASS (Egypt country-reference row is complete: captain 12000, energy 0.06,
#   grid_co2 0.45, marina 8000, cost_index 0.30)
python3 scripts/validate_country_reference.py --partner indrive \
  --corridors finance/recal/corridors-indrive.json \
  --country-reference finance/model/country-reference.json --json /tmp/indrive-cr-gate.json

# 1. aggregate (scoped view) → rollup
python3 finance/model/aggregate.py --partner indrive \
  --corridors finance/recal/corridors-indrive.json --json finance/recal/agg-indrive.json

# 2-4. growth ladder → frontend block → splice into partner JSON
# 5. transparent sheet (uv run --with openpyxl)
# 6. master tracker row
```

Then regenerate the deck deterministically (Slides API only; no PPTX):

```
python3 deck-studio/decks/gen_deck_economics.py --deck indrive-egypt
# then apply generated economics to live deck 1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk
```

## QA checks (must hold before seal)

- **Per-boat economics match the receipt** (N30 Pioneer II, 45% load, 12h schedule):
  - Giftun `rn-b06f6971ed47`: ~7,588 pax/boat, ~$242,827 rev, ~$73,959 opex, ~70% margin, ~3.55-yr payback.
  - Ras Mohammed `rn-c16a1627130f`: ~5,962 pax/boat, ~$298,114 rev, ~$74,494 opex, ~75% margin, ~2.68-yr payback.
- The unit-economics slide shows **route-level** economics (per boat), not market-level aggregates.
- The three held routes remain **absent** from grounded totals (no invented values).
- Market-scale / TAM figures are **labeled destination-pool** (pool × capture), not observed boardings.
- `scripts/audit_partner_copy.py` → zero jargon leaks. No visible Atlas-slot / build text.

## Two decisions for Jaideep (do NOT resolve silently)

1. **Capture rate for captive tourism.** `indrive-egypt` market `capture_rate` is 0.10 (contested).
   Giftun and Ras Mohammed are near-captive excursion corridors (boat is the only access), which
   under LB-254 would justify a higher captive capture and a captive TAM treatment. Held at the
   conservative 0.10 pending Jaideep's call; flag on the TAM slide accordingly.
2. **Representative route for the single unit-economics slide.** Default recommendation: Giftun
   (flagship / largest pool). Ras Mohammed has the cleaner payback (2.68 yr) and single-source-
   corroborated count. Jaideep to confirm which anchors the slide.

## Geography-owned cascade (corridor-inheritance)

Cascade the improved Giftun (187,512, replacing the 1.2M airport proxy) and corroborated Ras
Mohammed (50,000) counts to the shared `bolt-egypt` and `yango-egypt` corridor records so the
three partners stay consistent on shared Red Sea geometry.

## Out of scope / hold

- Cairo marine: null (Nile waterway, no BPs/routes).
- Alexandria: candidate/null — mint boarding points + routes in canonical geography and source
  route-level demand/fare before any economics.
- Sahl Hasheesh, Soma Bay, Sharks Bay: held pending route-level demand + fare.
