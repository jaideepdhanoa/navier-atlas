#!/usr/bin/env node
/**
 * build-story.mjs — emit public /story outreach proof reel to _dist/story/
 *
 * Source: handoff/story-microsite/contracts/{site,story,assets}.json
 * Rules: authored strings only; 31-term leak scan fails the build; no password.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'handoff', 'story-microsite');
const TEMPLATE = path.join(ROOT, 'story');
const OUT = path.join(ROOT, '_dist', 'story');
const HERO_BUDGET_BYTES = 4 * 1024 * 1024;

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
function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
function copyFile(src, dest) {
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
}

function resolveRepoPath(rel) {
  if (!rel || typeof rel !== 'string') return null;
  const candidates = [
    path.join(ROOT, rel),
    path.join(SRC, rel),
    path.join(ROOT, 'handoff', 'invest-microsite', rel),
    path.join(ROOT, 'handoff', 'invest-microsite', 'assets', rel.replace(/^assets\//, '')),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

/** Map a source repo path into a stable /story/assets/... URL path. */
function distAssetRel(assetKey, srcAbs) {
  const ext = path.extname(srcAbs) || '.bin';
  return `assets/${assetKey}${ext}`;
}

function collectRenderableStrings(obj, out) {
  if (obj == null) return;
  if (typeof obj === 'string') {
    out.push(obj);
    return;
  }
  if (Array.isArray(obj)) {
    obj.forEach((x) => collectRenderableStrings(x, out));
    return;
  }
  if (typeof obj === 'object') {
    for (const [k, v] of Object.entries(obj)) {
      if (k.startsWith('_')) continue;
      // Skip media paths / ids — filenames may contain banned substrings
      if (
        (k === 'path' || k === 'asset' || k === 'poster' || k === 'youtube_id' || k === 'url' || k === 'value') &&
        typeof v === 'string' &&
        (v.includes('/') || /^https?:/i.test(v) || /@/.test(v) || /^[A-Za-z0-9_-]{6,}$/.test(v))
      ) {
        // Still scan mailto subjects / visible labels — but skip pure URLs and asset paths
        if (k === 'url' || k === 'path' || k === 'asset' || k === 'poster' || k === 'youtube_id') continue;
        if (k === 'value' && (/^https?:/i.test(v) || v.includes('/') || v.startsWith('mailto:'))) continue;
      }
      collectRenderableStrings(v, out);
    }
  }
}

function leakScanTerms(rawStory) {
  return (rawStory._leak_scan && rawStory._leak_scan.terms) || [];
}

function termRegex(term) {
  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // Phrases / symbol-heavy terms ($120M, B-1): literal match. Single tokens: word-bounded
  // so "SAFE" does not hit "safety", "royal" does not hit unrelated stems.
  if (/\s/.test(term) || /[^A-Za-z0-9]/.test(term)) {
    return new RegExp(escaped, 'i');
  }
  return new RegExp(`\\b${escaped}\\b`, 'i');
}

function runLeakScan(label, text, terms) {
  const hits = [];
  for (const term of terms) {
    if (termRegex(term).test(text)) hits.push(term);
  }
  // Dollar figures other than $10M / $100M
  const dollars = text.match(/\$[\d,]+(?:\.\d+)?\s*[MBKmbk]?/g) || [];
  for (const d of dollars) {
    const norm = d.replace(/\s+/g, '').toUpperCase();
    if (norm === '$10M' || norm === '$100M') continue;
    hits.push(`dollar:${d}`);
  }
  if (hits.length) {
    throw new Error(`${label} leak-scan FAILED — hits: ${hits.join(', ')}`);
  }
}

function gatherAssetKeys(story) {
  const keys = new Set();
  const walk = (o) => {
    if (!o || typeof o !== 'object') return;
    if (Array.isArray(o)) return o.forEach(walk);
    if (typeof o.asset === 'string') keys.add(o.asset);
    if (o.media && typeof o.media === 'object' && !Array.isArray(o.media) && o.media.asset) {
      keys.add(o.media.asset);
    }
    Object.values(o).forEach(walk);
  };
  walk(story);
  return keys;
}

function normalizeAssetDefs(rawAssets) {
  const raw = rawAssets.assets || {};
  if (Array.isArray(raw)) {
    const out = {};
    for (const a of raw) {
      if (a && a.id) out[a.id] = a;
    }
    return out;
  }
  return raw;
}

