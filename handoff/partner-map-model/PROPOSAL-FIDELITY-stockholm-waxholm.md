# Proposal fidelity — stockholm-waxholm

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 13
- KEEP: 5
- DROP: 8
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 8

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Strömkajen (central Stockholm) → Vaxholm | `rn-b9c0a089fb61` | **DROP** | route_missing: rn-b9c0a089fb61 not in gold; bp_binding: route_id rn-b9c0a089fb61 missing from ROUTES.json |
| journey | — | Strömkajen (central Stockholm) → Nacka Strand | `—` | **KEEP** | — |
| journey | — | Frihamnen → Nybroplan | `—` | **KEEP** | — |
| journey | — | Vaxholm → Grinda | `rn-74e760c9c73c` | **DROP** | route_missing: rn-74e760c9c73c not in gold; bp_binding: route_id rn-74e760c9c73c missing from ROUTES.json |
| featured | 1 | Strömkajen (central Stockholm) ↔ Vaxholm | `rn-b9c0a089fb61` | **DROP** | route_missing: rn-b9c0a089fb61 not in gold; bp_binding: route_id rn-b9c0a089fb61 missing from ROUTES.json |
| featured | 1 | Strömkajen (central Stockholm) ↔ Nacka Strand | `—` | **KEEP** | — |
| featured | 1 | Frihamnen ↔ Nybroplan | `—` | **KEEP** | — |
| featured | 2 | Vaxholm ↔ Grinda | `rn-74e760c9c73c` | **DROP** | route_missing: rn-74e760c9c73c not in gold; bp_binding: route_id rn-74e760c9c73c missing from ROUTES.json |
| featured | 2 | Stavsnäs ↔ Sandhamn | `rn-8b9e8987c141` | **DROP** | route_missing: rn-8b9e8987c141 not in gold; bp_binding: route_id rn-8b9e8987c141 missing from ROUTES.json |
| featured | 2 | Vaxholm ↔ Ljusterö (Linanäs) | `rn-a3cc72c67a37` | **DROP** | route_missing: rn-a3cc72c67a37 not in gold; bp_binding: route_id rn-a3cc72c67a37 missing from ROUTES.json |
| featured | 3 | Strömkajen (central Stockholm) ↔ Sandhamn | `rn-afc06d85e708` | **DROP** | route_missing: rn-afc06d85e708 not in gold; bp_binding: route_id rn-afc06d85e708 missing from ROUTES.json |
| featured | 3 | Stavsnäs ↔ Nämdö | `—` | **KEEP** | — |
| featured | 3 | Strömkajen (central Stockholm) ↔ Utö | `rn-72110604025d` | **DROP** | route_missing: rn-72110604025d not in gold; bp_binding: route_id rn-72110604025d missing from ROUTES.json |
