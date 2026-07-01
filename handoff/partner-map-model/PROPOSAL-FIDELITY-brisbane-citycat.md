# Proposal fidelity — brisbane-citycat

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-07-01T03:14:58Z

## Summary

- Items audited: 12
- KEEP: 2
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 10
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | UQ St Lucia → North Quay | `rn-771a3b2ef251` | **TRIM** | distance_honesty: card 2.6nm vs route 1.6nm (62% delta) |
| journey | — | South Bank → Riverside | `rn-e3914af94b36` | **TRIM** | distance_honesty: card 1.0nm vs route 0.6nm (67% delta) |
| journey | — | North Quay → Northshore Hamilton | `rn-19fbaad122e8` | **TRIM** | distance_honesty: card 6.5nm vs route 3.7nm (76% delta) |
| journey | — | Riverside → Bulimba | `rn-5a374ade1b89` | **TRIM** | distance_honesty: card 3.2nm vs route 2.2nm (45% delta) |
| featured | 1 | UQ St Lucia ↔ North Quay | `rn-771a3b2ef251` | **TRIM** | distance_honesty: card 2.6nm vs route 1.6nm (62% delta) |
| featured | 1 | South Bank ↔ Riverside | `rn-e3914af94b36` | **TRIM** | distance_honesty: card 1.0nm vs route 0.6nm (67% delta) |
| featured | 1 | Holman Street (Kangaroo Point) ↔ Riverside | `rn-4558d9d269ed` | **KEEP** | — |
| featured | 2 | North Quay ↔ Northshore Hamilton | `rn-19fbaad122e8` | **TRIM** | distance_honesty: card 6.5nm vs route 3.7nm (76% delta) |
| featured | 2 | Riverside ↔ Bulimba | `rn-5a374ade1b89` | **TRIM** | distance_honesty: card 3.2nm vs route 2.2nm (45% delta) |
| featured | 2 | New Farm Park ↔ QUT Gardens Point | `rn-35192771d472` | **TRIM** | distance_honesty: card 2.4nm vs route 1.2nm (100% delta) |
| featured | 3 | Teneriffe ↔ Bulimba | `rn-5d114961ba2f` | **KEEP** | — |
| featured | 3 | Hawthorne ↔ North Quay | `rn-41e5061725f4` | **TRIM** | distance_honesty: card 4.4nm vs route 2.5nm (76% delta) |
