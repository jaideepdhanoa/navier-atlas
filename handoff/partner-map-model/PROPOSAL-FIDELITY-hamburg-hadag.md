# Proposal fidelity — hamburg-hadag

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-01T03:14:59Z

## Summary

- Items audited: 12
- KEEP: 5
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 7
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Landungsbrücken → Finkenwerder | `rn-f9c33ca7f60e` | **KEEP** | — |
| journey | — | Landungsbrücken → Neuhof | `rn-24451443bb54` | **TRIM** | distance_honesty: card 3.0nm vs route 1.5nm (100% delta) |
| journey | — | Landungsbrücken → Altona (Fischmarkt) | `rn-3aec7fb1f836` | **TRIM** | distance_honesty: card 2.0nm vs route 0.8nm (150% delta) |
| journey | — | Finkenwerder → Teufelsbrück | `rn-a5add4c4928b` | **TRIM** | distance_honesty: card 1.0nm vs route 1.5nm (33% delta) |
| featured | 1 | Landungsbrücken ↔ Finkenwerder | `rn-f9c33ca7f60e` | **KEEP** | — |
| featured | 1 | Landungsbrücken ↔ Altona (Fischmarkt) | `rn-3aec7fb1f836` | **TRIM** | distance_honesty: card 2.0nm vs route 0.8nm (150% delta) |
| featured | 1 | Landungsbrücken ↔ Elbphilharmonie | `rn-9771964f7bdc` | **TRIM** | distance_honesty: card 1.0nm vs route 0.6nm (67% delta) |
| featured | 2 | Landungsbrücken ↔ Neuhof | `rn-24451443bb54` | **TRIM** | distance_honesty: card 3.0nm vs route 1.5nm (100% delta) |
| featured | 2 | Finkenwerder ↔ Teufelsbrück | `rn-a5add4c4928b` | **TRIM** | distance_honesty: card 1.0nm vs route 1.5nm (33% delta) |
| featured | 2 | Elbphilharmonie ↔ Arningstraße | `rn-edce72f66ddb` | **KEEP** | — |
| featured | 3 | Landungsbrücken ↔ Blankenese | `rn-aa75b2a1bebb` | **KEEP** | — |
| featured | 3 | Blankenese ↔ Rüschpark | `rn-c1c5404c9fe2` | **KEEP** | — |
