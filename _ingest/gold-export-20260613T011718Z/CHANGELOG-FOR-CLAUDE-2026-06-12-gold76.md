# Gold #76 — overlay seal (2026-06-12)

Small carry-forward overlay over Gold #75. **No new geometry. No new routes. No edge-mints.** Route count unchanged at 5,283; cluster count 75.

## What changed in the zip

1. **`data-clean/CLUSTERS.json`** — 7 stray `bp-*` (boarding-point POI) ids stripped from `member_city_ids` arrays. These were never valid city/priority_city nodes and were causing the render to silently drop those endpoints. Affected clusters:
   - `oman` (1 stray)
   - `philippines` (5 strays)
   - `uae` (1 stray)
   `member_city_ids` is now 100% resolvable against `FEATURES_BY_TYPE.{city,priority_city}` (gate_city_ids PASS — 191 valid nodes, 5283 routes, 75 clusters).

2. **`data-clean/partners/grab.json`** — 1 high-confidence FR `route_id` binding applied:
   - **Cebu ↔ Boracay** (phase `ph1`, FR0) → `rn-32233df7de6e`.

3. **`data-clean/economics_by_route_id.json`** — rebuilt sidecar. Counts: 103 records route-pinned (was 98 in #75); 36 pending (no gold route); by partner — careem:14, grab:37, jih-global:43, qatar:3, red-sea-global:2, saudi-redsea-pif:4; grounded:73, estimated:23.

4. **`data-clean/SEAL.json`** — `meta.gold` bumped to `#76`; `sealed_at` refreshed; CLUSTERS sha + sidecar sha+count updated; `pitch.note` extended; `meta.notes` extended; `pitch.economics_records` → 103.

## Out-of-zip patches (applied to source tree; NOT included in the ship zip — call out for downstream tools)

- **`finance/model/corridors.json`** — 15 ics-* corridor `route_id`s nulled and `aspirational: true` set (per LB-117) across:
  - Singapore Marina↔Sentosa (1)
  - Philippines (6)
  - Taiwan-Penghu (3)
  - Langkawi (5)
- **`finance/build_economics_sidecar.py`** (LB-152) — now accepts both `agg-{partner}.json` and `{partner}-aggregate.json` naming conventions; alias map handles `saudi-redsea → saudi-redsea-pif`.
- **`atlas-external/datastore_audit.py`** (LB-152) — accepts flat `SEAL.FEATURES_BY_TYPE` shape (`city`/`poi` at top level) in addition to the nested `.count` shape. Eliminates a spurious ship-FEATURES-vs-SEAL FAIL.

## Gates

- `gate_city_ids.py`: **PASS** (0 unresolved).
- `gate_endpoint_labels.py`: **0 HARD FLAGS** (12 WEAK single-token binds accepted; 108 OK, 43 NULL_OK, 1 OK_NO_DISTINCTIVE).

## Carry-forward
Prior changelogs (#74 rationale-leak, #75) preserved alongside this one at zip root.
