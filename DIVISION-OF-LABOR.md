# Navier Atlas — Tasklet × Claude Code: Division of Labor & Deploy Protocol
_v4 · 2026-05-30 · **build + index.html move fully to Claude Code (data/render split)**_

> **What changed in v4 (read this first):** `index.html` is now **Claude-owned, data-free render**.
> The data ships as a **separate asset, `atlas-data.js`**, built by `scripts/build.mjs` from
> `data-clean/` and loaded via `<script src>`. There is now exactly **one generator of each file**:
> Claude owns `index.html` + the build; Tasklet delivers **data only** into `data-clean/` (sealed
> blobs + pitch JSON) and **never emits `index.html`**. This permanently ends the regression where
> Tasklet's `build.py` regenerated `index.html` and wiped Claude's render. See §1.2 and §2.
>
> **What changed in v3:** Claude Code owns **publish-to-Vercel**. Tasklet no longer runs a full
> build + deploy on every render push (the credit sink). Tasklet hands Claude a **sealed, pre-gated
> data bundle** and Claude deploys it after a cheap pre-flight. Security is preserved because the
> expensive gates run ONCE on data change, and the sealed bundle is safe by construction.

## Principle
**Tasklet owns the GRAPH + the SEAL. Claude Code owns the EYES + the DEPLOY.**
Tasklet produces a clean, classified, demand-weighted, land-validated route graph, runs the
security gates, and seals the result. Claude consumes the sealed bundle, makes it beautiful, and
publishes it. Neither side infers the other's half.

---

## 1 · Who owns what (v3)

### TASKLET — data spine · routing · demand · security gates · sealing · research
1. **Source of truth**: `.md` city files + all research/enrichment/outreach (internal tree, never in git).
2. **The route graph**: BP-graph routing, canonical node ids, layered trunk/regional/local, every edge
   sea-routed + land-validated.
3. **Demand model**: `traffic_weight` + `trip_purpose` calibrated to observed flows.
4. **Security gates (run ONCE per data change)**: partition → externalization gate → land-crossing gate →
   **BP-on-water gate** → **seal**. Tasklet publishes `data-clean/` + `SEAL.json` to `main`.
5. **Data delivery (v4)**: write the 4 sealed blobs (`FEATURES_BY_TYPE/ROUTES/STORIES/VESSEL_SPECS.json`)
   into `data-clean/`, and the **pitch content** as per-record JSON under
   `partner-pitch/city_briefs/<city_id>.json` and `partner-pitch/partners/<partner_id>.json`
   (the tree Tasklet already authors in). **Tasklet never emits `index.html`** and never inlines data
   into it. Claude's `build.mjs` reads both trees → `atlas-data.js`; Claude builds + deploys.
6. **Backstop**: a lightweight daily substring sweep on the live URL (cheap; pings Slack only on a hit).

Tasklet **no longer** runs `build_safe.sh` + Vercel CLI on every Claude push, and **no longer
generates `index.html`**. It runs the gates only when DATA changes, then seals + writes `data-clean/`.

### CLAUDE CODE — render layer · interaction · build · **deploy**
1. **Render** (unchanged scope): density visuals from `traffic_weight`, zoom-band reveal, `trip_purpose`
   colour, hub hierarchy from `degree`, curve smoothing clamped to corridor, chrome/legend/filters, partner views.
   `index.html` is Claude's render template — **data-free**; it reads `window.*` globals + the pitch render.
2. **Build (v4)**: `scripts/build.mjs` reads `data-clean/` (sealed blobs) + `partner-pitch/` (pitch)
   and emits **`atlas-data.js`** (a static asset setting
   `window.FEATURES_BY_TYPE/ROUTES/STORIES/VESSEL_SPECS/CITY_BRIEFS/PARTNERS`). `index.html` loads it
   via `<script src="atlas-data.js">`. `atlas-data.js` is a **gitignored build artifact** — built at
   deploy by `deploy.sh` and gate-scanned by §3.2 before it ships. Single generator per file ⇒ no clobber.
3. **Deploy**: publish `index.html` + **`atlas-data.js`** + `vercel.json` to `navier-atlas.vercel.app`
   via `scripts/deploy.sh` after the pre-flight below (`.vercelignore` allowlists the three files).
4. Claude **never** edits the graph, demand weights, or partition; it ships ONLY `data-clean/` data.

---

## 2 · The sealed-bundle contract (`data-clean/SEAL.json`)

When Tasklet's data changes, it writes:
```
data-clean/   FEATURES_BY_TYPE.json  ROUTES.json  STORIES.json  VESSEL_SPECS.json  SEAL.json  (sealed blobs)
partner-pitch/ city_briefs/<city_id>.json   partners/<partner_id>.json                       (pitch, per-record)
```
The 4 blobs are sealed (hashed in `SEAL.json`). Pitch content is narrative, not sealed, but is still
leak-scanned (§3.2) on every deploy. Claude's `scripts/build.mjs` concatenates all of it into the
deployed `atlas-data.js`; **Tasklet does not build or touch `index.html`/`atlas-data.js`** — it only
writes these source files.
`SEAL.json` shape:
```jsonc
{
  "sealed_at": "2026-05-30T…Z",
  "schema": "navier-atlas/seal/v1",
  "gates": {
    "externalization": "PASS — 0 exclusion hits",
    "land_crossing":   "PASS — 0/1354",
    "bp_on_water":     "PASS — 0 inland boarding points"
  },
  "blobs": {
    "FEATURES_BY_TYPE": { "sha256": "…", "count": {"city": …, "priority_city": 13, "poi": …} },
    "ROUTES":           { "sha256": "…", "count": 1354 },
    "STORIES":          { "sha256": "…", "count": … },
    "VESSEL_SPECS":     { "sha256": "…", "count": … }
  }
}
```
The `sha256` is over **canonical JSON** (`sort_keys=True, separators=(",",":")`). Reproduce with
`json.dumps(obj, sort_keys=True, separators=(",",":"))` then sha256.

