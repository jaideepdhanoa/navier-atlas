# India + GCC Partner Proposal Execution Status

## Status

Proceeding from the approved plan. First execution slice is complete: the shared corridor spines are now generated from the current Atlas repo branch `partner-proposal-schema-conformance-pr57` at `4611a7f`.

## India spine

Accepted India baseline is now:

1. Mumbai / Maharashtra waterfront corridors
2. Kerala corridors
3. Andaman Islands corridors
4. Goa corridors

Generated artifact:

- `india-shared-corridor-spine.json`

Route inventory extracted from current Atlas routes:

| Market | Total routes | Geometry-present | Quarantined / hidden | Notes |
|---|---:|---:|---:|---|
| Andaman | 40 | 40 | 0 | All N30 commercial-now range by distance |
| Goa | 16 | 16 | 0 | All N30 commercial-now range by distance |
| Kerala | 12 | 12 | 0 | All N30 commercial-now range by distance |
| Mumbai | 29 | 26 | 3 | 28 N30-range routes; 1 >150nm review route |

## India sufficiency correction

The first-slice counts are a safe accepted baseline, **not** final proposal sufficiency.

Allowed India additions should no longer be treated as passive candidates. Updated posture:

- **Goa** — already accepted, but under-covered for a tourism destination. Promote immediately to a full / marquee tourism-market expansion pass.
- **Gujarat port/coastal spine** — promote to active exact-bind expansion lane, especially for Reliance + Adani.
- **Tamil Nadu / Chennai coast** — promote to active exact-bind expansion lane.
- **Andhra Pradesh / Visakhapatnam coast** — promote to active exact-bind expansion lane.
- **West Bengal / Kolkata-Haldia-Sundarbans edge** — promote to active exact-bind expansion lane, with careful geography validation.
- **Lakshadweep** — hold unless already grounded or explicitly green-lit.

Goa needs more than the current short ferry / marina-hop baseline. Target expansion families: Panaji/Mandovi, North Goa beaches, airport/port-arrival transfers, South Goa resort corridors, and Goa ↔ Mumbai as Quanta-LR roadmap.

Repo addendum: `handoff/partner-map-model/INDIA-CORRIDOR-ADDITION-SUFFICIENCY-AUDIT-2026-06-20.md`.

## India partner × market use-case matrix

Generated artifact:

- `india-partner-use-case-matrix.json`

Summary:

| Status | Count |
|---|---:|
| Proposal-ready draft for Uber India | 4 |
| Proposal-ready after economics cascade for Rapido / Ola | 8 |
| Display-only / overlay-pending for Reliance / Adani | 8 |
| Rows passing the two-local-use-case gate | 20 |

Partner posture:

- **Rapido India** and **Ola India** already have Mumbai, Goa, Kerala, and Andaman market pages in the repo; next step is normalization onto the shared spine and economics cascade.
- **Uber India** should be created as an India-focused derivative using the same four accepted baseline markets first.
- **Reliance** should lead with Jio / consumer platform, but partner-market promotion needs a credible Jio/platform/asset overlay.
- **Adani** should lead with ports and coastal real estate; Gujarat is the natural first extension lane, but it needs exact asset-to-Atlas binding before promotion.

## UAE / Gulf spine

Generated artifact:

- `uae-gulf-shared-corridor-spine.json`

Scope rules applied:

- **Noon** mirrors Careem: domestic UAE plus cross-border from UAE, full-journey GMV / mobility-platform economics.
- **RAKTA** focuses on RAK domestic, then RAK ↔ other UAE emirates, then Musandam / Muscat / Doha / Bahrain.
- **Bahrain MOTC** focuses on Bahrain domestic, Manama ↔ KSA Eastern Province, then Doha / Dubai / Abu Dhabi.
- All RAK/Bahrain/Gulf cross-border routes are Quanta-LR roadmap except **Manama ↔ KSA Eastern Province**, which is the commercial-now cross-border candidate.

Route inventory extracted:

