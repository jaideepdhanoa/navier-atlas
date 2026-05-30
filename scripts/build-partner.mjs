#!/usr/bin/env node
// ─────────────────────────────────────────────────────────────────────────────
// Navier Atlas — per-partner build (DIVISION-OF-LABOR / PARTNER-VIEWS.md §3+§5)
//
//   node scripts/build-partner.mjs <slug> [<index.html>]
//
// Emits a SCOPED, LOCKED per-partner build at _dist/<slug>/index.html that:
//   1. keeps ONLY the partner's cities (resolved from PARTNERS[slug].phases[].cities) plus the
//      POIs / ROUTES / STORIES / CITY_BRIEFS reachable from them, and only PARTNERS[slug];
//   2. injects <script>window.__PARTNER_BUILD__='<slug>'</script> ahead of the app (lock);
//   3. runs the exclusion-token grep (docs/EXCLUSION-TOKENS.txt) AND a cross-partner sweep
//      (no OTHER partner's id / display name). Any hit ⇒ abort, nothing written.
//
// Works on the repo template (FEATURES_BY_TYPE/ROUTES/STORIES inlined as `const X = …;`;
// CITY_BRIEFS/PARTNERS still `__…__` tokens, read here from data-clean/), or on a built file.
//
// NOTE (flagged to Tasklet): true isolation depends on canonical route→city ids. Until ROUTES
// carry from_city_id/to_city_id, city resolution is best-effort (id · "city__sub" · parent_city_id).
// The render-side build lock already prevents switching partners regardless of scoping.
// ─────────────────────────────────────────────────────────────────────────────
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const slug = process.argv[2];
const INPUT = process.argv[3] || path.join(ROOT, 'index.html');
if (!slug) { console.error('usage: build-partner.mjs <slug> [index.html]'); process.exit(2); }

let html = fs.readFileSync(INPUT, 'utf8');

// ---- briefs / partners: prefer data-clean source; fall back to inlined token/JSON ----
const readDir = (d) => { const o={}; const p=path.join(ROOT,'data-clean',d);
  if (fs.existsSync(p)) for (const fn of fs.readdirSync(p)) if (fn.endsWith('.json')){ const j=JSON.parse(fs.readFileSync(path.join(p,fn),'utf8')); o[j.city_id||j.partner_id]=j; } return o; };
const CITY_BRIEFS = readDir('city_briefs');
const PARTNERS    = readDir('partners');
const partner = PARTNERS[slug];
if (!partner) { console.error(`partner "${slug}" not found in data-clean/partners (have: ${Object.keys(PARTNERS).join(', ')})`); process.exit(1); }

// ---- extract an inlined `const NAME = <json>;` (each on its own line) ----
function readConst(name){
  const m = html.match(new RegExp('^const ' + name + ' = (.*);\\s*$', 'm'));
  if (!m) return { found:false };
  try { return { found:true, value: JSON.parse(m[1]), raw:m[0] }; }
  catch(e){ console.error(`parse ${name}: ${e.message}`); process.exit(1); }
}
const FBT = readConst('FEATURES_BY_TYPE'), RT = readConst('ROUTES'), ST = readConst('STORIES');
if (!FBT.found || !RT.found) { console.error('FEATURES_BY_TYPE / ROUTES not inlined in input'); process.exit(1); }

// ---- resolve the partner's cities to real node ids (mirrors render _cityIdOf/_resolvePhaseCities) ----
const cityIds = new Set([...(FBT.value.city||[]), ...(FBT.value.priority_city||[])].map(f=>f.properties && f.properties.id).filter(Boolean));
const nodeIndex = {}; for (const t of Object.keys(FBT.value)) for (const f of FBT.value[t]){ const p=f.properties; if(p&&p.id) nodeIndex[p.id]=p; }
const cityIdOf = (id) => {
  if (!id) return null;
  if (cityIds.has(id)) return id;
  const p = nodeIndex[id];
  if (p && cityIds.has(p.parent_city_id)) return p.parent_city_id;
  const pre = String(id).split('__')[0];
  return cityIds.has(pre) ? pre : null;
};
const resolve = (loose) => {
  const out = new Set();
  for (const c of (loose||[])){
    if (cityIds.has(c)){ out.add(c); continue; }
    const x = String(c).toLowerCase();
    for (const id of cityIds){ const a=id.toLowerCase();
      if (a===x || a.startsWith(x+'-') || a.startsWith(x+'_') || a.split(/[-_]/).includes(x)) out.add(id); }
  }
  return out;
};
const keepCities = new Set();
for (const ph of (partner.phases||[])) for (const c of resolve(ph.cities)) keepCities.add(c);
if (!keepCities.size) { console.error('no cities resolved for partner — aborting'); process.exit(1); }

