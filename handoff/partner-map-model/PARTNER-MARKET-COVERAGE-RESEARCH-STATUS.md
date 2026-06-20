# Partner market coverage research status
This is the corrected upstream layer. The previous `partner-market-canonical-bindings.json` only bound **markets already present in partner JSON buckets**; it did not prove each partner’s full coastal operating-market coverage had been researched.
## Current directive update
- **Careem** is marked **UAE-only** per user directive and skipped for further coverage work in this pass.
- **Bolt** and **Yango** are marked **proposal-priority** because proposals are being prepared now.
## Rule
- Public/user-directed partner operating footprint first.
- Normalize source market labels second.
- Exact Atlas ID/alias/provenance bind third.
- Anything not bindable becomes alias/provenance/registry-expansion triage — never a partner-specific fake market.
## Research batch status
- **bolt**: 863 source rows; 27 exact-bound; 836 pending alias/registry triage; 0 scope-only/skipped rows.
- **careem**: 1 source rows; 0 exact-bound; 0 pending alias/registry triage; 1 scope-only/skipped rows.
- **didi**: 16 source rows; 0 exact-bound; 0 pending alias/registry triage; 16 scope-only/skipped rows.
- **grab**: 413 source rows; 14 exact-bound; 399 pending alias/registry triage; 0 scope-only/skipped rows.
- **yango**: 63 source rows; 4 exact-bound; 27 pending alias/registry triage; 32 scope-only/skipped rows.


## Yango correction / coverage guardrail — 2026-06-20
- The Yango official-source scan is **not** the Yango coverage ceiling. It is an additive candidate/gap scan only.
- Existing Yango proposal coverage in `partner-pitch/partners/yango.json` remains the baseline and must not be reduced by the scan.
- Current baseline from the live Yango proposal file: **8 sub-proposal markets**, **33 network_footprint entries**, **33 map-scope cluster city IDs**, and **24 unique anchor city IDs**.
- The prior “4 display-ready” language meant “4 rows bound inside that captured official-source subset,” not “Yango only has four display-ready markets.” That wording is now corrected.
- New guardrail artifact: `partner-market-coverage-yango-coverage-guardrail.json`.
- Any future Yango scan must diff against the existing partner file, `_map_scope`, `network_footprint[]`, and `map-scope.json::yango` before adding backlog rows; no source-page omission can delete or demote existing coverage.

## Proposal-priority interpretation
- **Bolt**: official city page is now the operating-market source; the remaining work is coastal/water relevance triage plus exact alias/provenance binding for relevant cities.
- **Yango**: official country/city rows are a partial additive scan only. Existing Yango proposal/map coverage is the baseline; the source scan can add candidates/gaps but must never shrink coverage.
- **Careem**: UAE-only scope is recorded; no more Careem coverage research until instructed otherwise.

## Files
- `partner-market-coverage-research.json`
- `partner-market-coverage-research-gap-queue.json` — full triage queue, not clean registry gaps yet.
- `partner-market-coverage-proposal-priority-queue.json` — Bolt/Yango active proposal subset.

## Added proposal triage artifacts
- `partner-market-coverage-yango-city-triage.json` — Yango city rows split into existing Atlas display-ready, coastal registry/alias backlog, and inland/not-map-footprint.
- `partner-market-coverage-bolt-country-rollup.json` — Bolt official city inventory rolled up by country so the active proposal pass can triage coastal relevance without confusing source coverage with marine footprint.
