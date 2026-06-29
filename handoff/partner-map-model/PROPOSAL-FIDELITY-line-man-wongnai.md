# Proposal fidelity — line-man-wongnai

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:36Z

## Summary

- Items audited: 44
- KEEP: 41
- DROP: 3
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 3

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| featured | 1 | Bophut / Fisherman's Village Jetty → Maenam Pier | `rn-0e850c291876` | **KEEP** | — |
| featured | 2 | Sathorn (Central) Pier → Phra Athit Pier (Khao San | `—` | **KEEP** | — |
| featured | 3 | Bophut / Fisherman's Village Jetty → Maenam Pier | `rn-0e850c291876` | **KEEP** | — |
| journey | market:koh_samui_gulf | Raja Ferry Lipa Noi Pier (Koh Samui) → Raja Ferry  | `rn-347c44e1d360` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Raja Ferry Lipa Noi Pier (Ko |
| journey | market:koh_samui_gulf | Koh Phangan → Thong Sala Pier (Koh Phangan main) | `rn-db5e83248f9d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Koh Phangan' → 'Thong Sala P |
| journey | market:koh_samui_gulf | Koh Phangan → Don Sak Ferry Harbour (Surat Thani m | `—` | **KEEP** | — |
| journey | market:koh_samui_gulf | Koh Phangan → Mae Haad Pier (Koh Tao main) | `rn-21d437d2bf84` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Koh Phangan' → 'Mae Haad Pie |
| featured | koh_samui_gulf/p1 | Raja Ferry Lipa Noi Pier (Koh Samui) → Raja Ferry  | `ics-5038f54700` | **KEEP** | — |
| featured | koh_samui_gulf/p1 | Koh Phangan → Thong Sala Pier (Koh Phangan main) | `—` | **KEEP** | — |
| featured | koh_samui_gulf/p1 | Koh Phangan → Don Sak Ferry Harbour (Surat Thani m | `—` | **KEEP** | — |
| featured | koh_samui_gulf/p2 | Koh Phangan → Mae Haad Pier (Koh Tao main) | `—` | **KEEP** | — |
| featured | koh_samui_gulf/p3 | Bophut / Fisherman's Village Jetty → Maenam Pier | `rn-0e850c291876` | **KEEP** | — |
| featured | koh_samui_gulf/p3 | Nathon Pier → Bangrak (Big Buddha) Pier | `rn-f2ca85cdc57b` | **KEEP** | — |
| featured | koh_samui_gulf/p3 | Maenam Pier → Thong Sala Pier | `rn-4cc25e9c8dba` | **KEEP** | — |
| journey | market:phuket_andaman | phuket-phang-nga-thailand__phuket → koh-lanta-thai | `rn-01a8c29df66a` | **KEEP** | — |
| journey | market:phuket_andaman | Phuket → Krabi (Ao Nang) | `gcn-e927fe8958-shared` | **KEEP** | — |
| journey | market:phuket_andaman | phuket-phang-nga-thailand__phuket → koh-lanta-thai | `rn-01a8c29df66a` | **KEEP** | — |
| journey | market:phuket_andaman | phuket-phang-nga-thailand__phuket → koh-lanta-thai | `rn-01a8c29df66a` | **KEEP** | — |
| featured | phuket_andaman/p1 | phuket-phang-nga-thailand__phuket → koh-lanta-thai | `rn-01a8c29df66a` | **KEEP** | — |
| featured | phuket_andaman/p2 | Ao Nang / Nopparat Thara Pier → Railay East Pier | `—` | **KEEP** | — |
| featured | phuket_andaman/p3 | Khong Kha Pier (Chao Fa) → Klong Jilad Pier | `—` | **KEEP** | — |
| journey | market:bangkok | ICONSIAM Pier (Chao Phraya) → ICONSIAM Pier (Chao  | `—` | **KEEP** | — |
| journey | market:bangkok | Sathorn (Central) Pier → Phra Arthit Pier | `gcn-e299366426-shared` | **KEEP** | — |
| journey | market:bangkok | Bangkok (Gulf mouth) → Pattaya (Bali Hai Pier) | `rn-dcbcbe8bfb4f` | **KEEP** | — |
| journey | market:bangkok | Bali Hai Pier → Na Ban Pier (Koh Larn) | `rn-f09e06bc2910` | **KEEP** | — |
| featured | bangkok/p1 | bangkok-thailand → bangkok-thailand | `—` | **KEEP** | — |
| featured | bangkok/p1 | Sathorn (Central) Pier → Phra Athit Pier (Khao San | `rn-787957da1609` | **KEEP** | — |
| featured | bangkok/p2 | Bali Hai Pier → Na Ban Pier (Koh Larn) | `rn-f09e06bc2910` | **KEEP** | — |
| featured | bangkok/p2 | bangkok-thailand → bangkok-thailand | `—` | **KEEP** | — |
| featured | bangkok/p3 | Bangkok → Pattaya | `rn-dcbcbe8bfb4f` | **KEEP** | — |
| journey | market:eastern_seaboard | Bangkok (Gulf mouth) → Pattaya (Bali Hai Pier) | `rn-dcbcbe8bfb4f` | **KEEP** | — |
| journey | market:eastern_seaboard | Bali Hai Pier → Na Ban Pier (Koh Larn) | `rn-f09e06bc2910` | **KEEP** | — |
| journey | market:eastern_seaboard | Pattaya (Bali Hai Pier) → Koh Samet (Na Dan Pier) | `rn-4a3b9db3cda5` | **KEEP** | — |
| journey | market:eastern_seaboard | Pattaya → Koh Samet | `rn-4a3b9db3cda5` | **KEEP** | — |
| featured | eastern_seaboard/p1 | Bali Hai Pier → Na Ban Pier (Koh Larn) | `rn-f09e06bc2910` | **KEEP** | — |
| featured | eastern_seaboard/p2 | Bangkok → Pattaya | `rn-dcbcbe8bfb4f` | **KEEP** | — |
| featured | eastern_seaboard/p2 | Pattaya → Koh Samet | `rn-4a3b9db3cda5` | **KEEP** | — |
| featured | eastern_seaboard/p3 | koh-samet-thailand → koh-samet-thailand | `—` | **KEEP** | — |
| journey | market:royal_coast | Hua Hin → Pattaya | `rn-9c2bce5bffd0` | **KEEP** | — |
| journey | market:royal_coast | Hua Hin → Cha-Am | `rn-7512bdcf3d4c` | **KEEP** | — |
| journey | market:royal_coast | Bangkok → Hua Hin | `rn-01f164a3d43c` | **KEEP** | — |
| featured | royal_coast/p1 | Hua Hin → Cha-Am | `rn-7512bdcf3d4c` | **KEEP** | — |
| featured | royal_coast/p2 | Hua Hin → Pattaya | `rn-9c2bce5bffd0` | **KEEP** | — |
| featured | royal_coast/p3 | Hua Hin → Pattaya | `rn-9c2bce5bffd0` | **KEEP** | — |
