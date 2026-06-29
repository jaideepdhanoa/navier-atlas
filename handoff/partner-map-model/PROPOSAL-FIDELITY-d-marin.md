# Proposal fidelity — d-marin

**Verdict:** REWRITE
**Checked:** 2026-06-29T12:17:21Z

## Summary

- Items audited: 5
- KEEP: 2
- DROP: 3
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 3

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Split → Hvar | `edge__hvar-croatia__split` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Hvar' vs route 'Hv |
| journey | — | Korčula → Dubrovnik | `edge__korcula-croatia__dubrovnik` | **KEEP** | — |
| featured | 1 | Split ↔ Hvar | `edge__hvar-croatia__split` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Hvar' vs route 'Hv |
| featured | 2 | Korčula ↔ Dubrovnik | `edge__korcula-croatia__dubrovnik` | **KEEP** | — |
| featured | 3 | split-croatia ↔ venice-italy | `rn-ae7179e3ce7b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'split-croatia' → 'venice-ita |
