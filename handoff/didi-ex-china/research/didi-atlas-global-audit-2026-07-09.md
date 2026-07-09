# DiDi Atlas global coverage audit — 2026-07-09

**Repository:** `/tmp/navier-atlas`  
**Commit:** `ae1b96917eaed901a84302b856ce53f6efd767ae` — fix(noon): #207 UAE economics cascade — inherit careem L3 + refresh growth_case  
**Scope:** Australia, New Zealand, Japan, Egypt, South Africa, Singapore, South Korea  
**Source discipline:** repository evidence only; no geographic inference and no repo source files modified.

> **Classification semantics.** The lane label is for the **DiDi partner layer**. Every assigned canonical cluster already exists in Atlas. `not_in_atlas` below means “not evidenced/included in the DiDi Atlas layer at this commit,” not “missing from `CLUSTERS.json`.” Four official-country-list markets qualify as `new_display_coverage`; the other three stay unconfirmed until direct/JV/aggregation/historical status is sourced.

## Executive findings

1. **The assigned expansion is absent:** 0/7 clusters, 0/25 member cities, and 0/7 full market subproposals are in DiDi’s current layer. Australia, New Zealand, Japan, and Egypt have official country-list evidence and are `new_display_coverage`; South Africa, Singapore, and South Korea have no current DiDi source row in the audited repo and must not be called direct footprint.
2. **The displayed economics are stale and non-reproducible:** the partner page shows a **$5,768,158 grounded floor, 16 boats, 35 sourced corridors and 341 greenfield corridors**, while `agg-didi.json` has **0 corridors** and `growth-didi.json` is null/zero.
3. **The finance spine has no identity:** `corridors-didi.json` holds 38 corridors, but the scoped market key is exactly `didi`; 0/38 scoped route IDs overlap the 9 proposal featured IDs, and only 8/38 exist in current `ROUTES.json`.
4. **DiDi borrows Grab’s census:** `growth-didi.json` names `grab-greenfield-census.json`. All 38 scoped demand records are T3 `bite2/econ_sidecar_inherit`, not DiDi-specific anchors.
5. **Country-cost preflight fails:** New Zealand, Japan, South Africa and South Korea/Korea are missing from `country-reference.json`, which would trigger silent Singapore-cost fallback in a future cascade.
6. **Atlas itself is substantial but not perfectly clean:** 728 raw assigned-country routes, 701 strict-valid routes, 1,780 POIs and 53 external BPs. New Zealand has 10 Kotor routes mis-stamped into the cluster; Korea has 7 nonmember routes; Singapore has 2 nonmember and 8 quarantined routes.
7. **Narrative/copy are the bright spot:** all current DiDi market anchor IDs resolve; DiDi carries all five slide-2 source fields; copy audit passes with 0 leaks. These do not cure the missing geography, stale finance, or absent sheet/deck receipts.

## Summary counts

| Metric | Count |
|---|---:|
| Countries / canonical clusters | 7 |
| Member cities | 25 |
| Official-country-list presence | 4 |
| Direct vs JV disambiguated by repo | 0 |
| Confirmed direct footprint in repo | 0 |
| Confirmed JV / aggregation / historical classification in repo | 0 |
| Confirmed country presence, operating model unresolved | 4 |
| Unconfirmed watchlist countries | 3 |
| Current DiDi clusters | 0 |
| Current DiDi assigned cities | 0 |
| Assigned full subproposals | 0 |
| Atlas routes (raw) | 728 |
| Atlas routes (strict valid) | 701 |
| POIs | 1780 |
| External BPs | 53 |
| Canonical marquee wow | 5 |
| Canonical marquee featured | 6 |
| Finance rows (raw; includes peer duplicate treatment) | 38 |
| Finance corridor signatures | 28 |
| Country references present | 3 |
| Country references missing | 4 |

**Cluster classifications:** `{"new_display_coverage": 4, "not_in_atlas": 3}`  
**City classifications:** `{"new_display_coverage": 19, "not_in_atlas": 6}`

## Country / cluster rollup

