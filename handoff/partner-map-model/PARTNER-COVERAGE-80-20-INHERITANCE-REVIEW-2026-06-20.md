# Partner Coverage 80:20 Inheritance Review — 2026-06-20

Review artifact only: no partner JSON, map scope, network footprint, or economics sheets are mutated here.

## Rule change captured

Credible country/region evidence may inherit **existing Atlas** coastal/island/waterfront registry cities inside that scope. We still do not create new geography from country evidence. Every inherited bind carries an evidence tier.

## Human review exclusions now applied

- **Bolt Malaysia** net-new binds are limited to **Penang** and **Sabah / Kota Kinabalu**.
- **Bolt Mexico** and **Bolt Morocco** have been removed from net-new candidate binds.
- **NEOM** and **Red Sea Global** have been removed from all net-new partner binds because those markets are exclusive to PIF / Red Sea Global / sovereign channels.
- Removed candidate bind rows: **16**.

## Accounting clarification

`already_covered_no_shrink` is **not total partner baseline coverage**. It only counts rows that were already covered **inside this incremental 80:20 inheritance candidate set**. Existing partner coverage is reported separately from `partner-global-registry-map.json` so partial/additive source scans cannot make partners such as Yango or Uber look empty.

## Headline counts
- **partners_scanned**: ['bolt', 'cabify', 'didi', 'freenow', 'gojek', 'grab', 'indrive', 'kakao-mobility', 'lyft', 'ola', 'uber', 'yango']
- **partner_scope_count**: 182
- **atlas_registry_city_count**: 208
- **atlas_registry_city_count_with_inferred_country**: 205
- **country_supported_candidate_rows_total**: 299
- **net_new_partner_market_binds_total**: 195
- **already_covered_no_shrink_total**: 104 *(incremental candidate-set overlap only)*
- **exact_supported_additive_rows_carried_forward**: 18
- **multi_partner_candidate_markets_2plus**: 104
- **true_gap_country_scopes_after_inheritance**: 87

## Existing baseline coverage snapshot

Source: `partner-global-registry-map.json`. Counts below are per-partner sums; the same Atlas city can appear under multiple partners.

- **partners_with_baseline_record**: 10
- **partners_without_baseline_record**: ['cabify', 'freenow']
- **existing_baseline_partner_market_rows_sum**: 83
- **existing_baseline_mapped_market_rows_sum**: 82
- **existing_baseline_unique_registry_city_ids_partner_sum**: 223

## Net-new promotion lanes
- **promote_new_display_and_economics_corridor_candidate**: 116
- **promote_new_display_and_marquee_economics_candidate**: 49
- **thin_market_country_supported_route_grounding_candidate**: 30

## Net-new density counts
- **full_display_geometry_no_economics**: 116
- **marquee_economics_ready**: 49
- **thin_brief_only_needs_route_grounding**: 30

## Partner accounting — baseline vs incremental inheritance

| Partner | baseline market rows | baseline unique Atlas city IDs | incremental scope matches | already covered within incremental scope | net-new incremental binds | marquee/econ-ready new | display+econ-corridor new | thin route-grounding new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bolt | — | — | 72 | 40 | 32 | 8 | 15 | 9 |
| cabify | — | — | 5 | 0 | 5 | 1 | 4 | 0 |
| didi | — | — | 13 | 11 | 2 | 0 | 1 | 1 |
| freenow | — | — | 30 | 0 | 30 | 8 | 18 | 4 |
| gojek | — | — | 14 | 10 | 4 | 1 | 3 | 0 |
| grab | — | — | 33 | 17 | 16 | 7 | 9 | 0 |
| indrive | — | — | 70 | 13 | 57 | 20 | 29 | 8 |
| kakao-mobility | — | — | 4 | 4 | 0 | 0 | 0 | 0 |
| lyft | — | — | 16 | 5 | 11 | 0 | 10 | 1 |
| ola | — | — | 4 | 4 | 0 | 0 | 0 | 0 |
| uber | — | — | 28 | 0 | 28 | 2 | 20 | 6 |
| yango | — | — | 10 | 0 | 10 | 2 | 7 | 1 |

