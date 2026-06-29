# Proposal fidelity — qatar

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:53:31Z

## Summary

- Items audited: 10
- KEEP: 4
- DROP: 4
- DEFER: 2
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Yas Marina → Four Seasons Al Maryah Jetty | `rn-80c408c085a6` | **KEEP** | — |
| journey | — | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-9349160e716f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour Marina' → 'Nik |
| journey | — | Fujairah → Khorfakkan Corniche / Port | `rn-bc685bdb0da3` | **KEEP** | — |
| journey | — | Ras Al Khaimah → ميناء صيادين غليلة | `rn-501c17b57a72` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ras Al Khaimah' → 'ميناء صيا |
| journey | — | Ushuaïa Dubai Harbour Experience → Marina Mall / B | `gcn-4ae479b872-bolt` | **DEFER** | cross_emirate_sanity: 57.4nm cross-emirate framed as everyday commerce |
| journey | — | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **DEFER** | cross_emirate_sanity: 49.8nm cross-emirate framed as everyday commerce |
| featured | 1 | Dubai Harbour Marina ↔ Nikki Beach Resort Pearl Ju | `rn-9349160e716f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour Marina' → 'Nik |
| featured | 2 | Ras Al Khaimah ↔ ميناء صيادين غليلة | `rn-501c17b57a72` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ras Al Khaimah' → 'ميناء صيا |
| featured | 3 | cross-border business travel | `—` | **KEEP** | — |
| featured | 4 | Fujairah ↔ Khorfakkan Corniche / Port | `rn-bc685bdb0da3` | **KEEP** | — |
