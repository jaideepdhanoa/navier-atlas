/**
 * /defense capability brief — port invest hero, nav, demo-grid, quanta, dual-use.
 * Password gate is middleware. No links to /invest.
 */
(function () {
  const D = window.DEFENSE_DATA;
  if (!D) {
    document.body.innerHTML = '<p style="padding:24px;color:#e0cb8f">Missing defense data.</p>';
    return;
  }
  const TEAM = (window.DEFENSE_TEAM && window.DEFENSE_TEAM.people) || [];
  const TEAM_ASSETS = (window.DEFENSE_TEAM_ASSETS && window.DEFENSE_TEAM_ASSETS.cards) || {};
  const TEAM_FEATURED = (window.DEFENSE_TEAM_ASSETS && window.DEFENSE_TEAM_ASSETS.featured) || '';
  const BASE = '/defense/';
  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (sel, el) => (el || document).querySelector(sel);

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function nl(s) {
    return esc(s).replace(/\n/g, '<br/>');
  }
  function mediaPath(src) {
    if (!src) return '';
    if (/^https?:\/\//i.test(src) || src.startsWith('//') || src.startsWith('/')) return src;
    return BASE + src.replace(/^\.\//, '');
  }
  function kicker(s, fallback) {
    const t = (s && (s.kicker || s.eyebrow)) || fallback || '';
    return t ? `<p class="eyebrow stage-kicker def-kicker">${esc(t)}</p>` : '';
  }
  function titleCaseHeadline(str) {
    if (!str) return '';
    const s = String(str);
    const letters = s.replace(/[^A-Za-z]/g, '');
    if (!letters || letters !== letters.toUpperCase()) return s;
    return s.toLowerCase().replace(/(^|[\s—–\-/:])([a-z])/g, function (_, p, c) {
      return p + c.toUpperCase();
    });
  }
  function goldStats(stats) {
    if (!stats || !stats.length) return '';
    const n = Math.min(stats.length, 5);
    const cells = stats
      .map(
        (st) => `<div class="gold-stat">
        <div class="value">${esc(st.value || st.stat || '')}</div>
        <div class="label">${esc(st.label || st.detail || '')}</div>
      </div>`
      )
      .join('');
    return `<div class="gold-stat-band cols-${n}" data-reveal>${cells}</div>`;
  }
  function plate(src, alt, caption) {
    if (!src) return '';
    return `<figure class="def-plate">
      <img src="${esc(mediaPath(src))}" alt="${esc(alt || '')}" loading="lazy" />
      ${caption ? `<figcaption>${esc(caption)}</figcaption>` : ''}
    </figure>`;
  }
  function blocksHtml(blocks) {
    if (!blocks || !blocks.length) return '';
    return `<div class="def-blocks">${blocks
      .map(
        (b) =>
          `<div class="def-block"><div class="head">${esc(b.head || b.title || '')}</div><p>${esc(b.body || '')}</p></div>`
      )
      .join('')}</div>`;
  }
  function brandMark() {
    return `<div class="inv-brand-mark" aria-hidden="true"><svg viewBox="9.5 9.5 160 160" fill="currentColor"><path d="M130.16 117.84 L120.18 135.12 A0.39 0.39 0 0 1 119.50 135.11 L68.16 44.06 A0.39 0.39 0 0 1 68.50 43.48 L88.22 43.48 A0.39 0.39 0 0 1 88.56 43.68 L130.16 117.46 A0.39 0.39 0 0 1 130.16 117.84 Z"/><path d="M132.68 111.67 L122.61 93.82 A0.55 0.55 0 0 1 122.62 93.28 L150.95 44.21 A0.55 0.55 0 0 1 151.90 44.21 L161.97 62.07 A0.55 0.55 0 0 1 161.96 62.61 L133.63 111.68 A0.55 0.55 0 0 1 132.68 111.67 Z"/><path d="M110.65 135.52 L90.76 135.52 A0.33 0.33 0 0 1 90.48 135.35 L48.97 61.75 A0.33 0.33 0 0 1 48.97 61.43 L59.03 44.00 A0.33 0.33 0 0 1 59.60 44.00 L110.93 135.03 A0.33 0.33 0 0 1 110.65 135.52 Z"/><path d="M26.53 134.96 L17.16 118.32 A0.67 0.67 0 0 1 17.16 117.66 L45.57 68.46 A0.67 0.67 0 0 1 46.74 68.46 L56.11 85.09 A0.67 0.67 0 0 1 56.11 85.75 L27.70 134.96 A0.67 0.67 0 0 1 26.53 134.96 Z"/></svg></div>`;
  }

  function filmCard(video, poster, label) {
    if (!video && !poster) return '';
    const p = mediaPath(poster || (video && video.poster) || '');
    const embed = (video && (video.embed_url || video.src)) || '';
    const isLocal = embed && !/^https?:/i.test(embed) && !embed.includes('youtube');
    const attrs = isLocal
      ? `data-film-src="${esc(mediaPath(embed))}"`
      : `data-yt-embed="${esc(embed)}"`;
    const dur = video && video.duration ? `<span class="dur">${esc(video.duration)}</span>` : '';
    return `<button type="button" class="film-card" ${attrs} aria-label="Play ${esc((video && video.title) || label || 'video')}">
      <span class="film-media">
        ${p ? `<img src="${esc(p)}" alt="" loading="lazy" />` : ''}
        <span class="play" aria-hidden="true"><span>▶</span></span>
        ${dur}
      </span>
      ${label ? `<span class="film-cap">${esc(label)}</span>` : ''}
    </button>`;
  }

  function videoTile(v, opts) {
    opts = opts || {};
    const poster = mediaPath(v.poster || '');
    const behavior = String(v.behavior || '');
    const withSound = /with sound/i.test(behavior) || !!opts.withSound;
    const autoplay = /autoplay/i.test(behavior) && !withSound && !reduceMotion;
    const click = !autoplay && (/click-to-play/i.test(behavior) || withSound || !!opts.click);

    if (v.embed_url && opts.filmCard) {
      return filmCard(v, v.poster, [v.title, v.duration].filter(Boolean).join(' · '));
    }
    if (v.embed_url) {
      const thumb = poster || '';
      return `<figure class="def-video-tile" data-yt-embed="${esc(v.embed_url)}">
        <div class="def-video-frame">
          ${thumb ? `<img class="def-video-poster" src="${esc(thumb)}" alt="${esc(v.title || '')}" loading="lazy" />` : '<div class="def-video-poster def-video-poster--empty"></div>'}
          <button type="button" class="film-play" aria-label="Play ${esc(v.title || 'video')}"><span class="film-play-btn" aria-hidden="true">▶</span></button>
        </div>
        ${v.title ? `<div class="def-video-title">${esc(v.title)}${v.duration ? ' · ' + esc(v.duration) : ''}</div>` : ''}
        ${v.caption ? `<figcaption>${esc(v.caption)}</figcaption>` : ''}
      </figure>`;
    }
    if (!v.src) return '';
    const attrs = [
      'playsinline',
      autoplay ? 'preload="auto"' : 'preload="metadata"',
      poster ? `poster="${esc(poster)}"` : '',
      autoplay ? 'muted loop autoplay data-lazy-video' : '',
      click ? 'data-click-play' : '',
      withSound ? 'data-click-sound-film' : '',
    ]
      .filter(Boolean)
      .join(' ');
    return `<figure class="def-video-tile${opts.wide ? ' def-video-tile--wide' : ''}">
      <div class="def-video-frame${click || withSound ? ' has-play' : ''}">
        <video ${attrs}><source src="${esc(mediaPath(v.src))}" type="video/mp4" /></video>
        ${
          click || withSound
            ? `<button type="button" class="film-play" aria-label="Play ${esc(v.title || 'video')}"><span class="film-play-btn" aria-hidden="true">▶</span></button>`
            : ''
        }
      </div>
      ${v.title ? `<div class="def-video-title">${esc(v.title)}${v.duration ? ' · ' + esc(v.duration) : ''}</div>` : ''}
      ${v.caption ? `<figcaption>${esc(v.caption)}</figcaption>` : ''}
    </figure>`;
  }

  function teamCard(p) {
    let src = '';
    for (const [k, v] of Object.entries(TEAM_ASSETS)) {
      if (
        p.name &&
        (k.toLowerCase().includes((p.name.toLowerCase().split(' ').pop() || '')) ||
          p.name
            .toLowerCase()
            .split(' ')
            .some((w) => w.length > 3 && k.toLowerCase().includes(w.toLowerCase())))
      ) {
        src = mediaPath(v);
        break;
      }
    }
    if (!src && /sampriti/i.test(p.name || '') && TEAM_FEATURED) src = mediaPath(TEAM_FEATURED);
    const href = p.url || p.bio_url || '';
    const nameEl = href
      ? `<a class="team-name team-link" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(p.name)}</a>`
      : `<div class="team-name">${esc(p.name)}</div>`;
    const photo = src
      ? href
        ? `<a class="team-photo-link" href="${esc(href)}" target="_blank" rel="noopener noreferrer"><img src="${esc(src)}" alt="${esc(p.name)}" loading="lazy" /></a>`
        : `<img src="${esc(src)}" alt="${esc(p.name)}" loading="lazy" />`
      : '';
    const creds = p.credentials ? `<div class="team-creds">${esc(p.credentials)}</div>` : '';
    return `<div class="team-card"><div class="team-photo">${photo}</div>${nameEl}<div class="team-role">${esc(p.role || '')}</div>${creds}</div>`;
  }

  const NAV_LINKS = [
    { href: '#def-navier', label: 'Thesis' },
    { href: '#def-problem', label: 'Problem' },
    { href: '#def-platform', label: 'Control' },
    { href: '#def-flight', label: 'Flight' },
    { href: '#def-quanta-moment', label: 'Quanta' },
    { href: '#def-dual-use', label: 'Defense' },
    { href: '#def-team', label: 'Team' },
  ];

  function renderNav() {
    const links = NAV_LINKS.map(
      (l) => `<a class="inv-chapter" href="${esc(l.href)}">${esc(l.label)}</a>`
    ).join('');
    return `<nav class="inv-nav" aria-label="Chapters">
      <div class="inv-nav-inner">
        <div class="inv-brand">
          ${brandMark()}
          <div class="inv-brand-text">
            <span class="name">NAVIER</span>
            <span class="tag">Defense</span>
          </div>
        </div>
        <div class="inv-chapters">${links}</div>
        <div class="inv-progress" id="inv-progress"></div>
      </div>
    </nav>`;
  }

  function renderHero(s) {
    const videoSrc = mediaPath(s.background_video || 'assets/hero-loop.mp4');
    const poster = mediaPath(s.poster || 'assets/hero-poster.jpg');
    const film = s.film || {};
    const filmSrc = film.src ? mediaPath(film.src) : '';
    return `<header class="hero" id="def-hero" data-home="hero">
      <div class="hero-media">
        <img class="hero-poster" src="${esc(poster)}" alt="" width="1280" height="720" fetchpriority="high" />
        <video class="hero-video" muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="metadata" poster="${esc(poster)}" data-lazy-video>
          <source src="${esc(videoSrc)}" type="video/mp4" />
        </video>
      </div>
      <div class="hero-scrim" aria-hidden="true"></div>
      <div class="hero-content shell-prose">
        <h1 class="hero-headline">${esc(s.headline || 'OWN THE EDGE')}</h1>
        <p class="hero-subline">${esc(s.subline || '')}</p>
        <div class="hero-actions">
          ${
            filmSrc
              ? `<button type="button" class="btn btn-primary" data-film-src="${esc(filmSrc)}" data-film-poster="${esc(mediaPath(film.poster || ''))}">${esc(s.play_button_label || 'Watch the film')}</button>`
              : ''
          }
        </div>
      </div>
      <div class="scroll-cue" id="scroll-cue">${esc((s.scroll_cue && s.scroll_cue.label) || 'Scroll')}</div>
    </header>`;
  }

  const R = {
    'def-hero'(s) {
      return renderHero(s);
    },
    'def-navier'(s) {
      const paras = (s.thesis_paragraphs || [])
        .map(
          (p, i) =>
            `<p class="about-para ${i === 0 ? 'lead-para' : 'body-para'}">${esc(p)}</p>`
        )
        .join('');
      const media = s.media || {};
      const imgSrc = mediaPath(media.src || media.image || '');
      const hangar = imgSrc
        ? `<figure class="about-plate" data-reveal>
            <div class="about-plate-frame">
              <img src="${esc(imgSrc)}" alt="${esc(media.alt || '')}" loading="lazy" />
            </div>
          </figure>`
        : '';
      const bridge = s.body ? `<p class="def-closer section-inner">${esc(s.body)}</p>` : '';
      return `<section class="section-block stage-section about-stage ${hangar ? 'about-stage--split' : ''}" id="${esc(s.id)}" data-reveal>
        <div class="section-inner about-stage-inner">
          <div class="about-copy">
            ${s.kicker ? `<p class="about-kicker">${esc(s.kicker)}</p>` : ''}
            <h2 class="h2 about-title">${esc(s.title || 'Core Thesis')}</h2>
            <div class="about-prose">${paras}</div>
          </div>
          ${hangar}
        </div>
        ${bridge}
      </section>`;
    },
    'def-problem'(s) {
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${blocksHtml(s.blocks)}
        ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
      </section>`;
    },
    'def-plainview'(s) {
      const m = s.media || {};
      const src = m.src ? mediaPath(m.src) : '';
      const cinema = src
        ? `<div class="cinema-block" data-reveal>
            <div class="cinema"><div class="cinema-media cinema-media--photo">
              <img src="${esc(src)}" alt="${esc(m.alt || '')}" loading="lazy" />
            </div></div>
            ${m.caption ? `<div class="media-inner"><p class="cinema-cap">${esc(m.caption)}</p></div>` : ''}
          </div>`
        : '';
      return `<section class="section-block" id="${esc(s.id)}" data-reveal>
        <div class="shell-stage">${kicker(s)}<h2 class="h2">${esc(s.title || '')}</h2></div>
        ${cinema}
        <div class="shell-stage">
          ${blocksHtml(s.blocks)}
          ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
          ${s.source_line ? `<p class="def-fine">${esc(s.source_line)}</p>` : ''}
        </div>
      </section>`;
    },
    'def-platform'(s) {
      const schem =
        (s.media_pair || []).find(function (m) {
          return m && m.src && !String(m.src).endsWith('.mp4');
        }) || (s.media_pair || [])[0];
      const film = (s.videos || []).find(function (v) {
        return v.role === 'control-film' || v.embed_url;
      });
      const wire = schem && schem.src ? mediaPath(schem.src) : '';
      return `<section class="section-block stage-section control-stage" id="${esc(s.id)}" data-reveal>
        <div class="section-inner">
          ${kicker(s)}
          <h2 class="h2">${esc(s.title || '')}</h2>
          ${s.body ? `<p class="lead">${esc(s.body)}</p>` : ''}
        </div>
        <div class="control-sbs media-inner">
          <div class="control-diagram control-diagram-plate">
            ${
              wire
                ? `<img class="control-wire control-plate-img" src="${esc(wire)}" alt="${esc(schem.alt || 'Navier control schematic')}" loading="eager" fetchpriority="high" />`
                : ''
            }
          </div>
          <div class="control-video">
            ${film ? filmCard(film, film.poster, [film.title, film.duration].filter(Boolean).join(' · ')) : ''}
          </div>
        </div>
      </section>`;
    },
    'def-flight'(s) {
      const cards = (s.clips || [])
        .map(function (c) {
          const poster = mediaPath(c.poster || '');
          const src = mediaPath(c.asset || c.src || '');
          if (!src) return '';
          return `<div class="vcard vcard-loop" data-loop-src="${esc(src)}" data-clip="${esc(c.id || '')}">
            <span class="vcard-media">
              <video muted playsinline loop preload="auto" poster="${esc(poster)}" data-lazy-video ${reduceMotion ? '' : 'autoplay'}>
                <source src="${esc(src)}" type="video/mp4" />
              </video>
              <span class="play"><span>▶</span></span>
              ${c.duration ? `<span class="dur">${esc(c.duration)}</span>` : ''}
            </span>
            <span class="vcard-cap">${esc(c.caption || c.title || '')}</span>
          </div>`;
        })
        .join('');
      const stab = s.stabilization || {};
      const stabSrc = stab.src ? mediaPath(stab.src) : '';
      const stabHtml = stabSrc
        ? `<figure class="defense-loop-video media-inner" style="margin-top:20px">
            <div class="defense-video-frame defense-video-frame--lead">
              <video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="auto" data-lazy-video>
                <source src="${esc(stabSrc)}" type="video/mp4" />
              </video>
            </div>
            ${stab.caption ? `<figcaption>${esc(stab.caption)}</figcaption>` : ''}
          </figure>`
        : '';
      return `<section class="section-block" id="${esc(s.id)}" data-reveal data-home="proof.demo_grid">
        <div class="section-inner">
          ${kicker(s)}
          <h2 class="h2">${esc(s.title || '')}</h2>
          ${s.sub ? `<p class="demo-lede lead">${esc(s.sub)}</p>` : ''}
        </div>
        <div class="video-grid equal-grid media-inner">${cards}</div>
        ${stabHtml}
        ${s.closer ? `<p class="def-closer section-inner">${esc(s.closer)}</p>` : ''}
      </section>`;
    },
    'def-quanta-moment'(s) {
      const headline = titleCaseHeadline(s.headline || '');
      return `<section class="section-block chapter-break quanta-moment" id="${esc(s.id)}" data-reveal>
        <div class="section-inner">
          ${kicker(s)}
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${headline ? `<h2 class="h2 quanta-headline">${esc(headline)}</h2>` : ''}
          <div class="quanta-video-lead">
            ${filmCard(s.video, (s.video && s.video.poster) || 'assets/posters/QhiaYVgXMf0.jpg', s.video_label || '')}
          </div>
        </div>
      </section>`;
    },
    'def-quanta-stats'(s) {
      const camo = s.plate ? mediaPath(s.plate) : mediaPath('assets/deck/quanta-defense-camo.png');
      return `<section class="section-block shell-stage quanta-stats-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <div class="quanta-stats-compose ${camo ? 'has-plate' : ''}">
          ${camo ? `<div class="quanta-stats-plate"><img src="${esc(camo)}" alt="" loading="lazy" /></div>` : ''}
          <div class="quanta-stats-copy">
            ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            ${goldStats(s.stats)}
          </div>
        </div>
      </section>`;
    },
    'def-quanta-unlocks'(s) {
      const doors = (s.doors || [])
        .map(
          (d) =>
            `<div class="door"><div class="title">${esc(d.title)}</div><div class="detail">${esc(d.detail)}</div></div>`
        )
        .join('');
      const map = s.atlantic_map ? mediaPath(s.atlantic_map) : '';
      const line = (s.atlantic_run && (s.atlantic_run.line || s.atlantic_run)) || '';
      return `<section class="section-block shell-stage quanta-unlocks-stage" id="${esc(s.id)}" data-reveal>
        <div class="section-inner">
          ${kicker(s)}
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="doors doors-${(s.doors || []).length}">${doors}</div>
          <div class="atlantic-band">
            ${map ? `<figure class="plate atlantic-map-plate"><img src="${esc(map)}" alt="Atlantic run map" loading="lazy" /></figure>` : ''}
            ${line ? `<div class="atlantic">${esc(typeof line === 'string' ? line : '')}</div>` : ''}
          </div>
          ${s.closing_line ? `<p class="closing-line quanta-unlock-closing">${esc(s.closing_line)}</p>` : ''}
        </div>
      </section>`;
    },
    'def-dual-use'(s) {
      const media = s.media || {};
      const lead = media.lead_video || {};
      const leadSrc = mediaPath(lead.src || '');
      const photos = (media.photos || []).slice(0, 2);
      const secondary = media.secondary_videos || [];
      const rail = ((s.capability_rail && s.capability_rail.rows) || [])
        .map(
          (r) => `<div class="defense-spec">
            <div class="defense-spec-term">${esc(r.term || '')}</div>
            <div class="defense-spec-desc">${esc(r.desc || '')}</div>
          </div>`
        )
        .join('');
      const blocks = (s.blocks || [])
        .map(
          (b) =>
            `<div class="chip-card"><div class="t">${esc(b.title || '')}</div><div class="b">${nl(b.body || '')}</div></div>`
        )
        .join('');
      function quoteBlock(q, extraClass) {
        if (!q) return '';
        const text = q.quote || q.text || '';
        const cite = q.url
          ? `<a href="${esc(q.url)}" target="_blank" rel="noopener noreferrer">${esc(q.attribution || '')}</a>`
          : esc(q.attribution || '');
        return `<blockquote class="defense-quote${extraClass ? ' ' + extraClass : ''}">
            <p>${esc(text)}</p>
            <cite>${cite}</cite>
          </blockquote>`;
      }
      const press = quoteBlock(s.press_quote, 'defense-quote--press');
      const usmi = quoteBlock(s.pull_quote, '');
      const photoHtml = photos
        .map(function (ph) {
          const raw = ph.src || ph;
          const src = mediaPath(raw);
          if (!src) return '';
          const isSof = /sofweek|sof week/i.test(String(raw) + (ph.caption || ''));
          return `<figure class="defense-photo${isSof ? ' defense-photo--sof' : ''}">
            <div class="defense-photo-frame"><img src="${esc(src)}" alt="${esc(ph.caption || '')}" loading="lazy" /></div>
            ${ph.caption ? `<figcaption>${esc(ph.caption)}</figcaption>` : ''}
          </figure>`;
        })
        .join('');
      const secondaryHtml = secondary
        .map(function (v) {
          const src = mediaPath(v.src);
          if (!src) return '';
          return `<figure class="defense-loop-video">
            <div class="defense-video-frame">
              <video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="auto" data-lazy-video>
                <source src="${esc(src)}" type="video/mp4" />
              </video>
            </div>
            ${v.caption ? `<figcaption>${esc(v.caption)}</figcaption>` : ''}
          </figure>`;
        })
        .join('');
      const quietProof =
        [press, usmi].filter(Boolean).join('') +
        (s.deployment_line ? `<p class="defense-deploy">${esc(s.deployment_line)}</p>` : '');
      return `<section class="section-block dual-use-stage" id="${esc(s.id)}" data-reveal data-home="gtm.defense">
        <div class="section-inner">
          ${kicker(s)}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${s.intro ? `<p class="dual-use-intro">${esc(s.intro)}</p>` : ''}

          <div class="defense-beat defense-beat--proof">
            <p class="sublabel">PROOF</p>
            <div class="defense-media-band">
              ${
                leadSrc
                  ? `<figure class="defense-lead-video">
                <div class="defense-video-frame defense-video-frame--lead">
                  <video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="auto" data-lazy-video>
                    <source src="${esc(leadSrc)}" type="video/mp4" />
                  </video>
                </div>
                ${lead.caption ? `<figcaption>${esc(lead.caption)}</figcaption>` : ''}
              </figure>`
                  : ''
              }
              ${photoHtml ? `<div class="defense-sbs">${photoHtml}</div>` : ''}
              ${secondaryHtml ? `<div class="defense-secondary">${secondaryHtml}</div>` : ''}
            </div>
            ${quietProof ? `<div class="defense-quiet">${quietProof}</div>` : ''}
          </div>

          <div class="defense-beat defense-beat--platform">
            <p class="sublabel">PLATFORM</p>
            ${s.thesis_line ? `<p class="defense-thesis">${esc(s.thesis_line)}</p>` : ''}
            ${rail ? `<div class="defense-specs">${rail}</div>` : ''}
            ${blocks ? `<div class="dual-use-blocks">${blocks}</div>` : ''}
          </div>

          ${
            s.sub_line || s.fine_print
              ? `<div class="defense-beat defense-beat--why">
            <p class="sublabel">DUAL-USE</p>
            ${s.sub_line ? `<p class="defense-why-lead">${esc(s.sub_line)}</p>` : ''}
            ${s.fine_print ? `<p class="defense-budgets muted">${esc(s.fine_print)}</p>` : ''}
          </div>`
              : ''
          }
        </div>
      </section>`;
    },
    'def-field'(s) {
      const t = s.table || {};
      const cols = t.columns || [];
      const rows = t.rows || [];
      const thead = `<tr>${cols.map((c) => `<th>${esc(c)}</th>`).join('')}</tr>`;
      const tbody = rows.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('');
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
        <div class="def-table-wrap"><table class="def-table"><thead>${thead}</thead><tbody>${tbody}</tbody></table></div>
        ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
      </section>`;
    },
    'def-family'(s) {
      const ladder = `<div class="def-ladder">${(s.ladder || [])
        .map((item) => {
          const name = item.name || item.vessel || '';
          return `<div class="def-ladder-item">
          <img src="${esc(mediaPath(item.image))}" alt="${esc(name)}" loading="lazy" />
          <div class="meta">
            <div class="v">${esc(name)}${item.length_class ? ' · ' + esc(item.length_class) : ''}</div>
            ${item.status ? `<div class="status">${esc(item.status)}</div>` : ''}
            <div class="l">${esc(item.defense_lens || item.line || '')}</div>
          </div>
        </div>`;
        })
        .join('')}</div>`;
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${s.body ? `<p>${esc(s.body)}</p>` : ''}
        ${ladder}
        ${s.media_extra ? plate(s.media_extra.src, s.media_extra.alt) : ''}
      </section>`;
    },
    'def-team'(s) {
      const people = TEAM.slice();
      const sam = people.find((p) => /sampriti/i.test(p.name || ''));
      const others = people.filter((p) => p !== sam);
      const cta = s.cta || {};
      return `<section class="section-block team-section shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        <div class="team-layout">
          ${sam ? `<div class="team-featured">${teamCard(sam)}</div>` : ''}
          <div class="team-grid">${others.map(teamCard).join('')}</div>
        </div>
        <div class="def-cta">
          <p>${esc(cta.line || '')}</p>
          ${cta.email ? `<p><a href="mailto:${esc(cta.email)}">${esc(cta.email)}</a></p>` : ''}
        </div>
        ${plate('assets/deck/goldenhour-bow.jpg', 'Navier vessel bow at golden hour')}
      </section>`;
    },
  };

  function renderSection(s) {
    const fn = R[s.id] || (s.type === 'defense-panel' ? R['def-dual-use'] : null);
    if (fn) return fn(s);
    return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
      ${kicker(s)}
      ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
    </section>`;
  }

  const app = document.getElementById('app');
  app.innerHTML = [
    renderNav(),
    ...(D.sections || []).map(renderSection),
    `<footer class="def-footer shell-stage"><p>${esc(D.footer || '')}</p></footer>`,
    `<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video">
      <div class="lightbox-inner">
        <button type="button" class="lightbox-close" id="lb-close" aria-label="Close">×</button>
        <div id="lb-frame"></div>
      </div>
    </div>`,
  ].join('\n');

  /* Lightbox */
  function openLb(html) {
    const frame = $('#lb-frame');
    const box = $('#lightbox');
    if (!frame || !box) return;
    frame.innerHTML = html;
    box.classList.add('open');
  }
  function closeLb() {
    const box = $('#lightbox');
    const frame = $('#lb-frame');
    if (box) box.classList.remove('open');
    if (frame) frame.innerHTML = '';
  }
  const lbClose = $('#lb-close');
  if (lbClose) lbClose.addEventListener('click', closeLb);
  const lb = $('#lightbox');
  if (lb) {
    lb.addEventListener('click', function (e) {
      if (e.target.id === 'lightbox') closeLb();
    });
  }

  document.querySelectorAll('[data-film-src]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      const src = el.getAttribute('data-film-src');
      if (!src) return;
      openLb(
        `<video controls autoplay playsinline style="width:100%;height:100%;background:#000"><source src="${esc(src)}" type="video/mp4" /></video>`
      );
    });
  });

  document.querySelectorAll('[data-yt-embed]').forEach(function (el) {
    const url = el.getAttribute('data-yt-embed');
    if (!url) return;
    function playYt(e) {
      if (e) e.preventDefault();
      if (el.classList.contains('film-card')) {
        openLb(
          `<iframe src="${esc(url)}?autoplay=1&rel=0" title="video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>`
        );
        return;
      }
      const frame = el.querySelector('.def-video-frame');
      if (!frame) return;
      frame.innerHTML = `<iframe src="${esc(url)}?autoplay=1&rel=0" title="video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>`;
    }
    if (el.classList.contains('film-card')) el.addEventListener('click', playYt);
    else {
      const btn = el.querySelector('.film-play');
      if (btn) btn.addEventListener('click', playYt);
    }
  });

  /* Demo loops: click toggles sound */
  document.querySelectorAll('.vcard-loop').forEach(function (card) {
    card.addEventListener('click', function () {
      const v = card.querySelector('video');
      if (!v) return;
      v.muted = !v.muted;
      card.classList.toggle('is-audible', !v.muted);
      v.play().catch(function () {});
    });
  });

  document.querySelectorAll('.def-video-tile, [data-def-film]').forEach(function (wrap) {
    const btn = wrap.querySelector('.film-play');
    const video = wrap.querySelector('video');
    if (btn && video) {
      btn.addEventListener('click', function () {
        if (video.hasAttribute('data-click-sound-film')) video.muted = false;
        video.controls = true;
        video.play().catch(function () {});
        btn.remove();
      });
    }
  });

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          const v = en.target;
          if (!(v instanceof HTMLVideoElement) || reduceMotion) return;
          if (v.hasAttribute('data-click-sound-film') || v.hasAttribute('data-click-play')) return;
          if (en.isIntersecting) v.play().catch(function () {});
          else v.pause();
        });
      },
      { threshold: 0.25 }
    );
    document.querySelectorAll('video[data-lazy-video], .hero-video').forEach(function (v) {
      io.observe(v);
    });
  }

  /* Scroll cue */
  const cue = $('#scroll-cue');
  if (cue) {
    window.addEventListener(
      'scroll',
      function () {
        if (window.scrollY > 40) cue.style.opacity = '0';
      },
      { passive: true }
    );
  }
})();
