# Drop ledger — Bay Area & New York demand pools

Every row present in the source employer trackers that did **not** reach the published block, and why.
No silent drops.

Sources: `Bay Employer Tracker v2` (37 rows) · `NY Employer Tracker v1` (31 rows).
Canon checked against: `MARINA-GAP-CHECK.md`, `EMPLOYER-UNIVERSE-V2.md` (esp. Part 4 — "do not use in
pitch materials without further sourcing"), `CURRENT-BAY-STOPS.txt`, `CURRENT-NY-STOPS.txt`, hub.json.

## Bay Area — 6 tracker rows dropped

| Row | Seats in tracker | Reason |
|---|---|---|
| **Gilead (Foster City)** | 180 | **No verified landing.** Foster City's only launches — Boat Park and Leo J. Ryan Park — are on the interior Foster City Lagoon; USACE material documents intake/outfall and emergency-rescue ramps, not a navigable Bay passage or a 30–45 ft commercial berth. There is no Foster City stop in `hub.json`. Failed locations stay off every surface. |
| **Stripe (Oyster Point)** | 60 | **Wrong location and unverified headcount.** Our own employer universe records Stripe's verified HQ as 510 Townsend St, SoMa, and lists "Stripe = Oyster Point" in Part 4 as a documentation error. The 2,000 figure traces to 2019 reporting of *worldwide* headcount. Both the binding and the number fail. |
| **Box (Redwood City)** | 36 | Headcount flagged unverified in the employer universe; small pool; no independent source located in this pass. |
| **Commute.org (peninsula TMA)** | — | Not demand. A commute aggregator — a distribution partner, not a rider pool. No headcount. |
| **Mission Bay TMA** | — | Same: partner, not demand. No headcount. |
| **Bay Area Council** | — | Same: convener/association, not demand. No headcount. |

Tracker total 3,717 → published **3,441**.

## New York — 1 tracker row dropped

| Row | Seats in tracker | Reason |
|---|---|---|
| **RXR / Starrett-Lehigh tenants** | — | No headcount, and no defensible stop binding: 601 W 26th St is thirteen blocks from Pier 79, the nearest landing, and there is no Chelsea stop in `hub.json`. |

Tracker total 2,769 → published **2,769** (the dropped row carried no seats).

## Rows kept but materially reframed

| Row | Tracker said | Published as | Why |
|---|---|---|---|
| **NewYork-Presbyterian / Weill Cornell** | 45,000, Upper East Side | "~45,000 system-wide", East 34th Street, note says about a mile away by ground shuttle | Part 4 flags the "10-min walk" claim as unverified — the campuses sit ~1–1.5 miles from the mapped landing. 45,000 is system-wide, not on-site. |
| **Memorial Sloan Kettering** · **Rockefeller University** | Upper East Side, walk implied | East 34th Street, note says ground shuttle | Same. Canon is explicit: shuttle from E 34th, no E 66th–68th landing exists. |
| **Oracle · Electronic Arts (Redwood City)** | Redwood City node | Port of Redwood City Municipal Marina, note says ground shuttle | Part 4: "no large-headcount employer verified as physically at/adjacent to the Port of Redwood City itself; Box/Oracle etc. are Redwood City tech employers generally, not port-adjacent." |
| **Meta** | 15,000, Redwood City via shuttle | "~15,000 in Menlo Park (directional)", note says about seven miles inland, never a walk | The distance is material and was invisible in the tracker. |
| **Goldman Sachs** | Goldman corridor, 200 West + 30 Hudson | Brookfield Place / BPC, no number | Part 4: 30 Hudson St is now multi-tenant and Goldman-specific headcount could not be verified. 200 West St stands on its own as a walk. |
| **Salesforce · OpenAI · Uber · Brooklyn Navy Yard** | bare numbers | "(directional)" suffix on each | Part 4 names exactly these as company/location verified but on-site headcount unconfirmed. |
| **BlackRock · Wells Fargo · KKR · Amazon** | node "Gold Coast" | Midtown West / Pier 79 | "Gold Coast" reads as New Jersey; these are Manhattan west-side employers on the Hudson Line. |

## Open question for Jaideep

**NewYork-Presbyterian alone is 1,350 of New York's 2,769 seats — 49% of the city total — and it rests
on a system-wide staff figure for campuses a mile from the water.** The row is published with both
caveats visible. If you would rather the city total not lean that hard on one soft number, the options
are to exclude it from the total (total becomes 1,419) or to hold the row at a site-level figure once
someone sources one. Flagging rather than deciding.

**Second, smaller conflict:** the playbook says MSK / Weill Cornell / Rockefeller shuttle from **E 34th**;
the employer universe maps the same campuses ~1–1.5 miles from **E 90th**. Both stops exist. I used
E 34th per the playbook. Worth settling once, since it drives the East Side geometry.
