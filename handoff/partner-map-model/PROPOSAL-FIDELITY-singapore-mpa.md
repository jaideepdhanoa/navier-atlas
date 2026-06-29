# Proposal fidelity — singapore-mpa

**Verdict:** REWRITE
**Checked:** 2026-06-29T12:19:01Z

## Summary

- Items audited: 13
- KEEP: 5
- DROP: 8
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 8

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Marina Bay / CBD → Sentosa & the Southern Islands | `rn-e486603e53a8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay / CBD' → 'Sentosa; inheritance_debt: inherited link via grok/relink_partner_journeys/scoped |
| journey | — | Singapore (Tanah Merah) → Bintan — Lagoi resorts ( | `rn-f3670ea7d99b` | **KEEP** | — |
| journey | — | Singapore (Tanah Merah / East Coast) → Desaru Coas | `rn-5d1a30fbb0a9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore (Tanah Merah / Eas; inheritance_debt: _inherit_source=grok/normalize/grab |
| journey | — | Bali (Sanur / Benoa) → Lombok & the Gilis | `rn-c001edd855aa` | **KEEP** | — |
| journey | — | Phuket → Langkawi (via the Andaman) | `rn-853cbe7dd006` | **KEEP** | — |
| journey | — | Manila CBD (Makati / BGC) → Manila Bay & Cavite | `rn-b109322aa1e9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manila CBD (Makati / BGC)' → |
| featured | 1 | Bedok Jetty (East Coast Park) → Marina Bay Water T | `—` | **KEEP** | — |
| featured | 1 | Marina Bay / CBD ↔ Sentosa & the Southern Islands | `rn-e486603e53a8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay / CBD' → 'Sentosa |
| featured | 1 | Marina Bay ↔ Changi Point / Pulau Ubin | `rn-e94c308a28e3` | **KEEP** | — |
| featured | 2 | Jurong / western harbour ↔ Marina Bay / CBD | `rn-55f72072dd69` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Jurong / western harbour' →  |
| featured | 2 | Marina Bay ↔ Sentosa / southern islands | `rn-76264638fa6b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay' → 'Sentosa / sou |
| featured | 3 | Singapore / Desaru ↔ East-coast Malaysia & outer R | `rn-5d1a30fbb0a9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore / Desaru' → 'East- |
| featured | 4 | Singapore (Tanah Merah) ↔ Batam / Bintan | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore (Tanah Merah)' → ' |
