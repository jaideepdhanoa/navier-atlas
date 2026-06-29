# Proposal fidelity — singapore-mpa

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:14:15Z

## Summary

- Items audited: 11
- KEEP: 3
- DROP: 8
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 8

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Marina Bay / CBD → Sentosa & the Southern Islands | `rn-e486603e53a8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay / CBD' → 'Sentosa; distance_honesty: card 11.2nm vs route 29.1nm (62% delta) (+1) |
| journey | — | Singapore (Tanah Merah) → Bintan — Lagoi resorts ( | `rn-f3670ea7d99b` | **KEEP** | — |
| journey | — | Singapore (Tanah Merah / East Coast) → Desaru Coas | `rn-5d1a30fbb0a9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore (Tanah Merah / Eas |
| journey | — | Bali (Sanur / Benoa) → Lombok & the Gilis | `—` | **KEEP** | — |
| featured | 1 | Bedok Jetty (East Coast Park) → Marina Bay Water T | `—` | **KEEP** | — |
| featured | 1 | Marina Bay / CBD ↔ Sentosa & the Southern Islands | `rn-e486603e53a8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay / CBD' → 'Sentosa; distance_honesty: card 11.2nm vs route 29.1nm (62% delta) |
| featured | 1 | Marina Bay ↔ Changi Point / Pulau Ubin | `rn-ea2233879811` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay' → 'Changi Point ; distance_honesty: card 14.2nm vs route 3.8nm (274% delta) |
| featured | 2 | Jurong / western harbour ↔ Marina Bay / CBD | `rn-55f72072dd69` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Jurong / western harbour' →  |
| featured | 2 | Marina Bay ↔ Sentosa / southern islands | `rn-76264638fa6b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay' → 'Sentosa / sou |
| featured | 3 | Singapore / Desaru ↔ East-coast Malaysia & outer R | `rn-5d1a30fbb0a9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore / Desaru' → 'East- |
| featured | 4 | Singapore (Tanah Merah) ↔ Batam / Bintan | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore (Tanah Merah)' → ' |
