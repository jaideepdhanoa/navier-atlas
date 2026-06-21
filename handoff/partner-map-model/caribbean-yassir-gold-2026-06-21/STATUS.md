# Caribbean Mobility + Yassir Gold-Standard Build Status — 2026-06-21

## What is now banked
- `partner-pitch/partners/yassir.json` created at Grab/Careem narrative depth, with two full sub-markets and route-ID-null featured routes.
- `finance/model/corridors.json` now has `yassir-tunisia` and `yassir-morocco`, cloned only from existing Atlas/Yango-supported Morocco/Tunisia corridors and labelled `country_supported`.
- `finance/recal/agg-yassir.json`, `finance/growth-yassir.json`, and `_growth-draft/yassir.growth.json` generated. Yassir is modeled for Morocco/Tunisia only; Algeria is held.
- `partner-pitch/partners/caribbean-mobility.json` created as a partner-generic regional mobility proposal with full market sub-pages over existing Atlas Caribbean IDs.
- Source inventory and gap queue saved in this handoff folder.

## Gold-standard gates
- Exactness over coverage: passed. Algeria is not displayed/modelled. Caribbean economics are not invented.
- Anchor-city ID match: preliminary pass uses existing `data-clean/FEATURES_BY_TYPE.json` IDs for every new market card.
- Economics: Yassir Morocco/Tunisia cascaded; Caribbean blocked pending country-reference + route-demand anchors.
- Deck Studio: content-ready; no live deck edit or image generation applied.
- Grok handoff: next step is deterministic route binding/seal after PR review, with route IDs left null.

## Next recursive bites
1. Build Caribbean country-reference rows with source-tiered assumptions.
2. Source route-specific demand anchors for the first 3 Caribbean prove markets: Bahamas, Puerto Rico, USVI/BVI.
3. Assemble Grok seal package for Yassir Morocco/Tunisia and Caribbean geometry render QA.
4. Publish/update economics Sheets in place once approved IDs exist; include sidecar in gold export.

## Batch 2 banked: Caribbean demand-anchor leads
- Added `caribbean-demand-anchor-research-batch-1.json` covering Bahamas, Puerto Rico, USVI/BVI, and Barbados.
- These are *not* final economics; they are source-backed prioritization and route-candidate anchors for the next model pass.
- Next hard gate: country-reference rows + route-level passenger/fare assumptions before any Caribbean economics cascade.
