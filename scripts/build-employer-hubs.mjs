/**
 * Build public employer-hub microsites from employer-hub/registry.json.
 *
 * Emits:
 *   _dist/employers/<id>/   (canonical)
 *   _dist/<alias>/          (e.g. bay-employers, ny-employers) — full copies for cleanUrls
 *
 * Each output: index.html, hub.css, hub.js, hub-data.js, assets/hero.jpg, BP-RESOLUTION-RECEIPT.json
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, '_dist');
const HUB_ROOT = path.join(ROOT, 'employer-hub');

/** Fail the build when hub.json corridor_table drifts from archetype page figures. */
function validateHubPageConsistency(hubId) {
  const hubDir = path.join(HUB_ROOT, 'hubs', hubId);
  const hubPath = path.join(hubDir, 'hub.json');
  if (!fs.existsSync(hubPath)) return;
  const hub = readJson(hubPath);
  if (!hub.corridor_table || !hub.corridor_table.corridors) return;
  const script = path.join(ROOT, 'scripts', 'validate_hub_page_consistency.py');
  if (!fs.existsSync(script)) {
    throw new Error(`corridor_table present on ${hubId} but ${script} missing`);
  }
  const r = spawnSync('python3', [script, hubDir], { encoding: 'utf8' });
  if (r.status !== 0) {
    throw new Error(
      `corridor drift gate FAILED for ${hubId}:\n${(r.stdout || '') + (r.stderr || '')}`
    );
  }
  console.log(`corridor drift gate → ${hubId} PASS`);
}

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

/** Inject CARTO basemap key at build/deploy time only — never commit the secret. */
function cartoKeyBootstrapScript() {
  const key = process.env.CARTO_BASEMAP_KEY || '';
  if (!key) return '';
  const safe = String(key).replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"');
  return `<script>window.CARTO_BASEMAP_KEY="${safe}";</script>\n`;
}

function injectCartoKey(html) {
  const boot = cartoKeyBootstrapScript();
  if (!boot) return html;
  if (/<\/head>/i.test(html)) return html.replace(/<\/head>/i, `${boot}</head>`);
  return boot + html;
}

/**
 * Attach Phase 4/5 gateway lines + terminal stops from corridor_table +
 * employer-hub/hubs/<id>/gateway-geometries.json (ROUTES proxies / hand paths).
 */
