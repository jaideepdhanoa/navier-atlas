# Proposal fidelity — abu-dhabi-itc

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:52:42Z

## Summary

- Items audited: 16
- KEEP: 8
- DROP: 6
- DEFER: 2
- TRIM/REWRITE: 0
- BP-binding errors: 6

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Yas Marina → Four Seasons Al Maryah Jetty | `rn-f46231fb7baf` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yas Marina' → 'Four Seasons  |
| journey | — | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-9349160e716f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour Marina' → 'Nik |
| journey | — | Fujairah → Khorfakkan Corniche / Port | `rn-bc685bdb0da3` | **KEEP** | — |
| journey | — | Ras Al Khaimah → ميناء صيادين غليلة | `rn-501c17b57a72` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ras Al Khaimah' → 'ميناء صيا |
| journey | — | Ushuaïa Dubai Harbour Experience → Marina Mall / B | `gcn-4ae479b872-bolt` | **DEFER** | cross_emirate_sanity: 57.4nm cross-emirate framed as everyday commerce |
| journey | — | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **DEFER** | cross_emirate_sanity: 49.8nm cross-emirate framed as everyday commerce |
| featured | 1 | Downtown ↔ Yas Island (events) | `rn-961cdc919083` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Downtown' → 'Yas Island (eve |
| featured | 1 | Yas Marina → Four Seasons Al Maryah Jetty | `rn-80c408c085a6` | **KEEP** | — |
| featured | 2 | Yas Island ↔ Saadiyat cultural district | `rn-d94bb048e34e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yas Island' → 'Saadiyat cult |
| featured | 2 | Abu Dhabi ↔ Sir Bani Yas / Western Region islands | `rn-08f29522c5f2` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Abu Dhabi' → 'Sir Bani Yas / |
| featured | 3 | Abu Dhabi ↔ Ras Al Khaimah | `rn-f50ee8b4d8f7` | **KEEP** | — |
| featured | 3 | Ushuaïa Dubai Harbour Experience → Marina Mall / B | `gcn-4ae479b872-bolt` | **KEEP** | — |
| featured | 4 | Abu Dhabi ↔ Doha | `edge-0684` | **KEEP** | — |
| featured | 4 | Abu Dhabi ↔ Manama | `edge-0685` | **KEEP** | — |
| featured | 4 | Abu Dhabi ↔ Muscat | `edge-0687` | **KEEP** | — |
| featured | 4 | Fujairah → Muscat | `edge-0712` | **KEEP** | — |
