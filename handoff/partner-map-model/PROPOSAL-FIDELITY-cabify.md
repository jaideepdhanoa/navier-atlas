# Proposal fidelity — cabify

**Verdict:** TRIM
**Checked:** 2026-06-29T13:00:21Z

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
| journey | — | Rio de Janeiro (Marina da Glória) → Angra dos Reis | `—` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/didi |
| journey | — | Cancún → Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| journey | — | Puerto Vallarta → Marietas Islands | `—` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/didi |
| journey | — | Cartagena (Marina) → Rosario Islands | `ics-e10b53b415` | **KEEP** | — |
| journey | — | Cabo San Lucas Marina → La Paz / Sea of Cortez | `—` | **KEEP** | — |
| journey | — | Samaná (Santa Bárbara) → Cayo Levantado | `rn-b7b7d78c475e` | **KEEP** | — |
| featured | 1 | Cartí ↔ Guna Yala overnight-island resorts | `rn-a1eae9288e3a` | **KEEP** | — |
| featured | 2 | Cancún ↔ Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| featured | 2 | Samaná town (Santa Bárbara) ↔ Cayo Levantado | `rn-b7b7d78c475e` | **KEEP** | — |
| featured | 3 | Cartagena ↔ Rosario Islands | `ics-90842b3637` | **KEEP** | — |
| featured | 3 | Cancún ↔ Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| featured | 4 | Cartí ↔ San Blas cays | `—` | **KEEP** | — |
| featured | 4 | Samaná ↔ Cayo Levantado | `rn-b7b7d78c475e` | **KEEP** | — |
| featured | 4 | Playa del Carmen ↔ Cozumel | `ics-dd1d814699` | **KEEP** | — |
| featured | spain/p1 | Barcelona & the Costa Brava coastal mesh | `ics-81984b66e9` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Barcelona & |
| featured | colombia/p1 | Cartagena & the Rosario Islands coastal mesh | `ics-2c66505042` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Club de pes |
