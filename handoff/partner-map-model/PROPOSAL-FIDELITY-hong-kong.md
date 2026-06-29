# Proposal fidelity — hong-kong

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:03Z

## Summary

- Items audited: 15
- KEEP: 9
- DROP: 6
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 6

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Hong Kong (Sheung Wan) → Macau (Outer Harbour) | `—` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/shun-tak |
| journey | — | Hong Kong → Shenzhen-Shekou / Zhuhai (PRD mainland | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/shun-tak |
| journey | — | HK Airport (SkyPier) → Macau (Outer Harbour / Taip | `—` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/shun-tak |
| journey | — | Hong Kong (Central piers) → Outlying islands (Lamm | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/shun-tak |
| journey | — | Macau (Outer Harbour) → Shenzhen-Shekou / Zhuhai ( | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Macau (Outer Harbour)' → 'Sh; inheritance_debt: _inherit_source=grok/normalize/shun-tak |
| journey | — | HK Airport (SkyPier) → Shenzhen-Shekou (PRD mainla | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **DROP** | bp_binding: labels ≠ route endpoints: card 'HK Airport (SkyPier)' → 'She; inheritance_debt: _inherit_source=grok/normalize/shun-tak |
| journey | — | Macau (Outer Harbour) → Taipa / Cotai | `ics-86ce23e759` | **KEEP** | — |
| journey | — | Hong Kong (Central piers) → Tsim Sha Tsui / Victor | `ics-7a9d126f16` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/shun-tak |
| featured | 1 | Central (Hong Kong Island) ↔ Tsim Sha Tsui (Kowloo | `edge__hong-kong__tsim-sha-tsui-star-ferry-victoria-dockside` | **KEEP** | — |
| featured | 1 | Central ↔ Outlying islands — Lamma, Cheung Chau, M | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Outlying islands |
| featured | 1 | HK Airport (SkyPier) ↔ Macau / PRD ports | `—` | **KEEP** | — |
| featured | 2 | Central ↔ Discovery Bay / Lantau | `edge__hong-kong__discovery-bay-lantau` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Discovery Bay /  |
| featured | 3 | Kai Tak cruise terminal / event pontoon ↔ Central  | `edge__hong-kong__kai-tak-cruise-terminal-sports-park-event-pontoon` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kai Tak cruise terminal / ev |
| featured | 4 | Central / Sheung Wan ↔ Macau (Outer Harbour) | `—` | **KEEP** | — |
| featured | 4 | HKIA SkyPier ↔ Shenzhen-Shekou / Zhuhai (PRD mainl | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **DROP** | bp_binding: labels ≠ route endpoints: card 'HKIA SkyPier' → 'Shenzhen-Sh |
