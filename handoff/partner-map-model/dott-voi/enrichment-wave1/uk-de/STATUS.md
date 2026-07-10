# UK + Germany Dott/Voi exact-depth audit — status

**Status:** research handoff only / **not seal-complete**. No repository source was edited.

## Programmatic counts

- Source rows reviewed: **178**
- Current rows: **176**
- Marine-relevant rows: **50**
- Exact-bound source rows: **5** (**3 unique partner-city binds**)
- Documented-alias-needed rows: **2**
- Unresolved marine rows: **45**
- Inland/non-marine exclusions: **126**
- Proposed global clusters: **9** (all `not_banked`)
- Proposed global cities: **17** (all `not_banked`)
- Candidate BPs: **23** (no IDs minted; two Clyde BPs held closed)
- Candidate routes: **11** (every `route_id` is null)

## P0 recommendations

1. **Stop Dott's London leak.** Current `data-clean/partners/dott.json::_map_scope.registry_keys` contains `uk`; `uk` contains `london-thames-uk`. Current `ROUTES.json` has 64 `uk`-cluster routes, including 33 associated with `london-thames-uk`; canonical inheritance therefore surfaces London even though Dott evidence includes an explicit current London exclusion. Do not solve this with partner-specific route filtering. Split the global country cluster into water-system clusters, then re-derive partner membership.
2. **Solent / Isle of Wight.** Voi explicitly supports Portsmouth, Southampton and Isle of Wight. Wightlink and Red Funnel provide exact terminal pairs. Bank only after canonical cluster/city/BP validation and water-only route seal.
3. **Clyde / Glasgow.** Both partners name Glasgow and Atlas has `firth-of-clyde-scotland`, but the alias is not documented. Add the alias only through review and split the Clyde system from broad `uk`. Hold route promotion because Glasgow City Council reports Broomielaw and Govan pontoons closed until further notice.
4. **Hamburg reuse.** Both partners exact-bind to existing `hamburg-germany`; reuse existing global HADAG BPs/routes. No duplicate route research is needed.

## P1 queue

Bristol Harbour; Kiel Fjord; Lübeck/Travemünde–Priwall; Flensburg Fjord; Rostock/Warnow; Berlin F10; and a conservative Rhine BP/route validation pass for Bonn–Cologne–Düsseldorf. Bath and Duisburg remain city/system gaps without promotion-ready BP meshes.

## Holds

- No Dott London current-operation claim.
- No country-wide UK exact-city inference.
- No Clyde route while cited pontoons are closed.
- No proposed ID, BP, route ID, geometry, demand, fare or economics is banked here.
- Secondary plausible waterfront rows remain unresolved rather than falsely excluded.

See `EXACT-BIND-LEDGER.json` for row-level evidence and `CANONICAL-GEOGRAPHY-HANDOFF.json` for citations and deterministic Grok actions.
