# GROK SEAL PROMPT — Grab Thailand (Gulf + Andaman)

**Owner of geometry seal:** Grok (deterministic only).
**Authored by:** Tasklet research, 2026-06-22. GitHub `main` is source of truth.
**Branch carrying inputs:** `tasklet/grab-thailand-2026-06-22` (PR #74).

## Mandate
Seal the Tasklet-authored Thailand geography onto the live Atlas render graph and bind the
Grab Thailand derivative's corridors to gold route_ids. Tasklet has authored all boarding points,
connected-city briefs, anchor locale briefs, and the Gate-A crosswalk. **You mint nothing from
scratch — you ID-match, validate, gate, route, and seal what is provided.**

## Inputs (all in-repo on this branch)
| Path | What |
|---|---|
| `grok-routing-output/bucketC-thailand-boarding-points/` | **18 boarding points** across 7 connected cities (Gulf 12 + Andaman 6) + `_CLUSTER-MANIFEST.json` |
| `partner-pitch/city_briefs/{koh-phangan,koh-tao,pattaya,koh-chang,krabi,koh-phi-phi}-thailand.json` | Connected-city briefs (+ registered in `_index.json`) |
| `partner-pitch/city_briefs/{koh-samui,bangkok}-thailand.json` | Enriched anchor briefs |
| `partner-pitch/locale_briefs/` | Pier-level anchor locale briefs (Bangkok Chao Phraya, Phuket eastern piers, Samui north arc) |
| `partner-pitch/GRAB-THAILAND-ANCHOR-CITY-CROSSWALK.json` | Gate-A anchor resolution + BP-authored status |
| `partner-pitch/partners/grab-thailand.json` | The proposal surface; `markets[].journeys_unlocked` are the corridors to bind; `route_ids` currently null |

## Tasks (deterministic)
1. **Validate coords.** Every BP carries `confidence:"low"` and `coord APPROXIMATE` — validate each
   against satellite/gazetteer before routing. Repoint or drop with a logged reason.
2. **Seal BPs as POIs.** ID-match into the gazetteer; promote to POI markers. City-id naming gotcha:
   BP files use country-suffixed slugs (`krabi-thailand`); confirm route/POI slug convention and match
   by prefix to avoid false gaps.
3. **Mint the 7 connected cities** as render geometry: Koh Phangan, Koh Tao, Pattaya, Koh Chang
   (Gulf) + Krabi, Koh Phi Phi (Andaman). (Phang Nga folds under the Phuket/Andaman anchor.)
4. **Build the BP↔BP route graph** for the corridors named in each market's `journeys_unlocked` and
   in the city/locale briefs' `signature_journeys`. Apply water + land-crossing gates.
5. **Bind route_ids** back onto the derivative's corridors and reseal the 3 markets to render.
6. **Separate Thailand-clean Phuket/Andaman** from the older Phuket+Malaysia bundle (no Malaysia in
   this derivative — Thailand only).

## Acceptance gate (your QA report must show)
- BP coverage: **0 silent drops** — every one of the 18 on-disk BPs is either sealed as a POI or in a
  drop-ledger with a reason (junk-POI repoint / failed water-adjacency / unresolved coords).
- **0 land-crossings** (post-gate); **0 orphan routes**; every surviving BP carries a source id.
- The 7 connected cities render real geometry OR are flagged visibly aspirational.
- Derivative corridors carry bound route_ids; 3 markets reseal to render.
- Counts: BPs sealed / dropped (+reason), routes built / culled, before→after POI total, land-crossing=0 proof.

## Out of scope for this seal
- **Economics** is Tasklet-owned: Thailand country-reference row + sourced demand anchors cascade
  through the finance model → Sheets → master tracker. After your seal lands new gold route_ids,
  Tasklet runs the route-keyed economics sidecar (`economics_by_route_id.json`) against the new gold.
- No Malaysia. No Andaman-India confusion (this is Thailand-Andaman: Krabi/Phi Phi/Phuket).
