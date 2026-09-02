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

  function teamCard(p, featured) {
    let src = '';
    const name = p.name || '';
    for (const [k, v] of Object.entries(TEAM_ASSETS)) {
      if (
        name &&
        (k.toLowerCase().includes(name.toLowerCase().split(' ')[0].toLowerCase()) ||
          name
            .toLowerCase()
            .split(' ')
            .some((w) => w.length > 3 && k.toLowerCase().includes(w.toLowerCase())))
      ) {
        src = mediaPath(v);
        break;
      }
    }
    if (!src && /sampriti/i.test(name) && TEAM_FEATURED) src = mediaPath(TEAM_FEATURED);
    // Invest-style filename fallback (team-firstname-lastname.png)
    if (!src && name) {
      if (/leclair/i.test(name)) src = mediaPath('assets/deck/team-ted-leclair.png');
      else if (/cederholm/i.test(name)) src = mediaPath('assets/deck/team-michael-cederholm.png');
      else if (/sampriti/i.test(name)) src = mediaPath('assets/deck/team-sampriti-bhattacharyya.png');
      else if (/kenneth|jensen/i.test(name)) src = mediaPath('assets/deck/team-kenneth-jensen.png');
      else if (/dan dorsch|dorsch/i.test(name)) src = mediaPath('assets/deck/team-dan-dorsch.png');
      else if (/dotan|feldman/i.test(name)) src = mediaPath('assets/deck/team-dotan-feldman.png');
      else if (/bieker/i.test(name)) src = mediaPath('assets/deck/team-paul-bieker.png');
      else if (/jaideep|dhanoa/i.test(name)) src = mediaPath('assets/deck/team-jaideep-dhanoa.png');
      else {
        const slug = name
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-|-$/g, '');
        src = mediaPath(`assets/deck/team-${slug}.png`);
      }
    }
    const href = p.url || p.bio_url || '';
    const nameEl = href
      ? `<a class="team-name team-link" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(name)}</a>`
      : `<div class="team-name">${esc(name)}</div>`;
    const photo = src
      ? href
        ? `<a class="team-photo-link" href="${esc(href)}" target="_blank" rel="noopener noreferrer"><img src="${esc(src)}" alt="${esc(name)}" loading="lazy" /></a>`
        : `<img src="${esc(src)}" alt="${esc(name)}" loading="lazy" />`
      : '';
    const creds = p.credentials ? `<div class="team-creds">${esc(p.credentials)}</div>` : '';
    if (featured) {
      return `<div class="team-featured-inner">
        <div class="team-photo lg">${photo}</div>
        ${nameEl}
        <div class="team-role">${esc(p.role || '')}</div>
        ${creds}
      </div>`;
    }
    return `<div class="team-card"><div class="team-photo">${photo}</div>${nameEl}<div class="team-role">${esc(p.role || '')}</div>${creds}</div>`;
  }

  // Scroll-spy chapters (invest-style progress + active chip)
  const NAV_LINKS = [
    { id: 'def-navier', label: 'Who we are' },
    { id: 'def-plainview', label: 'Why now' },
    { id: 'def-platform', label: 'Control' },
    { id: 'def-flight', label: 'Flight' },
    { id: 'def-quanta-moment', label: 'Quanta' },
    { id: 'def-dual-use', label: 'Proof' },
    { id: 'def-family', label: 'Fleet' },
    { id: 'def-team', label: 'Team' },
    { id: 'def-close', label: 'Close' },
  ];

  function renderNav() {
    const links = NAV_LINKS.map(
      (l) =>
        `<a class="inv-chapter" href="#${esc(l.id)}" data-nav="${esc(l.id)}">${esc(l.label)}</a>`
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
      // v4 defense-first opener: body + beats + doctrine (invest thesis paragraphs retired on this route)
      const paras = (s.thesis_paragraphs || [])
        .map(
          (p, i) =>
            `<p class="about-para ${i === 0 ? 'lead-para' : 'body-para'}">${esc(p)}</p>`
        )
        .join('');
      const bodyLead = s.body
        ? `<p class="about-para lead-para def-opener-body">${esc(s.body)}</p>`
        : '';
      const beats = (s.beats || [])
        .map(
          (b) => `<div class="defense-spec def-opener-beat">
            <div class="defense-spec-term">${esc(b.head || b.term || '')}</div>
            <div class="defense-spec-desc">${esc(b.body || b.desc || '')}</div>
          </div>`
        )
        .join('');
      const doctrine = s.doctrine_link && s.doctrine_link.url
        ? `<a class="def-doctrine-chip" href="${esc(s.doctrine_link.url)}" target="_blank" rel="noopener noreferrer">${esc(s.doctrine_link.label || 'Read the Navier Doctrine →')}</a>`
        : '';
      const media = s.media || {};
      const imgSrc = mediaPath(media.src || media.image || '');
      const hangar = imgSrc
        ? `<figure class="about-plate" data-reveal>
            <div class="about-plate-frame">
              <img src="${esc(imgSrc)}" alt="${esc(media.alt || '')}" loading="lazy" />
            </div>
          </figure>`
        : '';
      // Legacy ONE CORE bridge only when beats are absent (pre-v4 contracts)
      const bridge =
        !beats && s.body && paras
          ? `<div class="thesis-bridge">
            <p class="thesis-bridge-label">ONE CORE</p>
            <p class="thesis-bridge-body">${esc(s.body)}</p>
          </div>`
          : '';
      const film = s.film || {};
      const filmInner = film.src
        ? videoTile(
            Object.assign({}, film, { behavior: film.behavior || 'click-to-play with sound' }),
            { wide: false, withSound: true }
          )
        : '';
      // v4: intro|hangar, then beats|film (film no longer hangs alone below with empty stage)
      if (beats && filmInner) {
        return `<section class="section-block stage-section about-stage about-stage--opener" id="${esc(s.id)}" data-reveal>
          <div class="section-inner about-opener">
            <div class="about-opener-top">
              <div class="about-opener-intro">
                ${s.kicker ? `<p class="about-kicker">${esc(s.kicker)}</p>` : ''}
                <h2 class="h2 about-title">${esc(s.title || 'An American Maritime Company.')}</h2>
                ${bodyLead}
              </div>
              ${hangar ? `<div class="about-opener-hangar">${hangar}</div>` : ''}
            </div>
            <div class="about-opener-split">
              <div class="about-opener-beats-col">
                <div class="defense-specs def-opener-beats">${beats}</div>
                ${s.beats_source_line ? `<p class="def-fine def-beats-source">${esc(s.beats_source_line)}</p>` : ''}
                ${doctrine ? `<div class="def-doctrine-wrap">${doctrine}</div>` : ''}
              </div>
              <div class="about-opener-film def-film-wrap def-film-wrap--beside" data-def-film>
                ${filmInner}
              </div>
            </div>
          </div>
        </section>`;
      }
      const beatsBlock = beats
        ? `<div class="defense-specs def-opener-beats">${beats}</div>
           ${s.beats_source_line ? `<p class="def-fine def-beats-source">${esc(s.beats_source_line)}</p>` : ''}
           ${doctrine ? `<div class="def-doctrine-wrap">${doctrine}</div>` : ''}`
        : '';
      const filmHtml = filmInner
        ? `<div class="def-film-wrap media-inner" data-def-film>${filmInner}</div>`
        : '';
      const prose = beats ? `${bodyLead}${beatsBlock}` : `${paras}${doctrine}`;
      return `<section class="section-block stage-section about-stage ${hangar ? 'about-stage--split' : ''}" id="${esc(s.id)}" data-reveal>
        <div class="section-inner about-stage-inner">
          <div class="about-copy">
            ${s.kicker ? `<p class="about-kicker">${esc(s.kicker)}</p>` : ''}
            <h2 class="h2 about-title">${esc(s.title || 'An American Maritime Company.')}</h2>
            <div class="about-prose">${prose}</div>
          </div>
          ${hangar}
          ${bridge}
        </div>
        ${filmHtml}
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
        <div class="shell-stage">${kicker(s)}<h2 class="h2 plainview-title">${esc(s.title || '')}</h2></div>
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
      const vids = s.videos || [];
      const film = vids.find(function (v) {
        return v.role === 'control-film' || v.embed_url;
      });
      const loops = vids.filter(function (v) {
        return v !== film && v.src && /autoplay/i.test(v.behavior || '');
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
        ${
          loops.length
            ? `<div class="def-video-row media-inner" style="grid-template-columns:1fr;max-width:960px;margin:20px auto 0">${loops
                .map(function (v) {
                  return videoTile(v);
                })
                .join('')}</div>`
            : ''
        }
      </section>`;
    },
    'def-flight'(s) {
      // Exactly three equal tiles — no fourth floating video
      const clips = (s.clips || s.videos || []).slice(0, 3);
      const cards = clips
        .map(function (c) {
          const poster = mediaPath(c.poster || '');
          const src = mediaPath(c.asset || c.src || '');
          if (!src && c.embed_url) {
            // fallback click tile if no local asset
            return videoTile(c, { withSound: true });
          }
          if (!src) return '';
          return `<div class="vcard vcard-loop" data-loop-src="${esc(src)}" data-clip="${esc(c.id || '')}">
            <span class="vcard-media">
              <video muted playsinline loop preload="auto" poster="${esc(poster)}" data-lazy-video ${reduceMotion ? '' : 'autoplay'}>
                <source src="${esc(src)}" type="video/mp4" />
              </video>
              <span class="play"><span>▶</span></span>
              ${c.duration ? `<span class="dur">${esc(c.duration)}</span>` : ''}
            </span>
            ${c.title ? `<span class="vcard-title">${esc(c.title)}</span>` : ''}
            <span class="vcard-cap">${esc(c.caption || '')}</span>
          </div>`;
        })
        .join('');
      return `<section class="section-block" id="${esc(s.id)}" data-reveal data-home="proof.demo_grid">
        <div class="section-inner">
          ${kicker(s)}
          <h2 class="h2">${esc(s.title || '')}</h2>
          ${s.sub ? `<p class="demo-lede lead">${esc(s.sub)}</p>` : ''}
        </div>
        <div class="video-grid equal-grid media-inner" style="max-width:1100px;margin-left:auto;margin-right:auto">${cards}</div>
        ${s.closer ? `<p class="def-closer section-inner">${esc(s.closer)}</p>` : ''}
      </section>`;
    },
    'def-quanta-moment'(s) {
      // Short capability headline; belief_line as founder pull-quote (not an orphan italic)
      const headline = s.headline || '';
      const beliefCite = s.belief_attribution || s.video_label || '';
      const beliefQuote = s.belief_line
        ? `<blockquote class="defense-quote def-belief-quote">
            <p>${esc(s.belief_line)}</p>
            ${beliefCite ? `<cite>${esc(beliefCite)}</cite>` : ''}
          </blockquote>`
        : '';
      return `<section class="section-block chapter-break quanta-moment" id="${esc(s.id)}" data-reveal>
        <div class="section-inner">
          ${kicker(s)}
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${headline ? `<h2 class="h2 quanta-headline">${esc(headline)}</h2>` : ''}
          <div class="quanta-video-lead">
            ${filmCard(s.video, (s.video && s.video.poster) || 'assets/posters/QhiaYVgXMf0.jpg', '')}
          </div>
          ${beliefQuote}
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
      const post = s.public_post || {};
      const postLink =
        post.url && post.label
          ? `<p class="defense-public-post"><a href="${esc(post.url)}" target="_blank" rel="noopener noreferrer">${esc(post.label)}</a></p>`
          : '';
      const secondaryHtml = secondary
        .map(function (v) {
          const src = mediaPath(v.src);
          if (!src) return '';
          const isTe = /te263|te-263|te 26-3/i.test(String(v.src) + (v.caption || ''));
          return `<figure class="defense-loop-video${isTe ? ' defense-loop-video--te' : ''}">
            <div class="defense-video-frame">
              <video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="auto" data-lazy-video>
                <source src="${esc(src)}" type="video/mp4" />
              </video>
            </div>
            ${v.caption ? `<figcaption>${esc(v.caption)}</figcaption>` : ''}
            ${isTe ? postLink : ''}
          </figure>`;
        })
        .join('');
      // PLATFORM beat (thesis / blocks / mission renders) now lives under def-family
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

          ${
            s.resilience_thesis || s.sub_line || s.fine_print
              ? `<div class="defense-beat defense-beat--why">
            <p class="sublabel">DUAL-USE</p>
            ${
              s.resilience_thesis
                ? `<div class="def-resilience">
              ${s.resilience_thesis.kicker ? `<p class="def-resilience-kicker">${esc(s.resilience_thesis.kicker)}</p>` : ''}
              ${s.resilience_thesis.title ? `<h3 class="def-resilience-title">${esc(s.resilience_thesis.title)}</h3>` : ''}
              ${s.resilience_thesis.body ? `<p class="def-resilience-body">${esc(s.resilience_thesis.body)}</p>` : ''}
              ${s.resilience_thesis.support_line ? `<p class="def-resilience-support">${esc(s.resilience_thesis.support_line)}</p>` : ''}
            </div>`
                : ''
            }
            ${s.sub_line ? `<p class="defense-why-lead">${esc(s.sub_line)}</p>` : ''}
            ${s.fine_print ? `<p class="defense-budgets muted">${esc(s.fine_print)}</p>` : ''}
          </div>`
              : ''
          }
        </div>
      </section>`;
    },
    'def-field'(s) {
      // Invest comparison-table port
      const cols = s.columns || (s.table && s.table.columns) || [];
      const rows = s.rows || (s.table && s.table.rows) || [];
      const colNames = cols.map(function (c) {
        return typeof c === 'string' ? c : c.name || '';
      });
      const head = `<tr>${colNames
        .map(function (name, i) {
          const hi = /navier|quanta/i.test(name);
          return `<th class="${hi ? 'hi' : ''}${i === 0 ? ' row-label-th' : ''}">${esc(name || s.vessel_type_label || '')}</th>`;
        })
        .join('')}</tr>`;
      let body = '';
      if (s.vessel_type_row && s.vessel_type_row.length) {
        body += `<tr class="vessel-type-row">${s.vessel_type_row
          .map(function (cell, i) {
            return `<td class="${i === 1 ? 'hi' : ''}${i === 0 ? ' row-label' : ''}">${esc(cell)}</td>`;
          })
          .join('')}</tr>`;
      }
      body += rows
        .map(function (row) {
          return `<tr>${(row || [])
            .map(function (cell, i) {
              return `<td class="${i === 1 ? 'hi' : ''}${i === 0 ? ' row-label' : ''}">${esc(cell)}</td>`;
            })
            .join('')}</tr>`;
        })
        .join('');
      const takeaway = s.takeaway || s.closing_line || s.closer || '';
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal data-home="gtm.competitive">
        <div class="section-inner">
          ${kicker(s)}
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          <h2 class="h2">${esc(s.title || '')}</h2>
          ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
          <div class="table-wrap"><table class="cmp cmp-s17"><thead>${head}</thead><tbody>${body}</tbody></table></div>
          ${takeaway ? `<p class="closing-line takeaway-line">${esc(takeaway)}</p>` : ''}
          ${s.explainer ? `<p class="explainer">${esc(s.explainer)}</p>` : ''}
          ${s.source_note ? `<p class="muted source-note">${esc(s.source_note)}</p>` : ''}
        </div>
      </section>`;
    },
    'def-family'(s) {
      const g = s.gmvp_intro || {};
      const wire = g.wireframe_image ? mediaPath(g.wireframe_image) : '';
      const layers = (g.layers || [])
        .map(function (l, i) {
          return `<div class="gmvp-layer" data-layer="${i}">
            <div class="gmvp-layer-name">${esc(l.label || l.name || '')}</div>
            ${l.name && l.label ? `<div class="gmvp-layer-role">${esc(l.name)}</div>` : ''}
            ${l.note ? `<div class="gmvp-layer-detail">${esc(l.note)}</div>` : ''}
          </div>`;
        })
        .join('');
      const gmvp = g.title
        ? `<div class="gmvp-compose" style="margin:18px 0 28px">
            <div class="gmvp-wire">${wire ? `<img src="${esc(wire)}" alt="" loading="lazy" class="gmvp-wire-img" />` : ''}</div>
            <div class="gmvp-layers">
              <p class="eyebrow">THREE LAYERS</p>
              ${g.body ? `<p class="lead" style="margin-bottom:12px">${esc(g.body)}</p>` : ''}
              ${layers}
            </div>
          </div>`
        : '';
      const ladder = `<div class="def-ladder">${(s.ladder || [])
        .map((item) => {
          const name = item.name || item.vessel || '';
          // Crop rule: plate + object-fit contain — vessel must stay fully visible at all widths
          return `<div class="def-ladder-item">
          <div class="def-ladder-plate">
            <img src="${esc(mediaPath(item.image))}" alt="${esc(name)}" loading="lazy" />
          </div>
          <div class="meta">
            <div class="v">${esc(name)}${item.length_class ? ' · ' + esc(item.length_class) : ''}</div>
            ${item.status ? `<div class="status">${esc(item.status)}</div>` : ''}
            <div class="l">${esc(item.defense_lens || item.line || '')}</div>
          </div>
        </div>`;
        })
        .join('')}</div>`;
      const mg = s.morpheus_gallery || {};
      const morphImgs = mg.images || [];
      const morphCard = function (it) {
        const src = mediaPath(it.src);
        if (!src) return '';
        const cap = it.caption || '';
        const badge = it.badge || 'CONCEPT RENDER';
        return `<figure class="def-morph-card">
          <div class="def-morph-frame">
            <span class="def-morph-badge">${esc(badge)}</span>
            <img src="${esc(src)}" alt="${esc(it.alt || cap)}" loading="lazy" />
          </div>
          ${cap ? `<figcaption>${esc(cap)}</figcaption>` : ''}
        </figure>`;
      };
      const morphHtml = morphImgs.length
        ? `<div class="def-morph" data-reveal>
            <p class="sublabel">${esc(mg.kicker || 'SHIP SCALE')}</p>
            ${mg.title ? `<h3 class="h3">${esc(mg.title)}</h3>` : ''}
            ${mg.body ? `<p class="lead">${esc(mg.body)}</p>` : ''}
            <div class="def-morph-grid">${morphImgs.map(function (im) { return morphCard(im); }).join('')}</div>
          </div>`
        : '';
      // PLATFORM beat lives under Family (moved from dual-use)
      const blocks = (s.blocks || [])
        .map(
          (b) =>
            `<div class="chip-card"><div class="t">${esc(b.title || '')}</div><div class="b">${nl(b.body || '')}</div></div>`
        )
        .join('');
      const mr = s.mission_renders || {};
      const missionItems = (mr.items || [])
        .map(function (it) {
          const src = mediaPath(it.src);
          if (!src) return '';
          let cap = it.caption || '';
          if (cap && !/concept render/i.test(cap)) cap = cap + ' · CONCEPT RENDER';
          return `<figure class="def-mission-card">
            <div class="def-mission-frame"><img src="${esc(src)}" alt="${esc(it.alt || cap)}" loading="lazy" /></div>
            ${cap ? `<figcaption>${esc(cap)}</figcaption>` : ''}
          </figure>`;
        })
        .join('');
      const missionHtml = missionItems
        ? `<div class="def-mission-rail" data-reveal>
            <p class="sublabel">${esc(mr.kicker || 'MISSION CONFIGURATIONS')}</p>
            <p class="def-mission-note">Concept renders</p>
            <div class="def-mission-grid">${missionItems}</div>
          </div>`
        : '';
      const platformBeat =
        s.thesis_line || s.integrator_line || blocks || missionHtml
          ? `<div class="defense-beat defense-beat--platform" style="margin-top:28px">
            <p class="sublabel">PLATFORM</p>
            ${s.thesis_line ? `<p class="defense-thesis">${esc(s.thesis_line)}</p>` : ''}
            ${s.integrator_line ? `<p class="def-integrator-line">${esc(s.integrator_line)}</p>` : ''}
            ${blocks ? `<div class="dual-use-blocks">${blocks}</div>` : ''}
            ${missionHtml}
          </div>`
          : '';
      return `<section class="section-block shell-stage gmvp-stage" id="${esc(s.id)}" data-reveal>
        <div class="section-inner">
          ${kicker(s)}
          <h2 class="h2">${esc(s.title || '')}</h2>
          ${s.body ? `<p class="lead">${esc(s.body)}</p>` : ''}
          ${g.title ? `<h3 class="h3" style="margin-top:8px">${esc(g.title)}</h3>` : ''}
          ${gmvp}
          ${ladder}
          ${morphHtml}
          ${platformBeat}
        </div>
      </section>`;
    },
    'def-team'(s) {
      const people = TEAM.slice();
      const sam = people.find((p) => /sampriti/i.test(p.name || ''));
      const others = people.filter((p) => p !== sam);
      // Match other chapters: section-inner width (not full-bleed shell-stage)
      return `<section class="section-block team-section" id="${esc(s.id)}" data-reveal>
        <div class="section-inner">
          ${kicker(s)}
          <h2 class="h2">${esc(s.title || '')}</h2>
          <div class="team-layout">
            ${sam ? `<div class="team-featured">${teamCard(sam, true)}</div>` : ''}
            <div class="team-grid">${others.map(function (p) { return teamCard(p, false); }).join('')}</div>
          </div>
        </div>
      </section>`;
    },
    'def-close'(s) {
      const h = s.hero || {};
      const vsrc = mediaPath(h.background_video || 'assets/closing-loop.mp4');
      const poster = mediaPath(h.poster || 'assets/hero-poster.jpg');
      const cta = h.cta || {};
      const gd = s.go_deeper || {};
      const items = (gd.items || [])
        .map(function (it) {
          if (it.type === 'video' || it.embed_url) {
            return filmCard(
              {
                embed_url: it.embed_url,
                youtube_id: it.youtube_id,
                poster: it.poster,
                title: it.caption,
              },
              it.poster || (it.youtube_id ? `assets/posters/${it.youtube_id}.jpg` : ''),
              it.caption || ''
            );
          }
          if (it.src) {
            return `<figure class="go-deeper-plate">
              <div class="go-deeper-plate-frame"><img src="${esc(mediaPath(it.src))}" alt="" loading="lazy" /></div>
              ${it.caption ? `<figcaption class="go-deeper-plate-cap">${esc(it.caption)}</figcaption>` : ''}
            </figure>`;
          }
          return '';
        })
        .join('');
      return `<section class="section-block" id="${esc(s.id)}" data-reveal>
        <section class="finale" id="finale">
          <div class="finale-media">
            <video muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="metadata" poster="${esc(poster)}" data-lazy-video>
              <source src="${esc(vsrc)}" type="video/mp4" />
            </video>
          </div>
          <div class="finale-scrim" aria-hidden="true"></div>
          <div class="finale-inner">
            ${h.line ? `<p class="h">${esc(h.line)}</p>` : ''}
            <p class="mark">${esc(h.title || 'OWN THE LITTORAL')}</p>
            ${
              cta.href
                ? `<a class="btn btn-primary" href="${esc(cta.href)}">${esc(cta.label || 'Arrange a briefing')}</a>`
                : ''
            }
          </div>
        </section>
        <section class="go-deeper" id="go-deeper">
          <div class="shell-stage go-deeper-inner">
            <p class="chapter-label">${esc(gd.kicker || 'Go deeper')}</p>
            <div class="go-deeper-media">${items}</div>
          </div>
        </section>
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

  /* Scroll cue + invest-style chapter spy / progress bar */
  const cue = $('#scroll-cue');
  const progress = $('#inv-progress');
  const navLinks = [...document.querySelectorAll('[data-nav]')];
  const chapterIds = NAV_LINKS.map(function (l) {
    return l.id;
  });

  function jumpToId(id, updateHash) {
    const el = id && document.getElementById(id);
    if (!el) return false;
    const root = document.documentElement;
    const prev = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto';
    el.scrollIntoView();
    root.style.scrollBehavior = prev;
    if (updateHash && history.replaceState) history.replaceState(null, '', '#' + id);
    onScrollNav();
    return true;
  }

  function onScrollNav() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    if (cue && window.scrollY > 80) cue.style.opacity = '0';
    const hv = document.querySelector('.hero-video');
    if (hv && window.scrollY > window.innerHeight * 0.85) {
      try {
        hv.pause();
      } catch (_) {}
    }
    const thresh = 100;
    let active = chapterIds[0];
    for (let i = 0; i < chapterIds.length; i++) {
      const el = document.getElementById(chapterIds[i]);
      if (el && el.getBoundingClientRect().top <= thresh) active = chapterIds[i];
    }
    navLinks.forEach(function (a) {
      const on = a.getAttribute('data-nav') === active;
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }

  navLinks.forEach(function (a) {
    a.addEventListener('click', function (e) {
      const id = (a.getAttribute('href') || '').replace(/^#/, '');
      if (!id) return;
      e.preventDefault();
      jumpToId(id, true);
    });
  });

  window.addEventListener('scroll', onScrollNav, { passive: true });
  onScrollNav();
  if (location.hash) {
    requestAnimationFrame(function () {
      jumpToId(location.hash.slice(1), false);
    });
  }
})();
