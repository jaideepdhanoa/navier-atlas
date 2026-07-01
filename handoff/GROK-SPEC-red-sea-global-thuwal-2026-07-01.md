# GROK SPEC — Red Sea Global: Thuwal repoint + three-destination connectivity (2026-07-01)

**Supersedes the Jeddah-gateway scope in `GROK-SPEC-red-sea-global-ksa-repoint-2026-07-01.md`.**
Jaideep directive (2026-07-01): RSG scope = **The Red Sea + AMAALA + Thuwal** (RSG's own three portfolio destinations, per https://redseaglobal.com/en/portfolio/). **Jeddah is dropped as an RSG destination.** Cover **within-cluster** and **between-cluster** connectivity for all three — in the map, phases, and corridor unit economics.

Tasklet lane is complete for the proposal/data layer (this commit). The items below are **Grok's seal lane**. Rules in force: **ID-based matching only · null-beats-confidently-wrong · broad-footprint-first, exact-bind-second · hand-waypoints, no land crossings.**

Machine-readable seeds already live in the partner JSON at `phases[].featured_routes[]` (6 corridors, all `route_id: null`, `_link_status: "geometry_seal_pending"`, `_link_source: "tasklet/thuwal_repoint_2026-07-01"`). These are the corridors to seal. **There is no `wow_corridors` key** — do not look for one; the corridors are in `phases[].featured_routes`.

---

## 1. Node promotion + re-parenting (map render) — REQUIRED
Three destinations must render as three first-class nodes. Today only `red-sea-global-ksa` is a `city` feature; the other two exist mainly as POI `parent_city_id` values.

| Node id | Action | Anchor coord | Rendered label |
|---|---|---|---|
| `red-sea-global-ksa` | keep as `city`; **rename** to "The Red Sea" (currently "Red Sea Global (RSG + AMAALA)") | [36.93, 25.46] | The Red Sea |
| `amaala-triple-bay-ksa` | promote to `priority_city` **and re-parent the AMAALA branded BPs onto it** (see §2B) | resolve coord conflict in §3 first | AMAALA (Triple Bay) |
| `thuwal-private-retreat-ksa` | promote to `priority_city` **and re-parent the Thuwal/KAUST BPs onto it** (see §2C) | [39.0972, 22.305] | Thuwal (Private Retreat) |

`the-red-sea-archipelago-ksa` is a POI-parent (Sheybarah / Shura / Ummahat jetties). Fold it into `red-sea-global-ksa` (or keep as an explicit sub-anchor) — **do not leave a duplicate un-rendered parent.**

## 2. Boarding-point reconciliation — canonical inventory
**Two BP families exist and partially duplicate each other:**
- **`bp-<hash>` family** — the rich branded-jetty set, parented to `red-sea-global-ksa` (and `jeddah-ksa` for KAUST). **This is CANONICAL** — the sealed 102-edge mesh references it ~196× vs ~28× for the other.
- **`bp-w8-*` family** — a coarse seed set under the new parent nodes. Mostly duplicates of the above at **different coords (15–30 km off)**, BUT contains a few **unique** landmarks with no hash equivalent.

**Reconcile per-landmark (do NOT blanket-delete a family):** where a landmark exists in both families, **keep the `bp-<hash>` one, retire the `bp-w8-*` duplicate** (null-beats-wrong on the divergent coord). Where a landmark exists **only** as `bp-w8-*`, **keep it and re-parent** to the correct node.

### 2A · The Red Sea (parent `red-sea-global-ksa`)
Canonical hub + resort jetties (all `bp-<hash>`, keep):
- Shura Island Marina `bp-b80009b8a5` [36.966842, 25.491622] — hub
- Shura branded jetties: Edition `bp-e31b9984c3`, Fairmont `bp-dd8607b0ac`, Raffles `bp-cf8ed6bee4`, Rosewood `bp-55ccfd6065`, SLS `bp-96488c9461`, Grand Hyatt `bp-c9c8827d4b`, Jumeirah `bp-77b411c5c3`, Miraval `bp-5aac2fcfdb`, Faena `bp-017b883387`, Four Seasons Shura `bp-c2ba9e85d8`, Coral Bloom pontoon `bp-732d6f088b`
- Nujuma, a Ritz-Carlton Reserve (Ummahat AlShaykh) `bp-234d10fa88` [36.773173, 25.524957]
- Turtle Bay ops hub `bp-917041e2d9` [36.998241, 25.502429]; Fly Red Sea seaplane base `bp-3329df646d`
- **`bp-w8-*`-ONLY (keep, reconcile coords):** Sheybarah Island Resort Jetty `bp-w8-sheybarah-jetty` [36.6486, 25.4133]; Ummahat AlShaykh Resort Jetty `bp-w8-ummahat-jetty` [36.4626, 25.5536] (cross-check against Nujuma `bp-234d10fa88` — same island cluster, likely merge/keep-both as distinct berths, not duplicate)
- **Retire (duplicate):** `bp-w8-shura-marina` [36.8264, 25.5106] (duplicate of `bp-b80009b8a5`)

### 2B · AMAALA — re-parent to `amaala-triple-bay-ksa`
These are currently mis-parented to `red-sea-global-ksa`; move them:
- AMAALA Yacht Club (Triple Bay) `bp-7760762317` [36.210726, 26.64992]
- Triple Bay Marina Village `bp-5a67c2e718` [36.216382, 26.644087]
- Four Seasons AMAALA `bp-7fc32fcaf1` [36.216566, 26.64517]
- Rosewood AMAALA `bp-76496878a0` [36.232095, 26.624967]
- Six Senses AMAALA `bp-d3708a5d23` [36.229056, 26.636999]
- Yacht Club Red Sea Triple Bay `bp-7de7f6aab4`; AMAALA YC helideck `bp-5375db25ed`
- **`bp-w8-*` duplicates at ~[36.47, 26.75] (retire OR keep only if geo-resolution picks them):** `bp-w8-amaala-marina`, `bp-w8-amaala-yacht-club` — see §3.

### 2C · Thuwal — re-parent to `thuwal-private-retreat-ksa`
- KAUST Harbour & Yacht Club `bp-aafc758222` [39.099045, 22.315236] and/or KAUST Harbor `bp-1f65535380` [39.09825, 22.303309] (currently parented to `jeddah-ksa` — re-parent; keep one, retire the near-duplicate)
- **`bp-w8-*`-ONLY (keep, re-parent):** Thuwal Private Retreat Jetty `bp-w8-thuwal-jetty` [39.083299, 22.278]; KAUST Harbour `bp-w8-kaust-harbour` [39.0972, 22.305] (duplicate of the hash KAUST — retire if kept hash)

## 3. Coordinate conflicts to resolve (null-beats-wrong)
1. **AMAALA:** three coord clusters exist — hash family ~[36.21, 26.64], `bp-w8` family ~[36.47, 26.75], and a locale anchor at [36.066, 27.055]. Pick the correct real Triple Bay, bind the node + within-AMAALA routes to survivors, retire the rest. If unresolvable to a credible point, prefer null over a confidently-wrong pin.
2. **The Red Sea Shura/Ummahat:** hash vs `bp-w8` coords diverge 15–30 km. Trust the hash family (mesh-referenced) unless the `bp-w8`-only berths (Sheybarah, Ummahat jetty) are the true seaward landing.

## 4. Routes to mint (hand-waypoints, `interior_land_km==0` gate)
Seed corridors in `phases[].featured_routes` — verify against the existing mesh; don't duplicate already-sealed edges.

**Within The Red Sea** (Pioneer II):
- Shura Island Marina `bp-b80009b8a5` ↔ Ummahat / Nujuma `bp-234d10fa88` (+ `bp-w8-ummahat-jetty`) — St Regis Red Sea / Nujuma cluster, ~9.7 nm
- Shura ↔ Sheybarah `bp-w8-sheybarah-jetty` (~ resort hop)
- Shura ↔ Turtle Bay `bp-917041e2d9` — ~6 nm
- resort-island ↔ resort-island infill across the branded Shura jetties

**Within AMAALA** (Pioneer II):
- AMAALA Triple Bay Marina ↔ AMAALA Yacht Club — ~0.4 nm
- AMAALA Yacht Club ↔ Four Seasons / Six Senses / Rosewood AMAALA jetties

**Within Thuwal** (Pioneer II) — NEW:
- KAUST Harbour (`bp-aafc758222`) ↔ Thuwal Private Retreat Jetty (`bp-w8-thuwal-jetty`) — ~2 nm (marquee; today a ~45-min conventional yacht sail)
- Thuwal Private Retreat ↔ coral-archipelago anchorage — short reef hop

**Between-cluster** (Quanta-LR long-range):
- **The Red Sea (Shura) ↔ AMAALA (Triple Bay)** — ~76.6 nm coastal leg. Waypoints hug the coast / Al Wajh lagoon headlands; **no interior land crossing.** This is the featured "between" corridor.

## 5. Honest geographic constraint — DO NOT fabricate
Thuwal sits ~400 nm south of The Red Sea/AMAALA (off Jeddah, ~22.3°N vs ~25.5–26.7°N). **Do NOT mint a Thuwal↔The Red Sea or Thuwal↔AMAALA sea corridor** — it exceeds even Quanta-LR single-leg range. Thuwal's role is the **southern Jeddah-proximate gateway + private-island retreat**; movement to the northern cluster is by air (Fly Red Sea / RSI), not a Navier sea leg. Thuwal connectivity = within-cluster only. This is already reflected in `phases[3]` (scope `intra`, no north-bound leg).

## 6. Scope hygiene
- Confirm no RSG-tagged edges to `jeddah-ksa` (as an RSG destination) or `neom-*` remain in RSG scope. Sibling-partner edges (PIF/bolt/yango) that legitimately use `jeddah-ksa` are preserved — this is a scope tag question, not a delete. The Jeddah `journeys_unlocked` entry and Phase 3 are already repointed to Thuwal in the partner JSON.
- Residual Port-of-NEOM POI via cross-partner `phaseEndpoints` (flagged in the prior spec) still to clear at reseal.

## 7. Economics (Grok lane)
All 6 featured corridors carry `economics_status: "economics_pending"` + null route economics (Tasklet honest-pending). Grok mints corridor economics post-seal. The network TAM/SAM/SOM `growth_case` ladder is unchanged (Grok-owned). Deck appendix carries three conservative marquee unit-economics examples (The Red Sea, AMAALA, Thuwal) at $1M CAPEX / 15 trips-day / reduced fares — do not contradict these when minting: The Red Sea Shura→Ummahat $598,707 kept·81%; AMAALA YC→Triple Bay $642,297·82%; Thuwal KAUST→Retreat $561,018·80%.

## 8. Seal gates
Dedupe at seal (defensive Set dedupes retained), cluster_id sync, seal-integrity (expect new `priority_city` features for AMAALA + Thuwal and BP re-parenting churn). AMAALA/Thuwal promotion + re-parent warnings expected — Grok promotes.

## Files changed (Tasklet, this commit)
- `partner-pitch/partners/red-sea-global.json` — `phases[]` (3 phases, 6 `featured_routes` seeds), journeys_unlocked, hero/context/objections/end_state; `_thuwal_repoint` tag.
- `data-clean/partners/red-sea-global.json` — same.
- `data-clean/STORIES.json` — RSG story `narrative[1]` Jeddah→Thuwal; `scope_city_ids` updated to the three destinations.
