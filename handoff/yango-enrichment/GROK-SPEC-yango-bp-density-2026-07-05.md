# GROK SPEC — Yango BP density & clean routing (Peru · Senegal · Caspian · Maghreb)

**Owner:** Tasklet (research) → Grok (deterministic seal)
**Date:** 2026-07-05
**Trigger:** Jaideep flagged poor BP density + routing in Peru, Senegal, Caspian, Maghreb.
**Status:** research-complete / seal-needed.

## Scope & entry points
Four thin Yango markets deepened to real-world density with source-backed boarding points, short-hop corridors, and explicit hand-waypoints (no land crossings). Two already shipped, two new here.

| Market | Enrichment file | New BPs | New corridors | New cities |
|---|---|---|---|---|
| Caspian (AZ + KZ) | `caspian-enrichment-2026-07-05.json` *(PR #185)* | ~10 | 7 | 0 |
| Maghreb (Morocco + Tunisia) | `morocco-…` + `tunisia-enrichment-2026-07-05.json` *(PR #185)* | ~25 | 16 | ~6 |
| **Peru** | `peru-enrichment-2026-07-05.json` *(this batch)* | ~9 | 6 | 1 (Pisco/San Andrés) |
| **Senegal** | `senegal-enrichment-2026-07-05.json` *(this batch)* | ~9 | 6 | 3 (Saly, Somone, Mbour) |

Caspian + Maghreb route-mint spec is already written: `GROK-SPEC-caspian-maghreb-enrichment-2026-07-05.md` (PR #185). This doc adds Peru + Senegal and states the shared routing contract for all four.

## Shared routing contract (all four markets)
1. **ID-based matching only.** Every BP in the enrichment files is a real named place with a source URL. Do deterministic gazetteer promotion → exact coords → ID-match seal. Null beats confidently-wrong. Do not invent coords, cities, or corridors.
2. **New cities are additive.** Pisco/San Andrés (Peru); Saly, Somone, Mbour (Senegal) are sourced registry additions — mint as new city_ids under the existing `peru` / `senegal` clusters. Do not demote or drop existing cities/anchors.
3. **No land crossings.** Honour every `hand_waypoint_note`. Key offshore-rounding cases:
   - **Senegal:** Dakar port (SE) ↔ Ngor/Almadies (NW) must round the Cap-Vert / Les Almadies tip **offshore** — never cross the peninsula.
   - **Peru:** Callao island runs stay **offshore** of the naval/restricted islands (San Lorenzo, El Frontón) — water approach, no landings. Costa Verde runs stay offshore of the surf line.
   - **Caspian (Baku):** round the Absheron peninsula east tip offshore (south shore ↔ north shore).
   - **Maghreb:** stay in Moroccan/Tunisian water — offshore of Ceuta/Melilla (Spanish enclaves) and the Gulf of Gabès / Djerba shoals (depth mask).
4. **Range discipline.** Never mint corridors >70 nm as Navier routes: Callao↔Paracas (~130 nm), Baku↔Aktau (~250 nm cross-border), Dakar↔Saint-Louis/Casamance (~140 nm) stay context/ferry only. Range-edge links (La Punta↔Ancón ~18 nm; Dakar↔Saly ~40 nm) mint **only** if duty-cycle verifies.
5. **route_id inheritance / grounding.** Mint route_ids for each corridor at seal; corridors that cannot be grounded stay honest-null (do not fabricate a route_id).
6. **Depth/shoal masks.** Respect shallow-water masks on Somone lagoon (Senegal), Gulf of Gabès/Djerba (Tunisia), and lagoon mouths generally.

## After seal (cascade)
- Return sealed route geometry + route_ids + render QA.
- Fold new corridor L3 into the Yango finance registry (`finance/model/corridors.json`) for `yango-peru`, `yango-senegal`, `yango-caspian-az`, `yango-tunisia`/`yango-morocco` — reconcile with the model rebuild spec (PR #184). Do **not** invent L3 demand; use the model's standard corridor-seeding.
- Refresh the Yango deck market slides only after seal (Atlas screenshots are Jaideep's insert).

## No-shrink guarantee
This is additive density work. No existing Yango city, anchor BP, corridor, map-scope entry, or footprint key is removed. Peru stays 2 cities + deepened; Senegal stays 1 city + Petite Côte spur; Caspian/Maghreb per PR #185.
