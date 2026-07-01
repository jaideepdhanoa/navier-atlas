# Proposal fidelity — transport-nsw

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-01T03:14:59Z

## Summary

- Items audited: 12
- KEEP: 9
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 3
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Circular Quay ferry wharves → Manly Wharf | `—` | **KEEP** | — |
| journey | — | Circular Quay ferry wharves → Barangaroo Wharf | `—` | **KEEP** | — |
| journey | — | Circular Quay ferry wharves → Watsons Bay Wharf | `rn-a125df4284ba` | **KEEP** | — |
| journey | — | Barangaroo Wharf → Parramatta Wharf | `rn-0d609ac0ab33` | **TRIM** | distance_honesty: card 16.0nm vs route 9.8nm (63% delta) |
| featured | 1 | Circular Quay ferry wharves ↔ Manly Wharf | `—` | **KEEP** | — |
| featured | 1 | Circular Quay ferry wharves ↔ Barangaroo Wharf | `—` | **KEEP** | — |
| featured | 1 | Circular Quay ferry wharves ↔ Watsons Bay Wharf | `rn-a125df4284ba` | **KEEP** | — |
| featured | 2 | Barangaroo Wharf ↔ Parramatta Wharf | `rn-0d609ac0ab33` | **TRIM** | distance_honesty: card 16.0nm vs route 9.8nm (63% delta) |
| featured | 2 | Circular Quay ferry wharves ↔ Mosman Bay Wharf | `rn-2b603df666b7` | **TRIM** | distance_honesty: card 1.0nm vs route 1.9nm (47% delta) |
| featured | 3 | Circular Quay ferry wharves ↔ Cockatoo Island Whar | `—` | **KEEP** | — |
| featured | 3 | Barangaroo Wharf ↔ Sydney Fish Market Wharf | `—` | **KEEP** | — |
| featured | 4 | Circular Quay ferry wharves ↔ Taronga Zoo Wharf | `rn-9aa4b7d6ac10` | **KEEP** | — |
