# PTA Pair-Gap Table

Generated: 2026-07-01T01:52:07Z

## Fleet summary

| Metric | Value |
|--------|-------|
| authorities | 24 |
| boarding points | 401 |
| domestic pairs current | 207 |
| regional links | 12 |
| orphan bps | 144 |
| recommended hub spoke pairs | 144 |
| seal targets current | 219 |
| seal targets after expansion | 363 |
| published lines est sum | 48 |

## Per authority

| Authority | BPs | Pairs | Orphans | Pub~lines | Gap | Rec+ | Seal after | Action |
|-----------|-----|-------|---------|-----------|-----|------|------------|--------|
| transport-nsw | 31 | 8 | 22 | 10 | 2 | +22 | 30 | expand_hub_spoke |
| istanbul-sehir-hatlari | 28 | 10 | 17 | — | — | +17 | 27 | expand_hub_spoke |
| nyc-ferry | 25 | 8 | 16 | — | — | +16 | 24 | expand_hub_spoke |
| venice-actv | 26 | 8 | 16 | — | — | +16 | 24 | expand_hub_spoke |
| brisbane-citycat | 23 | 8 | 12 | — | — | +12 | 20 | expand_hub_spoke |
| thames-clippers | 24 | 8 | 12 | 4 | -4 | +12 | 20 | expand_hub_spoke |
| sf-bay-ferry | 17 | 10 | 7 | 6 | -4 | +7 | 17 | expand_hub_spoke |
| bangkok-chao-phraya | 17 | 9 | 6 | — | — | +6 | 15 | expand_hub_spoke |
| hamburg-hadag | 16 | 9 | 6 | — | — | +6 | 15 | expand_hub_spoke |
| wsf | 19 | 8 | 5 | 10 | 2 | +5 | 14 | expand_hub_spoke |
| auckland-ferries | 14 | 9 | 4 | — | — | +4 | 13 | expand_hub_spoke |
| kochi-water-metro | 16 | 10 | 4 | 16 | 6 | +4 | 14 | expand_hub_spoke |
| dubai-rta | 15 | 8 | 3 | — | — | +3 | 12 | review_orphans |
| stockholm-waxholm | 16 | 11 | 3 | — | — | +3 | 14 | review_orphans |
| abu-dhabi-itc | 15 | 8 | 2 | — | — | +2 | 12 | complete |
| bahrain-motc | 15 | 8 | 2 | — | — | +2 | 12 | complete |
| boston-mbta-ferry | 11 | 10 | 2 | 2 | -8 | +2 | 12 | complete |
| hong-kong | 16 | 10 | 2 | — | — | +2 | 13 | complete |
| mumbai-mmb | 13 | 9 | 1 | — | — | +1 | 10 | complete |
| qatar | 11 | 10 | 1 | — | — | +1 | 12 | complete |
| rakta | 7 | 6 | 1 | — | — | +1 | 8 | complete |
| lisbon-transtejo | 9 | 8 | 0 | — | — | +0 | 8 | complete |
| singapore-mpa | 11 | 8 | 0 | — | — | +0 | 11 | complete |
| vancouver-seabus | 6 | 6 | 0 | — | — | +0 | 6 | complete |

## Expansion detail (authorities with hub-spoke recs)

### Transport for NSW (`transport-nsw`)
- Hubs: `syd-circular-quay, syd-barangaroo`
- Orphans (22): Milsons Point Wharf, McMahons Point Wharf, Balmain East Wharf, Balmain (Thames St) Wharf, Drummoyne Wharf, Chiswick Wharf, Abbotsford Wharf, Cabarita Wharf…
- Recommended +22 hub-spoke pairs → seal targets 30

### İstanbul Şehir Hatları (City Lines) (`istanbul-sehir-hatlari`)
- Hubs: `sh-eminonu, sh-kadikoy`
- Orphans (17): Ortaköy, Beylerbeyi, Çengelköy, Kuzguncuk, Kanlıca, Anadolu Hisarı, Emirgan, İstinye…
- Recommended +17 hub-spoke pairs → seal targets 27

### NYC Ferry (`nyc-ferry`)
- Hubs: `nyc-wall-st-pier-11, nyc-east-34th`
- Orphans (16): East 90th Street (Manhattan), Corlears Hook (Manhattan), Stuyvesant Cove (Manhattan), Battery Park City (Manhattan), Midtown West / Pier 79 (Manhattan), Roosevelt Island, North Williamsburg (Brooklyn), South Williamsburg (Brooklyn)…
- Recommended +16 hub-spoke pairs → seal targets 24

### Venice Vaporetto (ACTV) (`venice-actv`)
- Hubs: `actv-burano, actv-lido-sme`
- Orphans (16): Piazzale Roma, Ferrovia (Santa Lucia), Rialto, Accademia, Ca' Rezzonico, San Tomà, Ca' d'Oro, San Marcuola…
- Recommended +16 hub-spoke pairs → seal targets 24

### Brisbane CityCat (`brisbane-citycat`)
- Hubs: `bcc-north-quay, bcc-riverside`
- Orphans (12): West End, Guyatt Park, Regatta, Milton, Maritime Museum, Thornton Street (Kangaroo Point), Dockside, Sydney Street (New Farm)…
- Recommended +12 hub-spoke pairs → seal targets 20

