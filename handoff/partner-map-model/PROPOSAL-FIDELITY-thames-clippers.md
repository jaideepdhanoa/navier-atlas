# Proposal fidelity — thames-clippers

**Verdict:** TRIM
**Checked:** 2026-06-29T15:10:47Z

## Summary

- Items audited: 16
- KEEP: 14
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | London (Embankment / Tower) → Canary Wharf | `—` | **KEEP** | — |
| journey | — | Central London → Thamesmead / Royal Docks (new dev | `—` | **KEEP** | — |
| journey | — | Putney (west) → Barking Riverside / Woolwich (east | `—` | **KEEP** | — |
| journey | — | London: Hermitage Community Moorings → Poplar Wate | `—` | **KEEP** | — |
| featured | 1 | London (Embankment / Tower) ↔ Canary Wharf | `ics-5e35d5734e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'London (Embankment / Tower)' |
| featured | 1 | Central London ↔ Thamesmead / Royal Docks (new dev | `ics-a7b6b93c46` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central London' → 'Thamesmea |
| featured | 1 | Putney (west) ↔ Barking Riverside / Woolwich (east | `—` | **KEEP** | — |
| featured | 2 | London: Hermitage Community Moorings → Harbour Cyc | `—` | **KEEP** | — |
| featured | 2 | London: Islington Boat Club → Lee Valley Marina Sp | `—` | **KEEP** | — |
| featured | 2 | London: Little Venice → Fulham Reach Boat Club | `—` | **KEEP** | — |
| featured | 3 | London: Westminster Pier → London | `—` | **KEEP** | — |
| featured | 3 | London: Westminster Pier → London | `—` | **KEEP** | — |
| featured | 3 | London: Laburnum Boat Club → Poplar Waterside & Ma | `—` | **KEEP** | — |
| featured | 4 | London: Harbour Cycles → Imperial Wharf Marina | `—` | **KEEP** | — |
| featured | 4 | London: Laburnum Boat Club → Limehouse Waterside & | `—` | **KEEP** | — |
| featured | 4 | London: Little Venice → London Corinthian Sailing  | `—` | **KEEP** | — |
