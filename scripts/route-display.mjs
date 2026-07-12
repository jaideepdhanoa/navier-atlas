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
const MARQUEE_JOURNEY_MAX = 6;
const AUTO_LEGACY_ROUTE_THRESHOLD = 40;

/** Cities where intra-city mesh routinely overwhelms the map at market scope. */
const HIGH_DENSITY_CITY_IDS = new Set([
  'dubai-uae', 'abu-dhabi-uae', 'sharjah-uae', 'doha-qatar', 'manama-bahrain',
  'bangkok-thailand', 'phuket-thailand', 'pattaya-thailand', 'koh-samui-thailand',
]);

function isGeometryPending(o) {
  if (!o) return true;
  if (o.display === 'text_only' || o.flag === 'network-chip-text-only') return true;
  if (o.flag === 'aspirational-no-built-route' || /aspirational-no-built-route/i.test(String(o._link_status || ''))) return true;
  if (/null-geometry-pending/i.test(String(o._link_status || ''))) return true;
  if (o.route_id === null && !routeIdsOf(o).length && o.from_node_id && o.from_node_id === o.to_node_id) return true;
  return false;
}

/** Score journeys for marquee display — higher = more map-ready / proposal-worthy. */
export function journeyDisplayScore(j, routeIdSet) {
  if (isGeometryPending(j)) return -1;
  const ids = routeIdsOf(j).filter((id) => routeIdSet.has(id));
  const hasNodes = !!(j.from_node_id && j.to_node_id && j.from_node_id !== j.to_node_id);
  if (!ids.length && !hasNodes) return -1;
  let score = ids.length ? 12 : 3;
  if (j.platform === 'Quanta-LR') score += 2;
  if (typeof j.distance_nm === 'number' && j.distance_nm >= 8) score += 2;
  else if (typeof j.distance_nm === 'number' && j.distance_nm >= 3) score += 1;
  if (j.with_navier) score += 0.5;
  if (j.today) score += 0.25;
  return score;
}

export function curateJourneys(journeys, routeIdSet, max = MARQUEE_JOURNEY_MAX) {
  return (journeys || [])
    .map((j) => ({ j, score: journeyDisplayScore(j, routeIdSet) }))
    .filter((x) => x.score >= 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, max)
    .map((x) => x.j);
}

export function curateSignatureRoutes(routes, routeIdSet, max = MARQUEE_JOURNEY_MAX) {
  return (routes || [])
    .map((r) => {
      const o = (typeof r === 'string') ? { label: r } : (r || {});
      if (isGeometryPending(o)) return { o, score: -1 };
      const ids = routeIdsOf(o).filter((id) => routeIdSet.has(id));
      if (!ids.length) return { o, score: -1 };
      let score = 10 + ids.length;
      if (typeof o.distance_nm === 'number' && o.distance_nm >= 5) score += 1;
      return { o, score };
    })
    .filter((x) => x.score >= 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, max)
    .map((x) => x.o);
}

function rankRouteForCull(f, storyById) {
  const p = ensureTrafficWeight(f.properties || {});
  const tw = resolveTW(p);
  const tier = resolveTier(p, tw);
  let score = tw;
  if (p.id && storyById.has(p.id)) score += 100;
  if (tier === 'trunk' || p.platform === 'Quanta-LR') score += 50;
  if (tier === 'regional') score += 20;
  if (typeof p.distance_nm === 'number' && p.distance_nm >= 5) score += 8;
  if (typeof p.distance_nm === 'number' && p.distance_nm < 1.5) score -= 25;
  return score;
}

/**
 * Thin intra-city meshes and duplicate inter-city pairs when route volume overwhelms area.
 * Story routes always survive; inter-city corridors are kept in full unless duplicated heavily.
 */
