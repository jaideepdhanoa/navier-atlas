#!/usr/bin/env node
// Audit partner proposals for phase featured_routes, journeys_unlocked, and signature route linkage.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { collectStoryRoutes } from './route-display.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PARTNERS_DIR = path.join(ROOT, 'data-clean', 'partners');
const ROUTES_PATH = path.join(ROOT, 'data-clean', 'ROUTES.json');
const CITY_BRIEFS_DIR = path.join(ROOT, 'data-clean', 'city_briefs');
const OUT_PATH = path.join(ROOT, 'handoff', 'partner-map-model', 'PARTNER-ROUTE-LINKAGE-AUDIT.json');
const ALLOWLIST_PATH = path.join(ROOT, 'handoff', 'partner-map-model', 'ROUTE-LINKAGE-ALLOWLIST.json');

const args = process.argv.slice(2);
const STRICT = args.includes('--strict');
const GLOBAL = args.includes('--global');
const partnerFilter = (() => {
  const i = args.indexOf('--partner');
  if (i < 0) return null;
  const rest = args.slice(i + 1).filter((a) => !a.startsWith('--'));
  return rest.length ? rest : null;
})();

function routeIdsOfItem(o) {
  const out = [];
  if (!o || typeof o === 'string') return out;
  if (o.route_id) out.push(o.route_id);
  if (Array.isArray(o.route_ids)) out.push(...o.route_ids);
  return out;
}

function loadRouteIds() {
  const raw = JSON.parse(fs.readFileSync(ROUTES_PATH, 'utf8'));
  const feats = Array.isArray(raw) ? raw : (raw.features || []);
  return new Set(feats.map((f) => f.properties?.id).filter(Boolean));
}

function loadCityBriefs() {
  const o = {};
  if (!fs.existsSync(CITY_BRIEFS_DIR)) return o;
  for (const fn of fs.readdirSync(CITY_BRIEFS_DIR).filter((f) => f.endsWith('.json'))) {
    const rec = JSON.parse(fs.readFileSync(path.join(CITY_BRIEFS_DIR, fn), 'utf8'));
    o[rec.city_id || fn.replace(/\.json$/, '')] = rec;
  }
  return o;
}

function loadAllowlist() {
  if (!fs.existsSync(ALLOWLIST_PATH)) return new Set();
  const doc = JSON.parse(fs.readFileSync(ALLOWLIST_PATH, 'utf8'));
  return new Set(doc.partners || []);
}

function isGeometryPendingChip(o) {
  if (!o || typeof o !== 'object') return false;
  return o.display === 'text_only'
    || o.flag === 'network-chip-text-only'
    || o._link_status === 'unlinked-intra-city'
    || o._link_status === 'aspirational-no-built-route';
}

function auditFeaturedRoutes(items, label, routeIds) {
  const gaps = [];
  for (const r of (items || [])) {
    if (isGeometryPendingChip(r)) continue;
    if (typeof r === 'string') {
      gaps.push({ label, issue: 'no_route_id', featured_label: r });
      continue;
    }
    const ids = routeIdsOfItem(r);
    if (!ids.length) {
      gaps.push({ label, issue: 'no_route_id', featured_label: r.label || r.title || null });
      continue;
    }
    const missing = ids.filter((id) => !routeIds.has(id));
    if (missing.length) gaps.push({ label, issue: 'route_id_not_in_atlas', route_ids: missing, featured_label: r.label || null });
  }
  return gaps;
}

function auditPhases(phases, prefix, routeIds) {
  const gaps = [];
  for (const ph of (phases || [])) {
    const plabel = `${prefix} phase ${ph.n ?? ph.phase ?? '?'}`;
    const featured = ph.featured_routes || [];
    if (!featured.length) gaps.push({ scope: plabel, issue: 'no_featured_routes' });
    gaps.push(...auditFeaturedRoutes(featured, plabel, routeIds));
    const substantive = featured.filter((r) => !isGeometryPendingChip(r));
    const linked = substantive.filter((r) => typeof r !== 'string' && routeIdsOfItem(r).length).length;
    if (substantive.length && linked === 0) gaps.push({ scope: plabel, issue: 'featured_routes_unlinked', count: substantive.length });
  }
  return gaps;
}

