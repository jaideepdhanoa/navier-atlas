# Proposal fidelity — bahrain-motc

**Verdict:** REWRITE
**Checked:** 2026-06-29T12:17:12Z

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
| journey | — | RAK Harbour / Corniche → Al Marjan and Mina Al Ara | `rn-ea8ffe092848` | **DROP** | bp_binding: labels ≠ route endpoints: card 'RAK Harbour / Corniche' → 'A |
| journey | — | Dubai Harbour → Wynn Al Marjan Island | `rn-0bdf53c78a31` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour' → 'Wynn Al Ma |
| journey | — | Manama Financial Harbour / Bahrain Bay → domestic  | `—` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/rakta |
| featured | 1 | Manama waterfront ↔ Sitra / Hawar fast passenger p | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama waterfront' → 'Sitra  |
| featured | 2 | Manama ↔ KSA Eastern Province | `rn-fffd9a53d482` | **KEEP** | — |
| featured | 3 | Manama ↔ Doha | `—` | **KEEP** | — |
| featured | 3 | Manama ↔ Dubai | `—` | **KEEP** | — |
| featured | 3 | Manama ↔ Abu Dhabi | `rn-c69c27c8b6e4` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manama' → 'Abu Dhabi' vs rou |
| featured | 3 | Ras Al Khaimah → Muscat | `edge-0772` | **KEEP** | — |
| featured | 3 | Ras Al Khaimah → Doha | `edge-0774` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ras Al Khaimah' → 'Doha' vs  |
| featured | 3 | Ras Al Khaimah → Manama | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ras Al Khaimah' → 'Manama' v |
