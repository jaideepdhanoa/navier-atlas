# Sub-page parity + Phase-3 routes + penang/borneo split — 2026-06-20 (pt.2)

Second parity handoff of the day (follows PR #46). Tasklet content/registry work done; deterministic
bind/render/re-aggregate is Grok's lane.

## What Tasklet did (in this PR)

### 1. Sub-page parity audit (Bolt 14 + Yango 8 = 22 markets)
Full field-level audit vs the Grab reference. **Result: rosters are healthy** — 0 roll-up stubs remain
(the LB-251 promotion already landed), every market carries all 14 top-level parity fields, `vessel_sizing`
present on 22/22, every phase has `use_cases` with non-empty summaries. The **only** structural gap was an
empty **Phase-3 (Mature) `featured_routes`** on 9 markets (Grab carries featured routes on every phase,
incl. Mature — confirmed against grab borneo/jakarta which feature the market's longest leg in Phase 3).

### 2. Phase-3 Mature backbone legs added (9 markets)
Each market's **longest real registry leg** added as the Phase-3 backbone, vessel-gated (LB-252), with real
`from_node_id`/`to_node_id`, `route_id: null` (Grok binds), reusing the market's existing `model_link`.
`_link_status: "pending"`, `_phase3_backbone: true`.

| partner:market | leg | nm | node binding | vessel | render |
|---|---|---|---|---|---|
| bolt:croatia | Dubrovnik → Korčula | 47 | split-croatia (intra) | Pioneer II | (geometry) |
| bolt:egypt | Hurghada/El Gouna → Sharm El Sheikh | 49.8 | hurghada-el-gouna → sharm-el-sheikh (**inter-node**) | Pioneer II | (geometry) |
| bolt:ireland | Dublin Port → Holyhead (Wales) | 67 | dublin-ireland (intra) | Pioneer II | aspirational |
| bolt:italy | Portofino → Cinque Terre | 22 | amalfi-coast-italy (intra) | Pioneer II | (geometry) |
| bolt:portugal | Cais do Sodré → Cascais | 13 | lisbon-tagus-portugal (intra) | Pioneer II | (geometry) |
| yango:cote-divoire | Abidjan → Jacqueville | 22 | abidjan-cote-divoire (intra) | Pioneer II | (geometry) |
| yango:egypt | Hurghada/El Gouna → Sharm El Sheikh | 49.8 | hurghada-el-gouna → sharm-el-sheikh (**inter-node**) | Pioneer II | (geometry) |
| yango:lagos | Lagos → Badagry | 32 | lagos-nigeria (intra) | Pioneer II | (geometry) |
| yango:turkey | Fethiye → Rhodes (Greece) | 42 | istanbul-turkey (intra) | Pioneer II | aspirational |

All ≤70nm → Pioneer II per the range gate. `ireland` and `turkey` flagged `aspirational` (Irish-Sea /
Greece international crossings). Where the longest leg also appears in Phase 2 (ireland Holyhead), that
repeat matches the sealed Grab borneo pattern (longest leg = mature backbone).

### 3. Narrative polish (22 sub-pages)
Scanned for verbatim-repeated narrative (the real boilerplate tell). Pages are already localized — **only one**
shared string existed (Yango cote-divoire/p3 == lagos/p3). Differentiated both, grounded in their new Phase-3
backbone leg (→Jacqueville, →Badagry). No other facts touched.

### 4. penang / borneo de-contamination (corridors.json) — extends the #46 Grab re-aggregate
The `penang` and `borneo` Grab buckets were cross-contaminated: borneo held 10 penang/langkawi rows and
penang held 3 Sabah rows, with heavy duplication. Re-partitioned strictly by node geography with **zero
corridor lost** + dedup:
- **penang** = `penang-malaysia` + `langkawi-malaysia` → 14 rows (matches grab penang anchor_cities)
- **borneo** = `sabah-kota-kinabalu-malaysia` → 3 rows (matches grab borneo anchor_cities)

(removed 9+3 duplicate rows that existed in both buckets — same root cause as the #46 SE-Asia supersets).

## Deterministic actions for Grok
- **Bind `route_id` for the 9 new Phase-3 featured routes** (currently null, `_link_status: pending`) and run
  render-check; finalize `render` (geometry vs aspirational) per the seal.
- **Extend the Grab re-aggregate already specced in PR #46** to include the corrected penang/borneo buckets —
  their TAM was double-counted alongside the bali/jakarta/phuket/bangkok/koh-samui supersets.
- Bolt/Yango economics unaffected by these edits (featured_routes + narrative only; no demand/fare change).

## Files
- `partners/bolt.json`, `partners/yango.json` — 9 Phase-3 legs + 2 differentiated narratives
- `corridors.json` — penang/borneo partition
