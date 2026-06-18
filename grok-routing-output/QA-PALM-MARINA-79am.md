# Palm Jumeirah / Dubai Marina cleanup — Gold #79am

**Date:** 2026-06-19 · **Seal:** #79am · **Bbox:** lon 55.09–55.19, lat 25.04–25.14

## Acceptance (all PASS)

| Gate | Result |
|------|--------|
| Visible DROP BPs in bbox | **0** |
| Orphan routes (bad endpoints) | **0** |
| Land-crossing polylines in bbox | **0** (threshold 0.05 km, v2 overlay) |
| Surviving BPs without gazetteer source | **0** |
| High-confidence gazetteer entries missing | **0** |

## Gazetteer gate #4b (Tasklet research)

Source: `grok-routing-output/palm-marina-boarding-point-gazetteer.json` (12 RTA/harbour entries, 6 exclusions, null-coords policy).

- Promotes RTA Dubai Marina marine-transport stations via name/alias match + water-adjacency override
- Collapses duplicate aliases to one visible BP per canonical `source_id`
- Applies exclusions (retail POIs, yacht clubs without water-bus service, etc.)
- **Keeps hotel jetty pins** alongside RTA stations (Phase-3 synth routes snap to jetty coords)

## Counts

| Metric | Before (approx) | After |
|--------|-----------------|-------|
| Visible BPs in bbox | ~75 | **23** |
| BPs dropped (junk/gate/exclusion) | — | **88** |
| BPs promoted (terminals) | — | **46** (→ **23** after alias collapse) |
| Gazetteer-sourced promotions | — | **33** |
| RTA high-confidence promoted | — | **5** |
| Routes cascade-quarantined (Palm bbox) | — | **107** |
| Palm bbox routes culled (spaghetti+geom) | — | **6** |
| Phase-3 patches applied | — | **14** |
| Phase-3 synth applied | — | **13** |
| Active routes (total gold) | ~5,864 | **5,351** |

## Surviving terminals (23)

**RTA / water-bus:** Marina Terrace, Marina Walk, Marina Promenade, Dubai Marina Mall, JBR The Walk water taxi, Bluewaters ferry.

**Dubai Harbour:** Cruise Terminal, Bay Marina, DMYC.

**Palm hotel jetties:** Anantara, Atlantis, Atlantis Royal, FIVE, Fairmont, One&Only, Rixos, Waldorf, Zabeel Saray, W Dubai.

**Other:** Bluewaters Marina, Ain Dubai pontoon, Dubai Marina Yacht Club (DMYC-adjacent), Skydive Dubai Marina jetty.

## Artifacts

- `grok-routing-output/palm-marina-boarding-point-gazetteer.json`
- `grok-routing-output/qa-palm-marina-acceptance.json` (work tree after reconcile)
- `grok-routing-output/palm-marina-cleanup-report.json` (work tree after reconcile)

## Prod

- https://navier-atlas.vercel.app