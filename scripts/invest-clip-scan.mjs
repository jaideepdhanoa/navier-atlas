#!/usr/bin/env node
/**
 * invest-clip-scan.mjs — v5 P0-1 gate
 * Fails if any selected text element's getBoundingClientRect().left < 24
 * at 1280 / 1440 / 2560.
 *
 * Usage: node scripts/invest-clip-scan.mjs [url]
 * Default url: http://127.0.0.1:8799/invest
 */
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';

const URL = process.argv[2] || 'http://127.0.0.1:8799/invest';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9355;
const WIDTHS = [
  [1280, 900],
  [1440, 900],
  [2560, 1440],
];

function get(url) {
  return new Promise((res, rej) => {
    http.get(url, (r) => {
      let d = '';
      r.on('data', (c) => (d += c));
      r.on('end', () => res(d));
    }).on('error', rej);
  });
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(
  CHROME,
  [
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    `--remote-debugging-port=${PORT}`,
    '--window-size=1280,900',
    'about:blank',
  ],
  { stdio: 'ignore' },
);

let ready = false;
for (let i = 0; i < 40; i++) {
  try {
    JSON.parse(await get(`http://127.0.0.1:${PORT}/json/version`));
    ready = true;
    break;
  } catch {
    await sleep(200);
  }
}
if (!ready) {
  console.error('CDP not ready');
  process.exit(2);
}

const list = JSON.parse(await get(`http://127.0.0.1:${PORT}/json/list`));
const page = list.find((t) => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0;
const pending = new Map();
ws.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) {
    pending.get(msg.id)(msg);
    pending.delete(msg.id);
  }
};
const send = (method, params = {}) =>
  new Promise((resolve) => {
    const mid = ++id;
    pending.set(mid, resolve);
    ws.send(JSON.stringify({ id: mid, method, params }));
  });

const report = {};
let fail = 0;

await send('Page.enable');
for (const [w, h] of WIDTHS) {
  await send('Emulation.setDeviceMetricsOverride', {
    width: w,
    height: h,
    deviceScaleFactor: 1,
    mobile: false,
  });
  await send('Page.navigate', { url: URL });
  await sleep(4500);
  // scroll through page to force layout of below-fold
  await send('Runtime.evaluate', {
    expression: `new Promise(r=>{let y=0; const step=()=>{window.scrollTo(0,y); y+=Math.max(400, innerHeight*0.8); if(y>document.body.scrollHeight){window.scrollTo(0,0); r();} else requestAnimationFrame(step);}; step();})`,
    awaitPromise: true,
  });
  await sleep(500);
  const r = await send('Runtime.evaluate', {
    expression: `(() => {
      const sels = 'h1,h2,h3,p,figcaption,li,th,td,button,a,.cinema-cap,.chapter-label,.gold-stat .value,.gold-stat .label,.eyebrow,.ns-kicker,.ns-chip .h,.ns-chip .s,.ns-chip .k,.floor-label,.floor-vessels,.floor-line,.team-name,.team-role,.team-creds,.btn,.vcard-cap,.film-cap,.backers-type .bl,.backers-type .names span,.chart-title,.chart-sub,.basis,.muted,.lead,.body-text,.closing-line,.kicker,.manifesto-body';
      const out = [];
      for (const el of document.querySelectorAll(sels)) {
        const t = (el.innerText || '').trim().replace(/\\s+/g, ' ');
        if (!t || t.length > 100) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2 || r.bottom < 0 || r.top > innerHeight * 3) continue;
        // measure content box: use left of first client rect of text if available
        let left = r.left;
        try {
          const range = document.createRange();
          range.selectNodeContents(el);
          const rects = range.getClientRects();
          if (rects.length) left = rects[0].left;
        } catch (_) {}
        if (left < 24) {
          out.push({
            left: Math.round(left * 10) / 10,
            text: t.slice(0, 60),
            tag: el.tagName,
            cls: (el.className || '').toString().slice(0, 50),
          });
        }
      }
      // unique by text+left
      const seen = new Set();
      const uniq = [];
      for (const o of out) {
        const k = o.left + '|' + o.text;
        if (seen.has(k)) continue;
        seen.add(k);
        uniq.push(o);
      }
      return { count: uniq.length, minLeft: uniq.length ? Math.min(...uniq.map((x) => x.left)) : 'none', items: uniq.slice(0, 40) };
    })()`,
    returnByValue: true,
  });
  const val = r.result.result.value;
  report[String(w)] = val;
  if (val.count > 0) fail += val.count;
  console.log(`\\n=== ${w}x${h} ===`);
  console.log(JSON.stringify(val, null, 2));
}

const outPath = 'handoff/invest-microsite/CLIP-SCAN-V5.json';
fs.writeFileSync(outPath, JSON.stringify({ url: URL, report, fail }, null, 2));
console.log('\\nWrote', outPath, 'failCount', fail);

ws.close();
chrome.kill();
process.exit(fail > 0 ? 1 : 0);
