# Proposal fidelity — dubai-rta

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:13:55Z

## Summary

- Items audited: 13
- KEEP: 8
- DROP: 5
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Yas Marina → Four Seasons Al Maryah Jetty | `—` | **KEEP** | — |
| journey | — | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `—` | **KEEP** | — |
| journey | — | Dubai → Fujairah (east coast) | `rn-5bac21e43fcb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai' → 'Fujairah (east coa |
| journey | — | Ras Al Khaimah → ميناء صيادين غليلة | `—` | **KEEP** | — |
| featured | 1 | Dubai Marina / Harbour ↔ Palm Jumeirah / Dubai Isl | `—` | **KEEP** | — |
| featured | 1 | Dubai Creek ↔ Dubai Marina | `—` | **DROP** | phase_narrative_fit: Phase 1 Dubai beachhead but route cities ['ras-al-khaimah-ua |
| featured | 2 | Dubai Creek ↔ Dubai Harbour / Bluewaters | `rn-355d8ba3c15a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Creek' → 'Dubai Harbou |
| featured | 3 | Dubai ↔ Abu Dhabi waterfront | `gcn-4ae479b872-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai' → 'Abu Dhabi waterfro |
| featured | 3 | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **KEEP** | — |
| featured | 3 | Dubai Harbour Marina → Al Khan Lagoon mouth | `gcn-8e3c2d581c-bolt` | **KEEP** | — |
| featured | 4 | Dubai ↔ Doha | `rn-46f3eac13400` | **KEEP** | — |
| featured | 4 | Dubai ↔ Manama | `rn-fffd9a53d482` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai' → 'Manama' vs route ' |
| featured | 4 | Dubai ↔ Muscat | `—` | **KEEP** | — |
