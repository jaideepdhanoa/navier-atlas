# Proposal fidelity — d-marin

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 5
- KEEP: 2
- DROP: 3
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 3

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Hvar & the Pakleni Islands → Split | `edge__hvar-croatia__split` | **DROP** | route_missing: edge__hvar-croatia__split not in gold; bp_binding: route_id edge__hvar-croatia__split missing from ROUTES.json |
| journey | — | Korčula → Dubrovnik | `edge__korcula-croatia__dubrovnik` | **DROP** | route_missing: edge__korcula-croatia__dubrovnik not in gold; bp_binding: route_id edge__korcula-croatia__dubrovnik missing from ROUTE |
| featured | 1 | Trajektna luka Split → Hvar Town Port | `—` | **KEEP** | — |
| featured | 2 | Korčula ↔ Dubrovnik | `rn-859abcf7ec1e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Korčula' → 'Dubrovnik' vs ro |
| featured | 3 | Split & Central Dalmatia → Venice Lagoon | `—` | **KEEP** | — |
