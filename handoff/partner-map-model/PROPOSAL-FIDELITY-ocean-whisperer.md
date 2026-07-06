# Proposal fidelity — ocean-whisperer

**Verdict:** REWRITE
**Checked:** 2026-07-06T03:21:43Z

## Summary

- Items audited: 8
- KEEP: 3
- DROP: 5
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 5

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Hato air arrival → leeward embarkation (Piscadera) | `rn-8ae6f0293d75` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Hato air arrival → leeward e |
| journey | — | Willemstad / Sint Anna Bay (cruise mega-pier) → Pi | `rn-29425ce31839` | **KEEP** | — |
| journey | — | Spanish Water / Jan Thiel → Klein Curaçao day-trip | `rn-09a43a616a1a` | **KEEP** | — |
| journey | — | Curaçao (Spanish Water) → Bonaire (Kralendijk) | `rn-0f8e77cfef46` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Curaçao (Spanish Water)' → ' |
| featured | 1 | Willemstad / Sint Anna Bay (cruise mega-pier) ↔ Pi | `rn-29425ce31839` | **KEEP** | — |
| featured | 2 | Piscadera leeward embark ↔ Sandals Royal Curaçao ( | `rn-8ae6f0293d75` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Piscadera leeward embark' →  |
| featured | 3 | Curaçao (Spanish Water) ↔ Bonaire (Kralendijk) | `rn-0f8e77cfef46` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Curaçao (Spanish Water)' → ' |
| featured | 3 | Curaçao (Spanish Water) ↔ Aruba (Oranjestad / Rena | `rn-e96930f83c0f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Curaçao (Spanish Water)' → ' |
