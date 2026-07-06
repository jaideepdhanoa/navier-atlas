# GROK SPEC — Country Cluster Merges (2026-07-06)

**Jaideep directive:** No reason for a country's coastal sub-cluster to be a separate cluster from the country. Merge:
1. `uae-east-coast` → `uae`
2. `dammam-eastern-province-ksa` → `saudi-arabia`

`ksa-commercial` is **NOT** in scope — it carries an explicit DO-NOT-MERGE guardrail (Bolt sovereign/commercial split). Leave untouched pending separate Jaideep decision.

## Canonical edit already applied (this commit)
`data-clean/CLUSTERS.json`:
- `uae.member_city_ids` now `[abu-dhabi, dubai, ras-al-khaimah, sharjah, fujairah]` (fujairah folded in).
- `saudi-arabia.member_city_ids` unchanged content (eastern-province + dammam-khobar already members); merge seal added.
- Retired clusters removed: `uae-east-coast`, `dammam-eastern-province-ksa` (109 → 107).

## Cascade to apply (Grok lane)
1. **Rebind route cluster_ids** in `data-clean/ROUTES.json`:
   - `uae-east-coast` → `uae` (**190 refs** across `cluster_id`/`from_cluster_id`/`to_cluster_id`/`cluster_ids`).
   - `dammam-eastern-province-ksa` → `saudi-arabia` (**10 refs**).
2. **UAE market-group definition:** collapse `{uae, uae-east-coast}` → `{uae}` in the front-end market-group config + `scripts/route-display.mjs`/market-groups applier. Browse rail already shows one "United Arab Emirates" chip — keep it, now keyed on single cluster.
3. **Re-derive partner scopes** (`global-partner-scope-derive`): yango/uber/noon/careem/bolt `_map_scope` drop `uae-east-coast`, keep `uae`. Same-country content unchanged (inherit-all binds identical corridor set).
4. **Re-inherit** corridors + `marquee_corridors[]` + finance spine under the merged cluster ids (`partner_corridors = global_canonical ∩ clusters`; finance spine identical across UAE partners).
5. **Run gates:** `validate_partner_inheritance.py` + `validate_finance_inheritance.py` — must stay green globally.
6. **Reseal + deploy.**

## Acceptance
- 0 residual references to `uae-east-coast` / `dammam-eastern-province-ksa` in live data (`data-clean/*`, `partner-pitch/partners/*`).
- Browse rail: one UAE chip, one Saudi Arabia chip (+ ksa-commercial unchanged).
- Spot-check `/careem`, `/yango/uae`, `/bolt/uae` — Fujairah/east-coast corridors still render; no corridor loss.
- Spot-check `/saudi-arabia` (or KSA aggregate) — Dammam/Eastern Province corridors render under saudi-arabia.
- Report route rebind counts + gate results.
