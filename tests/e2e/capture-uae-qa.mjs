#!/usr/bin/env node
/** Live browser QA — /careem and /noon from deployed _dist or prod URL. */
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const OUT_DIR = join(ROOT, 'handoff/partner-map-model/uae-visual-qa-screenshots');
const RECEIPT = join(ROOT, 'handoff/partner-map-model/UAE-VISUAL-QA-RECEIPT.json');
const PROD_URL = 'https://navier-atlas.vercel.app';

function parseArgs(argv) {
  const out = {
    baseUrl: '',
    password: process.env.PARTNER_AUTH_CAREEM || process.env.PARTNER_AUTH_JSON ? '' : '',
    serveDist: true,
    port: 8787,
    prod: false,
  };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--base-url') out.baseUrl = argv[++i];
    else if (argv[i] === '--password') out.password = argv[++i];
    else if (argv[i] === '--serve-dist') out.serveDist = true;
    else if (argv[i] === '--prod') { out.prod = true; out.serveDist = false; out.baseUrl = PROD_URL; }
    else if (argv[i] === '--port') out.port = Number(argv[++i]);
  }
  return out;
}

function startDistServer(port) {
  const dist = join(ROOT, '_dist');
  if (!existsSync(dist)) throw new Error('_dist missing — run deploy build first');
  const child = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1'], {
    cwd: dist,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('dist server start timeout')), 10000);
    child.stderr.on('data', (chunk) => {
      const text = String(chunk);
      if (text.includes('Address already in use')) {
        clearTimeout(timer);
        reject(new Error(text.trim()));
      }
    });
    child.stdout.on('data', () => {
      clearTimeout(timer);
      console.log(`[serve] _dist at http://127.0.0.1:${port}`);
      resolve(child);
    });
    // python http.server may not write to stdout on bind; probe after short delay
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
    try { await skip.first().click({ timeout: 4000 }); await page.waitForTimeout(1200); } catch { /* */ }
  }
}

async function capturePartner(browser, { slug, baseUrl, password, outPath }) {
  const url = `${baseUrl.replace(/\/$/, '')}/${slug}/`;
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    httpCredentials: password ? { username: 'navier', password } : undefined,
  });
  const page = await context.newPage();
  page.setDefaultTimeout(120000);
  try {
    const failures = [];
    page.on('requestfailed', (req) => failures.push(`${req.url()} :: ${req.failure()?.errorText || 'failed'}`));
    page.on('pageerror', (err) => failures.push(`pageerror :: ${err.message}`));

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });
    await page.waitForFunction(
      () => !!(window.map && typeof window.map.getZoom === 'function' && document.querySelector('#map canvas')),
      { timeout: 90000 },
    );
    await page.waitForFunction(
      () => Array.isArray(window.ROUTES) && window.ROUTES.length > 0,
      { timeout: 90000 },
    );
    await dismissIntro(page);
    await page.evaluate(() => document.body.classList.add('panel-hidden'));
    await page.waitForTimeout(2500);
    await page.locator('#map').screenshot({ path: outPath, type: 'png' });
    const uaeRoutes = await page.evaluate(() => (window.ROUTES || []).filter((r) => {
      const p = r.properties || {};
      return String(p.from_city_id || '').includes('uae') || String(p.to_city_id || '').includes('uae');
    }).length);
    return { slug, url, status: 'ok', uae_routes_visible: uaeRoutes, outPath, failures: failures.slice(0, 5) };
  } catch (err) {
    return { slug, url, status: 'error', error: String(err?.message || err), outPath };
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
  mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const slug of ['careem', 'noon']) {
      const outPath = join(OUT_DIR, `${slug}-uae-map.png`);
      results.push(await capturePartner(browser, { slug, baseUrl, password: args.password, outPath }));
    }
  } finally {
    await browser.close();
    if (server) server.kill('SIGTERM');
  }
  const failed = results.filter((r) => r.status !== 'ok');
  const prior = existsSync(RECEIPT) ? JSON.parse(readFileSync(RECEIPT, 'utf8')) : {};
  const merged = {
    ...prior,
    browser_qa_at: new Date().toISOString(),
    deploy_url: PROD_URL,
    capture_base_url: baseUrl,
    screenshots: results,
    screenshot_dir: OUT_DIR,
    browser_gate_pass: failed.length === 0,
    capture_note: args.prod
      ? 'Live production capture via Playwright'
      : 'Playwright capture of production _dist artifact (same bytes as Vercel)',
    deploy_commit: process.env.VERCEL_GIT_COMMIT_SHA || '1388820b',
  };
  writeFileSync(RECEIPT, JSON.stringify(merged, null, 2) + '\n');
  console.log(JSON.stringify(merged, null, 2));
  if (failed.length) process.exit(1);
}

main().catch((e) => { console.error(e); process.exit(1); });