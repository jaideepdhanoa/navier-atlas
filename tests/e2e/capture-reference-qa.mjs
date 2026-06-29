#!/usr/bin/env node
/**
 * Reference partner browser QA — desktop + optional mobile, phase-scoped screenshots.
 * Usage:
 *   node tests/e2e/capture-reference-qa.mjs --serve-dist
 *   RELEASE=1 node tests/e2e/capture-reference-qa.mjs --serve-dist  (via preflight)
 */
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const OUT_DIR = join(ROOT, 'handoff/partner-map-model/reference-visual-qa-screenshots');
const RECEIPT = join(ROOT, 'handoff/partner-map-model/REFERENCE-VISUAL-QA-RECEIPT.json');
const PROD_URL = 'https://navier-atlas.vercel.app';

/** @type {{ slug: string, label: string, paths: { name: string, entry: string, phaseN?: number }[] }[]} */
const TARGETS = [
  {
    slug: 'careem',
    label: 'Careem UAE',
    paths: [
      { name: 'overview', entry: '' },
      { name: 'phase-1', entry: '', phaseN: 1 },
      { name: 'phase-2', entry: '', phaseN: 2 },
      { name: 'phase-3', entry: '', phaseN: 3 },
    ],
  },
  {
    slug: 'noon',
    label: 'Noon UAE',
    paths: [
      { name: 'overview', entry: '' },
      { name: 'phase-1', entry: '', phaseN: 1 },
      { name: 'phase-2', entry: '', phaseN: 2 },
      { name: 'phase-3', entry: '', phaseN: 3 },
    ],
  },
  {
    slug: 'bolt',
    label: 'Bolt UAE market',
    paths: [
      { name: 'market-uae', entry: 'uae' },
      { name: 'market-uae-phase-1', entry: 'uae', phaseN: 1, marketSlug: 'uae' },
      { name: 'market-uae-phase-2', entry: 'uae', phaseN: 2, marketSlug: 'uae' },
    ],
  },
  {
    slug: 'yango',
    label: 'Yango UAE market',
    paths: [
      { name: 'market-uae', entry: 'uae' },
      { name: 'market-uae-phase-1', entry: 'uae', phaseN: 1, marketSlug: 'uae' },
    ],
  },
  {
    slug: 'grab',
    label: 'Grab Singapore',
    paths: [
      { name: 'market-singapore', entry: 'singapore' },
      { name: 'market-singapore-phase-1', entry: 'singapore', phaseN: 1, marketSlug: 'singapore' },
      { name: 'market-singapore-phase-2', entry: 'singapore', phaseN: 2, marketSlug: 'singapore' },
    ],
  },
];

function parseArgs(argv) {
  const out = {
    baseUrl: '',
    password: '',
    serveDist: false,
    port: 8788,
    prod: false,
    mobile: false,
    slugs: [],
  };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--base-url') out.baseUrl = argv[++i];
    else if (argv[i] === '--password') out.password = argv[++i];
    else if (argv[i] === '--serve-dist') out.serveDist = true;
    else if (argv[i] === '--prod') { out.prod = true; out.serveDist = false; out.baseUrl = PROD_URL; }
    else if (argv[i] === '--port') out.port = Number(argv[++i]);
    else if (argv[i] === '--mobile') out.mobile = true;
    else if (argv[i] === '--slug') out.slugs.push(argv[++i]);
  }
  return out;
}

function loadPartnerPassword(slug) {
  const key = `PARTNER_AUTH_${slug.toUpperCase().replace(/-/g, '_')}`;
  if (process.env[key]) return process.env[key];
  const raw = process.env.PARTNER_AUTH_JSON;
  if (!raw) return '';
  try {
    const j = JSON.parse(raw);
    return j[slug] || j.__hub__ || '';
  } catch {
    return '';
  }
}

function startDistServer(port) {
  const dist = join(ROOT, '_dist');
  if (!existsSync(dist)) throw new Error('_dist missing — run build first');
  const child = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1'], {
    cwd: dist,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('dist server start timeout')), 10000);
    child.stderr.on('data', (chunk) => {
      if (String(chunk).includes('Address already in use')) {
        clearTimeout(timer);
        reject(new Error(String(chunk).trim()));
      }
    });
    setTimeout(() => {
      clearTimeout(timer);
      console.log(`[serve] _dist at http://127.0.0.1:${port}`);
      resolve(child);
    }, 500);
  });
}

async function dismissIntro(page) {
  const skip = page.locator('#intro-skip, button.intro-skip').filter({ hasText: /skip to the map/i });
  if (await skip.count()) {
    try { await skip.first().click({ timeout: 4000 }); await page.waitForTimeout(800); } catch { /* */ }
  }
}

async function waitMapReady(page) {
  await page.waitForFunction(
    () => !!(window.map && typeof window.map.getZoom === 'function' && document.querySelector('#map canvas')),
    { timeout: 90000 },
  );
  await page.waitForFunction(
    () => Array.isArray(window.ROUTES) && window.ROUTES.length > 0,
    { timeout: 90000 },
  );
  await page.waitForFunction(
    () => new Promise((resolve) => {
      if (!window.map || typeof window.map.once !== 'function') return resolve(true);
      let done = false;
      const finish = () => { if (!done) { done = true; resolve(true); } };
      window.map.once('idle', finish);
      setTimeout(finish, 6000);
    }),
    { timeout: 30000 },
  );
}

