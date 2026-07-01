# Grok spec — Kakao Mobility · Seoul–Incheon seed-node seal

Source: housekeeping PR (2026-07-01). Tasklet has minted a seed city node so the
`kakao-mobility/seoul-han-river` market stops silently skipping the site build. Grok owns the
deterministic BP/route seal against the seed. This is the established seed-node pattern
(Brisbane / Hamburg / Kochi).

---

## What Tasklet shipped (this PR)

- **New seed node** `seoul-incheon-korea` in `data-clean/FEATURES_BY_TYPE.json` → `.city[]`
  (`type: "city"`, `_seed_node: true`, `_link_status: "geometry_seal_pending"`,
  `platform_class: "dual-platform"`, coords on **Incheon Bay water** `[126.5400, 37.4500]`,
  `coords_source: "kakao_seoul_han_river_seed_2026-07-01"`, `cluster_id: "korea"`).
- This resolves the pre-existing **ghost cluster member**: the `korea` cluster already listed
  `seoul-incheon-korea` in `member_city_ids` (`members_present: 4`, `members_missing: []`) with
  no backing feature — that mismatch is what made the market's `anchor_cities` unresolvable and
  skipped the sub-page build.
- **Result:** `node scripts/build-site.mjs` now emits `/kakao-mobility/seoul-han-river`
  (`cities:1`) with **0 skipped sub-pages**. POIs = 0 (no BPs sealed yet — Grok's lane).

## What Grok owns (deterministic seal)

1. **Snap the seed to real boarding points.** Seal BPs for the market's stated piers, all
   water-adjacent, matching the `wow_corridors` in `partner-pitch/partners/kakao-mobility.json`
   → `seoul-han-river`:
   - Han River piers: **Gimpo Ara, Yeouido, Jamsil, Ttukseom, Seoul Forest**.
   - Incheon / West Sea: **Incheon terminal, Muuido, Yeongjong**.
2. **Land-mask / hand-waypoints.** The intra-Seoul Han River legs are **riverine and sit inside
   the global land-mask**. Route them with explicit hand waypoints (interior_land_km == 0 gate),
   using the `data-clean/uae_hand_waypoints.json` format precedent, so the river commute renders
   without a land crossing. Incheon Bay legs are open-water.
3. **Bind route geometry + route_ids** for the four `wow_corridors`
   (Gimpo/Yeouido↔Jamsil↔Ttukseom commute; Yeouido↔Seoul Forest/Ttukseom; Incheon↔Muuido/Yeongjong;
   Han River↔Incheon Bay connector). Range-gate by hull (all ≤ ~20 nm → Pioneer II).
4. **Reconcile the seed marker.** Once BPs/routes are sealed, drop `_seed_node`/`_link_status`
   from the node (or flip to sealed), and confirm `korea` cluster `members_present` stays truthful.

## Acceptance

- `/kakao-mobility/seoul-han-river` renders real BP markers + drawn corridors (POIs > 0, routes > 0).
- 0 land crossings on the Han River legs (post hand-waypoints).
- 0 silent BP drops; `korea` cluster integrity holds.
- Full site build stays exit 0 with 0 skipped sub-pages.
