# Economics-sidecar opex refresh — handoff to Grok (2026-06-20)

## Why
The 2026-06-19 opex recal standardized a **6-line opex stack** (energy, crew ×1.8 FTE, marina overhead,
maintenance, **insurance = 2.5% regional capex**, **charging/berth = $18K**). It shipped into both engines
and the partner JSONs/sheets — but the **route-level economics sidecar** (`economics_by_route_id.json`,
the per-corridor breakdown the Atlas front end reads) was never regenerated. Result note "Next" item #2.

Two builder gaps fixed in this pass so the regen surfaces the new detail (Tasklet-owned spec fix):

1. **`run_cost` breakdown now emits all 6 lines.** It previously surfaced only 4 (energy/crew/marina/
   maintenance) + total + depreciation — **insurance and charging/berth were folded silently into the
   `annual_opex` total** and never shown on the corridor card. Added `insurance_usd_yr` +
   `charging_berth_usd_yr`.
2. **Partner coverage broadened.** `PARTNERS` was hardcoded to 6 (grab/careem/jih-global/red-sea-global/
   saudi-redsea-pif/qatar) — it **excluded bolt, yango, constance, four-seasons**, all recalibrated on 6-19.
   Now all 10 modeled partners (uber + saudi-pif still held, bespoke).
3. **`deck_url` (model-link CTA) wired from `economics_url_map.json`** for every partner, not just grab.

Verified by local dry-run: a bolt record now carries
`insurance_usd_yr=15000`, `charging_berth_usd_yr=18000`, summing correctly to `annual_opex_usd_yr=141372`.

## Inputs (all confirmed post-opex — `cost_components` carry insurance + charging/berth, dated 2026-06-19 17:xx)
- `finance/build_economics_sidecar.py` — **patched** (this pass).
- `finance/recal/agg-*.json` — refreshed aggs for all 10 partners.
- `finance/economics_url_map.json` — per-partner Sheet deep-links.

## Grok deterministic lane (do NOT build locally — needs freshly-sealed gold)
The sidecar resolves corridors → `route_id` against gold `ROUTES.json` (ID-based only). It must run
**after** the BP/route seal (`bp-seal-2026-06-20.zip`) lands, or Bolt/Yango corridors won't pin (local
pre-seal dry-run pinned only 3 bolt / 0 yango — expected, their geometry is mid-seal).

```
python3 build_economics_sidecar.py \
   --gold <freshly-sealed data-clean> --aggdir <recal aggs> --out economics_by_route_id.json
```
Then seal `economics_by_route_id.json` into the gold zip + commit to the GitHub source of truth.

## Sequence
1. Land BP/route seal (bp-seal-2026-06-20) → bolt/yango/spain/sweden route_ids bound.
2. Run patched sidecar builder against that gold → full 6-line breakdown, all 10 partners.
3. Seal into gold zip + commit. Front-end corridor cards then show the complete opex stack.
