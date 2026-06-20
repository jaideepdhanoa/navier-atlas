# Partner Coverage Phase 3 — Shared Registry Gap Queue — 2026-06-20

This is the clean Step 3 queue after the filtered 80:20 inheritance pass. It contains unresolved scopes that **could not inherit from existing Atlas hierarchy**. It does not mutate registry, geometry, partner pages, map scope, network footprint, or economics sidecars.

## Guardrails

- only unresolved scopes after existing-Atlas inheritance are included
- manual partner-bind exclusions are not converted into gaps
- NEOM and Red Sea Global are excluded from partner binds as sovereign-exclusive, not queued as generic partner gaps
- null/backlog beats speculative geography

## Summary
- **gap_scope_rows**: 87
- **deduped_country_gap_items**: 53
- **priority_counts**: {'P1_multi_partner_alias_registry_review': 6, 'P2_two_partner_registry_review': 18, 'P3_single_partner_hold_for_targeted_validation': 29}
- **affected_partner_counts**: {'cabify': 4, 'didi': 3, 'indrive': 15, 'uber': 16, 'yango': 19, 'bolt': 26, 'freenow': 3, 'grab': 1}

## Priority queue

| Country | priority | affected partners | gap rows | required next step |
|---|---|---:|---:|---|
| Peru | P1_multi_partner_alias_registry_review | cabify, didi, indrive, uber, yango | 5 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Chile | P1_multi_partner_alias_registry_review | cabify, didi, indrive, uber | 4 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Ghana | P1_multi_partner_alias_registry_review | bolt, indrive, uber, yango | 4 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Argentina | P1_multi_partner_alias_registry_review | cabify, didi, indrive | 3 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Guatemala | P1_multi_partner_alias_registry_review | indrive, uber, yango | 3 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Ukraine | P1_multi_partner_alias_registry_review | bolt, indrive, uber | 3 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Angola | P2_two_partner_registry_review | indrive, yango | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Austria | P2_two_partner_registry_review | bolt, freenow | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Bangladesh | P2_two_partner_registry_review | indrive, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Cyprus | P2_two_partner_registry_review | bolt, indrive | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Georgia | P2_two_partner_registry_review | bolt, yango | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Germany | P2_two_partner_registry_review | bolt, freenow | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Honduras | P2_two_partner_registry_review | indrive, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Jordan | P2_two_partner_registry_review | uber, yango | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Kazakhstan | P2_two_partner_registry_review | bolt, yango | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Lebanon | P2_two_partner_registry_review | indrive, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Namibia | P2_two_partner_registry_review | indrive, yango | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Netherlands | P2_two_partner_registry_review | bolt, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Pakistan | P2_two_partner_registry_review | indrive, yango | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Poland | P2_two_partner_registry_review | bolt, freenow | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Romania | P2_two_partner_registry_review | bolt, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Slovenia | P2_two_partner_registry_review | bolt, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Uganda | P2_two_partner_registry_review | bolt, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Uruguay | P2_two_partner_registry_review | cabify, uber | 2 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Algeria | P3_single_partner_hold_for_targeted_validation | indrive | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Armenia | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Azerbaijan | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Belgium | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Bolivia | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Bulgaria | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Cameroon | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Czechia | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Democratic Republic of the Congo | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Denmark | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Estonia | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Ethiopia | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Hungary | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Kuwait | P3_single_partner_hold_for_targeted_validation | uber | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Latvia | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Lithuania | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Madagascar | P3_single_partner_hold_for_targeted_validation | indrive | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Moldova | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Mozambique | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Myanmar | P3_single_partner_hold_for_targeted_validation | grab | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Nepal | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Paraguay | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Saint Lucia | P3_single_partner_hold_for_targeted_validation | uber | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Senegal | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Slovakia | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Switzerland | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Uzbekistan | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Zambia | P3_single_partner_hold_for_targeted_validation | yango | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |
| Zimbabwe | P3_single_partner_hold_for_targeted_validation | bolt | 1 | Validate coastal/waterfront relevance, then alias/provenance-bind or create registry/geometry task. |

## Explicit non-gaps / exclusions

- Bolt Malaysia exclusions outside Penang and Sabah / Kota Kinabalu are **not** converted into registry gaps.
- Bolt Mexico and Morocco removals are **not** converted into registry gaps in this batch.
- NEOM and Red Sea Global are sovereign-exclusive and are **not** generic partner bind/gap candidates.

Machine-readable artifact: `partner-coverage-phase-3-shared-registry-gap-queue-2026-06-20.json`.
