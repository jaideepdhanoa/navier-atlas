# Grok spec — Red Sea Global · KSA re-point (kill the Maldives render)

Source: RSG partner-page fix (2026-07-01). The Red Sea Global partner page was rendering
**Maldives / Bora Bora / Seychelles** instead of KSA. Root cause: the `global_hospitality`
regional-inheritance pack (`reference_partner: four-seasons`, `mode: subset`) dropped Four Seasons
journey/route cards onto RSG and the **structured node_ids were never re-pointed** — only the prose
was customized to KSA. Tasklet has fixed the data (both trees); Grok owns the deterministic route
binding, sub-cluster node promotion, story-scope fix, and render QA.

---

## What Tasklet shipped (this PR) — `partners/red-sea-global.json` (data-clean + partner-pitch)

- **`phases[].cities`** re-pointed from `male-maldives` / `bora-bora-french-polynesia` /
  `mahe-seychelles` → real KSA nodes:
  - Phase 1: `red-sea-global-ksa`
  - Phase 2: `red-sea-global-ksa`, `amaala-triple-bay-ksa`
  - Phase 3: `red-sea-global-ksa`, `neom-sindalah-ksa`, `jeddah-ksa`
- **`phases[].featured_routes`** and **`journeys_unlocked`** rewritten with real KSA node_ids,
  labels, nm and hull. `route_id: null` + `_link_status: "geometry_seal_pending"` on every leg
  (Grok binds — see table).
- Provenance stamped in `_ksa_repoint` (supersedes `_regional_inheritance` +
  `_hospitality_flagship_bind`).
- **Verified:** `build-site.mjs` now emits `/red-sea-global` at `cities:3, pois:157, routes:46`
  with **0** `male-maldives` / `bora-bora` / `seychelles` references in the scoped `atlas-data.js`.

## What Grok owns (deterministic)

### 1. Bind the already-sealed KSA route_ids
The geometry is **already sealed** in `data-clean/ROUTES.json` — just bind the `route_id`s onto the
featured_routes / journeys (verify endpoints + nm, then apply; do not re-mint):

| Leg (label) | from → to node | nm | hull | sealed route_id |
|---|---|---|---|---|
| Shura hub ↔ Ummahat AlShaykh | `red-sea-global-ksa` (intra) | 9.7 | Pioneer II | `ics-9be0e608c8` |
| Shura hub ↔ Turtle Bay | `red-sea-global-ksa` (intra) | 6 | Pioneer II | `ics-9c3433ddf3` |
| The Red Sea ↔ AMAALA Triple Bay | `red-sea-global-ksa` → `amaala-triple-bay-ksa` | 76.6 | Quanta-LR | `rn-w8-406de2eff9` (bp-w8-amaala-marina↔bp-w8-shura-marina) |
| AMAALA Marina ↔ Yacht Club | `amaala-triple-bay-ksa` (intra) | 0.4 | Pioneer II | `rn-w8-b0bb18007b` |
| The Red Sea ↔ NEOM (Sindalah) | `red-sea-global-ksa` → `neom-sindalah-ksa` | 196.9 | Quanta-LR | `rn-623a6aa42aba` |
| The Red Sea ↔ Jeddah gateway | `red-sea-global-ksa` → `jeddah-ksa` | 275.5 | Quanta-LR | `rn-d1c5fd6a269a` |
| Jeddah gateway ↔ NEOM (Sindalah) | `jeddah-ksa` → `neom-sindalah-ksa` | 458.2 | Quanta-LR | `edge__neom-sindalah-ksa__neom-jeddah` / `rn-ef5292285601` |

Flip `_link_status` → linked, set `render` appropriately (Quanta-LR roadmap legs = `roadmap-amber-dashed`).

### 2. Promote the RSG sub-cluster nodes (so the AMAALA / archipelago / Thuwal network renders)
`amaala-triple-bay-ksa`, `the-red-sea-archipelago-ksa`, `thuwal-private-retreat-ksa` currently exist
**only as BP `parent_city_id`s**, not as city/priority_city features — so their BPs
(`bp-w8-amaala-marina`, `bp-w8-shura-marina`, `bp-w8-kaust-harbour`, `bp-w8-thuwal-jetty`, …) drop out
of RSG map scope. Seal-integrity flags `amaala-triple-bay-ksa` as a cluster member with no rendered
feature. **Promote all three to city/priority_city nodes** in the `saudi-arabia` cluster (coords on
water, `_seed_node` if you prefer), so the AMAALA/Thuwal marinas render on the RSG page.

### 3. Fix the story scope + re-derive the partner view
`data-clean/STORIES.json` still carries the old Maldives/Four-Seasons `scope_city_ids` for
`red-sea-global`. Re-derive `scope_city_ids` from the corrected `phases[].cities` (KSA only) so the
partner-view map scope matches. Confirm no `male-maldives` / `bora-bora` / `mahe-seychelles` survive
anywhere in the RSG surface.

## Acceptance

- `/red-sea-global` renders **KSA only** — Shura/The Red Sea archipelago + AMAALA + Thuwal + NEOM
  Sindalah + Jeddah; **zero** Maldives/Bora Bora/Seychelles nodes anywhere on the page or scoped data.
- All seven featured/journey legs carry sealed `route_id`s and draw (no `text_only` fallbacks).
- AMAALA/archipelago/Thuwal BPs render; seal-integrity `amaala-triple-bay-ksa` warning clears.
- Full site build exit 0.
