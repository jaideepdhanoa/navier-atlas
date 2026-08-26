/* /story v3 — watch reel */
(function () {
  'use strict';
  const D = window.STORY_DATA;
  if (!D || !D.story) {
    console.error('[story] STORY_DATA missing');
    return;
  }

  const site = D.site || {};
  const story = D.story;
  const assets = D.assets || {};
  const badges = D.badges || {};
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData =
    (navigator.connection && navigator.connection.saveData) ||
    /iPhone|iPad|Android/i.test(navigator.userAgent);

  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function brandMark() {
    return `<span class="story-brand-mark" aria-hidden="true"><svg viewBox="9.5 9.5 160 160" fill="currentColor"><path d="M130.16 117.84 L120.18 135.12 A0.39 0.39 0 0 1 119.50 135.11 L68.16 44.06 A0.39 0.39 0 0 1 68.50 43.48 L88.22 43.48 A0.39 0.39 0 0 1 88.56 43.68 L130.16 117.46 A0.39 0.39 0 0 1 130.16 117.84 Z"/><path d="M132.68 111.67 L122.61 93.82 A0.55 0.55 0 0 1 122.62 93.28 L150.95 44.21 A0.55 0.55 0 0 1 151.90 44.21 L161.97 62.07 A0.55 0.55 0 0 1 161.96 62.61 L133.63 111.68 A0.55 0.55 0 0 1 132.68 111.67 Z"/><path d="M110.65 135.52 L90.76 135.52 A0.33 0.33 0 0 1 90.48 135.35 L48.97 61.75 A0.33 0.33 0 0 1 48.97 61.43 L59.03 44.00 A0.33 0.33 0 0 1 59.60 44.00 L110.93 135.03 A0.33 0.33 0 0 1 110.65 135.52 Z"/><path d="M26.53 134.96 L17.16 118.32 A0.67 0.67 0 0 1 17.16 117.66 L45.57 68.46 A0.67 0.67 0 0 1 46.74 68.46 L56.11 85.09 A0.67 0.67 0 0 1 56.11 85.75 L27.70 134.96 A0.67 0.67 0 0 1 26.53 134.96 Z"/></svg></span>`;
  }

  function track(event, payload) {
    const props = Object.assign({}, payload || {}, readUtms());
    try {
      if (window.va && typeof window.va === 'function') {
        window.va('event', Object.assign({ name: event }, props));
      }
    } catch (_) {}
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: event }, props));
    } catch (_) {}
  }

  function readUtms() {
    const out = {};
    try {
      const sp = new URLSearchParams(location.search);
      utmKeys.forEach(function (k) {
        const v = sp.get(k);
        if (v) out[k] = v;
      });
    } catch (_) {}
    return out;
  }

  function withUtms(url) {
    try {
      const u = new URL(url, location.origin);
      const sp = new URLSearchParams(location.search);
      utmKeys.forEach(function (k) {
        const v = sp.get(k);
        if (v && !u.searchParams.has(k)) u.searchParams.set(k, v);
      });
      return u.toString();
    } catch (_) {
      return url;
    }
  }

  function assetUrl(key) {
    return assets[key] || '';
  }

  function badgeFor(key, override) {
    if (override === null || override === '') return '';
    const b = override || badges[key] || 'FILMED';
    if (!b) return '';
    const cls = /render/i.test(b) ? ' media-badge--render' : '';
    return `<span class="media-badge${cls}">${esc(b)}</span>`;
  }

  function chipsHtml(chips) {
    if (!chips || !chips.length) return '';
    return `<div class="chip-row">${chips
      .map(function (c) {
        return `<div class="chip"><span class="chip-value">${esc(c.value)}</span><span class="chip-label">${esc(c.label)}</span></div>`;
      })
      .join('')}</div>`;
  }

  function pressCards(cards) {
    if (!cards || !cards.length) return '';
    return `<div class="press-row">${cards
      .map(function (c) {
        return `<a class="press-card" href="${esc(withUtms(c.url))}" target="_blank" rel="noopener noreferrer" data-outbound data-label="${esc(c.outlet)}">
          <span class="press-outlet">${esc(c.outlet)}</span>
          <span class="press-headline">${esc(c.headline)}</span>
        </a>`;
      })
      .join('')}</div>`;
  }

  function outboundLinks(links) {
    if (!links || !links.length) return '';
    return `<div class="link-row">${links
      .map(function (l) {
        return `<a class="doctrine-link" href="${esc(withUtms(l.url))}" target="_blank" rel="noopener noreferrer" data-outbound data-label="${esc(l.label)}">${esc(l.label)}</a>`;
      })
      .join('')}</div>`;
  }

  function loopCard(clip, opts) {
    opts = opts || {};
    const src = assetUrl(clip.asset);
    if (!src) return '';
    const poster = assets.hero_poster || '';
    const letterbox = clip.asset === 'loop_te263_montage' || opts.letterbox;
    const mediaCls = letterbox ? ' vcard-media--letterbox' : '';
    const posterOnly = (saveData || reduceMotion) && poster && opts.allowPosterOnly;
    return `<div class="vcard vcard-loop" data-clip="${esc(clip.id || clip.asset)}" data-section="${esc(opts.sectionId || '')}" data-asset="${esc(clip.asset)}">
      <span class="vcard-media${mediaCls}">
        ${badgeFor(clip.asset, clip.badge)}
        ${
          posterOnly
            ? `<img src="${esc(poster)}" alt="" loading="lazy" />`
            : `<video muted playsinline loop preload="metadata" ${poster ? `poster="${esc(poster)}"` : ''} data-ambient data-section="${esc(opts.sectionId || '')}" data-asset="${esc(clip.asset)}">
                <source src="${esc(src)}" type="video/mp4" />
              </video>`
        }
        <span class="play" aria-hidden="true"><span>▶</span></span>
        ${clip.duration ? `<span class="dur">${esc(clip.duration)}</span>` : ''}
      </span>
      ${clip.caption ? `<span class="vcard-cap">${esc(clip.caption)}</span>` : ''}
    </div>`;
  }

  function stillCard(item) {
    const src = assetUrl(item.asset);
    if (!src) return '';
    return `<figure class="vcard">
      <span class="vcard-media">
        ${badgeFor(item.asset, item.badge)}
        <img src="${esc(src)}" alt="" loading="lazy" />
      </span>
      ${item.caption ? `<span class="vcard-cap">${esc(item.caption)}</span>` : ''}
    </figure>`;
  }

  function renderHero(sec) {
    const loop = sec.media || {};
    const src = assetUrl(loop.asset);
    const poster = assets.hero_poster || '';
    const film = sec.film || {};
    const filmSrc = assetUrl(film.asset);
    return `<section class="story-section story-section--hero" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="hero-cinema">
        ${
          reduceMotion || (saveData && poster)
            ? `<img class="hero-poster" src="${esc(poster || src)}" alt="" fetchpriority="high" />`
            : `<video class="hero-video" muted playsinline loop preload="auto" ${poster ? `poster="${esc(poster)}"` : ''} data-ambient data-section="${esc(sec.id)}" data-asset="${esc(loop.asset || '')}">
                <source src="${esc(src)}" type="video/mp4" />
              </video>`
        }
        <div class="hero-overlay">
          <div class="section-inner" style="padding-inline:0;max-width:1100px">
            ${sec.eyebrow ? `<h1 class="eyebrow">${esc(sec.eyebrow)}</h1>` : ''}
            ${
              filmSrc
                ? `<button type="button" class="btn-watch" data-film="${esc(filmSrc)}" data-film-title="${esc(film.title || '')}" data-section="${esc(sec.id)}" data-cta="${esc(sec.play_button_label || 'Watch the film')}">${esc(sec.play_button_label || 'Watch the film')}</button>`
                : ''
            }
          </div>
        </div>
      </div>
      ${chipsHtml(sec.stats || sec.chips)}
    </section>`;
  }

  function renderDemoGrid(sec) {
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${sec.lede ? `<p class="lede">${esc(sec.lede)}</p>` : ''}
        <div class="video-grid">
          ${(sec.clips || []).map(function (c) { return loopCard(c, { sectionId: sec.id }); }).join('')}
        </div>
      </div>
    </section>`;
  }

  function renderFilmPlates(sec) {
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        <h2 class="headline">${esc(sec.headline)}</h2>
        <div class="film-plates">
          ${(sec.films || [])
            .map(function (f) {
              const poster =
                assets['yt_' + f.youtube_id] ||
                (f.youtube_id ? `https://img.youtube.com/vi/${f.youtube_id}/maxresdefault.jpg` : '');
              const meta = [f.duration, f.label].filter(Boolean).join(' · ');
              return `<button type="button" class="film-plate" data-yt="${esc(f.youtube_id || '')}" data-section="${esc(sec.id)}" data-film-title="${esc(f.title || '')}" aria-label="Play ${esc(f.title || 'film')}">
                <span class="vcard-media">
                  ${badgeFor('yt_' + f.youtube_id, 'FILMED')}
                  ${poster ? `<img src="${esc(poster)}" alt="" loading="lazy" />` : ''}
                  <span class="play" aria-hidden="true"><span>▶</span></span>
                  ${f.duration ? `<span class="dur">${esc(f.duration)}</span>` : ''}
                </span>
                <span class="film-plate-title">${esc(f.title || '')}</span>
                ${meta ? `<span class="film-plate-meta">${esc(meta)}</span>` : ''}
              </button>`;
            })
            .join('')}
        </div>
      </div>
    </section>`;
  }

  function renderField(sec) {
    const media = sec.media || [];
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        ${sec.kicker ? `<p class="kicker">${esc(sec.kicker)}</p>` : ''}
        ${sec.headline ? `<h2 class="headline">${esc(sec.headline)}</h2>` : ''}
        <div class="field-row">
          ${media
            .map(function (m) {
              if (m.class === 'ambient') return loopCard(m, { sectionId: sec.id, letterbox: m.asset === 'loop_te263_montage' });
              return stillCard(m);
            })
            .join('')}
        </div>
        ${outboundLinks(sec.links)}
      </div>
    </section>`;
  }

  function renderPress(sec) {
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${pressCards(sec.press)}
        ${outboundLinks(sec.links)}
      </div>
    </section>`;
  }

  function renderCta(sec) {
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${sec.body ? `<p class="body">${esc(sec.body)}</p>` : ''}
        <div class="cta-row">
          ${(sec.ctas || [])
            .map(function (c, i) {
              if (c.kind === 'mailto') {
                return `<a class="cta-btn${i === 0 ? ' cta-btn--primary' : ''}" href="mailto:${esc(c.value)}" data-cta="${esc(c.label)}">${esc(c.label)}</a>`;
              }
              if (c.kind === 'email-display') {
                return `<button type="button" class="cta-btn cta-btn--email" data-copy-email="${esc(c.value)}" data-cta="${esc(c.label)}" title="Copy email">
                  ${esc(c.value)}
                  <span class="cta-copied" hidden>Copied</span>
                </button>`;
              }
              return '';
            })
            .join('')}
        </div>
      </div>
    </section>`;
  }

  function renderSection(sec) {
    switch (sec.kind) {
      case 'hero-film':
        return renderHero(sec);
      case 'demo-grid':
        return renderDemoGrid(sec);
      case 'film-plate':
        return renderFilmPlates(sec);
      case 'field-row':
        return renderField(sec);
      case 'press-wall':
        return renderPress(sec);
      case 'cta':
        return renderCta(sec);
      default:
        return '';
    }
  }

  function renderNav() {
    const anchors = (site.nav && site.nav.anchors) || [];
    return `<div class="story-progress" id="story-progress"></div>
    <nav class="story-nav" aria-label="Sections">
      <a class="story-brand" href="#hero">${brandMark()}<span class="story-brand-name">Navier</span></a>
      <div class="story-anchors">
        ${anchors
          .map(function (a) {
            return `<a href="#${esc(a.id)}" data-nav="${esc(a.id)}">${esc(a.label)}</a>`;
          })
          .join('')}
      </div>
    </nav>`;
  }

  function lightboxHtml() {
    return `<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video">
      <button type="button" class="lightbox-close" id="lb-close" aria-label="Close">×</button>
      <div class="lightbox-frame" id="lb-frame"></div>
    </div>`;
  }

  const app = document.getElementById('app');
  const sections = story.sections || [];
  app.innerHTML = renderNav() + sections.map(renderSection).join('') + lightboxHtml();

  function openLb(html) {
    const box = document.getElementById('lightbox');
    const frame = document.getElementById('lb-frame');
    if (!box || !frame) return;
    frame.innerHTML = html;
    box.classList.add('open');
  }
  function closeLb() {
    const box = document.getElementById('lightbox');
    const frame = document.getElementById('lb-frame');
    if (box) box.classList.remove('open');
    if (frame) frame.innerHTML = '';
  }
  const lbClose = document.getElementById('lb-close');
  if (lbClose) lbClose.addEventListener('click', closeLb);
  const lb = document.getElementById('lightbox');
  if (lb) {
    lb.addEventListener('click', function (e) {
      if (e.target.id === 'lightbox') closeLb();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeLb();
  });

  document.querySelectorAll('[data-yt]').forEach(function (el) {
    el.addEventListener('click', function () {
      const id = el.getAttribute('data-yt');
      if (!id) return;
      const section = el.getAttribute('data-section') || '';
      const title = el.getAttribute('data-film-title') || id;
      track('video_play', { section_id: section, asset: 'yt:' + id, title: title, class: 'film' });
      openLb(
        `<iframe src="https://www.youtube.com/embed/${esc(id)}?autoplay=1&rel=0" title="${esc(title)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>`
      );
    });
  });

  document.querySelectorAll('[data-film]').forEach(function (el) {
    el.addEventListener('click', function () {
      const src = el.getAttribute('data-film');
      const section = el.getAttribute('data-section') || '';
      const title = el.getAttribute('data-film-title') || 'film';
      if (!src) return;
      track('video_play', { section_id: section, asset: src, title: title, class: 'film' });
      track('cta_click', { label: el.getAttribute('data-cta') || title });
      openLb(
        `<video controls autoplay playsinline style="width:100%;height:100%;background:#000"><source src="${esc(src)}" type="video/mp4" /></video>`
      );
      const v = document.querySelector('#lb-frame video');
      if (v) {
        v.addEventListener(
          'ended',
          function () {
            track('video_complete', { section_id: section, asset: src, title: title, class: 'film' });
          },
          { once: true }
        );
      }
    });
  });

  /* Demo-grid: click toggles mute, matching /invest */
  document.querySelectorAll('.vcard-loop').forEach(function (card) {
    card.addEventListener('click', function (e) {
      const v = card.querySelector('video');
      if (!v) return;
      e.preventDefault();
      if (v.muted) {
        v.muted = false;
        v.play().catch(function () {});
        card.classList.add('is-audible');
        track('video_play', {
          section_id: card.getAttribute('data-section') || '',
          asset: card.getAttribute('data-asset') || '',
          class: 'ambient',
          audible: true,
        });
      } else {
        v.muted = true;
        card.classList.remove('is-audible');
      }
    });
  });

  document.querySelectorAll('[data-outbound]').forEach(function (el) {
    el.addEventListener('click', function () {
      track('outbound_click', {
        label: el.getAttribute('data-label') || el.textContent.trim(),
        href: el.getAttribute('href') || '',
      });
    });
  });

  document.querySelectorAll('[data-cta]').forEach(function (el) {
    if (el.hasAttribute('data-film')) return;
    el.addEventListener('click', function () {
      track('cta_click', { label: el.getAttribute('data-cta') || '' });
    });
  });

  document.querySelectorAll('[data-copy-email]').forEach(function (el) {
    el.addEventListener('click', function () {
      const email = el.getAttribute('data-copy-email');
      const tip = el.querySelector('.cta-copied');
      function showCopied() {
        if (!tip) return;
        tip.hidden = false;
        setTimeout(function () {
          tip.hidden = true;
        }, 1600);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(email).then(showCopied).catch(showCopied);
      } else {
        showCopied();
      }
    });
  });

  const playedAmbient = new WeakSet();
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          const v = en.target;
          if (!(v instanceof HTMLVideoElement) || reduceMotion) return;
          if (en.isIntersecting) {
            v.play().catch(function () {});
            if (!playedAmbient.has(v)) {
              playedAmbient.add(v);
              track('video_play', {
                section_id: v.getAttribute('data-section') || '',
                asset: v.getAttribute('data-asset') || '',
                class: 'ambient',
              });
            }
          } else {
            v.pause();
          }
        });
      },
      { threshold: 0.35 }
    );
    document.querySelectorAll('video[data-ambient]').forEach(function (v) {
      io.observe(v);
      let completed = false;
      v.addEventListener('timeupdate', function () {
        if (completed || !v.duration) return;
        if (v.currentTime / v.duration >= 0.85) {
          completed = true;
          track('video_complete', {
            section_id: v.getAttribute('data-section') || '',
            asset: v.getAttribute('data-asset') || '',
            class: 'ambient',
          });
        }
      });
    });

    const seen = new Set();
    const sio = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          const id = en.target.getAttribute('data-section') || en.target.id;
          if (!id || seen.has(id)) return;
          seen.add(id);
          track('section_view', { section_id: id });
        });
      },
      { threshold: 0.45 }
    );
    document.querySelectorAll('[data-section]').forEach(function (el) {
      sio.observe(el);
    });
  }

  const progress = document.getElementById('story-progress');
  const navLinks = [...document.querySelectorAll('[data-nav]')];
  const chapterIds = navLinks.map(function (a) {
    return a.getAttribute('data-nav');
  });

  function jumpToId(id, updateHash) {
    const el = id && document.getElementById(id);
    if (!el) return false;
    el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
    if (updateHash && history.replaceState) history.replaceState(null, '', '#' + id);
    return true;
  }

  function onScrollNav() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    let active = chapterIds[0];
    for (let i = 0; i < chapterIds.length; i++) {
      const el = document.getElementById(chapterIds[i]);
      if (el && el.getBoundingClientRect().top <= 120) active = chapterIds[i];
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

  console.info('[story] v3 watch reel · sections', sections.length);
})();
