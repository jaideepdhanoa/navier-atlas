# GROK SPEC — Dubai RTA domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `dubai-rta`
**Goal:** Seal the Dubai RTA domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to Roads and Transport Authority (Dubai) — geometry credibility is the whole game. A single route clipped across land, a causeway, a reef, or a shipping lane sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-dubai-rta.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/dubai-rta.json` + `partner-pitch/` mirror): new authority narrative, domestic-first phases, public-value economics, all internal jargon and prior-partner contamination scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points (15) are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real berth / marina / jetty / pier / channel mouth — the core nodes are RTA's live marine-transport stations (Marine, Water Canal, Creek, Marina) — snap to their actual pontoons.
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (8) and the `regional_links` (1) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a reclamation edge, a causeway, a reef, a shallow, or a commercial shipping lane. Use the `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — write to **`data-clean/uae_hand_waypoints.json (extend; Dubai already has UAE precedent entries)`**.
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`, remove `_link_status: "pending-seal"` on bound items), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (Dubai RTA-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **Palm Jumeirah breakwater & fronds** | Palm Jumeirah is land/reclamation; routes to/from the Palm must round the outer crescent breakwater through the marked openings — NEVER straight across the fronds or trunk. |
| **Dubai Marina / Harbour / Bluewaters breakwaters** | Marina and Dubai Harbour are enclosed by breakwaters; snap entries to the marked harbour mouths, not the breakwater rock. |
| **Dubai Creek mouth & Port Rashid (Mina Rashid)** | The creek mouth is shared with commercial and abra traffic; Mina Rashid is an active cruise/commercial port. Route through the marked channel and respect port traffic separation. |
| **Dubai Water Canal** | The Water Canal is narrow with multiple low road/foot bridges; canal legs must be displacement / no-foil with strict wake and speed limits, following the dredged centreline through the bridge spans. |
| **Heritage abra lanes (Creek)** | The Deira <-> Bur Dubai abra crossings are dense and protected; geofence no-foil, low-wake zones across all abra lanes. |
| **The World Islands lagoons** | The World is a reclaimed archipelago served by dredged channels; snap to channel entries and keep geometry clear of the shallow inter-island flats. |
| **Jebel Ali Port TSS (south)** | Any coastal run extending south must stay clear of the Jebel Ali Port traffic separation scheme and approaches. |
| **Dubai <-> Abu Dhabi offshore (optional link only)** | If the domestic UAE link is routed, keep the line in open Gulf water clear of the Jebel Ali and Khalifa Port approaches and offshore oilfield exclusion zones; hand-waypoint around all reclamation. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair + regional link has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Legs near the hazards above visibly route **around/through** them, not across — spot-check the tightest legs on the map.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner dubai-rta` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs` = 0 gaps for `dubai-rta`.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate Dubai RTA economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter corridors / full network / mature network; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to UAE Net Zero 2050 and the Marine Transport Master Plan 2030 (22.2M trips/yr target)), road / bridge / causeway trips relieved, passenger-minutes saved, access widened. Re-derive operating revenue from the clean Dubai RTA domestic network (prior numbers inherited a noon/super-app recal — see `public_value._grok_regen`).
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration with the authority's existing media/app, operating cost per service-hour benchmarked to the existing fleet, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`; do not duplicate.

## 6. Replication note
This follows the **Bahrain MOTC gold-reference** PTA pattern (`GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`). Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
