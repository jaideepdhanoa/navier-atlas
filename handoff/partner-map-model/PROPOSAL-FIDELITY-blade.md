# Proposal fidelity — blade

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-28T21:13:23Z

## Summary

- Items audited: 12
- KEEP: 4
- DROP: 0
- DEFER: 2
- TRIM/REWRITE: 6
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | East 34th Street (Manhattan) → LGA Marine Air Term | `rn-0e2b916d3b8d` | **KEEP** | — |
| journey | — | Wall Street / Pier 11 (Manhattan) → Paulus Hook (J | `ics-bdacfbafa1` | **TRIM** | distance_honesty: card 2.0nm vs route 1.41nm (42% delta) |
| journey | — | Wall Street / Pier 11 (Manhattan) → Long Wharf (Sa | `rn-e2c8f0d3fe0d` | **TRIM** | geometry_preview: interior_land_km=3.42 (threshold 0.4) |
| journey | — | Wall Street / Pier 11 (Manhattan) → Viking Fleet D | `rn-1119113a9806` | **TRIM** | geometry_preview: interior_land_km=2.88 (threshold 0.4) |
| journey | market:usa-ny-harbor | East 34th Street (Manhattan) → LGA Marine Air Term | `rn-0e2b916d3b8d` | **KEEP** | — |
| journey | market:usa-ny-harbor | Wall Street / Pier 11 (Manhattan) → Paulus Hook (J | `ics-bdacfbafa1` | **TRIM** | distance_honesty: card 2.0nm vs route 1.41nm (42% delta) |
| journey | market:usa-ny-harbor | Wall Street / Pier 11 (Manhattan) → Long Wharf (Sa | `rn-e2c8f0d3fe0d` | **TRIM** | geometry_preview: interior_land_km=3.42 (threshold 0.4) |
| journey | market:usa-ny-harbor | Wall Street / Pier 11 (Manhattan) → Viking Fleet D | `rn-1119113a9806` | **TRIM** | geometry_preview: interior_land_km=2.88 (threshold 0.4) |
| featured | usa-ny-harbor/p1 | East 34th Street → LGA Marine Air Terminal | `rn-0e2b916d3b8d` | **KEEP** | — |
| featured | usa-ny-harbor/p1 | Pier 11 → Paulus Hook | `ics-bdacfbafa1` | **KEEP** | — |
| featured | usa-ny-harbor/p2 | Pier 11 → Sag Harbor | `rn-e2c8f0d3fe0d` | **DEFER** | geometry_preview: interior_land_km=3.42 (threshold 0.4) |
| featured | usa-ny-harbor/p2 | Pier 11 → Montauk | `rn-1119113a9806` | **DEFER** | geometry_preview: interior_land_km=2.88 (threshold 0.4) |
