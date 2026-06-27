# Grok → Tasklet handback — PR intake + production state

**Date:** 2026-06-27  
**Baseline:** `main` @ `65df120f`  
**Production:** https://navier-atlas.vercel.app (pre-flight clean, deployed)

---

## PR queue status

**Open Tasklet PRs: 0**

Grok fetched `origin` and listed all PRs through **#126**. Nothing new to merge, build, or deploy since the last intake wave.

| PR | Title | Grok disposition |
|----|-------|------------------|
| #106 | Grok-chat migration playbooks | ✅ Already on `main` |
| #107 | Operating playbooks + onboarding | ✅ Already on `main` |
| #108 | LINE MAN Wongnai deck + proposal | ✅ Merged (Tasklet owns live Slides) |
| #109 | Bolt parity re-audit | ✅ Merged; Grok applied renderer fixes |
| #110 | LINE MAN Grok handoff spec | CLOSED (superseded by #125) |
| #111 | Centara Thailand deck plan | ✅ Merged (Tasklet owns deck appendix) |
| #113 | Proposal completeness Bite 1 | ✅ Merged |
| #114 | Bite 2 ladder cascade handoff | ✅ Merged; Grok executed cascade |
| #116 | Bolt East Africa narrative | ✅ Merged |
| #117 | Bite 5 null-route journeys | ✅ Merged |
| #120 | Bite 8 Maldives de-boilerplate | ✅ Merged |
| #122 | De-jargon sweep (corpus) | CLOSED; content landed via #126 |
| #123 | FE-2 POI cleanup (−114 junk) | CLOSED; Grok completed handoff items below |
| #125 | FE-3 Grab + LINE MAN deck closes | ✅ Merged |
| #126 | De-jargon 8 partners + sub-$10M format | ✅ Merged |

**Gaps never opened:** #115, #118, #119, #121

---

## What Grok ran (post-PR, on `main`)

### 1. Story geometry — north star achieved

| Metric | Was (handoff 2026-06-26) | Now |
|--------|--------------------------|-----|
| Story pass | 852 / 168 fail | **1019 / 0 fail** |
| Allowlisted | 0 | 0 |

**Method:** Regional `WATER_BBOXES` waves 10–11 + sweet-spot solver on detour fails + 3 hand-fixed corridors (Komodo, Cannes–Monaco, Turkey Bosphorus).

**Artifacts:** `scripts/grok-geometry/regional_land_masks.py`, `handoff/partner-map-model/GEOMETRY-TRIAGE.json`

### 2. FE-2 Grok handoff (from #123) — completed

| Item | Status |
|------|--------|
| 16 route-bound junk POIs | ✅ Rebound to real piers; 28 route endpoint updates |
| Hua Hin Pier `bp-cd5ab934c8` | ✅ Coords fixed to `[99.959, 12.5712]` |
| 1,283-copy dedup worklist | ✅ **876** zero-ref duplicates dropped (safe keeper rule) |
| POI count | 12,380 → **11,490** |
| Gold reseal | ✅ `FEATURES_BY_TYPE` + `ROUTES` + `economics_by_route_id` hashes in `SEAL.json` |

**Scripts:** `scripts/grok-fe2/apply_fe2_routebound_cleanup.py`, `scripts/grok-fe2/apply_fe2_poi_dedup.py`  
**Reports:** `handoff/partner-map-model/fe2-routebound-cleanup-report.json`, `fe2-poi-dedup-report.json`

**Note:** ~407 dedup groups still have referenced copies — Grok only dropped unreferenced orphans per manifest guardrail.

### 3. Bite 2 ladder cascade (#114 handoff) — executed

| Metric | Was | Now |
|--------|-----|-----|
| `growth_case` bound | 16 / 36 | **32 / 36** |
| Economics records | 465 | **661** (+196 distance-tier stubs) |

