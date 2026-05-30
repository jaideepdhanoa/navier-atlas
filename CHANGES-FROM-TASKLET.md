# Changes from Tasklet — render-layer additions you must preserve

`main`'s `index.html` is the **fused production baseline** (Tasklet build + your render). Branch
from `main` so your next render starts with these already in place. They are render-layer code, so a
plain `index.html` regenerate that ignores them will silently drop them — please keep them.

## Priority (marquee) cities — always-on label layer  **(KEEP)**
- `build.py` emits a separate **`priority_city`** bucket in `FEATURES_BY_TYPE` (currently 13: Singapore,
  Dubai, Abu Dhabi, Doha, Hong Kong, Bangkok, Jakarta, Malé, Muscat, Jeddah, Manila, Phuket, Bali).
- The render adds a dedicated **`priority-cities`** geojson source with **unclustered** layers
  (`priority-hub-glow`, `priority-halo`, `priority-points`, `priority-labels`).
- **⚠️ REVERSED (Claude PR #2, kept): `priority-labels` is NO LONGER `text-allow-overlap:true`.** It is now
  **collision-thinned** with a degree `symbol-sort-key` (+ `text-optional:true`) so the highest-degree marquee
  hub wins placement and flagships stop piling up at world view (Doha/Dubai/Abu Dhabi/Muscat were stacking).
  Singapore still labels because it's top-degree. **Do NOT restore `allow-overlap:true` on regenerate** — the
  data still flows through `priority_city`, but the label collision policy is owned by Claude's render code.
- Wired into: the degree-max loop, the `stat-cities` count, the click-handler layer list, `DEFAULT_OPACITY`,
  and the story focus/dim block. If you add/rename layers, keep `priority-*` in those five places.

## Named-hub pin promotions  **(data — survives automatically)**
- Cebu, Bohol, El Nido, Coron, Puerto Princesa, Amanpulo, Boracay, Siargao, Sir Bani Yas, Daymaniyat are
  promoted to named `city` pins in the data spine — no render change needed.

## De-fused multi-place clusters → real separate cities  **(data — survives automatically)**
- Three fused parent nodes were **split into separately-anchored constituent cities** (each with its own
  correct map anchor, clean label, and own boarding-point file):
  - `manila-cebu-palawan-philippines` → **Manila, Cebu, Palawan (El Nido), Boracay, Siargao**
  - `japan-okinawa-yaeyama` → **Okinawa, Miyako, Yaeyama**
  - `japan-izu-shimoda` → **Izu Peninsula, Izu Islands**
- Two single nodes were **de-prefixed** (label cleanup only): "Hokkaido / Niseko Coastal Arrival Vector"
  → **Hokkaido**;  "Malé / Maldives (national)" → name **Maldives**, pin label **Malé**.
- Retired fused parents are hidden (`HIDE_ON_MAP`) and their stray `__` sub-POIs suppressed.
- `build.py` carries a **`RETIRED_REMAP`** normalization (edges/stories/orgs `city_presence`) so any surviving
  reference to a retired parent resolves to its primary constituent — holds regardless of partition state. **KEEP.**
- This also fixes the Cebu-POI mis-geocode root cause (Cebu was anchoring on Manila inside the fused node).
- Route network fully **re-run with land mask** after the split: **0/1504 land crossings** (a stale geometry
  cache had to be purged — split clusters generate new inter-constituent connectors that must be A*-validated).

## Your v17 look-feel — fused and live
- Basemap lift (raster brightness-min/saturation/contrast), Areas/locale tier removed end-to-end, bottom
  toggle bar deleted, region nav re-tiered. All preserved in `main`. (`locale` features may still appear in
  `FEATURES_BY_TYPE` — render-side correctly ignores them per your v17 skip code.)

## Merge protocol
- After every gated deploy, Tasklet pushes the production build back to `main` (index.html + data-clean/ +
  this note). Branch from `main` to avoid 3-way merges. If you ever branch from an older point, Tasklet
  re-applies the priority layers via a 3-way merge — but branching from `main` keeps it clean.
