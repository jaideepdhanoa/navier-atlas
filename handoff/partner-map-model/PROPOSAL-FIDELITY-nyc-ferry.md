# Proposal fidelity — nyc-ferry

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:31Z

## Summary

- Items audited: 42
- KEEP: 38
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Wall St / Pier 11 → Brooklyn (DUMBO) / Long Island | `ics-db90a41958` | **KEEP** | — |
| journey | — | Wall St / Pier 11 → Rockaway | `ics-f993f1e653` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Wall St / Pier 11' → 'Rockaw |
| journey | — | Midtown (E 34th) → Yonkers / NJ Gold Coast | `ics-25a683a51c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Midtown (E 34th)' → 'Yonkers |
| journey | — | New York Harbor: Harbor Freight → Frank A. Vincent | `ics-23d2f2724f` | **KEEP** | — |
| journey | — | New York Harbor: Harbor Freight → Bay Ridge | `ics-2531d38456` | **KEEP** | — |
| journey | — | New York Harbor: Harbour View Senior Living → Half | `ics-3768445940` | **KEEP** | — |
| journey | — | New York Harbor: South Ferry/Terminal → New York H | `ics-4ffc6e9f72` | **KEEP** | — |
| journey | — | New York Harbor: Cape Liberty Cruise Port → Elco F | `ics-5a2b98675d` | **KEEP** | — |
| journey | — | New York Harbor: Cape Liberty Cruise Port → Bay Ri | `ics-5d44acda8c` | **KEEP** | — |
| journey | — | New York Harbor: Classic Harbor Line → Harbour Vie | `ics-6481653e97` | **KEEP** | — |
| journey | — | New York Harbor: Harbor Freight → Harbor Freight T | `ics-91236e9098` | **KEEP** | — |
| journey | — | New York Harbor: South Williamsburg → Harbor Freig | `ics-93302ccafd` | **KEEP** | — |
| journey | — | New York Harbor: St. George Ferry Terminal → Elco  | `ics-b2b4435ce6` | **KEEP** | — |
| journey | — | New York Harbor: Harbor Freight Transport Corporat | `ics-b52afea4dd` | **KEEP** | — |
| journey | — | New York Harbor: Half Moon Harbour → Grand Cove Ma | `ics-c239910b5b` | **KEEP** | — |
| journey | — | New York Harbor: South Ferry/Terminal → New York H | `ics-d14c2be8fb` | **KEEP** | — |
| journey | — | New York Harbor: South Ferry/Terminal → New York H | `ics-e79dc60dd1` | **KEEP** | — |
| journey | — | New York Harbor: Whitehall (Staten Island Ferry) → | `ics-a5f00760b1` | **KEEP** | — |
| journey | — | New York Harbor: Pier 11 / Wall Street → Paulus Ho | `ics-bdacfbafa1` | **KEEP** | — |
| journey | — | New York Harbor: Pier 11 / Wall Street → Hoboken T | `ics-d5de69a39d` | **KEEP** | — |
| journey | — | New York Harbor: Pier 11 / Wall Street → Long Isla | `ics-db90a41958` | **KEEP** | — |
| featured | 1 | Wall St / Pier 11 ↔ Brooklyn (DUMBO) / Long Island | `ics-db90a41958` | **KEEP** | — |
| featured | 1 | Wall St / Pier 11 ↔ Rockaway | `ics-f993f1e653` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Wall St / Pier 11' → 'Rockaw |
| featured | 1 | Midtown (E 34th) ↔ Yonkers / NJ Gold Coast | `ics-25a683a51c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Midtown (E 34th)' → 'Yonkers |
| featured | 1 | New York Harbor: Harbor Freight → Frank A. Vincent | `ics-23d2f2724f` | **KEEP** | — |
| featured | 1 | New York Harbor: Harbor Freight → Bay Ridge | `ics-2531d38456` | **KEEP** | — |
| featured | 1 | New York Harbor: Harbour View Senior Living → Half | `ics-3768445940` | **KEEP** | — |
| featured | 2 | New York Harbor: South Ferry/Terminal → New York H | `ics-4ffc6e9f72` | **KEEP** | — |
| featured | 2 | New York Harbor: Cape Liberty Cruise Port → Elco F | `ics-5a2b98675d` | **KEEP** | — |
| featured | 2 | New York Harbor: Cape Liberty Cruise Port → Bay Ri | `ics-5d44acda8c` | **KEEP** | — |
| featured | 2 | New York Harbor: Classic Harbor Line → Harbour Vie | `ics-6481653e97` | **KEEP** | — |
| featured | 2 | New York Harbor: Harbor Freight → Harbor Freight T | `ics-91236e9098` | **KEEP** | — |
| featured | 2 | New York Harbor: South Williamsburg → Harbor Freig | `ics-93302ccafd` | **KEEP** | — |
| featured | 3 | New York Harbor: St. George Ferry Terminal → Elco  | `ics-b2b4435ce6` | **KEEP** | — |
| featured | 3 | New York Harbor: Harbor Freight Transport Corporat | `ics-b52afea4dd` | **KEEP** | — |
| featured | 3 | New York Harbor: Half Moon Harbour → Grand Cove Ma | `ics-c239910b5b` | **KEEP** | — |
| featured | 3 | New York Harbor: South Ferry/Terminal → New York H | `ics-d14c2be8fb` | **KEEP** | — |
| featured | 3 | New York Harbor: South Ferry/Terminal → New York H | `ics-e79dc60dd1` | **KEEP** | — |
| featured | 3 | New York Harbor: Whitehall (Staten Island Ferry) → | `ics-a5f00760b1` | **KEEP** | — |
| featured | 4 | New York Harbor: Pier 11 / Wall Street → Paulus Ho | `ics-bdacfbafa1` | **KEEP** | — |
| featured | 4 | New York Harbor: Pier 11 / Wall Street → Hoboken T | `ics-d5de69a39d` | **KEEP** | — |
| featured | 4 | New York Harbor: Pier 11 / Wall Street → Long Isla | `ics-db90a41958` | **KEEP** | — |
