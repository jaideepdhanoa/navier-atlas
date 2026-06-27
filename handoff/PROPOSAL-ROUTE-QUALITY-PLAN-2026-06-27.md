# Proposal route quality + UAE channel routing — plan (2026-06-27)

**Status:** PLAN APPROVED (2026-06-27) — Phase A audit + phase-map fix in progress  
**Trigger:** Careem proposal (`/careem`) — ~4/5 journeys_unlocked show wrong or distant BPs; UAE map still has land-crossing spaghetti  
**Principle:** **Reduce count, raise bar** — null beats wrong; fewer routes that are exact, relevant, and geometry-verified

---

## Locked decisions (Jaideep, 2026-06-27)

| # | Question | Decision |
|---|----------|----------|
| 1 | **Mesh on proposal pages** | **No mesh at any opacity.** Phase map shows **cumulative featured routes through the active phase only** (Phase 2 = Phase 1 + 2 routes, not the full network). Current behavior is inconsistent — **P0 bug**. |
| 2 | **Cross-emirate legs** (Dubai↔Abu Dhabi) | **Allowed** in `journeys_unlocked` when geometry and narrative fit. |
| 3 | **RAK / east coast in Careem Phase 1** | Not a global exclusion — the issue is **irrelevant routes featured outside the current phase narrative** (e.g. RAK fisherman jetty under "Dubai beachhead"). Phase-narrative fit is a **quality gate**, not a geography ban. |
| 4 | **Channel graph authorship** | **Grok only** — draft centerline graphs from satellite imagery, self-validate (land mask + visual QA). **No Tasklet** in the channel-graph loop. |

---

## Problem statement

Three layers currently fail the credibility test:

1. **Narrative layer** (`journeys_unlocked`, phase copy) promises corridors that read well but bind to weak geometry or irrelevant BPs.
2. **Proposal layer** (`featured_routes`, phased routes, signature routes) auto-links via `relink_partner_journeys.py` with fuzzy label/distance matching — passes linkage audit (route_id exists) but not **human exactness**.
3. **Map layer** (partner-scoped `story_route_count` + mesh) shows dense spaghetti; UAE in particular still cuts over Palm fronds, Deira Island, marina basins, and Abu Dhabi reclamation.

The existing gates (`PARTNER-ROUTE-LINKAGE-AUDIT`, `audit_partner_page_qa.py`) check **existence and scope**, not **endpoint plausibility, narrative fit, or visual geometry**.

---

## Scope surfaces (audit inventory)

| Surface | Source JSON | Renders as | Current gate |
|---------|-------------|------------|--------------|
| `journeys_unlocked` | `data-clean/partners/{id}.json` | Hero "journeys we unlock" | Link ratio only |
| `phases[].featured_routes` | same | Phase carousel cards | route_id ∈ ROUTES.json |
| `markets[].journeys_unlocked` | hub partners | Per-market unlocks | scoped city match |
| `signature_routes` | `cluster_briefs/*.json` | Brief-derived gold | story_registry |
| `story_routes` / map scope | build + `_map_scope` | Lines on partner map | geometry advisory |
| Mesh routes | ROUTES.json (non-story) | ~~Background density~~ **hidden on proposal pages** | 3035 fails (deferred) |

**Audit order:** Reference partners first (Careem, Noon, Grab, Rapido, Bolt UAE), then all MENA/super-app, then hub hospitality.

---

## Phase A — Diagnostic audit (read-only, ~1 session)

### A1. Per-partner proposal fidelity report

Extend `scripts/audit_partner_page_qa.py` (or sibling `audit_proposal_fidelity.py`) with **new checks**:

| Check | Fail example (Careem) |
|-------|----------------------|
| **BP binding** | `from`/`to` labels ≠ actual route endpoint BPs |
| **Distance honesty** | journey `distance_nm: 0.3` vs featured `12.4` for same corridor |
| **Phase-narrative fit** | Featured route in Phase N not tied to that phase's story (e.g. RAK→Ghallilah under "Dubai beachhead") |
| **Cross-emirate sanity** | 57nm Abu Dhabi↔Dubai labeled as everyday commerce leg — allowed if geometry perfect + phase-appropriate |
| **Geometry preview** | route `interior_land_km` > 0.4 or crosses known no-cross polygon |
| **Inheritance debt** | `_inherit_source: grok/normalize/noon` without re-validation |

Output: `handoff/partner-map-model/PROPOSAL-FIDELITY-AUDIT.json` + per-partner `-{id}.md` verdict (PASS / TRIM / REWRITE / HOLD-NULL).

### A2. Careem smoke deep-dive (user-reported)

Manually trace all 6 `journeys_unlocked` + Phase 1 `featured_routes`:

- Map each `route_id` → `ROUTES.json` geometry → endpoint `bp-*` coords → haversine vs labels
- Flag: RAK→Ghallilah, cross-city bolt-inherited legs, distance mismatches
- Deliver: **recommended keep set** (target 3–4 journeys max for Careem Phase 1)

### A3. Dependency matrix (revised)

| Question | Owner |
|----------|-------|
| Phase-narrative fit for featured_routes | **Grok** — audit + trim; null beats wrong |
| UAE channel graphs (Palm, Creek, Marina, AD islands, Deira) | **Grok** — satellite draft + self-validate |
| BP endpoint grounding | Grok + `CORRIDOR-ENDPOINT-GROUNDING` |
| Drop inherited `grok/normalize/noon` links | **Grok** — re-ground or null |
| Palm frond polygons (Tier 3) | Grok drafts; Tasklet optional for commercial-now sign-off only |

