# Proposal fidelity — uber

**Verdict:** TRIM
**Checked:** 2026-07-01T03:14:59Z

## Summary

- Items audited: 96
- KEEP: 94
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Dubai Marina → Downtown / Festival City | `—` | **KEEP** | — |
| journey | — | Miami (Brickell) → Miami Beach / Fisher Island | `—` | **KEEP** | — |
| journey | — | Malé (airport) → Resort islands | `—` | **KEEP** | — |
| featured | 1 | Howrah Ferry Ghat → Fairlie Place Ferry | `rn-97202b12d2ce` | **KEEP** | — |
| featured | 1 | Howrah Ferry Ghat → Millennium Park Jetty | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | 1 | Dakshineswar Ferry Ghat → Belur Math Ferry Ghat | `rn-b44cfaae1be2` | **KEEP** | — |
| featured | 2 | Fairlie Place Ferry → Bagbazar Ghat | `rn-46a91df66302` | **KEEP** | — |
| featured | 2 | Côte d'Azur Resort Marina (Heart of Europe) → Anan | `rn-af9d261fd724` | **KEEP** | — |
| featured | 2 | Sydney Harbour → Watsons Bay | `—` | **KEEP** | — |
| featured | 3 | Chennai Port WQIV Cruise Terminal → Marina Beach W | `rn-6e53a9fad2f1` | **KEEP** | — |
| featured | 3 | Molo Beverello (Naples) → Sorrento Marina Piccola | `rn-140626297ee9` | **KEEP** | — |
| featured | 3 | Port Hercule (Monaco) → Port de Villefranche-sur-M | `ics-4269303d3c` | **KEEP** | — |
| journey | market:mena | Dubai Marina → Downtown / Festival City | `—` | **KEEP** | — |
| journey | market:mena | Côte d'Azur Resort Marina (Heart of Europe) → Anan | `rn-af9d261fd724` | **KEEP** | — |
| journey | market:mena | Abu Dhabi Corniche → Saadiyat / Yas Island | `—` | **KEEP** | — |
| journey | market:mena | Dubai → Abu Dhabi | `e__uae__1b860507c38f` | **KEEP** | — |
| featured | mena/p1 | Ras Al Khaimah Harbour → RAK Corniche public pier  | `rn-2a5c2fe11732` | **KEEP** | — |
| featured | mena/p2 | Côte d'Azur Resort Marina (Heart of Europe) → Anan | `rn-af9d261fd724` | **KEEP** | — |
| featured | mena/p3 | Dubai island Marina Slipway → Yas Marina Abu Dhabi | `e__uae__1b860507c38f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai island Marina Slipway' |
| featured | mena/p4 | A continuous in-app water tier along the whole Gul | `—` | **KEEP** | — |
| journey | market:miami | Nassau & The Bahamas → Miami | `—` | **KEEP** | — |
| journey | market:miami | Palm Beach / Treasure Coast → Miami | `—` | **KEEP** | — |
| journey | market:miami | Miami → Nassau & The Bahamas | `—` | **KEEP** | — |
| journey | market:miami | West Palm Beach → Palm Beach / Singer Island | `—` | **KEEP** | — |
| featured | miami/p1 | Miami ↔ Key West | `—` | **KEEP** | — |
| featured | miami/p2 | Miami ↔ Key West | `—` | **KEEP** | — |
| featured | miami/p3 | Miami ↔ Key West | `—` | **KEEP** | — |
| featured | miami/p4 | Miami ↔ Key West | `—` | **KEEP** | — |
| featured | miami/p5 | Miami ↔ Key West | `—` | **KEEP** | — |
| journey | market:bay-area | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| journey | market:bay-area | SF → Sausalito / Tiburon | `—` | **KEEP** | — |
| journey | market:bay-area | SF → Redwood City / South Bay | `—` | **KEEP** | — |
| journey | market:bay-area | SF → Berkeley / Richmond | `—` | **KEEP** | — |
| featured | bay-area/p1 | San Francisco Bay Area → San Francisco Bay Area | `—` | **KEEP** | — |
| featured | bay-area/p2 | SF ↔ Redwood City | `—` | **KEEP** | — |
| featured | bay-area/p2 | SF ↔ Berkeley | `—` | **KEEP** | — |
| featured | bay-area/p2 | Oakland ↔ Peninsula | `—` | **KEEP** | — |
| featured | bay-area/p3 | whole-Bay mesh | `—` | **KEEP** | — |
| featured | bay-area/p3 | Larkspur ↔ SF ↔ South Bay | `—` | **KEEP** | — |
| featured | bay-area/p3 | Alameda ↔ Peninsula | `—` | **KEEP** | — |
| journey | market:hawaii | Honolulu / Oʻahu → Maui County (Maui · Lānaʻi · Mo | `—` | **KEEP** | — |
| journey | market:hawaii | Hawaiʻi Island (Kona · Kohala · Hilo) → Maui Count | `—` | **KEEP** | — |
| journey | market:hawaii | Kauaʻi → Honolulu / Oʻahu | `—` | **KEEP** | — |
| journey | market:hawaii | Lahaina Harbor → Manele Small Boat Harbor | `ics-e82d2ae202ed` | **KEEP** | — |
| featured | hawaii/p1 | Lahaina Harbor → Manele Small Boat Harbor | `ics-e82d2ae202ed` | **KEEP** | — |
| featured | hawaii/p2 | Nāwiliwili Harbor → Honolulu Harbor | `ics-42fbb80da505` | **KEEP** | — |
| featured | hawaii/p3 | Honolulu / Oʻahu → Maui County (Maui · Lānaʻi · Mo | `—` | **KEEP** | — |
| journey | market:mediterranean | Athens (Flisvos / Piraeus) → Hydra, Saronic Gulf | `—` | **KEEP** | — |
| journey | market:mediterranean | Mykonos → Santorini | `—` | **KEEP** | — |
| journey | market:mediterranean | Split → Hvar Town | `rn-cc40790a3078` | **KEEP** | — |
| journey | market:mediterranean | Split Ferry Port → Ferry - Šolta | `rn-8af39f1da94d` | **KEEP** | — |
| featured | mediterranean/p1 | Split Ferry Port → Ferry - Šolta | `rn-8af39f1da94d` | **KEEP** | — |
| featured | mediterranean/p2 | ACI Marina Trogir → Hvar Town Harbour | `rn-7c1e7f62f283` | **KEEP** | — |
| featured | mediterranean/p3 | E1 Gate Ferry to Kos - Piraeus Port → Skala Marina | `rn-16fa8284adf1` | **KEEP** | — |
| journey | market:sydney-nsw | Sydney Harbour → Sydney Harbour | `—` | **KEEP** | — |
| journey | market:sydney-nsw | Sydney Harbour → Sydney Harbour | `—` | **KEEP** | — |
| journey | market:sydney-nsw | Sydney Harbour → Watsons Bay / Eastern beaches | `—` | **KEEP** | — |
| journey | market:sydney-nsw | Sydney Harbour → Sydney Harbour | `—` | **KEEP** | — |
| featured | sydney-nsw/p1 | Sydney Harbour → Sydney Harbour | `—` | **KEEP** | — |
| featured | sydney-nsw/p2 | Sydney Harbour → Sydney Harbour | `—` | **KEEP** | — |
| featured | sydney-nsw/p3 | Sydney Harbour → Watsons Bay | `—` | **KEEP** | — |
| journey | market:brazil-latam | Rio (Praca XV) → Niteroi | `—` | **KEEP** | — |
| journey | market:brazil-latam | Rio → Buzios | `—` | **KEEP** | — |
| journey | market:brazil-latam | Angra dos Reis + Ilha Grande (Costa Verde) → Angra | `—` | **KEEP** | — |
| journey | market:brazil-latam | Florianópolis & Santa Catarina → Florianópolis & S | `—` | **KEEP** | — |
| featured | brazil-latam/p1 | Florianópolis & Santa Catarina → Florianópolis & S | `ics-2df0a1d37f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Florianópolis & Santa Catari |
| featured | brazil-latam/p2 | Angra dos Reis + Ilha Grande (Costa Verde) → Angra | `—` | **KEEP** | — |
| featured | brazil-latam/p3 | Rio (Praca XV) ↔ Niteroi | `—` | **KEEP** | — |
| journey | market:italy-luxury | Naples → Capri | `rn-01c592b8150e` | **KEEP** | — |
| journey | market:italy-luxury | Porto di Pozzuoli → Marina Grande (Capri) | `rn-2508d7811cef` | **KEEP** | — |
| journey | market:italy-luxury | Porto di Pozzuoli → Marina Grande (Capri) | `rn-2508d7811cef` | **KEEP** | — |
| journey | market:italy-luxury | Amalfi Coast / Bay of Naples → Costa Smeralda, Sar | `—` | **KEEP** | — |
| featured | italy-luxury/p1 | Molo Beverello (Naples) → Marina Grande (Capri) | `rn-01c592b8150e` | **KEEP** | — |
| featured | italy-luxury/p2 | Porto di Pozzuoli → Marina Grande (Capri) | `rn-2508d7811cef` | **KEEP** | — |
| featured | italy-luxury/p3 | Amalfi Coast → Costa Smeralda & Sardinia | `—` | **KEEP** | — |
| journey | market:cote-dazur | Nice (Airport / Port) → Monaco | `rn-d66efc6795b3` | **KEEP** | — |
| journey | market:cote-dazur | Cannes → Saint-Tropez | `rn-3f177aa9d890` | **KEEP** | — |
| journey | market:cote-dazur | Port Hercule (Monaco) → Port de Villefranche-sur-M | `—` | **KEEP** | — |
| journey | market:cote-dazur | Costa Smeralda & Sardinia → Côte d'Azur (French Ri | `—` | **KEEP** | — |
| featured | cote-dazur/p1 | Port Hercule (Monaco) → Port de Villefranche-sur-M | `—` | **KEEP** | — |
| featured | cote-dazur/p2 | Nice Port → Port Hercule (Monaco) | `rn-d66efc6795b3` | **KEEP** | — |
| featured | cote-dazur/p3 | Vieux Port (Cannes) → Port de Saint-Tropez | `rn-3f177aa9d890` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Fairlie Place Ferry → Bagbazar Ghat | `rn-46a91df66302` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p1 | Howrah Ferry Ghat → Fairlie Place Ferry | `rn-97202b12d2ce` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p2 | Howrah Ferry Ghat → Millennium Park Jetty | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Dakshineswar Ferry Ghat → Belur Math Ferry Ghat | `rn-b44cfaae1be2` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Napier Bridge → Kovalam Creek | `rn-6d907a5eae57` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai Port WQIV Cruise Terminal → Marina Beach W | `rn-6e53a9fad2f1` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai → Cuddalore Port | `rn-659673f9bc4d` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai Port WQIV Cruise Terminal → Puducherry Por | `rn-63ec78cd9afb` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p1 | Chennai Port WQIV Cruise Terminal → Marina Beach W | `rn-6e53a9fad2f1` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p2 | Napier Bridge → Kovalam Creek | `rn-6d907a5eae57` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p3 | Chennai Port WQIV Cruise Terminal → Puducherry Por | `rn-63ec78cd9afb` | **KEEP** | — |
