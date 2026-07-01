# Proposal fidelity — mumbai-mmb

**Verdict:** TRIM
**Checked:** 2026-07-01T02:14:50Z

## Summary

- Items audited: 12
- KEEP: 10
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Gateway of India → Mandwa (Alibaug) | `—` | **KEEP** | — |
| journey | — | Gateway of India → Elephanta (Gharapuri) | `—` | **KEEP** | — |
| journey | — | Ferry Wharf (Bhaucha Dhakka) → Mora (Uran) | `—` | **KEEP** | — |
| journey | — | Belapur (Navi Mumbai) → Gateway of India | `—` | **KEEP** | — |
| featured | 1 | Gateway of India ↔ Mandwa (Alibaug) | `—` | **KEEP** | — |
| featured | 1 | Belapur (Navi Mumbai) ↔ Gateway of India | `—` | **KEEP** | — |
| featured | 2 | Gateway of India ↔ Elephanta (Gharapuri) | `—` | **KEEP** | — |
| featured | 2 | Ferry Wharf (Bhaucha Dhakka) ↔ Mora (Uran) | `—` | **KEEP** | — |
| featured | 2 | Belapur (Navi Mumbai) ↔ Nerul | `ics-971049e54f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Belapur (Navi Mumbai)' → 'Ne |
| featured | 3 | Vashi ↔ Airoli | `—` | **KEEP** | — |
| featured | 3 | Gateway of India ↔ Rewas | `ics-f811ad5db4` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Gateway of India' → 'Rewas'  |
| featured | 3 | Bandra ↔ Gateway of India | `—` | **KEEP** | — |
