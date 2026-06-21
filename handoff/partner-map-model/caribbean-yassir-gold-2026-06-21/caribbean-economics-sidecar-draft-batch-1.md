# Caribbean mobility economics sidecar — draft batch 1

Generated: 2026-06-21

Status: **draft only; not cascaded into the live finance model**. This sidecar converts the first banked Caribbean demand anchors into source-tiered country-reference drafts and route-economics inputs while preserving null route IDs.

## Country-reference preflight

Draft rows prepared for:

- Bahamas
- Puerto Rico
- U.S. Virgin Islands
- British Virgin Islands
- Barbados

File: `caribbean-country-reference-draft-batch-1.json`

Do not apply these rows to `finance/model/country-reference.json` yet. Electricity anchors are directionally source-backed; wage and marina overhead assumptions remain low-confidence.

## Route-economics input preflight

File: `caribbean-route-economics-inputs-batch-1.json`

### Batch-1 candidates

1. Nassau / Paradise Island water layer — fare comparable found; demand still tourism-pool derived.
2. San Juan ↔ Cataño — route, schedule, fare, and system ridership found; route-specific ridership split still missing.
3. Red Hook ↔ Cruz Bay — schedule and fare found; demand is visitor-arrival pool only.
4. St. Thomas ↔ Tortola — schedule and fare range found; route demand missing.
5. Bridgetown Port waterfront extension — tourism/cruise pool found; fare comparable missing.

## Hard gates before model cascade

- Grok must seal exact route IDs and boarding points; no synthetic IDs.
- Country-reference rows need review before live model insertion.
- Route-level demand/fare assumptions must be accepted or downgraded to gap queue.
- Do not sum overlapping tourism pools without dedupe.
- Keep economics sidecar out of gold export until route IDs exist.
