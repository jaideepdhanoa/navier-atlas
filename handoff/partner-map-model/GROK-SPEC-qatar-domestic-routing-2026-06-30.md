# GROK SPEC — Qatar MOT domestic routing seal (2026-06-30)

**Partner:** `qatar` · National transport authority (PTA category) · region MENA
**Gold reference:** `bahrain-motc` (PR #141). Same pattern, Qatar geography.
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-qatar.json` (sourced facts, anchors, hazards).
**Economics convention:** `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`.

Tasklet has rewritten the page (content + economics presentation). Every `route_id`/`route_ids`
is `null` with `_link_status: "pending-seal"` — **honest intentional-null until you seal.** Your job:
mint/bind boarding points, route every leg through navigable water with **zero land crossings**, rebind
route_ids, and regenerate the economics numbers from the clean Qatar domestic network.

## 1. Boarding points to mint/bind (anchors — snap to real berths)
From the dossier `domestic_network.boarding_points`. Anchors are approximate `[lng,lat]`; snap to the real
terminal/marina/jetty. **Bold = already built by the Ministry (Nov 2024 water-taxi terminals).**

| node | name | approx [lng,lat] | note |
|---|---|---|---|
| **lusail-ferry-terminal** | **Lusail Ferry Terminal** | 51.5320, 25.4200 | built; >2,200 sqm; electric-charging pontoon |
| **corniche-ferry-stop** | **Corniche / West Bay Ferry Stop** | 51.5320, 25.3200 | built; electric-charging pontoon |
| **pearl-ferry-stop** | **The Pearl Ferry Stop** | 51.5500, 25.3700 | built; electric-charging pontoon |
| katara-cultural-village | Katara Cultural Village | 51.5250, 25.3590 | planned station |
| old-doha-port | Old Doha Port (Mina District) | 51.5460, 25.2880 | cruise/port terminal |
| hamad-airport-jetty | Hamad International Airport waterfront | 51.6080, 25.2730 | planned HIA water link |
| al-wakrah-marina | Souq Al Wakrah Marina | 51.6080, 25.1650 | southern terminus |
| simaisma-marina | Simaisma | 51.5550, 25.6300 | northern station |
| al-khor-marina | Al Khor Marina | 51.5050, 25.6840 | northern terminus — **mint as new node + cluster city `al-khor-qatar`** |

> `al-khor-qatar` is referenced in route labels/narrative but was **removed from page `cities` arrays**
> (no registry entry yet). Mint the node, add the cluster city, then it can rejoin the city arrays.

## 2. Domestic corridors to seal (the spine — lead the proposal)
From `domestic_network.domestic_pairs`. Route each through the sheltered Gulf water off Doha; **no land crossings.**

| pair | from → to | ~nm | routing note |
|---|---|---|---|
| qa-d01 | lusail-ferry-terminal → corniche-ferry-stop | 4.0 | inner Doha Bay; round West Bay headland, never cut across the corniche land |
| qa-d02 | corniche-ferry-stop → pearl-ferry-stop | 3.5 | Doha Bay open water between the two stations |
| qa-d03 | lusail-ferry-terminal → pearl-ferry-stop | 2.5 | short bay hop; clear the Pearl breakwaters |
| qa-d04 | old-doha-port → hamad-airport-jetty | 4.2 | south along the port frontage; stay seaward of the airport land reclamation |
| qa-d05 | old-doha-port → katara-cultural-village | 3.0 | north along the bay frontage |
| qa-d06 | old-doha-port → al-wakrah-marina | 9.0 | south down the sheltered east coast; stay outside the port breakwaters |
| qa-d07 | lusail-ferry-terminal → simaisma-marina → al-khor-marina | 18.0 | north up the coast; two legs, snap to each marina entrance; clear shallow reef flats north of Lusail |

## 3. Regional link (secondary — do NOT lead)
| link | from → to | ~nm | note |
|---|---|---|---|
| qa-r01 | old-doha-port → manama-bahrain (Sa'ada Marina) | ~70 | Qatar↔Bahrain ferry corridor (live since Nov 2025). Quanta-LR. Route across open Gulf; snap Bahrain end to Sa'ada Marina. Optional Phase 3 only. |

## 4. Hand-waypoint + no-land-crossing rules (the whole game for a ministry)
- **Every leg routed through navigable water; `interior_land_km == 0`.** Hand-curate waypoints — do not let the
  router straight-line across the West Bay / Lusail / Pearl / airport land.
- **Pearl & Lusail are reclaimed islands** with breakwaters and marina mouths — snap entries to the real channel
  openings; no clipping the reclamation edges.
- **HIA reclamation:** keep the airport leg seaward of the runway land; approach the planned waterfront jetty only.
- **Reef/shallow flats** north of Lusail toward Simaisma/Al Khor — route the deep channel, no foiling over flats.
- Use the `data-clean/uae_hand_waypoints.json` `{from,to,waypoints:[[lng,lat]...]}` format for any hand legs.
- QA gate: run the land-intersection check; **any leg with interior_land_km > 0 fails the seal.**

## 5. Economics regen (under the PTA convention)
- Rungs are already relabelled plain (Operating revenue — starter / full national network / mature; Total
  water-transport market) and the super-app journey-GMV rung is dropped. **Re-derive the numbers** from the clean
  Qatar domestic network — the prior figures inherited a UAE-contaminated, super-app recal (see `growth_case.public_value._grok_regen`).
- Quantify `growth_case.public_value.levers` (CO₂ t/yr vs the 25%-by-2030 target, Doha-Bay road trips relieved,
  minutes saved) and add a fares/operating-model table. **Fares/cost-recovery = "set with the Ministry" — never fabricate subsidy.**

## 6. Done = all green
Schema · fidelity (journey_bp=0) · linkage (pending-seal → sealed) · geometry (interior_land_km==0) ·
seal-integrity · build. Then hand the nav/map state per the seal pipeline.
