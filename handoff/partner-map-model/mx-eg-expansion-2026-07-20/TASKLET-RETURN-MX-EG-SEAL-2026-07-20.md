# Tasklet return — Mexico + Egypt coastal expansion seal (2026-07-20)

**From:** Grok · **To:** Tasklet · **Status:** `seal-complete + hand-waypoints / cascade-needed`  
**PRs:** research handoff [#314](https://github.com/jaideepdhanoa/navier-atlas/pull/314) · geometry seal [#315](https://github.com/jaideepdhanoa/navier-atlas/pull/315) · hand-waypoints (this return amend)  
**Lane:** `mx-eg-expansion-2026-07-20` + `mx-eg-hand-wp-2026-07-20`  
**Spec executed:** `GROK-SPEC-mx-eg-expansion-seal-2026-07-20.md`

---

## Grok task completion (this arc)

| Ask | Status | Notes |
|---|---|---|
| Merge PR #314 | **Done** | Phase 1 research + seal handoff on `main` |
| Geometry seal (BPs, routes, cities, clusters) | **Done** | PR #315 |
| Cozumel + Playa `members_missing` (blocking) | **PASS** | Both cities present; Mexico `members_missing: []` |
| Fare anchors $30 Playa↔Cozumel, $12 Holbox | **CONFIRMED** | Tagged on sealed routes; see fare receipt |
| City briefs → data-clean + `_index` | **Done** | 11 briefs |
| Water-allowlist (Nile, Manialtepec, El Gouna, Holbox) | **Done** | Folded into `data-clean/bp_water_allowlist.json` |
| Gold route IDs for Phase 3 | **Shipped** | Machine-readable list below |
| Hand-waypoints (no land crossings) | **Done** | A+B hardened; 24/27 ≤0.40 km; Nile allowlist hand channel |
| Phase 3 economics cascade | **Out of scope (Tasklet)** | Starts now on gold IDs |
| Phase 4 deck catch-up | **Out of scope (Tasklet/Grok later)** | After cascade |

**Also completed earlier in this session (adjacent, not this folder):**
- Country-deck standardize live apply (#308 work → #309): Egypt THE PRIZE 4-rung non-monotonic ladder + footnote; econ titles; chips; inDrive Brazil backup restructure.
- Deploy gate fixes: inDrive brief-only market-keep linkage skip (#310); exclusion-token scrubs (#311–#313). Prior `deploy-dist` green after those; post-#315 deploy was in flight at handoff write time.

---

## Seal scorecard

| Gate | Result |
|---|---|
| BPs sealed / dropped | **49 / 0** (no silent drops) |
| Routes built / failed | **27 / 2** |
| Hand-waypoints hard gate (≤0.40 km) | **24 / 27** after `mx-eg-hand-wp-2026-07-20` |
| Mexico members | **13** · `members_missing: []` |
| Egypt members | **7** · `members_missing: []` |
| Cozumel + Playa gate | **PASS** |
| Aspirational preserved | `cabos-r2`, `alex-r3` — still flagged aspirational |
| Cairo Nile | **2 geometry-only** + **hand channel spines** (ocean mask FP; not economics) |
| El Gouna | BPs attached under `hurghada-el-gouna-egypt` (no new member) |
| Partner inheritance | Cluster-level; DiDi Mexico / inDrive·Bolt·Yango Egypt inherit per corridor-inheritance |

### Hand-waypoint outcomes (2026-07-20)

| inventory_id | land before → after | method |
|---|---|---|
| cancun-r4 Punta Sam↔Isla Mujeres | 1.69 → **0.00** | water_polyline |
| sayulita-r2 La Cruz↔Punta Mita | 0.45 → **0.11** | offset_search |
| elgouna-r1 | 0.41 → **0.33** | water_polyline |
| pv-r3 Marina↔Las Ánimas | 0.34 → **0.00** | hand+solve_hand |
| alex-r2 Eastern Harbour↔Qaitbay | 0.20 → **0.06** | hand+solve_hand |
| cairo-r1 / cairo-r2 | hand Nile channel | `nile_allowlist_hand_spine` (mask treats Nile as land) |

**Residual holds (non-blocking):** `alex-r3` Montaza↔Abu Qir aspirational ~0.73 km; Holbox/PV minor &lt;0.35 already under soft visual bar. Self-pairs Dahab/Sayulita-r1 still inventory bugs.

**Receipts:** `MX-EG-HAND-WAYPOINTS-RECEIPT-2026-07-20.json` · `mx_eg_expansion_hand_waypoints.json` · `MX-EG-HAND-WP-CANDIDATES-2026-07-20.json`

### Intentional route inventory fails (not geometry bugs)
1. **`dahab-r1`** — self-pair (`dahab-lagoon-launch` → same). No distinct endpoints.
2. **`sayulita-r1`** — self-pair (`punta-mita-pier` → same). No distinct endpoints.

Tasklet: leave as display/experiences or re-author a second BP if a real lagoon/mesh leg is needed.

---

## Fare anchors (CONFIRMED 2026-07-20)

| Corridor | USD/leg MID | Status | Notes |
|---|---|---|---|
| Playa del Carmen ↔ Cozumel | **$30** | **CONFIRMED** | Mirror Cancún premium |
| Chiquilá ↔ Isla Holbox | **$12** | **CONFIRMED** | Short island-hop tier |

Provisional FX (pin at Phase 3): **MXN FIX ~17.50** · **EGP sell 51.1728**.

Machine receipt: `MX-EG-FARE-ANCHORS-CONFIRMED-2026-07-20.json`.

All other markets remain **display / null / conditional-on-demand** per research status — do not invent fares.

---

## Gold route spine for Phase 3 (authoritative)

**Machine-readable (use this):**  
`handoff/partner-map-model/mx-eg-expansion-2026-07-20/SEALED-ROUTE-IDS-FOR-CASCADE-2026-07-20.json`

**Full seal QA:**  
`handoff/partner-map-model/mx-eg-expansion-2026-07-20/MX-EG-EXPANSION-SEAL-RECEIPT-2026-07-20.json`

**Seal script (replay):**  
`scripts/grok-egypt/seal_mx_eg_expansion_2026_07_20.py`

### Signature / priority corridors (subset)

| inventory_id | market | route_id | sealed_nm | flags |
|---|---|---|---|---|
| cancun-r1 | cancun-riviera-maya-mexico | `rn-1b21ad26c9c7` | ~4.9 | signature · fare basis Cancún $30 already approved |
| cozumel-r1 / playa-r1 | cozumel / playa | see JSON | ~10 | signature · **$30 fare anchor** |
| holbox-r1 | isla-holbox-mexico | see JSON | ~5 | signature · **$12 fare anchor** |
| pv-r* | puerto-vallarta-mexico | see JSON | varies | south-shore water-taxi |
| cabos-r1 | los-cabos-mexico | see JSON | ~1.5 | signature |
| cabos-r2 | los-cabos-mexico | see JSON | coastal | **aspirational** |
| huatulco-r1 | huatulco-mexico | see JSON | ~4 | nine-bays spine |
| marsaalam-r1 | marsa-alam-wadi-el-gemal-egypt | see JSON | varies | boat-only park |
| alex-r1 | alexandria-egypt | `rn-fc211a5e2d2f` | ~11.7 | signature |
| alex-r3 | alexandria-egypt | `rn-6ac59ab9d246` | ~26.6 | **aspirational** |
| cairo-r1/r2 | cairo-egypt | `rn-c37df5916b71` / `rn-df422f98bbae` | — | **geometry-only — no economics** |

Exact IDs + nm for all 27 routes: open the sealed-route-ids JSON (do not re-mint).

---

## Cluster / city surface (post-seal)

**Mexico** `member_city_ids` (13):  
existing Cancún, Cozumel, Los Cabos, Playa del Carmen, Puerto Vallarta  
**+** Isla Holbox, Tulum, Sayulita–Riviera Nayarit, Mazatlán, La Paz, Acapulco, Puerto Escondido, Huatulco.

**Egypt** `member_city_ids` (7):  
existing Cairo, Hurghada–El Gouna, Red Sea, Sharm, Alexandria  
**+** Marsa Alam–Wadi El Gemal, Dahab.

City briefs in `data-clean/city_briefs/` (11 new + prior Cozumel/Playa).

---

## Tasklet Phase 3 checklist

1. **Bind economics only to gold `route_id`s** from `SEALED-ROUTE-IDS-FOR-CASCADE-2026-07-20.json`. Exact-ID only; null beats invent.
2. **Apply confirmed fares:** Playa↔Cozumel **$30**, Chiquilá↔Holbox **$12** (MID one-way). Cancún↔Isla Mujeres remains prior **$30** approved.
3. **Skip economics** for:
   - Cairo Nile (`geometry_only`)
   - Aspirational inventory legs unless explicitly promoted
   - Display/experiences markets without demand pins (Tulum, Sayulita, Mazatlán, La Paz, Acapulco, Puerto Escondido, Dahab, Alexandria Corniche)
4. **Demand pins still owed** (research status): Cozumel annual pax series, Holbox annual pax, Marsa Alam park permits, PV water-taxi + Huatulco nine-bays operator series.
5. **Country / market keys:** DiDi Mexico geography keys (`mexico-caribbean` / `mexico-pacific` or successor); Egypt markets under inDrive/Bolt/Yango inheritance — no catch-all partner key.
6. **FX pin** at cascade time (provisional MXN 17.50 / EGP 51.1728).
7. After cascade: hand back to Grok for **Phase 4 deck catch-up** (DiDi Mexico + inDrive Egypt spines / prize / unit-econ as needed). Country-deck standardize (#309) already landed Egypt prize ladder + chips on live decks.

---

## Do not

- Invent L3 demand or fares for display markets.
- Re-mint route IDs or BP coords (gazetteer already sealed; reuse atlas IDs).
- Attach platform rungs to inDrive Egypt prize (inDrive = no platform rung; sheet MID).
- Auto-swap Egypt ladder without capture footnote (SOM > SAM is intentional ~87% boat-only).

---

## Files (this folder)

| File | Role |
|---|---|
| `TASKLET-RETURN-MX-EG-SEAL-2026-07-20.md` | **This handoff** |
| `SEALED-ROUTE-IDS-FOR-CASCADE-2026-07-20.json` | Gold route IDs + nm for Phase 3 |
| `MX-EG-EXPANSION-SEAL-RECEIPT-2026-07-20.json` | Full QA / drop / density receipt |
| `MX-EG-FARE-ANCHORS-CONFIRMED-2026-07-20.json` | Confirmed fare anchors |
| `MX-EG-FARE-ANCHORS-2026-07-20.md` | Updated status table |
| `GROK-SPEC-mx-eg-expansion-seal-2026-07-20.md` | Spec Grok executed |
| `seal-manifest.json` | Authoritative market/cluster index from research |

**Gold surface:** `data-clean/FEATURES_BY_TYPE.json`, `ROUTES.json`, `CLUSTERS.json`, `bp_water_allowlist.json`, `city_briefs/*`.
