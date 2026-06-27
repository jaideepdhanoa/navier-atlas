# GROK SPEC — AirAsia MOVE Phase 2 Seal (Philippines + Singapore)

**Owner:** Grok (deterministic geometry seal + model pass)
**Author:** Tasklet · 2026-06-28
**Branch handed over:** `airasia-move-phase2` (PR open; copy review = Jaideep)
**Base file:** `data-clean/partners/airasia-move.json` (mirror `partner-pitch/partners/airasia-move.json`) — already on PR head.

## What Tasklet already did (do NOT redo)
- Authored 6 Phase-2 sub-pages onto **current main** (preserving the PR #131 Malaysia seal): `manila`, `cebu`, `boracay`, `palawan`, `siargao`, `singapore`.
- Real atlas `city_id` node_ids (all `city_id_resolves:true` in `AIRASIA-AIRPORT-HUB-CROSSWALK.json`).
- **Singapore launches bound:** cross-border legs inherit existing route_ids 1:1 — Batam `rn-2568d40ee060`, Bintan `rn-f3670ea7d99b`, Desaru `rn-5d1a30fbb0a9`, Tioman `ics-1a53f8237d` (roadmap). Same physical corridors as the sealed Riau/Desaru/Tioman registry entries.
- All Philippines journeys: `route_id:null`, `economics_status:model-pass-pending` (no fabrication).
- Added 6 `network_footprint` nodes (Singapore `render:"geometry"`; PH 5 `render:"label"`, `_seal_status:"mint-pending"`).
- Updated copy stats (Countries→5, Coastal gateways→21), `coverage_note`, `_provenance.phase2`.
- Schema parity verified against the live `langkawi` market (none/none key diff). QA gates: jargon-clean, anchors resolve, economics honest, node-ids resolve — 0 problems.

## Seal scope for Grok
1. **Mint the 18 Philippines corridors + `route_id`s** across the 5 PH markets, bind into BOTH `data-clean/` and `partner-pitch/` copies:
   - **manila** (4): Manila Bay↔Corregidor (26nm) · Manila Bay↔Nasugbu/Pico de Loro & Anvaya (48nm) · Manila Bay↔Subic (60nm) · Manila Bay↔Bataan/Las Casas (32nm). All node_ids = `manila-philippines`.
   - **cebu** (4): Cebu(Mactan)↔Bohol/Panglao (37nm) · Mactan↔Mactan resorts (3nm) · Cebu↔Camotes (26nm) · Cebu↔Malapascua/Bantayan (34nm). node_ids = `cebu-philippines`.
   - **boracay** (3): Caticlan↔Boracay (2nm) · Caticlan↔Boracay Station 1 (3nm) · Boracay↔Carabao (6nm). node_ids = `boracay-philippines`.
   - **palawan** (4): El Nido↔Bacuit Bay islands (10nm) · Puerto Princesa↔Honda Bay (8nm) · Coron↔Coron Bay (12nm) · Puerto Princesa↔El Nido coastal (125nm, **Quanta-LR roadmap**). node_ids = `palawan-philippines`.
   - **siargao** (3): General Luna↔Bucas Grande/Sohoton (22nm) · General Luna↔Naked/Daku/Guyam (5nm) · Dapa↔Dinagat (24nm). node_ids = `siargao-philippines`.
   - Intra-island legs follow the Malaysia pattern (origin=dest city_id). Distances above are authoring estimates — correct to registry geometry where it differs; **null beats confidently-wrong**.
2. **Cluster registry:** add the PH anchor clusters (manila, cebu, boracay, palawan, siargao) and the Singapore cross-border cluster to `CLUSTERS.json`, then run `scripts/partner-scope.mjs` to regenerate `_map_scope` (it is auto-synced; Tasklet did NOT hand-edit it).
3. **Footprint render flags:** after minting, flip the 5 PH `network_footprint` entries from `render:"label"` → `render:"geometry"` and clear `_seal_status`. Singapore is already `geometry`.
4. **`_philippines_seal` block:** add a seal block mirroring `_malaysia_seal` (timestamp, bindings count, `route_map`).
5. **Model pass (economics):** PH + SG `growth_case` stays `model-pass-pending` until the arriving-seat distribution-capture model runs (anchors in `AIRASIA-DEMAND-ANCHORS.json`; capture band per Jaideep). Bind `economics_url` + route-keyed sidecar against new gold afterward. **No invented numbers in the seal.**

## Held / explicit nulls
- All 18 PH `route_id`s = null until mint.
- PH `growth_case` numerics = null (model-pass-pending).
- Singapore↔Tioman = `ics-1a53f8237d`, **roadmap** (Quanta-LR, H2 2026+) — not a now-leg.
- Palawan PP↔El Nido coastal (125nm) = Quanta-LR roadmap.
- `_map_scope` PH/SG city_ids absent until `partner-scope.mjs` regen (depends on CLUSTERS.json add).

## Handback contract (required)
branch name · PR link · commit SHA · exact files changed · validation/render receipt · explicit nulls/held items. No self-certified completion, no line-range audits.
