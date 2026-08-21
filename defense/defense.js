/**
 * /defense capability brief v2 — render authored defense.json only.
 * No links to /invest or /teaser. Password gate is middleware.
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

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function mediaPath(src) {
    if (!src) return '';
    if (/^https?:\/\//i.test(src) || src.startsWith('//') || src.startsWith('/')) return src;
    return BASE + src.replace(/^\.\//, '');
  }
  function kicker(s) {
    return s.kicker ? `<p class="def-kicker">${esc(s.kicker)}</p>` : '';
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
        (b) => `<div class="def-block"><div class="head">${esc(b.head || '')}</div><p>${esc(b.body || '')}</p></div>`
      )
      .join('')}</div>`;
  }

  function videoTile(v, opts) {
    opts = opts || {};
    const poster = mediaPath(v.poster || '');
    const behavior = String(v.behavior || '');
    const withSound = /with sound/i.test(behavior) || !!opts.withSound;
    // Muted autoplay wins over a generic opts.click (section helpers must not kill loops)
    const autoplay = /autoplay/i.test(behavior) && !withSound && !reduceMotion;
    const click =
      !autoplay && (/click-to-play/i.test(behavior) || withSound || !!opts.click);

    if (v.embed_url) {
      const thumb = poster || '';
      const label = [v.title, v.duration].filter(Boolean).join(' · ');
      // Invest-style film card when requested (control-sbs companion)
      if (opts.filmCard) {
        return `<button type="button" class="film-card" data-yt-embed="${esc(v.embed_url)}" aria-label="Play ${esc(v.title || 'video')}">
          <span class="film-media">
            ${thumb ? `<img src="${esc(thumb)}" alt="" loading="lazy" />` : ''}
            <span class="play" aria-hidden="true"><span>▶</span></span>
            ${v.duration ? `<span class="dur">${esc(v.duration)}</span>` : ''}
          </span>
          ${label ? `<span class="film-cap">${esc(label)}</span>` : ''}
        </button>`;
      }
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
        <video ${attrs}>
          <source src="${esc(mediaPath(v.src))}" type="video/mp4" />
        </video>
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

  const R = {
    'def-hero'(s) {
      const v = s.media || {};
      return `<section class="section-block hero-section" id="${esc(s.id)}" data-reveal>
        <video class="def-hero-video hero-video" muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="metadata" poster="${esc(mediaPath(v.poster || 'assets/deck/defense-sofweek-armed.jpg'))}" data-lazy-video>
          <source src="${esc(mediaPath(v.src))}" type="video/mp4" />
        </video>
        <div class="shell-stage" style="padding-top:28px;padding-bottom:36px">
          ${kicker(s)}
          <h1 class="h1">${esc(s.title || '')}</h1>
          ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
        </div>
      </section>`;
    },
    'def-navier'(s) {
      // Invest prose-stage split — Core Thesis + hangar plate
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
            ${media.caption ? `<figcaption>${esc(media.caption)}</figcaption>` : ''}
          </figure>`
        : '';
      const bridge = s.body ? `<p class="def-closer section-inner">${esc(s.body)}</p>` : '';
      const film = s.film || {};
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
        ${
          film.src
            ? `<div class="def-film-wrap media-inner" data-def-film>
          ${videoTile(Object.assign({}, film, { behavior: film.behavior || 'click-to-play with sound' }), { wide: true, withSound: true })}
        </div>`
            : ''
        }
      </section>`;
    },
    'def-about'(s) {
      // legacy id support
      return R['def-navier'](s);
    },
    'def-problem'(s) {
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${blocksHtml(s.blocks)}
        ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
      </section>`;
    },
    'def-platform'(s) {
      // Invest control-sbs: callout schematic + CTO film; one muted stabilization loop
      const schem =
        (s.media_pair || []).find(function (m) {
          return m && m.src && !String(m.src).endsWith('.mp4');
        }) || (s.media_pair || [])[0];
      const vids = s.videos || [];
      const film =
        vids.find(function (v) {
          return v.role === 'control-film' || v.embed_url;
        }) || null;
      const loops = vids.filter(function (v) {
        return v !== film && v.src && /autoplay/i.test(v.behavior || '');
      });
      const other = vids.filter(function (v) {
        return v !== film && loops.indexOf(v) === -1;
      });
      const wire = schem && schem.src ? mediaPath(schem.src) : '';
      return `<section class="section-block stage-section control-stage" id="${esc(s.id)}" data-reveal>
        <div class="section-inner">
          ${kicker(s)}
          <h2 class="h2">${esc(s.title || '')}</h2>
          ${s.body ? `<p class="lead">${esc(s.body)}</p>` : ''}
        </div>
        <div class="control-sbs media-inner">
          <div class="control-diagram control-diagram-plate" id="control-diagram">
            ${
              wire
                ? `<img class="control-wire control-plate-img" src="${esc(wire)}" alt="${esc(schem.alt || 'Navier control schematic')}" loading="eager" fetchpriority="high" />`
                : ''
            }
          </div>
          <div class="control-video">
            ${film ? videoTile(film, { filmCard: true }) : ''}
          </div>
        </div>
        ${
          loops.length
            ? `<div class="def-video-row media-inner">${loops.map(function (v) {
                return videoTile(v);
              }).join('')}</div>`
            : ''
        }
        ${
          other.length
            ? `<div class="def-video-row media-inner">${other.map(function (v) {
                return videoTile(v);
              }).join('')}</div>`
            : ''
        }
      </section>`;
    },
    'def-flight'(s) {
      // Click-to-play with sound (YouTube) — local posters from contract
      const wall = `<div class="def-video-wall">${(s.videos || [])
        .map(function (v) {
          return videoTile(v, { withSound: true });
        })
        .join('')}</div>`;
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
        ${wall}
        ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
      </section>`;
    },
    'def-quanta'(s) {
      const specs = `<div class="def-spec-row">${(s.spec_row || [])
        .map((c) => `<div class="def-spec-chip"><div class="stat">${esc(c.stat)}</div><div class="detail">${esc(c.detail)}</div></div>`)
        .join('')}</div>`;
      const missions = `<div class="def-mission">${(s.mission_blocks || [])
        .map((b) => `<div class="def-block"><div class="head">${esc(b.head)}</div><p>${esc(b.body)}</p></div>`)
        .join('')}</div>`;
      const media = `<div class="def-pair">${(s.media || []).map((m) => plate(m.src, m.alt)).join('')}</div>`;
      const vids = s.videos || [];
      const loops = vids.filter((v) => v.src && /autoplay/i.test(v.behavior || ''));
      const lead = vids.filter((v) => v.embed_url || /with sound/i.test(v.behavior || ''));
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
        ${specs}
        ${loops.length ? `<div class="def-video-row">${loops.map((v) => videoTile(v)).join('')}</div>` : ''}
        ${missions}${media}
        ${lead.length ? `<div class="def-video-row def-video-row--lead">${lead.map((v) => videoTile(v, { wide: true, withSound: true, click: true })).join('')}</div>` : ''}
      </section>`;
    },
    'def-proof'(s) {
      const q1 = s.quote_lead
        ? `<blockquote class="def-quote"><div class="q">“${esc(s.quote_lead.text)}”</div><div class="a">${esc(s.quote_lead.attribution || '')}</div></blockquote>`
        : '';
      const q2 = s.quote_second
        ? `<blockquote class="def-quote"><div class="q">“${esc(s.quote_second.text)}”</div><div class="a">${
            s.quote_second.link
              ? `<a href="${esc(s.quote_second.link)}" target="_blank" rel="noopener noreferrer">${esc(s.quote_second.attribution || '')}</a>`
              : esc(s.quote_second.attribution || '')
          }</div></blockquote>`
        : '';
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${q1}
        ${s.body ? `<p>${esc(s.body)}</p>` : ''}
        ${s.deployment_line ? `<p class="def-deploy">${esc(s.deployment_line)}</p>` : ''}
        ${q2}
        <div class="def-pair">${(s.media || []).map((m) => plate(m.src, m.alt)).join('')}</div>
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
    'def-plainview'(s) {
      const m = s.media || {};
      const src = m.src ? mediaPath(m.src) : '';
      const cinema = src
        ? `<div class="cinema-block" data-reveal>
            <div class="cinema">
              <div class="cinema-media cinema-media--photo">
                <img src="${esc(src)}" alt="${esc(m.alt || '')}" loading="lazy" />
              </div>
            </div>
            ${m.caption ? `<div class="media-inner"><p class="cinema-cap">${esc(m.caption)}</p></div>` : ''}
          </div>`
        : '';
      return `<section class="section-block" id="${esc(s.id)}" data-reveal>
        <div class="shell-stage">
          ${kicker(s)}
          <h2 class="h2">${esc(s.title || '')}</h2>
        </div>
        ${cinema}
        <div class="shell-stage">
          ${blocksHtml(s.blocks)}
          ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
          ${s.source_line ? `<p class="def-fine">${esc(s.source_line)}</p>` : ''}
        </div>
      </section>`;
    },
    'def-atlantic'(s) {
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
        ${blocksHtml(s.blocks)}
        ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
        ${s.media ? plate(s.media.src, s.media.alt) : ''}
      </section>`;
    },
    'def-family'(s) {
      const ladder = `<div class="def-ladder">${(s.ladder || [])
        .map((item) => {
          const name = item.name || item.vessel || '';
          const line = item.defense_lens || item.line || '';
          const status = item.status || '';
          return `<div class="def-ladder-item">
          <img src="${esc(mediaPath(item.image))}" alt="${esc(name)}" loading="lazy" />
          <div class="meta">
            <div class="v">${esc(name)}${item.length_class ? ' · ' + esc(item.length_class) : ''}</div>
            ${status ? `<div class="status">${esc(status)}</div>` : ''}
            <div class="l">${esc(line)}</div>
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
    'def-industrial'(s) {
      const body = (Array.isArray(s.body) ? s.body : s.body ? [s.body] : []).map((p) => `<p>${esc(p)}</p>`).join('');
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        <div class="arch-prose">${body}</div>
        ${s.fine_print ? `<p class="def-fine">${esc(s.fine_print)}</p>` : ''}
        ${s.media ? plate(s.media.src, s.media.alt) : ''}
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
    const fn = R[s.id];
    if (fn) return fn(s);
    return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
      ${kicker(s)}
      ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
    </section>`;
  }

  const app = document.getElementById('app');
  app.innerHTML = [
    `<header class="nav"><div class="wrap nav-inner"><div class="brand"><span class="name">Navier</span><span class="tag">Defense</span></div></div></header>`,
    ...(D.sections || []).map(renderSection),
    `<footer class="def-footer shell-stage"><p>${esc(D.footer || '')}</p></footer>`,
  ].join('\n');

  function bindPlay(wrap) {
    const btn = wrap.querySelector('.film-play');
    const video = wrap.querySelector('video');
    const yt = wrap.getAttribute('data-yt-embed') || (wrap.closest && null);
    if (btn && video) {
      btn.addEventListener('click', function () {
        video.muted = !!video.hasAttribute('muted') && !video.hasAttribute('data-click-sound-film');
        if (video.hasAttribute('data-click-sound-film')) video.muted = false;
        video.controls = true;
        video.play().catch(function () {});
        btn.remove();
      });
    }
  }

  // Local click-to-play films
  document.querySelectorAll('.def-video-tile, [data-def-film]').forEach(bindPlay);

  // YouTube click-to-play: swap poster for iframe (figure tiles + invest film-card)
  document.querySelectorAll('[data-yt-embed]').forEach(function (el) {
    const url = el.getAttribute('data-yt-embed');
    if (!url) return;

    function playYt(e) {
      if (e) e.preventDefault();
      if (el.classList.contains('film-card')) {
        const media = el.querySelector('.film-media') || el;
        media.innerHTML = `<iframe src="${esc(url)}?autoplay=1&rel=0" title="video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>`;
        media.style.position = 'relative';
        media.style.aspectRatio = '16 / 9';
        el.classList.add('is-playing');
        return;
      }
      const frame = el.querySelector('.def-video-frame');
      if (!frame) return;
      frame.innerHTML = `<iframe src="${esc(url)}?autoplay=1&rel=0" title="video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>`;
    }

    if (el.classList.contains('film-card')) {
      el.addEventListener('click', playYt);
    } else {
      const btn = el.querySelector('.film-play');
      if (btn) btn.addEventListener('click', playYt);
    }
  });

  document.querySelectorAll('video[data-click-play]').forEach(function (v) {
    v.addEventListener('click', function () {
      if (v.paused) v.play().catch(function () {});
      else v.pause();
    });
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
})();
