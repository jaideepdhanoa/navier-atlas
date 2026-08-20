#!/usr/bin/env node
/**
 * build-invest.mjs — emit Series B investor microsite (+ teaser) to _dist/
 *
 * Source of truth: handoff/invest-microsite/contracts/*.json
 * Rule: render authored data only; strip underscore fields.
 *
 *   _dist/invest/  — full Series B site
 *   _dist/teaser/  — streamlined teaser (filtered sections + discrete pipeline)
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'handoff', 'invest-microsite');
const TEMPLATE = path.join(ROOT, 'invest');

/** Sections dropped from /teaser (keep Maldives + Gulf + discrete pipeline + Go Deeper + finale). */
const TEASER_EXCLUDE = {
  product: new Set(['quanta-unlocks', 'competitive']),
  gtm: new Set([
    'revenue-lines',
    'unit-econ',
    // Round-6h: keep cargo-gap + dual-use on /teaser
    'cargo-play',
    'sealift',
    'day-night-wedge',
    'offshore',
    'market-floor',
    'pipeline',
  ]),
  money: new Set([
    'operating-plan',
    'ramp-charts',
    'roadmap',
    'five-markets',
    'the-round',
  ]),
};

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

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function ensureDir(d) {
  fs.mkdirSync(d, { recursive: true });
}

