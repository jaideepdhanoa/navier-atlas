/* Series B /invest — render authored contracts only */
(function () {
  'use strict';

  const D = window.INVEST_DATA;
  if (!D || !D.site) {
    document.getElementById('app').innerHTML =
      '<p style="padding:40px;color:#c8c8ce">INVEST_DATA missing.</p>';
    return;
  }

  const $ = (sel, el = document) => el.querySelector(sel);
  const esc = (s) =>
    String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  const nl = (s) => esc(s).replace(/\n/g, '<br/>');

  /* ── shell ─────────────────────────────────────────── */
  function brandMark() {
    return `<div class="inv-brand-mark" aria-hidden="true"><svg viewBox="9.5 9.5 160 160" fill="currentColor"><path d="M130.16 117.84 L120.18 135.12 A0.39 0.39 0 0 1 119.50 135.11 L68.16 44.06 A0.39 0.39 0 0 1 68.50 43.48 L88.22 43.48 A0.39 0.39 0 0 1 88.56 43.68 L130.16 117.46 A0.39 0.39 0 0 1 130.16 117.84 Z"/><path d="M132.68 111.67 L122.61 93.82 A0.55 0.55 0 0 1 122.62 93.28 L150.95 44.21 A0.55 0.55 0 0 1 151.90 44.21 L161.97 62.07 A0.55 0.55 0 0 1 161.96 62.61 L133.63 111.68 A0.55 0.55 0 0 1 132.68 111.67 Z"/><path d="M110.65 135.52 L90.76 135.52 A0.33 0.33 0 0 1 90.48 135.35 L48.97 61.75 A0.33 0.33 0 0 1 48.97 61.43 L59.03 44.00 A0.33 0.33 0 0 1 59.60 44.00 L110.93 135.03 A0.33 0.33 0 0 1 110.65 135.52 Z"/><path d="M26.53 134.96 L17.16 118.32 A0.67 0.67 0 0 1 17.16 117.66 L45.57 68.46 A0.67 0.67 0 0 1 46.74 68.46 L56.11 85.09 A0.67 0.67 0 0 1 56.11 85.75 L27.70 134.96 A0.67 0.67 0 0 1 26.53 134.96 Z"/></svg></div>`;
  }

  function renderNav() {
    const chapters = (D.site.nav && D.site.nav.chapters) || [];
    const links = chapters
      .map(
        (c) =>
          `<a href="#${esc(c.id)}" data-nav="${esc(c.id)}">${esc(c.label)}</a>`,
      )
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

  function renderHero() {
    const h = D.hero;
    const poster = h.video && h.video.poster;
    const bg = poster
      ? `url(${esc(poster)})`
      : `url(./assets/hero-n30-sunset.png)`;
    return `
    <header class="hero" id="hero">
      <div class="hero-media" style="background-image:${bg}">
        <img src="./assets/hero-n30-sunset.png" alt="" width="1600" height="900" fetchpriority="high" />
      </div>
      <div class="hero-scrim" aria-hidden="true"></div>
      <div class="hero-content wrap">
        <h1 class="hero-headline">${esc(h.headline)}</h1>
        <p class="hero-subline">${esc(h.subline)}</p>
        <div class="hero-actions">
          ${
            h.video
              ? `<button type="button" class="btn btn-primary" data-yt="${esc(
                  h.video.youtube_id || '',
                )}" data-embed="${esc(h.video.embed_url || '')}">${esc(
                  h.play_button_label || 'Watch the film',
                )}</button>`
              : ''
          }
        </div>
        <div class="scroll-cue" id="scroll-cue">${esc(
          (h.scroll_cue && h.scroll_cue.label) || 'Scroll',
        )}</div>
      </div>
    </header>`;
  }

  /* ── section renderers ─────────────────────────────── */
  const R = {
    'text-block'(s) {
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.body ? `<p class="body-text">${nl(s.body)}</p>` : ''}
        </div>`;
    },

    'two-panel-transition'(s) {
      return `
        <div class="section-block" data-reveal data-shift>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
          <div class="shift">
            <div class="shift-panel before">
              <div class="label">${esc(s.panel_before.label)}</div>
              <div class="line">${esc(s.panel_before.line)}</div>
              <div class="stats-line">${esc(s.panel_before.stats_line)}</div>
            </div>
            <div class="shift-panel after">
              <div class="label">${esc(s.panel_after.label)}</div>
              <div class="line">${esc(s.panel_after.line)}</div>
              <div class="stats-line">${esc(s.panel_after.stats_line)}</div>
            </div>
          </div>
          ${
            s.closing_line
              ? `<p class="closing-line">${nl(s.closing_line)}</p>`
              : ''
          }
        </div>`;
    },

    'pill-sequence'(s) {
      const pills = (s.pills || [])
        .map((p, i) => {
          const isNow = s.now_marker_on != null && i + 1 === s.now_marker_on;
          return `
          <div class="pill" data-pill="${i}">
            ${isNow ? `<span class="now-badge">${esc(s.now_label || 'NOW')}</span>` : ''}
            <div class="num">${esc(p.number)}</div>
            <div class="title">${esc(p.title)}</div>
            <div class="detail">${esc(p.detail)}</div>
            <div class="meta">${esc(p.program || '')} · ${esc(p.market || '')}</div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block" data-reveal data-pills data-now="${s.now_marker_on || 0}">
          ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
          <div class="pills">${pills}</div>
        </div>`;
    },

    'team-grid'(s) {
      const people = (s.people || [])
        .map(
          (p) => `
        <div class="person">
          <div class="name">${esc(p.name)}</div>
          <div class="role">${esc(p.role)}</div>
          <div class="creds">${esc(p.credentials)}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${nl(s.subhead)}</p>` : ''}
          <div class="team-grid">${people}</div>
          ${
            s.backers_line
              ? `<div class="backers"><div class="bl">${esc(
                  s.backers_label || 'BACKED BY',
                )}</div><div class="line">${nl(s.backers_line)}</div></div>`
              : ''
          }
        </div>`;
    },

    'flip-cards'(s) {
      const cards = (s.pairs || [])
        .map(
          (pair, i) => `
        <div class="flip-card" data-flip="${i}">
          <div class="flip-inner">
            <div class="flip-face front">
              <div class="t">${esc(pair.cost.title)}</div>
              <div class="b">${esc(pair.cost.body)}</div>
            </div>
            <div class="flip-face back">
              <div class="t">${esc(pair.lever.title)}</div>
              <div class="mech">${esc(pair.lever.mechanism)}</div>
              <div class="b">${esc(pair.lever.proof)}</div>
            </div>
          </div>
        </div>`,
        )
        .join('');
      const why = s.why_now
        ? `<div class="why-now">
            <h3 class="h3">${esc(s.why_now.title)}</h3>
            <p class="body-text">${nl(s.why_now.body || s.why_now.line || '')}</p>
            ${s.why_now.closing_line ? `<p class="closing-line">${esc(s.why_now.closing_line)}</p>` : ''}
          </div>`
        : '';
      return `
        <div class="section-block" data-reveal data-flip-section>
          ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          ${s.costs_kicker ? `<p class="kicker">${esc(s.costs_kicker)}</p>` : ''}
          ${s.flip_headline ? `<p class="eyebrow" style="margin-top:28px">${esc(s.flip_headline)}</p>` : ''}
          <div class="flip-grid">${cards}</div>
          ${why}
        </div>`;
    },

    'stat-counters'(s) {
      const stats = (s.stats || [])
        .map(
          (st) => `
        <div class="stat-card">
          <div class="value" data-counter="${esc(st.value)}">${esc(st.value)}</div>
          <div class="label">${esc(st.label)}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          <div class="media-plate"><img src="./assets/hero-n30-sunset.png" alt="" loading="lazy" /></div>
          <div class="stat-grid">${stats}</div>
        </div>`;
    },

    'video-grid'(s) {
      const clips = (s.clips || [])
        .map((c) => {
          const isLoop = c.play_mode === 'loop' && c.asset;
          const src = isLoop
            ? `./${esc(c.asset.replace(/^assets\//, 'assets/'))}`
            : null;
          // asset path may be assets/foo.mp4 relative to handoff — we ship as assets/
          const assetPath = c.asset
            ? './assets/' + c.asset.split('/').pop()
            : null;
          return `
          <div class="vcard ${isLoop ? 'looping' : ''}"
               data-yt="${esc(c.youtube_id || '')}"
               data-embed="${esc(c.embed_url || '')}"
               data-mode="${esc(c.play_mode || 'inline')}">
            <div class="vcard-media">
              ${
                isLoop && assetPath
                  ? `<video src="${assetPath}" muted playsinline loop autoplay preload="metadata"></video>`
                  : `<img src="${esc(c.poster || '')}" alt="" loading="lazy" />
                     <div class="play"><span>▶</span></div>`
              }
            </div>
            <div class="vcard-cap">${esc(c.caption || c.title || '')}</div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="video-grid">${clips}</div>
        </div>`;
    },

    timeline(s) {
      const stickySrc = (s.stat_chips || s.sticky_chips || s.chips || []).filter(
        (c) => c.sticky !== false,
      );
      const stickyHtml = stickySrc
        .map((c) => {
          if (typeof c === 'string') return `<span class="chip">${esc(c)}</span>`;
          const detail = c.detail ? ` · ${esc(c.detail)}` : '';
          return `<span class="chip">${esc(c.value || c.label || '')}${detail}</span>`;
        })
        .join('');
      const items = (s.milestones || s.years || [])
        .map((m) => {
          const lis = (m.items || [])
            .map((it) => `<li>${esc(it)}</li>`)
            .join('');
          return `
          <div class="tl-item">
            <div class="tl-year">${esc(m.year)}</div>
            <ul class="tl-items">${lis}</ul>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${stickyHtml ? `<div class="sticky-chips">${stickyHtml}</div>` : ''}
          ${s.kicker ? `<p class="kicker">${esc(s.kicker)}</p>` : ''}
          <div class="timeline-wrap"><div class="timeline">${items}</div></div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'hotspot-diagram'(s) {
      const hs = (s.hotspots || [])
        .map(
          (h) => `
        <div class="hotspot-item">
          <strong>${esc(h.label)}</strong>
          ${h.detail ? `<div class="muted">${esc(h.detail)}</div>` : ''}
        </div>`,
        )
        .join('');
      const vid = s.video
        ? `<button type="button" class="btn btn-ghost" data-yt="${esc(
            s.video.youtube_id || '',
          )}" data-embed="${esc(s.video.embed_url || '')}">${esc(
            s.video_label || 'Watch',
          )}</button>
           <div class="media-plate" style="margin-top:16px;cursor:pointer" data-yt="${esc(
             s.video.youtube_id || '',
           )}" data-embed="${esc(s.video.embed_url || '')}">
             <img src="${esc(s.video.poster || '')}" alt="" loading="lazy" />
           </div>`
        : '';
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.body ? `<p class="body-text">${nl(s.body)}</p>` : ''}
          <div class="hotspot-layout">
            <div>
              <div class="media-plate"><img src="./assets/s14-four-vessel-lineup.png" alt="" loading="lazy" /></div>
              ${vid}
            </div>
            <div class="hotspot-list">${hs}</div>
          </div>
        </div>`;
    },

    'platform-intro'(s) {
      const layers = (s.layers || [])
        .map(
          (l) => `
        <div class="layer">
          <div class="name">${esc(l.name)}</div>
          ${l.detail ? `<div class="detail">${esc(l.detail)}</div>` : ''}
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.body ? `<p class="body-text">${nl(s.body)}</p>` : ''}
          <div class="layers">${layers}</div>
          ${s.tagline ? `<p class="closing-line">${esc(s.tagline)}</p>` : ''}
        </div>`;
    },

    interactive(s) {
      if (s.component === 'vessel-ladder-explorer' || s.data === 'ladder.json') {
        return renderLadder(s);
      }
      if (s.component === 'unit-econ-toggle' || s.data === 'unitecon.json') {
        return renderUnitEcon(s);
      }
      if (s.component === 'pipeline-map' || s.data === 'pipeline-map.json') {
        return renderPipeline(s);
      }
      return `<div class="section-block" data-reveal><p class="muted">Interactive unavailable.</p></div>`;
    },

    'chapter-break'(s) {
      const vid = s.video
        ? `<button type="button" class="btn btn-primary" data-yt="${esc(
            s.video.youtube_id || '',
          )}" data-embed="${esc(s.video.embed_url || '')}">Play film · ${esc(
            s.video.duration || '',
          )}</button>
           <div class="media-plate" style="margin-top:24px;max-width:720px;margin-left:auto;margin-right:auto;cursor:pointer"
                data-yt="${esc(s.video.youtube_id || '')}" data-embed="${esc(s.video.embed_url || '')}">
             <img src="${esc(s.video.poster || '')}" alt="" loading="lazy" />
           </div>`
        : '';
      return `
        <div class="section-block chapter-break" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.headline ? `<p class="headline">${esc(s.headline)}</p>` : ''}
          ${vid}
        </div>`;
    },

    'stat-chips'(s) {
      const stats = (s.stats || [])
        .map(
          (st) => `
        <div class="stat-card">
          <div class="value">${esc(st.value)}</div>
          <div class="label">${esc(st.label)}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          <div class="stat-grid">${stats}</div>
        </div>`;
    },

    'two-door'(s) {
      const doors = (s.doors || [])
        .map(
          (d) => `
        <div class="door">
          <div class="title">${esc(d.title)}</div>
          <div class="detail">${esc(d.detail)}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="doors">${doors}</div>
          ${
            s.third_point
              ? `<div class="third-point"><strong>${esc(
                  s.third_point.title,
                )}</strong> — ${esc(s.third_point.detail)}</div>`
              : ''
          }
          ${
            s.atlantic_run
              ? `<div class="atlantic">${esc(s.atlantic_run.line || s.atlantic_run)}</div>`
              : ''
          }
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'comparison-table'(s) {
      const cols = s.columns || [];
      const labels = s.row_labels || [];
      const head = `<tr><th></th>${cols
        .map(
          (c) =>
            `<th class="${c.highlight ? 'hi' : ''}">${esc(c.name)}${
              c.vessel_type
                ? `<div style="font-size:10px;margin-top:4px;font-weight:500;normal-case;letter-spacing:0;text-transform:none;color:var(--text-2)">${esc(
                    c.vessel_type,
                  )}</div>`
                : ''
            }</th>`,
        )
        .join('')}</tr>`;
      const rows = labels
        .map((lab, ri) => {
          const cells = cols
            .map(
              (c) =>
                `<td class="${c.highlight ? 'hi' : ''}">${esc(
                  (c.values && c.values[ri]) || '',
                )}</td>`,
            )
            .join('');
          return `<tr><td class="row-label">${esc(lab)}</td>${cells}</tr>`;
        })
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="table-wrap"><table class="cmp"><thead>${head}</thead><tbody>${rows}</tbody></table></div>
        </div>`;
    },

    'signed-contract-hero'(s) {
      const stats = (s.stats || [])
        .map(
          (st) => `
        <div><div class="v">${esc(st.value)}</div><div class="l">${esc(st.label)}</div></div>`,
        )
        .join('');
      const press = (s.press || [])
        .map(
          (p) => `
        <div class="press-item">
          <div class="outlet">${esc(p.outlet)}</div>
          <div class="quote">${esc(p.quote)}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          <div class="contract-hero">
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            <div class="stats">${stats}</div>
            ${s.press_label ? `<p class="eyebrow">${esc(s.press_label)}</p>` : ''}
            <div class="press">${press}</div>
          </div>
        </div>`;
    },

    'program-panel'(s) {
      const stats = (s.stats || [])
        .map(
          (st) => `
        <div class="stat-card"><div class="value">${esc(st.value)}</div><div class="label">${esc(
          st.label,
        )}</div></div>`,
        )
        .join('');
      const chips = (s.proof_chips || [])
        .map(
          (c) => `
        <div class="proof-chip"><div class="label">${esc(c.label)}</div><div class="detail">${esc(
          c.detail,
        )}</div></div>`,
        )
        .join('');
      const buyers = (s.buyers || [])
        .map((b) => `<span>${esc(b)}</span>`)
        .join('');
      return `
        <div class="section-block" data-reveal>
          <div class="program-panel">
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            <div class="stat-grid">${stats}</div>
            <div class="proof-chips">${chips}</div>
            ${s.program_line ? `<p class="eyebrow">${esc(s.program_line)}</p>` : ''}
            <div class="buyers">${buyers}</div>
            ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
          </div>
        </div>`;
    },

    'stacked-cards'(s) {
      const cards = (s.cards || [])
        .map(
          (c) => `
        <div class="stack-card">
          <div class="num">${esc(c.number)}</div>
          <div><div class="h3" style="margin:0 0 6px">${esc(c.title)}</div>
          <div class="muted">${esc(c.body)}</div></div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          <div class="stack-cards">${cards}</div>
          ${s.formula_line ? `<div class="formula">${esc(s.formula_line)}</div>` : ''}
        </div>`;
    },

    'four-role-diagram'(s) {
      const roles = (s.roles || s.cards || [])
        .map((r) => {
          const title = r.title || r.name || r.role;
          const tag = r.tag ? `<div class="eyebrow" style="margin:0 0 6px">${esc(r.tag)}</div>` : '';
          const does = r.does || r.body || r.detail || r.description || '';
          const earns = r.earns ? `<div class="muted" style="margin-top:8px;color:var(--accent)">${esc(r.earns)}</div>` : '';
          return `<div class="role">${tag}<div class="title">${esc(title)}</div><div class="muted">${esc(
            does,
          )}</div>${earns}</div>`;
        })
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead || s.body || s.intro ? `<p class="lead">${esc(s.subhead || s.body || s.intro)}</p>` : ''}
          <div class="roles">${roles}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'drawing-chart'(s) {
      // cargo-gap uses chart.air / ocean / gap
      if (s.chart) {
        const c = s.chart;
        const cards = ['air', 'ocean', 'gap']
          .filter((k) => c[k])
          .map((k) => {
            const x = c[k];
            return `<div class="chip-card">
              <div class="t">${esc(x.label || k)}</div>
              ${x.price ? `<div class="value" style="font-family:Playfair Display,serif;font-size:1.4rem;color:var(--accent);margin:8px 0">${esc(x.price)}</div>` : ''}
              ${x.value ? `<div class="value" style="font-family:Playfair Display,serif;font-size:1.4rem;color:var(--ok);margin:8px 0">${esc(x.value)}</div>` : ''}
              <div class="b">${esc(x.time || x.detail || x.line || '')}</div>
              ${x.range_note ? `<div class="muted" style="margin-top:6px;font-size:12px">${esc(x.range_note)}</div>` : ''}
            </div>`;
          })
          .join('');
        return `
          <div class="section-block" data-reveal>
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            <div class="chips-3">${cards}</div>
            ${c.navier_band ? `<div class="formula">${esc(c.navier_band)}</div>` : ''}
            ${s.island_band ? `<p class="kicker">${esc(typeof s.island_band === 'string' ? s.island_band : s.island_band.line || '')}</p>` : ''}
          </div>`;
      }
      const bars = (s.bars || s.rows || [])
        .map((b, i) => {
          const pct = b.pct != null ? b.pct : b.percent != null ? b.percent : 40 + i * 15;
          return `
          <div class="bar-row" data-bar-pct="${pct}">
            <div class="meta"><span>${esc(b.label || b.name)}</span><span>${esc(
            b.value || '',
          )}</span></div>
            <div class="bar-track"><div class="bar-fill"></div></div>
          </div>`;
        })
        .join('');
      return `
        <div class="section-block" data-reveal data-bars>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          <div class="chart-block">${bars}</div>
        </div>`;
    },

    'three-chips'(s) {
      const chips = (s.chips || s.cards || [])
        .map(
          (c) => `
        <div class="chip-card">
          <div class="t">${esc(c.title || c.label)}</div>
          <div class="b">${esc(c.body || c.detail || '')}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead || s.intro ? `<p class="lead">${esc(s.subhead || s.intro)}</p>` : ''}
          <div class="chips-3">${chips}</div>
        </div>`;
    },

    'stat-panel'(s) {
      const stats = (s.stats || [])
        .map(
          (st) => `
        <div class="stat-card"><div class="value">${esc(st.value)}</div><div class="label">${esc(
          st.label,
        )}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.body || s.subhead || s.intro ? `<p class="lead">${esc(s.body || s.subhead || s.intro)}</p>` : ''}
          <div class="stat-grid">${stats}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'day-night-flip'(s) {
      // Contract may use chips[] instead of day/night panels
      if (s.chips && s.chips.length) {
        const chips = s.chips
          .map(
            (c) => `
          <div class="chip-card">
            <div class="t">${esc(c.title || c.label)}</div>
            <div class="b">${esc(c.body || c.detail || '')}</div>
          </div>`,
          )
          .join('');
        return `
          <div class="section-block" data-reveal>
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
            <div class="chips-3">${chips}</div>
          </div>`;
      }
      const day = s.day || (s.panels && s.panels.day) || s.left;
      const night = s.night || (s.panels && s.panels.night) || s.right;
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro || s.body ? `<p class="lead">${esc(s.intro || s.body)}</p>` : ''}
          <div class="daynight">
            <div class="dn-panel day">
              <div class="eyebrow">${esc((day && day.label) || 'DAY')}</div>
              <p class="body-text">${esc((day && (day.body || day.line || day.detail)) || '')}</p>
            </div>
            <div class="dn-panel night">
              <div class="eyebrow">${esc((night && night.label) || 'NIGHT')}</div>
              <p class="body-text">${esc((night && (night.body || night.line || night.detail)) || '')}</p>
            </div>
          </div>
        </div>`;
    },

    'card-row'(s) {
      const cards = (s.cards || s.chips || [])
        .map(
          (c) => `
        <div class="c"><div class="h3" style="margin:0 0 6px">${esc(
          c.title || c.label,
        )}</div><div class="muted">${esc(c.body || c.detail || '')}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.subhead || s.intro ? `<p class="lead">${esc(s.subhead || s.intro)}</p>` : ''}
          <div class="card-row">${cards}</div>
        </div>`;
    },

    'defense-panel'(s) {
      const blocks = (s.blocks || s.points || [])
        .map(
          (b) => `
        <div class="chip-card" style="margin-bottom:10px">
          <div class="t">${esc(b.title || '')}</div>
          <div class="b">${nl(b.body || b.detail || (typeof b === 'string' ? b : ''))}</div>
        </div>`,
        )
        .join('');
      const quote = s.pull_quote
        ? `<blockquote style="margin:20px 0;padding:16px 18px;border-left:3px solid var(--accent);color:var(--text-1);font-style:italic">
            ${esc(s.pull_quote.quote || '')}
            <div class="muted" style="margin-top:8px;font-style:normal">${esc(
              s.pull_quote.attribution || '',
            )}</div>
          </blockquote>`
        : '';
      return `
        <div class="section-block" data-reveal>
          <div class="defense-panel">
            ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
            ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
            ${s.intro ? `<p class="body-text">${esc(s.intro)}</p>` : ''}
            ${blocks}
            ${quote}
            ${s.deployment_line ? `<p class="closing-line">${esc(s.deployment_line)}</p>` : ''}
            ${s.fine_print ? `<p class="muted">${esc(s.fine_print)}</p>` : ''}
          </div>
        </div>`;
    },

    'horizontal-bars'(s) {
      const segs = s.segments || s.bars || s.markets || s.rows || [];
      const bars = segs
        .map((b, i) => {
          let pct = b.pct;
          if (pct == null && b.bar_value_range) {
            pct = Math.min(95, 25 + (b.bar_value_range[1] || b.bar_value_range[0] || 5) * 3);
          }
          if (pct == null) pct = Math.min(95, 28 + i * 14);
          const right = b.dollars_floor || b.vessels_floor || b.value || b.detail || '';
          const sub = b.demand_pool
            ? `<div class="muted" style="font-size:12px;margin-bottom:6px">${esc(b.demand_pool)}</div>`
            : '';
          return `
          <div class="bar-row" data-bar-pct="${pct}">
            <div class="meta"><span><strong>${esc(b.name || b.label || b.market || '')}</strong></span><span>${esc(
            right,
          )}</span></div>
            ${sub}
            <div class="bar-track"><div class="bar-fill"></div></div>
            ${
              b.vessels_floor
                ? `<div class="muted" style="font-size:12px;margin-top:4px">${esc(
                    b.vessels_floor,
                  )} vessels</div>`
                : ''
            }
          </div>`;
        })
        .join('');
      return `
        <div class="section-block" data-reveal data-bars>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="chart-block">${bars}</div>
          ${s.totals ? `<p class="closing-line">${esc(typeof s.totals === 'string' ? s.totals : JSON.stringify(s.totals))}</p>` : ''}
          ${s.source_line ? `<p class="muted">${esc(s.source_line)}</p>` : ''}
        </div>`;
    },

    'stat-band'(s) {
      const stats = (s.stats || [])
        .map(
          (st) => `
        <div class="stat-card"><div class="value">${esc(st.value)}</div><div class="label">${esc(
          st.label,
        )}</div></div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.subhead ? `<p class="lead">${esc(s.subhead)}</p>` : ''}
          <div class="stat-grid">${stats}</div>
          ${s.footnote ? `<p class="muted">${esc(s.footnote)}</p>` : ''}
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
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          <div class="roadmap">${cols}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'status-rows'(s) {
      const rows = (s.rows || [])
        .map(
          (r) => `
        <div class="status-row">
          <div class="label">${esc(r.label)}</div>
          <div class="status">${esc(r.status)}</div>
        </div>`,
        )
        .join('');
      return `
        <div class="section-block" data-reveal>
          ${s.title ? `<h2 class="h2">${esc(s.title)}</h2>` : ''}
          ${s.intro ? `<p class="lead">${esc(s.intro)}</p>` : ''}
          <div class="status-rows">${rows}</div>
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
        <div class="section-block" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow">${esc(s.eyebrow)}</p>` : ''}
          ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
          <div class="round">${cols}</div>
          ${s.closing_line ? `<p class="closing-line">${esc(s.closing_line)}</p>` : ''}
        </div>`;
    },

    'finale-plate'(s) {
      return `
        <section class="finale" id="finale" data-reveal>
          <div class="finale-inner">
            <p class="h">${esc(s.headline)}</p>
            <p class="mark">${esc(s.closing_mark || 'OWN THE EDGE')}</p>
            ${
              s.cta
                ? `<a class="btn btn-primary" href="${esc(s.cta.href)}">${esc(
                    s.cta.label,
                  )}</a>`
                : ''
            }
          </div>
        </section>`;
    },

    footer(s) {
      // go-deeper
      return `
        <section class="go-deeper chapter" id="go-deeper">
          <div class="wrap">
            <p class="chapter-label">${esc(s.title || 'Go deeper')}</p>
            <div class="go-deeper-grid">
              <div class="vance-card" data-yt="${esc(
                (s.video && s.video.youtube_id) || '',
              )}" data-embed="${esc((s.video && s.video.embed_url) || '')}">
                <img src="${esc((s.video && s.video.poster) || '')}" alt="" loading="lazy" />
                <div class="cap">${esc(s.video_label || (s.video && s.video.title) || '')}</div>
              </div>
              <div>
                ${
                  s.contact
                    ? `<a class="btn btn-primary" href="${esc(s.contact.href)}">${esc(
                        s.contact.label,
                      )}</a>`
                    : ''
                }
                <p class="muted" style="margin-top:20px">Privileged &amp; Confidential · Distribution without consent is strictly prohibited · © 2026 Navier</p>
              </div>
            </div>
          </div>
        </section>`;
    },
  };

  function renderLadder(s) {
    const hulls = (D.ladder && D.ladder.hulls) || [];
    const tabs = hulls
      .map(
        (h, i) =>
          `<button type="button" class="ladder-tab ${i === 0 ? 'active' : ''}" data-hull="${i}">${esc(
            h.name,
          )}</button>`,
      )
      .join('');
    return `
      <div class="section-block" data-reveal>
        ${s.headline ? `<h2 class="h2">${esc(s.headline)}</h2>` : ''}
        <div class="ladder" id="ladder">
          <div class="ladder-tabs">${tabs}</div>
          <div class="ladder-body">
            <div class="ladder-sil" aria-hidden="true"></div>
            <div class="ladder-meta" id="ladder-meta"></div>
          </div>
        </div>
      </div>`;
  }

  function renderUnitEcon(s) {
    const u = D.unitecon;
    if (!u) return '';
    const tabs = (u.panels || [])
      .map(
        (p, i) =>
          `<button type="button" class="ue-tab ${i === 0 ? 'active' : ''}" data-ue="${i}">${esc(
            p.class_label,
          )}</button>`,
      )
      .join('');
    return `
      <div class="section-block" data-reveal>
        ${u.eyebrow ? `<p class="eyebrow">${esc(u.eyebrow)}</p>` : ''}
        ${u.title ? `<h2 class="h2">${esc(u.title)}</h2>` : ''}
        <div class="unitecon" id="unitecon">
          <div class="ue-tabs">${tabs}</div>
          <div class="ue-body" id="ue-body"></div>
        </div>
      </div>`;
  }

  function renderPipeline(s) {
    const p = D['pipeline-map'];
    if (!p) return '';
    const stats = (p.gold_stats || [])
      .map(
        (st) => `
      <div class="s"><div class="v">${esc(st.value)}</div><div class="l">${esc(st.label)}</div></div>`,
      )
      .join('');
    const tiers = (p.tiers || [])
      .map((t) => {
        const rows = (t.rows || [])
          .map(
            (r) => `
          <div class="pipe-row"><div class="party">${esc(r.party)}</div><div class="status">${esc(
            r.status,
          )}</div></div>`,
          )
          .join('');
        return `<div class="pipe-tier"><h3>${esc(t.name)}</h3>${rows}</div>`;
      })
      .join('');
    return `
      <div class="section-block" data-reveal>
        ${p.eyebrow ? `<p class="eyebrow">${esc(p.eyebrow)}</p>` : ''}
        ${p.title ? `<h2 class="h2">${esc(p.title)}</h2>` : ''}
        <div class="pipeline">
          <div class="pipe-stats">${stats}</div>
          <div class="pipe-map-plate" role="img" aria-label="Global coverage map"></div>
          ${tiers}
          <div class="pipe-foot">
            ${p.coverage_line ? `<div>${esc(p.coverage_line)}</div>` : ''}
            ${p.capital_efficiency_line ? `<div style="margin-top:8px;color:var(--accent)">${esc(p.capital_efficiency_line)}</div>` : ''}
          </div>
        </div>
      </div>`;
  }

  function renderChapter(key, data) {
    if (!data) return '';
    const sections = (data.sections || [])
      .map((sec) => {
        // finale and go-deeper handled specially for layout
        if (sec.type === 'finale-plate') return R['finale-plate'](sec);
        if (sec.type === 'footer') return R.footer(sec);
        const fn = R[sec.type];
        if (!fn) {
          // generic fallback: title + body fields
          return `
            <div class="section-block" data-reveal>
              ${sec.eyebrow ? `<p class="eyebrow">${esc(sec.eyebrow)}</p>` : ''}
              ${sec.title || sec.headline ? `<h2 class="h2">${esc(sec.title || sec.headline)}</h2>` : ''}
              ${sec.subhead || sec.body || sec.intro ? `<p class="lead">${nl(sec.subhead || sec.body || sec.intro)}</p>` : ''}
              ${sec.closing_line ? `<p class="closing-line">${esc(sec.closing_line)}</p>` : ''}
            </div>`;
        }
        return fn(sec);
      })
      .join('');

    // money: finale/go-deeper are full-bleed — separate from wrap
    if (key === 'money') {
      const main = (data.sections || []).filter(
        (s) => s.type !== 'finale-plate' && s.type !== 'footer',
      );
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
          <div class="wrap">
            <p class="chapter-label">${esc(data.chapter_label || '')}</p>
            ${mainHtml}
          </div>
          ${finale ? R['finale-plate'](finale) : ''}
          ${foot ? R.footer(foot) : ''}
        </section>`;
    }

    return `
      <section class="chapter" id="${esc(key)}">
        <div class="wrap">
          <p class="chapter-label">${esc(data.chapter_label || '')}</p>
          ${sections}
        </div>
      </section>`;
  }

  /* ── mount ─────────────────────────────────────────── */
  const app = document.getElementById('app');
  app.innerHTML = `
    ${renderNav()}
    ${renderHero()}
    ${renderChapter('claim', D.claim)}
    ${renderChapter('proof', D.proof)}
    ${renderChapter('product', D.product)}
    ${renderChapter('gtm', D.gtm)}
    ${renderChapter('money', D.money)}
    <footer class="site-footer">
      <div class="wrap">${esc(
        (D.site.footer && D.site.footer.confidentiality_line) || '',
      )}</div>
    </footer>
    <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video">
      <div class="lightbox-inner">
        <button type="button" class="lightbox-close" id="lb-close" aria-label="Close">×</button>
        <div id="lb-frame"></div>
      </div>
    </div>
  `;

  /* ── interactivity ─────────────────────────────────── */
  function openYt(embedUrl, youtubeId) {
    const url =
      embedUrl ||
      (youtubeId
        ? `https://www.youtube-nocookie.com/embed/${youtubeId}?autoplay=1&rel=0`
        : null);
    if (!url) return;
    const src = url.includes('?') ? `${url}&autoplay=1` : `${url}?autoplay=1&rel=0`;
    const lb = $('#lightbox');
    $('#lb-frame').innerHTML = `<iframe src="${esc(
      src,
    )}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen title="Video"></iframe>`;
    lb.classList.add('open');
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
    const t = e.target.closest('[data-yt], [data-embed]');
    if (!t) return;
    const yt = t.getAttribute('data-yt');
    const emb = t.getAttribute('data-embed');
    if (yt || emb) {
      e.preventDefault();
      openYt(emb, yt);
    }
  });

  // Ladder
  const hulls = (D.ladder && D.ladder.hulls) || [];
  function setHull(i) {
    const h = hulls[i];
    if (!h) return;
    document.querySelectorAll('.ladder-tab').forEach((el, j) => {
      el.classList.toggle('active', j === i);
    });
    const meta = $('#ladder-meta');
    if (!meta) return;
    meta.innerHTML = `
      <div class="name">${esc(h.name)}</div>
      <div class="class">${esc(h.length_class || '')}</div>
      <div class="mission">${esc(h.mission || '')}</div>
      ${h.status_chip ? `<div class="status">${esc(h.status_chip)}</div>` : ''}
      ${h.detail ? `<div class="detail">${esc(h.detail)}</div>` : ''}
    `;
  }
  document.querySelectorAll('.ladder-tab').forEach((el) => {
    el.addEventListener('click', () => setHull(+el.dataset.hull));
  });
  if (hulls.length) setHull(0);

  // Unit econ
  const panels = (D.unitecon && D.unitecon.panels) || [];
  const rowLabels = (D.unitecon && D.unitecon.row_labels) || [];
  function setUe(i) {
    const p = panels[i];
    if (!p) return;
    document.querySelectorAll('.ue-tab').forEach((el, j) => {
      el.classList.toggle('active', j === i);
    });
    const body = $('#ue-body');
    if (!body) return;
    const el = p.electric;
    const di = p.diesel;
    const rows = rowLabels
      .map((lab, ri) => {
        return `
        <div class="muted" style="padding:8px 0;border-bottom:1px solid var(--line)">${esc(lab)}</div>
        <div style="padding:8px 0;border-bottom:1px solid var(--line);font-weight:600;color:var(--ok)">${esc(
          (el.values && el.values[ri]) || '',
        )}</div>
        <div style="padding:8px 0;border-bottom:1px solid var(--line)">${esc(
          (di.values && di.values[ri]) || '',
        )}</div>`;
      })
      .join('');
    body.innerHTML = `
      <div class="ue-cols">
        <div class="head">Line</div>
        <div class="head">${esc(el.name)}</div>
        <div class="head">${esc(di.name)}</div>
        ${rows}
      </div>
      <div class="ue-punch">${esc(p.punchline || '')}</div>
      <ul class="ue-notes">${(D.unitecon.footnotes || [])
        .map((f) => `<li>${esc(f)}</li>`)
        .join('')}</ul>
    `;
  }
  document.querySelectorAll('.ue-tab').forEach((el) => {
    el.addEventListener('click', () => setUe(+el.dataset.ue));
  });
  if (panels.length) setUe(0);

  /* ── scroll motion ─────────────────────────────────── */
  const progress = $('#inv-progress');
  const scrollCue = $('#scroll-cue');
  const navLinks = [...document.querySelectorAll('[data-nav]')];
  const chapterIds = ((D.site.nav && D.site.nav.chapters) || []).map((c) => c.id);

  function onScroll() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
    if (progress) progress.style.width = pct + '%';
    if (scrollCue && window.scrollY > 80) scrollCue.classList.add('hidden');

    // active nav
    let active = chapterIds[0];
    for (const id of chapterIds) {
      const el = document.getElementById(id);
      if (el && el.getBoundingClientRect().top <= 120) active = id;
    }
    navLinks.forEach((a) => {
      a.classList.toggle('active', a.dataset.nav === active);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // IntersectionObserver reveals
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');

        // pills light sequentially
        if (en.target.dataset.pills != null) {
          const pills = en.target.querySelectorAll('.pill');
          const now = +(en.target.dataset.now || 0);
          pills.forEach((p, i) => {
            setTimeout(() => {
              p.classList.add('lit');
              if (i + 1 === now) p.classList.add('now');
            }, i * 160);
          });
        }

        // flip cards
        if (en.target.dataset.flipSection != null) {
          en.target.querySelectorAll('.flip-card').forEach((c, i) => {
            setTimeout(() => c.classList.add('flipped'), 400 + i * 280);
          });
        }

        // bars
        if (en.target.dataset.bars != null) {
          en.target.querySelectorAll('.bar-row').forEach((row) => {
            const pct = row.dataset.barPct || 50;
            const fill = row.querySelector('.bar-fill');
            if (fill) requestAnimationFrame(() => {
              fill.style.width = pct + '%';
            });
          });
        }
      });
    },
    { threshold: 0.18, rootMargin: '0px 0px -8% 0px' },
  );
  document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));
})();
