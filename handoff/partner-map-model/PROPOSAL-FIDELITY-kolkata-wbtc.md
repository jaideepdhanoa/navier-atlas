# Proposal fidelity — kolkata-wbtc

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 12
- KEEP: 3
- DROP: 9
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 9

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Howrah Ferry Ghat → Millennium Park Jetty | `rn-e9a7f7e474e3` | **DROP** | route_missing: rn-e9a7f7e474e3 not in gold; bp_binding: route_id rn-e9a7f7e474e3 missing from ROUTES.json |
| journey | — | Howrah Ferry Ghat → Fairlie Place Ferry | `rn-97202b12d2ce` | **DROP** | route_missing: rn-97202b12d2ce not in gold; bp_binding: route_id rn-97202b12d2ce missing from ROUTES.json |
| journey | — | Dakshineswar Ferry Ghat → Belur Math Ferry Ghat | `rn-b44cfaae1be2` | **DROP** | route_missing: rn-b44cfaae1be2 not in gold; bp_binding: route_id rn-b44cfaae1be2 missing from ROUTES.json |
| journey | — | Millennium Park Jetty → Chandannagar Riverfront | `rn-174af2f4a97c` | **DROP** | route_missing: rn-174af2f4a97c not in gold; bp_binding: route_id rn-174af2f4a97c missing from ROUTES.json |
| featured | 1 | Howrah Ferry Ghat ↔ Millennium Park Jetty | `rn-e9a7f7e474e3` | **DROP** | route_missing: rn-e9a7f7e474e3 not in gold; bp_binding: route_id rn-e9a7f7e474e3 missing from ROUTES.json |
| featured | 1 | Howrah Ferry Ghat ↔ Fairlie Place Ferry | `rn-97202b12d2ce` | **DROP** | route_missing: rn-97202b12d2ce not in gold; bp_binding: route_id rn-97202b12d2ce missing from ROUTES.json |
| featured | 2 | Fairlie Place Ferry ↔ Bagbazar Ghat | `rn-46a91df66302` | **DROP** | route_missing: rn-46a91df66302 not in gold; bp_binding: route_id rn-46a91df66302 missing from ROUTES.json |
| featured | 2 | Dakshineswar Ferry Ghat ↔ Belur Math Ferry Ghat | `rn-b44cfaae1be2` | **DROP** | route_missing: rn-b44cfaae1be2 not in gold; bp_binding: route_id rn-b44cfaae1be2 missing from ROUTES.json |
| featured | 3 | Millennium Park Jetty ↔ Chandannagar Riverfront | `rn-174af2f4a97c` | **DROP** | route_missing: rn-174af2f4a97c not in gold; bp_binding: route_id rn-174af2f4a97c missing from ROUTES.json |
| featured | 4 | Howrah ↔ Babughat (Chandpal Ghat) | `—` | **KEEP** | — |
| featured | 4 | Howrah ↔ Armenian Ghat | `—` | **KEEP** | — |
| featured | 4 | Howrah ↔ Baghbazar Ghat | `—` | **KEEP** | — |
