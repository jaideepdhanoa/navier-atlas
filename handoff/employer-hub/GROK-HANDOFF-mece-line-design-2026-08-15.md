# Grok → Tasklet handoff: MECE employer-hub line design

**Date:** 2026-08-15 · **Author:** Grok · **Audience:** Tasklet (future-city authoring)  
**Build PR:** [#356](https://github.com/jaideepdhanoa/navier-atlas/pull/356) · commits include DC/Miami/Boston/Seattle MECE refactors  
**Status:** Implemented on live hubs (Bay/NY untouched; DC, Miami, Boston, Seattle streamlined; San Diego already lean)

---

## Why this exists

Tasklet-authored v1 line lists for next cities optimized for **corridor inventory completeness** (every OD pair, every phase product, every event/feeder named). That produces microsites where:

- **Line count ≫ terminal count** (e.g. DC 7 lines / 11 stops; Boston 9 / 18; Miami 10 / 16)
- Several “lines” are **the same water path re-labeled** (OT↔Wharf appeared on four DC lines)
- Long-haul or edge stops become **orphan expresses** (Woodbridge Express; Scituate Express; Lynn Feeder) that look accidental on the map
- Customers cannot form a mental model of “which corridor am I on?”

**Grok rule going forward:** lines are a **product topology for humans**, not a dump of every segment in the routing graph. Stops carry phase; segments can `phase` / `phase_max`. One spine absorbs extensions.

---

## Design principles (author these into future hub specs)

### 1. Target ratio

| Terminals (public map) | Target lines (per independent cluster) | Hard ceiling |
|------------------------|----------------------------------------|--------------|
| ≤ 8 | 2–3 | 4 |
| 9–14 | 3–4 | 5 |
| 15–22 | 4–5 | 6 |
| Dual-cluster hub | Apply per cluster; total often 4–6 | Don’t sum “every spoke” blindly |

**Smell test:** if `lines > stops/2`, re-merge before handoff.

### 2. MECE corridors (Mutually Exclusive, Collectively Exhaustive)

Each **line** should be one of:

| Pattern | When to use | Example |
|---------|-------------|---------|
| **Spine** | Geographic order along one water body / shore | Potomac Line south→north; North Shore Line |
| **Branch** | Second water body that joins a hub | Anacostia Line from Old Town |
| **Spur / link** | Short jobs or no-wake circulator | Pentagon Link; Inner Harbor Line |
| **Exclusive spoke** | Multiple origins, **same hub**, **different water**, no shared intermediate path | Miami Island / Grove / Beach → Brickell |
| **Isolated sub-network** | Intentionally disconnected geography | Seattle Narrows (Gig Harbor↔Tacoma); dual-cluster rules |

**Not MECE (avoid):**

- Two lines that share ≥2 consecutive stops for “product marketing” only  
- A one-stop feeder that is really a phase-2 station on an existing spine  
- A long-haul express that only exists because the stop is far — put it on the spine as `phase: 3`

### 3. Phase belongs on stops (and segments), not on parallel product names

| Do | Don’t |
|----|-------|
| One **South Shore Line** with Scituate `phase: 3` | Scituate Express + Weymouth Feeder + South Shore Express |
| One **Potomac Line** with Occoquan `phase: 3` | Woodbridge Express + South Feeder Express + Monument Line |
| Segment `phase_max: 1` short-turn until intermediate stop opens | Separate “shuttle line” that redraws the same channel |

Template already supports:

- `stop.phase` — visibility by phase toggle  
- `segment.phase` — when the leg appears  
- `segment.phase_max` — short-turn drops out when full spine is live  
- Trip planner always routes on **full planned network** (short-turns with `phase_max < 3` excluded from trip graph)

### 4. Dual-cluster hubs (Miami, Seattle)

- **Zero cross-cluster segments** (already gated)  
- Apply MECE **inside each cluster**  
- Cluster toggle + copy.two_networks stay mandatory  
- Do not invent “future connector” lines for symmetry

### 5. When a lonely long-haul is correct

Only if **both** are true:

1. Geography is a **separate water system** (e.g. Tacoma Narrows ≠ Elliott Bay), and  
2. There is **no shared intermediate** on the main spine.

Otherwise: attach to the spine as a phase-gated terminal.

### 6. What stays in inventory, not as lines

Keep in `watchlist` / `decision_ledger` / `no_landing` / `note_internal`:

- Event-only notions (unless it’s a real P2 stop on a spine)  
- Partner/incumbent head-to-head pairs  
- Speed-stranded corridors (DC Ship Canal analogue)  
- Orphan demand with no landing  

Do **not** mint a map line just to show Tasklet scanned the OD pair.

### 7. Authored JSON checklist (Tasklet pre-PR)

Before opening a handoff PR, Tasklet should answer:

1. Can I name each line in one geographic phrase?  
2. Does any segment appear on two lines? If yes, merge.  
3. Is every `phase ≥ 2` stop an **extension of a line**, not a new product?  
4. `len(lines) ≤ ceil(len(stops)/2)` (per cluster)?  
5. Catchment counts still match the **graph after merge**?  
6. Gates (speed, incumbent, exclusion lists) still hold?

---

## What we changed (by city)

### Washington DC — 7 → 3 lines (11 stops)

| Before | After |
|--------|--------|
| Monument, Capitol, Pentagon Shuttle, NL Shuttle, Audi Event, South Feeder, **Woodbridge Express** | **Potomac Line** · **Anacostia Line** · **Pentagon Link** |

- **Potomac spine:** Occoquan → Ft Washington → National Harbor → Old Town → Daingerfield → Wharf → Georgetown  
  - Woodbridge is the **southern terminus (P3)**, not a solo express  
- **Anacostia branch:** Old Town → James Creek → Navy Yard → Yards  
- **Pentagon spur:** Wharf → Columbia Island (P2)

### Boston — 9 → 5 lines (18 stops)

| Before | After |
|--------|--------|
| North Shore, South Shore Express, Quincy, Lynn Feeder, Winthrop Feeder, Inner Harbor, Weymouth Feeder, Scituate Express, Riverside | **North Shore** · **South Shore** · **Quincy** · **Inner Harbor** · **Riverside** |

- Lynn / Beverly on **North Shore** (not orphan feeders)  
- Weymouth / Scituate on **South Shore** (not orphan express)  
- Winthrop folded into **Inner Harbor** (no-wake family)  
- Riverside stays separate (Mystic geography + all-no-wake honesty)

### Miami / FtL — 10 → 5 lines (16 stops, dual cluster)

| Before | After |
|--------|--------|
| Island, Grove, Beach, North Bay, Gold Coast, Bay, Aventura Seasonal, Hollywood Commuter, Isles Shuttle, Pompano | **Island · Grove · Beach** (spokes) · **North Bay** spine · **Fort Lauderdale** ICW |

- Brickell **spokes kept** (true MECE: exclusive origins, different water)  
- Four north-bay products → **one North Bay Line** (Aventura remains summer-season stop)  
- Three FTL products → **one Fort Lauderdale Line**  
- Still **no Miami↔FTL connector**

### Seattle — 8 → 5 lines (14 stops, dual cluster)

| Before | After |
|--------|--------|
| Bridge Bypass, Boeing, Kirkland Direct, Expedia Shuttle, Sound Gate, Des Moines, Kingston, Narrows | **Cross-Lake** · **Eastside** · **Elliott Bay** · **Sound** · **Narrows** |

- Lake: cross-lake flagship + **one Eastside spine** (Kirkland · Carillon · Meydenbauer · Coulon)  
- Sound: local Elliott Bay + **one regional Sound line** (Bainbridge / Des Moines / Edmonds / Kingston)  
- **Narrows kept** as isolated sub-network (correct exception)  
- Ship Canal still forbidden; no Lake↔Sound connector

### San Diego — already 3 / 7 (no change this pass)

South Bay · Point Loma · Bridge was already near-MECE. Left alone.

### Bay Area / New York

Unchanged this pass (larger networks; revisit only if line density smells).

---

## Implementation notes for Grok (and Tasklet reviewers)

- Prefer **editing `hubs/<id>/hub.json` lines** over inventing new template features  
- Reuse existing `water_path`s when merging; invent mid-channel waypoints only for new adjacencies  
- Preserve hard gates: speed labels, incumbent copy, exclusion greps, dual-cluster rules  
- Update `copy.hero_stats`, `network_lead`, `network_footnote`, `schedules_note` when line counts change  
- `legacy_ids` on lines document which authored products were merged (for audit)

---

## Suggested Tasklet doc updates

Please fold into:

1. `handoff/employer-hub/TASKLET-FUTURE-CITIES-HANDOFF.md` (or successor) — new section **“Line topology (MECE)”** with the table in §1–2 above  
2. Per-city GROK-SPEC template — acceptance bullet:  
   `Line count ≤ ceil(stops/2) per cluster; no orphan long-haul line; no duplicate multi-stop paths`  
3. Authored `*-hub-v1-stops-lines.json` — author **spines first**, then mark phase on stops; only then add a line if geography fails the “lonely long-haul” test  

---

## Live paths (post-deploy)

| Hub | Canonical | Lines (now) |
|-----|-----------|-------------|
| Washington DC | `/employers/washington-dc` | 3 |
| Miami / FtL | `/employers/miami` | 5 (2 clusters) |
| Boston | `/employers/boston` | 5 |
| Seattle | `/employers/seattle` | 5 |
| San Diego | `/employers/san-diego` | 3 |

Build PR: https://github.com/jaideepdhanoa/navier-atlas/pull/356  

---

## One-paragraph summary for Tasklet queue

> When authoring employer-hub lines, optimize for **customer-readable MECE corridors**, not OD inventory completeness. Prefer one geographic spine with phase-gated terminals over many named feeders that redraw the same water. Orphan long-haul expresses (e.g. Woodbridge, Scituate, Lynn) almost always belong on the spine at Phase 2/3. Exclusive multi-spoke-to-hub patterns (Miami Brickell) are fine; overlapping multi-stop paths are not. Dual-cluster rules unchanged. Grok streamlined DC/Boston/Miami/Seattle to this standard on 2026-08-15; please document and author next cities (and any v2 revisits) accordingly.
