# Parked — Routing & Geometry Closure Queue

**Parked:** 2026-06-24  
**Resume when:** Returning to navier-atlas routing/geometry work after interim tasks.

Use this file + `PARKED-ROUTING-GEOMETRY-QUEUE.json` to restore full context.  
Copy the **Resume prompt** block into a new Grok session to continue.

---

## Resume prompt (paste into Grok)

```
Continue the parked navier-atlas routing/geometry closure queue.

Repo: /Users/jaideep/navier-atlas
Read first: handoff/partner-map-model/PARKED-ROUTING-GEOMETRY-QUEUE.md
             handoff/partner-map-model/PARKED-ROUTING-GEOMETRY-QUEUE.json

Baseline (deployed): main @ e1f69dcf · https://navier-atlas.vercel.app
Story QA: 839 pass / 205 fail (80.4%) — target is now 100% (0 story fails).

Resume in priority order:
1. Story geometry completion (205 remaining; per-corridor authorship, not mask-only)
2. South Africa mesh (6/10 routes still fail QA; bind route_id on bolt.json journeys)
3. Croatia depth (bolt-croatia corridors)
4. Phase 0 footprint (≥80 Bolt cities; Cyprus/Israel/Auckland)
5. Phase 2 corridor minting waves (East Africa v2, Estonia, Grab Thailand, etc.)
6. Economics (Phase 5)

Do not re-do completed work (channel mint gate, city ID norm, deploy e1f69dcf).
```

---

## North star (updated)

| Metric | Deployed now | **Target when resumed** |
|--------|--------------|-------------------------|
| Story geometry pass | **839 / 1044 (80.4%)** | **1044 / 1044 (100%)** — all story routes complete |
| Story allowlisted | 0 | 0 (true aspirational only) |
| Severe story fails (>1 km) | ~170 | 0 |
| Bolt hub scoped routes | ~778 | ≥ 1,200 (after norm + footprint) |
| Bolt map rollout cities | 56 build / 38 `_map_scope` | ≥ 80 visible |
| `route_id: null` (partner JSON) | ~606 aspirational | < 50 true aspirational only |

The 80% gate was met for the interim deploy. **All story routes must pass land QA** before calling geometry “done.”

---

## Deployed baseline (do not redo)

| Item | Value |
|------|-------|
| **Production** | https://navier-atlas.vercel.app |
| **Git** | `main` @ `e1f69dcf` (includes `c47bafb1` regional masks) |
| **SEAL gate** | `geometry_story`: FAIL — story 839 pass / 205 fail |
| **SEAL allowlist** | PASS — 0 story routes on allowlist |
| **Pre-flight** | Green on `e1f69dcf` deploy (RELEASE=1) |
| **Linkage** | 0 gaps across 58 partners |

### Completed in this sprint

- **Channel minting (80% gate):** `regional_land_masks.py` + waypoint lookup → 663→839 story pass
- **City ID normalization (Phase 1):** ~0.46% mismatch (done earlier)
- **Deploy + SEAL refresh:** `e1f69dcf`
- **Scripts added/updated:** see Key files below

---

## Parked queue (priority order)

### P0 — Story geometry completion (205 routes)

**Why parked:** Mask refinements exhausted; remaining fails need per-corridor geometry.

**Fail profile** (from `GEOMETRY-TRIAGE.json` priority_fix):

| Land bucket | Count (approx.) |
|-------------|-----------------|
| < 1 km | ~30 |
| 1–5 km | ~95 |
| 5–15 km | ~50 |
| 15–50 km | ~20 |
| 50+ km (hard) | 5 |

**Hard blockers (50+ km):** Turkey 268 nm (`rn-460c45c21fb8`), Komodo 261 nm (`gcn-3273659cd1-shared`), India coastal (`rn-f6761e2793e7`), Chicago lake (`e__chicago-lake-michigan-usa__…`), Portugal Tagus→Algarve (`rn-67dc105ba6e9`).

**Approach:**

