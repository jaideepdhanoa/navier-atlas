# Partner → Global Registry Map

Maps partner market buckets to existing Atlas city IDs after the registry-first overlay. No new BP/route research is introduced.

## Summary
- **partners**: 47
- **partner_markets**: 113
- **mapped_partner_markets**: 112
- **unmapped_partner_markets**: 1
- **by_market_status**: {'all_economics_ready': 32, 'mixed_registry_gap_queue': 13, 'all_geometry_or_economics_ready_promote_missing_economics': 67, 'unmatched': 1}

## Priority notes
### didi
- `brazil` → 3 city IDs; all_geometry_or_economics_ready_promote_missing_economics (rio-de-janeiro-brazil, angra-dos-reis-ilha-grande-brazil, florianopolis-brazil)
- `mexico-pacific` → 2 city IDs; all_geometry_or_economics_ready_promote_missing_economics (los-cabos-mexico, puerto-vallarta-mexico)
- `mexico-caribbean` → 3 city IDs; mixed_registry_gap_queue (cancun-riviera-maya-mexico, cozumel-mexico, playa-del-carmen-mexico)
- `colombia` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (cartagena-colombia)
- `panama` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (san-blas-panama)
- `costa-rica` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (nicoya-papagayo-costa-rica)
- `dominican-republic` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (samana-dominican-republic)

### uber
- `mena` → 17 city IDs; mixed_registry_gap_queue (abu-dhabi-uae, dubai-uae, ras-al-khaimah-uae, sharjah-uae, fujairah-uae, doha-qatar, jeddah-ksa, red-sea-global-ksa…)
- `miami` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (miami-florida-usa)
- `bay-area` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (san-francisco-bay-area-usa)
- `hawaii` → 4 city IDs; all_geometry_or_economics_ready_promote_missing_economics (oahu-honolulu-hawaii-usa, maui-county-hawaii-usa, kauai-hawaii-usa, kona-hilo-hawaii-island-usa)
- `mediterranean` → 29 city IDs; all_geometry_or_economics_ready_promote_missing_economics (athens-saronic-greece, mykonos-greece, santorini-greece, paros-greece, naxos-greece, milos-western-cyclades-greece, crete-greece, corfu-ionian-greece…)
- `sydney-nsw` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (sydney-australia)
- `brazil-latam` → 3 city IDs; all_geometry_or_economics_ready_promote_missing_economics (rio-de-janeiro-brazil, angra-dos-reis-ilha-grande-brazil, florianopolis-brazil)
- `italy-luxury` → 8 city IDs; mixed_registry_gap_queue (amalfi-coast-italy, costa-smeralda-italy, naples-capri-procida-italy, portofino-cinque-terre-italy, sicily-aeolian-italy, tuscan-archipelago-italy, venice-italy, lake-como-italy)
- `cote-dazur` → 2 city IDs; all_economics_ready (cote-dazur-france, monaco-monaco)
- `istanbul` → 1 city IDs; all_economics_ready (istanbul-turkey)
- `india` → 4 city IDs; all_geometry_or_economics_ready_promote_missing_economics (mumbai-india, goa-india, kerala-backwaters-india, andaman-india)
- `japan` → 8 city IDs; all_geometry_or_economics_ready_promote_missing_economics (tokyo-bay-japan, setouchi-japan, izu-islands-japan, izu-peninsula-japan, okinawa-main-japan, yaeyama-japan, miyako-japan, hokkaido-niseko-japan)
- `hong-kong-prd` → 2 city IDs; all_geometry_or_economics_ready_promote_missing_economics (hong-kong, macau-china)
- `mexico` → 5 city IDs; mixed_registry_gap_queue (cancun-riviera-maya-mexico, cozumel-mexico, playa-del-carmen-mexico, los-cabos-mexico, puerto-vallarta-mexico)
- `lagos` → 1 city IDs; all_economics_ready (lagos-nigeria)
- `ksa-red-sea` → 3 city IDs; all_geometry_or_economics_ready_promote_missing_economics (red-sea-global-ksa, jeddah-ksa, neom-sindalah-ksa)
- `egypt` → 3 city IDs; all_economics_ready (cairo-egypt, hurghada-el-gouna-egypt, sharm-el-sheikh-egypt)

### lyft
- `new-york` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (new-york-harbor-usa)
- `miami` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (miami-florida-usa)
- `bay-area` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (san-francisco-bay-area-usa)
- `seattle` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (seattle-puget-sound-usa)
- `boston` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (boston-new-england-usa)
- `athens-cyclades` → 6 city IDs; all_geometry_or_economics_ready_promote_missing_economics (athens-saronic-greece, mykonos-greece, santorini-greece, paros-greece, naxos-greece, milos-western-cyclades-greece)

