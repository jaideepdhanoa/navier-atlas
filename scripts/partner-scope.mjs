// Live partner map scope — resolves inherited cities from CLUSTERS.json at build time.
// Hub partners no longer depend on a frozen _map_scope.cluster_city_ids allowlist.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/** Market slug / footprint registry_key → country cluster_id */
export const MARKET_CLUSTER_ALIASES = {
  bali: 'indonesia',
  jakarta: 'indonesia',
  phuket: 'thailand',
  bangkok: 'thailand',
  'koh-samui': 'thailand',
  penang: 'malaysia',
  'cross-border': '__cross_border__',
};

export function loadClusters(dcRoot = path.join(ROOT, 'data-clean')) {
  const raw = JSON.parse(fs.readFileSync(path.join(dcRoot, 'CLUSTERS.json'), 'utf8'));
  const clusters = raw.clusters || [];
  const byId = new Map(clusters.map((c) => [c.cluster_id, c]));
  const cityToCluster = new Map();
  for (const c of clusters) {
    for (const id of c.member_city_ids || []) cityToCluster.set(id, c.cluster_id);
  }
  return { clusters, byId, cityToCluster };
}

export function isHubPartner(partner) {
  return (partner?.layout === 'hub' || partner?.layout === 'network')
    && Array.isArray(partner.markets) && partner.markets.length > 0;
}

/** Registry / market keys that seal full cluster inheritance (B5). */
export function sealedRegistryKeys(partner) {
  const keys = new Set();
  for (const m of partner.markets || []) {
    if (m.slug) keys.add(m.slug);
    if (m.id) keys.add(m.id);
  }
  for (const fp of partner.network_footprint || []) {
    if (fp.covered === true) keys.add(fp.registry_key || fp.id);
  }
  for (const k of partner._map_scope?.registry_keys || []) keys.add(k);
  return keys;
}

function crossBorderCityIds(clusterById) {
  const out = new Set(['riau-islands-indonesia', 'desaru-coast-malaysia', 'langkawi-malaysia']);
  for (const cid of ['singapore', 'malaysia']) {
    const c = clusterById.get(cid);
    if (c) for (const id of c.member_city_ids || []) out.add(id);
  }
  return out;
}

export function resolveRegistryKeyToCityIds(key, clusterById) {
  const alias = MARKET_CLUSTER_ALIASES[key];
  if (alias === '__cross_border__') return crossBorderCityIds(clusterById);

  const clusterId = alias || key;
  const cluster = clusterById.get(clusterId);
  if (cluster?.member_city_ids?.length) return new Set(cluster.member_city_ids);

  // City-level id (e.g. bali-indonesia) or unknown — pass through if it looks like a city id
  if (key.includes('-') || clusterById.has(key)) {
    const c2 = clusterById.get(key);
    if (c2) return new Set(c2.member_city_ids || []);
    return new Set([key]);
  }
  return new Set();
}

export function marketCities(market) {
  return [].concat(
    market.anchor_cities || [],
    ...((market.phases || []).map((ph) => ph.cities || [])),
  );
}

/** Cities inherited from live cluster membership for a hub partner page. */
export function resolveInheritedCityIds(partner, clusterById, { pageKind = 'hub-index', market = null } = {}) {
  const out = new Set();

  if (!isHubPartner(partner)) return out;

  if (pageKind === 'market' && market) {
    const key = market.slug || market.id;
    for (const c of marketCities(market)) out.add(c);
    for (const id of resolveRegistryKeyToCityIds(key, clusterById)) out.add(id);
    return out;
  }

  if (pageKind === 'hub-index') {
    for (const key of sealedRegistryKeys(partner)) {
      for (const id of resolveRegistryKeyToCityIds(key, clusterById)) out.add(id);
    }
    for (const c of partner.end_state?.end_state_cities || []) out.add(c);
    return out;
  }

  return out;
}

export function hubRolloutCities(partner, clusterById, { pageKind = 'hub-index', market = null } = {}) {
  const fromMarkets = (pageKind === 'market' && market)
    ? marketCities(market)
    : [].concat(...(partner.markets || []).map(marketCities));
  const inherited = [...resolveInheritedCityIds(partner, clusterById, { pageKind, market })];
  // Live inheritance is authoritative; legacy allowlist only fills gaps on hub-index.
  if (pageKind === 'hub-index') {
    const legacy = partner._map_scope?.cluster_city_ids || [];
    return [...new Set([...fromMarkets, ...inherited, ...legacy])];
  }
  return [...new Set([...fromMarkets, ...inherited])];
}

/** Materialize live scope for audit / optional JSON sync. */
export function materializeLiveMapScope(partner, clusterById) {
  const keys = [...sealedRegistryKeys(partner)].sort();
  const cities = [...resolveInheritedCityIds(partner, clusterById, { pageKind: 'hub-index' })].sort();
  return {
    _doc: 'Live cluster inheritance (scripts/partner-scope.mjs) — auto-synced from CLUSTERS.json',
    generated: new Date().toISOString(),
    source: 'live_cluster_inheritance',
    registry_keys: keys,
    cluster_city_ids: cities,
    inheritance_policy: 'covered_markets_and_footprint_union_cluster_members',
  };
}

export function scopeDriftReport(partner, clusterById) {
  const pid = partner.partner_id || partner.slug || 'unknown';
  const live = materializeLiveMapScope(partner, clusterById);
  const stored = new Set(partner._map_scope?.cluster_city_ids || []);
  const liveSet = new Set(live.cluster_city_ids);
  const missing = [...liveSet].filter((id) => !stored.has(id)).sort();
  const stale = [...stored].filter((id) => !liveSet.has(id)).sort();
  const endState = new Set(partner.end_state?.end_state_cities || []);
  const endMissing = [...endState].filter((id) => !liveSet.has(id)).sort();

  let expectedClusters = [];
  if (isHubPartner(partner)) {
    for (const key of sealedRegistryKeys(partner)) {
      const alias = MARKET_CLUSTER_ALIASES[key];
      const clusterId = alias === '__cross_border__' ? 'cross-border' : (alias || key);
      if (clusterById.has(clusterId) || alias === '__cross_border__') {
        expectedClusters.push(clusterId);
      }
    }
  }

  return {
    partner_id: pid,
    layout: partner.layout || 'flat',
    is_hub: isHubPartner(partner),
    sealed_registry_keys: live.registry_keys,
    stored_city_count: stored.size,
    live_city_count: liveSet.size,
    missing_from_stored: missing,
    stale_in_stored: stale,
    end_state_missing_from_live: endMissing,
    coverage_pct: stored.size
      ? Math.round((liveSet.size - missing.length) / liveSet.size * 100)
      : (liveSet.size ? 0 : 100),
    expected_clusters: [...new Set(expectedClusters)],
  };
}