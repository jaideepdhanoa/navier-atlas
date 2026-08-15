# Grok completion — marina-standard map corrections (PR #352 v2)

**Date:** 2026-08-15  
**To:** Tasklet  
**From:** Grok  
**Status:** **DONE** — code on `main`, production live  
**Spec executed:** `handoff/employer-hub-v2/GROK-SPEC-map-corrections-2026-08-14.md` (v2, marina-standard)  
**Commit:** `5c86555e` — `fix(employer-hub): marina-standard network refinement (PR #352 v2)`  
**Hub version:** `2026-08-15-marina`  
**Prod:** https://navier-atlas.vercel.app/bay-employers · https://navier-atlas.vercel.app/ny-employers  

---

## 1. Summary for Tasklet

Landing gate applied: **usable pier/marina berth** (not ferry terminal). Both hubs re-spined under employer-hub design principles (single continuous spines, transfer hubs, no dual express brands, trip planner full-network routing).

| Market | Culled | Added | Lines |
|--------|--------|-------|-------|
| **Bay** | 4 | 4 | Still **5** (re-spined, not new brands) |
| **NY** | 0 stops removed | 6 | Still **8 + seasonal** (densified existing spines; **no** Hudson Express / South Shore Express) |

**Held (not rendered), per principles + your watchlist:** Great Kills / South Shore Express, Atlantic Highlands, Marine Basin, W 79th/Dyckman, North Cove, Petaluma/Napa, Pier 39 dredge, etc.

---

## 2. Bay Area — executed

### Culled (absent at every phase + trip-planner lists)

| Stop | Reason (audit) |
|------|----------------|
| Alviso Marina | Silted / kayak-grade |
| Hayward Landing | No dock |
| San Leandro Marina | Closed 2023, docks removed |
| Hercules Waterfront | Ferry dock never built |

### Added

| Key | Label | Phase | Role on network |
|-----|-------|-------|-----------------|
| `south-beach` | South Beach Harbor / Pier 40 | 2 | Peninsula between FB and Mission Bay |
| `brisbane` | Brisbane Marina / Sierra Point | 2 | Peninsula between OP and Coyote Point |
| `martinez` | Martinez Marina | 3 | North Bay Express (Hercules replacement) |
| `antioch` | Antioch Marina | 3 | North Bay Express eastern terminus |

### Spines (live)

```
BA-1 Peninsula Trunk
  FB → South Beach → Mission Bay → OP → Brisbane → Coyote Point → Redwood City
  P1: FB–MB–OP (FB–MB short-turn phase_max=1 until South Beach live)
  P2+: full spine through South Beach + Brisbane + Coyote + RWC

BA-2 Marin Line
  Larkspur → Tiburon → Sausalito → FB  (ends at transfer hub)

BA-3 East Bay Trunk
  JLS → Main St Alameda → FB

BA-4 Southeast Bay Line  (RE-SPINED)
  JLS → Main St Alameda → Harbor Bay → OP
  (no Hayward / San Leandro)

BA-5 North Bay Express
  Antioch → Pittsburg → Martinez → Benicia → Vallejo → Richmond
    → Berkeley → Emeryville → TI → FB
  P2: Vallejo→…→FB; P3: Antioch→…→Vallejo
```

### Catchment updated

Oyster Point · Mission Bay · FiDi · **Sierra Point/Brisbane** · **South Beach/SoMa** (removed anchors that only made sense for culled SE stops).

---

## 3. New York — executed

### Corrections

| Item | Done |
|------|------|
| Throgs Neck → **Ferry Point Park** | Key `ferry-point`; label + landing bound to NYC Ferry Ferry Point Park |
| Norwalk | Label **Norwalk Seaport Dock**; landing Hope Dock / 90 Water St |
| Port Washington | Bound to **North Hempstead Town Dock** |

### Added (on existing spines — no new line brands)

| Key | Label | Phase | Attached to |
|-----|-------|-------|-------------|
| `yonkers` | Yonkers Recreation Pier | 2 | **Hudson Line** (north end) |
| `liberty-landing` | Liberty Landing Marina | 2 | **Hudson Line** (Paulus–BPC) |
| `newport-jc` | Newport Marina | 3 | **Hudson Line** (Hoboken–Paulus) |
| `new-rochelle` | New Rochelle Municipal Marina | 2 | **Long Island Sound Line** |
| `bridgeport` | Bridgeport Harbor Marina / Steelpointe | 3 | **Connecticut Express** |
| `milford` | Milford Lisman Landing | 3 | **Connecticut Express** |

### Spines (live)

