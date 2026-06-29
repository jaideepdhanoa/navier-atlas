# Proposal fidelity — transport-nsw

**Verdict:** REWRITE
**Checked:** 2026-06-29T12:19:22Z

## Summary

- Items audited: 28
- KEEP: 20
- DROP: 8
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 8

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Circular Quay → Manly | `ics-bb25fb0b69` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Manly' vs  |
| journey | — | Circular Quay → Watsons Bay / Rose Bay | `ics-26759e3e76` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Watsons Ba |
| journey | — | Circular Quay → Parramatta | `ics-0bc6865ade` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Parramatta |
| journey | — | Sydney CBD → Sydney Olympic Park | `ics-4bfda3ec3e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Sydney CBD' → 'Sydney Olympi |
| journey | — | Watsons Bay → Manly Wharf | `ics-1961e2b06c` | **KEEP** | — |
| journey | — | Sydney Harbour: Woolwich Marina → FFB Dragon Boat  | `ics-1c999c04a0` | **KEEP** | — |
| journey | — | Sydney Harbour: Clifton Gardens Wharf → Freedom Bo | `ics-21d9d71119` | **KEEP** | — |
| journey | — | Sydney Harbour: Woolwich Wharf → Tunks Park Boat R | `ics-3355aded27` | **KEEP** | — |
| journey | — | Sydney Harbour → Watsons Bay | `ics-3c91a5bf67` | **KEEP** | — |
| journey | — | Sydney Harbour: Circular Quay, Sydney → Sydney Har | `ics-4e0a23c993` | **KEEP** | — |
| journey | — | Sydney Harbour: Rose Bay Marina → Yarra Bay Sailin | `ics-ae99b21b5d` | **KEEP** | — |
| journey | — | Sydney Harbour: Circular Quay, Sydney → Sydney Har | `ics-db6c3f2166` | **KEEP** | — |
| journey | — | Sydney Harbour: Yarra Bay Sailing Club → Georges R | `ics-df63d39ebe` | **KEEP** | — |
| journey | — | Sydney Harbour: Clifton Gardens Wharf → Tunks Park | `ics-fbd797389c` | **KEEP** | — |
| featured | 1 | Circular Quay ↔ Manly | `ics-bb25fb0b69` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Manly' vs  |
| featured | 1 | Circular Quay ↔ Watsons Bay / Rose Bay | `ics-26759e3e76` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Watsons Ba |
| featured | 1 | Circular Quay ↔ Parramatta | `ics-0bc6865ade` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Circular Quay' → 'Parramatta |
| featured | 1 | Sydney CBD ↔ Sydney Olympic Park | `ics-4bfda3ec3e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Sydney CBD' → 'Sydney Olympi |
| featured | 2 | Watsons Bay → Manly Wharf | `ics-1961e2b06c` | **KEEP** | — |
| featured | 2 | Sydney Harbour: Woolwich Marina → FFB Dragon Boat  | `ics-1c999c04a0` | **KEEP** | — |
| featured | 2 | Sydney Harbour: Clifton Gardens Wharf → Freedom Bo | `ics-21d9d71119` | **KEEP** | — |
| featured | 2 | Sydney Harbour: Woolwich Wharf → Tunks Park Boat R | `ics-3355aded27` | **KEEP** | — |
| featured | 3 | Sydney Harbour → Watsons Bay | `ics-3c91a5bf67` | **KEEP** | — |
| featured | 3 | Sydney Harbour: Circular Quay, Sydney → Sydney Har | `ics-4e0a23c993` | **KEEP** | — |
| featured | 3 | Sydney Harbour: Rose Bay Marina → Yarra Bay Sailin | `ics-ae99b21b5d` | **KEEP** | — |
| featured | 3 | Sydney Harbour: Circular Quay, Sydney → Sydney Har | `ics-db6c3f2166` | **KEEP** | — |
| featured | 4 | Sydney Harbour: Yarra Bay Sailing Club → Georges R | `ics-df63d39ebe` | **KEEP** | — |
| featured | 4 | Sydney Harbour: Clifton Gardens Wharf → Tunks Park | `ics-fbd797389c` | **KEEP** | — |
