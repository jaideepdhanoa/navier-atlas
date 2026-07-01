# GROK SPEC — Red Sea Global: Thuwal repoint + three-destination connectivity (2026-07-01)

**Supersedes the Jeddah-gateway scope in `GROK-SPEC-red-sea-global-ksa-repoint-2026-07-01.md`.**
Jaideep directive (2026-07-01): RSG scope = **The Red Sea + AMAALA + Thuwal** (RSG's own three portfolio destinations, per https://redseaglobal.com/en/portfolio/). **Jeddah is dropped as an RSG destination.** Cover **within-cluster** and **between-cluster** connectivity for all three, in the map, phases, and corridor unit economics.

Tasklet lane is complete for the proposal/data layer (this commit). The items below are **Grok's seal lane**.

---

## 1. Node promotion (map render) — REQUIRED
Three destinations must render as first-class nodes. Today only `red-sea-global-ksa` is a `city` feature; the other two exist **only as POI `parent_city_id` values** and must be promoted to `city`/`priority_city` features:

| Node id | Promote to | Anchor coord (from existing BPs) | Label |
|---|---|---|---|
| `red-sea-global-ksa` | already `city` | [36.93, 25.46] | The Red Sea |
| `amaala-triple-bay-ksa` | new `priority_city` | see §4 coord conflict — resolve first | AMAALA (Triple Bay) |
| `thuwal-private-retreat-ksa` | new `priority_city` | [39.0972, 22.305] (KAUST Harbour) | Thuwal (Private Retreat) |

Note: the `city` feature `red-sea-global-ksa` is currently named "Red Sea Global (RSG + AMAALA)". Once AMAALA is its own node, rename the anchor to **"The Red Sea"** so the three destinations read distinctly. There is also a `the-red-sea-archipelago-ksa` POI-parent (Sheybarah/Shura/Ummahat jetties) — fold into `red-sea-global-ksa` or promote consistently; do not leave a duplicate un-rendered parent.

## 2. Routes to mint (hand-waypoints, `interior_land_km==0` gate)
All `route_id: null` + `_link_status: geometry_seal_pending` in the partner JSON. Mint with explicit **hand waypoints hugging open water — no land crossings.**

**Within The Red Sea** (Pioneer II; most already sealed in the existing 98-edge mesh — verify, don't duplicate):
- Shura Island Marina [36.966842, 25.491622] ↔ Ummahat AlShaykh Resort Jetty [36.4626, 25.5536] (St Regis / Nujuma cluster) — ~9.7 nm
- Shura Island Marina ↔ Sheybarah Island Resort Jetty [36.6486, 25.4133] (Shebara)
- Shura Island Marina ↔ Turtle Bay [36.998241, 25.502429] — ~6 nm
- Resort-island ↔ resort-island infill

**Within AMAALA** (Pioneer II):
- AMAALA Triple Bay Marina ↔ AMAALA Yacht Club Jetty — ~0.4 nm
- AMAALA Yacht Club ↔ Four Seasons AMAALA / Six Senses AMAALA / Rosewood AMAALA jetties

**Within Thuwal** (Pioneer II) — NEW:
- KAUST Harbour (Thuwal) [39.0972, 22.305] ↔ Thuwal Private Retreat Jetty [39.083299, 22.278] — ~2 nm (the marquee corridor; today a ~45-min conventional yacht sail from KAUST North Marina)
- Thuwal Private Retreat ↔ coral-archipelago anchorage (short reef hop)

**Between-cluster** (Quanta-LR long-range):
- **The Red Sea (Shura) ↔ AMAALA (Triple Bay)** — ~77 nm coastal leg. Waypoints must hug the coast around the Al Wajh lagoon headlands; **no interior land crossing.** This is the featured "between" corridor.

## 3. Honest geographic constraint — DO NOT fabricate
Thuwal sits ~400 nm south of The Red Sea/AMAALA (off Jeddah, ~22.3°N vs ~25.5–26.7°N). **Do NOT mint a Thuwal↔The Red Sea or Thuwal↔AMAALA sea corridor** — it exceeds even Quanta-LR single-leg range and would cross into non-credible territory. Thuwal's role in the network is the **southern Jeddah-proximate gateway + private-island retreat**; inter-destination movement to the northern cluster is via air (Fly Red Sea / RSI), not a Navier sea leg. Represent Thuwal connectivity as within-cluster only.

## 4. AMAALA coordinate conflict — resolve (null-beats-wrong)
Two AMAALA BP sets exist ~26 km apart:
- under `red-sea-global-ksa`: AMAALA Yacht Club [36.210726, 26.64992], Four Seasons [36.216566, 26.64517], Six Senses [36.229056, 26.636999]
- under `amaala-triple-bay-ksa`: Triple Bay Marina [36.4717, 26.7456], Yacht Club Jetty [36.476, 26.751]
Pick the correct set (real Triple Bay ≈ 26.7°N), retire the wrong one, and bind the AMAALA node + within-AMAALA routes to the survivors. ID-based matching only.

## 5. Scope hygiene
- Confirm no RSG-tagged edges to `jeddah-ksa` or `neom-*` remain in RSG scope (PIF/bolt/yango sibling edges preserved). The Jeddah `journeys_unlocked` entry and Phase 3 have been repointed to Thuwal in the partner JSON.
- Residual Port-of-NEOM POI via cross-partner `phaseEndpoints` (flagged in the prior spec) still to clear at reseal.

## 6. Economics (Grok lane)
Thuwal within-cluster corridors are **net-new** — no finance-model seed. Tasklet has authored honest pending (`economics_status: economics_pending`, null route economics). Grok mints corridor economics post-seal. The network TAM/SAM/SOM `growth_case` ladder is unchanged (still Grok-owned). Deck appendix carries three conservative marquee unit-economics examples (The Red Sea, AMAALA, Thuwal) at $1M CAPEX / 15 trips-day / reduced fares — see deck.

## 7. Seal gates
Dedupe at seal (defensive Set dedupes retained), cluster_id sync, seal-integrity (expect new city/priority_city features for AMAALA + Thuwal). AMAALA/Thuwal city-feature promotion warnings expected — Grok promotes.

## Files changed (Tasklet, this commit)
- `partner-pitch/partners/red-sea-global.json` — phases[3]→Thuwal, journeys_unlocked, hero, context, objections, end_state, wow_corridors; `_thuwal_repoint` tag.
- `data-clean/partners/red-sea-global.json` — same.
- `data-clean/STORIES.json` — RSG story narrative[1] Jeddah→Thuwal; scope_city_ids updated.
