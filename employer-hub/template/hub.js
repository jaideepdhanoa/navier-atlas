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
  /** When true (public-partners / fleet-investors pages): map + trip planner only; skip employer LOI/calc chrome. */
  const MAP_ONLY = !!window.EMPLOYER_HUB_MAP_ONLY;
  const stops = DATA.stops || DATA.nodes || [];
  const lines = (DATA.lines || []).filter((l) => l.id);
  const nodesByKey = Object.fromEntries(stops.map((n) => [n.key, n]));
  const copy = DATA.copy || {};
  const market = DATA.market || {};
  const brand = DATA.brand || {};
  const calcMeta = DATA.calculator || DATA.roi_calculator || {};
  const profile = calcMeta.profile || 'bay_productivity';
  const contact = market.contact_email || 'jaideep@navierboat.com';
  const networkCfg = DATA.network || {};
  const phaseLabels = networkCfg.phase_labels || ['At launch', '+ Phase 2', 'Full network'];
  let activePhase = networkCfg.default_phase || 1;
  let showSeasonal = !!networkCfg.show_seasonal_default;
  const clusterDefs = networkCfg.clusters || [];
  let activeCluster =
    networkCfg.default_cluster ||
    (clusterDefs[0] && (clusterDefs[0].id || clusterDefs[0])) ||
    null;
  let map, popup, flavor, highlightKeys = null;
  /** @type {null | { from: string, to: string, path: object }} */
  let activeTrip = null;
  /** Last successful Find-my-ride snapshot for LOI sales context */
  let lastTripSnapshot = null;
  const tripCfg = DATA.trip_planner || {};
  const tripEnabled = tripCfg.enabled !== false;

  function inActiveCluster(obj) {
    if (!activeCluster) return true;
    if (!obj) return false;
    const c = obj.cluster;
    // Objects without cluster stay visible (single-network hubs)
    if (c == null || c === '') return true;
    return c === activeCluster;
  }
  function stopVisible(s) {
    if (!s) return false;
    if (s.exec_only) return false; // never on public employer map
    if (!inActiveCluster(s)) return false;
    if (s.seasonal || (s.tag && /seasonal/i.test(String(s.tag)))) {
      // Seasonal stops still require phase + seasonal toggle when line is seasonal
      if (s.seasonal && !showSeasonal && (s.phase || 1) > 1) {
        // fall through: phase gate may still show if phase allows and not line-seasonal-only
      }
    }
    if (s.seasonal && !showSeasonal) return false;
    return (s.phase || 1) <= activePhase;
  }
  function segmentVisible(seg, line) {
    if (!seg || !line) return false;
    if (line.exec_only) return false;
    if (!inActiveCluster(line)) return false;
    if (line.seasonal || line.type === 'seasonal') {
      if (!showSeasonal) return false;
    }
    const ph = seg.phase != null ? seg.phase : (line.phase || 1);
    if (ph > activePhase) return false;
    // phase_max: hide short-turn / alternate segments once later build-out is live
    if (seg.phase_max != null && activePhase > seg.phase_max) return false;
    return true;
  }
  function lineVisible(l) {
    if (!l) return false;
    if (l.exec_only) return false;
    if (!inActiveCluster(l)) return false;
    if (l.seasonal || l.type === 'seasonal') return showSeasonal;
    // Show line if it has any segment live at this phase (not only line.phase)
    const segs = l.segments || [];
    if (segs.length) return segs.some((seg) => segmentVisible(seg, l));
    return (l.phase || 1) <= activePhase;
  }
  function visibleStops() { return stops.filter(stopVisible); }
  function visibleLines() { return lines.filter(lineVisible); }
  function typeBadge(t) {
    const x = t || 'trunk';
    return `<span class="type-badge type-${x}">${x}</span>`;
  }

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

  // Full-bleed map section (content columns stay constrained elsewhere)
  const netSec = document.getElementById('network');
  if (netSec) netSec.classList.add('network-bleed');

  if (!MAP_ONLY) {
    document.title = brand.title || document.title;
    setText('hero-headline', copy.hero_headline);
    setText('hero-sub', copy.hero_sub);
    setText('hero-eyebrow', market.eyebrow || `${market.label || ''} · Employer water network`);
    setText('nav-tag', brand.nav_tag || market.tagline || 'Employer network');
    setText('stripe-lesson', copy.stripe_lesson || copy.precedent || '');
    setText('loi-cta', copy.loi_cta);
    setText('price-anchor', copy.price_anchor || '');
    setText('footer-note', copy.footer_note || 'Letters of intent are non-binding.');
    setText('calc-caveat', calcMeta.caveat || 'Indicative planning tool, not a quote.');
    setText('launch-trigger', copy.launch_trigger || '');
    setText('proof-title', copy.proof_title || 'We already proved the ride.');
    setText('proof-lead', copy.proof_lead || '');
    setText('why-title', copy.why_title || 'Why water');
    setText('why-lead', copy.why_lead || copy.problem_lead || '');
    setText('office-title', copy.office_title || 'One campus. Full network access.');
    setText('office-lead', copy.office_lead || '');
    setText('office-insight', copy.office_insight || '');
    setText('network-footnote', copy.network_footnote || '');
    setText(
      'products-title',
      (DATA.products && DATA.products.section_title) || copy.products_title || 'How employers join'
    );
    setText(
      'products-lead',
      (DATA.products && DATA.products.section_lead) || copy.products_lead || ''
    );
    setText('network-title', copy.network_title || 'Your ride on the network');
    setText('network-lead', copy.network_lead || '');
    setText('calc-title', copy.calc_title || 'Rough cost for your team');
    setHtml('calc-lead', copy.calc_lead_html || copy.calc_lead || '');
    setText('loi-title', copy.loi_title || 'Reserve interest for your campus');
    setText('hero-note', copy.hero_note || 'Non-binding letter of intent · no commitment');
    setText('map-detail', copy.map_detail_empty || 'Pick two terminals above — or select a line or stop.');
    setText('hero-cta-network', copy.hero_cta_network || 'Find a route to my office');
    setText('hero-cta-loi', copy.hero_cta_loi || copy.nav_cta || 'Reserve interest');
    setText('nav-cta', copy.nav_cta || 'Reserve interest');
    const stickyBtn = document.getElementById('sticky-cta-btn');
    if (stickyBtn) stickyBtn.textContent = copy.nav_cta || 'Reserve interest';
    const heroLoi = document.getElementById('hero-cta-loi');
    if (heroLoi) heroLoi.textContent = copy.hero_cta_loi || copy.nav_cta || 'Reserve interest';

    const heroStats = document.getElementById('hero-stats');
    if (heroStats) {
      const nStops = stops.filter((s) => !s.exec_only && !s.seasonal).length;
      const nLines = lines.filter((l) => !l.exec_only && !(l.seasonal || l.type === 'seasonal')).length;
      const stats = copy.hero_stats || [
        { value: String(nStops), label: 'terminals' },
        { value: String(nLines), label: 'lines' },
        { value: '1 seat', label: 'plugs into the network' },
      ];
      heroStats.hidden = false;
      heroStats.innerHTML = stats
        .map((s) => `<div class="hero-stat"><div class="v">${s.value}</div><div class="l">${s.label}</div></div>`)
        .join('');
    }

    const proofMeta = document.getElementById('proof-meta');
    if (proofMeta) {
      const bits = [
        copy.proof_worked_body &&
          `<strong>${copy.proof_worked_title || 'Worked'}:</strong> ${copy.proof_worked_body}`,
        copy.proof_fixed_body &&
          `<strong>${copy.proof_fixed_title || 'Fixed'}:</strong> ${copy.proof_fixed_body}`,
        copy.proof_ask_body && `<strong>${copy.proof_ask_title || 'Ask'}:</strong> ${copy.proof_ask_body}`,
      ].filter(Boolean);
      proofMeta.innerHTML = bits.map((b) => `<div class="proof-meta-item">${b}</div>`).join('');
    }

    document.querySelectorAll('[data-contact-email]').forEach((a) => {
      a.href = 'mailto:' + contact;
      if (a.dataset.contactEmail === 'text') a.textContent = contact;
    });

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
  } else {
    // Map-only: still show network section titles if present
    setText('network-title', copy.network_title || 'The network');
    setText('network-lead', copy.network_lead || '');
    setText('map-detail', copy.map_detail_empty || 'Pick two terminals above — or select a line or stop.');
    setText('network-footnote', copy.network_footnote || DATA.schedules_note || '');
    flavor = 'A';
  }


  // —— Cluster + phase + seasonal controls ——
  const clusterEl = document.getElementById('cluster-toggle');
  const clusterNote = document.getElementById('cluster-note');
  if (clusterEl && clusterDefs.length > 1) {
    clusterEl.hidden = false;
    clusterEl.innerHTML = '';
    clusterDefs.forEach((c) => {
      const id = typeof c === 'string' ? c : c.id;
      const label = typeof c === 'string' ? c : c.label || c.id;
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      b.dataset.cluster = id;
      if (id === activeCluster) b.classList.add('active');
      b.addEventListener('click', () => {
        activeCluster = id;
        [...clusterEl.querySelectorAll('button')].forEach((x) =>
          x.classList.toggle('active', x.dataset.cluster === activeCluster)
        );
        if (clusterNote) {
          const def = clusterDefs.find((x) => (x.id || x) === activeCluster);
          const note = (def && def.note) || networkCfg.cluster_note || copy.two_networks || '';
          if (note) {
            clusterNote.hidden = false;
            clusterNote.textContent = note;
          }
        }
        if (activeTrip) clearTripUI();
        // Refit map to cluster bounds when provided
        const def = clusterDefs.find((x) => (x.id || x) === activeCluster);
        if (map && def && def.map && def.map.center) {
          map.easeTo({ center: def.map.center, zoom: def.map.zoom || map.getZoom(), duration: 600 });
        }
        refreshNetworkUI();
      });
      clusterEl.appendChild(b);
    });
    if (clusterNote) {
      const def = clusterDefs.find((x) => (x.id || x) === activeCluster);
      const note =
        (def && def.note) ||
        networkCfg.cluster_note ||
        copy.two_networks ||
        (copy.sections && copy.sections.two_networks) ||
        '';
      if (note) {
        clusterNote.hidden = false;
        clusterNote.textContent = note;
      }
    }
  } else if (clusterEl) {
    clusterEl.hidden = true;
  }

  const phaseEl = document.getElementById('phase-toggle');
  if (phaseEl) {
    phaseEl.innerHTML = '';
    phaseLabels.forEach((label, i) => {
      const ph = i + 1;
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      b.dataset.phase = String(ph);
      if (ph === activePhase) b.classList.add('active');
      b.addEventListener('click', () => {
        activePhase = ph;
        [...phaseEl.querySelectorAll('button')].forEach((x) => x.classList.toggle('active', Number(x.dataset.phase) === activePhase));
        refreshNetworkUI();
      });
      phaseEl.appendChild(b);
    });
  }
  // Seasonal control is opt-in per hub (e.g. NYC East End). Bay has none.
  // Note: .seasonal-toggle { display:inline-flex } overrides bare [hidden] without !important.
  const seasonWrap = document.getElementById('seasonal-toggle-wrap');
  const seasonCb = document.getElementById('seasonal-toggle');
  const hasSeasonalLines = lines.some((l) => l.seasonal || l.type === 'seasonal');
  const seasonalEnabled = networkCfg.show_seasonal === true ||
    (networkCfg.show_seasonal !== false && hasSeasonalLines);
  if (seasonWrap && seasonCb) {
    if (seasonalEnabled) {
      seasonWrap.hidden = false;
      seasonWrap.classList.remove('is-hidden');
      seasonWrap.style.display = '';
      const labelEl = seasonWrap.querySelector('span');
      if (labelEl && networkCfg.seasonal_label) labelEl.textContent = networkCfg.seasonal_label;
      seasonCb.checked = showSeasonal;
      seasonCb.addEventListener('change', () => {
        showSeasonal = seasonCb.checked;
        refreshNetworkUI();
      });
    } else {
      seasonWrap.hidden = true;
      seasonWrap.classList.add('is-hidden');
      seasonWrap.style.display = 'none';
      showSeasonal = false;
    }
  }

  // Office / catchment — sets trip "To", highlights reachable origins, prefills LOI
  const catchGrid = document.getElementById('catchment-grid');
  function renderCatchment() {
    if (!catchGrid) return;
    const rows = DATA.catchment || [];
    if (!rows.length) {
      const sec = document.getElementById('office');
      if (sec) sec.hidden = true;
      return;
    }
    const filteredCatch = rows.filter((c) => {
      if (!activeCluster) return true;
      if (c.cluster) return c.cluster === activeCluster;
      const stop = nodesByKey[c.anchor_stop];
      return inActiveCluster(stop);
    });
    catchGrid.innerHTML = filteredCatch
      .map((c) => {
        const stop = nodesByKey[c.anchor_stop];
        const label = c.anchor || stop?.label || c.anchor_stop || '';
        return `<button type="button" class="catchment-card" data-anchor="${c.anchor_stop || ''}">
          <h3>${label}</h3>
          <div class="nums">${c.phase1_stations ?? '—'} <span>origins at launch</span> → ${c.full_network_stations ?? '—'} <span>full network</span></div>
          <div class="hint">Set as my office · show who can reach me</div>
        </button>`;
      })
      .join('');
    catchGrid.querySelectorAll('.catchment-card').forEach((card) => {
      card.addEventListener('click', () => {
        catchGrid.querySelectorAll('.catchment-card').forEach((x) => x.classList.remove('active'));
        card.classList.add('active');
        setOfficeStop(card.dataset.anchor);
      });
    });
  }
  renderCatchment();

  function setOfficeStop(anchorKey) {
    if (!anchorKey || !nodesByKey[anchorKey]) return;
    // Prefill LOI + trip To
    const fStop = document.getElementById('f-stop');
    if (fStop) fStop.value = anchorKey;
    const toSel = document.getElementById('trip-to');
    if (toSel) toSel.value = anchorKey;
    highlightCatchment(anchorKey);
    // If From already chosen, run trip; else scroll to trip finder with To set
    const fromSel = document.getElementById('trip-from');
    if (fromSel && fromSel.value && fromSel.value !== anchorKey) {
      runTripPlanner(fromSel.value, anchorKey);
    } else {
      const detail = document.getElementById('map-detail');
      const n = nodesByKey[anchorKey];
      const reach = highlightKeys ? highlightKeys.size : 0;
      if (detail && n) {
        detail.innerHTML = `<strong>${n.label}</strong> <span class="tag-pill">Your office</span>
          <div style="margin-top:6px">${reach} origin station${reach === 1 ? '' : 's'} can reach you on the current phase (including transfers).</div>
          <div style="margin-top:8px;color:var(--text-2);font-size:12px">Pick a home terminal above to see your ride and time vs driving.</div>`;
      }
    }
    document.getElementById('network')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    showStickyCta();
  }

  function highlightCatchment(anchorKey) {
    const g = {};
    visibleLines().forEach((ln) => {
      (ln.segments || []).forEach((seg) => {
        if (!segmentVisible(seg, ln)) return;
        g[seg.from] = g[seg.from] || new Set();
        g[seg.to] = g[seg.to] || new Set();
        g[seg.from].add(seg.to);
        g[seg.to].add(seg.from);
      });
    });
    const seen = new Set([anchorKey]);
    const q = [anchorKey];
    while (q.length) {
      const n = q.shift();
      (g[n] || []).forEach((nb) => {
        if (!seen.has(nb)) {
          seen.add(nb);
          q.push(nb);
        }
      });
    }
    highlightKeys = seen;
    // Don't wipe trip via full refresh — rebuild layers only
    renderLineList();
    renderStopList();
    renderLegend();
    rebuildMapLayers();
    const n = nodesByKey[anchorKey];
    if (n && map) map.flyTo({ center: [n.lng, n.lat], zoom: Math.max(map.getZoom(), 10), duration: 600 });
  }

  function applyTripToCalculator(trip, driveMin) {
    if (!trip) return;
    const hint = document.getElementById('calc-trip-hint');
    if (hint) {
      hint.hidden = false;
      hint.innerHTML = `Using your ride <strong>${trip.fromLabel} → ${trip.toLabel}</strong> (~${Math.round(trip.totalNavier)} min water${
        driveMin != null ? ` · ~${driveMin} min drive` : ''
      }). Adjust fields if needed.`;
    }
    // Prefill common calculator fields when present
    if (state.water_min != null || inputsMeta.water_min) {
      state.water_min = Math.round(trip.totalNavier);
    }
    if (driveMin != null && (state.car_min != null || inputsMeta.car_min)) {
      state.car_min = driveMin;
    }
    if (typeof renderFields === 'function') {
      try {
        renderFields();
        recompute();
      } catch (_) {
        /* calc may init later */
      }
    }
  }

  function showStickyCta() {
    const el = document.getElementById('sticky-cta');
    if (el) el.hidden = false;
  }

  function refreshNetworkUI() {
    renderLineList();
    renderStopList();
    renderLegend();
    rebuildMapLayers();
    populateTripSelects();
    renderCatchment();
    if (activeTrip && activeTrip.from && activeTrip.to) {
      runTripPlanner(activeTrip.from, activeTrip.to);
    }
  }

  // —— Trip planner (from → to) ——
  function isTransferHub(stop) {
    if (!stop) return false;
    if ((stop.hub_rank || 99) <= 2) return true;
    return (stop.role || '').includes('interchange');
  }
  function waterMinutes(seg) {
    if (seg.water_min != null) return Number(seg.water_min);
    if (seg.distance_nm != null) return Math.max(4, Math.round((seg.distance_nm / 20) * 60));
    return 10;
  }
  function driveMinutes(fromKey, toKey) {
    const mat = tripCfg.drive_am_peak || {};
    const k = fromKey + '|' + toKey;
    if (mat[k] != null) return Number(mat[k]);
    const a = nodesByKey[fromKey];
    const b = nodesByKey[toKey];
    if (!a || !b || a.lat == null || b.lat == null) return null;
    const toRad = (d) => (d * Math.PI) / 180;
    const R = 3958.8;
    const dLat = toRad(b.lat - a.lat);
    const dLon = toRad(b.lng - a.lng);
    const x =
      Math.sin(dLat / 2) ** 2 +
      Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLon / 2) ** 2;
    const miles = 2 * R * Math.asin(Math.sqrt(x));
    return Math.max(15, Math.round((miles / 18) * 60 + 15));
  }
  function orientedCoords(seg, fromKey) {
    const c = (seg.water_path && seg.water_path.length) ? seg.water_path.slice() : null;
    if (!c) {
      const a = nodesByKey[fromKey];
      const b = nodesByKey[fromKey === seg.from ? seg.to : seg.from];
      if (a && b) return [[a.lng, a.lat], [b.lng, b.lat]];
      return [];
    }
    // Ensure coords run from fromKey toward the other end
    if (fromKey === seg.to) return c.reverse();
    return c;
  }
  /** Segments available on the full planned network (for trip routing — ignore map phase filter). */
  function segmentInTripGraph(seg, line) {
    if (!seg || !line || line.exec_only) return false;
    if (!inActiveCluster(line)) return false;
    if (line.seasonal || line.type === 'seasonal') {
      if (!showSeasonal) return false;
    }
    // Exclude early short-turns that disappear once the full spine exists
    if (seg.phase_max != null && seg.phase_max < 3) return false;
    return true;
  }
  function stopPhaseLabel(stop) {
    const ph = Math.min(3, Math.max(1, stop.phase || 1));
    if (ph <= 1) return '';
    // Customer-facing availability (same labels as map control, not "later phase")
    const label = phaseLabels[ph - 1] || '';
    return label ? ` · ${label}` : '';
  }
  function tripRequiredPhase(chain) {
    let maxPh = 1;
    chain.forEach((rec) => {
      const seg = rec.edge.seg;
      const line = rec.edge.line;
      const ph = seg.phase != null ? seg.phase : (line.phase || 1);
      if (ph > maxPh) maxPh = ph;
    });
    return maxPh;
  }

  /** Dijkstra on state (stop|lineId). Always routes on full planned network. */
  function findTrip(fromKey, toKey) {
    if (!fromKey || !toKey || fromKey === toKey) return null;
    const transferMin = tripCfg.transfer_min != null ? tripCfg.transfer_min : 8;
    const maxXfer = tripCfg.max_transfers != null ? tripCfg.max_transfers : 2;

    // Full network graph — employers pick any terminal pair; map phase is visual only
    const edgesByStop = {};
    const addE = (k, e) => {
      if (!edgesByStop[k]) edgesByStop[k] = [];
      edgesByStop[k].push(e);
    };
    lines.forEach((line) => {
      if (line.exec_only) return;
      (line.segments || []).forEach((seg) => {
        if (!segmentInTripGraph(seg, line)) return;
        if (!nodesByKey[seg.from] || !nodesByKey[seg.to]) return;
        const w = waterMinutes(seg);
        addE(seg.from, {
          to: seg.to, from: seg.from, waterMin: w, seg, line,
        });
        addE(seg.to, {
          to: seg.from, from: seg.to, waterMin: w, seg, line,
        });
      });
    });
    if (!edgesByStop[fromKey]) return null;

    // state: stop + '\t' + lineId
    const start = fromKey + '\t';
    const dist = new Map([[start, 0]]);
    const parent = new Map(); // state -> { prevState, edge, didTransfer }
    const pq = [[0, start]];
    const pop = () => {
      let bi = 0;
      for (let i = 1; i < pq.length; i++) if (pq[i][0] < pq[bi][0]) bi = i;
      return pq.splice(bi, 1)[0];
    };
    let endState = null;
    while (pq.length) {
      const [d, st] = pop();
      if (d !== dist.get(st)) continue;
      const tab = st.indexOf('\t');
      const stop = st.slice(0, tab);
      const lineId = st.slice(tab + 1);
      if (stop === toKey) {
        endState = st;
        break;
      }
      const outs = edgesByStop[stop] || [];
      for (const e of outs) {
        let cost = e.waterMin;
        let didTransfer = false;
        if (lineId && lineId !== e.line.id) {
          if (!isTransferHub(nodesByKey[stop])) continue;
          // count transfers along path
          let xfers = 0;
          let walk = st;
          while (parent.has(walk)) {
            if (parent.get(walk).didTransfer) xfers++;
            walk = parent.get(walk).prevState;
          }
          if (xfers >= maxXfer) continue;
          cost += transferMin;
          didTransfer = true;
        }
        const ns = e.to + '\t' + e.line.id;
        const nd = d + cost;
        if (nd < (dist.get(ns) ?? Infinity)) {
          dist.set(ns, nd);
          parent.set(ns, { prevState: st, edge: e, didTransfer, fromStop: stop });
          pq.push([nd, ns]);
        }
      }
    }
    if (!endState) return null;

    // Reconstruct edge list from start to end
    const chain = [];
    let cur = endState;
    while (parent.has(cur)) {
      chain.push(parent.get(cur));
      cur = parent.get(cur).prevState;
    }
    chain.reverse();

    const transferMinUse = transferMin;
    const steps = [];
    const allCoords = [];
    let waterTotal = 0;
    let transferTotal = 0;
    let transfers = 0;
    let i = 0;
    while (i < chain.length) {
      const rec = chain[i];
      if (rec.didTransfer) {
        transfers++;
        transferTotal += transferMinUse;
        steps.push({
          kind: 'transfer',
          stopKey: rec.fromStop,
          label: nodesByKey[rec.fromStop]?.label || rec.fromStop,
          mins: transferMinUse,
          toLine: rec.edge.line.name,
          toColor: rec.edge.line.color || '#e0cb8f',
        });
      }
      const lid = rec.edge.line.id;
      let j = i + 1;
      while (j < chain.length && !chain[j].didTransfer && chain[j].edge.line.id === lid) j++;
      let w = 0;
      let constrained = false;
      const coords = [];
      for (let k = i; k < j; k++) {
        w += chain[k].edge.waterMin;
        if (chain[k].edge.seg && chain[k].edge.seg.speed_constrained) constrained = true;
        const c = orientedCoords(chain[k].edge.seg, chain[k].fromStop);
        if (!c.length) continue;
        if (!coords.length) coords.push(...c);
        else coords.push(...c.slice(1));
      }
      const fromFixed = chain[i].fromStop;
      const toFixed = chain[j - 1].edge.to;
      waterTotal += w;
      if (coords.length) allCoords.push(...coords);
      steps.push({
        kind: 'water',
        fromKey: fromFixed,
        toKey: toFixed,
        fromLabel: nodesByKey[fromFixed]?.label || fromFixed,
        toLabel: nodesByKey[toFixed]?.label || toFixed,
        lineId: lid,
        lineName: rec.edge.line.name,
        lineColor: rec.edge.line.color || '#e0cb8f',
        mins: w,
        speedConstrained: constrained,
        pathCoords: coords,
      });
      i = j;
    }
    const requiredPhase = tripRequiredPhase(chain);
    const anyConstrained = steps.some((s) => s.kind === 'water' && s.speedConstrained);
    return {
      from: fromKey,
      to: toKey,
      fromLabel: nodesByKey[fromKey]?.label || fromKey,
      toLabel: nodesByKey[toKey]?.label || toKey,
      steps,
      waterTotal,
      transferTotal,
      transfers,
      totalNavier: waterTotal + transferTotal,
      pathCoords: allCoords,
      requiredPhase,
      requiredPhaseLabel: phaseLabels[requiredPhase - 1] || null,
      speedConstrained: anyConstrained,
    };
  }

  function clearTripUI() {
    activeTrip = null;
    lastTripSnapshot = null;
    const res = document.getElementById('trip-result');
    const clr = document.getElementById('trip-clear');
    if (res) {
      res.hidden = true;
      res.innerHTML = '';
    }
    if (clr) clr.hidden = true;
    removeTripMapLayers();
    if (map && map.isStyleLoaded()) {
      visibleLines().forEach((line) => {
        if (!map.getLayer('line-' + line.id)) return;
        map.setPaintProperty('line-' + line.id, 'line-opacity', 0.95);
        map.setPaintProperty('line-glow-' + line.id, 'line-opacity', 0.18);
      });
    }
  }

  function captureTripSnapshot(trip, driveMin) {
    if (!trip) {
      lastTripSnapshot = null;
      return;
    }
    const drive = driveMin != null ? driveMin : driveMinutes(trip.from, trip.to);
    // Always capture model minutes — drive times are also estimates; don't blank Navier in LOI.
    const navierPart = '~' + Math.round(trip.totalNavier) + ' min Navier';
    lastTripSnapshot = {
      tripFrom: trip.from,
      tripFromLabel: trip.fromLabel,
      tripTo: trip.to,
      tripToLabel: trip.toLabel,
      tripNavierMin: String(Math.round(trip.totalNavier)),
      tripDriveMin: drive != null ? String(Math.round(drive)) : '',
      tripTransfers: String(trip.transfers || 0),
      tripSummary:
        trip.fromLabel +
        ' → ' +
        trip.toLabel +
        ' · ' +
        navierPart +
        (drive != null ? ' vs ~' + Math.round(drive) + ' min drive' : '') +
        (trip.transfers ? ' · ' + trip.transfers + ' transfer(s)' : ' · direct'),
    };
  }
  function removeTripMapLayers() {
    if (!map) return;
    ['trip-path-glow', 'trip-path', 'trip-endpoints'].forEach((id) => {
      if (map.getLayer(id)) map.removeLayer(id);
    });
    ['trip-path', 'trip-endpoints'].forEach((id) => {
      if (map.getSource(id)) map.removeSource(id);
    });
  }
  function paintTripOnMap(trip) {
    if (!map || !map.isStyleLoaded() || !trip) return;
    removeTripMapLayers();
    visibleLines().forEach((line) => {
      if (!map.getLayer('line-' + line.id)) return;
      map.setPaintProperty('line-' + line.id, 'line-opacity', 0.14);
      map.setPaintProperty('line-glow-' + line.id, 'line-opacity', 0.05);
    });
    const coords = (trip.pathCoords || []).filter((c) => Array.isArray(c) && c.length >= 2);
    if (coords.length >= 2) {
      map.addSource('trip-path', {
        type: 'geojson',
        data: { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: coords } },
      });
      map.addLayer({
        id: 'trip-path-glow', type: 'line', source: 'trip-path',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': '#e0cb8f', 'line-width': 12, 'line-opacity': 0.28, 'line-blur': 2 },
      });
      map.addLayer({
        id: 'trip-path', type: 'line', source: 'trip-path',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': '#f0e2b0', 'line-width': 4.5, 'line-opacity': 0.98 },
      });
      let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
      coords.forEach(([x, y]) => {
        minX = Math.min(minX, x); maxX = Math.max(maxX, x);
        minY = Math.min(minY, y); maxY = Math.max(maxY, y);
      });
      map.fitBounds([[minX, minY], [maxX, maxY]], {
        padding: { top: 70, bottom: 70, left: 56, right: 56 },
        duration: 700, maxZoom: 12.2,
      });
    }
    const feats = [];
    const a = nodesByKey[trip.from];
    const b = nodesByKey[trip.to];
    if (a) feats.push({ type: 'Feature', properties: { role: 'from' }, geometry: { type: 'Point', coordinates: [a.lng, a.lat] } });
    if (b) feats.push({ type: 'Feature', properties: { role: 'to' }, geometry: { type: 'Point', coordinates: [b.lng, b.lat] } });
    trip.steps.filter((s) => s.kind === 'transfer').forEach((s) => {
      const n = nodesByKey[s.stopKey];
      if (n) feats.push({ type: 'Feature', properties: { role: 'xfer' }, geometry: { type: 'Point', coordinates: [n.lng, n.lat] } });
    });
    map.addSource('trip-endpoints', { type: 'geojson', data: { type: 'FeatureCollection', features: feats } });
    map.addLayer({
      id: 'trip-endpoints', type: 'circle', source: 'trip-endpoints',
      paint: {
        'circle-radius': ['match', ['get', 'role'], 'xfer', 9, 11],
        'circle-color': ['match', ['get', 'role'], 'from', '#7dd3c0', 'to', '#e0cb8f', '#f0e2b0'],
        'circle-stroke-width': 2.5,
        'circle-stroke-color': '#0a0a0a',
      },
    });
  }
  function renderTripResult(trip, driveMin) {
    const res = document.getElementById('trip-result');
    const clr = document.getElementById('trip-clear');
    if (!res) return;
    if (!trip) {
      res.hidden = false;
      res.innerHTML = `<p class="trip-caveat">${tripCfg.no_path || 'No connected water path at this phase.'}</p>`;
      if (clr) clr.hidden = false;
      return;
    }
    // Drive times are also estimates — always show Navier model minutes so sales can compare.
    const save = driveMin != null ? driveMin - trip.totalNavier : null;
    const saveHtml =
      save != null && save > 0
        ? `<div class="trip-save">Save ~${Math.round(save)} min vs driving this trip</div>`
        : save != null
          ? `<div class="trip-save" style="color:var(--text-1);background:rgba(255,255,255,0.04);border-color:var(--line)">Similar to peak drive time — still skips toll stress &amp; parking</div>`
          : '';
    const xferNote =
      trip.transfers > 0
        ? `${trip.transfers} transfer${trip.transfers > 1 ? 's' : ''} · ${trip.transferTotal} min at hub${trip.transfers > 1 ? 's' : ''}`
        : 'Direct · no transfer';
    const phaseNote =
      trip.requiredPhase > 1 && trip.requiredPhaseLabel
        ? `<div class="trip-phase-note">This ride uses corridors on the planned <strong>${trip.requiredPhaseLabel}</strong> network — times assume those terminals are live.</div>`
        : '';
    const stepsHtml = trip.steps
      .map((s, idx) => {
        if (s.kind === 'transfer') {
          return `<div class="trip-step transfer">
            <span class="n">${idx + 1}</span>
            <div><strong>Transfer at ${s.label}</strong>
              <div style="margin-top:3px;font-size:12px;color:var(--text-2)">Change to <span class="line-dot" style="background:${s.toColor}"></span>${s.toLine}</div>
            </div>
            <span class="mins">~${s.mins} min</span>
          </div>`;
        }
        return `<div class="trip-step">
          <span class="n">${idx + 1}</span>
          <div><strong>${s.fromLabel} → ${s.toLabel}</strong>
            <div style="margin-top:3px;font-size:12px;color:var(--text-2)"><span class="line-dot" style="background:${s.lineColor}"></span>${s.lineName}</div>
          </div>
          <span class="mins">~${Math.round(s.mins)} min</span>
        </div>`;
      })
      .join('');
    const navierTotal = `<div class="v">~${Math.round(trip.totalNavier)} min</div>
          <div class="hint">Water ~${Math.round(trip.waterTotal)} min${trip.transferTotal ? ` + transfer ~${trip.transferTotal} min` : ''}</div>`;
    res.hidden = false;
    res.innerHTML = `
      <div class="trip-title">${trip.fromLabel} → ${trip.toLabel}</div>
      <p class="trip-sub">${xferNote}</p>
      ${phaseNote}
      <div class="trip-compare">
        <div class="trip-stat">
          <div class="k">Navier</div>
          ${navierTotal}
        </div>
        <div class="trip-stat">
          <div class="k">${tripCfg.drive_label || 'Drive (AM peak)'}</div>
          <div class="v drive">${driveMin != null ? `~${driveMin} min` : '—'}</div>
          <div class="hint">Typical weekday morning peak</div>
        </div>
      </div>
      ${saveHtml}
      <div class="trip-steps">${stepsHtml}</div>
      <p class="trip-caveat">${tripCfg.caveat || 'Indicative planning times, not a published timetable.'}</p>
      <div class="trip-actions">
        <button type="button" class="btn btn-primary btn-sm" id="trip-use-to">Use destination in LOI</button>
      </div>`;
    if (clr) clr.hidden = false;
    document.getElementById('trip-use-to')?.addEventListener('click', () => {
      const sel = document.getElementById('f-stop');
      if (sel) sel.value = trip.to;
      const lineStep = trip.steps.find((s) => s.kind === 'water');
      if (lineStep && document.getElementById('f-line')) document.getElementById('f-line').value = lineStep.lineId || '';
      document.getElementById('letter')?.scrollIntoView({ behavior: 'smooth' });
    });
  }
  function runTripPlanner(fromKey, toKey) {
    if (!fromKey || !toKey) {
      clearTripUI();
      return;
    }
    if (fromKey === toKey) {
      clearTripUI();
      const res = document.getElementById('trip-result');
      if (res) {
        res.hidden = false;
        res.innerHTML = '<p class="trip-caveat">Choose two different terminals.</p>';
      }
      document.getElementById('trip-clear') && (document.getElementById('trip-clear').hidden = false);
      return;
    }
    const trip = findTrip(fromKey, toKey);
    const drive = driveMinutes(fromKey, toKey);
    if (trip) {
      activeTrip = { from: fromKey, to: toKey, path: trip };
      captureTripSnapshot(trip, drive);
      paintTripOnMap(trip);
      renderTripResult(trip, drive);
      const detail = document.getElementById('map-detail');
      if (detail) {
        const phaseBit =
          trip.requiredPhase > 1 && trip.requiredPhaseLabel
            ? ` · ${trip.requiredPhaseLabel}`
            : '';
        const timeBit = `~${Math.round(trip.totalNavier)} min on Navier`;
        detail.innerHTML = `<strong>Your ride</strong>
          <div style="margin-top:6px">${trip.fromLabel} → ${trip.toLabel} · ${timeBit}${
            drive != null ? ` vs ~${drive} min drive` : ''
          }${phaseBit}</div>`;
      }
      // Prefill LOI office + calc from this trip
      const fStop = document.getElementById('f-stop');
      if (fStop) fStop.value = toKey;
      const lineStep = trip.steps.find((s) => s.kind === 'water');
      if (lineStep && document.getElementById('f-line')) {
        document.getElementById('f-line').value = lineStep.lineId || '';
      }
      applyTripToCalculator(trip, drive);
      showStickyCta();
      return;
    }
    // No path on full planned network (disconnected stops)
    activeTrip = { from: fromKey, to: toKey, path: null };
    lastTripSnapshot = null;
    removeTripMapLayers();
    const res = document.getElementById('trip-result');
    const clr = document.getElementById('trip-clear');
    if (res) {
      res.hidden = false;
      res.innerHTML = `<p class="trip-caveat">${
        tripCfg.no_path_full ||
        'No water connection between these terminals on the planned network yet.'
      }</p>`;
    }
    if (clr) clr.hidden = false;
  }
  function populateTripSelects() {
    const fromSel = document.getElementById('trip-from');
    const toSel = document.getElementById('trip-to');
    if (!fromSel || !toSel) return;
    const prevFrom = fromSel.value;
    const prevTo = toSel.value;
    // All public terminals; label with map-control availability (At launch / + Phase 2 / Full network)
    const opts = stops
      .filter((n) => !n.exec_only)
      .filter((n) => {
        if (n.seasonal) return showSeasonal;
        return true;
      })
      .slice()
      .sort((a, b) => {
        const pa = a.phase || 1;
        const pb = b.phase || 1;
        if (pa !== pb) return pa - pb;
        return (a.label || '').localeCompare(b.label || '');
      });
    const fill = (sel, placeholder) => {
      sel.innerHTML = `<option value="">${placeholder}</option>`;
      opts.forEach((n) => {
        const o = document.createElement('option');
        o.value = n.key;
        o.textContent = (n.label || n.key) + stopPhaseLabel(n);
        sel.appendChild(o);
      });
    };
    fill(fromSel, 'From terminal…');
    fill(toSel, 'To terminal…');
    if (prevFrom) fromSel.value = prevFrom;
    if (prevTo) toSel.value = prevTo;
  }
  function initTripFinder() {
    const wrap = document.getElementById('trip-finder');
    if (!wrap || !tripEnabled) {
      if (wrap) wrap.hidden = true;
      return;
    }
    wrap.hidden = false;
    populateTripSelects();
    const fromSel = document.getElementById('trip-from');
    const toSel = document.getElementById('trip-to');
    const swap = document.getElementById('trip-swap');
    const clear = document.getElementById('trip-clear');
    const onChange = () => {
      if (fromSel.value && toSel.value) runTripPlanner(fromSel.value, toSel.value);
      else clearTripUI();
    };
    fromSel.addEventListener('change', onChange);
    toSel.addEventListener('change', onChange);
    swap?.addEventListener('click', () => {
      const f = fromSel.value;
      fromSel.value = toSel.value;
      toSel.value = f;
      onChange();
    });
    clear?.addEventListener('click', () => {
      fromSel.value = '';
      toSel.value = '';
      clearTripUI();
      const detail = document.getElementById('map-detail');
      if (detail) detail.textContent = copy.map_detail_empty || 'Select a line or stop.';
    });
    // Deep links: #trip=from,to  or  ?stop=officeKey  or  ?from=&to=
    const params = new URLSearchParams(location.search || '');
    const hash = (location.hash || '').replace(/^#/, '');
    let deepFrom = params.get('from');
    let deepTo = params.get('to') || params.get('stop');
    if (hash.startsWith('trip=')) {
      const parts = hash.slice(5).split(',');
      deepFrom = deepFrom || parts[0];
      deepTo = deepTo || parts[1];
    } else if (hash.startsWith('stop=')) {
      deepTo = deepTo || hash.slice(5);
    }
    if (deepTo && nodesByKey[deepTo]) {
      toSel.value = deepTo;
      const fStop = document.getElementById('f-stop');
      if (fStop) fStop.value = deepTo;
    }
    if (deepFrom && nodesByKey[deepFrom]) fromSel.value = deepFrom;
    if (deepFrom && deepTo && nodesByKey[deepFrom] && nodesByKey[deepTo]) {
      setTimeout(() => runTripPlanner(deepFrom, deepTo), 700);
    } else if (deepTo && nodesByKey[deepTo] && !deepFrom) {
      setTimeout(() => setOfficeStop(deepTo), 700);
    }
  }

  // Map legend
  const legend = document.getElementById('map-legend');
  function renderLegend() {
    if (!legend) return;
    legend.innerHTML = '';
    visibleLines().forEach((line) => {
      const s = document.createElement('span');
      const sun = (line.seasonal || line.type === 'seasonal') ? ' ☀' : '';
      s.innerHTML = `<i style="background:${line.color}"></i>${line.id}${sun}`;
      legend.appendChild(s);
    });
  }
  renderLegend();

  // —— Calculator ——
  const inputsMeta = calcMeta.inputs || {};
  const state = {};
  Object.keys(inputsMeta).forEach((k) => {
    state[k] = inputsMeta[k].default;
  });
  const fieldsEl = MAP_ONLY ? null : document.getElementById('calc-fields');
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
    if (MAP_ONLY || !document.getElementById('out-net')) return null;
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
    if (MAP_ONLY || !document.getElementById('out-net')) return null;
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
  // MAP_ONLY pages skip calculator DOM — recompute() returns null; do not throw before initMap()
  if (check) {
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

  function dashForType(line) {
    const t = line.type || 'trunk';
    if (t === 'seasonal') return [1, 2];
    if (t === 'express') return [2, 1.5];
    if (t === 'feeder') return [1, 0];
    return line.optional || line.dashed ? [2, 2] : [1, 0];
  }
  function widthForType(line, focus) {
    const t = line.type || 'trunk';
    const base = t === 'trunk' ? 3.2 : t === 'feeder' ? 2.2 : 2.6;
    return focus ? base + 0.8 : base;
  }
  function rebuildMapLayers() {
    if (!map || !map.isStyleLoaded()) return;
    // remove prior line layers/sources
    lines.forEach((line) => {
      ['line-glow-' + line.id, 'line-' + line.id].forEach((id) => {
        if (map.getLayer(id)) map.removeLayer(id);
      });
      if (map.getSource('line-' + line.id)) map.removeSource('line-' + line.id);
    });
    if (map.getLayer('stops-label')) map.removeLayer('stops-label');
    if (map.getLayer('stops')) map.removeLayer('stops');
    if (map.getLayer('stops-halo')) map.removeLayer('stops-halo');
    if (map.getLayer('stops-hub')) map.removeLayer('stops-hub');
    if (map.getSource('stops')) map.removeSource('stops');

    const allCoords = [];
    function lineGeometry(waterPath) {
      if (!waterPath || !waterPath.length) return null;
      const multi = Array.isArray(waterPath[0]) && Array.isArray(waterPath[0][0]);
      if (multi) {
        waterPath.forEach((part) => part.forEach((c) => allCoords.push(c)));
        return { type: 'MultiLineString', coordinates: waterPath };
      }
      waterPath.forEach((c) => allCoords.push(c));
      return { type: 'LineString', coordinates: waterPath };
    }

    visibleLines().forEach((line) => {
      // Prefer per-segment water_path (authoritative); fall back to line.water_path
      const segs = (line.segments || []).filter((seg) => segmentVisible(seg, line));
      let parts = segs.map((seg) => seg.water_path).filter((p) => p && p.length);
      if (!parts.length) {
        let wp = line.water_path;
        if (!wp || !wp.length) return;
        const multi = Array.isArray(wp[0]) && Array.isArray(wp[0][0]);
        parts = multi ? wp : [wp];
      }
      if (!parts.length) return;
      const geom = parts.length === 1
        ? { type: 'LineString', coordinates: parts[0] }
        : { type: 'MultiLineString', coordinates: parts };
      parts.forEach((part) => part.forEach((c) => allCoords.push(c)));
      map.addSource('line-' + line.id, {
        type: 'geojson',
        data: { type: 'Feature', properties: { id: line.id, name: line.name }, geometry: geom },
      });
      const dash = dashForType(line);
      map.addLayer({
        id: 'line-glow-' + line.id, type: 'line', source: 'line-' + line.id,
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': line.color || '#e0cb8f', 'line-width': 10, 'line-opacity': 0.18, 'line-blur': 1.5 },
      });
      map.addLayer({
        id: 'line-' + line.id, type: 'line', source: 'line-' + line.id,
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-color': line.color || '#e0cb8f',
          'line-width': widthForType(line, false),
          'line-opacity': 0.95,
          'line-dasharray': dash,
        },
      });
    });

    const vStops = visibleStops().filter((n) => !highlightKeys || highlightKeys.has(n.key));
    const stopFeatures = visibleStops().map((n) => ({
      type: 'Feature',
      properties: {
        key: n.key, label: n.label, serves: servesText(n), bp: n.resolved_bp_id,
        hub: (n.role || '').includes('interchange') ? 1 : 0,
        hubRank: n.hub_rank || ((n.role || '').includes('interchange_primary') ? 1 : (n.role || '').includes('interchange') ? 2 : 3),
        hi: highlightKeys && highlightKeys.has(n.key) ? 1 : 0,
        dim: highlightKeys && !highlightKeys.has(n.key) ? 1 : 0,
      },
      geometry: { type: 'Point', coordinates: [n.lng, n.lat] },
    }));
    map.addSource('stops', { type: 'geojson', data: { type: 'FeatureCollection', features: stopFeatures } });
    map.addLayer({
      id: 'stops-halo', type: 'circle', source: 'stops',
      paint: {
        'circle-radius': ['case', ['==', ['get', 'hub'], 1], 14, 11],
        'circle-color': '#e0cb8f',
        'circle-opacity': ['case', ['==', ['get', 'dim'], 1], 0.05, 0.16],
      },
    });
    map.addLayer({
      id: 'stops-hub', type: 'circle', source: 'stops',
      filter: ['<=', ['get', 'hubRank'], 2],
      paint: {
        'circle-radius': ['case', ['==', ['get', 'hubRank'], 1], 11, 9],
        'circle-color': 'transparent',
        'circle-stroke-width': ['case', ['==', ['get', 'hubRank'], 1], 3, 2.2],
        'circle-stroke-color': '#e0cb8f',
        'circle-opacity': ['case', ['==', ['get', 'dim'], 1], 0.25, 1],
      },
    });
    map.addLayer({
      id: 'stops', type: 'circle', source: 'stops',
      paint: {
        'circle-radius': 6,
        'circle-color': '#ffffff',
        'circle-stroke-width': 2.5,
        'circle-stroke-color': '#e0cb8f',
        'circle-opacity': ['case', ['==', ['get', 'dim'], 1], 0.25, 1],
      },
    });
    map.addLayer({
      id: 'stops-label', type: 'symbol', source: 'stops',
      // Hubs always labeled; other stops only when zoomed in
      filter: ['any', ['<=', ['get', 'hubRank'], 2], ['>', ['zoom'], 11.5]],
      layout: {
        'text-field': ['get', 'label'],
        'text-size': ['case', ['==', ['get', 'hubRank'], 1], 13, 11],
        'text-offset': [0, 1.35],
        'text-anchor': 'top',
        'text-font': ['Open Sans Semibold', 'Arial Unicode MS Regular'],
        'text-max-width': 10,
        'text-allow-overlap': false,
      },
      paint: {
        'text-color': '#f7f7f8',
        'text-halo-color': 'rgba(10,10,10,0.9)',
        'text-halo-width': 1.4,
        'text-opacity': ['case', ['==', ['get', 'dim'], 1], 0.25, 1],
      },
    });

    // Harbor-first fit on At Launch; wider on full network (skip if trip view is active)
    if (allCoords.length && !activeTrip) {
      const lb = (market.map && market.map.launch_bounds) || null;
      if (activePhase === 1 && lb && !showSeasonal) {
        map.fitBounds(lb, { padding: 48, duration: 0, maxZoom: 12.2 });
      } else {
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        allCoords.forEach(([x, y]) => {
          minX = Math.min(minX, x); maxX = Math.max(maxX, x);
          minY = Math.min(minY, y); maxY = Math.max(maxY, y);
        });
        map.fitBounds([[minX, minY], [maxX, maxY]], {
          padding: { top: 48, bottom: 48, left: 40, right: 40 },
          duration: 0,
          maxZoom: market.map?.fit_max_zoom || 11.5,
        });
      }
    }
    // Re-paint active trip after layer rebuild
    if (activeTrip && activeTrip.path) {
      paintTripOnMap(activeTrip.path);
    }
  }

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
      // Ensure canvas matches container (full-bleed layout can resolve after first paint)
      map.resize();
      rebuildMapLayers();

      map.on('click', 'stops', (e) => selectStop(e.features[0].properties.key));
      map.on('mouseenter', 'stops', () => {
        map.getCanvas().style.cursor = 'pointer';
      });
      map.on('mouseleave', 'stops', () => {
        map.getCanvas().style.cursor = '';
      });
    });
    window.addEventListener('resize', () => {
      if (map) map.resize();
    });
    // Second pass after layout settles (side panel + full-bleed grid)
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (map) {
          map.resize();
          if (map.isStyleLoaded()) rebuildMapLayers();
        }
      });
    });
  }

  function setLineOpacity(focusId) {
    if (!map) return;
    visibleLines().forEach((line) => {
      if (!map.getLayer('line-' + line.id)) return;
      const on = !focusId || line.id === focusId;
      map.setPaintProperty('line-' + line.id, 'line-opacity', on ? 0.98 : 0.18);
      map.setPaintProperty('line-glow-' + line.id, 'line-opacity', on ? 0.28 : 0.05);
      map.setPaintProperty('line-' + line.id, 'line-width', on ? 3.5 : 2);
    });
  }

  function waterMinLabel(seg) {
    // Always prefer a planning number when we have one (drive times are estimates too).
    // Whitelist ranges (time_claim) first; else ~water_min; keep light honesty via the trip caveat, not blank times.
    if (seg.time_claim) {
      const t = String(seg.time_claim).trim();
      // If claim already has a number range, show it; strip pure-disclaimer labels that hide the clock.
      if (/\d/.test(t)) return /indicative/i.test(t) ? t : `${t} (indicative)`;
    }
    if (seg.water_min != null) return `~${seg.water_min} min on the water`;
    if (seg.distance_nm != null) {
      const mins = Math.ceil((seg.distance_nm / 20) * 60 / 5) * 5;
      return `${seg.distance_nm} nm · ~${mins} min on the water`;
    }
    // Fallback only when no model minutes exist
    if (seg.water_min_label && /\d/.test(seg.water_min_label)) return seg.water_min_label;
    return 'Water time indicative';
  }

  function selectLine(id) {
    if (activeTrip) clearTripUI();
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
    const calcBtn = MAP_ONLY
      ? ''
      : `<div style="margin-top:14px"><button type="button" class="btn btn-primary btn-sm" id="use-line-preset">Use this line in the calculator</button></div>`;
    document.getElementById('map-detail').innerHTML = `<strong>${line.name}</strong>
      <div style="margin-top:6px">A line launches when about ${tLabel} seats are committed. No public timetable yet — times below are one-way planning ranges.</div>${segs}${calcBtn}`;
    if (!MAP_ONLY) {
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
        const fl = document.getElementById('f-line');
        if (fl) fl.value = line.id;
        document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth' });
      });
      const fl2 = document.getElementById('f-line');
      if (fl2) fl2.value = line.id;
    }
    if (map && line.water_path?.length) {
      let minX = Infinity,
        minY = Infinity,
        maxX = -Infinity,
        maxY = -Infinity;
      const multi = Array.isArray(line.water_path[0]) && Array.isArray(line.water_path[0][0]);
      const parts = multi ? line.water_path : [line.water_path];
      parts.forEach((part) =>
        part.forEach(([x, y]) => {
          minX = Math.min(minX, x);
          maxX = Math.max(maxX, x);
          minY = Math.min(minY, y);
          maxY = Math.max(maxY, y);
        })
      );
      map.fitBounds(
        [
          [minX, minY],
          [maxX, maxY],
        ],
        { padding: 60, duration: 700, maxZoom: 12.5 }
      );
    }
  }

  function selectStop(key) {
    const n = nodesByKey[key];
    if (!n) return;
    [...document.querySelectorAll('.stop-btn')].forEach((b) => b.classList.toggle('active', b.dataset.key === key));
    const touchLines = lines.filter((l) => !l.exec_only && (l.stops || []).includes(key) && lineVisible(l));
    const touch = touchLines.map((l) => l.id).join(' · ');
    const touchNames = touchLines.map((l) => l.name).join(' · ');
    const isHub = (n.role || '').includes('interchange');
    const hubChip = isHub ? `<div class="transfer-chip">${n.role === 'interchange_primary' ? 'Primary transfer hub' : 'Transfer hub'} · ${touch || '—'}</div>` : '';
    const officeBtn = MAP_ONLY
      ? ''
      : `<button type="button" class="btn btn-primary btn-sm" id="use-stop">Use as my office terminal</button>`;
    document.getElementById('map-detail').innerHTML = `<strong>${n.label}</strong>${n.tag ? ` <span class="tag-pill">${n.tag}</span>` : ''}
      <div style="margin-top:6px">${servesText(n)}</div>
      ${hubChip}
      <div style="margin-top:8px;color:var(--text-2);font-size:12px">Lines: ${touchNames || '—'}</div>
      <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">
        ${officeBtn}
        <button type="button" class="btn btn-ghost btn-sm" id="trip-from-here">Route from here</button>
        <button type="button" class="btn btn-ghost btn-sm" id="trip-to-here">Route to here</button>
      </div>`;
    document.getElementById('use-stop')?.addEventListener('click', () => {
      const fs = document.getElementById('f-stop');
      if (fs) fs.value = key;
      const line = lines.find((l) => (l.stops || []).includes(key));
      if (line) {
        const fl = document.getElementById('f-line');
        if (fl) fl.value = line.id;
        if (line.calculator_preset && !MAP_ONLY) {
          Object.assign(state, {
            car_min: line.calculator_preset.car_min ?? state.car_min,
            water_min: line.calculator_preset.water_min ?? state.water_min,
            car_miles: line.calculator_preset.car_miles ?? state.car_miles,
          });
          renderFields();
          recompute();
        }
      }
      document.getElementById('letter')?.scrollIntoView({ behavior: 'smooth' });
    });
    document.getElementById('trip-from-here')?.addEventListener('click', () => {
      const fromSel = document.getElementById('trip-from');
      const toSel = document.getElementById('trip-to');
      if (fromSel) fromSel.value = key;
      if (fromSel && toSel && toSel.value) runTripPlanner(fromSel.value, toSel.value);
      document.getElementById('trip-finder')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    document.getElementById('trip-to-here')?.addEventListener('click', () => {
      const fromSel = document.getElementById('trip-from');
      const toSel = document.getElementById('trip-to');
      if (toSel) toSel.value = key;
      if (fromSel && toSel && fromSel.value) runTripPlanner(fromSel.value, toSel.value);
      document.getElementById('trip-finder')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    if (map) {
      map.flyTo({ center: [n.lng, n.lat], zoom: Math.max(map.getZoom(), 10.4), duration: 800 });
      popup
        .setLngLat([n.lng, n.lat])
        .setHTML(`<div style="color:#0a0a0a;font:600 12px Inter">${n.label}</div>`)
        .addTo(map);
    }
  }

  function renderLineList() {
    const lineList = document.getElementById('line-list');
    if (!lineList) return;
    lineList.innerHTML = '';
    // Show all non-exec lines; dim those beyond phase
    lines.filter((l) => !l.exec_only).forEach((line) => {
      const vis = lineVisible(line);
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'line-btn' + (vis ? '' : ' dimmed') + (line.flagship ? ' flagship' : '');
      b.dataset.id = line.id;
      const stopNames = (line.stops || []).filter((k) => nodesByKey[k] && ((nodesByKey[k].phase || 1) <= activePhase || nodesByKey[k].seasonal)).map((k) => nodesByKey[k]?.label || k).join(' · ');
      b.innerHTML = `<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${line.color};margin-right:8px;box-shadow:0 0 0 2px rgba(255,255,255,0.06)"></span>${line.name}${typeBadge(line.type)}<span class="sub">${stopNames || 'Planned'}</span>`;
      b.addEventListener('click', () => selectLine(line.id));
      lineList.appendChild(b);
    });
  }
  function renderStopList() {
    const stopList = document.getElementById('stop-list');
    if (!stopList) return;
    stopList.innerHTML = '';
    stops.filter((n) => !n.exec_only).forEach((n) => {
      const vis = stopVisible(n);
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'stop-btn' + (vis ? '' : ' dimmed');
      b.dataset.key = n.key;
      const tag = n.tag ? `<span class="tag-pill">${n.tag}</span>` : '';
      const role = (n.role || '').includes('interchange') ? ' · hub' : '';
      b.innerHTML = `${n.label}${role}${tag}<span class="sub">${servesText(n)}</span>`;
      b.addEventListener('click', () => selectStop(n.key));
      stopList.appendChild(b);
    });
  }
  renderLineList();
  renderStopList();

  if (document.getElementById('map')) initMap();
  initTripFinder();

  // Form selects
  const stopSel = document.getElementById('f-stop');
  if (stopSel) {
    stopSel.innerHTML = '';
    stops.filter((n) => !n.exec_only).forEach((n) => {
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

  if (!MAP_ONLY) {
    document.querySelectorAll('#flavor-options .option').forEach((btn) => {
      btn.addEventListener('click', () => {
        flavor = btn.dataset.flavor;
        const ff = document.getElementById('f-flavor');
        if (ff) ff.value = flavor;
        document.querySelectorAll('#flavor-options .option').forEach((b) => b.classList.toggle('active', b === btn));
      });
    });
  }

  const flavors = (DATA.loi && DATA.loi.flavors) || {};
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
    const trip = lastTripSnapshot || {};
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
      // Find-my-ride context (empty if user never ran a trip)
      tripFrom: trip.tripFrom || '',
      tripFromLabel: trip.tripFromLabel || '',
      tripTo: trip.tripTo || '',
      tripToLabel: trip.tripToLabel || '',
      tripNavierMin: trip.tripNavierMin || '',
      tripDriveMin: trip.tripDriveMin || '',
      tripTransfers: trip.tripTransfers || '',
      tripSummary: trip.tripSummary || '',
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
    const tripBlock = payload.tripSummary
      ? `\nFind my ride: ${payload.tripSummary}\n`
      : '';
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
${tripBlock}
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
