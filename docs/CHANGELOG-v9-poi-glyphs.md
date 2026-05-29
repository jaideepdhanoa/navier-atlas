# Atlas v9 — POI glyph differentiation

**Date:** 2026-05-28
**File touched:** `build.py` only (lines ~729–757 → replaced with symbol layer)
**Deploy status:** NOT deployed (per instructions; parent will deploy after batch-3 lands).

## Why

Per Jaideep: POI pins must NOT all be circles. v7/v8 rendered every boarding-point
as a colored disc with `circle-radius` variations — readable only to someone who
already knows the colour key. Color is now a *secondary* encoding; **shape is
primary**.

## What changed

Replaced the `poi-points` circle layer with a MapLibre **symbol layer** that
draws a Unicode glyph per POI. The `poi-halo` circle layer is retained (dimmed
to 0.18 opacity, blur 0.7) as a soft underglow for legibility on the dark
basemap. Cluster layers (`poi-clusters`, `poi-cluster-count`) are unchanged.

### Glyph map (Noto Sans-safe; no emoji)

| Glyph | U+    | POI families |
|-------|-------|--------------|
| ⚓    | 2693 | marina, working_harbour, anchor-marina, secondary-hub |
| ▲    | 25B2 | ferry_terminal, cruise_terminal, water_bus_terminal, cross-border-gateway |
| ★    | 2605 | yacht_club, leisure-spoke |
| ■    | 25A0 | hotel_jetty, resort_jetty, beach_club_jetty, hospitality-hub, resort-jetty |
| ✦    | 2726 | seaplane_base |
| ◆    | 25C6 | water_taxi_stop, abra_station, public_pier, floating_pontoon |
| ⬢    | 2B22 | shipyard_partner, mro-node, floating_helipad, event_pontoon, dive_centre, sandbox_water |
| ⬟    | 2B1F | refuel-mid-node |
| ●    | 25CF | out-of-range-marquee, default |

Emoji (⚓ as 🚢/🏨/🛥/🛬/🚤 in the original spec) were rejected because the
demotiles glyph server (`https://demotiles.maplibre.org/font/...`) ships
Noto Sans Regular/Bold only — emoji codepoints would render as tofu. Geometric
Shapes + Miscellaneous Symbols (the chosen set) are within Noto Sans Bold's
range and verified to render.

### Color (secondary encoding, preserved)

Same family palette as v8 (mint = hospitality, rose = ferry/cruise, gold =
yacht/leisure, cyan = water-taxi/pier, slate = harbour/MRO, purple = seaplane/
helipad, blue = marina, amber = refuel, grey = out-of-range). Applied as
`text-color` with `#0a0e14` halo at 1.6 px + 0.4 blur.

### Size

`text-size` interpolates 10–18 px by POI class — anchors/marinas largest, leaf
piers/abras smallest. Preserves v8's importance hierarchy.

## CRITICAL FIX — `bp_type` / `poi_class` propagation (v7 audit flag)

The v7 audit warned that `bp_type` was being flattened to a generic `poi` type.
Trace confirms it actually propagates correctly via `features.append(...)` at
build.py:172 and the dedup loop at build.py:242 explicitly preserves curated
boarding-points. **However**, the v7 BP_COLOR/BP_RADIUS expressions only keyed
on `bp_type`, ignoring the parallel `poi_class` field that nodes.json upstream
POIs carry (427 such POIs — `anchor-marina`, `leisure-spoke`,
`out-of-range-marquee`, `hospitality-hub`, `cross-border-gateway`,
`resort-jetty`, `refuel-mid-node`, `secondary-hub`, `marina`, `mro-node`,
`abra-station`, `public-pier`). Those rendered as the default blue dot.

v9 fixes this with a shared key expression:

```js
const BP_KEY = ['coalesce', ['get','bp_type'], ['get','poi_class'], 'default'];
```

…used by all three of `BP_COLOR`, `BP_GLYPH`, and `BP_SIZE`. Underscore
(`hotel_jetty`) and hyphen (`hospitality-hub`) variants are both listed in
each match expression so curated and upstream POIs render with consistent
visual semantics.

## Verification

- Build runs clean: `pois=955 routes=264 stories=6` (unchanged counts).
- `index.html` = 1,443 KB (was 1,422 KB; +21 KB for the longer match
  expressions, expected).
- `grep "BP_GLYPH\|BP_KEY"` → 5 hits in `index.html`.
- `grep "poi_class"` → 180 hits in `index.html` (confirms field flows into
  per-feature props on the JS side, not just the style expression).

## Not deployed

Per instructions, parent will deploy after batch-3 city stubs land. To deploy
locally: `cd /agent/home/navier/atlas-external && vercel deploy --prod`
(if Vercel CLI is configured) or whatever the standard flow is.

## Known follow-ups (not in scope here)

- `bp_type_label` is `undefined` for upstream `poi_class` POIs → the detail
  pill at build.py:860 falls back to `"boarding pt"`. Future patch: extend
  the coalesce to also use `poi_class` formatted to title case, or add a
  `POI_CLASS_LABELS` map mirroring `BP_TYPE_LABELS`.
- Glyph server is `demotiles.maplibre.org` (demo-grade, no SLA). If POI
  density ever grows enough that glyph requests become a perf concern,
  switch to a self-hosted PBF font stack or move to SDF icons via
  `loadImage` + `addImage` (Option B from the v9 brief).
- Consider a small in-map legend strip for the glyph→family mapping; current
  reliance on the detail panel pill is OK but adds a click for first-time
  viewers.
