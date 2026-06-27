#!/usr/bin/env node
// A4 — Partner scope drift audit: stored _map_scope vs live CLUSTERS.json inheritance.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  loadClusters,
  scopeDriftReport,
  isHubPartner,
  resolveInheritedCityIds,
} from './partner-scope.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PARTNERS_DIR = path.join(ROOT, 'data-clean', 'partners');
const OUT_DIR = path.join(ROOT, 'handoff', 'partner-map-model');
const OUT_JSON = path.join(OUT_DIR, 'PARTNER-SCOPE-DRIFT-AUDIT.json');

const args = process.argv.slice(2);
const only = args.includes('--grab')
  ? ['grab']
  : args.filter((a) => !a.startsWith('--'));

const { byId: clusterById } = loadClusters();

const files = fs.readdirSync(PARTNERS_DIR).filter((f) => f.endsWith('.json'));
const partners = [];
for (const f of files) {
  const p = JSON.parse(fs.readFileSync(path.join(PARTNERS_DIR, f), 'utf8'));
  const pid = p.partner_id || f.replace('.json', '');
  if (only.length && !only.includes(pid)) continue;
  partners.push(p);
}

const reports = partners.map((p) => scopeDriftReport(p, clusterById));
reports.sort((a, b) => (b.missing_from_stored?.length || 0) - (a.missing_from_stored?.length || 0));

const hubReports = reports.filter((r) => r.is_hub);
const withGaps = reports.filter((r) => r.missing_from_stored?.length > 0 || r.stale_in_stored?.length > 0);

const summary = {
  at: new Date().toISOString(),
  partners_audited: reports.length,
  hub_partners: hubReports.length,
  partners_with_drift: withGaps.length,
  total_missing_cities: withGaps.reduce((s, r) => s + r.missing_from_stored.length, 0),
  grab: reports.find((r) => r.partner_id === 'grab') || null,
};

// Grab detail: per-market live inheritance
let grabMarkets = null;
const grabPartner = partners.find((p) => p.partner_id === 'grab');
if (grabPartner) {
  grabMarkets = (grabPartner.markets || []).map((m) => ({
    slug: m.slug,
    anchor_cities: m.anchor_cities,
    live_inherited: [...resolveInheritedCityIds(grabPartner, clusterById, { pageKind: 'market', market: m })].sort(),
  }));
}

const payload = { summary, grab_markets: grabMarkets, partners: reports };
fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(OUT_JSON, JSON.stringify(payload, null, 2) + '\n');

console.log(`Scope drift audit → ${OUT_JSON}`);
console.log(`  partners: ${summary.partners_audited} · hubs: ${summary.hub_partners} · with drift: ${summary.partners_with_drift}`);
if (summary.grab) {
  const g = summary.grab;
  console.log(`  grab: stored ${g.stored_city_count} → live ${g.live_city_count} (missing ${g.missing_from_stored.length})`);
  if (g.missing_from_stored.length) {
    console.log(`    +missing: ${g.missing_from_stored.slice(0, 8).join(', ')}${g.missing_from_stored.length > 8 ? '…' : ''}`);
  }
}

process.exit(withGaps.length && args.includes('--strict') ? 1 : 0);