export function densityCullRoutes(routes, { storyById, cityIdOf, densityTier, pageKind, keep = [], inheritClusters = false }) {
  if (pageKind === 'aggregate' || densityTier === 'normal') return routes;
  // Hub index with live cluster inheritance: ship the full canonical set.
  // Density is a paint/zoom concern — never delete inherited geography (Dott/Voi #216).
  if (pageKind === 'hub-index' && inheritClusters) {
    return routes;
  }

  const touchesDense = keep.some((id) => HIGH_DENSITY_CITY_IDS.has(id));
  const intraCap = densityTier === 'extreme' ? (touchesDense ? 8 : 12) : 18;
  const interDupCap = densityTier === 'extreme' ? 4 : 6;

  const inter = [];
  const intraByCity = new Map();
  for (const f of routes) {
    const cf = cityIdOf(f.properties?.from);
    const ct = cityIdOf(f.properties?.to);
    if (cf && ct && cf === ct) {
      if (!intraByCity.has(cf)) intraByCity.set(cf, []);
      intraByCity.get(cf).push(f);
    } else {
      inter.push(f);
    }
  }

  const keptIntra = [];
  for (const list of intraByCity.values()) {
    const sorted = [...list].sort((a, b) => rankRouteForCull(b, storyById) - rankRouteForCull(a, storyById));
    keptIntra.push(...sorted.slice(0, intraCap));
  }

  const interByPair = new Map();
  for (const f of inter) {
    const cf = cityIdOf(f.properties?.from);
    const ct = cityIdOf(f.properties?.to);
    const k = [cf, ct].sort().join('|');
    if (!interByPair.has(k)) interByPair.set(k, []);
    interByPair.get(k).push(f);
  }
  const keptInter = [];
  for (const list of interByPair.values()) {
    if (list.length <= interDupCap) {
      keptInter.push(...list);
      continue;
    }
    const sorted = [...list].sort((a, b) => rankRouteForCull(b, storyById) - rankRouteForCull(a, storyById));
    keptInter.push(...sorted.slice(0, interDupCap));
  }

  return [...keptIntra, ...keptInter];
}

function resolveDensityPolicy(md, routeCount, keep = [], pageKind = 'flat', { inheritClusters = false } = {}) {
  // Aggregate atlas always ships the full network; lane filters + zoom opacity handle legibility.
  if (pageKind === 'aggregate') return 'tier_visual';
  // Live-inheritance hubs must never auto-switch to legacy tier deletion (threshold 40).
  if (pageKind === 'hub-index' && inheritClusters) return 'tier_visual';
  if (isLegacyDensity(md)) return 'legacy';
  const touchesDense = keep.some((id) => HIGH_DENSITY_CITY_IDS.has(id));
  if (routeCount >= AUTO_LEGACY_ROUTE_THRESHOLD || touchesDense) return 'legacy';
  return 'tier_visual';
}

export function curatePartnerDisplay(partner, {
  market = null,
  routeIdSet,
  cityBriefs = {},
  clusterBriefs = {},
  maxJourneys = MARQUEE_JOURNEY_MAX,
} = {}) {
  if (!partner) return partner;
  const out = { ...partner };
  const rid = routeIdSet || new Set();

  if (market) {
    const m = { ...market };
    m.journeys_unlocked = curateJourneys(market.journeys_unlocked, rid, maxJourneys);
    if (Array.isArray(m.phases)) {
      m.phases = m.phases.map((ph) => ({
        ...ph,
        featured_routes: (ph.featured_routes || []).filter((fr) => {
          if (typeof fr === 'string') return false;
          if (isGeometryPending(fr)) return false;
          const ids = routeIdsOf(fr).filter((id) => rid.has(id));
          return ids.length > 0 || !!(fr.from_node_id && fr.to_node_id && fr.from_node_id !== fr.to_node_id);
        }),
      }));
    }
    out.markets = (partner.markets || []).map((x) => (x.slug === market.slug ? m : x));
  } else {
    out.journeys_unlocked = curateJourneys(partner.journeys_unlocked, rid, maxJourneys);
    if (Array.isArray(out.phases)) {
      out.phases = out.phases.map((ph) => ({
        ...ph,
        featured_routes: (ph.featured_routes || []).filter((fr) => {
          if (typeof fr === 'string') return false;
          if (isGeometryPending(fr)) return false;
          const ids = routeIdsOf(fr).filter((id) => rid.has(id));
          return ids.length > 0 || !!(fr.from_node_id && fr.to_node_id && fr.from_node_id !== fr.to_node_id);
        }),
      }));
    }
  }

  return {
    partner: out,
    cityBriefs: Object.fromEntries(
      Object.entries(cityBriefs).map(([cid, b]) => [
        cid,
        { ...b, signature_routes: curateSignatureRoutes(b.signature_routes, rid, maxJourneys) },
      ]),
    ),
    clusterBriefs: Object.fromEntries(
      Object.entries(clusterBriefs).map(([cid, b]) => [
        cid,
        { ...b, signature_routes: curateSignatureRoutes(b.signature_routes, rid, maxJourneys) },
      ]),
    ),
  };
}

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

