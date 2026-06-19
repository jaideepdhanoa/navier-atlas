#!/usr/bin/env node
/**
 * Global taxonomy migration — Region → Cluster → City → Locale
 * Grok lane: CLUSTERS.json, FEATURES_BY_TYPE.locale, locale brief stubs, handoff manifest.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const DC = path.join(ROOT, 'data-clean');
const OUT = path.join(ROOT, 'grok-routing-output');
const SPINE = path.join(ROOT, 'app/data-spine/output/nodes.json');

const TODAY = '2026-06-19';

// ── Clusters to delete (demoted to locale OR duplicate twin) ─────────────────
const DELETE_CLUSTERS = new Set([
  'nassau-bahamas-cluster', 'turks-caicos-cluster', 'cayman-islands-cluster', 'usvi-bvi-cluster',
  'palm-jumeirah-dubai', 'the-world-dubai', 'abu-dhabi-islands',
  'aeolian-islands-italy', 'saronic-gulf-greece', 'ionian-islands-greece',
  'corsica-island-france', 'malta-archipelago', 'lisbon-tagus-estuary',
  'seychelles-archipelago', 'mauritius-island',
  'the-red-sea-archipelago', 'amaala-triple-bay', 'thuwal-private-retreat',
]);

// parent_cluster_id — multi-city sub-regions (routing anchor retained, hidden from nav)
const PARENT_CLUSTER = {
  'dalmatia-croatia': 'croatia',
  'bay-of-naples-amalfi-coast-italy': 'italy',
  'balearic-islands-spain': 'spain',
  'turkish-riviera-aegean': 'turkey',
  'cote-dazur-france-archipelago': 'france',
  'ksa-commercial': 'saudi-arabia',
  'leeward-antilles-northern': 'st-maarten-st-barths',
  'windward-antilles': 'st-lucia-grenadines',
};

// Demoted sub-cluster → locale brief stub(s)
const DEMOTE_TO_LOCALE = {
  'palm-jumeirah-dubai': {
    parent_city: 'dubai-uae',
    locale_ids: ['dubai-uae__palm-jumeirah-crescent-inner'],
    display: 'Palm Jumeirah',
    tagline: 'The iconic palm-shaped archipelago — dense marina and resort jetty network on a single causeway.',
  },
  'the-world-dubai': {
    parent_city: 'dubai-uae',
    locale_ids: ['dubai-uae__world-islands-heart-of-europe'],
    display: 'The World Islands',
    tagline: 'Artificial archipelago of 300 islands — Heart of Europe and resort jetties ripe for a clean marine layer.',
  },
  'abu-dhabi-islands': {
    parent_city: 'abu-dhabi-uae',
    locale_ids: [
      'abu-dhabi-uae__yas-island',
      'abu-dhabi-uae__saadiyat-island',
      'abu-dhabi-uae__abu-dhabi-island-corniche-al-maryah-cbd',
      'abu-dhabi-uae__sir-bani-yas-desert-islands',
    ],
    display: 'Abu Dhabi Islands & Corniche',
    tagline: 'Yas, Saadiyat, Lulu, Reem and the Corniche marina chain — the emirate\'s island corridor.',
    composite: true,
  },
  'aeolian-islands-italy': {
    parent_city: 'sicily-aeolian-italy',
    locale_ids: [],
    display: 'Aeolian Islands',
    tagline: 'Lipari · Vulcano · Stromboli · Panarea · Salina — volcanic island hop mesh.',
    note: 'City node sicily-aeolian-italy covers this market; no separate locale pins yet.',
  },
  'saronic-gulf-greece': {
    parent_city: 'athens-saronic-greece',
    locale_ids: [],
    display: 'Saronic Gulf',
    tagline: 'Piraeus · Aegina · Hydra · Spetses · Poros island ferry mesh.',
    note: 'City node athens-saronic-greece is the nav target.',
  },
  'ionian-islands-greece': {
    parent_city: 'corfu-ionian-greece',
    locale_ids: [],
    display: 'Ionian Islands',
    tagline: 'Corfu · Paxos · Lefkada · Kefalonia archipelago.',
    note: 'City node corfu-ionian-greece is the nav target.',
  },
  'corsica-island-france': {
    parent_city: 'corsica-france',
    locale_ids: [],
    display: 'Corsica',
    tagline: 'Ajaccio · Bastia · Bonifacio · Calvi coastal corridor.',
    note: 'City node corsica-france is the nav target.',
  },
  'malta-archipelago': {
    parent_city: 'malta-gozo',
    locale_ids: [],
    display: 'Maltese Archipelago',
    tagline: 'Valletta · Sliema · Gozo · Comino.',
    note: 'City node malta-gozo is the nav target.',
  },
  'lisbon-tagus-estuary': {
    parent_city: 'lisbon-tagus-portugal',
    locale_ids: [],
    display: 'Tagus Estuary',
    tagline: 'Cais do Sodré · Belém · south-bank ferries · Setúbal gateway.',
    note: 'City node lisbon-tagus-portugal is the nav target.',
  },
  'seychelles-archipelago': {
    parent_city: 'mahe-seychelles',
    locale_ids: [],
    display: 'Seychelles Archipelago',
    tagline: 'Mahé · Praslin · La Digue inter-island mesh.',
    note: 'City node mahe-seychelles is the nav target.',
  },
  'mauritius-island': {
    parent_city: 'port-louis-mauritius',
    locale_ids: [],
    display: 'Mauritius Island',
    tagline: 'Port Louis · Grand Baie · Le Morne coastal corridor.',
    note: 'City node port-louis-mauritius is the nav target.',
  },
  'the-red-sea-archipelago': {
    parent_city: 'the-red-sea-archipelago-ksa',
    locale_ids: [],
    display: 'The Red Sea Archipelago',
    tagline: 'Al Wajh archipelago — Shura · Ummahat · Sheybarah resort islands.',
    note: 'City node the-red-sea-archipelago-ksa is the nav target.',
  },
  'amaala-triple-bay': {
    parent_city: 'red-sea-global-ksa',
    locale_ids: [],
    display: 'AMAALA Triple Bay',
    tagline: 'Wellness hub · yacht club · marina jetties on the Red Sea coast.',
    note: 'Crosswalked to red-sea-global-ksa city.',
  },
  'thuwal-private-retreat': {
    parent_city: 'neom-sindalah-ksa',
    locale_ids: [],
    display: 'Thuwal Private Retreat',
    tagline: 'KAUST harbour access and private coastal retreat.',
    note: 'Parent city TBD by Tasklet — stub points to neom-sindalah-ksa.',
  },
};

const LATIN_AMERICA = new Set([
  'brazil', 'colombia', 'costa-rica', 'mexico', 'panama', 'galapagos-ecuador',
]);

const CARIBBEAN = new Set([
  'abc-islands', 'antigua-barbuda', 'bahamas', 'barbados', 'belize',
  'cayman-islands', 'cuba', 'dominican-republic', 'jamaica', 'puerto-rico',
  'st-lucia-grenadines', 'st-maarten-st-barths', 'turks-caicos', 'usvi-bvi',
  'leeward-antilles-northern', 'windward-antilles',
]);

const ORPHAN_WIRING = {
  'al-wakrah-qatar': 'qatar',
  'dammam-khobar-ksa': 'saudi-arabia',
  'moorea-french-polynesia': 'french-polynesia',
  'huahine-french-polynesia': 'french-polynesia',
  'maupiti-french-polynesia': 'french-polynesia',
};

// POI subnodes to promote as locale features when no locale twin exists
const PROMOTE_POI_TO_LOCALE = [
  'dubai-uae__palm-jumeirah-crescent-inner',
  'dubai-uae__dubai-marina-bluewaters',
  'abu-dhabi-uae__yas-island',
  'abu-dhabi-uae__saadiyat-island',
  'abu-dhabi-uae__abu-dhabi-island-corniche-al-maryah-cbd',
  'abu-dhabi-uae__sir-bani-yas-desert-islands',
];

function readJson(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n');
}

/** Prefer spine ids without '/' (filesystem-safe); maps slash variants → canonical. */
function canonicalLocaleId(id) {
  return id.replace(/\/-?/g, '-').replace(/-+/g, '-').replace(/-$/, '');
}

