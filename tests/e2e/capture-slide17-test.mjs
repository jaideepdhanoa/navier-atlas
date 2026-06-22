import { chromium } from '@playwright/test';

const URL = 'http://127.0.0.1:4176/bolt/greece/city/mykonos-greece/';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 2560, height: 1440 } });
await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 90000 });
await page.waitForSelector('#map canvas', { timeout: 60000 });
await page.waitForTimeout(4000);

const before = await page.evaluate(() => ({
  zoom: window.map?.getZoom?.(),
  center: window.map?.getCenter?.(),
  share: window.__SHARE_ROUTE__,
  hash: location.hash,
  path: location.pathname,
  panelText: document.getElementById('panel')?.innerText?.slice(0, 200),
  introHidden: document.getElementById('intro-modal')?.hidden,
}));

const skip = page.locator('#intro-skip, button.intro-skip').filter({ hasText: /skip to the map/i });
if (await skip.count()) await skip.first().click();
await page.waitForTimeout(3000);

const afterSkip = await page.evaluate(() => ({
  zoom: window.map?.getZoom?.(),
  center: window.map?.getCenter?.(),
  panelText: document.getElementById('panel')?.innerText?.slice(0, 300),
  presets: [...document.querySelectorAll('#presets button, #presets .preset')].map((el) => el.textContent?.trim()).filter(Boolean).slice(0, 6),
}));

// Try selecting Mykonos->Paros route in page context
await page.evaluate(() => {
  const routes = window.ROUTES || [];
  const target = routes.find((r) => r.properties?.id === 'rn-dc595b5a6ab8') || routes.find((r) => {
    const p = r.properties || {};
    return p.from === 'mykonos-greece' && (p.to === 'paros-greece' || String(p.to || '').includes('paros'));
  });
  if (target && typeof selectRoute === 'function') selectRoute(target);
});
await page.waitForTimeout(3500);

const afterRoute = await page.evaluate(() => ({
  zoom: window.map?.getZoom?.(),
  center: window.map?.getCenter?.(),
  selected: window.SELECTED_ROUTE,
  panelText: document.getElementById('panel')?.innerText?.slice(0, 300),
}));

await page.evaluate(() => document.body.classList.add('panel-hidden'));
await page.waitForTimeout(1000);
await page.locator('#map').screenshot({ path: '/tmp/slide17-city-test.png' });

console.log(JSON.stringify({ before, afterSkip, afterRoute }, null, 2));
await browser.close();