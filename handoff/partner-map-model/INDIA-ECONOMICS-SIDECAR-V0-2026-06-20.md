# India economics sidecar v0 — cleanup pass 1

Status: **draft only until crosswalk / route sealing**  
Updated: 2026-06-20 23:55 IST

Global controls preserved:

- `route_id: null` everywhere
- `distance_status: pending_seal` everywhere
- `model_use: draft_only_until_crosswalk`
- ID-based matching only; `null` beats confidently-wrong
- AAI airport traffic remains quarantined
- Adani/Reliance remain overlay-only/no-footprint

## Cleanup results

### Goa fare / transfer comparables — improved

Promoted to source-backed comparables, still not sealed route economics.

Sources captured:

- Goa River Navigation Department Citizens Charter: RND operates regular ferry services on 21 routes. Foot passengers, two-wheelers, and three-wheelers are toll-exempt; four-wheeler and cargo tolls apply. Sample toll floors include car/jeep/3-wheeler ₹7–₹27 by route group, light commercial vehicle ₹15–₹43, medium commercial vehicle ₹20–₹33 where allowed, heavy vehicle ₹23–₹38 where allowed, and special trips ₹55 or ₹255 depending route group.
- Goa Directorate of Transport / Official Gazette taxi fare notification: 4-hour/50-km tourist taxi rates from ₹900 hatchback to ₹4,600 premium cab; 8-hour/100-km rates from ₹1,750 to ₹8,400; one-way per-km rates from ₹26 to ₹146 by vehicle class.
- GoaMiles rate card: hatchback ₹21.50/km, sedan ₹23/km, MUV ₹26/km, SUV ₹29/km, before convenience/toll/care/GST/minute/traffic add-ons.

Exact BP hygiene:

- Matched city: `goa-india`
- Matched BP examples: `bp-8c5afef8b1` Panaji Jetty, `bp-c3a5659ec3` Betim Ferry Terminal, `bp-8fb017e867` Ribandar Ferry, `bp-d91cefa66e` Old Goa Ferry Terminal.
- Caution: Goa alias search returns false positives outside India; bind only after country/region filtering.

### DSS Andaman fare PDF capture — still quarantined

- Official PDF path confirmed: `https://dss.andaman.gov.in/docs/press/DSS_Passenger_Fares_2025-26.pdf`
- Direct capture still failed due web/PDF retrieval instability.
- Search snippet confirms a revised 2025–26 DSS fare PDF exists and exposes partial fare rows including Two Wheelers/ThreeWheelers values `60` and `95`, but this is **not finance-safe** until the PDF is captured directly.

Exact BP hygiene:

- Matched city: `andaman-india`
- Matched BP examples: Port Blair Haddo/Phoenix Bay `bp-7f1d145a12`, Port Blair Marina Park `bp-7bef8fd1aa`, Port Blair Wharf `bp-970643cf81`, Havelock/Swaraj Dweep `bp-68d009dffb`, Neil/Shaheed Dweep `bp-56fad569af`.
- Caution: filter out Thailand Andaman aliases.

### DG Sea Connect direct fare / capacity capture — partially improved

Promoted operator demand-scale snippet; pricing remains pending.

- DG Sea Connect official site shell was captured.
- Official-site search snippet reports milestone counts: Passengers `15,70,000`; Cars `2,17,000`; Two Wheelers `1,66,000`; Cargo Vehicles `1,99,000`.
- Direct current fare ladder / booking-flow pricing was **not** captured. Third-party/social fare claims remain excluded.

### Kolkata-Haldia / Hooghly fare and current ridership — fare floor improved, ridership pending

- Direct official route list captured from West Bengal Transport Department. Routes include Howrah–Shipping/Millennium Park, Howrah–Fairlie, Dakshineswar–Belur, Fairlie–Ariyadaha via Howrah/Baghbazar/Belur/Kutighat, Lot No. 8–Kachuberia, Roychak–Kukrahati, Narayanpur–Namkhana LCT, Hasnabad–Par-Hasnabad LCT, and Nebukhali–Dulduli LCT.
- Official-document search snippet for WBIWTLSDP ESIA reports current ferry fares: single passenger ₹6, passenger + cycle ₹12, passenger + two-wheeler ₹30.
- Direct PDF extraction failed, so this remains `partial`.
- Current route/corridor ridership remains pending.

### Chennai / Vizag fare, passenger data, and exact BP binds — partially improved

Tamil Nadu / Chennai-side comparable:

- MEA confirms commencement of India–Sri Lanka passenger ferry connectivity.
- The Hindu captured Nagapattinam–Kankesanthurai service resumption: 83 passengers outbound from Nagapattinam and 85 return from KKS on resumption day; operator-reported one-way fare ₹4,250 and round-trip fare ₹8,500; 10 kg luggage included and ₹50/kg beyond the limit.
- Treat as media/operator-reported until direct operator/official booking capture succeeds.

Vizag / Andhra coast comparable:

- Visakhapatnam Port Authority cruise terminal page confirms Vizag International Cruise Terminal and ₹96 Cr investment.
- VPA Cruise Shipping page says a passenger ship from Visakhapatnam to Port Blair is available every month; distance is 1,100 nautical miles and passenger fare is about ₹5,000.
- VPA itinerary PDF lists 2026 domestic cruise calls for Empress and an international Odessy call in Dec 2026.

Exact BP hygiene:

- Kankesanthurai/KKS exists as `bp-4f36afc9f8`.
- Chennai, Nagapattinam, Visakhapatnam/Vizag did **not** match in current Atlas `FEATURES_BY_TYPE` search.
- Route IDs remain null; do not seal Chennai/Nagapattinam/Vizag corridors until India-side BPs are created or matched exactly.

## Finance-readiness update

Usable now as draft model inputs/comparables:

- Mumbai fare floors
- Kochi ridership/network scale
- Gujarat official RoPax time-savings/usage precedent
- Goa public ferry toll floor + official taxi + GoaMiles comparables
- Vizag official long-haul passenger-ship fare as a non-urban comparable

Still quarantined or partial:

- AAI airport traffic
- Andaman primary tourist table
- DSS fare PDF until direct PDF capture succeeds
- DG Sea Connect fare ladder until direct booking/page capture succeeds
- Kolkata-Haldia current ridership
- Chennai/Nagapattinam/Vizag exact India-side BP binds
- Nagapattinam-KKS fare until direct operator/official booking capture succeeds

## Next bite-sized cleanup

1. Capture DSS PDF through alternate network/browser path and extract route fare table.
2. Probe DG Sea Connect booking/API flow only enough to capture current fare ladder and vessel categories; do not book.
3. Add or request exact Atlas BPs for Chennai, Nagapattinam, Vizag if the proposal needs those corridors sealed.
4. Find official Hooghly current ridership by route or station; otherwise keep it out of model inputs.

### Mumbai Candela/JalVimana competitive validation — added

Uploaded Business Standard / NDTV Profit capture says the Candela P-12 electric hydrofoil “flying boat” launched in Mumbai, developed by Candela and set to be operated in India by JalVimana. The cited initial routes are Gateway of India → Alibaug and Gateway of India → Elephanta Island, with a planned Navi Mumbai airport → central Mumbai route expected to reduce travel time from ~90 minutes to under 30 minutes. The article also cites a planned fleet of 11 hydrofoiling Candela P-12 commuter ferries.

Use: **market validation / competitive context only**. Do **not** use this as a fare anchor, demand anchor, route-ID binding, or distance seal. M2M/PIB/Indian Express/The Hindu remain the current Mumbai source spine, with annual demand still null until direct route-level passenger counts are captured.
