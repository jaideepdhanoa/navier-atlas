/* /story — public outreach proof reel (v2: /invest arc, sourced headlines) */
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
  const footnotes = story.footnotes || {};
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData =
    (navigator.connection && navigator.connection.saveData) ||
    /iPhone|iPad|Android/i.test(navigator.userAgent);

  const usedFns = new Set();
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
    if (/[?&]debug_analytics=1/.test(location.search)) {
      console.info('[story analytics]', event, props);
    }
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

  function firstMedia(sec) {
    if (!sec) return null;
    if (Array.isArray(sec.media)) return sec.media[0] || null;
    if (sec.media && typeof sec.media === 'object') return sec.media;
    return null;
  }

  function mediaList(sec) {
    if (!sec) return [];
    if (Array.isArray(sec.media)) return sec.media;
    if (sec.media && typeof sec.media === 'object') return [sec.media];
    return [];
  }

  function badgeFor(key, override) {
    if (override === null || override === '') return '';
    const b = override || badges[key] || 'FILMED';
    if (!b) return '';
    const cls = /render/i.test(b) ? ' media-badge--render' : '';
    return `<span class="media-badge${cls}">${esc(b)}</span>`;
  }

  function captionHtml(item) {
    if (!item || !item.caption) return '';
    let ref = '';
    if (item.footnote_ref && footnotes[item.footnote_ref]) {
      usedFns.add(item.footnote_ref);
      ref = ` <sup class="fn-ref">*</sup>`;
    }
    return `<p class="caption-band">${esc(item.caption)}${ref}</p>`;
  }

  function chipsHtml(chips) {
    if (!chips || !chips.length) return '';
    return `<div class="chip-row">${chips
      .map(function (c) {
        return `<div class="chip"><span class="chip-value">${esc(c.value)}</span><span class="chip-label">${esc(c.label)}</span></div>`;
      })
      .join('')}</div>`;
  }

  function chapterKicker(sec) {
    if (!sec || !sec.chapter) return '';
    return `<p class="chapter-index">${esc(sec.chapter)}</p>`;
  }

  function stillFrame(item, opts) {
    opts = opts || {};
    if (isMapComponent(item)) return atlasFrame(item);
    const src = assetUrl(item.asset);
    if (!src) return '';
    const letterbox = opts.letterbox ? ' media-frame--letterbox' : '';
    return `<figure class="proof-card${opts.te ? ' proof-card--te' : ''}${opts.wide ? ' proof-card--wide' : ''}">
      <div class="media-frame${letterbox}">
        ${badgeFor(item.asset, item.badge)}
        <img src="${esc(src)}" alt="" loading="${opts.eager ? 'eager' : 'lazy'}" ${opts.eager ? 'fetchpriority="high"' : ''} />
      </div>
      ${captionHtml(item)}
    </figure>`;
  }

  function ambientFrame(item, opts) {
    opts = opts || {};
    const src = assetUrl(item.asset);
    if (!src) return '';
    const poster = assets.hero_poster || '';
    const letterbox = opts.letterbox || item.asset === 'loop_te263_montage';
    const frameCls = letterbox ? ' media-frame--letterbox' : '';
    if ((saveData || reduceMotion) && poster && opts.allowPosterOnly) {
      return `<figure class="proof-card">
        <div class="media-frame${frameCls}">
          ${badgeFor(item.asset, item.badge)}
          <img src="${esc(poster)}" alt="" loading="lazy" />
        </div>
        ${captionHtml(item)}
      </figure>`;
    }
    return `<figure class="proof-card${letterbox ? ' proof-card--te' : ''}">
      <div class="media-frame${frameCls}">
        ${badgeFor(item.asset, item.badge)}
        <video muted playsinline loop preload="metadata" ${poster ? `poster="${esc(poster)}"` : ''} data-ambient data-section="${esc(opts.sectionId || '')}" data-asset="${esc(item.asset)}">
          <source src="${esc(src)}" type="video/mp4" />
        </video>
      </div>
      ${captionHtml(item)}
    </figure>`;
  }

  function isMapComponent(item) {
    return item && (item.class === 'map-component' || item.asset === 'plate_atlas_global');
  }

  function atlasFrame(item) {
    return `<figure class="proof-card proof-card--atlas">
      <div class="atlas-static" id="atlas-static" role="img" aria-label="${esc((item && item.caption) || 'Global marine corridors')}"></div>
      ${captionHtml(item)}
    </figure>`;
  }

  function mediaItem(item, opts) {
    if (!item) return '';
    if (isMapComponent(item)) return atlasFrame(item);
    if (item.class === 'ambient') return ambientFrame(item, opts);
    return stillFrame(item, opts);
  }

  function pressCards(cards) {
    if (!cards || !cards.length) return '';
    return `<div class="press-row">${cards
      .map(function (c) {
        const href = withUtms(c.url);
        return `<a class="press-card" href="${esc(href)}" target="_blank" rel="noopener noreferrer" data-outbound data-label="${esc(c.outlet)}">
          <span class="press-outlet">${esc(c.outlet)}</span>
          <span class="press-headline">${esc(c.headline)}</span>
        </a>`;
      })
      .join('')}</div>`;
  }

  function filmCards(cards, sectionId) {
    if (!cards || !cards.length) return '';
    return `<div class="film-row">${cards
      .map(function (c) {
        let poster = '';
        let playAttr = '';
        if (c.youtube_id) {
          poster = assets['yt_' + c.youtube_id] || `https://img.youtube.com/vi/${c.youtube_id}/maxresdefault.jpg`;
          playAttr = `data-yt="${esc(c.youtube_id)}"`;
        } else if (c.asset) {
          poster = assets[c.asset + '_poster'] || assets.hero_poster || '';
          playAttr = `data-film="${esc(assetUrl(c.asset))}"`;
        }
        return `<button type="button" class="film-card" ${playAttr} data-section="${esc(sectionId || '')}" data-film-title="${esc(c.title || '')}" aria-label="Play ${esc(c.title || 'film')}">
          <span class="film-media">
            ${badgeFor(c.asset || ('yt_' + c.youtube_id), c.badge || 'FILMED')}
            ${poster ? `<img src="${esc(poster)}" alt="" loading="lazy" />` : ''}
            <span class="film-play" aria-hidden="true"><span>▶</span></span>
          </span>
          <span class="film-cap">${esc(c.title || '')}</span>
        </button>`;
      })
      .join('')}</div>`;
  }

  function outboundLinks(links) {
    if (!links || !links.length) return '';
    return `<div class="link-row">${links
      .map(function (l) {
        return `<a class="doctrine-link" href="${esc(withUtms(l.url))}" ${l.external === false ? '' : 'target="_blank" rel="noopener noreferrer"'} data-outbound data-label="${esc(l.label)}">${esc(l.label)}</a>`;
      })
      .join('')}</div>`;
  }

  function proofGrid(media, sectionId) {
    const n = media.length;
    let gridCls = 'proof-grid--2';
    if (n === 3) gridCls = 'proof-grid--3';
    else if (n === 4) gridCls = 'proof-grid--4';
    else if (n >= 5) gridCls = 'proof-grid--mixed';
    return `<div class="proof-grid ${gridCls}">
      ${media
        .map(function (m) {
          return mediaItem(m, {
            sectionId: sectionId,
            letterbox: m.asset === 'loop_te263_montage',
          });
        })
        .join('')}
    </div>`;
  }

  function renderHero(sec) {
    const media = firstMedia(sec) || {};
    const src = assetUrl(media.asset);
    const poster = assets.hero_poster || '';
    return `<section class="story-section story-section--hero" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="hero-cinema">
        <div class="media-frame">
          ${badgeFor(media.asset, media.badge)}
          ${
            reduceMotion || (saveData && poster)
              ? `<img class="hero-poster" src="${esc(poster || src)}" alt="" fetchpriority="high" />`
              : `<video class="hero-video" muted playsinline loop preload="auto" ${poster ? `poster="${esc(poster)}"` : ''} data-ambient data-section="${esc(sec.id)}" data-asset="${esc(media.asset || '')}">
                  <source src="${esc(src)}" type="video/mp4" />
                </video>`
          }
        </div>
        <div class="hero-overlay">
          <div class="section-inner" style="padding-inline:0;max-width:1100px">
            ${sec.eyebrow ? `<p class="eyebrow">${esc(sec.eyebrow)}</p>` : ''}
            <h1 class="headline headline--thesis">${esc(sec.headline)}</h1>
            ${sec.subline ? `<p class="subline">${esc(sec.subline)}</p>` : ''}
            ${chipsHtml(sec.chips || sec.stats)}
          </div>
        </div>
      </div>
    </section>`;
  }

  function renderClaimChapter(sec) {
    const media = mediaList(sec);
    const levers = media.filter(function (m) {
      return String(m.asset || '').indexOf('lever_') === 0;
    });
    const rest = media.filter(function (m) {
      return String(m.asset || '').indexOf('lever_') !== 0;
    });
    const costs = sec.costs || [];
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        ${chapterKicker(sec)}
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${sec.headline_2 ? `<p class="headline-2">${esc(sec.headline_2)}</p>` : ''}
        ${sec.body ? `<p class="body">${esc(sec.body)}</p>` : ''}
        ${
          costs.length
            ? `<div class="cost-grid">${costs
                .map(function (c) {
                  return `<article class="cost-card">
                    <p class="cost-kicker">${esc(c.cost_title)}</p>
                    <p class="cost-body">${esc(c.cost_body)}</p>
                    <p class="lever-title">${esc(c.lever_title)}</p>
                    <p class="lever-body">${esc(c.lever_body)}</p>
                  </article>`;
                })
                .join('')}</div>`
            : ''
        }
        ${levers.length ? `<div class="proof-grid proof-grid--3">${levers.map(function (m) { return mediaItem(m, { sectionId: sec.id }); }).join('')}</div>` : ''}
        ${rest.map(function (m) { return `<div class="plainview-plate">${mediaItem(m, { sectionId: sec.id, wide: true })}</div>`; }).join('')}
        ${
          sec.why_now
            ? `<div class="why-now"><p class="why-now-title">${esc(sec.why_now.title)}</p><p class="why-now-body">${esc(sec.why_now.body)}</p></div>`
            : ''
        }
        ${sec.closing_line ? `<p class="closing-line">${esc(sec.closing_line)}</p>` : ''}
      </div>
    </section>`;
  }

  function renderProofChapter(sec) {
    const media = mediaList(sec);
    const press = sec.press || sec.press_cards || [];
    const films = sec.films || sec.film_cards || [];
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        ${chapterKicker(sec)}
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${sec.body ? `<p class="body">${esc(sec.body)}</p>` : ''}
        ${chipsHtml(sec.chips || sec.stats)}
        ${proofGrid(media, sec.id)}
        ${filmCards(films, sec.id)}
        ${pressCards(press)}
      </div>
    </section>`;
  }

  function renderProductChapter(sec) {
    const media = mediaList(sec);
    const plate = media[0];
    const rest = media.slice(1);
    const films = sec.films || sec.film_cards || [];
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        ${chapterKicker(sec)}
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${sec.body ? `<p class="body">${esc(sec.body)}</p>` : ''}
        ${plate ? `<div class="fleet-plate">${stillFrame(plate)}</div>` : ''}
        <div class="vessel-row">
          ${(sec.vessels || [])
            .map(function (v) {
              return `<div class="vessel-card"><h3 class="vessel-name">${esc(v.name)}</h3><p class="vessel-line">${esc(v.line)}</p></div>`;
            })
            .join('')}
        </div>
        ${rest.length ? `<div class="proof-grid proof-grid--3">${rest.map(function (m) { return mediaItem(m, { sectionId: sec.id }); }).join('')}</div>` : ''}
        ${sec.ride_note ? `<p class="ride-note">${esc(sec.ride_note)}</p>` : ''}
        ${filmCards(films, sec.id)}
      </div>
    </section>`;
  }

  function renderDualUseChapter(sec) {
    const media = mediaList(sec);
    const press = sec.press || sec.press_cards || [];
    const films = sec.films || sec.film_cards || [];
    const close = sec.quanta_close || {};
    const closeMedia = close.media || [];
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        ${chapterKicker(sec)}
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${sec.body ? `<p class="body">${esc(sec.body)}</p>` : ''}
        ${chipsHtml(sec.chips || sec.stats)}
        ${proofGrid(media, sec.id)}
        ${
          close.body
            ? `<div class="quanta-close">
                <p class="body">${esc(close.body)}</p>
                ${closeMedia.map(function (m) { return mediaItem(m, { sectionId: sec.id }); }).join('')}
              </div>`
            : ''
        }
        ${filmCards(films, sec.id)}
        ${pressCards(press)}
        ${outboundLinks(sec.links)}
      </div>
    </section>`;
  }

  function renderVisionClose(sec) {
    const media = mediaList(sec);
    return `<section class="story-section story-section--vision" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        ${chapterKicker(sec)}
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${sec.body ? `<p class="body">${esc(sec.body)}</p>` : ''}
        ${media.map(function (m) { return mediaItem(m, { sectionId: sec.id, wide: true }); }).join('')}
      </div>
    </section>`;
  }

  function renderFilmShelf(sec) {
    const films = sec.films || sec.film_cards || [];
    const wall = sec.press_wall || [];
    const links = sec.links || (sec.doctrine_link ? [sec.doctrine_link] : []);
    return `<section class="story-section" id="${esc(sec.id)}" data-section="${esc(sec.id)}">
      <div class="section-inner">
        <h2 class="headline">${esc(sec.headline)}</h2>
        ${filmCards(films, sec.id)}
        ${
          wall.length
            ? `<div class="press-wall">${wall
                .map(function (p) {
                  return `<a href="${esc(withUtms(p.url))}" target="_blank" rel="noopener noreferrer" data-outbound data-label="${esc(p.outlet)}">${esc(p.outlet)}</a>`;
                })
                .join('')}</div>`
            : ''
        }
        ${outboundLinks(links)}
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
                const href = 'mailto:' + c.value;
                return `<a class="cta-btn${i === 0 ? ' cta-btn--primary' : ''}" href="${esc(href)}" data-cta="${esc(c.label)}">${esc(c.label)}</a>`;
              }
              if (c.kind === 'email-display') {
                return `<button type="button" class="cta-btn cta-btn--email" data-copy-email="${esc(c.value)}" data-cta="${esc(c.label)}" title="Copy email">
                  ${esc(c.value)}
                  <span class="cta-copied" hidden>Copied</span>
                </button>`;
              }
              if (c.kind === 'url' && c.value && !/\[.*\]/.test(c.value)) {
                return `<a class="cta-btn" href="${esc(withUtms(c.value))}" target="_blank" rel="noopener noreferrer" data-cta="${esc(c.label)}">${esc(c.label)}</a>`;
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
      case 'hero-loop':
        return renderHero(sec);
      case 'claim-chapter':
        return renderClaimChapter(sec);
      case 'proof-chapter':
      case 'claim-proof':
        return renderProofChapter(sec);
      case 'product-chapter':
      case 'vessel-row':
        return renderProductChapter(sec);
      case 'dual-use-chapter':
        return renderDualUseChapter(sec);
      case 'vision-close':
        return renderVisionClose(sec);
      case 'film-shelf':
        return renderFilmShelf(sec);
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

  function renderFootnotes() {
    if (!usedFns.size) return '';
    const items = [...usedFns]
      .map(function (k) {
        return `<li id="fn-${esc(k)}">${esc(footnotes[k])}</li>`;
      })
      .join('');
    return `<footer class="story-footnotes"><ol>${items}</ol></footer>`;
  }

  function lightboxHtml() {
    return `<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video">
      <button type="button" class="lightbox-close" id="lb-close" aria-label="Close">×</button>
      <div class="lightbox-frame" id="lb-frame"></div>
    </div>`;
  }

  const app = document.getElementById('app');
  const sections = story.sections || [];
  let body = sections.map(renderSection).join('');
  app.innerHTML = renderNav() + body + renderFootnotes() + lightboxHtml();

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
      openLb(
        `<video controls autoplay playsinline style="width:100%;height:100%;background:#000" data-complete-track><source src="${esc(src)}" type="video/mp4" /></video>`
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

  document.querySelectorAll('[data-outbound]').forEach(function (el) {
    el.addEventListener('click', function () {
      track('outbound_click', {
        label: el.getAttribute('data-label') || el.textContent.trim(),
        href: el.getAttribute('href') || '',
      });
    });
  });

  document.querySelectorAll('[data-cta]').forEach(function (el) {
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
  }

  if ('IntersectionObserver' in window) {
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
    const thresh = 120;
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

  function mountAtlas() {
    const el = document.getElementById('atlas-static');
    if (!el || typeof maplibregl === 'undefined') return;
    try {
      const map = new maplibregl.Map({
        container: el,
        style: 'https://tiles.openfreemap.org/styles/dark',
        center: [12, 18],
        zoom: 1.35,
        minZoom: 1.2,
        maxZoom: 1.8,
        interactive: false,
        attributionControl: true,
        fadeDuration: 0,
      });
      map.scrollZoom.disable();
      map.dragPan.disable();
      map.dragRotate.disable();
      map.touchZoomRotate.disable();
      map.keyboard.disable();
      map.doubleClickZoom.disable();
      map.boxZoom.disable();
    } catch (err) {
      console.warn('[story] atlas map failed', err);
    }
  }
  if (document.getElementById('atlas-static')) {
    if (typeof maplibregl !== 'undefined') mountAtlas();
    else {
      const wait = setInterval(function () {
        if (typeof maplibregl !== 'undefined') {
          clearInterval(wait);
          mountAtlas();
        }
      }, 80);
      setTimeout(function () {
        clearInterval(wait);
      }, 4000);
    }
  }

  console.info('[story] mount ok · sections', sections.length);
})();
