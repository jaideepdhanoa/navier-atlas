# Proposal fidelity — bahrain-motc

**Verdict:** REWRITE
**Checked:** 2026-07-06T03:21:42Z

## Summary

- Items audited: 11
- KEEP: 8
- DROP: 3
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 3

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Bahrain Bay / Four Seasons (Manama) → Sa'ada Marin | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bahrain Bay / Four Seasons ( |
| journey | — | Bahrain Financial Harbour (Manama) → Amwaj Islands | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bahrain Financial Harbour (M |
| journey | — | Manama Corniche → Bahrain International Airport je | `—` | **KEEP** | — |
| journey | — | Reef Island (Manama) → Diyar Al Muharraq | `—` | **KEEP** | — |
| featured | 1 | Manama ↔ Muharraq inner-harbour shuttle | `—` | **KEEP** | — |
| featured | 1 | Manama Corniche ↔ Bahrain International Airport je | `—` | **KEEP** | — |
| featured | 2 | Manama ↔ Amwaj Islands | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama' → 'Amwaj Islands' vs |
| featured | 2 | Manama ↔ Diyar Al Muharraq | `—` | **KEEP** | — |
| featured | 2 | Manama ↔ Sitra | `—` | **KEEP** | — |
| featured | 3 | Bahrain ↔ Qatar (Sa'ada Marina ↔ Al-Ruwais) | `—` | **KEEP** | — |
| featured | 3 | Manama ↔ Saudi Eastern Province (causeway relief) | `—` | **KEEP** | — |
