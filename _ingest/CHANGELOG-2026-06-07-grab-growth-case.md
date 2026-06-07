# CHANGELOG 2026-06-07 — Grab `growth_case` merged to Gold #4 (note to Claude)

**Export:** `navier-export-20260607T034828Z.zip` (now GOLD). Superset of Gold #3 — parity verified
(228 = 228 file set; 0 missing). **Geometry untouched:** `ROUTES.json` (5154), `FEATURES_BY_TYPE.json`,
`STORIES.json`, `VESSEL_SPECS.json` are byte-identical to Gold #3. This is a **content-lane** change.

## TL;DR
`data-clean/partners/grab.json` now carries a new top-level **`growth_case`** block — a render-ready,
model-grounded "floor and the prize" layer for **revenue potential, phased economics, and vessel sizing**.
Please build 3 new front-end layouts for it (spec bundled: `RENDER-SPEC-growth-case.md`). A handful of
stale narrative numbers on the Grab page were reconciled to the financial model.

## Why this changed
Jaideep asked to incorporate the growth-case (SAM/TAM/SOM ladder + greenfield) into the partner page for
**vessel sizing and revenue potential by phase**, starting with Grab. He also **cleared $-based partner
opportunity-sizing for external use** (the "$100M+" ban applies only to *Navier's own raise/self-finance*,
never to the partner's prize), and approved reconciling the stale page numbers.

## What's new in `grab.json.growth_case` (3 render sub-blocks + 1 flag)
1. **`revenue_potential`** — the floor-and-prize ladder. 5 rungs: SOM-floor → SOM-full-network →
   SAM-matured → TAM journey-GMV → partner platform revenue. Each rung has `whose_money`, `basis`,
   banded `display.{low,mid,high}`, `confidence`. Plus `whose_money_legend`, `anchor_note`, `cite_rule`.
2. **`phase_economics`** — 3 horizons (Prove / Scale / Mature) with fleet, Navier transport rev, partner
   platform rev, CO₂/yr, vessel, confidence. This is the "revenue potential **by phase**" view.
3. **`vessel_sizing`** — 3 hull classes (N30 Pioneer II solid · N35 Shuttle solid 2027 · Quanta-LR
   amber-dashed H2 2026+) with `pax`, `range_nm`, `status`, `role`, and the `range_gate_note`.
4. **`_render_chip_flag.needs_new_layouts`** = `["revenue_ladder","phase_economics_table","vessel_sizing_cards"]`.

## TWO AXES — do not conflate (important)
- **Geographic phases** (existing `grab.json.phases[]`, boats 8/177/442/883) = **WHERE** we roll out
  (Singapore beachhead → region). Unchanged. Keep rendering as the rollout story.
- **Economic horizons** (`growth_case.phase_economics`, Prove/Scale/Mature) = **WHAT it's worth** as it
  scales. New. These are different lenses on the same network — render them as distinct sections.

## Reconciled stale numbers (applied to gold)
- `network_thesis.stats` "At scale": `250+ vessels` → `800+ vessels`; `on 120+ booked corridors` →
  `375+ mapped corridors (full-network floor)`.
- `end_state.steady_state.total_corridors`: `120+ booked` → `375+ mapped water corridors`.
- `end_state.steady_state.vessels_at_scale`: `250+` → `800+ at full-network floor, scaling to 2,700+ at maturity`.
- `steady_state_ceiling`: `2678` → `3638` (Mature Pioneer-equivalent mid).
- **Left as-is (flagged, do NOT free-float without a source):** `committed_fleet: 1071`.

## Honesty / render rules (hard — carry into every layout)
- **Headline the MID. Never headline the `high` band** (it stacks every optimistic assumption — ceiling only).
- **Lead with the floor + the corridor COUNT** (ID-traceable: 341 greenfield + 35 sourced = 376 mapped
  Pioneer-range corridors in Grab geography). Counts are harder evidence than the greenfield $ factor.
- Always show the **`whose_money_legend`** — Navier transport rev vs total journey wallet vs **partner's
  own platform revenue** (the rung the super-app actually cares about). Do not quote boat fare to Grab as
  the prize; the prize is journey-GMV → their platform take.
- **Quanta-LR renders amber-dashed** (roadmap), consistent with the atlas arc convention.
- Inter-city routes render **bidirectional `↔`** on the front end.

## Provenance / regenerate
- Generator: `finance/model/growth_frontend_block.py --partner grab` (reusable; Careem/RSG inherit it).
- Sources: `finance/grab-growth-case.json` + `finance/grab-aggregate-results.json`.
- One grounded unit drives everything: **$256,796 transport rev / boat / yr**, **30,194 t CO₂ at 165 boats**.
- Build spec for the 3 layouts: `RENDER-SPEC-growth-case.md` (bundled at export root).
