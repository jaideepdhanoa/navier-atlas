# GROK SPEC — BP Wishlist + Taiwan Restore (2026-07-06)

Tasklet flags real piers + intended OD pairs. **Grok sources exact coordinates, water-routes, mints proper `rn-` OD-pair corridors, re-seals.** Nobody invents a pier — every named terminal is a real, verifiable ferry port; confirm coords before minting.

Register: `handoff/BP-WISHLIST-2026-07-06.json`

## Part A — Taiwan (HIGHEST priority; regression, not a greenfield gap)

**What happened:** Taiwan is a fully-built canonical market (rich `data-clean/cluster_briefs/taiwan.json` + `kaohsiung-taiwan`/`penghu-taiwan` city briefs + a Grab deck slide). But on 2026-07-06 the global inherit-all `_map_scope` regen dropped Taiwan from `grab.json` entirely — `partner_corridors = global_canonical ∩ clusters` returned ∅ because Taiwan's **only** ROUTES entries were self-referential `ics-` intra-city hops, which the de-spaghetti cull correctly removed. Zero canonical corridors → Taiwan fell out of Grab's `registry_keys` and off the live map.

**Fix — mint 5 REAL OD-pair corridors (not ics- hops):**

| Corridor | nm | Tier | Source |
|---|---|---|---|
| Kaohsiung Ferry ↔ Cijin | ~1 | coastal | new mint · 3.2M riders/yr · **needs ISLAND_CITIES exception (<3nm)** |
| Donggang ↔ Xiaoliuqiu | ~9 | coastal | new mint · 1.1M crossings/yr · intra-kaohsiung → exception |
| Budai ↔ Magong (Penghu) | ~33 | coastal | new mint · mainland–Penghu trunk (cross-city) |
| Magong ↔ Xiyu / Baisha | ~12 | coastal | new mint · Penghu inter-island → exception |
| Kaohsiung ↔ Magong | ~73 | quanta_lr | **restore peak geometry** `e__kaohsiung-taiwan__kaohsiung-port__penghu-taiwan__magong-harbor` |

Then: add `taiwan` back to `grab.json` `_map_scope.registry_keys` + `cluster_city_ids` (inherit-all will bind the corridors automatically once sealed).

**ISLAND_CITIES hygiene exception (new, analogous to RIVER_CITIES):** add `{kaohsiung-taiwan, penghu-taiwan, koh-larn-thailand}` — floor ~0.4nm, keep genuinely-on-water cross-BP intra-city corridors. Prevents re-culling Cijin / Penghu inter-island on next hygiene pass.

## Part B — Batch 2b still pending
The 5 isolated-city corridors (Koh Lanta ↔ Phi Phi/Krabi/Phuket, Nice/Cannes ↔ St-Tropez) from `CORRIDOR-RESTORE-QLR-BATCH2B-ISOLATED-CITY.json` are **not yet applied** (`c6ce3116` was Batch 2's 22 Q-LR only). Current audit still lists koh-lanta/nice/saint-tropez as isolated. Please fold into next apply.

## Part C — Empty markets + isolated cities (source + mint)
Full named-pier wishlist in `BP-WISHLIST-2026-07-06.json`:
- **6 empty markets:** Balearics, Bay of Naples/Amalfi, KSA-commercial (Yanbu), Leeward Antilles (ABC), Shanghai, St Lucia/Grenadines.
- **35 isolated cities across 15 clusters** — Morocco (6), Kenya (4), Greece (5), India (3), Italy (3), Côte d'Azur (3), etc. Named coastal neighbours + OD intents per cluster in the register.

Priority order: Taiwan → Batch 2b → empty markets → isolated cities. Honest-null anything where a real pier can't be confirmed.
