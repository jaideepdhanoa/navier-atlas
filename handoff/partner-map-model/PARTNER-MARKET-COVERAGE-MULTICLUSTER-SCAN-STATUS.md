# Multi-cluster partner coverage scan — broad-footprint-first control

Created: 2026-06-20 14:48 GMT+5:30

## Rule

New research is additive only. It cannot shrink existing partner JSON, `network_footprint[]`, map scope, seal scope, or registry-bound markets. Broad web/AI summaries are country/region seeds, not city truth.

## P0 active partners

### yango
- Status: broad_seed_ready_needs_country_validation_and_city_diff
- Broad shape: 30+ countries across Middle East/MENAP, Latin America, Africa, Europe, South Asia, South Caucasus/Central Asia; user seed lists UAE, Oman, Egypt, Bahrain, Jordan, Qatar, Pakistan; Ghana, Senegal, Ivory Coast, Cameroon, Zambia, Angola, Mozambique, Namibia, Ethiopia, DRC; Bolivia, Peru, Colombia, Guatemala; Nepal, Sri Lanka, Armenia, Georgia, Uzbekistan, Kazakhstan; Finland, Norway.
- Next: Validate country list with official/about/press sources, then city-diff only priority coastal countries against existing Yango baseline.

### bolt
- Status: official_city_inventory_exists_needs_coastal_country_bucketing
- Broad shape: Official city list / support indicates hundreds of cities across 50+ countries in Europe, Africa, Asia, Latin America; repo already has 863 official city rows and 14 existing mapped partner markets.
- Next: Do country rollup first; triage only water-relevant countries/cities; park inland official city rows.

### uber
- Status: broad_seed_ready_huge_global_city_list_needs_atlas_overlap_filter
- Broad shape: Uber official city page claims availability in 15,000+ cities; newsroom/secondary sources indicate roughly 70 countries / global footprint. Needs country/region filtering before city scan.
- Next: Use Uber official city index only after prefiltering to Atlas-overlap/coastal regions; avoid trying to enumerate all cities.

### lyft
- Status: north_america_primary_plus_freenow_europe_watch
- Broad shape: Lyft official city pages cover US and Canada; 2025 FREENOW acquisition adds European taxi-platform footprint but should be represented as Lyft/FREENOW business-line distinction until integration is proposal-relevant.
- Next: Scan Lyft US/Canada coastal Atlas-overlap first; treat FREENOW as separate acquired platform source until Navier decides combined proposal framing.

## P1 next mobility / regional platforms

### grab
- Status: broad_seed_known_se_asia_superapp
- Broad shape: Official/credible sources indicate Grab operates across 8 Southeast Asian countries and 500+ cities/towns; repo baseline already has Southeast Asia coastal/island proposal clusters.
- Next: Diff official country/city location pages against existing Grab proposal clusters; focus on missing coastal/island coverage, not all inland towns.

### didi
- Status: broad_seed_latam_apac_needs_country_validation
- Broad shape: SEC/source results show DiDi across Asia Pacific, Latin America and other markets; LATAM sources cite Mexico, Brazil, Colombia, Peru and broader LatAm expansion. Existing repo has 7 coastal LATAM market buckets.
- Next: Country validate from DiDi/local sources, then city-level scan for coastal LATAM and APAC overlap only.

### gojek
- Status: regional_seed_indonesia_singapore_with_vietnam_thailand_exit_caveats
- Broad shape: Current sources point to Indonesia and Singapore as active core; older expansion included Vietnam/Thailand/Philippines, with Vietnam/Thailand exit caveats. Repo baseline already covers Indonesian island clusters and Singapore.
- Next: Use current GoTo official/current-country evidence first; do not revive exited markets unless confirmed active.

### ola
- Status: india_focus_after_international_exit
- Broad shape: Sources indicate Ola has exited UK/Australia/New Zealand ride-hailing and is focused on India, with 200+ Indian cities cited by app/store sources.
- Next: Treat India as active footprint; international historical markets as inactive unless new evidence says otherwise.

### indrive
- Status: broad_seed_large_emerging_market_footprint
- Broad shape: Official/company sources indicate roughly 48 countries and 1,000+ cities; repo already has Egypt, Morocco, India, sub-Saharan coastal buckets.
- Next: Start with official country list, then coastal Atlas-overlap countries; avoid full 1,000-city enumeration.

### cabify
- Status: broad_seed_spain_latam
- Broad shape: Official/help/about sources indicate Cabify operates across Spain and Latin America in about 6-7 countries / 40+ cities, with country/city help page available.
- Next: Use Cabify help city list as structured source; filter to coastal/Atlas overlap.

### freenow
- Status: broad_seed_europe_taxi_platform
- Broad shape: Official/transaction sources indicate 150-180+ cities across 9 European countries; now relevant to Lyft because of acquisition, but keep separate business-line provenance.
- Next: Scan official FREENOW city page; tag as Lyft-acquired but not Lyft-native until proposal framing is agreed.

### kakao-mobility
- Status: south_korea_national_service_seed
- Broad shape: Kakao T appears Korea-wide for taxi/mobility services; repo baseline already has Busan/Jeju/Seoul-area coastal relevance.
- Next: Use Korea city/service evidence to identify coastal/island gaps; do not over-expand inland Korea into marine footprint.

## Queue counts

- Total queued multi-cluster/seed partners: 19
- Existing registry partner baseline rows inspected: 47
