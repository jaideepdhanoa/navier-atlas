#!/usr/bin/env node
// ─────────────────────────────────────────────────────────────────────────────
// build.mjs — Claude-owned build step (render lives in index.html; this injects DATA).
//
// OWNERSHIP CONTRACT (see DIVISION-OF-LABOR / DEPLOY-PROTOCOL):
//   • Tasklet delivers DATA into data-clean/: the 4 sealed blobs (FEATURES_BY_TYPE, ROUTES,
//     STORIES, VESSEL_SPECS) + the PUBLIC-STRIPPED pitch surface (city_briefs/*.json, partners/*.json,
//     keyed by city_id / partner_id). Per SEAL.json the website build MUST bake the pitch from
//     data-clean/ — NOT partner-pitch/ (the internal, un-stripped authoring tree). Tasklet never emits index.html.
//   • Claude owns index.html (the render) + this build + deploy.
//
// This reads data-clean/ and emits atlas-data.js — a single static asset that
// sets the window.* globals index.html consumes. index.html loads it via <script src>.
// One generator of the deployable data, so a build regen can't clobber the render.
// ─────────────────────────────────────────────────────────────────────────────
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { parseProfile, applyProfile, normalizeRouteBlob } from './build-profile.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DC = join(ROOT, 'data-clean');        // Tasklet's sealed blobs
const PITCH = join(ROOT, 'partner-pitch');   // Tasklet's pitch source of truth (city_briefs/, partners/)
const OUT = join(ROOT, 'atlas-data.js');

const readJson = (p) => JSON.parse(readFileSync(p, 'utf8'));

// Assemble a {key: value} map from a directory of per-record JSON files (sorted for stable diffs).
function assembleDir(dir, keyField) {
  const out = {};
  if (!existsSync(dir)) return out;
  for (const f of readdirSync(dir).filter((n) => n.endsWith('.json')).sort()) {
    const rec = readJson(join(dir, f));
    const key = (keyField && rec[keyField]) || f.replace(/\.json$/, '');
    out[key] = rec;
  }
  return out;
}

// Sealed blobs — Tasklet's source of record (hashed by data-clean/SEAL.json). Required.
const blobs = ['FEATURES_BY_TYPE', 'ROUTES', 'STORIES', 'VESSEL_SPECS'];
const data = {};
for (const name of blobs) {
  const p = join(DC, `${name}.json`);
  if (!existsSync(p)) { console.error(`[build] FATAL: missing sealed blob data-clean/${name}.json`); process.exit(1); }
  let blob = readJson(p);
  if (name === 'ROUTES') blob = normalizeRouteBlob(blob);
  data[name] = blob;
}
// Pitch content — keyed by city_id / partner_id. MUST bake from data-clean/{city_briefs,partners}/:
// these are the PUBLIC-STRIPPED, sealed ship surface (internal + deck_only tiers removed, per
// SEAL.json.pitch.note). partner-pitch/ is the INTERNAL, un-stripped authoring tree and is also stale
// — it is only a last-resort dev fallback when the data-clean pitch surface is absent.
const briefsDir   = existsSync(join(DC, 'city_briefs')) ? join(DC, 'city_briefs') : join(PITCH, 'city_briefs');
const partnersDir = existsSync(join(DC, 'partners'))    ? join(DC, 'partners')    : join(PITCH, 'partners');
if (briefsDir.startsWith(PITCH) || partnersDir.startsWith(PITCH))
  console.warn('[build] ⚠ data-clean pitch surface missing — falling back to partner-pitch/ (INTERNAL, un-stripped). NOT valid for prod.');
// Belt-and-suspenders: internal tiers must never reach the public artifact (see SEAL pitch.note).
function sanitizePartner(rec) {
  if (!rec || typeof rec !== 'object') return rec;
  const { deck_only, reviewer_notes, ...rest } = rec;
  return rest;
}
data.CITY_BRIEFS = assembleDir(briefsDir, 'city_id');
data.PARTNERS = Object.fromEntries(
  Object.entries(assembleDir(partnersDir, 'partner_id')).map(([k, v]) => [k, sanitizePartner(v)])
);
// Cluster briefs (NEW surface — country/archipelago-scale, keyed by cluster_id; each carries a `tier`:
// first-class iff a signature_route resolves to a built route, else tag-only). Baked like city_briefs.
const clusterDir = existsSync(join(DC, 'cluster_briefs')) ? join(DC, 'cluster_briefs') : join(PITCH, 'cluster_briefs');
data.CLUSTER_BRIEFS = assembleDir(clusterDir, 'cluster_id');
// Route unit-economics sidecar (economics_by_route_id.json) → keyed by route_id for O(1) join at render
// time. Presence of a record => the route has economics; absent => none (never invent). The grounding
// artifact (CORRIDOR-ENDPOINT-GROUNDING.json) is internal QA provenance — deliberately not baked.
const econPath = join(DC, 'economics_by_route_id.json');
data.ROUTE_ECONOMICS = {};
if (existsSync(econPath)) { const econ = readJson(econPath); for (const r of (econ.records || [])) if (r && r.route_id) data.ROUTE_ECONOMICS[r.route_id] = r; }
// Cluster lookup (sealed CLUSTERS.json): cluster_id → {label, region, type, anchor [lng,lat], member_city_ids}.
// Pairs with the cluster_id now tagged on city nodes + the cluster_briefs surface to drive cluster nav.
const clustersPath = join(DC, 'CLUSTERS.json');
data.CLUSTERS = existsSync(clustersPath) ? readJson(clustersPath) : { clusters: [] };

