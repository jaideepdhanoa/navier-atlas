# Proposal fidelity — saudi-pif

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 13
- KEEP: 4
- DROP: 9
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 9

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | The Red Sea — Shura Island → Outer-island resorts  | `rn-1a140dacd3e6` | **DROP** | bp_binding: labels ≠ route endpoints: card 'The Red Sea — Shura Island'  |
| journey | — | The Red Sea destination → AMAALA (Triple Bay) | `ics-748e4ff724` | **DROP** | bp_binding: labels ≠ route endpoints: card 'The Red Sea destination' → ' |
| journey | — | Jeddah Corniche → Jeddah Central (PIF waterfront)  | `rn-05bf6ff26cb5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Jeddah Corniche' → 'Jeddah C |
| journey | — | NEOM — Sindalah → Magna / Oxagon coast | `—` | **KEEP** | — |
| featured | 1 | Shura ↔ outer-island resorts — The Red Sea lagoon | `rn-1a140dacd3e6` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Shura' → 'outer-island resor |
| featured | 1 | The Red Sea ↔ AMAALA — flagship corridor (Quanta-L | `ics-748e4ff724` | **DROP** | bp_binding: labels ≠ route endpoints: card 'The Red Sea' → 'AMAALA — fla |
| featured | 1 | NEOM — Sindalah ↔ Magna ↔ Oxagon coast | `—` | **KEEP** | — |
| featured | 2 | Jeddah Corniche ↔ Jeddah Central (PIF waterfront) | `rn-05bf6ff26cb5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Jeddah Corniche' → 'Jeddah C |
| featured | 2 | Jeddah ↔ KAEC ↔ Thuwal (KAUST) | `rn-05bf6ff26cb5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Jeddah' → 'KAEC ↔ Thuwal (KA |
| featured | 2 | Obhur Creek ↔ Jeddah Yacht Club | `rn-05bf6ff26cb5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Obhur Creek' → 'Jeddah Yacht |
| featured | 3 | Khobar / Dammam ↔ Manama (Bahrain) — cross-Gulf, s | `—` | **KEEP** | — |
| featured | 3 | Red Sea ↔ AMAALA ↔ NEOM — full Quanta-LR through-r | `—` | **KEEP** | — |
| featured | 3 | One foiling standard, coast to coast | `rn-4f307035b288` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Red Sea Mar |
