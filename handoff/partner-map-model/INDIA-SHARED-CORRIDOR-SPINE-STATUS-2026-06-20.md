# India Shared Corridor Spine — Execution Slice 1

Source branch: `partner-proposal-schema-conformance-pr57` (`4611a7f`).

## Accepted baseline now in scope

- **Mumbai / Maharashtra waterfront corridors** (`mumbai`) — accepted_baseline
- **Goa corridors** (`goa`) — accepted_baseline
- **Kerala corridors** (`kerala`) — accepted_baseline
- **Andaman Islands corridors** (`andaman`) — accepted_baseline

## Extracted route counts

- **andaman**: 40 routes; 40 geometry-present; 0 quarantined/hidden; 40 N30; 0 Quanta-LR roadmap; 0 >150nm review
- **goa**: 16 routes; 16 geometry-present; 0 quarantined/hidden; 16 N30; 0 Quanta-LR roadmap; 0 >150nm review
- **kerala**: 12 routes; 12 geometry-present; 0 quarantined/hidden; 12 N30; 0 Quanta-LR roadmap; 0 >150nm review
- **mumbai**: 29 routes; 26 geometry-present; 3 quarantined/hidden; 28 N30; 0 Quanta-LR roadmap; 1 >150nm review

## Allowed additions for this pass

- **Gujarat port/coastal spine** — `not_found_in_current_routes` in current `data-clean/ROUTES.json`; Adani-first; platform inheritance only after city/region support.
- **Tamil Nadu / Chennai coast** — `not_found_in_current_routes` in current `data-clean/ROUTES.json`; mobility-platform candidate if Atlas nodes can be cleanly added.
- **Andhra Pradesh / Visakhapatnam coast** — `not_found_in_current_routes` in current `data-clean/ROUTES.json`; Adani/port + city/tourism candidate if grounded.
- **West Bengal / Kolkata-Haldia-Sundarbans edge** — `not_found_in_current_routes` in current `data-clean/ROUTES.json`; evaluate carefully; exact-bind only.
- **Lakshadweep** — `not_found_in_current_routes` in current `data-clean/ROUTES.json`; backlog unless already grounded or explicitly green-lit.

## Partner reuse decision

- **Rapido India** and **Ola India** already have Mumbai, Goa, Kerala, and Andaman proposal market pages in the repo; these should be normalized onto this shared spine rather than recreated.
- **Uber India** should be split from global `uber.json` as an India-focused derivative using this spine.
- **Reliance** should inherit the same accepted baseline only where the Jio-led consumer-platform + asset/platform overlay is credible.
- **Adani** should use the accepted baseline opportunistically, but the first true extension lane is Gujarat/ports/coastal real estate, subject to exact asset binding.

## Next slice

Build `india-partner-use-case-matrix.json` with at least two local use cases per promoted market and flag any route whose geometry exists but economics are absent. Then prepare the Grok handoff for route sealing/economics cascade.
