# Proposal fidelity — bahrain-motc

**Verdict:** REWRITE
**Checked:** 2026-07-01T02:14:49Z

## Summary

- Items audited: 11
- KEEP: 5
- DROP: 6
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 6

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Bahrain Bay / Four Seasons (Manama) → Sa'ada Marin | `—` | **KEEP** | — |
| journey | — | Bahrain Financial Harbour (Manama) → Amwaj Islands | `—` | **KEEP** | — |
| journey | — | Manama Corniche → Bahrain International Airport je | `rn-b46c855eb3bf` | **KEEP** | — |
| journey | — | Reef Island (Manama) → Diyar Al Muharraq | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Reef Island (Manama)' → 'Diy |
| featured | 1 | Manama ↔ Muharraq inner-harbour shuttle | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama' → 'Muharraq inner-ha |
| featured | 1 | Manama Corniche ↔ Bahrain International Airport je | `rn-b46c855eb3bf` | **KEEP** | — |
| featured | 2 | Manama ↔ Amwaj Islands | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama' → 'Amwaj Islands' vs |
| featured | 2 | Manama ↔ Diyar Al Muharraq | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama' → 'Diyar Al Muharraq |
| featured | 2 | Manama ↔ Sitra | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama' → 'Sitra' vs route ' |
| featured | 3 | Bahrain ↔ Qatar (Sa'ada Marina ↔ Al-Ruwais) | `rn-063a88bc18d1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bahrain' → 'Qatar (Sa'ada Ma |
| featured | 3 | Manama ↔ Saudi Eastern Province (causeway relief) | `rn-fffd9a53d482` | **KEEP** | — |