const COMMERCIAL_SUPPRESS_ARCHETYPES = new Set([
  'ridehail', 'super_app', 'mobility_platform',
]);

function suppressCommercialSovereign(p, partner) {
  if (!p._commercial_suppress_sovereign) return false;
  const arch = partner?.archetype || '';
  const pid = partner?.partner_id || '';
  if (COMMERCIAL_SUPPRESS_ARCHETYPES.has(arch)) return true;
  if (pid === 'bolt' || pid === 'yango' || pid === 'uber' || pid === 'careem'
    || pid === 'noon' || pid === 'indrive' || pid === 'cabify') return true;
  return false;
}

/** Geographic scope only — tier affects paint, not inclusion (default). */
function filterRoutesTierVisual(routes, { keep, pageKind, cityIdOf, partner = null }) {
  const keepSet = new Set(keep);
  return routes.filter((f) => {
    const p = f.properties || {};
    if (p.render_hidden === true) return false;
    if (partner && suppressCommercialSovereign(p, partner)) return false;
    if (pageKind === 'market') {
      const cf = cityIdOf(p.from) || p.from_city_id || null;
      const ct = cityIdOf(p.to) || p.to_city_id || null;
      if (keepSet.has(cf) && keepSet.has(ct)) return true;
      // Cross-border connective tissue: trunk / Quanta-LR backbone edges render
      // when at least one endpoint is in scope (the far endpoint is an out-of-cluster
      // cross-border node). Mirrors classifyRenderLane's backbone touchesKeep rule.
      const tier = resolveTier(p, resolveTW(p));
      if ((tier === 'trunk' || p.platform === 'Quanta-LR') && (keepSet.has(cf) || keepSet.has(ct))) return true;
      return false;
    }
    return true;
  });
}

