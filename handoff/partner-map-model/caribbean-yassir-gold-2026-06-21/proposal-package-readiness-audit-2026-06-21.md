# Proposal package readiness audit — Caribbean Mobility + Yassir — 2026-06-21
This converts the definition of done into explicit pass/held gates for PR #65. It is a control checklist, not a render receipt.
## Scope lock
- **Caribbean Mobility:** generic regional partner proposal; no named operator footprint claims; route/economics rows stay preflight until Grok seals exact IDs.
- **Yassir:** Morocco/Tunisia are current display/economics scope; Algeria is first-class but held behind mint/seal/economics gates.
## Summary
- Source inventory: **29 rows** (yassir: 3, caribbean-mobility: 16, shared_or_unknown: 10).
- Anchor-city crosswalk: Caribbean **24/24 OK**; Yassir **18/18 OK**.
- Missing/held repo artifacts now explicit: `data-clean/partners/yassir.json`, `data-clean/partners/caribbean-mobility.json`.
## Caribbean Mobility gates
- **C-01 — Source-backed regional market footprint**: PASS. 16 Caribbean/source rows banked; 11 partner-generic market sections authored. Next: Keep generic until a named operator is approved.
- **C-02 — Unsupported geography guardrail**: PASS. Partner JSON uses existing Atlas Caribbean anchor IDs; route IDs remain null. Next: Do not claim named partner footprint or create new BPs without Grok seal.
- **C-03 — Anchor-city render crosswalk**: PASS. 24 / 24 anchor-city checks OK. Next: Grok should render-check against sealed city_id, not filenames.
- **C-04 — Country-reference preflight**: PASS — preflight. Draft country-reference batch exists for 5 country rows. Next: Review/accept rows before editing finance/model/country-reference.json.
- **C-05 — Route-economics conversion**: PASS — preflight. 5 route-economics inputs converted; 3 markets explicitly blocked/not modeled. Next: Seal exact route IDs and assumptions before cascade.
- **C-06 — Live finance cascade / growth_case**: HELD. No live Caribbean corridors/country-reference/model rows changed; partner JSON intentionally has no growth_case. Next: After Grok seal + assumption acceptance, add approved rows and run aggregate/growth cascade.
- **C-07 — Data-clean partner artifact**: HELD. data-clean/partners/caribbean-mobility.json is absent on PR #65 branch; this is now explicit. Next: Have Grok generate/seal data-clean only after deterministic route/city binding.
- **C-08 — Deck Studio package**: PASS. deck-studio/decks/caribbean-mobility has deck.config, content-source, image-manifest, and slide-manifest. Next: Bind/create live deck ID and pull object inventory before edits.
- **C-09 — Grok seal queue / unresolved gaps**: PASS. Caribbean economics sidecar draft and deck readiness queue identify route/country/economics gaps. Next: Return unresolved gaps separately; preserve nulls.
## Yassir gates
- **Y-01 — Source-backed Yassir footprint**: PASS — scoped/partial. 3 Yassir rows plus Algeria packets; display/economics scope remains Morocco/Tunisia only. Next: Keep Yassir source claims tiered; do not assume unsupported cities.
- **Y-02 — Algeria home-market treatment**: PASS — held from live scope. Algeria source/mint packet has 8 candidate cities; route hardening has 5 source-backed candidates. Next: Grok must mint/validate Algeria city IDs, BPs, and routes before display/economics.
- **Y-03 — Anchor-city render crosswalk**: PASS. 18 / 18 anchor-city checks OK for current Morocco/Tunisia display scope. Next: Render-check market cards against sealed city_id.
- **Y-04 — Partner JSON narrative/sub-markets**: PASS. Yassir JSON has 2 full market sections and 4 route-ID-null journey candidates. Next: Promote Algeria only after exact seal.
- **Y-05 — Economics cascade for current scope**: PASS — current scope. agg-yassir.json, growth-yassir.json, _growth-draft/yassir.growth.json, and yassir_unit_econ.xlsx are staged for Morocco/Tunisia. Next: Upload/replace economics Sheet only through approved in-place path after review.
- **Y-06 — Algeria economics cascade**: HELD. algeria-country-reference-draft.json exists, but no live Algeria model rows are included. Next: Add accepted Algeria country-reference + route rows after Grok seal, then rerun cascade.
- **Y-07 — Exact route IDs**: HELD — Grok. Authored route IDs remain null until deterministic sealing. Next: Bind only exact route IDs; return null for unresolved endpoints.
- **Y-08 — Data-clean partner artifact**: HELD. data-clean/partners/yassir.json is absent on PR #65 branch; current package is handoff/partner-pitch first. Next: Have Grok generate/seal data-clean after render graph QA.
- **Y-09 — Deck Studio package**: PASS. deck-studio/decks/yassir has deck.config, content-source, image-manifest, and slide-manifest. Next: Bind/create live deck ID and pull object inventory before edits.
## Global holds before full definition of done
- data-clean partner JSONs are absent and should be generated/sealed by Grok after deterministic route/city binding.
- No live Google Slides IDs are bound yet; Deck Studio configs intentionally retain pending deck IDs.
- Caribbean economics are draft/preflight only; no live model cascade or growth_case until route IDs and assumptions are accepted.
- Yassir Algeria is source-backed but not display/economics-ready until sealed Algeria city IDs, BPs, route IDs, country-reference row, and route-level demand/fare anchors exist.
- Grok render receipts, duplicate-corridor checks, deck QA receipts, and unresolved-gap return packet are still required.
## Next recommended bite
- Ask Grok to execute the seal/render/data-clean pass using the handoff prompt and this audit as the checklist.
- If Tasklet continues before Grok, only add source hardening or specs; do not fabricate data-clean, route IDs, or live economics.
- After Grok returns IDs, cascade approved economics and include the economics sidecar in the gold export/package.
## Non-negotiables
- Do not invent Caribbean operator footprint claims.
- Do not add Yassir Algeria to display/economics before exact Grok seal.
- Do not replace null route IDs with approximate or filename-based matches.
- Do not create or replace live Slides outside the approved API workflow.
- Do not treat this audit as a validation receipt for front-end render; it is a readiness control checklist.

