# Proposal fidelity — aman

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:04Z

## Summary

- Items audited: 73
- KEEP: 65
- DROP: 8
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 8

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Dharavandhoo Airport, Baa → Four Seasons Landaa Gi | `e__mald__5108f439d6bc` | **KEEP** | — |
| journey | — | Bora Bora Airport → Four Seasons Bora Bora | `—` | **KEEP** | — |
| journey | — | Mahé → Four Seasons Desroches | `—` | **KEEP** | — |
| journey | — | Four Seasons Kuda Huraa → North Malé reef sites | `—` | **KEEP** | — |
| featured | 1 | Launch the silent zero-wake foiling transfer at Am | `—` | **KEEP** | — |
| featured | 2 | Add silent zero-wake reef and island excursions at | `—` | **KEEP** | — |
| featured | 3 | Connect the Aman Indonesia collection — Bali, Moyo | `—` | **KEEP** | — |
| journey | market:venice | Marco Polo Airport → Aman Venice (Grand Canal) | `—` | **KEEP** | — |
| journey | market:venice | Aman Venice → Murano / Burano / Torcello | `—` | **KEEP** | — |
| journey | market:venice | Aman Venice → Venice Lido | `—` | **KEEP** | — |
| journey | market:venice | Venice → Adriatic coast (Punta Sabbioni / day-trip | `—` | **KEEP** | — |
| featured | venice/p1 | Marco Polo Airport ↔ Aman Venice (Grand Canal) | `—` | **KEEP** | — |
| featured | venice/p1 | Aman Venice ↔ Murano / Burano / Torcello | `—` | **KEEP** | — |
| featured | venice/p1 | Aman Venice ↔ Venice Lido | `—` | **KEEP** | — |
| featured | venice/p2 | Venice ↔ Adriatic coast (Punta Sabbioni / day-trip | `—` | **KEEP** | — |
| featured | venice/p3 | Marco Polo Airport ↔ Aman Venice (Grand Canal) | `—` | **KEEP** | — |
| featured | venice/p3 | Aman Venice ↔ Murano / Burano / Torcello | `—` | **KEEP** | — |
| featured | venice/p3 | Aman Venice ↔ Venice Lido | `—` | **KEEP** | — |
| journey | market:philippines | Amanpulo (Pamalican) → Cuyo archipelago islands | `—` | **KEEP** | — |
| journey | market:philippines | Amanpulo → Pamalican sandbars & dive sites | `—` | **KEEP** | — |
| journey | market:philippines | Amanpulo → El Nido / Palawan mainland | `—` | **KEEP** | — |
| journey | market:philippines | Amanpulo → Cuyo town (cultural visit) | `—` | **KEEP** | — |
| featured | philippines/p1 | Amanpulo (Pamalican) ↔ Cuyo archipelago islands | `—` | **KEEP** | — |
| featured | philippines/p1 | Amanpulo ↔ Pamalican sandbars & dive sites | `—` | **KEEP** | — |
| featured | philippines/p1 | Amanpulo ↔ El Nido / Palawan mainland | `—` | **KEEP** | — |
| featured | philippines/p2 | Amanpulo ↔ Cuyo town (cultural visit) | `—` | **KEEP** | — |
| featured | philippines/p3 | Amanpulo (Pamalican) ↔ Cuyo archipelago islands | `—` | **KEEP** | — |
| featured | philippines/p3 | Amanpulo ↔ Pamalican sandbars & dive sites | `—` | **KEEP** | — |
| featured | philippines/p3 | Amanpulo ↔ El Nido / Palawan mainland | `—` | **KEEP** | — |
| journey | market:indonesia | Bali (Amankila / east coast) → Lombok (Gili / west | `—` | **KEEP** | — |
| journey | market:indonesia | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| journey | market:indonesia | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| journey | market:indonesia | Lombok / Sumbawa → Komodo / Flores (Labuan Bajo) | `—` | **KEEP** | — |
| featured | indonesia/p1 | Bali / Nusa Penida / Lembongan / Gilis / Lombok /  | `—` | **KEEP** | — |
| featured | indonesia/p1 | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| featured | indonesia/p1 | Bali Marina (Benoa) → Six Senses Uluwatu | `rn-c256a044c8be` | **KEEP** | — |
| featured | indonesia/p2 | Lombok / Mandalika / Gilis / Sumbawa-Moyo gateway  | `—` | **KEEP** | — |
| featured | indonesia/p3 | Bali (Amankila / east coast) ↔ Lombok (Gili / west | `—` | **KEEP** | — |
| featured | indonesia/p3 | Bali / Lombok ↔ Amanwana (Moyo Island) | `—` | **KEEP** | — |
| featured | indonesia/p3 | Amankila (Bali east coast) ↔ Nusa Penida / Lembong | `—` | **KEEP** | — |
| journey | market:thailand | Ao Po Grand Marina → Anantara Layan Phuket Beach J | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ao Po Grand Marina' → 'Anant |
| journey | market:thailand | Amanpuri → Phang Nga Bay karsts & private islands | `—` | **KEEP** | — |
| journey | market:thailand | Manoh Pier (Koh Yao Yai) → Thap Lamu Pier (Similan | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manoh Pier (Koh Yao Yai)' →  |
| journey | market:thailand | Ao Po Grand Marina → Anantara Layan Phuket Beach J | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ao Po Grand Marina' → 'Anant |
| featured | thailand/p1 | Ao Po Grand Marina → Anantara Layan Phuket Beach J | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ao Po Grand Marina' → 'Anant |
| featured | thailand/p1 | Amanpuri ↔ Phang Nga Bay karsts & private islands | `—` | **KEEP** | — |
| featured | thailand/p1 | Manoh Pier (Koh Yao Yai) → Thap Lamu Pier (Similan | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manoh Pier (Koh Yao Yai)' →  |
| featured | thailand/p2 | Ao Po Grand Marina → Anantara Layan Phuket Beach J | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ao Po Grand Marina' → 'Anant |
| featured | thailand/p3 | Ao Po Grand Marina → Anantara Layan Phuket Beach J | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ao Po Grand Marina' → 'Anant |
| featured | thailand/p3 | Amanpuri ↔ Phang Nga Bay karsts & private islands | `—` | **KEEP** | — |
| featured | thailand/p3 | Manoh Pier (Koh Yao Yai) → Thap Lamu Pier (Similan | `rn-eb5758aeba2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Manoh Pier (Koh Yao Yai)' →  |
| journey | market:montenegro | Tivat Airport / Porto Montenegro → Aman Sveti Stef | `—` | **KEEP** | — |
| journey | market:montenegro | Sveti Stefan → Bay of Kotor (Perast / Kotor town) | `—` | **KEEP** | — |
| journey | market:montenegro | Sveti Stefan → Dubrovnik & the South Dalmatian coa | `—` | **KEEP** | — |
| journey | market:montenegro | Montenegro coast → Porto Montenegro / Portonovi ma | `—` | **KEEP** | — |
| featured | montenegro/p1 | Tivat Airport / Porto Montenegro ↔ Aman Sveti Stef | `—` | **KEEP** | — |
| featured | montenegro/p1 | Sveti Stefan ↔ Bay of Kotor (Perast / Kotor town) | `—` | **KEEP** | — |
| featured | montenegro/p1 | Sveti Stefan ↔ Dubrovnik & the South Dalmatian coa | `—` | **KEEP** | — |
| featured | montenegro/p2 | Montenegro coast ↔ Porto Montenegro / Portonovi ma | `—` | **KEEP** | — |
| featured | montenegro/p3 | Tivat Airport / Porto Montenegro ↔ Aman Sveti Stef | `—` | **KEEP** | — |
| featured | montenegro/p3 | Sveti Stefan ↔ Bay of Kotor (Perast / Kotor town) | `—` | **KEEP** | — |
| featured | montenegro/p3 | Sveti Stefan ↔ Dubrovnik & the South Dalmatian coa | `—` | **KEEP** | — |
| journey | market:greece | Athens (Hellinikon / Lavrio) → Amanzoe (Porto Heli | `—` | **KEEP** | — |
| journey | market:greece | Amanzoe / Porto Heli → Spetses & Hydra | `—` | **KEEP** | — |
| journey | market:greece | Amanzoe → Cycladic islands (Mykonos / Paros) | `—` | **KEEP** | — |
| journey | market:greece | Porto Heli → Nafplio & the Argolic coast | `—` | **KEEP** | — |
| featured | greece/p1 | Athens (Hellinikon / Lavrio) ↔ Amanzoe (Porto Heli | `—` | **KEEP** | — |
| featured | greece/p1 | Amanzoe / Porto Heli ↔ Spetses & Hydra | `—` | **KEEP** | — |
| featured | greece/p1 | Amanzoe ↔ Cycladic islands (Mykonos / Paros) | `—` | **KEEP** | — |
| featured | greece/p2 | Porto Heli ↔ Nafplio & the Argolic coast | `—` | **KEEP** | — |
| featured | greece/p3 | Athens (Hellinikon / Lavrio) ↔ Amanzoe (Porto Heli | `—` | **KEEP** | — |
| featured | greece/p3 | Amanzoe / Porto Heli ↔ Spetses & Hydra | `—` | **KEEP** | — |
| featured | greece/p3 | Amanzoe ↔ Cycladic islands (Mykonos / Paros) | `—` | **KEEP** | — |
