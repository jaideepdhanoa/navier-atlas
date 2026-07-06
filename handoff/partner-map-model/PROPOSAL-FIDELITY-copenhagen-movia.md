# Proposal fidelity — copenhagen-movia

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-06T01:15:46Z

## Summary

- Items audited: 7
- KEEP: 5
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 2
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Nyhavn Harbour Bus Stop → Opera House Ferry Stop | `rn-f7d4a824ec58` | **TRIM** | distance_honesty: card 0.3nm vs route 0.4nm (25% delta) |
| journey | — | Nyhavn Harbour Bus Stop → Refshaleøen Ferry Stop | `rn-72c8fc7fb527` | **KEEP** | — |
| journey | — | Opera House Ferry Stop → Nordre Toldbod Ferry Stop | `rn-6cb279554f53` | **KEEP** | — |
| featured | 1 | Nyhavn Harbour Bus Stop → Opera House Ferry Stop | `rn-f7d4a824ec58` | **TRIM** | distance_honesty: card 0.3nm vs route 0.4nm (25% delta) |
| featured | 1 | Nyhavn Harbour Bus Stop → Refshaleøen Ferry Stop | `rn-72c8fc7fb527` | **KEEP** | — |
| featured | 2 | Opera House Ferry Stop → Nordre Toldbod Ferry Stop | `rn-6cb279554f53` | **KEEP** | — |
| featured | 2 | Nordre Toldbod Ferry Stop → Refshaleøen Ferry Stop | `rn-192c0b6dac5e` | **KEEP** | — |
