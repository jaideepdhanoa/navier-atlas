# GROK SPEC — R2 Seed-and-Seal · kolkata-wbtc

**Lane:** Grok geometry (mint new BPs + route + seal at 0 km land, hand-waypoints).
**Source:** WB Transport Dept ferry-routes + travelingcreature Hooghly ghat guide
**Discipline:** ID-based match only; null-beats-wrong; inherit real network 1:1; never invent corridors. Approx seed coords below — geocode precisely, keep names authoritative.

## Existing BPs (reuse — do NOT re-mint)
- `bp-d5ddcaa659` — Howrah Ferry Ghat
- `bp-4767db5fe8` — Millennium Park Jetty
- `bp-c3d1996f22` — Fairlie Place Ferry
- `bp-3121aedcd3` — Dakshineswar Ferry Ghat
- `bp-063ee377c3` — Belur Math Ferry Ghat
- `bp-0ffc8ae32c` — Chandannagar Riverfront

## New BPs to mint (10)
- **Babughat (Chandpal Ghat)** — seed `kol-babughat` — ~(22.568, 88.341)
- **Armenian Ghat** — seed `kol-armenian` — ~(22.579, 88.345)
- **Baghbazar Ghat** — seed `kol-baghbazar` — ~(22.601, 88.36)
- **Golabari Ghat (Howrah)** — seed `kol-golabari` — ~(22.592, 88.343)
- **Ahiritola Ghat** — seed `kol-ahiritola` — ~(22.592, 88.356)
- **Sovabazar Ghat** — seed `kol-sovabazar` — ~(22.597, 88.358)
- **Bandhaghat (Howrah)** — seed `kol-bandhaghat` — ~(22.598, 88.348)
- **Ramkrishnapur Ghat (Howrah)** — seed `kol-ramkrishnapur` — ~(22.564, 88.334)
- **Ariadaha Ghat** — seed `kol-ariadaha` — ~(22.656, 88.362)
- **Kuthighat (Baranagar)** — seed `kol-kuthighat` — ~(22.642, 88.362)

## Corridors to seal (9)
- ▸ **Howrah Ferry Ghat ↔ Babughat (Chandpal Ghat)**
- ▸ **Howrah Ferry Ghat ↔ Armenian Ghat**
- ▸ **Howrah Ferry Ghat ↔ Baghbazar Ghat**
- ▸ **Golabari Ghat (Howrah) ↔ Ahiritola Ghat**
- ▸ **Ahiritola Ghat ↔ Bandhaghat (Howrah)**
- ▸ **Babughat (Chandpal Ghat) ↔ Ramkrishnapur Ghat (Howrah)**
- ▸ **Sovabazar Ghat ↔ Baghbazar Ghat**
- ▸ **Fairlie Place Ferry ↔ Ariadaha Ghat**
- ▸ **Baghbazar Ghat ↔ Kuthighat (Baranagar)**

## Hand-waypoint guidance
All corridors run along or across the Hooghly (Ganga) river channel through central Kolkata/Howrah. Cross-river hops (Howrah↔Babughat/Armenian, Ahiritola↔Bandhaghat, Babughat↔Ramkrishnapur) are short and clear. Along-river hops (Howrah↔Baghbazar, Fairlie↔Ariadaha, Baghbazar↔Kuthighat) follow the channel N under Howrah Bridge (Rabindra Setu) and Vivekananda Setu — keep mid-channel, no bank clipping.

## Write-back
- Bind `route_id`/`route_ids` per corridor into `data-clean/partners/kolkata-wbtc.json` + partner-pitch tree; `_link_status: sealed`.
- Serialization: data-clean ascii/indent2/newline; partner-pitch non-ascii/indent2/newline.
- Re-run land QA; confirm 0 crossings; append receipts to gap table.