function auditPartner(partner, routeIds, cityBriefs) {
  const pid = partner.partner_id;
  const storyById = collectStoryRoutes(partner, { cityBriefs });
  const gaps = [];
  gaps.push(...auditPhases(partner.phases, pid, routeIds));
  const hasLinkedFeatured = (partner.phases || []).some((ph) =>
    (ph.featured_routes || []).some((r) => typeof r !== 'string' && routeIdsOfItem(r).length));
  if (!hasLinkedFeatured && !partner.journeys_unlocked?.length
    && !(partner.markets || []).some((m) => m.journeys_unlocked?.length)) {
    gaps.push({ scope: pid, issue: 'no_story_routes_or_journeys' });
  }
  for (const j of (partner.journeys_unlocked || [])) {
    gaps.push(...auditFeaturedRoutes([j], `${pid} journey`, routeIds));
  }
  for (const m of (partner.markets || [])) {
    const mslug = m.slug || m.market_id || m.id || 'unknown';
    const mprefix = `${pid}/${mslug}`;
    gaps.push(...auditPhases(m.phases, mprefix, routeIds));
    gaps.push(...auditFeaturedRoutes(m.featured_routes, `${mprefix} featured`, routeIds));
    const mHasFeatured = (m.phases || []).some((ph) =>
      (ph.featured_routes || []).some((r) => typeof r !== 'string' && routeIdsOfItem(r).length))
      || (m.featured_routes || []).some((r) => typeof r !== 'string' && routeIdsOfItem(r).length);
    const mHasStoryChips = (m.phases || []).some((ph) => (ph.featured_routes || []).length > 0)
      || (m.journeys_unlocked || []).some((j) => isGeometryPendingChip(j))
      || (m.featured_routes || []).length > 0;
    if (!mHasFeatured && !m.journeys_unlocked?.length && !mHasStoryChips) {
      gaps.push({ scope: mprefix, issue: 'no_story_routes_or_journeys' });
    }
    for (const j of (m.journeys_unlocked || [])) {
      gaps.push(...auditFeaturedRoutes([j], `${mprefix} journey`, routeIds));
    }
  }
  return {
    partner_id: pid,
    layout: partner.layout || 'flat',
    story_route_count: storyById.size,
    gap_count: gaps.length,
    gaps,
  };
}

const routeIds = loadRouteIds();
const cityBriefs = loadCityBriefs();
const allowlist = loadAllowlist();
let partnerFiles = fs.readdirSync(PARTNERS_DIR).filter((f) => f.endsWith('.json') && !f.startsWith('_'));
if (partnerFilter) {
  const want = new Set(partnerFilter);
  partnerFiles = partnerFiles.filter((f) => want.has(f.replace(/\.json$/, '')));
}

const report = { generated_at: new Date().toISOString(), partners: [], summary: {} };
let totalGaps = 0;
let blockingGaps = 0;

for (const fn of partnerFiles.sort()) {
  const partner = JSON.parse(fs.readFileSync(path.join(PARTNERS_DIR, fn), 'utf8'));
  const row = auditPartner(partner, routeIds, cityBriefs);
  totalGaps += row.gap_count;
  const grandfathered = allowlist.has(row.partner_id) && row.gap_count > 0;
  const blocking = row.gap_count > 0 && (GLOBAL || !grandfathered);
  if (blocking) blockingGaps += row.gap_count;
  report.partners.push({ ...row, grandfathered, blocking });
}

report.summary = {
  partner_count: report.partners.length,
  partners_with_gaps: report.partners.filter((p) => p.gap_count).length,
  partners_blocking: report.partners.filter((p) => p.blocking).length,
  allowlist_size: allowlist.size,
  total_gaps: totalGaps,
  blocking_gaps: blockingGaps,
  partners_story_ready: report.partners.filter((p) => p.story_route_count >= 3).length,
};

if (!partnerFilter) {
  fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
  fs.writeFileSync(OUT_PATH, JSON.stringify(report, null, 2) + '\n');
}

console.log(`Route linkage audit${partnerFilter ? ` (${partnerFilter.join(', ')})` : ''} → ${OUT_PATH}`);
console.log(`  partners: ${report.summary.partner_count}`);
console.log(`  with gaps: ${report.summary.partners_with_gaps}`);
console.log(`  blocking (strict): ${report.summary.partners_blocking} (${report.summary.blocking_gaps} gaps)`);
console.log(`  allowlist: ${report.summary.allowlist_size}`);
console.log(`  story-ready (≥3 linked routes): ${report.summary.partners_story_ready}`);

for (const p of report.partners.filter((x) => x.gap_count).slice(0, 15)) {
  const tag = p.blocking ? '✗' : '⚠';
  console.log(`  ${tag} ${p.partner_id} — ${p.gap_count} gap(s)${p.grandfathered ? ' [allowlisted]' : ''}`);
}

if (STRICT && blockingGaps > 0) {
  console.error(`\nROUTE LINKAGE AUDIT FAILED — ${blockingGaps} blocking gap(s).`);
  console.error('  Fix: ./scripts/run-route-linkage-lane.sh --partner <slug> --apply');
  process.exit(1);
}