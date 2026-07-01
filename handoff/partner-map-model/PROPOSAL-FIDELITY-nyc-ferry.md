# Proposal fidelity — nyc-ferry

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-01T03:14:59Z

## Summary

- Items audited: 12
- KEEP: 8
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 4
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Wall Street → East 34th Street | `rn-b2490e3f6350` | **TRIM** | distance_honesty: card 5.3nm vs route 2.9nm (83% delta) |
| journey | — | DUMBO → Wall Street | `rn-c5916368a650` | **KEEP** | — |
| journey | — | Wall Street → Rockaway | `rn-73b284aecb57` | **KEEP** | — |
| journey | — | East 34th Street → Soundview | `rn-711092a81931` | **TRIM** | distance_honesty: card 9.5nm vs route 6.7nm (42% delta) |
| featured | 1 | Wall Street ↔ East 34th Street | `rn-b2490e3f6350` | **TRIM** | distance_honesty: card 5.3nm vs route 2.9nm (83% delta) |
| featured | 1 | DUMBO ↔ Wall Street | `rn-c5916368a650` | **KEEP** | — |
| featured | 1 | Wall Street ↔ Rockaway | `rn-73b284aecb57` | **KEEP** | — |
| featured | 2 | East 34th Street ↔ Soundview | `rn-711092a81931` | **TRIM** | distance_honesty: card 9.5nm vs route 6.7nm (42% delta) |
| featured | 2 | Wall Street ↔ St. George | `rn-76ebdbee871d` | **KEEP** | — |
| featured | 3 | Wall Street ↔ Atlantic Avenue | `—` | **KEEP** | — |
| featured | 3 | Atlantic Avenue ↔ Bay Ridge | `rn-5d8325451e3d` | **KEEP** | — |
| featured | 4 | Wall Street ↔ Astoria | `—` | **KEEP** | — |
