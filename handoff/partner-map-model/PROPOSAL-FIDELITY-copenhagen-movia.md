# Proposal fidelity — copenhagen-movia

**Verdict:** REWRITE
**Checked:** 2026-07-06T03:21:42Z

## Summary

- Items audited: 7
- KEEP: 3
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Nyhavn Harbour Bus Stop → Opera House Ferry Stop | `rn-f7d4a824ec58` | **DROP** | route_missing: rn-f7d4a824ec58 not in gold; bp_binding: route_id rn-f7d4a824ec58 missing from ROUTES.json |
| journey | — | Nyhavn Harbour Bus Stop → Refshaleøen Ferry Stop | `rn-72c8fc7fb527` | **DROP** | route_missing: rn-72c8fc7fb527 not in gold; bp_binding: route_id rn-72c8fc7fb527 missing from ROUTES.json |
| journey | — | Opera House Ferry Stop → Nordre Toldbod Ferry Stop | `rn-6cb279554f53` | **KEEP** | — |
| featured | 1 | Nyhavn Harbour Bus Stop → Opera House Ferry Stop | `rn-f7d4a824ec58` | **DROP** | route_missing: rn-f7d4a824ec58 not in gold; bp_binding: route_id rn-f7d4a824ec58 missing from ROUTES.json |
| featured | 1 | Nyhavn Harbour Bus Stop → Refshaleøen Ferry Stop | `rn-72c8fc7fb527` | **DROP** | route_missing: rn-72c8fc7fb527 not in gold; bp_binding: route_id rn-72c8fc7fb527 missing from ROUTES.json |
| featured | 2 | Opera House Ferry Stop → Nordre Toldbod Ferry Stop | `rn-6cb279554f53` | **KEEP** | — |
| featured | 2 | Nordre Toldbod Ferry Stop → Refshaleøen Ferry Stop | `rn-192c0b6dac5e` | **KEEP** | — |
