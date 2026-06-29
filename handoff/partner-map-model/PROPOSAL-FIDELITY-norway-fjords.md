# Proposal fidelity — norway-fjords

**Verdict:** REWRITE
**Checked:** 2026-06-29T12:19:00Z

## Summary

- Items audited: 9
- KEEP: 2
- DROP: 7
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 7

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Bergen (Strandkaiterminalen) → Stavanger (Fiskepir | `e__bergen-norway__strandkaiterminalen__stavanger-norway__fiskepiren-ferry-terminal` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bergen (Strandkaiterminalen) |
| journey | — | Geirangerfjord gateway — Festøya → Solavågen fjord | `ics-538b6e5b17` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Geirangerfjord gateway — Fes |
| journey | — | Stavanger / Lysefjord — Sør-Hidle → Tau (Ryfylke) | `ics-1ce41762cb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stavanger / Lysefjord — Sør- |
| journey | — | Bergen — Alvøen Kai → Bildøy Marina | `ics-c313e212ce` | **KEEP** | — |
| featured | 1 | Bergen (Strandkaiterminalen) ↔ Stavanger (Fiskepir | `e__bergen-norway__strandkaiterminalen__stavanger-norway__fiskepiren-ferry-terminal` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bergen (Strandkaiterminalen); phase_narrative_fit: Phase 1 beachhead but 101nm leg |
| featured | 1 | Geirangerfjord gateway — Festøya ↔ Solavågen fjord | `ics-538b6e5b17` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Geirangerfjord gateway — Fes |
| featured | 2 | Stavanger / Lysefjord — Sør-Hidle ↔ Tau (Ryfylke) | `ics-1ce41762cb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stavanger / Lysefjord — Sør- |
| featured | 2 | Bergen — Alvøen Kai ↔ Bildøy Marina | `ics-c313e212ce` | **KEEP** | — |
| featured | 3 | Stavanger / Lysefjord — Sør-Hidle ↔ Tau (Ryfylke) | `ics-1ce41762cb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stavanger / Lysefjord — Sør- |
