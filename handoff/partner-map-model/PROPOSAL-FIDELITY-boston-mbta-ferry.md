# Proposal fidelity — boston-mbta-ferry

**Verdict:** TRIM
**Checked:** 2026-07-06T03:21:42Z

## Summary

- Items audited: 13
- KEEP: 12
- DROP: 1
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 1

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Long Wharf → Charlestown Navy Yard | `rn-d8b5284f787b` | **KEEP** | — |
| journey | — | Long Wharf → East Boston (Lewis Mall) | `—` | **KEEP** | — |
| journey | — | Long Wharf → Hingham Shipyard | `—` | **KEEP** | — |
| journey | — | Long Wharf → Hull (Pemberton Point) | `rn-4648b70105a3` | **KEEP** | — |
| featured | 1 | Long Wharf ↔ Charlestown Navy Yard | `rn-d8b5284f787b` | **KEEP** | — |
| featured | 1 | Long Wharf ↔ East Boston (Lewis Mall) | `—` | **KEEP** | — |
| featured | 1 | Long Wharf ↔ Logan Airport ferry dock | `rn-b1104ed2e1eb` | **KEEP** | — |
| featured | 2 | Long Wharf ↔ Hingham Shipyard | `—` | **KEEP** | — |
| featured | 2 | Long Wharf ↔ Hull (Pemberton Point) | `rn-4648b70105a3` | **KEEP** | — |
| featured | 2 | Hingham Shipyard ↔ Hull (Pemberton Point) | `rn-a0edcc795e58` | **DROP** | route_missing: rn-a0edcc795e58 not in gold; bp_binding: route_id rn-a0edcc795e58 missing from ROUTES.json |
| featured | 3 | Long Wharf ↔ Winthrop | `rn-99a8856990c8` | **KEEP** | — |
| featured | 3 | Long Wharf ↔ Lynn | `—` | **KEEP** | — |
| featured | 3 | Quincy (Fore River) ↔ Logan Airport ferry dock | `rn-0183727f495b` | **KEEP** | — |
