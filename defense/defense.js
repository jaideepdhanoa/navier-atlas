/**
 * /defense capability brief — render authored defense.json only.
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
    if (/^https?:\/\//i.test(src) || src.startsWith('/')) return src;
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

  function teamCard(p) {
    let src = '';
    const cards = TEAM_ASSETS;
    for (const [k, v] of Object.entries(cards)) {
      if (
        p.name &&
        (k.toLowerCase().includes(p.name.toLowerCase().split(' ').pop().toLowerCase()) ||
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
        <video class="def-hero-video hero-video" muted playsinline loop ${reduceMotion ? '' : 'autoplay'} preload="metadata" data-lazy-video>
          <source src="${esc(mediaPath(v.src))}" type="video/mp4" />
        </video>
        <div class="shell-stage" style="padding-top:28px;padding-bottom:36px">
          ${kicker(s)}
          <h1 class="h1">${esc(s.title || '')}</h1>
          ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
        </div>
      </section>`;
    },
    'def-about'(s) {
      const body = (s.body || []).map((p) => `<p>${esc(p)}</p>`).join('');
      const film = s.film || {};
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        <div class="arch-prose">${body}</div>
        ${s.media ? plate(s.media.src, s.media.alt) : ''}
        ${
          film.src
            ? `<div class="def-film-wrap" data-def-film>
          <video playsinline preload="metadata" poster="" data-click-sound-film>
            <source src="${esc(mediaPath(film.src))}" type="video/mp4" />
          </video>
          <button type="button" class="film-play" aria-label="Play ${esc(film.title || 'film')}">
            <span class="film-play-btn" aria-hidden="true">▶</span>
          </button>
          ${film.title ? `<p class="muted" style="margin-top:10px">${esc(film.title)}${film.duration ? ' · ' + esc(film.duration) : ''}</p>` : ''}
        </div>`
            : ''
        }
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
    'def-platform'(s) {
      const pair = (s.media_pair || [])
        .map(function (m) {
          if (m.type === 'video') {
            return `<figure class="def-plate"><video muted playsinline controls preload="metadata" data-click-play>
              <source src="${esc(mediaPath(m.src))}" type="video/mp4" /></video></figure>`;
          }
          return plate(m.src, m.alt);
        })
        .join('');
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        <p>${esc(s.body || '')}</p>
        <div class="def-pair">${pair}</div>
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
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${s.sub ? `<p class="lead">${esc(s.sub)}</p>` : ''}
        ${specs}${missions}${media}
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
      return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
        ${kicker(s)}
        <h2 class="h2">${esc(s.title || '')}</h2>
        ${plate(m.src, m.alt, m.caption)}
        ${blocksHtml(s.blocks)}
        ${s.closer ? `<p class="def-closer">${esc(s.closer)}</p>` : ''}
        ${s.source_line ? `<p class="def-fine">${esc(s.source_line)}</p>` : ''}
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
        .map(
          (item) => `<div class="def-ladder-item">
          <img src="${esc(mediaPath(item.image))}" alt="${esc(item.vessel)}" loading="lazy" />
          <div class="meta"><div class="v">${esc(item.vessel)}</div><div class="l">${esc(item.line)}</div></div>
        </div>`
        )
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
      const body = (s.body || []).map((p) => `<p>${esc(p)}</p>`).join('');
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
          ${
            sam
              ? `<div class="team-featured">${teamCard(sam)}</div>`
              : ''
          }
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
    // generic fallback
    return `<section class="section-block shell-stage" id="${esc(s.id)}" data-reveal>
      ${kicker(s)}
      ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
      ${s.body ? `<p>${esc(Array.isArray(s.body) ? s.body.join(' ') : s.body)}</p>` : ''}
    </section>`;
  }

  const app = document.getElementById('app');
  const html = [
    `<header class="nav"><div class="wrap nav-inner"><div class="brand"><span class="name">Navier</span><span class="tag">Defense</span></div></div></header>`,
    ...(D.sections || []).map(renderSection),
    `<footer class="def-footer shell-stage"><p>${esc(D.footer || '')}</p></footer>`,
  ].join('\n');
  app.innerHTML = html;

  // Click-to-play launch film WITH sound
  document.querySelectorAll('[data-def-film]').forEach(function (wrap) {
    const video = wrap.querySelector('video');
    const btn = wrap.querySelector('.film-play');
    if (!video || !btn) return;
    btn.addEventListener('click', function () {
      video.muted = false;
      video.controls = true;
      const p = video.play();
      if (p && p.catch) p.catch(function () {});
      btn.remove();
    });
  });
  // Click-to-play muted comparison clips
  document.querySelectorAll('video[data-click-play]').forEach(function (v) {
    v.addEventListener('click', function () {
      if (v.paused) v.play().catch(function () {});
      else v.pause();
    });
  });

  // Autoplay muted hero / lazy videos
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          const v = en.target;
          if (!(v instanceof HTMLVideoElement) || reduceMotion) return;
          if (v.hasAttribute('data-click-sound-film')) return;
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
