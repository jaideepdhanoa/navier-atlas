# Proposal fidelity — bolt

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-06-29T11:29:21Z

## Summary

- Items audited: 160
- KEEP: 153
- DROP: 0
- DEFER: 4
- TRIM/REWRITE: 3
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Athens → Hydra (Saronic) | `—` | **KEEP** | — |
| journey | — | Split → Hvar | `rn-cc40790a3078` | **TRIM** | geometry_preview: interior_land_km=5.09 (threshold 0.4) |
| journey | — | Nice Airport → Monaco | `—` | **KEEP** | — |
| journey | — | Cais do Sodré (Lisbon) → Cacilhas (Almada) | `—` | **KEEP** | — |
| featured | 1 | Athens ↔ Saronic islands | `—` | **KEEP** | — |
| featured | 3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:croatia | Dubrovnik → Cavtat | `rn-27a8218aa694` | **KEEP** | — |
| journey | market:croatia | Dubrovnik → Kotor (Montenegro) | `—` | **KEEP** | — |
| featured | croatia/p1 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | croatia/p2 | Dubrovnik → Cavtat | `rn-27a8218aa694` | **KEEP** | — |
| featured | croatia/p2 | Zadar (Murter / Biograd gateway) → Kornati Nationa | `—` | **KEEP** | — |
| featured | croatia/p2 | Split → Hvar | `rn-cc40790a3078` | **DEFER** | geometry_preview: interior_land_km=5.09 (threshold 0.4) |
| featured | croatia/p3 | Split ↔ Trogir (via Čiovo) | `—` | **KEEP** | — |
| journey | market:east-africa | Dar es Salaam → Stone Town (Zanzibar) | `rn-46bee519109a` | **KEEP** | — |
| journey | market:east-africa | Mombasa → Diani / Ukunda | `—` | **KEEP** | — |
| featured | east-africa/pNone | Dar es Salaam → Stone Town | `rn-46bee519109a` | **KEEP** | — |
| journey | market:egypt | El Gouna (internal lagoon) → El Gouna Downtown / A | `rn-cf19a27c2e8a` | **KEEP** | — |
| journey | market:egypt | Cairo - Maadi → Cairo - Zamalek / Downtown | `rn-4d2d789c04ad` | **KEEP** | — |
| journey | market:egypt | Hurghada → El Gouna | `rn-abf46355ef7f` | **TRIM** | geometry_preview: interior_land_km=8.63 (threshold 0.4) |
| featured | egypt/p1 | El Gouna (internal lagoon) → El Gouna Downtown / A | `rn-cf19a27c2e8a` | **KEEP** | — |
| featured | egypt/p1 | Cairo - Maadi → Cairo - Zamalek / Downtown | `rn-4d2d789c04ad` | **KEEP** | — |
| featured | egypt/p2 | Greater Cairo - Maspero (Downtown) → Greater Cairo | `rn-148c41cefa55` | **KEEP** | — |
| featured | egypt/p2 | Hurghada → El Gouna | `rn-abf46355ef7f` | **DEFER** | geometry_preview: interior_land_km=8.63 (threshold 0.4) |
| featured | egypt/p2 | Hurghada → Soma Bay | `rn-fbbb4fae5cbe` | **DEFER** | geometry_preview: interior_land_km=13.51 (threshold 0.4) |
| featured | egypt/p3 | in-app journeys | `—` | **KEEP** | — |
| journey | market:estonia | Tallinn Old City Harbour → Pirita Marina | `rn-889f513853ae` | **KEEP** | — |
| journey | market:estonia | Tallinn → Prangli | `rn-aeb90d25487f` | **KEEP** | — |
| journey | market:estonia | Tallinn → Viimsi | `rn-d6554a0bc2c8` | **KEEP** | — |
| journey | market:estonia | Tallinn → Kakumäe | `rn-44d0d47fe330` | **KEEP** | — |
| featured | estonia/p1 | Tallinn Old City Harbour → Pirita Marina | `rn-889f513853ae` | **KEEP** | — |
| featured | estonia/p1 | Tallinn → Prangli | `rn-aeb90d25487f` | **KEEP** | — |
| featured | estonia/p1 | Tallinn → Viimsi | `rn-d6554a0bc2c8` | **KEEP** | — |
| featured | estonia/p2 | Tallinn → Kakumäe | `rn-44d0d47fe330` | **KEEP** | — |
| featured | estonia/p2 | Tallinn → Aegna | `—` | **KEEP** | — |
| featured | estonia/p2 | Tallinn → Naissaar | `rn-16666eaf140c` | **KEEP** | — |
| featured | estonia/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:finland | Helsinki → Lonna | `rn-312e87d88d71` | **KEEP** | — |
| journey | market:finland | Helsinki Market Square → Suomenlinna | `rn-ca17345bf0e8` | **KEEP** | — |
| journey | market:finland | Helsinki → Pihlajasaari | `rn-c470fde6e58f` | **KEEP** | — |
| journey | market:finland | Helsinki → Korkeasaari (Zoo island) | `rn-2025e138f6c3` | **KEEP** | — |
| featured | finland/p1 | Helsinki → Lonna | `rn-312e87d88d71` | **KEEP** | — |
| featured | finland/p1 | Helsinki Market Square → Suomenlinna | `rn-ca17345bf0e8` | **KEEP** | — |
| featured | finland/p1 | Helsinki → Pihlajasaari | `rn-c470fde6e58f` | **KEEP** | — |
| featured | finland/p2 | Helsinki → Korkeasaari (Zoo island) | `rn-2025e138f6c3` | **KEEP** | — |
| featured | finland/p2 | Helsinki → Kruunuvuorenranta (Laajasalo) | `rn-4ab75813e3cc` | **KEEP** | — |
| featured | finland/p2 | Helsinki → Vallisaari | `rn-8523ec0a5309` | **KEEP** | — |
| featured | finland/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:france-riviera | Menton → Monaco | `rn-5fb120384595` | **KEEP** | — |
| journey | market:france-riviera | Monaco → Sanremo | `rn-6af10d73458f` | **KEEP** | — |
| journey | market:france-riviera | St-Tropez → Pampelonne | `—` | **KEEP** | — |
| featured | france-riviera/p1 | Antibes → Cannes | `rn-3fab58bb5f82` | **KEEP** | — |
| featured | france-riviera/p2 | Menton → Monaco | `rn-5fb120384595` | **KEEP** | — |
| featured | france-riviera/p2 | Nice → Monaco | `rn-c0f2e69be06c` | **KEEP** | — |
| featured | france-riviera/p2 | Monaco → Sanremo | `rn-6af10d73458f` | **KEEP** | — |
| featured | france-riviera/p3 | St-Tropez → Pampelonne | `—` | **KEEP** | — |
| journey | market:greece | Rhodes → Marmaris (Turkey) | `rn-a95f11ef9a7e` | **KEEP** | — |
| featured | greece/p1 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | greece/p2 | Santorini (Thira) → Ios | `rn-be97f62a4421` | **KEEP** | — |
| featured | greece/p2 | Rhodes → Marmaris (Turkey) | `—` | **KEEP** | — |
| featured | greece/p3 | Mykonos → Santorini (Thira) | `—` | **KEEP** | — |
| journey | market:ireland | Dalkey → Dalkey Island | `—` | **KEEP** | — |
| journey | market:ireland | Howth → Ireland's Eye | `—` | **KEEP** | — |
| journey | market:ireland | Dublin Docklands → Dún Laoghaire | `rn-455eede91b5a` | **KEEP** | — |
| journey | market:ireland | Dublin Port → Holyhead (Wales) | `—` | **KEEP** | — |
| featured | ireland/p1 | Dalkey → Dalkey Island | `—` | **KEEP** | — |
| featured | ireland/p1 | Howth → Ireland's Eye | `—` | **KEEP** | — |
| featured | ireland/p1 | Dublin Docklands → Dún Laoghaire | `rn-455eede91b5a` | **KEEP** | — |
| featured | ireland/p2 | Dun Laoghaire → Howth | `rn-12e7db59f876` | **KEEP** | — |
| featured | ireland/p2 | Dublin City (Docklands) → Dalkey / Killiney | `—` | **KEEP** | — |
| featured | ireland/p2 | Dublin Port → Holyhead (Wales) | `—` | **KEEP** | — |
| featured | ireland/p3 | Dalkey ↔ Dalkey Island | `—` | **KEEP** | — |
| journey | market:italy | Venice → Lido | `rn-093619ef734a` | **KEEP** | — |
| journey | market:italy | San Marco → Murano / Burano | `rn-3483f535e23c` | **KEEP** | — |
| journey | market:italy | Sorrento → Capri | `rn-41ee5cb908d0` | **KEEP** | — |
| featured | italy/p1 | Venice → Lido | `—` | **KEEP** | — |
| featured | italy/p1 | San Marco → Murano / Burano | `—` | **KEEP** | — |
| featured | italy/p2 | Venice Marco Polo → San Marco | `—` | **KEEP** | — |
| featured | italy/p2 | Capri → Positano | `ics-9546e52c39` | **KEEP** | — |
| featured | italy/p2 | Sorrento → Capri | `rn-41ee5cb908d0` | **KEEP** | — |
| featured | italy/p3 | Venice ↔ Lido | `—` | **KEEP** | — |
| journey | market:nigeria | CMS / Marina (Lagos Island) → Victoria Island | `—` | **KEEP** | — |
| journey | market:nigeria | Osborne (Ikoyi) → CMS / Marina | `—` | **KEEP** | — |
| journey | market:nigeria | CMS / Marina → Apapa | `—` | **KEEP** | — |
| journey | market:nigeria | CMS / Marina → Ikorodu | `—` | **KEEP** | — |
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
| featured | portugal/p1 | Porto (Cais da Ribeira) → Vila Nova de Gaia (Cais  | `rn-20d8de578b2f` | **KEEP** | — |
| featured | portugal/p1 | Vila Real de Santo Antonio (Portugal) → Ayamonte ( | `rn-2f31310c4e84` | **KEEP** | — |
| featured | portugal/p1 | Lagos → Ponta da Piedade | `rn-f2aa06497c53` | **KEEP** | — |
| featured | portugal/p2 | Olhao → Culatra / Farol | `rn-7e047d3229fc` | **KEEP** | — |
| featured | portugal/p2 | Faro → Ilha Deserta (Barreta) | `rn-cd1337338a68` | **KEEP** | — |
| featured | portugal/p2 | Terreiro do Paco (Lisbon) → Barreiro | `rn-a4d791eb5afd` | **KEEP** | — |
| featured | portugal/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:qatar | Doha Corniche → The Pearl | `rn-f15bb66e8e87` | **KEEP** | — |
| featured | qatar/p1 | Lusail Marina → The Pearl | `rn-79da51f0117a` | **KEEP** | — |
| featured | qatar/p2 | Doha (Al Shyoukh Terminal) → Banana Island Resort  | `gcn-de7142cf37-bolt` | **KEEP** | — |
| featured | qatar/p2 | Al Wakrah → Banana Island | `rn-0b99edfc9e67` | **KEEP** | — |
| featured | qatar/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:ksa-commercial | Jeddah Corniche → Jeddah Central (PIF waterfront) | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| journey | market:ksa-commercial | Jeddah Corniche → Jeddah Yacht Club & Marina | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | ksa-commercial/p1 | Jeddah Corniche → Jeddah Central (PIF waterfront) | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | ksa-commercial/p1 | Jeddah Corniche → Jeddah Yacht Club & Marina | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | ksa-commercial/p2 | Dammam Corniche → Khobar Corniche | `rn-9331875d0d5d` | **KEEP** | — |
| featured | ksa-commercial/p2 | Khobar Corniche → Half Moon Bay | `rn-fdb6972a2536` | **KEEP** | — |
| featured | ksa-commercial/p3 | Jeddah Corniche → Jeddah Central (PIF waterfront) | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
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
| journey | market:spain | Lloret de Mar → Tossa de Mar | `ics-c250dbc94d` | **KEEP** | — |
| journey | market:spain | Port de Sóller (Mallorca) → Sa Calobra / Torrent d | `ics-7085b9f5f4` | **TRIM** | geometry_preview: interior_land_km=19.91 (threshold 0.4) |
| journey | market:spain | Tarifa → Tangier (Morocco) | `—` | **KEEP** | — |
| featured | spain/p1 | L'Estartit → Illes Medes | `—` | **KEEP** | — |
| featured | spain/p1 | Lloret de Mar → Tossa de Mar | `ics-c250dbc94d` | **KEEP** | — |
| featured | spain/p2 | Port de Sóller (Mallorca) → Sa Calobra / Torrent d | `ics-7085b9f5f4` | **DEFER** | distance_honesty: card 9.0nm vs route 14.32nm (37% delta); geometry_preview: interior_land_km=19.91 (threshold 0.4) |
| featured | spain/p2 | Tarifa → Tangier (Morocco) | `—` | **KEEP** | — |
| featured | spain/p3 | Barcelona → Palma de Mallorca | `—` | **KEEP** | — |
| featured | spain/p3 | Dénia → Palma de Mallorca | `—` | **KEEP** | — |
| journey | market:sweden | Stockholm (Stadshuskajen / Klara Malarstrand) → Dr | `—` | **KEEP** | — |
| journey | market:sweden | Stockholm (Vartahamnen / Stadsgarden) → Mariehamn  | `—` | **KEEP** | — |
| featured | sweden/p1 | Stockholm (Stadshuskajen / Klara Malarstrand) → Dr | `—` | **KEEP** | — |
| featured | sweden/p2 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | sweden/p3 | Stockholm (Vartahamnen / Stadsgarden) → Mariehamn  | `—` | **KEEP** | — |
| journey | market:thailand | Phuket (Ao Po / Boat Lagoon) → Phang Nga Bay (Jame | `—` | **KEEP** | — |
| journey | market:thailand | Phuket → Koh Yao Noi | `—` | **KEEP** | — |
| journey | market:thailand | Phuket → Phi Phi | `—` | **KEEP** | — |
| journey | market:thailand | Phuket → Krabi / Ao Nang | `—` | **KEEP** | — |
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
| featured | uae/p1 | One&Only The Palm Jetty → Jumeirah Zabeel Saray Je | `gcn-8d63400ee6-bolt` | **KEEP** | — |
| featured | uae/p1 | Dubai Harbour Marina → Bluewaters Marina | `gcn-5f710d44d4-bolt` | **KEEP** | — |
| featured | uae/p1 | Kempinski Hotel & Residences Palm Jumeirah Jetty → | `gcn-53d48bd905-bolt` | **KEEP** | — |
| featured | uae/p2 | La Mer / J1 Beach Jetty → Nikki Beach Resort Pearl | `gcn-196f720eb3-bolt` | **KEEP** | — |
| featured | uae/p2 | Dubai Creek Marina → Al Seef Marine Transport Stat | `gcn-e71d4cf5b6-bolt` | **KEEP** | — |
| featured | uae/p2 | Yacht Marina → The Westin Dubai Mina Seyahi Beach  | `gcn-0ca7f3ffe7-bolt` | **KEEP** | — |
| featured | uae/p3 | Marina Mall / Breakwater Marina → Bahrain Financia | `rn-c69c27c8b6e4` | **KEEP** | — |
