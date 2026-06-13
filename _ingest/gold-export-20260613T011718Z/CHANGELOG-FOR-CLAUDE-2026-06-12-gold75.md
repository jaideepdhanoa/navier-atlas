# Gold #75 — 2026-06-12

Safe-reseal building on Gold #74. Driver: schema-fix on 4 water-solver corridors that aborted the prior #75 attempt, plus a partner sweep.

## ROUTES.json (5,283 rows; unchanged count)
The 4 prior None-id water-routed corridors now carry full gold schema (fresh `rn-` ids, `from`/`to` boarding-point ids, `from_city_id`/`to_city_id`, `platform`, label, `verify: CLEAR`, water-routed `geometry.coordinates` arc preserved verbatim):

| id | label | platform | availability | nm |
| --- | --- | --- | --- | --- |
| `rn-df27ac2fd4a6` | Singapore: Marina South Pier → Resorts World Sentosa Waterfront | Pioneer II | (commercial) | 5.4 |
| `rn-a91713014506` | Singapore: Marina South Pier → Changi Point Ferry Terminal | Pioneer II | (commercial) | 18.4 |
| `rn-6327a9cbdd37` | Singapore: Marina South Pier → Pulau Ubin Jetty | Pioneer II | (commercial) | 19.8 |
| `rn-68b2f3d3df86` | Sabah: Jesselton Point → Labuan | quanta_lr | H2_2026_plus (amber_dashed) | 66.9 |

No new market deltas, no new edge-mints, no B3/B4 label fixes in this gold.

## Partners (46 files re-emitted from partner-pitch sources)
- **bolt.json** — 2 fresh Venice ↔ Dalmatian FR bindings.
- **kakao-mobility.json** — Hangang copy refresh.
- 41 partners — `use_cases` shape normalization + `coverage_note` hub additions.
- Bangkok corridors_note rewritten to be partner-safe.
- 2 multi-leg partner entries gained populated `route_ids[]`.
- LB-139 leak gate hardened (pattern set covers `aspirational-null`, `FLAG_MISSING`, bare `gate`).

## Economics sidecar
Rebuilt via `build_economics_sidecar.py` against the live gold + the `{partner}-aggregate.json` family (shimmed via `/tmp/agg_shim`). 98 route-pinned records / 37 unresolved (`_pending_route_pin`). Per-partner: careem 14, grab 37, jih-global 42, red-sea-global 2, saudi-redsea-pif 3. Grounded 71 / estimated 22.

## Gates (all PASS)
- **LB-62 endpoint label↔geometry** — 0 hard FLAGs against the 4 new routes; 15 carry-over `FLAG_MISSING_IN_GOLD` (Philippines / Taiwan / Langkawi / Saudi-redsea corridors inherited from #74).
- **LB-67 city_id resolution** — 0 ROUTES unresolved. 7 known-bad cluster `member_city_ids` carry over from #74 (oman bp-095a41dfcb; philippines bp-23245c74f6, bp-6af248fd3b, bp-7a5f687851, bp-893a394e6a, bp-d4738f6ad2; uae bp-4e324134ef). Gate exits 0; tracked here for a future #76 clean-up.
- **LB-137/139 partner rationale leak** — clean.

## Reminder
This worker did NOT flip `exports/GOLD-COPY.txt`. The parent agent promotes.
