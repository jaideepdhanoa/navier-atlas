# Adani exact-bind audit — 2026-06-20
Source-led audit against the current 97-route India spine. This is **not** a footprint promotion.
## Source
- Official source: `https://www.adaniports.com/ports-and-terminals`
- Existing Atlas source: `handoff/partner-map-model/india-shared-corridor-spine.json`
- Current India spine markets: andaman=40, goa=16, kerala=12, mumbai=29
## Verdict
No Adani asset is promoted to partner footprint. The official Adani asset list is real, but the current India spine has no exact asset/BP label hits for these ports. Mormugao and Vizhinjam have only broad existing market context (`goa-india`, `kerala-backwaters-india`), not exact asset binding.
| Asset | Lane | Official name/source hit | Existing spine hit count | Existing market candidate | Verdict | Status |
|---|---|---|---:|---|---|---|
| Mundra | Gujarat | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Tuna | Gujarat | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Dahej | Gujarat | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Hazira | Gujarat | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Mormugao | Goa | official page list | 0 | goa-india | CITY_SCOPE_ONLY_BP_MISSING | not_promoted_exact_bind_required |
| Vizhinjam | Kerala | official page list | 0 | kerala-backwaters-india | CITY_SCOPE_ONLY_BP_MISSING | not_promoted_exact_bind_required |
| Ennore | Tamil Nadu / Chennai | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Kattupalli | Tamil Nadu / Chennai | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Karaikal | Tamil Nadu / Chennai | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Gangavaram | Andhra / Vizag | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Krishnapatnam | Andhra / Vizag | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Haldia | West Bengal / Kolkata-Haldia | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | not_promoted_exact_bind_required |
| Dhamra | Odisha | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | backlog_not_promoted |
| Gopalpur | Odisha | official page list | 0 | — | NO_EXISTING_ATLAS_SCOPE_OR_LABEL_HIT | backlog_not_promoted |

## Next actions
1. For Goa/Mormugao and Kerala/Vizhinjam: verify exact boarding-point / asset aliases in the shared registry before any display bind.
2. For Gujarat, Tamil Nadu/Chennai, Andhra/Vizag, West Bengal, and Odisha: keep as registry expansion / exact-bind backlog, not current proposal footprint.
3. Do not cascade economics for Adani until a bind is `OK_EXACT_LABEL_HIT` or an ID mismatch is resolved.
