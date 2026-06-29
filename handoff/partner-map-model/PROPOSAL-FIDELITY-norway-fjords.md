# Proposal fidelity — norway-fjords

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:46Z

## Summary

- Items audited: 9
- KEEP: 4
- DROP: 5
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 5

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Bergen (Strandkaiterminalen) → Stavanger (Fiskepir | `—` | **KEEP** | — |
| journey | — | Geirangerfjord gateway — Festøya → Solavågen fjord | `ics-538b6e5b17` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Geirangerfjord gateway — Fes |
| journey | — | Stavanger / Lysefjord — Sør-Hidle → Tau (Ryfylke) | `ics-1ce41762cb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stavanger / Lysefjord — Sør- |
| journey | — | Bergen — Alvøen Kai → Bildøy Marina | `—` | **KEEP** | — |
| featured | 1 | Bergen (Strandkaiterminalen) ↔ Stavanger (Fiskepir | `—` | **KEEP** | — |
| featured | 1 | Geirangerfjord gateway — Festøya ↔ Solavågen fjord | `ics-538b6e5b17` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Geirangerfjord gateway — Fes |
| featured | 2 | Stavanger / Lysefjord — Sør-Hidle ↔ Tau (Ryfylke) | `ics-1ce41762cb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stavanger / Lysefjord — Sør- |
| featured | 2 | Bergen — Alvøen Kai ↔ Bildøy Marina | `—` | **KEEP** | — |
| featured | 3 | Stavanger / Lysefjord — Sør-Hidle ↔ Tau (Ryfylke) | `ics-1ce41762cb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stavanger / Lysefjord — Sør- |
