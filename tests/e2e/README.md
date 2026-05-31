# End-to-end smoke tests

Playwright smoke tests for the `index.html` render surface. Self-contained
(`node_modules` is gitignored), mirroring `scripts/preflight/`.

```bash
cd tests/e2e
npm install                 # one-time
npm run install:browser     # one-time — downloads the Chromium build
npm test                    # run the suite
npm run test:headed         # watch it in a real window
```

The Playwright `webServer` boots `serve.mjs` (a tiny static file server for the
repo root) and builds the gitignored `atlas-data.js` on first run if it's missing.

## What's covered

`bottom-sheet.spec.mjs` exercises the responsive bottom sheet added to `index.html`:

| Test | Asserts |
|---|---|
| peek → half → full → peek | tapping the grab handle cycles the snap points |
| drag up / drag down | dragging the handle snaps to the nearest point (full / peek) |
| auto-raise | rendering a real selection lifts the sheet from peek to half (the MutationObserver) |
| desktop rail | above 720px there's no handle and `#panel` is the right-anchored full-height rail |

## Offline / network note

The page loads MapLibre GL and fonts from CDNs. In sandboxed environments those
hosts may be blocked, and because `index.html` is one large inline script, a
throwing `new maplibregl.Map()` would halt it before the UI code runs. The tests
therefore **stub MapLibre** (`maplibre-stub.js`, served via route interception)
and abort font requests, so they run fully offline. These tests cover the
render-surface UI, **not** the map render itself — that's what `scripts/preflight`
§3.3 (the MapLibre layer smoke) is for.