**Why this is safe to deploy without re-gating:** every blob in `data-clean/` already passed
externalization (no Sampriti/investor/deal-term/internal fields — those live only in Tasklet's
internal tree and `humans.json`, which never enter git). Routes already passed the land gate. BPs
already passed the on-water gate. There is nothing left to leak.

---

## 3 · Claude Code's deploy pre-flight (cheap — seconds, no A*/no land gate)

Before every `vercel deploy`, Claude runs **all three**:

1. **§3.1 Seal hash match (anti-tamper).** Recompute the sha256 of each `data-clean/` blob and compare
   to `SEAL.json`. In **prod (`--release` / `RELEASE=1 ./scripts/deploy.sh`) any mismatch → ABORT**.
   In **dev it is advisory** (a stale seal — Tasklet's to refresh — must not block render iteration;
   Claude never edits the sealed blobs, and `build.mjs` derives `atlas-data.js` from them).
2. **§3.2 Substring externalization grep.** Grep the **full deployable surface** — `index.html` **and
   `atlas-data.js`** (where the data now lives) — for the `docs/EXCLUSION-TOKENS.txt` patterns.
   **Any hit → ABORT.** Catches leaks in either the render template or the data asset.
3. **§3.3 MapLibre style smoke test.** Eval `atlas-data.js` to set the window globals, then run the
   page's layer code headless and assert: (a) zero layers rejected by style validation, (b) the route
   line layers (`route-glow*`, `route-p2`, `route-qlr`) are present and bound to the `routes` source.
   Prevents the F-01 class (route layers silently dropped by an invalid expression).
4. **§3.4 Pitch-render presence.** If pitch content is shipped (`atlas-data.js` sets `CITY_BRIEFS`/
   `PARTNERS`) but the render that consumes it is missing from `index.html` (`CITY_BRIEFS[` read,
   `applyPhaseFocus`/`_renderCarousel`/`showPhase`, `_routeLabel`), **ABORT** — guards against a build
   regen shipping data with a dead UI.

If all checks pass → `vercel deploy --prod`. Then post a one-line deploy notice to `#tasklet-jaideep`.

> Tasklet's heavy gates (partition, land-crossing A*, BP-on-water) do **not** run here — they already
> ran at seal time and their verdicts are recorded in `SEAL.json`. Land-crossing cannot regress from a
> render-only change because route geometry is frozen in the sealed bundle.

**Deploy credentials:** Claude Code needs only the **Vercel token** in its environment
(`VERCEL_TOKEN`). The basemap is CARTO (public, token-free), so no map-tile secret is exposed. The
Vercel token must NOT be committed to git.

---

## 4 · Git flow (v3)
```
main          ← released state; mirrors live.
 ├─ tasklet/data   ← Tasklet pushes refreshed data-clean/ + SEAL.json on data change
 └─ claude/render  ← Claude pushes render template + builds + DEPLOYS, then merges to main
```
1. **Tasklet → `main`**: on data change, run gates → `seal_bundle.py` → commit `data-clean/` + `SEAL.json`
   (+ refreshed `docs/EXCLUSION-TOKENS.txt` if the exclusion list changed). Post to Slack: "data sealed, vN".
2. **Claude → deploy → `main`**: branch from `main`, edit render template, build against `data-clean/`,
   run the §3 pre-flight, `vercel deploy --prod`, then fast-forward `main` and commit the built `index.html`.
3. **No Tasklet build-on-push trigger.** The old `githubWebhook` auto-build trigger is **retired** — it was
   the credit sink. Tasklet's only post-deploy role is the daily backstop sweep (§1.5).

### Hard rules (v3)
- Claude ships ONLY sealed `data-clean/` data; never invents/edits data; never touches partition.
- The §3 pre-flight is mandatory before every prod deploy; a failing pre-flight blocks the deploy.
- Internal data never enters git (see `.gitignore`).
- If Claude needs a *new* data field, it requests it via PR comment / `HANDOFF`; Tasklet adds it to the
  render contract (§2 of v2 doc) and re-seals. Claude never fabricates graph data to fill a gap.

---

## 5 · Data issues handed to Tasklet from the QA report (Tasklet-owned)
- **F-03 inland boarding points** (Dubai ferry terminal in the street grid; Abu Dhabi hotel jetty at
  Khalifa City; Phuket ferry triangle near Thalang). Root cause = stored lng/lat is inland. Fix =
  Tasklet's new **BP-on-water gate** (snap-or-drop any boarding point not within Nm of navigable water);
  re-seal. Status: auditor built; triage + fix in flight.
- **F-11 route count varies across reloads (874→923)** — implies client-side route generation.
  Resolution: ROUTES are **fully baked & deterministic** in the sealed bundle; Claude must remove any
  client-side route synthesis and render the baked `ROUTES` array verbatim. Count comes from `SEAL.json`.

(Everything else in the QA report — F-01, F-02, F-04/05/06/07/08/09/10/12/13 — is `[RENDER]`, Claude Code's.)

---

## 6 · Acceptance bar (unchanged, marquee markets first)
Singapore · Dubai · Abu Dhabi · Bali · Phuket:
- [x] 0 land-crossings · [x] no raw-label endpoints · [x] cross-border story legible
- [ ] **route lines actually render** (F-01 — Claude, gated by §3.3 smoke test going forward)
- [ ] visible trunk/regional/local density hierarchy (Claude)
- [ ] all boarding points on water (Tasklet BP-on-water gate)
