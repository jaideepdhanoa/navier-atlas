# Prompt for Claude — Navier Atlas presentation-layer refinement

You can paste everything below this line into Claude alongside the `navier-atlas-export.zip` bundle.

---

## Who you are and what this is

You are helping refine the **front-end presentation layer** of the **Navier Atlas** — an interactive global map of maritime mobility opportunities for Navier (maker of software-defined electric/hybrid hydrofoiling vessels). The map shows cities/clusters, curated coastal boarding points, sea-routes between them, and a handful of partner "stories." It is built as a **single self-contained `index.html`** using **MapLibre GL JS** with Carto-style dark raster tiles, Inter + JetBrains Mono fonts, and a glassmorphic UI.

The bundle you have is a **safe, publishable export**. All confidential data has already been stripped out upstream — you are working only with sanitized, shippable content. **Do not attempt to add, infer, or reintroduce any names of people, deal terms, financials, or internal strategy.** Keep everything partner-/public-safe.

### Division of labor (important)
- **You (Claude)** own the **visual/interaction layer**: map styling, route rendering, clustering, zoom behavior, legend, filters, panels, and the partner-view feature described below. Iterate freely on `index.html` (and the render-template logic in `build.py` where the markup/style is generated).
- **A separate automation agent ("Tasklet")** owns the **research + data pipeline** and the **confidentiality gate + deploy**. It will take your changes, apply them against the live (fuller) dataset, run them through the security gate, and deploy. So: make your work **data-shape-preserving and easy to merge back** (see "Handoff back to Tasklet" at the end).

### Start by reading
- `README-FOR-CLAUDE.md` — orientation, app structure, glyph vocabulary, how data is embedded.
- `index.html` — the app itself. Open it in a browser to see current state.
- `data-clean/*.json` — the datasets (FEATURES_BY_TYPE, ROUTES, STORIES, VESSEL_SPECS) as standalone files, extracted from the built page.
- `routing/` — sea-router + intra-cluster route generator + waypoint/label/harbour override configs.
- `docs/` — POI rendering, glyph changelog, data schema.

First, **explore and form your own assessment.** Then propose a plan before large changes. You are encouraged to improve on the goals below — they are a starting point, not a ceiling.

---

## What I want improved

### 1. Routing quality (highest priority)
- **Smoothness:** routes currently look jagged/angular. Render them as smooth curves (great-circle-aware or spline/bezier-smoothed polylines) so they read as elegant arcs, not chained line segments.
- **Block overland routes:** no route should visibly cut across land at any zoom. The data pipeline already land-validates, but rendering can still make short hops *look* like they clip coastline. Improve the visual so nothing reads as crossing land (curve away from coast, or respect waypoints more faithfully).
- **Local routes more visible when zoomed in:** short intra-cluster/local spokes should become more prominent as you zoom in (thicker, brighter, labeled), while long-haul routes can recede.

### 2. Clusters & node visual hierarchy
- **Central/hub nodes should have more visual flair derived from their routes** — e.g., a node with many spokes radiating should feel like a hub (glow, halo, weighting, or a subtle burst of its outgoing routes) without manual tagging. Derive importance from degree/route-count in the data, not a hardcoded list.
- **Density management across zoom levels:** at low zoom the map should feel curated, not cluttered — cluster/aggregate nearby nodes and thin out routes/labels; at high zoom progressively reveal local boarding points, local routes, and labels. Define clean rules for what appears at each zoom band.

### 3. General visual polish
- Clean, consistent, polished **interface, legend, filters, and panels**. Tighten spacing, alignment, typography, contrast, and the glassmorphic treatment so it feels premium.
- **Legend/filter color consistency (known bug):** the filter controls at the bottom are a **different color than the actual glyphs/markers on the map**. Make the legend and filter swatches match exactly what's rendered on the map (glyph shape AND color), so they're a true key. The glyph vocabulary is in `README-FOR-CLAUDE.md` / `docs/POI-RENDERING.md`.
- Make sure terminology is consistent across all UI ("Areas," "Boarding pts," etc. per the docs).

### 4. Partner-specific views (new feature)
- Today the app is effectively an **admin view: every story is shown to everyone.** I want **partner-specific versions** so a given partner sees a tailored subset (e.g., only the stories/markets relevant to them) rather than the full set.
- Propose a clean mechanism — e.g., a `?partner=<slug>` URL parameter (and/or a small selector) that filters which stories/markets/routes are surfaced and adjusts copy/branding accordingly.
- Keep it **data-driven**: a partner-view should be expressible as a small config object (which story slugs, which regions, optional title/intro), so new partner views can be added without code changes. Define the schema for that config and document it. The admin/all view should remain available.
- Do **not** invent partner identities or confidential specifics — build the *mechanism* and demonstrate it with the existing public stories. Tasklet will populate real partner configs on its side.

---

## Constraints & ground rules
- Keep it a **single self-contained `index.html`** that works when opened directly (no build server required to preview). If you add a build step, keep `index.html` regenerable and document it.
- **Preserve data shapes.** If you need a data change, prefer additive optional fields and **document them** rather than restructuring existing ones — Tasklet regenerates the data and must be able to merge your render changes cleanly.
- **No new dependencies on paid/keyed services.** Stay within MapLibre + open tiles/fonts. No API keys anywhere.
- **Confidentiality:** never add personal names, financials, deal terms, or internal strategy. Treat all output as publicly shippable.
- Performance: the live dataset is larger than this sample (~60+ clusters, ~1,900 boarding points, ~470 routes). Make sure clustering/zoom/render choices scale to that.

---

## Handoff back to Tasklet (do this at the end)
So your work can be re-imported easily, produce a **`HANDOFF-FOR-TASKLET.md`** that includes:
1. **Changelog** — what you changed, file by file, with rationale.
2. **Schema changes / new data fields** — any new or optional fields you introduced (e.g., partner-view config, per-route style hints, node-importance field), with exact JSON shape and where they're consumed in the render code. Flag anything Tasklet needs to populate from the fuller dataset.
3. **Render contract** — the assumptions your render code makes about the data (field names, value ranges, defaults when a field is absent), so Tasklet's `build.py` can emit compatible data.
4. **Partner-view spec** — the config format for defining a partner view, and how to add a new one.
5. **Open questions / requests for Tasklet** — anything you need from the data side (e.g., "please emit a `degree` field per node," or "stories need a `regions` array").
6. **Migration notes** — anything Tasklet must do to its pipeline so a fresh `build.py` run produces output your front-end expects.

Bundle your modified `index.html`, any new/changed files, and `HANDOFF-FOR-TASKLET.md` back into a zip. I'll hand that back to Tasklet to apply against live data, run the security gate, and deploy.

---

## Suggested first response from you
1. A short read-out of the current state and the biggest visual/interaction weaknesses you see.
2. A prioritized plan (routing smoothness + overland → node/cluster hierarchy + zoom density → polish + legend/filter consistency → partner views).
3. Any clarifying questions, then start on the highest-impact item.
