# Proposal fidelity — nyc-ferry

**Verdict:** TRIM
**Checked:** 2026-06-29T17:05:23Z

## Summary

- Items audited: 16
- KEEP: 15
- DROP: 1
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 1

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Wall St / Pier 11 → Brooklyn (DUMBO) / Long Island | `ics-38e18c9220` | **KEEP** | — |
| journey | — | Pier 11 / Wall Street → South Williamsburg | `ics-f993f1e653` | **KEEP** | — |
| journey | — | Midtown / Pier 79 (W 39th St) → Hoboken Terminal | `ics-25a683a51c` | **KEEP** | — |
| journey | — | New York Harbor: Harbor Freight → Frank A. Vincent | `ics-23d2f2724f` | **KEEP** | — |
| featured | 1 | Pier 11 / Wall Street → Brooklyn / DUMBO Pier 1 | `ics-38e18c9220` | **KEEP** | — |
| featured | 1 | Pier 11 / Wall Street → South Williamsburg | `ics-f993f1e653` | **KEEP** | — |
| featured | 1 | Midtown / Pier 79 (W 39th St) → Hoboken Terminal | `ics-25a683a51c` | **KEEP** | — |
| featured | 2 | New York Harbor → New York Harbor | `ics-4ffc6e9f72` | **DROP** | bp_binding: labels ≠ route endpoints: card 'New York Harbor' → 'New York |
| featured | 2 | Cape Liberty Cruise Port → Elco Fisherman's Marina | `ics-5a2b98675d` | **KEEP** | — |
| featured | 2 | Cape Liberty Cruise Port → Bay Ridge | `ics-5d44acda8c` | **KEEP** | — |
| featured | 3 | St. George Ferry Terminal → Elco Fisherman's Marin | `ics-b2b4435ce6` | **KEEP** | — |
| featured | 3 | Harbor Freight Transport Corporation → Elco Fisher | `ics-b52afea4dd` | **KEEP** | — |
| featured | 3 | Half Moon Harbour → Grand Cove Marina | `ics-c239910b5b` | **KEEP** | — |
| featured | 4 | Pier 11 / Wall Street → Paulus Hook (Jersey City) | `ics-bdacfbafa1` | **KEEP** | — |
| featured | 4 | Pier 11 / Wall Street → Hoboken Terminal | `ics-d5de69a39d` | **KEEP** | — |
| featured | 4 | Pier 11 / Wall Street → Long Island City | `ics-db90a41958` | **KEEP** | — |
