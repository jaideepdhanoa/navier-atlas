# Changes from Tasklet — render-layer additions you must preserve

`main`'s `index.html` is the **fused production baseline** (Tasklet build + your render). Branch
from `main` so your next render starts with these already in place. They are render-layer code, so a
plain `index.html` regenerate that ignores them will silently drop them — please keep them.

## Priority (marquee) cities — always-on label layer  **(KEEP)**
- `build.py` emits a separate **`priority_city`** bucket in `FEATURES_BY_TYPE` (currently 13: Singapore,
  Dubai, Abu Dhabi, Doha, Hong Kong, Bangkok, Jakarta, Malé, Muscat, Jeddah, Manila, Phuket, Bali).
- The render adds a dedicated **`priority-cities`** geojson source with **unclustered, always-on** layers
  (`priority-hub-glow`, `priority-halo`, `priority-points`, `priority-labels`) so these flagship hubs are
  **never** absorbed into a cluster or lose label placement to dense neighbours (Singapore was being
  swallowed by Riau/Johor).
  - **⚠️ Updated 2026-05-30 (PR #2):** `priority-labels` no longer uses `text-allow-overlap:true` /
    `text-ignore-placement:true` — at world view the flagships piled on top of each other. They are now
    collision-thinned with `symbol-sort-key: ['-',0,degree]`, so the highest-degree marquee hub wins
    placement (Singapore still labels) without stacking. **Do not restore allow-overlap:true.** See
    `NOTES-FOR-TASKLET.md`.
- Wired into: the degree-max loop, the `stat-cities` count, the click-handler layer list, `DEFAULT_OPACITY`,
  and the story focus/dim block. If you add/rename layers, keep `priority-*` in those five places.

## Named-hub pin promotions  **(data — survives automatically)**
- Cebu, Bohol, El Nido, Coron, Puerto Princesa, Amanpulo, Boracay, Siargao, Sir Bani Yas, Daymaniyat are
  promoted to named `city` pins in the data spine — no render change needed.

## Your v17 look-feel — fused and live
- Basemap lift (raster brightness-min/saturation/contrast), Areas/locale tier removed end-to-end, bottom
  toggle bar deleted, region nav re-tiered. All preserved in `main`. (`locale` features may still appear in
  `FEATURES_BY_TYPE` — render-side correctly ignores them per your v17 skip code.)

## Merge protocol
- After every gated deploy, Tasklet pushes the production build back to `main` (index.html + data-clean/ +
  this note). Branch from `main` to avoid 3-way merges. If you ever branch from an older point, Tasklet
  re-applies the priority layers via a 3-way merge — but branching from `main` keeps it clean.
