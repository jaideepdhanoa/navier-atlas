#!/usr/bin/env node
/**
 * Live browser QA — /careem and /noon map screenshots.
 * Usage:
 *   node scripts/grok-geometry/capture_uae_partner_screenshots.mjs --base-url http://127.0.0.1:8787
 *   node scripts/grok-geometry/capture_uae_partner_screenshots.mjs --base-url https://navier-atlas.vercel.app --password <pw>
 */
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';
import { writeFileSync, mkdirSync } from 'node:fs';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const OUT_DIR = join(ROOT, 'handoff/partner-map-model/uae-visual-qa-screenshots');
const RECEIPT = join(ROOT, 'handoff/partner-map-model/UAE-VISUAL-QA-RECEIPT.json');

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

function parseArgs(argv) {
  const out = { baseUrl: '', password: '', serveDist: false, port: 8787 };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--base-url') out.baseUrl = argv[++i];
    else if (argv[i] === '--password') out.password = argv[++i];
    else if (argv[i] === '--serve-dist') out.serveDist = true;
    else if (argv[i] === '--port') out.port = Number(argv[++i]);
  }
  return out;
}

function resolveDistFile(dist, urlPath) {
  const distRoot = normalize(dist);
  let p = decodeURIComponent(urlPath.split('?')[0]).replace(/^\//, '').replace(/\/$/, '');
  if (!p) p = 'index.html';
  for (const candidate of [join(distRoot, p), join(distRoot, p, 'index.html'), join(distRoot, `${p}.html`)]) {
    const full = normalize(candidate);
    if (!full.startsWith(distRoot)) continue;
    if (existsSync(full) && !full.endsWith('/')) return full;
  }
  return null;
}

function startDistServer(port) {
  const dist = normalize(join(ROOT, '_dist'));
  if (!existsSync(dist)) throw new Error('_dist missing — run deploy build first');
  return new Promise((resolve) => {
    const server = createServer(async (req, res) => {
      const full = resolveDistFile(dist, req.url || '/');
      if (!full) {
        res.writeHead(404);
        return res.end('not found');
      }
      try {
        const body = await readFile(full);
        res.writeHead(200, { 'content-type': TYPES[extname(full)] || 'application/octet-stream' });
        res.end(body);
      } catch {
        res.writeHead(500);
        res.end('read error');
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
    try {
      await skip.first().click({ timeout: 4000 });
      await page.waitForTimeout(1200);
    } catch {
      /* ok */
    }
  }
}

async function capturePartner(browser, { slug, baseUrl, password, outPath }) {
  const url = `${baseUrl.replace(/\/$/, '')}/${slug}`;
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
    httpCredentials: password ? { username: 'navier', password } : undefined,
  });
  const page = await context.newPage();
  page.setDefaultTimeout(120000);
  try {
    await page.goto(url.endsWith('/') ? url : `${url}/`, { waitUntil: 'domcontentloaded', timeout: 120000 });
    await page.waitForFunction(
      () => !!(window.map && typeof window.map.getZoom === 'function' && document.querySelector('#map canvas')),
      { timeout: 90000 },
    );
    await page.waitForFunction(
      () => Array.isArray(window.ROUTES) && window.ROUTES.length > 0,
      { timeout: 90000 },
    );
    await page.waitForTimeout(2500);
    await dismissIntro(page);
    await page.evaluate(() => document.body.classList.add('panel-hidden'));
    await page.waitForTimeout(4000);
    await page.locator('#map').screenshot({ path: outPath, type: 'png' });
    const routes = await page.evaluate(() => {
      const rs = window.ROUTES || [];
      return rs.filter((r) => {
        const p = r.properties || {};
        const fc = p.from_city_id || '';
        const tc = p.to_city_id || '';
        return fc.includes('uae') || tc.includes('uae') || fc.includes('dubai') || tc.includes('dubai');
      }).length;
    });
    return { slug, url, status: 'ok', uae_routes_visible: routes, outPath };
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
  if (args.serveDist || !baseUrl) {
    server = await startDistServer(args.port);
    baseUrl = `http://127.0.0.1:${args.port}`;
  }
  mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const partners = ['careem', 'noon'];
  const results = [];
  try {
    for (const slug of partners) {
      const outPath = join(OUT_DIR, `${slug}-uae-map.png`);
      results.push(await capturePartner(browser, {
        slug,
        baseUrl,
        password: args.password,
        outPath,
      }));
    }
  } finally {
    await browser.close();
    if (server) server.close();
  }

  const failed = results.filter((r) => r.status !== 'ok');
  const receipt = {
    browser_qa_at: new Date().toISOString(),
    deploy_url: 'https://navier-atlas.vercel.app',
    capture_base_url: baseUrl,
    screenshots: results,
    screenshot_dir: OUT_DIR,
    browser_gate_pass: failed.length === 0,
  };
  const prior = existsSync(RECEIPT) ? JSON.parse(await readFile(RECEIPT, 'utf8')) : {};
  writeFileSync(RECEIPT, JSON.stringify({ ...prior, ...receipt }, null, 2) + '\n');
  console.log(JSON.stringify(receipt, null, 2));
  if (failed.length) process.exit(1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});