1. Tier nudge: `mint_story_channels.py --apply --nudge-only --min-land-km 0.05 --max-land-km 5`
2. Hand + channel: `mint_story_channels.py --apply --channel-only --min-land-km 1 --max-land-km 15`
3. Tier 5 ocean-chain: `mint_hand_waypoints.py --apply --min-land-km 0.05 --max-land-km 20`
4. Per-corridor `HAND_WAYPOINTS` in `channel_solver.py` / `mint_hand_waypoints.py` `city_wps` for `ics-*` island hops
5. Only expand `regional_land_masks.py` where shallow-water false positives are proven — not as a substitute for geometry

**Acceptance:** `python3 scripts/audit-route-geometry.py` → `story_fail: 0`  
Then: `python3 scripts/grok-geometry/update_seal_geometry_gate.py --apply` + `update_seal_hashes.py` + deploy.

**Key files:**

- `handoff/partner-map-model/GEOMETRY-TRIAGE.json` — full fail list + `priority_fix`
- `handoff/partner-map-model/GEOMETRY-STORY-HOLD.json` — severe holds
- `scripts/grok-geometry/mint_story_channels.py`
- `scripts/grok-geometry/mint_hand_waypoints.py`
- `scripts/grok-geometry/channel_solver.py` (`HAND_WAYPOINTS`)
- `scripts/grok-geometry/regional_land_masks.py`

---

### P1 — South Africa mesh

**Status:** 10 routes built; **4/10 pass QA** with regional masks.

| route_id | land_km | pass | notes |
|----------|---------|------|-------|
| rn-d1fb7d05ab6c | 0.0 | ✓ | V&A ↔ Robben |
| rn-8d68a59f5c77 | 0.0 | ✓ | |
| rn-a3db2399bad4 | 0.0 | ✓ | |
| rn-dd192c008158 | 0.0 | ✓ | |
| rn-373fbf71fa7d | 0.39 | ✗ | peninsula arc |
| rn-12ad23baa2fd | 0.20 | ✗ | |
| rn-9014901e2f96 | 0.67 | ✗ | |
| rn-5e0c1a18bf27 | 1.38 | ✗ | |
| rn-75e6606e3a52 | 4.28 | ✗ | |
| rn-242284fa4884 | 22.14 | ✗ | Hout Bay ↔ Simon's Town arc |

**Still to do:**

1. Tune Cape Peninsula waypoints in `HAND_WAYPOINTS` (`channel_solver.py` / `mint_hand_waypoints.py`)
2. Re-run `python3 scripts/grok-geometry/mint_bolt_south_africa_geometry.py --apply`
3. Bind `route_id` on `data-clean/partners/bolt.json` south-africa journeys (currently `null`)
4. Refresh `grok-routing-output/bolt-south-africa-seal-report.json`

**Key files:**

- `scripts/grok-geometry/mint_bolt_south_africa_geometry.py`
- `grok-routing-output/bolt-south-africa-seal-report.json`
- `data-clean/partners/bolt.json` (south-africa phase)

---

### P2 — Croatia depth

**Status:** +14 routes via `route_kept_markets.py` (16 → ~30 scoped on hub).  
15 corridors in model; not all bound with geometry.

**Commands:**

```bash
python3 scripts/grok-bolt-yango/route_kept_markets.py --markets bolt-croatia
python3 scripts/grok-geometry/mint_story_channels.py --apply --route <failing-rids>
```

**Key files:**

- `scripts/grok-bolt-yango/route_kept_markets.py`
- `data-clean/partners/bolt.json` (croatia)
- Dalmatia mask already in `regional_land_masks.py`

---

### P3 — Phase 0: Map footprint / regressions

**Gate:** Bolt hub build shows rollout ≥ 80 cities (not ~56).

