# GROK SPEC — Market coverage gap (empty / sparse markets + missing connective tissue)

**Date:** 2026-07-06
**Author:** Tasklet
**Trigger:** Jaideep — "empty markets where we used to have routes; most others have very
limited routes; missing Q-LR connective tissue (Phuket↔Langkawi, Bangkok↔Hua Hin,
Pattaya↔Hua Hin). Partial audit of a much larger issue. How do we identify / address?"

**Data audited:** `data-clean/ROUTES.json` @ `8ecd1227` (4221 routes) · `data-clean/CLUSTERS.json` (109 clusters).
**Scanner (repeatable, saved):** `scripts/grok-global/market_coverage_audit.py`
(durable copy: `/tasklet/agent/home/yango-program/gulf-and-restamp/market_coverage_audit.py`).
**Register:** `MARKET-COVERAGE-GAP-2026-07-06.json` (same folder).

---

## Architectural ground truth (verified in code, do not re-litigate)

`scripts/build-site.mjs` scopes a market/partner page's routes **purely by endpoint-city
membership**, NOT by the route's own `cluster_id`:

```js
// line ~218 / ~252
if (keep.has(cityIdOf(p.from)) || keep.has(cityIdOf(p.to))) { ... }
applyRouteDisplay(scoped, { keep: [...keep], ... })
```

`CLUSTERS.member_city_ids` is the authoritative, 100%-complete city→cluster map.
**Consequence:** a route renders on a market iff `cityIdOf(endpoint)` ∈ that market's
member cities. The route's `cluster_id` field only feeds region rollups / analytics.

---

## Root-cause taxonomy (5 buckets — keep separate)

### A — cluster_id taxonomy mismatch (HYGIENE, not render-critical) — 355 routes
355 routes carry a non-canonical `cluster_id` — a sub-region key that exists nowhere
(`phuket-andaman` ×41, `koh-samui-gulf` ×34, `bali-nusa-gili` ×14, `eastern-seaboard` ×44…)
or a city_id instead of the canonical COUNTRY cluster. This does **not** darken corridors
(rendering is endpoint-city based) but it breaks region rollups and any cluster_id-keyed
consumer, and it is what made the by-cluster_id census read "Thailand 0 / Indonesia 0".
**Fix (deterministic, no invention):** set `properties.cluster_id` = the canonical cluster
whose `member_city_ids` contains the route's endpoint city. Register: `A_restamp[]` — each
entry `{route_id, old, new, basis}`. Single-cluster routes → that cluster; cross-cluster →
from-side cluster.

### B — truly-empty markets (REAL gap) — 7
Zero routes attach by endpoint-city membership on the NEW build:
`balearic-islands-spain`, `bay-of-naples-amalfi-coast-italy`, `ksa-commercial`,
`leeward-antilles-northern`, `shanghai-china`, `st-lucia-grenadines`, `taiwan`.

### C — sparse markets (REAL gap) — 15 (1–4 routes each)
incl. `cyprus`(1), `ireland`(1), `morocco`(1), `romania`(1), `denmark`(2), `monaco`(2),
`dominican-republic`(2), `galapagos-ecuador`(3), `israel`(3), `madagascar`(3), `sweden`(3),
`great-lakes-usa`(4), `halifax-atlantic-canada`(4), `lebanon`(4), `bar-harbor-mdi-maine-usa`(1).

### D — isolated canonical cities (REAL gap — the "very limited routes" complaint) — 52 across 19 clusters
Canonical member cities that **no corridor touches**. Top: greece 8, morocco 6, indonesia 5,
cote-dazur 4, italy 4, kenya 4, thailand 4 (incl. **`hua-hin-thailand`**), cyprus 3,
india 3 (`chennai-india`, `kochi-india`, `kerala-backwaters-india`), taiwan 2. Full list in
register `D_isolated_cities`.

### E — unresolved-endpoint routes (registry gap; honest-null) — 66
Routes whose endpoints resolve to no canonical cluster: CalMac/Scotland + Norway fjords
(`flam`, `gudvangen`, `balestrand`). They render on the aggregate but attach to no market.
Do **not** invent cluster membership — needs backing city features first (registry lane).

### Named missing connective-tissue corridors (subset of B/C/D — source + mint)
- **Phuket ↔ Langkawi** — both BPs exist (`langkawi-malaysia` has 6 corridors; Phuket lit),
  cross-border TH↔MY, Q-LR range. Never minted.
- **Bangkok ↔ Hua Hin**, **Pattaya ↔ Hua Hin** — `hua-hin-thailand` is a canonical member
  city with 0 corridors (Gulf of Thailand crossings). Never minted.

---

## Grok lanes (ADDRESS)

1. **Deploy `main` @ `2b51b357`** (already unblocked — SEAL refreshed @ `79245162`).
   This alone relights the bulk of "empty markets that used to have routes" (endpoint
   resolution restored by the corridor-render-gap repair). Tasklet verifies live per-market
   after deploy.
2. **Apply A_restamp** (355) — deterministic cluster_id hygiene; re-run scanner to 0 mismatch.
3. **Source + mint (B/C/D + named corridors):** real BP/terminal sourcing at real-world
   scale (consistent with the geometry-completeness directive), then mint corridors.
   **Nobody invents a pier.** Where a canonical city has no sourced BP, hold honest-null.
4. **E:** registry lane — mint backing city features for CalMac/Norway before attaching.
5. **Standing gate:** wire `market_coverage_audit.py` as an acceptance check so empty/sparse
   markets and cluster_id mismatch cannot silently regress after a reseal.

## Tasklet lane
- Flags only (this register + scanner). Verifies live post-deploy. Does not invent geometry.
- Will expand the named-corridor + isolated-city sourcing targets into a per-market BP wishlist
  on request (Grok sources/meshes, nobody invents).