function attachGatewayOverlays(hub) {
  const hubId = hub.id;
  const geoPath = path.join(HUB_ROOT, 'hubs', hubId, 'gateway-geometries.json');
  if (!fs.existsSync(geoPath)) return hub;
  const table = hub.corridor_table && hub.corridor_table.corridors;
  if (!Array.isArray(table) || !table.length) return hub;

  const geoFile = readJson(geoPath);
  const geoms = geoFile.geometries || {};
  const out = structuredClone(hub);
  out.stops = Array.isArray(out.stops) ? out.stops.slice() : [];
  out.lines = Array.isArray(out.lines) ? out.lines.slice() : [];

  const stopKeys = new Set(out.stops.map((s) => s.key));
  function ensureStop(key, label, lng, lat, phase, tag) {
    if (stopKeys.has(key)) return;
    out.stops.push({
      key,
      label,
      resolved_bp_id: null,
      lng,
      lat,
      role: 'station',
      phase,
      serves: [],
      tag: tag || null,
      seasonal: false,
      hub_rank: 4,
    });
    stopKeys.add(key);
  }

  const gtwSegs = [];
  const gtwOrder = ['GTW-1a', 'GTW-1b', 'GTW-1c'];
  // Chain UAE Gateway toward RAK: AD→Dubai, Dubai←Sharjah (reverse), Sharjah→Marjan
  const gtwMeta = {
    'GTW-1a': { from: 'abu-dhabi-gateway', to: 'dubai-gateway', reverse: false },
    'GTW-1b': { from: 'dubai-gateway', to: 'sharjah-gateway', reverse: false },
    'GTW-1c': { from: 'sharjah-gateway', to: 'al-marjan', reverse: false },
  };
  const gtwLabels = {
    'abu-dhabi-gateway': 'Yas Marina — Abu Dhabi',
    'dubai-gateway': 'Dubai Harbour',
    'sharjah-gateway': 'Sharjah — Al Khan Lagoon',
  };

  for (const cid of gtwOrder) {
    const row = table.find((r) => r.id === cid);
    const g = geoms[cid];
    if (!row || !row.render_on_map || !g || !g.coordinates || g.coordinates.length < 2) continue;
    let coords = g.coordinates.map((c) => [c[0], c[1]]);
    const meta = gtwMeta[cid];
    if (meta.reverse) coords = coords.slice().reverse();
    const a = coords[0];
    const b = coords[coords.length - 1];
    if (meta.from !== 'al-marjan') {
      ensureStop(meta.from, gtwLabels[meta.from] || meta.from, a[0], a[1], 4, 'Phase 4 gateway terminal');
    }
    if (meta.to !== 'al-marjan') {
      ensureStop(meta.to, gtwLabels[meta.to] || meta.to, b[0], b[1], 4, 'Phase 4 gateway terminal');
    }
    gtwSegs.push({
      from: meta.from,
      to: meta.to,
      distance_nm: row.path_nm,
      water_min: row.min_day_30kn,
      water_path: coords,
      phase: 4,
      speed_constrained: false,
    });
  }
  if (gtwSegs.length) {
    out.lines = out.lines.filter((l) => l.id !== 'GTW-1');
    out.lines.push({
      id: 'GTW-1',
      name: 'UAE Gateway Line',
      color: '#7fd8b8',
      type: 'trunk',
      phase: 4,
      flagship: false,
      stops: ['abu-dhabi-gateway', 'dubai-gateway', 'sharjah-gateway', 'al-marjan'],
      segments: gtwSegs,
    });
  }

  const gulfDefs = [
    {
      id: 'GLF-2',
      lineId: 'GLF-doha',
      name: 'Gulf Gateway — Doha',
      from: 'al-marjan',
      to: 'doha-gateway',
      toLabel: 'Doha',
    },
    {
      id: 'GLF-3',
      lineId: 'GLF-manama',
      name: 'Gulf Gateway — Manama',
      from: 'al-marjan',
      to: 'manama-gateway',
      toLabel: 'Manama',
    },
    {
      id: 'GLF-1',
      lineId: 'GLF-khasab',
      name: 'Gulf Gateway — Khasab',
      from: 'al-marjan',
      to: 'khasab-gateway',
      toLabel: 'Khasab Port & Old Harbour',
    },
    {
      id: 'GLF-4',
      lineId: 'GLF-dammam',
      name: 'Gulf Gateway — Dammam',
      from: 'al-marjan',
      to: 'dammam-gateway',
      toLabel: 'Dammam (KSA Eastern Province)',
    },
    {
      id: 'GLF-5',
      lineId: 'GLF-muscat',
      name: 'Gulf Gateway — Muscat',
      from: 'al-marjan',
      to: 'muscat-gateway',
      toLabel: 'Muscat — Muttrah Corniche',
    },
  ];
  for (const def of gulfDefs) {
    const row = table.find((r) => r.id === def.id);
    const g = geoms[def.id];
    if (!row || !row.render_on_map || !g || !g.coordinates || g.coordinates.length < 2) continue;
    let coords = g.coordinates.map((c) => [c[0], c[1]]);
    // Orient toward foreign terminal: if path starts near RAK, keep; else reverse
    const rakLng = 55.85;
    const d0 = Math.abs(coords[0][0] - rakLng);
    const d1 = Math.abs(coords[coords.length - 1][0] - rakLng);
    if (d1 < d0) coords = coords.slice().reverse();
    const end = coords[coords.length - 1];
    ensureStop(def.to, def.toLabel, end[0], end[1], 5, 'Phase 5 roadmap terminal');
    out.lines = out.lines.filter((l) => l.id !== def.lineId);
    out.lines.push({
      id: def.lineId,
      name: def.name,
      color: '#9bb7ff',
      type: 'roadmap',
      phase: 5,
      dashed: true,
      stops: [def.from, def.to],
      segments: [
        {
          from: def.from,
          to: def.to,
          distance_nm: row.path_nm,
          water_min: row.min_day_30kn,
          water_path: coords,
          phase: 5,
          speed_constrained: false,
        },
      ],
    });
  }

  return out;
}