| Task | Acceptance |
|------|------------|
| 0.1 Restore `network_footprint` + `_map_scope` from pre-marine-tam backup / PR #81–#86 | `materialize_partner_map_scope.py` bolt → 47+ footprint cities; hub ingest matches |
| 0.2 Cyprus | `limassol-cyprus`, `larnaca-cyprus` visible on Bolt hub, no sub-proposal card |
| 0.3 Israel | `bolt-israel` held → render; `tel-aviv-israel` pin visible |
| 0.4 Auckland | `auckland-new-zealand` pin + footprint row |

**Current:** `network_footprint` = 50 rows, `_map_scope.cluster_city_ids` = 38 cities.

**Key files:**

- `data-clean/partners/bolt.json`
- `scripts/materialize_partner_map_scope.py` (if present)
- `seal-scope/` / `bolt.json` backups from PR #81–#86 era

---

### P4 — Phase 2: Corridor minting waves (partial)

| Wave | Market | Status |
|------|--------|--------|
| 2A | bolt-estonia (Tallinn↔Helsinki, etc.) | Not done |
| 2A | grab-thailand (17 unbound intra-island + Phuket↔Krabi) | Partial |
| 2A | bolt-east-africa (8 culled corridors) | 3/11; need `mint_bolt_east_africa_geometry.py` v2 |
| 2A | bolt-south-africa | See P1 |
| 2B | bolt-greece (15 corridors, ~2 bound) | Partial |
| 2B | bolt-croatia | See P2 |
| 2B | Other proposal markets | `route_kept_markets.py` + `route_bolt_yango_markets.py --refresh-existing` |

**Key files:**

- `grok-routing-output/corridors.json` (or `DEFAULT_CORRIDORS`)
- `scripts/grok-geometry/mint_bolt_east_africa_geometry.py`
- `scripts/grok-bucketC-thailand/route_bucketC_thailand.py`
- `scripts/grok-bolt-yango/route_kept_markets.py`

---

### P5 — Economics (not started)

Phase 5 reseal per original closure plan. Run after routing waves stabilize.

**Key files:**

- `scripts/grok-econ-reseal/`
- `data-clean/economics_by_route_id.json`

---

## Key scripts & commands

```bash
cd /Users/jaideep/navier-atlas

# Story QA audit (~2 min)
python3 scripts/audit-route-geometry.py

# Channel mint tiers
python3 scripts/grok-geometry/mint_story_channels.py --apply --nudge-only --max-land-km 5
python3 scripts/grok-geometry/mint_story_channels.py --apply --channel-only --min-land-km 1 --max-land-km 15
python3 scripts/grok-geometry/mint_hand_waypoints.py --apply --min-land-km 0.05 --max-land-km 20

# South Africa / Croatia
python3 scripts/grok-geometry/mint_bolt_south_africa_geometry.py --apply
python3 scripts/grok-bolt-yango/route_kept_markets.py --markets bolt-croatia

# Seal + deploy (after changes)
python3 scripts/grok-geometry/update_seal_geometry_gate.py --apply
python3 scripts/grok-econ-reseal/update_seal_hashes.py
RELEASE=1 BUILD_PROFILE=public ./scripts/deploy.sh
```

---

## Dirty / uncommitted at park time

Regenerated audit artifacts (safe to discard or commit on resume):

```
 M grok-routing-output/route-city-id-backfill-report.json
 M handoff/partner-map-model/GEOMETRY-AUDIT.json
 M handoff/partner-map-model/GEOMETRY-TRIAGE.json
 M handoff/partner-map-model/PARTNER-ROUTE-LINKAGE-AUDIT.json
 M handoff/partner-map-model/geometry-channel-mint-report.json
 M handoff/partner-map-model/geometry-hand-waypoints-report.json
```

Core geometry code and `ROUTES.json` are clean on `e1f69dcf`.

---

## Related handoff docs

- `handoff/partner-map-model/HANDOFF.md` — partner footprint / registry reconciliation
- `grok-routing-output/HANDOFF-FOR-TASKLET.md` — Tasklet seal lane
- Original closure plan metrics table (in conversation / transcript)

---

*Parked by Grok — resume with the prompt at the top of this file.*