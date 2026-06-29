# Grok handoff — Region briefs → cluster/city depth + seal-integrity fixes

**From:** Tasklet · **Date:** 2026-06-29 · **Branch:** `region-briefs-depth-seal-fix-2026-06-29`

Two workstreams, one PR. Everything below is already applied to `data-clean/` + `index.html` and
validated by two new strict gates. **Grok's job: build and push to prod**, then Jaideep pastes the
`/region/southeast-asia` link in WhatsApp to confirm the share card.

---

## Workstream A — Region briefs to cluster/city depth (all 11 regions)

Region briefs shipped as tagline + summary stubs and the renderer only drew summary + an auto
country grid. They now mirror the cluster-brief section system.

**A1 · `data-clean/region_briefs.json`** — all 11 regions enriched. Each region now carries:
`scope_stats {clusters, cities}`, `why_marine_mobility`, `demand_signals[]`, `use_cases[]`
(structured `{archetype,title,body,platform}`), `navier_fit {pioneer_ii, quanta_lr}`,
`signature_routes[]`, `transit_planning`, `competitive_landscape`, `seasonality`,
`regulatory_note` (intentionally `null` at region scale — licensing is per-country → defer to
cluster briefs). Existing taglines preserved; 6 summaries extended to clear the depth bar
(wording-tune only, no claims invented).

- **Signature routes are an ID-matched rollup** of each region's constituent clusters' sealed
  corridors — `route_id` only, every one validated against `data-clean/ROUTES.json`. Regions with no
  sealed corridors carry `signature_routes: null` (**Caribbean, Caspian**) — null beats
  confidently-wrong. No corridors invented.
- Archetypes use the canonical safe set (`tourism / super_app / essential_mobility / luxury /
  ride_hail`) so the visible chip renders clean.

**A2 · `index.html` `_regionBriefHtml`** — extended to render every new section (parity with
`_clusterBriefHtml`), a "Footprint" scope-stats row, and clickable signature-route chips that deep-link
to the corridor on the map. Added `_REGION_DISPLAY_ALIAS` / `_normRegionDisplay` (full alias map,
mirrors `region-share.mjs`) so every cluster lands in the correct region grid.

**A3 · `scripts/validate-region-briefs.py`** (new, `--strict`) — completeness + integrity gate:
depth fields present, `use_cases` structured, `navier_fit` not a flat string, **`scope_stats.clusters`
== count of clusters tagged to that region** (panel grid == share card), and **every signature
`route_id` resolves** in ROUTES.json. Receipt: `11 audited — 0 incomplete, 11 at standard`.

**A4 · `scripts/region-share.mjs`** — added `Caucasus`/`Central Asia` → `Caspian` to `REGION_ALIASES`.
The `caspian` brief previously matched **zero** clusters (its clusters are tagged Caucasus/Central
Asia); it now correctly rolls up Baku + Aktau/Kuryk (2 clusters · 3 cities).

**`scripts/author-region-briefs.py`** (new) — reproducible authoring script (idempotent; recomputes
share-card stats in pure Python mirroring `collectRegionStats`). Re-run after any rollup change.

---

## Workstream B — Seal-integrity fixes (Grok's NOTES-FOR-TASKLET §2026-06-29)

**`scripts/seal-integrity-fix.py`** (new, idempotent) — applied to `data-clean/FEATURES_BY_TYPE.json`
+ `data-clean/CLUSTERS.json`:

| Item | Note ref | What was done |
|---|---|---|
| Dedupe FEATURES_BY_TYPE | P0 #1 | `city` array had every id stacked **8×** (1661 rows → **212 unique**). One Feature per `(type,id)`. **Root cause of the duplicate MapLibre pins + count inflation** — Grok's defensive Set dedupes are now belt-and-suspenders, not load-bearing. |
| Seal gate: city ∈ CLUSTERS | P0 #2 | `scripts/validate-seal-integrity.py` (new, `--strict`) enforces no orphan city, every `cluster_id` set, no dupes, no twins. |
| Backfill `cluster_id` | P1 #3 | Set/updated on **249** city features from `member_city_ids`. |
| Reject/merge city twins | P1 #4 | `sabah-kk` → `sabah-kota-kinabalu-malaysia`; legacy fused `aruba-curacao-bonaire` → de-fused ABC islands (BPs re-homed to nearest island by anchor haversine). **62 boarding points re-homed, 2 twin features dropped.** |
| `algeria` cluster brief | P2 #5 | Created `algeria` cluster (Algiers/Oran/Annaba/Skikda) + bound 8 other orphaned coastal cities (Kenya ×4, Cyprus ×2, Croatia-Zadar, Morocco-Rabat) into their existing clusters. Every rendered city now resolves to a cluster. |

Also normalized `members_present = len(member_city_ids)` on every cluster (fixed stale `thailand` 10→14).

### ⚠ One geography decision flagged for Jaideep — NOT auto-resolved
North Africa is tagged three different ways across neighbours: **morocco = `Africa`**, **algeria =
`Maghreb`**, **tunisia = `Europe`**. I did **not** re-judge any cluster's macro-region (that's the
Atlas geography lane). I only enforced the seal principle that a *city must not contradict its own
cluster*: `tunis-tunisia` carried feature-region `Africa` while its cluster `tunisia` is tagged
`Europe`, so the city now inherits `Europe` (step **B3b**, 1 feature). **Please decide the canonical
macro-region for the three North-African clusters and normalize the cluster tags** — the cities will
follow automatically since they're now consistent.

---

## Validation receipts (on this branch)
```
python3 scripts/validate-seal-integrity.py --strict   →  ✓ all invariants hold (249 cities, 103 clusters); exit 0
python3 scripts/validate-region-briefs.py --strict     →  11 audited, 0 incomplete, 11 at standard; exit 0
node scripts/build-site.mjs                            →  _dist ready: 1 aggregate + 267 partner/market + 1004 share pages; exit 0
```
Baked-output spot checks: aggregate `atlas-data.js` city features = **212 rows / 212 unique** (0 dupes,
0 twins); `_dist/index.html` carries the new renderer; SEA share card reads **"44 cities · 8 clusters"**
== `scope_stats`. All 11 regions: `scope_stats.clusters` == rendered cluster-chip count.

## Grok's to-do
1. Build + deploy `_dist/` to prod (your lane).
2. Keep the defensive Set dedupes in place — harmless now, cheap insurance.
3. After Jaideep normalizes the North-Africa cluster tags, re-run `scripts/seal-integrity-fix.py`
   (idempotent) so city regions follow, then `scripts/author-region-briefs.py` to refresh `scope_stats`.

## Held / null (explicit)
- `signature_routes: null` for **Caribbean** and **Caspian** (no sealed corridors yet — additive when minted).
- `regulatory_note: null` for all regions (per-country → cluster briefs own it).
- 17 cluster member ids have no rendered city feature (coverage stubs) — non-fatal warn in the seal gate; not invented.
- North-Africa macro-region tags — awaiting Jaideep's call (above).
