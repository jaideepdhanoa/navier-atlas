# Proposal fidelity — careem

**Verdict:** PASS
**Checked:** 2026-07-02T19:35:40Z

## Summary

- Items audited: 9
- KEEP: 9
- DROP: 0
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-b1ba183aa886` | **KEEP** | — |
| journey | — | Vida Beach Resort Umm Al Quwain → Sharjah Waterfro | `rn-02a40748974d` | **KEEP** | — |
| journey | — | Dubai Harbour Marina → Al Khan Lagoon mouth | `gcn-8e3c2d581c-bolt` | **KEEP** | — |
| featured | 1 | Dubai Harbour Marina → Nikki Beach Resort Pearl Ju | `rn-b1ba183aa886` | **KEEP** | — |
| featured | 1 | Vida Beach Resort Umm Al Quwain → Sharjah Waterfro | `rn-02a40748974d` | **KEEP** | — |
| featured | 1 | Dubai Harbour Marina → Al Khan Lagoon mouth | `gcn-8e3c2d581c-bolt` | **KEEP** | — |
| featured | 2 | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **KEEP** | — |
| featured | 3 | Abu Dhabi → Muscat | `—` | **KEEP** | — |
| featured | 3 | Fujairah → Muscat | `—` | **KEEP** | — |

## Careem Phase 1 target keep set (post-trim)

**journeys_unlocked (≤4):**
- Dubai Harbour Marina → Nikki Beach Resort Pearl Jumeirah Jetty (`rn-b1ba183aa886`)
- Fujairah east-coast cluster → Dibba · Khor Fakkan · Kalba (`gcn-8f0d49bbde-careem` / `rn-bc685bdb0da3`)
- Ushuaïa Dubai Harbour → Marina Mall / Breakwater Marina — **defer to Phase 2** (not hub journeys)

**Phase 1 featured_routes (≤3, Dubai beachhead):**
- KEEP: Dubai Harbour Marina → Nikki Beach (`rn-b1ba183aa886`)
- KEEP: Vida Beach Resort UAQ → Sharjah Waterfront City marina (`rn-02a40748974d`) — Sharjah/Dubai adjacency
- DROP: Yas Marina → Four Seasons (Abu Dhabi; not beachhead)
- DROP: Fujairah → Khorfakkan (east coast; defer Phase 3)
- DROP: RAK → Ghallilah (RAK; phase-narrative misfit + 5.2km land)

**DROP from journeys_unlocked:**
- Yas Marina → Four Seasons (`rn-f46231fb7baf` binds Bahrain BP pair)
- RAK → Ghallilah (wrong endpoint pair on route)
- Dubai Harbour → Nikki Beach (`gcn-6a2841d6db-careem` — Anantara World Islands leak)
