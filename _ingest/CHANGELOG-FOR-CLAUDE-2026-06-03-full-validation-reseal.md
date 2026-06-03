# Changelog for Claude — Full-Validation Atlas Reseal (2026-06-03)

**Export:** `exports/navier-export-20260603T180831Z.zip`
**Sealed:** 2026-06-03T18:05Z · SEAL schema `navier-atlas/seal/v1`

## What changed
- **Full-validation build** (in-build A* land repair ENABLED via self-healed `global_land_mask`).
  - **ROUTES = 5136** (post-scrub, full-validation) — up from the 700fix baseline; ≥5072 floor ✓, no regression.
  - FEATURES_BY_TYPE: 115 cities · 11,311 POIs · 37 priority cities.
  - STORIES 20 · VESSEL_SPECS 3.
- **Jakarta mesh fix shipped** (`_SPLIT_SLUGS`) — Jakarta intra-routes now form (0 → ~16–18).
- **Land QA:** 0/5136 land-crossers (scrub dropped 160 land-crossing routes).
- **Integrity gate:** PASS (1 known warning: `edge_endpoints_resolve_KNOWN_GAP` ×6 — pre-existing, non-blocking).
- **Brief conformance gate:** PASS — 134 briefs carry required + v2 analytical fields.

## CRITICAL content fix (spec violation caught at seal-time leak scan)
- **`2,000 nm` was incorrectly attributed to Quanta-LR** in the STORIES blob and (in stale data-clean copies) several city briefs.
- Canonical spec: **Quanta-LR commercial = 700 nm**; 2,000 nm is Quanta-D defense (**NEVER SHIP**, never blend).
- Corrected `2,000 nm → 700 nm` in: `output-external/STORIES.json`, `output-external/stories.json`, and 2 city-brief sources (sabah-kota-kinabalu, tokyo-bay). STORIES sha256 changed (356237cd → 28087c09).
- Frozen partition source (`partition/stories-partner-view.json`) was already clean — the 2,000 nm was a legacy build artifact.
- **FOLLOW-UP for next build:** build.py still has stale `2,000 nm` in comments (L9, L1163) and the index.html legend (L1706, "Quanta-LR ≤2,000 nm hybrid"). index.html is not shipped, but these should be corrected for hygiene.
- **Final public-surface leak scan: CLEAN — 0 banned-token hits across all 183 data-clean files.**

## Pipeline hardening shipped this pass (so we stop rediscovering these)
1. **`build.py` `_bp_file()` hardened** — tolerates FUSE `EIO`/`ENOENT` on the boarding-points first-probe (was crashing the build mid-parse with `Errno 5`).
2. **`build.py` self-heal** — auto-installs `global_land_mask` at startup if a sandbox reset wiped it, so the build can never silently degrade to fast-mode (which produced regressed ~4943 route counts).
3. **`seal_bundle.py` FUSE write-back drain** — added `os.sync()` drain between the blob-seal loop (~20MB) and `_externalize_pitch` (178 small writes). Root cause of the long-standing "seal hangs after `sealed VESSEL_SPECS`" stall: FUSE write-back buffer saturation. Now deterministically completes.

## Deploy notes (unchanged)
- Bake website from `data-clean/{city_briefs,partners}/` — NOT `partner-pitch/` source.
- Verify blob sha256 against SEAL.json before deploy; mismatch = abort.
- Dossiers are internal-only and NOT in this export.
