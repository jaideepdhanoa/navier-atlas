# Proposal fidelity — hong-kong

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:14:00Z

## Summary

- Items audited: 11
- KEEP: 7
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Hong Kong (Sheung Wan) → Macau (Outer Harbour) | `—` | **KEEP** | — |
| journey | — | Hong Kong → Shenzhen-Shekou / Zhuhai (PRD mainland | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **KEEP** | — |
| journey | — | HK Airport (SkyPier) → Macau (Outer Harbour / Taip | `—` | **KEEP** | — |
| journey | — | Hong Kong (Central piers) → Outlying islands (Lamm | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **KEEP** | — |
| featured | 1 | Central (Hong Kong Island) ↔ Tsim Sha Tsui (Kowloo | `—` | **KEEP** | — |
| featured | 1 | Central ↔ Outlying islands — Lamma, Cheung Chau, M | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Outlying islands |
| featured | 1 | HK Airport (SkyPier) ↔ Macau / PRD ports | `—` | **KEEP** | — |
| featured | 2 | Central ↔ Discovery Bay / Lantau | `edge__hong-kong__discovery-bay-lantau` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Discovery Bay /  |
| featured | 3 | Kai Tak cruise terminal / event pontoon ↔ Central  | `edge__hong-kong__kai-tak-cruise-terminal-sports-park-event-pontoon` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kai Tak cruise terminal / ev |
| featured | 4 | Central / Sheung Wan ↔ Macau (Outer Harbour) | `—` | **KEEP** | — |
| featured | 4 | HKIA SkyPier ↔ Shenzhen-Shekou / Zhuhai (PRD mainl | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **DROP** | bp_binding: labels ≠ route endpoints: card 'HKIA SkyPier' → 'Shenzhen-Sh |
