# Partner market coverage research status
This is the corrected upstream layer. The previous `partner-market-canonical-bindings.json` only bound **markets already present in partner JSON buckets**; it did not prove each partner’s full coastal operating-market coverage had been researched.
## Rule
- Public partner operating footprint first.
- Normalize source market labels second.
- Exact Atlas ID/alias/provenance bind third.
- Anything not bindable becomes alias/provenance/registry-expansion triage — never a partner-specific fake market.
## First research batch
- **bolt**: 863 source rows; 27 exact-bound; 836 pending alias/registry triage; 0 scope-only rows.
- **careem**: 1 source rows; 0 exact-bound; 0 pending alias/registry triage; 1 scope-only rows.
- **didi**: 16 source rows; 0 exact-bound; 0 pending alias/registry triage; 16 scope-only rows.
- **grab**: 413 source rows; 14 exact-bound; 399 pending alias/registry triage; 0 scope-only rows.

## Interpretation
- **Bolt** and **Grab** now use official city/location pages as source input; this reveals many source markets that were not present in the existing partner buckets.
- **DiDi** official global page currently gives country-level presence only; no city IDs are bound from that alone.
- **Careem** official page currently gives count/scope only; city-level source is still needed.

## Files
- `partner-market-coverage-research.json`
- `partner-market-coverage-research-gap-queue.json` — triage queue, not clean registry gaps yet.
