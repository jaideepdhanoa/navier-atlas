# CHANGELOG — Gold #79t — Wave 4 (Pacific / Hawaii) scrub+enrich

**Date:** 2026-06-16
**Bite:** Wave 4 single bite — all four Hawaiian Islands (Oahu, Maui, Kauai, Big Island)
**Ledger:** LB-189 (see `OPS-LOOP-LEDGER.md`)
**Counterpart staged delta:** `/tmp/scrub-wave-4/`

## Counts (Gold #79s → #79t)

| Metric | Before | After | Δ |
|---|---:|---:|---:|
| Routes | 5,317 | 5,330 | **+13** |
| POIs   | 11,002 | 10,980 | **−22** |
| Cities | 171 | 171 | 0 |
| Clusters | 97 | 97 | 0 (1 re-anchor) |
| Sidecar `economics_by_route_id.json` | 78/48 | 78/48 | unchanged |

## Scrub kills (32 BPs)

- **Oahu (22):** Pearl Harbor National Memorial, HARBOR CENTER, Harbors Vintage, Pearl Harbor Hangar 79, Harbor Church Honolulu (+17).
- **Kauai (5):** Harbor Motors Service, Harbors Division, port cruise, cruise port, Scotty's Surf Co. Kauai.
- **Big Island (3):** Island of Hawaii YMCA, The Yard, Speedishuttle Kailua-Kona.
- **Maui (2):** Maalaea Yacht Marina Condos, Kihei (Outrigger) Canoe Club.

USS Arizona Memorial + Pearl Harbor National Memorial intentionally swept via `memorial` token (base Pearl Harbor BP + Disney Cruise Pier 11 retained). Conservatively NOT restored from kills.json — payload note honored.

## Enrich (10 new BPs / 13 new routes / 1 LB-174 re-anchor)

- **10 marquee BPs verified in Hawaii bbox:** Aloha Tower, Waikiki Hilton/Atlantis, Lahaina Harbor, Molokini Crater, Manele Bay (Four Seasons), Kaunakakai Wharf (Molokai), Napali Kalalau Anchorage, Hanalei Bay Tour Mooring, Anaehoomalu Bay (Waikoloa), Kona Village Resort Pier.
- **13 routes minted:**
  - Pioneer II (≤70 nm hard cap): Maui↔Lanai 9 nm (Expeditions), Maui↔Molokini 4 nm, Lahaina↔Maalaea 17 nm intra-Maui, Ko Olina↔Honolulu 18 nm intra-Oahu, Aloha Tower↔Waikiki, Kailua-Kona↔Anaehoomalu, Kailua-Kona↔Kona Village, Maalaea↔Kawaihae 60 nm (longest P-II).
  - Quanta-LR amber-dashed (≤700 nm): Nawiliwili↔Hanalei 22 nm Napali scenic, Port Allen↔Kalalau, Nawiliwili↔Honolulu 75 nm, Maalaea↔Molokai 30 nm aspirational, **Ko Olina↔Maalaea 80 nm aspirational LOCKED OUTSIDE Pioneer II 70 nm hard cap — Superferry restart H2 2026 explicit historical-corridor rationale annotated in label** (NEW standing rule promotion).
- **Cluster re-anchor (LB-174):** `hawaii-usa` cluster re-anchored from city_id `oahu-honolulu-hawaii-usa` → BP `bp-e0ed092434` (Honolulu Harbor BP). Existing 4-member archipelago cluster reused; NO duplicate `hawaii-archipelago` mint (NEW standing rule: existing meta-cluster reuse via LB-174 re-anchor instead of duplicate cluster mint).

## Noise patterns NEW this bite (promotion-ready)

- **Hawaiian NOISE_STRONG (NEW):** `keiki`, `lua`, `kupuna`, `ohana`, `luau`, `condos`, `resort residences`, `beach club`, `surf shop`, `surf co`, `ymca`, `speedishuttle`, `beach park`, `canoe club`. Highest yield Oahu 37%.
- **Hawaiian/Pacific RESCUE_PHRASES (NEW):** Expeditions, Hawaii Superferry, Trilogy, Navatek, Atlantis Submarines, Star of Honolulu, Pride of America (NCL captive), Roberts Hawaii, Kai Kanani, Scotch Mist, Hawaii Nautical, Body Glove Hawaii, Pink Sails, Makani Catamaran.
- **Marina-tail regex tuning:** REMOVE `center/centre/inn` from generic marina-tail (Marina Center named BPs collide). Codify `MARINA_TAIL_OUTDOOR_REC_RE` instead.

## Standing rules promoted by this bite

- **LB-174 existing meta-cluster reuse (NEW):** if cluster already exists with full member roster, RE-ANCHOR per LB-174 instead of duplicate-minting. First instance: avoided `hawaii-archipelago` duplicate of `hawaii-usa`.
- **Q-LR aspirational mint OUTSIDE Pioneer II 70 nm hard cap (NEW LOCKED):** permitted ONLY with explicit historical-corridor / restart rationale annotated in label. First instance: Ko Olina↔Maalaea 80 nm Superferry restart aspirational.

## Pattern carries (consistent with prior bites)

- DUAL-SEAL-WRITE (LB-182) + nested-blob SEAL shape (LB-188) — sha256 over actual bytes (LB-171).
- Phase-reorder + FUSE-quota fallback (LB-184/185/186/187): prior gold zip deleted BEFORE new zip cp; live changelog mirror to `atlas-external/data-clean/CHANGELOG-FOR-CLAUDE-2026-06-16-scrub-w4.md` skipped by default per standing rule.
- Economics sidecar built with `--aggdir finance/recal` (LB-185).
- 11th consecutive bite of inline LB-179/180/186/187 classifier+sweep patches. **Promotion backlog NOW OVERDUE — fires on this entry.**

## Wave 4 status: COMPLETE

After this seal Wave 4 (Pacific / Hawaii) is closed. **Strongly recommend pausing for classifier patch + scrubber promotion ship BEFORE starting Wave 5.**

## Pre-existing carries (NOT introduced this bite)

- 5 Sabah duplicate route_ids
- ~3,025 global orphan-endpoint bp- routes
- 2 Wakatobi POI dups
- Oman / Philippines cluster anchor orphans
- 4 HARD endpoint-label flags Philippines + UAE (identical to #79s)
- `atlas-external/content_store/navier-content.db` absent (9 consecutive bites)
