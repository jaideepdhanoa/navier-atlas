# Proposal fidelity — bahrain-motc

**Verdict:** TRIM
**Checked:** 2026-07-06T01:15:46Z

## Summary

- Items audited: 11
- KEEP: 10
- DROP: 1
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 1

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Bahrain Bay / Four Seasons (Manama) → Sa'ada Marin | `rn-5e90f69a5e03` | **KEEP** | — |
| journey | — | Bahrain Financial Harbour (Manama) → Amwaj Islands | `rn-f5130a29396c` | **KEEP** | — |
| journey | — | Manama Corniche → Bahrain International Airport je | `rn-b46c855eb3bf` | **KEEP** | — |
| journey | — | Reef Island (Manama) → Diyar Al Muharraq | `—` | **KEEP** | — |
| featured | 1 | Manama ↔ Muharraq inner-harbour shuttle | `—` | **KEEP** | — |
| featured | 1 | Manama Corniche ↔ Bahrain International Airport je | `rn-b46c855eb3bf` | **KEEP** | — |
| featured | 2 | Manama ↔ Amwaj Islands | `rn-f5130a29396c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama' → 'Amwaj Islands' vs |
| featured | 2 | Manama ↔ Diyar Al Muharraq | `—` | **KEEP** | — |
| featured | 2 | Manama ↔ Sitra | `—` | **KEEP** | — |
| featured | 3 | Bahrain ↔ Qatar (Sa'ada Marina ↔ Al-Ruwais) | `—` | **KEEP** | — |
| featured | 3 | Manama ↔ Saudi Eastern Province (causeway relief) | `—` | **KEEP** | — |
