// Region deeplink helpers — slug ↔ label, alias normalization (mirrors index.html region nav).
export const REGION_ALIASES = {
  SEA: 'Southeast Asia',
  'LatAm-Caribbean': 'Latin America',
  'Latin-America': 'Latin America',
  Caribbean: 'Caribbean',
  'Europe-Mediterranean': 'Europe',
  'Europe-Atlantic': 'Europe',
  'Europe-Baltic': 'Europe',
  'Europe-Med': 'Europe',
  Asia: 'East Asia',
  'Middle East': 'MENA',
  Maghreb: 'MENA',
};

export function normRegion(label) {
  return REGION_ALIASES[label] || label;
}

export function regionSlug(label) {
  return String(label || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function collectRegionStats(data) {
  const stats = {};
  for (const t of ['city', 'priority_city']) {
    for (const f of data.FEATURES_BY_TYPE[t] || []) {
      const r0 = f.properties?.region;
      if (!r0) continue;
      const label = normRegion(r0);
      const slug = regionSlug(label);
      if (!slug || label === 'Global') continue;
      const bucket = stats[slug] || (stats[slug] = { slug, label, cities: 0, clusters: new Set() });
      bucket.cities += 1;
      const cid = f.properties?.cluster_id;
      if (cid) bucket.clusters.add(cid);
    }
  }
  for (const c of (data.CLUSTERS?.clusters || [])) {
    const label = normRegion(c.region);
    const slug = regionSlug(label);
    if (!slug || !stats[slug]) continue;
    if (c.cluster_id) stats[slug].clusters.add(c.cluster_id);
  }
  return Object.fromEntries(
    Object.entries(stats).map(([slug, s]) => [slug, { ...s, clusters: s.clusters.size }]),
  );
}