function shortLabel(name) {
  if (!name) return name;
  const s = name.replace(/\s*\([^)]*\)/g, '').trim();
  if (s.includes(' — ')) {
    const parts = s.split(' — ');
    const tail = parts.slice(1).join(' — ');
    const first = tail.split(/\s*[+/,]\s*/)[0].trim();
    return first || parts[0];
  }
  return s.split(/\s*[+,]\s*/)[0].trim() || s;
}

function coordsOf(n) {
  const c = n.coords || n.coord;
  if (Array.isArray(c) && c.length === 2 && c.every(Number.isFinite)) return c;
  return null;
}

function buildLocaleFeatures(nodes, cityIds) {
  const byId = {};
  for (const n of nodes) {
    if (n.type !== 'locale') continue;
    const c = coordsOf(n);
    if (!c || !n.parent_city_id) continue;
    if (!cityIds.has(n.parent_city_id)) continue;
    const cid = canonicalLocaleId(n.id);
    const prev = byId[cid];
    if (!prev || (prev.id.includes('/') && !n.id.includes('/'))) byId[cid] = { ...n, id: cid };
  }

  // dedupe by parent+name
  const byKey = {};
  for (const n of Object.values(byId)) {
    const key = `${n.parent_city_id}::${(n.name || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ')}`;
    const prev = byKey[key];
    if (!prev || (prev.id.includes('/') && !n.id.includes('/'))) byKey[key] = n;
  }

  // promote POI subnodes
  for (const nid of PROMOTE_POI_TO_LOCALE) {
    const n = nodes.find(x => x.id === nid && coordsOf(x));
    if (!n) continue;
    const parent = n.anchor_node_id || n.parent_city_id;
    if (!parent || !cityIds.has(parent)) continue;
    const key = `${parent}::${(n.name || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ')}`;
    if (!byKey[key]) byKey[key] = { ...n, type: 'locale', parent_city_id: parent };
  }

  const features = [];
  for (const n of Object.values(byKey)) {
    const full = n.name || n.id;
    features.push({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: coordsOf(n) },
      properties: {
        id: n.id,
        type: 'locale',
        name: full,
        shortName: shortLabel(full),
        fullName: full,
        parent_city_id: n.parent_city_id || n.anchor_node_id,
        region: n.region || null,
        is_anchor: n.is_anchor || false,
      },
    });
  }
  features.sort((a, b) => a.properties.id.localeCompare(b.properties.id));
  return features;
}

