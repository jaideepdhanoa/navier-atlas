# Changes from Tasklet — render-layer additions you must preserve

_Pushed to `main` so your next `claude/*` branch starts from a render that already includes these.
`index.html` is a build artifact — when you regenerate it, **re-apply these template blocks** (same
rule as your own handoff §7)._

## 1 · Marquee always-on city layer (`priority-cities` source)
**Problem solved:** Singapore (and other P0 hubs) were absorbed into numbered clusters at default
zoom (`clusterMaxZoom:5` swallowed SG + Riau/Batam/Bintan/Johor), and lost label placement to dense
neighbours. Jaideep flagged it twice.

**Fix:** a dedicated **unclustered, always-on** source + layers for 13 marquee cities:
- Source: `map.addSource('priority-cities', {type:'geojson', data:{...features:FEATURES_BY_TYPE.priority_city||[]}})`
- Layers (added after `city-labels`, before locales): `priority-hub-glow`, `priority-halo`,
  `priority-points`, `priority-labels`.
- `priority-labels` uses `text-allow-overlap:true` + `text-ignore-placement` so the label is **never
  decluttered or clustered** — visible at every zoom.

**Data contract (new feature bucket):** `build.py` now splits the 13 marquee cities out of
`FEATURES_BY_TYPE.city` into **`FEATURES_BY_TYPE.priority_city`**. Each carries `priority_city:true`.
Render reads from that bucket. The 13: Singapore, Dubai, Abu Dhabi, Doha, Hong Kong, Bangkok,
Jakarta, Malé, Muscat, Jeddah, Manila, Phuket, Bali.
- Stat counters + degree-normalisation loops were updated to fold both `city` and `priority_city`
  buckets (`stat-cities`, `MAX_CITY_DEG`).

## 2 · Named-pin hub promotions
Island sub-hubs that were POIs-without-labels are now labelled pins: Cebu, Bohol/Panglao, El Nido,
Coron, Puerto Princesa, Amanpulo, Boracay, Siargao, Sir Bani Yas, Daymaniyat. Handled data-side in
`build.py` (promotion table + corrected coords). No render change required beyond §1 layers.

## 3 · Handlers updated (don't drop these layers from control logic)
The priority layers were wired into **all** route/feature control structures — if you restructure
layers, keep them in:
- `DEFAULT_OPACITY` map (`priority-points`, `priority-halo`, `priority-hub-glow`, `priority-labels`)
- the focus/dim loop (`for (const layer of [...])`)
- city-select highlight + story-focus dim handlers

## 4 · Merge mechanics going forward (per Jaideep)
Tasklet now pushes each gated production `index.html` back to `main` after deploy, so your branch
inherits Tasklet's render + data changes — no more 3-way hand-merges. Your v17 density-glow
(`route-glow-bloom`/`route-glow-core`, demand width/colour, edge-bundling) is **fully fused** into
this `main` and live on production. Branch from `main`, not from an older snapshot.
