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

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, '_dist');
const HUB_ROOT = path.join(ROOT, 'employer-hub');

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
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
  return clean;
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

    fs.writeFileSync(path.join(outDir, 'index.html'), html);
    fs.writeFileSync(path.join(outDir, 'hub.css'), tplCss);
    fs.writeFileSync(path.join(outDir, 'hub.js'), tplJs);
    const clientHub = sanitizeClientHub(hub);
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

  if (hub.market?.map?.aria_label) {
    html = html.replace(
      'aria-label="Water network map"',
      `aria-label="${hub.market.map.aria_label}"`
    );
  }

  fs.writeFileSync(path.join(outDir, 'index.html'), html);
  fs.writeFileSync(path.join(outDir, 'hub.css'), tplCss);
  fs.writeFileSync(path.join(outDir, 'archetype.css'), archCss);
  fs.writeFileSync(path.join(outDir, 'hub.js'), tplJs);
  fs.writeFileSync(path.join(outDir, 'archetype.js'), archJs);

  const clientHub = sanitizeClientHub(hub);
  fs.writeFileSync(
    path.join(outDir, 'hub-data.js'),
    `/* GENERATED hub geometry for archetype */\nwindow.EMPLOYER_HUB_DATA = ${JSON.stringify(clientHub)};\n`
  );

  const clientArch = stripUnderscoreKeys(archData);
  // Never ship private access flags that contradict product decision (all public)
  if (clientArch.access && typeof clientArch.access === 'object') {
    clientArch.access = {
      mode: 'public',
      noindex: false,
      in_sitemap: true,
      in_nav: false,
      inbound_links_allowed: false,
    };
  }
  clientArch.route = `/${routePrefix}/${hubId}`;
  fs.writeFileSync(
    path.join(outDir, 'archetype-data.js'),
    `/* GENERATED from hubs/${hubId}/${dataFileName} */\nwindow.ARCHETYPE_DATA = ${JSON.stringify(clientArch)};\n`
  );

  const heroSrc = hub.brand?.hero_asset
    ? path.join(ROOT, hub.brand.hero_asset)
    : path.join(ROOT, 'deck-studio/assets/weta/passengers-stern-bright.png');
  if (fs.existsSync(heroSrc)) {
    fs.copyFileSync(heroSrc, path.join(outDir, 'assets', 'hero.jpg'));
  }

  console.log(`archetype → ${pageBase}/  (${archetypeId} · ${hubId})`);
  return pageBase;
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
    emitHub(hub, entry);
    built.push(hub.id);

    // Archetype pages when data files exist (Boston pilot first)
    const pp = emitArchetypePage(hub.id, hub, 'public-partners', 'public-partners.json', 'public-partners');
    const fi = emitArchetypePage(hub.id, hub, 'fleet-investors', 'fleet-investors.json', 'fleet-investors');
    if (pp) archetypes.push(pp);
    if (fi) archetypes.push(fi);
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