## Focus partner notes

### bolt
- Existing baseline: **—** partner-market rows, **—** unique Atlas registry city IDs.
- Incremental 80:20 candidate set: **72** matches; **40** already-covered within that incremental set; **32** net-new additive binds.
- Human review filter applied: Malaysia keeps **Penang** and **Sabah / Kota Kinabalu** only; Mexico and Morocco removed; NEOM / Red Sea Global removed as sovereign-exclusive.
- Net-new by country: Greece (3), Italy (1), Kenya (2), Malaysia (2), Malta (1), New Zealand (2), Nigeria (1), Norway (3), South Africa (1), Taiwan (2), Tanzania (4), Thailand (3), United Arab Emirates (6), United Kingdom (1).

### grab
- Existing baseline: **—** partner-market rows, **—** unique Atlas registry city IDs.
- Incremental 80:20 candidate set: **33** matches; **17** already-covered within that incremental set; **16** net-new additive binds.
- Net-new by country: Indonesia (10), Malaysia (3), Philippines (3).

### uber
- Existing baseline: **—** partner-market rows, **—** unique Atlas registry city IDs.
- Incremental 80:20 candidate set: **28** matches; **0** already-covered within that incremental set; **28** net-new additive binds.
- Net-new by country: Bahrain (1), Barbados (1), Canada (1), Colombia (1), Costa Rica (1), Dominican Republic (1), Ecuador (4), Jamaica (1), Kenya (2), New Zealand (2), Norway (3), Panama (1), Portugal (2), South Africa (1), South Korea (4), Sri Lanka (1), Sweden (1).

### yango
- Existing baseline: **—** partner-market rows, **—** unique Atlas registry city IDs.
- Incremental 80:20 candidate set: **10** matches; **0** already-covered within that incremental set; **10** net-new additive binds.
- Yango note: `0 already covered` is only within the new additive seed scopes. It does **not** mean Yango had no baseline.
- Net-new by country: Bahrain (1), Colombia (1), Finland (1), Norway (3), Oman (3), Sri Lanka (1).

## Top multi-partner density candidates

