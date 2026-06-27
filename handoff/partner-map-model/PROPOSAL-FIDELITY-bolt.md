# Proposal fidelity — bolt

**Verdict:** REWRITE
**Checked:** 2026-06-27T15:00:01Z

## Summary

- Items audited: 271
- KEEP: 144
- DROP: 112
- DEFER: 5
- TRIM/REWRITE: 10
- BP-binding errors: 112

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Athens → Hydra (Saronic) | `—` | **KEEP** | — |
| journey | — | Split → Hvar | `rn-cc40790a3078` | **TRIM** | geometry_preview: interior_land_km=5.09 (threshold 0.4) |
| journey | — | Nice Airport → Monaco | `—` | **KEEP** | — |
| journey | — | Dubai Marina → Downtown Creek | `gcn-0ca7f3ffe7-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Marina' → 'Downtown Cr |
| journey | — | Cais do Sodré (Lisbon) → Cacilhas (Almada) | `—` | **KEEP** | — |
| journey | — | Jeddah Corniche → Jeddah Yacht Club & Marina | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | 1 | Athens ↔ Saronic islands | `—` | **KEEP** | — |
| featured | 1 | Split ↔ Hvar | `rn-7c1e7f62f283` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'ACI Marina ; geometry_preview: interior_land_km=12.94 (threshold 0.4) |
| featured | 2 | Capri ↔ Amalfi | `rn-2508d7811cef` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Porto di Po |
| featured | 2 | Mykonos ↔ Santorini | `rn-cb0ec9d194ca` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Mykonos & t |
| featured | 3 | Dubai ↔ Abu Dhabi | `gcn-4ae479b872-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'bp-933fd357; geometry_preview: interior_land_km=4.38 (threshold 0.4) |
| journey | market:croatia | Split → Trogir (via Čiovo) | `rn-97acf274a21e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Trogir (via Čiovo) |
| journey | market:croatia | Dubrovnik → Elaphiti Islands (Lopud / Šipan / Kolo | `rn-86a2678bad4c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubrovnik' → 'Elaphiti Islan; distance_honesty: card 8.0nm vs route 4.2nm (90% delta) |
| journey | market:croatia | Split → Šolta (Rogač) | `rn-8433d89475d9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Šolta (Rogač)' vs  |
| journey | market:croatia | Dubrovnik → Cavtat | `rn-27a8218aa694` | **TRIM** | distance_honesty: card 9.0nm vs route 6.2nm (45% delta) |
| journey | market:croatia | Split → Brač (Bol) | `rn-b3d4e2d907b1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Brač (Bol)' vs rou; distance_honesty: card 12.0nm vs route 21.1nm (43% delta) |
| journey | market:croatia | Dubrovnik → Kotor (Montenegro) | `—` | **KEEP** | — |
| featured | croatia/p1 | Split → Trogir (via Čiovo) | `rn-97acf274a21e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Trogir (via Čiovo) |
| featured | croatia/p1 | Dubrovnik → Elaphiti Islands (Lopud / Šipan / Kolo | `rn-86a2678bad4c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubrovnik' → 'Elaphiti Islan; distance_honesty: card 8.0nm vs route 4.2nm (90% delta) |
| featured | croatia/p1 | Split → Šolta (Rogač) | `rn-8433d89475d9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Šolta (Rogač)' vs  |
| featured | croatia/p2 | Dubrovnik → Cavtat | `rn-27a8218aa694` | **TRIM** | distance_honesty: card 9.0nm vs route 6.2nm (45% delta) |
| featured | croatia/p2 | Dubrovnik Airport (Čilipi) → Dubrovnik / Cavtat (r | `rn-e5f8515b10ff` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubrovnik Airport (Čilipi)' ; distance_honesty: card 10.0nm vs route 20.1nm (50% delta) (+1) |
| featured | croatia/p2 | Split → Brač (Bol) | `rn-b3d4e2d907b1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split' → 'Brač (Bol)' vs rou; distance_honesty: card 12.0nm vs route 21.1nm (43% delta) |
| featured | croatia/p2 | Split Airport (Resnik / Trogir) → Split / Brač / H | `rn-1270930dd61b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Split Airport (Resnik / Trog; distance_honesty: card 12.0nm vs route 22.2nm (46% delta) |
| featured | croatia/p2 | Zadar (Murter / Biograd gateway) → Kornati Nationa | `—` | **KEEP** | — |
| featured | croatia/p2 | Split → Hvar | `rn-cc40790a3078` | **DEFER** | geometry_preview: interior_land_km=5.09 (threshold 0.4) |
| featured | croatia/p3 | Split ↔ Trogir (via Čiovo) | `—` | **KEEP** | — |
| journey | market:east-africa | Dar es Salaam → Stone Town (Zanzibar) | `rn-46bee519109a` | **KEEP** | — |
| journey | market:east-africa | Mombasa → Diani / Ukunda | `—` | **KEEP** | — |
| featured | east-africa/pNone | Dar es Salaam → Stone Town | `rn-46bee519109a` | **KEEP** | — |
| featured | east-africa/pNone | Mombasa → Diani | `ics-0b3b436e41` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mombasa' → 'Diani' vs route  |
| journey | market:egypt | El Gouna (internal lagoon) → El Gouna Downtown / A | `rn-cf19a27c2e8a` | **KEEP** | — |
| journey | market:egypt | Cairo - Maadi → Cairo - Zamalek / Downtown | `rn-4d2d789c04ad` | **KEEP** | — |
| journey | market:egypt | Hurghada → Giftun Island (Orange Bay / Mahmya) | `gcn-73d7e2f19c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Hurghada' → 'Giftun Island ( |
| journey | market:egypt | Hurghada → Sahl Hasheesh | `gcn-73d7e2f19c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Hurghada' → 'Sahl Hasheesh'  |
| journey | market:egypt | Hurghada → El Gouna | `rn-abf46355ef7f` | **TRIM** | geometry_preview: interior_land_km=8.63 (threshold 0.4) |
| featured | egypt/p1 | El Gouna (internal lagoon) → El Gouna Downtown / A | `rn-cf19a27c2e8a` | **KEEP** | — |
| featured | egypt/p1 | Cairo - Maadi → Cairo - Zamalek / Downtown | `rn-4d2d789c04ad` | **KEEP** | — |
| featured | egypt/p1 | Hurghada → Giftun Island (Orange Bay / Mahmya) | `gcn-73d7e2f19c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Hurghada' → 'Giftun Island ( |
| featured | egypt/p2 | Hurghada → Sahl Hasheesh | `gcn-73d7e2f19c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Hurghada' → 'Sahl Hasheesh'  |
| featured | egypt/p2 | Greater Cairo - Maspero (Downtown) → Greater Cairo | `rn-148c41cefa55` | **KEEP** | — |
| featured | egypt/p2 | Hurghada → El Gouna | `rn-abf46355ef7f` | **DEFER** | geometry_preview: interior_land_km=8.63 (threshold 0.4) |
| featured | egypt/p2 | Sharm El Sheikh → Ras Mohammed / Tiran reefs | `gcn-73d7e2f19c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Sharm El Sheikh' → 'Ras Moha |
| featured | egypt/p2 | Hurghada → Soma Bay | `rn-fbbb4fae5cbe` | **DEFER** | geometry_preview: interior_land_km=13.51 (threshold 0.4) |
| featured | egypt/p2 | Sharm El Sheikh → Dahab | `gcn-73d7e2f19c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Sharm El Sheikh' → 'Dahab' v |
| featured | egypt/p3 | in-app journeys | `—` | **KEEP** | — |
| journey | market:estonia | Tallinn Old City Harbour → Pirita Marina | `rn-889f513853ae` | **KEEP** | — |
| journey | market:estonia | Tallinn → Prangli | `rn-aeb90d25487f` | **KEEP** | — |
| journey | market:estonia | Tallinn → Viimsi | `rn-d6554a0bc2c8` | **KEEP** | — |
| journey | market:estonia | Tallinn → Kakumäe | `rn-44d0d47fe330` | **KEEP** | — |
| journey | market:estonia | Tallinn → Helsinki | `rn-5ad3ac0aa657` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Tallinn' → 'Helsinki' vs rou; distance_honesty: card 43.0nm vs route 203.8nm (79% delta) |
| featured | estonia/p1 | Tallinn Old City Harbour → Pirita Marina | `rn-889f513853ae` | **KEEP** | — |
| featured | estonia/p1 | Tallinn → Prangli | `rn-aeb90d25487f` | **KEEP** | — |
| featured | estonia/p1 | Tallinn → Viimsi | `rn-d6554a0bc2c8` | **KEEP** | — |
| featured | estonia/p2 | Tallinn → Kakumäe | `rn-44d0d47fe330` | **KEEP** | — |
| featured | estonia/p2 | Tallinn → Aegna | `—` | **KEEP** | — |
| featured | estonia/p2 | Tallinn → Naissaar | `rn-16666eaf140c` | **KEEP** | — |
| featured | estonia/p2 | Tallinn → Helsinki | `rn-5ad3ac0aa657` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Tallinn' → 'Helsinki' vs rou; distance_honesty: card 43.0nm vs route 203.8nm (79% delta) |
| featured | estonia/p3 | Tallinn → Stockholm | `rn-44d0d47fe330` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Tallinn' → 'Stockholm' vs ro |
| journey | market:finland | Helsinki → Lonna | `rn-312e87d88d71` | **KEEP** | — |
| journey | market:finland | Helsinki Market Square → Suomenlinna | `rn-ca17345bf0e8` | **KEEP** | — |
| journey | market:finland | Helsinki → Pihlajasaari | `rn-c470fde6e58f` | **KEEP** | — |
| journey | market:finland | Helsinki → Korkeasaari (Zoo island) | `rn-2025e138f6c3` | **KEEP** | — |
| journey | market:finland | Helsinki → Kruunuvuorenranta (Laajasalo) | `rn-4ab75813e3cc` | **KEEP** | — |
| journey | market:finland | Helsinki → Tallinn | `rn-5ad3ac0aa657` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Helsinki' → 'Tallinn' vs rou; distance_honesty: card 43.0nm vs route 203.8nm (79% delta) |
| featured | finland/p1 | Helsinki → Lonna | `rn-312e87d88d71` | **KEEP** | — |
| featured | finland/p1 | Helsinki Market Square → Suomenlinna | `rn-ca17345bf0e8` | **KEEP** | — |
| featured | finland/p1 | Helsinki → Pihlajasaari | `rn-c470fde6e58f` | **KEEP** | — |
| featured | finland/p2 | Helsinki → Korkeasaari (Zoo island) | `rn-2025e138f6c3` | **KEEP** | — |
| featured | finland/p2 | Helsinki → Kruunuvuorenranta (Laajasalo) | `rn-4ab75813e3cc` | **KEEP** | — |
| featured | finland/p2 | Helsinki → Vallisaari | `rn-8523ec0a5309` | **KEEP** | — |
| featured | finland/p2 | Helsinki → Porvoo | `rn-a02134ddb302` | **DEFER** | geometry_preview: interior_land_km=15.98 (threshold 0.4) |
| featured | finland/p2 | Helsinki → Tallinn | `rn-5ad3ac0aa657` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Helsinki' → 'Tallinn' vs rou; distance_honesty: card 43.0nm vs route 203.8nm (79% delta) |
| featured | finland/p3 | Helsinki → Stockholm | `rn-db397ab37430` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Helsinki' → 'Stockholm' vs r |
| journey | market:france-riviera | Cannes → Ile Sainte-Marguerite (Iles de Lerins) | `rn-cb30f287dc0d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cannes' → 'Ile Sainte-Margue |
| journey | market:france-riviera | Menton → Monaco | `rn-5fb120384595` | **KEEP** | — |
| journey | market:france-riviera | Villefranche-sur-Mer → Monaco | `rn-c0f2e69be06c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Villefranche-sur-Mer' → 'Mon |
| journey | market:france-riviera | Antibes → Cannes | `rn-cb30f287dc0d` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Antibes' → 'Cannes' vs route |
| journey | market:france-riviera | Nice Airport → Monaco | `rn-48bac1363efe` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nice Airport' → 'Monaco' vs  |
| journey | market:france-riviera | Monaco → Sanremo | `rn-6af10d73458f` | **KEEP** | — |
| journey | market:france-riviera | St-Tropez → Pampelonne | `—` | **KEEP** | — |
| journey | market:france-riviera | Cannes → St-Tropez | `rn-186b89d0af31` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cannes' → 'St-Tropez' vs rou |
| journey | market:france-riviera | Nice → St-Tropez | `rn-d1e8ad221645` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nice' → 'St-Tropez' vs route |
| featured | france-riviera/p1 | Cannes → Ile Sainte-Marguerite (Iles de Lerins) | `ics-529325c5eb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cannes' → 'Ile Sainte-Margue; distance_honesty: card 1.5nm vs route 3.0nm (50% delta) |
| featured | france-riviera/p1 | Antibes → Cannes | `rn-3fab58bb5f82` | **KEEP** | — |
| featured | france-riviera/p2 | Menton → Monaco | `rn-5fb120384595` | **KEEP** | — |
| featured | france-riviera/p2 | Villefranche-sur-Mer → Monaco | `rn-c0f2e69be06c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Villefranche-sur-Mer' → 'Mon |
| featured | france-riviera/p2 | Nice → Monaco | `rn-c0f2e69be06c` | **KEEP** | — |
| featured | france-riviera/p2 | Nice Airport → Monaco | `rn-48bac1363efe` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nice Airport' → 'Monaco' vs  |
| featured | france-riviera/p2 | Nice Airport → Cannes | `rn-0e2ba6e5ba2f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nice Airport' → 'Cannes' vs ; distance_honesty: card 9.0nm vs route 18.5nm (51% delta) |
| featured | france-riviera/p2 | Nice → Cannes | `rn-8289390c6bad` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nice' → 'Cannes' vs route 'N |
| featured | france-riviera/p2 | Monaco → Sanremo | `rn-6af10d73458f` | **KEEP** | — |
| featured | france-riviera/p3 | Monaco → Portofino | `rn-c0f2e69be06c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Monaco' → 'Portofino' vs rou; distance_honesty: card 85.0nm vs route 7.0nm (1114% delta) |
| featured | france-riviera/p3 | Cannes → St-Tropez | `rn-186b89d0af31` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cannes' → 'St-Tropez' vs rou |
| featured | france-riviera/p3 | Nice → St-Tropez | `rn-d1e8ad221645` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nice' → 'St-Tropez' vs route |
| featured | france-riviera/p3 | St-Tropez → Pampelonne | `—` | **KEEP** | — |
| journey | market:greece | Mykonos Town → Delos | `rn-6be8bfbbdcd8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mykonos Town' → 'Delos' vs r |
| journey | market:greece | Glyfada (Athens Riviera) → Vouliagmeni (Astir reso | `rn-c2f16c0e44f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Glyfada (Athens Riviera)' →  |
| journey | market:greece | Naxos → Paros | `rn-cb5de99552b4` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Naxos' → 'Paros' vs route 'M; distance_honesty: card 6.0nm vs route 8.9nm (33% delta) |
| journey | market:greece | Athens (Piraeus) → Glyfada (Athens Riviera) | `rn-89552c9786ec` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Athens (Piraeus)' → 'Glyfada |
| journey | market:greece | Rhodes → Marmaris (Turkey) | `rn-a95f11ef9a7e` | **KEEP** | — |
| featured | greece/p1 | Mykonos Town → Delos | `rn-6be8bfbbdcd8` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mykonos Town' → 'Delos' vs r |
| featured | greece/p1 | Glyfada (Athens Riviera) → Vouliagmeni (Astir reso | `rn-c2f16c0e44f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Glyfada (Athens Riviera)' →  |
| featured | greece/p1 | Naxos → Paros | `rn-cb5de99552b4` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Naxos' → 'Paros' vs route 'M; distance_honesty: card 6.0nm vs route 8.9nm (33% delta) |
| featured | greece/p2 | Athens (Piraeus) → Glyfada (Athens Riviera) | `rn-89552c9786ec` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Athens (Piraeus)' → 'Glyfada |
| featured | greece/p2 | Athens (Piraeus) → Aegina | `ics-0c4a9cc9b3` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Athens (Piraeus)' → 'Aegina' |
| featured | greece/p2 | Santorini (Thira) → Ios | `rn-be97f62a4421` | **TRIM** | distance_honesty: card 17.0nm vs route 0.3nm (5567% delta) |
| featured | greece/p2 | Athens (Piraeus) → Agistri (Saronic) | `rn-16fa8284adf1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Athens (Piraeus)' → 'Agistri |
| featured | greece/p2 | Mykonos → Paros | `rn-9de6a1c0748a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mykonos' → 'Paros' vs route  |
| featured | greece/p2 | Rhodes → Marmaris (Turkey) | `—` | **KEEP** | — |
| featured | greece/p3 | Mykonos → Santorini (Thira) | `—` | **KEEP** | — |
| journey | market:ireland | Dalkey → Dalkey Island | `—` | **KEEP** | — |
| journey | market:ireland | Howth → Ireland's Eye | `—` | **KEEP** | — |
| journey | market:ireland | Dublin Docklands → Dún Laoghaire | `rn-455eede91b5a` | **KEEP** | — |
| journey | market:ireland | Dublin City (Docklands) → Howth | `rn-455eede91b5a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dublin City (Docklands)' → ' |
| journey | market:ireland | Dublin Port → Holyhead (Wales) | `—` | **KEEP** | — |
| featured | ireland/p1 | Dalkey → Dalkey Island | `—` | **KEEP** | — |
| featured | ireland/p1 | Howth → Ireland's Eye | `—` | **KEEP** | — |
| featured | ireland/p1 | Dublin Docklands → Dún Laoghaire | `rn-455eede91b5a` | **KEEP** | — |
| featured | ireland/p2 | Dublin City (Docklands) → Howth | `rn-455eede91b5a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dublin City (Docklands)' → ' |
| featured | ireland/p2 | Dun Laoghaire → Howth | `rn-12e7db59f876` | **KEEP** | — |
| featured | ireland/p2 | Dublin City (Docklands) → Dalkey / Killiney | `—` | **KEEP** | — |
| featured | ireland/p2 | Dublin Port → Holyhead (Wales) | `—` | **KEEP** | — |
| featured | ireland/p3 | Dalkey ↔ Dalkey Island | `—` | **KEEP** | — |
| journey | market:italy | Venice → Lido | `rn-093619ef734a` | **KEEP** | — |
| journey | market:italy | San Marco → Murano / Burano | `rn-3483f535e23c` | **KEEP** | — |
| journey | market:italy | Santa Margherita Ligure → Portofino | `rn-104bef78acf7` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Santa Margherita Ligure' → '; distance_honesty: card 2.0nm vs route 13.0nm (85% delta) |
| journey | market:italy | Positano → Amalfi | `ics-8302248934` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Positano' → 'Amalfi' vs rout |
| journey | market:italy | Sorrento → Capri | `rn-41ee5cb908d0` | **KEEP** | — |
| featured | italy/p1 | Venice → Lido | `—` | **KEEP** | — |
| featured | italy/p1 | San Marco → Murano / Burano | `—` | **KEEP** | — |
| featured | italy/p1 | Santa Margherita Ligure → Portofino | `rn-104bef78acf7` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Santa Margherita Ligure' → '; distance_honesty: card 2.0nm vs route 13.0nm (85% delta) |
| featured | italy/p2 | Positano → Amalfi | `ics-8302248934` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Positano' → 'Amalfi' vs rout |
| featured | italy/p2 | Venice Marco Polo → San Marco | `—` | **KEEP** | — |
| featured | italy/p2 | Capri → Positano | `ics-9546e52c39` | **KEEP** | — |
| featured | italy/p2 | Sorrento → Capri | `rn-41ee5cb908d0` | **KEEP** | — |
| featured | italy/p2 | Naples → Procida | `rn-bbc6263b4a59` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Naples' → 'Procida' vs route; distance_honesty: card 12.0nm vs route 7.5nm (60% delta) |
| featured | italy/p2 | Como → Bellagio | `rn-f954254a35c6` | **KEEP** | — |
| featured | italy/p3 | Venice ↔ Lido | `—` | **KEEP** | — |
| journey | market:nigeria | CMS / Marina (Lagos Island) → Victoria Island | `—` | **KEEP** | — |
| journey | market:nigeria | Osborne (Ikoyi) → CMS / Marina | `—` | **KEEP** | — |
| journey | market:nigeria | CMS / Marina → Apapa | `—` | **KEEP** | — |
| journey | market:nigeria | CMS / Marina → Ikorodu | `—` | **KEEP** | — |
| journey | market:nigeria | Lekki / VI → Epe (Lekki Free Zone axis) | `—` | **KEEP** | — |
| featured | nigeria/p1 | CMS / Marina → Victoria Island | `—` | **KEEP** | — |
| featured | nigeria/p1 | Osborne (Ikoyi) → CMS / Marina | `—` | **KEEP** | — |
| featured | nigeria/p1 | CMS / Marina → Apapa | `—` | **KEEP** | — |
| featured | nigeria/p2 | CMS / Marina → Ikorodu | `—` | **KEEP** | — |
| featured | nigeria/p2 | Victoria Island → Lekki Phase 1 | `—` | **KEEP** | — |
| featured | nigeria/p2 | Falomo / Five Cowries (Ikoyi) → Victoria Island | `—` | **KEEP** | — |
| featured | nigeria/p3 | Lekki / VI → Epe (Lekki Free Zone axis) | `—` | **KEEP** | — |
| featured | nigeria/p3 | CMS / Marina → Badagry | `—` | **KEEP** | — |
| journey | market:portugal | Porto (Cais da Ribeira) → Vila Nova de Gaia (Cais  | `rn-0db0c9859f5c` | **KEEP** | — |
| journey | market:portugal | Vila Real de Santo Antonio (Portugal) → Ayamonte ( | `rn-bd10456904cc` | **KEEP** | — |
| journey | market:portugal | Lagos → Ponta da Piedade | `rn-67dc105ba6e9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Lagos' → 'Ponta da Piedade'  |
| journey | market:portugal | Cais do Sodré (Lisbon) → Cacilhas (Almada) | `ics-a1f9af348e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cais do Sodré (Lisbon)' → 'C |
| journey | market:portugal | Belem (Lisbon) → Trafaria / Porto Brandao (Almada) | `ics-6b939c627f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Belem (Lisbon)' → 'Trafaria  |
| featured | portugal/p1 | Porto (Cais da Ribeira) → Vila Nova de Gaia (Cais  | `rn-20d8de578b2f` | **KEEP** | — |
| featured | portugal/p1 | Vila Real de Santo Antonio (Portugal) → Ayamonte ( | `rn-2f31310c4e84` | **KEEP** | — |
| featured | portugal/p1 | Lagos → Ponta da Piedade | `rn-f2aa06497c53` | **TRIM** | distance_honesty: card 1.2nm vs route 1.8nm (33% delta) |
| featured | portugal/p2 | Cais do Sodré (Lisbon) → Cacilhas (Almada) | `ics-a1f9af348e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cais do Sodré (Lisbon)' → 'C |
| featured | portugal/p2 | Belem (Lisbon) → Trafaria / Porto Brandao (Almada) | `ics-6b939c627f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Belem (Lisbon)' → 'Trafaria  |
| featured | portugal/p2 | Olhao → Culatra / Farol | `rn-7e047d3229fc` | **KEEP** | — |
| featured | portugal/p2 | Faro → Ilha Deserta (Barreta) | `rn-cd1337338a68` | **KEEP** | — |
| featured | portugal/p2 | Cais do Sodre (Lisbon) → Seixal | `rn-1cfa049d2707` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Cais do Sodre (Lisbon)' → 'S; geometry_preview: interior_land_km=3.75 (threshold 0.4) |
| featured | portugal/p2 | Terreiro do Paco (Lisbon) → Barreiro | `rn-a4d791eb5afd` | **KEEP** | — |
| featured | portugal/p3 | Porto (Cais da Ribeira) ↔ Vila Nova de Gaia (Cais  | `rn-1cfa049d2707` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Cais do Sod; geometry_preview: interior_land_km=3.75 (threshold 0.4) |
| journey | market:qatar | Lusail Marina → The Pearl | `rn-30d3fa93ca0e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Lusail Marina' → 'The Pearl' |
| journey | market:qatar | Doha Corniche → The Pearl | `rn-f15bb66e8e87` | **KEEP** | — |
| journey | market:qatar | The Pearl-Qatar (Marsa Arabia) → Doha Corniche / O | `rn-44cec9c94d4c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'The Pearl-Qatar (Marsa Arabi |
| journey | market:qatar | Doha → Banana Island | `gcn-de7142cf37-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Doha' → 'Banana Island' vs r |
| featured | qatar/p1 | Lusail Marina → The Pearl | `rn-79da51f0117a` | **TRIM** | distance_honesty: card 1.5nm vs route 2.1nm (29% delta) |
| featured | qatar/p1 | Doha Corniche → The Pearl | `rn-44cec9c94d4c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Doha Corniche' → 'The Pearl' |
| featured | qatar/p1 | The Pearl-Qatar (Marsa Arabia) → Doha Corniche / O | `rn-44cec9c94d4c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'The Pearl-Qatar (Marsa Arabi |
| featured | qatar/p2 | Doha → Banana Island | `gcn-de7142cf37-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Doha' → 'Banana Island' vs r |
| featured | qatar/p2 | Doha (Al Shyoukh Terminal) → Banana Island Resort  | `gcn-de7142cf37-bolt` | **KEEP** | — |
| featured | qatar/p2 | West Bay / Corniche (Doha) → Lusail Marina & Place | `rn-766596b9e733` | **DROP** | bp_binding: labels ≠ route endpoints: card 'West Bay / Corniche (Doha)'  |
| featured | qatar/p2 | Doha → Lusail Marina | `rn-766596b9e733` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Doha' → 'Lusail Marina' vs r |
| featured | qatar/p2 | Al Wakrah → Banana Island | `rn-0b99edfc9e67` | **KEEP** | — |
| featured | qatar/p2 | Doha → Al Wakrah Marina | `rn-1066679a7f79` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Doha' → 'Al Wakrah Marina' v |
| featured | qatar/p3 | Doha (Lusail Marina) → Manama (Bahrain Financial H | `gcn-7aa2645694-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Doha (Lusail Marina)' → 'Man |
| journey | market:ksa-commercial | Jeddah Corniche → Jeddah Central (PIF waterfront) | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| journey | market:ksa-commercial | Jeddah Corniche → Jeddah Yacht Club & Marina | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| journey | market:ksa-commercial | Khobar Corniche → Half Moon Bay | `gcn-adcdd3d09c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Khobar Corniche' → 'Half Moo |
| journey | market:ksa-commercial | Dammam → Tarout Island / Qatif | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dammam' → 'Tarout Island / Q |
| journey | market:ksa-commercial | Khobar / Dammam → Manama, Bahrain | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Khobar / Dammam' → 'Manama,  |
| featured | ksa-commercial/p1 | Jeddah Corniche → Jeddah Central (PIF waterfront) | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | ksa-commercial/p1 | Jeddah Corniche → Jeddah Yacht Club & Marina | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | ksa-commercial/p1 | Jeddah Corniche → Obhur Creek marina belt | `gcn-adcdd3d09c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Jeddah Corniche' → 'Obhur Cr |
| featured | ksa-commercial/p2 | Dammam Corniche → Khobar Corniche | `rn-9331875d0d5d` | **TRIM** | distance_honesty: card 28.7nm vs route 14.0nm (105% delta) |
| featured | ksa-commercial/p2 | Khobar Corniche → Half Moon Bay | `rn-fdb6972a2536` | **TRIM** | distance_honesty: card 28.7nm vs route 13.0nm (121% delta) |
| featured | ksa-commercial/p2 | Dammam → Tarout Island / Qatif | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dammam' → 'Tarout Island / Q |
| featured | ksa-commercial/p2 | Khobar / Dammam → Manama, Bahrain | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Khobar / Dammam' → 'Manama,  |
| featured | ksa-commercial/p3 | Jeddah Corniche → Jeddah Central (PIF waterfront) | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | ksa-commercial/p3 | Khobar Corniche → Half Moon Bay | `gcn-adcdd3d09c-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Khobar Corniche' → 'Half Moo |
| featured | ksa-commercial/p3 | Khobar / Dammam → Manama, Bahrain | `rn-3fcef88ee5f5` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Khobar / Dammam' → 'Manama,  |
| journey | market:south-africa | V&A Waterfront → Robben Island | `—` | **KEEP** | — |
| journey | market:south-africa | V&A Waterfront → Hout Bay | `—` | **KEEP** | — |
| journey | market:south-africa | Hout Bay → Simon's Town (False Bay) | `—` | **KEEP** | — |
| journey | market:south-africa | Cape Town → Gordon's Bay (False Bay) | `—` | **KEEP** | — |
| featured | south-africa/p1 | V&A Waterfront → Robben Island | `—` | **KEEP** | — |
| featured | south-africa/p1 | V&A Waterfront → Hout Bay | `—` | **KEEP** | — |
| featured | south-africa/p2 | Hout Bay → Simon's Town (False Bay) | `—` | **KEEP** | — |
| featured | south-africa/p2 | Cape Town → Gordon's Bay (False Bay) | `—` | **KEEP** | — |
| featured | south-africa/p3 | Cape Town → Exposed-coast reach (Quanta-LR reserve | `—` | **KEEP** | — |
| journey | market:spain | L'Estartit → Illes Medes | `—` | **KEEP** | — |
| journey | market:spain | Marbella → Puerto Banús | `rn-3b8e9da00462` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marbella' → 'Puerto Banús' v; distance_honesty: card 3.5nm vs route 5.8nm (40% delta) |
| journey | market:spain | Lloret de Mar → Tossa de Mar | `ics-c250dbc94d` | **KEEP** | — |
| journey | market:spain | Port de Sóller (Mallorca) → Sa Calobra / Torrent d | `ics-7085b9f5f4` | **TRIM** | distance_honesty: card 9.0nm vs route 14.32nm (37% delta); geometry_preview: interior_land_km=19.91 (threshold 0.4) |
| journey | market:spain | Tarifa → Tangier (Morocco) | `—` | **KEEP** | — |
| journey | market:spain | Palma de Mallorca → Ibiza Town | `ics-4c8c95334c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Palma de Mallorca' → 'Ibiza  |
| featured | spain/p1 | L'Estartit → Illes Medes | `—` | **KEEP** | — |
| featured | spain/p1 | Marbella → Puerto Banús | `rn-3b8e9da00462` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marbella' → 'Puerto Banús' v; distance_honesty: card 3.5nm vs route 5.8nm (40% delta) |
| featured | spain/p1 | Lloret de Mar → Tossa de Mar | `ics-c250dbc94d` | **KEEP** | — |
| featured | spain/p2 | Port de Sóller (Mallorca) → Sa Calobra / Torrent d | `ics-7085b9f5f4` | **DEFER** | distance_honesty: card 9.0nm vs route 14.32nm (37% delta); geometry_preview: interior_land_km=19.91 (threshold 0.4) |
| featured | spain/p2 | Ibiza Town (Eivissa) → Formentera (La Savina) | `ics-605dcb641e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Ibiza Town (Eivissa)' → 'For |
| featured | spain/p2 | Puerto Banús → Estepona | `rn-3b8e9da00462` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Puerto Banús' → 'Estepona' v; distance_honesty: card 12.0nm vs route 5.8nm (107% delta) |
| featured | spain/p2 | Tarifa → Tangier (Morocco) | `—` | **KEEP** | — |
| featured | spain/p2 | Alcúdia (Mallorca) → Ciutadella (Menorca) | `ics-f88551e209` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Alcúdia (Mallorca)' → 'Ciuta |
| featured | spain/p2 | Dénia → Ibiza Town (Eivissa) | `ics-ef670fc469` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dénia' → 'Ibiza Town (Eiviss |
| featured | spain/p3 | Palma de Mallorca → Ibiza Town | `ics-4c8c95334c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Palma de Mallorca' → 'Ibiza  |
| featured | spain/p3 | Palma de Mallorca → Maó (Menorca) | `ics-f88551e209` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Palma de Mallorca' → 'Maó (M; distance_honesty: card 100.0nm vs route 24.16nm (314% delta) |
| featured | spain/p3 | Barcelona → Palma de Mallorca | `—` | **KEEP** | — |
| featured | spain/p3 | Dénia → Palma de Mallorca | `—` | **KEEP** | — |
| featured | spain/p3 | Barcelona → Ibiza Town (Eivissa) | `rn-c89749acaa14` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Barcelona' → 'Ibiza Town (Ei; distance_honesty: card 140.0nm vs route 67.0nm (109% delta) (+1) |
| journey | market:sweden | Stockholm (Slussen) → Djurgarden | `rn-7061b9e5930e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Slussen)' → 'Djur; distance_honesty: card 0.5nm vs route 0.9nm (44% delta) |
| journey | market:sweden | Stockholm (Nybroplan) → Nacka Strand / Ropsten | `rn-1fc1a669275e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Nybroplan)' → 'Na; distance_honesty: card 3.0nm vs route 4.5nm (33% delta) |
| journey | market:sweden | Stockholm (Stadshuskajen / Klara Malarstrand) → Dr | `—` | **KEEP** | — |
| journey | market:sweden | Stockholm (Klara Malarstrand) → Ekero (Tappstrom) | `rn-66180c77771f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Klara Malarstrand; distance_honesty: card 8.6nm vs route 18.8nm (54% delta) |
| journey | market:sweden | Stockholm City → Vaxholm | `rn-c0c9469dd4fd` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm City' → 'Vaxholm'  |
| journey | market:sweden | Stockholm (Vartahamnen / Stadsgarden) → Mariehamn  | `—` | **KEEP** | — |
| featured | sweden/p1 | Stockholm (Slussen) → Djurgarden | `rn-7061b9e5930e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Slussen)' → 'Djur; distance_honesty: card 0.5nm vs route 0.9nm (44% delta) |
| featured | sweden/p1 | Stockholm (Nybroplan) → Nacka Strand / Ropsten | `rn-1fc1a669275e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Nybroplan)' → 'Na; distance_honesty: card 3.0nm vs route 4.5nm (33% delta) |
| featured | sweden/p1 | Stockholm (Stadshuskajen / Klara Malarstrand) → Dr | `—` | **KEEP** | — |
| featured | sweden/p2 | Stockholm (Klara Malarstrand) → Ekero (Tappstrom) | `rn-66180c77771f` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Klara Malarstrand; distance_honesty: card 8.6nm vs route 18.8nm (54% delta) |
| featured | sweden/p2 | Stockholm → Saltsjobaden (Nacka) | `rn-6b6babc145f9` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm' → 'Saltsjobaden (; distance_honesty: card 9.0nm vs route 5.8nm (55% delta) |
| featured | sweden/p2 | Stockholm (Stromkajen) → Alstaket (Varmdo) | `rn-f270f57e95eb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Stromkajen)' → 'A; distance_honesty: card 11.0nm vs route 18.3nm (40% delta) |
| featured | sweden/p2 | Stockholm City → Vaxholm | `rn-c0c9469dd4fd` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm City' → 'Vaxholm'  |
| featured | sweden/p2 | Stockholm (Strandvagen) → Grinda | `rn-d6a16682911b` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Strandvagen)' → ' |
| featured | sweden/p2 | Stockholm (Strandvagen) → Gallno | `rn-e388d0b647a6` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Stockholm (Strandvagen)' → ' |
| featured | sweden/p3 | Stockholm (Vartahamnen / Stadsgarden) → Mariehamn  | `—` | **KEEP** | — |
| journey | market:thailand | Phuket (Ao Po / Boat Lagoon) → Phang Nga Bay (Jame | `—` | **KEEP** | — |
| journey | market:thailand | Phuket → Koh Yao Noi | `—` | **KEEP** | — |
| journey | market:thailand | Phuket → Phi Phi | `—` | **KEEP** | — |
| journey | market:thailand | Phuket → Krabi / Ao Nang | `—` | **KEEP** | — |
| journey | market:thailand | Phuket → Koh Samui | `—` | **KEEP** | — |
| featured | thailand/p1 | Phuket (Ao Po / Boat Lagoon) → Phang Nga Bay (Jame | `—` | **KEEP** | — |
| featured | thailand/p1 | Phuket → Koh Yao Noi | `—` | **KEEP** | — |
| featured | thailand/p1 | Phuket → Naka Yai / Cape Yamu | `—` | **KEEP** | — |
| featured | thailand/p2 | Phuket → Phi Phi | `—` | **KEEP** | — |
| featured | thailand/p2 | Phuket → Krabi / Ao Nang | `—` | **KEEP** | — |
| featured | thailand/p2 | Phuket → Similan Islands (seasonal) | `—` | **KEEP** | — |
| featured | thailand/p3 | Phuket → Langkawi (Malaysia) | `—` | **KEEP** | — |
| featured | thailand/p3 | Phuket → Koh Samui | `—` | **KEEP** | — |
| journey | market:uae | One&Only The Palm Jetty → Jumeirah Zabeel Saray Je | `gcn-8d63400ee6-bolt` | **KEEP** | — |
| journey | market:uae | Dubai Harbour Marina → Bluewaters Marina | `gcn-5f710d44d4-bolt` | **KEEP** | — |
| journey | market:uae | Kempinski Hotel & Residences Palm Jumeirah Jetty → | `gcn-53d48bd905-bolt` | **KEEP** | — |
| journey | market:uae | La Mer / J1 Beach Jetty → Nikki Beach Resort Pearl | `gcn-196f720eb3-bolt` | **KEEP** | — |
| journey | market:uae | Dubai Marina → Abu Dhabi Corniche | `rn-25065af2bcb4` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Marina' → 'Abu Dhabi C |
| featured | uae/p1 | One&Only The Palm Jetty → Jumeirah Zabeel Saray Je | `gcn-8d63400ee6-bolt` | **KEEP** | — |
| featured | uae/p1 | Dubai Harbour Marina → Bluewaters Marina | `gcn-5f710d44d4-bolt` | **KEEP** | — |
| featured | uae/p1 | Kempinski Hotel & Residences Palm Jumeirah Jetty → | `gcn-53d48bd905-bolt` | **KEEP** | — |
| featured | uae/p2 | La Mer / J1 Beach Jetty → Nikki Beach Resort Pearl | `gcn-196f720eb3-bolt` | **KEEP** | — |
| featured | uae/p2 | Palm Jumeirah Marina West → Atlantis The Palm Jett | `gcn-53d48bd905-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Palm Jumeirah Marina West' → |
| featured | uae/p2 | Dubai Creek Marina → Al Seef Marine Transport Stat | `gcn-e71d4cf5b6-bolt` | **KEEP** | — |
| featured | uae/p2 | Yacht Marina → The Westin Dubai Mina Seyahi Beach  | `gcn-0ca7f3ffe7-bolt` | **KEEP** | — |
| featured | uae/p2 | Marina Mall / Breakwater Marina → Lulu Island Jett | `gcn-c45463c294-bolt` | **KEEP** | — |
| featured | uae/p2 | Dubai Harbour Marina → Palm Jumeirah Marina West | `gcn-0ca7f3ffe7-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour Marina' → 'Pal |
| featured | uae/p3 | Marina Mall / Breakwater Marina → Sir Bani Yas Cru | `gcn-8b5dd5d484-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Marina Mall / Breakwater Mar |
| featured | uae/p3 | Dubai Harbour Marina → Old Doha Port | `gcn-e71d4cf5b6-bolt` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Dubai Harbour Marina' → 'Old |
| featured | uae/p3 | Marina Mall / Breakwater Marina → Bahrain Financia | `rn-c69c27c8b6e4` | **KEEP** | — |
