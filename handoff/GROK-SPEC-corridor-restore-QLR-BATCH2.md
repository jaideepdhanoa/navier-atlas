# GROK SPEC — Corridor Restore BATCH 2 (Q-LR 180–700 nm)

**Date:** 2026-07-06 · **Follows:** deploy `a9b5d47e` (Batch 1: 51 restored + 3 mints)
**Trigger:** Jaideep corrected Q-LR range ceiling — **~700 nm, not 180 nm.**

## What this changes for you
Your Batch-1 execution used the old 180 nm ceiling, so **22 corridors landed in your "18 longhaul C-bucket / stay-dropped" pile that should actually be RESTORED.** They are all ≤401 nm — squarely inside the Q-LR envelope. Only **one** corridor truly stays dropped: **Jakarta↔Penghu (Taiwan), 1,936 nm.**

## Good news — no minting risk
I checked all 22 against the July-3 geometry: **every one has a proven water-following route** (301–1,286 vertices; not straight lines). So apply the **exact same copy-proven-features strategy** you used for the 51 — no re-minting, no land-crossing failures.

**Executable register:** `handoff/CORRIDOR-RESTORE-QLR-BATCH2-700nm.json` — each entry carries `pair`, `label`, `nm`, `jul3_source_route_id` (the feature to copy), `jul3_vertices`, `cross_border`, and `assign_tier: quanta_lr`.

## Two execution notes
1. **Assign `quanta_lr` tier on restore.** All 22 were untiered (`tier=None`) at July-3. 14 of 22 are **cross-border** (the whole Gulf trunk: Abu Dhabi/Dubai/RAK ↔ Manama/Doha/Muscat). They must carry the Q-LR tier so the **cross-border one-endpoint render policy** lights them up on scoped market pages (Careem outbound overlay, /uae, /qatar, /bahrain, /oman, etc.).
2. **`edge-XXXX` sources → re-seal to `rn-` format.** Some `jul3_source_route_id`s are old featured-edge ids (`edge-0705`, `edge-0834`…) rather than sealed `rn-` routes. Copy the geometry but **mint a fresh `rn-` id** and run it through the seal (don't keep the `edge-` id).

## Resolves your 3 "Jaideep judgment" flags
- **Goa↔Mumbai (206 nm, 847 vtx)** → restore (Q-LR, water-clean).
- **Split↔Venice (218 nm, 836 vtx)** → restore (Q-LR, water-clean across Adriatic).
- **Bangkok↔Koh Samui (212 nm, 478 vtx)** → restore, BUT **label/pair QA first:** my register pair reads `koh-chang-thailand ↔ koh-phangan-thailand` while the label says "Bangkok↔Koh Samui." Reconcile the label to the actual endpoints before it goes live.

## Stays dropped (correct)
- **Jakarta↔Penghu — 1,936 nm.** Beyond Q-LR range. Leave dropped.

## Unchanged / your other deferred items are fine as-is
- 7 truly-empty markets + 38 isolated cities + 66 registry-gap routes = honest-null, need Tasklet BP wishlists. That's my lane; no action for you until I ship pier lists.
