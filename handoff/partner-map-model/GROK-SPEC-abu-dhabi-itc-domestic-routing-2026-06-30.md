# GROK SPEC — Abu Dhabi ITC domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `abu-dhabi-itc`
**Goal:** Seal the Abu Dhabi ITC domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to Integrated Transport Centre / Abu Dhabi Mobility (Abu Dhabi Maritime) — geometry credibility is the whole game. A single route clipped across land, a causeway, a reef, or a shipping lane sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-abu-dhabi-itc.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/abu-dhabi-itc.json` + `partner-pitch/` mirror): new authority narrative, domestic-first phases, public-value economics, all internal jargon and prior-partner contamination scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points (15) are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real berth / marina / jetty / pier / channel mouth — the core nodes are the live Abu Dhabi Maritime water-taxi/ferry terminals (Yas Bay, Al Bandar, Saadiyat, Rabdan, Corniche) — snap to their actual pontoons.
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (8) and the `regional_links` (2) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a reclamation edge, a causeway, a reef, a shallow, or a commercial shipping lane. Use the `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — write to **`data-clean/uae_hand_waypoints.json (extend)`**.
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`, remove `_link_status: "pending-seal"` on bound items), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (Abu Dhabi ITC-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **Maqta & Mussafah channels and low bridges** | Khor Al Maqta and the Mussafah channel carry low road bridges (Maqta, Sheikh Zayed, Mussafah). Legs through them must be displacement / no-foil, following the dredged centreline through the bridge spans. |
| **Mangrove flats and dredged lagoons** | Eastern Mangroves, Reem and Al Raha are threaded by shallow mangrove channels; keep all geometry in charted dredged channels, never across the mangrove or sabkha flats. |
| **Khalifa Port TSS (north-east)** | Any leg toward Yas/north-east must stay well clear of the Khalifa Port traffic separation scheme and approaches. |
| **Mina Zayed commercial & cruise port** | Marsa Mina sits beside the working Mina Zayed port; route through the marked passenger channel and respect commercial traffic separation. |
| **Yas Channel & Al Raha shallows** | The Yas <-> Al Raha water is shallow and dredged; snap entries to the channel and avoid the inter-island flats. |
| **Hudayriat / Lulu breakwaters** | Reclaimed leisure islands enclosed by breakwaters; snap to marked openings, not the rock. |
| **Abu Dhabi <-> Dubai / Al Dhafra offshore (optional links only)** | Long links must stay in open Gulf water clear of Khalifa Port, Jebel Ali approaches, and the western offshore oilfield exclusion zones; hand-waypoint around Saadiyat, Lulu and any reclamation. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair + regional link has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Legs near the hazards above visibly route **around/through** them, not across — spot-check the tightest legs on the map.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner abu-dhabi-itc` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs` = 0 gaps for `abu-dhabi-itc`.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate Abu Dhabi ITC economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter corridors / full network / mature network; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to UAE Net Zero 2050 and the Abu Dhabi Environment Vision), road / bridge / causeway trips relieved, passenger-minutes saved, access widened. Re-derive operating revenue from the clean Abu Dhabi ITC domestic network (prior numbers inherited a noon/super-app recal — see `public_value._grok_regen`).
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration with the authority's existing media/app, operating cost per service-hour benchmarked to the existing fleet, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`; do not duplicate.

## 6. Replication note
This follows the **Bahrain MOTC gold-reference** PTA pattern (`GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`). Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
