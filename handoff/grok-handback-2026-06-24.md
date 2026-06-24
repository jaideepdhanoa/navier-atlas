# Grok handback — proposal completeness · 2026-06-24

> Canonical record of the Grok → Tasklet handback. Grok mint lane is idle pending Tasklet cascade.
> Production: https://navier-atlas.vercel.app · Latest commit: `6a5e9f67` · Pre-flight: clean · 0 partner linkage gaps · 59/59 story-ready.

## Closed on Grok side (mint → bind → deploy)
| Priority | Item | Status |
|---|---|---|
| P2 | Grab Thailand | Sealed — BKK↔Hua Hin marquee, Thailand mesh, economics cascade |
| P3 | Bolt kept markets (12) | 12/12 legs bound — residual gaps closed (`f109be93`) |
| P4 | Minor Hotels Phase 1+2 | 80/80 journeys bound; Phase-2b economics ($16M SOM) |
| P5.1 | India corporate dedupe | Adani vs Reliance differentiated — no longer byte-identical |
| — | Intra-city mesh | +535 routes (ABC, UAE, Greece, Croatia, Red Sea, Phuket, Goa) |
| — | Partner relink | Full 59-partner pass; list-node_id crash fixed |
| — | Route linkage | 104 blocking gaps cleared via linkage lane (`6a5e9f67`) |

India transparent sheets (published to Drive):
- Adani Ports — https://docs.google.com/spreadsheets/d/1nHiCS0crF7zdFvpZ5GhRjApknsvFDerAjIlRfB4kW5w/edit — $18.2M rev / 103 fleet / $1.60B TAM
- Reliance Industries — https://docs.google.com/spreadsheets/d/12A3sSM5HMOF1qoDm4lq8zOKQ5YU17VzlIQ9favraS8Y/edit — $12.7M rev / 73 fleet / $1.12B TAM

Key scripts added/used:
- `scripts/grok-bolt-yango/mint_bolt_residual_gaps.py`
- `scripts/grok-econ-reseal/dedupe_india_corporate_economics.py`
- `scripts/grok-geometry/mint_intra_city_mesh.py`
- `scripts/relink_partner_journeys.py` (list-node fix)
- `scripts/run-route-linkage-lane.sh` (hospitality/authority gap restore)

## Open on Tasklet side (cascade + narrative)
1. **Growth ladders — 36 no-ladder proposals.** No `growth_case` on: aman, six-senses, four-seasons, soneva, discovery-land, crown-champa, sun-siyam, villa-hotels, indian-ocean-luxury, lyft, didi, gojek, kakao-mobility, line, cabify, indrive, freenow, yango, dubai-rta, d-marin, abu-dhabi-itc, bc-ferries, fullers360, hawaii, hong-kong, maldives-government, maldives, norway-fjords, nyc-ferry, shun-tak, singapore-mpa, thames-clippers, transport-nsw, universal-enterprises, wsf, cote-dazur, french-polynesia, red-sea-global. → Cascade TAM ladder on minted route_ids per partner; hospitality uses $1M/vessel.
2. **Bolt East Africa narrative.** Only market missing UAE-parity narrative (9/12 fields). Geometry sealed (Dar↔Stone Town, Mombasa↔Diani). → Author partner_context, why_navier_now, differentiation, proof_points, objections, the_ask, close, end_state, vessel_sizing.
3. **Bolt data bugs (from audit).** Floor rounding: 1.54M must not display as "2M". Stale `source_rollup`: careem-aggregate.json → Bolt's own rollup. Ladder rungs should rest on minted corridors, not shared 341-route census.
4. **~190 null `journeys_unlocked` (23 partners).** Largest tails: minor-hotels (30 intra-POI labels), six-senses (21), aman (18), uber (13), lyft (14), four-seasons (11). Mostly resort transfers + mobility aspirational legs — mark aspirational or cascade after property BP mint.
5. **SEAL re-seal (advisory).** FEATURES_BY_TYPE.json, ROUTES.json, economics_by_route_id.json differ from SEAL snapshot after mesh + relink. Not blocking dev deploy; re-seal when cutting next gold tag.
6. **Grab deck KPI refresh.** Post-#101 de-jargon; PR #96 backgrounds on live Slides.

## Hard gates (unchanged)
- 0 silent drops · 0 land-crossings · ID-based matching only · null beats confidently-wrong
- Per-partner census — no shared global TAM between partners
- Renderer: Bolt display_order + hidden:true on 6 suppressed markets

## Suggested Tasklet sequence
1. India sheets QA (Adani/Reliance on Drive) → wire `economics_url` if needed
2. Bolt East Africa narrative + ladder regen on minted routes
3. Hospitality ladder cascade (aman → six-senses → four-seasons → soneva tail)
4. Mobility ladder cascade (lyft, didi, gojek, indrive, freenow, yango)
5. SEAL re-seal package after ladder pass
6. Grab deck KPI refresh

---
### Tasklet triage notes (added on receipt)
- **Bangkok marquee divergence to verify:** Atlas now seals Grab Thailand marquee as **BKK↔Hua Hin**, but the live Grab Thailand *deck* econ/map corridor for Bangkok is **ICONSIAM → Wat Arun** (PR #102). These serve different surfaces (network map vs deck econ pick) but should be reconciled intentionally, not by drift.
- Item 6 (Grab deck KPI refresh) lands in the deck lane and overlaps with PR #101 (de-jargon) and PR #102 (corridors) — sequence after those settle.
