# Tasklet handoff: planning employer hubs beyond Bay Area & New York

**Date:** 2026-08-14  
**Audience:** Tasklet (and any agent planning a third+ city)  
**Status:** Living handoff after Bay + NYC v2/v3 product iteration  
**Source of truth (code):** `employer-hub/` (template + `hubs/<id>/hub.json` + `registry.json`)  
**Do not fork pages.** New cities are **data + registry**, not new HTML/JS trees.

---

## 1. What we built (product, not tech)

Employer hubs are **public sales microsites** that sell a **commuter water network** to workplace / real-estate / HR decision-makers.

### The pitch (locked narrative)

1. **One terminal. Full network access.** An employer only needs a stop near the office.
2. **Transfers are the product.** Riders board near home, change once at a hub, arrive at the employer stop.
3. **Personal proof.** From → To route on the map with Navier time (incl. stops/transfers) vs AM-peak drive.
4. **Non-binding LOI.** Captures demand to sequence which corridor launches first.
5. **Cost is secondary.** Calculator supports Finance; it does not lead the page.

### Live hubs (reference implementations)

| Hub | Canonical | Alias | Calculator profile | Seasonal? |
|-----|-----------|-------|--------------------|-----------|
| Bay Area | `/employers/bay-area` | `/bay-employers` | `bay_productivity` | No |
| New York | `/employers/new-york` | `/ny-employers` | `nyc_parking_toll` | Yes (East End toggle) |

**Page order (v3, both cities):**

```
Hero → Your ride (map + trip planner) → Your office (catchment) → Why water (3 chips)
  → How employers join (products) → Rough cost (calculator) → Proof (one card) → LOI
```

---

## 2. Architecture (how cities plug in)

```
employer-hub/
  registry.json                 # enable hubs, canonical_path, aliases
  template/
    index.html                  # shared shell
    hub.css
    hub.js                      # map, phases, trip planner, calc, LOI
  hubs/
    bay-area/hub.json
    new-york/hub.json
    <new-city>/hub.json         # ADD HERE

scripts/build-employer-hubs.mjs # emits _dist/employers/<id>/ + alias copies
```

**Build:**

```bash
node scripts/build-employer-hubs.mjs
# full site (includes hubs if wired from build-site):
node scripts/build-site.mjs
```

**Deploy:** static `_dist` to Vercel (current practice: `cd _dist && vercel deploy --prod --yes --archive=tgz`).

**URLs:**

- Canonical: `/employers/<id>/`
- Aliases: full copies (e.g. `/bay-employers/`) for cleanUrls — register both in `registry.json` and `hub.aliases`.

**LOI:** `POST /api/loi` → Google Sheets webhook. Payload includes `hub_id` / `source`. **One sheet, hub column** — do not create a new tab per city unless product explicitly asks.

---

## 3. Network design rules (learned the hard way)

These are **non-negotiable** for map credibility and future-city planning.

### 3.1 Topology

| Rule | Do | Don’t |
|------|----|--------|
| **One spine per line** | Ordered A→B→C→D segments | Radial spokes all to one hub (reads as 4 separate lines) |
| **Geography-first names** | “Southeast Bay Line”, “East River Line” | Industry brands (“Biotech Crosstown”, “Medical Spine”) |
| **Transfer hubs** | Lines **end** at hubs; riders transfer | Redraw the same hub→hub segment on every express |
| **No dual paths** | One path at full network | P2 shortcut **and** full path both visible at full build-out |
| **phase_max** | Use for P1 short-turns that **disappear** at P2+ | Leave short-turn forever (double lines) |
| **Seasonal** | Opt-in per hub (`network.show_seasonal: true`) | Show “Seasonal East End” on cities without a seasonal product |

### 3.2 Geometry

- Coordinates: **`[lng, lat]`** always.
- Each segment needs densified **`water_path`** mid-channel (hand-authored or carefully scripted).
- **No land chords.** Visual QA: click every line at Full network; zoom corners (estuaries, peninsulas, bridges).
- Waterfront **stop pins** slightly offshore/at true landing — inland pins force paths onto land.
- `market.map.max_bounds` must include farthest stops (Pittsburg / Alviso / Norwalk-class extremes).
- `launch_bounds` = tight harbor/core for At Launch fit; full network uses all coords.

### 3.3 Phasing model

```
At launch (1)  → core trunks that can launch with LOI demand
+ Phase 2 (2)  → feeders / express / mid-build corridors  
Full network (3) → long-range / Carquinez / deep South Bay / outer feeders
```

