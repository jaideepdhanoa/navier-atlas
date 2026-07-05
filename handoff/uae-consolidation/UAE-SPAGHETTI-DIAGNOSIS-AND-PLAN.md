# UAE map — why it's a spaghetti disaster, and how we fix it

**Date:** 2026-07-05 · **Author:** Tasklet · **Source:** `data-clean/ROUTES.json` (8,135 routes; UAE slice analysed)

## The numbers (UAE today)
- **936** routes touch the UAE. **666** are actually rendered (270 are hidden/quarantined).
- **348** unique boarding points are wired into those visible routes.
- **202** rendered routes are **flagged as crossing land** (`_qa_land_flag=true`) — 176 of them *inside a single city*, and **78 cut across more than 5 km of land** (max 28 km). These are the lines you see slicing over the Palm, over Deira, across islands, and over the Hajar mountains to the east coast.
- **23** rendered routes are **longer than 70 nm** (beyond the vessel's range — they should never be corridors).
- **10** are cross-border noise (Qatar / Oman / Bahrain edges leaking into the UAE view).
- Even after removing all of the above, **450** "clean" routes remain — and **146 of those are trivial sub-2 nm hops**. Hub BPs are wired at **degree 40–42** (one point connected to 40+ others).

By contrast Singapore looks calmer only because it has fewer BPs and lighter meshing — but it has the same disease in milder form, and a couple of egregious land-cutters.

## Why it happened (root causes)
1. **All-pairs meshing.** The generator connected *every* BP in a city to *every* other BP → combinatorial explosion. That's the spaghetti.
2. **Land-crossing geometry was rendered anyway.** There are already **788 hand-waypoint pairs** authored for the UAE, but they were never fully applied at seal — so 202 straight-line land-cutters are still on the map despite being QA-flagged.
3. **Dirty boarding points.** Bare city centroids (`Abu Dhabi`, `Fujairah`, `Ras Al Khaimah`), activity operators that aren't real transfer piers (`Jet Ski Abu Dhabi Waves`, `MSC`, `Boat ramp`, `DiveCampus Diving Club`), plus planned/duplicate jetties.
4. **West coast + east coast meshed together.** Gulf-side emirates (Dubai/AD/Sharjah/RAK) and the Gulf-of-Oman side (Fujairah/Khor Fakkan/Dibba) were treated as one pool → routes drawn straight across the mountains.

## Why Careem, Bolt, Yango, and Noon each show *different* routes
This surprised us too, and it has a clean explanation: **routes are not tagged by commercial partner.** A route's only partner-ish fields are `_pta_partner` (for public transit authorities) and `platform` (the vessel class). Nothing says "this corridor belongs to Bolt."

Instead, the front-end renders **each partner's own `_map_scope`** — a list of `registry_keys` + `cluster_city_ids` + an `inheritance_policy`. And those four scopes are all different:
- **Bolt** — its own curated footprint (Saadiyat, Yas, Sir Bani Yas, Palm Jumeirah, World Islands + 5 emirate cities).
- **Yango** — a *thinner* footprint (only `fujairah-uae` bound, though it scopes 5 cities).
- **Noon** — a "UAE waterfront geometry" activation (the superapp reference pack).
- **Careem** — **mirrors Noon** (`_regional_inheritance: uae_superapp`, 17 bound cards).

So all four are filtering the *same* messy 666-route pool through *four different masks* → four different-looking maps. Fixing the pool is necessary but not sufficient; we must also give all four **one identical UAE scope**.

## The fix (two layers)
**Layer 1 — clean the canonical pool (Grok geometry lane):**
1. Drop dirty BPs (centroids, activity operators, junk, duplicates) → ~60–80 real on-water piers.
2. Kill all-pairs meshing; keep only **significant corridors** (hub-and-spoke + marquee OD pairs).
3. Apply the existing 788 hand-waypoints (and add the missing ones) so **every** remaining corridor routes cleanly on water — target **0** `_qa_land_flag` rendered.
4. Purge the 23 over-range, the zero-distance, and the cross-border leaks (keep only 1–2 *deliberate* cross-border marquees).
5. Split east coast (Fujairah/Khor Fakkan/Dibba) into its own cluster — never mesh it to the Gulf side.
   **Target: ~666 → ~35–45 significant clean corridors.**

**Layer 2 — unify the partners (Tasklet scope lane):**
Define **one canonical UAE `_map_scope`** and apply it identically to `careem`, `bolt`, `yango`, `noon`. All four then render the same clean UAE network. (Partner *narrative/economics* stay partner-specific; only the geometry scope is unified.)

## Ownership & sequencing
- **Tasklet (this handoff):** the diagnosis above, the significant-corridor target list, the BP-cleanup signatures, and the unified `_map_scope` definition → `GROK-SPEC-uae-corridor-consolidation.md`.
- **Grok (deterministic seal):** BP drop + de-mesh + waypoint application + land QA to zero + re-seal `ROUTES.json`.
- Then apply the same policy to **Singapore** (tighten its outliers) as the second marquee.

No live partner decks are touched by this. This is a map/geometry cleanup.
