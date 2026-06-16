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
//   --release          prod deploy — §3.1 seal mismatch/absence ABORTS. Without it, §3.1 is advisory
//                      (dev iteration on the render must not be blocked by a seal only Tasklet refreshes).
//   --allow-unsealed   proceed if SEAL.json is absent (NON-PROD smoke only; never for prod deploy)
// ─────────────────────────────────────────────────────────────────────────────
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { JSDOM } from 'jsdom';
import styleSpec from '@maplibre/maplibre-gl-style-spec';

const ROOT  = path.resolve(process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : '.');
const ALLOW_UNSEALED = process.argv.includes('--allow-unsealed');
const RELEASE = process.argv.includes('--release');   // prod deploy: enforce the seal (§3.1). Dev: advisory.
const INDEX  = path.join(ROOT, 'index.html');
const SEAL   = path.join(ROOT, 'data-clean', 'SEAL.json');
const TOKENS = path.join(ROOT, 'docs', 'EXCLUSION-TOKENS.txt');

let failed = false;
const fail = (m) => { console.error('   ✗ ' + m); failed = true; };
const ok   = (m) => console.log('   ✓ ' + m);
const head = (m) => console.log('\n' + m);

if (!fs.existsSync(INDEX)) { console.error('FATAL: index.html not found at ' + INDEX); process.exit(2); }
const html = fs.readFileSync(INDEX, 'utf8');

// Data now ships as a separate asset (atlas-data.js, built from data-clean/ by scripts/build.mjs)
// rather than inlined into index.html. Read it once: the smoke test evals it to set window globals,
// and the leak-grep (§3.2) must scan it since that is now where excluded data would surface.
const ATLAS = path.join(ROOT, 'atlas-data.js');
const atlasData = fs.existsSync(ATLAS) ? fs.readFileSync(ATLAS, 'utf8') : null;
const deployText = atlasData ? (html + '\n' + atlasData) : html;

// ─── §3.1 · Hash match (anti-tamper) ──────────────────────────────────────────
// SEAL.json (Tasklet-produced) supports multiple manifest shapes (merged + deduped):
//   legacy:       { "blobs": { "ROUTES": { "sha256": "<hex>", ... }, ... } }
//   v2/v3:        { "files": { "ROUTES.json": "<hex>" | { "sha256": "<hex>" }, ... } }
//   v5 (#79i+):   { "file_hashes": { "ROUTES.json": "<hex>", "partners/grab.json": "<hex>", ... } }
// Optional "sidecars" block uses the same meta shapes. Any on-disk mismatch ⇒ ABORT.
const collectSealEntries = (seal) => {
  const merged = {};
  for (const block of [seal.file_hashes, seal.files, seal.blobs, seal.sidecars]) {
    if (!block) continue;
    for (const [name, meta] of Object.entries(block)) {
      const rel = /\.(json|md)$/i.test(name) ? name : `${name}.json`;
      merged[rel] = meta;
    }
  }
  return merged;
};
const sealExpectedHex = (meta) => {
  if (!meta) return null;
  if (typeof meta === 'string') return meta.replace(/^sha256:/, '');
  const raw = meta.sha256 || meta.sha;
  return raw ? String(raw).replace(/^sha256:/, '') : null;
};
const sealBlobPath = (name) => {
  const rel = /\.(json|md)$/i.test(name) ? name : `${name}.json`;
  return { rel, abs: path.join(ROOT, 'data-clean', rel) };
};
const verifySealEntries = (entries, label, sealIssue) => {
  let n = 0, bad = 0;
  for (const [name, meta] of Object.entries(entries)) {
    const expected = sealExpectedHex(meta);
    if (!expected) { sealIssue(`${label} ${name}: no sha256 in SEAL entry`); bad++; continue; }
    const { rel, abs } = sealBlobPath(name);
    if (!fs.existsSync(abs)) { sealIssue(`SEAL lists ${name} but data-clean/${rel} is missing`); bad++; continue; }
    const sha = crypto.createHash('sha256').update(fs.readFileSync(abs)).digest('hex');
    if (sha !== expected) { sealIssue(`${rel}: sha256 mismatch vs SEAL (data changed after sealing)`); bad++; }
    else { ok(`${rel}: sha256 matches SEAL`); n++; }
  }
  return { n, bad };
};

