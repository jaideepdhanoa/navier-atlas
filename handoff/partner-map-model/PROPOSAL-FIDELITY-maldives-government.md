# Proposal fidelity — maldives-government

**Verdict:** REWRITE
**Checked:** 2026-06-29T12:18:53Z

## Summary

- Items audited: 38
- KEEP: 9
- DROP: 29
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 28

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Malé (Velana) → Soneva Fushi — flagship resort tra | `e__velana__soneva-fushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'Soneva Fus |
| journey | — | Malé (Velana) → Six Senses Laamu — southern-atoll  | `e__velana__six-senses-laamu-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'Six Senses |
| journey | — | Colombo → Malé — South Asian regional gateway | `edge-1155` | **KEEP** | — |
| journey | — | Malé (Velana) → North Malé resort transfers (visib | `ics-173c84d9b6` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'North Malé |
| journey | — | Malé (Velana) → North Malé resort transfers (visib | `ics-04c6991993` | **KEEP** | — |
| journey | — | Malé (Velana) → North Malé resort transfers (visib | `ics-0859b17244` | **KEEP** | — |
| journey | — | Malé (Velana) → North Malé resort transfers (visib | `ics-344b95721b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'North Malé |
| journey | — | Malé (Velana) → North Malé resort transfers (visib | `ics-e38bf95ac7` | **KEEP** | — |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__soneva-fushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__como-cocoa-island-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__kurumba-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__gili-lankanfushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__waldorf-ithaafushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__taj-exotica-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__banyan-tree-vabbinfaru-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__baros-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__patina-fari-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__ritz-fari-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| journey | — | Kadhdhoo Airport (Laamu) → Six Senses Laamu — sout | `e__mald__b95e8093ec6d` | **KEEP** | — |
| featured | 1 | Malé (Velana) → Soneva Fushi — flagship resort tra | `e__velana__soneva-fushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'Soneva Fus; phase_narrative_fit: Phase 1 beachhead but 63.7nm leg |
| featured | 1 | Malé (Velana) → Six Senses Laamu — southern-atoll  | `e__velana__six-senses-laamu-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'Six Senses; phase_narrative_fit: Phase 1 beachhead but 141.8nm leg |
| featured | 1 | Colombo ↔ Malé — South Asian regional gateway | `edge-1155` | **DROP** | phase_narrative_fit: Phase 1 beachhead but 413.1nm leg |
| featured | 1 | Malé (Velana) ↔ North Malé resort transfers (visib | `ics-173c84d9b6` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'North Malé |
| featured | 1 | Malé (Velana) ↔ North Malé resort transfers (visib | `ics-04c6991993` | **KEEP** | — |
| featured | 1 | Malé (Velana) ↔ North Malé resort transfers (visib | `ics-0859b17244` | **KEEP** | — |
| featured | 1 | Malé (Velana) ↔ North Malé resort transfers (visib | `ics-344b95721b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'North Malé |
| featured | 2 | Malé (Velana) ↔ North Malé resort transfers (visib | `ics-e38bf95ac7` | **KEEP** | — |
| featured | 2 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__soneva-fushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 2 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__como-cocoa-island-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 2 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__kurumba-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 2 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__gili-lankanfushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 2 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__waldorf-ithaafushi-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 2 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__taj-exotica-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 3 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__banyan-tree-vabbinfaru-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 3 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__baros-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 3 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__patina-fari-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 3 | Malé (Velana) → named resort jetties (promoted e__ | `e__velana__ritz-fari-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Malé (Velana)' → 'named reso |
| featured | 3 | Kadhdhoo Airport (Laamu) → Six Senses Laamu — sout | `e__mald__b95e8093ec6d` | **KEEP** | — |
