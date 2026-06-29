# Proposal fidelity — shun-tak

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:38Z

## Summary

- Items audited: 56
- KEEP: 50
- DROP: 6
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 6

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Central (Hong Kong Island) → Tsim Sha Tsui (Kowloo | `edge__hong-kong__tsim-sha-tsui-star-ferry-victoria-dockside` | **KEEP** | — |
| journey | — | Central → Outlying islands — Lamma, Cheung Chau, M | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Outlying islands |
| journey | — | Central → Discovery Bay / Lantau | `edge__hong-kong__discovery-bay-lantau` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Discovery Bay /  |
| journey | — | Kai Tak cruise terminal / event pontoon → Central  | `edge__hong-kong__kai-tak-cruise-terminal-sports-park-event-pontoon` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kai Tak cruise terminal / ev |
| journey | — | Hong Kong–Macau Ferry Terminal → Macau Outer Harbo | `e__hong-kong__hk-macau-ferry-terminal-sheung-wan__macau-china__macau-outer-harbour-ferry-terminal` | **KEEP** | — |
| journey | — | North Lantau → Outlying Islands | `ics-0c12b7f1a8` | **KEEP** | — |
| journey | — | Hong Kong → South HK Island | `ics-0c15a9c1bf` | **KEEP** | — |
| journey | — | Lantau → NT West | `ics-10fbfadeb5` | **KEEP** | — |
| journey | — | Outlying Islands: Outlying Islands — Lamma Island  | `ics-115254c150` | **KEEP** | — |
| journey | — | NT West → North Lantau | `ics-123c96c40b` | **KEEP** | — |
| journey | — | Lantau → West Lantau | `ics-1351043a92` | **KEEP** | — |
| journey | — | Outlying Islands → South Lantau | `ics-27c4b85d04` | **KEEP** | — |
| journey | — | South HK Island → Outlying Islands | `ics-3a1983969f` | **KEEP** | — |
| journey | — | Victoria Harbour → Outlying Islands | `ics-787899aca6` | **KEEP** | — |
| journey | — | Hong Kong → Victoria Harbour | `ics-7a9d126f16` | **KEEP** | — |
| journey | — | South HK Island → Outlying Islands | `ics-956a9d6190` | **KEEP** | — |
| journey | — | North Lantau → West Lantau | `ics-a24f3db94c` | **KEEP** | — |
| journey | — | South HK Island: South HK Island — Aberdeen / Shum | `ics-aa47cb0825` | **KEEP** | — |
| journey | — | Hong Kong → HK Island | `ics-b2ac50e442` | **KEEP** | — |
| journey | — | North Lantau → South Lantau | `ics-d53bf8f5c4` | **KEEP** | — |
| journey | — | Hong Kong → HK Island | `ics-dd9563f52a` | **KEEP** | — |
| journey | — | South HK Island → Victoria Harbour | `ics-e226a39c28` | **KEEP** | — |
| journey | — | Hong Kong → South HK Island | `ics-03f49b9ccf` | **KEEP** | — |
| journey | — | North Lantau → NT West | `ics-690a700460` | **KEEP** | — |
| journey | — | South HK Island → HK Island | `ics-93e86a029b` | **KEEP** | — |
| journey | — | Hong Kong → Wan Chai / Central waterfront extensio | `edge__hong-kong__wan-chai-central-waterfront-extension` | **KEEP** | — |
| journey | — | Hong Kong → Aberdeen / Repulse Bay / Stanley | `edge__hong-kong__aberdeen-repulse-bay-stanley-south-side` | **KEEP** | — |
| journey | — | Hong Kong → Shenzhen Shekou / Zhuhai | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **KEEP** | — |
| featured | 1 | Central (Hong Kong Island) ↔ Tsim Sha Tsui (Kowloo | `edge__hong-kong__tsim-sha-tsui-star-ferry-victoria-dockside` | **KEEP** | — |
| featured | 1 | Central ↔ Outlying islands — Lamma, Cheung Chau, M | `edge__hong-kong__outlying-islands-lamma-cheung-chau-peng-chau-mui-wo` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Outlying islands |
| featured | 1 | Central ↔ Discovery Bay / Lantau | `edge__hong-kong__discovery-bay-lantau` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Central' → 'Discovery Bay /  |
| featured | 1 | Kai Tak cruise terminal / event pontoon ↔ Central  | `edge__hong-kong__kai-tak-cruise-terminal-sports-park-event-pontoon` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kai Tak cruise terminal / ev |
| featured | 1 | Hong Kong–Macau Ferry Terminal → Macau Outer Harbo | `e__hong-kong__hk-macau-ferry-terminal-sheung-wan__macau-china__macau-outer-harbour-ferry-terminal` | **KEEP** | — |
| featured | 1 | North Lantau → Outlying Islands | `ics-0c12b7f1a8` | **KEEP** | — |
| featured | 1 | Hong Kong → South HK Island | `ics-0c15a9c1bf` | **KEEP** | — |
| featured | 1 | Lantau → NT West | `ics-10fbfadeb5` | **KEEP** | — |
| featured | 1 | Outlying Islands: Outlying Islands — Lamma Island  | `ics-115254c150` | **KEEP** | — |
| featured | 1 | NT West → North Lantau | `ics-123c96c40b` | **KEEP** | — |
| featured | 2 | Lantau → West Lantau | `ics-1351043a92` | **KEEP** | — |
| featured | 2 | Outlying Islands → South Lantau | `ics-27c4b85d04` | **KEEP** | — |
| featured | 2 | South HK Island → Outlying Islands | `ics-3a1983969f` | **KEEP** | — |
| featured | 2 | Victoria Harbour → Outlying Islands | `ics-787899aca6` | **KEEP** | — |
| featured | 2 | Hong Kong → Victoria Harbour | `ics-7a9d126f16` | **KEEP** | — |
| featured | 2 | South HK Island → Outlying Islands | `ics-956a9d6190` | **KEEP** | — |
| featured | 2 | North Lantau → West Lantau | `ics-a24f3db94c` | **KEEP** | — |
| featured | 2 | South HK Island: South HK Island — Aberdeen / Shum | `ics-aa47cb0825` | **KEEP** | — |
| featured | 2 | Hong Kong → HK Island | `ics-b2ac50e442` | **KEEP** | — |
| featured | 2 | North Lantau → South Lantau | `ics-d53bf8f5c4` | **KEEP** | — |
| featured | 3 | Hong Kong → HK Island | `ics-dd9563f52a` | **KEEP** | — |
| featured | 3 | South HK Island → Victoria Harbour | `ics-e226a39c28` | **KEEP** | — |
| featured | 3 | Hong Kong → South HK Island | `ics-03f49b9ccf` | **KEEP** | — |
| featured | 3 | North Lantau → NT West | `ics-690a700460` | **KEEP** | — |
| featured | 3 | South HK Island → HK Island | `ics-93e86a029b` | **KEEP** | — |
| featured | 3 | Hong Kong → Wan Chai / Central waterfront extensio | `edge__hong-kong__wan-chai-central-waterfront-extension` | **KEEP** | — |
| featured | 3 | Hong Kong → Aberdeen / Repulse Bay / Stanley | `edge__hong-kong__aberdeen-repulse-bay-stanley-south-side` | **KEEP** | — |
| featured | 3 | Hong Kong → Shenzhen Shekou / Zhuhai | `edge__hong-kong__shenzhen-shekou-zhuhai-prd-mainland` | **KEEP** | — |
