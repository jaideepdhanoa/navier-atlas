# Proposal fidelity — rotterdam-mrdh

**Verdict:** REWRITE
**Checked:** 2026-07-06T03:21:43Z

## Summary

- Items audited: 7
- KEEP: 4
- DROP: 3
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 3

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Erasmusbrug (Willemsplein) Waterbus → Dordrecht Me | `rn-3f66b28288bb` | **KEEP** | — |
| journey | — | Erasmusbrug (Willemsplein) Waterbus → Kinderdijk W | `rn-abc26e08d412` | **DROP** | route_missing: rn-abc26e08d412 not in gold; bp_binding: route_id rn-abc26e08d412 missing from ROUTES.json |
| journey | — | Erasmusbrug (Willemsplein) Waterbus → Hoek van Hol | `rn-1b4b7ebdff41` | **KEEP** | — |
| featured | 1 | Erasmusbrug (Willemsplein) Waterbus → Dordrecht Me | `rn-3f66b28288bb` | **KEEP** | — |
| featured | 1 | Erasmusbrug (Willemsplein) Waterbus → Kinderdijk W | `rn-abc26e08d412` | **DROP** | route_missing: rn-abc26e08d412 not in gold; bp_binding: route_id rn-abc26e08d412 missing from ROUTES.json |
| featured | 2 | Dordrecht Merwekade Waterbus → Kinderdijk Waterbus | `rn-5fa92c917969` | **DROP** | route_missing: rn-5fa92c917969 not in gold; bp_binding: route_id rn-5fa92c917969 missing from ROUTES.json |
| featured | 2 | Erasmusbrug (Willemsplein) Waterbus → Hoek van Hol | `rn-1b4b7ebdff41` | **KEEP** | — |
