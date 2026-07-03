# Proposal fidelity — hawaii

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-03T02:54:02Z

## Summary

- Items audited: 11
- KEEP: 6
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 5
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Lahaina Harbor (Maui) ↔ Manele Harbor (Lānaʻi) | `rn-c9f2c84a930f` | **TRIM** | distance_honesty: card 9.0nm vs route 14.1nm (36% delta) |
| journey | — | Honolulu Harbor (Oʻahu) ↔ Lahaina Harbor (Maui) | `rn-e25ef6b56f0b` | **KEEP** | — |
| journey | — | Honolulu Harbor (Oʻahu) ↔ Kaunakakai Harbor (Molok | `rn-c8e5b922f861` | **KEEP** | — |
| journey | — | Māʻalaea Harbor (Maui) ↔ Kawaihae Harbor (Hawaiʻi  | `rn-c31c9226033b` | **TRIM** | distance_honesty: card 30.0nm vs route 59.3nm (49% delta) |
| featured | 1 | Lahaina Harbor (Maui) ↔ Manele Harbor (Lānaʻi) | `rn-c9f2c84a930f` | **TRIM** | distance_honesty: card 9.0nm vs route 14.1nm (36% delta) |
| featured | 1 | Māʻalaea Harbor (Maui) ↔ Manele Harbor (Lānaʻi) | `rn-81905e92b3fb` | **TRIM** | distance_honesty: card 13.0nm vs route 21.4nm (39% delta) |
| featured | 2 | Honolulu Harbor (Oʻahu) ↔ Kaunakakai Harbor (Molok | `rn-c8e5b922f861` | **KEEP** | — |
| featured | 2 | Honolulu Harbor (Oʻahu) ↔ Lahaina Harbor (Maui) | `rn-e25ef6b56f0b` | **KEEP** | — |
| featured | 2 | Lahaina Harbor (Maui) ↔ Kaunakakai Harbor (Molokaʻ | `rn-22e73dae1a4c` | **KEEP** | — |
| featured | 3 | Māʻalaea Harbor (Maui) ↔ Kawaihae Harbor (Hawaiʻi  | `rn-c31c9226033b` | **TRIM** | distance_honesty: card 30.0nm vs route 59.3nm (49% delta) |
| featured | 3 | Honolulu Harbor (Oʻahu) ↔ Nāwiliwili Harbor (Kauaʻ | `rn-040e1b32c700` | **KEEP** | — |
