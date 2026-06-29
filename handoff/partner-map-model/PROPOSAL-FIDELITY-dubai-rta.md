# Proposal fidelity — dubai-rta

**Verdict:** REWRITE
**Checked:** 2026-06-29T14:52:50Z

## Summary

- Items audited: 19
- KEEP: 9
- DROP: 9
- DEFER: 1
- TRIM/REWRITE: 0
- BP-binding errors: 8

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Yas Marina → Four Seasons Al Maryah Jetty | `rn-f46231fb7baf` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yas Marina' → 'Four Seasons  |
| journey | — | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-9349160e716f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour Marina' → 'Nik |
| journey | — | Dubai → Fujairah (east coast) | `rn-5bac21e43fcb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai' → 'Fujairah (east coa; inheritance_debt: _inherit_source=grok/normalize/noon |
| journey | — | Ras Al Khaimah → ميناء صيادين غليلة | `rn-501c17b57a72` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ras Al Khaimah' → 'ميناء صيا |
| journey | — | Ushuaïa Dubai Harbour Experience → Marina Mall / B | `gcn-4ae479b872-bolt` | **DEFER** | cross_emirate_sanity: 57.4nm cross-emirate framed as everyday commerce |
| journey | — | Dubai → Ras Al Khaimah (northern emirates) | `gcn-9e515da38a-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai' → 'Ras Al Khaimah (no; inheritance_debt: _inherit_source=grok/normalize/noon |
| featured | 1 | Dubai Marina / Harbour ↔ Palm Jumeirah / Dubai Isl | `rn-42aa1791bb60` | **DROP** | phase_narrative_fit: Phase 1 Dubai beachhead but route cities ['dubai-uae__palm-j |
| featured | 1 | Dubai Creek ↔ Dubai Marina | `rn-96ac70c9ebf8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Creek' → 'Dubai Marina |
| featured | 2 | Dubai Creek ↔ Dubai Harbour / Bluewaters | `rn-b1ba183aa886` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Creek' → 'Dubai Harbou |
| featured | 3 | Dubai ↔ Abu Dhabi waterfront | `rn-25065af2bcb4` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai' → 'Abu Dhabi waterfro |
| featured | 3 | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **KEEP** | — |
| featured | 3 | Dubai Harbour Marina → Al Khan Lagoon mouth | `gcn-8e3c2d581c-bolt` | **KEEP** | — |
| featured | 4 | Dubai ↔ Doha | `edge__dubai-uae__doha-qatar` | **KEEP** | — |
| featured | 4 | Dubai ↔ Manama | `edge-0705` | **KEEP** | — |
| featured | 4 | Dubai ↔ Muscat | `edge-0703` | **KEEP** | — |
| featured | 4 | Abu Dhabi → Muscat | `edge-0687` | **KEEP** | — |
| featured | 4 | Abu Dhabi → Manama | `edge-0685` | **KEEP** | — |
| featured | 4 | Abu Dhabi → Doha | `edge-0684` | **KEEP** | — |
| featured | 4 | Fujairah → Muscat | `edge-0712` | **KEEP** | — |
