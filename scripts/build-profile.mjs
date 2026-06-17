// Build profiles for atlas-data.js — public (network atlas) vs internal (full admin).

/** ROUTES blob may be a bare Feature[] or GeoJSON FeatureCollection (#79aj-v2+). */
export function normalizeRouteBlob(routes) {
  if (Array.isArray(routes)) return routes;
  if (routes && Array.isArray(routes.features)) return routes.features;
  return routes || [];
}

export function parseProfile(argv = process.argv) {
  const flag = argv.find((a) => a.startsWith('--profile='));
  if (flag) return flag.split('=')[1];
  const i = argv.indexOf('--profile');
  if (i >= 0 && argv[i + 1]) return argv[i + 1];
  return process.env.BUILD_PROFILE || 'public';
}

const SHEET_URL = /docs\.google\.com\/spreadsheets/i;

/** Drop partner attribution + internal model links from a route-economics record. */
export function sanitizePublicEconRecord(rec) {
  const { partner, deck_url, ...rest } = rec;
  return scrubSheetUrls(rest);
}

function scrubSheetUrls(val) {
  if (val == null) return val;
  if (typeof val === 'string') return SHEET_URL.test(val) ? null : val;
  if (Array.isArray(val)) return val.map(scrubSheetUrls).filter((v) => v != null);
  if (typeof val === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(val)) {
      const scrubbed = scrubSheetUrls(v);
      if (scrubbed != null) out[k] = scrubbed;
    }
    return out;
  }
  return val;
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
    ROUTE_ECONOMICS[rid] = sanitizePublicEconRecord(rec);
  }
  return {
    ...data,
    PARTNERS: {},
    STORIES: [],
    CITY_BRIEFS,
    ROUTE_ECONOMICS,
  };
}