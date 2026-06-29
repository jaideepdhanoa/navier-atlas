# Proposal fidelity — rakta

**Verdict:** REWRITE
**Checked:** 2026-06-29T12:19:00Z

## Summary

- Items audited: 49
- KEEP: 45
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 3

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | RAK Harbour / Corniche → Al Marjan and Mina Al Ara | `rn-0d9b2acf81b1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'RAK Harbour / Corniche' → 'A |
| journey | — | Dubai Harbour → Wynn Al Marjan Island | `rn-cf6a87b5e146` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour' → 'Wynn Al Ma |
| journey | — | RAK / UAE → Musandam, Muscat, Doha, Bahrain | `rn-e520b4e228e8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'RAK / UAE' → 'Musandam, Musc |
| featured | 1 | Al Marjan Island public arrival marina → Rixos Bab | `rn-f0d6b20a125c` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah Harbour → RAK Corniche public pier | `rn-2a5c2fe11732` | **KEEP** | — |
| featured | 1 | Marjan Island Resort & Spa beach jetty → Hampton b | `rn-67316de45b8f` | **KEEP** | — |
| featured | 1 | Wynn Al Marjan Island arrival lagoon → Marjan Isla | `rn-0bdf53c78a31` | **KEEP** | — |
| featured | 1 | Anantara Mina Al Arab Ras Al Khaimah Resort jetty  | `rn-259c74613206` | **KEEP** | — |
| featured | 1 | Al Hamra Marina & Royal Yacht Club RAK → Waldorf A | `rn-f6d21c86c4d0` | **KEEP** | — |
| featured | 1 | Al Marjan Island public arrival marina → Hampton b | `rn-f7356e7a6fb3` | **KEEP** | — |
| featured | 1 | Mina Al Arab marina / lagoon basin → InterContinen | `rn-1ad18654169b` | **KEEP** | — |
| featured | 1 | Anantara Mina Al Arab Ras Al Khaimah Resort jetty  | `rn-239a65d9ff67` | **KEEP** | — |
| featured | 1 | Rixos Bab Al Bahr beach jetty → Hampton by Hilton  | `rn-4f0d97b8a3ed` | **KEEP** | — |
| featured | 1 | Wynn Al Marjan Island arrival lagoon → Hampton by  | `rn-cf6a87b5e146` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah Harbour → Hilton Garden Inn Ras Al  | `rn-ea8ffe092848` | **KEEP** | — |
| featured | 1 | Hilton Garden Inn Ras Al Khaimah (Corniche) jetty  | `rn-c35ab68f5b90` | **KEEP** | — |
| featured | 1 | Bin Majid Beach Resort jetty → Acacia by Bin Majid | `rn-f1870f49bf3e` | **KEEP** | — |
| featured | 1 | Raksa → Ras Al Khaimah Harbour | `rn-45de8febe019` | **KEEP** | — |
| featured | 1 | Sha'am Fishing Boat Harbour → Sha'am coastal stagi | `rn-610b1a3bb4db` | **KEEP** | — |
| featured | 1 | The Cove Rotana Resort jetty → Anantara Mina Al Ar | `rn-fc522269661a` | **KEEP** | — |
| featured | 1 | ميناء صيادين غليلة → Sha'am Fishing Boat Harbour | `rn-e54d51128055` | **KEEP** | — |
| featured | 1 | ميناء صيادين غليلة → ميناء صيادين خورخوير | `rn-501c17b57a72` | **KEEP** | — |
| featured | 1 | Acacia by Bin Majid jetty → The Cove Rotana Resort | `rn-c861bfe0ceb6` | **KEEP** | — |
| featured | 1 | Raksa → Hilton Garden Inn Ras Al Khaimah (Corniche | `rn-0fecef31458f` | **KEEP** | — |
| featured | 1 | Bin Majid Beach Resort jetty → The Cove Rotana Res | `rn-86d55b7a87a5` | **KEEP** | — |
| featured | 1 | Sha'am coastal staging point → ميناء صيادين غليلة | `rn-75773e5540dc` | **KEEP** | — |
| featured | 1 | ميناء صيادين خورخوير → Sha'am Fishing Boat Harbour | `rn-d4e4d1a279ed` | **KEEP** | — |
| featured | 1 | UAQ Marine Club → Rixos Bab Al Bahr beach jetty | `rn-8570d8c24098` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah → ميناء صيادين غليلة | `rn-d61bc3c848d9` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah → Al Hamra Marina & Royal Yacht Clu | `rn-80cfe59d2d79` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah → Al Marjan Island public arrival m | `rn-482b047f5a66` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah → UAQ Marine Club | `rn-7ef1b64eebe0` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah → Ajman Marina | `rn-dacbbff1792e` | **KEEP** | — |
| featured | 1 | Ras Al Khaimah → Dubai Islands Marina | `rn-8bc1e153cdc4` | **DROP** | phase_narrative_fit: Phase 1 beachhead but 50nm leg |
| featured | 1 | Al Zorah Marina 1 → Ajman Marina | `rn-11d3a0b9153a` | **KEEP** | — |
| featured | 1 | Daba Port → Dibba Al-Hisn Marina - Sharjah | `rn-86890f46f3a5` | **KEEP** | — |
| featured | 1 | Al Zorah Marina 1 → Hamriyah Port Main Harbour | `rn-bcf9fd99ef5a` | **KEEP** | — |
| featured | 1 | Ajman Marina → Hamriyah Port Main Harbour | `rn-a68b658bd154` | **KEEP** | — |
| featured | 1 | Zighy Marina → Dibba Al-Hisn Marina - Sharjah | `rn-2494f5a9242d` | **KEEP** | — |
| featured | 1 | UAQ Marine Club → Hamriyah Port Main Harbour | `rn-2d00ee6cdb3e` | **KEEP** | — |
| featured | 1 | Gumda Fishing Harbour → Sha'am coastal staging poi | `rn-dfb7c3fcf0e4` | **KEEP** | — |
| featured | 1 | Gumda Fishing Harbour → Sha'am Fishing Boat Harbou | `rn-73cfebcabacd` | **KEEP** | — |
| featured | 2 | Dubai Harbour Marina → Wynn Al Marjan Island arriv | `gcn-9e515da38a-bolt` | **KEEP** | — |
| featured | 2 | Ras Al Khaimah → Abu Dhabi | `rn-e70860f21af3` | **KEEP** | — |
| featured | 2 | Ras Al Khaimah → Sharjah | `rn-46bf5bf09b13` | **KEEP** | — |
| featured | 2 | Ras Al Khaimah → Fujairah | `rn-5bac21e43fcb` | **KEEP** | — |
| featured | 3 | Ras Al Khaimah → Muscat | `edge-0772` | **KEEP** | — |
| featured | 3 | Ras Al Khaimah → Doha | `edge-0773` | **KEEP** | — |
| featured | 3 | Ras Al Khaimah → Manama | `edge-0774` | **KEEP** | — |