function migrateClusters(clustersData) {
  const changes = { deleted: [], parent_cluster_id: [], region_migrated: [], orphans_wired: [], locale_ids_removed: [] };
  const byId = Object.fromEntries(clustersData.clusters.map(c => [c.cluster_id, c]));

  // capture demoted cluster metadata before delete
  const demotedMeta = {};
  for (const cid of DELETE_CLUSTERS) {
    if (byId[cid]) demotedMeta[cid] = { ...byId[cid] };
  }

  let clusters = clustersData.clusters.filter(c => {
    if (DELETE_CLUSTERS.has(c.cluster_id)) {
      changes.deleted.push({ cluster_id: c.cluster_id, cluster_label: c.cluster_label, reason: DEMOTE_TO_LOCALE[c.cluster_id] ? 'demote_to_locale' : 'duplicate_twin' });
      return false;
    }
    return true;
  });

  clusters = clusters.map(c => {
    const copy = { ...c };
    if (PARENT_CLUSTER[c.cluster_id]) {
      copy.parent_cluster_id = PARENT_CLUSTER[c.cluster_id];
      copy.nav_hidden = true;
      changes.parent_cluster_id.push({ cluster_id: c.cluster_id, parent_cluster_id: PARENT_CLUSTER[c.cluster_id] });
    }
    if (c.region === 'LatAm-Caribbean') {
      if (LATIN_AMERICA.has(c.cluster_id)) {
        copy.region = 'Latin-America';
        changes.region_migrated.push({ cluster_id: c.cluster_id, from: 'LatAm-Caribbean', to: 'Latin-America' });
      } else if (CARIBBEAN.has(c.cluster_id)) {
        copy.region = 'Caribbean';
        changes.region_migrated.push({ cluster_id: c.cluster_id, from: 'LatAm-Caribbean', to: 'Caribbean' });
      }
    }
    // strip locale ids mistakenly listed as cluster members
    const cleaned = (copy.member_city_ids || []).filter(id => {
      if (id.includes('__')) {
        changes.locale_ids_removed.push({ cluster_id: c.cluster_id, locale_id: id });
        return false;
      }
      return true;
    });
    copy.member_city_ids = cleaned;
    return copy;
  });

  // wire orphans
  for (const [cityId, clusterId] of Object.entries(ORPHAN_WIRING)) {
    const cl = clusters.find(c => c.cluster_id === clusterId);
    if (!cl) continue;
    if (!(cl.member_city_ids || []).includes(cityId)) {
      cl.member_city_ids = [...(cl.member_city_ids || []), cityId];
      cl.members_present = cl.member_city_ids.length;
      changes.orphans_wired.push({ city_id: cityId, cluster_id: clusterId });
    }
  }

  clustersData.clusters = clusters;
  clustersData.version = 'v2-taxonomy';
  clustersData.generated = TODAY;
  clustersData.taxonomy_note = 'Global 4-tier migration: Region→Cluster→City→Locale. Sub-clusters demoted or parent_cluster_id.';
  return { clustersData, changes, demotedMeta };
}