/** Legacy tier-based inclusion filter (opt-in via map_display.density_policy = legacy). */
function filterRoutesLegacy(routes, { keep, net, storyById, pageKind, cityIdOf, partner = null }) {
  const keepSet = new Set(keep);
  const netSet = new Set(net);

  const filtered = routes.filter((f) => {
    const p = f.properties || {};
    if (p.render_hidden === true) return false;
    if (partner && suppressCommercialSovereign(p, partner)) return false;
    const id = p.id;
    if (id && storyById.has(id)) return true;

    const cf = cityIdOf(p.from) || p.from_city_id || null;
    const ct = cityIdOf(p.to) || p.to_city_id || null;
    const tw = resolveTW(p);
    const tier = resolveTier(p, tw);

    if (pageKind === 'market') {
      if (keepSet.has(cf) && keepSet.has(ct)) return true;
      // Cross-border connective tissue: trunk / Quanta-LR backbone edges render when
      // at least one endpoint is in scope. Kept consistent with the tier_visual path so
      // dense (legacy) markets don't strip the cross-border edges back out on the 2nd pass.
      if ((tier === 'trunk' || p.platform === 'Quanta-LR') && (keepSet.has(cf) || keepSet.has(ct))) return true;
      return false;
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

  // Market pages use area-density culling (densityCullRoutes) — skip the flat 120 cap here.
  if (pageKind !== 'aggregate' && pageKind !== 'market' && filtered.length > DENSITY_ROUTE_CAP) {
    return filtered.filter((f) => {
      const p = f.properties || {};
      const tier = resolveTier(p, resolveTW(p));
      return passesDensityCap(p, tier, p.id, storyById);
    });
  }
  return filtered;
}

/** Filter routes included on a scoped partner page. */
export function filterRoutesForPage(routes, { keep, net, storyById, pageKind, cityIdOf, densityPolicy = 'tier_visual', partner = null }) {
  if (pageKind === 'aggregate') return routes;
  if (densityPolicy === 'legacy') {
    return filterRoutesLegacy(routes, { keep, net, storyById, pageKind, cityIdOf, partner });
  }
  return filterRoutesTierVisual(routes, { keep, pageKind, cityIdOf, partner });
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
  // Partner landing / "The network" overview: full mesh. Phase carousel tightens via applyPhaseFocus.
  if (tier === 'extreme' || tier === 'high' || storyCount > 0) return 'mesh';
  return 'backbone';
}

export function buildMapDisplay(partner, { market = null, routeCount = 0, storyCount = 0, pageKind = 'flat', densityPolicy = null } = {}) {
  const md = { ...(partner?.map_display || {}), ...(market?.map_display || {}) };
  if (pageKind === 'aggregate') {
    return {
      density_tier: inferDensityTier(routeCount, partner, market),
      density_policy: 'tier_visual',
      default_mode: 'full_network',
      page_kind: pageKind,
      route_count: routeCount,
      story_count: storyCount,
      scope_mode: 'full_network',
      modes: [],
    };
  }
  const legacy = densityPolicy === 'legacy' || (densityPolicy == null && isLegacyDensity(md));
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

export function applyRouteDisplay(scoped, { partner, market = null, pageKind, keep, net, cityIdOf, inheritClusters = false }) {
  const md = { ...(partner?.map_display || {}), ...(market?.map_display || {}) };

  const storyById = collectStoryRoutes(partner, {
    market,
    cityBriefs: scoped.CITY_BRIEFS || {},
    clusterBriefs: scoped.CLUSTER_BRIEFS || {},
  });

  const rawRoutes = scoped.ROUTES || [];
  const preTier = inferDensityTier(rawRoutes.length, partner, market);
  const densityPolicy = resolveDensityPolicy(md, rawRoutes.length, keep, pageKind, { inheritClusters });

  let filtered = filterRoutesForPage(rawRoutes, {
    keep,
    net,
    storyById,
    pageKind,
    cityIdOf,
    densityPolicy: 'tier_visual',
    partner,
  });

  // Full-set inheritance: skip cull + legacy re-filter for hub-index live cluster pages.
  if (!(pageKind === 'hub-index' && inheritClusters)) {
    const cullTier = preTier !== 'normal' ? preTier : inferDensityTier(filtered.length, partner, market);
    if (pageKind !== 'aggregate' && cullTier !== 'normal') {
      filtered = densityCullRoutes(filtered, { storyById, cityIdOf, densityTier: cullTier, pageKind, keep, inheritClusters });
    }

    if (densityPolicy === 'legacy') {
      filtered = filterRoutesForPage(filtered, {
        keep,
        net,
        storyById,
        pageKind,
        cityIdOf,
        densityPolicy: 'legacy',
        partner,
      });
    }
  }

  const ROUTES = annotateRoutes(filtered, { storyById, keep, cityIdOf });
  const storyCount = ROUTES.filter((f) => f.properties?.render_lane === 'story').length;
  const routeIdSet = new Set(ROUTES.map((f) => f.properties?.id).filter(Boolean));
  const curated = partner ? curatePartnerDisplay(partner, {
    market,
    routeIdSet,
    cityBriefs: scoped.CITY_BRIEFS || {},
    clusterBriefs: scoped.CLUSTER_BRIEFS || {},
  }) : null;

  const slug = partner?.partner_id;
  const MAP_DISPLAY = buildMapDisplay(partner, {
    market,
    routeCount: ROUTES.length,
    storyCount,
    pageKind,
    densityPolicy,
  });
  if (densityPolicy === 'legacy' && !md.default_layer) {
    MAP_DISPLAY.default_mode = defaultDensityMode(MAP_DISPLAY.density_tier, storyCount);
  }

  return {
    ...scoped,
    ROUTES,
    MAP_DISPLAY,
    ...(curated ? {
      CITY_BRIEFS: curated.cityBriefs,
      CLUSTER_BRIEFS: curated.clusterBriefs,
      PARTNERS: slug ? { [slug]: curated.partner } : scoped.PARTNERS,
    } : {}),
    _route_display: {
      story_ids: [...storyById.keys()],
      filtered_from: rawRoutes.length,
      culled_to: ROUTES.length,
      density_policy: densityPolicy,
    },
  };
}