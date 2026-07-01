# Grok spec — Red Sea Global · KSA re-point + scope lock (2026-07-01, v2)

## Why
The Red Sea Global partner page was rendering **Maldives / Bora Bora / Seychelles** — Four Seasons
`global_hospitality` inheritance boilerplate whose structured `node_id`s were never re-pointed to KSA
(only the prose was). Tasklet has re-pointed every structured field to real, already-sealed KSA nodes and
**locked RSG scope to its actual portfolio**.

## Scope decision (product-owner, 2026-07-01) — LOCKED
**RSG = The Red Sea + AMAALA + Jeddah gateway ONLY.**
- **NEOM / Sindalah is NOT an RSG asset** (different developer — NEOM Company). Dropped from the RSG page & deck.
- **Eastern Province / Khobar→Manama (Bahrain) is NOT an RSG asset.** Dropped from RSG.
- Both remain valid in the **broader PIF model / a future PIF partner view** — do **not** delete them globally.

## What Tasklet already did (in this PR)
1. **`partners/red-sea-global.json` (both `data-clean/` + `partner-pitch/`):** `phases`, `journeys_unlocked`,
   `featured_routes`, `use_cases`, and all prose re-pointed to KSA. Phases:
   - **Phase 1 — The Red Sea flagship** · `red-sea-global-ksa` · Pioneer II reef hops.
   - **Phase 2 — The Red Sea + AMAALA network** · `+ amaala-triple-bay-ksa` · Shura↔AMAALA (Quanta-LR) + intra-AMAALA.
   - **Phase 3 — Jeddah gateway integration** · `+ jeddah-ksa` · intra-Jeddah waterfront (Corniche↔Jeddah Central).
   - All `route_id: null` + `_link_status: geometry_seal_pending`.
2. **`STORIES.json`** `red-sea-global`: `scope_city_ids = [red-sea-global-ksa, amaala-triple-bay-ksa, jeddah-ksa]`
   (was `[red-sea-global-ksa, jeddah-ksa, neom-sindalah-ksa]` — neom removed, amaala added); dropped the
   "NEOM Sindalah — adjacent greenfield mega-cluster" narrative section; scrubbed the NEOM clause from the anchor section.
3. **`ROUTES.json`:** removed **4 RSG-tagged** edges to NEOM/Eastern Province
   (`gcn-9540121836-red-sea-global`, `gcn-7bd6efa01a-red-sea-global`, `gcn-8dc863114a-red-sea-global`, and the
   `red-sea-global-ksa↔neom` mints). **Left intact** the same geometry's other-partner variants
   (`-bolt`, `-yango`, `-saudi-redsea-pif`) and all bare/PIF Jeddah↔NEOM & NEOM↔Egypt edges.

**Verified:** `build-site.mjs` → `/red-sea-global` renders **cities:2, pois:116, routes:26**, **0 Maldives**.
strict-narrative exit 0 · route-linkage 0 gaps · seal-integrity invariants hold.

## Grok TODO (deterministic)
1. **Bind the already-sealed KSA `route_id`s** onto the featured/journey legs so they draw (Shura↔resort islands,
   The Red Sea↔AMAALA, intra-AMAALA, Jeddah Corniche↔Jeddah Central). Use the sealed gold edges between these
   KSA nodes; do not mint new geometry except intra-Jeddah if absent.
2. **Promote `amaala-triple-bay-ksa`** (currently a BP-parent only) to a **city node** so the AMAALA marina renders
   and it counts as a network city (clears the non-fatal seal-integrity warning: `amaala-triple-bay-ksa` cluster
   member with no rendered city feature). Same for `the-red-sea-archipelago-ksa` / `thuwal-private-retreat-ksa`
   if you want their marinas to render.
3. **Cull the residual NEOM POI from the RSG view (partner-view scoping):** one POI — **"Port of NEOM"
   (`bp-60b4fa4494`, parent `neom-sindalah-ksa`)** — still renders on `/red-sea-global`. Root cause: the build's
   `phaseEndpoints` pass is **partner-agnostic** — it pulls the far endpoint of *any* global route whose near
   endpoint is an RSG phase-city, so **other partners'** Jeddah↔NEOM edges (`gcn-…-bolt` / `-saudi-redsea-pif`,
   and the bare `rn-1322c440ea8d`) drag NEOM's port POI onto the RSG page even though NEOM is out of RSG scope.
   Tasklet must **not** delete those edges (they belong to bolt/PIF). Fix in the render/scoping lane — make the
   partner-page POI scope partner-aware (only POIs whose parent city ∈ `scope_city_ids`, or endpoints of routes
   in this partner's view), or explicitly exclude out-of-scope-city POIs. Acceptance: **0 NEOM/Eastern-Province
   POIs or dots on `/red-sea-global`.**
4. **Leave `CLUSTERS.member_city_ids` for the KSA cluster unchanged** — `neom-sindalah-ksa` / `eastern-province-ksa`
   are legit KSA geography (they only drive the "Part of {cluster}" breadcrumb, not RSG routes). This is correct.
5. **Render QA:** confirm `/red-sea-global` shows only The Red Sea + AMAALA + Jeddah, real KSA corridors, and
   **zero** Maldives / Bora Bora / Seychelles / NEOM / Eastern-Province anywhere.
