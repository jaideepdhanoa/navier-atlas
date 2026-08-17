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
  function formatBackers(line) {
    if (!line) return '';
    return String(line)
      .split(/[·•\n]/)
      .map(function (n) { return n.trim(); })
      .filter(Boolean)
      .map(function (n, i, arr) {
        return '<span>' + esc(n) + '</span>' +
          (i < arr.length - 1 ? '<i class="sep" aria-hidden="true"></i>' : '');
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
    return `
      <div class="cinema-block" data-home="${esc(opts.home || '')}" data-reveal>
        <div class="cinema">
          <div class="cinema-media" style="${opts.vh ? `height:${opts.vh}` : ''}">
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
        ${
          s.closing_line
            ? `<div class="section-inner"><p class="ns-kicker">${nl(s.closing_line)}</p></div>`
            : ''
        }
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
            ? `<div class="backers-type"><div class="bl">${esc(s.backers_label || 'BACKED BY')}</div><div class="names">${formatBackers(s.backers_line)}</div></div>`
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
        <div class="section-block stage-section arc-section" data-reveal data-pills data-now="${s.now_marker_on || 0}">
          <div class="section-inner">
            <p class="stage-kicker">01 · THE CLAIM</p>
            ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
            <div class="arc-rail media-inner" style="max-width:none;padding:0">${pills}</div>
          </div>
        </div>`;
    },

    'team-grid'(s) {
      return renderTeam(s);
    },

    'flip-cards'(s) {
      // v1-blocking: two-stage scroll morph — costs pillars → lever columns (deck 435/436)
      const pairs = s.pairs || [];
      const costRail = pairs
        .map((pair, i) => {
          const n = String(i + 1).padStart(2, '0');
          const title = pair.cost.title || '';
          const lead = title.split(/\s*[—–-]\s*/)[0] || title;
          const rest = title.slice(lead.length).replace(/^\s*[—–-]\s*/, '');
          return `
          <div class="cm-cost-row" data-i="${i}">
            <span class="cm-num">${n}</span>
            <div>
              <div class="cm-cost-lead">${esc(lead)}</div>
              ${rest ? `<div class="cm-cost-sub">${esc(rest)}</div>` : ''}
              <div class="cm-cost-body">${esc(pair.cost.body || '')}</div>
            </div>
          </div>`;
        })
        .join('');
      const leverCols = pairs
        .map((pair, i) => {
          const n = String(i + 1).padStart(2, '0');
          return `
          <div class="cm-lever-col" data-i="${i}">
            <div class="cm-num">${n}</div>
            <div class="cm-lever-title">${esc(pair.lever.title || '')}</div>
            <div class="cm-lever-mech">${esc(pair.lever.mechanism || '')}</div>
            <div class="cm-lever-proof">${esc(pair.lever.proof || '')}</div>
          </div>`;
        })
        .join('');
      const why = s.why_now
        ? `<div class="why-now">
            <h3 class="h3">${esc(s.why_now.title)}</h3>
            <p class="body-text">${nl(s.why_now.body || s.why_now.line || '')}</p>
            ${s.why_now.closing_line ? `<p class="closing-line">${esc(s.why_now.closing_line)}</p>` : ''}
          </div>`
        : '';
      return `
        <div class="section-block costs-morph-section" data-reveal data-home="claim.three_costs">
          <div class="section-inner">
            ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          </div>
          <div class="costs-morph" id="costs-morph">
            <div class="costs-morph-sticky">
              <div class="cm-stage cm-stage-costs" data-stage="costs">
                <div class="cm-grid">
                  <div class="cm-rail">
                    <p class="stage-kicker">THREE COSTS</p>
                    ${costRail}
                  </div>
                  <div class="cm-photo-stack">
                    <p class="cm-kicker">${esc(s.costs_kicker || 'Different missions. Same constraints.')}</p>
                    <div class="cm-stack-card" aria-hidden="true"></div>
                    <div class="cm-stack-card" aria-hidden="true"></div>
                    <div class="cm-stack-card" aria-hidden="true"></div>
                  </div>
                </div>
              </div>
              <div class="cm-stage cm-stage-levers" data-stage="levers">
                <div class="cm-levers-head">
                  <p class="stage-kicker">THREE LEVERS</p>
                  ${s.flip_headline ? `<h3 class="cm-flip-h">${esc(s.flip_headline)}</h3>` : ''}
                </div>
                <div class="cm-levers-grid">${leverCols}</div>
              </div>
            </div>
          </div>
          <div class="section-inner">${why}
            ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
          </div>
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
      const wire = homeSrc('product.control.diagram') || mediaPath('assets/deck/control-wireframe-clean.png');
      const hs = (s.hotspots || [])
        .map(
          (h, i) =>
            `<div class="callout-item" data-callout="${i}"><strong>${esc(h.label)}</strong>${h.detail ? esc(h.detail) : ''}</div>`,
        )
        .join('');
      return `
        <div class="section-block stage-section" data-reveal data-home="product.control.diagram">
          <div class="section-inner">
            ${s.title ? `<p class="stage-kicker">03 · THE PRODUCT</p><h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.body ? `<p class="lead">${nl(s.body)}</p>` : ''}
            <div class="stage-grid">
              <div class="sg-media">
                ${wire ? plate(wire, { home: 'product.control.diagram', className: 'wire-plate contain' }) : ''}
                ${s.video ? filmCard(s.video, filmPoster, 'product.control.film', s.video_label || '') : ''}
              </div>
              <div class="sg-title"><div class="callout-list">${hs}</div></div>
            </div>
          </div>
        </div>`;
    },

    'platform-intro'(s) {
      const wire = homeSrc('product.gmvp.diagram') || mediaPath('assets/deck/fleet-wireframe.png');
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
              <!-- Four Seasons film stays in Proof demo grid only (v6) -->
            </div>
          </div>
        </div>`;
    },

    'program-panel'(s) {
      const gulf = homeSrc('gtm.gulf.plate') || mediaPath('assets/deck/gulf-hero.png');
      return `
        <div class="section-block stage-section" data-reveal data-home="gtm.gulf.plate">
          ${gulf ? cinema(gulf, { home: 'gtm.gulf.plate', vh: '55vh' }) : ''}
          <div class="section-inner">
            ${s.title ? `<p class="stage-kicker">04 · GO-TO-MARKET</p><h2 class="h2">${esc(s.title)}</h2>` : ''}
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
        <div class="section-block shell-stage" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          <div class="stack-cards">${cards}</div>
          ${s.formula_line ? `<div class="formula">${esc(s.formula_line)}</div>` : ''}
        </div>`;
    },

    'four-role-diagram'(s) {
      const logos = homeAssets('gtm.coastal.logos') || {};
      const order = [
        { key: 'navier', role: 'Platform & vessels' },
        { key: 'jih', role: 'Capital' },
        { key: 'harim', role: 'Hotels & resorts' },
        { key: 'visit_maldives', role: 'Demand' },
      ];
      // Prefer contract roles for captions when present
      const roles = s.roles || s.cards || [];
      const logoCards = order
        .map((o, i) => {
          const src = logos[o.key] ? mediaPath(logos[o.key]) : '';
          const r = roles[i] || {};
          const title = r.title || r.name || r.role || o.key.replace(/_/g, ' ');
          const does = r.does || r.body || r.detail || o.role;
          return `<div class="player-logo">
            ${src ? `<img src="${esc(src)}" alt="${esc(title)}" loading="lazy" />` : ''}
            <div class="title" style="font-weight:700;margin-bottom:4px">${esc(title)}</div>
            <div class="role">${esc(does)}</div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block stage-section" data-reveal data-home="gtm.coastal.logos">
          <div class="section-inner">
            ${s.title ? `<p class="stage-kicker">04 · GO-TO-MARKET</p><h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead || s.intro ? `<p class="lead">${esc(s.subhead || s.intro)}</p>` : ''}
            <div class="player-logos">${logoCards}</div>
            ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
          </div>
        </div>`;
    },

    'drawing-chart'(s) {
      const ca = homeAssets('gtm.cargo') || {};
      const opener = ca.opener ? mediaPath(ca.opener) : mediaPath('assets/deck/air-vs-ocean-cargo.png');
      const playPlate = mediaPath(ca.play || 'assets/deck/cargo-play-skyline.png');
      const shipH = mediaPath(ca.shipscale || 'assets/deck/shipscale-hero.png');
      const shipG = mediaPath(ca.shipscale_grid || 'assets/deck/shipscale-variants-grid.png');
      const wedgeP = mediaPath(ca.wedge || 'assets/deck/wedge-day-night.png');
      const night = ca.night_pair || [];
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
          <div class="section-inner">
            ${s.title ? `<p class="stage-kicker">04 · GO-TO-MARKET</p><h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            <div class="chips-3">${cards}</div>
            ${c.navier_band ? `<div class="formula">${esc(c.navier_band)}</div>` : ''}
          </div>`;
      }
      let islandHtml = '';
      const ib = s.island_band;
      if (ib && typeof ib === 'object') {
        islandHtml = `
          <div class="section-inner island-band" data-reveal>
            ${ib.title ? `<p class="stage-kicker">ISLANDS</p><h2 class="h2">${esc(ib.title)}</h2>` : ''}
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
          </div>`;
      }
      return `
        <div class="section-block" data-reveal data-home="gtm.cargo">
          <div class="cinema-block" data-reveal>
            <div class="cinema"><div class="cinema-media" style="height:min(80vh,720px);display:flex;align-items:center;justify-content:center;background:#0a0a0c">
              <img src="${esc(opener)}" alt="" loading="lazy" style="object-fit:contain;max-height:80vh;width:auto;max-width:100%" />
            </div></div>
          </div>
          ${chartHtml}
          ${islandHtml}
          ${
            night.length
              ? `<div class="media-inner foundry-pair">${night.map((n) => plate(mediaPath(n), { home: 'gtm.cargo' })).join('')}</div>`
              : ''
          }
          <div class="section-block stage-section" data-reveal>
            <div class="section-inner">
              <p class="stage-kicker">THE PLAY</p>
              ${plate(playPlate, { className: 'contain' })}
            </div>
          </div>
          <div class="section-block stage-section" data-reveal>
            <div class="section-inner">
              <p class="stage-kicker">SHIP SCALE</p>
              ${plate(shipH, { className: 'contain' })}
              ${plate(shipG, { className: 'contain' })}
            </div>
          </div>
          <div class="section-block stage-section" data-reveal>
            <div class="section-inner">
              <p class="stage-kicker">THE WEDGE</p>
              ${plate(wedgeP, { className: 'contain' })}
            </div>
          </div>
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

    'native-line-charts'(s) {
      // Money v2 lead: FY26E–FY30E ramp — exact contract series, native SVG only
      // Series data stays in INVEST_DATA.money; draw pass reads it after mount
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
        <div class="section-block shell-stage" data-reveal data-home="money.charts" data-ramp-root>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="native-charts ramp-charts">${charts}</div>
          ${s.note ? `<p class="muted">${esc(s.note)}</p>` : ''}
        </div>`;
    },

    'stat-band'(s) {
      // FY30 chips — secondary to ramp charts (money v2)
      const foot =
        s.footnote && !/^[a-z0-9-]+$/i.test(String(s.footnote).trim())
          ? s.footnote
          : '';
      return `
        <div class="section-block shell-stage" data-reveal data-home="money.charts">
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${goldStats(s.stats)}
          ${foot ? `<p class="muted">${esc(foot)}</p>` : ''}
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
    const id = hull.id || '';
    // v6: N30 + Quanta = pioneer photo; N45 mobility render; N80 wireframe (render pending approval); N180 shipscale
    if (id === 'n30-pioneer' || id === 'quanta-lr') {
      const src = la.n30_pioneer || la.quanta_lr;
      return { src: src ? mediaPath(src) : '', photo: true, dev: false };
    }
    if (id === 'n45-explorer' && la.n45_explorer) {
      return { src: mediaPath(la.n45_explorer), photo: true, dev: false };
    }
    if (id === 'n80-valkyrie') {
      // n80-render-v1 APPROVED 2026-08-17 — photoreal + render chip
      const src = la.n80_valkyrie || 'assets/deck/n80-render-v1.png';
      return { src: mediaPath(src), photo: true, dev: true };
    }
    if (id === 'n180-morpheus' && la.n180_morpheus) {
      return { src: mediaPath(la.n180_morpheus), photo: true, dev: false };
    }
    const key = String(id).replace(/-/g, '_');
    if (la[key]) return { src: mediaPath(la[key]), photo: false, dev: true };
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

  function renderPipeline() {
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
          ${p.eyebrow ? `<p class="eyebrow">${esc(p.eyebrow)}</p>` : ''}
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
    return `
      <section class="chapter" id="money">
        <div class="section-inner"><p class="chapter-label">${esc(data.chapter_label || '')}</p></div>
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


  /* v5 P0-1 wrap */
  document.querySelectorAll('.section-block').forEach(function (block) {
    if (block.classList.contains('network-shift')) return;
    if (block.classList.contains('costs-morph-section')) return;
    if (block.id === 'pipeline-section') return;
    if (block.querySelector(':scope > .section-inner')) return;
    if (block.querySelector(':scope > .cinema-block, :scope > .ns-pin, :scope > .costs-morph')) return;
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

  /* ── Three-costs two-stage scroll morph ─────────────── */
  (function initCostsMorph() {
    var root = document.getElementById('costs-morph');
    if (!root) return;
    var costs = root.querySelector('.cm-stage-costs');
    var levers = root.querySelector('.cm-stage-levers');
    if (!costs || !levers) return;
    if (reduceMotion) {
      root.classList.add('is-static');
      costs.style.opacity = '1';
      levers.style.opacity = '1';
      levers.style.position = 'relative';
      return;
    }
    function onScrollCosts() {
      var rect = root.getBoundingClientRect();
      var vh = window.innerHeight || 1;
      var total = Math.max(1, root.offsetHeight - vh * 0.5);
      var p = -rect.top / total;
      if (p < 0) p = 0;
      if (p > 1) p = 1;
      // hold costs 0–0.35, morph 0.35–0.7, hold levers 0.7–1
      var t = 0;
      if (p < 0.35) t = 0;
      else if (p > 0.7) t = 1;
      else t = (p - 0.35) / 0.35;
      costs.style.opacity = String(1 - t);
      costs.style.transform = 'translateY(' + t * -24 + 'px)';
      levers.style.opacity = String(t);
      levers.style.transform = 'translateY(' + (1 - t) * 28 + 'px)';
      root.classList.toggle('on-levers', t > 0.55);
    }
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
      if (!map || !map.getSource('pipe-hi')) return;
      var feats = (coords || []).map(function (c, i) {
        return {
          type: 'Feature',
          geometry: { type: 'Point', coordinates: c },
          properties: { i: i, weight: weight || 'pipeline' },
        };
      });
      map.getSource('pipe-hi').setData({ type: 'FeatureCollection', features: feats });
      if (feats.length) {
        var c0 = feats[0].geometry.coordinates;
        map.easeTo({ center: c0, zoom: Math.max(map.getZoom(), 3.2), duration: 700 });
      }
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
          center: [40, 20],
          zoom: 1.35,
          attributionControl: false,
          interactive: true,
        });
        map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
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