| Country | Stable cluster ID | Member cities | DiDi evidence / operating model | Class | Routes raw / strict | POIs / external BPs | Marquee wow / featured | Finance markets: rows / unique signatures | Brief maturity |
|---|---|---:|---|---|---:|---:|---:|---|---|
| Australia | `australia` | 4 | `confirmed_current_country_presence`; `not_disambiguated_direct_vs_aggregation_or_jv` | `new_display_coverage` | 92 / 92 | 273 / 0 | 0 / 0 | none: 0 / 0 | `city_led_partial_no_cluster_brief` |
| New Zealand | `new-zealand` | 3 | `confirmed_current_country_presence`; `not_disambiguated_direct_vs_aggregation_or_jv` | `new_display_coverage` | 52 / 42 | 173 / 0 | 0 / 0 | none: 0 / 0 | `city_led_partial_no_cluster_brief` |
| Japan | `japan` | 8 | `confirmed_current_country_presence`; `not_disambiguated_direct_vs_aggregation_or_jv` | `new_display_coverage` | 161 / 161 | 667 / 0 | 0 / 0 | none: 0 / 0 | `first_class_cluster_and_city_coverage` |
| Egypt | `egypt` | 4 | `confirmed_current_country_presence`; `not_disambiguated_direct_vs_aggregation_or_jv` | `new_display_coverage` | 179 / 179 | 166 / 0 | 0 / 0 | `bolt-egypt`, `yango-egypt`: 20 / 10 | `first_class_cluster_brief_with_city_gaps` |
| South Africa | `south-africa` | 1 | `no_current_repository_confirmation`; `aggregation_jv_or_historical_status_unverified_in_repo` | `not_in_atlas` | 9 / 9 | 66 / 0 | 0 / 0 | none: 0 / 0 | `city_led_partial_no_cluster_brief` |
| Singapore | `singapore` | 1 | `no_current_repository_confirmation`; `aggregation_jv_or_historical_status_unverified_in_repo` | `not_in_atlas` | 196 / 186 | 107 / 53 | 5 / 6 | `singapore`: 18 / 18 | `city_led_complete_no_cluster_brief` |
| South Korea | `korea` | 4 | `no_current_repository_confirmation`; `aggregation_jv_or_historical_status_unverified_in_repo` | `not_in_atlas` | 39 / 32 | 328 / 0 | 0 / 0 | none: 0 / 0 | `first_class_cluster_and_city_coverage` |

### Footprint interpretation

- **Confirmed country presence, operating model unresolved:** `australia`, `new-zealand`, `japan`, `egypt`. The repo records official homepage structured country links but only `country_scope_only_not_city_bound`. It does **not** say whether each is direct, JV, aggregation or another operating model.
- **No current repository confirmation:** `south-africa`, `singapore`, `korea`. These are valid Atlas clusters but requested-market watchlist items for DiDi. Historical, corporate, aggregation or JV association is not enough for current consumer-footprint inclusion without a source row.
- **No true registry gaps:** all 7 clusters and all 25 member city IDs are canonical and present. The work is partner inheritance/status research, not city invention.

## Exact city inventory

`R` = incident raw routes; `S` = strict-valid incident routes; POIs match `FEATURES_BY_TYPE.json::poi[].properties.parent_city_id`; external BP counts come only from `atlas-external/boarding-points/<city_id>.json`.

