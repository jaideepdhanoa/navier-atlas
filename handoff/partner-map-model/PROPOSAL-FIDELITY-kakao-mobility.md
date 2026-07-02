# Proposal fidelity — kakao-mobility

**Verdict:** TRIM
**Checked:** 2026-07-02T19:35:41Z

## Summary

- Items audited: 38
- KEEP: 37
- DROP: 1
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 1

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Gimpo / Yeouido → Jamsil / Ttukseom | `—` | **KEEP** | — |
| journey | — | Busan → Busan/Geoje Cluster | `—` | **KEEP** | — |
| journey | — | Busan / Geoje → Fukuoka (Hakata) | `—` | **KEEP** | — |
| journey | — | Seongsan Eup → Seopjikoji | `—` | **KEEP** | — |
| featured | 1 | Busan → Busan/Geoje Cluster | `—` | **KEEP** | — |
| featured | 2 | Busan / Geoje → Fukuoka (Hakata) | `—` | **KEEP** | — |
| featured | 4 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `—` | **KEEP** | — |
| featured | 4 | Busan / Geoje → Fukuoka (Hakata) | `—` | **KEEP** | — |
| journey | market:busan | Haeundae (Mipo Harbour) → Gwangalli / Marine City | `—` | **KEEP** | — |
| journey | market:busan | Busan / Geoje → Busan / Geoje / Hallyeo, Korea | `—` | **KEEP** | — |
| journey | market:busan | Busan / Geoje → Jeju | `—` | **KEEP** | — |
| journey | market:busan | Busan / Geoje → Fukuoka (Hakata) | `—` | **KEEP** | — |
| featured | busan/p1 | Haeundae ↔ Gwangalli / Marine City | `—` | **KEEP** | — |
| featured | busan/p1 | Nampo ↔ Oryukdo / Songdo / Yeongdo loop | `—` | **KEEP** | — |
| featured | busan/p2 | Busan → Busan/Geoje Cluster | `—` | **KEEP** | — |
| featured | busan/p3 | Busan / Geoje → Fukuoka (Hakata) | `—` | **KEEP** | — |
| journey | market:jeju | Seongsan Port → Udo (Cow Island) | `—` | **KEEP** | — |
| journey | market:jeju | Moseulpo Port → Marado / Gapado | `—` | **KEEP** | — |
| journey | market:jeju | Hallim Port → Biyangdo | `—` | **KEEP** | — |
| journey | market:jeju | Busan / Geoje → Jeju | `—` | **KEEP** | — |
| featured | jeju/p1 | Seongsan Eup → Seopjikoji | `—` | **KEEP** | — |
| featured | jeju/p1 | Moseulpo ↔ Marado / Gapado | `—` | **KEEP** | — |
| featured | jeju/p2 | Jeju → Seogwipo Jungmun | `—` | **KEEP** | — |
| featured | jeju/p3 | Busan / Geoje → Jeju | `—` | **KEEP** | — |
| journey | market:yeosu-tongyeong | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `—` | **KEEP** | — |
| journey | market:yeosu-tongyeong | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `—` | **KEEP** | — |
| journey | market:yeosu-tongyeong | Yeosu → Tongyeong | `—` | **KEEP** | — |
| journey | market:yeosu-tongyeong | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `—` | **KEEP** | — |
| featured | yeosu-tongyeong/p1 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `—` | **KEEP** | — |
| featured | yeosu-tongyeong/p2 | Yeosu ↔ Geumodo / Geomundo | `—` | **KEEP** | — |
| featured | yeosu-tongyeong/p3 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `—` | **KEEP** | — |
| journey | market:seoul-han-river | Gimpo Ara Marina → Jamsil Ttukseom Riverside Pier | `rn-806c3d8d2fe9` | **KEEP** | — |
| journey | market:seoul-han-river | Yeouido Hangang Park Pier → Ttukseom Hangang Park  | `rn-bca95ab1f7cf` | **KEEP** | — |
| journey | market:seoul-han-river | Incheon Coastal Passenger Terminal → Muuido Island | `rn-62345e60f1a1` | **KEEP** | — |
| journey | market:seoul-han-river | Yeouido Hangang Park Pier → Incheon Coastal Passen | `rn-3f7b5af983cd` | **KEEP** | — |
| featured | seoul-han-river/p1 | Gimpo Ara Marina ↔ Jamsil Ttukseom Riverside Pier | `rn-806c3d8d2fe9` | **KEEP** | — |
| featured | seoul-han-river/p2 | Incheon → Muuido / Yeongjong | `rn-62345e60f1a1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Incheon' → 'Muuido / Yeongjo |
| featured | seoul-han-river/p3 | Yeouido Hangang Park Pier ↔ Incheon Coastal Passen | `rn-3f7b5af983cd` | **KEEP** | — |
