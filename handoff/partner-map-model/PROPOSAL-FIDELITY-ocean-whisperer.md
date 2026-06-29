# Proposal fidelity — ocean-whisperer

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:31Z

## Summary

- Items audited: 12
- KEEP: 5
- DROP: 7
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 7

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Hato air arrival → leeward embarkation (Piscadera) | `rn-8ae6f0293d75` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Hato air arrival → leeward e |
| journey | — | Willemstad / Sint Anna Bay (cruise mega-pier) → Pi | `rn-29425ce31839` | **KEEP** | — |
| journey | — | Spanish Water / Jan Thiel → Klein Curaçao day-trip | `rn-09a43a616a1a` | **KEEP** | — |
| journey | — | Curaçao (Spanish Water) → Bonaire (Kralendijk) | `rn-0f8e77cfef46` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Curaçao (Spanish Water)' → ' |
| journey | — | Hato air arrival → leeward embarkation (Piscadera) | `rn-aefa1c104456` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Hato air arrival → leeward e |
| journey | — | Willemstad / Sint Anna Bay (cruise mega-pier) → Sa | `rn-d1eb05689785` | **KEEP** | — |
| journey | — | Spanish Water / Jan Thiel → Baoase Luxury Resort | `rn-43c96cef749c` | **KEEP** | — |
| journey | — | Curaçao (Spanish Water) → Aruba (Oranjestad / Rena | `rn-e96930f83c0f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Curaçao (Spanish Water)' → ' |
| featured | 1 | Willemstad / Sint Anna Bay (cruise mega-pier) ↔ Pi | `rn-29425ce31839` | **KEEP** | — |
| featured | 2 | Piscadera leeward embark ↔ Sandals Royal Curaçao ( | `rn-8ae6f0293d75` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Piscadera leeward embark' →  |
| featured | 3 | Curaçao (Spanish Water) ↔ Bonaire (Kralendijk) | `rn-0f8e77cfef46` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Curaçao (Spanish Water)' → ' |
| featured | 3 | Curaçao (Spanish Water) ↔ Aruba (Oranjestad / Rena | `rn-e96930f83c0f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Curaçao (Spanish Water)' → ' |