function copyFile(src, dst) {
  ensureDir(path.dirname(dst));
  fs.copyFileSync(src, dst);
}

function computeBayNet(inputs) {
  const S = inputs.seats?.default ?? 60;
  const P = inputs.price_seat_month?.default ?? 1000;
  const sigma = inputs.subsidy_share?.default ?? 0.8;
  const X = inputs.pretax_benefit?.default ?? 325;
  const V = inputs.shuttle_cost?.default ?? 550;
  const K = inputs.parking_cost?.default ?? 350;
  const rho = inputs.parking_share?.default ?? 0.5;
  const gross = S * P;
  const emp = S * Math.min(X, (1 - sigma) * P);
  const netInc = gross - emp - S * V - S * rho * K;
  return { netInc, perRider: S ? netInc / S : 0, S };
}

function computeNycNet(inputs) {
  const S = inputs.S_committed_seats?.default ?? inputs.seats?.default ?? 60;
  const P = inputs.P_price_per_seat_month?.default ?? inputs.price_seat_month?.default ?? 750;
  const sigma = inputs.sigma_employer_subsidy_share?.default ?? inputs.subsidy_share?.default ?? 0.8;
  const X = inputs.X_pretax_benefit_cap_month?.default ?? inputs.pretax_benefit?.default ?? 340;
  const V = inputs.V_current_shuttle_cost_seat_month?.default ?? inputs.shuttle_cost?.default ?? 0;
  const K = inputs.K_parking_cost_stall_month?.default ?? inputs.parking_cost?.default ?? 570;
  const rho = inputs.rho_share_displacing_stall?.default ?? inputs.parking_share?.default ?? 0.5;
  const G = inputs.G_congestion_toll_weekday?.default ?? 9;
  const W = inputs.W_weekdays_per_month?.default ?? 21;
  const gross = S * P;
  const emp = S * Math.min(X, (1 - sigma) * P);
  const netEmployer = gross - emp;
  const netPerRider = S ? netEmployer / S : 0;
  const benchmark = K + G * W;
  const netInc = netEmployer - S * rho * K - S * V;
  return {
    netInc,
    perRider: S ? netInc / S : 0,
    netEmployerPerRider: netPerRider,
    benchmark,
    S,
  };
}

function bannedDockScan(blob) {
  return /\b(unlock(?:s|ing)?\s+(?:the\s+)?(?:berths?|docks?)|docks?\s+ahead\s+of\s+demand|demand\s+ahead\s+of\s+docks?|terminal access)\b/i.test(
    blob
  );
}


function sanitizeClientHub(hub) {
  // Strip internal fields that must never reach the browser
  const stripKeys = new Set([
    'dock_track',
    'note_internal',
    'note',
    'landing',
    'geometry_receipt',
    'stop_migrations',
    'decision_ledger',
    'watchlist',
    'no_landing',
    'no_intercity_link',
    'source_inventory',
    'authored_by',
    'status',
  ]);
  const clean = JSON.parse(JSON.stringify(hub));
  for (const s of clean.stops || []) {
    for (const k of [...Object.keys(s)]) {
      if (stripKeys.has(k) || k.endsWith('_internal')) delete s[k];
    }
  }
  for (const l of clean.lines || []) {
    delete l.phase_notes;
    delete l.geometry_receipt;
    for (const seg of l.segments || []) {
      // routing directives are build-time only; can contain internal refs
      delete seg.routing;
      delete seg.constraint;
      delete seg.note_internal;
    }
  }
  delete clean.geometry_receipt;
  delete clean.stop_migrations;
  // Internal QA ledgers stay on disk only — not in the browser bundle
  delete clean.bp_gap;
  delete clean.decision_ledger;
  delete clean.watchlist;
  delete clean.no_landing;
  delete clean.no_intercity_link;
  if (clean.gates) {
    delete clean.gates.banned_terms; // avoid shipping held place-names into client JS
    // Keep speed_constrained_label for client UI; drop long internal rule blobs
    for (const k of Object.keys(clean.gates)) {
      if (k === 'speed_constrained_label' || k === 'two_cluster_render' || k === 'no_intercity_link') continue;
      if (typeof clean.gates[k] === 'object') delete clean.gates[k];
    }
  }
  // External-copy kill terms: rename/drop `catchment` keys and scrub the word from strings
  const scrub = (v) => {
    if (typeof v === 'string') return v.replace(/catchment/gi, 'area');
    if (Array.isArray(v)) return v.map(scrub);
    if (v && typeof v === 'object') {
      for (const k of Object.keys(v)) {
        const nk = k === 'catchment' ? 'service_area' : k;
        const val = scrub(v[k]);
        if (nk !== k) delete v[k];
        v[nk] = val;
      }
    }
    return v;
  };
  return scrub(clean);
}

