# Proposal fidelity — wsf

**Verdict:** TRIM
**Checked:** 2026-06-29T15:14:27Z

## Summary

- Items audited: 13
- KEEP: 11
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Seattle & Puget Sound: Fauntleroy Terminal → City  | `—` | **KEEP** | — |
| journey | — | Seattle & Puget Sound: Harbor Island Marina → Vash | `ics-144a42e64e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound: Harbo |
| journey | — | Seattle & Puget Sound: Cruise Terminal → Blakely H | `—` | **KEEP** | — |
| journey | — | Seattle & Puget Sound: Colman Dock → Seattle & Pug | `—` | **KEEP** | — |
| featured | 1 | Seattle & Puget Sound: Fauntleroy Terminal → City  | `—` | **KEEP** | — |
| featured | 1 | Seattle & Puget Sound: Harbor Island Marina → Vash | `ics-144a42e64e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Seattle & Puget Sound: Harbo |
| featured | 1 | Seattle & Puget Sound: Cruise Terminal → Blakely H | `—` | **KEEP** | — |
| featured | 2 | Seattle & Puget Sound: Cruise Terminal → Shilshole | `—` | **KEEP** | — |
| featured | 2 | Seattle & Puget Sound: Vashon Island North-End Fer | `—` | **KEEP** | — |
| featured | 2 | Seattle & Puget Sound: Elliott Bay Marina Inc → Sh | `—` | **KEEP** | — |
| featured | 3 | Colman Dock (Seattle Ferry Terminal) → Bainbridge  | `—` | **KEEP** | — |
| featured | 3 | Friday Harbor Ferry Terminal → Orcas Island Ferry  | `—` | **KEEP** | — |
| featured | 3 | Anacortes Ferry Terminal → Friday Harbor Ferry Ter | `—` | **KEEP** | — |
