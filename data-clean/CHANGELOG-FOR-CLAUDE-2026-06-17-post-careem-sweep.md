# Gold #79ag — Post-Careem queue sweep (E + F + G1 + G2 + G3)

**Date:** 2026-06-17
**Scope:** sidecar / model-link wiring on partner JSONs (E); Careem Phase 4 GCC cross-border on Quanta-LR (F); featured_routes `route_ids[]` singleton-dup collapse across all 6 sidecar-built partners (G1); UAE `traffic_weight` showcase + spiderweb seeding on `ROUTES.json` (G2); duplicate-feature dedup audit on `ROUTES.json` (G3).
**Geometry change:** none (G2 is a `properties.traffic_weight` patch on existing UAE features; G3 reported 0 duplicates — gold already clean from prior LB-201/LB-202 dedup). G3 is therefore a verify-only no-op this bite.

## E — sidecar_url + model_link
- Added `sidecar_url` (top-level) on all 6 sidecar-built partners (careem, grab, qatar, red-sea-global, jih-global, saudi-pif) pointing to #79af gold zip Drive copy (file id `16NDtKcL77JyqWUdNt5jxYgPV3RVrtgS2` — sidecar `economics_by_route_id.json` lives inside `data-clean/`). Pinned to the #79af snapshot, not rolled forward; the URL is intentionally a stable historical pin.
- Added per-corridor `model_link` on every `featured_routes[*]` entry across the 6 partners (136 entries total: careem 11, grab 91, qatar 8, red-sea-global 12, jih-global 6, saudi-pif 8). Each `model_link` resolves to the partner's transparent sheet from `finance/PARTNER-SHEET-IDS.json` (LB-83 registry). Plain `edit#gid=0` link — anchored to corridor row not yet supported (sheet `gid` per-corridor not registered).
- FP (French Polynesia) partner JSON not present in tree; skipped per "leave a TODO marker" guardrail — when the FP partner JSON is materialised the same shape applies and the sidecar TODO marker (`_sidecar_todo`) should flip to a populated `sidecar_url` once FP records land in `economics_by_route_id.json`.

## F — Careem Phase 4 GCC cross-border (Quanta-LR aspirational)
- `partner-pitch/partners/careem.json` `phases[3]` (n=4) appended: `Phase 4 — GCC cross-border (Quanta-LR)` with three aspirational/amber-dashed featured routes — Dubai/AD↔Manama (~265nm), AD/Dubai↔Doha (~210nm), Dibba/Fujairah↔Khasab (~80nm), all on Quanta-LR, H2 2026+. Phase carries `aspirational: true`, `render_style: amber_dashed`, `vessel_class: Quanta-LR Hybrid`, `boats: null` (held out of grounded numbers — LB-201 amber-dashed convention).
- `route_id: null` on the three featured entries (no `rn-` pins yet; LB-202 noted Doha + Manama corridor ids exist in corridors aggregate but not yet present as `properties.id` keys in ROUTES.json — pending future mint).

## G1 — featured_routes `route_ids[]` singleton-dup collapse
- Pattern: each featured_route had identical id in both `route_id` (singular) and `route_ids[]` (array) — array carried a single element equal to the scalar id. Dropped the redundant `route_ids[]` field on collapse; multi-leg arrays retained where `route_ids[]` carried distinct leg ids.
- Collapsed counts (across 6 sidecar-built partners): careem 3, grab 80, qatar 7, red-sea-global 4, jih-global 2, saudi-pif 3 → **99 singleton-dup `route_ids[]` arrays dropped**. Remaining `route_ids[]` arrays: 4 (3 grab multi-leg + 1 jih multi-leg, all distinct-leg arrays, retained).

## G2 — UAE `traffic_weight` showcase + spiderweb
- 294 UAE-tagged routes (`from_city_id` or `to_city_id` ending in `-uae`).
- Showcase corridors (8 pinned by `properties.id`):
  - 0.85 — `rn-42aa1791bb60` (Dubai Harbour → Palm Marina West); `rn-a5ac4f587aee` (Dubai Harbour → Marina Mall / Breakwater = DXB↔AUH trunk)
  - 0.75 — `rn-dd4500aa99f5` (Wynn Al Marjan); `rn-12f09bd4d4d6` (Côte d'Azur / Heart of Europe); `rn-c2a5e2033f94` (Yas Marina → Saadiyat Beach Club)
  - 0.65 — `rn-01b4a3efaf0f` (Dubai Harbour → Al Khan Lagoon / Sharjah); `rn-355d8ba3c15a` (Dubai Creek Marina → Al Seef); `rn-aef40f1a50bb` (Marina Mall/Breakwater → Al Bateen)
- Spiderweb seeding: 20 UAE routes with `traffic_weight == None` set to 0.15. 266 already-curated UAE weights kept untouched (LB-192a / null-beats-wrong).
- **Note (provenance carry):** the showcase rn-ids live as `properties.id` (not `properties.route_id`) in ROUTES.json — `route_id` is null on these UAE routes. Codified below.

## G3 — duplicate-feature audit
- Group-by `properties.id` over all 5,198 routes: **0 duplicate groups, 0 extras to remove**. Gold is already clean (LB-201 ics-dedup carry-forward).
- Idempotent guard preserved (`keep longest geometry on N>1` logic) but no rows mutated.

## Anti-regression
- ROUTES.json: count stable 5,198 → 5,198 (G3 zero-removed); UAE route count stable at 294; **geometry coordinates byte-identical** on all 294 UAE routes — G2 patches only `properties.traffic_weight`.
- Sidecar `economics_by_route_id.json`: **byte-identical to #79af** (no econ change; carried forward — records 78/99 unchanged, pending unchanged).
- Partner JSONs: 6 changed (careem grab qatar red-sea-global jih-global saudi-pif) — schema-additive (sidecar_url + per-corridor model_link + careem.phases[3]) + dedup (route_ids[] collapse). No econ values touched.

## Counters into SEAL meta
- `meta.gold` → `79ag`
- file_hashes: ROUTES.json sha changes (traffic_weight patch); 6 partners/{x}.json sha changes; this CHANGELOG added → file_hashes count 30 → 31.
- blobs.ROUTES.sha256 recomputes on actual bytes (LB-171); blobs.FEATURES_BY_TYPE / CLUSTERS sha256 byte-identical to #79af.
- sidecars.economics_by_route_id.json.sha256 byte-identical to #79af.

## Loop-breakers introduced (banked in OPS-LOOP-LEDGER.md)
- **LB-203** — Showcase corridor IDs live under `properties.id`, not `properties.route_id`, on UAE corridors. `route_id` is null for many corridors that exist in the aggregate as `rn-…` ids; the aggregate-side `rn-…` id is mirrored into `properties.id` in ROUTES.json. Lookup for any "corridor id → route feature" join MUST try `properties.id` first.
- **LB-204** — Partner-pitch JSON sidecar/model wiring: `sidecar_url` (top-level, one Drive zip file per gold rev) + per-featured-route `model_link` (one transparent-sheet URL per partner) is the codified shape. Multi-leg `route_ids[]` retains only distinct leg ids; singleton `[rid]` arrays MUST be dropped (covered by G1 sweep).
- **LB-205** — Local `partner-pitch/partners/*.json.bak-*` swarm consumes FUSE quota; the pattern is to delete bak* files before any in-tree patch sweep (only-newest equivalent for partner sources, mirrors LB-181 for zips).
