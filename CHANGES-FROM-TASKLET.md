# Changes from Tasklet — pitch layer + route-label + Quanta-LR curation

_Last updated 2026-05-30 (overnight session)._

## This push (dev-mode build, route cache warm)

### Route labels — every tooltip now reads City → City (no slugs, no hashes)
- `route_labels.py` resolves BP endpoints in all forms: node id, raw BP id, **rendered
  `bp-<hash>` pin id**, and `city__suffix`.
- **Fixed a latent bug affecting ~906 local-mesh capillary routes**: bp-hash endpoints
  previously prettified to "Bp <hash>". Now they resolve to the real BP name AND real
  parent city. Verify: 0 routes contain a raw "Bp <hash>" label.
- Verbose BP names trimmed for tooltips (e.g. "Nuweiba Port (historic … ferry terminal)"
  → "Nuweiba Port"). Intra-city capillaries read "City: A → B".
- **Front-end ask still open**: tooltip should use `properties.label` (clean) — one-line change.

### Quanta-LR curation (A+B+C+D applied)
- **A** — any route ≤70 nm is now Pioneer II (all-electric range), even if the spine/config
  marked it Quanta-LR. Enforced in both `route_network._emit` and build.py edge gate.
  Result: Quanta-LR count 94 → 46; **0 Quanta-LR routes ≤70 nm**.
- **B** — illustrative placeholder endpoint (`rsg-marawi-east-island`) suppressed
  (`relevance:"hide"`); its 6 spur routes are gone.
- **C** — fixed the one raw unresolved endpoint (now "Nuweiba Port").
- **D** — genuine long-haul hospitality spurs kept, framed City → Region.
- Clean QLR hero backbone: Jeddah→NEOM (472nm), Wakatobi→Banda (370), Manama→Dubai (291),
  Lombok→Komodo (237), Bangkok→Koh Samui (205), Doha→Dubai (196)…
- Full curation log: `docs/QUANTA-LR-CURATION-REVIEW.md`.

### Partner pitch content layer (expanded — for Claude's render)
- **19 city briefs** (`partner-pitch/city_briefs/*.json`) — partner-neutral pitch synthesis
  (demand, use-cases by archetype, routes, POIs, PT angle, vessel fit) with per-partner overlays:
  MENA — dubai, abu-dhabi, doha, manama, muscat, jeddah, red-sea-global, neom, sharm-el-sheikh;
  SEA — singapore, bali, lombok, komodo, phuket, bangkok, hong-kong, maldives, jakarta-batam, colombo.
- **6 partner proposals** (`partner-pitch/partners/*.json`) — phased narrative arcs (hero,
  why-now, ordered phases w/ city subsets + routes + camera + KPIs):
  grab, dubai-rta, careem, abu-dhabi-itc, singapore-mpa, red-sea-global.
- **Now live in the page**: build injects `window.CITY_BRIEFS` and `window.PARTNERS` globals
  (guaranteed, idempotent) so the front-end can read them immediately. If/when the template
  adds `__CITY_BRIEFS__` / `__PARTNERS__` placeholders, the build uses those instead.
- **Claude action**: read `window.CITY_BRIEFS[cityId]` for the rich city panel; read
  `window.PARTNERS[slug]` (phases[]) for the phase carousel + `?partner=<slug>` scoping.
- Render specs: `docs/BRIEF-FOR-CLAUDE-pitch-panels.md`, test brief `docs/BRIEF-FOR-COWORK-pitch-flow.md`.

### Build architecture v4 — fast dev path vs weekly release gate
- `BUILD-ARCHITECTURE-v4.md`: `dev.sh` (seconds, default) vs `release.sh` (weekly full gate + seal + sweep).
- Two recurring traps fixed permanently in code: vessel_specs fallback (never empty),
  route-cache key now hashes supplemental inputs (no manual cache deletes).

## data-clean blobs (this build)
- FEATURES_BY_TYPE (4), ROUTES (1501), STORIES (7), VESSEL_SPECS (2).
- NOTE: dev-mode push — `SEAL.json` will be re-derived at next weekly `release.sh`.