| Country / cluster | Stable city ID | Class | R / S | POI / external BP | Marquee wow / featured | Current DiDi map / footprint / anchor / full page | Brief maturity |
|---|---|---|---:|---:|---:|---|---|
| Australia / `australia` | `brisbane-australia` | `new_display_coverage` | 20 / 20 | 23 / 0 | 0 / 0 | 0/0/0/0 | `narrative_only_no_signature_routes` |
| Australia / `australia` | `gold-coast-australia` | `new_display_coverage` | 16 / 16 | 83 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| Australia / `australia` | `sydney-australia` | `new_display_coverage` | 41 / 41 | 115 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| Australia / `australia` | `whitsundays-australia` | `new_display_coverage` | 15 / 15 | 52 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| New Zealand / `new-zealand` | `auckland-new-zealand` | `new_display_coverage` | 28 / 28 | 127 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| New Zealand / `new-zealand` | `bay-of-islands-new-zealand` | `new_display_coverage` | 10 / 10 | 42 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| New Zealand / `new-zealand` | `wellington-new-zealand` | `new_display_coverage` | 4 / 4 | 4 / 0 | 0 / 0 | 0/0/0/0 | `missing` |
| Japan / `japan` | `hokkaido-niseko-japan` | `new_display_coverage` | 13 / 13 | 60 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| Japan / `japan` | `izu-islands-japan` | `new_display_coverage` | 13 / 13 | 123 / 0 | 0 / 0 | 0/0/0/0 | `data_clean_only_with_signatures` |
| Japan / `japan` | `izu-peninsula-japan` | `new_display_coverage` | 29 / 29 | 73 / 0 | 0 / 0 | 0/0/0/0 | `data_clean_only_with_signatures` |
| Japan / `japan` | `miyako-japan` | `new_display_coverage` | 15 / 15 | 21 / 0 | 0 / 0 | 0/0/0/0 | `data_clean_only_with_signatures` |
| Japan / `japan` | `okinawa-main-japan` | `new_display_coverage` | 26 / 26 | 95 / 0 | 0 / 0 | 0/0/0/0 | `data_clean_only_with_signatures` |
| Japan / `japan` | `setouchi-japan` | `new_display_coverage` | 23 / 23 | 194 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| Japan / `japan` | `tokyo-bay-japan` | `new_display_coverage` | 37 / 37 | 47 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| Japan / `japan` | `yaeyama-japan` | `new_display_coverage` | 28 / 28 | 54 / 0 | 0 / 0 | 0/0/0/0 | `data_clean_only_with_signatures` |
| Egypt / `egypt` | `cairo-egypt` | `new_display_coverage` | 0 / 0 | 4 / 0 | 0 / 0 | 0/0/0/0 | `data_clean_only_with_signatures` |
| Egypt / `egypt` | `hurghada-el-gouna-egypt` | `new_display_coverage` | 97 / 97 | 42 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| Egypt / `egypt` | `redsea-egypt` | `new_display_coverage` | 87 / 87 | 32 / 0 | 0 / 0 | 0/0/0/0 | `missing` |
| Egypt / `egypt` | `sharm-el-sheikh-egypt` | `new_display_coverage` | 34 / 34 | 88 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| South Africa / `south-africa` | `cape-town-south-africa` | `not_in_atlas` | 9 / 9 | 66 / 0 | 0 / 0 | 0/0/0/0 | `narrative_only_no_signature_routes` |
| Singapore / `singapore` | `singapore` | `not_in_atlas` | 196 / 186 | 107 / 53 | 5 / 6 | 0/0/0/0 | `paired_with_signatures` |
| South Korea / `korea` | `busan-geoje-korea` | `not_in_atlas` | 7 / 6 | 126 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| South Korea / `korea` | `jeju-korea` | `not_in_atlas` | 9 / 9 | 77 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |
| South Korea / `korea` | `seoul-incheon-korea` | `not_in_atlas` | 13 / 9 | 12 / 0 | 0 / 0 | 0/0/0/0 | `data_clean_only_with_signatures` |
| South Korea / `korea` | `yeosu-tongyeong-korea` | `not_in_atlas` | 12 / 12 | 113 / 0 | 0 / 0 | 0/0/0/0 | `paired_with_signatures` |

## Route hygiene exceptions

### New Zealand — `new-zealand`
- Nonmember/misclustered: **10** — `ics-327dfe7c55`, `ics-4fe80c09ba`, `ics-8aaa6c73a6`, `ics-b14813cbf4`, `ics-b793b9cdae`, `ics-c9153f090d`, `ics-ddac6d7754`, `ics-dea3ec2a3a`, `ics-ed2acdc803`, `ics-ff95471dba`
- Quarantined: **0** — none

### Singapore — `singapore`
- Nonmember/misclustered: **2** — `ics-423b647c48`, `ics-1a53f8237d`
- Quarantined: **8** — `rn-0e4c994f77af`, `rn-4aeb0355b86f`, `rn-6bd7d2329345`, `rn-6d9dc1bf4811`, `rn-8139a384edfc`, `rn-8621d655c7cd`, `rn-bc8c36362710`, `rn-eea366adb95e`