- Segment `phase` = first phase the segment is live.
- Segment `phase_max` (optional) = last phase a segment is shown (short-turns).
- Line `phase` ≈ earliest useful phase; **visibility** is “any segment visible.”
- Stop `phase` should match when the pin appears (align with segments).

### 3.4 Transfer hubs (gold rings)

Mark with `role: interchange` / `interchange_primary` and `hub_rank: 1|2`.

Trip planner **only allows line changes at hubs** (`hub_rank ≤ 2` or role contains `interchange`). Plan 2–5 hubs per city, not “every pier.”

**Bay pattern:** Ferry Building (primary), Mission Bay, Oyster Point, Oakland JLS.  
**NY pattern:** Pier 11 + E 34th (primaries), BPC, Paulus, E 90th, Pier 79 (transfer-only, not a branch).

---

## 4. `hub.json` checklist for a new city

Copy structure from **Bay** (simpler, no seasonal) or **NY** (seasonal + parking/toll calc). Minimum fields:

### Identity & market

```json
{
  "id": "miami",
  "version": "YYYY-MM-DD-v1",
  "aliases": ["miami-employers"],
  "market": {
    "label": "Miami",
    "short_label": "Miami",
    "tagline": "Employer water network",
    "eyebrow": "Miami · Employer water commute",
    "cluster_city_id": null,
    "contact_email": "jaideep@navierboat.com",
    "map": {
      "center": [-80.19, 25.78],
      "zoom": 10.5,
      "max_bounds": [[west, south], [east, north]],
      "fit_max_zoom": 12,
      "launch_bounds": [[west, south], [east, north]],
      "aria_label": "Miami employer water network map"
    }
  },
  "brand": {
    "title": "Navier · Miami Employer Network",
    "nav_tag": "Employer network"
  }
}
```

### Network controls

```json
"network": {
  "phase_labels": ["At launch", "+ Phase 2", "Full network"],
  "default_phase": 1,
  "map_layout": "full_bleed",
  "show_seasonal": false,
  "show_seasonal_default": false
}
```

Set `"show_seasonal": true` and `"seasonal_label": "..."` only if a seasonal line exists.

### Stops

Each stop:

| Field | Notes |
|-------|--------|
| `key` | Stable slug (`ferry-building`) |
| `label` | Public name |
| `lng`, `lat` | Waterfront-accurate |
| `phase` | When pin appears |
| `role` | `station` \| `interchange` \| `interchange_primary` |
| `hub_rank` | 1 primary, 2 secondary hub, 3 normal |
| `serves` | Array of short employer/catchment phrases |
| `resolved_bp_id` | Prefer sealed BP when available; optional |
| `seasonal` / `exec_only` | Rare; `exec_only` never shown on public map |

### Lines

```json
{
  "id": "MI-1",
  "name": "Biscayne Line",
  "type": "trunk|feeder|express|seasonal",
  "phase": 1,
  "color": "#e0cb8f",
  "flagship": true,
  "stops": ["a", "b", "c"],
  "segments": [
    {
      "from": "a",
      "to": "b",
      "phase": 1,
      "distance_nm": 3.2,
      "water_min": 12,
      "water_path": [[lng, lat], ...],
      "phase_max": null
    }
  ],
  "water_path": [ /* optional MultiLineString of segment paths */ ],
  "phase_notes": "Internal only — stripped from client"
}
```

**Line count guidance:** Prefer **4–7 public lines** + optional seasonal. NY-style sprawl (9) works only if spines stay clean. Avoid EXEC/airport shuttles on the public employer map unless product insists.

### Catchment (office cards)

```json
"catchment": [
  {
    "anchor": "Downtown campus name",
    "anchor_stop": "stop-key",
    "phase1_stations": 8,
    "full_network_stations": 18,
    "derived": true
  }
]
```

UI: tap card → sets trip **To**, LOI office stop, highlights reachable origins at current phase.

### Trip planner

```json
"trip_planner": {
  "enabled": true,
  "transfer_min": 8,
  "stop_dwell_min": 2,
  "max_transfers": 2,
  "drive_label": "Typical AM peak drive",
  "navier_label": "Navier water time (incl. stops & transfers)",
  "caveat": "Indicative planning times, not a published timetable.",
  "drive_am_peak": {
    "stop-a|stop-b": 55
  }
}
```

