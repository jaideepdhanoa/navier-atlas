# GROK SPEC — Uber Boat by Thames Clippers domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `thames-clippers`
**Goal:** Seal the Uber Boat by Thames Clippers domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to Thames Clippers (London river bus; TfL-coordinated River Bus network) — geometry credibility is the whole game. A single route clipped across land, a breakwater, a reef, a bridge pier, or a shipping lane sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-thames-clippers.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/thames-clippers.json`): authority narrative, domestic-first phases, public-value economics, all internal jargon (SOM/SAM/TAM, Journey GMV, Prove/Scale/Mature labels) and prior-binding noise scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points (24) are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry. They map to the authority's real live piers / wharves / terminals.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real pier / wharf / terminal / berth — the core nodes are the authority's live ferry stops on the tidal Thames through London — snap to their actual pontoons.
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (8) (the network is domestic-only; no regional links in scope) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a breakwater, a reclamation edge, a barrier, a bridge pier, a reef, a shallow, or a commercial shipping lane. Use the `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — extend **`data-clean/thames_clippers_hand_waypoints.json`** (same schema as `data-clean/uae_hand_waypoints.json`).
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`, remove `_link_status: "pending-seal"` on bound items), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (Uber Boat by Thames Clippers-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **Thames Barrier** | The Thames Barrier at Woolwich Reach is a moveable flood barrier; eastbound legs to Royal Wharf/Woolwich/Barking Riverside must pass through the marked open navigation spans and obey PLA barrier-closure signals - never route across a closed span. |
| **Strong tidal flow & restricted wash** | The Thames is fast-flowing and tidal with PLA wash and speed restrictions through central London; central reaches must be displacement / no-foil and low-wash, with foiling reserved for the wider, clearer east-London reaches where permitted. |
| **Bridges** | Central London has many bridges (Putney, Wandsworth, Battersea, Chelsea, Vauxhall, Lambeth, Westminster, Blackfriars, Southwark, London, Tower); keep geometry in the marked navigation arch of each bridge. |
| **Dense river traffic** | The Thames carries heavy tripboat, freight (tug-and-barge aggregate), and Woolwich Ferry traffic under PLA control; respect navigation rules and cross the Woolwich free-ferry crossing cleanly. |
| **Tidal limit / shallows at Putney** | Putney is near the tidal navigation limit; the upper-western reach dries and shoals at low water - route the dredged channel and respect tide windows. |
| **Moorings & no-wash zones** | Houseboats and moorings line the central and western reaches with strict no-wash rules; geofence low-wake zones along all moored frontages and pier approaches. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Legs near the hazards above visibly route **around/through** them, not across — spot-check the tightest legs on the map.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner thames-clippers` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs` = 0 gaps for `thames-clippers`.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate Uber Boat by Thames Clippers economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter corridors / full network / mature network; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to London net-zero by 2030 and the Mayor's Transport Strategy river-growth target), central- and east-London road trips relieved, passenger-minutes saved, access widened. Re-derive operating revenue from the clean Uber Boat by Thames Clippers domestic network (prior numbers inherited a super-app/ride-hail recal — see `public_value._grok_regen`).
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration with the authority's existing ticketing, operating cost per service-hour benchmarked to the existing fleet, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`; do not duplicate.

## 6. Replication note
This follows the **Bahrain MOTC gold-reference** PTA pattern (`GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`). Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