### South Korea — `korea`
- Nonmember/misclustered: **7** — `rn-7c451ce2752d`, `rn-b4b6294b39e2`, `rn-e44147de575d`, `rn-dd8e26889f29`, `rn-0a711c22926a`, `rn-6e4ab1de83d4`, `rn-bc4b1bfe4b23`
- Quarantined: **0** — none

## Brief availability and maturity

### Australia — `australia`
- Cluster brief: **missing**.
- Maturity: `city_led_partial_no_cluster_brief`; city briefs present 4/4; missing: none.
  - `brisbane-australia` — `narrative_only_no_signature_routes`; partner_pitch (3 src, 0 sig), data_clean (3 src, 0 sig).
  - `gold-coast-australia` — `paired_with_signatures`; partner_pitch (3 src, 3 sig), data_clean (3 src, 3 sig).
  - `sydney-australia` — `paired_with_signatures`; partner_pitch (3 src, 4 sig), data_clean (3 src, 4 sig).
  - `whitsundays-australia` — `paired_with_signatures`; partner_pitch (3 src, 4 sig), data_clean (3 src, 4 sig).

### New Zealand — `new-zealand`
- Cluster brief: **missing**.
- Maturity: `city_led_partial_no_cluster_brief`; city briefs present 2/3; missing: `wellington-new-zealand`.
  - `auckland-new-zealand` — `paired_with_signatures`; partner_pitch (3 src, 4 sig), data_clean (3 src, 4 sig).
  - `bay-of-islands-new-zealand` — `paired_with_signatures`; partner_pitch (3 src, 4 sig), data_clean (3 src, 4 sig).
  - `wellington-new-zealand` — `missing`; none.

### Japan — `japan`
- Cluster brief: `data-clean/cluster_briefs/japan.json` — tier `first-class`, 2 sources, 2 signatures / 2 resolvable.
- Maturity: `first_class_cluster_and_city_coverage`; city briefs present 8/8; missing: none.
  - `hokkaido-niseko-japan` — `paired_with_signatures`; partner_pitch (2 src, 4 sig), data_clean (2 src, 4 sig).
  - `izu-islands-japan` — `data_clean_only_with_signatures`; data_clean (4 src, 5 sig).
  - `izu-peninsula-japan` — `data_clean_only_with_signatures`; data_clean (3 src, 5 sig).
  - `miyako-japan` — `data_clean_only_with_signatures`; data_clean (4 src, 5 sig).
  - `okinawa-main-japan` — `data_clean_only_with_signatures`; data_clean (3 src, 5 sig).
  - `setouchi-japan` — `paired_with_signatures`; partner_pitch (3 src, 4 sig), data_clean (3 src, 4 sig).
  - `tokyo-bay-japan` — `paired_with_signatures`; partner_pitch (2 src, 4 sig), data_clean (2 src, 4 sig).
  - `yaeyama-japan` — `data_clean_only_with_signatures`; data_clean (4 src, 5 sig).

### Egypt — `egypt`
- Cluster brief: `data-clean/cluster_briefs/egypt.json` — tier `first-class`, 2 sources, 2 signatures / 2 resolvable.
- Maturity: `first_class_cluster_brief_with_city_gaps`; city briefs present 3/4; missing: `redsea-egypt`.
  - `cairo-egypt` — `data_clean_only_with_signatures`; data_clean (2 src, 3 sig).
  - `hurghada-el-gouna-egypt` — `paired_with_signatures`; partner_pitch (2 src, 4 sig), data_clean (2 src, 4 sig).
  - `redsea-egypt` — `missing`; none.
  - `sharm-el-sheikh-egypt` — `paired_with_signatures`; partner_pitch (2 src, 3 sig), data_clean (2 src, 3 sig).

### South Africa — `south-africa`
- Cluster brief: **missing**.
- Maturity: `city_led_partial_no_cluster_brief`; city briefs present 1/1; missing: none.
  - `cape-town-south-africa` — `narrative_only_no_signature_routes`; partner_pitch (4 src, 0 sig), data_clean (4 src, 0 sig).

### Singapore — `singapore`
- Cluster brief: **missing**.
- Maturity: `city_led_complete_no_cluster_brief`; city briefs present 1/1; missing: none.
  - `singapore` — `paired_with_signatures`; partner_pitch (2 src, 3 sig), data_clean (2 src, 3 sig).