| Corridor family | Total routes | Geometry-present | Quarantined / hidden | Commercial-now candidates | Quanta-LR roadmap |
|---|---:|---:|---:|---:|---:|
| Domestic UAE intra-city | 706 | 452 | 254 | 446 | 0 |
| Inter-emirate UAE | 26 | 18 | 8 | 18 | 0 |
| Bahrain domestic | 92 | 87 | 5 | 86 | 0 |
| Bahrain ↔ KSA Eastern Province | 3 | 2 | 1 | 2 | 0 |
| Bahrain ↔ Doha / Dubai / Abu Dhabi roadmap | 7 | 6 | 1 | 0 | 7 |
| RAK cross-border roadmap | 3 | 3 | 0 | 0 | 3 |
| RAK / Musandam candidate via Khasab-labelled routes | 5 | 4 | 1 | 0 | 0 |
| UAE ↔ Gulf cross-border | 23 | 14 | 9 | 0 | 23 |

## Partner normalization batch — 2026-06-20 continuation

Generated artifacts:

- `INDIA-PARTNER-NORMALIZATION-BATCH-2026-06-20.md`
- `india-partner-normalization-batch-2026-06-20.json`

Batch decisions:

- **Rapido India** — anchors resolve for Mumbai, Goa, Kerala, and Andaman. Normalize featured routes to the shared India spine, bind only exact route IDs, then cascade economics.
- **Ola India** — same four-market spine as Rapido; keep India-only for this pass after the UK/Australia/NZ exit correction.
- **Uber India** — existing global Uber file has an India market with Mumbai + Goa only. Preferred next move is an India-focused derivative/draft from the same four accepted baseline markets, not a destructive global Uber replacement.
- **Goa** — promoted from safe baseline to marquee/full tourism expansion. It clears the two-local-use-case gate via Mandovi/ferry mobility plus beach/resort transfer logic; arrival/port flows remain exact-bind candidates.
- **Gujarat, Tamil Nadu/Chennai, Andhra/Vizag, and West Bengal/Kolkata-Haldia** — active exact-bind expansion lanes, not passive candidates.
- **Lakshadweep** — still held unless grounded or explicitly green-lit.
- **Noon** — next UAE/Gulf build after India normalization; use Careem-style platform economics from the Gulf spine.

## Immediate next execution steps

1. Add the partner normalization batch artifacts to PR #58.
2. Prepare the Grok deterministic handoff for Rapido/Ola route reconciliation, Uber India derivative generation, Goa label canonicalization, economics cascade, sidecar generation, and render QA.
3. Keep Reliance and Adani overlay-pending until asset/platform binding is exact.

Clean route spine first; proposal sparkle after. This keeps the build reusable and avoids duplicate geography.

## Grok deterministic handoff — added to PR #58

Generated artifact:

- `GROK-INDIA-GCC-PARTNER-HANDOFF-2026-06-20.md`

Commit added to PR #58:

- `ee68ebe` — `Add Grok India GCC partner handoff`

Handoff scope:

- Rapido/Ola route reconciliation against the India spine.
- Uber India derivative/draft generation from the four-market baseline.
- Goa marquee expansion and label canonicalization.
- Active exact-bind lanes for Gujarat, Tamil Nadu/Chennai, Andhra/Vizag, and West Bengal/Kolkata-Haldia.
- Noon queued from the UAE/Gulf spine.
- Economics cascade + sidecar after route IDs are final.
- Render QA gates: 0 anchor mismatches, 0 invented route IDs, 0 land crossings after LB-242 allowlist, no silent drops.

## Noon / Reliance / Adani next slice — added to PR #58

Generated artifacts:

- `NOON-RELIANCE-ADANI-NEXT-SLICE-2026-06-20.md`
- `noon-reliance-adani-next-slice-2026-06-20.json`

Commit added to PR #58:

- `fc2627c` — `Add Noon Reliance Adani next slice`

Locked decisions:

- Noon proceeds **UAE-first** from the UAE/Gulf spine, with KSA/Egypt held as coverage-note/future scope until exact Atlas overlap and local use cases are validated.
- Noon has **484 geometry-present candidate routes** in the UAE/Gulf spine (`452` domestic UAE, `18` inter-emirate UAE, `14` UAE/Gulf cross-border). Domestic UAE + selected inter-emirate are first; cross-border remains amber/roadmap unless regulatory/hull gates pass.
- Reliance remains **overlay-only**. Jamnagar/Sikka + Mumbai are candidate narrative lanes, but not partner map footprint and not economics-ready.
- Adani remains **overlay-only with exact-bind asset backlog**. Active bind lanes: Gujarat, Goa, Kerala, Tamil Nadu/Chennai, Andhra/Vizag, and West Bengal/Kolkata-Haldia. Odisha is source-supported but backlog unless green-lit.
- No broad country/port-operator footprint is promoted as consumer marine mobility. Exact binds only.

