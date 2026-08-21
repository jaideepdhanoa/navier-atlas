/**
 * Fleet-investors P&L model — pure functions over authored revenue_build + opex_rows.
 * Presets snap to Tasklet scenarios; custom levers stay inside authored bands.
 * Attaches to window.FI_PNL_MODEL (no bundler).
 */
(function (global) {
  const CAPEX_DEFAULT = 2500000;

  function parseMoney(str) {
    if (str == null) return null;
    if (typeof str === 'number' && Number.isFinite(str)) return str;
    const m = String(str).replace(/,/g, '').match(/-?\$?\s*([\d]+(?:\.\d+)?)/);
    return m ? Number(m[1]) : null;
  }

  function parseNetworkSharePct(share) {
    if (!share) return 0.1;
    const v = share.value != null ? String(share.value) : String(share);
    const m = v.match(/([\d.]+)\s*%/);
    return m ? Number(m[1]) / 100 : 0.1;
  }

  function isUpsideRow(row) {
    if (!row) return false;
    if (row.upside === true || row.status === 'upside') return true;
    return /upside/i.test(String(row.line || ''));
  }

  function lineKey(line) {
    return String(line || '')
      .toLowerCase()
      .replace(/\s*\(upside\)\s*/g, '')
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_|_$/g, '');
  }

  function opexTotals(opexRows) {
    const rows = opexRows || [];
    let lo = 0;
    let hi = 0;
    rows.forEach(function (r) {
      lo += Number(r.per_mo_low) || 0;
      hi += Number(r.per_mo_high) || 0;
    });
    return { lo: lo, hi: hi };
  }

  function collectLineKeys(scenarios) {
    const keys = [];
    const seen = {};
    ['conservative', 'mid', 'upside'].forEach(function (s) {
      const rows = (scenarios[s] && scenarios[s].rows) || [];
      rows.forEach(function (r) {
        if (isUpsideRow(r)) return;
        const k = lineKey(r.line);
        if (!seen[k]) {
          seen[k] = true;
          keys.push({ key: k, label: r.line });
        }
      });
    });
    return keys;
  }

  function anchorsForLine(scenarios, key) {
    const out = {};
    ['conservative', 'mid', 'upside'].forEach(function (s) {
      const rows = (scenarios[s] && scenarios[s].rows) || [];
      const row = rows.find(function (r) {
        return lineKey(r.line) === key && !isUpsideRow(r);
      });
      if (row) out[s] = row;
    });
    return out;
  }

  function upsideAnchors(scenarios) {
    const map = {};
    ['conservative', 'mid', 'upside'].forEach(function (s) {
      const rows = (scenarios[s] && scenarios[s].rows) || [];
      rows.forEach(function (r) {
        if (!isUpsideRow(r)) return;
        const k = lineKey(r.line);
        if (!map[k]) map[k] = { key: k, label: r.line.replace(/\s*\(upside\)\s*/i, '').trim(), byScenario: {} };
        map[k].byScenario[s] = r;
      });
    });
    return Object.keys(map).map(function (k) {
      return map[k];
    });
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function lerpRow(a, b, t) {
    if (!a && !b) return null;
    if (!a) return b;
    if (!b) return a;
    const subA = Number(a.subtotal_usd) || 0;
    const subB = Number(b.subtotal_usd) || 0;
    return {
      line: b.line || a.line,
      quantity: t < 0.5 ? a.quantity : b.quantity,
      price: t < 0.5 ? a.price : b.price,
      subtotal_usd: Math.round(lerp(subA, subB, t)),
      status: b.status || a.status,
      note: b.note || a.note,
      fn: b.fn || a.fn,
    };
  }

  /** t in [0,1]: 0=conservative, 0.5=mid, 1=upside */
  function rowAt(anchors, t) {
    const c = anchors.conservative;
    const m = anchors.mid;
    const u = anchors.upside;
    if (t <= 0.5) return lerpRow(c || m, m || c, t / 0.5);
    return lerpRow(m || u, u || m, (t - 0.5) / 0.5);
  }

  function buildModel(arch) {
    const pnl = (arch && arch.pnl && arch.pnl.data) || {};
    const rb = (arch && arch.revenue_build && arch.revenue_build.data && arch.revenue_build.data.scenarios) || {};
    const sharePct = parseNetworkSharePct(pnl.network_share);
    const ox = opexTotals(pnl.opex_rows);
    const assetCapex =
      (arch.asset && arch.asset.data && arch.asset.data.capex_usd) ||
      (pnl.vessel_capex_usd) ||
      CAPEX_DEFAULT;
    const lineMetas = collectLineKeys(rb);
    const lines = {};
    lineMetas.forEach(function (lm) {
      lines[lm.key] = anchorsForLine(rb, lm.key);
    });
    const upside = upsideAnchors(rb);
    const scenarioTable = (pnl.scenarios && pnl.scenarios.table) || [];

    return {
      sharePct: sharePct,
      opexLo: ox.lo,
      opexHi: ox.hi,
      capex: assetCapex,
      lineMetas: lineMetas,
      lines: lines,
      upside: upside,
      opexRows: pnl.opex_rows || [],
      networkShare: pnl.network_share || null,
      scenarioTable: scenarioTable,
      revenueRowsMeta: pnl.revenue_rows || [],
      upsideRowsMeta: pnl.upside_rows || [],
      paybackAuthored: (pnl.payback && pnl.payback.per_scenario) || {},
      grossAuthored: (pnl.gross && pnl.gross.per_scenario) || {},
      netAuthored: (pnl.net && pnl.net.per_scenario) || {},
      hasRevenueBuild: Object.keys(rb).length > 0,
    };
  }

  function defaultState(model) {
    const lineT = {};
    (model.lineMetas || []).forEach(function (lm) {
      lineT[lm.key] = 0.5; // mid
    });
    const upsideOn = {};
    (model.upside || []).forEach(function (u) {
      upsideOn[u.key] = false;
    });
    return {
      preset: 'mid',
      lineT: lineT,
      upsideOn: upsideOn,
      opexT: 0.5,
    };
  }

  function applyPreset(model, preset) {
    const t = preset === 'conservative' ? 0 : preset === 'upside' ? 1 : 0.5;
    const state = defaultState(model);
    state.preset = preset;
    Object.keys(state.lineT).forEach(function (k) {
      state.lineT[k] = t;
    });
    Object.keys(state.upsideOn).forEach(function (k) {
      state.upsideOn[k] = preset === 'upside';
    });
    state.opexT = t;
    return state;
  }

  function evaluate(model, state) {
    const revenueLines = [];
    let grossBase = 0;
    (model.lineMetas || []).forEach(function (lm) {
      const row = rowAt(model.lines[lm.key] || {}, state.lineT[lm.key] != null ? state.lineT[lm.key] : 0.5);
      if (!row) return;
      revenueLines.push(row);
      grossBase += Number(row.subtotal_usd) || 0;
    });

    const upsideLines = [];
    let grossUpside = 0;
    (model.upside || []).forEach(function (u) {
      const on = !!(state.upsideOn && state.upsideOn[u.key]);
      const row = rowAt(u.byScenario || {}, 1); // use upside anchor amounts when on
      if (!row) return;
      const entry = Object.assign({}, row, { line: u.label, upside: true, enabled: on });
      upsideLines.push(entry);
      if (on) grossUpside += Number(row.subtotal_usd) || 0;
    });

    let gross = grossBase + grossUpside;
    let opex = lerp(model.opexLo, model.opexHi, state.opexT != null ? state.opexT : 0.5);
    let net = gross * (1 - model.sharePct) - opex;
    let payback = null;
    let paybackLabel = '—';

    // For exact presets, prefer authored scenario table / payback strings
    if (state.preset && state.preset !== 'custom' && model.hasRevenueBuild) {
      const authoredGross = model.grossAuthored[state.preset];
      const authoredNet = model.netAuthored[state.preset];
      const authoredPb = model.paybackAuthored[state.preset];
      const scenRows = null;
      if (authoredGross != null) gross = authoredGross;
      if (authoredNet != null) net = authoredNet;
      // Back out opex for display consistency when using authored net
      if (authoredGross != null && authoredNet != null) {
        opex = authoredGross * (1 - model.sharePct) - authoredNet;
      }
      if (authoredPb != null) paybackLabel = String(authoredPb);
      else if (net > 0) {
        payback = model.capex / (net * 12);
        paybackLabel = '~' + payback.toFixed(1) + ' yr';
      }
    } else if (net > 0) {
      payback = model.capex / (net * 12);
      paybackLabel = '~' + payback.toFixed(1) + ' yr';
    }

    const opexLines = (model.opexRows || []).map(function (r) {
      const lo = Number(r.per_mo_low) || 0;
      const hi = Number(r.per_mo_high) || 0;
      return {
        line: r.line,
        amount: Math.round(lerp(lo, hi, state.opexT != null ? state.opexT : 0.5)),
        per_mo_low: lo,
        per_mo_high: hi,
        note: r.note,
        status: r.status,
        fn: r.fn,
      };
    });

    return {
      revenueLines: revenueLines,
      upsideLines: upsideLines,
      opexLines: opexLines,
      gross: Math.round(gross),
      opex: Math.round(opex),
      networkShareAmt: Math.round(gross * model.sharePct),
      sharePct: model.sharePct,
      net: Math.round(net),
      payback: payback,
      paybackLabel: paybackLabel,
      capex: model.capex,
      networkShare: model.networkShare,
    };
  }

  function markCustom(state) {
    return Object.assign({}, state, { preset: 'custom' });
  }

  /** Labels for lever chrome: live qty/price/$ and authored endcaps */
  function leverDisplay(model, state, lineKeyName) {
    const anchors = model.lines[lineKeyName] || {};
    const t = state.lineT[lineKeyName] != null ? state.lineT[lineKeyName] : 0.5;
    const cur = rowAt(anchors, t) || {};
    const lo = anchors.conservative || anchors.mid || {};
    const hi = anchors.upside || anchors.mid || {};
    return {
      live:
        [cur.quantity, cur.price, cur.subtotal_usd != null ? '$' + Math.round(cur.subtotal_usd).toLocaleString('en-US') : null]
          .filter(Boolean)
          .join(' · '),
      endLo: [lo.quantity, lo.price].filter(Boolean).join(' · ') || 'Low',
      endHi: [hi.quantity, hi.price].filter(Boolean).join(' · ') || 'High',
      quantity: cur.quantity || '',
      price: cur.price || '',
      subtotal: cur.subtotal_usd,
    };
  }

  function opexDisplay(model, state) {
    const t = state.opexT != null ? state.opexT : 0.5;
    const amt = Math.round(lerp(model.opexLo, model.opexHi, t));
    return {
      live: '$' + amt.toLocaleString('en-US') + '/mo',
      endLo: '$' + Math.round(model.opexLo).toLocaleString('en-US'),
      endHi: '$' + Math.round(model.opexHi).toLocaleString('en-US'),
    };
  }

  global.FI_PNL_MODEL = {
    CAPEX_DEFAULT: CAPEX_DEFAULT,
    buildModel: buildModel,
    defaultState: defaultState,
    applyPreset: applyPreset,
    evaluate: evaluate,
    markCustom: markCustom,
    leverDisplay: leverDisplay,
    opexDisplay: opexDisplay,
    parseMoney: parseMoney,
    lineKey: lineKey,
  };
})(typeof window !== 'undefined' ? window : globalThis);
