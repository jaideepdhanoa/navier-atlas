# India Mumbai demand/fare gate — 2026-06-21

Status: **source-backed market scale found; route-level demand still not executable**.

This note preserves exactness over coverage for the India economics cascade. It does **not** promote new executable economics rows by itself.

## Gate result

| Gate | Result | Model action |
|---|---|---|
| Mumbai/Mandwa fare | **Direct fare floor available** from M2M Ferries | Keep as pricing anchor / comparable; do not execute without demand |
| Mumbai/Mandwa annual demand | **Not route-level closed** | Keep annual demand `null`; row contributes zero until sourced |
| Mumbai/MMR market scale | **Source-backed high-level anchor** | Use as narrative/market context only |
| Maharashtra dataset rows | **Resource identified, rows not extracted** | Do not infer route counts from metadata |
| Kochi | **Candidate official ridership/fare leads found** | Keep out of executable corridors until exact route-level fare+demand mapping is closed |

## Mumbai source anchors captured

### Maharashtra passenger water transport dataset metadata

- Source: Open Government Data Platform India / Maharashtra Maritime Board
- URL: `https://kerala.data.gov.in/resource/statistics-annual-passenger-water-transport-maharashtra-2022-23-2024-25`
- Resource path exposed in API tab: `/resource/aad4ae5e-5229-496e-8405-4c5b29069e19`
- Captured metadata note: Maharashtra Maritime Board operates passenger water transport on **36 routes**, including **7 Ro-Pax services**, carrying about **18 million passengers annually**. Of these, **21 routes are in the Mumbai Metropolitan Region (MMR)**, connecting Gateway of India, Versova, Madh, Mandwa, Mora, Elephanta, Rewas, and Belapur.
- Constraint: download requires captcha; public API key returned `Key not authorised`. Dataset values were **not** extracted.
- Use: market-scale/context anchor only. It is not exact enough to annualize Mumbai Ferry Wharf/Bhaucha Dhakka ↔ Mandwa or any single route.

### M2M Ferries fare anchor

- Source: M2M Ferries official page
- URL: `https://www.m2mferries.com/`
- Captured metrics: Mumbai Ferry Wharf/Bhaucha Dhakka ↔ Mandwa Ro-Pax service; passenger fares from ₹400 onwards; motorcycle ₹210 onwards; four-wheelers ₹1,020 onwards; bicycles ₹110 onwards; buses ₹4,500 onwards; vehicle deck over 120 cars/two-wheelers/buses.
- Use: direct published fare floor / premium ferry comparable.
- Constraint: no annual passenger count captured from operator page in this pass.

### PIB route precedent

- Source: PIB Ministry of Ports, Shipping and Waterways
- URL: `https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1799056`
- Captured metrics: Belapur water taxi connects Mumbai/Navi Mumbai nodes including DCT, Nerul, Belapur, Elephanta and JNPT; Belapur jetty enables movement to Bhaucha Dhakka, Mandwa, Elephanta and Karanja.
- Use: route/terminal precedent only.

## Decision for next model patch

Do **not** change Mumbai executable economics yet:

- `fare_inr`: can be referenced in sidecar as fare floor, but should not be treated as closed executable economics without demand.
- `annual_demand`: remains `null` for Mumbai/Mandwa rows until route-level annual passenger count or operator-reported route ridership is sourced.
- `pool`, `fleet`, contribution: remain zero under current model behavior.

## Next exact-bind task

Find one of:

1. M2M annual passengers or route ridership, operator-reported; or
2. MMB dataset row values for Mandwa / Gateway / Bhaucha Dhakka / Belapur / Elephanta; or
3. an official authority report with route-level passenger counts.

Until then: **visible registry row, zero contribution**.