### South Korea — `korea`
- Cluster brief: `data-clean/cluster_briefs/korea.json` — tier `first-class`, 2 sources, 3 signatures / 3 resolvable.
- Maturity: `first_class_cluster_and_city_coverage`; city briefs present 4/4; missing: none.
  - `busan-geoje-korea` — `paired_with_signatures`; partner_pitch (3 src, 3 sig), data_clean (3 src, 3 sig).
  - `jeju-korea` — `paired_with_signatures`; partner_pitch (4 src, 4 sig), data_clean (4 src, 4 sig).
  - `seoul-incheon-korea` — `data_clean_only_with_signatures`; data_clean (4 src, 4 sig).
  - `yeosu-tongyeong-korea` — `paired_with_signatures`; partner_pitch (2 src, 3 sig), data_clean (2 src, 3 sig).

## DiDi proposal parity — Gates A–G

| Gate | Status | Core result |
|---|---|---|
| A_market_render_parity | **FAIL** | 10/10 current anchor city IDs resolve to canonical city features. Assigned countries contribute 0 map-scope city IDs and 0 full market pages. Rosters do not reconcile: 7 full markets, 0 roll-ups, 20 network_footprint rows, 21 map-scope registry keys, 18 map-scope city IDs, and 10 unique anchor cities. No DiDi anchor-city crosswalk artifact was found. |
| B_economics_tam_ladder | **FAIL** | finance/recal/corridors-didi.json holds 38 T3 inherited corridors, but agg-didi.json has 0 rows and 0 corridors because the only scoped market key is exactly didi rather than a didi-* market key consumed by partner filtering. growth-didi.json is dated 2026-06-07 and is null/zero; partner JSON still presents a nonzero $5,768,158 grounded floor, 16 boats, 35 sourced corridors and 341 greenfield corridors. Partner growth provenance names growth-didi.json/agg-didi.json, but those current files cannot produce the displayed numbers. growth-didi.json silently borrows grab-greenfield-census.json (35 sourced / 341 headline), violating own-census or labelled-global-template rules. All 38 scoped demand records are T3 bite2/econ_sidecar_inherit, not DiDi-specific demand anchors. Country-reference rows are missing for New Zealand, Japan, South Africa, and South Korea/Korea. |
| C_subproposal_parity | **FAIL** | All 7 existing Latin America market pages populate the core 14 market fields audited. None of the 7 assigned countries has a full subproposal. All 21 market phases have empty featured_routes arrays and omit fleet_confidence. Per-market vessel_sizing blocks are absent. |
| C1_vessel_range_and_phase_sizing | **FAIL** | Top-level growth_case.vessel_sizing exists, but it is not repeated per subproposal. No phase has fleet_confidence or route-bound featured routes, so range gates and phase fleet reconciliation cannot be audited per market. |
| D_cascade_and_provenance | **FAIL** | Proposal and data-clean partner JSON are byte-identical, but finance identity is broken. 0 of 38 scoped finance route IDs overlap the 9 proposal featured route IDs; only 8 of 38 scoped IDs exist in current data-clean/ROUTES.json. No DiDi sheet ID, xlsx, deck artifact, anchor crosswalk, render receipt, or partner-specific sidecar receipt was found. The global data-clean/economics_by_route_id.json exists, but it is not a DiDi delivery/cascade receipt. |
| E_partner_specific_framing | **FAIL** | Repository evidence confirms country-list presence for Australia, New Zealand, Japan, and Egypt but does not classify direct operation versus aggregation/JV. South Africa, Singapore, and South Korea have no current DiDi source rows in the audited repository. They must remain unconfirmed/historical-or-JV watchlist items, not be presented as direct footprint. Current proposal framing is Latin-America-centric and contains no assigned-country status treatment. |
| F_exec_summary_and_deck_readiness | **PARTIAL** | DiDi carries all five narrative source fields and the strict narrative section reports every 30 deck-eligible partner narrative-ready. The full repository validator exits nonzero because seven unrelated partner files fail schema; DiDi is not among them. No DiDi deck artifact or narrative binding output was found, so deck readiness is not delivery readiness. |
| G_partner_copy_gate | **PASS** | python3 scripts/audit_partner_copy.py partner-pitch/partners/didi.json returned PASS with 0 internal-jargon leaks. Copy pass does not cure stale economics or missing country status. |