Immediate next execution steps:

1. Convert the Noon UAE-first spec into a partner skeleton / scope spec for Grok.
2. Build Adani exact-bind crosswalk for the active India lanes only.
3. Keep Reliance as overlay/gap-queue until a buyer/use-case owner is validated.
4. After Grok route finalization, run economics cascade + sidecar for accepted scopes.

## Noon skeleton + Adani crosswalk — added to PR #58

Generated artifacts:

- `NOON-SKELETON-ADANI-CROSSWALK-2026-06-20.md`
- `noon-skeleton-adani-crosswalk-2026-06-20.json`

Commit added to PR #58:

- `dcd3e96` — `Add Noon skeleton and Adani crosswalk`

Key findings:

- Noon now has a Grok-ready draft scope spec: derive `scope_city_ids` from UAE/Gulf spine routes where `usable_by_noon = true` and geometry is present. Do not hand-list city IDs.
- Noon first-pass route pools remain `452` domestic UAE, `18` selected inter-emirate, and `14` UAE/Gulf cross-border amber-only.
- Adani official assets were turned into a crosswalk. Current finding: no exact Adani asset label hits in the current 97-route India spine, so all Adani lanes remain `MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS` until exact-bind review.
- Reliance remains held as overlay-only because the current 97-route India spine has no exact Reliance route/asset label hits.

Next execution slice:

1. Build the actual Noon partner skeleton file/spec from the draft scope, without touching live partner JSON until reviewed or Grok-run.
2. Run exact-bind research for Adani active lanes: Gujarat, Goa, Kerala, Tamil Nadu/Chennai, Andhra/Vizag, West Bengal/Kolkata-Haldia.
3. Keep Odisha as Adani backlog unless explicitly green-lit.

## Noon skeleton + Adani exact-bind audit — added to PR #58

Commits added:

- `92a3a06` — `Add Noon partner skeleton draft`
- `7673a17` — `Add Adani exact-bind audit`

Generated artifacts:

- `NOON-PARTNER-SKELETON-2026-06-20.md`
- `noon.partner-skeleton.draft.json`
- `noon-skeleton-derivation-2026-06-20.json`
- `ADANI-EXACT-BIND-AUDIT-2026-06-20.md`
- `adani-exact-bind-audit-2026-06-20.json`

Noon status:

- Built a schema-valid, review-safe draft object. It is **not** a live partner JSON replacement.
- Scope is derived from `handoff/partner-map-model/uae-gulf-shared-corridor-spine.json` using `usable_by_noon = true` and `current_geometry_status = geometry_present`.
- Derived Noon route pools remain: `452` domestic UAE, `18` selected inter-emirate UAE, and `14` UAE/Gulf cross-border amber-only.
- Derived scope IDs are generated from endpoints, not hand-listed. Active UAE IDs: `abu-dhabi-uae`, `dubai-uae`, `fujairah-uae`, `ras-al-khaimah-uae`, `sharjah-uae`. Non-UAE IDs stay amber/future: `doha-qatar`, `manama-bahrain`, `muscat-oman`.
- All route IDs remain null until Grok seals canonical IDs. Schema validation passed against `partner-pitch/schema/partner_proposal.schema.json`.

Adani status:

- Official Adani source confirms the asset list, but the current 97-route India spine does not have exact Adani asset/BP label hits.
- Audit result: `12` assets have no existing Atlas scope/label hit; `2` assets — Mormugao and Vizhinjam — are only broad city/market-scope candidates because Goa/Kerala exist in the spine, with no exact BP/asset alias yet.
- No Adani asset is promoted to partner footprint or economics. Goa/Mormugao and Kerala/Vizhinjam need exact boarding-point/alias verification first; Gujarat, Tamil Nadu/Chennai, Andhra/Vizag, West Bengal, and Odisha stay registry expansion / exact-bind backlog.

Next execution slice:

1. Hand the Noon skeleton to Grok for route-ID seal and side-panel render QA.
2. If continuing Tasklet-side first, build the actual Grok CI prompt/package around `noon.partner-skeleton.draft.json` and `noon-skeleton-derivation-2026-06-20.json`.
3. Keep Adani/Reliance out of live partner footprint until exact binds are resolved.

