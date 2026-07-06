# Route Density Policy — Redundant vs Isolated vs Empty (2026-07-06)

Three distinct conditions, three different actions. The target is always the same:
**every rendered corridor is a genuine, distinct, on-water OD pair.** Coverage comes from
real sourced piers (never invented); null beats confidently-wrong.

## A. "Too many / redundant / overlapping" routes
Two very different things get lumped here — only one is a problem:

1. **Distinct intra-metro mesh (KEEP)** — Singapore 409, Abu Dhabi 391, Krabi 360 route
   touches. These are mostly *distinct* berth-to-berth OD pairs = the real marine network
   we just restored. NOT redundancy. Coastal metros genuinely have many piers.
2. **True redundancy (CLEAN)** — the *same two berths* connected by >1 edge (481 such edges
   across 295 berth-pairs post-restore). Pure duplication from overlapping restore sources.
   Action: collapse to one canonical edge. No coverage loss.

Map "spaghetti" is controlled at the **render layer**, not by deleting real routes:
- Marquee/featured gate limits what renders as *signature/wow* (3.0nm floor, land/junk gates).
- Tier-visual weighting controls line prominence.
- Dedupe removes exact duplicates; parallel/near-parallel edges collapse at mint.
So a dense-but-clean metro is correct; it should not look like spaghetti once dedupe + tier
weighting apply.

## B. "Isolated" cities (17)
Has a boarding point / city but **no inter-city corridor** — only self-hops or nothing.
This is *under*-coverage. Action:
1. BP-pair wishlist → source REAL piers + real OD intents (Tasklet flags, Grok mints, nobody
   invents a pier).
2. If no genuine ferry market exists → **honest-null**. Not every coastal city has marine
   mobility.

## C. "Empty" markets (6)
Zero routes at all. Same as isolated but larger gap — needs full BP sourcing from scratch,
or honest-null if there's no real marine-mobility market.

## One-line rule
Redundant → **dedupe** (hygiene, zero coverage loss). Isolated/empty → **source real piers**
(coverage, never invented). Everywhere → **null beats wrong**, and the marquee gate — not
deletion — controls what renders as signature.
