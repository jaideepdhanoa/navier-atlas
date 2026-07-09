# De-Spaghetti Cull — Class-Bug Review (2026-07-06)

**Trigger:** Jaideep clarified — `<3nm` is a **marquee/featured curation gate, NOT a corridor-existence gate**. A short corridor may exist as a normal route if it is *meaningful* (real distinct BPs, on water, no land crossing, not spaghetti). Taiwan revealed the cull used `<3nm` + "same city_id = self-referential" as a **deletion** rule. Question: how wide is the blast radius?

## The numbers (jul3 → current diff, distinct-BP OD pairs)

Total dropped distinct-BP OD pairs: **3,770**
- **602** — land-crossing → correct drops (stay dropped).
- **101** — cross-city on-water → the inter-city restore lane (Batch 1/2/2b already cover the real ones).
- **3,067** — **intra-metro, distinct-BP, on-water** → the newly-surfaced class. THIS is the blast radius.

## The 3,067 split two ways (this is the whole point)

**(1) Road-metro spaghetti — CORRECTLY culled, do NOT restore the mesh.**
Big mainland commuter metros where every-BP-to-every-BP combinatorial edges made a hairball and where roads/metro exist:
Singapore (~208), Abu Dhabi (179), Dubai (163), Sharjah (160), RAK (101), Jakarta (100), Doha (91), Mumbai, Manama, Kochi, Kolkata, HCMC, Istanbul, etc.
→ These are the intended WS-7/WS-8 de-spaghetti targets. Keep culled (or restore only the ONE signature water crossing per metro, never the mesh).

**(2) Ferry-necessary island/archipelago/resort markets — WRONGLY culled, RESTORE the meaningful ones.**
Markets where water IS the network (no road alternative between the islands) and the intra-cluster hop is literally the product:
Krabi/Phi Phi/Railay (~179), Bali (125), Mykonos (109), Santorini (59), Koh Chang (58), Koh Phangan (78), Andaman (36), Riau Is (39), Komodo/Flores, Raja Ampat, Karimunjawa, Male/Maldives, Langkawi, Penang, Naples/Capri/Procida, Venice lagoon, Kaohsiung/Penghu (Taiwan), Aeolian/Sicily, Corfu/Ionian, Krabi cluster, San Blas, Nicoya, Seychelles, etc.
→ These are Taiwan's exact failure mode at scale. The cull deleted real ferry routes for being short + intra-metro.

## Recommended policy (principled, defensible)

1. **Restore criterion (ferry markets):** intra-metro OD pair qualifies for restore if — distinct real BPs · on water · `_qa_land_flag=false` and land_km ≤ 0.25 · endpoints are on **separate landmasses / islands** (ferry is the only link) · not a junk/POI endpoint. **No distance floor** for existence (Cijin 1nm is valid). Reuse July-3 proven geometry.
2. **Hold criterion (road metros):** intra-metro meshes on mainland commuter metros stay culled; restore at most one signature crossing.
3. **Marquee rule stands:** none of these `<3nm` corridors may be `featured/signature/wow`. Marquee floor stays 3.0nm (0.4nm river/island exception).
4. **New hygiene exception ISLAND_CITIES** (analogous to RIVER_CITIES) so restored island hops survive the next hygiene pass.

## Why cluster `type` alone can't auto-decide
Most ferry markets (Bali, Riau, Komodo, Andaman) sit under `country`-type clusters (Indonesia/India), same bucket as Gulf road-metros. The separate-landmass test is the real discriminator → needs a per-OD landmass check at mint time (Grok's lane) or a curated ferry-market allowlist.

## Recommendation
This is a **map-shape decision** bigger than the isolated-cities wishlist. Two options for Jaideep:
- **A (broad):** authorise a full ferry-market restore pass (separate-landmass rule) across all island/archipelago/resort clusters — recovers the real product surface, biggest lift.
- **B (narrow):** restore only deck-backed + isolated ferry markets for now (Taiwan, Batch 2b, wishlist cities); defer the rest.

Awaiting his call before mass-minting — restoring wrong = re-spaghetti; not restoring = hundreds of dead real ferry routes.