## Noon Grok CI seal/render QA handoff — added to PR #58

Commit added:

- `23b9e51` — `Add Noon Grok CI seal handoff`

Generated artifacts:

- `NOON-GROK-CI-SEAL-RENDER-QA-2026-06-20.md`
- `noon-grok-ci-seal-render-qa-2026-06-20.json`

Status:

- The Noon skeleton now has a deterministic Grok CI handoff for anchor-city ID crosswalk, route-ID sealing, render-safe draft generation, and render QA.
- Active scope remains UAE-only: Abu Dhabi, Dubai, Fujairah, Ras Al Khaimah, and Sharjah.
- Doha, Manama, and Muscat remain amber/future scope only.
- The handoff explicitly flags the anchor-city ID risk from country-suffixed draft IDs versus internal Atlas renderer IDs.
- The handoff carries the featured-route seal queue and requires Grok to keep route IDs null unless canonical IDs can be deterministically sealed.
- Economics cascade remains blocked until route IDs and render QA pass.

Storage note:

- Removed the duplicated local `uae-gulf-shared-corridor-spine.json` from Tasklet private storage after it had already been committed to PR #58, to make room for the new handoff files. GitHub remains the source of truth.

Next execution slice:

1. Move from handoff to actual Grok CI execution: anchor-city crosswalk + route seal + render QA ledgers.
2. If staying Tasklet-side first, prepare the exact GitHub issue/comment text for Grok and include PR #58 artifact paths.
3. Keep Adani/Reliance parked as overlay/exact-bind backlog until exact BP/asset aliases are validated.

## Noon Grok execution command — posted on PR #58

Commit/comment added:

- `9789d1f` — `Add Noon Grok execution command packet`
- PR #58 comment id: `4759130922`

Generated artifact:

- `NOON-GROK-EXECUTION-COMMAND-2026-06-20.md`

Status:

- A paste-ready deterministic execution command is now both committed to PR #58 and posted as a PR comment.
- Command directs Grok to produce:
  - `partner-pitch/NOON-ANCHOR-CITY-CROSSWALK.json`
  - `handoff/partner-map-model/noon-route-seal-ledger.json`
  - render-safe Noon partner draft/live JSON per CI branch policy
  - `handoff/partner-map-model/noon-render-qa-ledger.json`
- Gates remain unchanged: UAE-only active scope; non-UAE Gulf amber/future; KSA/Egypt coverage-note/future; no Adani/Reliance promotion; no invented route IDs; economics pending until seal/render QA pass.

Next execution slice:

1. Monitor/respond to Grok CI output on PR #58.
2. If no CI output appears, run a Tasklet-side pre-crosswalk from available city brief IDs to pre-empt the known `*-uae` renderer-ID mismatch risk.
3. Continue Adani exact-bind research only as source-led backlog, with no footprint promotion.

## Tasklet-independent India/GCC continuation — source/narrative slices banked on PR #58

Completed autonomous Tasklet-owned slices after the Noon Grok packet:

- `d10d6cf` — Add India market evidence and partner narrative drafts
  - `handoff/partner-map-model/INDIA-MARKET-EVIDENCE-BANK-2026-06-20.json`
  - `handoff/partner-map-model/INDIA-PARTNER-NARRATIVE-DRAFTS-2026-06-20.md`
- `1ae55aa` — Add Uber India city evidence extract
  - `handoff/partner-map-model/UBER-INDIA-CITY-EVIDENCE-EXTRACT-2026-06-20.json`
  - `handoff/partner-map-model/UBER-INDIA-CITY-EVIDENCE-EXTRACT-2026-06-20.md`
- `9066546` — Add India market subproposal blocks
  - `handoff/partner-map-model/INDIA-MARKET-SUBPROPOSAL-BLOCKS-2026-06-20.md`
  - `handoff/partner-map-model/INDIA-MARKET-SUBPROPOSAL-BLOCKS-2026-06-20.json`
- `295fe90` — Add India demand anchor queue
  - `handoff/partner-map-model/INDIA-DEMAND-ANCHOR-QUEUE-2026-06-20.json`
  - `handoff/partner-map-model/INDIA-DEMAND-ANCHOR-QUEUE-2026-06-20.md`
