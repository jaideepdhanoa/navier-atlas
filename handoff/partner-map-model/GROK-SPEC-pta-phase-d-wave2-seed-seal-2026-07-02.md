# GROK SPEC — PTA Phase D Wave 2 · greenfield seed-and-seal (4 authorities)

**From:** Tasklet · **Date:** 2026-07-02 · **Phase:** D (Batch-8) Wave 2

## Why this is a seed-and-seal handoff (not bound partner JSONs)
All four Wave-2 authorities are **greenfield** — the atlas holds **no real boarding points** for them (every existing hit is a mis-geocode; see each dossier `atlas_warning`). Per "null beats confidently-wrong," Tasklet does **not** emit partner JSONs with guessed `bp-`/`rn-` geometry. Instead this follows the established **seed-node pattern** (Brisbane / Hamburg / Kochi / kakao-Seoul): Tasklet ships sourced dossiers + seed city-node coordinates; **Grok geocodes + mints BPs and seals routes** with hand-waypoints, then Tasklet binds the partner JSON in a follow-up.

Dossiers (this PR): `PTA-DOSSIER-seoul-hangang-bus.json`, `PTA-DOSSIER-mersey-ferries.json`, `PTA-DOSSIER-toronto-island-ferry.json`, `PTA-DOSSIER-calmac.json`.

## Grok asks — per authority

### 1. Seoul / Hangang Bus (`seoul-hangang-bus`) — SMG public transit
- **Reuse** existing city node `seoul-incheon-korea` (do not mint a new one).
- **Reconciliation (critical):** Han River piers are physically singular. Bind the **shared piers Yeouido / Ttukseom / Jamsil to ONE canonical pier node each** — the same physical node the kakao-mobility `seoul-han-river` seal uses (currently `bp-kakao-*`). **Do not double-plot.** Keep Hangang (SMG public transit) and kakao (commercial) as **separate markets/stakeholders**; only the physical BP nodes are shared.
- **Mint new** Hangang-exclusive piers: Magok, Mangwon, Oksu, Apgujeong.
- **Seal** the trunk: Jamsil↔Yeouido (Eastern), Magok↔Yeouido (Western), Yeouido↔Ttukseom, Magok↔Jamsil through-run (~28.9 km). All **riverine → hand waypoints, interior_land_km == 0**, follow the Han River channel.

### 2. Mersey Ferries (`mersey-ferries`) — Merseytravel / LCRCA
- **Mint seed city node** `liverpool-mersey-uk` on River Mersey water `[-3.0120, 53.4080]` (`_seed_node`, `_link_status: geometry_seal_pending`, `cluster_id` per UK convention).
- **Mint BPs:** Gerry Marsden/Pier Head (Liverpool), Seacombe (Wallasey), Woodside (Birkenhead — under refurb, include).
- **Seal** Pier Head↔Seacombe, Pier Head↔Woodside, Seacombe↔Woodside. Short estuary crossings; hand-waypoint clear of landing-stage shorelines.

### 3. Toronto Island Ferry (`toronto-island-ferry`) — City of Toronto
- **Mint seed city node** `toronto-island-canada` on Inner Harbour water `[-79.3775, 43.6300]`.
- **Mint BPs:** Jack Layton Ferry Terminal (hub), Centre Island, Hanlan's Point, Ward's Island.
- **Seal** hub→3 island docks (hub-and-spoke). Protected harbour crossings; hand-waypoint around island shoreline + breakwater.

### 4. CalMac (`calmac`) — Transport Scotland lifeline network
- **Mint seed city node** `firth-of-clyde-scotland` on Clyde water `[-4.9500, 55.7000]`.
- **Domestic-first scope:** seal only the busy Clyde gateway crossings now — Ardrossan↔Brodick (Arran, busiest), Wemyss Bay↔Rothesay (Bute), Gourock↔Dunoon (Cowal), Oban↔Craignure (Mull). **Hold** Outer Hebrides long-haul lifeline legs for a later horizon.
- Open-water crossings; hand-waypoint around headlands/harbour approaches.

## Global guardrails
- **Do not bind any existing atlas hit** for these authorities — all are mis-geocodes (Birkenhead→Sydney, Woodside→Nova Scotia, Tacloban→Philippines, Otrobanda→Curaçao). Greenfield mint only.
- Hand-waypoints on every riverine/enclosed leg (interior_land_km == 0). Null beats wrong.
- Economics = authority public-value lane (Grok), post-seal. No `growth_case` authored by Tasklet.
- **Follow-up:** once BPs/routes are sealed, Tasklet binds each partner JSON (both trees) in the Kolkata/Manila anchor-ready pattern and opens per-authority PRs.
