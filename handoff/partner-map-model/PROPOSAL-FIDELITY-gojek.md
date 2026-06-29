# Proposal fidelity — gojek

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:26Z

## Summary

- Items audited: 118
- KEEP: 96
- DROP: 22
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 22

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Bali / Nusa Penida / Lembongan / Gilis / Lombok /  | `rn-91e276ba733c` | **KEEP** | — |
| journey | — | Marina Ancol → Pulau Bidadari / Onrust | `ics-9e59ba5c5c` | **KEEP** | — |
| journey | — | Riau Islands (Kepulauan Riau) — Batam / Bintan / A | `rn-2568d40ee060` | **KEEP** | — |
| journey | — | Komodo / Labuan Bajo / Flores / Sumba → Pink Beach | `rn-453a25f98ad9` | **KEEP** | — |
| featured | 1 | Sanur Beach Fast Boat Terminal → GoBoat.id - Nelay | `rn-488fcf2617fe` | **KEEP** | — |
| featured | 1 | Gili Meno Harbour → Ferry Terminal Gili Trawangan | `rn-cf0b8fa978b0` | **KEEP** | — |
| featured | 1 | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| featured | 2 | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-fe31c28f2c` | **KEEP** | — |
| featured | 2 | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-fe31c28f2c` | **KEEP** | — |
| featured | 2 | Riau Islands (Kepulauan Riau) — Batam / Bintan / A | `rn-2568d40ee060` | **KEEP** | — |
| featured | 3 | Komodo / Labuan Bajo / Flores / Sumba → Komodo Isl | `rn-4f204600cf23` | **KEEP** | — |
| featured | 3 | Labuan Bajo ↔ Pink Beach / manta points | `—` | **KEEP** | — |
| featured | 3 | Likupang / Manado / Bunaken, North Sulawesi, Indon | `ics-60c865429d` | **KEEP** | — |
| journey | market:jakarta | Marina Ancol → Pulau Bidadari / Onrust | `ics-9e59ba5c5c` | **KEEP** | — |
| journey | market:jakarta | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-62e1590af9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Thousand Is |
| journey | market:jakarta | Marina Ancol → Pulau Macan / Pelangi / Sepa (outer | `ics-fe31c28f2c` | **KEEP** | — |
| journey | market:jakarta | Marina Ancol → Thousand Islands outer ring (Sepa/P | `ics-fe31c28f2c` | **KEEP** | — |
| featured | jakarta/p1 | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-62e1590af9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Thousand Is |
| featured | jakarta/p1 | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-62e1590af9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Thousand Is |
| featured | jakarta/p1 | Marina Ancol → Thousand Islands outer ring (Sepa/P | `ics-fe31c28f2c` | **KEEP** | — |
| featured | jakarta/p2 | Marina Ancol → Thousand Islands outer ring (Sepa/P | `ics-fe31c28f2c` | **KEEP** | — |
| featured | jakarta/p2 | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-62e1590af9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Thousand Is |
| featured | jakarta/p3 | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-62e1590af9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Thousand Is |
| featured | jakarta/p3 | Marina Ancol → Thousand Islands inner ring (Bidada | `ics-62e1590af9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Ancol' → 'Thousand Is |
| featured | jakarta/p3 | Marina Ancol → Thousand Islands outer ring (Sepa/P | `ics-fe31c28f2c` | **KEEP** | — |
| journey | market:bali-nusa-gili | Bali / Nusa Penida / Lembongan / Gilis / Lombok /  | `rn-91e276ba733c` | **KEEP** | — |
| journey | market:bali-nusa-gili | Bali / Nusa Penida / Lembongan / Gilis / Lombok /  | `rn-c001edd855aa` | **KEEP** | — |
| journey | market:bali-nusa-gili | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| journey | market:bali-nusa-gili | Sampalan Harbour (Nusa Penida E) → Maruti Port - N | `rn-5f35cc1efa05` | **KEEP** | — |
| featured | bali-nusa-gili/p1 | Sanur Beach Fast Boat Terminal → GoBoat.id - Nelay | `rn-488fcf2617fe` | **KEEP** | — |
| featured | bali-nusa-gili/p1 | Gili Meno Harbour → Ferry Terminal Gili Trawangan | `rn-cf0b8fa978b0` | **KEEP** | — |
| featured | bali-nusa-gili/p1 | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| featured | bali-nusa-gili/p2 | Jalan Crystal Bay → Nusa Bahari Lembongan | `rn-606b21464c26` | **KEEP** | — |
| featured | bali-nusa-gili/p2 | Sanur Beach Fast Boat Terminal → GoBoat.id - Nelay | `rn-488fcf2617fe` | **KEEP** | — |
| featured | bali-nusa-gili/p3 | Bali Marina (Benoa) → Jungutbatu Beach (Nusa Lembo | `gcn-3d7809869d-shared` | **KEEP** | — |
| featured | bali-nusa-gili/p3 | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| featured | bali-nusa-gili/p3 | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| journey | market:lombok | Bali Marina (Benoa) → Gili Trawangan Main Harbour | `gcn-869b9d144c-shared` | **KEEP** | — |
| journey | market:lombok | Bangsal Harbour (Pelabuhan Bangsal) → Gili Air mai | `rn-00e3ed569ebc` | **KEEP** | — |
| journey | market:lombok | Lombok → Komodo / Labuan Bajo | `rn-d2f360f76d12` | **KEEP** | — |
| journey | market:lombok | Mandalika Marina Zone (ITDC KEK SEZ greenfield) →  | `rn-0a8e5aab0b22` | **KEEP** | — |
| featured | lombok/p1 | Bangsal Harbour (Pelabuhan Bangsal) → Gili Air mai | `rn-00e3ed569ebc` | **KEEP** | — |
| featured | lombok/p1 | Mandalika Marina Zone (ITDC KEK SEZ greenfield) →  | `rn-0a8e5aab0b22` | **KEEP** | — |
| featured | lombok/p2 | Bali Marina (Benoa) → Gili Trawangan Main Harbour | `gcn-869b9d144c-shared` | **KEEP** | — |
| featured | lombok/p2 | Lombok / Mandalika / Gilis / Sumbawa-Moyo gateway  | `rn-d2f360f76d12` | **KEEP** | — |
| featured | lombok/p3 | Bali Marina (Benoa) → Gili Trawangan Main Harbour | `gcn-869b9d144c-shared` | **KEEP** | — |
| featured | lombok/p3 | Bangsal Harbour (Pelabuhan Bangsal) → Gili Air mai | `rn-00e3ed569ebc` | **KEEP** | — |
| journey | market:komodo-flores | Komodo / Labuan Bajo / Flores / Sumba → Pink Beach | `rn-453a25f98ad9` | **KEEP** | — |
| journey | market:komodo-flores | Labuan Bajo → Pink Beach / manta points | `—` | **KEEP** | — |
| journey | market:komodo-flores | Komodo / Labuan Bajo / Flores / Sumba → Sumba | `rn-11d0c322c8c8` | **KEEP** | — |
| journey | market:komodo-flores | Komodo / Labuan Bajo / Flores / Sumba → Pelabuhan  | `rn-1f3002dd00e5` | **KEEP** | — |
| featured | komodo-flores/p1 | Komodo / Labuan Bajo / Flores / Sumba → Komodo Isl | `rn-4f204600cf23` | **KEEP** | — |
| featured | komodo-flores/p1 | Labuan Bajo ↔ Pink Beach / manta points | `—` | **KEEP** | — |
| featured | komodo-flores/p1 | Komodo / Labuan Bajo / Flores / Sumba → Meruorah K | `rn-871e5ff3b6a7` | **KEEP** | — |
| featured | komodo-flores/p2 | Labuan Bajo ↔ Lombok / Mandalika (refuel mid-node) | `—` | **KEEP** | — |
| featured | komodo-flores/p3 | Komodo / Labuan Bajo / Flores / Sumba → Padar Isla | `rn-c5978b9ec0b4` | **KEEP** | — |
| featured | komodo-flores/p3 | Padang Bai (Bali east — Pioneer II Bali↔Lombok poi | `gcn-3273659cd1-shared` | **KEEP** | — |
| featured | komodo-flores/p3 | Marina Labuan Bajo (KEK LBJ — ITDC) → Maumere Port | `rn-f464cef34281` | **KEEP** | — |
| journey | market:sumba | Komodo / Labuan Bajo → Sumba (Nihi coast) | `gcn-224eb8acd1-shared` | **KEEP** | — |
| journey | market:sumba | Tambolaka / Waingapu gateway → Nihi Sumba | `rn-33fe0cc24a60` | **KEEP** | — |
| journey | market:sumba | NIHI Sumba (private jetty + beach-landing) → Cap K | `rn-c77ad1314ae3` | **KEEP** | — |
| journey | market:sumba | Bali / Lombok → Sumba | `rn-e8aab4ebc00f` | **KEEP** | — |
| featured | sumba/p1 | Tambolaka Airport gateway (Waikabubak) → NIHI Sumb | `rn-33fe0cc24a60` | **KEEP** | — |
| featured | sumba/p1 | NIHI Sumba (private jetty + beach-landing) → Cap K | `rn-c77ad1314ae3` | **KEEP** | — |
| featured | sumba/p2 | Meruorah Komodo Labuan Bajo → NIHI Sumba (private  | `gcn-224eb8acd1-shared` | **KEEP** | — |
| featured | sumba/p2 | Lombok / Mandalika / Gilis / Sumbawa-Moyo gateway  | `rn-e8aab4ebc00f` | **KEEP** | — |
| featured | sumba/p3 | Meruorah Komodo Labuan Bajo → NIHI Sumba (private  | `gcn-224eb8acd1-shared` | **KEEP** | — |
| featured | sumba/p3 | Tambolaka Airport gateway (Waikabubak) → NIHI Sumb | `rn-33fe0cc24a60` | **KEEP** | — |
| journey | market:riau-singapore | Riau Islands (Kepulauan Riau) — Batam / Bintan / A | `rn-2568d40ee060` | **KEEP** | — |
| journey | market:riau-singapore | Singapore → Bintan (Bandar Bentan Telani / Lagoi) | `rn-f3670ea7d99b` | **KEEP** | — |
| journey | market:riau-singapore | Singapore → Riau Islands (Kepulauan Riau) — Batam  | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Riau Islands ( |
| journey | market:riau-singapore | Singapore → Riau Islands (Kepulauan Riau) — Batam  | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Riau Islands ( |
| featured | riau-singapore/p1 | Riau Islands (Kepulauan Riau) — Batam / Bintan / A | `rn-2568d40ee060` | **KEEP** | — |
| featured | riau-singapore/p1 | Singapore → Riau Islands (Kepulauan Riau) — Batam  | `rn-f3670ea7d99b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Riau Islands ( |
| featured | riau-singapore/p1 | Singapore → Riau Islands (Kepulauan Riau) — Batam  | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Riau Islands ( |
| featured | riau-singapore/p2 | Singapore → Riau Islands (Kepulauan Riau) — Batam  | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Riau Islands ( |
| featured | riau-singapore/p3 | Riau Islands (Kepulauan Riau) — Batam / Bintan / A | `rn-2568d40ee060` | **KEEP** | — |
| featured | riau-singapore/p3 | Singapore → Riau Islands (Kepulauan Riau) — Batam  | `rn-f3670ea7d99b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Riau Islands ( |
| featured | riau-singapore/p3 | Singapore → Riau Islands (Kepulauan Riau) — Batam  | `rn-dc3e2f90d207` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Singapore' → 'Riau Islands ( |
| journey | market:singapore | ONE°15 Marina Sentosa Cove → Harbour Bay | `rn-76264638fa6b` | **KEEP** | — |
| journey | market:singapore | Marina Bay / CBD → Changi Point / Pulau Ubin | `rn-e94c308a28e3` | **KEEP** | — |
| journey | market:singapore | Marina Bay Cruise Centre Singapore (MBCCS) → ONE°1 | `rn-f3443bbac675` | **KEEP** | — |
| journey | market:singapore | Riau Islands (Kepulauan Riau) — Batam / Bintan / A | `rn-2568d40ee060` | **KEEP** | — |
| featured | singapore/p1 | ONE°15 Marina Sentosa Cove → Harbour Bay | `rn-76264638fa6b` | **KEEP** | — |
| featured | singapore/p1 | Marina Bay Water Taxi Stops (MPA pilot — Esplanade | `rn-e94c308a28e3` | **KEEP** | — |
| featured | singapore/p1 | ONE°15 Marina Sentosa Cove → Harbour Bay | `rn-76264638fa6b` | **KEEP** | — |
| featured | singapore/p2 | Riau Islands (Kepulauan Riau) — Batam / Bintan / A | `rn-2568d40ee060` | **KEEP** | — |
| featured | singapore/p3 | ONE°15 Marina Sentosa Cove → Harbour Bay | `rn-76264638fa6b` | **KEEP** | — |
| featured | singapore/p3 | Marina Bay Water Taxi Stops (MPA pilot — Esplanade | `rn-e94c308a28e3` | **KEEP** | — |
| featured | singapore/p3 | ONE°15 Marina Sentosa Cove → Harbour Bay | `rn-76264638fa6b` | **KEEP** | — |
| journey | market:raja-ampat | Raja Ampat / Sorong / Misool / Cenderawasih → Mans | `ics-da5220fd24` | **KEEP** | — |
| journey | market:raja-ampat | Raja Ampat (Waisai) → Wayag / Misool | `ics-5840f85047` | **KEEP** | — |
| journey | market:raja-ampat | Raja Ampat → Mioskon Islet | `ics-71281cdfb5` | **KEEP** | — |
| journey | market:raja-ampat | Raja Ampat → Waisai Waterfront | `ics-90f2ce57d8` | **KEEP** | — |
| featured | raja-ampat/p1 | Raja Ampat / Sorong / Misool / Cenderawasih → Mans | `ics-da5220fd24` | **KEEP** | — |
| featured | raja-ampat/p1 | Raja Ampat / Sorong / Misool / Cenderawasih → Mios | `ics-71281cdfb5` | **KEEP** | — |
| featured | raja-ampat/p2 | Raja Ampat / Sorong / Misool / Cenderawasih → Mans | `ics-da5220fd24` | **KEEP** | — |
| featured | raja-ampat/p2 | Raja Ampat / Sorong / Misool / Cenderawasih → Mios | `ics-71281cdfb5` | **KEEP** | — |
| featured | raja-ampat/p3 | Raja Ampat / Sorong / Misool / Cenderawasih → Miso | `ics-5840f85047` | **KEEP** | — |
| journey | market:likupang | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| journey | market:likupang | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| journey | market:likupang | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| journey | market:likupang | Manado → Lembeh Strait (muck-diving) | `—` | **KEEP** | — |
| featured | likupang/p1 | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| featured | likupang/p1 | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| featured | likupang/p2 | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| featured | likupang/p2 | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| featured | likupang/p3 | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-ab1b7a224c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| featured | likupang/p3 | Likupang (North Sulawesi) → Likupang / Manado / Bu | `ics-c142307006` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Likupang (North Sulawesi)' → |
| journey | market:lake-toba | Parapat → Tomok / Tuk Tuk (Samosir) | `rn-db305ed7f029` | **KEEP** | — |
| journey | market:lake-toba | Tuktuk Siadong village pier → Ambarita | `rn-89174b6f31fe` | **KEEP** | — |
| journey | market:lake-toba | Tigaraja Port (Parapat) → Tomok pier (Samosir) | `rn-db305ed7f029` | **KEEP** | — |
| featured | lake-toba/p1 | Tigaraja Port (Parapat) → Tomok pier (Samosir) | `rn-db305ed7f029` | **KEEP** | — |
| featured | lake-toba/p1 | Tuktuk Siadong village pier → Ambarita | `rn-89174b6f31fe` | **KEEP** | — |
| featured | lake-toba/p2 | Tigaraja Port (Parapat) → Tomok pier (Samosir) | `rn-db305ed7f029` | **KEEP** | — |
| featured | lake-toba/p2 | Tuktuk Siadong village pier → Ambarita | `rn-89174b6f31fe` | **KEEP** | — |
| featured | lake-toba/p3 | Tigaraja Port (Parapat) → Tomok pier (Samosir) | `rn-db305ed7f029` | **KEEP** | — |
| featured | lake-toba/p3 | Tuktuk Siadong village pier → Ambarita | `rn-89174b6f31fe` | **KEEP** | — |
