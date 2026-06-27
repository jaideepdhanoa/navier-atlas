#!/usr/bin/env node
// Sync partner _map_scope.cluster_city_ids from live CLUSTERS.json inheritance.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadClusters, materializeLiveMapScope, isHubPartner } from './partner-scope.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PARTNERS_DIR = path.join(ROOT, 'data-clean', 'partners');
const PITCH_DIR = path.join(ROOT, 'partner-pitch', 'partners');

const args = process.argv.slice(2);
const dry = args.includes('--dry');
const only = args.filter((a) => !a.startsWith('--'));

const { byId: clusterById } = loadClusters();
const files = fs.readdirSync(PARTNERS_DIR).filter((f) => f.endsWith('.json'));

let updated = 0;
for (const f of files) {
  const pj = path.join(PARTNERS_DIR, f);
  const partner = JSON.parse(fs.readFileSync(pj, 'utf8'));
  const pid = partner.partner_id || f.replace('.json', '');
  if (only.length && !only.includes(pid)) continue;
  if (!isHubPartner(partner)) continue;

  const live = materializeLiveMapScope(partner, clusterById);
  const before = JSON.stringify(partner._map_scope?.cluster_city_ids || []);
  const after = JSON.stringify(live.cluster_city_ids);
  if (before === after && partner._map_scope?.source === 'live_cluster_inheritance') continue;

  console.log(`  ${dry ? '[dry] ' : ''}${pid}: ${(partner._map_scope?.cluster_city_ids || []).length} → ${live.cluster_city_ids.length} cities`);
  if (!dry) {
    partner._map_scope = live;
    const text = JSON.stringify(partner, null, 2) + '\n';
    fs.writeFileSync(pj, text);
    const pitch = path.join(PITCH_DIR, f);
    if (fs.existsSync(path.dirname(pitch))) fs.writeFileSync(pitch, text);
    updated++;
  }
}

console.log(dry ? 'Dry run complete.' : `Synced ${updated} hub partner(s).`);