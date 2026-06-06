# Deploy-size dedup plan — shared geography + per-page pitch

**Status:** planned (not started). Tracked item from the 2026-06-05 size investigation.
**Owner:** Claude (build + render lane).

## Problem
The deploy tree (`_dist/`) reached **~261 MB** and the Vercel upload started hitting transient
API failures (`upstream connect error` → `FetchError: invalid json response body`). A retry/backoff
loop now lives in `scripts/deploy.sh` as the immediate mitigation, but the size keeps growing with
every data drop.

## Diagnosis (measured 2026-06-05, HEAD 5913a81)
- 145 pages, 145 `atlas-data.js` files = **231 MB of data** (HTML adds ~28 MB).
- **4.5× feature duplication**: 52,196 features shipped across all files vs **11,548 unique**.
- Gzipping all data together: 231 MB → **52 MB**; true unique content ≈ **20 MB**.
- Per-page byte anatomy (`/grab` example): ROUTES 2.2 MB + FEATURES 1.3 MB = **~90% public map
  geometry**; PARTNERS 0.14 MB + CITY_BRIEFS 0.12 MB + STORIES 0.01 MB = **~10% pitch**.

The duplicated bulk is the **public route/city/POI geometry** (`ROUTES`, `FEATURES_BY_TYPE`,
`VESSEL_SPECS`), copied into every page. The partner-confidential content (`PARTNERS`, `STORIES`,
scoped `CITY_BRIEFS`) is tiny.

## Isolation constraint (confirmed with Jaideep, 2026-06-05)
The reason pages are self-contained today: **don't expose other partners' proposals/content**, and
keep page load fast. The confidential surface is the **pitch** (`PARTNERS`/`STORIES`/briefs) — *not*
the route/city geometry. So geometry may be shared; pitch must stay per-page.

## Proposed change
Split each page's data into two files:
1. **`atlas-geo.js`** — `ROUTES` + `FEATURES_BY_TYPE` + `VESSEL_SPECS`. **One copy at root**, loaded
   by every page. Carries **zero** partner proposal content, so sharing it leaks nothing
   confidential. ~17 MB (gz ~5 MB), browser-cached across navigation.
2. **`atlas-pitch.js`** — `PARTNERS` + scoped `CITY_BRIEFS` + `STORIES`, **per page**, kept behind
   the existing `__PARTNER_BUILD__` / `__PARTNER_MARKET__` lock + cross-partner sweep. ~0.2–0.3 MB.

Result: ~210 MB of duplicated geometry → one ~17 MB file. **`_dist/` ~261 MB → ~80 MB.**

### Open trade-off to decide at implementation
Today per-partner geometry is **regionally scoped** (`/grab` = SEA's ~1,183 routes, not the global
5,150). A single shared geo blob would put the **full** global geometry in every page's browser.
Geometry isn't proposal content, so this doesn't expose pitches — but it does (a) make a single-page
first load heavier (~5 MB gz vs ~1 MB gz today, offset by cross-page caching) and (b) let any partner
inspect the whole network's routes client-side. If (b) is unwanted, keep **per-region** geo blobs
(e.g. `geo/sea.js`, `geo/mena.js`) instead of one global — still collapses ~145 copies down to
~6–8 regional ones, and pages load only their region. Recommend per-region blobs as the safer default.

## Scope of work
- `scripts/build.mjs` / `build-site.mjs`: emit split blobs (+ region grouping if chosen); keep the
  leak grep + cross-partner sweep on the **pitch** blob only (geo is public).
- `index.html`: load `atlas-geo*.js` + `atlas-pitch.js`; assemble `FEATURES_BY_TYPE` from both.
- `scripts/preflight/`: update the seal/leak gates for the new file layout; assert pitch isolation
  per page still holds (no foreign `partner_id` in a page's pitch blob).
- Verify e2e (4/4) + per-partner isolation lock still pass.

## Also worth considering (separate, smaller win)
The 145 near-identical `index.html` copies = ~28 MB. Externalizing the render to a shared bundle +
tiny per-page config/lock would cut that to ~1 MB. Independent of the data split.
