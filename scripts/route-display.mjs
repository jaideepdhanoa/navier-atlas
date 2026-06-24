// Route display density — build-time classification + scoping (PR 1–3).
// Annotates routes with render_lane / story_tags / render_tw; emits MAP_DISPLAY config.
// Default (tier_visual): ship all geographically scoped routes; tier controls paint only.

export const EDGE_CLASS_TW = {
  trunk: 0.9,
  regional: 0.6,
  'cross-border-radial': 0.6,
  'inter-island': 0.58,
  'refuel-mid-node-leg': 0.62,
  'hub-radial-spoke': 0.5,
  'intra-cluster-spoke': 0.28,
  'intra-city': 0.18,
  local: 0.25,
};

export function resolveTW(p) {
  let w = (typeof p.traffic_weight === 'number') ? p.traffic_weight : (EDGE_CLASS_TW[p.edge_class] ?? 0.25);
  return w < 0.08 ? 0.08 : (w > 1 ? 1 : w);
}

export function resolveTier(p, tw) {
  if (typeof p.traffic_weight === 'number') return tw >= 0.80 ? 'trunk' : (tw >= 0.45 ? 'regional' : 'local');
  const ec = p.edge_class;
  if (ec === 'trunk') return 'trunk';
  if (ec === 'regional' || ec === 'cross-border-radial' || ec === 'inter-island'
    || ec === 'refuel-mid-node-leg' || ec === 'hub-radial-spoke') return 'regional';
  return 'local';
}

export function routeIdsOf(o) {
  const out = [];
  if (!o) return out;
  if (o.route_id) out.push(o.route_id);
  if (Array.isArray(o.route_ids)) out.push(...o.route_ids);
  return out;
}

/** Collect story route ids + tags from partner, optional market, and scoped briefs. */
export function collectStoryRoutes(partner, { market = null, cityBriefs = {}, clusterBriefs = {} } = {}) {
  const byId = new Map(); // routeId -> Set<tag>

  const add = (id, tag) => {
    if (!id) return;
    if (!byId.has(id)) byId.set(id, new Set());
    byId.get(id).add(tag);
  };

  const scanPhases = (phases, prefix) => {
    for (const ph of (phases || [])) {
      const n = ph.n ?? ph.phase ?? null;
      const phaseTag = n != null ? `phase:${n}` : `${prefix}:phase`;
      for (const r of (ph.featured_routes || [])) {
        for (const id of routeIdsOf(r)) add(id, phaseTag);
        add(r.route_id, 'featured');
      }
    }
  };

  if (market) {
    scanPhases(market.phases, `market:${market.slug || 'market'}`);
    for (const j of (market.journeys_unlocked || [])) {
      for (const id of routeIdsOf(j)) add(id, 'journey');
    }
    if (market.map_display?.roadmap_route_ids) {
      for (const id of market.map_display.roadmap_route_ids) add(id, 'roadmap');
    }
  } else if (partner) {
    scanPhases(partner.phases, 'partner');
    for (const j of (partner.journeys_unlocked || [])) {
      for (const id of routeIdsOf(j)) add(id, 'journey');
    }
    for (const m of (partner.markets || [])) {
      for (const j of (m.journeys_unlocked || [])) {
        for (const id of routeIdsOf(j)) add(id, `journey:${m.slug}`);
      }
      scanPhases(m.phases, `market:${m.slug}`);
    }
  }

  const md = (market?.map_display || partner?.map_display || {});
  for (const id of (md.roadmap_route_ids || [])) add(id, 'roadmap');
  for (const id of (md.promote_route_ids || [])) add(id, 'promoted');

  for (const brief of Object.values(cityBriefs)) {
    for (const sr of (brief.signature_routes || [])) {
      for (const id of routeIdsOf(sr)) add(id, 'signature');
    }
  }
  for (const brief of Object.values(clusterBriefs)) {
    for (const sr of (brief.signature_routes || [])) {
      for (const id of routeIdsOf(sr)) add(id, 'signature');
    }
  }

  return byId;
}