### bolt
- `uae` → 5 city IDs; all_geometry_or_economics_ready_promote_missing_economics (abu-dhabi-uae, dubai-uae, ras-al-khaimah-uae, sharjah-uae, fujairah-uae)
- `croatia` → 4 city IDs; all_geometry_or_economics_ready_promote_missing_economics (hvar-croatia, korcula-croatia, split-croatia, dubrovnik-croatia)
- `egypt` → 3 city IDs; all_economics_ready (cairo-egypt, hurghada-el-gouna-egypt, sharm-el-sheikh-egypt)
- `estonia` → 1 city IDs; all_economics_ready (tallinn-estonia)
- `finland` → 1 city IDs; all_economics_ready (helsinki-finland)
- `france-riviera` → 4 city IDs; all_geometry_or_economics_ready_promote_missing_economics (cote-dazur-france, monaco-monaco, marseille-calanques-france, corsica-france)
- `greece` → 9 city IDs; mixed_registry_gap_queue (athens-saronic-greece, chios-north-aegean-greece, corfu-ionian-greece, milos-western-cyclades-greece, naxos-greece, paros-greece, santorini-greece, skiathos-sporades-greece…)
- `ireland` → 1 city IDs; all_economics_ready (dublin-ireland)
- `italy` → 8 city IDs; mixed_registry_gap_queue (amalfi-coast-italy, costa-smeralda-italy, naples-capri-procida-italy, ponza-pontine-italy, portofino-cinque-terre-italy, sicily-aeolian-italy, tuscan-archipelago-italy, venice-italy)
- `portugal` → 3 city IDs; mixed_registry_gap_queue (lisbon-tagus, porto, algarve)
- `qatar` → 1 city IDs; all_economics_ready (doha-qatar)
- `ksa-commercial` → 2 city IDs; all_geometry_or_economics_ready_promote_missing_economics (jeddah-ksa, eastern-province-ksa)
- `spain` → 4 city IDs; all_geometry_or_economics_ready_promote_missing_economics (costa-brava-spain, menorca-spain, ibiza-spain, mallorca-spain)
- `sweden` → 1 city IDs; all_economics_ready (stockholm-sweden)

### yango
- `uae` → 5 city IDs; all_geometry_or_economics_ready_promote_missing_economics (abu-dhabi-uae, dubai-uae, ras-al-khaimah-uae, sharjah-uae, fujairah-uae)
- `cote-divoire` → 1 city IDs; mixed_registry_gap_queue (abidjan)
- `egypt` → 3 city IDs; all_economics_ready (cairo-egypt, hurghada-el-gouna-egypt, sharm-el-sheikh-egypt)
- `lagos` → 1 city IDs; all_economics_ready (lagos-nigeria)
- `morocco` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (agadir-essaouira-morocco)
- `qatar` → 1 city IDs; all_economics_ready (doha-qatar)
- `ksa-commercial` → 2 city IDs; all_geometry_or_economics_ready_promote_missing_economics (jeddah-ksa, eastern-province-ksa)
- `turkey` → 4 city IDs; all_geometry_or_economics_ready_promote_missing_economics (antalya-turkey, bodrum-turkey, cesme-izmir-turkey, istanbul-turkey)

### grab
- `singapore` → 1 city IDs; all_economics_ready (singapore)
- `cross-border` → 0 city IDs; unmatched ()
- `bali` → 1 city IDs; all_economics_ready (bali-indonesia)
- `phuket` → 1 city IDs; all_economics_ready (phuket-phang-nga-thailand)
- `philippines` → 3 city IDs; mixed_registry_gap_queue (boracay-philippines, palawan-philippines__el-nido-bacuit-bay, siargao-philippines)
- `vietnam` → 4 city IDs; all_economics_ready (da-nang-hoi-an-vietnam, ha-long-bay-vietnam, ho-chi-minh-city-vietnam, phu-quoc-vietnam)
- `cambodia` → 1 city IDs; all_economics_ready (koh-rong-cambodia)
- `borneo` → 3 city IDs; all_geometry_or_economics_ready_promote_missing_economics (sabah-kota-kinabalu-malaysia, brunei-darussalam, derawan-berau-east-kalimantan-indonesia)
- `penang` → 1 city IDs; all_economics_ready (penang-malaysia)
- `jakarta` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (jakarta-indonesia)
- `koh-samui` → 1 city IDs; all_economics_ready (koh-samui-thailand)
- `bangkok` → 1 city IDs; all_geometry_or_economics_ready_promote_missing_economics (bangkok-thailand)
- `taiwan` → 2 city IDs; all_economics_ready (kaohsiung-taiwan, penghu-taiwan)

