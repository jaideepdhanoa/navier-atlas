# Proposal fidelity — universal-enterprises

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:56Z

## Summary

- Items audited: 10
- KEEP: 5
- DROP: 5
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 5

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Velana International Airport (Malé) → North & Sout | `e__velana__kurumba-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Velana International Airport |
| journey | — | Malé hub → Ari Atoll / Baa Atoll resorts | `—` | **KEEP** | — |
| journey | — | Velana International Airport → Greater Malé / Hulh | `e__velana__kurumba-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Velana International Airport |
| journey | — | Universal Resorts resort lagoon → Neighbouring isl | `—` | **KEEP** | inheritance_debt: _inherit_source=grok/normalize/jih-global |
| featured | 1 | Velana International Airport (Malé) ↔ North & Sout | `e__velana__kurumba-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Velana International Airport |
| featured | 1 | Velana International Airport ↔ Greater Malé / Hulh | `e__velana__kurumba-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Velana International Airport |
| featured | 2 | Malé hub ↔ Ari Atoll / Baa Atoll resorts | `—` | **KEEP** | — |
| featured | 2 | Resort lagoon ↔ Neighbouring island / sandbank / d | `—` | **KEEP** | — |
| featured | 3 | Velana International Airport (Malé) ↔ North & Sout | `e__velana__kurumba-jetty` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Velana International Airport |
| featured | 3 | Malé hub ↔ Ari Atoll / Baa Atoll resorts | `—` | **KEEP** | — |
