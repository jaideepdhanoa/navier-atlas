/**
 * build-defense.mjs — emit gated /defense capability brief to _dist/defense/
 *
 * Source: deck-studio/microsite/contracts/defense.json (+ assets)
 * Hard gate: word-bounded leak_scan_terms_must_be_zero over renderable strings.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'deck-studio', 'microsite');
const CONTRACT = path.join(SRC, 'contracts', 'defense.json');
const TEMPLATE = path.join(ROOT, 'defense');
const INVEST_ASSETS = path.join(ROOT, 'handoff', 'invest-microsite');
const OUT = path.join(ROOT, '_dist', 'defense');

function ensureDir(d) {
  fs.mkdirSync(d, { recursive: true });
}
function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}
function stripUnderscore(obj) {
  if (obj == null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(stripUnderscore);
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    if (k.startsWith('_')) continue;
    out[k] = stripUnderscore(v);
  }
  return out;
}
function copyFile(src, dest) {
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
}
function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  ensureDir(dest);
  for (const name of fs.readdirSync(src)) {
    const s = path.join(src, name);
    const d = path.join(dest, name);
    if (fs.statSync(s).isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function collectRenderableStrings(obj, out, skipKeys = new Set(['render_notes', 'leak_scan_notes', 'global_render_rules', 'leak_scan_terms_must_be_zero', 'behavior', 'render', 'advisors_note', 'core_note', 'alt'])) {
  if (obj == null) return;
  if (typeof obj === 'string') {
    out.push(obj);
    return;
  }
  if (Array.isArray(obj)) {
    obj.forEach((x) => collectRenderableStrings(x, out, skipKeys));
    return;
  }
  if (typeof obj === 'object') {
    for (const [k, v] of Object.entries(obj)) {
      if (k.startsWith('_') || skipKeys.has(k)) continue;
      // skip media paths for leak content (filenames may contain YouTube ids)
      if ((k === 'src' || k === 'image' || k === 'poster') && typeof v === 'string' && v.includes('/')) continue;
      collectRenderableStrings(v, out, skipKeys);
    }
  }
}

function leakScan(contract) {
  const terms = contract.leak_scan_terms_must_be_zero || [];
  const strings = [];
  collectRenderableStrings(stripUnderscore(contract), strings);
  // Also scan joined page-ish text
  const blob = strings.join('\n');
  const hits = [];
  for (const term of terms) {
    const re = new RegExp(`\\b${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
    if (re.test(blob)) hits.push(term);
  }
  // Extra: no YouTube embed id for launch film on this route
  if (/aavaIZPkDyk/i.test(blob)) hits.push('youtube:aavaIZPkDyk');
  return hits;
}

function resolveAsset(rel) {
  const candidates = [
    path.join(SRC, rel),
    path.join(INVEST_ASSETS, rel),
    path.join(ROOT, rel),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

function gatherAssetRels(obj, out = new Set()) {
  if (!obj || typeof obj !== 'object') return out;
  if (Array.isArray(obj)) {
    obj.forEach((x) => gatherAssetRels(x, out));
    return out;
  }
  for (const [k, v] of Object.entries(obj)) {
    if (
      (k === 'src' || k === 'image' || k === 'poster') &&
      typeof v === 'string' &&
      !/^https?:/i.test(v) &&
      !v.startsWith('//')
    ) {
      out.add(v);
    } else if (v && typeof v === 'object') {
      gatherAssetRels(v, out);
    }
  }
  return out;
}

export function buildDefense() {
  if (!fs.existsSync(CONTRACT)) {
    console.warn('build-defense: no contract at', CONTRACT);
    return null;
  }
  const raw = readJson(CONTRACT);
  const hits = leakScan(raw);
  if (hits.length) {
    throw new Error(`defense leak-scan FAILED — hits: ${hits.join(', ')}`);
  }

  ensureDir(OUT);
  ensureDir(path.join(OUT, 'assets'));
  ensureDir(path.join(OUT, 'data'));

  // Copy templates
  fs.copyFileSync(path.join(TEMPLATE, 'defense.css'), path.join(OUT, 'defense.css'));
  fs.copyFileSync(path.join(TEMPLATE, 'defense.js'), path.join(OUT, 'defense.js'));

  // Client data (strip underscore)
  const client = stripUnderscore(raw);
  // Drop gate password from client bundle — middleware owns auth
  if (client.gate) {
    delete client.gate.password;
  }
  fs.writeFileSync(
    path.join(OUT, 'data', 'defense-data.js'),
    `/* GENERATED defense contract */\nwindow.DEFENSE_DATA = ${JSON.stringify(client)};\n`
  );

  // Team from invest claim + assets (advisors already on main)
  const claimPath = path.join(INVEST_ASSETS, 'contracts', 'claim.json');
  const assetsPath = path.join(INVEST_ASSETS, 'contracts', 'assets.json');
  let teamPeople = [];
  let teamAssets = { featured: '', cards: {} };
  if (fs.existsSync(claimPath)) {
    const claim = readJson(claimPath);
    const walk = (o) => {
      if (!o || typeof o !== 'object') return;
      if (Array.isArray(o)) return o.forEach(walk);
      if (Array.isArray(o.people) && o.people[0] && o.people[0].name) {
        teamPeople = o.people;
        return;
      }
      Object.values(o).forEach(walk);
    };
    walk(claim);
  }
  if (fs.existsSync(assetsPath)) {
    const assets = readJson(assetsPath);
    for (const block of assets.sections || []) {
      if (block.home === 'claim.team' && block.assets) {
        teamAssets = {
          featured: block.assets.featured || '',
          cards: block.assets.cards || {},
        };
      }
    }
  }
  // Ensure bio_url → url for advisors
  teamPeople = teamPeople.map((p) => {
    const out = { ...p };
    if (out.bio_url && !out.url) out.url = out.bio_url;
    return out;
  });
  fs.writeFileSync(
    path.join(OUT, 'data', 'defense-team.js'),
    `window.DEFENSE_TEAM = ${JSON.stringify({ people: stripUnderscore(teamPeople) })};\n` +
      `window.DEFENSE_TEAM_ASSETS = ${JSON.stringify(teamAssets)};\n`
  );

  // Copy referenced assets + closing plate + invest control/thesis/poster canon
  const rels = gatherAssetRels(raw);
  for (const must of [
    'assets/hero-loop.mp4',
    'assets/hero-poster.jpg',
    'assets/navier-launch-film-540p.mp4',
    'assets/deck/navier-launch-film-poster.jpg',
    'assets/deck/goldenhour-bow.jpg',
    'assets/deck/schematic-controls.png',
    'assets/deck/thesis-hangar-crane.jpg',
    'assets/demos/no-wake.mp4',
    'assets/demos/rough-seas.mp4',
    'assets/demos/flat-turning.mp4',
    'assets/stabilization-juxtaposition.mp4',
    'assets/defense-sofweek-loop.mp4',
    'assets/defense-sofweek-cockpit.mp4',
    'assets/defense-sofweek-approach.mp4',
    'assets/posters/S7WB91FvSFI.jpg',
    'assets/posters/Hlp9oynUQNE.jpg',
    'assets/posters/7HETK4rsByc.jpg',
    'assets/posters/93MCRJYsD_8.jpg',
    'assets/posters/QhiaYVgXMf0.jpg',
  ]) {
    rels.add(must);
  }
  for (const rel of rels) {
    const src = resolveAsset(rel);
    if (!src) throw new Error(`defense missing asset: ${rel}`);
    copyFile(src, path.join(OUT, rel));
  }

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Navier — Defense</title>
<meta name="robots" content="noindex,nofollow" />
<meta name="description" content="A standardized foiling platform changes how navies move." />
<meta name="theme-color" content="#0a0a0a" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/defense/defense.css" />
</head>
<body class="defense-page">
<div id="app"></div>
<script src="/defense/data/defense-data.js"></script>
<script src="/defense/data/defense-team.js"></script>
<script src="/defense/defense.js"></script>
</body>
</html>
`;
  fs.writeFileSync(path.join(OUT, 'index.html'), html);

  console.log(`defense → /defense/  (${(raw.sections || []).length} sections · noindex · gate password from contract/middleware)`);
  return { out: OUT, sections: (raw.sections || []).length };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  try {
    buildDefense();
  } catch (e) {
    console.error(e.message || e);
    process.exit(1);
  }
}
