/* Series B /invest v6 — slide-stage doctrine · new canon plates */
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
  function formatBackers(line, backers) {
    var items = [];
    if (backers && backers.length) {
      items = backers.map(function (b) {
        return { name: b.name || b.label || '', url: b.url || b.href || '' };
      }).filter(function (b) { return b.name; });
    } else if (line) {
      items = String(line)
        .split(/[·•\n;]+/)
        .map(function (n) { return n.trim(); })
        .filter(Boolean)
        .map(function (n) { return { name: n, url: '' }; });
    }
    return items
      .map(function (b, i, arr) {
        var inner = b.url
          ? '<a class="backer-link" href="' + esc(b.url) + '" target="_blank" rel="noopener noreferrer">' + esc(b.name) + '</a>'
          : '<span>' + esc(b.name) + '</span>';
        return inner + (i < arr.length - 1 ? '<i class="sep" aria-hidden="true"></i>' : '');
      })
      .join('');
  }


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
    if (!h || h.caption == null || h.caption === '') return '';
    const c = String(h.caption);
    // Never render manifest/usage metadata as captions (v6 §C.10)
    if (/manifest|full-bleed with|treatment|opener full|only home|pending/i.test(c)) return '';
    return c;
  }

  function cinema(src, opts = {}) {
    if (!src) return '';
    const cap = opts.caption;
    // Size via CSS vars/classes — never inline vh (defeats mobile clamps)
    let sizeClass = 'cinema-media--chapter';
    if (opts.size === 'hero') sizeClass = 'cinema-media--hero';
    else if (opts.size === 'gtm') sizeClass = 'cinema-media--gtm';
    else if (opts.size === 'divider') sizeClass = 'cinema-media--divider';
    else if (opts.vh) {
      const n = parseInt(String(opts.vh), 10);
      if (n >= 68) sizeClass = 'cinema-media--hero';
      else if (n >= 54) sizeClass = 'cinema-media--gtm';
      else if (n >= 50) sizeClass = 'cinema-media--divider';
      else sizeClass = 'cinema-media--chapter';
    }
    return `
      <div class="cinema-block" data-home="${esc(opts.home || '')}" data-reveal>
        <div class="cinema">
          <div class="cinema-media ${sizeClass}">
            ${
              opts.video
                ? `<video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="none" data-lazy-video poster="${esc(opts.poster || '')}">
                     <source src="${esc(src)}" type="video/mp4" />
                   </video>`
                : `<img src="${esc(src)}" alt="${esc(opts.alt || '')}" loading="${opts.eager ? 'eager' : 'lazy'}" ${opts.eager ? 'fetchpriority="high"' : ''} />`
            }
          </div>
        </div>
        ${cap ? `<div class="media-inner"><p class="cinema-cap">${esc(cap)}</p></div>` : ''}
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

  /** One authored kicker per section — never hardcode chapter labels twice (v8 render_rules.kickers) */
  function kicker(s, fallback) {
    const t = (s && (s.kicker || s.eyebrow)) || fallback || '';
    if (!t) return '';
    return `<p class="eyebrow stage-kicker">${esc(t)}</p>`;
  }

  /** Title Case for headlines that arrive as all-caps (v8 headline_case) */
  function titleCaseHeadline(str) {
    if (!str) return '';
    const s = String(str);
    // Only rewrite if mostly uppercase
    const letters = s.replace(/[^A-Za-z]/g, '');
    if (!letters || letters !== letters.toUpperCase()) return s;
    return s
      .toLowerCase()
      .replace(/(^|[\s—–\-/:])([a-z])/g, function (_, p, c) {
        return p + c.toUpperCase();
      });
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
    // open_network_line = quiet line under the interactive (contract-locked)
    return `
      <div class="section-block network-shift ns-section" data-reveal data-home="claim.network_shift">
        <div class="section-inner">
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
        </div>
        <div class="ns-pin">
          <div class="ns-pin-sticky">
            <div id="ns-mount" class="ns-mount"></div>
          </div>
        </div>
        <div class="section-inner ns-after">
          ${s.open_network_line ? `<p class="ns-open-line">${esc(s.open_network_line)}</p>` : ''}
          ${s.closing_line ? `<p class="ns-kicker">${nl(s.closing_line)}</p>` : ''}
        </div>
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
      const nameEl = p.url
        ? `<a class="team-name team-link" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">${esc(p.name)}</a>`
        : `<div class="team-name">${esc(p.name)}</div>`;
      const photoInner = src
        ? p.url
          ? `<a class="team-photo-link" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer"><img src="${esc(src)}" alt="${esc(p.name)}" loading="lazy" /></a>`
          : `<img src="${esc(src)}" alt="${esc(p.name)}" loading="lazy" />`
        : '';
      return `
        <div class="team-card">
          <div class="team-photo">${photoInner}</div>
          ${nameEl}
          <div class="team-role">${esc(p.role)}</div>
          <div class="team-creds">${esc(p.credentials)}</div>
        </div>`;
    }

    const logoStrip = logos
      .map((l) => `<img src="${esc(mediaPath(l))}" alt="" loading="lazy" />`)
      .join('');

    const samName = sam
      ? sam.url
        ? `<a class="team-name team-link" href="${esc(sam.url)}" target="_blank" rel="noopener noreferrer">${esc(sam.name)}</a>`
        : `<div class="team-name">${esc(sam.name)}</div>`
      : '';
    const samPhoto = sam && featured
      ? sam.url
        ? `<a class="team-photo-link" href="${esc(sam.url)}" target="_blank" rel="noopener noreferrer"><img src="${esc(featured)}" alt="${esc(sam.name)}" loading="lazy" /></a>`
        : `<img src="${esc(featured)}" alt="${esc(sam.name)}" loading="lazy" />`
      : '';

    return `
      <div class="section-block team-section" data-reveal data-home="claim.team">
        ${s.title ? `<h2 class="h2 shell-prose">${esc(s.title)}</h2>` : ''}
        ${s.subhead ? `<p class="lead shell-prose team-lede">${nl(s.subhead)}</p>` : ''}
        <div class="team-layout shell-stage">
          ${
            sam
              ? `<div class="team-featured">
                  <div class="team-photo lg">${samPhoto}</div>
                  ${samName}
                  <div class="team-role">${esc(sam.role)}</div>
                  <div class="team-creds">${esc(sam.credentials)}</div>
                </div>`
              : ''
          }
          <div class="team-grid">${others.map(cardFor).join('')}</div>
        </div>
        ${logoStrip ? `<div class="logo-strip shell-stage" aria-label="Pedigree">${logoStrip}</div>` : ''}
        ${
          s.backers || s.backers_line
            ? `<div class="backers-type shell-prose"><div class="bl">${esc(s.backers_label || 'BACKED BY')}</div><div class="names">${formatBackers(s.backers_line, s.backers)}</div></div>`
            : ''
        }
      </div>`;
  }

  /* ── Section renderers ─────────────────────────────── */
  const R = {
    'text-block'(s) {
      // Legacy fallback
      return `
        <div class="section-block manifesto" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.body ? `<p class="manifesto-body">${nl(s.body)}</p>` : ''}
        </div>`;
    },

    'prose-stage'(s) {
      // Core Thesis (v9.1) — deck prose VERBATIM. Full-viewport stage; para 1 = lead weight.
      const paras = (s.paragraphs || [])
        .map(
          (p, i) =>
            `<p class="about-para ${i === 0 ? 'lead-para' : 'body-para'}" data-reveal>${esc(p)}</p>`,
        )
        .join('');
      return `
        <div class="section-block stage-section about-stage" data-reveal data-home="claim.about">
          <div class="section-inner about-stage-inner">
            ${s.kicker ? `<p class="about-kicker">${esc(s.kicker)}</p>` : ''}
            ${s.title ? `<h2 class="h2 about-title">${esc(s.title)}</h2>` : ''}
            <div class="about-prose">${paras}</div>
          </div>
        </div>`;
    },

    'thesis-strands'(s) {
      // Kept for older contracts; prefer prose-stage
      const strands = (s.strands || [])
        .map(
          (st) => `
          <div class="strand">
            <div class="strand-label">${esc(st.label || '')}</div>
            <div class="strand-body">${esc(st.body || '')}</div>
          </div>`,
        )
        .join('');
      return `
        <div class="section-block stage-section about-stage" data-reveal data-home="claim.about">
          <div class="section-inner about-stage-inner">
            ${s.title ? `<p class="stage-kicker">${esc(s.title)}</p>` : ''}
            ${s.identity ? `<p class="about-identity">${esc(s.identity)}</p>` : ''}
            ${s.thesis ? `<h2 class="about-thesis h2">${esc(s.thesis)}</h2>` : ''}
            <div class="strands-grid media-inner" style="max-width:none;padding:0">${strands}</div>
          </div>
        </div>`;
    },

    'two-panel-transition'(s) {
      return renderNetworkShift(s);
    },

    'pill-sequence'(s) {
      // Scroll-driven sequence: phases accumulate 1→6; NOW badge on phase 3
      const nowOn = s.now_marker_on != null ? +s.now_marker_on : 3;
      const pills = (s.pills || [])
        .map((p, i) => {
          const isNow = i + 1 === nowOn;
          return `
          <div class="arc-phase ${isNow ? 'is-now' : ''}" data-pill="${i}" data-step="${i + 1}">
            <div class="arc-node">
              ${isNow ? `<span class="now-badge">${esc(s.now_label || 'NOW')}</span>` : ''}
              <div class="arc-num">${esc(p.number)}</div>
            </div>
            <div class="arc-body">
              <div class="title">${esc(p.title)}</div>
              <div class="detail">${esc(p.detail)}</div>
              <div class="meta">${esc(p.program || '')} · ${esc(p.market || '')}</div>
            </div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block arc-section" data-reveal data-pills data-now="${nowOn}" data-arc-steps="${(s.pills || []).length}">
          <div class="arc-pin" id="arc-pin">
            <div class="arc-pin-sticky">
              <div class="section-inner">
                ${kicker(s, '01 · THESIS')}
                ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
              </div>
              <div class="arc-rail media-inner" id="arc-rail">${pills}</div>
            </div>
          </div>
        </div>`;
    },

    'team-grid'(s) {
      return renderTeam(s);
    },

    'flip-cards'(s) {
      // v9.4: two-tone flip title · exclusive states · ≤2-line wrap · no reflow
      const pairs = s.pairs || [];
      const parts = s.flip_headline_parts || {};
      const flipWhite = parts.white || 'Three Costs Kept Maritime Stuck.';
      const flipGold = parts.gold || 'Three Levers Collapse Them.';
      const cards = pairs
        .map((pair, i) => {
          const n = String(i + 1).padStart(2, '0');
          const title = pair.cost.title || '';
          const lead = title.split(/\s*[—–-]\s*/)[0] || title;
          const rest = title.slice(lead.length).replace(/^\s*[—–-]\s*/, '');
          return `
          <div class="flip-slot" data-i="${i}">
            <div class="flip-card" data-flip-card="${i}">
              <div class="flip-face flip-cost">
                <div class="cm-num">${n}</div>
                <div class="cm-cost-lead">${esc(lead)}</div>
                ${rest ? `<div class="cm-cost-sub">${esc(rest)}</div>` : ''}
                <div class="cm-cost-body">${esc(pair.cost.body || '')}</div>
              </div>
              <div class="flip-face flip-lever">
                <div class="cm-num">${n}</div>
                <div class="cm-lever-title">${esc(pair.lever.title || '')}</div>
                <div class="cm-lever-mech">${esc(pair.lever.mechanism || '')}</div>
                <div class="cm-lever-proof">${esc(pair.lever.proof || '')}</div>
                ${pair.lever.bridge ? `<div class="cm-lever-bridge">${esc(pair.lever.bridge)}</div>` : ''}
              </div>
            </div>
          </div>`;
        })
        .join('');
      const staticCosts = pairs
        .map((pair, i) => {
          const n = String(i + 1).padStart(2, '0');
          return `<div class="static-pair-card cost"><div class="cm-num">${n}</div><div class="t">${esc(pair.cost.title || '')}</div><div class="b">${esc(pair.cost.body || '')}</div></div>`;
        })
        .join('');
      const staticLevers = pairs
        .map((pair, i) => {
          const n = String(i + 1).padStart(2, '0');
          return `<div class="static-pair-card lever"><div class="cm-num">${n}</div><div class="t">${esc(pair.lever.title || '')}</div><div class="mech">${esc(pair.lever.mechanism || '')}</div><div class="b">${esc(pair.lever.proof || '')}</div>${pair.lever.bridge ? `<div class="cm-lever-bridge">${esc(pair.lever.bridge)}</div>` : ''}</div>`;
        })
        .join('');
      // State A = costs headline + $1T subhead + kicker
      // State B = two-tone flip title + closing line in the reserved subhead slot (exclusive)
      // Spacer (state A, invisible) keeps width+height in normal flow — no reflow, no width collapse
      const stateA = `
                ${s.headline ? `<h2 class="h2 costs-title" data-fit-title>${esc(s.headline)}</h2>` : ''}
                ${s.subhead ? `<p class="lead costs-subhead">${esc(s.subhead)}</p>` : ''}
                ${s.costs_kicker ? `<p class="cm-kicker">${esc(s.costs_kicker)}</p>` : ''}`;
      const stateB = `
                <h2 class="h2 costs-title costs-flip-title" data-fit-title>
                  <span class="flip-title-white">${esc(flipWhite)}</span>
                  <span class="flip-title-gold">${esc(flipGold)}</span>
                </h2>
                ${s.closing_line ? `<p class="costs-flip-closing">${esc(s.closing_line)}</p>` : ''}`;
      return `
        <div class="section-block costs-morph-section" data-reveal data-home="claim.three_costs">
          <div class="section-inner costs-compose">
            <div class="costs-head costs-head-fixed" id="costs-head">
              <div class="costs-head-spacer" aria-hidden="true">${stateA}</div>
              <div class="costs-head-layer is-cost is-visible" data-head="cost">${stateA}</div>
              <div class="costs-head-layer is-lever" data-head="lever" aria-hidden="true">${stateB}</div>
            </div>
            <div class="costs-morph" id="costs-morph">
              <div class="flip-grid" id="flip-grid">${cards}</div>
              <div class="flip-static" hidden>
                <p class="eyebrow">THREE COSTS</p>
                <div class="static-row">${staticCosts}</div>
                <p class="eyebrow" style="margin-top:28px">THREE LEVERS</p>
                <div class="static-row">${staticLevers}</div>
                <h2 class="h2 costs-flip-title" style="margin-top:20px">
                  <span class="flip-title-white">${esc(flipWhite)}</span>
                  <span class="flip-title-gold">${esc(flipGold)}</span>
                </h2>
                ${s.closing_line ? `<p class="costs-flip-closing">${esc(s.closing_line)}</p>` : ''}
              </div>
            </div>
            <div class="costs-after" id="costs-after" hidden>
              ${
                s.why_now
                  ? `<div class="why-now why-now-stage costs-why-now">
                <h3 class="h3">${esc(s.why_now.title)}</h3>
                <p class="why-now-body">${nl(s.why_now.body || s.why_now.line || '')}</p>
              </div>`
                  : ''
              }
            </div>
          </div>
        </div>`;
    },

    'stat-counters'(s) {
      // v9 #3: Pioneer hero video (poster fallback until mp4 lands)
      const hv = s.hero_video || {};
      const poster = mediaPath(hv.poster_asset || 'assets/deck/n30-pioneer-at-sea.png');
      const vsrc = hv.asset ? mediaPath(hv.asset) : '';
      return `
        <div class="section-block shell-stage pioneer-hero-section" data-reveal data-home="proof.n30.hero">
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          <div class="pioneer-hero">
            <video class="pioneer-hero-video" muted playsinline loop preload="metadata"
              poster="${esc(poster)}" ${reduceMotion ? '' : 'autoplay'} data-lazy-video>
              ${vsrc ? `<source src="${esc(vsrc)}" type="video/mp4" />` : ''}
            </video>
            <img class="pioneer-hero-fallback" src="${esc(poster)}" alt="" loading="lazy" />
          </div>
          ${goldStats(s.stats)}
        </div>`;
    },

    'video-grid'(s) {
      // Equal-weight 2/3-col grid; prefer self-hosted mp4 loops when asset is present
      const demos = homeAssets('proof.demo_grid') || {};
      const idMap = {
        'no-wake': 'no_wake',
        'flat-turning': 'flat_turn',
        'rough-seas': 'rough_seas',
        takeoff: 'foiling_18s',
        stabilization: 'anchor',
      };
      const clips = s.clips || [];
      const cards = clips
        .map((c) => {
          const key = idMap[c.id] || c.id;
          const poster = demos[key]
            ? mediaPath(demos[key])
            : c.poster
              ? mediaPath(c.poster)
              : c.youtube_id
                ? `https://i.ytimg.com/vi/${c.youtube_id}/hqdefault.jpg`
                : c.asset
                  ? mediaPath('assets/deck/n30-pioneer-at-sea.png')
                  : '';
          const sub = c.subcaption || '';
          // Self-hosted asset wins (YouTube kept as provenance only)
          if (c.asset) {
            return `
            <div class="vcard vcard-loop" data-loop-src="${esc(mediaPath(c.asset))}" data-clip="${esc(c.id || '')}">
              <span class="vcard-media">
                <video muted playsinline loop preload="metadata" poster="${esc(poster)}" data-lazy-video>
                  <source src="${esc(mediaPath(c.asset))}" type="video/mp4" />
                </video>
                <span class="play"><span>▶</span></span>
                ${c.duration ? `<span class="dur">${esc(c.duration)}</span>` : ''}
              </span>
              <span class="vcard-cap">${esc(c.caption || c.title || '')}</span>
              ${sub ? `<span class="vcard-sub">${esc(sub)}</span>` : ''}
            </div>`;
          }
          return `
          <button type="button" class="vcard"
            data-yt="${esc(c.youtube_id || '')}" data-embed="${esc(c.embed_url || '')}">
            <span class="vcard-media">
              <img src="${esc(poster)}" alt="" loading="lazy" />
              <span class="play"><span>▶</span></span>
              ${c.duration ? `<span class="dur">${esc(c.duration)}</span>` : ''}
            </span>
            <span class="vcard-cap">${esc(c.caption || c.title || '')}</span>
            ${sub ? `<span class="vcard-sub">${esc(sub)}</span>` : ''}
          </button>`;
        })
        .join('');

      return `
        <div class="section-block" data-reveal data-home="proof.demo_grid">
          <div class="section-inner">
            ${kicker(s)}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.lede ? `<p class="demo-lede">${esc(s.lede)}</p>` : ''}
          </div>
          <div class="video-grid equal-grid media-inner">${cards}</div>
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
          <div class="section-inner">
            ${kicker(s)}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${sticky ? `<div class="sticky-chips">${sticky}</div>` : ''}
          </div>
          ${plate ? cinema(plate, { home: 'proof.traction.plate', vh: '50vh' }) : ''}
          <div class="timeline media-inner">${items}</div>
          ${s.closing_line ? `<p class="closing-line section-inner">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'hotspot-diagram'(s) {
      // Pre-labeled schematic plate (no HTML callouts/leaders — labels are baked into the PNG)
      const filmPoster = homeSrc('product.control.film') || mediaPath('assets/posters/S7WB91FvSFI.jpg');
      const schem = s.schematic || {};
      const wire = mediaPath(
        schem.asset || homeSrc('product.control.diagram') || 'assets/deck/schematic-controls.png',
      );
      const altBits = (schem.callouts || [])
        .map(function (h) {
          return h.label + (h.detail ? ' — ' + h.detail : '');
        })
        .filter(Boolean);
      const alt =
        'Navier control schematic showing ' +
        (altBits.length ? altBits.join('; ') : 'sensors, NavierOS, foils, hull, and powertrain');
      return `
        <div class="section-block stage-section control-stage" data-reveal data-home="product.control.diagram">
          <div class="section-inner">
            ${kicker(s)}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.body ? `<p class="lead">${nl(s.body)}</p>` : ''}
          </div>
          <div class="control-sbs media-inner">
            <div class="control-diagram control-diagram-plate" id="control-diagram">
              ${
                wire
                  ? `<img class="control-wire control-plate-img" src="${esc(wire)}" alt="${esc(alt)}" loading="eager" fetchpriority="high" />`
                  : ''
              }
            </div>
            <div class="control-video">
              ${s.video ? filmCard(s.video, filmPoster, 'product.control.film', s.video_label || '') : ''}
            </div>
          </div>
        </div>`;
    },

    'platform-intro'(s) {
      // v8 #5–6: connected 3-layer diagram + wireframe; NO foundry/hangar here
      const wire = homeSrc('product.gmvp.diagram') || mediaPath('assets/deck/fleet-wireframe.png');
      const layers = (s.layers || [])
        .map((l, i) => {
          const parts = String(l.name || '').split(/\s*\|\s*/);
          const name = parts[0] || l.name || '';
          const role = parts[1] || '';
          return `
          <div class="gmvp-layer" data-layer="${i}">
            <div class="gmvp-layer-name">${esc(name)}</div>
            ${role ? `<div class="gmvp-layer-role">${esc(role)}</div>` : ''}
            ${l.detail ? `<div class="gmvp-layer-detail">${esc(l.detail)}</div>` : ''}
          </div>`;
        })
        .join('');
      return `
        <div class="section-block shell-stage gmvp-stage" data-reveal data-home="product.gmvp.diagram">
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.body ? `<p class="lead">${nl(s.body)}</p>` : ''}
          <div class="gmvp-compose">
            <div class="gmvp-wire">
              ${wire ? `<img src="${esc(wire)}" alt="" loading="lazy" class="gmvp-wire-img" />` : ''}
            </div>
            <div class="gmvp-layers">
              <p class="eyebrow">THREE LAYERS</p>
              ${layers}
            </div>
          </div>
        </div>`;
    },

    interactive(s) {
      if (s.component === 'vessel-ladder-explorer' || s.data === 'ladder.json') return renderLadder(s);
      if (s.component === 'unit-econ-toggle' || s.data === 'unitecon.json') return renderUnitEcon(s);
      if (s.component === 'pipeline-map' || s.data === 'pipeline-map.json') return renderPipeline(s);
      return '';
    },

    'chapter-break'(s) {
      // v8 #7: ONE title moment — Title Case headline, founder video FIRST ≥70% width, no camo here
      const qa = homeAssets('product.quanta') || {};
      const filmP = qa.film ? mediaPath(qa.film) : mediaPath('assets/posters/QhiaYVgXMf0.jpg');
      const headline = titleCaseHeadline(s.headline || '');
      return `
        <div class="section-block chapter-break quanta-moment" data-reveal data-home="product.quanta">
          <div class="section-inner">
            ${kicker(s)}
            ${headline ? `<h2 class="h2 quanta-headline">${esc(headline)}</h2>` : ''}
            <div class="quanta-video-lead">
              ${s.video ? filmCard(s.video, filmP, 'product.quanta', s.video_label || 'Sampriti Bhattacharyya · CEO Navier') : ''}
            </div>
          </div>
        </div>`;
    },

    'stat-chips'(s) {
      // v9 #8: image ≥60% width, chips ≥260px, minimal dead air
      const qa = homeAssets('product.quanta') || {};
      const camo = qa.defense_plate ? mediaPath(qa.defense_plate) : '';
      return `
        <div class="section-block shell-stage quanta-stats-stage" data-reveal data-home="product.quanta">
          ${kicker(s)}
          <div class="quanta-stats-compose ${camo ? 'has-plate' : ''}">
            ${camo ? `<div class="quanta-stats-plate"><img src="${esc(camo)}" alt="" loading="lazy" /></div>` : ''}
            <div class="quanta-stats-copy">
              ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
              ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
              ${goldStats(s.stats)}
            </div>
          </div>
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
          ${kicker(s)}
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
      // v9 #9: full S17 10-row table + vessel-type band + takeaway/explainer/source
      const cols = s.columns || [];
      // New shape: columns may be string[], rows may be string[][]
      const colNames = cols.map(function (c) {
        return typeof c === 'string' ? c : c.name || '';
      });
      const useRows = Array.isArray(s.rows) && s.rows.length;
      const head = `<tr>${colNames
        .map(function (name, i) {
          const hi = /navier|quanta/i.test(name);
          return `<th class="${hi ? 'hi' : ''}${i === 0 ? ' row-label-th' : ''}">${esc(name || (s.vessel_type_label || ''))}</th>`;
        })
        .join('')}</tr>`;
      let body = '';
      if (s.vessel_type_row && s.vessel_type_row.length) {
        body += `<tr class="vessel-type-row">${s.vessel_type_row
          .map(function (cell, i) {
            const hi = i === 1;
            return `<td class="${hi ? 'hi' : ''}${i === 0 ? ' row-label' : ''}">${esc(cell)}</td>`;
          })
          .join('')}</tr>`;
      }
      if (useRows) {
        body += s.rows
          .map(function (row) {
            return `<tr>${(row || [])
              .map(function (cell, i) {
                const hi = i === 1;
                return `<td class="${hi ? 'hi' : ''}${i === 0 ? ' row-label' : ''}">${esc(cell)}</td>`;
              })
              .join('')}</tr>`;
          })
          .join('');
      } else {
        // Legacy object-columns shape
        const labels = s.row_labels || [];
        const objCols = cols.filter(function (c) {
          return typeof c === 'object';
        });
        body += labels
          .map(function (lab, ri) {
            const cells = objCols
              .map(function (c) {
                return `<td class="${c.highlight ? 'hi' : ''}">${esc((c.values && c.values[ri]) || '')}</td>`;
              })
              .join('');
            return `<tr><td class="row-label">${esc(lab)}</td>${cells}</tr>`;
          })
          .join('');
      }
      const takeaway = s.takeaway || s.closing_line || '';
      return `
        <div class="section-block shell-stage" data-reveal data-home="gtm.competitive">
          ${kicker(s)}
          ${s.headline || s.title ? `<h2 class="h2">${esc(s.headline || s.title)}</h2>` : ''}
          <div class="table-wrap"><table class="cmp cmp-s17"><thead>${head}</thead><tbody>${body}</tbody></table></div>
          ${takeaway ? `<p class="closing-line takeaway-line">${esc(takeaway)}</p>` : ''}
          ${s.explainer ? `<p class="explainer">${esc(s.explainer)}</p>` : ''}
          ${s.source_note ? `<p class="muted source-note">${esc(s.source_note)}</p>` : ''}
        </div>`;
    },

    'signed-contract-hero'(s) {
      // Players with roles/activities + linked press quotes
      const ga = homeAssets('gtm.maldives') || {};
      const logos = homeAssets('gtm.coastal.logos') || {};
      const hero = ga.opener ? mediaPath(ga.opener) : '';
      const players = s.players || [];
      const playersBlock = players.length
        ? `<div class="maldives-players">
            ${s.players_label ? `<p class="eyebrow">${esc(s.players_label)}</p>` : ''}
            <div class="player-logos maldives-logos cols-${Math.min(players.length, 4)}">${players
              .map(function (pl) {
                const key = pl.id || '';
                const src = logos[key] ? mediaPath(logos[key]) : '';
                return `<div class="player-logo player-card">
                  ${src ? `<img src="${esc(src)}" alt="${esc(pl.name || '')}" loading="lazy" />` : ''}
                  <div class="title">${esc(pl.name || '')}</div>
                  ${pl.role ? `<div class="player-role">${esc(pl.role)}</div>` : ''}
                  ${pl.does ? `<div class="player-does">${esc(pl.does)}</div>` : ''}
                </div>`;
              })
              .join('')}</div>
          </div>`
        : '';
      const pressItems = (s.press || [])
        .map(function (p) {
          const body = `<div class="outlet">${esc(p.outlet)}</div><div class="quote">${esc(p.quote)}</div>`;
          if (p.url) {
            return `<a class="press-item press-link" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">${body}</a>`;
          }
          return `<div class="press-item">${body}</div>`;
        })
        .join('');
      return `
        <div class="section-block stage-section gtm-hero-section" data-reveal data-home="gtm.maldives">
          ${hero ? cinema(hero, { home: 'gtm.maldives', size: 'gtm' }) : ''}
          <div class="section-inner gtm-hero-copy">
            ${kicker(s)}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            ${goldStats(s.stats)}
            ${playersBlock}
            <div class="press-block">
              ${s.press_label ? `<p class="eyebrow">${esc(s.press_label)}</p>` : ''}
              <div class="press">${pressItems}</div>
            </div>
          </div>
        </div>`;
    },

    'program-panel'(s) {
      const gulf = homeSrc('gtm.gulf.plate') || mediaPath('assets/deck/gulf-hero.png');
      return `
        <div class="section-block stage-section gtm-hero-section" data-reveal data-home="gtm.gulf.plate">
          ${gulf ? cinema(gulf, { home: 'gtm.gulf.plate', size: 'gtm' }) : ''}
          <div class="section-inner gtm-hero-copy">
            ${kicker(s)}
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
          </div>
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
        <div class="section-block shell-stage revenue-lines-stage" data-reveal>
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          ${s.flywheel_line ? `<p class="flywheel-line">${esc(s.flywheel_line)}</p>` : ''}
          <div class="stack-cards">${cards}</div>
          ${s.formula_line ? `<div class="formula">${esc(s.formula_line)}</div>` : ''}
        </div>`;
    },

    'four-role-diagram'(s) {
      // v9 #10: logos moved to Maldives — keep model roles as text cards only
      const roles = s.roles || s.cards || [];
      const roleCards = roles
        .map(function (r) {
          const title = r.title || r.name || r.role || '';
          const does = r.does || r.body || r.detail || '';
          return `<div class="role-card">
            <div class="title">${esc(title)}</div>
            <div class="role">${esc(does)}</div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block stage-section" data-reveal>
          <div class="section-inner">
            ${kicker(s)}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead || s.intro ? `<p class="lead">${esc(s.subhead || s.intro)}</p>` : ''}
            <div class="role-cards">${roleCards}</div>
            ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
          </div>
        </div>`;
    },

    'drawing-chart'(s) {
      // v8 #9: cargo gap only — play/shipscale/wedge are their own composed sections
      const ca = homeAssets('gtm.cargo') || {};
      const opener = ca.opener ? mediaPath(ca.opener) : mediaPath('assets/deck/air-vs-ocean-cargo.png');
      // Keep "$0.25" and "/kg" on one tight line (never a disconnected wrap)
      const priceHtml = function (price) {
        const m = String(price || '').match(/^(.*?)(\s*\/\s*kg)\s*$/i);
        if (m) {
          return `<span class="chip-amt">${esc(m[1].trim())}</span><span class="chip-unit">/kg</span>`;
        }
        return esc(price);
      };
      let chartCards = '';
      if (s.chart) {
        const c = s.chart;
        chartCards = ['air', 'ocean', 'gap']
          .filter((k) => c[k])
          .map((k) => {
            const x = c[k];
            return `<div class="chip-card">
              <div class="t">${esc(x.label || k)}</div>
              ${x.price ? `<div class="chip-num">${priceHtml(x.price)}</div>` : ''}
              ${x.value ? `<div class="chip-num ok">${esc(x.value)}</div>` : ''}
              <div class="b">${esc(x.time || x.detail || x.line || '')}</div>
            </div>`;
          })
          .join('');
      }
      const ib = s.island_band;
      const islandHtml =
        ib && typeof ib === 'object'
          ? `
          <div class="island-band" data-reveal>
            <p class="sublabel">ISLANDS</p>
            ${ib.title ? `<h3 class="h3">${esc(ib.title)}</h3>` : ''}
            <div class="gold-stat-band cols-${Math.min((ib.stats || []).length, 3)}">
              ${(ib.stats || [])
                .map(
                  (st) => `
                <div class="gold-stat">
                  <div class="value">${esc(st.value)}</div>
                  <div class="label">${esc(st.label)}</div>
                </div>`,
                )
                .join('')}
            </div>
            ${ib.footnote ? `<p class="muted">${esc(ib.footnote)}</p>` : ''}
          </div>`
          : '';
      return `
        <div class="section-block cargo-compose" data-reveal data-home="gtm.cargo">
          <div class="section-inner">
            ${kicker(s)}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            <div class="cargo-stage">
              <div class="cargo-stage-media contain-media">
                <img src="${esc(opener)}" alt="" loading="lazy" />
              </div>
              <div class="cargo-stage-copy">
                ${chartCards ? `<div class="chips-3">${chartCards}</div>` : ''}
                ${s.chart && s.chart.navier_band ? `<div class="formula">${esc(s.chart.navier_band)}</div>` : ''}
              </div>
            </div>
            ${islandHtml}
          </div>
        </div>`;
    },

    'three-chips'(s) {
      // Cargo play — image composed with copy (v8 #9)
      const ca = homeAssets('gtm.cargo') || {};
      const img = mediaPath(ca.play || 'assets/deck/cargo-play-skyline.png');
      const chips = (s.chips || s.cards || [])
        .map(
          (c) => `
        <div class="chip-card"><div class="t">${esc(c.title || c.label)}</div><div class="b">${esc(c.body || c.detail || '')}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block cargo-compose" data-reveal data-home="gtm.cargo">
          <div class="section-inner">
            ${kicker(s)}
            <p class="sublabel">THE PLAY</p>
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.intro || s.subhead ? `<p class="lead">${esc(s.intro || s.subhead)}</p>` : ''}
            <div class="cargo-stage">
              <div class="cargo-stage-media"><img src="${esc(img)}" alt="" loading="lazy" /></div>
              <div class="cargo-stage-copy"><div class="chips-3">${chips}</div></div>
            </div>
          </div>
        </div>`;
    },

    'stat-panel'(s) {
      const ca = homeAssets('gtm.cargo') || {};
      const img = mediaPath(ca.shipscale || 'assets/deck/shipscale-hero.png');
      const grid = mediaPath(ca.shipscale_grid || 'assets/deck/shipscale-variants-grid.png');
      const isShipScale = /ship scale|sealift/i.test((s.title || '') + (s.id || '') + (s.kicker || ''));
      const kpiStack = (s.stats || [])
        .map(function (st) {
          return `<div class="shipscale-kpi">
            <div class="value">${esc(st.value)}</div>
            <div class="label">${esc(st.label)}</div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block cargo-compose" data-reveal data-home="gtm.cargo">
          <div class="section-inner">
            ${kicker(s)}
            ${isShipScale ? `<p class="sublabel">SHIP SCALE</p>` : ''}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.intro || s.subhead ? `<p class="lead">${esc(s.intro || s.subhead)}</p>` : ''}
            ${
              isShipScale
                ? `<div class="shipscale-layout">
              <div class="shipscale-images">
                <div class="shipscale-col shipscale-hero">
                  <img src="${esc(img)}" alt="Ship-scale sealift landing craft" loading="lazy" />
                </div>
                <div class="shipscale-col shipscale-grid">
                  <img src="${esc(grid)}" alt="Ship-scale variants" loading="lazy" />
                </div>
              </div>
              <div class="shipscale-kpis">${kpiStack}</div>
            </div>`
                : goldStats(s.stats)
            }
            ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
          </div>
        </div>`;
    },

    'day-night-flip'(s) {
      const ca = homeAssets('gtm.cargo') || {};
      const img = mediaPath(ca.wedge || 'assets/deck/wedge-day-night.png');
      const chips = (s.chips || [])
        .map(
          (c) => `
        <div class="chip-card"><div class="t">${esc(c.title || c.label)}</div><div class="b">${esc(c.body || c.detail || '')}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block cargo-compose" data-reveal data-home="gtm.cargo">
          <div class="section-inner">
            ${kicker(s)}
            <p class="sublabel">THE WEDGE</p>
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
            <div class="cargo-stage">
              <div class="cargo-stage-media"><img src="${esc(img)}" alt="" loading="lazy" /></div>
              <div class="cargo-stage-copy"><div class="chips-3">${chips}</div></div>
            </div>
          </div>
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
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro || s.subhead ? `<p class="lead">${esc(s.intro || s.subhead)}</p>` : ''}
          <div class="media-duo">
            <div class="card-row">${cards}</div>
            ${ctv ? plate(ctv, { home: 'gtm.service.plate', className: '' }) : ''}
          </div>
        </div>`;
    },

    'defense-panel'(s) {
      // v8 #11: camo + Navy 50/50 side by side
      const da = homeAssets('gtm.defense') || {};
      const plateSrc = da.plate ? mediaPath(da.plate) : '';
      const inset = da.inset ? mediaPath(da.inset) : '';
      const quote = s.pull_quote
        ? `<blockquote class="defense-quote-inline">
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
        <div class="section-block dual-use-stage" data-reveal data-home="gtm.defense">
          <div class="section-inner">
            ${kicker(s)}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            ${s.intro ? `<p class="dual-use-intro">${esc(s.intro)}</p>` : ''}
            ${s.sub_line ? `<p class="dual-use-sub">${esc(s.sub_line)}</p>` : ''}
            <div class="defense-sbs">
              ${inset ? `<div class="defense-sbs-img"><img src="${esc(inset)}" alt="" loading="lazy" /></div>` : ''}
              ${plateSrc ? `<div class="defense-sbs-img"><img src="${esc(plateSrc)}" alt="" loading="lazy" /></div>` : ''}
            </div>
            ${quote}
            <div class="dual-use-blocks">${blocks}</div>
            ${s.deployment_line ? `<p class="closing-line">${esc(s.deployment_line)}</p>` : ''}
            ${s.fine_print ? `<p class="muted">${esc(s.fine_print)}</p>` : ''}
          </div>
        </div>`;
    },

    'horizontal-bars'(s) {
      // v8 #12: explicit column labels
      const segs = s.segments || [];
      const cl = s.column_labels || {};
      const max = Math.max(...segs.map((b) => (b.bar_value_range && b.bar_value_range[1]) || 1), 1);
      const header = `
        <div class="tam-head">
          <span class="tam-h-name"></span>
          <span>${esc(cl.demand_pool || 'DEMAND POOL')}</span>
          <span>${esc(cl.vessels_floor || 'VESSELS · 10-YR FLOOR')}</span>
          <span>${esc(cl.dollars_floor || 'HULL $ · 10-YR FLOOR')}</span>
        </div>`;
      const bars = segs
        .map((b) => {
          const hi = (b.bar_value_range && b.bar_value_range[1]) || 1;
          const pct = Math.round((hi / max) * 100);
          return `
          <div class="bar-row tam-row" data-bar-pct="${pct}">
            <div class="tam-grid">
              <div class="tam-name"><strong>${esc(b.name || b.label || '')}</strong></div>
              <div class="tam-demand muted tiny">${esc(b.demand_pool || '')}</div>
              <div class="tam-vessels">${esc(b.vessels_floor || '')}</div>
              <div class="tam-dollars">${esc(b.dollars_floor || b.value || '')}</div>
            </div>
            <div class="bar-track"><div class="bar-fill"></div></div>
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
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="chart-block tam-chart">${header}${bars}</div>
          ${floor}
          ${s.source_line ? `<p class="muted">${esc(s.source_line)}</p>` : ''}
        </div>`;
    },

    'native-line-charts'(s) {
      // Charts only — section title “The Ramp…” renders on the KPI strip above
      const charts = (s.charts || [])
        .map(function (ch) {
          return `
          <div class="native-chart ramp-chart" data-reveal data-ramp="${esc(ch.id || '')}">
            <p class="chart-title">${esc(ch.title || '')}</p>
            <div class="ramp-svg-host" data-chart-id="${esc(ch.id || '')}"></div>
            <div class="ramp-legend" data-legend="${esc(ch.id || '')}"></div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block shell-stage money-ramp-charts" data-reveal data-home="money.charts" data-ramp-root>
          <div class="native-charts ramp-charts">${charts}</div>
          ${s.note ? `<p class="muted">${esc(s.note)}</p>` : ''}
        </div>`;
    },

    'stat-band'(s) {
      // Money opener: eyebrow → title → subhead → KPIs (title above the strip)
      return `
        <div class="section-block shell-stage money-opener" data-reveal data-home="money.charts">
          ${kicker(s)}
          ${s.title ? `<h2 class="h2 money-ramp-title">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
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
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="roadmap">${cols}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'status-rows'(s) {
      // v8 #15: expand-on-hover/focus
      const thumbs = (home('money.thesis_board.thumbs') && home('money.thesis_board.thumbs').assets) || [];
      const rows = (s.rows || [])
        .map((r, i) => {
          const thumb = thumbs[i] ? mediaPath(thumbs[i]) : '';
          return `
          <div class="thesis-row" tabindex="0" role="button" aria-expanded="false">
            ${thumb ? `<div class="thesis-thumb"><img src="${esc(thumb)}" alt="" loading="lazy" /></div>` : ''}
            <div class="label">${esc(r.label)}</div>
            <div class="status">${esc(r.status)}</div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal data-home="money.thesis_board.thumbs">
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          <div class="thesis-board">${rows}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'two-column-round'(s) {
      // v9 P3: Title Case headings + timing eyebrows (NOW / 18–24 MONTHS)
      const cols = (s.columns || [])
        .map(function (c) {
          const raw = c.title || '';
          let eyebrow = '';
          let heading = raw;
          if (/NOW/i.test(raw)) {
            eyebrow = 'NOW';
            heading = raw.replace(/\s*[—–-]\s*NOW/i, '').replace(/NOW\s*[—–-]?\s*/i, '');
          } else if (/18\s*[–-]?\s*24/i.test(raw)) {
            eyebrow = '18–24 MONTHS';
            heading = raw.replace(/SERIES B PROGRAM\s*\([^)]+\)/i, 'Series B Program');
          }
          heading = titleCaseHeadline(heading.replace(/\$10M SERIES B-1/i, '$10M Series B-1'));
          return `
        <div class="round-col">
          ${eyebrow ? `<p class="eyebrow">${esc(eyebrow)}</p>` : ''}
          <h3>${esc(heading || raw)}</h3>
          <ul>${(c.items || []).map((it) => `<li>${esc(it)}</li>`).join('')}</ul>
        </div>`;
        })
        .join('');
      return `
        <div class="section-block shell-stage" data-reveal>
          ${kicker(s)}
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
    if (!hull) return { src: '', photo: false, dev: false, id: '' };
    const la = homeAssets('product.ladder') || {};
    const id = hull.id || '';
    // 4-tab ladder: n30 (Pioneer & Quanta merged) · n45 · n80 approved render · n180
    if (id === 'n30' || id === 'n30-pioneer' || id === 'quanta-lr') {
      const src = la.n30_pioneer || la.quanta_lr || 'assets/deck/n30-pioneer-at-sea.png';
      return { src: mediaPath(src), photo: true, dev: false, id: id };
    }
    if (id === 'n45-explorer') {
      // C4: RENDER chip on every render-image tab
      const src = la.n45_explorer || 'assets/deck/n45-mobility-render.png';
      return { src: mediaPath(src), photo: true, dev: true, id: id };
    }
    if (id === 'n80-valkyrie') {
      const src = la.n80_valkyrie || 'assets/deck/n80-render-v1.png';
      return { src: mediaPath(src), photo: true, dev: true, id: id };
    }
    if (id === 'n180-morpheus') {
      const src = la.n180_morpheus || 'assets/deck/shipscale-hero.png';
      return { src: mediaPath(src), photo: true, dev: true, id: id };
    }
    const key = String(id).replace(/-/g, '_');
    if (la[key]) return { src: mediaPath(la[key]), photo: true, dev: false, id: id };
    return { src: '', photo: false, dev: false, id: id };
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
    // v8 #6: tagline becomes ladder lead-in
    const gmvp = ((D.product && D.product.sections) || []).find((x) => x.id === 'gmvp');
    const leadIn = (gmvp && gmvp.tagline) || 'Single Platform. Multiple Use Cases.';
    return `
      <div class="section-block shell-stage" data-reveal data-home="product.ladder">
        ${kicker(s)}
        <p class="ladder-leadin">${esc(leadIn)}</p>
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

  function renderUnitEcon(s) {
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
        ${kicker(s || u)}
        ${u.eyebrow && !(s && (s.kicker || s.eyebrow)) ? `<p class="eyebrow">${esc(u.eyebrow)}</p>` : ''}
        ${u.title ? `<h2 class="h2">${esc(u.title)}</h2>` : ''}
        <div class="unitecon" id="unitecon">
          <div class="ue-tabs">${tabs}</div>
          <div class="ue-body" id="ue-body"></div>
        </div>
      </div>`;
  }

  function pipeNodeFor(party, status) {
    // Map anonymized pipeline rows → public geographic anchors (no partner resolution)
    const s = String(party || '');
    const st = String(status || '');
    const signed = /SIGNED/i.test(st);
    const advanced = /ADVANCED|CLOSING/i.test(st);
    const weight = signed ? 'signed' : advanced ? 'advanced' : /defense|navy|police|prime/i.test(s + st) ? 'defense' : 'pipeline';
    // Prefer Atlas city ids when present; else public geo fallbacks only for named places in the row
    if (/maldives/i.test(s)) return { ids: ['maldives'], coords: [[73.509, 4.175]], label: 'Maldives', weight };
    if (/gulf nation/i.test(s)) return { ids: ['sharjah-uae', 'ras-al-khaimah-uae', 'fujairah-uae', 'neom-sindalah-ksa'], coords: [[55.38, 25.36]], label: 'Gulf', weight };
    if (/turkish/i.test(s)) return { ids: ['antalya-turkey', 'bodrum-turkey', 'cesme-izmir-turkey'], coords: [[28.98, 41.01]], label: 'Türkiye', weight };
    if (/gulf super-app/i.test(s)) return { ids: ['sharjah-uae', 'manama-bahrain'], coords: [[55.27, 25.2]], label: 'Gulf', weight };
    if (/korean/i.test(s)) return { ids: ['seoul-incheon-korea', 'busan-geoje-korea'], coords: [[126.98, 37.56]], label: 'Korea', weight };
    if (/u\.?s\.?\s*public ferry/i.test(s)) return { ids: ['boston-new-england-usa', 'new-york-harbor-usa', 'tampa-bay-sarasota-florida-usa'], coords: [[-71.05, 42.36]], label: 'U.S. coasts', weight };
    if (/u\.?s\.?\s*navy/i.test(s)) return { ids: ['new-york-harbor-usa', 'boston-new-england-usa'], coords: [[-74.0, 40.7]], label: 'U.S. Navy', weight };
    if (/u\.?s\.?\s*defense/i.test(s)) return { ids: ['new-york-harbor-usa', 'boston-new-england-usa'], coords: [[-77.04, 38.91]], label: 'U.S. defense', weight };
    if (/gulf defense/i.test(s)) return { ids: ['al-wakrah-qatar', 'sharjah-uae', 'neom-sindalah-ksa'], coords: [[51.53, 25.3]], label: 'Gulf defense', weight };
    if (/gulf police/i.test(s)) return { ids: ['manama-bahrain', 'sharjah-uae'], coords: [[50.59, 26.23]], label: 'Gulf police', weight };
    if (/coastal & archipelago/i.test(s)) return { ids: ['ha-long-bay-vietnam', 'palawan-philippines', 'phu-quoc-vietnam'], coords: [[103.85, 1.29]], label: 'Archipelagos', weight };
    if (/global ridehail/i.test(s)) return { ids: ['seoul-incheon-korea', 'new-york-harbor-usa', 'manama-bahrain'], coords: [[103.85, 1.29]], label: 'Ridehail markets', weight };
    return { ids: [], coords: [], label: '', weight: 'pipeline' };
  }

  function renderPipeline(sec) {
    const p = D['pipeline-map'];
    if (!p) return '';
    const homePipe = home('gtm.pipeline.map') || {};
    const fallbackSrc = mediaPath(homePipe.fallback || homePipe.asset || 'assets/deck/world-pipeline-map.png');
    const stats = goldStats(p.gold_stats || []);
    let rowIdx = 0;
    const tiers = (p.tiers || [])
      .map((t) => {
        const rows = (t.rows || [])
          .map((r) => {
            const i = rowIdx++;
            const node = pipeNodeFor(r.party, r.status);
            const weight = node.weight;
            return `
          <button type="button" class="pipe-row weight-${esc(weight)}" data-pipe-row="${i}" data-weight="${esc(weight)}" data-coords="${esc(JSON.stringify(node.coords))}" data-ids="${esc((node.ids || []).join(','))}">
            <span class="party">${esc(r.party)}</span>
            <span class="status">${esc(r.status)}</span>
          </button>`;
          })
          .join('');
        return `<div class="pipe-tier"><h3>${esc(t.name)}</h3>${rows}</div>`;
      })
      .join('');
    return `
      <div class="section-block" data-reveal data-home="gtm.pipeline.map" id="pipeline-section">
        <div class="section-inner">
          ${kicker(sec || p)}
          ${!(sec && (sec.kicker || sec.eyebrow)) && p.eyebrow ? `<p class="eyebrow">${esc(p.eyebrow)}</p>` : ''}
          ${p.title ? `<h2 class="h2">${esc(p.title)}</h2>` : ''}
          ${stats}
        </div>
        <div class="pipe-layout media-inner">
          <div class="pipe-map-host" id="pipe-map-host">
            <div id="pipe-map" class="pipe-map" role="img" aria-label="Live pipeline map"></div>
            <noscript>
              ${fallbackSrc ? `<img src="${esc(fallbackSrc)}" alt="" class="pipe-fallback-img" />` : ''}
            </noscript>
            <div class="pipe-map-fallback" id="pipe-map-fallback" hidden>
              ${fallbackSrc ? `<img src="${esc(fallbackSrc)}" alt="" loading="lazy" />` : ''}
            </div>
          </div>
          <div class="pipe-tiers">${tiers}</div>
        </div>
        <div class="pipe-foot section-inner">
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
        <div class="section-inner"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
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
        <div class="section-inner"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
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
        <div class="section-inner"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
        ${parts.join('')}
      </section>`;
  }

  function gtmChapter() {
    const data = D.gtm;
    if (!data) return '';
    // Maldives hero is owned by signed-contract-hero — do not double-render
    const parts = [];
    for (const sec of data.sections || []) {
      const fn = R[sec.type];
      if (fn) parts.push(fn(sec));
    }
    return `
      <section class="chapter" id="gtm">
        <div class="section-inner"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
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
    // Go Deeper before Own the Edge finale so the film/contact isn't buried after the close
    return `
      <section class="chapter" id="money">
        <div class="section-inner"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
        ${mainHtml}
        ${foot ? R.footer(foot) : ''}
        ${finale ? R['finale-plate'](finale) : ''}
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


  /* v5 P0-1 wrap */
  document.querySelectorAll('.section-block').forEach(function (block) {
    if (block.classList.contains('network-shift')) return;
    if (block.classList.contains('costs-morph-section')) return;
    if (block.id === 'pipeline-section') return;
    if (block.querySelector(':scope > .section-inner')) return;
    if (block.querySelector(':scope > .cinema-block, :scope > .ns-pin, :scope > .costs-morph, :scope > .arc-pin')) return;
    var kids = [];
    while (block.firstChild) kids.push(block.removeChild(block.firstChild));
    if (!kids.length) return;
    var inner = document.createElement('div');
    inner.className = 'section-inner';
    kids.forEach(function (k) { inner.appendChild(k); });
    block.appendChild(inner);
  });
  document.querySelectorAll('.video-grid, .ladder, .table-wrap, .media-duo, .native-charts, .roadmap, .thesis-board, .round, .team-layout, .demo-anchor, .unitecon, .flow-roles, .chips-3, .stack-cards').forEach(function (el) {
    if (el.closest('.media-inner, .section-inner, .pipe-layout')) return;
    var wrap = document.createElement('div');
    wrap.className = 'media-inner';
    el.parentNode.insertBefore(wrap, el);
    wrap.appendChild(el);
  });

  /* v5 P0-2 Tasklet Network Shift */
  (function () {
    var mount = document.getElementById('ns-mount');
    if (!mount || typeof window.initNetworkShift !== 'function') {
      console.warn('[invest] Network Shift engine missing');
      return;
    }
    var nsSec = ((D.claim && D.claim.sections) || []).filter(function (x) {
      return x.id === 'network-shift' || x.type === 'two-panel-transition';
    })[0];
    window.initNetworkShift(mount, {
      chips: {
        aLabel: (nsSec && nsSec.panel_before && nsSec.panel_before.label) || 'SHIPPING TODAY',
        aLine: (nsSec && nsSec.panel_before && nsSec.panel_before.line) || '',
        aStats: (nsSec && nsSec.panel_before && nsSec.panel_before.stats_line) || '',
        bLabel: (nsSec && nsSec.panel_after && nsSec.panel_after.label) || 'THE NAVIER NETWORK',
        bLine: (nsSec && nsSec.panel_after && nsSec.panel_after.line) || '',
        bStats: (nsSec && nsSec.panel_after && nsSec.panel_after.stats_line) || '',
      },
    });
    var pin = document.querySelector('.ns-pin');
    if (!pin) return;
    function onScrollNS() {
      var rect = pin.getBoundingClientRect();
      var vh = window.innerHeight || 1;
      var total = Math.max(1, pin.offsetHeight - vh * 0.35);
      var m = -rect.top / total;
      if (m < 0) m = 0;
      if (m > 1) m = 1;
      m = Math.min(1, m / 0.7);
      if (typeof window.setNetworkMix === 'function') window.setNetworkMix(m);
    }
    window.addEventListener('scroll', onScrollNS, { passive: true });
    onScrollNS();
  })();

  document.querySelectorAll('.nbar-fill[data-w]').forEach(function (el) {
    var run = function () {
      var pct = parseFloat(el.getAttribute('data-w') || '0');
      var max = parseFloat(el.getAttribute('data-max') || '100');
      if (el.namespaceURI === 'http://www.w3.org/2000/svg') {
        el.setAttribute('width', String((pct / 100) * max));
      } else {
        el.style.width = pct + '%';
      }
    };
    var io2 = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (en.isIntersecting) {
          requestAnimationFrame(run);
          io2.unobserve(el);
        }
      });
    }, { threshold: 0.15 });
    io2.observe(el);
  });

  /* ── Money ramp charts (native SVG, contract series only) ── */
  (function drawRampCharts() {
    var money = D.money;
    if (!money) return;
    var sec = (money.sections || []).filter(function (x) {
      return x.type === 'native-line-charts' || x.id === 'ramp-charts';
    })[0];
    if (!sec) return;
    var years = sec.years || [];
    var W = 400;
    var H = 200;
    var pad = { t: 16, r: 16, b: 32, l: 44 };

    function niceFmt(v) {
      // Preserve authored contract precision (e.g. 512.1, 10.5, -11.8)
      if (!isFinite(v)) return '';
      if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
      return String(Math.round(v * 10) / 10);
    }

    function drawChart(ch) {
      var host = document.querySelector('.ramp-svg-host[data-chart-id="' + ch.id + '"]');
      var legend = document.querySelector('.ramp-legend[data-legend="' + ch.id + '"]');
      if (!host) return;
      var series = ch.series || [];
      var allVals = [];
      series.forEach(function (s) {
        (s.values || []).forEach(function (v) {
          allVals.push(+v);
        });
      });
      if (!allVals.length || !years.length) return;
      var minV = Math.min.apply(null, allVals.concat(ch.zero_line ? [0] : []));
      var maxV = Math.max.apply(null, allVals.concat(ch.zero_line ? [0] : []));
      if (minV === maxV) {
        minV -= 1;
        maxV += 1;
      }
      var span = maxV - minV;
      minV -= span * 0.08;
      maxV += span * 0.12;
      var iw = W - pad.l - pad.r;
      var ih = H - pad.t - pad.b;
      function xAt(i) {
        return pad.l + (years.length <= 1 ? iw / 2 : (i / (years.length - 1)) * iw);
      }
      function yAt(v) {
        return pad.t + ih - ((v - minV) / (maxV - minV)) * ih;
      }
      var parts = [];
      // grid
      for (var g = 0; g < 4; g++) {
        var gy = pad.t + (ih * g) / 3;
        var gv = maxV - ((maxV - minV) * g) / 3;
        parts.push(
          '<line x1="' +
            pad.l +
            '" y1="' +
            gy +
            '" x2="' +
            (W - pad.r) +
            '" y2="' +
            gy +
            '" stroke="#2a2a30" stroke-width="1"/>',
        );
        parts.push(
          '<text x="' +
            (pad.l - 8) +
            '" y="' +
            (gy + 4) +
            '" text-anchor="end" fill="#8f8f96" font-size="10" font-family="Inter,sans-serif">' +
            niceFmt(gv) +
            '</text>',
        );
      }
      if (ch.zero_line && minV < 0 && maxV > 0) {
        var zy = yAt(0);
        parts.push(
          '<line x1="' +
            pad.l +
            '" y1="' +
            zy +
            '" x2="' +
            (W - pad.r) +
            '" y2="' +
            zy +
            '" stroke="#5a5a62" stroke-width="1" stroke-dasharray="4 3"/>',
        );
      }
      years.forEach(function (yr, i) {
        parts.push(
          '<text x="' +
            xAt(i) +
            '" y="' +
            (H - 8) +
            '" text-anchor="middle" fill="#8f8f96" font-size="10" font-family="Inter,sans-serif">' +
            esc(yr) +
            '</text>',
        );
      });
      var colors = { primary: '#d4af5f', secondary: '#7dd3c0' };
      series.forEach(function (ser, si) {
        var vals = ser.values || [];
        var col = colors[ser.style] || (si === 0 ? colors.primary : colors.secondary);
        var pts = vals
          .map(function (v, i) {
            return xAt(i) + ',' + yAt(+v);
          })
          .join(' ');
        var d = vals
          .map(function (v, i) {
            return (i === 0 ? 'M' : 'L') + xAt(i) + ' ' + yAt(+v);
          })
          .join(' ');
        // area for primary
        if (ser.style === 'primary' || si === 0) {
          var baseY = yAt(Math.max(0, minV) === 0 || minV > 0 ? minV : 0);
          if (ch.zero_line) baseY = yAt(0);
          else baseY = pad.t + ih;
          var area =
            d +
            ' L' +
            xAt(vals.length - 1) +
            ' ' +
            baseY +
            ' L' +
            xAt(0) +
            ' ' +
            baseY +
            ' Z';
          parts.push(
            '<path class="ramp-area" d="' +
              area +
              '" fill="' +
              col +
              '" fill-opacity="0.12"/>',
          );
        }
        parts.push(
          '<path class="ramp-line" d="' +
            d +
            '" fill="none" stroke="' +
            col +
            '" stroke-width="' +
            (ser.style === 'secondary' ? 1.75 : 2.5) +
            '" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>',
        );
        vals.forEach(function (v, i) {
          parts.push(
            '<circle class="ramp-dot" cx="' +
              xAt(i) +
              '" cy="' +
              yAt(+v) +
              '" r="3.5" fill="' +
              col +
              '"/>',
          );
          if (ser.style === 'primary' || series.length === 1) {
            parts.push(
              '<text x="' +
                xAt(i) +
                '" y="' +
                (yAt(+v) - 10) +
                '" text-anchor="middle" fill="#e0cb8f" font-size="11" font-family="Playfair Display,Georgia,serif">' +
                niceFmt(+v) +
                '</text>',
            );
          }
        });
      });
      host.innerHTML =
        '<svg viewBox="0 0 ' +
        W +
        ' ' +
        H +
        '" preserveAspectRatio="xMidYMid meet" role="img" aria-label="' +
        esc(ch.title || '') +
        '">' +
        parts.join('') +
        '</svg>';
      if (legend) {
        legend.innerHTML = series
          .map(function (ser, si) {
            var col = colors[ser.style] || (si === 0 ? colors.primary : colors.secondary);
            return (
              '<span class="ramp-leg-item"><i style="background:' +
              col +
              '"></i>' +
              esc(ser.name || '') +
              '</span>'
            );
          })
          .join('');
      }
    }

    (sec.charts || []).forEach(drawChart);

    // draw-on-enter stroke animation
    var ioRamp = new IntersectionObserver(
      function (ents) {
        ents.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.querySelectorAll('.ramp-line').forEach(function (line) {
            line.style.transition = 'stroke-dashoffset 1.1s cubic-bezier(.2,.7,.2,1)';
            line.style.strokeDashoffset = '0';
          });
          ioRamp.unobserve(en.target);
        });
      },
      { threshold: 0.25 },
    );
    document.querySelectorAll('.ramp-chart').forEach(function (el) {
      ioRamp.observe(el);
    });
  })();

  /* ── Three-costs flip: exclusive states + no-reflow + ≤2-line titles (v9.4) ── */
  (function initCostsMorph() {
    var root = document.getElementById('costs-morph');
    var section = document.querySelector('.costs-morph-section');
    var head = document.getElementById('costs-head');
    if (!root || !head) return;
    var cards = root.querySelectorAll('[data-flip-card]');
    var headCost = head.querySelector('.costs-head-layer.is-cost');
    var headLever = head.querySelector('.costs-head-layer.is-lever');
    var after = document.getElementById('costs-after');
    var staticEl = root.querySelector('.flip-static');
    var afterTimer = null;
    var titles = head.querySelectorAll('[data-fit-title]');

    function fitTitlesToTwoLines() {
      // Full-width titles; both states same size; step down until ≤2 lines
      var w = Math.max(head.clientWidth || 0, (document.querySelector('.costs-compose') || {}).clientWidth || 0, 800);
      var base = Math.max(28, Math.min(52, (3.0 / 100) * w));
      var sizes = [base, 48, 44, 40, 36, 32, 28, 24];
      var seen = {};
      sizes = sizes.filter(function (v) {
        var n = Math.round(v);
        if (seen[n]) return false;
        seen[n] = true;
        return true;
      });
      var chosen = 24;
      for (var si = 0; si < sizes.length; si++) {
        var px = sizes[si];
        var ok = true;
        titles.forEach(function (el) {
          el.style.fontSize = px + 'px';
          el.style.lineHeight = '1.2';
          el.style.maxWidth = '100%';
          el.style.width = '100%';
          var lh = px * 1.2;
          if (el.scrollHeight > lh * 2.2 + 2) ok = false;
        });
        if (ok) {
          chosen = px;
          break;
        }
      }
      titles.forEach(function (el) {
        el.style.fontSize = chosen + 'px';
        el.style.lineHeight = '1.2';
      });
      // Keep spacer titles matched so reserved height stays correct
      head.querySelectorAll('.costs-head-spacer .costs-title').forEach(function (el) {
        el.style.fontSize = chosen + 'px';
        el.style.lineHeight = '1.2';
      });
    }

    fitTitlesToTwoLines();
    window.addEventListener('resize', function () {
      fitTitlesToTwoLines();
    });

    if (reduceMotion) {
      root.classList.add('is-static');
      if (staticEl) staticEl.hidden = false;
      var grid = document.getElementById('flip-grid');
      if (grid) grid.hidden = true;
      if (after) {
        after.hidden = false;
        after.classList.add('is-in');
      }
      if (headCost) headCost.classList.add('is-visible');
      if (headLever) headLever.classList.add('is-visible');
      return;
    }

    var lastOn = false;
    function setExclusive(onLevers) {
      // Exactly one state painted — opacity 0 + visibility hidden + pointer-events none
      if (headCost) {
        headCost.classList.toggle('is-visible', !onLevers);
        headCost.setAttribute('aria-hidden', onLevers ? 'true' : 'false');
      }
      if (headLever) {
        headLever.classList.toggle('is-visible', onLevers);
        headLever.setAttribute('aria-hidden', onLevers ? 'false' : 'true');
      }
    }

    function setState(onLevers) {
      cards.forEach(function (card, i) {
        var delay = i * 120;
        setTimeout(function () {
          card.classList.toggle('is-flipped', onLevers);
        }, delay);
      });
      setExclusive(onLevers);
      if (after) {
        clearTimeout(afterTimer);
        if (onLevers) {
          afterTimer = setTimeout(function () {
            after.hidden = false;
            after.classList.add('is-in');
          }, cards.length * 120 + 300);
        } else {
          after.hidden = true;
          after.classList.remove('is-in');
        }
      }
      if (section) section.classList.toggle('on-levers', onLevers);
      lastOn = onLevers;
    }

    function onScrollCosts() {
      var rect = root.getBoundingClientRect();
      var vh = window.innerHeight || 1;
      var mid = rect.top + rect.height * 0.4;
      var on = mid < vh * 0.55 && rect.bottom > vh * 0.2;
      if (on !== lastOn) setState(on);
    }
    setExclusive(false);
    window.addEventListener('scroll', onScrollCosts, { passive: true });
    onScrollCosts();
  })();

  /* ── Live Atlas pipeline map (MapLibre + city registry) ── */
  (function initPipelineMap() {
    var host = document.getElementById('pipe-map');
    var fallback = document.getElementById('pipe-map-fallback');
    if (!host) return;

    function showFallback() {
      if (fallback) fallback.hidden = false;
      host.setAttribute('data-failed', '1');
    }

    if (reduceMotion) {
      showFallback();
      return;
    }

    var map = null;
    var activeRow = null;

    function weightColor(w) {
      if (w === 'signed') return '#d4af5f';
      if (w === 'advanced') return '#e0cb8f';
      if (w === 'defense') return '#7dd3c0';
      return '#8f8f96';
    }

    function loadScript(src) {
      return new Promise(function (resolve, reject) {
        if (document.querySelector('script[src="' + src + '"]')) {
          resolve();
          return;
        }
        var s = document.createElement('script');
        s.src = src;
        s.async = true;
        s.onload = function () {
          resolve();
        };
        s.onerror = reject;
        document.head.appendChild(s);
      });
    }

    function loadCss(href) {
      if (document.querySelector('link[href="' + href + '"]')) return;
      var l = document.createElement('link');
      l.rel = 'stylesheet';
      l.href = href;
      document.head.appendChild(l);
    }

    function cityIndex() {
      var geo = window.INVEST_PIPELINE_GEO;
      if (!geo || !geo.cities) return { byId: new Map(), all: [] };
      var byId = new Map();
      var all = geo.cities.map(function (c) {
        var feat = {
          type: 'Feature',
          geometry: { type: 'Point', coordinates: [c[0], c[1]] },
          properties: { id: c[2], name: c[3] },
        };
        byId.set(c[2], feat);
        return feat;
      });
      return { byId: byId, all: all };
    }

    function highlightNodes(coords, weight) {
      // DISCLOSURE-CRITICAL: fixed camera — NEVER pan/zoom/flyTo on row focus
      if (!map || !map.getSource('pipe-hi')) return;
      var feats = (coords || []).map(function (c, i) {
        return {
          type: 'Feature',
          geometry: { type: 'Point', coordinates: c },
          properties: { i: i, weight: weight || 'pipeline' },
        };
      });
      map.getSource('pipe-hi').setData({ type: 'FeatureCollection', features: feats });
    }

    function clearHighlight() {
      if (!map || !map.getSource('pipe-hi')) return;
      map.getSource('pipe-hi').setData({ type: 'FeatureCollection', features: [] });
    }

    function bindRows() {
      document.querySelectorAll('[data-pipe-row]').forEach(function (btn) {
        function activate() {
          document.querySelectorAll('[data-pipe-row]').forEach(function (b) {
            b.classList.toggle('is-active', b === btn);
          });
          activeRow = btn;
          var coords = [];
          try {
            coords = JSON.parse(btn.getAttribute('data-coords') || '[]');
          } catch (_) {}
          var weight = btn.getAttribute('data-weight') || 'pipeline';
          // Prefer Atlas city coords when ids resolve
          var idx = cityIndex();
          var ids = (btn.getAttribute('data-ids') || '').split(',').filter(Boolean);
          var resolved = [];
          ids.forEach(function (id) {
            var f = idx.byId.get(id);
            if (f) resolved.push(f.geometry.coordinates);
          });
          highlightNodes(resolved.length ? resolved : coords, weight);
        }
        btn.addEventListener('mouseenter', activate);
        btn.addEventListener('focus', activate);
        btn.addEventListener('click', function (e) {
          e.preventDefault();
          activate();
        });
      });
    }

    function bootMap() {
      if (typeof maplibregl === 'undefined') {
        showFallback();
        return;
      }
      var idx = cityIndex();
      try {
        // Fixed global framing — no nav control, no drag/scroll zoom (disclosure rule)
        map = new maplibregl.Map({
          container: host,
          style: {
            version: 8,
            sources: {
              basemap: {
                type: 'raster',
                tiles: [
                  'https://basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}@2x.png',
                ],
                tileSize: 256,
                attribution: '© CARTO · © OSM',
              },
            },
            layers: [
              {
                id: 'basemap',
                type: 'raster',
                source: 'basemap',
              },
            ],
          },
          center: [20, 18],
          zoom: 1.15,
          minZoom: 1.15,
          maxZoom: 1.15,
          attributionControl: false,
          interactive: false,
          dragPan: false,
          scrollZoom: false,
          boxZoom: false,
          doubleClickZoom: false,
          touchZoomRotate: false,
          keyboard: false,
        });
        map.on('load', function () {
          map.addSource('cities', {
            type: 'geojson',
            data: { type: 'FeatureCollection', features: idx.all },
          });
          map.addLayer({
            id: 'cities-dot',
            type: 'circle',
            source: 'cities',
            paint: {
              'circle-radius': 2.2,
              'circle-color': '#5a6570',
              'circle-opacity': 0.55,
            },
          });
          // default pipeline nodes (all rows)
          var allNodes = [];
          document.querySelectorAll('[data-pipe-row]').forEach(function (btn) {
            var weight = btn.getAttribute('data-weight') || 'pipeline';
            var coords = [];
            try {
              coords = JSON.parse(btn.getAttribute('data-coords') || '[]');
            } catch (_) {}
            var ids = (btn.getAttribute('data-ids') || '').split(',').filter(Boolean);
            var resolved = [];
            ids.forEach(function (id) {
              var f = idx.byId.get(id);
              if (f) resolved.push(f.geometry.coordinates);
            });
            (resolved.length ? resolved : coords).forEach(function (c) {
              allNodes.push({
                type: 'Feature',
                geometry: { type: 'Point', coordinates: c },
                properties: { weight: weight },
              });
            });
          });
          map.addSource('pipe-nodes', {
            type: 'geojson',
            data: { type: 'FeatureCollection', features: allNodes },
          });
          map.addLayer({
            id: 'pipe-nodes-glow',
            type: 'circle',
            source: 'pipe-nodes',
            paint: {
              'circle-radius': 10,
              'circle-color': [
                'match',
                ['get', 'weight'],
                'signed',
                '#d4af5f',
                'advanced',
                '#e0cb8f',
                'defense',
                '#7dd3c0',
                '#8f8f96',
              ],
              'circle-opacity': 0.22,
            },
          });
          map.addLayer({
            id: 'pipe-nodes-core',
            type: 'circle',
            source: 'pipe-nodes',
            paint: {
              'circle-radius': [
                'match',
                ['get', 'weight'],
                'signed',
                6,
                'advanced',
                5,
                4,
              ],
              'circle-color': [
                'match',
                ['get', 'weight'],
                'signed',
                '#d4af5f',
                'advanced',
                '#e0cb8f',
                'defense',
                '#7dd3c0',
                '#a0a0a8',
              ],
              'circle-stroke-width': [
                'match',
                ['get', 'weight'],
                'signed',
                0,
                1.5,
              ],
              'circle-stroke-color': '#d4af5f',
            },
          });
          map.addSource('pipe-hi', {
            type: 'geojson',
            data: { type: 'FeatureCollection', features: [] },
          });
          map.addLayer({
            id: 'pipe-hi-ring',
            type: 'circle',
            source: 'pipe-hi',
            paint: {
              'circle-radius': 14,
              'circle-color': '#d4af5f',
              'circle-opacity': 0.18,
            },
          });
          map.addLayer({
            id: 'pipe-hi-core',
            type: 'circle',
            source: 'pipe-hi',
            paint: {
              'circle-radius': 7,
              'circle-color': '#f0d78c',
              'circle-stroke-width': 2,
              'circle-stroke-color': '#fff8e0',
            },
          });
          bindRows();
          // flash signed Maldives as default money moment
          var signed = document.querySelector('[data-pipe-row].weight-signed');
          if (signed) signed.dispatchEvent(new Event('mouseenter'));
        });
      } catch (err) {
        console.warn('[invest] pipeline map failed', err);
        showFallback();
      }
    }

    // Lazy-init when section nears viewport
    var section = document.getElementById('pipeline-section');
    var started = false;
    function start() {
      if (started) return;
      started = true;
      loadCss('https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css');
      Promise.all([
        loadScript('https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js'),
        loadScript('/invest/pipeline-geo.js'),
      ])
        .then(bootMap)
        .catch(function (e) {
          console.warn('[invest] pipeline deps', e);
          showFallback();
        });
    }
    if (!section) {
      start();
      return;
    }
    var ioPipe = new IntersectionObserver(
      function (ents) {
        ents.forEach(function (en) {
          if (en.isIntersecting) {
            start();
            ioPipe.disconnect();
          }
        });
      },
      { rootMargin: '200px', threshold: 0.01 },
    );
    ioPipe.observe(section);
  })();

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
    const loopCard = e.target.closest('.vcard-loop');
    if (loopCard) {
      const v = loopCard.querySelector('video');
      const play = loopCard.querySelector('.play');
      if (v) {
        e.preventDefault();
        // First click: unmute + ensure playing. Second: mute again.
        if (v.muted) {
          v.muted = false;
          v.play().catch(function () {});
          loopCard.classList.add('is-audible');
          if (play) play.style.opacity = '0';
        } else {
          v.muted = true;
          loopCard.classList.remove('is-audible');
          if (play) play.style.opacity = '';
        }
      }
      return;
    }
    const t = e.target.closest('[data-yt]');
    if (!t || t.classList.contains('looping')) return;
    const yt = t.getAttribute('data-yt');
    const emb = t.getAttribute('data-embed');
    if (yt || emb) {
      e.preventDefault();
      openYt(emb, yt);
    }
  });

  /* ── Control diagram: hairline leaders (mandatory annotations) ── */
  (function initControlLeaders() {
    var root = document.getElementById('control-diagram');
    var svg = document.getElementById('control-leaders');
    if (!root || !svg) return;
    var img = root.querySelector('.control-wire');
    // Percentage viewBox — coords match the figure box (tight to the PNG)
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.setAttribute('preserveAspectRatio', 'none');
    function drawLeaders() {
      var lines = [];
      root.querySelectorAll('.ctrl-anchor').forEach(function (anchor) {
        var i = anchor.getAttribute('data-anchor');
        var callout = root.querySelector('.ctrl-callout[data-callout="' + i + '"]');
        if (!callout) return;
        var x1 = parseFloat(anchor.style.left) || 50;
        var y1 = parseFloat(anchor.style.top) || 50;
        var lx = parseFloat(callout.style.left) || x1;
        var ly = parseFloat(callout.style.top) || y1;
        // left/top on the callout is already the near-edge (toward the boat)
        lines.push(
          '<line class="ctrl-leader" x1="' +
            x1 +
            '" y1="' +
            y1 +
            '" x2="' +
            lx +
            '" y2="' +
            ly +
            '" vector-effect="non-scaling-stroke" />',
        );
        lines.push(
          '<circle class="ctrl-dot" cx="' +
            x1 +
            '" cy="' +
            y1 +
            '" r="1.15" data-dot="' +
            i +
            '" />',
        );
      });
      svg.innerHTML = lines.join('');
      root.classList.add('is-lit');
    }
    drawLeaders();
    if (img && !img.complete) img.addEventListener('load', drawLeaders);
    window.addEventListener('resize', drawLeaders);

    // Hover/focus: highlight one callout, dim others
    function focusCallout(idx) {
      root.querySelectorAll('.ctrl-callout, .ctrl-anchor').forEach(function (el) {
        var i = el.getAttribute('data-callout') || el.getAttribute('data-anchor');
        el.classList.toggle('is-focus', String(i) === String(idx));
        el.classList.toggle('is-dim', String(i) !== String(idx));
      });
      // leaders and dots alternate in SVG (line, circle, line, circle, …)
      var kids = svg.querySelectorAll('.ctrl-leader, .ctrl-dot');
      kids.forEach(function (el, li) {
        var pair = Math.floor(li / 2);
        el.classList.toggle('is-dim', String(pair) !== String(idx));
      });
    }
    function clearFocus() {
      root.querySelectorAll('.is-focus, .is-dim').forEach(function (el) {
        el.classList.remove('is-focus', 'is-dim');
      });
      svg.querySelectorAll('.is-dim').forEach(function (el) {
        el.classList.remove('is-dim');
      });
    }
    root.querySelectorAll('.ctrl-callout, .ctrl-anchor').forEach(function (el) {
      var idx = el.getAttribute('data-callout') || el.getAttribute('data-anchor');
      el.addEventListener('mouseenter', function () {
        focusCallout(idx);
      });
      el.addEventListener('focus', function () {
        focusCallout(idx);
      });
      el.addEventListener('mouseleave', clearFocus);
      el.addEventListener('blur', clearFocus);
    });

    var io = new IntersectionObserver(
      function (ents) {
        ents.forEach(function (en) {
          if (en.isIntersecting) root.classList.add('is-lit');
        });
      },
      { threshold: 0.15 },
    );
    io.observe(root);
  })();

  /* Pioneer hero: hide poster fallback when video plays */
  (function () {
    document.querySelectorAll('.pioneer-hero-video').forEach(function (v) {
      var wrap = v.closest('.pioneer-hero');
      function ok() {
        if (wrap) wrap.classList.add('has-video');
      }
      function bad() {
        if (wrap) wrap.classList.remove('has-video');
      }
      v.addEventListener('loadeddata', ok);
      v.addEventListener('playing', ok);
      v.addEventListener('error', bad);
      // If source 404s, keep poster
      var src = v.querySelector('source');
      if (src && src.getAttribute('src')) {
        fetch(src.getAttribute('src'), { method: 'HEAD' }).then(function (r) {
          if (!r.ok) bad();
        }).catch(bad);
      }
    });
  })();

  /* Thesis board — tap to expand on touch (no hover) */
  (function initThesisTap() {
    document.querySelectorAll('.thesis-row').forEach(function (row) {
      row.addEventListener('click', function () {
        var open = row.classList.toggle('is-open');
        row.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      row.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          row.click();
        }
      });
    });
  })();

  /* ── Arc scroll-driven sequence (accumulate 1→N) ───── */
  (function initArcReveal() {
    var pin = document.getElementById('arc-pin');
    var rail = document.getElementById('arc-rail') || document.querySelector('.arc-rail');
    if (!pin || !rail) return;
    var phases = Array.prototype.slice.call(rail.querySelectorAll('.arc-phase'));
    if (!phases.length) return;
    var section = pin.closest('[data-pills]') || pin;
    var total = phases.length;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var mobile = window.matchMedia('(max-width: 720px)').matches;

    function setVisible(count) {
      var n = Math.max(1, Math.min(total, count));
      phases.forEach(function (p, i) {
        var on = i < n;
        p.classList.toggle('is-revealed', on);
        p.classList.toggle('lit', on);
        p.setAttribute('aria-hidden', on ? 'false' : 'true');
      });
      pin.setAttribute('data-arc-visible', String(n));
      rail.style.setProperty('--arc-progress', String(n / total));
    }

    if (reduce) {
      setVisible(total);
      return;
    }

    // Mobile: reveal each phase as it enters the viewport (column stack)
    if (mobile) {
      setVisible(1);
      var io = new IntersectionObserver(
        function (ents) {
          ents.forEach(function (en) {
            if (!en.isIntersecting) return;
            var step = +en.target.getAttribute('data-step') || 1;
            var cur = +pin.getAttribute('data-arc-visible') || 1;
            if (step > cur) setVisible(step);
          });
        },
        { threshold: 0.35, rootMargin: '0px 0px -10% 0px' },
      );
      phases.forEach(function (p) { io.observe(p); });
      return;
    }

    // Desktop: sticky pin — scroll progress maps to how many phases are visible
    function onScroll() {
      var rect = pin.getBoundingClientRect();
      var pinH = pin.offsetHeight;
      var viewH = window.innerHeight || 1;
      // progress 0 when sticky starts, 1 when pin bottom hits viewport bottom
      var scrollable = Math.max(1, pinH - viewH);
      var scrolled = Math.min(scrollable, Math.max(0, -rect.top));
      var progress = scrolled / scrollable;
      // Map progress across phases: start with 1, end with all 6
      var count = 1 + Math.floor(progress * (total - 0.0001));
      setVisible(count);
    }

    setVisible(1);
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    onScroll();
  })();

  /* ── Ladder ────────────────────────────────────────── */
  const hulls = (D.ladder && D.ladder.hulls) || [];
  function setHull(i) {
    const h = hulls[i];
    if (!h) return;
    document.querySelectorAll('.ladder-tab').forEach((el, j) => el.classList.toggle('active', j === i));
    const img = $('#ladder-img');
    const plate = $('#ladder-plate');
    const info = ladderImg(h);
    if (plate) {
      plate.classList.toggle('photo', !!info.photo);
      plate.setAttribute('data-hull-id', info.id || h.id || '');
    }
    // A1: set src immediately — delayed swap left N80 showing prior N30 frame
    if (img && info.src) {
      if (img.getAttribute('src') !== info.src) {
        img.style.opacity = '0.35';
        img.onload = function () {
          img.style.opacity = '1';
        };
        img.src = info.src;
        img.setAttribute('data-hull-id', info.id || h.id || '');
        img.alt = h.name || '';
      } else {
        img.style.opacity = '1';
      }
    }
    const meta = $('#ladder-meta');
    if (meta) {
      const dev = info.dev
        ? `<div class="render-chip">RENDER — IN DEVELOPMENT</div>`
        : '';
      const chips = [h.status_chip, h.status_chip_2].filter(Boolean)
        .map((c) => `<div class="status">${esc(c)}</div>`)
        .join('');
      meta.innerHTML = `
        <div class="name">${esc(h.name)}</div>
        <div class="class">${esc(h.length_class || '')}</div>
        <div class="mission">${esc(h.mission || '')}</div>
        ${chips}
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
        // Arc phases are scroll-driven in initArcReveal — do not stagger-lit here
        if (en.target.dataset.bars != null || en.target.querySelector('[data-bar-pct]')) {
          const root = en.target.dataset.bars != null ? en.target : en.target;
          root.querySelectorAll('.bar-row').forEach((row) => {
            const pct = row.dataset.barPct || 50;
            const fill = row.querySelector('.bar-fill');
            if (fill) requestAnimationFrame(() => (fill.style.width = pct + '%'));
          });
        }
        en.target.querySelectorAll('.callout-item').forEach((c, i) => {
          setTimeout(() => c.classList.add('in'), i * 120);
        });
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
  document.querySelectorAll('[data-reveal]').forEach((el) => {
    // optional enhance only if user hasn't reduced motion
    if (!reduceMotion) el.classList.add('reveal-pending');
    io.observe(el);
  });
  // observe bar sections
  document.querySelectorAll('[data-bars]').forEach((el) => io.observe(el));

  // QA: no raw JSON braces in visible text
  try {
    const text = app.innerText || '';
    if (text.includes('{"') || text.includes('{"label"')) {
      console.warn('[invest] G3 possible JSON leak in rendered text');
    }
    console.info('[invest] v6 mount ok, homes', homes.size);
  } catch (_) {}
})();
