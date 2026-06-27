# Proposal fidelity — grab

**Verdict:** REWRITE
**Checked:** 2026-06-27T16:00:27Z

## Summary

- Items audited: 143
- KEEP: 33
- DROP: 108
- DEFER: 0
- TRIM/REWRITE: 2
- BP-binding errors: 108

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Marina Bay / CBD → Sentosa & the Southern Islands | `—` | **KEEP** | — |
| journey | — | Singapore (Tanah Merah) → Bintan — Lagoi resorts ( | `rn-f3670ea7d99b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore (Tanah Merah)' → ' |
| journey | — | Singapore (Tanah Merah) → Desaru Coast (Johor, Mal | `rn-ef7c059adbde` | **KEEP** | — |
| journey | — | Bali (Sanur / Benoa) → Lombok & the Gilis | `rn-c001edd855aa` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bali (Sanur / Benoa)' → 'Lom |
| journey | — | Phuket → Langkawi (via the Andaman) | `rn-853cbe7dd006` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Phuket' → 'Langkawi (via the |
| journey | — | Manila CBD (Makati / BGC) → Manila Bay & Cavite | `—` | **KEEP** | — |
| featured | 1 | Marina Bay ↔ Changi Point / Pulau Ubin | `rn-e94c308a28e3` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Marina Bay  |
| featured | 1 | East Coast ↔ Marina / CBD | `rn-82453f6cb33e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bedok Jetty |
| featured | 1 | Manila (Bay / Pasig) ↔ Cavite / Bataan | `rn-b109322aa1e9` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Esplanade S |
| featured | 2 | Da Nang (Han River) ↔ Hoi An / Cham Islands | `ics-1312999652` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Da Nang / H |
| featured | 2 | Marina Bay ↔ Sentosa / southern islands | `rn-9b7446ded0a5` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Pulau Brani |
| featured | 2 | Singapore ↔ Riau resort islands (regional reach) | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Singapore'  |
| featured | 3 | Ha Long / Tuan Chau ↔ Lan Ha Bay / Cat Ba | `ics-f21c5d7e8d` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Ha Long Bay; geometry_preview: interior_land_km=10.16 (threshold 0.4) |
| featured | 3 | Phuket (Royal Phuket Marina) ↔ Phang Nga Bay / Jam | `rn-b28ac4ca3d14` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'bp-655b11d9 |
| featured | 3 | Singapore ↔ Bintan (Lagoi resort zone) | `rn-f3670ea7d99b` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Singapore'  |
| featured | 4 | Bach Dang Wharf (District 1) ↔ Thu Duc / Grand Par | `rn-a0654d43e7e4` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'bp-f5f91624 |
| featured | 4 | Singapore / Desaru ↔ East-coast Malaysia & outer R | `rn-5d1a30fbb0a9` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Desaru Coas |
| featured | 4 | Singapore ↔ Desaru Coast / Johor | `rn-f2a4c410dfa8` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Desaru Coas |
| journey | market:singapore | Marina Bay → Sentosa / southern islands | `rn-76264638fa6b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Bay' → 'Sentosa / sou |
| journey | market:singapore | East Coast → Marina / CBD | `rn-82453f6cb33e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'East Coast' → 'Marina / CBD' |
| journey | market:singapore | Marina Bay → Changi Point / Pulau Ubin | `rn-e94c308a28e3` | **KEEP** | — |
| journey | market:singapore | Singapore → Riau resort islands (regional reach) | `rn-f3670ea7d99b` | **TRIM** | distance_honesty: card 13.0nm vs route 21.9nm (41% delta) |
| featured | singapore/p1 | East Coast ↔ Marina / CBD | `rn-82453f6cb33e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bedok Jetty |
| featured | singapore/p2 | Marina Bay ↔ Sentosa / southern islands | `rn-76264638fa6b` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'ONE°15 Mari |
| featured | singapore/p3 | Marina Bay ↔ Sentosa / southern islands | `rn-76264638fa6b` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'ONE°15 Mari |
| journey | market:cross-border | Singapore → Desaru Coast / Johor | `rn-f2a4c410dfa8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Desaru Coast / |
| journey | market:cross-border | Singapore → Bintan (Lagoi resort zone) | `rn-f3670ea7d99b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Bintan (Lagoi  |
| journey | market:cross-border | Singapore → Batam (Harbour Bay / Nongsa) | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Batam (Harbour |
| journey | market:cross-border | Singapore / Desaru → East-coast Malaysia & outer R | `rn-5d1a30fbb0a9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore / Desaru' → 'East- |
| featured | cross-border/p1 | Singapore ↔ Batam (Harbour Bay / Nongsa) | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Singapore'  |
| featured | cross-border/p2 | Singapore ↔ Bintan (Lagoi resort zone) | `rn-f3670ea7d99b` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Singapore'  |
| featured | cross-border/p3 | Singapore / Desaru ↔ East-coast Malaysia & outer R | `rn-5d1a30fbb0a9` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Desaru Coas |
| journey | market:bali | Bali (Benoa / Sanur) → Nusa Penida / Lembongan | `rn-c256a044c8be` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bali (Benoa / Sanur)' → 'Nus |
| journey | market:bali | Bali → Gili Islands / Lombok | `rn-91e276ba733c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bali' → 'Gili Islands / Lomb |
| journey | market:bali | Lombok → Komodo / Labuan Bajo | `rn-d2f360f76d12` | **KEEP** | — |
| journey | market:bali | Komodo / Labuan Bajo → Sumba (Nihi) | `rn-11d0c322c8c8` | **KEEP** | — |
| journey | market:bali | Bali (Canggu) → Uluwatu / Bukit | `rn-c256a044c8be` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bali (Canggu)' → 'Uluwatu /  |
| featured | bali/p1 | Bali (Benoa / Sanur) ↔ Nusa Penida / Lembongan | `rn-c256a044c8be` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bali Marina |
| featured | bali/p2 | Bali ↔ Gili Islands / Lombok | `rn-91e276ba733c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bali / Nusa |
| featured | bali/p3 | Komodo / Labuan Bajo ↔ Sumba (Nihi) | `rn-11d0c322c8c8` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Komodo / La |
| journey | market:jakarta | Marina Ancol → Pulau Bidadari / Onrust | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Pulau Bidad |
| journey | market:jakarta | Pluit / PIK → Ancol / Tanjung Priok | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Pluit / PIK' → 'Ancol / Tanj |
| journey | market:jakarta | Marina Ancol → Pulau Macan / Pelangi / Sepa (outer | `ics-fe31c28f2c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Pulau Macan |
| journey | market:jakarta | Jakarta Bay → Pulau Putri / Pantara | `ics-fe31c28f2c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Jakarta Bay' → 'Pulau Putri  |
| journey | market:jakarta | Tanjung Priok → Marina Ancol / city waterfront | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Tanjung Priok' → 'Marina Anc |
| journey | market:jakarta | Pluit / PIK (north Jakarta) → Marunda / Cilincing  | `edge__karimunjawa-central-java-indonesia__jakarta-marina-ancol-karimunjawa-line-haul` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Pluit / PIK (north Jakarta)' |
| journey | market:jakarta | Thousand Islands — inner ring → Thousand Islands — | `ics-62e1590af9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Thousand Islands — inner rin |
| featured | jakarta/p1 | Marina Ancol ↔ Pulau Bidadari / Onrust | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| featured | jakarta/p1 | Pluit / PIK ↔ Ancol / Tanjung Priok | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| featured | jakarta/p1 | Marina Ancol ↔ Pulau Macan / Pelangi / Sepa (outer | `ics-fe31c28f2c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| featured | jakarta/p2 | Jakarta Bay ↔ Pulau Putri / Pantara | `ics-fe31c28f2c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| featured | jakarta/p2 | Tanjung Priok ↔ Marina Ancol / city waterfront | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| featured | jakarta/p3 | Marina Ancol ↔ Pulau Bidadari / Onrust | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| featured | jakarta/p3 | Pluit / PIK ↔ Ancol / Tanjung Priok | `ics-9e59ba5c5c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| featured | jakarta/p3 | Marina Ancol ↔ Pulau Macan / Pelangi / Sepa (outer | `ics-fe31c28f2c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Jakarta' →  |
| journey | market:lombok | Bali (Padang Bai / Serangan) → Gili Islands / Lomb | `gcn-869b9d144c-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Bali (Padang Bai / Serangan) |
| journey | market:lombok | Lombok (Bangsal / Senggigi) → Gili Trawangan / Men | `rn-00e3ed569ebc` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Lombok (Bangsal / Senggigi)'; distance_honesty: card 6.0nm vs route 2.1nm (186% delta) |
| journey | market:lombok | Lombok → Komodo / Labuan Bajo | `rn-d2f360f76d12` | **KEEP** | — |
| journey | market:lombok | Kuta Lombok / Mandalika → Gili Islands | `rn-0a8e5aab0b22` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kuta Lombok / Mandalika' → '; distance_honesty: card 22.0nm vs route 1.9nm (1058% delta) |
| featured | lombok/p1 | Lombok (Bangsal / Senggigi) ↔ Gili Trawangan / Men | `rn-00e3ed569ebc` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bangsal Har; distance_honesty: card 6.0nm vs route 2.1nm (186% delta) |
| featured | lombok/p1 | Kuta Lombok / Mandalika ↔ Gili Islands | `rn-0a8e5aab0b22` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Mandalika M; distance_honesty: card 22.0nm vs route 1.9nm (1058% delta) |
| featured | lombok/p2 | Bali (Padang Bai / Serangan) ↔ Gili Islands / Lomb | `gcn-869b9d144c-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bali Marina |
| featured | lombok/p2 | Lombok ↔ Komodo / Labuan Bajo | `rn-d2f360f76d12` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Lombok / Ma |
| featured | lombok/p3 | Bali (Padang Bai / Serangan) ↔ Gili Islands / Lomb | `gcn-869b9d144c-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bali Marina |
| featured | lombok/p3 | Lombok (Bangsal / Senggigi) ↔ Gili Trawangan / Men | `rn-00e3ed569ebc` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Bangsal Har; distance_honesty: card 6.0nm vs route 2.1nm (186% delta) |
| journey | market:komodo-flores | Labuan Bajo → Komodo / Rinca / Padar | `rn-453a25f98ad9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Labuan Bajo' → 'Komodo / Rin |
| journey | market:komodo-flores | Labuan Bajo → Pink Beach / manta points | `—` | **KEEP** | — |
| journey | market:komodo-flores | Labuan Bajo → Maumere / east Flores | `rn-11d0c322c8c8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Labuan Bajo' → 'Maumere / ea |
| journey | market:komodo-flores | Labuan Bajo → Lombok / Mandalika (refuel mid-node) | `rn-1f3002dd00e5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Labuan Bajo' → 'Lombok / Man |
| journey | market:komodo-flores | Komodo → Komodo Island — Ata Modo village | `rn-4f204600cf23` | **KEEP** | — |
| journey | market:komodo-flores | Komodo → Meruorah Komodo Labuan Bajo | `rn-871e5ff3b6a7` | **KEEP** | — |
| journey | market:komodo-flores | Komodo → Padar Island Viewing-Platform Pier | `rn-c5978b9ec0b4` | **KEEP** | — |
| journey | market:komodo-flores | Marina Labuan Bajo → Maumere Port (Lorenz Say) — K | `rn-f464cef34281` | **KEEP** | — |
| featured | komodo-flores/p1 | Labuan Bajo ↔ Komodo / Rinca / Padar | `rn-4f204600cf23` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Komodo / La |
| featured | komodo-flores/p1 | Labuan Bajo ↔ Pink Beach / manta points | `—` | **KEEP** | — |
| featured | komodo-flores/p1 | Labuan Bajo ↔ Maumere / east Flores | `rn-871e5ff3b6a7` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Komodo / La |
| featured | komodo-flores/p2 | Labuan Bajo ↔ Lombok / Mandalika (refuel mid-node) | `—` | **KEEP** | — |
| featured | komodo-flores/p3 | Labuan Bajo ↔ Komodo / Rinca / Padar | `rn-c5978b9ec0b4` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Komodo / La |
| featured | komodo-flores/p3 | Labuan Bajo ↔ Pink Beach / manta points | `gcn-3273659cd1-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Padang Bai  |
| featured | komodo-flores/p3 | Labuan Bajo ↔ Maumere / east Flores | `rn-f464cef34281` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Marina Labu |
| journey | market:sumba | Komodo / Labuan Bajo → Sumba (Nihi coast) | `gcn-224eb8acd1-shared` | **KEEP** | — |
| journey | market:sumba | Tambolaka / Waingapu gateway → Nihi Sumba | `—` | **KEEP** | — |
| journey | market:sumba | Nihi Sumba → Southwest surf bays | `—` | **KEEP** | — |
| journey | market:sumba | Bali / Lombok → Sumba | `—` | **KEEP** | — |
| featured | sumba/p1 | Tambolaka / Waingapu gateway ↔ Nihi Sumba | `—` | **KEEP** | — |
| featured | sumba/p1 | Nihi Sumba ↔ Southwest surf bays | `—` | **KEEP** | — |
| featured | sumba/p2 | Komodo / Labuan Bajo ↔ Sumba (Nihi coast) | `gcn-224eb8acd1-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Meruorah Ko |
| featured | sumba/p2 | Bali / Lombok ↔ Sumba | `—` | **KEEP** | — |
| featured | sumba/p3 | Komodo / Labuan Bajo ↔ Sumba (Nihi coast) | `gcn-224eb8acd1-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Meruorah Ko |
| featured | sumba/p3 | Tambolaka / Waingapu gateway ↔ Nihi Sumba | `—` | **KEEP** | — |
| journey | market:raja-ampat | Sorong (West Papua) → Waisai / Raja Ampat | `ics-da5220fd24` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Sorong (West Papua)' → 'Wais |
| journey | market:raja-ampat | Raja Ampat (Waisai) → Wayag / Misool | `ics-5840f85047` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Raja Ampat (Waisai)' → 'Waya |
| journey | market:raja-ampat | Raja Ampat → Mioskon Islet | `ics-71281cdfb5` | **KEEP** | — |
| journey | market:raja-ampat | Raja Ampat → Waisai Waterfront | `ics-90f2ce57d8` | **KEEP** | — |
| featured | raja-ampat/p1 | Sorong (West Papua) ↔ Waisai / Raja Ampat | `ics-da5220fd24` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Raja Ampat  |
| featured | raja-ampat/p1 | Raja Ampat ↔ Mioskon Islet | `ics-71281cdfb5` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Raja Ampat  |
| featured | raja-ampat/p2 | Sorong (West Papua) ↔ Waisai / Raja Ampat | `ics-da5220fd24` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Raja Ampat  |
| featured | raja-ampat/p2 | Raja Ampat ↔ Mioskon Islet | `ics-71281cdfb5` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Raja Ampat  |
| featured | raja-ampat/p3 | Raja Ampat (Waisai) ↔ Wayag / Misool | `ics-5840f85047` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Raja Ampat  |
| journey | market:likupang | Manado → Bunaken / Siladen / Lembeh | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manado' → 'Bunaken / Siladen |
| journey | market:likupang | Manado → Sangihe-Talaud archipelago | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manado' → 'Sangihe-Talaud ar |
| journey | market:likupang | Manado → Bunaken Marine Park | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manado' → 'Bunaken Marine Pa |
| journey | market:likupang | Manado → Lembeh Strait (muck-diving) | `—` | **KEEP** | — |
| journey | market:likupang | Likupang gateway → Bunaken / Siladen resorts | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang gateway' → 'Bunaken; distance_honesty: card 12.0nm vs route 7.1nm (69% delta) |
| featured | likupang/p1 | Manado ↔ Bunaken / Siladen / Lembeh | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Likupang (N |
| featured | likupang/p1 | Manado ↔ Sangihe-Talaud archipelago | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Likupang (N |
| featured | likupang/p2 | Manado ↔ Bunaken / Siladen / Lembeh | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Likupang (N |
| featured | likupang/p2 | Manado ↔ Sangihe-Talaud archipelago | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Likupang (N |
| featured | likupang/p3 | Manado ↔ Bunaken / Siladen / Lembeh | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Likupang (N |
| featured | likupang/p3 | Manado ↔ Sangihe-Talaud archipelago | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Likupang (N |
| journey | market:lake-toba | Parapat → Tomok / Tuk Tuk (Samosir) | `rn-db305ed7f029` | **KEEP** | — |
| journey | market:lake-toba | Tuk Tuk → Samosir shoreline villages | `rn-89174b6f31fe` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Tuk Tuk' → 'Samosir shorelin |
| journey | market:lake-toba | Parapat → Samosir resorts | `rn-db305ed7f029` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Parapat' → 'Samosir resorts'; distance_honesty: card 6.0nm vs route 3.2nm (87% delta) |
| featured | lake-toba/p1 | Parapat ↔ Tomok / Tuk Tuk (Samosir) | `rn-db305ed7f029` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Tigaraja Po |
| featured | lake-toba/p1 | Tuk Tuk ↔ Samosir shoreline villages | `rn-89174b6f31fe` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Tuktuk Siad |
| featured | lake-toba/p2 | Parapat ↔ Tomok / Tuk Tuk (Samosir) | `rn-db305ed7f029` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Tigaraja Po |
| featured | lake-toba/p2 | Tuk Tuk ↔ Samosir shoreline villages | `rn-89174b6f31fe` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Tuktuk Siad |
| featured | lake-toba/p3 | Parapat ↔ Tomok / Tuk Tuk (Samosir) | `rn-db305ed7f029` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Tigaraja Po |
| featured | lake-toba/p3 | Tuk Tuk ↔ Samosir shoreline villages | `rn-89174b6f31fe` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Tuktuk Siad |
| journey | market:phuket | Phuket (Royal Phuket Marina) → Phang Nga Bay / Jam | `rn-b28ac4ca3d14` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Phuket (Royal Phuket Marina) |
| journey | market:phuket | Phuket → Phi Phi / Krabi | `rn-b28ac4ca3d14` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Phuket' → 'Phi Phi / Krabi'  |
| journey | market:phuket | Phuket → Similan / Surin Islands | `gcn-0cc5f4e157-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Phuket' → 'Similan / Surin I; geometry_preview: interior_land_km=16.94 (threshold 0.4) |
| journey | market:phuket | Phuket → Langkawi (cross-border, regional reach) | `rn-b28ac4ca3d14` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Phuket' → 'Langkawi (cross-b |
| featured | phuket/p1 | Phuket (Royal Phuket Marina) ↔ Phang Nga Bay / Jam | `rn-b28ac4ca3d14` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'bp-655b11d9 |
| featured | phuket/p2 | Phuket ↔ Similan / Surin Islands | `gcn-0cc5f4e157-shared` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'bp-b2d72216; geometry_preview: interior_land_km=16.94 (threshold 0.4) |
| featured | phuket/p3 | Phuket ↔ Similan | `rn-b1313beb0eaa` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Manoh Pier  |
| featured | phuket/p3 | Phuket ↔ Surin | `rn-b28ac4ca3d14` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'bp-655b11d9 |
| featured | phuket/p3 | Phuket ↔ Langkawi reach | `rn-b28ac4ca3d14` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'bp-655b11d9 |
| journey | market:philippines | Manila (Bay / Pasig) → Cavite / Bataan | `—` | **KEEP** | — |
| journey | market:philippines | Cebu (Mactan) → Bohol / Panglao | `rn-66e9451f405f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cebu (Mactan)' → 'Bohol / Pa |
| journey | market:philippines | Manila → Coron / El Nido (Palawan) | `edge__manila-philippines__palawan-el-nido-coron-amanpulo` | **KEEP** | — |
| journey | market:philippines | Cebu → Boracay | `rn-66e9451f405f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cebu' → 'Boracay' vs route ' |
| featured | philippines/p1 | Manila (Bay / Pasig) ↔ Cavite / Bataan | `—` | **KEEP** | — |
| featured | philippines/p2 | Manila (Bay / Pasig) ↔ Cavite / Bataan | `—` | **KEEP** | — |
| featured | philippines/p3 | Manila (Bay / Pasig) ↔ Cavite / Bataan | `—` | **KEEP** | — |
| journey | market:vietnam | Bach Dang Wharf (District 1) → Thu Duc / Grand Par | `—` | **KEEP** | — |
| journey | market:vietnam | Saigon (Bach Dang) → Vung Tau | `rn-00dfea36a4d9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Saigon (Bach Dang)' → 'Vung ; geometry_preview: interior_land_km=38.60 (threshold 0.4) |
| journey | market:vietnam | Da Nang (Han River) → Hoi An / Cham Islands | `ics-1312999652` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Da Nang (Han River)' → 'Hoi  |
| journey | market:vietnam | Ha Long / Tuan Chau → Lan Ha Bay / Cat Ba | `ics-f21c5d7e8d` | **TRIM** | geometry_preview: interior_land_km=10.16 (threshold 0.4) |
| journey | market:vietnam | Phu Quoc (Duong Dong) → An Thoi Archipelago | `ics-26acf800c5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Phu Quoc (Duong Dong)' → 'An |
| featured | vietnam/p1 | Da Nang (Han River) ↔ Hoi An / Cham Islands | `ics-1312999652` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Da Nang / H |
| featured | vietnam/p2 | Ha Long / Tuan Chau ↔ Lan Ha Bay / Cat Ba | `ics-f21c5d7e8d` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Ha Long Bay; geometry_preview: interior_land_km=10.16 (threshold 0.4) |
| featured | vietnam/p3 | Bach Dang Wharf (District 1) ↔ Thu Duc / Grand Par | `—` | **KEEP** | — |
