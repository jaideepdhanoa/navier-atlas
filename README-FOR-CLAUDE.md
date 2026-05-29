# Navier Atlas — Presentation-Layer Working Bundle

This is a self-contained export of the **Navier Atlas** front-end so you (Claude) can iterate
on the **presentation / UX layer independently**. The data research + secure build pipeline runs
on the other side and changes are merged back there.

Live reference: the production atlas renders from `index.html`.

---

## TL;DR — where to work

- **`index.html`** is the whole app: a single bundled file (MapLibre GL JS + Carto Dark tiles,
  Inter + JetBrains Mono fonts, glassmorphic UI, glowing markers). **All data is embedded** in it
  as JS consts. Open it in a browser and it runs standalone (needs internet for map tiles + libs).
  **This is the primary thing to iterate on for presentation work.**
- For data-driven prototyping, the embedded datasets are also provided as standalone JSON in
  **`data-clean/`** (extracted verbatim from `index.html`).

---

## What's in here

```
index.html                 # THE app — bundled presentation + embedded data (~2.3MB). Edit freely.
vercel.json                # Static hosting config (single-file deploy).
build.py                   # REFERENCE: how index.html is generated from data. See note below.
build_safe.sh              # REFERENCE: the full build pipeline shape.
routing/
  sea_router.py            # General grid A* sea-router (avoids land; LOS sampling).
  intra_cluster_routes.py  # Generates island-hopping spokes within a city cluster.
  auto_waypoints.py        # Region-pair waypoint helper (long-haul routes).
  route-waypoints.json     # Hand waypoints for specific corridors.
  harbour-overrides.json   # Harbour entry-point overrides.
  label-overrides.json     # Map label text overrides.
data-clean/
  FEATURES_BY_TYPE.json    # All map features (city nodes, boarding-point POIs) keyed by type.
  ROUTES.json              # All routes (origin/destination, platform, distance nm, est. time).
  STORIES.json             # Partner stories (side-panel narrative content).
  VESSEL_SPECS.json        # N30 Pioneer II + Quanta-LR platform specs used in UI.
docs/
  POI-RENDERING.md         # How boarding-point glyphs/colors/sizes render.
  CHANGELOG-v9-poi-glyphs.md
  atlas-external-README.md
  data-spine-SCHEMA.md     # Data schema reference.
```

---

## How the app is structured (inside `index.html`)

Data is embedded as JS consts (around line 305+):
- `FEATURES_BY_TYPE` — map features grouped by POI/marker type
- `ROUTES` — every route line
- `STORIES`, `STORY_BY_SLUG` — side-panel partner stories
- `VESSEL_SPECS`, `CRUISE_KTS` — platform specs + speeds for ETA calc
- `NODE_INDEX`, `SEARCH_INDEX` — built at runtime
- `BP_KEY` / `BP_COLOR` / `BP_GLYPH` / `BP_SIZE` — MapLibre paint expressions for boarding-point
  markers (this is the **legend + glyph styling** — a great place for presentation polish)
- `CAMERAS` — preset camera/fly-to positions
- `DEFAULT_OPACITY` — layer opacity defaults

**Boarding-point glyph vocabulary** (Noto-safe Unicode, not emoji):
marina (anchor) - ferry/cruise terminal (triangle) - yacht club (star) - hotel jetty (square) -
seaplane base - water taxi/abra (diamond) - MRO - refuel. See `docs/POI-RENDERING.md`.

**Platform scope:** N30 only by default (Pioneer II = 70 nm all-electric; Quanta-LR = 2,000 nm
hybrid). N80/N120/roadmap routes are hidden behind a toggle.

---

## Good areas for presentation-layer work

- Legend / glyph styling and consistency (glyphs must match actual map markers).
- Route hover tooltips (origin to destination, platform, distance nm, est. time).
- Side panel: collapse-to-0-width behavior, story layout, typography.
- Label rendering: map uses short labels (`shortName`); full name in panel; no country prefix.
- Terminology consistency: use **"Areas"** everywhere (not "Locales"); **"Boarding pts"** for POIs.
- Marker glow, color ramps by confidence, camera presets, mobile responsiveness.

---

## Important note on `build.py` (REFERENCE ONLY)

`build.py` is included so you can see exactly how `index.html` is assembled and propose changes
to the template/render logic. It **imports an internal-only `partition/` security module that is
intentionally excluded** from this bundle (it enforces a confidentiality gate that strips sensitive
content). So `build.py` won't run as-is here — that's by design. The full rebuild happens on the
source side. For presentation work you don't need to rebuild: edit `index.html` directly, or
prototype against `data-clean/`.

If you change the render template, describe the change (or edit a copy of the relevant code block)
and it gets applied + rebuilt + security-gated + deployed on the source side.

---

## How changes flow back

Hand back any of: an edited `index.html`, edited code blocks, or a written spec of the desired
presentation changes. They'll be applied against the live data pipeline, run through the
confidentiality gate, and deployed. Deploys are static (single `index.html` via the host config).

---

## What's intentionally NOT here (and why)

To keep this bundle safe to move around, the following are excluded:
- The `partition/` confidentiality gate (contains the sensitive-term denylist).
- Raw research data inputs (boarding-point source files, pre-partition node/org/edge data,
  contacts/CRM layer) — these contain internal strategy notes and are never shipped.
- API keys / deploy tokens (map tiles load from public CDNs; no key needed to view `index.html`).

The `data-clean/` JSON and `index.html` provided here are the **post-sanitization, publishable**
versions — safe to work with freely.
