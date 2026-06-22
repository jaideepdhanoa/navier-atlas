#!/usr/bin/env node
// Build /partners — internal directory (browse-style UX aligned with Atlas partner index).
import fs from 'node:fs';
import path from 'node:path';

const DECK_ROOT = 'deck-studio/decks';

const CAT_LABELS = {
  ridehail: 'Ride-hail platforms',
  super_app: 'Super-apps',
  commerce_logistics_superapp: 'Commerce & logistics super-apps',
  hospitality_brand: 'Luxury hospitality',
  luxury_portfolio: 'Luxury portfolios',
  investment_jv: 'Investment JVs',
  transit_authority: 'Transit authorities',
  'Authority / public transport': 'Transit authorities',
  'Authority / national transport': 'National transport authorities',
  ferry_operator: 'Ferry operators',
  sovereign_developer: 'Sovereign developers',
  marina_network: 'Marina networks',
  destination_region: 'Destination regions',
  india_water_mobility_operator: 'India water mobility',
};

const CAT_ORDER = [
  'super_app', 'commerce_logistics_superapp', 'ridehail',
  'hospitality_brand', 'luxury_portfolio', 'investment_jv',
  'india_water_mobility_operator', 'transit_authority',
  'Authority / public transport', 'Authority / national transport',
  'ferry_operator', 'sovereign_developer', 'marina_network', 'destination_region',
];

const ARCHETYPE_LABELS = {
  super_app: 'Super-app',
  ridehail: 'Ride-hail',
  public_transit: 'Public transit',
  hospitality: 'Hospitality',
  corporate: 'Corporate',
  sovereign: 'Sovereign',
  charter: 'Charter',
};

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
    } catch { /* skip */ }
  }
  return byPartner;
}

function partnerBlurb(p) {
  const h = p.hero;
  if (h && typeof h === 'object' && h.subtitle) return h.subtitle;
  if (typeof h === 'string') return h;
  if (p.network_thesis?.headline) return p.network_thesis.headline;
  if (p.network_thesis?.body) return p.network_thesis.body.slice(0, 160);
  return '';
}

function partnerCategory(p) {
  return p.category || p.archetype || 'other';
}

export function buildPartnersManifest({ partners, economicsUrlMap, root }) {
  const econ = economicsUrlMap?.economics_url || economicsUrlMap || {};
  const decks = readDeckIndex(root);
  return Object.entries(partners)
    .map(([slug, p]) => {
      const cat = partnerCategory(p);
      return {
        slug,
        display: p.display || slug,
        category: cat,
        category_label: CAT_LABELS[cat] || cat.replace(/_/g, ' '),
        archetype: p.archetype || '',
        archetype_label: ARCHETYPE_LABELS[p.archetype] || p.archetype || '',
        region: p.region || '',
        layout: p.layout || 'single',
        blurb: partnerBlurb(p),
        proposal_path: `/${slug}`,
        economics_url: p.economics_url || econ[slug] || null,
        has_growth_case: Boolean(p.growth_case),
        deck_status: decks[slug] ? 'in_progress' : 'none',
        deck_label: decks[slug]?.display_name || null,
        markets_count: Array.isArray(p.markets) ? p.markets.length : 0,
      };
    })
    .sort((a, b) => a.display.localeCompare(b.display));
}