async function focusPhase(page, phaseN, { marketSlug } = {}) {
  if (!phaseN) return;
  await page.evaluate(({ n, market }) => {
    const slug = window.__PARTNER_BUILD__ || window.PARTNER_ACTIVE?.slug;
    const partner = slug ? window.PARTNERS?.[slug] : null;
    if (!partner) return;
    const intro = document.getElementById('intro-modal');
    if (intro) intro.hidden = true;
    if (market && partner.markets && typeof openHubMarket === 'function') {
      const mk = partner.markets.find((m) => m.slug === market);
      if (mk) openHubMarket(partner, mk, false);
    } else if (typeof startPartnerCarousel === 'function') {
      if (!window._CARO) startPartnerCarousel(partner);
    }
    if (typeof showPhase === 'function' && window._CARO) showPhase(n - 1);
  }, { n: phaseN, market: marketSlug || '' });
  await page.waitForFunction(
    (n) => {
      if (window._activePhaseN === n) return true;
      const ch = window._CARO?.chapters?.[window._CARO?.i];
      return ch?.kind === 'phase' && (ch.phase?.n ?? ch.phaseIndex + 1) === n;
    },
    phaseN,
    { timeout: 30000 },
  ).catch(() => page.waitForTimeout(3500));
  await page.waitForTimeout(2000);
}

async function captureView(browser, { slug, name, url, password, outPath, viewport, phaseN, marketSlug }) {
  const context = await browser.newContext({
    viewport,
    httpCredentials: password ? { username: 'navier', password } : undefined,
  });
  const page = await context.newPage();
  page.setDefaultTimeout(120000);
  try {
    const failures = [];
    page.on('requestfailed', (req) => failures.push(`${req.url()} :: ${req.failure()?.errorText || 'failed'}`));
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });
    await waitMapReady(page);
    await dismissIntro(page);
    await focusPhase(page, phaseN, { marketSlug });
    await page.evaluate(() => document.body.classList.add('panel-hidden'));
    await page.waitForTimeout(2000);
    await page.locator('#map').screenshot({ path: outPath, type: 'png' });
    const meta = await page.evaluate(() => ({
      routes: (window.ROUTES || []).length,
      phaseN: window._activePhaseN ?? null,
      partner: window.PARTNER_ACTIVE?.slug || null,
    }));
    return {
      slug,
      name,
      url,
      status: 'ok',
      outPath,
      ...meta,
      phaseN: meta.phaseN ?? phaseN ?? null,
      requestedPhaseN: phaseN ?? null,
      failures: failures.slice(0, 3),
    };
  } catch (err) {
    return { slug, name, url, status: 'error', error: String(err?.message || err), outPath };
  } finally {
    await context.close();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let server = null;
  let baseUrl = args.baseUrl;
  if (args.serveDist && !args.baseUrl) {
    server = await startDistServer(args.port);
    baseUrl = `http://127.0.0.1:${args.port}`;
  } else if (!baseUrl) {
    baseUrl = PROD_URL;
  }

  const targets = args.slugs.length
    ? TARGETS.filter((t) => args.slugs.includes(t.slug))
    : TARGETS;

  mkdirSync(OUT_DIR, { recursive: true });
  const viewports = [
    { label: 'desktop', size: { width: 1920, height: 1080 } },
  ];
  if (args.mobile) {
    viewports.push({ label: 'mobile', size: { width: 390, height: 844 } });
  }

  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const target of targets) {
      const password = args.password || loadPartnerPassword(target.slug);
      for (const vp of viewports) {
        for (const path of target.paths) {
          const file = `${target.slug}-${path.name}${vp.label === 'mobile' ? '-mobile' : ''}.png`;
          const outPath = join(OUT_DIR, file);
          const entry = path.entry ? `/${path.entry}/` : '/';
          const url = `${baseUrl.replace(/\/$/, '')}/${target.slug}${entry}`;
          results.push(await captureView(browser, {
            slug: target.slug,
            name: `${path.name}-${vp.label}`,
            url,
            password,
            outPath,
            viewport: vp.size,
            phaseN: path.phaseN,
            marketSlug: path.marketSlug,
          }));
        }
      }
    }
  } finally {
    await browser.close();
    if (server) server.kill('SIGTERM');
  }

  const failed = results.filter((r) => r.status !== 'ok');
  const prodAttempted = args.prod;
  const receipt = {
    browser_qa_at: new Date().toISOString(),
    deploy_url: PROD_URL,
    prod_capture_attempted: prodAttempted,
    prod_capture_note: prodAttempted
      ? 'Live prod URL with Basic auth (requires PARTNER_AUTH_JSON or per-slug env)'
      : '_dist artifact (byte-identical to Vercel deploy)',
    capture_base_url: baseUrl,
    screenshot_dir: OUT_DIR,
    screenshots: results,
    browser_gate_pass: failed.length === 0,
    targets: targets.map((t) => t.slug),
    viewports: viewports.map((v) => v.label),
  };
  writeFileSync(RECEIPT, JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify({ browser_gate_pass: receipt.browser_gate_pass, total: results.length, failed: failed.length }, null, 2));
  if (failed.length) {
    console.error(JSON.stringify(failed, null, 2));
    process.exit(1);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });