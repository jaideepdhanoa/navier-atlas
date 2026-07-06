# Proposal fidelity — gothenburg-vasttrafik

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 7
- KEEP: 0
- DROP: 7
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 7

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Styrsö Bratten Pier → Vrångö Pier | `rn-f1d39ae68265` | **DROP** | route_missing: rn-f1d39ae68265 not in gold; bp_binding: route_id rn-f1d39ae68265 missing from ROUTES.json |
| journey | — | Saltholmen Ferry Terminal → Styrsö Bratten Pier | `rn-e4e4b4528230` | **DROP** | route_missing: rn-e4e4b4528230 not in gold; bp_binding: route_id rn-e4e4b4528230 missing from ROUTES.json |
| journey | — | Saltholmen Ferry Terminal → Vrångö Pier | `rn-dc8e5c244e9c` | **DROP** | route_missing: rn-dc8e5c244e9c not in gold; bp_binding: route_id rn-dc8e5c244e9c missing from ROUTES.json |
| featured | 1 | Styrsö Bratten Pier → Vrångö Pier | `rn-f1d39ae68265` | **DROP** | route_missing: rn-f1d39ae68265 not in gold; bp_binding: route_id rn-f1d39ae68265 missing from ROUTES.json |
| featured | 1 | Saltholmen Ferry Terminal → Styrsö Bratten Pier | `rn-e4e4b4528230` | **DROP** | route_missing: rn-e4e4b4528230 not in gold; bp_binding: route_id rn-e4e4b4528230 missing from ROUTES.json |
| featured | 2 | Saltholmen Ferry Terminal → Vrångö Pier | `rn-dc8e5c244e9c` | **DROP** | route_missing: rn-dc8e5c244e9c not in gold; bp_binding: route_id rn-dc8e5c244e9c missing from ROUTES.json |
| featured | 2 | Saltholmen Ferry Terminal → Fiskebäckskil Pier | `rn-2f8d13f61db7` | **DROP** | route_missing: rn-2f8d13f61db7 not in gold; bp_binding: route_id rn-2f8d13f61db7 missing from ROUTES.json |
