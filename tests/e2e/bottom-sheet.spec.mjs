// Smoke tests for the mobile bottom-sheet behaviour added to index.html.
// MapLibre is stubbed offline (see maplibre-stub.js); these cover the sheet
// drag/snap UI and the desktop rail, not the map render itself.
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';

const STUB = readFileSync(new URL('./maplibre-stub.js', import.meta.url), 'utf8');

// Load index.html with the CDN deps neutralised so the page runs fully offline.
async function loadAtlas(page) {
  await page.route(/maplibre-gl@[^/]+\/dist\/maplibre-gl\.js(\?.*)?$/, (r) =>
    r.fulfill({ contentType: 'application/javascript', body: STUB }));
  await page.route(/maplibre-gl@[^/]+\/dist\/maplibre-gl\.css(\?.*)?$/, (r) =>
    r.fulfill({ contentType: 'text/css', body: '' }));
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
  await page.goto('/');
  // Tiles never load offline; clear the cold-load overlay so it can't intercept input.
  await page.evaluate(() => {
    const l = document.getElementById('loading');
    if (l) { l.classList.add('done'); l.style.display = 'none'; }
  });
}

// Rendered top edge of the sheet (smaller = sheet raised higher = more open).
const panelTop = (page) => page.locator('#panel').evaluate((el) => el.getBoundingClientRect().top);
// Sheet transition is 300ms; give it margin to settle before measuring.
const settle = (page) => page.waitForTimeout(420);

test.describe('mobile bottom sheet (390×844)', () => {
  test.use({ viewport: { width: 390, height: 844 } });
  const IH = 844;

  test('starts at peek; tapping the handle cycles peek → half → full → peek', async ({ page }) => {
    await loadAtlas(page);
    const grab = page.locator('#sheet-grab');
    await expect(grab).toBeVisible();

    await settle(page);
    expect(await panelTop(page)).toBeGreaterThan(IH * 0.82); // peek ≈ 748

    await grab.click(); await settle(page);                  // → half ≈ 422
    expect(await panelTop(page)).toBeGreaterThan(IH * 0.42);
    expect(await panelTop(page)).toBeLessThan(IH * 0.58);

    await grab.click(); await settle(page);                  // → full ≈ 67
    expect(await panelTop(page)).toBeLessThan(IH * 0.12);

    await grab.click(); await settle(page);                  // → peek
    expect(await panelTop(page)).toBeGreaterThan(IH * 0.82);
  });

  test('dragging the handle up snaps to full, dragging down snaps to peek', async ({ page }) => {
    await loadAtlas(page);
    const grab = page.locator('#sheet-grab');
    await expect(grab).toBeVisible();
    await settle(page);

    // Drag up toward the top → nearest snap is full.
    let box = await grab.boundingBox();
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.mouse.down();
    await page.mouse.move(195, 120, { steps: 12 });
    await page.mouse.up();
    await settle(page);
    expect(await panelTop(page)).toBeLessThan(IH * 0.12);

    // Drag back down toward the bottom → nearest snap is peek.
    box = await grab.boundingBox();
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.mouse.down();
    await page.mouse.move(195, 820, { steps: 12 });
    await page.mouse.up();
    await settle(page);
    expect(await panelTop(page)).toBeGreaterThan(IH * 0.82);
  });

  test('rendering real content auto-raises the sheet from peek to half', async ({ page }) => {
    await loadAtlas(page);
    await settle(page);
    expect(await panelTop(page)).toBeGreaterThan(IH * 0.82); // peek (empty/admin state)

    // The MutationObserver should lift peek → half when a real selection renders.
    await page.evaluate(() => {
      document.getElementById('panel').innerHTML =
        '<div class="panel-hero"><h2>Test City</h2></div>';
    });
    await settle(page);
    const t = await panelTop(page);
    expect(t).toBeGreaterThan(IH * 0.42);
    expect(t).toBeLessThan(IH * 0.58);
  });
});

test.describe('desktop rail unchanged (1280×800)', () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  test('no bottom-sheet handle; #panel is the right-anchored full-height rail', async ({ page }) => {
    await loadAtlas(page);
    await expect(page.locator('#sheet-grab')).toBeHidden();
    const r = await page.locator('#panel').evaluate((el) => {
      const b = el.getBoundingClientRect();
      return { right: b.right, width: b.width, top: b.top };
    });
    expect(Math.round(r.right)).toBe(1280); // flush to the viewport's right edge
    expect(r.top).toBeLessThan(2);          // spans full height from the top
    expect(r.width).toBeGreaterThan(300);   // rail width (default --panel-w 420)
  });
});
