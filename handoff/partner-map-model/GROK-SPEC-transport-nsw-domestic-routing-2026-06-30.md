# GROK SPEC — Transport for NSW domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `transport-nsw`
**Goal:** Seal the Transport for NSW domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to Transport for NSW (Sydney Ferries network) — geometry credibility is the whole game. A single route clipped across land, a breakwater, a reef, a bridge pier, or a shipping lane sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-transport-nsw.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/transport-nsw.json`): authority narrative, domestic-first phases, public-value economics, all internal jargon (SOM/SAM/TAM, Journey GMV, Prove/Scale/Mature labels) and prior-binding noise scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points (31) are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry. They map to the authority's real live piers / wharves / terminals.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real pier / wharf / terminal / berth — the core nodes are the authority's live ferry stops on Sydney Harbour and the Parramatta River — snap to their actual pontoons.
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (8) (the network is domestic-only; no regional links in scope) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a breakwater, a reclamation edge, a barrier, a bridge pier, a reef, a shallow, or a commercial shipping lane. Use the `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — extend **`data-clean/transport_nsw_hand_waypoints.json`** (same schema as `data-clean/uae_hand_waypoints.json`).
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`, remove `_link_status: "pending-seal"` on bound items), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (Transport for NSW-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **Sydney Heads ocean exposure** | The F1 Manly run crosses the open Heads where harbour meets the Pacific - exposed to ocean swell. Route through the marked harbour channel; the foiling control system must manage swell and the Sow and Pigs reef off Watsons Bay. |
| **Sow and Pigs Reef** | Shallow reef in the middle of the harbour off Watsons Bay/Vaucluse - marked by beacons; hand-waypoint clear of it. |
| **Parramatta River shallows & low bridges** | Above Gladesville the river is shallow, tidal and crossed by the Gladesville, Silverwater and other low bridges; upper-river legs must be displacement / no-foil on the dredged channel with strict wake limits past moorings and mangroves. |
| **Garden Island naval base** | Garden Island (Fleet Base East) is an active RAN naval base with an exclusion zone; route clear of the restricted waters off Potts Point. |
| **Dense harbour traffic & wake zones** | Sydney Harbour carries heavy ferry, tripboat and recreational traffic; geofence no-foil, low-wake zones at all wharf approaches and in the heritage coves. |
| **Spit / Middle Harbour (if extended)** | Any Middle Harbour extension passes the Spit Bridge (a lifting bridge) - must follow the opening schedule and marked channel. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Legs near the hazards above visibly route **around/through** them, not across — spot-check the tightest legs on the map.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner transport-nsw` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs` = 0 gaps for `transport-nsw`.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate Transport for NSW economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter corridors / full network / mature network; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to NSW net-zero by 2050 and the first NSW electric ferry (Sydney Fish Market, 2029)), road / Spit / Parramatta Road / harbour-bridge trips relieved, passenger-minutes saved, access widened. Re-derive operating revenue from the clean Transport for NSW domestic network (prior numbers inherited a super-app/ride-hail recal — see `public_value._grok_regen`).
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration with the authority's existing ticketing, operating cost per service-hour benchmarked to the existing fleet, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`; do not duplicate.

## 6. Replication note
This follows the **Bahrain MOTC gold-reference** PTA pattern (`GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`). Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
