# GROK-SPEC — Mexico + Egypt coastal expansion seal (2026-07-20)

**From:** Tasklet · **To:** Grok (deterministic seal) · **Handoff dir:** `handoff/partner-map-model/mx-eg-expansion-2026-07-20/`

## Mandate
Seal the Mexico + Egypt coastal expansion onto the Atlas render graph, mirroring the Brazil expansion seal
(`GROK-SPEC-brazil-expansion-seal-2026-07-19.md`). Promote the named boarding points, build the BP↔BP route
graph, add the new cities to the `mexico`/`egypt` clusters, and fix the two `members_missing` Mexico cities.
All partners scoped to Mexico/Egypt inherit the geometry per corridor-inheritance — **no per-partner hand-listing.**

## Inputs (this dir)
- `seal-manifest.json` — clusters, member changes, partner inheritance, per-market counts (authoritative index).
- `boarding-points/*.json` — 18 markets, 49 named official terminals/marinas/piers. **`lng`/`lat` are null by
  design** (`coord_status: "gazetteer_pending"`): promote each named terminal to its sealed coordinate via
  gazetteer/ID-match. Named terminal + `source` is authoritative; do not invent coordinates.
- `route-inventories/*.json` — 31 candidate routes (20 signature, 2 aspirational). `distance_nm` approximate.
- `demand-records/*.json` — 6 source-backed demand records (economics reference only; not needed for the graph).
- `bp_water_allowlist_additions.json` — 4 inland/lagoon water bodies (Cairo Nile, Manialtepec, El Gouna lagoons,
  Holbox/Yalahau channel). Fold into `data-clean/bp_water_allowlist.json`; validate/snap bboxes.
- `../../../partner-pitch/city_briefs/*.json` — 11 new partner-facing city briefs (data-clean seal = straight copy
  + `_index.json` update, per the Atlas brief pattern).

## Cluster changes
**Mexico** (`cluster_id: mexico`):
- **Fix `members_missing`:** `cozumel-mexico`, `playa-del-carmen-mexico` — seal real geometry so both render (both
  already have data-clean briefs). This is a **blocking acceptance gate.**
- **Add 8 new member city ids:** `isla-holbox-mexico`, `tulum-mexico`, `sayulita-riviera-nayarit-mexico`,
  `mazatlan-mexico`, `la-paz-mexico`, `acapulco-mexico`, `puerto-escondido-mexico`, `huatulco-mexico`.
- **Densify existing:** `cancun-riviera-maya-mexico` (hotel-zone mesh), `puerto-vallarta-mexico` (south-shore
  water-taxi line), `los-cabos-mexico` (El Arco runs).

**Egypt** (`cluster_id: egypt`):
- **Add 2 new member city ids:** `marsa-alam-wadi-el-gemal-egypt`, `dahab-egypt`. (Fold candidates: Marsa Alam →
  `redsea-egypt`, Dahab → `sharm-el-sheikh-egypt` — your call if geographically cleaner; else standalone members.)
- **Attach-only (no new member):** `el-gouna-egypt` BPs attach to existing `hurghada-el-gouna-egypt`.
- **Add Nile lane to existing member `cairo-egypt`** (0 → scheduled Nile Taxi geometry). **Geometry-only, no economics.**
- **Alexandria** (`alexandria-egypt`, existing member, ~2 routes today) → thin-to-full display.

## Gates / acceptance (QA report must show)
1. **BP coverage: 0 silent drops.** Every named BP is either sealed as a POI or in a drop-ledger with a reason.
2. **0 land crossings** post-allowlist; 0 orphan routes; every surviving BP carries a `source`.
3. **Cozumel + Playa del Carmen `members_missing` cleared** — both render real geometry (blocking).
4. **Egypt BP-endpoint audit:** the existing Egypt network references only ~3 unique BPs across 184 routes
   (pre-BP-standard). Re-seal so routes terminate at proper named terminals, not shared placeholders.
5. **Tier density targets:** marquee 15–40+ (Cancún/Isla Mujeres, Cozumel); full 8–15 (Holbox, Puerto Vallarta,
   Los Cabos, Alexandria, Marsa Alam, Huatulco); display 6–10; brief-only 0–4. Report before→after route counts per city.
6. **Aspirational flags preserved, never silently mixed:** `cabos-r2` (Cabo↔San José coastal), `alex-r3`
   (Montaza↔Abu Qir), and any Hurghada↔Sharm intercity crossing added to the Red Sea network must render visibly aspirational.
7. **Riverine/lagoon geometry-only:** Cairo Nile lane renders but is tagged economics-out-of-scope (like Belém/Manaus).
8. **Partner inheritance:** DiDi Mexico inherits the Mexico geometry; inDrive/Bolt/Yango Egypt inherit the Egypt
   geometry. Country tags correct; cross-partner overlap intact.
9. Counts: BPs sealed/dropped (+reason), routes built/culled, before→after POI totals, land-crossing=0 proof.

## Explicitly OUT of scope for economics (this seal is geometry)
Economics cascade (Phase 3) is a separate world (`partner-model-cascade`) and runs **after** this seal returns
gold route IDs. Fare anchors are proposed but pending Jaideep approval (see `MX-EG-FARE-ANCHORS-2026-07-20.md`).
Do not attach economics to any market here.
