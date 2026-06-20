# India / Noon finance wiring spec — 2026-06-20
Base: PR #59 / `pr-59`. Purpose: convert Grok’s sealed route IDs into finance-model work without attaching economics to unsafe rows.
## Acceptance snapshot
- India ledger: {'total': 921, 'sealed': 900, 'held_null': 21}
- Noon ledger: {'total': 12, 'sealed': 12, 'held_null': 0}
- India distinct sealed route IDs: **39** despite 900 sealed partner references.
- Held-null remains: {'rapido': 7, 'ola': 7, 'uber-india-derivative': 7} — keep economics pending.
## Correction to prior blocker note
Grok has Google Sheets access. Current blockers are finance/model wiring plus Sheet ID registration for `rapido`, `ola`, `noon`, and the Uber India derivative, not OAuth.
## Country-reference preflight
- India: missing — add before cascade
- United Arab Emirates: present
- Sri Lanka: missing — add before cascade

## Candela / JalVimana Mumbai signal
- India first electric hydrofoil flying boat, Candela P12, launched in Mumbai.
- Developed by Swedish manufacturer Candela and set to be operated in India by JalVimana.
- Initial routes: Gateway of India to Alibaug; Gateway of India to Elephanta Island.
- Planned route: upcoming Navi Mumbai airport to central Mumbai; expected to cut travel from around 90 minutes to under 30 minutes.
- Planned fleet: 11 hydrofoiling Candela P12 commuter ferries; larger electric water transport ecosystem language.

Use as **market validation / competitive context only** for now — not fare, demand, or Navier economics. It strengthens the Adani airport-access wedge around Navi Mumbai airport ↔ central Mumbai and supports Reliance platform/energy/corporate-demand framing, without creating partner footprint.

## India wiring decision
### ola — Andaman / Port Blair / island mobility
- Suggested market key: `ola-andaman`
- Distinct sealed routes: 10
- Readiness: `route_ids_sealed_demand_partial_pricing_quarantined`
- Action: do not publish route economics; keep rows economics_pending until DSS fare PDF direct capture succeeds
### ola — Goa
- Suggested market key: `ola-goa`
- Distinct sealed routes: 7
- Readiness: `route_ids_sealed_pricing_comparables_ready_tourism_tam_ready`
- Action: wire draft corridor rows using official RND/taxi/GoaMiles comparables; keep airport demand quarantined
### ola — Kochi / Kerala Water Metro adjacency
- Suggested market key: `ola-kochi`
- Distinct sealed routes: 8
- Readiness: `route_ids_sealed_demand_ready_pricing_partial`
- Action: wire only with conservative fare placeholder from DPR planning benchmark if labelled historical; preferably source current fare before finance publish
### ola — Mumbai / Navi Mumbai / Mandwa / Elephanta
- Suggested market key: `ola-mumbai`
- Distinct sealed routes: 12
- Readiness: `route_ids_sealed_price_floor_ready_demand_partial`
- Action: wire as draft corridor rows with M2M fare floor/comparable; keep demand confidence partial until passenger counts are sourced
### rapido — Andaman / Port Blair / island mobility
- Suggested market key: `rapido-andaman`
- Distinct sealed routes: 10
- Readiness: `route_ids_sealed_demand_partial_pricing_quarantined`
- Action: do not publish route economics; keep rows economics_pending until DSS fare PDF direct capture succeeds
### rapido — Goa
- Suggested market key: `rapido-goa`
- Distinct sealed routes: 7
- Readiness: `route_ids_sealed_pricing_comparables_ready_tourism_tam_ready`
- Action: wire draft corridor rows using official RND/taxi/GoaMiles comparables; keep airport demand quarantined
### rapido — Kochi / Kerala Water Metro adjacency
- Suggested market key: `rapido-kochi`
- Distinct sealed routes: 8
- Readiness: `route_ids_sealed_demand_ready_pricing_partial`
- Action: wire only with conservative fare placeholder from DPR planning benchmark if labelled historical; preferably source current fare before finance publish
### rapido — Mumbai / Navi Mumbai / Mandwa / Elephanta
- Suggested market key: `rapido-mumbai`
- Distinct sealed routes: 14
- Readiness: `route_ids_sealed_price_floor_ready_demand_partial`
- Action: wire as draft corridor rows with M2M fare floor/comparable; keep demand confidence partial until passenger counts are sourced
### uber-india-derivative — Andaman / Port Blair / island mobility
- Suggested market key: `uber-andaman`
- Distinct sealed routes: 10
- Readiness: `route_ids_sealed_demand_partial_pricing_quarantined`
- Action: do not publish route economics; keep rows economics_pending until DSS fare PDF direct capture succeeds
### uber-india-derivative — Goa
- Suggested market key: `uber-goa`
- Distinct sealed routes: 7
- Readiness: `route_ids_sealed_pricing_comparables_ready_tourism_tam_ready`
- Action: wire draft corridor rows using official RND/taxi/GoaMiles comparables; keep airport demand quarantined
### uber-india-derivative — Kochi / Kerala Water Metro adjacency
- Suggested market key: `uber-kochi`
- Distinct sealed routes: 8
- Readiness: `route_ids_sealed_demand_ready_pricing_partial`
- Action: wire only with conservative fare placeholder from DPR planning benchmark if labelled historical; preferably source current fare before finance publish
### uber-india-derivative — Mumbai / Navi Mumbai / Mandwa / Elephanta
- Suggested market key: `uber-mumbai`
- Distinct sealed routes: 14
- Readiness: `route_ids_sealed_price_floor_ready_demand_partial`
- Action: wire as draft corridor rows with M2M fare floor/comparable; keep demand confidence partial until passenger counts are sourced

## Noon wiring decision
- needs_new_uae_demand_anchor_before_noon_economics: 5
- inherit_existing_finance_anchor_after_partner-scope-review: 3
- defer_cross_border_until_LB-242_UAE_Gulf_land_crossing_QA_and_demand_anchor: 4

## Next bite
1. Add India country-reference row.
2. Patch corridors only for sealed Mumbai/Goa/Kochi rows with source-backed draft inputs.
3. Keep Andaman and cross-border UAE Gulf rows pending until source/QA gates clear.
