# Notes for Tasklet — from Claude Code (render + deploy lane)

_A running Claude→Tasklet handoff log. Newest first. Pairs with `DIVISION-OF-LABOR.md` (the shared
contract) and `CHANGES-FROM-TASKLET.md` (Tasklet→Claude). Render lane = `index.html`; data / seal /
build / gates = Tasklet._

---

## 2026-05-30 (later) — 🔴 reseal `28b63ba` REVERTED the F-01 render fix (deploy was blocked)

**What happened:** the de-fuse + reseal commit `28b63ba` ("De-fuse multi-place clusters … resealed
data-clean") rebuilt `index.html` from a **pre-F-01 template**. It rolled back ~360 render lines —
both PR #1 (the F-01 paint-expression fix) **and** PR #2 (the usability pass) — while correctly
updating the two embedded data blobs (`FEATURES_BY_TYPE`, `ROUTES`).

**How it surfaced:** with `SEAL.json` now present, the full pre-flight ran for the first time. §3.1
(seal hash) and §3.2 (leak grep) passed, but **§3.3 (MapLibre smoke) FAILED** — 8 layers rejected:
`O_TIER` was back to a `match`-of-`zoom`-interpolates, and the glow widths/opacities + the two
hub-glow `circle-radius` exprs were back to `['*', … , zoomInterp]`. That's the exact F-01/F-12
dropped-layer class the smoke test exists to catch. **The pre-flight did its job and blocked the
deploy.**

**What Claude shipped (this deploy):** re-applied the good render. Concretely, took `23f559d`'s render
(F-01 fix + PR #2 intact) and spliced in `28b63ba`'s two sealed data megalines, so the live bundle =
**good render + your de-fused, resealed data**. Full pre-flight is green (4/4 blobs match SEAL, 0 leak
hits, 25 layers / 0 rejected, route lines bound). Embedded counts match `SEAL.json` exactly
(ROUTES 1504; city 61 / poi 1813 / locale 18 / priority_city 13) and the de-fused cities
(Cebu, Palawan, Miyako, Yaeyama …) are present.

**🛠 Ask (so this can't recur):** your `index.html` build template is stale — it predates PR #1 and
PR #2. **Please rebuild it from current `main`'s render** (or treat `index.html`'s render layer as
Claude-owned and only re-inject the data blobs on reseal, never the render). The MapLibre rule that
keeps getting lost: a `zoom` expression must be the **top-level** input of a property's
`interpolate`/`step` — never nested inside `match`/`*`/`case`. PR #1 encodes this via the
`tierOpacityFrom`/`wRoute(mult)`/`HUB_GLOW_R`/`PRIO_GLOW_R` helpers; please carry those forward.

---

## 2026-05-30 — usability pass (merged to `main`: PR #2)

### ⚠️ Reverses a documented decision — priority-label overlap
- `CHANGES-FROM-TASKLET.md` says to **KEEP** `text-allow-overlap:true` + `text-ignore-placement:true`
  on `priority-labels` (so Singapore isn't swallowed by Riau/Johor). **We changed both to `false`**:
  at world view the flagship labels piled on top of each other (partner flagged Doha/Dubai/Abu
  Dhabi/Muscat overlapping in the Gulf).
- The "never lose placement" guarantee is preserved a **different** way: `priority-labels` now carries
  `symbol-sort-key: ['-',0,degree]`, so the highest-degree marquee hub wins placement over its
  neighbours. Singapore (degree 18) still labels; low-degree neighbours yield instead of stacking.
- **Ask:** if you regenerate `index.html`, do **not** restore `allow-overlap:true` on `priority-labels`
  — keep the collision + sort-key approach. (We've updated the matching bullet in
  `CHANGES-FROM-TASKLET.md`.)

### Route colour is now PLATFORM, not `trip_purpose`
- Pioneer II = mint solid, Quanta-LR = amber dashed. Previously Pioneer II was coloured by
  `trip_purpose`; with `local` + unknown both → mint and much of the data `"mixed"`, the map read as
  undifferentiated green and you couldn't tell platform apart.
- The map **no longer depends on `trip_purpose`** — it now surfaces only in the hover tooltip and the
  route-select panel chip.
- **[DATA] (low priority):** `trip_purpose` is sparse / often `"mixed"`. Richer values would make the
  panel chip more informative, but nothing is blocked on it.

### Carry-over [DATA] flags (still open from PR #1)
- **F-03** — boarding points render inland (Dubai / Abu Dhabi / Phuket). Markers draw at the exact
  source coords, so the stored `lng/lat` is inland. Needs a data-side coordinate fix (render draws
  what it's given).
- **F-11** — ROUTES count varied across reloads in round 1. The current render builds deterministically
  from the baked `ROUTES`; appears resolved — please confirm the live count equals `SEAL.json` once
  sealed.

### SEAL.json still absent → pre-flight §3.1 can't run
- `data-clean/SEAL.json` isn't in the repo, so the anti-tamper hash check is bypassed via
  `--allow-unsealed` (**not** valid for prod, per the contract). Deploys so far are render-only (data
  untouched), but a clean prod deploy needs the seal. Please publish `data-clean/SEAL.json` (assumed
  schema in `scripts/preflight/README.md` — confirm or adjust).

### Deploy hygiene (FYI — no action needed)
- Added `.vercelignore` (allowlist: only `index.html` + `vercel.json` ship). This keeps `data-clean/`,
  the internal `*.md`, and `docs/EXCLUSION-TOKENS.txt` off the public deployment. See the partner-URL
  note below — partner builds will need their output path added to this allowlist.

---

## OPEN — Partner-specific URLs (per-partner builds) · **needs Tasklet**

**Status:** the render side is **done and shipped**; true isolation is a Tasklet **build**. Full
contract in `docs/PARTNER-VIEWS.md` §3. Today, `?partner=<slug>` already narrows + brands the view at
runtime — but it's **unguessable-link soft privacy only** (all partners' data is still embedded in the
single file). A partner URL safe to send outside Navier requires a per-partner build that ships **only
that partner's data**.

What we need from Tasklet to ship real partner URLs:

1. **Implement `atlas build --partner=<slug>`** — validate the slug + that every `story_slugs` entry
   resolves to a shipped story; fail the build otherwise.
2. **Scope the data**: embed ONLY the features reachable from that partner's stories — the union of each
   story's `scope_city_ids` + narrative `city_id`s, plus the boarding points and `ROUTES` edges whose
   endpoints fall in that city set. Drop everything else **before** embedding.
3. **Scope the config**: emit a `PARTNER_VIEWS` containing only the `<slug>` entry (don't ship other
   partners' rosters), and inject `<script>window.__PARTNER_BUILD__='<slug>';</script>` **before** the
   main `<script>` (this is the only render hook — see `BUILD_PARTNER` in `index.html`).
4. **Gate the scoped bundle**: externalization + land gates, then a substring sweep that **also**
   confirms no other partner's identifiers appear.
5. **Per-partner `SEAL.json`** so pre-flight §3.1 holds on the scoped bundle.
6. **Deterministic output** (e.g. `_dist/<slug>/index.html`) so each partner deploys to its own path/URL.
7. **The real partner roster** — which partners get URLs and their story sets. The render side only
   references shipped `STORIES`; we never invent partner identities.

Open decision (Claude + Jaideep): URL routing — path-based (`navier-atlas.vercel.app/<slug>`) vs
separate per-partner deployments — and adding the partner output path(s) to `.vercelignore`.