### Uber Boat by Thames Clippers (`thames-clippers`)
- Hubs: `ldn-canary-wharf, ldn-north-greenwich`
- Orphans (12): Wandsworth Riverside Quarter Pier, Plantation Wharf Pier, Chelsea Harbour Pier, Cadogan Pier (Chelsea), Vauxhall (St George Wharf) Pier, Millbank Pier, London Eye (Waterloo) Pier, Bankside Pier…
- Recommended +12 hub-spoke pairs → seal targets 20

### San Francisco Bay Ferry (`sf-bay-ferry`)
- Hubs: `sfbf-ferry-building, sfbf-oakland`
- Orphans (7): San Francisco – Pier 41, Mare Island, Berkeley Marina, Port of Redwood City, Antioch, Hercules, Martinez
- Recommended +7 hub-spoke pairs → seal targets 17

### Bangkok Chao Phraya River Transit (`bangkok-chao-phraya`)
- Hubs: `bkk-sathorn, bkk-nonthaburi`
- Orphans (6): Oriental (N1), Si Phraya (N3), Rachawong (N5), Memorial Bridge (N6), Rajinee (N7), Thewes (N15)
- Recommended +6 hub-spoke pairs → seal targets 15

### Hamburg Harbour Ferries (HADAG) (`hamburg-hadag`)
- Hubs: `ham-landungsbrucken, ham-finkenwerder`
- Orphans (6): Dockland (Fischereihafen), Neumühlen / Övelgönne, Ernst-August-Schleuse, Argentinienbrücke, Bubendey-Ufer, Waltershof
- Recommended +6 hub-spoke pairs → seal targets 15

### Washington State Ferries (`wsf`)
- Hubs: `wsf-seattle-colman, wsf-vashon`
- Orphans (5): Point Defiance (Tacoma), Tahlequah (south Vashon), Orcas Island, Lopez Island, Shaw Island
- Recommended +5 hub-spoke pairs → seal targets 14

### Auckland Ferries (Auckland Transport) (`auckland-ferries`)
- Hubs: `akl-downtown, akl-half-moon-bay`
- Orphans (4): Northcote Point (Te Onewa), West Harbour, Stanley Bay, Rakino Island
- Recommended +4 hub-spoke pairs → seal targets 13

### Kochi Water Metro (KMRL) (`kochi-water-metro`)
- Hubs: `kch-high-court, kch-vyttila`
- Orphans (4): Mulavukad North, Nettoor, Kumbalam, Eroor
- Recommended +4 hub-spoke pairs → seal targets 14

### Dubai RTA (`dubai-rta`)
- Hubs: `dubai-marina-station, dubai-harbour`
- Orphans (3): Deira Old Souq / Bur Dubai abra station (Creek mouth), Al Jaddaf Marine Station (upper Creek), Dubai Water Canal — Jumeirah/Safa
- Recommended +3 hub-spoke pairs → seal targets 12

### Stockholm Archipelago Ferries (Waxholmsbolaget) (`stockholm-waxholm`)
- Hubs: `stk-stromkajen, stk-vaxholm`
- Orphans (3): Slussen, Möja, Tynningö
- Recommended +3 hub-spoke pairs → seal targets 14

### Abu Dhabi ITC (`abu-dhabi-itc`)
- Hubs: `ad-corniche-breakwater, ad-marsa-mina`
- Orphans (2): Al Muneera (Al Raha Beach), Al Zeina (Al Raha Beach)
- Recommended +2 hub-spoke pairs → seal targets 12

### Bahrain MOTC (`bahrain-motc`)
- Hubs: `manama-bahrain-bay, saada-marina-muharraq`
- Orphans (2): The Avenues (Manama), Marassi / Northern Town
- Recommended +2 hub-spoke pairs → seal targets 12

### Boston Harbor Ferries (MBTA) (`boston-mbta-ferry`)
- Hubs: `bos-long-wharf, bos-hingham`
- Orphans (2): Rowes Wharf, Seaport (Fan Pier)
- Recommended +2 hub-spoke pairs → seal targets 12

### Hong Kong Transport Department (`hong-kong`)
- Hubs: `hk-central-piers, hk-mui-wo`
- Orphans (2): Wan Chai Ferry Pier, Kwun Tong Ferry Pier
- Recommended +2 hub-spoke pairs → seal targets 13

### Mumbai Water Transport (Maharashtra Maritime Board) (`mumbai-mmb`)
- Hubs: `mum-gateway, mum-belapur`
- Orphans (1): Worli
- Recommended +1 hub-spoke pairs → seal targets 10

### Qatar MOT (`qatar`)
- Hubs: `old-doha-port, corniche-ferry-stop`
- Orphans (1): West Bay / DECC waterfront
- Recommended +1 hub-spoke pairs → seal targets 12

### RAK RAKTA (`rakta`)
- Hubs: `rak-al-marjan-island, rak-al-hamra-marina`
- Orphans (1): Wynn Al Marjan Island arrival lagoon
- Recommended +1 hub-spoke pairs → seal targets 8

