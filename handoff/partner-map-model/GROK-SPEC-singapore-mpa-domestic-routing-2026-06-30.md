# GROK SPEC — Singapore MPA domestic routing seal (2026-06-30)

**Partner:** `singapore-mpa` · National transport authority (PTA category) · region SEA
**Gold reference:** `bahrain-motc` (PR #141). Same pattern, Singapore geography.
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-singapore-mpa.json`.
**Economics convention:** `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`.

Page rewritten (content + economics presentation); Grab/Bali/Indonesia contamination removed. Every
`route_id`/`route_ids` is `null` + `_link_status: "pending-seal"`. Your job: mint/bind boarding points,
route every leg through navigable water with **zero land crossings** (in the world's busiest port), rebind
route_ids, regenerate economics from the clean Singapore network.

## 1. Boarding points to mint/bind (anchors — snap to real berths)
From `domestic_network.boarding_points`. **Bold = live ferry stop today; ★ = e-HC charging pilot site.**

| node | name | approx [lng,lat] | note |
|---|---|---|---|
| marina-bay-stops | Marina Bay water-taxi stops (Esplanade/Bayfront/Promontory) | 103.8570, 1.2880 | inner waterfront |
| **marina-south-pier ★** | **Marina South Pier** | 103.8630, 1.2710 | live Southern-Islands ferry + e-HC charging pilot |
| marina-east-bedok | Marina East / Bedok Jetty | 103.9120, 1.3010 | East Coast commuter node |
| sentosa-cove-marina | ONE°15 Marina Sentosa Cove | 103.8390, 1.2440 | harbour node |
| keppel-harbourfront | Keppel Bay / HarbourFront | 103.8200, 1.2650 | harbour node |
| **st-johns-lazarus** | **St John's / Lazarus Island** | 103.8480, 1.2180 | live Southern-Islands ferry |
| **kusu-island** | **Kusu Island** | 103.8600, 1.2250 | live Southern-Islands ferry |
| **changi-point** | **Changi Point Ferry Terminal** | 103.9920, 1.3900 | live Pulau Ubin bumboat |
| **pulau-ubin** | **Pulau Ubin** | 103.9640, 1.4100 | live island link |
| west-coast-pier | West Coast Pier / Pasir Panjang | 103.7700, 1.2900 | working waterfront |
| jurong-island-banyan | Jurong Island (Banyan Basin) | 103.7000, 1.2650 | working waterfront |

## 2. Domestic corridors to seal (the spine — lead the proposal)
From `domestic_network.domestic_pairs`. **The Port of Singapore is one of the world's busiest** — route on
cleared corridors, geofence low-wake/no-foil zones in anchorages and fairways, full pilotage compliance.

| pair | from → to | ~nm | routing note |
|---|---|---|---|
| sg-d01 | marina-east-bedok → marina-bay-stops | 5.6 | along the East Coast then into Marina Bay through the Marina Barrage approach; stay clear of the East Coast reclamation |
| sg-d02 | marina-bay-stops → keppel-harbourfront | 4.2 | inner harbour; round the southern waterfront, no cut across the CBD land |
| sg-d03 | marina-south-pier → st-johns-lazarus | 4.0 | live corridor; cross the anchorage on the charted channel, no-foil over anchored ships |
| sg-d04 | marina-south-pier → kusu-island | 3.6 | live corridor; charted channel through the southern anchorage |
| sg-d05 | sentosa-cove-marina → st-johns-lazarus | 2.2 | short island hop; clear Sentosa breakwaters and reef flats |
| sg-d06 | changi-point → pulau-ubin | 1.5 | live link; route the Serangoon Harbour channel, **avoid Pulau Tekong + live-firing areas entirely** |
| sg-d07 | west-coast-pier → keppel-harbourfront | 5.5 | working waterfront; seaward of Pasir Panjang Terminal, on the fairway edge |
| sg-d08 | jurong-island-banyan → keppel-harbourfront | 7.5 | along the working harbour; stay on cleared corridors past the container terminals |

## 3. Regional / relief links (secondary — do NOT lead)
| link | from → to | ~nm | note |
|---|---|---|---|
| sg-r01 | changi-point (Tanah Merah) → batam-indonesia (Batam Centre) | ~13 | live ferry; cross the Singapore Strait TSS at right angles, marked points only; snap Batam to its real ferry berth. **Mint node + cluster city `batam-indonesia`.** |
| sg-r02 | changi-point (Tanah Merah) → bintan-indonesia (Bandar Bentan Telani) | ~22 | live ferry; Quanta-LR across the Strait. **Mint node + cluster city `bintan-indonesia`.** |
| sg-r03 | marina-east-bedok → desaru-coast-malaysia | ~18 | Causeway-relief candidate; **route AROUND the eastern (Tebrau Strait) or western end of the island — never through/over the Johor–Singapore Causeway.** Bilateral review pending. |

> `batam-indonesia` and `bintan-indonesia` were **removed from page `cities` arrays** (no registry entry).
> `desaru-coast-malaysia` exists and is retained. Mint Batam/Bintan nodes + cluster cities, then they can rejoin.

## 4. Hand-waypoint + no-land-crossing rules (decisive for a maritime authority)
- **Every leg `interior_land_km == 0`.** MPA will scrutinize the map harder than anyone — this is the whole game.
- **Traffic Separation Scheme / anchorages:** cross fairways and the TSS only at marked points; geofence no-foil
  zones over anchorages; full pilotage compliance. The vessel foils only on cleared corridors.
- **Causeway:** physically blocks the middle of the Johor Strait — any Singapore↔Johor/Desaru leg routes around
  the island ends, never over the embankment.
- **Sisters' Islands Marine Park & Southern reefs:** keep clear of reef flats; no-wake on approach; snap to channels.
- **Pulau Tekong + live-firing/danger areas:** avoid entirely; Changi↔Ubin uses the charted Serangoon channel.
- Use `data-clean/uae_hand_waypoints.json` `{from,to,waypoints:[[lng,lat]...]}` format for hand legs.
- QA gate: land-intersection check; any leg with interior_land_km > 0 fails the seal.

## 5. Economics regen (under the PTA convention)
- Rungs already relabelled plain; super-app journey-GMV rung dropped. **Re-derive numbers** from the clean
  Singapore domestic network — prior figures inherited a Grab/Indonesia-contaminated, super-app recal
  (see `growth_case.public_value._grok_regen`).
- Quantify `public_value.levers` (harbour-craft CO₂ cut vs the 2030 mandate & net-zero 2050, seats/capacity added,
  Causeway minutes saved) and add a fares/operating-model table. Fares/cost-recovery = "set with MPA" — never fabricate.

## 6. Done = all green
Schema · fidelity (journey_bp=0) · linkage (sealed) · geometry (interior_land_km==0) · seal-integrity · build.