- Build full pair matrix with peak-adjusted haversine (see Bay/NY generation pattern).
- **Override 10–20 flagship OD pairs** with human-credible peak times for demos.
- Deep links: `?stop=<office>`, `?from=&to=`, `#trip=from,to`.

### Calculator

Pick **one** profile and pass `worked_assert` so build fails on math drift:

| Profile | Use when | Assert pattern |
|---------|----------|----------------|
| `bay_productivity` | Productivity / parking-subsidy markets | net_incremental + per_rider (Bay: $4500 / $75) |
| `nyc_parking_toll` | Toll + parking dominated CBDs | net_employer_cost_per_rider vs benchmark |

New markets may need a **third profile** later (e.g. pure productivity, or transit-subsidy). Prefer reusing Bay/NY until math is locked with founders.

### Products (LOI flavors)

Two paths (keep simple):

1. **Reserve seats** / pilot capacity (N30-class story)
2. **Anchor a line** (commit demand that sequences a trunk)

`products.section_title`: “How employers join”  
`loi.flavors` + `flavor_order` drive the LOI option cards.

### Copy (network-first)

Required-ish keys (see Bay/NY `copy`):

| Key | Purpose |
|-----|---------|
| `hero_headline` | “One terminal. The whole {market} network.” |
| `hero_sub` | Transfers + hydrofoil one-liner |
| `hero_stats` | Optional: terminals / lines / “1 stop plugs in” |
| `hero_cta_network` | “Find a route to my office” |
| `hero_cta_loi` / `nav_cta` | “Reserve interest” |
| `network_title` / `network_lead` / `network_footnote` | Map section |
| `office_title` / `office_lead` / `office_insight` | Catchment section |
| `why_title` / `why_lead` / `problem_chips` | 3 chips max |
| `proof_title` / `proof_lead` / `stripe_lesson` | One proof card |
| `calc_title` / `calc_lead_html` | Secondary cost |
| `loi_title` / `loi_cta` | Capture |
| `launch_trigger` | Seat threshold honesty |

### Gates / QA

- `gates.banned_terms` / dock-language scan: avoid “unlock the dock” style dependency copy in customer-facing fields.
- `schedules_note`: no invented timetables.
- `bp_gap` optional internal ledger (stripped from client).

---

## 5. Page & UX contract (do not re-break)

### Nav

`Your ride · Your office · Cost · Reserve`

### Primary conversion path

```
Hero CTA → Find my ride (To = office) → time save → LOI (stop prefilled)
```

Secondary: campus card → same.

### Trip planner behavior (implemented in `hub.js`)

- Graph = visible segments at `activePhase` (+ seasonal if on).
- Dijkstra on `(stop, lineId)` state; transfers only at hubs; cost = water_min + transfer_min.
- Max 2 transfers default.
- Map: dim network, highlight path, fit bounds to path.
- No path this phase → probe later phases and offer “Show + Phase 2 / Full network”.
- Prefills: LOI office stop, preferred line, calculator `water_min` / `car_min` when fields exist.

### Seasonal CSS gotcha

`.seasonal-toggle { display: inline-flex }` overrides bare `[hidden]`. Template forces `display:none !important` + `.is-hidden`. Keep that when editing CSS.

### Full-bleed map CSS gotcha

`margin: auto` on `.map-shell` inside a grid parent collapses map width unless `width: 100%`. Do not remove.

---

## 6. Playbook: stand up city N (Tasklet checklist)

### Phase A — Market design (before code)

1. **Employer density on water** — Which campuses sit on real or plausible landings?
2. **Pain metric** — Bridge? Congestion charge? Parking? Island access? → drives calculator profile + chips.
3. **2–5 transfer hubs** — Named, gold-ring ready.
4. **4–7 lines max at v1** — trunks at P1; feeders/express P2; outer P3.
5. **Spine order** — Write stop sequences as A→B→C before drawing geometry.
6. **Seasonal?** — Only if a real product (Hamptons-class). Else `show_seasonal: false`.
7. **LOI story** — Seats vs anchor line; launch seat band (~60–80).
8. **Hero one-liner** — “One terminal. The whole {place} network.”

### Phase B — Data

1. Create `employer-hub/hubs/<id>/hub.json` from Bay (template).
2. Stops with waterfront coords + phases + hub ranks.
3. Lines with sequential segments + densified mid-channel `water_path` + `water_min`.
4. Catchment 3–6 employer anchors.
5. `trip_planner.drive_am_peak` matrix + flagship overrides.
6. Calculator profile + `worked_assert`.
7. Network-first `copy` + products + loi flavors.
8. Hero image: `hubs/<id>/assets/hero.jpg` (or build fallback from template).