// ---- scope each data layer ----
const scopedRoutes = (RT.value||[]).filter(f => { const p=f.properties||{}; return keepCities.has(cityIdOf(p.from)) || keepCities.has(cityIdOf(p.to)); });
const endpointIds = new Set();
for (const f of scopedRoutes){ const p=f.properties||{}; if(p.from) endpointIds.add(p.from); if(p.to) endpointIds.add(p.to); }
const scopedFBT = {};
for (const t of Object.keys(FBT.value)){
  scopedFBT[t] = FBT.value[t].filter(f => { const p=f.properties||{};
    if (t==='city'||t==='priority_city') return keepCities.has(p.id);
    return keepCities.has(p.parent_city_id) || endpointIds.has(p.id); });
}
const scopedBriefs = {}; for (const [cid,b] of Object.entries(CITY_BRIEFS)) if (keepCities.has(cid)) scopedBriefs[cid]=b;
const scopedStories = (ST.found?ST.value:[]).filter(s => [...(s.scope_city_ids||[]), ...((s.narrative||[]).map(n=>n&&n.city_id))].filter(Boolean).some(c=>keepCities.has(c)));
const scopedPartners = { [slug]: partner };

// ---- re-inline scoped consts + substitute brief/partner tokens (or inlined try-block) ----
let out = html;
out = out.replace(FBT.raw, `const FEATURES_BY_TYPE = ${JSON.stringify(scopedFBT)};`);
out = out.replace(RT.raw,  `const ROUTES = ${JSON.stringify(scopedRoutes)};`);
if (ST.found) out = out.replace(ST.raw, `const STORIES = ${JSON.stringify(scopedStories)};`);
const sub = (token, reAssign, value) => {
  const json = JSON.stringify(value);
  if (out.includes(token)) out = out.replace(token, json);
  else out = out.replace(reAssign, (m,p1)=>p1+json+';'); // already-substituted try-block form
};
sub('__CITY_BRIEFS__', /(CITY_BRIEFS = )(?:\{[\s\S]*?\}|\[[\s\S]*?\]);(?= \} catch)/, scopedBriefs);
sub('__PARTNERS__',    /(PARTNERS = )(?:\{[\s\S]*?\}|\[[\s\S]*?\]);(?= \} catch)/,    scopedPartners);
// Locked build: drop other partners' PARTNER_VIEWS entries (the lock + PARTNERS data drive activation).
out = out.replace(/const PARTNER_VIEWS = \{[\s\S]*?\n\};/, 'const PARTNER_VIEWS = {};');

// ---- inject the build lock ahead of the first <script> ----
const lock = `<script>window.__PARTNER_BUILD__=${JSON.stringify(slug)};</script>\n`;
const si = out.indexOf('<script>');
out = out.slice(0,si) + lock + out.slice(si);

// ---- safety sweeps ----
const lower = out.toLowerCase();
let leaks = [];
const tokFile = path.join(ROOT,'docs','EXCLUSION-TOKENS.txt');
if (fs.existsSync(tokFile)) for (const line of fs.readFileSync(tokFile,'utf8').split('\n')){
  const t=line.trim(); if(!t||t.startsWith('#')) continue;
  try { if (new RegExp(t,'i').test(out)) leaks.push(t); } catch(e){}
}
// Distinctive signals only (avoid common-word false positives like the verb "grab"):
// another partner's hero.title (long, unique) or its partner_id used as a JSON/object key.
const crossHits = [];
for (const [pid,pr] of Object.entries(PARTNERS)){ if(pid===slug) continue;
  if ((pr.hero && pr.hero.title && out.includes(pr.hero.title)) || out.includes('"'+pid+'":')) crossHits.push(pid); }

const report = { slug, input:path.relative(ROOT,INPUT), keptCities:[...keepCities],
  counts:{ cities:(scopedFBT.city||[]).length, priority:(scopedFBT.priority_city||[]).length, pois:(scopedFBT.poi||[]).length,
    routes:scopedRoutes.length, stories:scopedStories.length, briefs:Object.keys(scopedBriefs).length, partners:1 },
  leaks, crossHits };
if (leaks.length || crossHits.length){ console.error('ABORT — safety sweep failed:\n', JSON.stringify(report,null,2)); process.exit(1); }

const outDir = path.join(ROOT,'_dist',slug);
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,'index.html'), out);
fs.writeFileSync(path.join(ROOT,'_dist','vercel.json'), JSON.stringify({cleanUrls:true},null,2)+'\n');
console.log('✅ built', path.relative(ROOT,path.join(outDir,'index.html')));
console.log(JSON.stringify(report,null,2));