export function renderPartnersHubHtml(manifest) {
  const payload = JSON.stringify({
    partners: manifest,
    catLabels: CAT_LABELS,
    catOrder: CAT_ORDER,
  });
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Navier Atlas · Partners</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-0:#0a0a0a; --bg-1:#171717; --bg-2:#202020; --bg-3:#2b2b2b;
      --line:rgba(255,255,255,0.07); --line-strong:rgba(255,255,255,0.14);
      --text-0:#f4f4f5; --text-1:#c7c7cc; --text-2:#959595;
      --accent:#e0cb8f; --accent-dim:#c7ad6f;
      --steel:#60a5fa; --ok:#6ee7b7;
    }
    * { box-sizing:border-box; }
    html, body { margin:0; min-height:100%; background:var(--bg-0); color:var(--text-0);
      font-family:'Inter',system-ui,sans-serif; -webkit-font-smoothing:antialiased; }
    .shell { max-width:1040px; margin:0 auto; padding:28px 24px 48px; }
    .top { display:flex; align-items:flex-start; justify-content:space-between; gap:16px;
      flex-wrap:wrap; margin-bottom:20px; padding-bottom:18px; border-bottom:1px solid var(--line); }
    .brand { display:flex; align-items:center; gap:12px; }
    .brand-mark { width:36px; height:36px; border-radius:10px; background:var(--bg-3);
      border:1px solid var(--line-strong); display:flex; align-items:center; justify-content:center; }
    .brand-mark svg { width:22px; height:22px; }
    .brand h1 { margin:0; font-size:18px; font-weight:700; letter-spacing:-0.02em; }
    .brand .tag { font-size:10px; color:var(--text-2); letter-spacing:0.1em; text-transform:uppercase; margin-top:2px; }
    .intro { font-size:13px; line-height:1.55; color:var(--text-2); max-width:36rem; margin:0; }
    .stats { display:flex; gap:20px; flex-wrap:wrap; }
    .stat .v { font-family:'JetBrains Mono',monospace; font-size:17px; font-weight:600; color:var(--text-0); }
    .stat .k { font-size:9px; color:var(--text-2); margin-top:4px; letter-spacing:0.1em; text-transform:uppercase; }
    .panel { background:rgba(23,23,23,0.86); border:1px solid var(--line-strong); border-radius:16px;
      overflow:hidden; box-shadow:0 24px 80px rgba(0,0,0,0.35); }
    .panel-head { display:flex; align-items:center; gap:12px; padding:16px 20px; border-bottom:1px solid var(--line); flex-wrap:wrap; }
    .browse-tabs { display:flex; gap:4px; }
    .browse-tab { background:none; border:none; color:var(--text-2); font:600 13px Inter;
      padding:6px 12px; border-radius:8px; cursor:pointer; }
    .browse-tab:hover { color:var(--text-0); }
    .browse-tab.active { color:var(--text-0); background:rgba(224,203,143,0.12); }
    #q { flex:1; min-width:180px; background:rgba(23,23,23,0.86); border:1px solid var(--line-strong);
      border-radius:999px; color:var(--text-0); font:500 13px Inter; padding:8px 14px; }
    #q:focus { outline:2px solid var(--accent); outline-offset:1px; }
    #q::placeholder { color:var(--text-2); }
    .panel-body { padding:8px 20px 20px; max-height:calc(100vh - 220px); overflow-y:auto; }
    .pidx-group { margin-top:16px; }
    .pidx-group:first-child { margin-top:8px; }
    .pidx-cat { font-size:10px; text-transform:uppercase; letter-spacing:0.12em;
      color:var(--accent); font-weight:700; margin:0 0 9px; }
    .pidx-cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    @media (max-width:720px){ .pidx-cards { grid-template-columns:1fr; } .shell { padding:16px 14px 32px; } }
    .card { text-align:left; background:rgba(23,23,23,0.6); border:1px solid var(--line);
      border-radius:12px; padding:14px 16px; display:flex; flex-direction:column; gap:10px; }
    .card:hover { border-color:rgba(224,203,143,0.4); background:rgba(224,203,143,0.04); }
    .card .t { font:600 14px Inter; color:var(--text-0); display:flex; align-items:center;
      gap:8px; flex-wrap:wrap; margin:0; }
    .card .s { font:400 12px/1.5 Inter; color:var(--text-2); margin:0;
      display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }
    .pidx-badge { font-size:9px; font-weight:700; letter-spacing:0.04em; color:var(--accent);
      background:rgba(224,203,143,0.12); border-radius:99px; padding:1px 7px; text-transform:uppercase; }
    .pidx-badge.region { color:var(--steel); background:rgba(96,165,250,0.12); text-transform:none; }
    .pidx-badge.muted { color:var(--text-2); background:rgba(255,255,255,0.06); text-transform:none; }
    .pidx-badge.ok { color:var(--ok); background:rgba(110,231,183,0.12); text-transform:none; }
    .pidx-badge.pending { color:var(--accent-dim); background:rgba(224,203,143,0.08); text-transform:none; }
    .card-actions { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:auto; padding-top:4px; }
    .btn { font:600 11px Inter; padding:6px 12px; border-radius:8px; text-decoration:none;
      border:1px solid var(--line-strong); color:var(--text-1); background:var(--bg-3); cursor:pointer; }
    .btn:hover { border-color:rgba(224,203,143,0.45); color:var(--accent); }
    .btn.primary { background:rgba(224,203,143,0.14); border-color:rgba(224,203,143,0.45); color:var(--accent); }
    .btn.primary:hover { background:rgba(224,203,143,0.22); }
    .btn.disabled { opacity:0.45; cursor:default; pointer-events:none; }
    .slug { font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-2); }
    .empty { padding:32px 16px; text-align:center; color:var(--text-2); font:400 13px Inter; }
    .count-line { font-size:12px; color:var(--text-2); padding:0 0 8px; }
  </style>
