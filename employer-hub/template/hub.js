/**
 * Shared employer-hub runtime.
 * Expects window.EMPLOYER_HUB_DATA (normalized hub.json).
 * Calculator profiles: bay_productivity | nyc_parking_toll
 */
(function () {
  const DATA = window.EMPLOYER_HUB_DATA;
  if (!DATA) {
    document.body.insertAdjacentHTML(
      'afterbegin',
      '<p style="padding:24px;color:#e0cb8f">Missing employer hub data — rebuild and redeploy the site.</p>'
    );
    return;
  }

  const HUB_ID = DATA.id || 'unknown';
  const stops = DATA.stops || DATA.nodes || [];
  const lines = (DATA.lines || []).filter((l) => l.id);
  const nodesByKey = Object.fromEntries(stops.map((n) => [n.key, n]));
  const copy = DATA.copy || {};
  const market = DATA.market || {};
  const brand = DATA.brand || {};
  const calcMeta = DATA.calculator || DATA.roi_calculator || {};
  const profile = calcMeta.profile || 'bay_productivity';
  const contact = market.contact_email || 'jaideep@navierboat.com';
  let map, popup, flavor;

  function money(n) {
    const sign = n < 0 ? '-' : '';
    const a = Math.abs(n);
    if (a >= 1e6) return sign + '$' + (a / 1e6).toFixed(2) + 'M';
    return sign + '$' + Math.round(a).toLocaleString('en-US');
  }

  function servesText(n) {
    if (!n) return '';
    if (Array.isArray(n.serves)) return n.serves.join(' · ');
    return n.serves || '';
  }

  function chipValue(c) {
    return c.value != null ? c.value : c.stat;
  }

  // —— Static copy ——
  const setText = (id, v) => {
    const el = document.getElementById(id);
    if (el && v != null) el.textContent = v;
  };
  const setHtml = (id, v) => {
    const el = document.getElementById(id);
    if (el && v != null) el.innerHTML = v;
  };

  document.title = brand.title || document.title;
  setText('hero-headline', copy.hero_headline);
  setText('hero-sub', copy.hero_sub);
  setText('hero-eyebrow', market.eyebrow || `${market.label || ''} · Employer water commute`);
  setText('nav-tag', brand.nav_tag || market.tagline || 'Employer network');
  setText('stripe-lesson', copy.stripe_lesson || copy.precedent);
  setText('loi-cta', copy.loi_cta);
  setText('price-anchor', copy.price_anchor || '');
  setText('footer-note', copy.footer_note || 'Letters of intent are non-binding.');
  setText('calc-caveat', calcMeta.caveat || 'Indicative planning tool, not a quote.');
  setText('launch-trigger', copy.launch_trigger || '');
  setText('problem-title', copy.problem_title || '');
  setText('problem-lead', copy.problem_lead || '');
  setText('proof-title', copy.proof_title || '');
  setText('proof-lead', copy.proof_lead || '');
  setText('proof-worked-title', copy.proof_worked_title || 'What worked');
  setText('proof-worked-body', copy.proof_worked_body || '');
  setText('proof-fixed-title', copy.proof_fixed_title || 'What we fixed');
  setText('proof-fixed-body', copy.proof_fixed_body || '');
  setText('proof-ask-title', copy.proof_ask_title || 'What we ask now');
  setText('proof-ask-body', copy.proof_ask_body || '');
  setText('products-title', (DATA.products && DATA.products.section_title) || 'Two paths for employers');
  setText('products-lead', (DATA.products && DATA.products.section_lead) || '');
  setText('network-title', copy.network_title || 'The network');
  setText('network-lead', copy.network_lead || '');
  setText('calc-title', copy.calc_title || 'What it costs your team');
  setHtml('calc-lead', copy.calc_lead_html || copy.calc_lead || '');
  setText('loi-title', copy.loi_title || 'Letter of intent');
  setText('hero-note', copy.hero_note || 'Non-binding letter of intent · no commitment');
  setText('map-detail', copy.map_detail_empty || 'Select a line or stop.');
  setText('hero-cta-network', copy.hero_cta_network || 'See the network near me');
  setText('hero-cta-calc', copy.hero_cta_calc || 'Estimate cost for my team');
  setText('nav-cta', copy.nav_cta || 'Reserve interest');

  // Contact links
  document.querySelectorAll('[data-contact-email]').forEach((a) => {
    a.href = 'mailto:' + contact;
    if (a.dataset.contactEmail === 'text') a.textContent = contact;
  });

  // Problem chips
  const chips = document.getElementById('problem-chips');
  if (chips) {
    chips.innerHTML = '';
    (copy.problem_chips || []).forEach((c) => {
      const el = document.createElement('div');
      el.className = 'chip';
      el.innerHTML = `<div class="v">${chipValue(c)}</div><div class="l">${c.label}</div>`;
      chips.appendChild(el);
    });
  }

  // Products
  const productsEl = document.getElementById('products-grid');
  if (productsEl && DATA.products && DATA.products.items) {
    productsEl.innerHTML = DATA.products.items
      .map(
        (p) => `
      <article class="card product">
        <span class="tag ${p.tag_class || 'tag-line'}">${p.tag || ''}</span>
        <h3>${p.title}</h3>
        <p>${p.body || ''}</p>
        <div class="meta-row">${(p.meta || []).map((m) => `<span class="meta">${m}</span>`).join('')}</div>
        <a class="btn ${p.cta_class || 'btn-ghost'}" href="${p.cta_href || '#letter'}">${p.cta_label || 'Learn more'}</a>
      </article>`
      )
      .join('');
  }

  // LOI flavors
  const loi = DATA.loi || {};
  const flavors = loi.flavors || {};
  const flavorOrder = loi.flavor_order || Object.keys(flavors);
  const flavorOpts = document.getElementById('flavor-options');
  if (flavorOpts && flavorOrder.length) {
    flavorOpts.innerHTML = flavorOrder
      .map((key, i) => {
        const f = flavors[key];
        if (!f) return '';
        const active = i === 0 ? ' active' : '';
        return `<button type="button" class="option${active}" data-flavor="${f.id}" data-flavor-key="${key}">
          <h4>${f.title}</h4>
          <p>${f.body || ''}</p>
        </button>`;
      })
      .join('');
    flavor = flavors[flavorOrder[0]]?.id || loi.default_flavor || 'A';
    const hid = document.getElementById('f-flavor');
    if (hid) hid.value = flavor;
  } else {
    flavor = loi.default_flavor || 'A';
  }

  // Map legend
  const legend = document.getElementById('map-legend');
  if (legend) {
    legend.innerHTML = '';
    lines.forEach((line) => {
      const s = document.createElement('span');
      s.innerHTML = `<i style="background:${line.color}"></i>${line.id}`;
      legend.appendChild(s);
    });
  }

  // —— Calculator ——
  const inputsMeta = calcMeta.inputs || {};
  const state = {};
  Object.keys(inputsMeta).forEach((k) => {
    state[k] = inputsMeta[k].default;
  });
  const fieldsEl = document.getElementById('calc-fields');
  const fieldOrder =
    calcMeta.field_order ||
    Object.keys(inputsMeta);

  function formatInput(key, v) {
    if (key === 'subsidy_share' || key === 'parking_share' || key === 'sigma_employer_subsidy_share' || key === 'rho_share_displacing_stall')
      return Math.round(v * 100) + '%';
    if (
      key === 'price_seat_month' ||
      key === 'P_price_per_seat_month' ||
      key === 'parking_cost' ||
      key === 'K_parking_cost_stall_month' ||
      key === 'shuttle_cost' ||
      key === 'V_current_shuttle_cost_seat_month' ||
      key === 'pretax_benefit' ||
      key === 'X_pretax_benefit_cap_month'
    )
      return '$' + Math.round(v);
    return String(v);
  }

  function isShareKey(key) {
    return /share|sigma|rho/i.test(key) && !/cost|price|seat/i.test(key);
  }
  function isPriceKey(key) {
    return /price|cost|benefit|toll/i.test(key) && !isShareKey(key);
  }

  function renderFields() {
    if (!fieldsEl) return;
    fieldsEl.innerHTML = '';
    fieldOrder.forEach((key) => {
      const meta = inputsMeta[key];
      if (!meta) return;
      const wrap = document.createElement('div');
      wrap.className = 'field';
      const id = 'in-' + key;
      let control;
      const useRange =
        meta.min != null ||
        meta.max != null ||
        key === 'price_seat_month' ||
        key === 'P_price_per_seat_month' ||
        isShareKey(key);
      if (useRange) {
        let min = meta.min != null ? meta.min : isShareKey(key) ? 0 : 0;
        let max = meta.max != null ? meta.max : isShareKey(key) ? 1 : 2000;
        let step = meta.step != null ? meta.step : isShareKey(key) ? 0.05 : 25;
        if (key === 'price_seat_month' || key === 'P_price_per_seat_month') {
          min = meta.min != null ? meta.min : 750;
          max = meta.max != null ? meta.max : 1200;
          step = 25;
        }
        control = `<input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${state[key]}" />
          <div class="hint"><span id="${id}-val">${formatInput(key, state[key])}</span>${meta.note ? ` · ${meta.note}` : ''}</div>`;
      } else {
        control = `<input id="${id}" type="number" step="any" value="${state[key]}" />
          ${meta.note ? `<div class="hint">${meta.note}</div>` : ''}`;
      }
      wrap.innerHTML = `<label for="${id}">${meta.label || key}</label>${control}`;
      fieldsEl.appendChild(wrap);
      const input = wrap.querySelector('input');
      input.addEventListener('input', () => {
        state[key] = Number(input.value);
        const valEl = document.getElementById(id + '-val');
        if (valEl) valEl.textContent = formatInput(key, state[key]);
        recompute();
      });
    });
  }

  function recomputeBay() {
    const S = state.seats,
      D = state.days_per_month,
      P = state.price_seat_month;
    const sigma = state.subsidy_share,
      X = state.pretax_benefit,
      V = state.shuttle_cost;
    const K = state.parking_cost,
      rho = state.parking_share;
    const Tc = state.car_min,
      Tw = state.water_min,
      M = state.car_miles;
    const E = state.co2_kg_per_mile,
      H = state.hour_cost;
    const gross = S * P;
    const employee_contribution = S * Math.min(X, (1 - sigma) * P);
    const net_employer = gross - employee_contribution;
    const shuttle_offset = S * V;
    const parking_offset = S * rho * K;
    const net_incremental = net_employer - shuttle_offset - parking_offset;
    const hours_returned = (S * D * 2 * (Tc - Tw)) / 60;
    const productivity_value = hours_returned * H;
    const co2_tonnes = (S * D * 2 * M * E) / 1000;
    const net_cost_per_hour = hours_returned === 0 ? 0 : net_incremental / hours_returned;
    const per_rider = S === 0 ? 0 : net_incremental / S;

    document.getElementById('out-net').textContent = money(net_incremental) + '/mo';
    document.getElementById('out-per').textContent = money(per_rider) + ' per rider / month';
    const kicker = document.querySelector('.headline-out .kicker');
    if (kicker) kicker.textContent = (calcMeta.headline && calcMeta.headline.kicker) || 'Net incremental employer cost';

    const rows = [
      ['Gross program cost', money(gross) + '/mo'],
      ['Employee pre-tax contribution', money(employee_contribution) + '/mo'],
      ['Net employer cost', money(net_employer) + '/mo'],
      ['Shuttle offset', money(shuttle_offset) + '/mo'],
      ['Parking offset', money(parking_offset) + '/mo'],
      ['Hours returned / month', Math.round(hours_returned).toLocaleString('en-US')],
      ['Productivity value (framing only)', money(productivity_value) + '/mo'],
      ['CO₂ avoided', co2_tonnes.toFixed(1) + ' t/mo'],
      ['Net cost per employee-hour returned', money(net_cost_per_hour)],
    ];
    document.getElementById('out-rows').innerHTML = rows
      .map(([k, v]) => `<div class="out-row"><span>${k}</span><strong>${v}</strong></div>`)
      .join('');

    window.__HUB_CALC__ = {
      profile,
      net_incremental,
      per_rider,
      hours_returned,
      S,
      P,
      sigma,
      net_employer_cost_per_rider: per_rider,
    };
    return { net_incremental, per_rider };
  }

  function recomputeNyc() {
    // Keys from NY package (with fallbacks to short names)
    const S = state.S_committed_seats ?? state.seats ?? 60;
    const P = state.P_price_per_seat_month ?? state.price_seat_month ?? 750;
    const sigma = state.sigma_employer_subsidy_share ?? state.subsidy_share ?? 0.8;
    const X = state.X_pretax_benefit_cap_month ?? state.pretax_benefit ?? 340;
    const V = state.V_current_shuttle_cost_seat_month ?? state.shuttle_cost ?? 0;
    const K = state.K_parking_cost_stall_month ?? state.parking_cost ?? 570;
    const rho = state.rho_share_displacing_stall ?? state.parking_share ?? 0.5;
    const G = state.G_congestion_toll_weekday ?? state.congestion_toll ?? 9;
    const W = state.W_weekdays_per_month ?? state.weekdays_per_month ?? 21;

    const gross = S * P;
    const employee_pretax = S * Math.min(X, (1 - sigma) * P);
    const net_employer = gross - employee_pretax;
    const net_per_rider = S === 0 ? 0 : net_employer / S;
    const benchmark = K + G * W;
    const parking_offset = S * rho * K;
    const shuttle_offset = S * V;
    const net_incremental = net_employer - parking_offset - shuttle_offset;
    const net_inc_per_rider = S === 0 ? 0 : net_incremental / S;
    const delta = net_per_rider - benchmark;

    document.getElementById('out-net').textContent = money(net_per_rider) + ' / rider';
    document.getElementById('out-per').textContent =
      'vs ' + money(benchmark) + ' parking + toll benchmark';
    const kicker = document.querySelector('.headline-out .kicker');
    if (kicker) kicker.textContent = 'Net employer cost per rider';
    const anchor = document.getElementById('price-anchor');
    if (anchor) {
      anchor.textContent =
        delta < 0
          ? 'less than the parking space it replaces'
          : copy.price_anchor || 'Indicative planning estimate';
      anchor.style.color = delta < 0 ? 'var(--ok)' : '';
    }

    const rows = [
      ['Gross program cost', money(gross) + '/mo'],
      ['Employee pre-tax contribution', money(employee_pretax) + '/mo'],
      ['Net employer cost', money(net_employer) + '/mo'],
      ['Net employer cost / rider', money(net_per_rider) + '/mo'],
      ['Status-quo benchmark / rider', money(benchmark) + '/mo'],
      ['Parking offset', money(parking_offset) + '/mo'],
      ['Shuttle offset', money(shuttle_offset) + '/mo'],
      ['Net incremental after offsets', money(net_incremental) + '/mo'],
      ['Net incremental / rider', money(net_inc_per_rider) + '/mo'],
    ];
    document.getElementById('out-rows').innerHTML = rows
      .map(([k, v]) => `<div class="out-row"><span>${k}</span><strong>${v}</strong></div>`)
      .join('');

    window.__HUB_CALC__ = {
      profile,
      net_incremental,
      per_rider: net_inc_per_rider,
      net_employer_cost_per_rider: net_per_rider,
      benchmark,
      S,
      P,
      sigma,
    };
    return {
      net_incremental,
      per_rider: net_inc_per_rider,
      net_employer_cost_per_rider: net_per_rider,
      benchmark,
    };
  }

  function recompute() {
    if (profile === 'nyc_parking_toll') return recomputeNyc();
    return recomputeBay();
  }

  // Presets
  const presetsEl = document.getElementById('presets');
  function addPreset(label, patch, id) {
    if (!presetsEl) return null;
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = label;
    b.dataset.id = id;
    b.addEventListener('click', () => {
      Object.assign(state, patch);
      renderFields();
      recompute();
      [...presetsEl.querySelectorAll('button')].forEach((x) => x.classList.toggle('active', x === b));
    });
    presetsEl.appendChild(b);
    return b;
  }

  if (presetsEl) {
    presetsEl.innerHTML = '';
    const defaults = {};
    Object.keys(inputsMeta).forEach((k) => {
      defaults[k] = inputsMeta[k].default;
    });
    const defBtn = addPreset('Planning defaults', defaults, 'defaults');
    if (defBtn) defBtn.classList.add('active');
    lines.forEach((line) => {
      if (!line.calculator_preset) return;
      const patch = {};
      const p = line.calculator_preset;
      if (p.car_min != null) patch.car_min = p.car_min;
      if (p.water_min != null) patch.water_min = p.water_min;
      if (p.car_miles != null) patch.car_miles = p.car_miles;
      if (p.price_seat_month != null) patch.price_seat_month = p.price_seat_month;
      if (p.P_price_per_seat_month != null) patch.P_price_per_seat_month = p.P_price_per_seat_month;
      addPreset(p.label || line.name, patch, 'line-' + line.id);
    });
  }

  renderFields();
  const check = recompute();
  const assert = calcMeta.worked_assert || {};
  if (assert.net_incremental != null && Math.round(check.net_incremental) !== assert.net_incremental) {
    console.warn('[employer-hub] calculator net_incremental mismatch', check, assert);
  }
  if (assert.per_rider != null && Math.round(check.per_rider) !== assert.per_rider) {
    console.warn('[employer-hub] calculator per_rider mismatch', check, assert);
  }
  if (
    assert.net_employer_cost_per_rider != null &&
    Math.round(check.net_employer_cost_per_rider) !== assert.net_employer_cost_per_rider
  ) {
    console.warn('[employer-hub] net_employer_cost_per_rider mismatch', check, assert);
  }

  document.getElementById('copy-summary')?.addEventListener('click', async () => {
    const c = window.__HUB_CALC__ || {};
    let text;
    if (profile === 'nyc_parking_toll') {
      text = [
        `Navier ${market.label || HUB_ID} employer water network — planning estimate (not a quote).`,
        `Net employer cost: ${money(c.net_employer_cost_per_rider)}/rider/mo vs ${money(c.benchmark)} parking+toll benchmark.`,
        `Net incremental after offsets: ${money(c.net_incremental)}/mo (~${money(c.per_rider)}/rider), at ${c.S} seats and $${c.P}/seat-month.`,
        `Letter of intent is non-binding.`,
      ].join('\n');
    } else {
      text = [
        `Navier ${market.label || HUB_ID} employer water network — planning estimate (not a quote).`,
        `Net incremental employer cost: ${money(c.net_incremental)}/mo (~${money(c.per_rider)} per rider), at ${c.S} seats and $${c.P}/seat-month with ${((c.sigma || 0) * 100).toFixed(0)}% employer subsidy.`,
        `${copy.price_anchor || 'Roughly a parking space — often less'}. Letter of intent is non-binding.`,
      ].join('\n');
    }
    try {
      await navigator.clipboard.writeText(text);
      const btn = document.getElementById('copy-summary');
      const prev = btn.textContent;
      btn.textContent = 'Copied';
      setTimeout(() => {
        btn.textContent = prev;
      }, 1500);
    } catch {
      prompt('Copy this summary:', text);
    }
  });

  // —— Map ——
  function initMap() {
    const mapCfg = market.map || {};
    map = new maplibregl.Map({
      container: 'map',
      style: {
        version: 8,
        sources: {
          carto: {
            type: 'raster',
            tiles: ['https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png'],
            tileSize: 256,
            attribution: '© CARTO · © OpenStreetMap',
          },
        },
        layers: [{ id: 'carto', type: 'raster', source: 'carto' }],
      },
      center: mapCfg.center || [-122.34, 37.72],
      zoom: mapCfg.zoom || 9.35,
      maxBounds: mapCfg.max_bounds || undefined,
      attributionControl: true,
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
    popup = new maplibregl.Popup({ closeButton: false, offset: 14 });

    map.on('load', () => {
      const stopFeatures = stops.map((n) => ({
        type: 'Feature',
        properties: { key: n.key, label: n.label, serves: servesText(n), bp: n.resolved_bp_id },
        geometry: { type: 'Point', coordinates: [n.lng, n.lat] },
      }));
      map.addSource('stops', { type: 'geojson', data: { type: 'FeatureCollection', features: stopFeatures } });

      const allCoords = [];
      lines.forEach((line) => {
        const coords = line.water_path;
        if (!coords || !coords.length) return;
        coords.forEach((c) => allCoords.push(c));
        map.addSource('line-' + line.id, {
          type: 'geojson',
          data: {
            type: 'Feature',
            properties: { id: line.id, name: line.name },
            geometry: { type: 'LineString', coordinates: coords },
          },
        });
        map.addLayer({
          id: 'line-glow-' + line.id,
          type: 'line',
          source: 'line-' + line.id,
          layout: { 'line-cap': 'round', 'line-join': 'round' },
          paint: {
            'line-color': line.color || '#e0cb8f',
            'line-width': 10,
            'line-opacity': 0.2,
            'line-blur': 1.5,
          },
        });
        map.addLayer({
          id: 'line-' + line.id,
          type: 'line',
          source: 'line-' + line.id,
          layout: { 'line-cap': 'round', 'line-join': 'round' },
          paint: {
            'line-color': line.color || '#e0cb8f',
            'line-width': 3,
            'line-opacity': 0.95,
            'line-dasharray': line.optional || line.dashed ? [2, 2] : [1, 0],
          },
        });
      });

      map.addLayer({
        id: 'stops-halo',
        type: 'circle',
        source: 'stops',
        paint: { 'circle-radius': 12, 'circle-color': '#e0cb8f', 'circle-opacity': 0.16 },
      });
      map.addLayer({
        id: 'stops',
        type: 'circle',
        source: 'stops',
        paint: {
          'circle-radius': 6,
          'circle-color': '#ffffff',
          'circle-stroke-width': 2.5,
          'circle-stroke-color': '#e0cb8f',
        },
      });
      map.addLayer({
        id: 'stops-label',
        type: 'symbol',
        source: 'stops',
        layout: {
          'text-field': ['get', 'label'],
          'text-size': 12,
          'text-offset': [0, 1.35],
          'text-anchor': 'top',
          'text-font': ['Open Sans Semibold', 'Arial Unicode MS Regular'],
          'text-max-width': 10,
        },
        paint: {
          'text-color': '#f7f7f8',
          'text-halo-color': 'rgba(10,10,10,0.9)',
          'text-halo-width': 1.4,
        },
      });

      if (allCoords.length) {
        let minX = Infinity,
          minY = Infinity,
          maxX = -Infinity,
          maxY = -Infinity;
        allCoords.forEach(([x, y]) => {
          minX = Math.min(minX, x);
          maxX = Math.max(maxX, x);
          minY = Math.min(minY, y);
          maxY = Math.max(maxY, y);
        });
        map.fitBounds(
          [
            [minX, minY],
            [maxX, maxY],
          ],
          {
            padding: { top: 48, bottom: 48, left: 40, right: 40 },
            duration: 0,
            maxZoom: mapCfg.fit_max_zoom || 10.2,
          }
        );
      }

      map.on('click', 'stops', (e) => selectStop(e.features[0].properties.key));
      map.on('mouseenter', 'stops', () => {
        map.getCanvas().style.cursor = 'pointer';
      });
      map.on('mouseleave', 'stops', () => {
        map.getCanvas().style.cursor = '';
      });
    });
  }

  function setLineOpacity(focusId) {
    if (!map) return;
    lines.forEach((line) => {
      if (!map.getLayer('line-' + line.id)) return;
      const on = !focusId || line.id === focusId;
      map.setPaintProperty('line-' + line.id, 'line-opacity', on ? 0.98 : 0.18);
      map.setPaintProperty('line-glow-' + line.id, 'line-opacity', on ? 0.28 : 0.05);
      map.setPaintProperty('line-' + line.id, 'line-width', on ? 3.5 : 2);
    });
  }

  function waterMinLabel(seg) {
    if (seg.water_min != null) return `~${seg.water_min} min on the water`;
    if (seg.distance_nm != null) {
      const mins = Math.ceil(seg.distance_nm / 20 * 60 / 5) * 5;
      return `${seg.distance_nm} nm · ~${mins} min on the water`;
    }
    return 'Water time indicative';
  }

  function selectLine(id) {
    setLineOpacity(id);
    const line = lines.find((l) => l.id === id);
    [...document.querySelectorAll('.line-btn')].forEach((b) => b.classList.toggle('active', b.dataset.id === id));
    [...document.querySelectorAll('.stop-btn')].forEach((b) => b.classList.remove('active'));
    if (!line) return;
    const segs = (line.segments || [])
      .map((s) => {
        const a = nodesByKey[s.from]?.label || s.from;
        const b = nodesByKey[s.to]?.label || s.to;
        const drive =
          s.drive_min && s.drive_min.length
            ? `<span>${s.drive_min[0]}–${s.drive_min[1]} min driving</span>`
            : '';
        return `<div style="margin-top:10px"><strong>${a} → ${b}</strong>
        <div class="time-chip"><span><em>${waterMinLabel(s)}</em></span>${drive}</div></div>`;
      })
      .join('');
    const trigger = (DATA.locked_numbers && DATA.locked_numbers.launch_trigger_committed_seats) ||
      (DATA.locked_numbers && DATA.locked_numbers.corridor_launch_trigger_committed_seats) || [60, 80];
    const tLabel = Array.isArray(trigger) ? `${trigger[0]}–${trigger[1]}` : String(trigger);
    document.getElementById('map-detail').innerHTML = `<strong>${line.name}</strong>
      <div style="margin-top:6px">A line launches when about ${tLabel} seats are committed. No public timetable yet — times below are one-way planning ranges.</div>${segs}
      <div style="margin-top:14px"><button type="button" class="btn btn-primary btn-sm" id="use-line-preset">Use this line in the calculator</button></div>`;
    document.getElementById('use-line-preset')?.addEventListener('click', () => {
      if (line.calculator_preset) {
        Object.assign(state, {
          car_min: line.calculator_preset.car_min ?? state.car_min,
          water_min: line.calculator_preset.water_min ?? state.water_min,
          car_miles: line.calculator_preset.car_miles ?? state.car_miles,
        });
        renderFields();
        recompute();
      }
      document.getElementById('f-line').value = line.id;
      document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' });
    });
    document.getElementById('f-line').value = line.id;
    if (map && line.water_path?.length) {
      let minX = Infinity,
        minY = Infinity,
        maxX = -Infinity,
        maxY = -Infinity;
      line.water_path.forEach(([x, y]) => {
        minX = Math.min(minX, x);
        maxX = Math.max(maxX, x);
        minY = Math.min(minY, y);
        maxY = Math.max(maxY, y);
      });
      map.fitBounds(
        [
          [minX, minY],
          [maxX, maxY],
        ],
        { padding: 60, duration: 700, maxZoom: 10.6 }
      );
    }
  }

  function selectStop(key) {
    const n = nodesByKey[key];
    if (!n) return;
    [...document.querySelectorAll('.stop-btn')].forEach((b) => b.classList.toggle('active', b.dataset.key === key));
    const touch = lines
      .filter((l) => (l.stops || []).includes(key))
      .map((l) => l.name)
      .join(' · ');
    document.getElementById('map-detail').innerHTML = `<strong>${n.label}</strong>
      <div style="margin-top:6px">${servesText(n)}</div>
      <div style="margin-top:8px;color:var(--text-2);font-size:12px">Lines: ${touch || '—'}</div>
      <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">
        <button type="button" class="btn btn-primary btn-sm" id="use-stop">Use as my office terminal</button>
      </div>`;
    document.getElementById('use-stop')?.addEventListener('click', () => {
      document.getElementById('f-stop').value = key;
      const line = lines.find((l) => (l.stops || []).includes(key));
      if (line) {
        document.getElementById('f-line').value = line.id;
        if (line.calculator_preset) {
          Object.assign(state, {
            car_min: line.calculator_preset.car_min ?? state.car_min,
            water_min: line.calculator_preset.water_min ?? state.water_min,
            car_miles: line.calculator_preset.car_miles ?? state.car_miles,
          });
          renderFields();
          recompute();
        }
      }
      document.getElementById('letter').scrollIntoView({ behavior: 'smooth' });
    });
    if (map) {
      map.flyTo({ center: [n.lng, n.lat], zoom: Math.max(map.getZoom(), 10.4), duration: 800 });
      popup
        .setLngLat([n.lng, n.lat])
        .setHTML(`<div style="color:#0a0a0a;font:600 12px Inter">${n.label}</div>`)
        .addTo(map);
    }
  }

  const lineList = document.getElementById('line-list');
  if (lineList) {
    lineList.innerHTML = '';
    lines.forEach((line) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'line-btn';
      b.dataset.id = line.id;
      b.innerHTML = `<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${line.color};margin-right:8px;box-shadow:0 0 0 2px rgba(255,255,255,0.06)"></span>${line.name}<span class="sub">${(line.stops || []).map((k) => nodesByKey[k]?.label || k).join(' · ')}</span>`;
      b.addEventListener('click', () => selectLine(line.id));
      lineList.appendChild(b);
    });
  }
  const stopList = document.getElementById('stop-list');
  if (stopList) {
    stopList.innerHTML = '';
    stops.forEach((n) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'stop-btn';
      b.dataset.key = n.key;
      b.innerHTML = `${n.label}<span class="sub">${servesText(n)}</span>`;
      b.addEventListener('click', () => selectStop(n.key));
      stopList.appendChild(b);
    });
  }

  if (document.getElementById('map')) initMap();

  // Form selects
  const stopSel = document.getElementById('f-stop');
  if (stopSel) {
    stopSel.innerHTML = '';
    stops.forEach((n) => {
      const o = document.createElement('option');
      o.value = n.key;
      o.textContent = n.label;
      stopSel.appendChild(o);
    });
  }
  const lineSel = document.getElementById('f-line');
  if (lineSel) {
    lineSel.innerHTML = '<option value="">Not sure yet</option>';
    lines.forEach((l) => {
      const o = document.createElement('option');
      o.value = l.id;
      o.textContent = l.name;
      lineSel.appendChild(o);
    });
  }

  document.querySelectorAll('#flavor-options .option').forEach((btn) => {
    btn.addEventListener('click', () => {
      flavor = btn.dataset.flavor;
      document.getElementById('f-flavor').value = flavor;
      document.querySelectorAll('#flavor-options .option').forEach((b) => b.classList.toggle('active', b === btn));
    });
  });

  function flavorLabel(id) {
    for (const key of Object.keys(flavors)) {
      if (flavors[key].id === id) return flavors[key].title;
    }
    return id === 'B' ? 'Option B — Anchor a line' : 'Option A — Reserve seats';
  }

  function buildLoiPayload(fd) {
    const stop = fd.get('stop');
    const line = fd.get('line');
    const c = window.__HUB_CALC__ || {};
    return {
      name: fd.get('name'),
      company: fd.get('company'),
      role: fd.get('role'),
      email: fd.get('email'),
      stop,
      stopLabel: nodesByKey[stop]?.label || stop,
      line: line || '',
      lineLabel: lines.find((l) => l.id === line)?.name || (line || 'Not sure yet'),
      employees: fd.get('employees') || 'n/a',
      cc: fd.get('cc') || '',
      flavor: fd.get('flavor') || flavor || 'A',
      flavorLabel: flavorLabel(fd.get('flavor') || flavor || 'A'),
      netIncremental: money(c.net_incremental || 0),
      perRider: money(c.per_rider || c.net_employer_cost_per_rider || 0),
      seats: c.S != null ? String(c.S) : '',
      hp: fd.get('hp') || '',
      source: HUB_ID,
      hub_id: HUB_ID,
    };
  }

  function openMailtoFallback(payload) {
    const loiCfg = DATA.loi || {};
    const subj = encodeURIComponent(
      `${loiCfg.mailto_subject_prefix || market.label + ' employer letter of intent'} — ${payload.company}`
    );
    const netLabel = loiCfg.mailto_network_label || `${market.label || HUB_ID} employer water network`;
    const body = encodeURIComponent(
      `Non-binding letter of intent — ${netLabel}

I am submitting a non-binding letter of intent. This costs nothing and commits nothing.

Hub: ${HUB_ID}
Name: ${payload.name}
Company: ${payload.company}
Role: ${payload.role}
Email: ${payload.email}
Nearest office terminal: ${payload.stopLabel}
Preferred line: ${payload.lineLabel}
Estimated interested employees: ${payload.employees}
Path: ${payload.flavorLabel}

Planning estimate (not a quote): net incremental ~${payload.netIncremental}/mo (~${payload.perRider}/rider) at ${payload.seats || '—'} seats.

Please follow up to discuss next steps.`
    );
    let mailto = `mailto:${contact}?subject=${subj}&body=${body}`;
    if (payload.cc) mailto += `&cc=${encodeURIComponent(payload.cc)}`;
    window.location.href = mailto;
  }

  document.getElementById('loi-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const btn = document.getElementById('loi-submit');
    const status = document.getElementById('loi-status');
    const success = document.getElementById('loi-success');
    const payload = buildLoiPayload(new FormData(form));

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
      } catch {
        /* non-json */
      }

      if (res.ok && data && data.ok) {
        status.textContent = '';
        status.hidden = true;
        success.classList.add('show');
        form.reset();
        document.getElementById('f-flavor').value = flavor;
        return;
      }

      if (res.status === 503 || res.status === 502 || res.status >= 500) {
        status.textContent = 'Opening email draft as backup…';
        openMailtoFallback(payload);
        success.innerHTML = `<strong>Draft ready.</strong> We could not reach the server intake, so your mail client should open with a non-binding letter. Or email <a href="mailto:${contact}">${contact}</a> directly.`;
        success.classList.add('show');
        return;
      }

      status.textContent =
        data && data.error === 'invalid_email'
          ? 'Please use a valid work email.'
          : 'Please check the form and try again.';
    } catch (err) {
      console.warn('[employer-hub] LOI submit failed', err);
      status.textContent = 'Opening email draft as backup…';
      openMailtoFallback(payload);
      success.innerHTML = `<strong>Draft ready.</strong> Offline or network error — your mail client should open with a non-binding letter. Or email <a href="mailto:${contact}">${contact}</a>.`;
      success.classList.add('show');
    } finally {
      btn.disabled = false;
    }
  });

  console.info('[employer-hub]', HUB_ID, 'stops', stops.map((n) => ({ key: n.key, bp: n.resolved_bp_id })));
})();
