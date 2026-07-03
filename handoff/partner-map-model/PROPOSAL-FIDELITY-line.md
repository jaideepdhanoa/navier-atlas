# Proposal fidelity — line

**Verdict:** TRIM
**Checked:** 2026-07-03T02:54:02Z

## Summary

- Items audited: 25
- KEEP: 24
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
| journey | — | Rassada Pier (Phuket Deep Sea Port) → Manoh Pier ( | `rn-830bd4d377ca` | **KEEP** | — |
| featured | 1 | Busan → Busan/Geoje Cluster | `—` | **KEEP** | — |
| featured | 2 | Busan / Geoje → Fukuoka (Hakata) | `—` | **KEEP** | — |
| featured | 4 | Yeosu / Tongyeong (Hallyeohaesang) → Yeosu / Tongy | `—` | **KEEP** | — |
| featured | 4 | Busan / Geoje → Fukuoka (Hakata) | `—` | **KEEP** | — |
| journey | market:japan | Setouchi (Naoshima / Teshima Inland Sea) → Setouch | `—` | **KEEP** | — |
| journey | market:japan | Hiroshima / Miyajimaguchi → Miyajima (Itsukushima) | `—` | **KEEP** | — |
| journey | market:japan | Tokyo Bay (Tokyo–Yokohama) → Tokyo Bay | `—` | **KEEP** | — |
| featured | japan/p1 | Takamatsu ↔ Naoshima | `—` | **KEEP** | — |
| featured | japan/p2 | Hiroshima ↔ Miyajima | `—` | **KEEP** | — |
| featured | japan/p3 | Tokyo Bay (Tokyo–Yokohama) → Tokyo Bay | `—` | **KEEP** | — |
| journey | market:taiwan | Kaohsiung harbour → Cijin Island | `—` | **KEEP** | — |
| journey | market:taiwan | Donggang → Xiaoliuqiu (Liuqiu) | `—` | **KEEP** | — |
| journey | market:taiwan | Magong South Sea Visitor Center / Magong Harbour ( | `—` | **KEEP** | — |
| featured | taiwan/p1 | Kaohsiung ↔ Cijin | `—` | **KEEP** | — |
| featured | taiwan/p2 | Magong South Sea Visitor Center / Magong Harbour ( | `—` | **KEEP** | — |
| journey | market:thailand | Krabi → Nonthasak Marine | `—` | **KEEP** | — |
| journey | market:thailand | Krabi → Marina Seaview Krabi | `—` | **KEEP** | — |
| journey | market:thailand | Koh Phangan → Thong Sala Pier (Koh Phangan main) | `—` | **KEEP** | — |
| featured | thailand/p1 | Koh Phangan ↔ Thong Sala Pier (Koh Phangan main) | `—` | **KEEP** | — |
| featured | thailand/p2 | Banyan Tree Krabi → Koh Phi Phi Tour Pier | `rn-41b28873ff52` | **KEEP** | — |
| featured | thailand/p3 | Koh Phangan → Thong Sala Pier (Koh Phangan main) | `rn-db5e83248f9d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Koh Phangan' → 'Thong Sala P |
