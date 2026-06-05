# Changelog for Claude — Build/Seal Architecture Implementation (2026-06-03)

Implements the full architecture plan from `BUILD-ARCHITECTURE-REVIEW-2026-06-03.md`.
**All Tasklet-side tooling. No deploy, no GitHub push, no index.html. The public ship surface
(data-clean/ blobs) is UNCHANGED in shape — these changes only make producing it fast & safe.**

## TL;DR for the deploy lane
- Nothing about how you consume `data-clean/` changes. Same blobs, same SEAL.json, same
  externalized `data-clean/{city_briefs,partners}/`.
- The last sealed export (`navier-export-20260603T180831Z.zip`, ROUTES 5136) remains current;
  these moves did not alter data, only the machinery.

## Recursive-learning layer (so we stop rediscovering gaps)
- **`atlas-external/BUILD-PLAYBOOK.md`** — living Symptom→Cause→Fix→Guardrail table + canonical
  run sequence. Every future failure adds a row + (ideally) a guardrail assertion.
- **`atlas-external/preflight.sh`** — blocks a build/seal unless preconditions hold: 0 competing
  procs, no stale index.html, land-mask present (warn), Python scandir==shell ls (FUSE readdir
  staleness), cache-mode sanity, arc-store presence. Run with `bash preflight.sh` (FUSE noexec).
- **`atlas-external/postflight.sh`** — GATES the seal: route floor ≥5072, 0 land-crossers,
  public-surface leak scan (HARD gate — caught the "2,000 nm" regression), SEAL.json freshness,
  blob sanity, arc-store non-empty. `bash postflight.sh`; non-zero exit == DO NOT SHIP.

## Move 1 — durable route-arc store (kills repeated A* cost + the fast-mode regression class)
- **`atlas-external/route_arc_store.py`** (new) — content-addressed cache: each sea arc keyed by
  sha1(endpoints+waypoints+routing params+version), frozen in `route-arcs/arc-store.json`.
- **`atlas-external/build.py`** — `_sea_route_arc` is now a thin caching wrapper around
  `_sea_route_arc_compute` (the old body, unchanged). Cache HIT returns instantly with NO land
  mask and NO A*. Store saved right after routing (before the slow pitch-bake tail).
- **Full-mode-only persistence (the real regression fix):** arc-store, the intra-cluster cache
  (`.icr_cluster_cache.json`) and the route-network cluster cache (`.rn_cluster_cache.json`) now
  ONLY write when `_FULL_ROUTING` (land mask present AND `BUILD_SKIP_SEA!=1`). A degraded run can
  no longer poison a cache with inferior fast-mode geometry.
- **Validated:** cold build populated 75 data-spine arcs, ROUTES 5296 (== prior full-validation);
  warm build = **100% arc hit, 0 A* runs, 0 land-mask dependency, ROUTES 5296 identical**.
- Env: `ARC_STORE_DISABLE=1` (bypass), `ARC_STORE_REBUILD=1` (ignore existing then overwrite).

## Move 2 — content-only fast pipeline (seconds instead of minutes)
- **`atlas-external/build_content.py`** (new) — reuses FROZEN geometry blobs (FEATURES_BY_TYPE,
  ROUTES) untouched; re-bakes only STORIES + VESSEL_SPECS from their static sources. Refuses to
  run if geometry blobs are absent. **Measured 4.5 s**; ROUTES.json byte-identical (mtime
  unchanged). Note: partner-proposal / city-brief edits need NO build at all — `seal_bundle.py`
  externalizes those straight from `partner-pitch/`; build_content is only for STORIES changes.
- Fast cycle: `build_content.py → seal_bundle.py --external → postflight.sh`.

## Move 3A — SQLite working store (kills FUSE per-file pain on the content you iterate on)
- **`content_store/`** (new): `schema.sql`, `db.py`, `README.md`, `navier-content.db`.
- Document store over `partner-pitch/{partners,city_briefs}/*.json`: one transactional indexed
  file; `body` holds byte-faithful source text; index columns (doc_id/category/tier/region) for
  instant queries. `import` / `export` / `verify` / `stats` / `query` commands.
- **Round-trip verify: 179 docs, 0 mismatches (byte-identical).** Export regenerates the exact
  JSON files the seal already reads → drop-in, nothing downstream changes.
- DB operated on local disk then copied to the FUSE canonical path (SQLite+FUSE locking caution).
- The JSON files remain source-of-truth; DB is a rebuildable authoring cache. Move 3B (hosted
  Postgres for BD-Studio live editing) is deferred per the plan until editing velocity needs it.

## Also fixed this pass
- **`partition/partition_spec.py`** — tightened the over-broad `\bconvener\b` exclusion to the
  strategy sense (requires royal/gate/intro/channel/access/hold adjacency). Plain descriptive
  English ("marina-resort convener", El Gouna copy) no longer trips the leak gate or the daily
  sweep. Strategy uses still caught. This pattern is shared by the partition step + seal gate +
  postflight + daily sweep.

## Files touched / added
```
atlas-external/BUILD-PLAYBOOK.md        (new)
atlas-external/preflight.sh             (new)
atlas-external/postflight.sh            (new)
atlas-external/route_arc_store.py       (new)
atlas-external/build_content.py         (new)
atlas-external/route-arcs/arc-store.json(new, generated)
atlas-external/build.py                 (edit: arc-store wrapper + full-mode cache guards)
atlas-external/partition/partition_spec.py (edit: convener pattern)
content_store/{schema.sql,db.py,README.md,navier-content.db} (new)
```
