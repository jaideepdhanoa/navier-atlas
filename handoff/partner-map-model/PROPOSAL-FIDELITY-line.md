# Proposal fidelity — line

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:14:07Z

## Summary

- Items audited: 25
- KEEP: 16
- DROP: 9
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 9

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Gimpo / Yeouido → Jamsil / Ttukseom | `—` | **KEEP** | — |
| journey | — | Busan → Busan/Geoje Cluster | `ics-00024a3bd3` | **KEEP** | — |
| journey | — | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| journey | — | Rassada Pier (Phuket Deep Sea Port) → Manoh Pier ( | `rn-830bd4d377ca` | **KEEP** | — |
| featured | 1 | Busan → Busan/Geoje Cluster | `ics-00024a3bd3` | **KEEP** | — |
| featured | 2 | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| featured | 4 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `ics-843b41b72d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Yeosu / Tongyeong (Hallyeoha |
| featured | 4 | Busan / Geoje → Fukuoka (Hakata) | `rn-e44147de575d` | **KEEP** | — |
| journey | market:japan | Setouchi (Naoshima / Teshima Inland Sea) → Setouch | `ics-987e1b9cc7` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Setouchi (Naoshima / Teshima |
| journey | market:japan | Hiroshima / Miyajimaguchi → Miyajima (Itsukushima) | `—` | **KEEP** | — |
| journey | market:japan | Tokyo Bay (Tokyo–Yokohama) → Tokyo Bay | `ics-0be05f213b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Tokyo Bay (Tokyo–Yokohama)'  |
| featured | japan/p1 | Takamatsu ↔ Naoshima | `—` | **KEEP** | — |
| featured | japan/p2 | Hiroshima ↔ Miyajima | `—` | **KEEP** | — |
| featured | japan/p3 | Tokyo Bay (Tokyo–Yokohama) → Tokyo Bay | `ics-e6e369b77c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Tokyo Bay (Tokyo–Yokohama)'  |
| journey | market:taiwan | Kaohsiung harbour → Cijin Island | `—` | **KEEP** | — |
| journey | market:taiwan | Donggang → Xiaoliuqiu (Liuqiu) | `ics-91951379c0` | **KEEP** | — |
| journey | market:taiwan | Magong South Sea Visitor Center / Magong Harbour ( | `ics-25ecef3e3b` | **KEEP** | — |
| featured | taiwan/p1 | Kaohsiung ↔ Cijin | `—` | **KEEP** | — |
| featured | taiwan/p2 | Magong South Sea Visitor Center / Magong Harbour ( | `ics-25ecef3e3b` | **KEEP** | — |
| journey | market:thailand | Krabi → Nonthasak Marine | `rn-4e06ca55ff7a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Krabi' → 'Nonthasak Marine'  |
| journey | market:thailand | Krabi → Marina Seaview Krabi | `rn-759caec9f963` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Krabi' → 'Marina Seaview Kra |
| journey | market:thailand | Koh Phangan → Thong Sala Pier (Koh Phangan main) | `rn-db5e83248f9d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Koh Phangan' → 'Thong Sala P |
| featured | thailand/p1 | Koh Phangan ↔ Thong Sala Pier (Koh Phangan main) | `rn-db5e83248f9d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Koh Phangan' → 'Thong Sala P |
| featured | thailand/p2 | Banyan Tree Krabi → Koh Phi Phi Tour Pier | `rn-41b28873ff52` | **KEEP** | — |
| featured | thailand/p3 | Koh Phangan → Thong Sala Pier (Koh Phangan main) | `rn-db5e83248f9d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Koh Phangan' → 'Thong Sala P |
