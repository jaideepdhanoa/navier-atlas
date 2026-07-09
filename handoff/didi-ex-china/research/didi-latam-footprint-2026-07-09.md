# DiDi Latin America current-footprint audit

**As of:** 2026-07-09  
**Scope:** current consumer mobility marketed directly by DiDi or via its owned local brand 99. This audit excludes old launches without current confirmation, overseas-travel aggregation, food/fintech-only activity, office presence, unaffiliated taxi/JV products, and weak press/social claims.

## Result

DiDi’s official current-country help page names **10 Latin American operating countries**: Mexico, Brazil, Colombia, Chile, Costa Rica, Panama, Argentina, Ecuador, Peru, and the Dominican Republic. Brazil is an **owned-local-brand** operation through **99**, whose official company page says it has been part of DiDi since 2018. The other nine are classified as direct DiDi consumer operations.

The JSON records **18 country assessments** (10 positive + 8 tested additional markets) and **1465 city/source records**. Combined official source labels are split for normalization but preserve the original label; duplicates, typos, regions, and clusters are marked `source_cleanup_needed`.

| Country | Status | City/source records | High marine | Medium waterfront | Cleanup |
|---|---:|---:|---:|---:|---:|
| Mexico | direct_consumer_operation | 71 | 16 | 1 | 4 |
| Brazil | owned_local_brand | 1310 | 138 | 29 | 45 |
| Colombia | direct_consumer_operation | 20 | 4 | 1 | 0 |
| Chile | direct_consumer_operation | 28 | 11 | 0 | 10 |
| Costa Rica | direct_consumer_operation | 3 | 0 | 0 | 0 |
| Panama | direct_consumer_operation | 1 | 1 | 0 | 0 |
| Argentina | direct_consumer_operation | 20 | 2 | 10 | 0 |
| Ecuador | direct_consumer_operation | 2 | 1 | 0 | 0 |
| Peru | direct_consumer_operation | 3 | 1 | 0 | 0 |
| Dominican Republic | direct_consumer_operation | 7 | 5 | 0 | 0 |

## Marine-priority findings

Outside Brazil, high-relevance official city records include: Acapulco, Campeche, Cancún, Chetumal, Ciudad del Carmen, Coatzacoalcos, Ensenada, Guaymas, La Paz, Manzanillo, Mazatlán, Puerto Escondido, Puerto Vallarta, Tampico, Tijuana, Veracruz, Barranquilla, Buenaventura, Cartagena, Santa Marta, Antofagasta, Arica, Concepción, Iquique, La Serena, Coquimbo, Puerto Montt, Punta Arenas, Valdivia, Valparaíso, Viña del Mar, Buenos Aires, Mar del Plata, Ciudad de Panamá, Guayaquil, Lima, La Romana, Puerto Plata, Punta Cana, San Pedro de Macoris, Santo Domingo. Brazil has **138 high-marine records**, principally 99-listed cities matched to IBGE’s 2024 ocean-facing-municipality dataset; all are enumerated in the JSON with source URLs. Freshwater cities are conservatively marked medium.

## Additional claimed markets

Guatemala, Nicaragua, Honduras, El Salvador, Uruguay, Bolivia, Paraguay, and Venezuela are **uncertain**, not positive operations and not historical exits. None appears on the official current-country list, and this audit found no current official local operation page or credible launch confirmation. Negative evidence was not overstated.

## Strongest sources

1. [DiDi official: current operating countries](https://web.didiglobal.com/au/help-center/how-many-countries-does-didi-operate-in/) — definitive current-tense country list.
2. [99 official operating-cities index](https://99app.com/cidades/) — 1,308 Brazil source links before normalization/cleanup.
3. [99 official company page](https://99app.com/quem-somos/) — confirms 99 has been part of DiDi since 2018 and lists consumer mobility products.
4. Country-specific official DiDi “operating cities” pages for the nine direct-brand markets.
5. [IBGE 2024 ocean-facing municipalities](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/24072-municipios-defrontantes-com-o-mar.html) — marine classification for mapped Brazilian municipalities.
6. [DiDi Q1 2026 investor results](https://ir.didiglobal.com/static-files/ecefa64e-9101-4928-a628-89a2eeed2fd0) — confirms active/growing international mobility, but is not granular enough for country/city inference.

## Caveats / unresolved

- DiDi’s country and city pages use current tense but expose no update timestamp.
- Driver-facing city indexes may lag passenger booking availability and do not define service boundaries or product-by-city matrices.
- 99’s index contains duplicate/alias/region/cross-admin records; affected rows are explicitly flagged.
- Mexico’s `Quintana Roo` and `Sinaloa`, and Chile’s `Magallanes`, are regional labels, not canonical cities.
- No city record should be read as a corridor, boarding point, fare, demand, or full-municipality coverage claim.
