/**
 * Archetype runtime — contract v3 (keeps all v2 wins).
 * G1 sticky nav · G2 image/video · G3 navier_intro · G4 service_day ·
 * G5 revenue_build · G6 no self-owns · G7 section_order + reference expanders ·
 * G8 footnotes/P&L/status chips/role cards/speed expander · G9 kill-scan QA.
 *
 * Expects window.ARCHETYPE_DATA + window.EMPLOYER_HUB_DATA (map via hub.js MAP_ONLY).
 * NEVER render _-prefixed fields or naked source_url in body copy.
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
  const FOOTNOTES = A.footnotes && typeof A.footnotes === 'object' ? A.footnotes : {};
  /** @type {Set<string>} */
  const usedFn = new Set();

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
    return '$' + Math.round(x).toLocaleString('en-US', { maximumFractionDigits: 0 });
  }

  function moneyRangeLoose(low, high) {
    if (low == null && high == null) return null;
    if (low == null) return money(high);
    if (high == null) return money(low);
    if (low === high) return money(low);
    return money(low) + '–' + money(high);
  }

  function moneyRange(arr) {
    if (!Array.isArray(arr) || arr.length < 2) return '—';
    return money(arr[0]) + '–' + money(arr[1]);
  }

  function fnNumber(key) {
    const keys = Object.keys(FOOTNOTES);
    const i = keys.indexOf(key);
    return i >= 0 ? i + 1 : String(key).replace(/^fn/i, '');
  }

  function fnMark(key) {
    if (!key || !FOOTNOTES[key]) return '';
    usedFn.add(key);
    return `<sup class="fn-ref"><a href="#fn-${esc(key)}" id="fnref-${esc(key)}">${fnNumber(key)}</a></sup>`;
  }

  function statusChip(status) {
    if (!status) return '';
    const s = String(status).toLowerCase();
    let cls = 'status-modeled';
    let label = String(status).replace(/_/g, ' ').toUpperCase();
    if (s === 'market_priced' || s === 'market-priced') {
      cls = 'status-market';
      label = 'MARKET-PRICED';
    } else if (s === 'upside') {
      cls = 'status-upside';
      label = 'UPSIDE';
    } else if (s === 'modeled') {
      cls = 'status-modeled';
      label = 'MODELED';
    }
    return `<span class="status-chip ${cls}">${esc(label)}</span>`;
  }

  function domainChip(url) {
    if (!url || typeof url !== 'string' || !/^https?:\/\//i.test(url)) return '';
    try {
      const host = new URL(url).hostname.replace(/^www\./, '');
      return `<a class="domain-chip" href="${esc(url)}" target="_blank" rel="noopener">${esc(host)}</a>`;
    } catch (_) {
      return '';
    }
  }

  function withText(fnKey, text) {
    if (text == null || text === '') return '';
    return `${esc(text)}${fnMark(fnKey)}`;
  }

  function youtubeEmbed(url) {
    if (!url) return '';
    let src = String(url).trim();
    // normalize watch?v= to embed/
    const m = src.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([A-Za-z0-9_-]+)/);
    if (m) src = `https://www.youtube.com/embed/${m[1]}`;
    if (!/youtube\.com\/embed\//.test(src)) return '';
    return `<div class="video-embed">
      <iframe src="${esc(src)}" title="Navier vessel" loading="lazy"
        allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>
    </div>`;
  }

  function imgTag(src, alt, cls) {
    if (!src) return '';
    return `<img class="${esc(cls || '')}" src="${esc(src)}" alt="${esc(alt || '')}" loading="lazy" />`;
  }

  function sectionShell(id, title, innerHtml, opts) {
    if (!innerHtml) return '';
    const lead = opts && opts.lead ? `<p class="section-lead">${opts.lead}</p>` : '';
    const titleHtml = title
      ? `<h2>${esc(title)}${opts && opts.fn ? fnMark(opts.fn) : ''}</h2>`
      : '';
    return `<section class="arch-section" id="${esc(id)}">
      <div class="wrap">
        ${titleHtml}
        ${lead}
        ${innerHtml}
      </div>
    </section>`;
  }

  // —— Hero ——
  const hero = A.hero || {};
  const heroCopy = hero.copy || {};
  const heroData = hero.data || {};
  if (heroData.image) {
    document.documentElement.style.setProperty('--hub-hero-image', `url('${heroData.image}')`);
  }
  const headlineEl = document.getElementById('hero-headline');
  const subEl = document.getElementById('hero-sub');
  if (headlineEl) headlineEl.textContent = heroCopy.headline || '';
  if (subEl) subEl.textContent = heroCopy.subline || '';

  const chipsHost = document.getElementById('hero-chips');
  if (chipsHost && Array.isArray(heroCopy.stat_chips) && heroCopy.stat_chips.length) {
    chipsHost.hidden = false;
    chipsHost.innerHTML = heroCopy.stat_chips
      .map((c) => {
        const raw = String(c).trim();
        const parts = raw.split(/\s[·•]\s/);
        if (parts.length >= 2) {
          return `<div class="chip"><div class="v">${esc(parts[0])}</div><div class="l">${esc(parts.slice(1).join(' · '))}</div></div>`;
        }
        const m = raw.match(/^(\$?~?[\d.,]+(?:[–-][\d.,]+)?%?(?:\s*\/\s*\w+)?(?:\s*M)?(?:\s*yr)?)\s+(.+)$/i);
        if (m) {
          return `<div class="chip"><div class="v">${esc(m[1])}</div><div class="l">${esc(m[2])}</div></div>`;
        }
        return `<div class="chip"><div class="v" style="font-size:17px;line-height:1.25">${esc(raw)}</div><div class="l"></div></div>`;
      })
      .join('');
  }
  const smallPrint = document.getElementById('hero-small-print');
  if (smallPrint) {
    if (heroCopy.small_print) {
      smallPrint.hidden = false;
      smallPrint.innerHTML = withText(heroCopy.fn, heroCopy.small_print);
    } else {
      smallPrint.hidden = true;
    }
  }
  const heroCta = document.getElementById('hero-cta-primary');
  if (heroCta) {
    heroCta.textContent = isInvest ? 'Request fleet memo' : 'Start a conversation';
    heroCta.href = '#cta';
  }
  const navCta = document.getElementById('nav-cta');
  if (navCta) navCta.textContent = isInvest ? 'Request memo' : 'Get in touch';

  // —— G1 sticky nav ——
  const anchors = Array.isArray(A.nav_anchors) ? A.nav_anchors : [];
  const sticky = document.getElementById('arch-sticky-nav');
  const stickyInner = document.getElementById('arch-sticky-inner');
  if (sticky && stickyInner && anchors.length) {
    sticky.hidden = false;
    stickyInner.innerHTML = anchors
      .map((a) => `<a class="arch-sticky-link" href="#${esc(a.id)}" data-anchor="${esc(a.id)}">${esc(a.label)}</a>`)
      .join('');
    // active section highlight
    const linkEls = [...stickyInner.querySelectorAll('.arch-sticky-link')];
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (!en.isIntersecting) return;
          const id = en.target.id;
          linkEls.forEach((l) => l.classList.toggle('active', l.dataset.anchor === id));
        });
      },
      { rootMargin: '-30% 0px -55% 0px', threshold: 0.01 }
    );
    // observe after DOM assembled
    setTimeout(() => {
      anchors.forEach((a) => {
        const el = document.getElementById(a.id);
        if (el) obs.observe(el);
      });
    }, 400);
  }

  // —— Section builders ——
  function buildNavierIntro() {
    const ni = A.navier_intro;
    if (!ni) return '';
    const c = ni.copy || {};
    const d = ni.data || {};
    const imgs = d.images || {};
    const leftMedia =
      youtubeEmbed(d.video_url) ||
      imgTag(imgs.vessel_n45_plate || imgs.vessel_n30_plate, c.headline || 'Navier vessel', 'intro-hero-img');

    const tech = Array.isArray(c.tech_chips)
      ? `<div class="tech-chips">${c.tech_chips
          .map(
            (t) =>
              `<div class="tech-chip"><div class="k">${esc(t.label || '')}</div><div class="v">${esc(t.value || '')}</div></div>`
          )
          .join('')}</div>`
      : '';

    const cards = Array.isArray(c.fleet_cards)
      ? `<div class="vessel-plate-grid">${c.fleet_cards
          .map((v) => {
            const plate =
              /n30/i.test(v.model || '')
                ? imgs.vessel_n30_plate
                : imgs.vessel_n45_plate;
            const specs = [
              v.passengers != null ? `${v.passengers} passengers` : null,
              v.propulsion,
              v.cruise_speed_kn != null ? `~${v.cruise_speed_kn} kn cruise` : null,
              v.capex_usd != null ? money(v.capex_usd) : null,
              v.range_nm_approx != null ? `~${v.range_nm_approx} nm` : null,
              v.grade,
            ]
              .filter(Boolean)
              .map((s) => `<span class="spec-pill">${esc(s)}</span>`)
              .join('');
            return `<div class="vessel-plate-card">
              ${imgTag(plate, v.model || 'Vessel', 'vessel-plate')}
              <h3>${esc(v.model || '')}</h3>
              <div class="spec-pills">${specs}</div>
            </div>`;
          })
          .join('')}</div>`
      : '';

    const body = `
      <div class="intro-grid">
        <div class="intro-media">${leftMedia}</div>
        <div class="intro-copy">
          ${c.headline ? `<p class="lead">${esc(c.headline)}</p>` : ''}
          ${c.subline ? `<p class="subline">${esc(c.subline)}</p>` : ''}
          ${c.body ? `<p>${esc(c.body)}</p>` : ''}
          ${tech}
          ${c.note ? `<p class="section-note">${esc(c.note)}</p>` : ''}
        </div>
      </div>
      ${cards}`;

    return sectionShell(ni.id || 'navier_intro', ni.title || 'Meet the vessel', body);
  }

  function buildModel() {
    const model = A.model;
    if (!model || !model.copy) return '';
    const cards = model.copy.cards || [];
    // G6: never render demand-gated launch callouts / trigger blocks
    let html = '';
    if (cards.length) {
      html += `<div class="role-grid">${cards
        .map(
          (c) => `<div class="role-card">
          <h3>${esc(c.title || '')}</h3>
          <p>${esc(c.body || '')}</p>
        </div>`
        )
        .join('')}</div>`;
    }
    return sectionShell('model', model.copy.title || 'The model', html);
  }

  function buildServiceDay() {
    const sd = A.service_day;
    if (!sd || !sd.data || !sd.data.windows || !sd.data.windows.length) return '';
    const windows = sd.data.windows;
    const html = `<div class="day-timeline" role="list">
      ${windows
        .map((w) => {
          const upside = !!w.upside;
          return `<div class="day-block ${upside ? 'upside' : ''}" role="listitem">
            <div class="day-time">${esc(w.time_range || '')}</div>
            <div class="day-label">${esc(w.label || '')}${fnMark(w.fn)}</div>
            <div class="day-layer">${esc(w.layer || '')}</div>
            ${w.note ? `<p class="day-note">${esc(w.note)}</p>` : ''}
            ${w.image ? imgTag(w.image, w.label || '', 'day-img') : ''}
            ${upside ? '<span class="status-chip status-upside">UPSIDE</span>' : ''}
          </div>`;
        })
        .join('')}
    </div>`;
    return sectionShell('service_day', sd.title || 'How one vessel earns', html);
  }

  function buildRevenueBuild() {
    const rb = A.revenue_build;
    if (!rb || !rb.data || !rb.data.scenarios) return '';
    const scenarios = rb.data.scenarios;
    const keys = Object.keys(scenarios);
    if (!keys.length) return '';
    const defaultKey = scenarios.mid ? 'mid' : keys[0];

    let html = '';
    if (rb.note) html += `<p class="assump-label">${esc(rb.note)}${fnMark(rb.fn)}</p>`;
    html += `<div class="scenario-tabs" id="rev-scenario-tabs" role="tablist">
      ${keys
        .map(
          (k) =>
            `<button type="button" data-scenario="${esc(k)}" class="${k === defaultKey ? 'active' : ''}">${esc(k.charAt(0).toUpperCase() + k.slice(1))}</button>`
        )
        .join('')}
    </div>
    <div id="rev-scenario-panel"></div>`;

    // Store for paint after inject
    window.__REV_BUILD__ = { scenarios, defaultKey, fn: rb.fn };

    return sectionShell('revenue_build', rb.title || 'The revenue build', html, { fn: rb.fn });
  }

  function paintRevenueBuild(key) {
    const store = window.__REV_BUILD__;
    const panel = document.getElementById('rev-scenario-panel');
    const tabs = document.getElementById('rev-scenario-tabs');
    if (!store || !panel) return;
    const sc = store.scenarios[key];
    if (!sc) return;
    if (tabs) {
      [...tabs.querySelectorAll('button')].forEach((b) =>
        b.classList.toggle('active', b.dataset.scenario === key)
      );
    }
    const rows = sc.rows || [];
    let sum = 0;
    panel.innerHTML = `<div class="pnl-wrap"><table class="pnl-table rev-build-table" aria-label="Revenue build">
      <thead><tr><th>Line</th><th>Quantity</th><th class="num">Price</th><th class="num">$/mo</th><th></th></tr></thead>
      <tbody>
        ${rows
          .map((r) => {
            const sub = Number(r.subtotal_usd) || 0;
            sum += sub;
            return `<tr class="${r.status === 'upside' ? 'upside-row' : ''}">
              <td class="line">${esc(r.line || '')}${fnMark(r.fn)}</td>
              <td>${esc(r.quantity || '')}</td>
              <td class="num">${esc(r.price || '')}</td>
              <td class="num">${money(sub)}</td>
              <td class="chip-cell">${statusChip(r.status)}</td>
            </tr>
            ${r.note ? `<tr class="note-row"><td colspan="5" class="note">${esc(r.note)}</td></tr>` : ''}`;
          })
          .join('')}
        <tr class="net-row">
          <td class="line" colspan="3">Gross revenue / month</td>
          <td class="num gold">${money(sc.gross_monthly_usd != null ? sc.gross_monthly_usd : sum)}</td>
          <td></td>
        </tr>
      </tbody>
    </table></div>`;
  }

  function buildPnl() {
    const pnl = A.pnl;
    if (!pnl || !pnl.data) return '';
    const d = pnl.data;
    let html = '';
    if (pnl.copy && pnl.copy.body) {
      html += `<p class="section-lead">${esc(pnl.copy.body)}${fnMark(pnl.fn)}</p>`;
    } else if (pnl.copy && pnl.copy.headline) {
      html += `<p class="section-lead">${esc(pnl.copy.headline)}${fnMark(pnl.fn)}</p>`;
    }

    const sc = d.scenarios;
    if (sc && sc.table && sc.table.length) {
      if (sc.note) html += `<p class="assump-label">${esc(sc.note)}${fnMark(sc.fn)}</p>`;
      html += `<div class="scenario-tabs" id="scenario-tabs" role="tablist"></div>
        <div id="scenario-panel"></div>`;
      window.__PNL_SCENARIOS__ = sc.table;
    }

    html += `<div class="pnl-wrap"><table class="pnl-table" aria-label="Unit economics">
      <thead><tr><th>Line</th><th class="num">Pricing / range</th><th>Note</th><th></th></tr></thead>
      <tbody>`;

    function rowHtml(r, extraClass) {
      let rangeHtml = '—';
      if (r.pricing != null && r.pricing !== '') rangeHtml = esc(r.pricing);
      else {
        const built = moneyRangeLoose(r.per_mo_low, r.per_mo_high);
        if (built) rangeHtml = built;
        else if (r.value != null) rangeHtml = esc(r.value);
      }
      return `<tr class="${extraClass || ''}">
        <td class="line">${esc(r.line || r.title || '')}${fnMark(r.fn)}</td>
        <td class="num">${rangeHtml}</td>
        <td class="note">${r.note ? esc(r.note) : ''}</td>
        <td class="chip-cell">${statusChip(r.status)}</td>
      </tr>`;
    }

    if (d.revenue_rows && d.revenue_rows.length) {
      html += `<tr class="section-row"><td colspan="4">Revenue layers</td></tr>`;
      d.revenue_rows.forEach((r) => {
        html += rowHtml(r, 'rev-row');
      });
    }
    if (d.gross && d.gross.per_scenario) {
      const g = d.gross.per_scenario;
      html += `<tr class="subtotal-row">
        <td class="line">${esc(d.gross.title || 'Gross revenue / month')}</td>
        <td class="num">${money(g.conservative)} · <strong class="mid">${money(g.mid)}</strong> · ${money(g.upside)}</td>
        <td class="note">Conservative · Mid · Upside</td><td></td>
      </tr>`;
    }
    if (d.opex_rows && d.opex_rows.length) {
      html += `<tr class="section-row"><td colspan="4">Operating costs</td></tr>`;
      d.opex_rows.forEach((r) => {
        html += rowHtml(r, 'opex-row');
      });
    }
    if (d.opex_total) {
      html += `<tr class="subtotal-row">
        <td class="line">${esc(d.opex_total.title || 'Operating cost / month')}</td>
        <td class="num">${moneyRangeLoose(d.opex_total.per_mo_low, d.opex_total.per_mo_high) || '—'}</td>
        <td class="note"></td><td></td>
      </tr>`;
    }
    if (d.network_share) {
      html += `<tr class="share-row">
        <td class="line">${esc(d.network_share.line || 'Navier network share')}</td>
        <td class="num">${esc(d.network_share.value || '')}</td>
        <td class="note"></td><td></td>
      </tr>`;
    }
    if (d.net && d.net.per_scenario) {
      const n = d.net.per_scenario;
      html += `<tr class="net-row">
        <td class="line">${esc(d.net.title || 'Net to investor / month')}</td>
        <td class="num">${money(n.conservative)} · <strong class="mid">${money(n.mid)}</strong> · ${money(n.upside)}</td>
        <td class="note">Conservative · Mid · Upside</td><td></td>
      </tr>`;
    }
    if (d.payback && d.payback.per_scenario) {
      const p = d.payback.per_scenario;
      html += `<tr class="payback-row">
        <td class="line">${esc(d.payback.title || 'Payback')}</td>
        <td class="num gold">${esc(p.conservative)} · <strong class="mid">${esc(p.mid)}</strong> · ${esc(p.upside)}</td>
        <td class="note">Conservative · Mid · Upside</td><td></td>
      </tr>`;
    }
    if (d.upside_rows && d.upside_rows.length) {
      html += `<tr class="section-row upside-section"><td colspan="4">Upside only — never summed into base</td></tr>`;
      d.upside_rows.forEach((r) => {
        html += rowHtml(r, 'upside-row');
      });
    }
    html += `</tbody></table></div>`;
    return sectionShell('pnl', (pnl.copy && pnl.copy.headline) || 'Economics', html);
  }

  function buildAsset() {
    const asset = A.asset;
    if (!asset || !asset.data) return '';
    // Prefer navier_intro when present — avoid double vessel sections
    if (A.navier_intro) return '';
    const d = asset.data;
    let html = `<div class="scenario-hero">
      <div class="metric"><div class="k">Vessel</div><div class="v" style="font-size:18px">${esc(d.vessel || 'N45')}</div></div>
      <div class="metric"><div class="k">Capex</div><div class="v">${money(d.capex_usd)}</div></div>
      <div class="metric"><div class="k">Seats</div><div class="v">${esc(d.seats)}</div></div>
      <div class="metric"><div class="k">Cruise</div><div class="v">${esc(d.cruise_speed_kn)} kn</div></div>
    </div>`;
    if (asset.note) html += `<p class="section-note">${esc(asset.note)}</p>`;
    return sectionShell('asset', asset.title || 'The asset', html);
  }

  function buildDemand() {
    const dp = A.demand_pool;
    if (!dp || !dp.data || !dp.data.rows || !dp.data.rows.length) return '';
    let html = `<div style="overflow-x:auto"><table class="data-table">
      <thead><tr><th>Employer</th><th>Node</th><th>Line(s)</th><th>Headcount</th><th>Seats</th></tr></thead>
      <tbody>${dp.data.rows
        .map(
          (r) => `<tr>
          <td>${esc(r.employer || '')}${r.note ? `<div class="cell-note">${esc(r.note)}</div>` : ''}</td>
          <td>${esc(r.node || '')}</td>
          <td>${esc(Array.isArray(r.lines) ? r.lines.join(', ') : r.lines || '')}</td>
          <td>${r.headcount != null ? Number(r.headcount).toLocaleString('en-US') : '—'}</td>
          <td>${r.seats != null ? Number(r.seats).toLocaleString('en-US') : '—'}</td>
        </tr>`
        )
        .join('')}</tbody></table></div>`;
    if (dp.data.city_total_seats != null) {
      html += `<p class="assump-label" style="margin-top:10px">City total (indicative): ${Number(dp.data.city_total_seats).toLocaleString('en-US')} seats</p>`;
    }
    return sectionShell('demand_pool', dp.title || 'Who works on these corridors', html, { fn: dp.fn });
  }

  function buildFleetPhasing() {
    const fp = A.fleet_phasing;
    if (!fp || !fp.data) return '';
    let html = '';
    const pair = fp.copy && fp.copy.stat_pair;
    if (pair && pair.length) {
      html += `<div class="stat-pair">${pair
        .map(
          (s) => `<div class="stat-pair-card">
          <div class="k">${esc(s.title || '')}</div>
          <div class="v">${esc(s.value || '')}</div>
          ${s.note ? `<div class="n">${esc(s.note)}</div>` : ''}
        </div>`
        )
        .join('')}</div>`;
    }
    if (fp.data.launch && fp.data.launch.per_line && fp.data.launch.per_line.length) {
      const fullByLine = {};
      (fp.data.full_build && fp.data.full_build.per_line || []).forEach((r) => {
        fullByLine[r.line] = r;
      });
      html += `<div style="overflow-x:auto;margin-top:18px"><table class="data-table">
        <thead><tr><th>Line</th><th>Launch vessels</th><th>Launch capital</th><th>Full-build vessels</th><th>Full-build capital</th></tr></thead>
        <tbody>`;
      fp.data.launch.per_line.forEach((r) => {
        const full = fullByLine[r.line] || {};
        html += `<tr>
          <td>${esc(r.line)}</td>
          <td>${esc(r.launch_vessels)}</td>
          <td>${r.launch_capital_usd_range ? moneyRange(r.launch_capital_usd_range) : '—'}</td>
          <td>${full.vessels != null ? esc(full.vessels) : '—'}</td>
          <td>${full.capital_usd != null ? money(full.capital_usd) : '—'}</td>
        </tr>`;
      });
      html += `</tbody></table></div>`;
    }
    return sectionShell('fleet_phasing', fp.title || 'Fleet phasing', html, { fn: fp.fn });
  }

  function buildProtection() {
    const prot = A.protection_stack && A.protection_stack.copy && A.protection_stack.copy.cards;
    if (!prot || !prot.length) return '';
    const html = `<div class="arch-grid-2">${prot
      .map((c) => `<div class="arch-card"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p></div>`)
      .join('')}</div>`;
    return sectionShell('protection_stack', 'Protection stack', html);
  }

  function buildGap() {
    const gap = A.gap;
    if (!gap) return '';
    let html = `<div class="arch-prose">`;
    if (gap.copy && gap.copy.lead) html += `<p class="lead">${withText(gap.copy.fn, gap.copy.lead)}</p>`;
    if (gap.copy && gap.copy.support) html += `<p>${esc(gap.copy.support)}</p>`;
    html += `</div>`;
    // v3: plans nested under gap.data
    const plans = gap.data && gap.data.plans;
    if (plans && plans.length) {
      html += plans
        .map((p) => {
          let q = '';
          if (p.quote) q += `<blockquote>“${esc(p.quote)}”</blockquote>`;
          if (p.quote2) q += `<blockquote>“${esc(p.quote2)}”</blockquote>`;
          const note = p.note ? `<p class="plan-note">${esc(p.note)}${fnMark(p.fn)}</p>` : '';
          return `<div class="quote-card">
            <div class="plan-name">${esc(p.plan || '')}${!p.note ? fnMark(p.fn) : ''}</div>
            ${q}${note}
          </div>`;
        })
        .join('');
    }
    return sectionShell('gap', gap.title || 'The gap', html);
  }

  function buildInfra() {
    const inf = A.infrastructure_light;
    if (!inf || !inf.copy) return '';
    let html = `<div class="arch-prose">`;
    if (inf.copy.headline) html += `<p class="lead">${esc(inf.copy.headline)}</p>`;
    if (inf.copy.body) html += `<p>${esc(inf.copy.body)}</p>`;
    html += `</div>`;
    const lv = inf.data && inf.data.landings_verified;
    if (lv && (lv.value || lv.title)) {
      html += `<div class="stat-band"><div class="stat-card">
        <div class="stat">${esc(lv.value || lv.title)}</div>
      </div></div>`;
    }
    return sectionShell('infrastructure_light', 'Infrastructure-light', html);
  }

  function buildPosture() {
    const posture = A.posture;
    if (!posture || !posture.copy) return '';
    const w = (posture.data && posture.data.weighting) || 'balanced';
    const enableFirst = w !== 'operate_dominant';
    const enableCard = `<div class="arch-card ${enableFirst ? 'emphasis' : ''}">
      <span class="arch-badge enable">Enable</span>
      <h3>Enable the network</h3>
      <p>${esc(posture.copy.enable_track || '')}</p>
    </div>`;
    const operateCard = `<div class="arch-card ${!enableFirst ? 'emphasis' : ''}">
      <span class="arch-badge operate">Operate</span>
      <h3>Operate the service</h3>
      <p>${esc(posture.copy.operate_track || '')}</p>
      ${
        posture.data && posture.data.operate_proof_points && posture.data.operate_proof_points.length
          ? `<ul class="pair-list">${posture.data.operate_proof_points
              .map((p) => `<li><strong>${esc(p.body || '')}</strong> — ${esc(p.proof || '')}</li>`)
              .join('')}</ul>`
          : ''
      }
    </div>`;
    let html = '';
    if (posture.copy.framing) html += `<p class="lead">${esc(posture.copy.framing)}</p>`;
    html += `<div class="arch-grid-2">${enableFirst ? enableCard + operateCard : operateCard + enableCard}</div>`;
    return sectionShell('posture', 'Two ways to partner', html);
  }

  function buildPublicValue() {
    const pv = A.public_value;
    if (!pv) return '';
    let html = '';
    if (pv.data && pv.data.stats && pv.data.stats.length) {
      html += `<div class="stat-band">${pv.data.stats
        .map((s) => {
          const mark = fnMark(s.fn);
          const note = s.note
            ? `<div class="src">${esc(s.note)}${mark}</div>`
            : mark
              ? `<div class="src">${mark}</div>`
              : '';
          return `<div class="stat-card"><div class="stat">${esc(s.stat || s.title || '')}</div>${note}</div>`;
        })
        .join('')}</div>`;
    }
    if (pv.copy && pv.copy.pillars && pv.copy.pillars.length) {
      html += `<ul class="pillars">${pv.copy.pillars.map((p) => `<li>${esc(p)}</li>`).join('')}</ul>`;
    }
    return sectionShell('public_value', 'Public value', html);
  }

  function buildSpeedRelief() {
    const srr = A.speed_rule_relief;
    if (!srr || !srr.copy) return '';
    let html = `<div class="arch-prose">
      <p class="lead">${withText(srr.copy.fn, srr.copy.headline || '')}</p>`;
    if (srr.copy.framing) html += `<p>${esc(srr.copy.framing)}</p>`;
    html += `</div>`;
    if (Array.isArray(srr.copy.chips) && srr.copy.chips.length) {
      html += `<div class="relief-chips">${srr.copy.chips
        .map((c) => `<span class="relief-chip">${esc(c)}</span>`)
        .join('')}</div>`;
    }
    if (srr.copy.ask) html += `<p class="ask-line">${esc(srr.copy.ask)}</p>`;
    const exp = srr.expander;
    if (exp && (exp.body || exp.title)) {
      const bodyParas = Array.isArray(exp.body)
        ? exp.body.map((p) => `<p>${esc(p)}</p>`).join('')
        : exp.body
          ? `<p>${esc(exp.body)}</p>`
          : '';
      html += `<details class="relief-box">
        <summary>${esc(exp.title || 'Details')}${fnMark(exp.fn)}</summary>
        ${bodyParas}
      </details>`;
    }
    return sectionShell('speed_rule_relief', 'Speed-rule relief', html);
  }

  function buildFlywheel() {
    const fw = A.flywheel && A.flywheel.copy;
    if (!fw) return '';
    const html = `<div class="flywheel">
      <div class="wheel"><div class="n">1 · Employers</div><p>${esc(fw.employers || '')}</p></div>
      <div class="wheel"><div class="n">2 · Public partners</div><p>${esc(fw.public_partners || '')}</p></div>
      <div class="wheel"><div class="n">3 · Fleet investors</div><p>${esc(fw.fleet_investors || '')}</p></div>
    </div>`;
    return sectionShell('flywheel', 'How the pieces fit', html);
  }

  function buildAuthoritiesBlock(auth, asExpander) {
    if (!auth || !auth.data || !auth.data.bodies || !auth.data.bodies.length) return '';
    let inner = auth.copy && auth.copy.intro ? `<p class="lead">${esc(auth.copy.intro)}</p>` : '';
    inner += `<div class="arch-grid-2">${auth.data.bodies
      .map((b) => {
        const cls = (b.classification || '').toLowerCase().replace(/[^a-z_]/g, '');
        return `<div class="arch-card">
          <span class="arch-badge ${esc(cls)}">${esc((b.classification || '').replace(/_/g, ' '))}</span>
          <h3>${esc(b.body)}</h3>
          <p>${esc(b.role || '')}</p>
          ${b.engagement_window ? `<p class="assump-label">${esc(b.engagement_window)}</p>` : ''}
        </div>`;
      })
      .join('')}</div>`;
    if (asExpander) {
      return `<details class="ref-expander" ${auth.collapsed === false ? 'open' : ''}>
        <summary>${esc(auth.title || 'Authority landscape')}</summary>
        <div class="ref-body">${inner}</div>
      </details>`;
    }
    return sectionShell('authorities', auth.title || 'Authority landscape', inner);
  }

  function buildModalBlock(modal, asExpander) {
    if (!modal || !modal.data || !modal.data.pairs || !modal.data.pairs.length) return '';
    let inner = modal.copy && modal.copy.lead ? `<p class="lead">${esc(modal.copy.lead)}</p>` : '';
    inner += `<ul class="pair-list">${modal.data.pairs
      .map((p) => `<li><strong>${esc(p.station)}</strong> → ${esc(p.connects || '')}</li>`)
      .join('')}</ul>`;
    if (asExpander) {
      return `<details class="ref-expander" ${modal.collapsed === false ? 'open' : ''}>
        <summary>${esc(modal.title || 'Modal integration')}</summary>
        <div class="ref-body">${inner}</div>
      </details>`;
    }
    return sectionShell('modal_integration', modal.title || 'Modal integration', inner);
  }

  function buildReference() {
    const ref = A.reference;
    if (!ref) return '';
    const sections = ref.sections || {};
    let inner = '';
    if (sections.authorities) inner += buildAuthoritiesBlock(sections.authorities, true);
    if (sections.modal_integration) inner += buildModalBlock(sections.modal_integration, true);
    if (!inner) return '';
    // G7: section title always visible; inner authorities/modal are closed expanders
    return sectionShell('reference', ref.title || 'Reference', inner);
  }

  function buildNetworkNote() {
    const net = A.network;
    if (!net || !net.note) return '';
    // Network map is separate; this is optional prose above map handled via network-lead
    return '';
  }

  // Map of section id → builder. geometry/network are special (DOM move).
  const builders = {
    navier_intro: buildNavierIntro,
    model: buildModel,
    service_day: buildServiceDay,
    revenue_build: buildRevenueBuild,
    pnl: buildPnl,
    asset: buildAsset,
    demand_pool: buildDemand,
    fleet_phasing: buildFleetPhasing,
    protection_stack: buildProtection,
    gap: buildGap,
    infrastructure_light: buildInfra,
    posture: buildPosture,
    public_value: buildPublicValue,
    speed_rule_relief: buildSpeedRelief,
    flywheel: buildFlywheel,
    reference: buildReference,
    plan_alignment: () => '', // merged into gap in v3
    authorities: () => buildAuthoritiesBlock(A.authorities, false),
    modal_integration: () => buildModalBlock(A.modal_integration, false),
    vessels: () => {
      // skip if navier_intro present
      if (A.navier_intro) return '';
      const vessels = A.vessels && A.vessels.data && A.vessels.data.fleet;
      if (!vessels || !vessels.length) return '';
      const html = `<div class="vessel-row">${vessels
        .map(
          (v) => `<div class="arch-card">
          <h3>${esc(v.model || '')}</h3>
          <p>${v.passengers != null ? esc(v.passengers) + ' passengers' : ''}${v.propulsion ? ' · ' + esc(v.propulsion) : ''}</p>
        </div>`
        )
        .join('')}</div>`;
      return sectionShell('vessels', 'The vessels', html);
    },
  };

  // Default order if section_order missing
  const defaultOrder = isInvest
    ? [
        'navier_intro',
        'model',
        'service_day',
        'revenue_build',
        'pnl',
        'network',
        'demand_pool',
        'fleet_phasing',
        'protection_stack',
        'footnotes',
        'cta',
      ]
    : [
        'navier_intro',
        'gap',
        'posture',
        'infrastructure_light',
        'public_value',
        'speed_rule_relief',
        'geometry',
        'flywheel',
        'reference',
        'footnotes',
        'cta',
      ];

  const order = Array.isArray(A.section_order) && A.section_order.length ? A.section_order : defaultOrder;

  // Build module HTML for non-shell sections
  const modulesEl = document.getElementById('archetype-modules');
  const networkEl = document.getElementById('network');
  const notesEl = document.getElementById('archetype-notes');
  const ctaEl = document.getElementById('cta');
  const flow = document.getElementById('page-flow');

  // Collect fragment nodes in order
  const frag = document.createDocumentFragment();
  const moduleHtmlParts = [];

  order.forEach((id) => {
    if (id === 'hero') return; // already in page
    if (id === 'network' || id === 'geometry') {
      // placeholder marker — network moved after modules assembled
      moduleHtmlParts.push({ type: 'network' });
      return;
    }
    if (id === 'footnotes') {
      moduleHtmlParts.push({ type: 'notes' });
      return;
    }
    if (id === 'cta') {
      moduleHtmlParts.push({ type: 'cta' });
      return;
    }
    const fn = builders[id];
    if (fn) {
      const html = fn();
      if (html) moduleHtmlParts.push({ type: 'html', html });
    }
  });

  // Clear modules container; re-parent everything into page-flow in order
  if (modulesEl) modulesEl.innerHTML = '';
  if (flow) {
    // Remove current children temporarily
    const hold = document.createDocumentFragment();
    while (flow.firstChild) hold.appendChild(flow.firstChild);

    moduleHtmlParts.forEach((part) => {
      if (part.type === 'html') {
        const wrap = document.createElement('div');
        wrap.innerHTML = part.html;
        while (wrap.firstChild) flow.appendChild(wrap.firstChild);
      } else if (part.type === 'network' && networkEl) {
        flow.appendChild(networkEl);
      } else if (part.type === 'notes' && notesEl) {
        flow.appendChild(notesEl);
      } else if (part.type === 'cta' && ctaEl) {
        flow.appendChild(ctaEl);
      }
    });
    // Append any leftover shell nodes not referenced
    if (networkEl && !flow.contains(networkEl)) flow.appendChild(networkEl);
    if (notesEl && !flow.contains(notesEl)) flow.appendChild(notesEl);
    if (ctaEl && !flow.contains(ctaEl)) flow.appendChild(ctaEl);
  } else if (modulesEl) {
    modulesEl.innerHTML = moduleHtmlParts
      .filter((p) => p.type === 'html')
      .map((p) => p.html)
      .join('');
  }

  // Wire revenue build tabs
  if (window.__REV_BUILD__) {
    paintRevenueBuild(window.__REV_BUILD__.defaultKey);
    const tabs = document.getElementById('rev-scenario-tabs');
    tabs?.querySelectorAll('button').forEach((b) => {
      b.addEventListener('click', () => paintRevenueBuild(b.dataset.scenario));
    });
  }

  // Wire P&L scenario tabs
  if (window.__PNL_SCENARIOS__) {
    const table = window.__PNL_SCENARIOS__;
    const tabs = document.getElementById('scenario-tabs');
    const panel = document.getElementById('scenario-panel');
    if (tabs && panel) {
      const midIdx = Math.max(
        0,
        table.findIndex((t) => /mid/i.test(t.case))
      );
      function paint(i) {
        const row = table[i];
        if (!row) return;
        [...tabs.querySelectorAll('button')].forEach((b, j) => b.classList.toggle('active', j === i));
        panel.innerHTML = `<div class="scenario-hero">
          <div class="metric"><div class="k">Gross / mo</div><div class="v">${money(row.gross_monthly)}</div></div>
          <div class="metric"><div class="k">Net to investor / mo</div><div class="v">${money(row.net_to_investor_monthly)}</div></div>
          <div class="metric"><div class="k">Annual</div><div class="v">${money(row.annual)}</div></div>
          <div class="metric"><div class="k">Payback</div><div class="v gold" style="font-size:18px">${esc(row.payback)}</div></div>
        </div>
        ${row.upside_lines_included ? '<p class="assump-label">Includes labeled upside lines (sponsorship + overnight cargo).</p>' : '<p class="assump-label">Base utilization stack only — no sponsorship or cargo.</p>'}
        ${row.note ? `<p class="assump-label">${esc(row.note)}</p>` : ''}`;
      }
      tabs.innerHTML = table
        .map((t, i) => `<button type="button" data-i="${i}">${esc(t.case)}</button>`)
        .join('');
      tabs.querySelectorAll('button').forEach((b) => {
        b.addEventListener('click', () => paint(Number(b.dataset.i)));
      });
      paint(midIdx);
    }
  }

  // —— Footnotes ——
  if (notesEl && Object.keys(FOOTNOTES).length) {
    let keys = Object.keys(FOOTNOTES).filter((k) => usedFn.has(k));
    if (!keys.length) keys = Object.keys(FOOTNOTES);
    keys = Object.keys(FOOTNOTES).filter((k) => keys.includes(k));
    notesEl.hidden = false;
    notesEl.id = 'footnotes';
    notesEl.innerHTML = `<div class="wrap">
      <h2>Notes &amp; assumptions</h2>
      <ol class="fn-list">
        ${keys
          .map((k) => {
            const f = FOOTNOTES[k] || {};
            const text = typeof f === 'string' ? f : f.text || '';
            const chip = typeof f === 'object' ? domainChip(f.source_url) : '';
            return `<li id="fn-${esc(k)}"><span class="fn-text">${esc(text)}</span>${chip ? ' ' + chip : ''}</li>`;
          })
          .join('')}
      </ol>
    </div>`;
  }

  // —— CTA form ——
  const cta = A.cta || {};
  const ctaCopy = cta.copy || {};
  const intake = (cta.data && cta.data.intake) || {};
  const ctaHeadline = document.getElementById('cta-headline');
  const ctaBody = document.getElementById('cta-body');
  if (ctaHeadline) ctaHeadline.textContent = ctaCopy.headline || 'Get in touch';
  if (ctaBody) ctaBody.textContent = ctaCopy.body || '';

  const fieldDefs = (intake.fields || []).map((f) => {
    const raw = String(f);
    const [name, opts] = raw.split(':');
    return { name, opts: opts ? opts.split('|') : null };
  });
  if (!fieldDefs.some((f) => f.name === 'email')) {
    fieldDefs.splice(Math.min(2, fieldDefs.length), 0, { name: 'email', opts: null });
  }
  function labelize(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }
  const formFields = document.getElementById('form-fields');
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
    const btn = document.getElementById('form-submit');
    const status = document.getElementById('form-status');
    const success = document.getElementById('form-success');
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
      success.innerHTML = '<strong>Draft ready.</strong> Opening your mail client as backup.';
    } catch (err) {
      console.warn(err);
      status.textContent = 'Could not send — try emailing directly.';
    } finally {
      btn.disabled = false;
    }
  });

  document.querySelectorAll('[data-contact-email]').forEach((a) => {
    a.href = 'mailto:' + contact;
    if (a.dataset.contactEmail === 'text') a.textContent = contact;
  });

  // Network titles / footnotes (no internal jargon)
  const nt = document.getElementById('network-title');
  const nl = document.getElementById('network-lead');
  const nf = document.getElementById('network-footnote');
  if (isPartners) {
    if (nt) nt.textContent = 'The network';
    if (nl)
      nl.textContent =
        'Same corridors as the employer network — coverage without new ferry terminals. Find a ride and compare to driving.';
    if (nf)
      nf.textContent =
        'Gold rings mark transfer hubs. Five corridors: North Shore · South Shore · Quincy · Inner Harbor · Riverside. Alongside the MBTA ferry — premium tier, not a replacement.';
  }
  if (isInvest) {
    if (nt) nt.textContent = A.network?.title || 'Where the fleet works';
    if (nl)
      nl.textContent =
        A.network?.note ||
        'Same corridors employers will ride — utilization starts with real demand on real water. Find a ride and compare to driving.';
    if (nf)
      nf.textContent =
        A.network?.note ||
        'Same five corridors as the employer network. Service phases corridor by corridor. Target first sailings: 2027.';
  }

  // Resize map after reparent
  setTimeout(() => {
    window.dispatchEvent(new Event('resize'));
  }, 100);

  console.info('[archetype]', A.archetype, A.city, 'contract', A.contract_version || 'v1');
})();
