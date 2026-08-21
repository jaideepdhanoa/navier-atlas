/**
 * Archetype page runtime (public-partners | fleet-investors).
 * Expects window.ARCHETYPE_DATA + window.EMPLOYER_HUB_DATA (map/trip via hub.js MAP_ONLY).
 * Renders authored copy/data verbatim; omits empty modules (fail-closed).
 */
(function () {
  const A = window.ARCHETYPE_DATA;
  const HUB = window.EMPLOYER_HUB_DATA;
  if (!A) {
    document.body.insertAdjacentHTML(
      'afterbegin',
      '<p style="padding:24px;color:#e0cb8f">Missing archetype data — rebuild the site.</p>'
    );
    return;
  }

  const isPartners = A.archetype === 'public-partners';
  const isInvest = A.archetype === 'fleet-investors';
  const contact = (HUB && HUB.market && HUB.market.contact_email) || 'jaideep@navierboat.com';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function money(n) {
    if (n == null || n === '') return '—';
    const x = Number(n);
    if (Number.isNaN(x)) return esc(n);
    return (
      '$' +
      Math.round(x).toLocaleString('en-US', { maximumFractionDigits: 0 })
    );
  }

  function moneyRange(arr) {
    if (!Array.isArray(arr) || arr.length < 2) return '—';
    return money(arr[0]) + '–' + money(arr[1]);
  }

  function section(id, title, innerHtml) {
    if (!innerHtml) return '';
    return `<section class="arch-section" id="${esc(id)}">
      <div class="wrap">
        ${title ? `<h2>${esc(title)}</h2>` : ''}
        ${innerHtml}
      </div>
    </section>`;
  }

  // —— Hero ——
  const hero = A.hero || {};
  const heroCopy = hero.copy || {};
  const headlineEl = document.getElementById('hero-headline');
  const subEl = document.getElementById('hero-sub');
  if (headlineEl) headlineEl.textContent = heroCopy.headline || '';
  if (subEl) subEl.textContent = heroCopy.subline || '';
  const heroCta = document.getElementById('hero-cta-primary');
  if (heroCta) {
    heroCta.textContent = isInvest ? 'Request fleet memo' : 'Start a conversation';
    heroCta.href = '#cta';
  }
  const navCta = document.getElementById('nav-cta');
  if (navCta) navCta.textContent = isInvest ? 'Request memo' : 'Get in touch';

  // —— Module HTML builders ——
  function renderPartnersModules() {
    const parts = [];

    // Shared About + Vessels (same media pack as fleet-investors)
    const aboutHtml = renderAboutNavier();
    if (aboutHtml) parts.push(aboutHtml);
    const vesselsHtml = renderVessels();
    if (vesselsHtml) parts.push(vesselsHtml);

    // Gap
    const gap = A.gap;
    if (gap && gap.copy) {
      let html = `<div class="arch-prose"><p class="lead">${esc(gap.copy.lead)}</p>`;
      if (gap.copy.support) html += `<p>${esc(gap.copy.support)}</p>`;
      if (gap.data && gap.data.source) {
        html += `<p class="assump-label">Source: <a href="${esc(gap.data.source)}" target="_blank" rel="noopener">${esc(gap.data.source)}</a></p>`;
      }
      html += '</div>';
      parts.push(section('story', 'The gap', html));
    }

    // Infrastructure-light
    const inf = A.infrastructure_light;
    if (inf && inf.copy) {
      let html = `<div class="arch-prose"><p class="lead">${esc(inf.copy.headline || '')}</p><p>${esc(inf.copy.body || '')}</p>`;
      const lv = inf.data && inf.data.landings_verified;
      if (lv && lv.stat_copy) {
        html += `<div class="stat-band"><div class="stat-card"><div class="stat">${esc(lv.stat_copy)}</div>`;
        if (lv.note) html += `<div class="src">${esc(lv.note)}</div>`;
        html += `</div></div>`;
      }
      html += '</div>';
      parts.push(section('infra', 'Infrastructure-light', html));
    }

    // Dual posture
    const posture = A.posture;
    if (posture && posture.copy) {
      const w = (posture.data && posture.data.weighting) || 'balanced';
      const enableFirst = w !== 'operate_dominant';
      const enableCard = `<div class="arch-card ${enableFirst ? 'emphasis' : ''}">
        <span class="arch-badge enable">Enable</span>
        <h3>Enable the network</h3>
        <p>${esc(posture.copy.enable_track)}</p>
      </div>`;
      const operateCard = `<div class="arch-card ${!enableFirst ? 'emphasis' : ''}">
        <span class="arch-badge operate">Operate</span>
        <h3>Operate the service</h3>
        <p>${esc(posture.copy.operate_track)}</p>
        ${
          posture.data && posture.data.operate_proof_points && posture.data.operate_proof_points.length
            ? `<ul class="pair-list">${posture.data.operate_proof_points
                .map(
                  (p) =>
                    `<li><strong>${esc(p.body || '')}</strong> — ${esc(p.proof || '')}</li>`
                )
                .join('')}</ul>`
            : ''
        }
      </div>`;
      const cards = enableFirst ? enableCard + operateCard : operateCard + enableCard;
      let html = '';
      if (posture.copy.framing) html += `<p class="lead">${esc(posture.copy.framing)}</p>`;
      html += `<div class="arch-grid-2">${cards}</div>`;
      parts.push(section('posture', 'Two ways to partner', html));
    }

    // Public value
    const pv = A.public_value;
    if (pv) {
      let html = '';
      if (pv.data && pv.data.stats && pv.data.stats.length) {
        html += `<div class="stat-band">${pv.data.stats
          .map((s) => {
            let src = '';
            if (s.source) {
              src = s.source.startsWith('http')
                ? `<a href="${esc(s.source)}" target="_blank" rel="noopener">Source</a>`
                : esc(s.source);
            }
            return `<div class="stat-card"><div class="stat">${esc(s.stat)}</div><div class="src">${src}${s.note ? ' · ' + esc(s.note) : ''}</div></div>`;
          })
          .join('')}</div>`;
      }
      if (pv.copy && pv.copy.pillars && pv.copy.pillars.length) {
        html += `<ul class="pillars">${pv.copy.pillars.map((p) => `<li>${esc(p)}</li>`).join('')}</ul>`;
      }
      if (html) parts.push(section('value', 'Public value', html));
    }

    // Speed-rule relief
    const srr = A.speed_rule_relief;
    if (srr && srr.copy) {
      let html = `<div class="arch-prose">
        <p class="lead">${esc(srr.copy.headline || '')}</p>
        <p>${esc(srr.copy.body || '')}</p>
        <p>${esc(srr.copy.invitation || '')}</p>
        <p>${esc(srr.copy.precedent || '')}</p>`;
      if (srr.data && srr.data.base_times_policy) {
        html += `<p class="assump-label">${esc(srr.data.base_times_policy)}</p>`;
      }
      html += `<details class="relief-box"><summary>What speed-rule relief unlocks</summary>`;
      if (srr.data && srr.data.relief_minutes != null) {
        html += `<p>${esc(String(srr.data.relief_minutes))}</p>`;
      } else {
        html += `<p>${esc(srr.copy.invitation || 'Relief is conditional on measurement and authority action — not assumed in map times.')}</p>`;
      }
      html += `</details></div>`;
      parts.push(section('speed-relief', 'Speed-rule relief', html));
    }

    // Plan alignment
    const plans = A.plan_alignment && A.plan_alignment.data && A.plan_alignment.data.plans;
    if (plans && plans.length) {
      const html = plans
        .map((p) => {
          let q = '';
          if (p.quote) q += `<blockquote>“${esc(p.quote)}”</blockquote>`;
          if (p.quote2) q += `<blockquote>“${esc(p.quote2)}”</blockquote>`;
          const src = p.source
            ? p.source.startsWith('http')
              ? `<a href="${esc(p.source)}" target="_blank" rel="noopener">${esc(p.plan || 'Source')}</a>`
              : esc(p.source)
            : esc(p.plan || '');
          return `<div class="quote-card">${q}<div class="meta">${src}${p.alignment ? ' · ' + esc(p.alignment) : ''}</div></div>`;
        })
        .join('');
      parts.push(section('plans', 'Plan alignment', html));
    }

    // Authorities
    const auth = A.authorities;
    if (auth && auth.data && auth.data.bodies && auth.data.bodies.length) {
      let html = auth.copy && auth.copy.intro ? `<p class="lead">${esc(auth.copy.intro)}</p>` : '';
      html += `<div class="arch-grid-2">${auth.data.bodies
        .map((b) => {
          const cls = (b.classification || '').toLowerCase();
          return `<div class="arch-card">
            <span class="arch-badge ${esc(cls)}">${esc(b.classification || '')}</span>
            <h3>${esc(b.body)}</h3>
            <p>${esc(b.role || '')}</p>
            ${b.engagement_window ? `<p class="assump-label">${esc(b.engagement_window)}</p>` : ''}
          </div>`;
        })
        .join('')}</div>`;
      if (auth.data.omitted_note) {
        html += `<p class="assump-label" style="margin-top:14px">${esc(auth.data.omitted_note)}</p>`;
      }
      parts.push(section('authorities', 'Authority landscape', html));
    }

    // Modal integration
    const modal = A.modal_integration;
    if (modal && modal.data && modal.data.pairs && modal.data.pairs.length) {
      let html = modal.copy && modal.copy.lead ? `<p class="lead">${esc(modal.copy.lead)}</p>` : '';
      html += `<ul class="pair-list">${modal.data.pairs
        .map(
          (p) =>
            `<li><strong>${esc(p.station)}</strong> → ${esc(p.connects || '')}${p.source ? ` <span class="assump-label">(${esc(p.source)})</span>` : ''}</li>`
        )
        .join('')}</ul>`;
      parts.push(section('modal', 'Modal integration', html));
    }

    // Flywheel
    const fw = A.flywheel && A.flywheel.copy;
    if (fw) {
      const html = `<div class="flywheel">
        <div class="wheel"><div class="n">1 · Employers</div><p>${esc(fw.employers || '')}</p></div>
        <div class="wheel"><div class="n">2 · Public partners</div><p>${esc(fw.public_partners || '')}</p></div>
        <div class="wheel"><div class="n">3 · Fleet investors</div><p>${esc(fw.fleet_investors || '')}</p></div>
      </div>`;
      parts.push(section('flywheel', 'How the pieces fit', html));
    }

    return parts.join('');
  }

  function statusChip(status) {
    if (!status) return '';
    const s = String(status);
    return `<span class="status-chip status-${esc(s)}">${esc(s.replace(/_/g, ' '))}</span>`;
  }

  function mediaUrl(path) {
    if (!path) return '';
    const p = String(path);
    if (/^https?:\/\//i.test(p) || p.startsWith('//')) return p;
    // Shared vessel assets ship at /employer-hub/assets/... and also copied beside each page
    if (p.startsWith('/employer-hub/')) return p;
    if (p.startsWith('/')) return p;
    return p;
  }

  function renderAboutNavier() {
    const about = A.about_navier;
    if (!about || !about.copy) return '';
    const demos = about.demos || [];
    let html = `<p class="lead about-lead">${esc(about.copy.body || '')}</p>`;
    if (demos.length) {
      html += `<div class="fi-demo-grid" data-fi-demos>${demos
        .map(
          (d) => `<figure class="fi-demo-tile">
          <video muted playsinline loop preload="metadata" poster="${esc(mediaUrl(d.poster || ''))}" data-autoplay-demo>
            <source src="${esc(mediaUrl(d.video || ''))}" type="video/mp4" />
          </video>
          <figcaption>${esc(d.label || '')}</figcaption>
        </figure>`
        )
        .join('')}</div>`;
    }
    return section('about_navier', about.title || 'About Navier', html);
  }

  function renderVessels() {
    const v = A.vessels;
    if (!v) return '';
    const loop = v.loop || {};
    const cards = v.cards || [];
    let html = '';
    if (v.copy && v.copy.headline) html += `<p class="lead">${esc(v.copy.headline)}</p>`;
    if (v.copy && v.copy.body) html += `<p>${esc(v.copy.body)}</p>`;
    if (loop.video) {
      html += `<div class="vessel-loop">
        <video class="vessel-loop-video" muted playsinline loop autoplay preload="metadata" poster="${esc(mediaUrl(loop.poster || ''))}">
          <source src="${esc(mediaUrl(loop.video))}" type="video/mp4" />
        </video>
      </div>`;
    }
    if (cards.length) {
      html += `<div class="vessel-row navier-vessel-cards">${cards
        .map((card) => {
          const bits = [];
          if (card.passengers != null) bits.push(card.passengers + ' passengers');
          if (card.propulsion) bits.push(card.propulsion);
          if (card.cruise_speed_kn) bits.push('~' + card.cruise_speed_kn + ' kn');
          if (card.capex_usd) bits.push(money(card.capex_usd));
          return `<div class="arch-card vessel-card">
            <div class="vessel-card-media"><img src="${esc(mediaUrl(card.image || ''))}" alt="${esc(card.model || '')}" loading="lazy" /></div>
            <h3>${esc(card.model || '')}</h3>
            ${bits.length ? `<p class="assump-label">${esc(bits.join(' · '))}</p>` : ''}
            ${card.blurb ? `<p>${esc(card.blurb)}</p>` : ''}
          </div>`;
        })
        .join('')}</div>`;
    }
    return section('vessels', v.title || 'Meet the vessels', html);
  }

  function renderBusinessModel() {
    const bm = A.business_model || A.shared_business_model;
    const layers = bm && bm.copy && bm.copy.layers;
    if (!layers || !layers.length) return '';
    let html = `<p class="lead">${esc(bm.copy.headline || '')}</p>`;
    if (bm.copy.body) html += `<p>${esc(bm.copy.body)}</p>`;
    html += `<div class="biz-layers">${layers
      .map(
        (L) => `<div class="arch-card biz-layer">
        <div class="biz-layer-top">
          <div class="biz-id">${esc(L.id || '')}</div>
          ${L.when ? `<div class="biz-when">${esc(L.when)}</div>` : ''}
        </div>
        <h3>${esc(L.title || '')}</h3>
        <p>${esc(L.body || '')}</p>
        <div class="biz-meta">
          ${L.yield ? `<span class="tech-chip">${esc(L.yield)}</span>` : ''}
          ${L.feeds ? `<span class="tech-chip">P&amp;L · ${esc(L.feeds)}</span>` : ''}
        </div>
      </div>`
      )
      .join('')}</div>`;
    if (bm.copy.bridge) html += `<p class="assump-label" style="margin-top:12px">${esc(bm.copy.bridge)}</p>`;
    return section('business_model', bm.title || 'How one hull earns', html);
  }

  function networkFeeAccordionHtml() {
    const nf = A.network_fee || A.shared_network_fee;
    if (!nf || !nf.copy || !nf.copy.items) return '';
    const items = nf.copy.items || [];
    return `<details class="fee-accordion">
      <summary>What the 10% network fee buys</summary>
      <p class="assump-label">${esc(nf.copy.callout || nf.copy.headline || '')}</p>
      <ul class="fee-list compact">${items
        .map((it) => `<li><strong>${esc(it.title || '')}</strong><span>${esc(it.body || '')}</span></li>`)
        .join('')}</ul>
    </details>`;
  }

  function renderServiceDay() {
    const sd = A.service_day;
    const windows = sd && sd.data && sd.data.windows;
    if (!windows || !windows.length) return '';
    const html = `<div class="service-day" role="list">
      ${windows
        .map(
          (w) => `<div class="service-window ${w.upside ? 'is-upside' : ''}" role="listitem">
          <div class="sw-time">${esc(w.time_range || '')}</div>
          <div class="sw-label">${esc(w.label || '')}</div>
          <div class="sw-layer">${esc(w.layer || '')}</div>
          ${w.note ? `<p class="assump-label">${esc(w.note)}</p>` : ''}
        </div>`
        )
        .join('')}
    </div>`;
    return section('service_day', sd.title || 'How one vessel earns across the day', html);
  }

  function demandValueCell(r) {
    if (r.value != null && String(r.value).trim() !== '') return esc(String(r.value));
    if (r.headcount != null && r.headcount !== '') {
      const n = Number(r.headcount);
      return Number.isFinite(n) ? '~' + n.toLocaleString('en-US') : esc(String(r.headcount));
    }
    return '';
  }

  function fnSup(fn) {
    if (!fn) return '';
    const key = String(fn);
    const num = key.replace(/^fn/i, '');
    return ` <sup class="fn-ref"><a href="#fn-${esc(num)}">${esc(num)}</a></sup>`;
  }

  function renderDemandPool() {
    const dp = A.demand_pool;
    if (!dp) return '';
    // standing_label must be top-level — _internal is stripped at build
    // Keep this short and muted; legal weight lives in footnotes.
    const standing = dp.standing_label || 'Indicative corridor demand — not commitments.';
    let html = `<p class="standing-label">${esc(standing)}${fnSup(dp.fn)}</p>`;

    const data = dp.data || {};
    const variant = data.table_variant === 'stop' ? 'stop' : 'employer';
    const rows = (data.rows || []).filter(function (r) {
      const hasValue = r.value != null && String(r.value).trim() !== '';
      const hasHead = r.headcount != null && r.headcount !== '';
      const hasNote = r.note != null && String(r.note).trim() !== '';
      return hasValue || hasHead || hasNote; // fail closed on empty rows
    });
    const COLLAPSE_AT = 5;
    const collapse = rows.length > COLLAPSE_AT;

    if (rows.length) {
      if (data.capture_assumption || data.headcount_label) {
        html += `<p class="assump-label">${
          data.capture_assumption ? esc('Capture assumption: ' + data.capture_assumption) : ''
        }${data.capture_assumption && data.headcount_label ? ' · ' : ''}${
          data.headcount_label ? esc(data.headcount_label) : ''
        }</p>`;
      }

      function rowClass(i) {
        return collapse && i >= COLLAPSE_AT ? ' class="demand-row-more"' : '';
      }

      let tableHtml = '';
      if (variant === 'stop') {
        tableHtml = `<table class="data-table demand-table">
          <thead><tr><th>Stop</th><th>Line(s)</th><th>Demand pool</th><th>Note</th></tr></thead>
          <tbody>${rows
            .map(function (r, i) {
              const demand = demandValueCell(r);
              const note = r.note ? esc(r.note) : '';
              return `<tr data-stop="${esc(r.node || '')}"${rowClass(i)}>
                <td>${esc(r.node || '')}${fnSup(r.fn)}</td>
                <td>${esc(Array.isArray(r.lines) ? r.lines.join(', ') : r.lines || '')}</td>
                <td>${demand || '—'}</td>
                <td class="assump-label">${note}</td>
              </tr>`;
            })
            .join('')}</tbody></table>`;
      } else {
        tableHtml = `<table class="data-table demand-table">
          <thead><tr><th>Employer</th><th>Stop</th><th>Line(s)</th><th>Demand pool</th></tr></thead>
          <tbody>${rows
            .map(function (r, i) {
              const demand = demandValueCell(r);
              const note = r.note
                ? `<div class="assump-label demand-note">${esc(r.note)}</div>`
                : '';
              const employer = r.employer || r.cluster || '';
              return `<tr data-stop="${esc(r.node || '')}"${rowClass(i)}>
                <td><div class="line-main">${esc(employer)}${fnSup(r.fn)}</div>${note}</td>
                <td>${esc(r.node || '')}</td>
                <td>${esc(Array.isArray(r.lines) ? r.lines.join(', ') : r.lines || '')}</td>
                <td>${demand || '—'}</td>
              </tr>`;
            })
            .join('')}</tbody></table>`;
      }

      const noun = variant === 'stop' ? 'stops' : 'employers';
      const moreCount = rows.length - COLLAPSE_AT;
      html += `<div class="demand-table-wrap${collapse ? ' is-collapsed' : ''}"${
        collapse ? ' data-demand-collapse' : ''
      }>
        <div style="overflow-x:auto">${tableHtml}</div>
        ${
          collapse
            ? `<button type="button" class="demand-expand-btn" aria-expanded="false">
            <span class="demand-expand-more">Show all ${rows.length} ${noun} (+${moreCount})</span>
            <span class="demand-expand-less">Show fewer</span>
          </button>`
            : ''
        }
      </div>`;

      if (data.city_total_seats != null) {
        html += `<p class="assump-label" style="margin-top:10px">City total (indicative): <strong>${esc(
          String(data.city_total_seats)
        )}</strong> seats${
          data.capture_assumption ? ' · ' + esc(data.capture_assumption) : ''
        }</p>`;
      }
      if (data.honesty_notes && data.honesty_notes.length) {
        html += `<ul class="pillars">${data.honesty_notes.map((n) => `<li>${esc(n)}</li>`).join('')}</ul>`;
      }
    }

    // Optional corridor cards only when no table rows
    const cards = dp.copy && dp.copy.cards;
    if ((!rows || !rows.length) && cards && cards.length) {
      html += `<div class="demand-cards arch-grid-2">${cards
        .map(
          (c) => `<div class="arch-card demand-card">
          <h3>${esc(c.title || '')}</h3>
          <p>${esc(c.body || '')}</p>
        </div>`
        )
        .join('')}</div>`;
    }

    if ((!rows || !rows.length) && !(cards && cards.length)) return '';
    return section('demand', dp.title || 'Who rides these corridors', html);
  }

  function renderFootnotes() {
    const fn = A.footnotes;
    if (!fn || typeof fn !== 'object') return '';
    const keys = Object.keys(fn).sort(function (a, b) {
      return String(a).localeCompare(String(b), undefined, { numeric: true });
    });
    if (!keys.length) return '';
    const html = `<ol class="footnote-list">${keys
      .map(function (k) {
        const item = fn[k];
        const text = typeof item === 'string' ? item : (item && item.text) || '';
        if (!text) return '';
        const num = String(k).replace(/^fn/i, '');
        return `<li id="fn-${esc(num)}"><span class="fn-key">${esc(num)}.</span> ${esc(text)}</li>`;
      })
      .filter(Boolean)
      .join('')}</ol>`;
    return section('footnotes', 'Notes & assumptions', html);
  }

  function renderPnlStudioShell() {
    const pnl = A.pnl;
    if (!pnl || !pnl.data) return '';
    const headline = (pnl.copy && (pnl.copy.headline || pnl.copy.body)) || '';
    let html = '';
    if (pnl.copy && pnl.copy.headline) html += `<p class="lead">${esc(pnl.copy.headline)}</p>`;
    if (pnl.copy && pnl.copy.body) html += `<p>${esc(pnl.copy.body)}</p>`;
    html += `<div class="pnl-studio" id="pnl-studio">
      <div class="pnl-sticky" id="pnl-sticky">
        <div class="pnl-metric"><div class="k">Payback · N45 Explorer</div><div class="v" id="pnl-m-payback">—</div></div>
        <div class="pnl-metric"><div class="k">Net / month</div><div class="v" id="pnl-m-net">—</div></div>
        <div class="pnl-metric"><div class="k">Gross / month</div><div class="v" id="pnl-m-gross">—</div></div>
        <div class="pnl-presets" id="pnl-presets" role="tablist" aria-label="Scenario presets"></div>
      </div>
      <div class="pnl-layout">
        <aside class="pnl-levers" id="pnl-levers" aria-label="P&L levers"></aside>
        <div class="pnl-statement-wrap">
          <div class="pnl-statement" id="pnl-statement" aria-live="polite"></div>
          <p class="assump-label" id="pnl-honesty">Payback is for a single <strong>N45 Explorer (~$2.5M)</strong>. Levers stay inside authored scenario bands. Upside lines never enter base totals unless toggled.</p>
        </div>
      </div>
    </div>`;
    return section('pnl', (pnl.copy && pnl.copy.title) || 'Economics — utilization stack', html);
  }

  function renderInvestModules() {
    const builders = {
      about_navier: renderAboutNavier,
      vessels: renderVessels,
      navier_intro: renderAboutNavier, // legacy slot → About
      business_model: renderBusinessModel,
      model: renderBusinessModel, // earning layers only (no roles)
      footnotes: renderFootnotes,
      asset: function () {
        const asset = A.asset;
        if (!asset || !asset.data) return '';
        const d = asset.data;
        let html = `<div class="scenario-hero">
          <div class="metric"><div class="k">Vessel</div><div class="v" style="font-size:18px">${esc(d.vessel || 'N45')}</div></div>
          <div class="metric"><div class="k">Capex</div><div class="v">${money(d.capex_usd)}</div></div>
          <div class="metric"><div class="k">Seats</div><div class="v">${esc(d.seats)}</div></div>
          <div class="metric"><div class="k">Cruise</div><div class="v">${esc(d.cruise_speed_kn)} kn</div></div>
        </div>
        <p class="assump-label">${esc(d.grade || '')}${d.powertrain ? ' · ' + esc(d.powertrain) : ''}${d.range_nm_approx ? ' · ~' + esc(d.range_nm_approx) + ' nm range' : ''}</p>`;
        if (asset.copy && asset.copy.redeployability) {
          html += `<div class="arch-card" style="margin-top:14px"><h3>Redeployability</h3><p>${esc(asset.copy.redeployability)}</p></div>`;
        }
        return section('asset', asset.title || 'The asset', html);
      },
      service_day: renderServiceDay,
      revenue_build: function () {
        return ''; // redundant with P&L qty × price lines
      },
      network_fee: function () {
        return ''; // demoted into P&L accordion
      },
      pnl: renderPnlStudioShell,
      demand_pool: renderDemandPool,
      fleet_phasing: function () {
        const fp = A.fleet_phasing && A.fleet_phasing.data;
        if (!fp) return '';
        let html = '';
        if (fp.launch) {
          html += `<div class="arch-card emphasis"><h3>Launch fleet</h3>
            <p>${moneyRange(fp.launch.capital_usd_range)} capital · ${Array.isArray(fp.launch.vessels_range) ? fp.launch.vessels_range.join('–') : esc(fp.launch.vessels_range)} vessels</p>
            <p class="assump-label">${esc(fp.launch.label || '')}</p></div>`;
        }
        if (fp.full_build) {
          html += `<div class="arch-card" style="margin-top:14px"><h3>Full build (illustrative)</h3>
            <p>${money(fp.full_build.capital_usd)} · ${esc(fp.full_build.vessels)} vessels</p>
            <p class="assump-label">${esc(fp.full_build.label || '')}</p></div>`;
        }
        if (fp.spares_note) html += `<p class="assump-label" style="margin-top:10px">${esc(fp.spares_note)}</p>`;
        return section('phasing', 'Fleet phasing', html);
      },
      protection_stack: function () {
        const prot = A.protection_stack && A.protection_stack.copy && A.protection_stack.copy.cards;
        if (!prot || !prot.length) return '';
        const html = `<div class="arch-grid-2">${prot
          .map((c) => `<div class="arch-card"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p></div>`)
          .join('')}</div>`;
        return section('protection', 'Protection stack', html);
      },
    };

    const skip = { hero: 1, network: 1, cta: 1 };
    // Brochure: About → Vessels → (network moved here in DOM) → Demand → Earn → Service day → P&L → Protection
    const brochureOrder = [
      'about_navier',
      'vessels',
      'demand_pool',
      'business_model',
      'service_day',
      'pnl',
      'fleet_phasing',
      'protection_stack',
      'footnotes',
    ];
    // Drop demoted / redundant modules from authored order
    const drop = {
      revenue_build: 1,
      network_fee: 1,
      navier_intro: 1, // replaced by about_navier + vessels
      model: 1, // replaced by business_model
      asset: 1,
    };
    let order = brochureOrder.slice();
    // Append any remaining authored sections that still have builders (except dropped)
    (A.section_order || []).forEach(function (id) {
      if (skip[id] || drop[id] || order.indexOf(id) >= 0) return;
      if (builders[id]) order.push(id);
    });

    const parts = [];
    const seen = {};
    order.forEach(function (id) {
      if (seen[id] || skip[id] || drop[id]) return;
      seen[id] = true;
      const fn = builders[id];
      if (fn) {
        const html = fn();
        if (html) parts.push(html);
      }
    });
    return parts.join('');
  }

  function initInvestPnl() {
    const studio = document.getElementById('pnl-studio');
    if (!studio || !window.FI_PNL_MODEL) return;
    const M = window.FI_PNL_MODEL;
    const model = M.buildModel(A);
    if (!model.hasRevenueBuild) return;
    let state = M.applyPreset(model, 'mid');

    const presetsEl = document.getElementById('pnl-presets');
    const leversEl = document.getElementById('pnl-levers');
    const statementEl = document.getElementById('pnl-statement');
    const rbLive = document.getElementById('revenue-build-live');

    function paintPresets() {
      if (!presetsEl) return;
      const items = [
        { id: 'conservative', label: 'Conservative' },
        { id: 'mid', label: 'Mid' },
        { id: 'upside', label: 'Upside' },
        { id: 'custom', label: 'Custom' },
      ];
      presetsEl.innerHTML = items
        .map(
          (p) =>
            `<button type="button" class="pnl-preset ${state.preset === p.id ? 'active' : ''}" data-preset="${p.id}" ${p.id === 'custom' && state.preset !== 'custom' ? 'disabled' : ''}>${esc(p.label)}</button>`
        )
        .join('');
      presetsEl.querySelectorAll('button[data-preset]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          const id = btn.getAttribute('data-preset');
          if (id === 'custom') return;
          state = M.applyPreset(model, id);
          paint();
        });
      });
    }

    function paintLevers() {
      if (!leversEl) return;
      let html = `<h3 class="pnl-levers-title">Key levers</h3>
        <p class="assump-label">Drag to change the inputs in the P&amp;L math — seats, prices, fill, and opex stay inside authored bands.</p>`;
      model.lineMetas.forEach(function (lm) {
        const t = state.lineT[lm.key] != null ? state.lineT[lm.key] : 0.5;
        const pct = Math.round(t * 100);
        const disp = M.leverDisplay(model, state, lm.key);
        html += `<label class="pnl-lever">
          <span class="pnl-lever-label">${esc(lm.label)}</span>
          <span class="pnl-lever-live" data-live-line="${esc(lm.key)}">${esc(disp.live)}</span>
          <input type="range" min="0" max="100" step="1" value="${pct}" data-line="${esc(lm.key)}" aria-valuetext="${esc(disp.live)}" />
          <span class="pnl-lever-ends"><span>${esc(disp.endLo)}</span><span>${esc(disp.endHi)}</span></span>
        </label>`;
      });
      const ox = M.opexDisplay(model, state);
      html += `<label class="pnl-lever">
        <span class="pnl-lever-label">Operating cost</span>
        <span class="pnl-lever-live" data-live-opex="1">${esc(ox.live)}</span>
        <input type="range" min="0" max="100" step="1" value="${Math.round((state.opexT || 0.5) * 100)}" data-opex="1" aria-valuetext="${esc(ox.live)}" />
        <span class="pnl-lever-ends"><span>${esc(ox.endLo)}</span><span>${esc(ox.endHi)}</span></span>
      </label>`;
      if (model.upside && model.upside.length) {
        html += `<div class="pnl-upside-toggles"><div class="pnl-lever-label">Upside layers</div>`;
        model.upside.forEach(function (u) {
          const on = !!(state.upsideOn && state.upsideOn[u.key]);
          const row = (u.byScenario && (u.byScenario.upside || u.byScenario.mid)) || {};
          const amt = row.subtotal_usd != null ? money(row.subtotal_usd) + '/mo' : '';
          html += `<label class="pnl-toggle"><input type="checkbox" data-upside="${esc(u.key)}" ${on ? 'checked' : ''}/> ${esc(u.label)}${amt ? ' · ' + amt : ''}</label>`;
        });
        html += `</div>`;
      }
      leversEl.innerHTML = html;
      leversEl.querySelectorAll('input[type="range"][data-line]').forEach(function (input) {
        input.addEventListener('input', function () {
          const key = input.getAttribute('data-line');
          state = M.markCustom(state);
          state.lineT[key] = Number(input.value) / 100;
          paint(true);
        });
      });
      const opexInput = leversEl.querySelector('input[data-opex]');
      if (opexInput) {
        opexInput.addEventListener('input', function () {
          state = M.markCustom(state);
          state.opexT = Number(opexInput.value) / 100;
          paint(true);
        });
      }
      leversEl.querySelectorAll('input[data-upside]').forEach(function (input) {
        input.addEventListener('change', function () {
          state = M.markCustom(state);
          state.upsideOn[input.getAttribute('data-upside')] = input.checked;
          paint(true);
        });
      });
    }

    function paintStatement(result, skipLevers) {
      const mPay = document.getElementById('pnl-m-payback');
      const mNet = document.getElementById('pnl-m-net');
      const mGross = document.getElementById('pnl-m-gross');
      if (mPay) mPay.textContent = result.paybackLabel;
      if (mNet) mNet.textContent = money(result.net);
      if (mGross) mGross.textContent = money(result.gross);

      if (rbLive) rbLive.innerHTML = '';

      if (statementEl) {
        statementEl.innerHTML = `
          <table class="data-table ue-table pnl-table">
            <thead><tr><th>P&amp;L (per vessel / month)</th><th class="num">Amount</th></tr></thead>
            <tbody>
              <tr class="section-row"><td colspan="2">Revenue</td></tr>
              ${result.revenueLines
                .map(
                  (r) =>
                    `<tr><td><div class="line-main">${esc(r.line)} ${statusChip(r.status)}</div>${r.note ? `<div class="assump-label">${esc(r.note)}</div>` : ''}<div class="assump-label">${esc(r.quantity || '')} · ${esc(r.price || '')}</div></td><td class="num">${money(r.subtotal_usd)}</td></tr>`
                )
                .join('')}
              <tr class="total"><td><strong>Gross revenue / month</strong></td><td class="num"><strong>${money(result.gross)}</strong></td></tr>
              <tr class="section-row"><td colspan="2">Operating cost</td></tr>
              ${result.opexLines
                .map(
                  (r) =>
                    `<tr><td><div class="line-main">${esc(r.line)} ${statusChip(r.status)}</div>${r.note ? `<div class="assump-label">${esc(r.note)}</div>` : ''}</td><td class="num">${money(r.amount)}</td></tr>`
                )
                .join('')}
              <tr class="total"><td><strong>Operating cost / month</strong></td><td class="num"><strong>${money(result.opex)}</strong></td></tr>
              <tr><td><div class="line-main">${esc((result.networkShare && result.networkShare.line) || 'Navier network share')}</div><div class="assump-label">${esc((result.networkShare && result.networkShare.value) || Math.round(result.sharePct * 100) + '% of gross')}</div>${networkFeeAccordionHtml()}</td><td class="num">(${money(result.networkShareAmt)})</td></tr>
              <tr class="emphasis"><td><strong>Net to investor / month</strong></td><td class="num"><strong>${money(result.net)}</strong></td></tr>
              <tr class="emphasis"><td><strong>Payback · N45 Explorer @ ${money(result.capex)}</strong></td><td class="num"><strong>${esc(result.paybackLabel)}</strong></td></tr>
              ${
                result.upsideLines.length
                  ? `<tr class="section-row upside"><td colspan="2">Upside (labeled — not in base)</td></tr>` +
                    result.upsideLines
                      .map(
                        (r) =>
                          `<tr class="upside ${r.enabled ? 'on' : 'off'}"><td><div class="line-main">${esc(r.line)} ${statusChip('upside')}</div><div class="assump-label">${esc(r.quantity || '')} · ${esc(r.price || '')}${r.enabled ? '' : ' · off'}</div></td><td class="num">${r.enabled ? money(r.subtotal_usd) : '—'}</td></tr>`
                      )
                      .join('')
                  : ''
              }
            </tbody>
          </table>`;
      }
      if (!skipLevers) {
        paintPresets();
        paintLevers();
      } else {
        paintPresets();
        // Update live parameter readouts without rebuilding inputs (keeps focus)
        model.lineMetas.forEach(function (lm) {
          const el = leversEl && leversEl.querySelector('[data-live-line="' + lm.key + '"]');
          if (el) el.textContent = M.leverDisplay(model, state, lm.key).live;
        });
        const oxEl = leversEl && leversEl.querySelector('[data-live-opex]');
        if (oxEl) oxEl.textContent = M.opexDisplay(model, state).live;
      }
    }

    function paint(fromLever) {
      const result = M.evaluate(model, state);
      paintStatement(result, !!fromLever);
    }

    paint(false);
    initDemoVideos();
  }

  function initDemoVideos() {
    if (!('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          const v = en.target;
          if (!(v instanceof HTMLVideoElement)) return;
          if (en.isIntersecting) {
            const p = v.play();
            if (p && p.catch) p.catch(function () {});
          } else {
            v.pause();
          }
        });
      },
      { threshold: 0.35 }
    );
    document.querySelectorAll('video[data-autoplay-demo], video.vessel-loop-video').forEach(function (v) {
      io.observe(v);
    });
  }

  function initDemandCollapse() {
    document.querySelectorAll('[data-demand-collapse]').forEach(function (wrap) {
      const btn = wrap.querySelector('.demand-expand-btn');
      if (!btn) return;
      btn.addEventListener('click', function () {
        const expanded = wrap.classList.toggle('is-collapsed') === false;
        // toggle returns whether class is now present; collapsed=false means expanded
        btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
      });
    });
  }

  const modulesEl = document.getElementById('archetype-modules');
  if (modulesEl) {
    modulesEl.innerHTML = isInvest ? renderInvestModules() : renderPartnersModules();
  }
  initDemandCollapse();
  // Place network map after vessels so About → Vessels → Network leads
  const networkEl = document.getElementById('network');
  const vesselsEl = document.getElementById('vessels');
  if (networkEl && vesselsEl && vesselsEl.parentNode) {
    vesselsEl.after(networkEl);
  }
  if (isInvest) {
    initInvestPnl();
  } else {
    initDemoVideos();
  }

  // CTA
  const cta = A.cta || {};
  const ctaCopy = cta.copy || {};
  const ctaData = cta.data || {};
  const intake = ctaData.intake || {};
  document.getElementById('cta-headline').textContent = ctaCopy.headline || 'Get in touch';
  document.getElementById('cta-body').textContent = ctaCopy.body || '';

  const fields = intake.fields || [];
  const formFields = document.getElementById('form-fields');
  const fieldDefs = fields.map((f) => {
    const raw = String(f);
    const [name, opts] = raw.split(':');
    return { name, opts: opts ? opts.split('|') : null };
  });
  // Always collect work email for intake
  if (!fieldDefs.some((f) => f.name === 'email')) {
    fieldDefs.splice(Math.min(2, fieldDefs.length), 0, { name: 'email', opts: null });
  }

  function labelize(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  if (formFields) {
    formFields.innerHTML = fieldDefs
      .map((f) => {
        const full = f.name === 'message' || f.name === 'corridors_of_interest' ? ' full' : '';
        if (f.opts) {
          return `<div class="field${full}"><label for="af-${esc(f.name)}">${esc(labelize(f.name))}</label>
            <select id="af-${esc(f.name)}" name="${esc(f.name)}" required>
              <option value="">Select…</option>
              ${f.opts.map((o) => `<option value="${esc(o)}">${esc(labelize(o))}</option>`).join('')}
            </select></div>`;
        }
        if (f.name === 'message') {
          return `<div class="field full"><label for="af-message">Message</label>
            <textarea id="af-message" name="message" rows="4"></textarea></div>`;
        }
        const type = f.name.includes('email') ? 'email' : 'text';
        return `<div class="field${full}"><label for="af-${esc(f.name)}">${esc(labelize(f.name))}</label>
          <input id="af-${esc(f.name)}" name="${esc(f.name)}" type="${type}" ${f.name === 'name' || f.name === 'authority_name' || f.name === 'entity' ? 'required' : ''} /></div>`;
      })
      .join('');
  }

  const form = document.getElementById('archetype-form');
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const tag = intake.tag || A.archetype || 'archetype';
    const email = String(fd.get('email') || '').trim();
    if (!email) {
      status.hidden = false;
      status.textContent = 'Please enter a work email.';
      return;
    }
    const payload = {
      name: fd.get('name') || fd.get('authority_name') || '',
      company: fd.get('entity') || fd.get('authority_name') || fd.get('agency_type') || '',
      role: fd.get('role') || fd.get('capital_type') || '',
      email,
      employees: fd.get('indicative_fleet_interest') || fd.get('posture_interest') || '',
      stop: '',
      stopLabel: fd.get('corridors_of_interest') || fd.get('cities_of_interest') || '',
      line: '',
      lineLabel: '',
      flavor: tag,
      flavorLabel: isInvest ? 'Fleet investor interest' : 'Public partner interest',
      cc: '',
      message: fd.get('message') || '',
      source: tag,
      hub_id: (HUB && HUB.id) || A.city || 'boston',
      hp: '',
    };

    const btn = document.getElementById('form-submit');
    const status = document.getElementById('form-status');
    const success = document.getElementById('form-success');
    btn.disabled = true;
    status.hidden = false;
    status.textContent = 'Sending…';
    success.classList.remove('show');

    try {
      const res = await fetch('/api/loi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      });
      let data = null;
      try {
        data = await res.json();
      } catch (_) {}
      if (res.ok && data && data.ok) {
        status.hidden = true;
        success.classList.add('show');
        success.innerHTML =
          '<strong>Received.</strong> Thanks — we have your note and will follow up.';
        form.reset();
        return;
      }
      // mailto fallback
      const subj = encodeURIComponent(
        `${isInvest ? 'Fleet investor' : 'Public partner'} interest — ${A.city || 'Boston'}`
      );
      const body = encodeURIComponent(
        Object.entries(Object.fromEntries(fd.entries()))
          .map(([k, v]) => `${k}: ${v}`)
          .join('\n') + `\n\nTag: ${tag}`
      );
      window.location.href = `mailto:${contact}?subject=${subj}&body=${body}`;
      success.classList.add('show');
      success.innerHTML =
        '<strong>Draft ready.</strong> Opening your mail client as backup.';
    } catch (err) {
      console.warn(err);
      status.textContent = 'Could not send — try emailing directly.';
    } finally {
      btn.disabled = false;
    }
  });

  // Contact links
  document.querySelectorAll('[data-contact-email]').forEach((a) => {
    a.href = 'mailto:' + contact;
    if (a.dataset.contactEmail === 'text') a.textContent = contact;
  });

  // Network titles for map section
  if (isPartners) {
    const nt = document.getElementById('network-title');
    const nl = document.getElementById('network-lead');
    if (nt) nt.textContent = 'The network';
    if (nl)
      nl.textContent =
        'Same corridors as the employer network — coverage without new ferry terminals. Find a ride and compare to driving.';
  }
  if (isInvest) {
    const nt = document.getElementById('network-title');
    const nl = document.getElementById('network-lead');
    if (nt) nt.textContent = 'Where the fleet works';
    if (nl)
      nl.textContent =
        'Same corridors employers will ride — utilization starts with real demand on real water. Find a ride and compare to driving.';
  }

  console.info('[archetype]', A.archetype, A.city);
})();
