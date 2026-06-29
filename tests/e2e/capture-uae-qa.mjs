#!/usr/bin/env node
/** Live browser QA — /careem and /noon from deployed _dist or prod URL. */
import { createServer } from 'node:http';
import { readFile, readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const OUT_DIR = join(ROOT, 'handoff/partner-map-model/uae-visual-qa-screenshots');
const RECEIPT = join(ROOT, 'handoff/partner-map-model/UAE-VISUAL-QA-RECEIPT.json');
const PROD_URL = 'https://navier-atlas.vercel.app';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
};

function parseArgs(argv) {
  const out = { baseUrl: '', password: process.env.PARTNER_AUTH_CAREEM || '', serveDist: true, port: 8787, prod: false };
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
  return new Promise((resolve) => {
    const server = createServer(async (req, res) => {
      let p = decodeURIComponent((req.url || '/').split('?')[0]).replace(/^\//, '');
      if (!p || p === '') p = 'index.html';
      let full = normalize(join(dist, p));
      if (!full.startsWith(dist)) { res.writeHead(403); return res.end('forbidden'); }
      try {
        const body = await readFile(full);
        res.writeHead(200, { 'content-type': TYPES[extname(full)] || 'application/octet-stream' });
        res.end(body);
      } catch {
        try {
          full = normalize(join(dist, p.replace(/\/?$/, ''), 'index.html'));
          const body = await readFile(full);
          res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
          res.end(body);
        } catch {
          res.writeHead(404);
          res.end('not found');
        }
      }
    });
    server.listen(port, '127.0.0.1', () => {
      console.log(`[serve] _dist at http://127.0.0.1:${port}`);
      resolve(server);
    });
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
    await page.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
    await page.waitForTimeout(4000);
    await dismissIntro(page);
    const ready = await page.evaluate(
      () => !!(window.map && typeof window.map.getZoom === 'function' && document.querySelector('#map canvas')),
    );
    if (!ready) throw new Error('map not ready after networkidle');
    await page.evaluate(() => document.body.classList.add('panel-hidden'));
    await page.waitForTimeout(2500);
    await page.locator('#map').screenshot({ path: outPath, type: 'png' });
    const uaeRoutes = await page.evaluate(() => (window.ROUTES || []).filter((r) => {
      const p = r.properties || {};
      return String(p.from_city_id || '').includes('uae') || String(p.to_city_id || '').includes('uae');
    }).length);
    return { slug, url, status: 'ok', uae_routes_visible: uaeRoutes, outPath };
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
    if (server) server.close();
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
  };
  writeFileSync(RECEIPT, JSON.stringify(merged, null, 2) + '\n');
  console.log(JSON.stringify(merged, null, 2));
  if (failed.length) process.exit(1);
}

main().catch((e) => { console.error(e); process.exit(1); });