# Grok deterministic handoff — India + GCC partner proposal continuation

Date: 2026-06-20  
PR target: `tasklet/india-gcc-partner-spines-2026-06-20` / PR #58  
Tasklet owner: research, spec, economics orchestration  
Grok owner: deterministic route reconciliation, sealing, render QA, sidecar build, CI loop

## Mandate

Continue the India + GCC partner proposal build using the PR #58 artifacts. Do not reinterpret this as a new geography research pass. This is a deterministic normalization/seal/economics handoff.

Primary inputs already in the PR:

- `handoff/partner-map-model/india-shared-corridor-spine.json`
- `handoff/partner-map-model/india-partner-use-case-matrix.json`
- `handoff/partner-map-model/uae-gulf-shared-corridor-spine.json`
- `handoff/partner-map-model/INDIA-CORRIDOR-ADDITION-SUFFICIENCY-AUDIT-2026-06-20.md`
- `handoff/partner-map-model/INDIA-PARTNER-NORMALIZATION-BATCH-2026-06-20.md`
- `handoff/partner-map-model/india-partner-normalization-batch-2026-06-20.json`

## Hard rules

1. **Exactness over coverage.** ID/alias/provenance match only. Null beats confidently wrong.
2. **No new unsupported geography.** Do not add markets to `network_footprint[]` unless they map to existing sealed registry keys and Atlas hierarchy support.
3. **Display can precede economics.** If Atlas hierarchy + geometry exist, display the market even if economics is pending; track economics separately.
4. **Goa gets promoted; Lakshadweep stays gated.** Goa needs a full tourism-market expansion pass. Lakshadweep remains hold unless already grounded or explicitly green-lit.
5. **No full-replace / PPTX-style round trip.** Work through repo data and deterministic CI.
6. **Use GitHub as source of truth.** Push deterministic changes to the PR branch or a follow-on PR; no zip hand-back as final state.
7. **Fold LB-242 `route_water_allowlist.json` into routing/mask gates** before final route QA.
8. **Economics sidecar is required** in every gold/export package after route IDs are final.

## Workstream A — Rapido India normalization

Input partner file: `partner-pitch/partners/rapido.json`

Task:

- Reconcile existing Rapido India markets against `india-shared-corridor-spine.json`:
  - Mumbai / Maharashtra waterfront corridors
  - Goa corridors
  - Kerala / Kochi + backwaters
  - Andaman Islands
- Bind `featured_routes[].route_id` only where an exact route exists in the spine.
- Leave `route_id: null` when the route is narrative, not yet geometry-bound, or a new exact-bind candidate.
- Re-gate every route by range:
  - ≤70nm → N30 Pioneer II commercial-now
  - 75–150nm → Quanta-LR roadmap
  - >150nm → Quanta-LR flagged for review
- After reconciliation, run the partner economics cascade and update partner JSON + growth block + sidecar inputs.

Acceptance:

- Anchor city IDs resolve.
- Market roster equals story scope equals route chips minus explicitly held lanes.
- No invented route IDs.
- Economics are present or explicitly economics-pending.

## Workstream B — Ola India normalization

Input partner file: `partner-pitch/partners/ola.json`

Task:

- Keep Ola India-only for this pass.
- Normalize the same four accepted baseline India markets to the shared spine.
- Preserve Ola Electric / clean-mobility framing, but do not let narrative create geography.
- Bind exact route IDs and null everything else.
- Run the same economics cascade after route reconciliation.

Acceptance:

- Same route-binding and anchor-city gates as Rapido.
- No UK/Australia/NZ scope included in this pass.

## Workstream C — Uber India draft

Current state:

- Existing global `partner-pitch/partners/uber.json` has an India market with Mumbai + Goa anchors.
- The India-focused pass needs the same four accepted baseline markets: Mumbai, Goa, Kerala, Andaman.

Preferred action:

- Create an India-focused derivative/draft spec for review rather than destructively replacing the global Uber page.
- If implementation prefers a single file, expand the global Uber India market only after review; do not shrink any existing global Uber markets.

Task:

- Draft Uber India from the same accepted India spine used for Rapido/Ola.
- Add Kerala and Andaman baseline coverage to the India-focused draft.
- Keep Gujarat, Tamil Nadu/Chennai, Andhra/Vizag, and West Bengal/Kolkata-Haldia as exact-bind expansion lanes until sealed.
- Do not import non-India global Uber markets into the India derivative.

