# New York Harbor — Navier Partner Brief & Corridor Economics
*2026-07-26 · deep-dive on our #1 US market · N30 Pioneer II, MID scenario, US cost basis*

## Thesis
New York Harbor is the largest urban water market in the Americas (~32.3M water-demand trips/yr; Staten Island Ferry 16.7M, NYC Ferry a record 7.4M in 2024) — and congestion pricing is now actively pushing trips onto the water. But the unit economics point to a specific wedge: **Navier's play here is the premium tier — above all the unclaimed airport-water link — not the subsidized mass ferry.** An 8-seat foiling vessel with a US crew can't compete at a $4.50 farebox; it wins where fares are premium and demand is captive.

## The economics that decide the strategy
A single N30 Pioneer II in NYC carries a **~$266K/yr fixed opex floor** — loaded crew $171K (a US captain at ~$95K × 1.8 FTE for year-round relief), plus insurance $22.5K (2.5% of the $900K US vessel), berth & port admin ~$45K, fast-charge berth/demand $18K, and maintenance $10K. At MID utilization one boat serves ~11,755 premium seats/yr. That fixed floor is the whole story:

| Fare / seat | Revenue/yr | EBITDA/yr | Margin | Payback |
|---|---|---|---|---|
| $4.50 *(NYC Ferry mass)* | $52,900 | **−$216,500** | — | — |
| $9 *(NY Waterway commuter)* | $105,800 | **−$163,700** | — | — |
| $18 *(premium express)* | $211,600 | **−$57,900** | — | — |
| **$25 *(breakeven line)*** | $293,900 | **+$24,400** | 8% | 37 yr |
| **$35 *(airport premium)*** | $411,400 | **+$142,000** | 35% | 6.3 yr |
| **$50 *(top premium)*** | $587,700 | **+$318,300** | 54% | 2.8 yr |

The read: mass-transit fares are a structural loss for an 8-seat premium vessel (exactly why NYC Ferry needs an $8.33/rider subsidy). **Break-even is ~$25/seat; real margins start at ~$35.** So we sell time, comfort and weather-stability at a premium — we do not chase the farebox.

## The flagship opportunity: the airport-water link (greenfield)
No fast premium water link exists to LaGuardia (whose **Marine Air Terminal literally sits on the water**) or JFK, despite congestion pricing making the roads worse. Modelled as a ~6 nm Midtown (Pier 79) → LaGuardia run:

- at **$35/seat**: ~$411K revenue, **~$136K EBITDA (33% margin), 6.6-yr payback**, ~160 t CO₂ avoided/vessel/yr;
- at **$50/seat**: ~$588K revenue, **~$312K EBITDA (53% margin), 2.9-yr payback**.

This is the highest-margin, most defensible entry: premium fare, captive airport demand, no incumbent, and a natural **Port Authority of NY & NJ** counterparty. *(This corridor is not yet a mapped Atlas route — it needs an Atlas route ID and Port Authority terminal validation before it graduates to a modelled corridor.)*

## Real Atlas corridors (the network-fill layer)
The six sourced NY Harbor corridors in our Atlas are the Pier 11 financial-district network plus the Staten Island crossing — all N30 Pioneer II, all short (0.5–4.4 nm):

Pier 11 → Paulus Hook (`ics-bdacfbafa1`, 1.4 nm) · Pier 11 → Hoboken (`ics-d5de69a39d`, 2.2 nm) · Pier 11 → South Williamsburg (`ics-f993f1e653`, 1.8 nm) · Pier 11 → Long Island City (`ics-db90a41958`, 3.6 nm) · Midtown/Pier 79 → Hoboken (`ics-25a683a51c`, 1.9 nm) · Whitehall → St. George / Staten Island (`ics-a5f00760b1`, 4.4 nm).

These are **premium-express / brand-building, not the profit engine**: even at a $25 premium-express fare they sit at ~break-even, and they only clear margin as the premium tier matures. Run them for network presence, congestion-pricing modal-shift volume, and the Uber/Lyft in-app story — subsidise them with the airport and luxury legs.

## The prize (grounded ladder)
- **Market:** ~32.3M water-demand trips/yr (Atlas).
- **Navier premium capture @ 10% (contested):** ~3.23M trips/yr.
- **SAM — Navier transport revenue/yr @ ~$22 blended premium:** **~$71M**.
- **Fleet to serve:** ~275 vessels → **~$247M hardware TAM**.
- **Journey GMV proxy (@ ~$35 all-in premium):** ~$113M/yr.

## Partner map & roles
- **Port Authority of NY & NJ** — the flagship counterparty for the **airport-water link** (LGA Marine Air Terminal, JFK): terminal access, concession, security integration. *Start here.*
- **Hornblower Group + NYC EDC** — Hornblower operates NYC Ferry (contract ≥2028) and Boston Harbor City Cruises; NYC EDC owns the program. The route to a **premium tier layered over the existing network** and the operator who can run the vessels.
- **Uber / Lyft** — the demand + booking layer ("a water tier inside the app"); Lyft is already a tracked Navier partner (multimodal + Citi Bike). Their role is filling premium-express and airport seats as congestion pricing bites.
- **NY Waterway / Seastreak** — commuter-ferry incumbents on the Pier 11 ↔ NJ corridors; fleet-upgrade / JV / vessel-supply partners for the network-fill layer.

## The ask / next steps
1. **Working session** with Port Authority on a LaGuardia Marine Air Terminal premium water pilot (terminal slot, fare band, security).
2. **Vessel demonstration** on the East River (Pier 11 / Pier 79).
3. **Pilot scope** — one premium airport route + one Pier 11 express, 2–4 vessels, with Uber/Lyft as the in-app demand channel.

## Assumptions & provenance
Model = the locked Navier N30 Pioneer II engine (8 seats, 70 nm, $900K US CAPEX, 20-yr straight-line, 2.5% insurance, $18K fast-charge berth, 274 op-days @ 0.75 uptime, MID = 0.55 seat × 0.65 revenue-leg, 15 revenue-legs/day cap, 10% contested capture). US inputs are **modelled planning values**, not operator quotes: captain ~$95K (US ferry-captain surveys, loaded ×1.8), Con Ed commercial energy ~$0.22/kWh, NYC berth/port admin ~$45K, NY grid ~0.20 kg CO₂/kWh. Corridors and distances are real Atlas routes; the airport link is an illustrative greenfield estimate pending an Atlas route + Port Authority validation. Fares: NYC Ferry $4.50 (published); NY Waterway commuter and premium/airport fares are benchmarked, not quoted.

Sources: [NYC Ferry fares](https://www.ferry.nyc/ticketing-info/) · [MTA congestion pricing 1-yr](https://www.mta.info/press-release/icymi-less-traffic-better-transit-its-first-anniversary-governor-hochul-celebrates) · [NYCEDC / Hornblower contract](https://edc.nyc/press-release/nycedc-announces-new-nyc-ferry-contract-hornblower-group) · US ferry-captain wage (Glassdoor/SalaryExpert/Salary.com) · [Con Edison rates](https://www.coned.com/en/accounts-billing/your-bill/time-of-use). Demand figures from the Navier Atlas `new-york-harbor-usa` brief.
