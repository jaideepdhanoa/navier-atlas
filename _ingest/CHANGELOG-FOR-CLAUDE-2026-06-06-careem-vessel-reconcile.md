# Changelog for Claude — Careem east-coast vessel reconcile (2026-06-06)

**Scope:** content-only (one partner proposal). Geometry byte-identical to prior gold — ROUTES `dac87d0f…`, FEATURES `0ac62823…`, 5,154 routes unchanged. No build/A* needed.

## What changed
`data-clean/partners/careem.json` only. Reconciled a copy-vs-geometry mismatch (backlog D5):

- The **drawn** Careem east-coast geometry is the locked intra-Fujairah cluster — **Dibba ↔ Khor Fakkan ↔ Kalba, ~28 nm** (Phase 1 featured route, `_link_kind: node-network`), which sits inside the **N30 Pioneer II** 70 nm all-electric range.
- The **prose** (Phase 2 rationale + narrative, two KPIs, and `end_state.steady_state.platform_mix`) still described the demoted story: a **Quanta-LR arc around the Musandam peninsula**. That long-range-hybrid framing was removed per the locked judgment call (DXB↔FJR demoted; Careem reframed as a self-contained intra-Fujairah east-coast cluster).

## Edits
- Phase 2 `rationale` / `narrative`: Quanta-LR Musandam arc → self-contained **Pioneer II** Fujairah cluster (Dibba/Khor Fakkan/Kalba).
- KPI "East coast: Quanta-LR arc" → "East coast: Fujairah cluster".
- KPI "Charging: None required" → "Infrastructure: None new" (the no-charging benefit is hybrid-specific; an all-electric Pioneer II cluster charges at existing berths).
- `steady_state.platform_mix`: now "Pioneer II throughout — Dubai↔Abu Dhabi trunk, intra-metro hops, and a self-contained Fujairah east-coast cluster (Dibba–Khor Fakkan–Kalba)".

## Retained (legitimate, not route claims)
Two Quanta-LR mentions remain — both standard Navier platform boilerplate present across all 46 partners: the range-headroom objection ("…with Quanta-LR for anything longer") and `why_navier_now.no_new_infrastructure` ("the Quanta-LR hybrid needs no charging infrastructure at all"). These describe platform capability, not a Careem route.

## Render impact
None structural. Careem Phase 2 east-coast copy now matches the drawn 28 nm cluster. No new fields, no schema change.