function createLocaleBriefs(demotedMeta, cityBriefsDir, existingBriefs, cityRegion) {
  const created = [];
  const skipped = [];

  for (const [clusterId, spec] of Object.entries(DEMOTE_TO_LOCALE)) {
    const cluster = demotedMeta[clusterId];
    for (const localeId of spec.locale_ids || []) {
      if (existingBriefs.has(localeId)) { skipped.push({ locale_id: localeId, reason: 'exists' }); continue; }
      const brief = {
        city_id: localeId,
        display: spec.display,
        region: cityRegion[spec.parent_city] || cluster?.region || 'Global',
        tagline: spec.tagline,
        summary: `Migrated from cluster \`${clusterId}\` (${cluster?.cluster_label || clusterId}). ${cluster?.anchor_lb174_note || 'LB-174 routing anchor group — now a locale under ' + spec.parent_city + '.'} Tasklet: enrich with demand signals and signature routes.`,
        _taxonomy: {
          migrated_from_cluster: clusterId,
          parent_city_id: spec.parent_city,
          migration_date: TODAY,
          status: 'stub',
          grok_owner: 'Grok',
          tasklet_action: 'enrich',
        },
      };
      const fname = path.join(cityBriefsDir, `${canonicalLocaleId(localeId)}.json`);
      writeJson(fname, brief);
      created.push({ locale_id: localeId, from_cluster: clusterId, path: `data-clean/city_briefs/${localeId}.json` });
    }
    if ((spec.locale_ids || []).length === 0) {
      skipped.push({ cluster_id: clusterId, reason: spec.note || 'no_locale_pins', parent_city: spec.parent_city });
    }
  }
  return { created, skipped };
}

// ── main ─────────────────────────────────────────────────────────────────────
const clustersPath = path.join(DC, 'CLUSTERS.json');
const fbtPath = path.join(DC, 'FEATURES_BY_TYPE.json');
const nodesPath = SPINE;
const briefsDir = path.join(DC, 'city_briefs');

const clustersData = readJson(clustersPath);
const fbt = readJson(fbtPath);
const nodes = readJson(nodesPath).nodes || [];

const cityIds = new Set([
  ...(fbt.city || []).map(f => f.properties.id),
  ...(fbt.priority_city || []).map(f => f.properties.id),
]);

const { clustersData: migrated, changes, demotedMeta } = migrateClusters(clustersData);
writeJson(clustersPath, migrated);

const localeFeatures = buildLocaleFeatures(nodes, cityIds);
fbt.locale = localeFeatures;
writeJson(fbtPath, fbt);

const existingBriefs = new Set(fs.readdirSync(briefsDir).filter(f => f.endsWith('.json')).map(f => f.replace('.json', '')));
const cityRegion = {};
for (const f of [...(fbt.city || []), ...(fbt.priority_city || [])]) {
  if (f.properties?.id) cityRegion[f.properties.id] = f.properties.region;
}
const { created: briefsCreated, skipped: briefsSkipped } = createLocaleBriefs(demotedMeta, briefsDir, existingBriefs, cityRegion);

const manifest = {
  schema: 'navier-atlas/taxonomy-migration/v1',
  date: TODAY,
  summary: {
    clusters_before: clustersData.clusters.length,
    clusters_after: migrated.clusters.length,
    clusters_deleted: changes.deleted.length,
    parent_cluster_id_set: changes.parent_cluster_id.length,
    region_migrations: changes.region_migrated.length,
    orphans_wired: changes.orphans_wired.length,
    locale_features: localeFeatures.length,
    locale_briefs_created: briefsCreated.length,
    locale_briefs_skipped: briefsSkipped.length,
  },
  changes,
  demote_to_locale: DEMOTE_TO_LOCALE,
  locale_briefs_created: briefsCreated,
  locale_briefs_skipped: briefsSkipped,
  parent_cluster_map: PARENT_CLUSTER,
  delete_clusters: [...DELETE_CLUSTERS],
  tasklet_guardrails: [
    'Never add a cluster sharing member_city_id with an existing cluster unless parent_cluster_id is set.',
    'Sub-geographies inside a city → locale subnode (parent__locale id) + city_briefs entry.',
    'LB-174 routing anchors: parent_cluster_id + nav_hidden, OR locale under parent city.',
    'locale ids must never appear in CLUSTERS.member_city_ids.',
    'Re-emit FEATURES_BY_TYPE.locale on Tasklet builds (do not strip locales for BP-covered cities — Grok layer owns locale features until Tasklet adopts).',
  ],
};

fs.mkdirSync(OUT, { recursive: true });
writeJson(path.join(OUT, 'TAXONOMY-MIGRATION-2026-06-19.json'), manifest);

console.log('[taxonomy] clusters:', manifest.summary.clusters_before, '→', manifest.summary.clusters_after);
console.log('[taxonomy] locale features:', localeFeatures.length);
console.log('[taxonomy] locale brief stubs:', briefsCreated.length);
console.log('[taxonomy] manifest → grok-routing-output/TAXONOMY-MIGRATION-2026-06-19.json');