**Newly bound:** didi, kakao-mobility, cabify, wsf, shun-tak, bc-ferries, nyc-ferry, thames-clippers, transport-nsw, fullers360, hong-kong, norway-fjords, maldives, crown-champa, universal-enterprises, villa-hotels (+ prior 16).

**Blocked (4):**

| Partner | Reason |
|---------|--------|
| **hawaii** | Inter-island routes >70 nm → `growth_frontend_block.py` null `SOM_full_network_*` keys (Quanta-LR roadmap) |
| **cote-dazur** | 0 `route_id`s in partner JSON |
| **d-marin** | 0 `route_id`s |
| **discovery-land** | 0 `route_id`s |

**Scripts:** `scripts/grok-bite2/mint_bite2_economics_stubs.py`, `run_partner_cascade.sh` (`SKIP_ECON_SIDECAR_REFRESH=1` preserves stubs)  
**Report:** `handoff/partner-map-model/bite2-cascade-report.json`

### 4. Pre-flight (release mode) — PASS

```
story: 1019 pass / 0 fail (0 allowlisted)
SEAL: 5/5 blobs match
linkage: 61 partners, 0 blocking gaps
exclusion tokens: 0 hits
```

---

## Still on Tasklet (unchanged ownership)

### Deck lane (highest priority)

1. **Centara Thailand** — bind 7 sealed corridors into live deck appendix; refresh economics from `handoff/centara-thailand/centara-thailand-economics-sidecar.json`; dock/pier/beach rights still null.
2. **LINE MAN Wongnai** — live Google Slides build (#108 package on `main`).
3. **Minor Hotels gold deck** — LB-261 rebase refresh (#106).

### Formal SEAL / gates

| Gate | Grok interim | Tasklet formal action |
|------|--------------|----------------------|
| `geometry_story` | **PASS** (1019/0) | Sign gold SEAL; update gate string in official `SEAL.json` |
| `bp_on_water` | NOT_RUN | Run `gate_bp_water_adjacency.py`; record in SEAL |
| Official blob reseal | Grok refreshed hashes post-FE-2 | Tasklet gold reseal cadence (#119 never opened) |

### Economics quality (stubs ≠ deck-grounded)

196 bite-2 records are **distance-tier stubs** (`bite2/distance_tier_stub`). Tasklet should replace with deck-grounded rows when sheets exist. `build_economics_sidecar.py` full refresh **overwrites** stubs — bite2 cascade uses `SKIP_ECON_SIDECAR_REFRESH=1` until Tasklet merges grounded economics.

### Narrative / proposal completeness

- ~190 null `journeys_unlocked` across 23 partners (Bite 5 hygiene merged; content still sparse)
- Bolt East Africa parity fields — merged in #116; verify on live `/bolt` sub-pages
- India sheets QA — wire `economics_url` on Adani/Reliance tracker cards

### Mesh / coverage (out of story scope)

Mesh fail: **3,036** routes. See `handoff/MESH-BACKLOG.md`.

---

## Suggested Tasklet priority order (updated)

1. **Formal gold SEAL** — acknowledge geometry_story PASS; run `bp_on_water`; reseal
2. **Centara deck appendix** — 7 corridors + economics refresh
3. **LINE MAN live Slides**
4. **Minor gold deck** refresh
5. **Hawaii growth_case** — Quanta-LR roadmap handling in `growth_frontend_block.py` OR mark partner forward-SAM-only in JSON
6. **Mint route_ids** for cote-dazur / d-marin / discovery-land (0 corridors today)
7. **Replace bite-2 stubs** with deck-grounded economics for didi, wsf, bc-ferries, etc.
8. **Grab deck KPI** — reconcile BKK marquee (Atlas BKK↔Hua Hin vs deck ICONSIAM→Wat Arun)

---

## Grok idle / watching

- No open PRs to process
- `main` deployable; production at `65df120f`
- Will auto-intake on next Tasklet PR (#127+)

---

*Grok seat · navier-atlas · handback for Tasklet triage*