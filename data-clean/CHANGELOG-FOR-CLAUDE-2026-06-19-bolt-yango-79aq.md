# CHANGELOG — Gold #79aq — Bolt/Yango BP seal + economics (2026-06-19)

**BP coverage:** 207 city files ingested, 12,241 handoff BPs ledgered with 0 silent drops.
**POIs:** 11,689 → 12,008 sealed (+371 net after reconciliation); exclusion scrub → 12,008.
**Partners:** 18 Bolt + 15 Yango full sub-proposals; all `anchor_cities` resolve post-crosswalk.
**Economics:** `economics_by_route_id.json` refreshed with bolt/yango partners (103 route-pinned records).
**Yango:** `growth_case` bound from `agg-yango.json` rollup + `economics_url`.
**Method:** `scripts/grok-bolt-yango/` apply → scrub → splice → economics → reseal #79aq.