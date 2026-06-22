#!/usr/bin/env node
/**
 * Playwright capture for atlas_route_screenshot deck slides.
 * Invoked by deck-studio/builders/capture_atlas_screenshots.py with JSON manifest on stdin.
 */
import { readFileSync } from 'node:fs';
import { chromium } from '@playwright/test';

function loadManifest(argv) {
  const flag = argv.indexOf('--manifest');
  if (flag >= 0) {
    return JSON.parse(readFileSync(argv[flag + 1], 'utf8'));
  }
  return JSON.parse(readFileSync(0, 'utf8'));
}

async function dismissIntro(page) {
  const skip = page.locator('#intro-skip, button.intro-skip').filter({ hasText: /skip to the map/i });
  if (await skip.count()) {
    try {
      await skip.first().click({ timeout: 3000 });
      await page.waitForTimeout(1200);
      return;
    } catch {
      /* overlay may already be gone */
    }
  }
}

async function waitForAtlasReady(page) {
  await page.waitForFunction(
    () => typeof window._openCityDeepLink === 'function' || (window.map && typeof window.map.getZoom === 'function'),
    { timeout: 60000 },
  );
}

async function frameCityView(page, item) {
  const cityId = item.atlas_city_id;
  if (!cityId) return;
  await page.evaluate((id) => {
    if (typeof _openCityDeepLink === 'function') _openCityDeepLink(id);
  }, cityId);
  await page.waitForTimeout(2200);
}

async function frameRoute(page, routeId) {
  if (!routeId) return;
  await page.evaluate((id) => {
    const routes = window.ROUTES || [];
    const target = routes.find((r) => (r.properties || {}).id === id);
    if (target && typeof selectRoute === 'function') selectRoute(target);
  }, routeId);
  await page.waitForTimeout(3800);
}

async function prepareMapView(page, item, defaults) {
  await waitForAtlasReady(page);
  await page.waitForTimeout(defaults.map_settle_ms || 2500);
  await dismissIntro(page);

  const mode = item.capture_mode || (item.url.includes('/city/') ? 'city' : 'market');
  if (mode === 'city' || mode === 'city_route') {
    await frameCityView(page, item);
  }
  if (mode === 'city_route' && item.atlas_route_id) {
    await frameRoute(page, item.atlas_route_id);
  }

  await page.evaluate(() => document.body.classList.add('panel-hidden'));
  await page.waitForTimeout(defaults.post_panel_ms || 3500);
}

async function captureOne(browser, item, defaults) {
  const viewport = item.viewport || defaults.viewport || { width: 2560, height: 1440 };
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: 1,
    httpCredentials: defaults.password
      ? { username: defaults.username || 'navier', password: defaults.password }
      : undefined,
  });
  const page = await context.newPage();
  const out = item.output_path;
  try {
    await page.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.waitForSelector('#map canvas', { timeout: 60000 });
    await prepareMapView(page, item, defaults);
    const map = page.locator('#map');
    await map.screenshot({ path: out, type: 'png' });
    return { slide_index: item.slide_index, output_path: out, status: 'ok' };
  } catch (err) {
    return {
      slide_index: item.slide_index,
      output_path: out,
      status: 'error',
      error: String(err?.message || err),
    };
  } finally {
    await context.close();
  }
}

async function main() {
  const manifest = loadManifest(process.argv.slice(2));
  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const item of manifest.items) {
      results.push(await captureOne(browser, item, manifest));
    }
  } finally {
    await browser.close();
  }
  const failed = results.filter((r) => r.status !== 'ok');
  console.log(JSON.stringify({ captured: results.length - failed.length, failed: failed.length, results }, null, 2));
  if (failed.length) process.exit(1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});