### Finance spine identity

- `finance/recal/corridors-didi.json`: market key `didi`; `_partner_market_keys: []`; 38 requested / 38 bound corridors.
- `finance/recal/agg-didi.json`: 0 rows, 0 total corridors, $0 floor.
- `finance/recal/growth-didi.json`: `_as_of: 2026-06-07`; null floor; source rollup 0 corridors; borrowed `grab-greenfield-census.json`.
- Current partner/data-clean JSON: identical bytes, but still displays $5.768M grounded floor, 16 boats, 35 sourced and 341 greenfield corridors.
- Route identity: 0/38 scoped IDs overlap proposal featured IDs; 8/38 scoped IDs exist in current `ROUTES.json`; all 9 proposal featured IDs do exist in `ROUTES.json`.
- `country` is malformed on all 38 scoped corridor rows (city/market labels rather than country-reference keys), so the finance view cannot apply country costs safely.

### Current market/subproposal completeness

- Current full markets: `brazil`, `mexico-pacific`, `mexico-caribbean`, `colombia`, `panama`, `costa-rica`, `dominican-republic`.
- All 7 populate the 14 audited core fields; 10/10 unique anchor IDs resolve.
- Roster mismatch: 7 full markets, 0 roll-ups, 20 footprint rows, 21 map registry keys, 18 map city IDs, 10 unique anchors.
- All 21 market phases have empty `featured_routes[]` and no `fleet_confidence`; 0/7 markets carry per-market `vessel_sizing`.
- Assigned-country full markets: **0/7**.

## Prioritized defect register

| Priority | ID | Gate | Defect | Evidence / impact | Required next action |
|---|---|---|---|---|---|
| **P0** | `DIDI-FIN-IDENTITY-001` | B/D | Displayed DiDi economics contradict current aggregate and growth files | Partner displays $5.768M floor / 16 boats / 35 sourced corridors; agg is 0 and growth is null/zero. Partner-facing TAM is stale and non-reproducible. | Repair scoped market identity, rebuild agg/growth/frontend splice, and verify one finance spine end to end before any deck or expansion. |
| **P0** | `DIDI-CENSUS-002` | B | DiDi growth file borrows Grab census | finance/recal/growth-didi.json greenfield._census.source = grab-greenfield-census.json. Peer census is presented as DiDi upside. | Use a DiDi-owned census or the labelled global 3.44/4.9/6.36 template band; never a peer file. |
| **P0** | `DIDI-SCOPE-003` | A/C/E | Assigned ex-China country layer is completely absent | 0/7 assigned clusters, 0/25 cities, and 0/7 full subproposals in current DiDi footprint/map/markets. Four repository-confirmed countries cannot render for DiDi and three unconfirmed markets risk being overstated. | Inherit the four official-country-list markets into existing Atlas hierarchy after operating-model review; keep the other three explicitly unconfirmed. |
| **P0** | `DIDI-SPINE-004` | D | Scoped finance route roster is detached from proposal and gold routes | 0/38 scoped IDs overlap 9 proposal featured IDs; only 8/38 scoped IDs exist in ROUTES.json. No deterministic economics-to-render identity. | Re-materialize from current gold route IDs and reconcile proposal featured/wow routes before cascade. |
| **P1** | `DIDI-DEMAND-005` | B | Demand provenance is inherited T3, not DiDi-specific | 38/38 scoped corridors use T3 bite2/econ_sidecar_inherit. No source-backed DiDi demand floor. | Build country/city demand and fare anchors for promoted markets; hold economics until sourced. |
| **P1** | `DIDI-CREF-006` | B | Four assigned country-reference rows are missing | New Zealand, Japan, South Africa, and South Korea/Korea are absent. A future cascade would silently apply Singapore costs. | Add source-tiered rows before any assigned-country finance run. |
| **P1** | `DIDI-SUBPAGE-007` | C/C1 | Current subproposals lack route-bound phase detail | 21/21 phases have no featured routes and no fleet_confidence; 0/7 markets have vessel_sizing. Existing proposal is structurally populated but below Grab/Careem phase parity. | Bind real route IDs/node IDs, add fleet confidence and per-market vessel sizing, then reconcile phase fleets. |
| **P1** | `ATLAS-ROUTE-HYGIENE-008` | A | Canonical clusters contain misclustered/quarantined routes | New Zealand has 10 Kotor routes; Korea has 7 nonmember routes; Singapore has 2 nonmember routes and 8 quarantined routes. Raw route counts overstate usable cluster coverage. | Restamp/remove nonmember routes and preserve raw versus strict counts in QA. |
| **P1** | `DIDI-STATUS-009` | E | Direct versus JV/aggregation/historical status is not encoded | Official country-list rows prove four countries only; the repo has no operating-model discriminator and no current rows for three watchlist markets. Partner-facing copy could incorrectly claim direct footprint. | Add evidence-tier and operating-model fields before copy or map promotion. |
| **P2** | `ATLAS-BRIEF-010` | C | Brief maturity is uneven | No cluster brief for Australia, New Zealand, South Africa, or Singapore; Wellington and redsea-egypt lack city briefs; several briefs exist only in data-clean. Subproposal authoring will be uneven and non-reproducible. | Promote missing briefs and reconcile partner-pitch/data-clean brief surfaces. |
| **P2** | `ATLAS-MARQUEE-011` | C | Six of seven clusters have zero canonical marquee rows | Only Singapore has canonical marquee counts (5 wow / 6 featured). Dense route registries do not yet translate into flagship sales narratives. | Run canonical marquee selection after route hygiene; bind only current gold route IDs. |
| **P2** | `DIDI-DELIVERY-012` | D/F | Sheet/deck/crosswalk/render receipts are missing | No DiDi Sheet ID/xlsx/deck/crosswalk/render receipt found. Cannot claim proposal-complete or deck-ready delivery. | Create deterministic artifacts only after P0/P1 data defects are cleared. |

