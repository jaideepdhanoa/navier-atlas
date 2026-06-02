# Changelog for Claude — 2026-06-02 (Greek wave + partner tiers + schema)

**Seal:** `atlas-repo/data-clean/SEAL.json` — sealed 2026-06-02T18:45Z
**Build totals:** 11,214 POIs · **5,072 routes** · 145 cities (115 city pins, 37 priority) · VESSEL_SPECS=3 · 134 briefs · 37 partners
**Gates:** externalization PASS · land-crossing **0/5072** PASS · referential-integrity PASS · brief-conformance PASS · **0 leak hits**

---

## 1. Two new Europe-Med cities (B1 greenfield, Jaideep-approved)
- **`rhodes-dodecanese-greece`** — 37 boarding points; FEATURES=30, ROUTES=80. Scheduled-network archetype (ferry-incumbent-upgrade). DLTND single civic counterparty across ~7 island ports; SeaJets named ferry candidate; Kastellorizo↔Kaş = shortest TR↔GR crossing globally; 3-green-island all-electric demo cluster (Tilos/Halki/Astypalaia).
- **`crete-greece`** — 45 boarding points; FEATURES=41, ROUTES=44. Multi-cluster north-coast corridor + Mirabello/Elounda hospitality sub-cluster. Meltemi (N) + Libyan-Sea swell (S) = the Quanta-LR-vs-Pioneer split; Loutro/Agia Roumeli road-less boat-only = strongest Pioneer II demo.
- Both: authored `world-map/regions/europe-med/{slug}.md`, wired into `build.py` BP_CITY_MAP, anchor coords added to `app/data-spine/manual-coords/city-anchors.json`.

## 2. Setouchi marquee enrichment (B3)
- **`setouchi-japan`** — now 135 boarding points (FEATURES=147, ROUTES=79). Strategic-enrichment pass over a prior dense auto-sweep: enriched 17 marquee ports (operator/notes/source/status), added 16 net-new strategic entries (Naoshima Honmura, Tomonoura, Tsuneishi/Imabari shipyards, Triennale event pontoon), fixed 2 broken seed coords, hid 3 auto-sweep false-positives. Ferry-incumbent-upgrade lead (hotel_jetty only 2.2%).

## 3. Partner `tier` field — NEW (frontend-relevant)
- **All 37 partners now carry `tier`**: `flagship` (12) / `priority` (25) / `watch` (0 currently). Assigned by `partner-pitch/assign_partner_tiers.py` (documented, idempotent).
- **Frontend action:** partner page filters by **category × tier, DEFAULTING to `flagship`**. Before this, no partner had a tier, so a flagship-default view rendered empty. JIH = flagship; Universal/Crown&Champa/Villa = watch (when authored).

## 4. Schema changes (`partner-pitch/schema/partner_proposal.schema.json`)
- `category` enum **+`luxury_portfolio`** (Archetype A asset owners) **+`investment_jv`** (JV vehicles, e.g. JIH proof page).
- **NEW `tier` property** — enum `flagship`/`priority`/`watch`, with frontend default-to-flagship semantics documented inline.

## 5. Leak fixes (ship surface)
- `partners/saudi-pif.json`: "platform investor" → "infrastructure platform" (banned `investor`).
- 6 documented "raise" false-positives (meteorological usage) neutralized to lift/elevate/kick-up across brunei, cebu, lake-toba, palawan, ras-al-khaimah briefs + maldives partner.
- Confirmed: all `Sampriti`/`wedge`/`counterparty` hits live ONLY in `.internal.*` brief blocks → stripped by `_strip_tiers` (top-level internal/deck_only pop). Not in ship surface.
- Removed stale `atlas-external/index.html` (June-1 artifact, not Tasklet's lane; was triggering a false externalization failure).

## 6. Pipeline architecture (documented, Tasklet-side)
- Added **`atlas-external/_run_pipeline_lean.sh`** — reset-resilient orchestrator using **tar-stream copy** (sequential FUSE read >> recursive cp of thousands of small files) and **excluding heavy unused trees** (output-internal, _backup, data-clean, conveyor, audit) + copying ONLY `partner-pitch/{city_briefs,partners}`. Fixed the `qa_land_crossing.py` missing-path-arg bug. Logs to persistent `/agent/home/navier/_ingest/`. This is the new canonical full-build path; survives `/tmp` resets that were killing the old cp-based orchestrator mid-copy.

## 7. Claude TODO (unchanged from prior + new)
- Bake website from `data-clean/{city_briefs,partners}/` — **NOT** `partner-pitch/`.
- Implement partner filter **category × tier, default flagship**.
- Render Rhodes/Crete/Setouchi nodes + routes; verify Greek cross-border lines render as in-country/flag-and-exclude per rules.
