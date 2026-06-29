# Proposal fidelity — didi

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:13:53Z

## Summary

- Items audited: 87
- KEEP: 83
- DROP: 4
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 4

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Rio de Janeiro (Marina da Glória) → Angra dos Reis | `—` | **KEEP** | — |
| journey | — | Cancún → Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| journey | — | Puerto Vallarta → Marietas Islands | `—` | **KEEP** | — |
| journey | — | Cartagena (Marina) → Rosario Islands | `ics-e10b53b415` | **KEEP** | — |
| featured | 1 | Cartí Sugdup (Gardi Sugdub) community dock → Cartí | `rn-a1eae9288e3a` | **KEEP** | — |
| featured | 2 | Cancun Adventures → Marina Puerto Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| featured | 2 | Samaná Peninsula & Bay — Dominican Republic → Sant | `rn-b7b7d78c475e` | **KEEP** | — |
| featured | 3 | Cartagena & the Rosario Islands → Cartagena & The  | `ics-2c0462e53e` | **KEEP** | — |
| featured | 3 | Cancun Adventures → Marina Puerto Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| featured | 4 | Cartí ↔ San Blas cays | `—` | **KEEP** | — |
| featured | 4 | Samaná Peninsula & Bay — Dominican Republic → Sant | `rn-b7b7d78c475e` | **KEEP** | — |
| featured | 4 | Muelle Fiscal Playa del Carmen → Passenger Ferry U | `ics-dd1d814699` | **KEEP** | — |
| journey | market:brazil | Rio (Marina da Glória) → Angra dos Reis / Ilha Gra | `—` | **KEEP** | — |
| journey | market:brazil | Angra dos Reis + Ilha Grande (Costa Verde) → Angra | `ics-580360f22d` | **KEEP** | — |
| journey | market:brazil | Angra dos Reis + Ilha Grande (Costa Verde) → Angra | `ics-0effac4535` | **KEEP** | — |
| journey | market:brazil | Florianópolis & Santa Catarina → Florianópolis & S | `ics-70df874036` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Florianópolis & Santa Catari |
| featured | brazil/p1 | Club Caiçaras → Iate Clube de Coroa Grande | `ics-07560a31af` | **KEEP** | — |
| featured | brazil/p1 | Angra dos Reis + Ilha Grande (Costa Verde) → Angra | `ics-6536c49acf` | **KEEP** | — |
| featured | brazil/p2 | Florianópolis & Santa Catarina → Florianópolis & S | `—` | **KEEP** | — |
| featured | brazil/p3 | Rio (Marina da Glória) ↔ Angra dos Reis / Ilha Gra | `—` | **KEEP** | — |
| featured | brazil/p3 | Angra dos Reis + Ilha Grande (Costa Verde) → Angra | `ics-e6e8db7a6b` | **KEEP** | — |
| journey | market:mexico-pacific | Los Cabos → Los Cabos, Baja Sur | `ics-c7f9a1723e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Los Cabos' → 'Los Cabos, Baj |
| journey | market:mexico-pacific | Puerto Vallarta & Riviera Nayarit → Puerto Vallart | `ics-121f3d1628` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Puerto Vallarta & Riviera Na |
| journey | market:mexico-pacific | Puerto Vallarta → Yelapa / southern Banderas Bay | `ics-58af4a4a7a` | **KEEP** | — |
| journey | market:mexico-pacific | Los Cabos → Santa María | `ics-9f6ef631b4` | **KEEP** | — |
| featured | mexico-pacific/p1 | Puerto Vallarta & Riviera Nayarit → Puerto Vallart | `ics-58accdef81` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Puerto Vallarta & Riviera Na |
| featured | mexico-pacific/p1 | Puerto Vallarta & Riviera Nayarit → Yelapa | `ics-58af4a4a7a` | **KEEP** | — |
| featured | mexico-pacific/p1 | Los Cabos → Los Cabos, Baja Sur | `—` | **KEEP** | — |
| featured | mexico-pacific/p2 | Los Cabos → La Ribera | `ics-1ef9b3ecdc` | **KEEP** | — |
| featured | mexico-pacific/p3 | Palmilla → San José Del Cabo Marina | `ics-b5861451fb` | **KEEP** | — |
| featured | mexico-pacific/p3 | Puerto Vallarta & Riviera Nayarit → Puerto Vallart | `—` | **KEEP** | — |
| featured | mexico-pacific/p3 | Puerto Vallarta & Riviera Nayarit → Yelapa | `ics-89a8844858` | **KEEP** | — |
| journey | market:mexico-caribbean | Cancún → Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| journey | market:mexico-caribbean | Playa del Carmen → Cozumel | `ics-dd1d814699` | **KEEP** | — |
| journey | market:mexico-caribbean | Cancún & the Riviera Maya → Cancún & The Riviera M | `ics-39e68b6194` | **KEEP** | — |
| journey | market:mexico-caribbean | Riviera Maya → Cozumel reef / Banco Chinchorro | `—` | **KEEP** | — |
| featured | mexico-caribbean/p1 | Cancun Adventures → Marina Puerto Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| featured | mexico-caribbean/p1 | Muelle Fiscal Playa del Carmen → Passenger Ferry U | `ics-dd1d814699` | **KEEP** | — |
| featured | mexico-caribbean/p1 | Cancún ↔ Holbox | `—` | **KEEP** | — |
| featured | mexico-caribbean/p2 | Riviera Maya ↔ Cozumel reef / Banco Chinchorro | `—` | **KEEP** | — |
| featured | mexico-caribbean/p3 | Cancun Adventures → Marina Puerto Isla Mujeres | `ics-6ee0d44804` | **KEEP** | — |
| featured | mexico-caribbean/p3 | Muelle Fiscal Playa del Carmen → Passenger Ferry U | `ics-dd1d814699` | **KEEP** | — |
| featured | mexico-caribbean/p3 | Marina Puerto Cancún → Marina Hacienda del Mar | `ics-0885ec38ac` | **KEEP** | — |
| journey | market:colombia | Cartagena (Marina) → Rosario Islands | `ics-e10b53b415` | **KEEP** | — |
| journey | market:colombia | Cartagena → Barú / Playa Blanca | `ics-2c66505042` | **KEEP** | — |
| journey | market:colombia | San Blas (Guna Yala) Archipelago — Panama → Cartag | `e__san-blas-panama__cartagena-colombia` | **KEEP** | — |
| journey | market:colombia | Cartagena → Santa Marta / Tayrona coast | `ics-b98d3376f8` | **KEEP** | — |
| featured | colombia/p1 | Club de pesca de Cartagena - Marina → Rosario Isla | `ics-e10b53b415` | **KEEP** | — |
| featured | colombia/p1 | Club de pesca de Cartagena - Marina → Isla baru Pl | `ics-2c66505042` | **KEEP** | — |
| featured | colombia/p1 | Cartagena & the Rosario Islands → Aruba | `edge-1088` | **KEEP** | — |
| featured | colombia/p2 | Club de pesca de Cartagena - Marina → Marina Santa | `ics-b98d3376f8` | **KEEP** | — |
| featured | colombia/p3 | Club de pesca de Cartagena - Marina → Rosario Isla | `ics-e10b53b415` | **KEEP** | — |
| featured | colombia/p3 | Club de pesca de Cartagena - Marina → Isla baru Pl | `ics-2c66505042` | **KEEP** | — |
| featured | colombia/p3 | Cartagena & the Rosario Islands → Cartagena & The  | `ics-2c0462e53e` | **KEEP** | — |
| journey | market:panama | Cartí (Cartí Sugdup) → Isla Perro / Cayos Holandes | `—` | **KEEP** | — |
| journey | market:panama | El Porvenir → Achutupu / eastern Guna Yala | `—` | **KEEP** | — |
| journey | market:panama | San Blas (Guna Yala) Archipelago — Panama → Playón | `rn-249011467661` | **KEEP** | — |
| journey | market:panama | Cartí → Guna Yala overnight-island resorts | `rn-c7ea7b8632d4` | **KEEP** | — |
| featured | panama/p1 | Cartí (Cartí Sugdup) ↔ Isla Perro / Cayos Holandes | `—` | **KEEP** | — |
| featured | panama/p1 | El Porvenir ↔ Achutupu / eastern Guna Yala | `—` | **KEEP** | — |
| featured | panama/p1 | San Blas (Guna Yala) Archipelago — Panama → Nargan | `rn-a5d53d26dfe1` | **KEEP** | — |
| featured | panama/p2 | Puerto Cartí (Cartí / Gardi mainland dock) → Cartí | `rn-c7ea7b8632d4` | **KEEP** | — |
| featured | panama/p3 | San Blas (Guna Yala) Archipelago — Panama → Cartí  | `rn-3d3a08c42c16` | **KEEP** | — |
| featured | panama/p3 | El Porvenir ↔ Achutupu / eastern Guna Yala | `—` | **KEEP** | — |
| featured | panama/p3 | San Blas (Guna Yala) Archipelago — Panama → Cartí  | `rn-74a4db70919a` | **KEEP** | — |
| journey | market:costa-rica | Marina Papagayo → Playas del Coco / resort coast | `rn-761106cfaa0a` | **KEEP** | — |
| journey | market:costa-rica | Puntarenas → Paquera (Gulf of Nicoya) | `ics-b98ea23eee` | **KEEP** | — |
| journey | market:costa-rica | Gulf of Papagayo & Nicoya Peninsula — Costa Rica → | `rn-4ab58a9e0d63` | **KEEP** | — |
| journey | market:costa-rica | Gulf of Papagayo & Nicoya Peninsula — Costa Rica → | `rn-0931127fbf2f` | **KEEP** | — |
| featured | costa-rica/p1 | Gulf of Papagayo & Nicoya Peninsula — Costa Rica → | `rn-761106cfaa0a` | **KEEP** | — |
| featured | costa-rica/p1 | Puntarenas → Paquera | `ics-b98ea23eee` | **KEEP** | — |
| featured | costa-rica/p1 | Gulf of Papagayo & Nicoya Peninsula — Costa Rica → | `rn-fc0f6a62c378` | **KEEP** | — |
| featured | costa-rica/p2 | Liberia (LIR) gateway ↔ Nicoya Peninsula beach tow | `—` | **KEEP** | — |
| featured | costa-rica/p3 | Gulf of Papagayo & Nicoya Peninsula — Costa Rica → | `rn-761106cfaa0a` | **KEEP** | — |
| featured | costa-rica/p3 | Puntarenas → Paquera | `ics-b98ea23eee` | **KEEP** | — |
| featured | costa-rica/p3 | Gulf of Papagayo & Nicoya Peninsula — Costa Rica → | `rn-28283e0e27a4` | **KEEP** | — |
| journey | market:dominican-republic | Samaná town (Santa Bárbara) → Cayo Levantado | `rn-780e81cf832c` | **KEEP** | — |
| journey | market:dominican-republic | Samaná → Las Galeras | `rn-342daebb3603` | **KEEP** | — |
| journey | market:dominican-republic | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| journey | market:dominican-republic | Samaná Peninsula & Bay — Dominican Republic → Turk | `e__samana-dominican-republic__turks-caicos` | **KEEP** | — |
| featured | dominican-republic/p1 | Samaná Peninsula & Bay — Dominican Republic → Cayo | `rn-780e81cf832c` | **KEEP** | — |
| featured | dominican-republic/p1 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | dominican-republic/p1 | Samaná Peninsula & Bay — Dominican Republic → Saba | `rn-25bd003736cd` | **KEEP** | — |
| featured | dominican-republic/p2 | Samaná Peninsula & Bay — Dominican Republic → Los  | `rn-42f2340027cc` | **KEEP** | — |
| featured | dominican-republic/p3 | Samaná Peninsula & Bay — Dominican Republic → Cayo | `rn-780e81cf832c` | **KEEP** | — |
| featured | dominican-republic/p3 | Samaná Peninsula & Bay — Dominican Republic → Las  | `rn-342daebb3603` | **KEEP** | — |
| featured | dominican-republic/p3 | Samaná Peninsula & Bay — Dominican Republic → Cayo | `rn-780e81cf832c` | **KEEP** | — |
