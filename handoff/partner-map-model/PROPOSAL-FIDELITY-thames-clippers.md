# Proposal fidelity — thames-clippers

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:53Z

## Summary

- Items audited: 32
- KEEP: 26
- DROP: 6
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 6

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | London (Embankment / Tower) → Canary Wharf | `ics-5e35d5734e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'London (Embankment / Tower)' |
| journey | — | Central London → Thamesmead / Royal Docks (new dev | `ics-a7b6b93c46` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central London' → 'Thamesmea |
| journey | — | Putney (west) → Barking Riverside / Woolwich (east | `ics-b2fd5c9640` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Putney (west)' → 'Barking Ri |
| journey | — | London: Hermitage Community Moorings → Poplar Wate | `ics-1e317781e7` | **KEEP** | — |
| journey | — | London: Hermitage Community Moorings → Harbour Cyc | `ics-309bcd96f0` | **KEEP** | — |
| journey | — | London: Islington Boat Club → Lee Valley Marina Sp | `ics-48307916e1` | **KEEP** | — |
| journey | — | London: Little Venice → Fulham Reach Boat Club | `ics-53908d580e` | **KEEP** | — |
| journey | — | London: Islington Boat Club → Hermitage Community  | `ics-6f0676dff8` | **KEEP** | — |
| journey | — | London: Westminster Pier → London | `ics-924f0cf540` | **KEEP** | — |
| journey | — | London: Westminster Pier → London | `ics-a4867a38c1` | **KEEP** | — |
| journey | — | London: Laburnum Boat Club → Poplar Waterside & Ma | `ics-c23410d715` | **KEEP** | — |
| journey | — | London: Laburnum Boat Club → Lee Valley Marina Spr | `ics-c65d1cd81a` | **KEEP** | — |
| journey | — | London: Harbour Cycles → Imperial Wharf Marina | `ics-d0be19c708` | **KEEP** | — |
| journey | — | London: Laburnum Boat Club → Limehouse Waterside & | `ics-d82a8016ac` | **KEEP** | — |
| journey | — | London: Little Venice → London Corinthian Sailing  | `ics-dff94c35eb` | **KEEP** | — |
| journey | — | London: Hurlingham Harbour → London Corinthian Sai | `ics-f65c175ffe` | **KEEP** | — |
| featured | 1 | London (Embankment / Tower) ↔ Canary Wharf | `ics-5e35d5734e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'London (Embankment / Tower)' |
| featured | 1 | Central London ↔ Thamesmead / Royal Docks (new dev | `ics-a7b6b93c46` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central London' → 'Thamesmea |
| featured | 1 | Putney (west) ↔ Barking Riverside / Woolwich (east | `ics-b2fd5c9640` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Putney (west)' → 'Barking Ri |
| featured | 1 | London: Hermitage Community Moorings → Poplar Wate | `ics-1e317781e7` | **KEEP** | — |
| featured | 2 | London: Hermitage Community Moorings → Harbour Cyc | `ics-309bcd96f0` | **KEEP** | — |
| featured | 2 | London: Islington Boat Club → Lee Valley Marina Sp | `ics-48307916e1` | **KEEP** | — |
| featured | 2 | London: Little Venice → Fulham Reach Boat Club | `ics-53908d580e` | **KEEP** | — |
| featured | 2 | London: Islington Boat Club → Hermitage Community  | `ics-6f0676dff8` | **KEEP** | — |
| featured | 3 | London: Westminster Pier → London | `ics-924f0cf540` | **KEEP** | — |
| featured | 3 | London: Westminster Pier → London | `ics-a4867a38c1` | **KEEP** | — |
| featured | 3 | London: Laburnum Boat Club → Poplar Waterside & Ma | `ics-c23410d715` | **KEEP** | — |
| featured | 3 | London: Laburnum Boat Club → Lee Valley Marina Spr | `ics-c65d1cd81a` | **KEEP** | — |
| featured | 4 | London: Harbour Cycles → Imperial Wharf Marina | `ics-d0be19c708` | **KEEP** | — |
| featured | 4 | London: Laburnum Boat Club → Limehouse Waterside & | `ics-d82a8016ac` | **KEEP** | — |
| featured | 4 | London: Little Venice → London Corinthian Sailing  | `ics-dff94c35eb` | **KEEP** | — |
| featured | 4 | London: Hurlingham Harbour → London Corinthian Sai | `ics-f65c175ffe` | **KEEP** | — |