function assertCanonicalHeadlines(story) {
  const invest = path.join(ROOT, 'handoff', 'invest-microsite', 'contracts');
  const hero = readJson(path.join(invest, 'hero.json'));
  const proof = readJson(path.join(invest, 'proof.json'));
  const product = readJson(path.join(invest, 'product.json'));
  const money = readJson(path.join(invest, 'money.json'));
  const byId = Object.fromEntries((story.sections || []).map((s) => [s.id, s]));
  const demo = (proof.sections || []).find((s) => s.id === 'demo-grid') || {};
  const cto = (product.sections || []).find((s) => s.video && s.video.youtube_id === 'S7WB91FvSFI') || {};
  const sam = (product.sections || []).find((s) => s.video && s.video.youtube_id === 'QhiaYVgXMf0') || {};
  const vance = (money.sections || []).find((s) => s.id === 'go-deeper') || {};
  const checks = [
    ['hero.play_button_label', byId.hero?.play_button_label, hero.play_button_label],
    ['hero.film.title', byId.hero?.film?.title, hero.video?.title],
    ['ride.headline', byId.ride?.headline, demo.title],
    ['ride.lede', byId.ride?.lede, demo.lede],
  ];
  const storyClips = byId.ride?.clips || [];
  const srcClips = demo.clips || [];
  srcClips.forEach((c, i) => {
    const got = storyClips[i] || {};
    checks.push([`ride.clips[${i}].title`, got.title, c.title]);
    checks.push([`ride.clips[${i}].caption`, got.caption, c.caption]);
    checks.push([`ride.clips[${i}].duration`, got.duration, c.duration]);
  });
  const films = byId.films?.films || [];
  checks.push(['films[0].youtube_id', films[0]?.youtube_id, 'QhiaYVgXMf0']);
  checks.push(['films[0].title', films[0]?.title, sam.headline]);
  checks.push(['films[1].youtube_id', films[1]?.youtube_id, 'S7WB91FvSFI']);
  checks.push(['films[1].title', films[1]?.title, cto.video_label]);
  checks.push(['films[2].youtube_id', films[2]?.youtube_id, 'ZNgh39DM_Jg']);
  checks.push(['films[2].title', films[2]?.title, vance.video_label]);
  const dual = (readJson(path.join(invest, 'gtm.json')).sections || []).find(
    (s) => s.id === 'dual-use' || /dual-use/i.test(s.id || '') || /Dual-Use/i.test(s.title || '')
  ) || {};
  const fieldCaps = (byId.field?.media || []).map((m) => m.caption);
  const wantCaps = [
    dual.media?.lead_video?.caption,
    ...(dual.media?.secondary_videos || []).map((v) => v.caption),
    (dual.media?.photos || [])[0]?.caption,
  ].filter(Boolean);
  wantCaps.forEach((cap, i) => {
    checks.push([`field.media[${i}].caption`, fieldCaps[i], cap]);
  });
  const mismatches = checks.filter(([, got, want]) => got !== want);
  if (mismatches.length) {
    const detail = mismatches
      .map(([k, got, want]) => `  ${k}\n    got:  ${JSON.stringify(got)}\n    want: ${JSON.stringify(want)}`)
      .join('\n');
    throw new Error(`story headline byte-diff FAILED — sourced titles must match /invest contracts:\n${detail}`);
  }
}