export function classifyRenderLane(p, tw, tier, storyTags, { keepSet, cityIdOf } = {}) {
  if (p.render_hidden === true) return 'hidden';
  if (storyTags && storyTags.size) return 'story';
  const cf = cityIdOf ? cityIdOf(p.from) : null;
  const ct = cityIdOf ? cityIdOf(p.to) : null;
  const touchesKeep = !keepSet || !keepSet.size || keepSet.has(cf) || keepSet.has(ct);
  if ((tier === 'trunk' || p.platform === 'Quanta-LR') && touchesKeep) return 'backbone';
  if (tier === 'regional' && touchesKeep) return 'context';
  if (p.distance_nm != null && p.distance_nm < 1.5) return 'capillary';
  if (tier === 'local') return 'capillary';
  return 'context';
}

export function ensureTrafficWeight(p) {
  if (typeof p.traffic_weight === 'number') return p;
  const tw = EDGE_CLASS_TW[p.edge_class];
  if (tw == null) return p;
  return { ...p, traffic_weight: tw, _traffic_weight_synth: true };
}

const DENSITY_ROUTE_CAP = 120;

function passesDensityCap(p, tier, id, storyById) {
  if (storyById.has(id)) return true;
  if (tier === 'trunk' || p.platform === 'Quanta-LR') return true;
  if (tier === 'regional') return true;
  if (p.distance_nm != null && p.distance_nm < 1.5) return false;
  if (tier === 'local') return false;
  return true;
}

function isLegacyDensity(md) {
  return md?.density_policy === 'legacy';
}

/** Geographic scope only — tier affects paint, not inclusion (default). */
function filterRoutesTierVisual(routes, { keep, pageKind, cityIdOf }) {
  const keepSet = new Set(keep);
  return routes.filter((f) => {
    const p = f.properties || {};
    if (p.render_hidden === true) return false;
    if (pageKind === 'market') {
      const cf = cityIdOf(p.from);
      const ct = cityIdOf(p.to);
      return keepSet.has(cf) && keepSet.has(ct);
    }
    return true;
  });
}

/** Legacy tier-based inclusion filter (opt-in via map_display.density_policy = legacy). */
function filterRoutesLegacy(routes, { keep, net, storyById, pageKind, cityIdOf }) {
  const keepSet = new Set(keep);
  const netSet = new Set(net);

  const filtered = routes.filter((f) => {
    const p = f.properties || {};
    if (p.render_hidden === true) return false;
    const id = p.id;
    if (id && storyById.has(id)) return true;

    const cf = cityIdOf(p.from);
    const ct = cityIdOf(p.to);
    const tw = resolveTW(p);
    const tier = resolveTier(p, tw);

    if (pageKind === 'market') {
      return keepSet.has(cf) && keepSet.has(ct);
    }

    if (pageKind === 'hub-index') {
      if (tier === 'trunk') return keepSet.has(cf) || keepSet.has(ct) || (netSet.has(cf) && netSet.has(ct));
      if (tier === 'regional') return (netSet.has(cf) && netSet.has(ct)) || (keepSet.has(cf) && keepSet.has(ct));
      return keepSet.has(cf) && keepSet.has(ct);
    }

    if (pageKind === 'flat') {
      if (tier === 'trunk') return keepSet.has(cf) || keepSet.has(ct);
      if (tier === 'regional') return (keepSet.has(cf) || netSet.has(cf)) && (keepSet.has(ct) || netSet.has(ct));
      return keepSet.has(cf) && keepSet.has(ct);
    }

    return true;
  });

  if (pageKind !== 'aggregate' && filtered.length > DENSITY_ROUTE_CAP) {
    return filtered.filter((f) => {
      const p = f.properties || {};
      const tier = resolveTier(p, resolveTW(p));
      return passesDensityCap(p, tier, p.id, storyById);
    });
  }
  return filtered;
}

/** Filter routes included on a scoped partner page. */
export function filterRoutesForPage(routes, { keep, net, storyById, pageKind, cityIdOf, densityPolicy = 'tier_visual' }) {
  if (pageKind === 'aggregate') return routes;
  if (densityPolicy === 'legacy') {
    return filterRoutesLegacy(routes, { keep, net, storyById, pageKind, cityIdOf });
  }
  return filterRoutesTierVisual(routes, { keep, pageKind, cityIdOf });
}