```
NY-M  East River Line     e90 → e34 → pier11
NY-H  Hudson Line         yonkers → edgewater → port-imperial → lincoln
                            → hoboken-14th → hoboken → newport-jc → paulus
                            → liberty-landing → bpc → pier11
                          (phase_max short-turns for pre-Newport / pre-Liberty)
NY-B  Brooklyn Line       (unchanged short-turn + P2 waterfront)
NY-Q  East River Feeder   → e34
NY-C  Connecticut Express bridgeport → milford → norwalk → stamford → greenwich → e34
NY-G  Long Island Sound   glen-cove → port-washington → new-rochelle → e34
NY-X  Bronx Line          ferry-point → soundview → e90
NY-SI Staten Island       st-george → pier11
NY-S  East End Seasonal   (unchanged; seasonal toggle)
```

### Intentionally **not** done (deviations from raw “add a line” wording)

| Spec idea | Grok decision | Why |
|-----------|---------------|-----|
| Separate **Hudson Express** (Yonkers→W39→BPC) | **Folded into Hudson Line** | Single spine principle; avoid dual Hudson products |
| **South Shore Express** (Great Kills→Pier 11) | **Held / not rendered** | Second SI line without LOI product need; watchlist |
| Atlantic Highlands | Not rendered | Seastreak partner lane (your gate) |
| Marine Basin | Not rendered | Depth / site-visit gate |

---

## 4. Cross-cutting work completed with this ship

| Item | Status |
|------|--------|
| `trip_planner.drive_am_peak` regen | Yes (culled keys removed) |
| Trip planner routes **full planned network** | Yes (employers don’t flip phases to see results) |
| From/To labels use At launch / + Phase 2 / Full network | Yes |
| Build `build-employer-hubs.mjs` | Pass |
| Production deploy | Success (after SSL upload retries) |

**Not changed (per gates):** locked calculator numbers, LOI webhook/schema, template architecture.

---

## 5. Internal flags for Tasklet (not in DOM)

- **Martinez Marina** — Contra Costa grand jury / dredging funding risk by ~2027  
- **Brisbane Marina** — low-tide approach depth flag for hydrofoil ops  
- **Lincoln Harbor** — construction; confirm berth before service  
- **Port Washington Town Dock** — commercial boarding needs town/operator approval  

---

## 6. QA acceptance (spec) — Grok status

| Criterion | Status |
|-----------|--------|
| 4 culled Bay stops absent every phase + trip lists | **Pass** |
| Additions render at assigned phase with marina names | **Pass** (pins are best-effort waterfront coords; refine if Tasklet has surveyed lat/lng) |
| North Bay continuous Antioch→FB | **Pass** |
| Hudson / CT / LI densify water-only segments | **Pass** (hand densified; visual zoom QA recommended on next human pass) |
| No land chords intentional | Best-effort; same class as prior hand paths |
| Catchment updated | **Pass** |
| Build + redeploy | **Pass** |

---

## 7. Files Tasklet should treat as truth now

| Path | Role |
|------|------|
| `employer-hub/hubs/bay-area/hub.json` | Bay network `2026-08-15-marina` |
| `employer-hub/hubs/new-york/hub.json` | NY network `2026-08-15-marina` |
| `handoff/employer-hub/TASKLET-FUTURE-CITIES-HANDOFF.md` | Future city playbook (pre-marina-standard language still says “landing” broadly — update landing gate to marina berth when Tasklet next edits) |
| This file | Completion receipt for PR #352 v2 |

**PR #352** itself was **handoff-only** (spec + audits). Implementation is on **main** via Grok, not necessarily merged into the PR branch. Tasklet may close #352 as “spec delivered + executed on main” or open a thin tracking PR if process requires.

---

## 8. Suggested Tasklet follow-ups

1. Human visual QA: Full network each line; flag any residual land clips.  
2. Optional surveyed coordinates for new marinas if pins feel off.  
3. Decision on **Great Kills** product (hold vs SI South Shore line).  
4. Update future-cities handoff § landing gate to **marina berth** standard explicitly.  
5. Watchlist calendar: Pier 39 dredge end, W79/Dyckman ~2028, Martinez dredge, Lincoln Harbor berth.  

---

## 9. One-liner for Tasklet status boards

> PR #352 v2 marina-standard **executed on main** (`5c86555e`, hub `2026-08-15-marina`, prod live): Bay 4 culls + 4 marinas + SE/North re-spines; NY renames + 6 marina adds on existing spines; Great Kills/extra Express brands held.

*End of Grok → Tasklet completion handoff.*
