// Build profiles for atlas-data.js — public (network atlas) vs internal (full admin).

export function parseProfile(argv = process.argv) {
  const flag = argv.find((a) => a.startsWith('--profile='));
  if (flag) return flag.split('=')[1];
  const i = argv.indexOf('--profile');
  if (i >= 0 && argv[i + 1]) return argv[i + 1];
  return process.env.BUILD_PROFILE || 'public';
}

/** Strip partner-private globals for the public network atlas. */
export function applyProfile(data, profile) {
  if (profile !== 'public') return data;
  const CITY_BRIEFS = {};
  for (const [cid, brief] of Object.entries(data.CITY_BRIEFS || {})) {
    if (!brief || typeof brief !== 'object') { CITY_BRIEFS[cid] = brief; continue; }
    const { partner_overlays, ...rest } = brief;
    CITY_BRIEFS[cid] = rest;
  }
  const ROUTE_ECONOMICS = {};
  for (const [rid, rec] of Object.entries(data.ROUTE_ECONOMICS || {})) {
    if (!rec || typeof rec !== 'object') continue;
    const { partner, deck_url, ...rest } = rec;
    ROUTE_ECONOMICS[rid] = rest;
  }
  return {
    ...data,
    PARTNERS: {},
    STORIES: [],
    CITY_BRIEFS,
    ROUTE_ECONOMICS,
  };
}