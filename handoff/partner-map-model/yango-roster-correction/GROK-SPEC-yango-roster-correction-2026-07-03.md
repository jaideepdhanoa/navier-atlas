# GROK SPEC — Yango roster correction + net-new coastal seal (2026-07-03)

**Owner split:** Tasklet has corrected the partner roster, authored net-new geography + briefs, and completed narrative. Grok executes the deterministic seal: **unseal removed markets, seal net-new markets, complete the TAM ladder, bind route_ids, re-derive map scope.** GitHub `main` is source of truth.

Supersedes the additive-only seeds from PR #177 that were **not validated Yango markets**. Authoritative footprint = Jaideep's Yango market list (2026-07-03). Rule throughout: **ID-based matching only; null beats confidently-wrong; no invented route_ids.**

---

## 1. UNSEAL — remove markets that are NOT Yango (from map, ROUTES.json, POIs)
Remove these city nodes and everything hanging off them (POIs, corridors, route_ids, cluster membership) from the Yango surface. Some are shared corridor-network nodes used by other partners (Bolt) — **only remove them from the Yango partner view / `_map_scope`; do not delete shared atlas geometry other partners rely on.**

| Remove from Yango | Country | Note |
|---|---|---|
| `manama-bahrain`, `muharraq-bahrain` | Bahrain | Not a Yango market |
| `muscat-oman`, `salalah-dhofar-oman`, `khasab-musandam-oman`, `sohar-oman`, `muscat-oman__daymaniyat-islands-unesco-marine-reserve-candidate` | Oman | Not a Yango market |
| `colombo-sri-lanka` | Sri Lanka | Not a Yango market |
| `eastern-province-ksa` | Saudi Arabia | Not a Yango market |
| `baku-azerbaijan` | Azerbaijan | Not a Yango market |
| `lagos-nigeria` | Nigeria | Not a Yango market |

Also drop the two cross-border Bahrain legs already removed from the partner JSON (UAE→Bahrain Financial Harbour; Doha→Manama) from any Yango corridor rendering.
**Do NOT delete any city/cluster briefs.** The briefs for removed markets (Baku, Manama, Muharraq, Muscat, Khasab, Sohar, Salalah, Colombo, Eastern Province, Lagos) are **partner-neutral shared assets** other partners rely on (e.g., Bolt serves Baku). They are retained as harmless orphans; only Yango's partner surface (footprint / `_map_scope` / sub-pages / featured_routes) is corrected.

## 2. SEAL — net-new coastal Yango markets (candidate BPs + corridors provided)
Dossiers in `handoff/partner-map-model/yango-roster-correction/`. ID-match → seal POIs → build BP↔BP routes → bind `route_id`s. Honour the water/land-crossing gate; each land-crossing corridor carries **explicit hand waypoints (lng, lat)** — fold them into the routing mask.

| Cluster file | City node(s) | BPs | Corridors (hand-waypointed) |
|---|---|---|---|
| `cameroon` | `douala-cameroon` | 4 | 3 (2 HW; Kribi express = Quanta-LR roadmap) |
| `congo-brazzaville` | `pointe-noire-congo` | 3 | 2 (1 HW) |
| `namibia` | `walvis-bay-namibia` | 4 | 3 (3 HW; Pelican Point spit rounding) |
| `venezuela` | `la-guaira-venezuela`, `maracaibo-venezuela` | 5 | 3 (1 HW; Los Roques 80nm = Quanta-LR roadmap) |

Vessel gate: ≤70nm → Pioneer II `solid`; 75–150nm → Quanta-LR `amber-dashed`; >150nm review. Two corridors are already flagged Quanta-LR roadmap (Kribi express ~78nm; La Guaira↔Los Roques ~80nm). Namibia's Sandwich Harbour leg is road-less — keep it, it is a real water-only link.

## 3. Bind the 8 sub-pages' `route_id`s (Gap 2)
Routes live in `markets[].phases[].featured_routes` (labels) and `markets[].journeys_unlocked` (corridor labels). Bind state:
- **UAE/Qatar/Egypt/CIV — already bound** (12/8/10/10 route_ids across phases+journeys). Leave intact **minus the removed Bahrain legs**.
- **Senegal/Colombia/Norway/Kazakhstan — 22 `featured_routes` + 16 `journeys_unlocked`, all null** (`from_node_id`/`to_node_id`/`route_id` = null, `_link_status: "pending-grok-bind"`, real place-name labels present). Bind node_ids + route_ids by **ID-matching the PR #177 BP/corridor dossiers** for these four markets.

**Never fabricate a route_id — leave null where geometry isn't sealed.**

## 4. Complete the TAM ladder (Gap 1) — over the CORRECTED footprint
`growth_case` currently renders only the floor rung; it is missing `journey_gmv`, `marine_mobility_tam`, `partner_platform_rev_on_navier` (present on Bolt/Grab). Re-run the marine-TAM-split (a `.bak-pre-marine-tam-split` exists — the split regressed for Yango) **after** the unseal/seal so aggregation covers the corrected 25-node footprint (Bahrain/Oman/Sri Lanka/KSA/Azerbaijan/Nigeria removed; 5 net-new added). Apply the plain-English render descriptors per the Slides convention (`SOM = "SOM full network (~XX% capture, today, +greenfield)"`). Keep captive-capture rules (LB-254) and the no-silent-Singapore-opex / CAPEX-region rules (LB-243). This is Grok's economics lane — Tasklet did not touch growth_case.

## 5. Re-derive `_map_scope` (do NOT hand-list)
`_map_scope` is auto-synced by `scripts/partner-scope.mjs` from CLUSTERS.json + `network_footprint`. Re-run it against the corrected footprint so cluster_city_ids/registry_keys reflect the removals + net-new. Tasklet edited `network_footprint` only.

## 6. Flip the status flag (Gap 5)
Set `_coverage_expansion.status` → sealed once §1–§5 land; refresh `_render_chip_flag` in growth_case.

---

## Acceptance gate (Grok QA report must show)
- Map renders the 8 sub-page anchors + all footprint nodes; **zero renders for the 7 removed markets** on the Yango view (shared geometry preserved for other partners).
- Net-new: BPs sealed as POIs (0 silent drops), corridors built, land-crossings = 0 post-hand-waypoint, every surviving BP carries a source id.
- 8 sub-pages' route_ids bound where geometry exists; null where not (no fabricated ids).
- TAM ladder renders all rungs (SOM floor / SOM full / SAM / journey-GMV / marine TAM) with plain-English descriptors; magnitudes sane vs corrected footprint.
- `_map_scope` re-derived; counts reconcile: geometry chips == sub-pages (8) + footprint roll-ups.
- Counts: BPs sealed/dropped(+reason), routes built/culled, before→after POI total, land-crossing=0 proof.
