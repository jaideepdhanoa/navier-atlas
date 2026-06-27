# Proposal fidelity — noon

**Verdict:** REWRITE
**Checked:** 2026-06-27T16:00:27Z

## Summary

- Items audited: 18
- KEEP: 5
- DROP: 9
- DEFER: 4
- TRIM/REWRITE: 0
- BP-binding errors: 9

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Yas Marina → Four Seasons Al Maryah Jetty | `rn-f46231fb7baf` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yas Marina' → 'Four Seasons  |
| journey | — | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-9349160e716f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour Marina' → 'Nik |
| journey | — | Fujairah → Khorfakkan Corniche / Port | `rn-bc685bdb0da3` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Fujairah' → 'Khorfakkan Corn |
| journey | — | Ras Al Khaimah → ميناء صيادين غليلة | `rn-501c17b57a72` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ras Al Khaimah' → 'ميناء صيا |
| journey | — | Ushuaïa Dubai Harbour Experience → Marina Mall / B | `gcn-4ae479b872-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ushuaïa Dubai Harbour Experi; geometry_preview: interior_land_km=4.38 (threshold 0.4) |
| journey | — | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **DEFER** | cross_emirate_sanity: 49.8nm cross-emirate framed as everyday commerce |
| featured | 1 | Yas Marina → Four Seasons Al Maryah Jetty | `rn-80c408c085a6` | **DEFER** | geometry_preview: interior_land_km=3.33 (threshold 0.4) |
| featured | 1 | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-b1ba183aa886` | **DEFER** | geometry_preview: interior_land_km=2.01 (threshold 0.4) |
| featured | 1 | Fujairah → Khorfakkan Corniche / Port | `rn-bc685bdb0da3` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Fujairah' → 'Khorfakkan Corn |
| featured | 1 | Ras Al Khaimah → ميناء صيادين غليلة | `rn-d61bc3c848d9` | **DEFER** | geometry_preview: interior_land_km=5.20 (threshold 0.4) |
| featured | 1 | Vida Beach Resort Umm Al Quwain → Sharjah Waterfro | `rn-02a40748974d` | **KEEP** | — |
| featured | 2 | Ushuaïa Dubai Harbour Experience → Marina Mall / B | `gcn-4ae479b872-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ushuaïa Dubai Harbour Experi; geometry_preview: interior_land_km=4.38 (threshold 0.4) |
| featured | 2 | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **KEEP** | — |
| featured | 2 | Dubai Harbour Marina → Al Khan Lagoon mouth | `gcn-8e3c2d581c-bolt` | **KEEP** | — |
| featured | 3 | Abu Dhabi → Muscat | `edge-0687` | **KEEP** | — |
| featured | 3 | Abu Dhabi → Manama | `edge-0685` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Abu Dhabi' → 'Manama' vs rou |
| featured | 3 | Abu Dhabi → Doha | `edge-0684` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Abu Dhabi' → 'Doha' vs route; geometry_preview: interior_land_km=8.43 (threshold 0.4) |
| featured | 3 | Fujairah → Muscat | `edge-0712` | **KEEP** | — |
