/* Series B /invest v4 — S1 safe-area · vessel canon · Network Shift respec */
(function () {
  'use strict';

  const D = window.INVEST_DATA;
  if (!D || !D.site) {
    document.getElementById('app').innerHTML =
      '<p style="padding:40px;color:#c8c8ce">INVEST_DATA missing.</p>';
    return;
  }

  const $ = (sel, el = document) => el.querySelector(sel);
  const ASSET = '/invest/assets/';
  const A = D.assets || {};
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const esc = (s) =>
    String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  const nl = (s) => esc(s).replace(/\n/g, '<br/>');

  function mediaPath(p) {
    if (!p) return '';
    const s = String(p);
    if (/^https?:\/\//i.test(s)) return s;
    return ASSET + s.replace(/^assets\//, '').replace(/^\.\//, '');
  }

  /* ── v4 homes index ─────────────────────────────────── */
  const homes = new Map();
  for (const s of A.sections || []) {
    if (s && s.home) homes.set(s.home, s);
  }
  function home(id) {
    return homes.get(id) || null;
  }
  function homeSrc(id) {
    const h = home(id);
    return h && h.asset ? mediaPath(h.asset) : '';
  }
  function homeAssets(id) {
    const h = home(id);
    return (h && h.assets) || null;
  }
  function homeCap(id) {
    const h = home(id);
    return (h && h.caption) || '';
  }

  function cinema(src, opts = {}) {
    if (!src) return '';
    const cap = opts.caption;
    return `
      <div class="cinema" data-home="${esc(opts.home || '')}" data-reveal>
        <div class="cinema-media" style="${opts.vh ? `height:${opts.vh}` : ''}">
          ${
            opts.video
              ? `<video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="none" data-lazy-video poster="${esc(opts.poster || '')}">
                   <source src="${esc(src)}" type="video/mp4" />
                 </video>`
              : `<img src="${esc(src)}" alt="${esc(opts.alt || '')}" loading="${opts.eager ? 'eager' : 'lazy'}" ${opts.eager ? 'fetchpriority="high"' : ''} />`
          }
        </div>
        ${cap ? `<p class="cinema-cap">${esc(cap)}</p>` : ''}
      </div>`;
  }

  function plate(src, opts = {}) {
    if (!src) return '';
    return `
      <figure class="plate ${opts.className || ''}" data-home="${esc(opts.home || '')}">
        <img src="${esc(src)}" alt="${esc(opts.alt || '')}" loading="lazy" />
        ${opts.caption ? `<figcaption>${esc(opts.caption)}</figcaption>` : ''}
      </figure>`;
  }

  function goldStats(stats) {
    if (!stats || !stats.length) return '';
    const n = Math.min(stats.length, 4);
    const cells = stats
      .map(
        (st) => `
      <div class="gold-stat">
        <div class="value" data-counter="${esc(st.value)}">${esc(st.value)}</div>
        <div class="label">${esc(st.label)}</div>
      </div>`,
      )
      .join('');
    return `<div class="gold-stat-band cols-${n}" data-reveal>${cells}</div>`;
  }

  function brandMark() {
    return `<div class="inv-brand-mark" aria-hidden="true"><svg viewBox="9.5 9.5 160 160" fill="currentColor"><path d="M130.16 117.84 L120.18 135.12 A0.39 0.39 0 0 1 119.50 135.11 L68.16 44.06 A0.39 0.39 0 0 1 68.50 43.48 L88.22 43.48 A0.39 0.39 0 0 1 88.56 43.68 L130.16 117.46 A0.39 0.39 0 0 1 130.16 117.84 Z"/><path d="M132.68 111.67 L122.61 93.82 A0.55 0.55 0 0 1 122.62 93.28 L150.95 44.21 A0.55 0.55 0 0 1 151.90 44.21 L161.97 62.07 A0.55 0.55 0 0 1 161.96 62.61 L133.63 111.68 A0.55 0.55 0 0 1 132.68 111.67 Z"/><path d="M110.65 135.52 L90.76 135.52 A0.33 0.33 0 0 1 90.48 135.35 L48.97 61.75 A0.33 0.33 0 0 1 48.97 61.43 L59.03 44.00 A0.33 0.33 0 0 1 59.60 44.00 L110.93 135.03 A0.33 0.33 0 0 1 110.65 135.52 Z"/><path d="M26.53 134.96 L17.16 118.32 A0.67 0.67 0 0 1 17.16 117.66 L45.57 68.46 A0.67 0.67 0 0 1 46.74 68.46 L56.11 85.09 A0.67 0.67 0 0 1 56.11 85.75 L27.70 134.96 A0.67 0.67 0 0 1 26.53 134.96 Z"/></svg></div>`;
  }

  function renderNav() {
    const chapters = (D.site.nav && D.site.nav.chapters) || [];
    const links = chapters
      .map((c) => `<a href="#${esc(c.id)}" data-nav="${esc(c.id)}">${esc(c.label)}</a>`)
      .join('');
    return `
    <nav class="inv-nav" aria-label="Chapters">
      <div class="inv-nav-inner">
        <div class="inv-brand">
          ${brandMark()}
          <div class="inv-brand-text">
            <span class="name">NAVIER</span>
            <span class="tag">Series B</span>
          </div>
        </div>
        <div class="inv-chapters">${links}</div>
      </div>
      <div class="inv-progress" id="inv-progress"></div>
    </nav>`;
  }

  /* ── §1 Hero ───────────────────────────────────────── */
  function renderHero() {
    const h = D.hero;
    const heroA = A.hero || {};
    const videoSrc = mediaPath(heroA.background_video || 'assets/hero-loop.mp4');
    const poster = mediaPath(heroA.poster || 'assets/hero-poster.jpg');
    return `
    <header class="hero" id="hero" data-home="hero">
      <div class="hero-media">
        <img class="hero-poster" src="${esc(poster)}" alt="${esc(heroA.alt || '')}" width="1280" height="720" fetchpriority="high" />
        <video class="hero-video" muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="metadata" poster="${esc(poster)}">
          <source src="${esc(videoSrc)}" type="video/mp4" />
        </video>
      </div>
      <div class="hero-scrim" aria-hidden="true"></div>
      <div class="hero-content shell-prose">
        <h1 class="hero-headline">${esc(h.headline)}</h1>
        <p class="hero-subline">${esc(h.subline)}</p>
        <div class="hero-actions">
          ${
            h.video
              ? `<button type="button" class="btn btn-primary" data-yt="${esc(h.video.youtube_id || '')}" data-embed="${esc(h.video.embed_url || '')}">${esc(h.play_button_label || 'Watch the film')}</button>`
              : ''
          }
        </div>
      </div>
      <div class="scroll-cue" id="scroll-cue">${esc((h.scroll_cue && h.scroll_cue.label) || 'Scroll')}</div>
    </header>`;
  }

  function filmCard(video, poster, homeId, label) {
    if (!video && !poster) return '';
    const p =
      poster ||
      (video && video.poster && mediaPath(video.poster)) ||
      (video && video.youtube_id
        ? `https://i.ytimg.com/vi/${video.youtube_id}/hqdefault.jpg`
        : '');
    return `
      <button type="button" class="film-card" data-home="${esc(homeId || '')}"
        data-yt="${esc((video && video.youtube_id) || '')}" data-embed="${esc((video && video.embed_url) || '')}">
        <span class="film-media">
          <img src="${esc(p)}" alt="" loading="lazy" />
          <span class="play" aria-hidden="true"><span>▶</span></span>
          ${video && video.duration ? `<span class="dur">${esc(video.duration)}</span>` : ''}
        </span>
        ${label ? `<span class="film-cap">${esc(label)}</span>` : ''}
      </button>`;
  }

  /* ── Network Shift interactive 4a ──────────────────── */
  function renderNetworkShift(s) {
    /* DESIGN-AUDIT-V4 §C — stylized coastline, State A sparse trunk, State B gold mesh */
    const nodesB = [];
    const coasts = [
      // left landmass harbors
      [80, 200], [110, 240], [140, 280], [100, 320], [160, 360], [90, 400],
      [180, 220], [200, 300], [220, 380], [150, 250], [130, 340],
      // right landmass
      [1000, 210], [1040, 250], [1080, 290], [1020, 330], [1060, 370], [1100, 410],
      [980, 280], [1120, 320], [990, 360], [1050, 200], [1090, 240],
      // island chain center
      [520, 180], [560, 200], [600, 190], [640, 210], [580, 240], [620, 260],
      [540, 280], [660, 230], [700, 250], [480, 220],
    ];
    coasts.forEach(([x, y], i) => {
      nodesB.push(`<circle class="ns-node-b" cx="${x}" cy="${y}" r="${i % 5 === 0 ? 5 : 3.5}" fill="#b99a5f" style="transition-delay:${i * 30}ms"/>`);
    });
    // arcs between random pairs (great-circle-ish curves)
    const arcs = [];
    const pts = coasts;
    for (let i = 0; i < 40; i++) {
      const a = pts[i % pts.length];
      const b = pts[(i * 7 + 3) % pts.length];
      if (a === b) continue;
      const mx = (a[0] + b[0]) / 2;
      const my = (a[1] + b[1]) / 2 - 30 - (i % 5) * 8;
      arcs.push(
        `<path class="ns-arc" d="M${a[0]} ${a[1]} Q${mx} ${my} ${b[0]} ${b[1]}" fill="none" stroke="#b99a5f" stroke-width="1" />`,
      );
    }
    // fast dots along mesh
    const dots = [];
    for (let i = 0; i < 50; i++) {
      const p = pts[i % pts.length];
      const q = pts[(i * 5 + 2) % pts.length];
      const t = (i % 10) / 10;
      const x = p[0] + (q[0] - p[0]) * t;
      const y = p[1] + (q[1] - p[1]) * t - 10;
      dots.push(`<circle class="ns-dot-fast" cx="${x}" cy="${y}" r="2.2" fill="#e0cb8f"/>`);
    }

    return `
      <div class="section-block network-shift" data-reveal data-home="claim.network_shift">
        ${s.eyebrow ? `<p class="eyebrow shell-prose">${esc(s.eyebrow)}</p>` : ''}
        ${s.headline ? `<h2 class="h2 shell-prose">${esc(s.headline)}</h2>` : ''}
        <div class="ns-wrap">
          <div class="ns-stage cinema" id="ns-stage" data-state="0">
            <svg class="ns-svg" viewBox="0 0 1200 560" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
              <defs>
                <linearGradient id="nsSea" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#0a0a0a"/>
                  <stop offset="100%" stop-color="#050505"/>
                </linearGradient>
              </defs>
              <rect width="1200" height="560" fill="url(#nsSea)"/>
              <!-- landmasses -->
              <path d="M0 120 C80 100 140 160 120 260 C100 360 40 420 0 480 Z" fill="#111318"/>
              <path d="M1200 100 C1100 90 1040 150 1060 250 C1080 360 1140 420 1200 500 Z" fill="#111318"/>
              <path d="M480 160 C520 140 620 145 680 175 C720 200 700 260 640 280 C560 300 500 250 480 160 Z" fill="#12151a"/>
              <!-- STATE A: trunk + mega ports + slow ships -->
              <g class="ns-layer-a">
                <path d="M140 300 C400 280 700 300 1060 290" fill="none" stroke="#6b7280" stroke-width="6" stroke-linecap="round" opacity="0.7"/>
                <circle cx="160" cy="298" r="12" fill="#6b7280"/>
                <circle cx="1040" cy="292" r="12" fill="#6b7280"/>
                <g fill="#6b7280">
                  <rect x="320" y="286" width="70" height="16" rx="4"/>
                  <rect x="520" y="296" width="80" height="18" rx="4"/>
                  <rect x="740" y="284" width="74" height="16" rx="4"/>
                  <rect x="900" y="300" width="60" height="14" rx="3"/>
                </g>
              </g>
              <!-- STATE B: mesh + harbors + fast dots -->
              <g class="ns-layer-b">
                ${arcs.join('')}
                ${nodesB.join('')}
                ${dots.join('')}
              </g>
            </svg>
          </div>
          <div class="ns-chip-row">
            <div class="ns-chip" id="ns-chip">
              <div class="ns-chip-label" id="ns-chip-label">${esc(s.panel_before.label)}</div>
              <div class="ns-chip-line" id="ns-chip-line">${esc(s.panel_before.line)}</div>
              <div class="ns-chip-stats" id="ns-chip-stats">${esc(s.panel_before.stats_line)}</div>
            </div>
            <div class="ns-toggle" role="group" aria-label="Network state">
              <button type="button" class="ns-btn active" data-ns="0">${esc(s.panel_before.label)}</button>
              <button type="button" class="ns-btn" data-ns="1">${esc(s.panel_after.label)}</button>
            </div>
          </div>
        </div>
        ${s.closing_line ? `<p class="ns-kicker">${nl(s.closing_line)}</p>` : ''}
      </div>`;
  }

  /* ── Team ──────────────────────────────────────────── */
  function renderTeam(s) {
    const ta = homeAssets('claim.team') || {};
    const featured = ta.featured ? mediaPath(ta.featured) : '';
    const cards = ta.cards || {};
    const logos = []; /* v4: logo strip disabled — illegible; BACKED BY text only */
    // Map people: Sampriti featured, others from cards by name match
    const people = s.people || [];
    const sam = people.find((p) => /sampriti/i.test(p.name));
    const others = people.filter((p) => p !== sam);

    function cardFor(p) {
      // match card key "Name — Role"
      let src = '';
      for (const [k, v] of Object.entries(cards)) {
        if (k.toLowerCase().includes(p.name.toLowerCase().split(' ')[0].toLowerCase()) ||
            p.name.toLowerCase().split(' ').some((w) => w.length > 3 && k.toLowerCase().includes(w.toLowerCase()))) {
          src = mediaPath(v);
          break;
        }
      }
      // direct filename fallback
      if (!src) {
        const slug = p.name.toLowerCase().replace(/\s+/g, '-');
        src = mediaPath(`assets/deck/team-${slug}.png`);
      }
      return `
        <div class="team-card">
          <div class="team-photo">${src ? `<img src="${esc(src)}" alt="${esc(p.name)}" loading="lazy" />` : ''}</div>
          <div class="team-name">${esc(p.name)}</div>
          <div class="team-role">${esc(p.role)}</div>
          <div class="team-creds">${esc(p.credentials)}</div>
        </div>`;
    }

    const logoStrip = logos
      .map((l) => `<img src="${esc(mediaPath(l))}" alt="" loading="lazy" />`)
      .join('');

    return `
      <div class="section-block team-section" data-reveal data-home="claim.team">
        ${s.title ? `<h2 class="h2 shell-prose">${esc(s.title)}</h2>` : ''}
        ${s.subhead ? `<p class="lead shell-prose team-lede">${nl(s.subhead)}</p>` : ''}
        <div class="team-layout shell-stage">
          ${
            sam
              ? `<div class="team-featured">
                  <div class="team-photo lg">${featured ? `<img src="${esc(featured)}" alt="${esc(sam.name)}" loading="lazy" />` : ''}</div>
                  <div class="team-name">${esc(sam.name)}</div>
                  <div class="team-role">${esc(sam.role)}</div>
                  <div class="team-creds">${esc(sam.credentials)}</div>
                </div>`
              : ''
          }
          <div class="team-grid">${others.map(cardFor).join('')}</div>
        </div>
        ${logoStrip ? `<div class="logo-strip shell-stage" aria-label="Pedigree">${logoStrip}</div>` : ''}
        ${
          s.backers_line
            ? `<div class="backers shell-prose"><div class="bl">${esc(s.backers_label || 'BACKED BY')}</div><div class="line">${nl(s.backers_line)}</div></div>`
            : ''
        }
      </div>`;
  }

  /* ── Section renderers ─────────────────────────────── */
  const R = {
    'text-block'(s) {
      // About Navier — manifesto under fleet plate
      const body = s.body || '';
      const goldPhrase = '5× less energy';
      let htmlBody = nl(body);
      if (body.includes(goldPhrase)) {
        htmlBody = esc(body)
          .replace(/\n/g, '<br/>')
          .replace(goldPhrase, `<span class="gold-em">${goldPhrase}</span>`);
      }
      return `
        <div class="section-block manifesto" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <p class="manifesto-body">${htmlBody}</p>
        </div>`;
    },

    'two-panel-transition'(s) {
      return renderNetworkShift(s);
    },

    'pill-sequence'(s) {
      const pills = (s.pills || [])
        .map((p, i) => {
          const isNow = s.now_marker_on != null && i + 1 === s.now_marker_on;
          return `
          <div class="arc-phase" data-pill="${i}">
            ${isNow ? `<span class="now-badge">${esc(s.now_label || 'NOW')}</span>` : ''}
            <div class="arc-num">${esc(p.number)}</div>
            <div class="arc-body">
              <div class="title">${esc(p.title)}</div>
              <div class="detail">${esc(p.detail)}</div>
              <div class="meta">${esc(p.program || '')} · ${esc(p.market || '')}</div>
            </div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block arc-section" data-reveal data-pills data-now="${s.now_marker_on || 0}">
          ${s.headline ? `<h2 class="h2 shell-prose">${esc(s.headline)}</h2>` : ''}
          <div class="arc-spine shell-stage">${pills}</div>
        </div>`;
    },

    'team-grid'(s) {
      return renderTeam(s);
    },

    'flip-cards'(s) {
      // Three costs — 3-up with gold numerals, heritage divider before is injected by claim chapter
      const cards = (s.pairs || [])
        .map((pair, i) => {
          const n = String(i + 1).padStart(2, '0');
          return `
          <div class="cost-card" data-flip="${i}">
            <div class="cost-num">${n}</div>
            <div class="cost-front">
              <div class="t">${esc(pair.cost.title)}</div>
              <div class="b">${esc(pair.cost.body)}</div>
            </div>
            <div class="cost-lever">
              <div class="t">${esc(pair.lever.title)}</div>
              <div class="mech">${esc(pair.lever.mechanism)}</div>
              <div class="b">${esc(pair.lever.proof)}</div>
            </div>
          </div>`;
        })
        .join('');
      const why = s.why_now
        ? `<div class="why-now shell-stage">
            <h3 class="h3">${esc(s.why_now.title)}</h3>
            <p class="body-text">${nl(s.why_now.body || s.why_now.line || '')}</p>
            ${s.why_now.closing_line ? `<p class="closing-line">${esc(s.why_now.closing_line)}</p>` : ''}
          </div>`
        : '';
      return `
        <div class="section-block" data-reveal data-home="claim.three_costs">
          ${s.headline ? `<h2 class="h2 shell-prose">${esc(s.headline)}</h2>` : ''}
          ${s.subhead ? `<p class="lead shell-prose">${esc(s.subhead)}</p>` : ''}
          ${s.costs_kicker ? `<p class="kicker shell-prose">${esc(s.costs_kicker)}</p>` : ''}
          ${s.flip_headline ? `<p class="eyebrow shell-prose" style="margin-top:28px">${esc(s.flip_headline)}</p>` : ''}
          <div class="cost-grid shell-stage">${cards}</div>
          ${why}
        </div>`;
    },

    'stat-counters'(s) {
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
        </div>`;
    },

    'video-grid'(s) {
      const demos = homeAssets('proof.demo_grid') || {};
      const idMap = {
        'no-wake': 'no_wake',
        'flat-turning': 'flat_turn',
        'rough-seas': 'rough_seas',
        takeoff: 'foiling_18s',
        stabilization: 'anchor',
      };
      const clips = s.clips || [];
      const anchor = clips.find((c) => c.play_mode === 'loop' || c.id === 'stabilization');
      const rest = clips.filter((c) => c !== anchor);
      const anchorSrc = mediaPath(
        demos.anchor_full_width_native_loop || (anchor && anchor.asset) || 'assets/stabilization-juxtaposition.mp4',
      );

      const cards = rest
        .map((c) => {
          const key = idMap[c.id] || c.id;
          const poster = demos[key]
            ? mediaPath(demos[key])
            : c.poster
              ? mediaPath(c.poster)
              : c.youtube_id
                ? `https://i.ytimg.com/vi/${c.youtube_id}/hqdefault.jpg`
                : '';
          return `
          <button type="button" class="vcard"
            data-yt="${esc(c.youtube_id || '')}" data-embed="${esc(c.embed_url || '')}">
            <span class="vcard-media">
              <img src="${esc(poster)}" alt="" loading="lazy" />
              <span class="play"><span>▶</span></span>
              ${c.duration ? `<span class="dur">${esc(c.duration)}</span>` : ''}
            </span>
            <span class="vcard-cap">${esc(c.caption || c.title || '')}</span>
          </button>`;
        })
        .join('');

      return `
        <div class="section-block" data-reveal data-home="proof.demo_grid">
          ${s.title ? `<h2 class="h2 shell-prose">${esc(s.title)}</h2>` : ''}
          ${
            anchorSrc
              ? `<div class="demo-anchor shell-stage">
                  <video src="${esc(anchorSrc)}" muted playsinline loop preload="none" data-lazy-video></video>
                  <p class="vcard-cap">${esc((anchor && (anchor.caption || anchor.title)) || '')}</p>
                </div>`
              : ''
          }
          <div class="video-grid shell-stage">${cards}</div>
        </div>`;
    },

    timeline(s) {
      const sticky = (s.stat_chips || [])
        .filter((c) => c.sticky !== false)
        .map((c) => {
          if (typeof c === 'string') return `<span class="chip">${esc(c)}</span>`;
          return `<span class="chip"><strong data-counter="${esc(c.value || '')}">${esc(c.value || c.label || '')}</strong>${c.detail ? ` · ${esc(c.detail)}` : ''}</span>`;
        })
        .join('');
      const items = (s.milestones || [])
        .map(
          (m) => `
        <div class="tl-item">
          <div class="tl-year">${esc(m.year)}</div>
          <ul>${(m.items || []).map((it) => `<li>${esc(it)}</li>`).join('')}</ul>
        </div>`,
        )
        .join('');
      const plate = homeSrc('proof.traction.plate');
      return `
        <div class="section-block" data-reveal data-home="proof.traction.plate">
          ${s.title ? `<h2 class="h2 shell-prose">${esc(s.title)}</h2>` : ''}
          ${sticky ? `<div class="sticky-chips shell-stage">${sticky}</div>` : ''}
          ${s.kicker ? `<p class="kicker shell-prose">${esc(s.kicker)}</p>` : ''}
          ${plate ? cinema(plate, { home: 'proof.traction.plate', vh: '50vh' }) : ''}
          <div class="timeline shell-stage">${items}</div>
          ${s.closing_line ? `<p class="closing-line shell-prose">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'hotspot-diagram'(s) {
      const filmPoster = homeSrc('product.control.film') || mediaPath('assets/posters/S7WB91FvSFI.jpg');
      const hs = (s.hotspots || [])
        .map(
          (h) => `
        <div class="hotspot-item"><strong>${esc(h.label)}</strong>
          ${h.detail ? `<div class="muted">${esc(h.detail)}</div>` : ''}</div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal data-home="product.control.film">
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.body ? `<p class="body-text shell-prose">${nl(s.body)}</p>` : ''}
          <div class="media-duo">
            ${s.video ? filmCard(s.video, filmPoster, 'product.control.film', s.video_label || '') : ''}
            <div class="hotspot-list">${hs}</div>
          </div>
        </div>`;
    },

    'platform-intro'(s) {
      const wire = homeSrc('product.gmvp.diagram');
      const foundry = homeSrc('product.foundry.plate');
      const fCap = homeCap('product.foundry.plate');
      const layers = (s.layers || [])
        .map(
          (l) => `
        <div class="layer"><div class="name">${esc(l.name)}</div>
          ${l.detail ? `<div class="detail">${esc(l.detail)}</div>` : ''}</div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal data-home="product.gmvp.diagram">
          ${s.title ? `<h2 class="h2 shell-prose">${esc(s.title)}</h2>` : ''}
          ${s.body ? `<p class="body-text shell-prose">${nl(s.body)}</p>` : ''}
          <div class="shell-stage">${wire ? plate(wire, { home: 'product.gmvp.diagram', className: 'wire-plate' }) : ''}
          <div class="layers">${layers}</div></div>
          ${s.tagline ? `<p class="closing-line shell-prose">${esc(s.tagline)}</p>` : ''}
          ${foundry ? cinema(foundry, { home: 'product.foundry.plate', caption: fCap, vh: '62vh' }) : ''}
        </div>`;
    },

    interactive(s) {
      if (s.component === 'vessel-ladder-explorer' || s.data === 'ladder.json') return renderLadder(s);
      if (s.component === 'unit-econ-toggle' || s.data === 'unitecon.json') return renderUnitEcon(s);
      if (s.component === 'pipeline-map' || s.data === 'pipeline-map.json') return renderPipeline(s);
      return '';
    },

    'chapter-break'(s) {
      // Quanta interstitial — film + defense (v3: quanta home)
      const qa = homeAssets('product.quanta') || {};
      const filmP = qa.film ? mediaPath(qa.film) : homeSrc('product.quanta') ;
      const defense = qa.defense_plate ? mediaPath(qa.defense_plate) : '';
      return `
        <div class="section-block chapter-break shell-stage" data-reveal data-home="product.quanta">
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.headline ? `<p class="break-headline">${esc(s.headline)}</p>` : ''}
          <div class="media-duo">
            ${s.video ? filmCard(s.video, filmP, 'product.quanta', s.video_label || '') : ''}
            ${defense ? plate(defense, { home: 'product.quanta', className: '' }) : ''}
          </div>
        </div>`;
    },

    'stat-chips'(s) {
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
        </div>`;
    },

    'two-door'(s) {
      const qa = homeAssets('product.quanta') || {};
      const atlantic = qa.atlantic_map ? mediaPath(qa.atlantic_map) : '';
      const doors = (s.doors || [])
        .map(
          (d) => `
        <div class="door"><div class="title">${esc(d.title)}</div><div class="detail">${esc(d.detail)}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="media-duo">
            <div>
              <div class="doors">${doors}</div>
              ${
                s.third_point
                  ? `<div class="third-point"><strong>${esc(s.third_point.title)}</strong> — ${esc(s.third_point.detail)}</div>`
                  : ''
              }
              ${s.atlantic_run ? `<div class="atlantic">${esc(s.atlantic_run.line || s.atlantic_run)}</div>` : ''}
              ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
            </div>
            ${atlantic ? plate(atlantic, { home: 'product.quanta', className: '' }) : ''}
          </div>
        </div>`;
    },

    'comparison-table'(s) {
      // No photo plate (v3 §13)
      const cols = s.columns || [];
      const labels = s.row_labels || [];
      const head = `<tr><th></th>${cols
        .map(
          (c) =>
            `<th class="${c.highlight ? 'hi' : ''}">${esc(c.name)}${
              c.vessel_type ? `<div class="th-sub">${esc(c.vessel_type)}</div>` : ''
            }</th>`,
        )
        .join('')}</tr>`;
      const rows = labels
        .map((lab, ri) => {
          const cells = cols
            .map((c) => `<td class="${c.highlight ? 'hi' : ''}">${esc((c.values && c.values[ri]) || '')}</td>`)
            .join('');
          return `<tr><td class="row-label">${esc(lab)}</td>${cells}</tr>`;
        })
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal data-home="gtm.competitive">
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="table-wrap"><table class="cmp"><thead>${head}</thead><tbody>${rows}</tbody></table></div>
        </div>`;
    },

    'signed-contract-hero'(s) {
      const ga = homeAssets('gtm.maldives') || {};
      // opener is chapter divider; inset here
      const inset = ga.inset ? mediaPath(ga.inset) : '';
      const filmP = ga.film_card ? mediaPath(ga.film_card) : '';
      return `
        <div class="section-block shell-stage" data-reveal data-home="gtm.maldives">
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
          <div class="media-duo">
            ${inset ? plate(inset, { home: 'gtm.maldives', className: '' }) : ''}
            <div>
              ${s.press_label ? `<p class="eyebrow">${esc(s.press_label)}</p>` : ''}
              <div class="press">${(s.press || [])
                .map(
                  (p) => `
                <div class="press-item"><div class="outlet">${esc(p.outlet)}</div><div class="quote">${esc(p.quote)}</div></div>`,
                )
                .join('')}</div>
              ${filmP ? filmCard({ youtube_id: 'htUWE3AJUbc', embed_url: 'https://www.youtube-nocookie.com/embed/htUWE3AJUbc' }, filmP, 'gtm.maldives', '') : ''}
            </div>
          </div>
        </div>`;
    },

    'program-panel'(s) {
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
          <div class="proof-chips">${(s.proof_chips || [])
            .map(
              (c) => `
            <div class="proof-chip"><div class="label">${esc(c.label)}</div><div class="detail">${esc(c.detail)}</div></div>`,
            )
            .join('')}</div>
          ${s.program_line ? `<p class="eyebrow">${esc(s.program_line)}</p>` : ''}
          <div class="buyers">${(s.buyers || []).map((b) => `<span>${esc(b)}</span>`).join('')}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'stacked-cards'(s) {
      const cards = (s.cards || [])
        .map(
          (c) => `
        <div class="stack-card"><div class="num">${esc(c.number)}</div>
          <div><div class="h3" style="margin:0 0 6px">${esc(c.title)}</div><div class="muted">${esc(c.body)}</div></div></div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          <div class="stack-cards">${cards}</div>
          ${s.formula_line ? `<div class="formula">${esc(s.formula_line)}</div>` : ''}
        </div>`;
    },

    'four-role-diagram'(s) {
      const roles = (s.roles || s.cards || [])
        .map((r, i) => {
          const title = r.title || r.name || r.role;
          const does = r.does || r.body || r.detail || '';
          return `
          <div class="flow-role">
            ${i ? '<div class="flow-arrow" aria-hidden="true">→</div>' : ''}
            <div class="role">
              ${r.tag ? `<div class="eyebrow" style="margin:0 0 6px">${esc(r.tag)}</div>` : ''}
              <div class="title">${esc(title)}</div>
              <div class="muted">${esc(does)}</div>
              ${r.earns ? `<div class="muted" style="margin-top:8px;color:var(--accent)">${esc(r.earns)}</div>` : ''}
            </div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead || s.intro ? `<p class="lead">${esc(s.subhead || s.intro)}</p>` : ''}
          <div class="flow-roles">${roles}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'drawing-chart'(s) {
      const cargo = homeAssets('gtm.cargo') || {};
      const opener = cargo.opener ? mediaPath(cargo.opener) : '';
      const play = cargo.play ? mediaPath(cargo.play) : '';
      const night = cargo.night_pair || [];
      let openHtml = opener
        ? cinema(opener, {
            home: 'gtm.cargo',
            caption: (home('gtm.cargo') && home('gtm.cargo').treatment) || '',
            vh: '58vh',
          })
        : '';
      // caption from assets if present
      const cargoHome = home('gtm.cargo');
      // use a sensible caption from chart if needed - assets don't have caption on cargo in v3 except treatment
      // Air freight caption from remediation: use island or chart

      let chartHtml = '';
      if (s.chart) {
        const c = s.chart;
        const cards = ['air', 'ocean', 'gap']
          .filter((k) => c[k])
          .map((k) => {
            const x = c[k];
            return `<div class="chip-card">
              <div class="t">${esc(x.label || k)}</div>
              ${x.price ? `<div class="chip-num">${esc(x.price)}</div>` : ''}
              ${x.value ? `<div class="chip-num ok">${esc(x.value)}</div>` : ''}
              <div class="b">${esc(x.time || x.detail || x.line || '')}</div>
            </div>`;
          })
          .join('');
        chartHtml = `
          <div class="shell-stage">
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            <div class="chips-3">${cards}</div>
            ${c.navier_band ? `<div class="formula">${esc(c.navier_band)}</div>` : ''}
          </div>`;
      }
      // island_band as structured object (G3 fix)
      let islandHtml = '';
      const ib = s.island_band;
      if (ib && typeof ib === 'object') {
        islandHtml = `
          <div class="island-band shell-stage" data-reveal>
            ${ib.title ? `<h3 class="h3">${esc(ib.title)}</h3>` : ''}
            <div class="gold-stat-band cols-${Math.min((ib.stats || []).length, 3)}">
              ${(ib.stats || [])
                .map(
                  (st) => `
                <div class="gold-stat">
                  <div class="value">${esc(st.value)}</div>
                  <div class="label">${esc(st.label)}</div>
                  ${st.source ? `<div class="muted tiny">${esc(st.source)}</div>` : ''}
                </div>`,
                )
                .join('')}
            </div>
            ${ib.footnote ? `<p class="muted">${esc(ib.footnote)}</p>` : ''}
          </div>`;
      } else if (typeof ib === 'string') {
        islandHtml = `<p class="kicker shell-prose">${esc(ib)}</p>`;
      }

      return `
        <div class="section-block" data-reveal data-home="gtm.cargo">
          ${openHtml}
          ${chartHtml}
          ${islandHtml}
          ${play ? plate(play, { home: 'gtm.cargo', className: 'shell-stage' }) : ''}
          ${
            night.length
              ? `<div class="foundry-pair shell-stage">
                  ${night.map((n) => plate(mediaPath(n), { home: 'gtm.cargo' })).join('')}
                </div>`
              : ''
          }
        </div>`;
    },

    'three-chips'(s) {
      const chips = (s.chips || s.cards || [])
        .map(
          (c) => `
        <div class="chip-card"><div class="t">${esc(c.title || c.label)}</div><div class="b">${esc(c.body || c.detail || '')}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro || s.subhead ? `<p class="lead">${esc(s.intro || s.subhead)}</p>` : ''}
          <div class="chips-3">${chips}</div>
        </div>`;
    },

    'stat-panel'(s) {
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro || s.subhead ? `<p class="lead">${esc(s.intro || s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'day-night-flip'(s) {
      const chips = (s.chips || [])
        .map(
          (c) => `
        <div class="chip-card"><div class="t">${esc(c.title || c.label)}</div><div class="b">${esc(c.body || c.detail || '')}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          <div class="chips-3">${chips}</div>
        </div>`;
    },

    'card-row'(s) {
      const ctv = homeSrc('gtm.service.plate');
      const cards = (s.cards || s.chips || [])
        .map(
          (c) => `
        <div class="c"><div class="h3" style="margin:0 0 6px">${esc(c.title || c.label)}</div><div class="muted">${esc(c.body || c.detail || '')}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal data-home="gtm.service.plate">
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro || s.subhead ? `<p class="lead">${esc(s.intro || s.subhead)}</p>` : ''}
          <div class="media-duo">
            <div class="card-row">${cards}</div>
            ${ctv ? plate(ctv, { home: 'gtm.service.plate', className: '' }) : ''}
          </div>
        </div>`;
    },

    'defense-panel'(s) {
      const da = homeAssets('gtm.defense') || {};
      const plateSrc = da.plate ? mediaPath(da.plate) : '';
      const inset = da.inset ? mediaPath(da.inset) : '';
      const quote = s.pull_quote
        ? `<blockquote class="defense-quote">
            <p>${esc(s.pull_quote.quote || '')}</p>
            <cite>${esc(s.pull_quote.attribution || '')}</cite>
          </blockquote>`
        : '';
      const blocks = (s.blocks || [])
        .map(
          (b) => `
        <div class="chip-card"><div class="t">${esc(b.title || '')}</div><div class="b">${nl(b.body || b.detail || '')}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal data-home="gtm.defense">
          ${s.title ? `<h2 class="h2 shell-prose">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead shell-prose">${esc(s.subhead)}</p>` : ''}
          ${s.intro ? `<p class="body-text shell-prose">${esc(s.intro)}</p>` : ''}
          ${
            plateSrc
              ? `<div class="cinema defense-cinema" data-home="gtm.defense">
                  <div class="cinema-media" style="height:62vh">
                    <img src="${esc(plateSrc)}" alt="" loading="lazy" />
                    ${quote}
                  </div>
                </div>`
              : quote
          }
          <div class="shell-stage">
            ${inset ? plate(inset, { home: 'gtm.defense' }) : ''}
            ${blocks}
            ${s.deployment_line ? `<p class="closing-line">${esc(s.deployment_line)}</p>` : ''}
            ${s.fine_print ? `<p class="muted">${esc(s.fine_print)}</p>` : ''}
          </div>
        </div>`;
    },

    'horizontal-bars'(s) {
      // G3: totals as structured gold floor band
      const segs = s.segments || [];
      const max = Math.max(...segs.map((b) => (b.bar_value_range && b.bar_value_range[1]) || 1), 1);
      const bars = segs
        .map((b) => {
          const hi = (b.bar_value_range && b.bar_value_range[1]) || 1;
          const pct = Math.round((hi / max) * 100);
          return `
          <div class="bar-row" data-bar-pct="${pct}">
            <div class="meta">
              <span><strong>${esc(b.name || b.label || '')}</strong></span>
              <span>${esc(b.dollars_floor || b.value || '')}</span>
            </div>
            ${b.demand_pool ? `<div class="muted tiny">${esc(b.demand_pool)}</div>` : ''}
            <div class="bar-track"><div class="bar-fill"></div></div>
            ${b.vessels_floor ? `<div class="muted tiny mt-xs">${esc(b.vessels_floor)} vessels</div>` : ''}
          </div>`;
        })
        .join('');
      const t = s.totals;
      let floor = '';
      if (t && typeof t === 'object') {
        floor = `
          <div class="floor-band" data-reveal>
            <div class="floor-label">${esc(t.label || '')}</div>
            <div class="floor-vessels">${esc(t.vessels || '')}</div>
            <div class="floor-line">${esc(t.line || '')}</div>
          </div>`;
      } else if (typeof t === 'string') {
        floor = `<p class="closing-line">${esc(t)}</p>`;
      }
      return `
        <div class="section-block shell-stage" data-reveal data-bars>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="chart-block">${bars}</div>
          ${floor}
          ${s.source_line ? `<p class="muted">${esc(s.source_line)}</p>` : ''}
        </div>`;
    },

    'stat-band'(s) {
      // Money open — stats + native-ish charts from PNGs at contain + simple SVG from stats
      const rev = mediaPath('assets/deck/chart-revenue-by-segment.png');
      const ebitda = mediaPath('assets/deck/chart-ebitda-margin.png');
      return `
        <div class="section-block shell-stage" data-reveal data-home="money.charts">
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
          ${s.footnote ? `<p class="muted">${esc(s.footnote)}</p>` : ''}
          <div class="money-charts">
            <figure class="chart-native" data-reveal>
              <figcaption class="eyebrow">Revenue by segment (conservative case)</figcaption>
              <img src="${esc(rev)}" alt="Revenue by segment chart" loading="lazy" />
            </figure>
            <figure class="chart-native" data-reveal>
              <figcaption class="eyebrow">EBITDA margin</figcaption>
              <img src="${esc(ebitda)}" alt="EBITDA margin chart" loading="lazy" />
            </figure>
          </div>
          <div class="native-stat-bars" data-bars data-reveal>
            ${(s.stats || [])
              .map((st, i) => {
                const pct = [85, 25, 95, 70][i] || 50;
                return `<div class="bar-row" data-bar-pct="${pct}">
                  <div class="meta"><span>${esc(st.label)}</span><span class="accent">${esc(st.value)}</span></div>
                  <div class="bar-track"><div class="bar-fill"></div></div>
                </div>`;
              })
              .join('')}
          </div>
        </div>`;
    },

    'four-column-roadmap'(s) {
      const cols = (s.columns || [])
        .map(
          (c) => `
        <div class="rm-col">
          <div class="period">${esc(c.period)}</div>
          <ul>${(c.items || []).map((it) => `<li>${esc(it)}</li>`).join('')}</ul>
          <div class="focus">${esc(s.focus_label || 'FOCUS')}: ${esc(c.focus || '')}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="roadmap">${cols}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'status-rows'(s) {
      // Five markets thesis board with thumbs
      const thumbs = (home('money.thesis_board.thumbs') && home('money.thesis_board.thumbs').assets) || [];
      const rows = (s.rows || [])
        .map((r, i) => {
          const thumb = thumbs[i] ? mediaPath(thumbs[i]) : '';
          return `
          <div class="thesis-row">
            ${thumb ? `<div class="thesis-thumb"><img src="${esc(thumb)}" alt="" loading="lazy" /></div>` : ''}
            <div class="label">${esc(r.label)}</div>
            <div class="status">${esc(r.status)}</div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal data-home="money.thesis_board.thumbs">
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          <div class="thesis-board">${rows}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'two-column-round'(s) {
      const cols = (s.columns || [])
        .map(
          (c) => `
        <div class="round-col">
          <h3>${esc(c.title)}</h3>
          <ul>${(c.items || []).map((it) => `<li>${esc(it)}</li>`).join('')}</ul>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
          <div class="round">${cols}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'finale-plate'(s) {
      const close = homeAssets('close') || {};
      const vsrc = mediaPath(close.video || 'assets/closing-loop.mp4');
      return `
        <section class="finale" id="finale" data-home="close">
          <div class="finale-media">
            <video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="none" data-lazy-video>
              <source src="${esc(vsrc)}" type="video/mp4" />
            </video>
          </div>
          <div class="finale-scrim" aria-hidden="true"></div>
          <div class="finale-inner">
            <p class="h">${esc(s.headline)}</p>
            <p class="mark">${esc(s.closing_mark || 'OWN THE EDGE')}</p>
            ${s.cta ? `<a class="btn btn-primary" href="${esc(s.cta.href)}">${esc(s.cta.label)}</a>` : ''}
          </div>
        </section>`;
    },

    footer(s) {
      const close = homeAssets('close') || {};
      const vance = close.go_deeper_film ? mediaPath(close.go_deeper_film) : '';
      return `
        <section class="go-deeper" id="go-deeper">
          <div class="shell-stage go-deeper-inner">
            <p class="chapter-label">${esc(s.title || 'Go deeper')}</p>
            <div class="go-deeper-grid">
              ${s.video ? filmCard(s.video, vance, 'close', s.video_label || (s.video && s.video.title) || '') : ''}
              <div class="go-deeper-cta">
                ${s.contact ? `<a class="btn btn-primary" href="${esc(s.contact.href)}">${esc(s.contact.label)}</a>` : ''}
                <p class="muted foot-legal">Privileged &amp; Confidential · Distribution without consent is strictly prohibited · © 2026 Navier</p>
              </div>
            </div>
          </div>
        </section>`;
    },
  };

  /* ── Interactives ──────────────────────────────────── */
  function ladderImg(hull) {
    if (!hull) return { src: '', photo: false, dev: false };
    const la = homeAssets('product.ladder') || {};
    const key = String(hull.id).replace(/-/g, '_');
    // Canon: N30 may use pioneer photo; N45/N80/N180 wireframe only; Quanta = quanta render (30ft class real)
    const id = hull.id || '';
    if (id === 'n30-pioneer' && la.n30_pioneer) {
      return { src: mediaPath(la.n30_pioneer), photo: true, dev: false };
    }
    if (id === 'quanta-lr' && la.quanta_lr) {
      return { src: mediaPath(la.quanta_lr), photo: true, dev: false };
    }
    // Prefer per-class wireframe
    if (la[key]) return { src: mediaPath(la[key]), photo: false, dev: true };
    // Map to fleet-wireframe-* keys
    const wfMap = {
      'n30-pioneer': 'n30_wireframe',
      'n45-explorer': 'n45_explorer',
      'n80-valkyrie': 'n80_valkyrie',
      'n180-morpheus': 'n180_morpheus',
    };
    const wf = la[wfMap[id]];
    if (wf) return { src: mediaPath(wf), photo: false, dev: id !== 'n30-pioneer' };
    if (la.base) return { src: mediaPath(la.base), photo: false, dev: true };
    return { src: '', photo: false, dev: false };
  }

  function renderLadder(s) {
    const hulls = (D.ladder && D.ladder.hulls) || [];
    const tabs = hulls
      .map(
        (h, i) =>
          `<button type="button" class="ladder-tab ${i === 0 ? 'active' : ''}" data-hull="${i}">
            <span class="lt-name">${esc(h.name)}</span>
            <span class="lt-mission">${esc(h.mission || '')}</span>
          </button>`,
      )
      .join('');
    const first = ladderImg(hulls[0]);
    return `
      <div class="section-block shell-stage" data-reveal data-home="product.ladder">
        ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
        <div class="ladder" id="ladder">
          <div class="ladder-tabs">${tabs}</div>
          <div class="ladder-body">
            <div class="ladder-plate ${first.photo ? 'photo' : ''}" id="ladder-plate">
              ${first.src ? `<img src="${esc(first.src)}" alt="" id="ladder-img" />` : ''}
            </div>
            <div class="ladder-meta" id="ladder-meta"></div>
          </div>
          <div class="ladder-scale" id="ladder-scale" aria-hidden="true"></div>
        </div>
      </div>`;
  }

  function renderUnitEcon() {
    const u = D.unitecon;
    if (!u) return '';
    const tabs = (u.panels || [])
      .map(
        (p, i) =>
          `<button type="button" class="ue-tab ${i === 0 ? 'active' : ''}" data-ue="${i}">${esc(p.class_label)}</button>`,
      )
      .join('');
    return `
      <div class="section-block shell-stage" data-reveal>
        ${u.eyebrow ? `<p class="eyebrow">${esc(u.eyebrow)}</p>` : ''}
        ${u.title ? `<h2 class="h2">${esc(u.title)}</h2>` : ''}
        <div class="unitecon" id="unitecon">
          <div class="ue-tabs">${tabs}</div>
          <div class="ue-body" id="ue-body"></div>
        </div>
      </div>`;
  }

  function renderPipeline() {
    const p = D['pipeline-map'];
    if (!p) return '';
    const mapSrc = homeSrc('gtm.pipeline.map');
    const stats = goldStats(p.gold_stats || []);
    const tiers = (p.tiers || [])
      .map((t) => {
        const rows = (t.rows || [])
          .map(
            (r) => `
          <div class="pipe-row"><div class="party">${esc(r.party)}</div><div class="status">${esc(r.status)}</div></div>`,
          )
          .join('');
        return `<div class="pipe-tier"><h3>${esc(t.name)}</h3>${rows}</div>`;
      })
      .join('');
    return `
      <div class="section-block" data-reveal data-home="gtm.pipeline.map">
        ${p.eyebrow ? `<p class="eyebrow shell-prose">${esc(p.eyebrow)}</p>` : ''}
        ${p.title ? `<h2 class="h2 shell-prose">${esc(p.title)}</h2>` : ''}
        <div class="shell-stage">${stats}</div>
        ${mapSrc ? cinema(mapSrc, { home: 'gtm.pipeline.map', vh: '75vh' }) : ''}
        <div class="pipe-tiers shell-stage">${tiers}</div>
        <div class="pipe-foot shell-prose">
          ${p.coverage_line ? `<div>${esc(p.coverage_line)}</div>` : ''}
          ${p.capital_efficiency_line ? `<div class="accent-line">${esc(p.capital_efficiency_line)}</div>` : ''}
        </div>
      </div>`;
  }

  /* ── Chapters ──────────────────────────────────────── */
  function claimChapter() {
    const data = D.claim;
    if (!data) return '';
    const fleet = homeSrc('claim.opener');
    const heritage = homeSrc('claim.three_costs.divider');
    const secs = data.sections || [];
    const parts = [];
    // cinema opener
    if (fleet) parts.push(cinema(fleet, { home: 'claim.opener', caption: homeCap('claim.opener'), vh: '72vh', eager: true }));
    for (const sec of secs) {
      if (sec.id === 'costs-levers' && heritage) {
        parts.push(cinema(heritage, { home: 'claim.three_costs.divider', caption: homeCap('claim.three_costs.divider'), vh: '58vh' }));
      }
      const fn = R[sec.type];
      if (fn) parts.push(fn(sec));
    }
    return `
      <section class="chapter" id="claim">
        <div class="shell-prose"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
        ${parts.join('')}
      </section>`;
  }

  function proofChapter() {
    const data = D.proof;
    if (!data) return '';
    const div = homeSrc('proof.divider');
    const parts = [];
    if (div) parts.push(cinema(div, { home: 'proof.divider', caption: homeCap('proof.divider'), vh: '68vh' }));
    for (const sec of data.sections || []) {
      const fn = R[sec.type];
      if (fn) parts.push(fn(sec));
    }
    return `
      <section class="chapter" id="proof">
        <div class="shell-prose"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
        ${parts.join('')}
      </section>`;
  }

  function productChapter() {
    const data = D.product;
    if (!data) return '';
    // product chapter: no wrong maldives plate; quanta-dark is traction not product opener
    const parts = [];
    for (const sec of data.sections || []) {
      // competitive table has no plate
      const fn = R[sec.type];
      if (fn) parts.push(fn(sec));
    }
    return `
      <section class="chapter" id="product">
        <div class="shell-prose"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
        ${parts.join('')}
      </section>`;
  }

  function gtmChapter() {
    const data = D.gtm;
    if (!data) return '';
    const maldives = (homeAssets('gtm.maldives') || {}).opener
      ? mediaPath(homeAssets('gtm.maldives').opener)
      : '';
    const parts = [];
    if (maldives) {
      parts.push(
        cinema(maldives, {
          home: 'gtm.maldives',
          caption: 'Maldives — $100M signed, 100 vessels.',
          vh: '70vh',
        }),
      );
    }
    for (const sec of data.sections || []) {
      // cargo-gap handles its own air-vs-ocean opener
      const fn = R[sec.type];
      if (fn) parts.push(fn(sec));
    }
    return `
      <section class="chapter" id="gtm">
        <div class="shell-prose"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
        ${parts.join('')}
      </section>`;
  }

  function moneyChapter() {
    const data = D.money;
    if (!data) return '';
    const main = (data.sections || []).filter((s) => s.type !== 'finale-plate' && s.type !== 'footer');
    const finale = (data.sections || []).find((s) => s.type === 'finale-plate');
    const foot = (data.sections || []).find((s) => s.type === 'footer');
    const mainHtml = main
      .map((sec) => {
        const fn = R[sec.type];
        return fn ? fn(sec) : '';
      })
      .join('');
    return `
      <section class="chapter" id="money">
        <div class="shell-prose"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
        ${mainHtml}
        ${finale ? R['finale-plate'](finale) : ''}
        ${foot ? R.footer(foot) : ''}
      </section>`;
  }

  /* ── Mount ─────────────────────────────────────────── */
  const app = document.getElementById('app');
  app.innerHTML = `
    ${renderNav()}
    ${renderHero()}
    ${claimChapter()}
    ${proofChapter()}
    ${productChapter()}
    ${gtmChapter()}
    ${moneyChapter()}
    <footer class="site-footer">
      <div class="shell-prose">${esc((D.site.footer && D.site.footer.confidentiality_line) || '')}</div>
    </footer>
    <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video">
      <div class="lightbox-inner">
        <button type="button" class="lightbox-close" id="lb-close" aria-label="Close">×</button>
        <div id="lb-frame"></div>
      </div>
    </div>
  `;

  /* ── Lightbox ──────────────────────────────────────── */
  function openYt(embedUrl, youtubeId) {
    const url =
      embedUrl ||
      (youtubeId ? `https://www.youtube-nocookie.com/embed/${youtubeId}?autoplay=1&rel=0` : null);
    if (!url) return;
    const src = url.includes('?') ? `${url}&autoplay=1` : `${url}?autoplay=1&rel=0`;
    $('#lb-frame').innerHTML = `<iframe src="${esc(src)}" width="100%" height="100%" style="position:absolute;inset:0;width:100%;height:100%;border:0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen title="Video"></iframe>`;
    $('#lightbox').classList.add('open');
  }
  function closeLb() {
    $('#lightbox').classList.remove('open');
    $('#lb-frame').innerHTML = '';
  }
  $('#lb-close').addEventListener('click', closeLb);
  $('#lightbox').addEventListener('click', (e) => {
    if (e.target.id === 'lightbox') closeLb();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLb();
  });
  document.body.addEventListener('click', (e) => {
    const t = e.target.closest('[data-yt]');
    if (!t || t.classList.contains('looping')) return;
    const yt = t.getAttribute('data-yt');
    const emb = t.getAttribute('data-embed');
    if (yt || emb) {
      e.preventDefault();
      openYt(emb, yt);
    }
  });

  /* ── Network shift toggle + scroll ─────────────────── */
  function setNs(state) {
    const stage = $('#ns-stage');
    if (!stage) return;
    stage.dataset.state = state;
    stage.classList.toggle('state-b', state === 1);
    const nsSec = (D.claim && D.claim.sections || []).find((x) => x.id === 'network-shift' || x.type === 'two-panel-transition');
    const panel = nsSec && (state === 1 ? nsSec.panel_after : nsSec.panel_before);
    if (panel) {
      const lab = $('#ns-chip-label');
      const line = $('#ns-chip-line');
      const stats = $('#ns-chip-stats');
      if (lab) lab.textContent = panel.label || '';
      if (line) line.textContent = panel.line || '';
      if (stats) stats.textContent = panel.stats_line || '';
    }
    document.querySelectorAll('.ns-btn').forEach((btn) => {
      btn.classList.toggle('active', +btn.dataset.ns === state);
    });
  }
  document.querySelectorAll('.ns-btn').forEach((btn) => {
    btn.addEventListener('click', () => setNs(+btn.dataset.ns));
  });
  // scroll-linked on ns-stage
  const nsStage = $('#ns-stage');
  if (nsStage && !reduceMotion) {
    const nsIo = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (!en.isIntersecting) return;
          const r = en.intersectionRatio;
          setNs(r > 0.55 ? 1 : 0);
        });
      },
      { threshold: [0.25, 0.45, 0.55, 0.7, 0.9] },
    );
    nsIo.observe(nsStage);
  }

  /* ── Ladder ────────────────────────────────────────── */
  const hulls = (D.ladder && D.ladder.hulls) || [];
  function setHull(i) {
    const h = hulls[i];
    if (!h) return;
    document.querySelectorAll('.ladder-tab').forEach((el, j) => el.classList.toggle('active', j === i));
    const img = $('#ladder-img');
    const plate = $('#ladder-plate');
    const info = ladderImg(h);
    if (plate) plate.classList.toggle('photo', !!info.photo);
    if (img && info.src) {
      img.style.opacity = '0';
      setTimeout(() => {
        img.src = info.src;
        img.style.opacity = '1';
      }, 140);
    }
    const meta = $('#ladder-meta');
    if (meta) {
      const dev = info.dev
        ? `<div class="render-chip">RENDER — IN DEVELOPMENT</div>`
        : '';
      meta.innerHTML = `
        <div class="name">${esc(h.name)}</div>
        <div class="class">${esc(h.length_class || '')}</div>
        <div class="mission">${esc(h.mission || '')}</div>
        ${h.status_chip ? `<div class="status">${esc(h.status_chip)}</div>` : ''}
        ${dev}
        ${h.detail ? `<div class="detail">${esc(h.detail)}</div>` : ''}`;
    }
    const scale = $('#ladder-scale');
    if (scale) {
      const lengths = hulls.map((x) => parseInt(x.length_class, 10) || 30);
      const max = Math.max(...lengths, 1);
      scale.innerHTML = hulls
        .map((x, j) => {
          const len = parseInt(x.length_class, 10) || 30;
          const w = Math.max(12, Math.round((len / max) * 100));
          return `<div class="scale-row ${j === i ? 'on' : ''}"><span>${esc(x.name)}</span><i style="width:${w}%"></i></div>`;
        })
        .join('');
    }
  }
  document.querySelectorAll('.ladder-tab').forEach((el) => {
    el.addEventListener('click', () => setHull(+el.dataset.hull));
  });
  if (hulls.length) setHull(0);

  /* ── Unit econ ─────────────────────────────────────── */
  const panels = (D.unitecon && D.unitecon.panels) || [];
  const rowLabels = (D.unitecon && D.unitecon.row_labels) || [];
  function setUe(i) {
    const p = panels[i];
    if (!p) return;
    document.querySelectorAll('.ue-tab').forEach((el, j) => el.classList.toggle('active', j === i));
    const body = $('#ue-body');
    if (!body) return;
    const el = p.electric;
    const di = p.diesel;
    const rows = rowLabels
      .map(
        (lab, ri) => `
      <div class="ue-lab">${esc(lab)}</div>
      <div class="ue-el">${esc((el.values && el.values[ri]) || '')}</div>
      <div class="ue-di">${esc((di.values && di.values[ri]) || '')}</div>`,
      )
      .join('');
    body.innerHTML = `
      <div class="ue-cols">
        <div class="head">Line</div>
        <div class="head ok">${esc(el.name)}</div>
        <div class="head">${esc(di.name)}</div>
        ${rows}
      </div>
      <div class="ue-punch">${esc(p.punchline || '')}</div>
      <ul class="ue-notes">${(D.unitecon.footnotes || []).map((f) => `<li>${esc(f)}</li>`).join('')}</ul>`;
  }
  document.querySelectorAll('.ue-tab').forEach((el) => {
    el.addEventListener('click', () => setUe(+el.dataset.ue));
  });
  if (panels.length) setUe(0);

  /* ── Scroll / motion ───────────────────────────────── */
  const progress = $('#inv-progress');
  const scrollCue = $('#scroll-cue');
  const navLinks = [...document.querySelectorAll('[data-nav]')];
  const chapterIds = ((D.site.nav && D.site.nav.chapters) || []).map((c) => c.id);

  function onScroll() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    if (scrollCue && window.scrollY > 80) scrollCue.classList.add('hidden');
    // pause hero video after scroll
    const hv = document.querySelector('.hero-video');
    if (hv && window.scrollY > window.innerHeight * 0.85) {
      try {
        hv.pause();
      } catch (_) {}
    }
    let active = chapterIds[0];
    for (const id of chapterIds) {
      const el = document.getElementById(id);
      if (el && el.getBoundingClientRect().top <= 120) active = id;
    }
    navLinks.forEach((a) => a.classList.toggle('active', a.dataset.nav === active));
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const videoIo = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        const v = en.target;
        if (!(v instanceof HTMLVideoElement) || reduceMotion) return;
        if (en.isIntersecting) v.play().catch(() => {});
        else v.pause();
      });
    },
    { threshold: 0.25 },
  );
  document.querySelectorAll('video[data-lazy-video], .hero-video').forEach((v) => {
    if (!reduceMotion) videoIo.observe(v);
  });

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        if (en.target.dataset.pills != null) {
          const now = +(en.target.dataset.now || 0);
          en.target.querySelectorAll('.arc-phase').forEach((p, i) => {
            setTimeout(() => {
              p.classList.add('lit');
              if (i + 1 === now) p.classList.add('now');
            }, i * 140);
          });
        }
        if (en.target.dataset.bars != null || en.target.querySelector('[data-bar-pct]')) {
          const root = en.target.dataset.bars != null ? en.target : en.target;
          root.querySelectorAll('.bar-row').forEach((row) => {
            const pct = row.dataset.barPct || 50;
            const fill = row.querySelector('.bar-fill');
            if (fill) requestAnimationFrame(() => (fill.style.width = pct + '%'));
          });
        }
        // also bars nested
        en.target.querySelectorAll('.bar-row').forEach((row) => {
          const pct = row.dataset.barPct || 50;
          const fill = row.querySelector('.bar-fill');
          if (fill && !fill.style.width) requestAnimationFrame(() => (fill.style.width = pct + '%'));
        });
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -6% 0px' },
  );
  document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));
  // observe bar sections
  document.querySelectorAll('[data-bars]').forEach((el) => io.observe(el));

  // QA: no raw JSON braces in visible text
  try {
    const text = app.innerText || '';
    if (text.includes('{"') || text.includes('{"label"')) {
      console.warn('[invest] G3 possible JSON leak in rendered text');
    }
    console.info('[invest] v4 mount ok, homes', homes.size);
  } catch (_) {}
})();
