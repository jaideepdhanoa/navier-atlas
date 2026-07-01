# GROK SPEC — Bahrain MOTC domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `bahrain-motc`
**Goal:** Seal the Bahrain domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to a national transport ministry — geometry credibility is the whole game. A single route clipped across a causeway or reef sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-bahrain-motc.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/bahrain-motc.json` + `partner-pitch/` mirror): new authority narrative, domestic-first phases, public-value economics, all internal jargon scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real berth / marina / jetty / channel mouth (the six core nodes are the **live Masar water-taxi stations** — snap to their actual pontoons).
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (8) and the two `regional_links` (2) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a causeway, a reef, or a shallow. Use the same `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — add a `bahrain_hand_waypoints.json` or extend the existing file.
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (Bahrain-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **Manama–Muharraq causeway complex** (Shaikh Hamad, Shaikh Isa bin Salman, Shaikh Khalifa bridges/causeways) | Inner Manama↔Muharraq/Amwaj/Diyar legs must route through the **open water north/east of the causeways** or through a **marked bridge navigation span** — never straight across a causeway embankment. |
| **King Fahd Causeway** (any Bahrain↔KSA leg) | Pass through the **marked navigation channel near Passport Island** — not over the embankment. |
| **Sitra causeway & bridges** | Follow the **dredged channels** to/from Sitra; do not cross the Sitra causeway. |
| **Western & southern shallows / sabkha** | Keep geometry in **charted deeper channels east of the main islands**; avoid the west-coast and far-south flats. |
| **Amwaj / Diyar / Dilmunia dredged developments** | Snap entries to the **dredged approach-channel mouths**, not the reclaimed edge. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair + regional link has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Inner-harbour legs visibly route **around/through** the causeway complex, not across it (spot-check Manama↔Muharraq and Manama↔Amwaj geometry on the map).
- [ ] King Fahd Causeway leg passes the navigation channel, not the embankment.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner bahrain-motc` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs --partner bahrain-motc` = 0 gaps.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate Bahrain economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter / full archipelago / mature; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to −30% by 2035 / net-zero 2060), road & causeway trips relieved, passenger-minutes saved, access widened.
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration via Masar app, operating cost per service-hour benchmarked to bus/ferry, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`, do not duplicate.

## 6. Replication note
This is the **gold-reference PTA**. The dossier schema, hazard table, and routing gate are the template for Qatar MOTC, Singapore MPA, and every future transit authority. Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
