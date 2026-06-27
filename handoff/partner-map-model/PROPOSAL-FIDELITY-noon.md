# Proposal fidelity — noon

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-06-27T17:34:02Z

## Summary

- Items audited: 9
- KEEP: 7
- DROP: 0
- DEFER: 1
- TRIM/REWRITE: 1
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-b1ba183aa886` | **TRIM** | geometry_preview: interior_land_km=2.01 (threshold 0.4) |
| journey | — | Vida Beach Resort Umm Al Quwain → Sharjah Waterfro | `rn-02a40748974d` | **KEEP** | — |
| journey | — | Dubai Harbour Marina → Al Khan Lagoon mouth | `gcn-8e3c2d581c-bolt` | **KEEP** | — |
| featured | 1 | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-b1ba183aa886` | **DEFER** | geometry_preview: interior_land_km=2.01 (threshold 0.4) |
| featured | 1 | Vida Beach Resort Umm Al Quwain → Sharjah Waterfro | `rn-02a40748974d` | **KEEP** | — |
| featured | 2 | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **KEEP** | — |
| featured | 2 | Dubai Harbour Marina → Al Khan Lagoon mouth | `gcn-8e3c2d581c-bolt` | **KEEP** | — |
| featured | 3 | Abu Dhabi → Muscat | `edge-0687` | **KEEP** | — |
| featured | 3 | Fujairah → Muscat | `edge-0712` | **KEEP** | — |
