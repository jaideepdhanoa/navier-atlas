# Changelog for Claude — 2026-06-01 — Partner HUB layout (Uber + Grab)

## What changed
Introduced a **hub/spoke** render mode for multi-market platform partners. Two partners converted:
`uber` (9 markets) and `grab` (5 markets). All other partners remain `layout:"single"` (flat) — no change.

## Schema additions (`partner-pitch/schema/partner_proposal.schema.json`, backward-compatible)
1. **`layout`** (top-level, enum `"single"|"hub"`, default `"single"`)
   - `"single"` = the existing flat one-page proposal. **Unchanged behaviour.**
   - `"hub"` = render an **index landing page** (global thesis + map + market grid) at the bare route, with per-market **deep-dives** at sub-routes.
2. **`network_thesis`** (top-level, hub only): `{ headline, body, stats[{label,value,sub}], how_to_read }` — the global network argument shown on the index above the market grid.
3. **`markets[]`** extended (was already present): added `slug`, `summary` (card blurb), `recommended_entry` (bool), `status` (freeform momentum cue), `anchor_cities` (city_ids for card thumb + market map focus). Each market is a full mini-proposal: `hero, why_now, multimodal_fit, journeys_unlocked, proof_points, objections, phases, close, differentiation`.

## Routing (please implement)
- **`/uber`** → render the **index** (network_thesis + global map + a card per `markets[]` entry). Bare `/uber` is the index, NOT a redirect target away.
- **`/uber/{market.slug}`** → render that market's deep-dive (full proposal layout, scoped to `anchor_cities` + its `phases`).
- Same pattern for **`/grab`** and **`/grab/{slug}`**.
- Market slugs:
  - **uber**: `mena` (recommended), `miami`, `bay-area`, `hawaii`, `mediterranean`, `sydney-nsw`, `brazil-latam`, `italy-luxury`, `cote-dazur`
  - **grab**: `singapore` (recommended), `cross-border`, `bali`, `phuket`, `philippines`
- `recommended_entry:true` marks the suggested starting card on the index (badge/sort-first). It does **NOT** diminish the others — all markets are presented as equal, real opportunities.
- Top-level `phases` on a hub partner = the **recommended regional sequence** to show on the index (Grab keeps its crisp 4-phase sequence here). Per-market `phases` drive each deep-dive.

## Framing rule (important)
Do **not** tier or hedge markets as "optionality only" / "network reach". Every market card is a real opportunity; exclusivity is a negotiation matter, not a page label. Content depth varies (MENA/Miami/Singapore are deepest) but framing is uniform.

## Data hygiene fix bundled in
- Fixed a dead node id in `grab.json`: `malaysia-desaru-coast` → **`desaru-coast-malaysia`** (canonical `{place}-{country}`), in both phases and journeys. This previously dangled and dropped the SG↔Desaru route.

## Stories
`gen_partner_stories.py` is already markets-aware (`gather_cities`/`first_camera` walk `markets[].phases`). Regenerated; uber story now scopes all 9 markets' cities. Grab story stays hand-authored in base `stories.json` (BASE_STORY_PARTNERS) — unchanged.

## Notes / open
- `sumba-indonesia` is referenced narratively in grab→bali (the Bali→Lombok→Komodo→**Sumba** chain) but is **not yet a node**; map linkage uses `bali/lombok/komodo-flores`. Add a Sumba node later if we want it pinned.
- Hawaii appears both as its own `single` partner page (`/hawaii`) and as an Uber market (`/uber/hawaii`) — intentional; the Uber one is the demand-app framing, complementary not conflicting.

---

## RESOLVED — your two action items from 2026-06-01 partner-tour render pass
**(1) route_scope on single-city phases → fixed at source.** Set `route_scope:"intra"` on every phase that resolves to ≤1 city, across ALL partners + markets. 10 phases corrected (abu-dhabi-itc p2, dubai-rta p2, qatar p2, red-sea-global p2, saudi-pif p2, singapore-mpa p2, grab/singapore p2, grab/phuket p1, grab/philippines p1, uber/bay-area p3). Your safety-net (force ≤1-city phase to intra) is now belt-and-suspenders. **0 single-city `route_scope:"all"` phases remain.**

**(2) `addressable_market_count` semantics — reconciled & documented.** It counts **addressable sub-markets/metros** in the partner's end-state region (a TAM figure), **intentionally ≥** the count of specifically-named `end_state_cities` nodes. Existing values already follow this (abu-dhabi-itc=10 over 2 nodes; grab=30 over 19; hawaii=6 over 4). The only inconsistent value was `dubai-rta=1` (below its 2 lit nodes) — **corrected to 8** (Dubai waterfront sub-markets: Creek, Marina, JBR, Palm, Harbour, Festival City, Bluewaters, Deira). **Invariant going forward: `addressable_market_count` ≥ phase-union node count for every partner.** Your render rule ("drop the 'of M' when M < lit count") is still a good guard, but the data now never trips it.
