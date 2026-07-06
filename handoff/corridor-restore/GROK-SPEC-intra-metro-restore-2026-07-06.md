# GROK SPEC — Global Intra-Metro On-Water Corridor Restore (2026-07-06)

**Jaideep directive (2026-07-06):** The de-spaghetti cull over-reached. It deleted valid intra-metro marine OD pairs, not just junk. Coastal metros (Jakarta, Mumbai, Doha, Dubai) legitimately have marine mobility that **augments** car routes — do NOT cull a route just because the city is on a coast or a road also exists. This is the **UAE canonical corridor discipline applied globally**: keep every genuine, distinct, on-water OD pair; eliminate only duplicates, parallel edges, land-crossers, junk BPs.

## Register
`RESTORE-REGISTER-intra-metro-onwater-2026-07-06.json` — **3,076 corridors across 119 cities**, all with July-3 proven water-following geometry.

## Restore rule (apply per corridor)
Restore an entry IF at mint it satisfies ALL:
1. Two **distinct real BPs** (not junk/POI — apply `bp_hygiene.py`).
2. **On water**, no land crossing > 0.25 km (recheck geometry).
3. Not a **duplicate / near-parallel** of an already-present or already-restored edge in the same metro → dedupe, keep one representative.

**No distance floor for EXISTENCE** — a 1nm harbour ferry (e.g. Kaohsiung↔Cijin) is valid. The 3.0nm floor is a **marquee/featured** gate only; short restored hops render as normal routes, never signature/wow.

## Guards
- **Copy July-3 proven geometry** (same safe strategy as Batch 1/2). Re-seal `edge-`/`gcn-`/`e__` sources → fresh `rn-` ids.
- **Parallel/duplicate dedupe is the spaghetti control**, not geographic culling. Metros with high counts (Singapore 208, Abu Dhabi 192, Dubai 170, Sharjah 163) will shrink after dedupe — that's expected; keep the distinct OD pairs.
- **UAE conservatism:** abu-dhabi / dubai / sharjah / ras-al-khaimah were hand-curated in WS-7/WS-8 (55 cut, 17 preserved, 8 creek segments minted with water-following waypoints). Apply dedupe carefully so the creek spine is preserved; restore only genuinely distinct OD pairs that were over-cut.
- Add **hygiene exception** so restored short intra-metro hops survive the next `bp_hygiene` pass (extend the RIVER_CITIES/ISLAND_CITIES exception model to all coastal-metro cities in this register).
- Land-crossers and junk-BP endpoints in the register (already excluded, minimal) stay dropped.

## Sequence
1. Fold in still-pending **Batch 2b** (5 Koh Lanta + Riviera corridors) — did not land in `c6ce3116`.
2. Then this intra-metro restore pass.
3. Re-run `market_coverage_audit.py` + `bp_hygiene.py` (target 0 residual) as acceptance.
4. Re-add Taiwan to Grab scope (per prior BP-wishlist spec) once its OD pairs seal.

## Acceptance
- Report routes before→after, restored vs deduped counts, per-metro deltas for the top 25 cities.
- Visual QA on Jakarta, Doha, Dubai, Singapore, Mumbai, Bali, Mykonos, Kaohsiung — confirm valid marine mesh present, no land-crossers, no parallel dupes.
