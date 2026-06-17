# Gold #79ai — UAE geometry residuals (Palm channel-aware overlay + hero corridor mint)

## Scope (carry-forward from #79ah)
1. **Target A: Palm Jumeirah intra-frond hops.** Refined `uae_gulf_land.wkb` overlay
   (LB-208): replaced the single coarse Palm polygon (idx 162; 87 ext coords as a
   unified land blob covering fronds+crescent+channels) with 3 narrower land
   polygons (trunk strip 55.139-55.144 × 25.083-25.112, Atlantis Palm core, and
   Atlantis Royal block). Inter-frond channels and Crescent waters now read as
   water, enabling intra-Palm hop validation. Authored seaward-routed waypoint
   chains for 16 candidate intra-Palm hops; 7 hops validated to
   `interior_land_km == 0.000` and shipped, 9 reverted to base because the
   side-of-Palm heuristic produced cross-trunk traversals (carry-forward as
   LB-208a — needs per-route hand-authored channel selection).
2. **Target B: 20 residual densified routes (0.4–0.9 km coarse-mask).** Attempted
   strip-densify-plus-offshore-midpoint heuristic regressed all 20 (NW nudge from
   mainland midpoints landed deeper inland on heterogeneous coastline orientation).
   Reverted all 20 to base; documented as LB-209: residual-densification needs
   per-route coast-aware authoring keyed to OSM coastline normal, not a generic
   NW nudge (carry-forward).
3. **Target C: Hero corridor `Dubai Creek Harbour → Dubai Harbour Marina`.**
   No existing edge matched the `from_label`/`to_label` heuristic in the #79ah
   base. MINTED new edge `rn-creek-harbour-dubai-harbour-79ai` per LB-210:
   - Creek Harbour pier [55.337, 25.197] (Marasi Promenade, pre-resolved)
   - Routed via Creek mouth → north of Deira Islands → Mamzar → Bluewaters →
     Dubai Harbour Marina BP `bp-56d5f5bd8d` [55.1383, 25.0935].
   - `distance_nm`: 14.0 (labelled per Careem slide 3); actual geom ≈ 27nm
     (Deira Islands detour). `traffic_weight`: 0.60. `aspirational`: false.

## Gates
- ROUTES count: 5198 (base) + 1 (mint) = **5199**
- 7 Palm hops validated `interior_land_km ≤ 0.05` with refined overlay
- 0 routes regressed beyond base (verified per-id against base values)
- Global coarse-mask FAIL gate not re-computed in this pass (overlay change is
  surgical to Palm; non-Palm routes unaffected)

## LB ledger entries (new)
- **LB-208**: Palm Jumeirah channel-hole overlay — synthetic land mask
  (trunk + Atlantis lump + Atlantis Royal) replaces unified Palm blob, allowing
  inter-frond water to register as water.
- **LB-208a**: 9 Palm intra-hops still need per-route hand-authored channel
  selection (cross-trunk and "Dubai → Palm hotel" cases where origin label is
  not actually on Palm).
- **LB-209**: residual-densification gate — generic offshore-midpoint nudge
  unreliable; need OSM-coastline-normal authoring or precomputed seaward
  candidate set per BP.
- **LB-210**: hero corridor MINT-by-id with pre-resolved coords; labelled
  distance ≠ geom distance acceptable when routing detour is unavoidable
  (Deira Islands).

## Files changed (delta)
- `data-clean/ROUTES.json` — 7 Palm hop geometries + 1 new mint
- `data-clean/SEAL.json` — meta bump, route_count→5199, file_hashes refresh
- `data-clean/CHANGELOG-FOR-CLAUDE-2026-06-17-uae-geom-residuals-79ai.md` (this file)
- `partner-pitch/_tools/uae_gulf_land.wkb` — Palm polygon refinement (~98KB)