## Recommended sequence

1. Freeze partner-facing DiDi economics; do not reuse the displayed $5.768M/$1.53B figures.
2. Resolve DiDi direct/JV status for the four official-country-list markets and source status for the three watchlist markets.
3. Fix route and market identity: gold route IDs -> scoped finance roster -> aggregate -> growth -> partner splice.
4. Repair New Zealand/Korea/Singapore route hygiene and add four missing country-reference rows.
5. Add sourced demand/fare anchors, then promote Australia/New Zealand/Japan/Egypt as new_display_coverage.
6. Build full subproposals, per-phase route bindings/fleet confidence/vessel sizing, then create sheet/deck/render receipts.

## Validation receipts

- `python3 scripts/audit_partner_copy.py partner-pitch/partners/didi.json` → **PASS**, 0 internal-jargon leaks.
- `python3 scripts/validate_partner_proposals.py --strict-narrative` → DiDi narrative fields are ready; command exits nonzero at repo level because 7 unrelated partner files fail schema.
- No DiDi anchor crosswalk, transparent sheet ID/xlsx, deck, narrative binding, render receipt or partner-specific sidecar receipt was found.

## Source artifacts

- `partner-pitch/partners/didi.json`
- `data-clean/partners/didi.json`
- `data-clean/CLUSTERS.json`
- `data-clean/ROUTES.json`
- `data-clean/FEATURES_BY_TYPE.json`
- `atlas-external/boarding-points/singapore.json`
- `finance/model/corridors.json`
- `finance/model/country-reference.json`
- `finance/recal/agg-didi.json`
- `finance/recal/growth-didi.json`
- `finance/recal/corridors-didi.json`
- `handoff/global-marquee-pass2/CANONICAL-MARQUEES.json`
- `handoff/partner-map-model/partner-market-coverage-research.json`
- `handoff/partner-map-model/partner-market-coverage-p1-p2-continuation-batch-2026-06-20.json`
- `data-clean/cluster_briefs/*.json`
- `partner-pitch/city_briefs/*.json`
- `data-clean/city_briefs/*.json`

## Completion status

**`research-needed` / proposal not at parity.** Country operating-model status is unresolved, demand/fare provenance is inherited T3, finance identity is broken, assigned market pages are absent, and sheet/deck/render receipts are missing. The four official-country-list markets are suitable for an inheritance research lane; none is economics-ready.
