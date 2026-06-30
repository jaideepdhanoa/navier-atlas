# GROK SPEC — NYC Ferry domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `nyc-ferry`
**Goal:** Seal the NYC Ferry domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to NYC Ferry (New York City Economic Development Corporation) — geometry credibility is the whole game. A single route clipped across land, a breakwater, a reef, a bridge pier, or a shipping lane sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-nyc-ferry.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/nyc-ferry.json`): authority narrative, domestic-first phases, public-value economics, all internal jargon (SOM/SAM/TAM, Journey GMV, Prove/Scale/Mature labels) and prior-binding noise scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points (25) are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry. They map to the authority's real live piers / wharves / terminals.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real pier / wharf / terminal / berth — the core nodes are the authority's live ferry stops on New York Harbor and the East River — snap to their actual pontoons.
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (8) (the network is domestic-only; no regional links in scope) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a breakwater, a reclamation edge, a barrier, a bridge pier, a reef, a shallow, or a commercial shipping lane. Use the `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — extend **`data-clean/nyc_ferry_hand_waypoints.json`** (same schema as `data-clean/uae_hand_waypoints.json`).
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`, remove `_link_status: "pending-seal"` on bound items), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (NYC Ferry-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **East River currents & Hell Gate** | The East River is a tidal strait with very strong reversing currents, peaking at Hell Gate; routing and speed must account for current set, and foiling control must manage the standing chop. |
| **Harbor commercial & ferry traffic** | New York Harbor carries dense commercial, tug-and-barge and Staten Island Ferry traffic under Coast Guard VTS; respect the traffic-separation scheme and cross lanes cleanly. |
| **Buttermilk Channel & the Narrows** | Governors Island / Red Hook legs cross Buttermilk Channel; St. George legs cross the Upper Bay toward the Narrows - both busy, current-swept and wake-sensitive. |
| **Rockaway open-water exposure** | The Rockaway run crosses open Lower Bay / ocean-influenced water past Coney Island; route the marked channel and manage swell. |
| **Wake-sensitive landings** | Many landings sit on narrow piers with kayak and recreational traffic; geofence no-foil, low-wake zones at every landing approach. |
| **Bridge & pier clearances** | All harbour bridges have ample navigable clearance for ferries; keep geometry in the marked channels under the East River bridges. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Legs near the hazards above visibly route **around/through** them, not across — spot-check the tightest legs on the map.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner nyc-ferry` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs` = 0 gaps for `nyc-ferry`.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate NYC Ferry economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter corridors / full network / mature network; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to NYC carbon-neutral 2050 and the citywide subway-fare ferry mandate), FDR / BQE / East River bridge trips relieved, passenger-minutes saved, access widened. Re-derive operating revenue from the clean NYC Ferry domestic network (prior numbers inherited a super-app/ride-hail recal — see `public_value._grok_regen`).
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration with the authority's existing ticketing, operating cost per service-hour benchmarked to the existing fleet, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`; do not duplicate.

## 6. Replication note
This follows the **Bahrain MOTC gold-reference** PTA pattern (`GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`). Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
