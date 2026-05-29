# POI rendering — dual-key schema + glyph-server constraint

_Created 2026-05-28 (consolidation pass #10). Promoted from atlas build.py v9 POI glyph rewrite + v8 visual audit findings._

## Dual-key POI schema

POI features carry **two parallel typing keys** that are NOT synonyms:

| Key | Source | Format | Example values |
|---|---|---|---|
| `bp_type` | `boarding-points/*.json` (curated city POIs) | underscore_separated | `hotel_jetty`, `ferry_terminal`, `working_harbour`, `seaplane_base`, `floating_pontoon`, `event_pontoon`, `beach_club_jetty`, `public_pier`, `water_bus_terminal`, `shipyard_partner` |
| `poi_class` | upstream `nodes.json` (project-wide POIs, 427 rows) | hyphen-separated | `hospitality-hub`, `anchor-marina`, `out-of-range-marquee`, `gateway-airport-adjacent`, … |

Both flow through `build.py` (preserved at the GeoJSON builder lines for nodes + boarding-points) but have historically been treated by the consumer (style expressions) as if `bp_type` were the only key.

**Authoring requirement (all future POI styling, filtering, legend, deep-link, audit work):**

```js
const BP_KEY = ["coalesce", ["get","bp_type"], ["get","poi_class"], "default"];
```

Every `BP_COLOR`, `BP_GLYPH`, `BP_SIZE`, and any `match`/`filter` expression keyed on POI type MUST include both underscore (`hotel_jetty`) AND hyphen (`hospitality-hub`) variants in its match-cases. Underscore-only matching is the root cause of the v7/v8 "POI type collapsed to generic poi" audit defect — propagation is fine; consumer was the bug.

## Glyph-server / fontstack constraint

The MapLibre style currently points at `demotiles.maplibre.org/font/...` which ships **Noto Sans Regular/Bold only**. Emoji codepoints (🚢 🏨 🛥 🛬 🚤 …) render as tofu boxes at this glyph server.

**Authoring requirement for `text-field` glyphs:**

- Default to **Geometric Shapes + Misc Symbols block** Unicode points that are within Noto Sans Bold's PBF range: `⚓ ▲ ★ ■ ✦ ◆ ⬢ ⬟ ●`.
- Verify any new glyph at the demo server before committing — if it tofu's at z=11, replace.
- If emoji-class glyphs are strictly required for a future legend, options are:
  - self-host a fontstack with emoji coverage (Noto Sans + Noto Emoji merged PBFs), or
  - switch to SDF icon sprites via `map.loadImage` + `map.addImage` (carries higher build cost).

## Detail-pill label parity

`bp_type_label` (BP_TYPE_LABELS) is `undefined` for nodes.json POIs → the detail-pill currently falls back to "boarding pt" for 427 of the 700+ POIs.

**Follow-up patch:** mirror `BP_TYPE_LABELS` with `POI_CLASS_LABELS` and coalesce in the pill rendering at the detail-pill code path.

## Cross-references

- Pass #10 source-discovery learnings entry 2026-05-28 in `_subagent-learnings.md`.
- `CITY_TEMPLATE.md` section MMM (coastal-POI authoring) for the source schema.
- `build.py` v9 patch + `CHANGELOG-v9-poi-glyphs.md` for the rendering-side implementation.
