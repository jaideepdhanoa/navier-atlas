#!/usr/bin/env node
// ─────────────────────────────────────────────────────────────────────────────
// Navier Atlas — deploy pre-flight  (DIVISION-OF-LABOR.md §3)
// Run before EVERY `vercel deploy --prod`. Exit 0 = all checks pass; non-zero = ABORT.
//
//   node scripts/preflight/preflight.mjs [repo-root]
//
// Three checks, cheap (seconds), no land/A* gate (those ran at seal time):
//   §3.1  hash match      — recompute sha256 of each sealed data blob vs data-clean/SEAL.json
//   §3.2  exclusion grep   — final index.html must not match any docs/EXCLUSION-TOKENS.txt pattern
//   §3.3  MapLibre smoke   — run the page's real layer code under a MapLibre stub, validate every
//                            layer with the official style-spec, assert route line layers register
//                            & are bound to `routes` (directly prevents the F-01 dropped-layer class)
//
// Flags:
//   --allow-unsealed   proceed if SEAL.json is absent (NON-PROD smoke only; never for prod deploy)
// ─────────────────────────────────────────────────────────────────────────────
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { JSDOM } from 'jsdom';
import styleSpec from '@maplibre/maplibre-gl-style-spec';

const ROOT  = path.resolve(process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : '.');
const ALLOW_UNSEALED = process.argv.includes('--allow-unsealed');
const INDEX  = path.join(ROOT, 'index.html');
const SEAL   = path.join(ROOT, 'data-clean', 'SEAL.json');
const TOKENS = path.join(ROOT, 'docs', 'EXCLUSION-TOKENS.txt');

let failed = false;
const fail = (m) => { console.error('   ✗ ' + m); failed = true; };
const ok   = (m) => console.log('   ✓ ' + m);
const head = (m) => console.log('\n' + m);

if (!fs.existsSync(INDEX)) { console.error('FATAL: index.html not found at ' + INDEX); process.exit(2); }
const html = fs.readFileSync(INDEX, 'utf8');

// ─── §3.1 · Hash match (anti-tamper) ──────────────────────────────────────────
// SEAL.json (Tasklet-produced) is expected to be: { "blobs": { "<NAME>": { "sha256": "...", "count": N }, ... } }
// where <NAME>.json lives in data-clean/ and is injected into index.html. Any mismatch ⇒ data was
// altered after sealing (only Tasklet may change data) ⇒ ABORT.
head('§3.1  seal hash match (anti-tamper)');
if (!fs.existsSync(SEAL)) {
  if (ALLOW_UNSEALED) console.warn('   ⚠ data-clean/SEAL.json absent — bypassed via --allow-unsealed (NOT valid for prod)');
  else fail('data-clean/SEAL.json missing — cannot verify data integrity. Tasklet must ship it. (Use --allow-unsealed for a non-prod smoke run.)');
} else {
  try {
    const seal  = JSON.parse(fs.readFileSync(SEAL, 'utf8'));
    const blobs = seal.blobs || seal;
    let n = 0;
    for (const [name, meta] of Object.entries(blobs)) {
      const expected = (meta && (meta.sha256 || meta.sha)) || meta;
      const src = path.join(ROOT, 'data-clean', name + '.json');
      if (!fs.existsSync(src)) { fail(`SEAL lists ${name} but data-clean/${name}.json is missing`); continue; }
      const sha = crypto.createHash('sha256').update(fs.readFileSync(src)).digest('hex');
      if (sha !== expected) fail(`${name}: sha256 mismatch vs SEAL (data altered after sealing)`);
      else { ok(`${name}: sha256 matches SEAL`); n++; }
    }
    if (n && !failed) ok(`${n} sealed blob(s) verified`);
  } catch (e) { fail('SEAL.json parse error: ' + e.message); }
}

// ─── §3.2 · Substring externalization grep ────────────────────────────────────
head('§3.2  exclusion-token grep (leak guard)');
if (!fs.existsSync(TOKENS)) {
  fail('docs/EXCLUSION-TOKENS.txt missing — cannot run the leak guard');
} else {
  const pats = fs.readFileSync(TOKENS, 'utf8').split('\n')
    .map(l => l.trim()).filter(l => l && !l.startsWith('#'));
  let hits = 0;
  for (const p of pats) {
    let re; try { re = new RegExp(p, 'i'); } catch { console.warn('   (skipped un-compilable pattern: ' + p + ')'); continue; }
    const m = html.match(re);
    if (m) { hits++; fail(`exclusion token matched /${p}/i → "${String(m[0]).slice(0,60)}"`); }
  }
  if (!hits) ok(`${pats.length} tokens checked · 0 hits`);
}

