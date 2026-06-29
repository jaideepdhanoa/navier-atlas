# Proposal fidelity — nyc-ferry

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:46Z

## Summary

- Items audited: 16
- KEEP: 12
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Wall St / Pier 11 → Brooklyn (DUMBO) / Long Island | `—` | **KEEP** | — |
| journey | — | Wall St / Pier 11 → Rockaway | `ics-f993f1e653` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Wall St / Pier 11' → 'Rockaw |
| journey | — | Midtown (E 34th) → Yonkers / NJ Gold Coast | `ics-25a683a51c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Midtown (E 34th)' → 'Yonkers |
| journey | — | New York Harbor: Harbor Freight → Frank A. Vincent | `—` | **KEEP** | — |
| featured | 1 | Wall St / Pier 11 ↔ Brooklyn (DUMBO) / Long Island | `—` | **KEEP** | — |
| featured | 1 | Wall St / Pier 11 ↔ Rockaway | `ics-f993f1e653` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Wall St / Pier 11' → 'Rockaw |
| featured | 1 | Midtown (E 34th) ↔ Yonkers / NJ Gold Coast | `ics-25a683a51c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Midtown (E 34th)' → 'Yonkers |
| featured | 2 | New York Harbor: South Ferry/Terminal → New York H | `—` | **KEEP** | — |
| featured | 2 | New York Harbor: Cape Liberty Cruise Port → Elco F | `—` | **KEEP** | — |
| featured | 2 | New York Harbor: Cape Liberty Cruise Port → Bay Ri | `—` | **KEEP** | — |
| featured | 3 | New York Harbor: St. George Ferry Terminal → Elco  | `—` | **KEEP** | — |
| featured | 3 | New York Harbor: Harbor Freight Transport Corporat | `—` | **KEEP** | — |
| featured | 3 | New York Harbor: Half Moon Harbour → Grand Cove Ma | `—` | **KEEP** | — |
| featured | 4 | New York Harbor: Pier 11 / Wall Street → Paulus Ho | `—` | **KEEP** | — |
| featured | 4 | New York Harbor: Pier 11 / Wall Street → Hoboken T | `—` | **KEEP** | — |
| featured | 4 | New York Harbor: Pier 11 / Wall Street → Long Isla | `—` | **KEEP** | — |
