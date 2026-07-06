# Proposal fidelity — seoul-hangang-bus

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 10
- KEEP: 3
- DROP: 7
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 7

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Magok Pier → Mangwon Pier | `rn-dd8e26889f29` | **DROP** | route_missing: rn-dd8e26889f29 not in gold; bp_binding: route_id rn-dd8e26889f29 missing from ROUTES.json |
| journey | — | Mangwon Pier → Yeouido Pier | `rn-0a711c22926a` | **DROP** | route_missing: rn-0a711c22926a not in gold; bp_binding: route_id rn-0a711c22926a missing from ROUTES.json |
| journey | — | Yeouido Pier → Oksu Pier | `rn-6e4ab1de83d4` | **DROP** | route_missing: rn-6e4ab1de83d4 not in gold; bp_binding: route_id rn-6e4ab1de83d4 missing from ROUTES.json |
| journey | — | Oksu Pier → Apgujeong Pier | `rn-7c451ce2752d` | **KEEP** | — |
| featured | 1 | Yeouido Pier → Oksu Pier | `rn-6e4ab1de83d4` | **DROP** | route_missing: rn-6e4ab1de83d4 not in gold; bp_binding: route_id rn-6e4ab1de83d4 missing from ROUTES.json |
| featured | 1 | Oksu Pier → Apgujeong Pier | `rn-7c451ce2752d` | **KEEP** | — |
| featured | 1 | Apgujeong Pier → Seoul Forest Wharf | `rn-b4b6294b39e2` | **KEEP** | — |
| featured | 2 | Magok Pier → Mangwon Pier | `rn-dd8e26889f29` | **DROP** | route_missing: rn-dd8e26889f29 not in gold; bp_binding: route_id rn-dd8e26889f29 missing from ROUTES.json |
| featured | 2 | Mangwon Pier → Yeouido Pier | `rn-0a711c22926a` | **DROP** | route_missing: rn-0a711c22926a not in gold; bp_binding: route_id rn-0a711c22926a missing from ROUTES.json |
| featured | 2 | Ttukseom Pier → Jamsil Pier | `rn-529e3834c165` | **DROP** | route_missing: rn-529e3834c165 not in gold; bp_binding: route_id rn-529e3834c165 missing from ROUTES.json |