export function buildStory() {
  const sitePath = path.join(SRC, 'contracts', 'site.json');
  const storyPath = path.join(SRC, 'contracts', 'story.json');
  const assetsPath = path.join(SRC, 'contracts', 'assets.json');
  if (!fs.existsSync(sitePath) || !fs.existsSync(storyPath) || !fs.existsSync(assetsPath)) {
    console.warn('build-story: contracts missing — skip');
    return false;
  }
  for (const f of ['story.css', 'story.js']) {
    if (!fs.existsSync(path.join(TEMPLATE, f))) {
      throw new Error(`build-story: missing template ${path.join(TEMPLATE, f)}`);
    }
  }

  const rawSite = readJson(sitePath);
  const rawStory = readJson(storyPath);
  const rawAssets = readJson(assetsPath);
  const terms = leakScanTerms(rawStory);

  // Pre-emit leak scan on authored renderable strings
  const strings = [];
  collectRenderableStrings(stripUnderscore(rawStory), strings);
  collectRenderableStrings(stripUnderscore(rawSite), strings);
  runLeakScan('story contracts', strings.join('\n'), terms);

  const site = stripUnderscore(rawSite);
  const story = stripUnderscore(rawStory);
  const assetsManifest = stripUnderscore(rawAssets);
  assertCanonicalHeadlines(rawStory);

  ensureDir(OUT);
  ensureDir(path.join(OUT, 'assets'));
  ensureDir(path.join(OUT, 'data'));
  ensureDir(path.join(OUT, 'assets', 'posters'));

  // Resolve + copy referenced assets; rewrite client paths to /story/assets/...
  const assetMap = {}; // key → /story/assets/...
  const missing = [];
  const keys = gatherAssetKeys(rawStory);
  // Always include hero poster for ambient poster-first
  const assetDefs = normalizeAssetDefs(rawAssets);
  for (const key of keys) {
    const def = assetDefs[key];
    if (def && (def.class === 'map-component' || def.path == null)) {
      continue; // atlas globe is a live map, not a file
    }
    if (!def || !def.path) {
      missing.push(`${key} (no path in assets.json)`);
      continue;
    }
    let src = resolveRepoPath(def.path);
    // Hero budget: if ambient hero candidate is oversized, fall back to hero-loop
    if (key === 'loop_takeoff' && src) {
      const size = fs.statSync(src).size;
      if (size > HERO_BUDGET_BYTES) {
        const fb = resolveRepoPath('handoff/invest-microsite/assets/hero-loop.mp4');
        if (fb && path.resolve(fb) !== path.resolve(src)) {
          console.warn(
            `build-story: ${key} is ${(size / 1024 / 1024).toFixed(1)}MB > 4MB — using hero-loop.mp4`
          );
          src = fb;
        } else if (size > HERO_BUDGET_BYTES * 1.3) {
          console.warn(
            `build-story: ${key} is ${(size / 1024 / 1024).toFixed(1)}MB (hero budget 4MB) — no smaller fallback`
          );
        }
      }
    }
    if (!src) {
      missing.push(`${key}: ${def.path}`);
      continue;
    }
    const rel = distAssetRel(key, src);
    copyFile(src, path.join(OUT, rel));
    assetMap[key] = `/story/${rel}`;
  }

  // YouTube posters used by film cards
  const ytIds = new Set();
  for (const sec of rawStory.sections || []) {
    for (const fc of [...(sec.film_cards || []), ...(sec.films || [])]) {
      if (fc.youtube_id) ytIds.add(fc.youtube_id);
    }
  }
  for (const id of ytIds) {
    const src =
      resolveRepoPath(`handoff/invest-microsite/assets/posters/${id}.jpg`) ||
      resolveRepoPath(`assets/posters/${id}.jpg`);
    if (src) {
      const rel = `assets/posters/${id}.jpg`;
      copyFile(src, path.join(OUT, rel));
      assetMap[`yt_${id}`] = `/story/${rel}`;
    } else {
      // Fallback: YouTube maxresdefault URL left to client
      assetMap[`yt_${id}`] = `https://img.youtube.com/vi/${id}/maxresdefault.jpg`;
    }
  }

  // Launch film poster
  const launchPoster =
    resolveRepoPath('handoff/invest-microsite/assets/deck/navier-launch-film-poster.jpg') ||
    resolveRepoPath('handoff/invest-microsite/assets/hero-poster.jpg');
  if (launchPoster) {
    const rel = 'assets/posters/film_launch_1080.jpg';
    copyFile(launchPoster, path.join(OUT, rel));
    assetMap.film_launch_1080_poster = `/story/${rel}`;
  }

  // Hero still poster (poster-first mobile)
  const heroPoster = resolveRepoPath('handoff/invest-microsite/assets/hero-poster.jpg');
  if (heroPoster) {
    const rel = 'assets/hero-poster.jpg';
    copyFile(heroPoster, path.join(OUT, rel));
    assetMap.hero_poster = `/story/${rel}`;
  }

  if (missing.length) {
    throw new Error(`story assets missing:\n  ${missing.join('\n  ')}`);
  }

  // Client bundle — never ship leak list
  const client = {
    site,
    story,
    assets: assetMap,
    badges: Object.fromEntries(
      Object.entries(assetDefs).map(([k, v]) => [k, (v && v.badge) || 'FILMED'])
    ),
  };
  fs.writeFileSync(
    path.join(OUT, 'data', 'story-data.js'),
    `/* GENERATED /story — authored contracts only */\nwindow.STORY_DATA = ${JSON.stringify(client)};\n`
  );

  fs.copyFileSync(path.join(TEMPLATE, 'story.css'), path.join(OUT, 'story.css'));
  fs.copyFileSync(path.join(TEMPLATE, 'story.js'), path.join(OUT, 'story.js'));

  const title = site.title || 'Navier';
  const desc = (site.og && site.og.description) || 'Watch the films. Read the coverage.';
  const ogImage = assetMap.photo_goldengate || assetMap.hero_poster || '';
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>${escapeHtml(title)}</title>
<meta name="robots" content="${escapeHtml(site.robots_meta || 'noindex,nofollow')}" />
<meta name="description" content="${escapeHtml(desc)}" />
<meta property="og:title" content="${escapeHtml((site.og && site.og.title) || title)}" />
<meta property="og:description" content="${escapeHtml(desc)}" />
<meta property="og:type" content="website" />
${ogImage ? `<meta property="og:image" content="${escapeHtml(ogImage)}" />` : ''}
<meta name="theme-color" content="#070708" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/story/story.css" />
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body class="story-page">
<div id="app"></div>
<script src="/story/data/story-data.js"></script>
<script src="/story/story.js"></script>
</body>
</html>
`;
  fs.writeFileSync(path.join(OUT, 'index.html'), html);

  // Post-emit leak scan on built HTML + data blob only (not template JS — code may share English words)
  const builtBlob =
    fs.readFileSync(path.join(OUT, 'index.html'), 'utf8') +
    '\n' +
    fs.readFileSync(path.join(OUT, 'data', 'story-data.js'), 'utf8');
  runLeakScan('story built output', builtBlob, terms);

  console.log(
    `story → /story/  (${(story.sections || []).length} sections · noindex · public · ${keys.size} assets)`
  );
  return true;
}

const isMain =
  process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  try {
    buildStory();
  } catch (e) {
    console.error(e.message || e);
    process.exit(1);
  }
}
