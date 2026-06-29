# Proposal fidelity — d-marin

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:13:42Z

## Summary

- Items audited: 5
- KEEP: 3
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Split → Hvar | `edge__hvar-croatia__split` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Hvar' vs route 'Hv |
| journey | — | Korčula → Dubrovnik | `edge__korcula-croatia__dubrovnik` | **KEEP** | — |
| featured | 1 | Split ↔ Hvar | `—` | **KEEP** | — |
| featured | 2 | Korčula ↔ Dubrovnik | `rn-ebb2c7e82b38` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Korčula' → 'Dubrovnik' vs ro |
| featured | 3 | split-croatia ↔ venice-italy | `—` | **KEEP** | — |
