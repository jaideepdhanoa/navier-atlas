# Proposal package readiness audit — Caribbean Mobility + Yassir — 2026-06-21
This converts the definition of done into explicit pass/held gates for PR #65. It is a control checklist, not a render receipt.
## Scope lock
- **Caribbean Mobility:** generic regional partner proposal; no named operator footprint claims; route/economics rows stay preflight until Grok seals exact IDs.
- **Yassir:** Morocco/Tunisia are current display/economics scope; Algeria is first-class. Tasklet owns remaining city/BP research; Grok owns route seal/render receipts before economics/display unlock.
## Summary
- Source inventory: **29 rows** (yassir: 3, caribbean-mobility: 16, shared_or_unknown: 10).
- Anchor-city crosswalk: Caribbean **24/24 OK**; Yassir **18/18 OK**.
- Missing/held repo artifacts now explicit: `data-clean/partners/yassir.json`, `data-clean/partners/caribbean-mobility.json`.
## Caribbean Mobility gates
- **C-01 — Source-backed regional market footprint**: PASS. 16 Caribbean/source rows banked; 11 partner-generic market sections authored. Next: Keep generic until a named operator is approved.
- **C-02 — Unsupported geography guardrail**: PASS. Partner JSON uses existing Atlas Caribbean anchor IDs; route IDs remain null. Next: Do not claim named partner footprint or promote new BPs without Tasklet evidence and Grok route/render seal.
- **C-03 — Anchor-city render crosswalk**: PASS. 24 / 24 anchor-city checks OK. Next: Grok should render-check against sealed city_id, not filenames.
- **C-04 — Country-reference preflight**: PASS — preflight. Draft country-reference batch exists for 5 country rows. Next: Review/accept rows before editing finance/model/country-reference.json.
- **C-05 — Route-economics conversion**: PASS — preflight. 5 route-economics inputs converted; 3 markets explicitly blocked/not modeled. Next: Tasklet keeps assumptions/evidence explicit; Grok seals exact route IDs before cascade.
- **C-06 — Live finance cascade / growth_case**: HELD. No live Caribbean corridors/country-reference/model rows changed; partner JSON intentionally has no growth_case. Next: After Grok route seal + assumption acceptance, Tasklet adds approved rows and runs aggregate/growth cascade.
- **C-07 — Data-clean partner artifact**: HELD. data-clean/partners/caribbean-mobility.json is absent on PR #65 branch; this is now explicit. Next: Have Grok generate/seal data-clean only after deterministic route/city binding.
- **C-08 — Deck Studio package**: PASS. deck-studio/decks/caribbean-mobility has deck.config, content-source, image-manifest, and slide-manifest. Next: Bind/create live deck ID and pull object inventory before edits.
- **C-09 — Grok seal queue / unresolved gaps**: PASS. Caribbean economics sidecar draft and deck readiness queue identify route/country/economics gaps. Next: Return unresolved gaps separately; preserve nulls.
## Yassir gates
- **Y-01 — Source-backed Yassir footprint**: PASS — scoped/partial. 3 Yassir rows plus Algeria packets; display/economics scope remains Morocco/Tunisia only. Next: Keep Yassir source claims tiered; do not assume unsupported cities.
- **Y-02 — Algeria home-market treatment**: PASS — held from live scope. Algeria source/mint packet has 8 candidate cities; route hardening has 5 source-backed candidates. Next: Tasklet continues Algeria city/BP evidence hardening; Grok validates/binds/mints exact IDs only where needed and seals routes/render before display/economics.
- **Y-03 — Anchor-city render crosswalk**: PASS. 18 / 18 anchor-city checks OK for current Morocco/Tunisia display scope. Next: Render-check market cards against sealed city_id.
- **Y-04 — Partner JSON narrative/sub-markets**: PASS. Yassir JSON has 2 full market sections and 4 route-ID-null journey candidates. Next: Promote Algeria only after Tasklet city/BP evidence is ready and Grok route/render seal succeeds.
- **Y-05 — Economics cascade for current scope**: PASS — current scope. agg-yassir.json, growth-yassir.json, _growth-draft/yassir.growth.json, and yassir_unit_econ.xlsx are staged for Morocco/Tunisia. Next: Upload/replace economics Sheet only through approved in-place path after review.
- **Y-06 — Algeria economics cascade**: HELD. algeria-country-reference-draft.json exists, but no live Algeria model rows are included. Next: Add accepted Algeria country-reference + route rows after Grok seal, then rerun cascade.
- **Y-07 — Exact route IDs**: HELD — Grok. Authored route IDs remain null until deterministic sealing. Next: Bind only exact route IDs; return null for unresolved endpoints.
- **Y-08 — Data-clean partner artifact**: HELD. data-clean/partners/yassir.json is absent on PR #65 branch; current package is handoff/partner-pitch first. Next: Have Grok generate/seal data-clean after render graph QA.
- **Y-09 — Deck Studio package**: PASS. deck-studio/decks/yassir has deck.config, content-source, image-manifest, and slide-manifest. Next: Bind/create live deck ID and pull object inventory before edits.
## Global holds before full definition of done
- data-clean partner JSONs are absent and should be generated/sealed only after deterministic route/city render checks; Tasklet supplies source evidence, Grok supplies route/render receipts.
- No live Google Slides IDs are bound yet; Deck Studio configs intentionally retain pending deck IDs.
- Caribbean economics are draft/preflight only; no live model cascade or growth_case until route IDs and assumptions are accepted.
- Yassir Algeria is source-backed but not display/economics-ready until Tasklet city/BP evidence, sealed route IDs, country-reference row, and route-level demand/fare anchors exist.
- Grok render receipts, duplicate-corridor checks, deck QA receipts, and unresolved-gap return packet are still required.
## Next recommended bite
- Tasklet should continue city/BP/source hardening where evidence is incomplete.
- Ask Grok to execute route seal/render/data-clean only against Tasklet-provided evidence and this audit checklist.
- After Grok returns IDs, cascade approved economics and include the economics sidecar in the gold export/package.
## Non-negotiables
- Do not invent Caribbean operator footprint claims.
- Do not add Yassir Algeria to display/economics before Tasklet city/BP evidence is exact and Grok route/render seal succeeds.
- Do not replace null route IDs with approximate or filename-based matches.
- Do not create or replace live Slides outside the approved API workflow.
- Do not treat this audit as a validation receipt for front-end render; it is a readiness control checklist.

