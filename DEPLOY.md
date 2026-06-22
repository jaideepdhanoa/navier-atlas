# Deploying Navier Atlas (v5 — multi-page)

Single command, from the repo root:

```bash
VERCEL_TOKEN=<token> ./scripts/deploy.sh
```

`deploy.sh` does everything: builds the data asset (`build.mjs`), assembles the full site tree
(`build-site.mjs`), runs the §3 pre-flight (seal · leak-grep · MapLibre smoke · render-presence),
carries the Vercel project link into `_dist/`, and deploys `_dist/` to prod. It aborts if pre-flight fails.

> **Pull `main` first.** The deployable is built from `data-clean/` (Tasklet's sealed surface) + the
> render in `index.html`; both live on `main`.

---

## What the deploy is (changed in v5 — read this)

1. **It's a directory tree, not a single file.** The deploy publishes the **`_dist/` directory**:
   ```
   _dist/index.html          aggregate render (all partners; internal)
   _dist/atlas-data.js       full data (~4 MB)
   _dist/vercel.json
   _dist/<slug>/index.html   per-partner page  (render + __PARTNER_BUILD__ lock)
   _dist/<slug>/atlas-data.js per-partner data, SCOPED to that partner only
   _dist/partners/index.html  internal directory (password-protected; links to proposals + sheets)
   ```
   Do **not** hand-copy `index.html`, and do **not** use `tasklet-build/dev.sh` — it only copies
   `index.html` + `vercel.json`, which would ship a blank page (no data) and none of the partner pages.
   Use `scripts/deploy.sh`.

2. **`atlas-data.js` is a built, git-ignored artifact** — it is not committed. The build generates it
   from `data-clean/` (the public-stripped, sealed surface — never `partner-pitch/`). That's why you
   must run the build (or `deploy.sh`); deploying the repo as-is would have no data.

3. **Partner pages are path-based and isolated.** Each partner deploys at `/<slug>` containing **only
   its own data** (cities/POIs/routes/own story + only that partner) behind a render lock that ignores
   `?partner=` overrides. Per-build exclusion-token grep + cross-partner sweep abort on any leak.
   The aggregate (all partners, internal) stays at `/`.

   Current partner pages:
   `/grab` · `/careem` · `/uber` · `/dubai-rta` · `/abu-dhabi-itc` · `/qatar` · `/saudi-pif` ·
   `/red-sea-global` · `/singapore-mpa` · `/hawaii`
   (New partners appear automatically — `build-site.mjs` emits one page per `data-clean/partners/*.json`.)

4. **Internal partner directory at `/partners`.** Password-protected index listing every partner with
   links to proposal pages (`/<slug>`) and unit-economics Google Sheets (when available). Deck status
   is shown as "in progress" but not linked until iterations are complete. Set `PARTNERS_HUB_PASSWORD`
   (+ `AUTH_SECRET` for session cookies) in Vercel Production env.

---

## Requirements

- **`VERCEL_TOKEN`** in the environment (never commit it).
- The repo's **`.vercel/` link** (or `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` env vars) must point at the
  existing **navier-atlas** project, so the deploy lands there and does not create a new project.
  `deploy.sh` copies `.vercel/project.json` into `_dist/` for you (after the build wipes `_dist/`).
- Node (for the build scripts) + first-run installs pre-flight deps into `scripts/preflight/node_modules`.

## Dev vs release

- **Default (dev):** a stale `data-clean/SEAL.json` is **advisory** — it does not block the deploy
  (per `DEPLOY-PROTOCOL.md`; the seal refreshes on Tasklet's weekly release).
- **Prod cut:** `RELEASE=1 VERCEL_TOKEN=… ./scripts/deploy.sh` — pre-flight then **enforces** the seal
  hash (§3.1). Only use when the seal is fresh.

## Manual fallback (no deploy.sh)

```bash
node scripts/build.mjs && node scripts/build-site.mjs   # builds _dist/
node scripts/preflight/preflight.mjs .                  # must print: PRE-FLIGHT PASSED
cp -r .vercel _dist/ 2>/dev/null                         # carry the project link into _dist
cd _dist && vercel deploy --prod --yes --token <token>   # deploy the _dist DIRECTORY
```

## After deploy — 30-second smoke

- `/` loads the aggregate (stats ≈ 84 cities / 1,567 routes) with **region chips** next to Global.
- **Region → city drill-down:** click a region chip (e.g. **MENA**) → the row swaps to that region's
  marquee cities (Abu Dhabi · Doha · Dubai · Jeddah · Muscat) with a **‹ MENA** back chip; click a city
  (Dubai) → it flies there and opens its brief; the back chip / **Global** return to the region row.
- **Partner guided tour:** `/grab` opens a **large dialogue** (hero + "Your world"), then "Take the
  tour →" lands on **Chapter 1 "The network"** with a clear **Step X of N** stepper — a progress bar
  and an explicit **"Next · ‹title› →"** button (plus dots) so it reads as a walkthrough; stepping
  flies the camera per phase; **"About ▾"** reopens the dialogue.
- **End-state shows the FULL regional network:** Chapter 1 (and the close) render the whole network the
  partner could run — `/grab` = the full **Southeast Asia** network (~28 cities / ~650 routes), with the
  caption "your rollout lights up N of M markets". The per-phase chapters then highlight subsets.
- **Isolation (pitch, not the base map):** a partner page contains **only that partner's PITCH** —
  `PARTNERS` = just the slug, only its own story, overlays stripped — verified by the `__PARTNER_BUILD__`
  lock and the cross-partner sweep. `/grab?partner=uber` must **stay Grab**. (The *map* deliberately spans
  the partner's whole region now — that's the public atlas, not partner-private; route counts are
  regional, no longer ~360.)
- Cold load shows the **"Charting the network…"** overlay, not a blank map.

---

## How it fits together (ownership)

- **Tasklet** delivers DATA: the 4 sealed blobs + `SEAL.json` in `data-clean/`, and the public-stripped
  pitch in `data-clean/{city_briefs,partners}/`. Tasklet never emits `index.html`.
- **Claude** owns `index.html` (the render), the build (`build.mjs` → `atlas-data.js`,
  `build-site.mjs` → the `_dist/` tree), and deploy.

See `DIVISION-OF-LABOR.md` (v4/v5) for the full contract and `scripts/preflight/` for the gate details.
