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

## Batch 3 banked: Yassir Algeria market addressed
- Added `yassir-algeria-market-source-and-mint-queue.json` with official Yassir/Google Cloud/YC sources, Algeria city candidates, and a route mint queue.
- Updated `partner-pitch/partners/yassir.json` so Algeria is a first-class home-market unlock, not an omission.
- Kept Algeria out of `markets` and `corridors.json` for now because this branch has no sealed Algeria Atlas IDs and no Algeria country-reference row; exactness over coverage.
- Next gate: Tasklet continues Algeria city/BP evidence hardening; Grok validates/binds/mints IDs only where the evidence is exact, seals routes/render, then Tasklet adds Algeria country-reference + route demand/fare anchors and reruns the Yassir economics cascade.

## Batch 4 banked: Algeria country-reference draft prepared
- Added `algeria-country-reference-draft.json` with draft opex/grid inputs for Algeria.
- Did **not** edit `finance/model/country-reference.json` yet: no Algeria corridors are modeled and the wage/marina sources are still low-confidence.
- Proposed draft row: energy ~$0.04/kWh, grid CO₂ ~0.55 kg/kWh, captain ~$12k/yr, marina overhead ~$8k/yr, cost index ~0.30 — all explicitly source-tiered and gated before cascade.

## 2026-06-21 — Algeria route hardening batch 1
- Added `yassir-algeria-route-source-hardening-batch-1.json` as the first Algeria route/source mint packet.
- Promoted concrete source-backed candidates while keeping live model untouched:
  - A: Algiers Bay — La Pêcherie / Port d’Alger ↔ El Djamila / Aïn Bénian.
  - A-: Algiers Bay — La Pêcherie ↔ Tamentfoust / Les Sablettes axis.
  - A-: Port de Béjaïa ↔ Port d’Alger HSC line.
  - B+: Oran ↔ Mostaganem seasonal ENTMV line.
  - B: Annaba port existence lead only; not model-ready.
- Sources now include ENTMV/Algérie Ferries, Radio Algérienne/APS Algiers Bay, Port de Béjaïa PDF, Radio Algérienne/APS Oran–Mostaganem, Ferryhopper Algeria, and GNV Algiers port page.
- Exactness gate unchanged: Tasklet owns city/BP research; no Algeria render/economics until Grok seals exact route geometry/IDs from that evidence; unresolved endpoints stay null.


## 2026-06-21 — Grok Algeria mint handoff prompt updated
- Updated `GROK-SEAL-AND-DECK-PROMPT.md` to reference the Algeria source/mint queue, country-reference draft, and route hardening batch 1.
- Clarified ownership: Tasklet supplies city/BP evidence; Grok validates/binds/mints exact IDs only as needed and seals routes/render under the null policy.
- Still no live `yassir-algeria` display/economics until Grok returns sealed IDs and route QA.

## Batch 5 banked: Caribbean economics preflight conversion
- Added `caribbean-country-reference-draft-batch-1.json` for Bahamas, Puerto Rico, U.S. Virgin Islands, British Virgin Islands, and Barbados.
- Added `caribbean-route-economics-inputs-batch-1.json` converting the banked demand anchors into first route-economics inputs for Nassau/Paradise Island, San Juan-Cataño, Red Hook-Cruz Bay, St. Thomas-Tortola, and Bridgetown Port waterfront extension.
- Added `caribbean-economics-sidecar-draft-batch-1.md` as the review sidecar.
- No live finance/model rows were changed; route IDs remain null until Grok seals exact geometry and demand/fare assumptions are accepted.


## Batch 6 banked: Deck Studio prep for both proposal lanes
- Added repo-native Deck Studio packages for `caribbean-mobility` and `yassir` under `deck-studio/decks/`.
- Each package now has `deck.config.json`, `content-source.json`, `image-manifest.json`, and `slide-manifest.json`.
- Added `deck-studio-readiness-queue.json` with the Grok deck-bind/create instructions, QA commands, image rules, and known gaps.
- No live Google Slides edits were made; deck IDs are intentionally `PENDING_GROK_CREATE_OR_BIND` until Grok binds or creates the live deck and pulls object inventory.
- Image policy remains canonical N30/N35 compositing, market-specific backgrounds, and no Atlas-generated imagery.

## Batch 7 banked: Proposal-package readiness audit
- Added `proposal-package-readiness-audit-2026-06-21.json` and `.md` to turn the full definition of done into explicit pass/held gates for both lanes.
- Caribbean is marked source/deck/preflight-ready, with live economics/growth/data-clean held until Grok seals exact route IDs and assumptions are accepted.
- Yassir is marked source/deck/economics-ready for the current Morocco/Tunisia scope, with Algeria explicitly first-class; Tasklet owns remaining city/BP research, while route/render sealing and economics unlock stay held behind Grok receipts + country-reference/economics cascade gates.
- Data-clean partner JSONs are intentionally called out as missing/held artifacts, not silently implied.
- This audit is a readiness control checklist; it is not a render receipt.

## Batch 8 correction: City/BP vs route ownership
- Corrected the handoff language: Tasklet owns source-led city and boarding-point research/evidence packs.
- Grok owns deterministic route geometry sealing, route IDs, render checks, and null returns for unresolved routes.
- Grok may validate/bind/mint city/BP IDs only from Tasklet-provided exact evidence; it should not be treated as the primary city/BP research lane.
