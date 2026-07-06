# Proposal fidelity — bangkok-chao-phraya

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:08Z

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
| journey | — | Sathorn (Central / Taksin) → Phra Arthit (N13) | `rn-25379cffb8f5` | **DROP** | route_missing: rn-25379cffb8f5 not in gold; bp_binding: route_id rn-25379cffb8f5 missing from ROUTES.json |
| journey | — | Sathorn (Central / Taksin) → Nonthaburi (N30) | `rn-c18979a20340` | **DROP** | route_missing: rn-c18979a20340 not in gold; bp_binding: route_id rn-c18979a20340 missing from ROUTES.json |
| journey | — | Nonthaburi (N30) → Pak Kret (N33) | `rn-4b84916793ff` | **DROP** | route_missing: rn-4b84916793ff not in gold; bp_binding: route_id rn-4b84916793ff missing from ROUTES.json |
| journey | — | Sathorn (Central / Taksin) → Wat Rajsingkorn (S3) | `—` | **KEEP** | — |
| featured | 1 | Sathorn (Central / Taksin) ↔ Phra Arthit (N13) | `rn-25379cffb8f5` | **DROP** | route_missing: rn-25379cffb8f5 not in gold; bp_binding: route_id rn-25379cffb8f5 missing from ROUTES.json |
| featured | 1 | Sathorn (Central / Taksin) ↔ Tha Chang (N9) | `rn-6caac4541352` | **DROP** | route_missing: rn-6caac4541352 not in gold; bp_binding: route_id rn-6caac4541352 missing from ROUTES.json |
| featured | 1 | Sathorn (Central / Taksin) ↔ ICONSIAM | `—` | **KEEP** | — |
| featured | 2 | Sathorn (Central / Taksin) ↔ Nonthaburi (N30) | `rn-c18979a20340` | **DROP** | route_missing: rn-c18979a20340 not in gold; bp_binding: route_id rn-c18979a20340 missing from ROUTES.json |
| featured | 2 | Sathorn (Central / Taksin) ↔ Wat Rajsingkorn (S3) | `—` | **KEEP** | — |
| featured | 2 | Sathorn (Central / Taksin) ↔ Rama VIII (N14) | `—` | **KEEP** | — |
| featured | 3 | Nonthaburi (N30) ↔ Pak Kret (N33) | `rn-4b84916793ff` | **DROP** | route_missing: rn-4b84916793ff not in gold; bp_binding: route_id rn-4b84916793ff missing from ROUTES.json |
| featured | 3 | Sathorn (Central / Taksin) ↔ Rat Burana (S4) | `—` | **KEEP** | — |
