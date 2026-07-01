# GROK SPEC — RAK RAKTA domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `rakta`
**Goal:** Seal the RAK RAKTA domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to Ras Al Khaimah Transport Authority — geometry credibility is the whole game. A single route clipped across land, a causeway, a reef, or a shipping lane sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-rakta.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/rakta.json` + `partner-pitch/` mirror): new authority narrative, domestic-first phases, public-value economics, all internal jargon and prior-partner contamination scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points (7) are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real berth / marina / jetty / pier / channel mouth — the live nodes are the RAKTA Marine Transport Project berths (Al Marjan, Al Qawasim Corniche) — snap to their actual jetties; the resort-island berths are mint-new.
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (6) and the `regional_links` (1) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a reclamation edge, a causeway, a reef, a shallow, or a commercial shipping lane. Use the `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — write to **`data-clean/uae_hand_waypoints.json (extend)`**.
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`, remove `_link_status: "pending-seal"` on bound items), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (RAK RAKTA-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **Al Marjan Island breakwaters** | Al Marjan is reclaimed (coral-shaped fronds) enclosed by breakwaters; route around the outer breakwater through the marked openings, never across the fronds or land. |
| **Mina Al Arab & Al Hamra lagoons** | These are dredged lagoon communities; snap entries to the channel mouths and keep geometry in charted channels, not across the shallow lagoon flats. |
| **Saqr Port & RAK commercial port (north)** | Saqr Port is a major bulk-cargo port north of the city; keep all geometry clear of its traffic separation scheme and approaches. |
| **RAK Creek mouth & northern shallows** | The creek mouth and the northern coast carry shallow reef/sand flats; follow charted channels and hand-waypoint around the flats. |
| **Al Marjan <-> Dubai offshore (optional link only)** | If routed, keep the line in open Gulf water clear of the Saqr Port and Dubai (Hamriyah/Dubai Islands) approaches and any reclamation; hand-waypoint the full leg. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair + regional link has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Legs near the hazards above visibly route **around/through** them, not across — spot-check the tightest legs on the map.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner rakta` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs` = 0 gaps for `rakta`.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate RAK RAKTA economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter corridors / full network / mature network; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to UAE Net Zero 2050 and the RAKTA Transport Master Plan 2030), road / bridge / causeway trips relieved, passenger-minutes saved, access widened. Re-derive operating revenue from the clean RAK RAKTA domestic network (prior numbers inherited a noon/super-app recal — see `public_value._grok_regen`).
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration with the authority's existing media/app, operating cost per service-hour benchmarked to the existing fleet, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`; do not duplicate.

## 6. Replication note
This follows the **Bahrain MOTC gold-reference** PTA pattern (`GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`). Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
