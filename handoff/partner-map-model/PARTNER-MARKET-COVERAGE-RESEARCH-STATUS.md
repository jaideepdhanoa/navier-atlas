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

## Proposal-priority interpretation
- **Bolt**: official city page is now the operating-market source; the remaining work is coastal/water relevance triage plus exact alias/provenance binding for relevant cities.
- **Yango**: official country footprint is captured from Yango country links, and city-level rows are captured where official country pages expose city links or explicit location bullets. Country-only rows are intentionally not city-bound.
- **Careem**: UAE-only scope is recorded; no more Careem coverage research until instructed otherwise.

## Files
- `partner-market-coverage-research.json`
- `partner-market-coverage-research-gap-queue.json` — full triage queue, not clean registry gaps yet.
- `partner-market-coverage-proposal-priority-queue.json` — Bolt/Yango active proposal subset.
