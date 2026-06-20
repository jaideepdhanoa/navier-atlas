# Noon — Grok execution command packet (2026-06-20)

Grok: please run the deterministic Noon seal/render lane from PR #58 using these source artifacts:

- `handoff/partner-map-model/NOON-GROK-CI-SEAL-RENDER-QA-2026-06-20.md`
- `handoff/partner-map-model/noon-grok-ci-seal-render-qa-2026-06-20.json`
- `handoff/partner-map-model/noon.partner-skeleton.draft.json`
- `handoff/partner-map-model/noon-skeleton-derivation-2026-06-20.json`
- `handoff/partner-map-model/uae-gulf-shared-corridor-spine.json`

## Execute

1. Build `partner-pitch/NOON-ANCHOR-CITY-CROSSWALK.json`.
   - Resolve draft IDs to renderer/internal Atlas `city_id` values.
   - Watch for country-suffix mismatch (`dubai-uae` may render as internal `dubai`, etc.).
   - No unresolved `ID_MISMATCH` may remain in active scope.

2. Build `handoff/partner-map-model/noon-route-seal-ledger.json`.
   - Use source corridor IDs + BP node IDs from the manifest.
   - Bind canonical `route_id`/`route_ids` only if deterministic.
   - Keep null with reason when not deterministic.

3. Build a render-safe Noon partner draft/live JSON according to CI branch policy.
   - Active UAE only: Abu Dhabi, Dubai, Fujairah, Ras Al Khaimah, Sharjah.
   - Doha, Manama, Muscat remain amber/future only.
   - KSA/Egypt remain coverage-note/future only.
   - No network-footprint card grid.
   - No Adani/Reliance promotion in this lane.

4. Run render QA and write `handoff/partner-map-model/noon-render-qa-ledger.json`.
   - Confirm active UAE markets render.
   - Confirm featured routes render or are explicitly held.
   - Confirm no blank cards and no non-UAE active scope.
   - Confirm economics remain pending unless route seal + model cascade are explicitly run later.

## Hard gates

- Null beats confidently wrong.
- No invented route IDs.
- No active KSA/Egypt/Qatar/Bahrain/Oman map scope in this pass.
- Display is allowed without economics; economics-pending must be explicit.
- Economics cascade starts only after route IDs and render QA are clean.
