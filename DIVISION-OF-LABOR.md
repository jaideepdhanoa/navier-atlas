# Navier Atlas — Tasklet × Claude Code: Division of Labor & Deploy Protocol
_v3 · 2026-05-30 · **deploy moves to Claude Code**_

> **What changed in v3 (read this first):** Claude Code now **owns publish-to-Vercel**.
> Tasklet no longer runs a full build + deploy on every render push (that was the credit sink).
> Instead Tasklet hands Claude a **sealed, pre-gated data bundle** and Claude deploys it directly
> after a cheap pre-flight. Security is preserved because the expensive gates run ONCE on data
> change, and the sealed bundle is **safe by construction** — it contains zero internal data.

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
   **BP-on-water gate (new)** → **seal**. Tasklet publishes `data-clean/` + `SEAL.json` to `main`.
5. **Backstop**: a lightweight daily substring sweep on the live URL (cheap; pings Slack only on a hit).

Tasklet **no longer** runs `build_safe.sh` + Vercel CLI on every Claude push. It runs the gates only
when DATA changes, then seals.

### CLAUDE CODE — render layer · interaction · build · **deploy**
1. **Render** (unchanged scope): density visuals from `traffic_weight`, zoom-band reveal, `trip_purpose`
   colour, hub hierarchy from `degree`, curve smoothing clamped to corridor, chrome/legend/filters, partner views.
2. **Build**: inject the sealed `data-clean/` blobs into the render template → bundled `index.html`.
3. **Deploy** (NEW): publish `index.html` + `vercel.json` to `navier-atlas.vercel.app` after the pre-flight below.
4. Claude **never** edits the graph, demand weights, or partition; it ships ONLY sealed `data-clean/` data.

---

## 2 · The sealed-bundle contract (`data-clean/SEAL.json`)

When Tasklet's data changes, it writes to `data-clean/`:
```
FEATURES_BY_TYPE.json   ROUTES.json   STORIES.json   VESSEL_SPECS.json   SEAL.json
```
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

1. **Hash match (anti-tamper).** For each blob actually injected into `index.html`, recompute the
   canonical sha256 and compare to `SEAL.json`. **Any mismatch → ABORT** (means data was altered
   after sealing; only Tasklet may change data).
2. **Substring externalization grep.** Grep the *final built* `index.html` for the exclusion tokens
   (provided in `docs/EXCLUSION-TOKENS.txt`, every token with `s?` plural suffix). **Any hit → ABORT.**
   This catches accidental leaks introduced in the *render template* (hardcoded strings, comments) —
   the only new leak surface a render change can create.
3. **MapLibre style smoke test.** Load the built style headless and assert: (a) zero layers rejected
   by style validation, (b) the route line layers (`route-glow`, `route-p2`, `route-qlr`) are present
   and bound to the `routes` source. This directly prevents the F-01 class of bug (route layers
   silently dropped by an invalid zoom expression) from ever shipping again.

If all three pass → `vercel deploy --prod`. Then post a one-line deploy notice to `#tasklet-jaideep`.

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