### Phase C — Register & build

1. Add entry to `employer-hub/registry.json` (`enabled`, `public`, `canonical_path`, `aliases`).
2. `node scripts/build-employer-hubs.mjs` — fix assert/copy/dock-scan failures.
3. Visual QA:
   - At launch / Phase 2 / Full network for every line
   - Trip: 3 flagship OD pairs + one multi-transfer
   - Office card → map + LOI stop
   - No seasonal toggle if disabled
   - Mobile sticky CTA after trip
4. Deploy `_dist` prod; hard-refresh aliases.

### Phase D — Content gates

- No fake schedules.
- No land-cutting paths.
- No dual express chords.
- No industry line names unless founders insist.
- Proof section: **one card**, not a curriculum.

---

## 7. Reference topologies (copy patterns, not geography)

### Bay Area (streamlined)

| Line | Spine (simplified) | Phase idea |
|------|-------------------|------------|
| Peninsula Trunk | FB → Mission Bay → OP → Coyote Point → RWC → Alviso | P1 core; South Bay extends |
| Marin Line | Larkspur → Tiburon → Sausalito → **FB** (ends) | Transfer at FB |
| East Bay Trunk | JLS → Main St → FB | P1 |
| Southeast Bay Line | Hayward → San Leandro → Harbor Bay → **OP** | P2; OP transfer |
| North Bay Express | Pittsburg → Benicia → Vallejo → Hercules → Richmond → Berkeley → Emeryville → TI → FB | Outer P3 |

### New York (streamlined)

| Line | Spine idea | Phase idea |
|------|------------|------------|
| East River Line | E90 → E34 → Pier 11 | P1 spine / transfers |
| Hudson Line | Edgewater → … → Paulus → BPC → Pier 11 | Single NJ→downtown spine |
| Brooklyn Line | P1 short-turn DUMBO–P11 (`phase_max`); P2 full waterfront | |
| East River Feeder | Queens chain → **E34** | Ends at hub |
| CT / LI Sound express | … → **E34** | No E34→P11 redraw |
| Bronx | … → **E90** | Transfer to East River Line |
| SI | St. George → Pier 11 | P3 |
| East End Seasonal | Toggle only | `show_seasonal: true` |

---

## 8. Anti-patterns (seen in Bay/NY iterations)

1. **Hub-and-spoke segments** (“everything to Ferry Building”) → looks like multiple lines + land cuts.
2. **Keeping a P1 short-turn forever** → dual paths; use `phase_max`.
3. **Expresses that re-draw the spine** to the primary hub → map spaghetti; end at secondary hub.
4. **Seasonal UI on every city** → CSS `hidden` override; gate with `show_seasonal`.
5. **Map as page appendix** → network must lead after hero; education below.
6. **Calculator as hero CTA** → demote; trip planner is the demo.
7. **EXEC/airport as peer network lines** → hide or omit from employer map.
8. **Invented timetables** — water_min is indicative only.

---

## 9. Candidate future cities (planning lens, not a commitment)

Tasklet should score cities on:

| Criterion | Weight |
|-----------|--------|
| Employer density on waterfront / near landings | High |
| Congestion or toll pain story | High |
| Existing ferry culture or WETA-like legitimacy | Medium |
| Clear 2–5 hub structure | High |
| Founder GTM / LOI pipeline | High |
| Geometry feasibility (not landlocked) | Hard gate |

**Illustrative classes** (for research, not roadmap):

- **Island / archipelago** — transfers natural (e.g. harbor cities).
- **Bridge-tax metros** — Bay-like productivity calc.
- **Toll CBD metros** — NY-like parking+toll calc.
- **Tourism + commute mix** — seasonal only if product is real.

For each shortlist city, deliver a **1-pager** before `hub.json`:

1. Hubs (names + why)  
2. Line list with ordered stops + phases  
3. Calculator profile choice  
4. Top 5 LOI employer anchors  
5. Flagship From→To demos (3 pairs)  
6. Seasonal yes/no  

Then implement per §6.

---

## 10. Files Tasklet should touch for city N