- `bd36a4b` — Add Adani Reliance exact bind queue
  - `handoff/partner-map-model/ADANI-RELIANCE-EXACT-BIND-QUEUE-2026-06-20.json`
  - `handoff/partner-map-model/ADANI-RELIANCE-EXACT-BIND-QUEUE-2026-06-20.md`

Current Tasklet-independent status:

- India evidence bank now covers Goa, Mumbai/Navi Mumbai, Kerala/Kochi, Andaman, Gujarat, Chennai/TN, Vizag/Andhra, and Kolkata-Haldia/West Bengal.
- Rapido/Ola/Uber India derivative narrative drafts are banked.
- Per-market sub-proposal prose blocks are banked with local-use-case gates explicit.
- Uber official India city evidence was extracted into candidate buckets. Counts are broad/source-supported but still require Atlas alias review before display.
- Demand anchor queue separates strong narrative anchors from cleanup leads. Finance model must wait for route seal and final source cleanup.
- Adani/Reliance remain no-promotion overlay/backlog. Exact-bind queue is explicit.

Remaining Tasklet-owned bites:

1. Build final partner assembly specs for Rapido India, Ola India, and Uber India derivative from the narrative/evidence bank.
2. Clean high-value demand anchors: Andaman official tourism table, official airport passenger sources, Gujarat route/fare/capacity source, ferry fare comparables.
3. Build an Atlas-alias search/crosswalk queue for India expansion terms once repo state is available or Grok returns seal output.
4. Prepare the next Grok-safe command packet for India partner derivative assembly after evidence cleanup.

### Additional Tasklet-owned India assembly artifacts

- `d0e5cde` — Add India partner assembly specs
  - `handoff/partner-map-model/INDIA-PARTNER-ASSEMBLY-SPECS-2026-06-20.json`
  - `handoff/partner-map-model/INDIA-PARTNER-ASSEMBLY-SPECS-2026-06-20.md`
- `56075a8` — Add India derivative Grok-ready draft packet
  - `handoff/partner-map-model/INDIA-PARTNER-DERIVATIVE-GROK-READY-PACKET-2026-06-20.md`
  - `handoff/partner-map-model/INDIA-PARTNER-DERIVATIVE-GROK-READY-PACKET-2026-06-20.json`
- PR #58 update comment posted: `4759220929`

Updated status:

- Tasklet has now banked the India partner assembly plan for Rapido India, Ola India, and Uber India derivative.
- The next deterministic packet is prepared but explicitly marked draft/not-for-execution until Noon seal/render output and India crosswalk review are stable.
- Remaining Tasklet cleanup is source/alias work, not narrative structure: Andaman tourism capture, airport/traffic anchors, Gujarat route/fare/capacity cleanup, ferry fare comparables, and alias/crosswalk queue.

### India finish pass — source hardening, crosswalk hygiene, partner blocks

Closed the requested remaining India slice:
- Source hardening: Gujarat RoPax upgraded to clean official PIB + Gujarat Maritime Board anchors; Andaman tourism numeric fallback captured from IBEF with the primary Andaman Tourism table still marked as unreachable/source-lead; AAI airport traffic quarantined until direct AAI PDF/page capture works.
- Exact-bind hygiene: built a pre-crosswalk city/BP mismatch table. Goa, Mumbai, Kerala/Kochi and Andaman have usable Atlas city/BP scope; Gujarat, Chennai/TN India-side, Vizag/Andhra, and Kolkata-Haldia remain null/backlog where current branch search found no exact city/BP hit.
- Adani/Reliance: preserved overlay-only/no-footprint. Mormugao has BP hits but no partner promotion; other Adani/Reliance asset aliases remain null/backlog.
- Partner package finalization: final proposal-ready blocks produced for Rapido India, Ola India, Uber India derivative, and Adani/Reliance overlay lanes. All partner-package route IDs remain null unless sealed.
- Grok handoff timing: India derivative packet remains parked/non-executable until Noon output and crosswalk state are stable.

Artifacts:
- `/tasklet/agent/home/INDIA-SOURCE-HARDENING-CLOSURE-2026-06-20.json`
- `/tasklet/agent/home/INDIA-PRE-CROSSWALK-CITY-ID-MISMATCH-TABLE-2026-06-20.json`
- `/tasklet/agent/home/INDIA-PARTNER-PROPOSAL-READY-BLOCKS-FINAL-2026-06-20.md`
