# Proposal fidelity — hawaii

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:03Z

## Summary

- Items audited: 6
- KEEP: 2
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Oʻahu (Ko Olina) → Maui (Maalaea) — the marquee in | `edge-1127` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Oʻahu (Ko Olina)' → 'Maui (M |
| journey | — | Honolulu (Oʻahu) → Kauaʻi — the Garden Isle channe | `edge__oahu-honolulu-hawaii-usa__kauaʻi-nāwiliwili` | **KEEP** | — |
| journey | — | Maui → Hawaiʻi Island (Kawaihae) — the Big Island  | `edge__maui-county-hawaii-usa__hawaiʻi-island-kawaihae` | **KEEP** | — |
| featured | 1 | Oʻahu (Ko Olina) ↔ Maui (Maalaea) — the marquee in | `edge-1127` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Oʻahu (Ko Olina)' → 'Maui (M; phase_narrative_fit: Phase 1 beachhead but 72.1nm leg |
| featured | 2 | Honolulu (Oʻahu) ↔ Kauaʻi — the Garden Isle channe | `edge-1123` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Honolulu (Oʻahu)' → 'Kauaʻi  |
| featured | 3 | Maui ↔ Hawaiʻi Island (Kawaihae) — the Big Island  | `edge-1125` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Maui' → 'Hawaiʻi Island (Kaw |
