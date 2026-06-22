#!/usr/bin/env node
// Build /partners — internal directory of partner proposals, economics sheets, deck status.
import fs from 'node:fs';
import path from 'node:path';

const DECK_ROOT = 'deck-studio/decks';

function readDeckIndex(root) {
  const deckDir = path.join(root, DECK_ROOT);
  const byPartner = {};
  if (!fs.existsSync(deckDir)) return byPartner;
  for (const fn of fs.readdirSync(deckDir)) {
    const cfgPath = path.join(deckDir, fn, 'deck.config.json');
    if (!fs.existsSync(cfgPath)) continue;
    try {
      const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
      const pid = cfg.partner_id || cfg.deck_key;
      if (pid) byPartner[pid] = { deck_key: cfg.deck_key, display_name: cfg.display_name };
    } catch { /* skip malformed */ }
  }
  return byPartner;
}

export function buildPartnersManifest({ partners, economicsUrlMap, root }) {
  const econ = economicsUrlMap?.economics_url || economicsUrlMap || {};
  const decks = readDeckIndex(root);
  return Object.entries(partners)
    .map(([slug, p]) => ({
      slug,
      display: p.display || slug,
      archetype: p.archetype || '',
      region: p.region || '',
      layout: p.layout || 'single',
      proposal_path: `/${slug}`,
      economics_url: p.economics_url || econ[slug] || null,
      has_growth_case: Boolean(p.growth_case),
      deck_status: decks[slug] ? 'in_progress' : 'none',
      deck_label: decks[slug]?.display_name || null,
      markets_count: Array.isArray(p.markets) ? p.markets.length : 0,
    }))
    .sort((a, b) => a.display.localeCompare(b.display));
}

function esc(s) {
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function renderPartnersHubHtml(manifest, siteUrl) {
  const data = JSON.stringify(manifest);
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Navier — Partner directory</title>
  <style>
    :root {
      --navy: #0c1a2e;
      --steel: #1a3352;
      --gold: #c9a227;
      --text: #e8edf4;
      --muted: #8fa3bc;
      --border: #2a4568;
      --ok: #3d9a6e;
      --pending: #b8860b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
      background: var(--navy);
      color: var(--text);
      line-height: 1.45;
      min-height: 100vh;
    }
    header {
      padding: 2rem 1.5rem 1rem;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, #0f2238 0%, var(--navy) 100%);
    }
    h1 { margin: 0 0 0.35rem; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
    .sub { color: var(--muted); font-size: 0.92rem; max-width: 42rem; }
    main { padding: 1.25rem 1.5rem 3rem; max-width: 1100px; margin: 0 auto; }
    .toolbar {
      display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center;
      margin-bottom: 1.25rem;
    }
    input[type="search"] {
      flex: 1; min-width: 200px;
      padding: 0.55rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--steel);
      color: var(--text);
      font-size: 0.95rem;
    }
    input[type="search"]::placeholder { color: var(--muted); }
    .count { color: var(--muted); font-size: 0.85rem; }
    .grid { display: grid; gap: 0.85rem; }
    .card {
      background: var(--steel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1rem 1.1rem;
      display: grid;
      gap: 0.65rem;
    }
    .card-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.5rem 0.75rem; }
    .card h2 { margin: 0; font-size: 1.05rem; font-weight: 600; }
    .slug { color: var(--muted); font-size: 0.8rem; font-family: ui-monospace, monospace; }
    .badges { display: flex; flex-wrap: wrap; gap: 0.35rem; }
    .badge {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      background: rgba(255,255,255,0.06);
      color: var(--muted);
    }
    .badge.hub { color: var(--gold); border: 1px solid rgba(201,162,39,0.35); }
    .links { display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; font-size: 0.9rem; }
    .links a {
      color: #7eb8ff;
      text-decoration: none;
      border-bottom: 1px solid transparent;
    }
    .links a:hover { border-bottom-color: #7eb8ff; }
    .links a.primary { color: var(--gold); font-weight: 500; }
    .muted { color: var(--muted); }
    .status-ok { color: var(--ok); }
    .status-pending { color: var(--pending); }
    @media (min-width: 720px) {
      .grid { grid-template-columns: 1fr 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Partner directory</h1>
    <p class="sub">Internal index of partner proposal pages, unit-economics sheets, and deck status. Deck links are withheld until iterations are complete.</p>
  </header>
  <main>
    <div class="toolbar">
      <input type="search" id="q" placeholder="Search partners…" autocomplete="off" aria-label="Search partners">
      <span class="count" id="count"></span>
    </div>
    <div class="grid" id="list"></div>
  </main>
  <script id="manifest" type="application/json">${data}</script>
  <script>
    const MANIFEST = JSON.parse(document.getElementById('manifest').textContent);
    const list = document.getElementById('list');
    const q = document.getElementById('q');
    const count = document.getElementById('count');

    function linkRow(label, href, cls) {
      if (!href) return '<span class="muted">' + label + ' —</span>';
      return '<a class="' + (cls || '') + '" href="' + href + '">' + label + '</a>';
    }

    function deckLine(p) {
      if (p.deck_status === 'in_progress')
        return '<span class="status-pending">Deck — in progress</span>';
      return '<span class="muted">Deck —</span>';
    }

    function render(items) {
      count.textContent = items.length + ' of ' + MANIFEST.length;
      list.innerHTML = items.map(p => {
        const layoutBadge = (p.layout === 'hub' || p.layout === 'network')
          ? '<span class="badge hub">' + p.layout + (p.markets_count ? ' · ' + p.markets_count + ' mkts' : '') + '</span>'
          : '<span class="badge">' + (p.layout || 'single') + '</span>';
        const econ = p.economics_url
          ? linkRow('Unit economics sheet', p.economics_url, '')
          : '<span class="muted">Unit economics —</span>';
        return '<article class="card" data-q="' + (p.display + ' ' + p.slug + ' ' + p.region + ' ' + p.archetype).toLowerCase() + '">'
          + '<div class="card-head"><h2>' + p.display + '</h2><span class="slug">' + p.slug + '</span></div>'
          + '<div class="badges">' + layoutBadge
          + (p.region ? '<span class="badge">' + p.region + '</span>' : '')
          + (p.archetype ? '<span class="badge">' + p.archetype + '</span>' : '')
          + (p.has_growth_case ? '<span class="badge status-ok">growth case</span>' : '')
          + '</div>'
          + '<div class="links">'
          + linkRow('Proposal page', p.proposal_path, 'primary')
          + ' · ' + econ
          + ' · ' + deckLine(p)
          + '</div></article>';
      }).join('');
    }

    function filter() {
      const term = q.value.trim().toLowerCase();
      const items = term
        ? MANIFEST.filter(p => (p.display + ' ' + p.slug + ' ' + p.region + ' ' + p.archetype).toLowerCase().includes(term))
        : MANIFEST;
      render(items);
    }

    q.addEventListener('input', filter);
    render(MANIFEST);
  </script>
</body>
</html>`;
}

export function buildPartnersHub({ root, dist, partners, economicsUrlMap, siteUrl }) {
  const manifest = buildPartnersManifest({ partners, economicsUrlMap, root });
  const outDir = path.join(dist, 'partners');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'index.html'), renderPartnersHubHtml(manifest, siteUrl));
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ _doc: 'Internal partner directory manifest', partners: manifest }, null, 2) + '\n');
  return manifest.length;
}