Acceptance:

- India-focused story has all four accepted baseline markets.
- Existing global Uber proposal remains intact unless explicitly merged.
- All market display scope is Atlas-grounded.

## Workstream D — Goa marquee expansion

Current state:

- Goa has 16 geometry-present baseline routes.
- That is safe for display but insufficient for a tourism-led proposal.

Task:

Promote Goa to a marquee/full tourism-market pass with these families:

1. Panaji / Mandovi / Old Goa ferry spine.
2. North Goa beach-resort corridor.
3. South Goa resort corridor.
4. Grande Island / day-trip corridor if exact geometry is clean.
5. Mormugao / port-arrival corridor if exact geometry is clean.
6. Goa ↔ Mumbai as Quanta-LR roadmap, not N30 commercial-now.

Special QA:

- Canonicalize raw POI labels before any partner-facing render. Existing labels like `Marina Russian B2B Thai Spa Service near me` must not leak into partner proposals.
- Use official Goa ferry route evidence as a local-use-case anchor, but do not fabricate route geometry from prose.

Acceptance:

- Goa has at least two local use cases in the proposal narrative:
  - Mandovi/river ferry commuter + tourist mobility.
  - Tourism resort/beach transfers.
- Any arrival/airport/port transfer route remains exact-bind pending unless sealed.
- Roadmap legs are visibly roadmap/Quanta-LR.

## Workstream E — Active India exact-bind expansion lanes

These lanes are active, but not display-ready until exact support exists.

| Lane | Action | Gate |
|---|---|---|
| Gujarat coast / ports | Adani-first asset/port binding; Reliance/Jio overlay later. | Exact Mundra/Tuna/Dahej/Hazira or other port/city/BP bind. |
| Tamil Nadu / Chennai coast | Mobility + Adani overlay candidate. | Exact Chennai/Kattupalli/Ennore bind. |
| Andhra / Visakhapatnam | Mobility + Adani overlay candidate. | Exact Vizag/Gangavaram bind. |
| West Bengal / Kolkata-Haldia | Mobility + Adani overlay candidate. | Exact Kolkata/Haldia/Sundarbans-edge geography validation. |
| Lakshadweep | Hold. | Grounding or explicit green-light only. |

Do not render a non-marine footprint card grid for these. Use `coverage_note` prose until map-scope-safe.

## Workstream F — Noon UAE/Gulf proposal build

After India normalization:

- Use `uae-gulf-shared-corridor-spine.json`.
- Build Noon using Careem-style UAE/Gulf platform mechanics.
- Domestic UAE first.
- UAE/Gulf cross-border roadmap second.
- Treat Noon as commerce/platform GMV + mobility enablement, not a ride-hail clone.
- Keep **Manama ↔ KSA Eastern Province** as the only commercial-now Gulf cross-border candidate; the rest remains Quanta-LR roadmap.

## Economics cascade and sidecar

For Rapido, Ola, and any accepted Uber India draft:

1. Reconcile route IDs and vessel gates first.
2. Run economics cascade only after route reconciliation.
3. Update partner JSON growth blocks.
4. Build transparent sheet outputs in place when sheet access is available.
5. Build `economics_by_route_id.json` after the final route seal, against the new gold route IDs.
6. Include economics sidecar in every gold/export package.

Known blocker:

- Live Google Sheets write path is still blocked by service-account/editor permissions for the live partner sheet IDs. Do not create replacement sheets; preserve live URLs once access is fixed.

## Render QA acceptance

Grok QA report must include:

- 0 anchor-city ID mismatches for Rapido/Ola/Uber India draft.
- 0 invented `route_id`s.
- 0 land crossings after water/mask allowlist logic, including LB-242 `route_water_allowlist.json`.
- Route vessel gates regenerated from range, not stale registry labels.
- Goa label canonicalization ledger.
- Market roster reconciliation:
  - partner markets
  - story scope
  - route chips
  - roll-up/brief-only lanes
- Economics provenance updated or explicitly `economics_pending`.
- Sidecar generated after final seal.
- Any dropped route/BP has a reason; no silent drops.

## Output expected from Grok

- PR branch update or follow-on PR with deterministic data changes.
- QA report markdown in `handoff/partner-map-model/`.
- Updated partner JSONs / draft spec as applicable.
- Updated sealed data-clean outputs if the seal is run.
- Economics sidecar and manifest references for any gold/export package.