function emitHub(hub, registryEntry) {
  const id = hub.id;
  const calc = hub.calculator || {};
  const profile = calc.profile || 'bay_productivity';
  const inputs = calc.inputs || {};

  // Math gate
  if (profile === 'bay_productivity') {
    const { netInc, perRider } = computeBayNet(inputs);
    const want = calc.worked_assert || { net_incremental: 4500, per_rider: 75 };
    if (Math.round(netInc) !== want.net_incremental) {
      throw new Error(`${id}: net_incremental=${netInc}, expected ${want.net_incremental}`);
    }
    if (want.per_rider != null && Math.round(perRider) !== want.per_rider) {
      throw new Error(`${id}: per_rider=${perRider}, expected ${want.per_rider}`);
    }
  } else if (profile === 'nyc_parking_toll') {
    const r = computeNycNet(inputs);
    const want = calc.worked_assert || {};
    if (want.net_incremental != null && Math.round(r.netInc) !== want.net_incremental) {
      throw new Error(`${id}: net_incremental=${r.netInc}, expected ${want.net_incremental}`);
    }
    if (
      want.net_employer_cost_per_rider != null &&
      Math.round(r.netEmployerPerRider) !== want.net_employer_cost_per_rider
    ) {
      throw new Error(
        `${id}: net_employer_cost_per_rider=${r.netEmployerPerRider}, expected ${want.net_employer_cost_per_rider}`
      );
    }
    if (want.benchmark != null && Math.round(r.benchmark) !== want.benchmark) {
      throw new Error(`${id}: benchmark=${r.benchmark}, expected ${want.benchmark}`);
    }
  }

  // Scan customer-facing copy only (not gates.banned_terms list itself)
  const copyBlob = JSON.stringify({
    copy: hub.copy,
    products: hub.products,
    loi: hub.loi,
    stops: (hub.stops || []).map((s) => ({ label: s.label, serves: s.serves })),
    lines: (hub.lines || []).map((l) => ({ name: l.name })),
  });
  if (hub.gates?.forbid_dock_unlock !== false && bannedDockScan(copyBlob)) {
    throw new Error(`${id}: dock/berth dependency language in hub copy`);
  }
  for (const term of hub.gates?.banned_terms || []) {
    if (new RegExp(term, 'i').test(copyBlob)) {
      throw new Error(`${id}: banned term in hub copy: ${term}`);
    }
  }

  // Stops must have coordinates
  for (const s of hub.stops || []) {
    if (s.lng == null || s.lat == null) {
      throw new Error(`${id}: stop ${s.key} missing coordinates`);
    }
  }

  const basePaths = [];
  const canonical = registryEntry.canonical_path || `/employers/${id}`;
  basePaths.push(canonical.replace(/^\//, ''));
  for (const a of registryEntry.aliases || hub.aliases || []) {
    basePaths.push(String(a).replace(/^\//, ''));
  }

  const tplHtml = fs.readFileSync(path.join(HUB_ROOT, 'template/index.html'), 'utf8');
  const tplCss = fs.readFileSync(path.join(HUB_ROOT, 'template/hub.css'), 'utf8');
  const tplJs = fs.readFileSync(path.join(HUB_ROOT, 'template/hub.js'), 'utf8');

  const brand = hub.brand || {};
  const heroSrc = brand.hero_asset
    ? path.join(ROOT, brand.hero_asset)
    : path.join(ROOT, 'deck-studio/assets/weta/passengers-stern-bright.png');

  for (const rel of basePaths) {
    const outDir = path.join(DIST, rel);
    ensureDir(outDir);
    ensureDir(path.join(outDir, 'assets'));
    const hubBase = '/' + rel.replace(/\/$/, '');

    let html = tplHtml
      .replaceAll('__HUB_BASE__', hubBase)
      .replaceAll('__HUB_TITLE__', brand.title || `Navier · ${hub.market?.label || id}`)
      .replaceAll('__HUB_DESCRIPTION__', brand.description || '')
      .replaceAll('__HUB_OG_DESCRIPTION__', brand.og_description || brand.description || '');

    // map aria
    if (hub.market?.map?.aria_label) {
      html = html.replace(
        'aria-label="Employer water network map"',
        `aria-label="${hub.market.map.aria_label}"`
      );
    }

    fs.writeFileSync(path.join(outDir, 'index.html'), injectCartoKey(html));
    fs.writeFileSync(path.join(outDir, 'hub.css'), tplCss);
    fs.writeFileSync(path.join(outDir, 'hub.js'), tplJs);
    // Shared About + Vessels styles/media used by employer brochure sections
    const archCss = fs.readFileSync(path.join(HUB_ROOT, 'template/archetype.css'), 'utf8');
    fs.writeFileSync(path.join(outDir, 'archetype.css'), archCss);
    const clientHub = sanitizeClientHub(attachGatewayOverlays(hub));
    const sharedAbout = path.join(HUB_ROOT, 'shared/about-navier.json');
    const sharedVessels = path.join(HUB_ROOT, 'shared/vessels.json');
    if (fs.existsSync(sharedAbout)) {
      clientHub.about_navier = stripUnderscoreKeys(readJson(sharedAbout));
    }
    if (fs.existsSync(sharedVessels)) {
      clientHub.vessels = resolveVesselsForAudience(readJson(sharedVessels), 'employers');
    }
    fs.writeFileSync(
      path.join(outDir, 'hub-data.js'),
      `/* GENERATED from employer-hub/hubs/${id}/hub.json */\nwindow.EMPLOYER_HUB_DATA = ${JSON.stringify(clientHub)};\n`
    );

    // Legacy Bay data global for any residual consumers
    if (id === 'bay-area') {
      const legacy = {
        version: hub.version,
        locked_numbers: hub.locked_numbers,
        nodes: hub.stops,
        lines: hub.lines,
        schedules: null,
        schedules_note: hub.schedules_note,
        roi_calculator: {
          inputs: calc.inputs,
          formulas: calc.formulas,
          worked_example_at_defaults: calc.worked_example_at_defaults,
          caveat: calc.caveat,
        },
        copy: hub.copy,
        references: hub.references,
      };
      fs.writeFileSync(
        path.join(outDir, 'bay-employers-data.js'),
        `/* GENERATED compatibility shim */\nwindow.BAY_EMPLOYERS_DATA = ${JSON.stringify(legacy)};\nwindow.EMPLOYER_HUB_DATA = window.EMPLOYER_HUB_DATA || ${JSON.stringify(clientHub)};\n`
      );
    }

    if (fs.existsSync(heroSrc)) {
      // keep .jpg extension for CSS url even if source is png
      const dest = path.join(outDir, 'assets', 'hero.jpg');
      fs.copyFileSync(heroSrc, dest);
    }

    const receipt = {
      generated: new Date().toISOString(),
      hub_id: id,
      canonical_path: canonical,
      emit_path: hubBase,
      stops: (hub.stops || []).map((n) => ({
        key: n.key,
        label: n.label,
        resolved_bp_id: n.resolved_bp_id,
        lng: n.lng,
        lat: n.lat,
      })),
      calculator_profile: profile,
      worked_assert: calc.worked_assert || null,
    };
    fs.writeFileSync(path.join(outDir, 'BP-RESOLUTION-RECEIPT.json'), JSON.stringify(receipt, null, 2) + '\n');
    console.log(`employer-hub → ${hubBase}/  (${receipt.stops.length} stops · ${profile})`);
  }
}

function stripUnderscoreKeys(obj) {
  if (obj == null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(stripUnderscoreKeys);
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    if (k.startsWith('_')) continue;
    out[k] = stripUnderscoreKeys(v);
  }
  return out;
}

/** Soft-split vessel card copy by audience; shared media stays identical.
 *  ADDENDUM v4: interiors sell productivity (employers) / pricing power (FI).
 *  Public Partner pages get ZERO interior/executive-comfort content (G11).
 */
function resolveVesselsForAudience(raw, audience) {
  const vessels = stripUnderscoreKeys(raw);
  if (!vessels || !Array.isArray(vessels.cards)) return vessels;
  const isFi = audience === 'fleet-investors';
  const isPp = audience === 'public-partners';
  if (isPp) {
    delete vessels.interior_footnote;
    if (vessels.copy && vessels.copy.body_public_partners) {
      vessels.copy.body = vessels.copy.body_public_partners;
    } else if (vessels.copy && vessels.copy.body) {
      // Fail closed: strip cabin/productivity pitch on PP
      vessels.copy.body = String(vessels.copy.body)
        .replace(/\s*Cabins are built for the working crossing[^.]*\./gi, '')
        .replace(/\s*— quiet enough to take a call/gi, '')
        .trim();
    }
  }
  if (vessels.copy) delete vessels.copy.body_public_partners;
  vessels.cards = vessels.cards.map((card) => {
    const out = { ...card };
    if (isFi && out.blurb_fleet_investors) {
      out.blurb = out.blurb_fleet_investors;
    }
    if (isFi && out.interior_caption_fleet_investors) {
      out.interior_caption = out.interior_caption_fleet_investors;
    }
    if (isPp) {
      delete out.interior_image;
      delete out.interior_caption;
      delete out.interior_caption_fleet_investors;
    }
    delete out.blurb_fleet_investors;
    delete out.blurb_public_partners;
    delete out.blurb_employers;
    delete out.interior_caption_fleet_investors;
    return out;
  });
  return vessels;
}

/**
 * Emit public-partners and fleet-investors pages when data files exist.
 * Routes: /public-partners/{city}, /fleet-investors/{city}
 * Both public (indexable). No cross-links between archetype pages.
 * Shared map + trip planner via hub.js MAP_ONLY + hub.json.
 */
function emitArchetypePage(hubId, hub, archetypeId, dataFileName, routePrefix) {
  const dataPath = path.join(HUB_ROOT, 'hubs', hubId, dataFileName);
  if (!fs.existsSync(dataPath)) return null;

  const archData = readJson(dataPath);
  const rel = `${routePrefix}/${hubId}`.replace(/\/+/g, '/');
  const outDir = path.join(DIST, rel);
  ensureDir(outDir);
  ensureDir(path.join(outDir, 'assets'));
  const pageBase = '/' + rel.replace(/\/$/, '');

  const tplHtml = fs.readFileSync(path.join(HUB_ROOT, 'template/archetype.html'), 'utf8');
  const tplCss = fs.readFileSync(path.join(HUB_ROOT, 'template/hub.css'), 'utf8');
  const archCss = fs.readFileSync(path.join(HUB_ROOT, 'template/archetype.css'), 'utf8');
  const tplJs = fs.readFileSync(path.join(HUB_ROOT, 'template/hub.js'), 'utf8');
  const archJs = fs.readFileSync(path.join(HUB_ROOT, 'template/archetype.js'), 'utf8');
  const pnlModelJs = fs.readFileSync(path.join(HUB_ROOT, 'template/pnl-model.js'), 'utf8');

  const label =
    archetypeId === 'fleet-investors'
      ? 'Fleet Investors'
      : archetypeId === 'public-partners'
        ? 'Public Partners'
        : archetypeId;
  const headline = archData.hero?.copy?.headline || `${hub.market?.label || hubId} · ${label}`;
  const subline = archData.hero?.copy?.subline || hub.brand?.description || '';

  let html = tplHtml
    .replaceAll('__PAGE_BASE__', pageBase)
    .replaceAll('__PAGE_TITLE__', `Navier · ${headline}`.slice(0, 120))
    .replaceAll('__PAGE_DESCRIPTION__', subline.slice(0, 300))
    .replaceAll('__ARCHETYPE_ID__', archetypeId)
    .replaceAll('__ARCHETYPE_LABEL__', label);

  if (archetypeId === 'fleet-investors' && !/name="robots"/i.test(html)) {
    html = html.replace(
      '</head>',
      '<meta name="robots" content="noindex, nofollow" />\n</head>'
    );
  }

  if (hub.market?.map?.aria_label) {
    html = html.replace(
      'aria-label="Water network map"',
      `aria-label="${hub.market.map.aria_label}"`
    );
  }

  fs.writeFileSync(path.join(outDir, 'index.html'), injectCartoKey(html));
  fs.writeFileSync(path.join(outDir, 'hub.css'), tplCss);
  fs.writeFileSync(path.join(outDir, 'archetype.css'), archCss);
  fs.writeFileSync(path.join(outDir, 'hub.js'), tplJs);
  fs.writeFileSync(path.join(outDir, 'archetype.js'), archJs);
  fs.writeFileSync(path.join(outDir, 'pnl-model.js'), pnlModelJs);

  const clientHub = sanitizeClientHub(attachGatewayOverlays(hub));
  fs.writeFileSync(
    path.join(outDir, 'hub-data.js'),
    `/* GENERATED hub geometry for archetype */\nwindow.EMPLOYER_HUB_DATA = ${JSON.stringify(clientHub)};\n`
  );

  const clientArch = stripUnderscoreKeys(archData);
  // Shared city-agnostic About + Vessels media for FI and PP (copy soft-split by audience)
  const sharedAbout = path.join(HUB_ROOT, 'shared/about-navier.json');
  const sharedVessels = path.join(HUB_ROOT, 'shared/vessels.json');
  if (fs.existsSync(sharedAbout)) {
    clientArch.about_navier = stripUnderscoreKeys(readJson(sharedAbout));
  }
  if (fs.existsSync(sharedVessels)) {
    clientArch.vessels = resolveVesselsForAudience(readJson(sharedVessels), archetypeId);
  }
  // FI-only shared economics defaults; city JSON may override
  if (archetypeId === 'fleet-investors') {
    const sharedBm = path.join(HUB_ROOT, 'shared/business-model.json');
    const sharedFee = path.join(HUB_ROOT, 'shared/network-fee.json');
    if (!clientArch.business_model && fs.existsSync(sharedBm)) {
      clientArch.business_model = stripUnderscoreKeys(readJson(sharedBm));
    }
    if (!clientArch.network_fee && fs.existsSync(sharedFee)) {
      clientArch.network_fee = stripUnderscoreKeys(readJson(sharedFee));
    }
  }
  // FI pages stay unlisted; PP pages are public/indexable
  const isFi = archetypeId === 'fleet-investors';
  if (clientArch.access && typeof clientArch.access === 'object') {
    clientArch.access = {
      mode: 'public',
      noindex: isFi,
      in_sitemap: !isFi,
      in_nav: false,
      inbound_links_allowed: false,
    };
  } else if (isFi) {
    clientArch.access = { mode: 'public', noindex: true, in_sitemap: false, in_nav: false, inbound_links_allowed: false };
  }
  clientArch.route = `/${routePrefix}/${hubId}`;
  fs.writeFileSync(
    path.join(outDir, 'archetype-data.js'),
    `/* GENERATED from hubs/${hubId}/${dataFileName} */\nwindow.ARCHETYPE_DATA = ${JSON.stringify(clientArch)};\n`
  );

  // Prefer archetype-authored hero (e.g. hubs/<id>/assets/hero-public-*.jpg), then hub brand, then fallback
  const archHeroRel = (archData.hero && archData.hero.data && archData.hero.data.image) || '';
  const archHeroPath = archHeroRel
    ? path.join(ROOT, String(archHeroRel).replace(/^\//, ''))
    : '';
  const heroCandidates = [
    archHeroPath,
    hub.brand?.hero_asset ? path.join(ROOT, hub.brand.hero_asset) : '',
    path.join(ROOT, 'deck-studio/assets/weta/passengers-stern-bright.png'),
  ].filter(Boolean);
  const heroSrc = heroCandidates.find((p) => fs.existsSync(p));
  if (heroSrc) {
    fs.copyFileSync(heroSrc, path.join(outDir, 'assets', 'hero.jpg'));
  }

  console.log(`archetype → ${pageBase}/  (${archetypeId} · ${hubId})`);
  return pageBase;
}

function copySharedDir(rel) {
  const srcDir = path.join(HUB_ROOT, rel);
  const dstDir = path.join(DIST, 'employer-hub', rel);
  if (!fs.existsSync(srcDir)) return;
  ensureDir(dstDir);
  for (const name of fs.readdirSync(srcDir)) {
    const src = path.join(srcDir, name);
    if (!fs.statSync(src).isFile()) continue;
    fs.copyFileSync(src, path.join(dstDir, name));
  }
}

function copySharedVesselAssets() {
  copySharedDir('assets/vessels');
  copySharedDir('assets/demos');
  copySharedDir('assets/posters');
}

function emitArchetypesForHubId(hubId, hub, archetypes) {
  const pp = emitArchetypePage(hubId, hub, 'public-partners', 'public-partners.json', 'public-partners');
  const fi = emitArchetypePage(hubId, hub, 'fleet-investors', 'fleet-investors.json', 'fleet-investors');
  if (pp) archetypes.push(pp);
  if (fi) archetypes.push(fi);
}

export function buildEmployerHubs() {
  const registryPath = path.join(HUB_ROOT, 'registry.json');
  if (!fs.existsSync(registryPath)) {
    console.warn('⚠ employer-hub/registry.json missing — skipping employer hubs');
    return [];
  }
  const registry = readJson(registryPath);
  const built = [];
  const archetypes = [];
  const registryIds = new Set();

  copySharedVesselAssets();

  for (const entry of registry.hubs || []) {
    if (entry.enabled === false) continue;
    const hubPath = path.join(HUB_ROOT, entry.path || `hubs/${entry.id}/hub.json`);
    if (!fs.existsSync(hubPath)) {
      console.warn(`⚠ hub data missing: ${hubPath}`);
      continue;
    }
    const hub = readJson(hubPath);
    if (hub.id !== entry.id) {
      console.warn(`⚠ hub id mismatch file=${hub.id} registry=${entry.id} — using file id`);
    }
    validateHubPageConsistency(hub.id);
    emitHub(hub, entry);
    built.push(hub.id);
    registryIds.add(hub.id);
    emitArchetypesForHubId(hub.id, hub, archetypes);
  }

  // Archetype-only cities: have hub.json + PP/FI but are not employer microsites
  const hubsDir = path.join(HUB_ROOT, 'hubs');
  if (fs.existsSync(hubsDir)) {
    for (const hubId of fs.readdirSync(hubsDir)) {
      if (registryIds.has(hubId)) continue;
      const hubPath = path.join(hubsDir, hubId, 'hub.json');
      const hasPp = fs.existsSync(path.join(hubsDir, hubId, 'public-partners.json'));
      const hasFi = fs.existsSync(path.join(hubsDir, hubId, 'fleet-investors.json'));
      if (!fs.existsSync(hubPath) || (!hasPp && !hasFi)) continue;
      const hub = readJson(hubPath);
      console.log(`archetype-only city → ${hubId} (no employer microsite)`);
      validateHubPageConsistency(hubId);
      emitArchetypesForHubId(hubId, hub, archetypes);
    }
  }

  if (archetypes.length) {
    console.log(`archetypes built: ${archetypes.join(', ')}`);
  }
  return built;
}

// CLI
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const built = buildEmployerHubs();
    console.log(`employer-hubs built: ${built.join(', ') || '(none)'}`);
  } catch (e) {
    console.error('build-employer-hubs FAILED:', e.message || e);
    process.exit(1);
  }
}

