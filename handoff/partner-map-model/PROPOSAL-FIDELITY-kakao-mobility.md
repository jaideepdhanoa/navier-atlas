# Proposal fidelity — kakao-mobility

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:14:06Z

## Summary

- Items audited: 38
- KEEP: 31
- DROP: 7
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 7

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Gimpo / Yeouido → Jamsil / Ttukseom | `—` | **KEEP** | — |
| journey | — | Busan → Busan/Geoje Cluster | `ics-00024a3bd3` | **KEEP** | — |
| journey | — | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| journey | — | Seongsan Eup → Seopjikoji | `ics-58f34f8676` | **KEEP** | — |
| featured | 1 | Busan → Busan/Geoje Cluster | `ics-00024a3bd3` | **KEEP** | — |
| featured | 2 | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| featured | 4 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `ics-843b41b72d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yeosu / Tongyeong (Hallyeoha |
| featured | 4 | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| journey | market:busan | Haeundae (Mipo Harbour) → Gwangalli / Marine City | `—` | **KEEP** | — |
| journey | market:busan | Busan / Geoje → Busan / Geoje / Hallyeo, Korea | `ics-ed8db10726` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Busan / Geoje' → 'Busan / Ge |
| journey | market:busan | Busan / Geoje → Jeju | `rn-6786317ef18f` | **KEEP** | — |
| journey | market:busan | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| featured | busan/p1 | Haeundae ↔ Gwangalli / Marine City | `—` | **KEEP** | — |
| featured | busan/p1 | Nampo ↔ Oryukdo / Songdo / Yeongdo loop | `—` | **KEEP** | — |
| featured | busan/p2 | Busan → Busan/Geoje Cluster | `ics-00024a3bd3` | **KEEP** | — |
| featured | busan/p3 | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| journey | market:jeju | Seongsan Port → Udo (Cow Island) | `—` | **KEEP** | — |
| journey | market:jeju | Moseulpo Port → Marado / Gapado | `—` | **KEEP** | — |
| journey | market:jeju | Hallim Port → Biyangdo | `—` | **KEEP** | — |
| journey | market:jeju | Busan / Geoje → Jeju | `rn-6786317ef18f` | **KEEP** | — |
| featured | jeju/p1 | Seongsan Eup → Seopjikoji | `ics-58f34f8676` | **KEEP** | — |
| featured | jeju/p1 | Moseulpo ↔ Marado / Gapado | `—` | **KEEP** | — |
| featured | jeju/p2 | Jeju → Seogwipo Jungmun | `ics-dc7202dc23` | **KEEP** | — |
| featured | jeju/p3 | Busan / Geoje → Jeju | `rn-6786317ef18f` | **KEEP** | — |
| journey | market:yeosu-tongyeong | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `ics-2b5e1073dc` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yeosu / Tongyeong (Hallyeoha |
| journey | market:yeosu-tongyeong | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `ics-843b41b72d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yeosu / Tongyeong (Hallyeoha |
| journey | market:yeosu-tongyeong | Yeosu → Tongyeong | `ics-2b5e1073dc` | **KEEP** | — |
| journey | market:yeosu-tongyeong | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `ics-ffeada3079` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yeosu / Tongyeong (Hallyeoha |
| featured | yeosu-tongyeong/p1 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `ics-2b5e1073dc` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yeosu / Tongyeong (Hallyeoha |
| featured | yeosu-tongyeong/p2 | Yeosu ↔ Geumodo / Geomundo | `—` | **KEEP** | — |
| featured | yeosu-tongyeong/p3 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `ics-843b41b72d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yeosu / Tongyeong (Hallyeoha |
| journey | market:seoul-han-river | Gimpo / Yeouido → Jamsil / Ttukseom | `—` | **KEEP** | — |
| journey | market:seoul-han-river | Yeouido → Seoul Forest / Ttukseom | `—` | **KEEP** | — |
| journey | market:seoul-han-river | Incheon → Muuido / Yeongjong (West Sea islands) | `—` | **KEEP** | — |
| journey | market:seoul-han-river | Han River (Yeouido) → Incheon Bay | `—` | **KEEP** | — |
| featured | seoul-han-river/p1 | Gimpo / Yeouido ↔ Jamsil / Ttukseom | `—` | **KEEP** | — |
| featured | seoul-han-river/p2 | Incheon → Muuido / Yeongjong | `ics-6f074085c9` | **KEEP** | — |
| featured | seoul-han-river/p3 | Han River (Yeouido) ↔ Incheon Bay | `—` | **KEEP** | — |
