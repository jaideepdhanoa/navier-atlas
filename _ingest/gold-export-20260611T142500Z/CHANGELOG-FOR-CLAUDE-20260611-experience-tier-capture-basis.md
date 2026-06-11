# CHANGELOG FOR CLAUDE — 2026-06-11 — experience tier ×4 SEA markets + capture-basis fix (Gold #52)

Lineage: **Gold #52**, parent **Gold #51** (`navier-export-20260610T203354Z.zip`). Pure LB-23 content
zip-patch — **NO geometry work**. Changed entries vs #51: `data-clean/partners/grab.json`,
`data-clean/economics_by_route_id.json`, `data-clean/SEAL.json`, plus this changelog. Every other
entry is byte-identical to #51.

## (a) `partners/grab.json` changed — LB-103 capture-basis recal + LB-98 experience tier

- **NEW `bangkok` market** ("Bangkok / Chao Phraya"): 2 journeys with **`route_id: null`** —
  geometry intentionally pending a river mint. Phase featured_routes also carry `route_id: null`
  (`_link_status: "null-geometry-pending-lb46"`); two placeholder ids (`rn-bkk-exp-hoponhopoff`,
  `rn-bkk-exp-dinner-cruise`) were authored upstream but do not exist in gold, so they were nulled
  per the LB-46 gate (null beats confidently-wrong). Bangkok: `committed_fleet: 10`, phase boats
  `[5, 10]`, `steady_state_ceiling: 10`.
- **Network ladder updated** (capture-basis recal): network `committed_fleet: 231` (was 233),
  `steady_state_ceiling: 1132` (was 1142).
- Per-market ladders updated: **cross-border** `committed_fleet: 13`, phase boats `[6, 6, 13]`,
  ceiling `13`; **singapore** `committed_fleet: 10`, phase boats `[3, 3, 10]`, ceiling `14`;
  plus recalibrated `phases`/`steady_state_ceiling`/`_fleet_basis` on bali, phuket, koh-samui,
  jakarta. (Figures quoted from the shipped file.)

## (b) Economics sidecar regenerated from the LB-103 aggregates

- `data-clean/economics_by_route_id.json`: **105 route-pinned records / 23 `_pending_route_pin`**.
- **Capture is now `pool_basis`-aware**: demand pools already narrowed to *addressable* (or with
  capture pre-applied) are no longer double/triple-discounted by the global 10% capture. Example:
  Singapore ↔ Bintan (`rn-f3670ea7d99b`) vessels_10pct 1 → 4, market_rev $0.59M → $2.36M.
- **Zero resolution regression**: the same 105 route_ids as Gold #51 resolve; nothing lost or
  re-pinned. Pending grew 4 → 23 because 19 NEW LB-98 experience-tier / SG modal-shift corridors
  (singapore ×11, bali ×2, phuket ×2, jakarta ×2, bangkok ×2) entered the model without gold
  geometry — they pend honestly, never fuzzy-attached.
- Every record still carries its `assumptions` block (LB-28-extended) — render on corridor cards.

## (c) NO geometry changes vs Gold #51

`ROUTES.json` (5,280) / `CLUSTERS.json` (75) / `FEATURES_BY_TYPE.json` / `STORIES.json` /
`VESSEL_SPECS.json` are **byte-identical** to #51 (hash-verified against the #51 seal).

## (d) Front-end note

**Bangkok has no routable corridors yet** — render its journeys/featured routes WITHOUT map
links (route_id is null) until the next geometry mint. Absent sidecar record = no economics yet;
never invent.

Gates at seal: endpoint label↔geometry **0 HARD** / 13 weak (same benign set as #51);
`gate_city_ids` **PASS** (198 nodes, 5,280 routes, 75 clusters; `bangkok-thailand` resolves).