</head>
<body>
  <div class="shell">
    <div class="top">
      <div>
        <div class="brand">
          <div class="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg"><rect width="180" height="180" rx="40" fill="#2b2b2b"/><g fill="#fff"><path d="M130.16 117.84L120.18 135.12A.39.39 0 00119.50 135.11L68.16 44.06A.39.39 0 0168.50 43.48L88.22 43.48A.39.39 0 0188.56 43.68L130.16 117.46A.39.39 0 01130.16 117.84Z"/><path d="M132.68 111.67L122.61 93.82A.55.55 0 01122.62 93.28L150.95 44.21A.55.55 0 01151.90 44.21L161.97 62.07A.55.55 0 01161.96 62.61L133.63 111.68A.55.55 0 01132.68 111.67Z"/></g></svg>
          </div>
          <div>
            <h1>Partner directory</h1>
            <div class="tag">Internal · proposals · models · decks</div>
          </div>
        </div>
        <p class="intro" style="margin-top:14px">Browse the full partner roster like the Atlas <b>Browse</b> dialog — grouped, filterable, with quick links to each proposal page and unit-economics sheet. Deck URLs stay hidden until iterations are done.</p>
      </div>
      <div class="stats" id="stats"></div>
    </div>
    <div class="panel">
      <div class="panel-head">
        <div class="browse-tabs">
          <button type="button" class="browse-tab active" data-view="category">By category</button>
          <button type="button" class="browse-tab" data-view="region">By region</button>
        </div>
        <input type="search" id="q" placeholder="Filter partners…" autocomplete="off" aria-label="Filter partners">
      </div>
      <div class="panel-body" id="body"></div>
    </div>
  </div>
  <script id="payload" type="application/json">${payload.replace(/</g, '\\u003c')}</script>
  <script>
    const { partners: MANIFEST, catLabels: CAT_LABELS, catOrder: CAT_ORDER } =
      JSON.parse(document.getElementById('payload').textContent);
    let view = 'category';
    const q = document.getElementById('q');
    const body = document.getElementById('body');

    function esc(s) {
      return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }

    function renderStats() {
      const econ = MANIFEST.filter(p => p.economics_url).length;
      const deck = MANIFEST.filter(p => p.deck_status === 'in_progress').length;
      document.getElementById('stats').innerHTML =
        '<div class="stat"><div class="v">' + MANIFEST.length + '</div><div class="k">Partners</div></div>' +
        '<div class="stat"><div class="v">' + econ + '</div><div class="k">Models</div></div>' +
        '<div class="stat"><div class="v">' + deck + '</div><div class="k">Decks WIP</div></div>';
    }

    function matchesQ(p, term) {
      if (!term) return true;
      const hay = [p.display, p.slug, p.region, p.category_label, p.archetype_label, p.blurb].join(' ').toLowerCase();
      return hay.includes(term);
    }

    function cardHtml(p) {
      const mk = (p.layout === 'hub' || p.layout === 'network') && p.markets_count
        ? '<span class="pidx-badge">' + p.markets_count + ' markets</span>' : '';
      const rg = p.region ? '<span class="pidx-badge region">' + esc(p.region) + '</span>' : '';
      const econBadge = p.economics_url
        ? '<span class="pidx-badge ok">model</span>' : '<span class="pidx-badge muted">no model</span>';
      const deckBadge = p.deck_status === 'in_progress'
        ? '<span class="pidx-badge pending">deck WIP</span>' : '';
      const growth = p.has_growth_case ? '<span class="pidx-badge ok">growth</span>' : '';
      const econBtn = p.economics_url
        ? '<a class="btn" href="' + esc(p.economics_url) + '" target="_blank" rel="noopener">Unit economics</a>'
        : '<span class="btn disabled">Unit economics</span>';
      return '<article class="card">' +
        '<h2 class="t">' + esc(p.display) + mk + rg + econBadge + deckBadge + growth + '</h2>' +
        '<p class="s">' + (esc(p.blurb) || '<span class="slug">' + esc(p.slug) + '</span>') + '</p>' +
        '<div class="card-actions">' +
        '<a class="btn primary" href="' + esc(p.proposal_path) + '">Open proposal</a>' +
        econBtn +
        (p.deck_status === 'in_progress' ? '<span class="btn disabled">Deck (in progress)</span>' : '') +
        '</div></article>';
    }

    function renderGrouped(groups, order, labelFn) {
      let html = '', n = 0;
      const term = q.value.trim().toLowerCase();
      for (const key of order) {
        const items = (groups[key] || [])
          .filter(p => matchesQ(p, term))
          .sort((a,b) => a.display.localeCompare(b.display));
        if (!items.length) continue;
        n += items.length;
        html += '<div class="pidx-group"><div class="pidx-cat">' + esc(labelFn(key)) + '</div><div class="pidx-cards">' +
          items.map(cardHtml).join('') + '</div></div>';
      }
      return { html, n };
    }

    function render() {
      const term = q.value.trim().toLowerCase();
      let content = '', shown = 0;

      if (view === 'region') {
        const groups = {};
        for (const p of MANIFEST) {
          const r = p.region || 'Other';
          (groups[r] = groups[r] || []).push(p);
        }
        const order = Object.keys(groups).sort((a,b) => groups[b].length - groups[a].length || a.localeCompare(b));
        const out = renderGrouped(groups, order, k => k);
        content = out.html; shown = out.n;
      } else {
        const groups = {};
        for (const p of MANIFEST) {
          const c = p.category || 'other';
          (groups[c] = groups[c] || []).push(p);
        }
        const order = CAT_ORDER.filter(c => groups[c]).concat(
          Object.keys(groups).filter(c => !CAT_ORDER.includes(c)).sort());
        const out = renderGrouped(groups, order, k => CAT_LABELS[k] || k.replace(/_/g, ' '));
        content = out.html; shown = out.n;
      }

      const countLine = '<div class="count-line">Showing ' + shown + ' of ' + MANIFEST.length + ' partners</div>';
      body.innerHTML = countLine + (shown
        ? content
        : '<div class="empty">No partners match your filters.</div>');
    }

    document.querySelectorAll('.browse-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        view = btn.dataset.view;
        document.querySelectorAll('.browse-tab').forEach(b => b.classList.toggle('active', b.dataset.view === view));
        render();
      });
    });
    q.addEventListener('input', render);
    renderStats();
    render();
  </script>
</body>
</html>`;
}

export function buildPartnersHub({ root, dist, partners, economicsUrlMap }) {
  const manifest = buildPartnersManifest({ partners, economicsUrlMap, root });
  const outDir = path.join(dist, 'partners');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'index.html'), renderPartnersHubHtml(manifest));
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ _doc: 'Internal partner directory manifest', partners: manifest }, null, 2) + '\n');
  return manifest.length;
}