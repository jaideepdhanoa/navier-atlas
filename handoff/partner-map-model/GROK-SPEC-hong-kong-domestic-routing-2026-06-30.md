# GROK SPEC — Hong Kong Transport Department domestic routing (hand-waypointed, no land crossings)

**From:** Tasklet · **Date:** 2026-06-30 · **Partner:** `hong-kong`
**Goal:** Seal the Hong Kong Transport Department domestic water-transport network to real `route_id`s with hand-curated waypoints so **every leg stays in navigable water with zero land crossings**. This proposal goes to Transport Department, Government of the Hong Kong SAR — geometry credibility is the whole game. A single route clipped across land, a causeway, a reef, or a shipping lane sinks the pitch.

Source of truth for nodes, pairs, and hazards: **`handoff/partner-map-model/PTA-DOSSIER-hong-kong.json`**.

---

## 1. What Tasklet has done (do not redo)
- Rewrote the partner page (`data-clean/partners/hong-kong.json` + `partner-pitch/` mirror): new authority narrative, domestic-first phases, public-value economics, all internal jargon and prior-partner contamination scrubbed.
- Every journey and featured route is `route_id: null` with `_link_status: "pending-seal"` — **intentional-null, awaiting your seal**. All four strict gates pass in this state.
- Boarding points (16) are **candidate anchors only** (approximate `[lng,lat]`), not sealed geometry.

## 2. What Grok owns (this spec)
1. **Mint / bind boarding points** from the dossier `domestic_network.boarding_points`. Snap each anchor to the real berth / marina / jetty / pier / channel mouth — every node is a real, licensed ferry pier (Central Piers, Star Ferry, the outlying-island piers) — snap to the actual pier.
2. **Route every domestic pair** in `domestic_network.domestic_pairs` (10) and the `regional_links` (1) with **hand-curated waypoints** that keep the line in charted navigable water.
3. **Hand waypoints are mandatory** wherever a straight line would clip land, a reclamation edge, a causeway, a reef, a shallow, or a commercial shipping lane. Use the `uae_hand_waypoints.json` mechanism (`{from, to, waypoints:[[lng,lat],…]}`) — write to **`data-clean/hong_kong_hand_waypoints.json (new; same schema as uae_hand_waypoints.json)`**.
4. **Run land/water QA** (`qa_land_crossing_report.json` lane) on every new leg. **No leg ships with `interior_land_km > 0`.**
5. Return sealed `route_id`s; bind them back into the partner page featured_routes/journeys (replace `route_id: null`, remove `_link_status: "pending-seal"` on bound items), then regenerate the fidelity + linkage audits.

## 3. No-land-crossing rules (Hong Kong Transport Department-specific hazards)
From the dossier `routing_hazards` — these are the traps:

| Hazard | Rule |
|---|---|
| **Victoria Harbour traffic & fairways** | The harbour is extremely busy with cross-harbour ferries, tugs, barges and ocean traffic. Route through marked fairways with strict no-foil/low-speed geofences across the cross-harbour ferry lanes; never cut across the main fairway at foiling speed. |
| **East Lamma Channel & West Lamma Channel TSS** | Major container-ship traffic separation schemes south and west of the islands. Island legs to Lamma, Cheung Chau and Mui Wo must cross these channels at marked crossing points, perpendicular and clear of large-vessel lanes. |
| **Kap Shui Mun / Ma Wan channel & bridges** | Routes toward Ma Wan/north Lantau pass under the Tsing Ma and Kap Shui Mun bridges through a regulated channel; follow the marked channel, displacement/no-foil where required. |
| **Tathong Channel (eastern approach)** | Eastern-harbour and Lei Yue Mun legs must respect the Tathong Channel ocean-traffic lane. |
| **Sha Chau & Lung Kwu Chau Marine Park / dolphins** | Western waters near north Lantau are a Chinese white dolphin marine park with speed/route restrictions; keep clear or transit slowly per marine-park rules. |
| **Typhoon shelters (Causeway Bay, Aberdeen, Yau Ma Tei)** | Typhoon shelters are congested, slow-speed anchorages; any pier inside a shelter requires displacement/no-foil, low-wake approach. |
| **Kwai Tsing container terminals** | Keep all geometry clear of the Kwai Tsing container-terminal approaches and turning basins. |

## 4. Routing acceptance gate (all must hold)
- [ ] Every domestic pair + regional link has a sealed `route_id` with a real LineString.
- [ ] `interior_land_km == 0` for every leg (land/water QA clean).
- [ ] Legs near the hazards above visibly route **around/through** them, not across — spot-check the tightest legs on the map.
- [ ] Partner page featured_routes/journeys rebound from `null` → sealed `route_id`; `_link_status: "pending-seal"` removed on bound items.
- [ ] `audit_proposal_fidelity.py --partner hong-kong` = PASS, `journey_bp=0`.
- [ ] `audit-partner-route-linkage.mjs` = 0 gaps for `hong-kong`.
- [ ] `audit-route-geometry.py --strict-severe` exit 0.

## 5. Economics regeneration (under the new PTA convention)
After routes seal, regenerate Hong Kong Transport Department economics under **`handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`**:
- Keep the plain rung labels Tasklet set (Operating revenue — starter corridors / full network / mature network; Total water-transport market). **No SOM/SAM/TAM/journey-GMV/super-app language.**
- Replace the `growth_case.public_value.levers` placeholders with **quantified** figures: CO₂ avoided t/yr (tie to the Hong Kong Climate Action Plan 2050 (carbon neutrality before 2050) and the government electric-ferry pilot), road / bridge / causeway trips relieved, passenger-minutes saved, access widened. Re-derive operating revenue from the clean Hong Kong Transport Department domestic network (prior numbers inherited a noon/super-app recal — see `public_value._grok_regen`).
- Add a **fares / operating-model** table (illustrative, flagged "set with the authority"): fare integration with the authority's existing media/app, operating cost per service-hour benchmarked to the existing fleet, cost-recovery band. **No fabricated subsidy numbers** — band + "agreed with authority."
- Horizons stay maturity-honest (Starter service / Full network / Mature network) — geography-led phasing lives in the story `phases`; do not duplicate.

## 6. Replication note
This follows the **Bahrain MOTC gold-reference** PTA pattern (`GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`). Hand-waypointing + zero-land-crossing QA is **mandatory for the whole category** — authorities will scrutinize the map.
