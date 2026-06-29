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
  // Caspian basin — Baku (Caucasus) + Aktau/Kuryk (Central Asia) roll into the
  // `caspian` region brief; without these aliases the card auto-populated zero
  // clusters (the slugs `caucasus`/`central-asia` never matched `caspian`).
  Caucasus: 'Caspian',
  'Central Asia': 'Caspian',
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
  // FEATURES_BY_TYPE can carry duplicate rows per city id (mesh build artifact) — count unique ids only.
  const cityIdsBySlug = {};
  for (const t of ['city', 'priority_city']) {
    for (const f of data.FEATURES_BY_TYPE[t] || []) {
      const p = f.properties;
      const id = p?.id;
      const r0 = p?.region;
      if (!id || !r0) continue;
      const label = normRegion(r0);
      const slug = regionSlug(label);
      if (!slug || label === 'Global') continue;
      const bucket = stats[slug] || (stats[slug] = { slug, label, cities: 0, clusters: new Set() });
      const seen = cityIdsBySlug[slug] || (cityIdsBySlug[slug] = new Set());
      if (!seen.has(id)) {
        seen.add(id);
        bucket.cities += 1;
      }
      if (p.cluster_id) bucket.clusters.add(p.cluster_id);
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