| Market | Country | partners in scope | net-new partner candidates | density lane | routes | economics keys |
|---|---|---:|---:|---|---:|---:|
| Sumba (`sumba-indonesia`) | Indonesia | 3 | 3 | full_to_marquee_candidate | 8 | 1 |
| Phuket / Phang Nga (`phuket-phang-nga-thailand`) | Thailand | 3 | 2 | full_to_marquee_candidate | 188 | 1 |
| Koh Samui / Koh Phangan / Koh Tao (`koh-samui-thailand`) | Thailand | 3 | 2 | full_to_marquee_candidate | 102 | 1 |
| Sabah / Kota Kinabalu (`sabah-kota-kinabalu-malaysia`) | Malaysia | 3 | 2 | full_to_marquee_candidate | 76 | 2 |
| Penang (George Town) (`penang-malaysia`) | Malaysia | 3 | 2 | full_to_marquee_candidate | 70 | 2 |
| Lombok (`lombok-indonesia`) | Indonesia | 3 | 2 | full_to_marquee_candidate | 48 | 1 |
| Komodo / Labuan Bajo (`komodo-flores-indonesia`) | Indonesia | 3 | 2 | full_to_marquee_candidate | 30 | 1 |
| Ibiza & Formentera (`ibiza-spain`) | Spain | 3 | 2 | full_to_marquee_candidate | 21 | 1 |
| Bali (`bali-indonesia`) | Indonesia | 3 | 1 | full_to_marquee_candidate | 131 | 1 |
| Manama (`manama-bahrain`) | Bahrain | 2 | 2 | full_to_marquee_candidate | 105 | 11 |
| Manila (`manila-philippines`) | Philippines | 2 | 2 | full_to_marquee_candidate | 95 | 1 |
| Cebu / Mactan (`cebu-philippines`) | Philippines | 2 | 2 | full_to_marquee_candidate | 94 | 1 |
| Langkawi (`langkawi-malaysia`) | Malaysia | 2 | 2 | full_to_marquee_candidate | 62 | 3 |
| Desaru Coast (Johor) (`desaru-coast-malaysia`) | Malaysia | 2 | 2 | full_to_marquee_candidate | 42 | 1 |
| Rhodes & the Dodecanese (`rhodes-dodecanese-greece`) | Greece | 2 | 2 | full_to_marquee_candidate | 38 | 1 |
| Mykonos & the Cyclades (`mykonos-greece`) | Greece | 2 | 1 | full_to_marquee_candidate | 91 | 1 |
| Jeddah (`jeddah-ksa`) | Saudi Arabia | 2 | 1 | full_to_marquee_candidate | 86 | 4 |
| Boracay / Caticlan (`boracay-philippines`) | Philippines | 2 | 1 | full_to_marquee_candidate | 56 | 1 |
| Phu Quoc (`phu-quoc-vietnam`) | Vietnam | 2 | 1 | full_to_marquee_candidate | 44 | 1 |
| Côte d'Azur (French Riviera) (`cote-dazur-france`) | France | 2 | 1 | full_to_marquee_candidate | 42 | 1 |
| Helsinki & the Archipelago (`helsinki-finland`) | Finland | 2 | 1 | full_to_marquee_candidate | 40 | 1 |
| Amalfi Coast & Capri (`amalfi-coast-italy`) | Italy | 2 | 1 | full_to_marquee_candidate | 36 | 1 |
| Athens & the Saronic Gulf (`athens-saronic-greece`) | Greece | 2 | 1 | full_to_marquee_candidate | 32 | 1 |
| Stockholm Archipelago (`stockholm-sweden`) | Sweden | 2 | 1 | full_to_marquee_candidate | 30 | 1 |
| Lagos (Lagos Lagoon) (`lagos-nigeria`) | Nigeria | 2 | 1 | full_to_marquee_candidate | 23 | 1 |
| Da Nang / Hoi An / Lang Co (`da-nang-hoi-an-vietnam`) | Vietnam | 2 | 1 | full_to_marquee_candidate | 21 | 1 |
| Ha Long Bay (`ha-long-bay-vietnam`) | Vietnam | 2 | 1 | full_to_marquee_candidate | 18 | 1 |
| Venice Lagoon (`venice-italy`) | Italy | 2 | 1 | full_to_marquee_candidate | 16 | 1 |
| Dublin Bay & the East Coast (`dublin-ireland`) | Ireland | 2 | 1 | full_to_marquee_candidate | 13 | 1 |
| Ho Chi Minh City (Saigon River) + Vung Tau (`ho-chi-minh-city-vietnam`) | Vietnam | 2 | 1 | full_to_marquee_candidate | 11 | 1 |
| Singapore (`singapore`) | Singapore | 2 | 0 | full_to_marquee_candidate | 280 | 2 |
| Cartagena & the Rosario Islands (`cartagena-colombia`) | Colombia | 5 | 4 | thin_to_full_economics_corridor_candidate | 25 | 0 |
| Karimunjawa (`karimunjawa-central-java-indonesia`) | Indonesia | 3 | 3 | thin_to_full_economics_corridor_candidate | 31 | 0 |
| Bergen & the Fjords (`bergen-norway`) | Norway | 3 | 3 | thin_to_full_economics_corridor_candidate | 30 | 0 |
| Stavanger & Lysefjord (`stavanger-norway`) | Norway | 3 | 3 | thin_to_full_economics_corridor_candidate | 25 | 0 |
| Geirangerfjord (`geiranger-norway`) | Norway | 3 | 3 | thin_to_full_economics_corridor_candidate | 22 | 0 |
| Likupang & Bunaken (North Sulawesi) (`likupang-north-sulawesi-indonesia`) | Indonesia | 3 | 3 | thin_to_full_economics_corridor_candidate | 15 | 0 |
| Lake Toba (Samosir) (`lake-toba-samosir-indonesia`) | Indonesia | 3 | 3 | thin_to_full_economics_corridor_candidate | 1 | 0 |
| Bangkok (`bangkok-thailand`) | Thailand | 3 | 2 | thin_to_full_economics_corridor_candidate | 69 | 0 |
| Bintan & the Riau Islands (`riau-islands-indonesia`) | Indonesia | 3 | 2 | thin_to_full_economics_corridor_candidate | 59 | 0 |
| San Blas (Guna Yala) Archipelago (`san-blas-panama`) | Panama | 3 | 2 | thin_to_full_economics_corridor_candidate | 52 | 0 |
| Mallorca & the Balearics (`mallorca-spain`) | Spain | 3 | 2 | thin_to_full_economics_corridor_candidate | 49 | 0 |
| Samaná Peninsula & Bay (`samana-dominican-republic`) | Dominican Republic | 3 | 2 | thin_to_full_economics_corridor_candidate | 38 | 0 |
| Raja Ampat (`raja-ampat-indonesia`) | Indonesia | 3 | 2 | thin_to_full_economics_corridor_candidate | 31 | 0 |
| Wakatobi (`wakatobi-southeast-sulawesi-indonesia`) | Indonesia | 3 | 2 | thin_to_full_economics_corridor_candidate | 26 | 0 |
| Cape Town (`cape-town-south-africa`) | South Africa | 3 | 2 | thin_to_full_economics_corridor_candidate | 19 | 0 |
| Barcelona & the Costa Brava (`costa-brava-spain`) | Spain | 3 | 2 | thin_to_full_economics_corridor_candidate | 14 | 0 |
| Mombasa (`mombasa-kenya`) | Kenya | 3 | 2 | thin_to_full_economics_corridor_candidate | 9 | 0 |
| Banda Islands (Maluku) (`banda-maluku-indonesia`) | Indonesia | 3 | 2 | thin_to_full_economics_corridor_candidate | 3 | 0 |
| Menorca (Balearics) (`menorca-spain`) | Spain | 3 | 2 | thin_to_full_economics_corridor_candidate | 2 | 0 |
| Lamu Archipelago (`lamu-kenya`) | Kenya | 3 | 2 | thin_to_full_economics_corridor_candidate | 1 | 0 |
| Jakarta (`jakarta-indonesia`) | Indonesia | 3 | 1 | thin_to_full_economics_corridor_candidate | 112 | 0 |
| Derawan Islands (East Kalimantan) (`derawan-berau-east-kalimantan-indonesia`) | Indonesia | 3 | 1 | thin_to_full_economics_corridor_candidate | 6 | 0 |
| Colombo & South Coast Resort Belt (`colombo-sri-lanka`) | Sri Lanka | 2 | 2 | thin_to_full_economics_corridor_candidate | 77 | 0 |
| Nicoya Peninsula & Papagayo (`nicoya-papagayo-costa-rica`) | Costa Rica | 2 | 2 | thin_to_full_economics_corridor_candidate | 69 | 0 |
| Palawan (El Nido / Coron) (`palawan-philippines`) | Philippines | 2 | 2 | thin_to_full_economics_corridor_candidate | 40 | 0 |
| Montego Bay & Jamaica (`montego-bay-jamaica`) | Jamaica | 2 | 2 | thin_to_full_economics_corridor_candidate | 19 | 0 |
| Crete (`crete-greece`) | Greece | 2 | 2 | thin_to_full_economics_corridor_candidate | 16 | 0 |
| London (River Thames) (`london-thames-uk`) | United Kingdom | 2 | 2 | thin_to_full_economics_corridor_candidate | 16 | 0 |
| Bay of Islands (`bay-of-islands-new-zealand`) | New Zealand | 2 | 2 | thin_to_full_economics_corridor_candidate | 15 | 0 |

## How to use this

1. Review `candidate_inherited_binds` in the JSON for partner-by-partner promotion batches.
2. Promote country/region-supported rows to partner display only when the registry ID already exists and the evidence tier is carried forward.
3. Use `multi_partner_density_promotion_candidates` to choose thin → full and full → marquee/economics-corridor upgrades.
4. Use the Phase 3 artifact for true shared registry gaps only; do not treat human-excluded binds as gaps.

Full machine-readable artifact: `partner-coverage-80-20-inheritance-review-2026-06-20.json`.
Phase 3 artifact: `partner-coverage-phase-3-shared-registry-gap-queue-2026-06-20.json`.
