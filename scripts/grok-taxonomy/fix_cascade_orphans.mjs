#!/usr/bin/env node
/**
 * Fix region → cluster → city cascade orphans (#79aq housekeeping).
 * - Normalize Asia → East Asia (Shanghai duplicate region chip)
 * - Wire Bolt/Yango mint cities into CLUSTERS.json
 * - Demote Philippines BP-as-city nodes to locales under parent cities
 * - Remove duplicate city twins (phuket-thailand, sabah-kk)
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const DC = path.join(ROOT, 'data-clean');

const REGION_ALIAS = { Asia: 'East Asia' };

const DELETE_CITIES = new Set(['phuket-thailand', 'sabah-kk']);

const CITY_ID_REMAP = {
  'phuket-thailand': 'phuket-phang-nga-thailand',
  'sabah-kk': 'sabah-kota-kinabalu-malaysia',
  'aktau-caspian-kazakhstan': 'aktau-kazakhstan',
  'baku-caspian-azerbaijan': 'baku-azerbaijan',
};

const CLUSTER_ADD = {
  'abc-islands': ['aruba-curacao-bonaire'],
  croatia: ['zadar-croatia'],
  cyprus: ['ayia-napa-cyprus', 'paphos-cyprus'],
  kenya: ['diani-ukunda-kenya', 'kilifi-kenya', 'malindi-kenya', 'watamu-kenya'],
  morocco: ['tangier-morocco', 'rabat-sale-morocco', 'mdiq-tetouan-morocco', 'mohammedia-morocco'],
  tunisia: ['tunis-tunisia', 'bizerte-tunisia', 'hammamet-tunisia', 'sousse-tunisia', 'monastir-tunisia'],
  'kazakhstan-caspian': ['aktau-kazakhstan', 'kuryk-kazakhstan'],
  'azerbaijan-caspian': ['baku-azerbaijan'],
  peru: ['pisco-san-andres-peru'],
  senegal: ['saly-senegal', 'somone-senegal', 'mbour-senegal'],
};

const NEW_CLUSTERS = [
  {
    cluster_id: 'algeria',
    cluster_label: 'Algeria',
    region: 'Maghreb',
    type: 'coastal',
    member_city_ids: ['algiers-algeria', 'bejaia-algeria', 'oran-algeria', 'mostaganem-algeria'],
    anchor_source: 'algiers-algeria',
  },
  {
    cluster_id: 'lebanon',
    cluster_label: 'Lebanon',
    region: 'MENA',
    type: 'coastal',
    member_city_ids: ['beirut-lebanon'],
    anchor_source: 'beirut-lebanon',
  },
  {
    cluster_id: 'finland',
    cluster_label: 'Finland',
    region: 'Europe',
    type: 'coastal',
    member_city_ids: ['helsinki-finland'],
    anchor_source: 'helsinki-finland',
  },
  {
    cluster_id: 'romania',
    cluster_label: 'Romania',
    region: 'Europe',
    type: 'coastal',
    member_city_ids: ['constanta-romania'],
    anchor_source: 'constanta-romania',
  },
];

const DEMOTE_TO_LOCALE = [
  { from: 'bp-d4738f6ad2', to: 'palawan-philippines__amanpulo', shortName: 'Amanpulo' },
  { from: 'bp-23245c74f6', to: 'palawan-philippines__el-nido', shortName: 'El Nido' },
  { from: 'bp-6af248fd3b', to: 'palawan-philippines__coron', shortName: 'Coron' },
  { from: 'bp-7a5f687851', to: 'palawan-philippines__puerto-princesa', shortName: 'Puerto Princesa' },
  { from: 'bp-893a394e6a', to: 'cebu-philippines__bohol-panglao', shortName: 'Bohol / Panglao' },
];

function load(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
function save(p, o) { fs.writeFileSync(p, JSON.stringify(o, null, 2) + '\n'); }

function remapDeep(obj, stats) {
  if (obj == null) return obj;
  if (typeof obj === 'string') {
    if (CITY_ID_REMAP[obj]) { stats.remap++; return CITY_ID_REMAP[obj]; }
    return obj;
  }
  if (Array.isArray(obj)) return obj.map((v) => remapDeep(v, stats));
  if (typeof obj === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(obj)) out[k] = remapDeep(v, stats);
    return out;
  }
  return obj;
}

function cityFeature(fbt, id) {
  for (const tier of ['city', 'priority_city']) {
    const hit = (fbt[tier] || []).find((f) => f.properties?.id === id);
    if (hit) return { tier, feat: hit };
  }
  return null;
}

function main() {
  const fbtPath = path.join(DC, 'FEATURES_BY_TYPE.json');
  const clustersPath = path.join(DC, 'CLUSTERS.json');
  const fbt = load(fbtPath);
  const clusters = load(clustersPath);
  const log = [];

  // 1. Region normalization
  for (const tier of ['city', 'priority_city', 'locale']) {
    for (const f of fbt[tier] || []) {
      const r = f.properties?.region;
      if (r && REGION_ALIAS[r]) {
        f.properties.region = REGION_ALIAS[r];
        log.push(`region ${f.properties.id}: ${r} → ${REGION_ALIAS[r]}`);
      }
    }
  }

  // 2. Demote Philippines BP-as-city → locale
  for (const { from, to, shortName } of DEMOTE_TO_LOCALE) {
    const hit = cityFeature(fbt, from);
    if (!hit) { log.push(`skip demote (missing): ${from}`); continue; }
    const { feat } = hit;
    fbt[hit.tier] = fbt[hit.tier].filter((f) => f.properties?.id !== from);
    const parent = feat.properties.parent_city_id;
    feat.properties.id = to;
    feat.properties.type = 'locale';
    feat.properties.shortName = shortName;
    delete feat.properties.promoted;
    feat.properties._demoted_from = from;
    if (!fbt.locale) fbt.locale = [];
    fbt.locale.push(feat);
    log.push(`demoted ${from} → locale ${to}`);
  }

  // 3. Delete duplicate city twins
  for (const tier of ['city', 'priority_city']) {
    const before = (fbt[tier] || []).length;
    fbt[tier] = (fbt[tier] || []).filter((f) => !DELETE_CITIES.has(f.properties?.id));
    const removed = before - (fbt[tier] || []).length;
    if (removed) log.push(`deleted ${removed} duplicate(s) from ${tier}`);
  }

  // 4. Rewire locale parents off deleted twins
  for (const loc of fbt.locale || []) {
    const p = loc.properties?.parent_city_id;
    if (p && CITY_ID_REMAP[p]) {
      loc.properties.parent_city_id = CITY_ID_REMAP[p];
      log.push(`locale ${loc.properties.id} parent ${p} → ${CITY_ID_REMAP[p]}`);
    }
  }

  // 5. CLUSTERS.json — add members, replace stale ids, mint country clusters
  const byId = Object.fromEntries(clusters.clusters.map((c) => [c.cluster_id, c]));

  for (const cl of clusters.clusters) {
    const orig = [...(cl.member_city_ids || [])];
    cl.member_city_ids = orig
      .map((id) => CITY_ID_REMAP[id] || id)
      .filter((id) => !DELETE_CITIES.has(id));
    const add = CLUSTER_ADD[cl.cluster_id] || [];
    for (const id of add) if (!cl.member_city_ids.includes(id)) cl.member_city_ids.push(id);
    if (JSON.stringify(orig) !== JSON.stringify(cl.member_city_ids)) {
      log.push(`cluster ${cl.cluster_id} members: ${cl.member_city_ids.join(', ')}`);
    }
    cl.members_present = cl.member_city_ids.length;
  }

  for (const spec of NEW_CLUSTERS) {
    if (byId[spec.cluster_id]) {
      for (const id of spec.member_city_ids) {
        if (!byId[spec.cluster_id].member_city_ids.includes(id)) {
          byId[spec.cluster_id].member_city_ids.push(id);
          byId[spec.cluster_id].members_present = byId[spec.cluster_id].member_city_ids.length;
        }
      }
      continue;
    }
    const anchorHit = cityFeature(fbt, spec.anchor_source);
    const anchor = anchorHit?.feat?.geometry?.coordinates || [0, 0];
    clusters.clusters.push({
      ...spec,
      anchor,
      members_present: spec.member_city_ids.length,
      members_missing: [],
      anchor_lb174_note: 'Grok cascade fix: Bolt/Yango mint wired to country cluster.',
    });
    log.push(`minted cluster ${spec.cluster_id}`);
  }

  clusters.clusters.sort((a, b) => a.cluster_id.localeCompare(b.cluster_id));

  // 6. Partner JSON id remap
  const remapStats = { remap: 0 };
  for (const file of fs.readdirSync(path.join(DC, 'partners')).filter((f) => f.endsWith('.json'))) {
    const p = path.join(DC, 'partners', file);
    const before = fs.readFileSync(p, 'utf8');
    const obj = load(p);
    const next = remapDeep(obj, remapStats);
    const after = JSON.stringify(next, null, 2) + '\n';
    if (after !== before) {
      save(p, next);
      log.push(`remapped ids in partners/${file}`);
    }
  }

  save(fbtPath, fbt);
  save(clustersPath, clusters);

  // 7. Orphan audit
  const clustered = new Set();
  for (const cl of clusters.clusters) for (const id of cl.member_city_ids || []) clustered.add(id);
  const orphans = [];
  for (const tier of ['city', 'priority_city']) {
    for (const f of fbt[tier] || []) {
      const id = f.properties?.id;
      if (!id || id.includes('__') || clustered.has(id)) continue;
      orphans.push({ id, name: f.properties.shortName || f.properties.name, region: f.properties.region, parent: f.properties.parent_city_id });
    }
  }
  orphans.sort((a, b) => a.region.localeCompare(b.region) || a.name.localeCompare(b.name));

  console.log('── fix_cascade_orphans ──');
  for (const line of log) console.log('  ', line);
  console.log(`partner id remaps: ${remapStats.remap}`);
  console.log(`orphans remaining: ${orphans.length}`);
  for (const o of orphans) console.log('  !', JSON.stringify(o));
  if (orphans.length) process.exit(1);
}

main();