# Gold #37 — duplicate-route reconciliation + Okinawa orphan-brief fix (2026-06-09)

## TL;DR
- **Duplicate-route collapse (backlog #3, "~204 same-direction dups"): 0 true duplicates exist on this gold under the agreed basis (`from_node_id + to_node_id + geometry_hash`). Nothing collapsed — by design, per "null beats confidently-wrong."**
- The apparent inflation resolves to two NODE-MODEL / RENDER-LAYER categories below — both your domain, not a route-level collapse Tasklet should make.
- One real content bug fixed: the orphan Okinawa brief now renders.

## Reconciliation of the "~204 same-direction duplicate corridors" figure
Measured on Gold #36 (`navier-export-20260608T223640Z.zip`, 5,201 routes):

| Basis | Count | Verdict |
|---|---|---|
| **TRUE exact dups** — identical `from` + `to` (node ids) + byte-identical geometry | **0** | Gold #29 already removed the 28 real ones. None remain. **Nothing to collapse.** |
| Collocated-geometry, **city-node ↔ BP** — a city-origin access edge (`jakarta-indonesia → bp-752…`) traces the SAME polyline as a BP-origin edge (`bp-f29… → bp-752…`) because the city node is collocated with a boarding point | **52** | **Not route duplicates.** Distinct endpoints + different `traffic_weight`/labels. The city-origin access edges serve city-to-city journey routing; deleting them risks breaking journeys. Visual line-stacking is a **render de-dupe** concern (collapse collocated polylines at draw time) — your layer. |
| Collocated-geometry, **two BP-ids for one physical dock** — `sicily-aeolian-italy__villa-san-giovanni` vs `…__villa-san-giovanni-reggio-calabria` (same dock, two node ids) | **1** | **Node-merge candidate** (merge the duplicate node, then the second edge collapses naturally). Node-model fix, not a route fix. Neither route id is referenced downstream. |
| **Directional mirror pairs** A→B and B→A both present | **1,225** | **Intentional.** Locked rule: Tasklet authoring stays directional; front-end shows ↔ and de-dupes display. Not duplicates. |

**Conclusion:** "~204" ≈ a mix of the 52 city↔BP collocations + a subset of the 1,225 mirrors counted as one corridor. Under the exact agreed dedup key there is nothing to remove. If you want the 52 collocations gone at the data level, the correct fix is upstream: either (a) don't emit a city-origin access edge when the city node is collocated (<~50 m) with a BP, or (b) render-time de-dupe of byte-identical polylines. Tasklet will not delete city-origin or BP-variant edges blind, because that loses labeled variants / can break journey routing.

## What DID change in this gold (vs #36)
1. **Okinawa orphan brief reconciled.** `city_briefs/okinawa-yaeyama-japan.json` (combined "Okinawa & Yaeyama Islands", `city_id = okinawa-yaeyama-japan`) matched NO node (gold nodes are `okinawa-main-japan` + `yaeyama-japan`) → it rendered nowhere. Rekeyed `city_id` + filename to the lead hub **`okinawa-main-japan`**. No other file referenced the old id (0 dangling). `yaeyama-japan` remains brief-less (its content is covered within the combined brief on the main hub).
2. Economics sidecar re-verified: 71 records, 0 country mislabels (all UAE records correct; the 4 `country:Singapore` records are genuinely Singapore/Grab corridors).

## Still queued for you (node-model / render layer — unchanged)
- 7 `bp-*` nodes misfiled as `city` type in FEATURES_BY_TYPE (reclassify city→poi).
- The 52 city↔BP collocations + 1 duplicate-node (Villa San Giovanni) above.
- Geo-mistags blocked on Places API: Musandam/Zighy Bay, real Montenegro BPs.