| File | Action |
|------|--------|
| `employer-hub/hubs/<id>/hub.json` | Create |
| `employer-hub/hubs/<id>/assets/hero.jpg` | Add |
| `employer-hub/registry.json` | Register |
| `employer-hub/template/*` | **Only if** multi-city capability needed |
| `scripts/build-employer-hubs.mjs` | Only if new calculator profile |
| `api/loi.js` / Sheets | Confirm `hub_id` column; no new sheet |
| Vercel `_dist` deploy | After build |

---

## 11. Definition of done (new city)

- [ ] Registry entry + alias resolve 200  
- [ ] At launch shows ≥1 coherent trunk spine, not empty map  
- [ ] Full network: every line continuous, water-only, no dual chords  
- [ ] Trip planner: 3 flagship OD pairs work; multi-transfer if hubs exist  
- [ ] Office card sets To + LOI stop  
- [ ] Calculator `worked_assert` passes in build  
- [ ] Seasonal hidden unless product exists  
- [ ] Copy is network-first (“one terminal / full network”)  
- [ ] LOI submit works with `hub_id`  
- [ ] Mobile: trip + sticky reserve usable  

---

## 12. Related docs

| Path | Role |
|------|------|
| `employer-hub/README.md` | Quick start / add-a-city |
| `handoff/employer-hub/ARCHITECTURE.md` | Early locked decisions (partially superseded by this doc for UX) |
| `handoff/employer-hub-v2/` | PR #351 network expansion notes (historical) |
| Live Bay | https://navier-atlas.vercel.app/bay-employers |
| Live NY | https://navier-atlas.vercel.app/ny-employers |

---

## 13. One-paragraph brief for Tasklet planning prompts

> Build the next employer hub as a **hub.json + registry entry** on the shared `employer-hub` template. Design a **small set of sequential water spines** with **2–5 transfer hubs**, mid-channel geometry, and phase 1/2/3 extensions. Sell **network access from one office stop**, prove it with **From→To routing vs AM peak drive**, capture demand with a **non-binding LOI** (`hub_id` on the shared sheet). Do not fork the page, invent schedules, show seasonal UI without a seasonal line, or redraw dual paths to the same hub. Use Bay Area and New York `hub.json` as reference implementations; follow page order Hero → Ride map → Office → Why → Join → Cost → Proof → LOI.

---


## 14. Line topology (MECE) — adopted 2026-08-15

Source: `handoff/employer-hub/GROK-HANDOFF-mece-line-design-2026-08-15.md` (Grok, PR #356). Lines are a **product topology for humans**, not a dump of the routing graph. Author spines first; phase lives on stops/segments, not on parallel product names.

### Target ratios (per independent cluster)
| Terminals (public map) | Target lines | Hard ceiling |
|---|---|---|
| ≤ 8 | 2–3 | 4 |
| 9–14 | 3–4 | 5 |
| 15–22 | 4–5 | 6 |

Smell test: if `lines > stops/2`, re-merge before handoff.

### Every line must be one MECE pattern
**Spine** (geographic order along one water body) · **Branch** (second water body joining a hub) · **Spur/link** (short job or no-wake circulator) · **Exclusive spoke** (multiple origins, same hub, different water, no shared intermediates) · **Isolated sub-network** (genuinely separate water system, e.g. Tacoma Narrows).

Not MECE: two lines sharing ≥2 consecutive stops for marketing; a one-stop feeder that is really a phase-2 station on a spine; a long-haul express that exists only because the stop is far (put it on the spine as `phase: 3`). A lonely long-haul is correct **only** when the geography is a separate water system **and** shares no intermediate with the main spine. Event-only notions, incumbent head-to-head pairs, speed-stranded corridors, and orphan demand stay in `watchlist`/`decision_ledger`/`no_landing`/`note_internal` — never minted as map lines.

### Tasklet pre-PR checklist
1. Can each line be named in one geographic phrase?
2. Does any segment appear on two lines? Merge.
3. Is every `phase ≥ 2` stop an extension of a line, not a new product?
4. `len(lines) ≤ ceil(len(stops)/2)` per cluster?
5. Catchment counts match the post-merge graph?
6. Hard gates (speed labels, incumbent copy, exclusions, dual-cluster rules) still hold?

### Acceptance bullet for every per-city GROK-SPEC
> Line count ≤ ceil(stops/2) per cluster; no orphan long-haul line; no duplicate multi-stop paths; merged lines carry `legacy_ids`.

This section also governs **archetype views** (Public Partners, Fleet Investors): they render the same hub topology and inherit these rules unchanged.

---

*End of handoff. Update this file when a third city ships or calculator profiles expand.*