// ─── §3.3 · MapLibre style smoke test ─────────────────────────────────────────
// Execute the page's inline script under a MapLibre stub that records addSource/addLayer, then
// validate the resulting style with the official style-spec and assert the route line layers exist.
head('§3.3  MapLibre style smoke test');
try {
  // Grab the LAST bare <script> (the app script). The page may carry earlier bare <script> blocks
  // (e.g. the head content-layer script that sets window.CITY_BRIEFS/PARTNERS) — those must not be
  // swept into the captured text, or eval hits stray HTML ("Unexpected token '<'").
  const start = html.lastIndexOf('<script>');
  const end = start >= 0 ? html.indexOf('</script>', start) : -1;
  if (start < 0 || end < 0) throw new Error('could not locate the inline app <script>');
  const scriptText = html.slice(start + '<script>'.length, end);

  const sources = {};
  const layers = [];
  const layerIds = new Set();
  const loadCbs = [];   // defer 'load' callbacks until after the script runs (real browser timing —
                        // otherwise module-scope `let`s referenced in the callback hit the TDZ)

  class StubMap {
    constructor(opts) { this._opts = opts || {}; }
    on(type, a, _b) { if (type === 'load' && typeof a === 'function') loadCbs.push(a); return this; }
    once(type, a) { return this.on(type, a); }
    off() { return this; }
    addSource(id, def) { sources[id] = def; }
    getSource(id) { return sources[id] ? { ...sources[id], getClusterExpansionZoom: () => Promise.resolve(2), setData(){} } : undefined; }
    addLayer(def) { if (def && def.id) { layers.push(def); layerIds.add(def.id); } }
    getLayer(id) { return layerIds.has(id) ? { id } : undefined; }
    removeLayer() {} removeSource() {}
    setPaintProperty() {} setLayoutProperty() {} setFilter() {} setLayerZoomRange() {}
    getPaintProperty() {} getLayoutProperty() {}
    addControl() { return this; } removeControl() { return this; }
    getCanvas() { return { style: {} }; }
    getContainer() { return { style: {} }; }
    flyTo() {} easeTo() {} jumpTo() {} fitBounds() {} panTo() {} setCenter() {} setZoom() {} resize() {}
    getZoom() { return 1.8; } getCenter() { return { lng: 40, lat: 15 }; } getBounds() { return { getWest:()=>0,getSouth:()=>0,getEast:()=>0,getNorth:()=>0 }; }
    queryRenderedFeatures() { return []; } querySourceFeatures() { return []; }
    project() { return { x: 0, y: 0 }; } unproject() { return { lng: 0, lat: 0 }; }
  }
  // maplibregl proxy: real Map; any other member (NavigationControl, Marker, Popup, …) → no-op ctor/fn
  const NoOp = function () { return new Proxy({}, { get: () => () => {} }); };
  const maplibregl = new Proxy({ Map: StubMap }, { get: (t, p) => (p in t ? t[p] : NoOp) });

  const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true, url: 'https://navier-atlas.vercel.app/' });
  const { window } = dom;
  window.maplibregl = maplibregl;
  if (!window.matchMedia) window.matchMedia = () => ({ matches: false, addListener(){}, removeListener(){}, addEventListener(){}, removeEventListener(){} });

  // Run the page's script in the jsdom window scope (uses our stub + the real DOM), then fire the
  // deferred 'load' callbacks (which is where addSource/addLayer happen) — now that all module-scope
  // declarations are initialized, exactly as in a real browser.
  window.eval(scriptText);
  for (const cb of loadCbs) cb();

  if (!layers.length) throw new Error('no layers were added (script may have thrown before map setup)');

  // (a) zero layers rejected by style validation
  const style = {
    version: 8,
    sources: Object.fromEntries(Object.entries(sources).map(([id, s]) =>
      [id, s && s.type === 'geojson' ? { type: 'geojson', data: { type: 'FeatureCollection', features: [] } } : s])),
    layers: layers.map(l => ({ ...l })),
  };
  const errors = styleSpec.validateStyleMin(style) || [];
  // Only fail on layer/expression errors (ignore glyphs/sprite/source-data nits from the stubbed style).
  const real = errors.filter(e => !/glyphs|sprite|sources\.|^source/i.test(e.message || ''));
  if (real.length) {
    for (const e of real.slice(0, 25)) fail(`style validation: ${e.message}`);
  } else ok(`${layers.length} layers · 0 rejected by style validation`);

  // (b) route line layers present & bound to the `routes` source
  const routeLineLayers = layers.filter(l => l.type === 'line' && l.source === 'routes');
  const need = ['route-p2', 'route-qlr'];
  const missing = need.filter(id => !layerIds.has(id));
  if (missing.length) fail(`route line layer(s) missing: ${missing.join(', ')}`);
  else if (routeLineLayers.length < 2) fail(`expected ≥2 line layers bound to source "routes", found ${routeLineLayers.length}`);
  else ok(`route line layers present & bound to "routes": ${routeLineLayers.map(l => l.id).join(', ')}`);
} catch (e) {
  fail('smoke test threw: ' + (e && e.message ? e.message : e));
}

// ─── §3.4 · Pitch-render presence ───────────────────────────────────────────────
// Guards the recurring failure where a build.py regen re-emits index.html WITHOUT the PR#3
// render: the window.CITY_BRIEFS/PARTNERS data still loads, but nothing renders it (dead UI).
// If the content is inlined, the render that consumes it MUST be present — else abort the deploy.
head('§3.4  pitch-render layer present');
{
  const hasContent = /window\.CITY_BRIEFS\s*=/.test(html) || /window\.PARTNERS\s*=/.test(html);
  if (!hasContent) {
    ok('no inline pitch content (CITY_BRIEFS/PARTNERS) — render check skipped');
  } else {
    const need = [
      ['city pitch panel (CITY_BRIEFS read)', /CITY_BRIEFS\s*\[/],
      ['partner phase carousel',              /function\s+applyPhaseFocus|_renderCarousel|showPhase\s*\(/],
      ['route-label recovery',                /_routeLabel\s*\(/],
    ];
    const gone = need.filter(([, re]) => !re.test(html)).map(([n]) => n);
    if (gone.length) fail(`pitch content is inlined but its render is MISSING: ${gone.join(' · ')} — a build regen likely dropped the PR#3 render (re-apply it, then run claude_to_template.py so the template keeps it)`);
    else ok('city panel + partner carousel + route-label recovery all present');
  }
}

// ─── verdict ──────────────────────────────────────────────────────────────────
console.log('');
if (failed) { console.error('PRE-FLIGHT FAILED — deploy ABORTED.'); process.exit(1); }
console.log('PRE-FLIGHT PASSED — clear to deploy.');
process.exit(0);