---

## Phase B — Quality bar + reduction policy (design, no data change)

### B1. Tier taxonomy (proposal-visible routes only)

| Tier | Criteria | UI treatment |
|------|----------|--------------|
| **S — Signature** | Tasklet-sealed BP pair + hand/channel geometry + economics grounded + narrative match | journeys_unlocked + featured + map highlight |
| **A — Featured** | Sealed endpoints, geometry pass, phase-scoped | phase carousel only |
| **B — Map context** | Geometry pass, lower traffic | map only, no proposal copy |
| **H — Hold null** | Fails any gate | explicit "roadmap" or omit |

**Default cap:** ≤4 `journeys_unlocked`, ≤3 `featured_routes` per active phase, ≤6 signature routes per cluster brief.

### B2. Binding policy change

Replace fuzzy auto-win in `relink_partner_journeys.py` for proposal surfaces:

1. **Require endpoint grounding** — `from_node_id`/`to_node_id` must be `bp-*` in `CORRIDOR-ENDPOINT-GROUNDING` or explicit brief signature.
2. **Require geometry tier** — story route must pass regional mask OR `hand_waypoints` seal.
3. **Kill inheritance** — drop `_inherit_source: grok/normalize/noon` links unless re-grounded.
4. **Null beats wrong** — empty carousel beats misleading line on map.

### B3. Deploy gate (future)

Add preflight **§3.7 proposal fidelity** — fail deploy if reference partners (Careem, Noon, Grab) have any S-tier journey failing BP exactness.

---

## Phase C — UAE channel routing methodology (design)

### Current toolchain

| Tool | What it does | UAE gap |
|------|--------------|---------|
| `global_land_mask` | Coarse ocean mask | Misses creeks, marina basins, fronds |
| `channel_solver.py` | A* on `uae_gulf_land_v2` grid + `HAND_WAYPOINTS` | ~dozen hand pairs; Palm has 2 entries |
| OVERLAY-ONLY bbox detour (#79ah) | Inserts seaward corner waypoints | Axis-aligned; intra-Palm still fails |
| `regional_land_masks.py` | Extra water bodies | UAE creek/marina not fine enough |
| `route_water_allowlist.json` | Allowlist land-crossing | Masks problem, doesn't fix geometry |

### Recommended methodology (tiered)

**Tier 1 — Channel graphs (high-value sub-areas)**  
Author **navigable centerline graphs** per sub-area:

- Palm Jumeirah trunk + frond mouths
- Dubai Marina / JBR / Harbour basin
- Dubai Creek + Business Bay connector
- Abu Dhabi: Yas ↔ Saadiyat ↔ Lulu ↔ Reem ↔ Hudayriyat
- Deira Islands / Palm Deira apron

Format: GeoJSON `LineString` networks in `data-clean/channel_graphs/uae-{area}.geojson` + solver snaps A→B onto graph.

**Tier 2 — Expand `HAND_WAYPOINTS` in `channel_solver.py`**  
Short-term: Grok pair-list for ~30–50 sealed UAE commercial corridors; each gets 3–8 waypoints authored from satellite/OSM + self-validation.

**Tier 3 — Frond-resolution polygons**  
Replace Palm/Deira axis bboxes with Grok-authored frond polygons (carry-forward from #79ah known limitation).

**Tier 4 — Marina apron tolerance**  
Extend LB-224 marina apron rule (0.12 km) consistently in proposal gate, not just routing.

### Tooling comparison

| Approach | Pros | Cons |
|----------|------|------|
| More bbox detours | Fast | Still spaghetti on complex shapes |
| Hand waypoints only | Precise per corridor | Doesn't scale to 5000 routes |
| **Channel graphs** | Scales within sub-areas; visually correct | Upfront authorship cost |
| Full OSM waterway routing | Comprehensive | Gulf OSM incomplete; maintenance |
| Hide mesh, show story only | Instant credibility win | Doesn't fix proposal cards |

**Recommendation:** **Channel graphs + zero mesh on proposal pages** — proposal map shows cumulative phase featured routes only; capillary mesh never rendered (not even dimmed). End-state chapter may show backbone/context, never mesh.

---

## Phase D — Execution sequence

1. **Fix phase-map cumulative scoping** (P0 bug) — hide mesh; highlight routes through active phase only  
2. Run Phase A audit → Careem deep-dive + per-partner fidelity report  
3. Careem pilot: trim Phase 1 to 3–4 phase-aligned journeys; drop narrative-misfit featured routes (e.g. RAK in beachhead)  
4. UAE channel graph v1: Palm + Creek + Marina (Grok satellite draft + self-validate)  
5. Roll binding policy + phase-narrative gate to Noon/Grab/Rapido reference set  
6. Add preflight §3.7 proposal fidelity  
7. Deploy + visual QA on `/careem`, `/noon`, `/dubai-rta`  
8. FE-2 dedup + mesh geometry (only after proposal surfaces credible)

---

## Success metrics

| Metric | Current (est.) | Target |
|--------|----------------|--------|
| Careem journeys_unlocked passing BP exactness | ~1/6 | 4/4 (after trim) |
| UAE story routes crossing no-cross polygons | unknown | 0 visible on proposal map |
| Reference partner proposal fidelity | not gated | 100% S-tier pass |
| Partner map route count (Careem) | 126 story | ≤40 story + ≤20 featured |

---

*Decisions locked 2026-06-27 — see table at top*