# India economics sidecar v0 — draft only until crosswalk

Created: 2026-06-20  
Status: source-backed v0; not final finance model

## Controls

- `route_id: null` for every row unless Atlas/Grok has sealed the route.
- `distance_status: pending_seal` until geometry is bound.
- `model_use: draft_only_until_crosswalk` throughout.
- AAI airport traffic remains quarantined until direct official page/PDF capture succeeds.
- Search snippets and inaccessible pages remain source leads only.
- Adani/Reliance remain overlay-only/no-footprint until exact Atlas IDs and partner asset route evidence exist.

## Readiness by market

| Market | Demand status | Pricing status | Draft economics use |
|---|---:|---:|---|
| Goa | sourced | pending | Strong tourism TAM; pricing still needs clean transfer/ferry comparable. |
| Mumbai / Navi Mumbai / Mandwa / Elephanta | partial | direct | Best v0 fare comparable via M2M RoPax fare floors. |
| Kochi / Kerala Water Metro | sourced | partial | Strongest ridership/network proof; current fare chart still needed. |
| Gujarat RoPax precedent | sourced | pending | Official travel-time and usage precedent; no direct fare ladder yet. |
| Andaman | partial | pending | Good island-mobility thesis; tourism/fare inputs not finance-safe yet. |
| Kolkata-Haldia | partial | pending | Strong infrastructure/opportunity framing; fare and volume still weak. |
| Chennai / Vizag | partial | pending | Keep lower-confidence tail until fare/passenger data and BP binds improve. |

## Market notes

### Goa

- `route_id: null`
- `distance_status: pending_seal`
- `demand_status: sourced`
- `pricing_status: pending`
- `model_use: draft_only_until_crosswalk`

**Economics read:** strong tourism TAM, not yet priceable. Goa Tourism reported **10,802,410 total tourist arrivals in 2025**, including **10,284,608 domestic** and **517,802 foreign** tourists. Goa also reported **189 charter flights** and **40,336 foreign tourists** in 2025 across Dabolim and Mopa.

**Next:** capture official Goa RND ferry toll/fare table, premium airport/resort transfer comparables, and keep AAI airport traffic out until direct capture works.

### Mumbai / Navi Mumbai / Mandwa / Elephanta

- `route_id: null`
- `distance_status: pending_seal`
- `demand_status: partial`
- `pricing_status: direct`
- `model_use: draft_only_until_crosswalk`

**Economics read:** best v0 pricing comparable. PIB supports route/terminal precedent across Belapur, DCT, Nerul, Elephanta, JNPT, Bhaucha Dhakka, Mandwa and Karanja. M2M Ferries gives direct fare floors: **passengers from ₹400**, **motorcycles from ₹210**, **4-wheelers from ₹1,020**, **bicycles from ₹110**, and **buses from ₹4,500**. The operator also states the vehicle deck can accommodate **over 120 cars, two-wheelers and buses**.

**Next:** capture trip/passenger volume and booking-class fare ladder; bind exact BPs before geometry economics.

### Kochi / Kerala Water Metro adjacency

- `route_id: null`
- `distance_status: pending_seal`
- `demand_status: sourced`
- `pricing_status: partial`
- `model_use: draft_only_until_crosswalk`

**Economics read:** strongest demand proof. Kochi Water Metro page captured **7,070,083 joined passengers**, **5,873 daily riders on 2026-06-19**, **75+ e-boats**, **15 routes**, and **75+ km**. The Water Metro DPR supports **16 routes**, **38 jetties**, **10 island communities**, **76 km**, and full Phase II fleet of **78 boats** with **10–20 minute headways**. DPR fare economics are old planning assumptions only, not current fare table.

**Next:** capture current official route fare chart and terminal-level ridership if available.

### Gujarat RoPax precedent / Ghogha-Hazira

- `route_id: null`
- `distance_status: pending_seal`
- `demand_status: sourced`
- `pricing_status: pending`
- `model_use: draft_only_until_crosswalk`

**Economics read:** clean precedent, not yet priceable. PIB states Ghogha-Hazira RoPax reduced travel time from **10 hours to 4 hours** and had facilitated **15,000+ trucks**, **50,000 cars**, and **around 2 lakh passengers** by the cited point. Gujarat Maritime Board supplies official Ro-Ro/RoPax strategic context.

**Next:** capture DG Sea Connect fare/capacity directly and exact-match Hazira/Ghogha BPs before any route promotion.

### Andaman / Port Blair

- `route_id: null`
- `distance_status: pending_seal`
- `demand_status: partial`
- `pricing_status: pending`
- `model_use: draft_only_until_crosswalk`

**Economics read:** good island-mobility logic, not finance-safe yet. IBEF fallback says 2024 arrivals were **7,10,397 domestic** and **11,497 foreign** tourists, but this is not the primary Andaman Tourism table. DSS proves official foreshore/inter-island/mainland ferry operations, passes, ticketing and cruises. DSS fare PDF path was found but not captured.

**Next:** retry DSS fare PDF and primary Andaman Tourism table; keep AAI Port Blair traffic quarantined.

### Kolkata-Haldia / Hooghly waterways

- `route_id: null`
- `distance_status: pending_seal`
- `demand_status: partial`
- `pricing_status: pending`
- `model_use: draft_only_until_crosswalk`

**Economics read:** strong infrastructure thesis. World Bank supports a **$105M** inland water transport project; more than **80%** of freight/passenger traffic crosses via three bridges; existing ferries serve **less than 2%** of passenger traffic; and KMA is framed around **30M people**.

**Next:** capture ferry fares, current passenger volumes and terminal upgrades; exact-bind Kolkata/Haldia/Howrah/Hooghly BPs.

### Chennai / Tamil Nadu and Vizag / Andhra coast

- `route_id: null`
- `distance_status: pending_seal`
- `demand_status: partial`
- `pricing_status: pending`
- `model_use: draft_only_until_crosswalk`

**Economics read:** lower-confidence v0 tail. MEA supports the India-Sri Lanka passenger ferry commencement. Vizag has official port context but not a clean passenger/fare economics row. Nagapattinam-KKS fare claims found in search are not finance-safe until direct official/operator capture.

**Next:** capture official/operator ferry fares and schedule for Nagapattinam-KKS; capture official Vizag passenger/cruise/AAI traffic data; split Chennai and Vizag into separate rows after stronger inputs.

## Finance readiness summary

**Can be used now for draft narrative/economics framing:** Goa, Mumbai/Navi Mumbai, Kochi, Gujarat precedent.

**Can be used as v0 model inputs with flags:**

- Mumbai M2M fare floors as premium water-transfer comparable.
- Kochi ridership/network scale as direct demand proof.
- Gujarat RoPax official travel-time and usage precedent.

**Still quarantined or partial:** AAI airport traffic, Andaman primary tourist table, DSS fare PDF, DG Ferry fare/capacity, Chennai/Vizag passenger traffic, Nagapattinam-KKS fare claims.

The compact answer: we can start India economics now; Grok is needed later to seal geometry/IDs, not to begin the research runway.

