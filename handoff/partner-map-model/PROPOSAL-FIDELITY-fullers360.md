# Proposal fidelity — fullers360

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-02T19:16:17Z

## Summary

- Items audited: 12
- KEEP: 10
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 2
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Auckland Downtown Ferry Terminal (CBD) ↔ Devonport | `rn-5999ce7962d1` | **KEEP** | — |
| journey | — | Auckland Downtown Ferry Terminal (CBD) ↔ Matiatia  | `—` | **KEEP** | — |
| journey | — | Auckland Downtown Ferry Terminal (CBD) ↔ Gulf Harb | `—` | **KEEP** | — |
| journey | — | Auckland Downtown Ferry Terminal (CBD) ↔ Tryphena  | `—` | **KEEP** | — |
| featured | 1 | Auckland Downtown Ferry Terminal (CBD) ↔ Devonport | `rn-5999ce7962d1` | **KEEP** | — |
| featured | 1 | Auckland Downtown Ferry Terminal (CBD) ↔ Matiatia  | `—` | **KEEP** | — |
| featured | 1 | Auckland Downtown Ferry Terminal (CBD) ↔ Half Moon | `rn-e2418e4a8191` | **KEEP** | — |
| featured | 1 | Auckland Downtown Ferry Terminal (CBD) ↔ Bayswater | `rn-8e4964cba436` | **TRIM** | distance_honesty: card 2.0nm vs route 1.3nm (54% delta) |
| featured | 2 | Auckland Downtown Ferry Terminal (CBD) ↔ Hobsonvil | `rn-1a7829f121c8` | **TRIM** | distance_honesty: card 8.0nm vs route 5.4nm (48% delta) |
| featured | 2 | Auckland Downtown Ferry Terminal (CBD) ↔ Gulf Harb | `—` | **KEEP** | — |
| featured | 2 | Auckland Downtown Ferry Terminal (CBD) ↔ Rangitoto | `—` | **KEEP** | — |
| featured | 3 | Auckland Downtown Ferry Terminal (CBD) ↔ Tryphena  | `—` | **KEEP** | — |
