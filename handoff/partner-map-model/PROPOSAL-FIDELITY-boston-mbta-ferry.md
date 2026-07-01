# Proposal fidelity — boston-mbta-ferry

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-01T03:14:58Z

## Summary

- Items audited: 13
- KEEP: 11
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 2
- BP-binding errors: 0

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
| featured | 2 | Hingham Shipyard ↔ Hull (Pemberton Point) | `rn-a0edcc795e58` | **TRIM** | distance_honesty: card 3.0nm vs route 2.3nm (30% delta) |
| featured | 3 | Long Wharf ↔ Winthrop | `rn-99a8856990c8` | **KEEP** | — |
| featured | 3 | Long Wharf ↔ Lynn | `—` | **KEEP** | — |
| featured | 3 | Quincy (Fore River) ↔ Logan Airport ferry dock | `rn-0183727f495b` | **TRIM** | distance_honesty: card 6.0nm vs route 8.2nm (27% delta) |
