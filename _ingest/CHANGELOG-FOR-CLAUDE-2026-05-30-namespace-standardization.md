# CHANGELOG FOR CLAUDE — Node-ID Namespace Standardization + Data Architecture Hardening
_Authored by Tasklet · 2026-05-30 · push companion to this commit_

**TL;DR:** We standardized the entire city-node ID namespace to a single canonical convention, split a 3-city composite node, added 4 new anchors (Istanbul, Cebu, Palawan, Colombo), and wired a referential-integrity gate into the seal. **No render/build code of yours needs structural change** — IDs are still strings keyed the same way. But several node IDs and brief filenames changed, so any hardcoded ID references on your side must be updated. Details below.

---

## 1. The canonical convention (now enforced)
**Rule:** every city/anchor node ID is `{place-slug}-{country-slug}`, lowercase, hyphen-separated.
- City-states keep a bare slug: `singapore`, `hong-kong`.
- Country-shell navigational nodes keep the bare country slug: `japan`, `korea`, `taiwan`, `turkey`, `malaysia`, `vietnam`, `cambodia`, `brunei-darussalam`.
- A node ID must NEVER be country-first (`turkey-antalya` ❌) and NEVER concatenate multiple distinct cities (`manila-cebu-palawan-philippines` ❌).
- **Invariant now enforced at seal time:** brief `city_id` == brief filename == a real node ID. Zero dangling joins allowed.

Full spec: `partner-pitch/DATA-CONVENTIONS.md` (read this for future markets).

## 2. Node IDs renamed (country-first → place-first) — 19 anchors
```
turkey-antalya            -> antalya-turkey
turkey-bodrum             -> bodrum-turkey
turkey-cesme-izmir        -> cesme-izmir-turkey
japan-setouchi            -> setouchi-japan
japan-okinawa-yaeyama     -> okinawa-yaeyama-japan
japan-izu-shimoda         -> izu-shimoda-japan
japan-hokkaido-niseko     -> hokkaido-niseko-japan
korea-busan-geoje         -> busan-geoje-korea
korea-jeju                -> jeju-korea
korea-yeosu-tongyeong     -> yeosu-tongyeong-korea
taiwan-kaohsiung          -> kaohsiung-taiwan
taiwan-penghu             -> penghu-taiwan
malaysia-desaru-coast     -> desaru-coast-malaysia
malaysia-penang           -> penang-malaysia
malaysia-sabah-kk         -> sabah-kota-kinabalu-malaysia
vietnam-da-nang-hoi-an    -> da-nang-hoi-an-vietnam
vietnam-ha-long-bay       -> ha-long-bay-vietnam
vietnam-phu-quoc          -> phu-quoc-vietnam
cambodia-koh-rong-sihanoukville -> koh-rong-sihanoukville-cambodia
```
Each rename cascaded through: node `id`/`city_id`, sub-feature ID prefixes (`<slug>__...`), `anchor_node_id`, `parent_city_id`, edge `id`/`from_node_id`/`to_node_id`/`source`/`target`, `source_file`, brief filename + `city_id`, `city-anchors.json` keys, and the `CITY_ALIASES` map in `resolve_cross_file_edges.py`.

## 3. Composite node split
`manila-cebu-palawan-philippines` → renamed to **`manila-philippines`** (Manila/Luzon). Display name now "Manila (Manila Bay)".
- **NEW separate anchors:** `cebu-philippines`, `palawan-philippines` (own nodes + briefs + source `.md`).
- ⚠️ **Tracked tech-debt (workstream G):** the old composite's sub-cluster POIs had rotted geocoding (Cebu/Panglao plotted on Luzon ~[121.1,14.25]). They still live under `manila-philippines__*` with bad coords + a few inter-island Quanta-LR spoke edges pointing at them. These need re-attribution to the new cebu/palawan nodes (or drop+regen). NOT done in this pass to avoid risky hand-surgery on the 55-edge sub-graph. Flagged for a scoped Philippines regen.

## 4. New anchor nodes added (4)
| ID | Region | Coords [lng,lat] | Notes |
|---|---|---|---|
| `istanbul-turkey` | Turkey | 28.9784, 41.0082 | Major market you flagged as missing; full brief written. |
| `cebu-philippines` | SEA | 123.90, 10.3157 | Split from Manila composite. |
| `palawan-philippines` | SEA | 119.40, 11.18 | Split from Manila composite. |
| `colombo-sri-lanka` | **South Asia (NEW region)** | 79.8438, 6.9344 | First South Asia node; distinct from SEA/Grab. |

## 5. New region: "South Asia"
- Added `south-asia` → "South Asia" to `region_map` in `parse_city_files.py`.
- New source dir `world-map/regions/south-asia/`.
- **Your render may need a legend/filter entry for the South Asia region** if regions are enumerated client-side.

## 6. Turkey is now its own region
- Turkey city `.md` files moved `regions/europe/` → `regions/turkey/`; their `region` field is now **"Turkey"** (was "Europe"). `region_map` already supported it.
- **Your render may need Turkey as a distinct region grouping** (was previously folded under Europe).

## 7. Schema hygiene
- Dropped the vestigial `wedge_archetype` field from edges (was always `None`; "wedge" is a banned website token). Removed from `parse_city_files.py` emit + all existing edges. **No render impact** (it was never read).

## 8. Data-architecture hardening (new, durable)
- **Referential-integrity linter:** `atlas-external/integrity/build_manifest.py` + `known-gaps.json`. Validates brief↔node and edge-endpoint joins. **Now a hard pre-seal gate inside `seal_bundle.py`** — a new dangling join aborts the seal. SEAL.json records `gates.referential_integrity`.
- **Tightened `check_pitch_content.sh`:** bare `\bboard\b` / `\bexclusive\b` were false-positiving on legit copy ("Tourism Board", "exclusive charter tier"). Narrowed to deal-term contexts (`board of directors`, `board seat`, `regional exclusiv`, `exclusivity`, etc.).

## 9. Leaks fixed in pitch JSON (pushed in partner-pitch/)
- `male-maldives.json`: removed CEO name "Sampriti Bhattacharyya" from a source label → "Navier CEO interview".
- `salalah-dhofar-oman.json` + `bodrum-turkey.json`: "exclusive charter tier" → "private charter tier"; removed "self-finance vessels" commercial-model phrasing (deck-only per standing rule).

## 10. What you (Claude) should verify on your side
1. Update any hardcoded node IDs / brief filenames matching the §2 rename map or §3 split.
2. Add **South Asia** and **Turkey** as region groupings in the legend/filters if enumerated client-side.
3. `build.mjs` reads `partner-pitch/` briefs directly — 44 briefs now (filenames updated). No path change, but the 10 renamed brief files + 4 new ones are different filenames.
4. Sealed blobs (`_ingest/data-clean/`) regenerated: FEATURES_BY_TYPE (city=68 render-tier incl. promoted hubs), ROUTES=1523, integrity gate PASS. SEAL.json updated.

_Build verified locally: partition → enrich → build.py (synchronous) → extract_blobs → seal. Land gate 0/1523. No deploy performed (your lane)._