// Defensive strip: internal classification fields that must never reach the public artifact. The render
// never reads these. Belt-and-suspenders over Tasklet's externalizer — the 2026-06-01 P0+P1 reseal leaked
// `posture` (P0/P1/P2/Watch) + `archetype_scores` onto city features (both on the EXCLUSION blocklist).
// Stripping here keeps the sealed source intact (seal still verifies) while the deployed atlas-data.js
// stays clean. Safe to keep permanently; remove only if these ever become intended-public fields.
const STRIP_PROPS = ['posture', 'archetype_scores', 'archetype_fit'];
const STRIP_POI_PROPS = ['linked_locale', 'linked_subcluster', 'validation_log', 'source_chain', 'operator', 'notes'];
const isPitchTrapPoi = (f) => {
  const p = f?.properties;
  if (!p) return false;
  const blob = `${p.id || ''} ${p.name || ''} ${p._handoff_bp_id || ''}`.toLowerCase();
  return blob.includes('pitch-trap') || blob.includes('pitch trap');
};
for (const t of Object.keys(data.FEATURES_BY_TYPE || {})) {
  if (t === 'poi') {
    data.FEATURES_BY_TYPE.poi = (data.FEATURES_BY_TYPE[t] || []).filter((f) => !isPitchTrapPoi(f));
    for (const f of data.FEATURES_BY_TYPE.poi)
      if (f?.properties) {
        for (const k of STRIP_PROPS) delete f.properties[k];
        for (const k of STRIP_POI_PROPS) delete f.properties[k];
      }
    continue;
  }
  for (const f of (data.FEATURES_BY_TYPE[t] || []))
    if (f?.properties) for (const k of STRIP_PROPS) delete f.properties[k];
}
// City-brief index + records can carry internal posture stamps — strip before public bake.
for (const rec of Object.values(data.CITY_BRIEFS || {})) {
  if (!rec || typeof rec !== 'object') continue;
  if (Array.isArray(rec.index)) for (const row of rec.index) {
    if (!row || typeof row !== 'object') continue;
    for (const k of STRIP_PROPS) delete row[k];
    delete row.posture_note;
  }
  for (const k of STRIP_PROPS) delete rec[k];
  delete rec.posture_note;
  delete rec.internal;
  if (rec.partner_overlays && typeof rec.partner_overlays === 'object') {
    for (const ov of Object.values(rec.partner_overlays)) {
      if (!ov || typeof ov !== 'object') continue;
      delete ov.wedge;
      delete ov.posture;
      delete ov.posture_note;
      delete ov.internal;
      for (const k of STRIP_PROPS) delete ov[k];
    }
  }
}

const profile = parseProfile();
const baked = applyProfile(data, profile);

const banner = `/* GENERATED by scripts/build.mjs from data-clean/ — do not edit by hand.\n` +
  `   Tasklet delivers data into data-clean/; Claude builds this asset + deploys. */\n` +
  `/* profile: ${profile} */\n`;
const body = Object.entries(baked)
  .map(([k, v]) => `window.${k}=${JSON.stringify(v)};`)
  .join('\n');
writeFileSync(OUT, banner + body + '\n');

const fc = data.FEATURES_BY_TYPE, ftypes = Object.keys(fc);
const nodes = ftypes.reduce((n, t) => n + (fc[t] ? fc[t].length : 0), 0);
console.log(`[build] atlas-data.js written (${(readFileSync(OUT).length / 1e6).toFixed(2)} MB) · profile:${profile}`);
console.log(`[build]   features: ${nodes} across ${ftypes.length} types · routes: ${baked.ROUTES.length} · stories: ${baked.STORIES.length}`);
console.log(`[build]   city briefs: ${Object.keys(baked.CITY_BRIEFS).length} · partners: ${Object.keys(baked.PARTNERS).length} · cluster briefs: ${Object.keys(baked.CLUSTER_BRIEFS).length} · route-economics: ${Object.keys(baked.ROUTE_ECONOMICS).length}`);

if (process.env.RELEASE || process.env.BUILD_ENFORCE_CITY_IDS) {
  const gate = spawnSync('python3', ['scripts/backfill_route_city_ids.py', '--assert-build'], {
    cwd: ROOT, encoding: 'utf8',
  });
  if (gate.stdout) process.stdout.write(gate.stdout);
  if (gate.stderr) process.stderr.write(gate.stderr);
  if (gate.status !== 0) {
    console.error('[build] FATAL: route *_city_id gate failed — run scripts/backfill_route_city_ids.py --apply');
    process.exit(1);
  }
  console.log('[build]   route city_id gate: pass (<5% non-gold)');
}
