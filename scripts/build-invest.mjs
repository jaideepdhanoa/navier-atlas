#!/usr/bin/env node
/**
 * build-invest.mjs — emit Series B investor microsite to _dist/invest/
 *
 * Source of truth: handoff/invest-microsite/contracts/*.json
 * Rule: render authored data only; strip underscore fields.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'handoff', 'invest-microsite');
const TEMPLATE = path.join(ROOT, 'invest');
const DIST = path.join(ROOT, '_dist', 'invest');

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

export function buildInvest() {
  if (!fs.existsSync(path.join(SRC, 'contracts', 'site.json'))) {
    console.warn('build-invest: contracts missing — skip');
    return false;
  }

  ensureDir(DIST);
  ensureDir(path.join(DIST, 'data'));
  ensureDir(path.join(DIST, 'assets'));

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
  ];

  const bundle = {};
  for (const name of contracts) {
    const p = path.join(SRC, 'contracts', `${name}.json`);
    if (!fs.existsSync(p)) {
      console.error(`FATAL: missing ${p}`);
      process.exit(1);
    }
    const stripped = stripUnderscore(readJson(p));
    bundle[name] = stripped;
    fs.writeFileSync(
      path.join(DIST, 'data', `${name}.json`),
      JSON.stringify(stripped),
    );
  }

  // Single data blob for zero-fetch first paint
  fs.writeFileSync(
    path.join(DIST, 'data', 'invest-data.js'),
    `window.INVEST_DATA = ${JSON.stringify(bundle)};\n`,
  );

  // Assets from handoff + invest/
  const assetSrc = path.join(SRC, 'assets');
  if (fs.existsSync(assetSrc)) copyDir(assetSrc, path.join(DIST, 'assets'));
  const localAssets = path.join(TEMPLATE, 'assets');
  if (fs.existsSync(localAssets)) copyDir(localAssets, path.join(DIST, 'assets'));

  // Template CSS/JS
  for (const f of ['invest.css', 'invest.js']) {
    const p = path.join(TEMPLATE, f);
    if (!fs.existsSync(p)) {
      console.error(`FATAL: missing template ${p}`);
      process.exit(1);
    }
    fs.copyFileSync(p, path.join(DIST, f));
  }

  const site = bundle.site;
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
<link rel="stylesheet" href="./invest.css" />
</head>
<body>
<div id="app"></div>
<script src="./data/invest-data.js"></script>
<script src="./invest.js"></script>
</body>
</html>
`;
  fs.writeFileSync(path.join(DIST, 'index.html'), html);

  // Kill-scan on emitted data blob
  // Word-boundary aware — avoid matching "evaluation" as "valuation"
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
      console.error(`FATAL invest kill-scan hit: ${re}`);
      process.exit(1);
    }
  }

  console.log(`invest → _dist/invest/  (${contracts.length} contracts · noindex)`);
  return true;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const isMain =
  process.argv[1] &&
  (process.argv[1].endsWith('build-invest.mjs') ||
    process.argv[1].includes('build-invest'));
if (isMain) buildInvest();
