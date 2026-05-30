# Build Architecture v4 — Dev fast-path vs Weekly release gate

**Why this exists:** the full security/seal pipeline was being run on *every* build, which is
slow and expensive. It's unnecessary day-to-day because the renderer is **safe by construction**.
This splits work into a cheap default path and a heavy weekly path.

## The key safety property
`build.py` reads **only** from `output-external/` — the already-partitioned, externalized clean
data. It **never** reads the internal spine (`app/data-spine/output/*`, `humans.json`, scores,
hold-flags). Therefore a render iteration **cannot** leak internal spine data. The only new leak
surface during dev is the partner-facing pitch JSON we author by hand.

## Two modes

### `dev.sh` — default, seconds. Use 95% of the time.
```
enrich (cheap) → build (warm route cache) → grep pitch JSON only → deploy
```
- NO partition, NO full-page externalization scan, NO land gate, NO seal, NO leak sweep, NO push.
- Cheap targeted leak grep runs on `partner-pitch/**` only (the dev leak surface).
- Deploys to `navier-atlas.vercel.app` so you see changes immediately.

### `release.sh` — weekly, or before sharing the URL widely. The heavy guarantees.
```
partition → enrich → build → externalization gate → land gate → isolated dist →
deploy → live leak sweep → reseal data-clean → (then push to main)
```
- Only path that re-derives clean data from the internal spine and re-seals blobs.
- Run it on a cadence (weekly) or right before a real external share.

## Two permanent traps — now fixed in code (won't recur)
1. **vessel_specs silently empty.** `enrich` writes vessel_specs into `output-external/stories.json`,
   but a `partition` re-run regenerates that file without it. **Fix:** `build.py` now falls back to
   the frozen `partition/stories-partner-view.json`, so vessel_specs can never be empty regardless
   of build order.
2. **Poisoned route cache after a cluster split.** The cache key now also hashes
   `supplemental-nodes/edges`, `harbour-overrides`, `route-waypoints`, `label-overrides`. Any change
   that affects geometry auto-invalidates the cache — **no manual `.rn_cache.json` deletion ever needed.**

## When do I actually need release.sh?
- New cities/intel added to the internal spine (re-partition needed).
- Before announcing/sharing the live URL with an outside party.
- Weekly hygiene re-seal.
Everything else — template tweaks, route config, city briefs, partner proposals, label fixes — is `dev.sh`.
