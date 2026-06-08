# Gold #19 — Catalina Island & the L.A. Channel (autonomous lane, market #1)

**Date:** 2026-06-08
**Base:** Gold #18 (Maldives expansion)
**Method:** `add_market.py` delta (NEW-MARKET-RECIPE / LB-25) — no full build.

## What changed
- **New city node:** `catalina-channel-islands-usa` ("Catalina Island & the L.A. Channel"), anchor Avalon/Cabrillo Mole `[-118.32164, 33.34447]`, dual-platform, North America. First-class atlas PIN.
- **+16 boarding-point POIs** (web-verified anchors + free-OSM densify; 1 duplicate id removed pre-build).
- **+7 routes** (5206 → 5213). All Pioneer-class (≤70 nm). Generator produced 8 spokes; scrub dropped 1 land-crosser; gen-phase dropped 4 land + 1 range.

## Hero corridors (real channel crossings)
- **Cabrillo Mole (Avalon) ↔ Shoreline Village (Long Beach)** — 26.0 nm
- **Cabrillo Mole (Avalon) ↔ Balboa Island (Newport Beach)** — 26.3 nm
- Plus mainland L.A. coastal hops (Long Beach / Alamitos Bay / Newport).

## Economics
- Sidecar unchanged at **69 records**. Catalina is a geometry-only autonomous-lane hero (no partner finance corridor in corridors.json), so no economics records — correct by design.

## Seal
- Changed blobs resealed (raw-bytes sha256): `ROUTES` (5213), `FEATURES_BY_TYPE` (city 162 / poi 11353), sidecar re-hashed.
- Provenance under `_gold19_catalina`.

## Front-end note (for Claude's build.mjs)
- `FEATURES_BY_TYPE.city` ∋ `catalina-channel-islands-usa` (PIN). `.poi` includes its 16 BPs.
- Inter-city/channel routes render bidirectional `↔` on the front end (Tasklet authoring stays directional).