head('§3.1  seal hash match (anti-tamper)' + (RELEASE ? '' : '  [dev: advisory — pass --release to enforce]'));
// The seal is Tasklet's data-integrity gate, refreshed on their cadence. In prod (--release) any
// mismatch/absence ABORTS. In dev it is advisory: a stale seal must not block Claude's render +
// deploy iteration (Claude never edits the sealed blobs; build.mjs derives atlas-data.js from them).
const sealIssue = (m) => RELEASE ? fail(m) : console.warn('   ⚠ ' + m + '  [advisory in dev]');
if (!fs.existsSync(SEAL)) {
  if (ALLOW_UNSEALED) console.warn('   ⚠ data-clean/SEAL.json absent — bypassed via --allow-unsealed');
  else sealIssue('data-clean/SEAL.json missing — cannot verify data integrity (Tasklet ships it)');
} else {
  try {
    const seal = JSON.parse(fs.readFileSync(SEAL, 'utf8'));
    const entries = collectSealEntries(seal);
    const { n, bad } = verifySealEntries(entries, 'sealed', sealIssue);
    if (n && !bad) ok(`${n} sealed file(s) verified`);
    else if (bad && !RELEASE) console.warn(`   ⚠ ${bad}/${n + bad} file(s) differ from SEAL — Tasklet should re-seal; not blocking dev`);
  } catch (e) { sealIssue('SEAL.json parse error: ' + e.message); }
}

// ─── §3.2 · Substring externalization grep ────────────────────────────────────
head('§3.2  exclusion-token grep (leak guard)');
if (!fs.existsSync(TOKENS)) {
  fail('docs/EXCLUSION-TOKENS.txt missing — cannot run the leak guard');
} else {
  const pats = fs.readFileSync(TOKENS, 'utf8').split('\n')
    .map(l => l.trim()).filter(l => l && !l.startsWith('#'));
  // Allowlist: neutralize vetted partner-facing phrases (e.g. hospitality "guest privacy and
  // exclusivity") so the token is still caught everywhere else. Keep tiny + specific.
  let scanText = deployText;
  const ALLOWFILE = path.join(ROOT, 'docs', 'EXCLUSION-ALLOWLIST.txt');
  if (fs.existsSync(ALLOWFILE)) for (const phrase of fs.readFileSync(ALLOWFILE, 'utf8').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'))) {
    scanText = scanText.replace(new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), ' ');
  }
  let hits = 0;
  for (const p of pats) {
    let re; try { re = new RegExp(p, 'i'); } catch { console.warn('   (skipped un-compilable pattern: ' + p + ')'); continue; }
    const m = scanText.match(re);   // scan index.html + atlas-data.js (the full deployable surface), allowlist-neutralized
    if (m) { hits++; fail(`exclusion token matched /${p}/i → "${String(m[0]).slice(0,60)}"`); }
  }
  if (!hits) ok(`${pats.length} tokens checked · 0 hits${atlasData ? ' (index.html + atlas-data.js)' : ''}`);
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
  // Set the window.* data globals first (atlas-data.js runs before the app script in the browser),
  // then run the app script so its `const X = window.X` reads resolve, exactly as in production.
  if (atlasData) window.eval(atlasData);
  else throw new Error('atlas-data.js not found — run `node scripts/build.mjs` (data asset missing)');
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
  // Pitch CONTENT lives in atlas-data.js (window globals); the RENDER that consumes it lives in
  // index.html. If content exists but its render doesn't, the UI is dead — abort.
  const contentSrc = atlasData || html;
  const hasContent = /window\.CITY_BRIEFS\s*=/.test(contentSrc) || /window\.PARTNERS\s*=/.test(contentSrc);
  if (!hasContent) {
    ok('no pitch content (CITY_BRIEFS/PARTNERS) — render check skipped');
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
