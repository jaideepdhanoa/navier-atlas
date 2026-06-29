# Proposal fidelity — cote-dazur

**Verdict:** TRIM
**Checked:** 2026-06-29T12:17:19Z

## Summary

- Items audited: 5
- KEEP: 4
- DROP: 1
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 1

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Nice (Port) → Monaco (Port Hercule) | `e__cote-dazur-france__port-de-nice__monaco-monaco__port-hercule` | **KEEP** | — |
| journey | — | Cannes → Îles de Lérins (Sainte-Marguerite) | `ics-529325c5eb` | **KEEP** | — |
| featured | 1 | Nice (Port) ↔ Monaco (Port Hercule) | `e__cote-dazur-france__port-de-nice__monaco-monaco__port-hercule` | **KEEP** | — |
| featured | 2 | Cannes ↔ Îles de Lérins (Sainte-Marguerite) | `ics-529325c5eb` | **KEEP** | — |
| featured | 3 | costa-smeralda-italy ↔ cote-dazur-france | `rn-147bf78ddf5b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'costa-smeralda-italy' → 'cot |