export function annotateRoutes(routes, { storyById = new Map(), keep = [], cityIdOf } = {}) {
  const keepSet = new Set(keep);
  return routes.map((f) => {
    const p0 = f.properties || {};
    const p = ensureTrafficWeight(p0);
    const tw = resolveTW(p);
    const tier = resolveTier(p, tw);
    const tags = storyById.get(p.id);
    const tagArr = tags ? [...tags] : undefined;
    const lane = classifyRenderLane(p, tw, tier, tags, { keepSet, cityIdOf });
    const capillary = tier === 'local' && p.distance_nm != null && p.distance_nm < 1.5;
    return {
      type: 'Feature',
      geometry: f.geometry,
      properties: {
        ...p,
        render_tier: tier,
        render_tw: Math.round(tw * 1000) / 1000,
        render_lane: lane,
        ...(tagArr ? { story_tags: tagArr } : {}),
        ...(capillary ? { render_capillary: true } : {}),
      },
    };
  });
}

const DENSITY_THRESHOLDS = { high: 41, extreme: 81 };

export function inferDensityTier(routeCount, partner, market) {
  const md = market?.map_display || partner?.map_display || {};
  if (md.density_tier) return md.density_tier;
  if (routeCount >= DENSITY_THRESHOLDS.extreme) return 'extreme';
  if (routeCount >= DENSITY_THRESHOLDS.high) return 'high';
  return 'normal';
}

export function defaultDensityMode(tier, storyCount) {
  if (storyCount > 0 && (tier === 'high' || tier === 'extreme')) return 'story';
  if (tier === 'extreme') return 'story';
  if (tier === 'high') return 'backbone';
  return 'backbone';
}

export function buildMapDisplay(partner, { market = null, routeCount = 0, storyCount = 0, pageKind = 'flat' } = {}) {
  const md = { ...(partner?.map_display || {}), ...(market?.map_display || {}) };
  const legacy = isLegacyDensity(md);
  const tier = inferDensityTier(routeCount, partner, market);
  if (legacy) {
    return {
      density_tier: tier,
      density_policy: 'legacy',
      default_mode: md.default_layer || defaultDensityMode(tier, storyCount),
      page_kind: pageKind,
      route_count: routeCount,
      story_count: storyCount,
      scope_mode: md.scope_mode || (pageKind === 'market' ? 'rollout_only' : 'phase_network'),
      modes: ['story', 'backbone', 'mesh'],
    };
  }
  return {
    density_tier: tier,
    density_policy: 'tier_visual',
    default_mode: 'full_network',
    page_kind: pageKind,
    route_count: routeCount,
    story_count: storyCount,
    scope_mode: 'full_network',
    modes: [],
  };
}

export function applyRouteDisplay(scoped, { partner, market = null, pageKind, keep, net, cityIdOf }) {
  const md = { ...(partner?.map_display || {}), ...(market?.map_display || {}) };
  const densityPolicy = isLegacyDensity(md) ? 'legacy' : 'tier_visual';

  const storyById = collectStoryRoutes(partner, {
    market,
    cityBriefs: scoped.CITY_BRIEFS || {},
    clusterBriefs: scoped.CLUSTER_BRIEFS || {},
  });

  const rawRoutes = scoped.ROUTES || [];
  const filtered = filterRoutesForPage(rawRoutes, {
    keep,
    net,
    storyById,
    pageKind,
    cityIdOf,
    densityPolicy,
  });

  const ROUTES = annotateRoutes(filtered, { storyById, keep, cityIdOf });
  const storyCount = ROUTES.filter((f) => f.properties?.render_lane === 'story').length;
  const MAP_DISPLAY = buildMapDisplay(partner, {
    market,
    routeCount: ROUTES.length,
    storyCount,
    pageKind,
  });

  return { ...scoped, ROUTES, MAP_DISPLAY, _route_display: { story_ids: [...storyById.keys()], filtered_from: rawRoutes.length } };
}