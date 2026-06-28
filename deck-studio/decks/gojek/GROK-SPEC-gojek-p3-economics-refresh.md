# GROK SPEC — Gojek Phase-3 economics refresh

**Owner:** Grok (model engine lives in `finance/`; not in Tasklet's filesystem).
**Context:** Phase-3 deck expansion is live. Per-corridor grounded unit-economics already exist and are now on
the deck (5 deep-dive slides: Bali, Singapore, Riau↔Singapore, Komodo & Flores, Likupang & Bunaken). Two
economics gaps remain that require a model pass.

## What Tasklet already did (do NOT redo / do NOT rebuild the deck)
- Repointed all interactive links `/grab/*` → `/gojek/*` (live deck, Slides API, in place).
- Overview slide: "six markets" → "ten markets".
- Built Komodo & Flores and Likupang & Bunaken "What one boat earns" slides from the **grounded** breakdowns
  in `data-clean/economics_by_route_id.json` (ID-matched, every line item ties).
- The Gojek deck was edited directly via the Slides API. **Do not rebuild or full-replace it.** Hand numbers
  back as JSON; Tasklet binds them in place.

## Gap 1 — Ladder + $127M anchor predate the frontier seal (re-cascade)
- The deck's overview anchor ($127M) and "The Prize" ladder ($18M floor → $87M → $280M → $1.12B → $3.36B →
  $151M platform) were cascaded **2026-06-21**, **before** the 2026-06-27 Indonesia frontier seal that grounded
  Komodo, Likupang, Raja Ampat and bound Lake Toba.
- **Action:** re-run the §B cascade for `gojek` over the **current 10-sub-proposal / 59-bound-corridor** network
  (`aggregate.py → growth.py → growth_frontend_block.py → splice_growth_into_partner.py → build_transparent_sheet.py
  → build_master_sheet.py`). Honor LB-254 (captive vs contested capture) — Gojek is contested ride-hail/super-app,
  14% floor capture.
- **Return:** refreshed `agg-gojek.json` + growth_case rungs (floor / som_network / sam / tam_transfer / journey_gmv /
  platform_rev) and the new $-anchor for the sourced corridors. Tasklet binds the refreshed numbers into the deck
  overview + ladder in place.

## Gap 2 — Lake Toba & Sumba have estimated stubs only (mint grounded)
**Corridors are bound (Tasklet verified on main, 2026-06-28) — geometry is NOT the gap; grounded economics is.**
The following route_ids exist in `data-clean/partners/gojek.json` / `_main-dc-gojek.json` but their entries in
`economics_by_route_id.json` are bite-2 placeholder stubs (`status:"estimated"`, "replace with deck-grounded rows
when available") — so they have **no** honest unit-economics and got **no** deep-dive slide:

- **`lake-toba`** — 2 bound corridors:
  - `rn-db305ed7f029` — Parapat → Tomok / Tuk Tuk (Samosir)
  - `rn-89174b6f31fe` — Tuk Tuk → Samosir shoreline villages
- **`sumba`** — 1 bound marquee corridor:
  - `gcn-224eb8acd1-shared` — Komodo / Labuan Bajo → Sumba (Nihi coast)

- **Action:** mint grounded records (full `breakdown.revenue_build` + `run_cost` + `result`) keyed to those exact
  route_ids, same shape as the existing gojek-registry grounded records. CAPEX = $600K (Indonesia, region rule).
  Use ID-based matching only — bind to the route_ids above, do not re-mint or duplicate corridors. If demand
  evidence is thin, return `status:"estimated"` honestly — do not fabricate a grounded floor (null beats
  confidently-wrong).
- **Return:** the route-keyed records. Tasklet builds the Lake Toba / Sumba deep-dive slides from them (same
  duplicate-template method) if they clear the compelling-economics bar (payback ≲ 2.5yr); otherwise they stay
  footprint-only / narrative.

## Lean markets (no action — recorded, not a gap)
Jakarta (14.1yr), Lombok (4.9yr), Raja Ampat (7.6yr) are grounded but lean. Per "exactness over coverage /
null beats confidently-wrong" they are represented via the map footprint + network ladder, **not** a rosy
"what one boat earns" deep-dive. Their grounded numbers are in `GOJEK-P3-ECONOMICS-DATAPACK.json`.

## Handback contract (required)
Branch name · PR link · commit SHA · exact files changed · validation receipt · explicit nulls/held items.
No self-certified completion or line-range audits.
