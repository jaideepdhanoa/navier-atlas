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

    // Vessels
    const vessels = A.vessels && A.vessels.data && A.vessels.data.fleet;
    if (vessels && vessels.length) {
      const html = `<div class="vessel-row">${vessels
        .map(
          (v) => `<div class="arch-card">
          <h3>${esc(v.model || '')}</h3>
          <p>${v.passengers != null ? esc(v.passengers) + ' passengers' : ''}${v.propulsion ? ' · ' + esc(v.propulsion) : ''}</p>
        </div>`
        )
        .join('')}</div>`;
      parts.push(section('vessels', 'The vessels', html));
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

  function renderInvestModules() {
    const parts = [];

    // Model
    const model = A.model;
    if (model && model.copy) {
      let html = '';
      if (model.copy.roles && model.copy.roles.length) {
        html += `<ul class="pillars">${model.copy.roles.map((r) => `<li>${esc(r)}</li>`).join('')}</ul>`;
      }
      if (model.copy.trigger) {
        html += `<div class="arch-card emphasis" style="margin-top:16px"><h3>Launch trigger</h3><p>${esc(model.copy.trigger)}</p></div>`;
      }
      parts.push(section('story', 'The model', html));
    }

    // Asset
    const asset = A.asset;
    if (asset && asset.data) {
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
      parts.push(section('asset', 'The asset', html));
    }

    // Network note (map is separate section below)
    const net = A.network;
    if (net && net.copy && net.copy.trigger_explainer) {
      parts.push(
        section(
          'network-note',
          'Demand-gated corridors',
          `<p class="lead">${esc(net.copy.trigger_explainer)}</p>`
        )
      );
    }

    // Demand pool
    const dp = A.demand_pool;
    if (dp && dp.data && dp.data.rows && dp.data.rows.length) {
      let html = `<p class="standing-label">${esc(dp.standing_label || '')}</p>`;
      if (dp.data.capture_assumption) {
        html += `<p class="assump-label">Capture assumption: ${esc(dp.data.capture_assumption)}. Headcount: ${esc(dp.data.headcount_label || '')}</p>`;
      }
      html += `<div style="overflow-x:auto"><table class="data-table">
        <thead><tr><th>Employer</th><th>Node</th><th>Line(s)</th><th>Headcount</th><th>Demand-pool seats</th></tr></thead>
        <tbody>${dp.data.rows
          .map(
            (r) => `<tr>
            <td>${esc(r.employer || '')}</td>
            <td>${esc(r.node || '')}</td>
            <td>${esc(Array.isArray(r.lines) ? r.lines.join(', ') : r.lines || '')}</td>
            <td>${r.headcount != null ? esc(r.headcount) : '—'}</td>
            <td>${r.seats != null ? esc(r.seats) : '—'}</td>
          </tr>`
          )
          .join('')}</tbody></table></div>`;
      if (dp.data.city_total_seats != null) {
        html += `<p class="assump-label" style="margin-top:10px">City total (indicative): ${esc(dp.data.city_total_seats)} seats</p>`;
      }
      if (dp.data.honesty_notes && dp.data.honesty_notes.length) {
        html += `<ul class="pillars">${dp.data.honesty_notes.map((n) => `<li>${esc(n)}</li>`).join('')}</ul>`;
      }
      parts.push(section('demand', 'Demand pool', html));
    }

    // P&L utilization stack
    const pnl = A.pnl;
    if (pnl && pnl.data) {
      let html = '';
      const layers = pnl.data.stack_layers;
      if (layers) {
        if (layers.frame) html += `<p class="lead">${esc(layers.frame)}</p>`;
        if (layers.layers && layers.layers.length) {
          html += `<div class="stack-layers">${layers.layers
            .map((L) => {
              const upside = String(L.id || '').startsWith('U');
              return `<div class="stack-layer ${upside ? 'upside' : ''}">
                <div class="id">${esc(L.id)}</div>
                <h4>${esc(L.name)}</h4>
                <p class="pricing">${esc(L.pricing || '')}</p>
                <p class="status">${esc(L.status || '')}</p>
              </div>`;
            })
            .join('')}</div>`;
        }
      }

      // Scenarios
      const sc = pnl.data.scenarios;
      if (sc && sc.table && sc.table.length) {
        if (sc.label) html += `<p class="assump-label">${esc(sc.label)}</p>`;
        html += `<div class="scenario-tabs" id="scenario-tabs" role="tablist"></div>
          <div id="scenario-panel"></div>`;
        if (sc.honesty_note) html += `<p class="assump-label" style="margin-top:12px">${esc(sc.honesty_note)}</p>`;
      }

      // Opex
      const opex = pnl.data.opex_monthly_per_vessel;
      if (opex && opex.lines && opex.lines.length) {
        html += `<h3 style="margin:28px 0 10px;font-size:16px">Monthly opex (per vessel)</h3>
          <div style="overflow-x:auto"><table class="data-table"><thead><tr><th>Item</th><th>Range</th><th>Assumption</th></tr></thead><tbody>
          ${opex.lines
            .map(
              (r) => `<tr>
              <td>${esc(r.item)}</td>
              <td>${moneyRange(r.range_usd)}</td>
              <td class="assump-label">${esc(r.label || '')}</td>
            </tr>`
            )
            .join('')}
          ${
            opex.total_range_usd
              ? `<tr><td><strong>Total</strong></td><td><strong>${moneyRange(opex.total_range_usd)}</strong></td><td></td></tr>`
              : ''
          }
          </tbody></table></div>`;
      }

      if (pnl.data.network_share) {
        html += `<div class="arch-card" style="margin-top:16px"><h3>Navier network share</h3>
          <p>${esc(pnl.data.network_share.value || '')}</p>
          <p class="assump-label">${esc(pnl.data.network_share.label || '')}</p></div>`;
      }

      if (pnl.data.payback_summary) {
        const pb = pnl.data.payback_summary;
        html += `<div class="scenario-hero" style="margin-top:16px">
          <div class="metric"><div class="k">Conservative</div><div class="v" style="font-size:16px">${esc(pb.conservative || '')}</div></div>
          <div class="metric"><div class="k">Mid (headline)</div><div class="v" style="font-size:16px">${esc(pb.mid || '')}</div></div>
          <div class="metric"><div class="k">Upside</div><div class="v" style="font-size:16px">${esc(pb.upside || '')}</div></div>
        </div>
        <p class="assump-label">${esc(pb.label || '')}</p>`;
      }

      const relief = pnl.data.speed_relief_upside_row;
      if (relief) {
        html += `<div class="relief-box" style="margin-top:16px">
          <strong>${esc(relief.label || 'Speed-rule relief upside')}</strong>
          ${relief.values != null ? `<p>${esc(String(relief.values))}</p>` : ''}
          ${relief.note ? `<p class="assump-label">${esc(relief.note)}</p>` : ''}
        </div>`;
      }

      parts.push(section('pnl', 'Economics — utilization stack', html));
    }

    // Fleet phasing
    const fp = A.fleet_phasing && A.fleet_phasing.data;
    if (fp) {
      let html = '';
      if (fp.launch) {
        html += `<div class="arch-card emphasis"><h3>Launch fleet</h3>
          <p>${moneyRange(fp.launch.capital_usd_range)} capital · ${Array.isArray(fp.launch.vessels_range) ? fp.launch.vessels_range.join('–') : esc(fp.launch.vessels_range)} vessels</p>
          <p class="assump-label">${esc(fp.launch.label || '')}</p></div>`;
        if (fp.launch.per_line && fp.launch.per_line.length) {
          html += `<div style="overflow-x:auto;margin-top:12px"><table class="data-table"><thead><tr><th>Line</th><th>Vessels</th><th>Capital</th></tr></thead><tbody>
            ${fp.launch.per_line
              .map(
                (r) =>
                  `<tr><td>${esc(r.line)}</td><td>${esc(r.launch_vessels)}</td><td>${moneyRange(r.launch_capital_usd_range)}</td></tr>`
              )
              .join('')}
          </tbody></table></div>`;
        }
      }
      if (fp.full_build) {
        html += `<div class="arch-card" style="margin-top:14px"><h3>Full build (illustrative)</h3>
          <p>${money(fp.full_build.capital_usd)} · ${esc(fp.full_build.vessels)} vessels</p>
          <p class="assump-label">${esc(fp.full_build.label || '')}</p></div>`;
      }
      if (fp.spares_note) html += `<p class="assump-label" style="margin-top:10px">${esc(fp.spares_note)}</p>`;
      parts.push(section('phasing', 'Fleet phasing', html));
    }

    // Protection stack
    const prot = A.protection_stack && A.protection_stack.copy && A.protection_stack.copy.cards;
    if (prot && prot.length) {
      const html = `<div class="arch-grid-2">${prot
        .map((c) => `<div class="arch-card"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p></div>`)
        .join('')}</div>`;
      parts.push(section('protection', 'Protection stack', html));
    }

    // Flywheel (shared story)
    const fw = A.flywheel && A.flywheel.copy;
    // fleet file may not have flywheel - optional
    if (fw) {
      const html = `<div class="flywheel">
        <div class="wheel"><div class="n">Employers</div><p>${esc(fw.employers || '')}</p></div>
        <div class="wheel"><div class="n">Public partners</div><p>${esc(fw.public_partners || '')}</p></div>
        <div class="wheel"><div class="n">Fleet investors</div><p>${esc(fw.fleet_investors || '')}</p></div>
      </div>`;
      parts.push(section('flywheel', 'How the pieces fit', html));
    }

    return parts.join('');
  }

  const modulesEl = document.getElementById('archetype-modules');
  if (modulesEl) {
    // Insert modules BEFORE network section in DOM order: story first, then map stays in HTML
    // User wants map for all - keep network in page. Modules above network for narrative.
    modulesEl.innerHTML = isInvest ? renderInvestModules() : renderPartnersModules();
  }

  // Scenario tabs (invest)
  if (isInvest && A.pnl && A.pnl.data && A.pnl.data.scenarios && A.pnl.data.scenarios.table) {
    const table = A.pnl.data.scenarios.table;
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
          <div class="metric"><div class="k">Payback</div><div class="v" style="font-size:16px">${esc(row.payback)}</div></div>
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
