# Proposal fidelity — shun-tak

**Verdict:** REWRITE
**Checked:** 2026-07-06T03:21:43Z

## Summary

- Items audited: 13
- KEEP: 8
- DROP: 5
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 5

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Central (Hong Kong Island) → Tsim Sha Tsui (Kowloo | `edge__hong-kong__tsim-sha-tsui-star-ferry-victoria-dockside` | **KEEP** | — |
| journey | — | Central → Outlying islands — Lamma, Cheung Chau, M | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Outlying islands |
| journey | — | Central → Discovery Bay / Lantau | `edge__hong-kong__discovery-bay-lantau` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Discovery Bay /  |
| journey | — | Kai Tak cruise terminal / event pontoon → Central  | `edge__hong-kong__kai-tak-cruise-terminal-sports-park-event-pontoon` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kai Tak cruise terminal / ev |
| featured | 1 | Central (Hong Kong Island) ↔ Tsim Sha Tsui (Kowloo | `edge__hong-kong__tsim-sha-tsui-star-ferry-victoria-dockside` | **KEEP** | — |
| featured | 1 | Central ↔ Outlying islands — Lamma, Cheung Chau, M | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Outlying islands |
| featured | 1 | Central ↔ Discovery Bay / Lantau | `edge__hong-kong__discovery-bay-lantau` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Discovery Bay /  |
| featured | 2 | Lantau → West Lantau | `ics-1351043a92` | **KEEP** | — |
| featured | 2 | Outlying Islands → South Lantau | `ics-27c4b85d04` | **KEEP** | — |
| featured | 2 | South HK Island → Outlying Islands | `ics-3a1983969f` | **KEEP** | — |
| featured | 3 | Hong Kong → HK Island | `ics-dd9563f52a` | **KEEP** | — |
| featured | 3 | South HK Island → Victoria Harbour | `ics-e226a39c28` | **KEEP** | — |
| featured | 3 | Hong Kong → South HK Island | `ics-03f49b9ccf` | **KEEP** | — |
