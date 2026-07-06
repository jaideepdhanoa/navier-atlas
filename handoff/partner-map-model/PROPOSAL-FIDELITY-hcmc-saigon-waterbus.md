# Proposal fidelity — hcmc-saigon-waterbus

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 8
- KEEP: 4
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Bach Dang Wharf (District 1) → Binh An Waterbus St | `rn-9eb0307b3eb1` | **DROP** | route_missing: rn-9eb0307b3eb1 not in gold; bp_binding: route_id rn-9eb0307b3eb1 missing from ROUTES.json |
| journey | — | Binh An Waterbus Station (Thu Duc) → Thanh Da Whar | `rn-da00b3e2e930` | **DROP** | route_missing: rn-da00b3e2e930 not in gold; bp_binding: route_id rn-da00b3e2e930 missing from ROUTES.json |
| journey | — | Thanh Da Wharf (Binh Thanh) → Linh Dong Wharf (Thu | `rn-0f49fc10d206` | **KEEP** | — |
| journey | — | Bach Dang Wharf (District 1) → Linh Dong Wharf (Th | `rn-e32f782a58ac` | **KEEP** | — |
| featured | 1 | Bach Dang Wharf (District 1) → Binh An Waterbus St | `rn-9eb0307b3eb1` | **DROP** | route_missing: rn-9eb0307b3eb1 not in gold; bp_binding: route_id rn-9eb0307b3eb1 missing from ROUTES.json |
| featured | 1 | Binh An Waterbus Station (Thu Duc) → Thanh Da Whar | `rn-da00b3e2e930` | **DROP** | route_missing: rn-da00b3e2e930 not in gold; bp_binding: route_id rn-da00b3e2e930 missing from ROUTES.json |
| featured | 2 | Thanh Da Wharf (Binh Thanh) → Linh Dong Wharf (Thu | `rn-0f49fc10d206` | **KEEP** | — |
| featured | 2 | Bach Dang Wharf (District 1) → Linh Dong Wharf (Th | `rn-e32f782a58ac` | **KEEP** | — |
