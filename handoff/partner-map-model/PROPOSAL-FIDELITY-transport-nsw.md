# Proposal fidelity — transport-nsw

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:47Z

## Summary

- Items audited: 15
- KEEP: 12
- DROP: 3
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 3

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Circular Quay → Manly | `—` | **KEEP** | — |
| journey | — | Circular Quay → Watsons Bay / Rose Bay | `—` | **KEEP** | — |
| journey | — | Circular Quay → Parramatta | `—` | **KEEP** | — |
| journey | — | Sydney CBD → Sydney Olympic Park | `—` | **KEEP** | — |
| featured | 1 | Circular Quay ↔ Manly | `ics-bb25fb0b69` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Manly' vs  |
| featured | 1 | Circular Quay ↔ Watsons Bay / Rose Bay | `ics-26759e3e76` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Watsons Ba |
| featured | 1 | Circular Quay ↔ Parramatta | `ics-0bc6865ade` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Parramatta |
| featured | 2 | Watsons Bay → Manly Wharf | `—` | **KEEP** | — |
| featured | 2 | Sydney Harbour: Woolwich Marina → FFB Dragon Boat  | `—` | **KEEP** | — |
| featured | 2 | Sydney Harbour: Clifton Gardens Wharf → Freedom Bo | `—` | **KEEP** | — |
| featured | 3 | Sydney Harbour → Watsons Bay | `—` | **KEEP** | — |
| featured | 3 | Sydney Harbour: Circular Quay, Sydney → Sydney Har | `—` | **KEEP** | — |
| featured | 3 | Sydney Harbour: Rose Bay Marina → Yarra Bay Sailin | `—` | **KEEP** | — |
| featured | 4 | Sydney Harbour: Yarra Bay Sailing Club → Georges R | `—` | **KEEP** | — |
| featured | 4 | Sydney Harbour: Clifton Gardens Wharf → Tunks Park | `—` | **KEEP** | — |