function copyDir(src, dest) {
  ensureDir(dest);
  for (const name of fs.readdirSync(src)) {
    const s = path.join(src, name);
    const d = path.join(dest, name);
    if (fs.statSync(s).isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function discretePipelineSection(pipelineMap) {
  const p = pipelineMap || {};
  return {
    id: 'discrete-pipeline',
    type: 'discrete-pipeline',
    kicker: '04 · GTM — THE PIPELINE',
    eyebrow: p.eyebrow || 'THE PIPELINE',
    // Teaser discrete plate — market thesis title + pipeline KPIs (not the live map)
    title: 'From One Nation to a Global Network',
    gold_stats: p.gold_stats || [],
    takeaways: [
      {
        body: '100+ prospects across 672 corridors · 385 cities · 79 countries.',
      },
      {
        body: 'Strategic acquisitions under review as catalyst for capability expansion',
      },
      {
        title: 'THE TEN-YEAR FLOOR — REPLACEMENT ONLY',
        body: '≈ 13,000 vessels',
        emphasis: true,
      },
    ],
    art: {
      asset: 'assets/deck/n180-morpheus-hero.png',
      alt: 'Morpheus 180 — ship-scale foiling landing craft',
    },
  };
}

function applyTeaserFilter(bundle) {
  const out = structuredClone(bundle);

  out.site = {
    ...out.site,
    title: 'Navier — Teaser · OWN THE EDGE',
    route: '/teaser',
    base_path: '/teaser',
    og: {
      ...(out.site.og || {}),
      title: 'Navier — Teaser',
      description: 'OWN THE EDGE',
    },
  };

  // Drop Money chapter from sticky nav when it only holds Go Deeper + finale
  if (out.site.nav && Array.isArray(out.site.nav.chapters)) {
    out.site.nav.chapters = out.site.nav.chapters.filter((c) => c.id !== 'money');
  }

  for (const [chapter, drop] of Object.entries(TEASER_EXCLUDE)) {
    if (!out[chapter] || !Array.isArray(out[chapter].sections)) continue;
    out[chapter].sections = out[chapter].sections.filter((s) => !drop.has(s.id));
  }

  // Insert discrete pipeline after Gulf (Maldives → Gulf → Discrete Pipeline → …)
  if (out.gtm && Array.isArray(out.gtm.sections)) {
    const sections = out.gtm.sections.filter((s) => s.id !== 'discrete-pipeline');
    const gulfIdx = sections.findIndex((s) => s.id === 'gulf');
    const insertAt = gulfIdx >= 0 ? gulfIdx + 1 : sections.length;
    sections.splice(insertAt, 0, discretePipelineSection(out['pipeline-map']));
    out.gtm.sections = sections;
  }

  // Soften money chapter label — only Go Deeper + Own the Edge remain
  if (out.money) {
    out.money.chapter_label = '';
  }

  return out;
}

function emitSite({ basePath, distRel, bundle, label }) {
  const DIST = path.join(ROOT, '_dist', distRel);
  ensureDir(DIST);
  ensureDir(path.join(DIST, 'data'));
  ensureDir(path.join(DIST, 'assets'));

  // Per-contract JSON + single blob
  for (const [name, data] of Object.entries(bundle)) {
    fs.writeFileSync(
      path.join(DIST, 'data', `${name}.json`),
      JSON.stringify(data),
    );
  }
  fs.writeFileSync(
    path.join(DIST, 'data', 'invest-data.js'),
    `window.INVEST_DATA = ${JSON.stringify(bundle)};\n`,
  );

  // Assets from handoff + invest/ extras
  const assetSrc = path.join(SRC, 'assets');
  if (fs.existsSync(assetSrc)) copyDir(assetSrc, path.join(DIST, 'assets'));
  const localAssets = path.join(TEMPLATE, 'assets');
  if (fs.existsSync(localAssets)) copyDir(localAssets, path.join(DIST, 'assets'));

  // Verify every assets.json path exists
  if (bundle.assets) {
    const missing = [];
    const checkPath = (rel) => {
      if (!rel || typeof rel !== 'string') return;
      const candidates = [
        path.join(SRC, rel),
        path.join(SRC, 'assets', rel.replace(/^assets\//, '')),
        path.join(DIST, 'assets', rel.replace(/^assets\//, '')),
      ];
      if (!candidates.some((c) => fs.existsSync(c))) missing.push(rel);
    };
    const walk = (v) => {
      if (!v) return;
      if (typeof v === 'string') {
        if (/^assets\//.test(v) || /\.(png|jpe?g|gif|webp|mp4|webm|svg)$/i.test(v)) {
          checkPath(v);
        }
        return;
      }
      if (Array.isArray(v)) v.forEach((x) => walk(x));
      else if (typeof v === 'object') {
        for (const [k, x] of Object.entries(v)) {
          if (
            k === 'note' ||
            k === 'treatment' ||
            k === 'behavior' ||
            k === 'exception' ||
            k === 'alt' ||
            k === 'caption' ||
            k === 'purpose' ||
            k === 'provenance' ||
            k === 'resolution_note' ||
            k === 'pending' ||
            k === 'status'
          ) {
            continue;
          }
          walk(x);
        }
      }
    };
    walk(bundle.assets.hero);
    walk(bundle.assets.sections);
    walk(bundle.assets.slots);
    walk(bundle.assets.chapter_dividers);
    // Teaser also needs discrete-pipeline art
    if (bundle.gtm) {
      for (const sec of bundle.gtm.sections || []) {
        if (sec.art && sec.art.asset) checkPath(sec.art.asset);
      }
    }
    if (missing.length) {
      console.error(`FATAL ${label} assets missing on disk:\n  ` + missing.join('\n  '));
      process.exit(1);
    }
  }

  // Template CSS/JS (+ Network Shift reference engine + pipeline geo)
  for (const f of ['invest.css', 'invest.js', 'network-shift.js', 'pipeline-geo.js']) {
    const p = path.join(TEMPLATE, f);
    if (!fs.existsSync(p)) {
      if (f === 'network-shift.js' || f === 'pipeline-geo.js') {
        console.warn(`build-invest: ${f} missing`);
        continue;
      }
      console.error(`FATAL: missing template ${p}`);
      process.exit(1);
    }
    fs.copyFileSync(p, path.join(DIST, f));
  }

  const site = bundle.site;
  // Absolute ${basePath}/* asset paths — required with cleanUrls + trailingSlash:false
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>${escapeHtml(site.title || 'Navier — Series B')}</title>
<meta name="robots" content="${escapeHtml(site.robots_meta || 'noindex,nofollow')}" />
<meta name="description" content="${escapeHtml(site.og?.description || 'OWN THE EDGE')}" />
<meta property="og:title" content="${escapeHtml(site.og?.title || 'Navier — Series B')}" />
<meta property="og:description" content="${escapeHtml(site.og?.description || 'OWN THE EDGE')}" />
<meta property="og:type" content="website" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="${basePath}/invest.css" />
</head>
<body>
<div id="app"></div>
<script src="${basePath}/data/invest-data.js"></script>
<script src="${basePath}/network-shift.js"></script>
<script src="${basePath}/invest.js"></script>
</body>
</html>
`;
  fs.writeFileSync(path.join(DIST, 'index.html'), html);

  // Kill-scan on emitted data blob
  const banned = [
    /\$600\s*B/i,
    /2,?400\s*NMi/i,
    /\bN120\b/,
    /Sergey Brin/i,
    /not yet public/i,
    /LC-180/i,
    /\bAD Ports\b/i,
    /\bpre-money\b/i,
    /\bpost-money\b/i,
  ];
  const blob = JSON.stringify(bundle);
  for (const re of banned) {
    if (re.test(blob)) {
      console.error(`FATAL ${label} kill-scan hit: ${re}`);
      process.exit(1);
    }
  }

  const nContracts = Object.keys(bundle).length;
  console.log(`${label} → _dist/${distRel}/  (${nContracts} contracts · noindex · base ${basePath})`);
  return true;
}

function loadBundle() {
  if (!fs.existsSync(path.join(SRC, 'contracts', 'site.json'))) {
    console.warn('build-invest: contracts missing — skip');
    return null;
  }

  const contracts = [
    'site',
    'hero',
    'claim',
    'proof',
    'product',
    'gtm',
    'money',
    'ladder',
    'pipeline-map',
    'unitecon',
    'assets',
  ];

  const bundle = {};
  for (const name of contracts) {
    const p = path.join(SRC, 'contracts', `${name}.json`);
    if (!fs.existsSync(p)) {
      if (name === 'assets') {
        console.warn('build-invest: assets.json missing — visual slots unavailable');
        continue;
      }
      console.error(`FATAL: missing ${p}`);
      process.exit(1);
    }
    bundle[name] = stripUnderscore(readJson(p));
  }

  // Full invest site always carries base_path for the shared JS template
  bundle.site = { ...bundle.site, base_path: '/invest' };
  return bundle;
}

export function buildInvest() {
  const bundle = loadBundle();
  if (!bundle) return false;

  emitSite({
    basePath: '/invest',
    distRel: 'invest',
    bundle,
    label: 'invest',
  });

  emitSite({
    basePath: '/teaser',
    distRel: 'teaser',
    bundle: applyTeaserFilter(bundle),
    label: 'teaser',
  });

  return true;
}

const isMain =
  process.argv[1] &&
  (process.argv[1].endsWith('build-invest.mjs') ||
    process.argv[1].includes('build-invest'));
if (isMain) buildInvest();
