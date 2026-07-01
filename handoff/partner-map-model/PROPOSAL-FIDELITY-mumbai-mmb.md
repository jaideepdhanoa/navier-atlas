# Proposal fidelity — mumbai-mmb

**Verdict:** TRIM
**Checked:** 2026-07-01T03:14:59Z

## Summary

- Items audited: 12
- KEEP: 1
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 9
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Gateway of India → Mandwa (Alibaug) | `rn-c9bcc9219b04` | **TRIM** | distance_honesty: card 2.1nm vs route 7.3nm (71% delta) |
| journey | — | Gateway of India → Elephanta (Gharapuri) | `rn-af6a20ee2a0a` | **TRIM** | distance_honesty: card 2.1nm vs route 6.0nm (65% delta) |
| journey | — | Ferry Wharf (Bhaucha Dhakka) → Mora (Uran) | `rn-a685bc50d3c2` | **TRIM** | distance_honesty: card 2.5nm vs route 8.2nm (70% delta) |
| journey | — | Belapur (Navi Mumbai) → Gateway of India | `rn-0c05727c37fa` | **TRIM** | distance_honesty: card 2.1nm vs route 12.7nm (83% delta) |
| featured | 1 | Gateway of India ↔ Mandwa (Alibaug) | `rn-c9bcc9219b04` | **TRIM** | distance_honesty: card 2.1nm vs route 7.3nm (71% delta) |
| featured | 1 | Belapur (Navi Mumbai) ↔ Gateway of India | `rn-0c05727c37fa` | **TRIM** | distance_honesty: card 2.1nm vs route 12.7nm (83% delta) |
| featured | 2 | Gateway of India ↔ Elephanta (Gharapuri) | `rn-af6a20ee2a0a` | **TRIM** | distance_honesty: card 2.1nm vs route 6.0nm (65% delta) |
| featured | 2 | Ferry Wharf (Bhaucha Dhakka) ↔ Mora (Uran) | `rn-a685bc50d3c2` | **TRIM** | distance_honesty: card 2.5nm vs route 8.2nm (70% delta) |
| featured | 2 | Belapur (Navi Mumbai) ↔ Nerul | `ics-ed747a4789` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Belapur (Navi Mumbai)' → 'Ne |
| featured | 3 | Vashi ↔ Airoli | `rn-8faa635f9348` | **KEEP** | — |
| featured | 3 | Gateway of India ↔ Rewas | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Gateway of India' → 'Rewas'  |
| featured | 3 | Bandra ↔ Gateway of India | `rn-c70751e14751` | **TRIM** | distance_honesty: card 2.1nm vs route 7.4nm (72% delta) |
