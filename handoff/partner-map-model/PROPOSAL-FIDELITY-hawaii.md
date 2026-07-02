# Proposal fidelity — hawaii

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-02T19:16:15Z

## Summary

- Items audited: 11
- KEEP: 10
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 1
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Lahaina Harbor (Maui) ↔ Manele Harbor (Lānaʻi) | `—` | **KEEP** | — |
| journey | — | Honolulu Harbor (Oʻahu) ↔ Lahaina Harbor (Maui) | `—` | **KEEP** | — |
| journey | — | Honolulu Harbor (Oʻahu) ↔ Kaunakakai Harbor (Molok | `—` | **KEEP** | — |
| journey | — | Māʻalaea Harbor (Maui) ↔ Kawaihae Harbor (Hawaiʻi  | `—` | **KEEP** | — |
| featured | 1 | Lahaina Harbor (Maui) ↔ Manele Harbor (Lānaʻi) | `—` | **KEEP** | — |
| featured | 1 | Māʻalaea Harbor (Maui) ↔ Manele Harbor (Lānaʻi) | `—` | **KEEP** | — |
| featured | 2 | Honolulu Harbor (Oʻahu) ↔ Kaunakakai Harbor (Molok | `—` | **KEEP** | — |
| featured | 2 | Honolulu Harbor (Oʻahu) ↔ Lahaina Harbor (Maui) | `—` | **KEEP** | — |
| featured | 2 | Lahaina Harbor (Maui) ↔ Kaunakakai Harbor (Molokaʻ | `rn-22e73dae1a4c` | **TRIM** | distance_honesty: card 15.0nm vs route 23.4nm (36% delta) |
| featured | 3 | Māʻalaea Harbor (Maui) ↔ Kawaihae Harbor (Hawaiʻi  | `—` | **KEEP** | — |
| featured | 3 | Honolulu Harbor (Oʻahu) ↔ Nāwiliwili Harbor (Kauaʻ | `rn-040e1b32c700` | **KEEP** | — |
