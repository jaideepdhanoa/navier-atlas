# India Adani/Reliance exact-bind queue — 2026-06-21

Status: **research queue only**. This file does not create partner binds, executable corridors, fare assumptions, or demand assumptions.

## Guardrail

Use registry-first, ID-based matching only. Broad corporate or infrastructure adjacency is not a route bind. `null` beats confidently-wrong.

Promotion requires all of the following:

1. exact asset/source match;
2. exact reusable Atlas boarding-point or route ID;
3. explicit route relevance for passenger or captive mobility;
4. fare evidence if economics are requested;
5. demand evidence if fleet/pool economics are requested.

Until then, every item below remains `candidate_only_no_bind` and contributes zero to finance outputs.

## Adani queue

| Candidate label | Source-backed asset | Official evidence captured | Safe proposal angle | Required next validation | Status |
|---|---|---|---|---|---|
| `adani_nmia_ulwe_airport_waterfront_access_candidate` | Navi Mumbai International Airport, Ulwe / Navi Mumbai | NMIA contact page lists S17-C, New Project Office, near Ulwe Gaothan Bus Stop, Amara Marg, Ulwe, Navi Mumbai 410206. Prior NMIA release captured high-capacity airport/connectivity context. | Premium airport/waterfront transfer concept if a real MMR waterfront node can be reused. | Find exact reusable Atlas boarding point(s) around Mumbai/Navi Mumbai; prove passenger transfer relevance; do not infer demand from airport capacity. | `candidate_only_no_bind` |
| `adani_dighi_agardanda_dighi_port_infrastructure_candidate` | Dighi Port, Maharashtra | Adani Ports page describes Dighi as an all-weather deep-draft multipurpose port; lists Agardanda Terminal and Dighi Terminal road links to NH66 via Indapur/Mangaon; direct berthing and cargo/marine infrastructure. | Maharashtra coastal-infrastructure narrative; possible executive/captive access only after route proof. | Exact coordinates / BP IDs for Dighi and Agardanda terminals; passenger/captive-mobility evidence; route relevance. | `candidate_only_no_bind` |
| `adani_hazira_port_surat_industrial_waterfront_candidate` | Hazira Port, Surat, Gujarat | Adani Ports page describes Hazira as a deep-water, multi-product commercial port in Surat, Gujarat with bulk/liquid/container/marine services, Delhi-Mumbai Industrial Corridor proximity, and rail/road/air connectivity notes. | Gujarat industrial waterfront adjacency and potential enterprise access narrative. | Exact BP/route match; separate from Reliance Hazira industrial seed; prove passenger/captive-mobility use case before proposal corridor. | `candidate_only_no_bind` |
| `adani_mundra_port_kutch_enterprise_waterfront_candidate` | Mundra Port, Kutch, Gujarat | Adani Ports page describes Mundra as India’s largest commercial port / mega port with deep-draft all-weather infrastructure, multimodal connectivity, container, liquid, crude, marine, RO-RO, STS services. | Strategic enterprise/logistics-infrastructure context; not passenger demand. | Exact BP/route match; evaluate whether relevant to partner proposal before adding to deck narrative. | `candidate_only_no_bind` |

### Adani source URLs

- NMIA contact: `https://navimumbai.adaniairports.com/en/contact-us`
- NMIA release: `https://www.adani.com/newsroom/media-releases/pm-modi-inaugurates-navi-mumbai-international-airport`
- Dighi Port: `https://www.adaniports.com/ports-and-terminals/dighi-port`
- Hazira Port: `https://www.adaniports.com/ports-and-terminals/hazira-port`
- Mundra Port: `https://www.adaniports.com/ports-and-terminals/mundra-port`

## Reliance queue

| Candidate label | Source-backed asset | Official evidence captured | Safe proposal angle | Required next validation | Status |
|---|---|---|---|---|---|
| `reliance_rcp_ghansoli_navi_mumbai_waterfront_access_candidate` | Reliance Corporate Park, Navi Mumbai / Ghansoli | RIL media-kit page confirms Reliance Corporate Park (RCP), Navi Mumbai. Search/source snippets identify Ghansoli / Thane-Belapur Road context, but proposal artifact should cite RIL page as the official source and keep street-level detail pending official confirmation. | Corporate-demand overlay near Navi Mumbai only if a waterfront transfer node is exact. | Official street-level source or coordinate confirmation; exact BP/route match; no employee-demand assumption. | `candidate_only_no_bind` |
| `reliance_nariman_point_corporate_office_waterfront_candidate` | RIL Corporate Office, Nariman Point, Mumbai | RIL contact page lists Reliance Industries Limited, Maker Chambers IV, Nariman Point, Mumbai 400021, India. | South Mumbai CBD executive/corporate access narrative if an exact waterfront node is reused. | Exact BP/route ID near Nariman Point / Gateway / south-Mumbai waterfront; route relevance; fare/demand evidence if economics requested. | `candidate_only_no_bind` |
| `reliance_jamnagar_giga_complex_industrial_mobility_candidate` | Dhirubhai Ambani Green Energy Giga Complex, Jamnagar | RIL New Energy page states over 5,000 acres in Jamnagar for giga factories; transcript includes segregated people/material circulation, 550 trucks per day for 20 GW, and 20,000+ people for 20 GW in all shifts. RIL refining page separately describes Jamnagar as the world’s largest/most complex single-site refinery with marine logistics access. | Gujarat industrial/new-energy scale; possible captive mobility narrative only after geometry and use-case proof. | Exact Jamnagar waterfront/route geometry; passenger/captive mobility source; do not convert people/truck counts into ferry demand. | `candidate_only_no_bind` |
| `reliance_hazira_carbon_fibre_industrial_candidate` | Reliance carbon-fibre plant, Hazira | RIL New Energy page says Reliance will build India’s first and one of the world’s largest carbon-fibre plants at Hazira, 20,000 MTPA target capacity, with first phase during 2025. | Hazira industrial-materials adjacency; candidate narrative if paired carefully with Gujarat coastal industrial map. | Exact facility coordinates or official address; avoid conflating with Adani Hazira Port; exact route/BP match. | `candidate_only_no_bind` |

### Reliance source URLs

- RIL contact: `https://www.ril.com/contact-us`
- RCP Navi Mumbai media kit: `https://www.ril.com/news-media/resource-center/media-kit/rcp-navi-mumbai`
- RIL New Energy & New Materials: `https://www.ril.com/businesses/new-energy-materials`
- RIL Refining & Marketing / Jamnagar: `https://www.ril.com/businesses/energy/refining-marketing`

## Immediate work queue

1. **Registry-first lookup**
   - Query existing shared registry / Atlas boarding points for Mumbai, Navi Mumbai, Ulwe, Dighi, Agardanda, Hazira, Mundra, Jamnagar.
   - Reuse existing IDs only; do not create new BPs in this queue step.

2. **Exact-label crosswalk**
   - Produce `known / unknown / blocked` for each asset.
   - Accept only `OK_EXACT_LABEL_HIT` or keep null.

3. **Narrative packet draft**
   - Adani: airport + port infrastructure adjacency, with NMIA and Dighi first; Hazira/Mundra as optional India enterprise context.
   - Reliance: Mumbai/Navi Mumbai corporate + Gujarat industrial/new-energy scale; do not claim existing water mobility.

4. **Economics gate**
   - No fare, demand, fleet, pool, revenue, or utilization fields until route-specific sources exist.

## Explicit non-actions

- Do not edit partner footprint JSON.
- Do not edit `finance/model/corridors.json`.
- Do not seal to Atlas.
- Do not cascade to Sheets.
- Do not use these sources as TAM/demand counts.
