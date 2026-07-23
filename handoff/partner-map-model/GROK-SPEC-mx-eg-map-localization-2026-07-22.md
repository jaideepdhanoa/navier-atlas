# GROK-SPEC — DiDi Mexico + inDrive Egypt map localization

**Date:** 2026-07-22
**Author:** Tasklet
**Context:** Both decks were duplicated off the DiDi Brazil chassis. Text was localized; imagery was not. Covers, partner-proposal backgrounds, Three-C's (S3), and four Mexico city route maps have now been re-localized on the live decks (see PR #329 for the two new Three-C's composites). The remaining gap is **geographic maps**, which must be produced by the geojson renderer — not image generation. Fail closed on any corridor lacking sourced geometry.

**Live deck IDs:** DiDi Mexico `1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c` · inDrive Egypt `1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk`.

## Map assets still showing Brazil (must be replaced)

### DiDi Mexico
1. **Market-overview map (S4)** — currently the Brazil coastline (Rio/Paraty). Needs a Mexico national/coastal plate covering all in-scope cities.
2. **Holbox route map** — confirmed T1 city (Chiquilá↔Holbox, $12/leg OW MID, unit econ $141,082 / 40% / 10.64yr, route `rn-8e76868a5b01`). No route map exists; slide still shows Brazil (Ilha do Mel).
3. **Huatulco route map** — confirmed T1 city ($20/leg OW MID, unit econ $235,136 / 66% / 3.88yr, route `rn-66e2241ca732`). No route map exists; slide still shows Brazil.

Route maps that DO exist and are placed (reference for renderer style): `deck-studio/assets/didi/city-maps/didi-{cancun-isla-mujeres,playa-cozumel,los-cabos,puerto-vallarta}-exact-route-map.png`.

### inDrive Egypt
4. **Market-overview map** — currently Brazil coastline. Needs Egypt Red Sea + Nile plate.
5. **All city route maps** — none exist. Deck currently shows Hurghada + Sharm cities on Brazil maps. Model was built around Cairo/Nile commute + El Gouna + Sharm (deck/model diverge — reconcile as part of this work).
   - **Renderable now (four-input likely satisfied):** Hurghada (Giftun Island reefs), Sharm El Sheikh (Ras Mohammed). Confirm endpoints/nm from source before rendering.
   - **Blocked (fail closed) pending sourcing:** Cairo/Nile Zamalek–Maadi, El Gouna, Marsa Alam — demand + fare pairs not yet sourced.

## Four-input rule reminder
A city earns a full slide (map + unit-econ P&L) only with all four sourced for ≥1 corridor: (1) named pier-to-pier route, (2) distance (nm), (3) benchmarked premium fare ($/seat OW), (4) anchored demand (annual pax or riders/day). Otherwise fail closed.

## Discipline
- Text-free plates. Routes validated water-clean against coastline polygon.
- Endpoints sealed at official terminals; aspirational routes flagged.
- Style parity with existing Mexico route maps (dark left clear-space for title, turquoise/blue route lines).
- Render via renderer; do not image-generate maps.

## Sourcing unblocker
Amber cells in `/tasklet/agent/uploads/Navier_Atlas_Corridor_Data_Request.xlsx` (nm, fare, demand, demand-basis per corridor) — pending Jaideep go + recipient before external send.
