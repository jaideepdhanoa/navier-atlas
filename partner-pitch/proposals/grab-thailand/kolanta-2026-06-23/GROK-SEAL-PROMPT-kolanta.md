# Grok seal mandate — Grab Thailand: Ko Lanta (Andaman) addition

**Pass:** `grab-thailand-kolanta-2026-06-23` · **Partner:** `grab-thailand` · **Market:** `phuket_andaman`

Tasklet-owned source is in this folder. This is an **input package** — `main` is source of truth. Deterministic
seal (BP ID-match + snap, route geometry, route_id binding, data-clean reseal, economics cascade) is Grok's lane.
Adds one Andaman connected city to the existing Phuket cluster; no new markets, no moved cities.

## Mandate
1. **Seal the new city `koh-lanta-thailand`** from `boarding-points/koh-lanta-thailand.json`
   (2 BPs: `koh-lanta-saladan-pier` P0, `koh-lanta-old-town-pier` P1). Coordinates are curated seeds —
   **regeocode/snap + water-adjacency check**. 0 silent drops; every surviving BP keeps a source id.
2. **Bind the 3 near-term routes** in `GRAB-THAILAND-KOLANTA-BINDSET.json` to real BP↔BP geometry and
   assign `route_id`s. They are `route_id: null` / `_link_status: pending-seal-thailand-kolanta` in the partner
   JSON's `connected_city_mesh` — **bind, never fabricate**:
   - `koh-lanta-thailand → koh-phi-phi-thailand` (~17 nm, Pioneer II, tier A)
   - `koh-lanta-thailand → krabi-thailand` (~24 nm, Pioneer II, tier B)
   - `phuket-phang-nga-thailand → koh-lanta-thailand` (~40 nm, Pioneer II, tier B)
3. **Range gate:** all three ≤ 40 nm ⇒ **Pioneer II** (render `solid`, `range_status: now`). No Quanta-LR here.
4. **Reseal `data-clean/partners/grab-thailand.json`** so the live front end renders Ko Lanta with real
   geometry (Tasklet did **not** touch data-clean/partners — it must not render geometry-less).
   Add `koh-lanta-thailand` to the `phuket_andaman` scope (`connected_cities` already lists it in the
   partner-pitch surface; derive `scope_city_ids` by ID-match, never hand-list).
5. **Economics cascade** (after binding): wire the demand anchors in `GRAB-THAILAND-KOLANTA-DEMAND-ANCHORS.json`
   as premium-tier fare × haircut-demand records under the existing `phuket_andaman` market in
   `finance/model/corridors.json` (no rollup pseudo-geographies), then `aggregate.py → growth.py → splice →
   transparent sheet → economics sidecar`. Thailand `country-reference.json` row already required by the depth
   pass — confirm present (no silent Singapore-opex fallback). SOM floor is the honest sell; do not inflate.

## Acceptance gate (QA report must show)
- BP coverage: **0 silent drops**; both Ko Lanta BPs sealed (or drop-ledgered with a reason).
- 3 routes built, all Pioneer II, 0 land-crossings, every endpoint carries a source id.
- `koh-lanta-thailand` renders in the Grab Thailand `phuket_andaman` view with real geometry.
- `data-clean/partners/grab-thailand.json` carries Ko Lanta (no stale/empty market).
- De-attribution (PR #87) preserved; no attribution reintroduced.
- Economics: Ko Lanta corridors carry bound `route_id`s + sidecar entries; floor cascaded, not fabricated.
