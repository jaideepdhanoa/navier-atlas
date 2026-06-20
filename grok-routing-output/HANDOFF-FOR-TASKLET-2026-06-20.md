# Grok → Tasklet Handoff — Post-#79as economics + geometry backlog

**Date:** 2026-06-20  
**From:** Grok lane (Jaideep)  
**To:** Tasklet  
**Prod:** https://navier-atlas.vercel.app  
**Repo:** `navier-atlas` `main`

---

## Headline

Grok ran three lanes today (`#79ar-pending-uae`, `#79aq-bp-seal`, `#79as-bp-pair-bind`). Gold is deployed. **151 corridors still pending economics** — most are structural, but **~19 are actionable** and blocked on Tasklet inputs in `finance/model/corridors.json` and boarding-point research.

| Surface | Count |
|---------|-------|
| Economics pinned | **351** |
| Economics pending | **151** (19 actionable, 132 structural holds) |
| Raw pin rate | **~69.9%** |
| Actionable pin rate | **~94.9%** |
| Routes | **~7,400** |
| POIs | **~12,722** |

---

## What Grok already did (do not redo)

| Lane | What shipped |
|------|----------------|
| `#79ar-pending-uae` | Minted 197 `gcn-*` UAE routes; rebuilt economics sidecar; spliced `subproposals-enriched-2026-06-20.json` |
| `#79aq-bp-seal` | Sealed 50/51 new BPs from `bp-seal-2026-06-20.zip`; route-sealed Spain/Sweden/Portugal/Finland/Estonia/Abidjan/Morocco (+54 routes) |
| `#79as-bp-pair-bind` | Minted 458 routes (Grab SEA binds + Turkey + intra-city mesh) |

**Changelogs:** `data-clean/CHANGELOG-FOR-CLAUDE-2026-06-20-{pending-uae,bp-seal,bp-pair-bind}.md`

---

## Division of labor (locked)

| Work | Owner |
|------|-------|
| `finance/model/corridors.json` — corridor registry, node IDs, `route_id` pins, `endpoint_boarding_points`, `aspirational` flags | **Tasklet** |
| Boarding-point research + `boarding-points/*.json` handoffs | **Tasklet** |
| Demand/fare records (`L3_locals`), agg refresh, growth_case cascade | **Tasklet** |
| Partner pitch copy (`partners/*.json`, sub-proposal narratives) | **Tasklet** |
| Mint `gcn-*` / `rn-*` into `ROUTES.json` | **Grok** |
| Seal BPs from handoff zips into `FEATURES_BY_TYPE.json` | **Grok** |
| Rebuild `economics_by_route_id.json` (ID-based resolver — do not loosen) | **Grok** |
| Partner hub splice/bind (`bolt.json`, `yango.json`) | **Grok** |
| Reseal, gates, deploy | **Grok** (geometry) / **Claude** (render deploy) |

**Rule:** Tasklet never edits `data-clean/ROUTES.json` or `FEATURES_BY_TYPE.json` directly in git. Ship inputs; Grok applies.

---

## Read first (in this order)

1. **`data-clean/PENDING-ECONOMICS-TRIAGE.json`** — authoritative backlog audit (Grok-generated; re-run after corridor edits)
2. **`_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json`** — copy of finance corridors Grok reads today (54 markets / 747 corridors). **Your master is `finance/model/corridors.json`** — edit there, ship back.
3. **`_ingest/econ-reseal-2026-06-19/econ-reseal/README.md`** + **`docs/GROK-PROMPT.md`** — economics reseal contract
4. **`_ingest/bp-seal-2026-06-20/README.md`** + **`docs/GROK-PROMPT.md`** — BP-seal mandate (partially applied by Grok)
5. **`_ingest/bp-seal-2026-06-20/inputs/subproposals-enriched-2026-06-20.json`** — 22 active Bolt/Yango sub-proposal pages (geometry spliced; narrative still Tasklet)
6. **Changelogs:** `data-clean/CHANGELOG-FOR-CLAUDE-2026-06-20-*.md`
7. **`DIVISION-OF-LABOR.md`** — long-term RACI
8. **`docs/BRAND-VOICE-FOR-TASKLET.md`** — optional voice polish when touching copy

---

## Economics resolver contract (do not break)

Grok's `build_economics_sidecar.py` resolves corridors **ID-only**:

1. `route_id` in corridor row **and** present in gold `ROUTES.json` → pin
2. Else exact unordered match on `(from_node_id, to_node_id)` in gold → pin
3. Else BP-pair match when endpoints resolve to distinct `bp-*` IDs
4. `from_node_id == to_node_id` with no route → **`aspirational_intra_city`** (structural, not a failure)
5. `aspirational: true` → **`aspirational_declared`** (intentional hold)

**Implication:** pinning economics requires either a declared `route_id` Grok can mint, or **distinct endpoint node IDs / `endpoint_boarding_points` that map to real sealed BPs**.

---

## Pending backlog — what Tasklet fixes

### Sub-bucket summary

| Sub-bucket | Count | Tasklet action |
|------------|-------|----------------|
| `same_node_no_route_id` | 55 | Add distinct BPs or `endpoint_boarding_points`; fix node chips |
| `one_bp` | 74 | Research + seal **second endpoint BP** (37 in **active** markets) |
| `gcn_declared_not_in_gold` | 18 | Add `endpoint_boarding_points` / BP labels → Grok mints declared `gcn-*` |
| `intentional_hold` | 2 | Set `aspirational: true`; do not chase pin |
| `no_bp` | 1 | Egypt Hurghada→El Gouna — fix node IDs + BPs |
| `other_actionable` | 1 | Tangier→Tarifa — hold (cross-strait excluded) |

### Pruned markets — ignore (proposal pages retired)

`bolt-cyprus`, `bolt-israel`, `bolt-lebanon`, `bolt-romania`, `yango-senegal`, `yango-mozambique`, `yango-tunisia`, `yango-pakistan`, `yango-caspian-az`, `yango-caspian-kz`, `yango-israel`

Geometry/cities may linger; do not resurrect sub-proposal pages or chase economics in these markets.

---

## Priority queue

### P0 — `corridors.json` backfill (unblocks Grok minting)

**File to edit:** `finance/model/corridors.json`  
**Ship:** full file or JSON-patch delta in handoff zip

#### A. Egypt — broken node IDs (why Grok minted 0 Egypt routes)

Gold cities:

- `hurghada-el-gouna-egypt` (combined Red Sea city)
- `sharm-el-sheikh-egypt`
- `cairo-egypt`
- `redsea-egypt`

Corridors currently reference **`hurghada-egypt` / `el-gouna-egypt`** — **these do not exist in gold**.

**Fix for `Hurghada -> El Gouna` (the `no_bp` row):**

```json
{
  "from_node_id": "hurghada-el-gouna-egypt",
  "to_node_id": "hurghada-el-gouna-egypt",
  "endpoint_boarding_points": {
    "from": "Hurghada Marina",
    "to": "Abu Tig Marina, El Gouna"
  }
}
```

BP research exists in `_ingest/bp-seal-2026-06-20/boarding-points/hurghada-el-gouna-egypt.json` and `el-gouna-egypt-boarding-points.json` — align label strings to those files.

**Fix all 16 `same_node_no_route_id` Egypt rows** the same way: keep city chip, add `endpoint_boarding_points` with human labels Grok can match to sealed `bp-*`.

**Intentional hold — do not pin:**

- `Hurghada / El Gouna -> Sharm El Sheikh` — already `aspirational: true` + `gcn-73d7e2f19c-bolt`
- `yango-egypt` copy should mirror with `aspirational: true`

**Actionable mint after fix:**

- `yango-egypt` `Hurghada -> El Gouna` has `route_id: gcn-6f2754b63b-yango` — pins once endpoints resolve

#### B. Grab Bali + Phuket — 7 `gcn-*` rows missing gold geometry

| Market | Corridor | `route_id` |
|--------|----------|------------|
| bali | Pantai Laguna (Ancol) ↔ itself | `gcn-1998d7cd48-shared` |
| bali | Batavia Marina ↔ itself | `gcn-5eba638e49-shared` |
| bali | Marina Ancol → Thousand Islands inner ring | `gcn-54274fe1cb-shared` |
| bali | Marina Ancol → Thousand Islands outer ring | `gcn-a655e97b56-shared` |
| bali | Inner ring → outer ring | `gcn-5058e45aad-shared` |
| phuket | ICONSIAM Pier ↔ itself | `gcn-334cc44485-shared` |
| phuket | Sathorn Pier → Phra Arthit Pier | `gcn-e299366426-shared` |

Add `endpoint_boarding_points` (or split node chips) using research in `_ingest/bp-seal-2026-06-20/boarding-points/bali.json` and `phuket.json`.

#### C. Qatar — 1 row

`Doha -> Al Wakrah Marina` — `gcn-e2b0929d6f-qatar`, has `to_bp: bp-b7acff0504` but no `from_bp`. Add from-endpoint BP label or `endpoint_boarding_points.from`.

#### D. KSA commercial — 8 rows (bolt + yango)

`bolt-ksa-commercial` / `yango-ksa-commercial` — NEOM/Sindalah, AMAALA, Shura Island resort hops. Add `endpoint_boarding_points` tied to sealed Red Sea BPs.

**Node crosswalk (already applied in Grok routing):**

- `neom-ksa` → `neom-sindalah-ksa`
- `amaala-ksa` → `red-sea-global-ksa`

See `grok-routing-output/NODE-ID-CROSSWALK-2026-06-19.json`.

---

### P0 — Boarding-point handoffs (37 active `one_bp` corridors)

**Pattern:** corridor has one sealed `bp-*` but needs a second endpoint. Research the missing pier, add to `boarding-points/<city>.json`, include in handoff zip.

**Active markets (ignore pruned):**

| Market | `one_bp` count | Notes |
|--------|----------------|-------|
| `yango-lagos` | 7 | Lagoon hops — second pier per corridor |
| `bolt-croatia` | 5 | Hvar/Korčula splits |
| `singapore` | 3 | Clarke Quay, Marina Bay, Sentosa — need distinct to-BPs |
| `bolt-italy` | 3 | Lake Como / Costa Smeralda |
| `bolt-ireland` | 3 | |
| `bolt-greece` | 2 | Saronic — may need `endpoint_boarding_points` not second city |
| `bolt-portugal` | 2 | |
| `yango-turkey` | 2 | Kadıköy↔Kabataş, Kabataş↔Büyükada |
| `yango-cote-divoire` | 2 | |
| + 8 markets with 1 each | bali, phuket, vietnam, cambodia, bolt-estonia, bolt-sweden, bolt-spain, yango-morocco |

**Handoff format:** same as `bp-seal-2026-06-20` — `boarding-points/*.json` + manifest listing new BPs.

---

### P1 — Turkey node-chip cleanup

**Problem:** All `yango-turkey` (and bolt turkey) corridors use `from_node_id: istanbul-turkey` / `to_node_id: istanbul-turkey` even for **Bodrum, Antalya, Çeşme** legs.

Grok added a routing workaround (`_corridor_city_ids` expansion) but economics still keys on corridor node IDs.

**Fix:** Per-city node chips in `corridors.json`:

- `istanbul-turkey` — Bosphorus / Princes' Islands
- `bodrum-turkey` — Bodrum peninsula
- `antalya-turkey` — Antalya coast
- `cesme-turkey` — Çeşme / Izmir

BP files exist: `boarding-points/antalya.json`, `cesme-izmir.json`, etc.

---

### P1 — Intentional holds (flag, don't fix)

Set `aspirational: true` and stop chasing pin:

| Market | Corridor | Reason |
|--------|----------|--------|
| `taiwan` | Budai (Chiayi) → Magong (Penghu) | `aspirational_declared` |
| `bolt-egypt` / `yango-egypt` | Hurghada/El Gouna → Sharm | No active ferry; long cross-gulf |
| `yango-morocco` | Tangier Marina → Tarifa | `no_endpoints` — cross-strait excluded |
| `bolt-spain` | Tarifa ↔ Tangier, L'Estartit ↔ Medes | Already held in partner journeys |

---

### P2 — Sub-proposal narrative enrichment

**File:** `_ingest/bp-seal-2026-06-20/inputs/subproposals-enriched-2026-06-20.json`

Grok spliced **14 bolt + 8 yango** active market pages into `data-clean/partners/{bolt,yango}.json`. Structure + `anchor_cities` + `journeys_unlocked` refs are done.

**Tasklet job:** polish prose fields (`summary`, `why_now`, `hero`, `proof_points`, `objections`, `the_ask`, `close`) per `docs/BRAND-VOICE-FOR-TASKLET.md`. Do not change numbers/facts without re-running aggs.

**Partner binding gaps** (Grok sweeps after journey refs stabilize):

- Bolt: **163 linked / ~47 unlinked** featured+journey refs
- Yango: **90 linked / ~26 unlinked**

---

### P3 — Agg refresh (only if labels/node IDs change)

If you rename corridor `from`/`to` labels or split markets, re-run aggregate → growth_case for affected partners:

- Source aggs: `_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/aggs/agg-<partner>.json`
- Partners with fresh economics: grab, careem, bolt, yango, qatar, jih-global, constance, four-seasons
- **Held:** saudi-pif, red-sea-global (do not reseal economics yet)

---

## Corridor row shape (reference)

```json
{
  "route_id": null,
  "from": "Human label A",
  "to": "Human label B",
  "from_node_id": "city-chip-in-gold",
  "to_node_id": "city-chip-in-gold",
  "endpoint_boarding_points": {
    "from": "Pier name matching boarding-points research",
    "to": "Other pier name"
  },
  "country": "Egypt",
  "aspirational": false,
  "distance_nm": 14.0,
  "vessel": "Pioneer II",
  "archetype": "tourism",
  "L3_locals": { "...": "unchanged unless re-anchoring fare/demand" }
}
```

**After Grok mints a route:** backfill `route_id` on the matching corridor row so future sidecar rebuilds stay deterministic.

---

## What Tasklet must NOT do

- Do not resurrect the **11 pruned** Bolt/Yango markets listed above
- Do not edit `data-clean/ROUTES.json` or `FEATURES_BY_TYPE.json` in git
- Do not loosen the economics resolver (no fuzzy label matching)
- Do not remove cities/clusters when pruning — only proposal pages go away
- Do not re-seal held partners (`saudi-pif`, `red-sea-global`) until forward-SAM reconciliation lands

---

## Deliverable package (what to ship Grok)

Zip to `Downloads/` (name pattern: `tasklet-handoff-2026-06-20.zip`):

```
tasklet-handoff-2026-06-20/
├── README.md                    # what changed, corridor count delta, BP count
├── corridors.json               # full finance/model/corridors.json (or PATCH manifest)
├── boarding-points/             # new/updated BP files only
│   └── <city>-boarding-points.json
├── inputs/
│   └── BP-COVERAGE-NEW-<date>.json   # if minting new BPs
├── aggs/                        # only if you re-ran aggregates
│   └── agg-<partner>.json
└── partners/                    # optional narrative deltas
    └── subproposals-enriched-<date>.json
```

Post to `#tasklet-jaideep` with a one-line summary: *"N corridor fixes, M new BPs, K markets touched — ready for Grok ingest."*

Grok ingest lane: drop zip into `_ingest/`, run the appropriate orchestrator, rebuild sidecar, deploy.

---

## Acceptance (Grok verifies after ingest)

- [ ] `PENDING-ECONOMICS-TRIAGE.json` actionable pending **≤ 5** (structural holds OK)
- [ ] Egypt: `Hurghada -> El Gouna` pins; intra-city Red Sea + Nile corridors have `endpoint_boarding_points`
- [ ] Bali/Phuket 7 `gcn-*` rows mint into gold
- [ ] Qatar `Doha -> Al Wakrah` pins
- [ ] Turkey corridors use per-city node chips (not all `istanbul-turkey`)
- [ ] 0 silent BP drops on any new handoff
- [ ] Economics pin rate **> 75% raw** / **> 97% actionable**
- [ ] Partner binding: bolt **> 180 linked**, yango **> 100 linked**

---

## Suggested work order

1. Fix Egypt node IDs + `endpoint_boarding_points` (biggest zero-route market)
2. Add Bali/Phuket/Qatar `endpoint_boarding_points` for declared `gcn-*` rows
3. Ship second-endpoint BP research for top `one_bp` markets (Lagos, Croatia, Singapore, Italy)
4. Turkey node-chip split
5. Narrative pass on 22 active sub-proposals
6. KSA commercial resort hops (lower urgency — held economics partners)

---

## Related artifacts in repo

| Path | Role |
|------|------|
| `data-clean/PENDING-ECONOMICS-TRIAGE.json` | Actionable vs structural pending audit |
| `data-clean/economics_by_route_id.json` | Route-keyed economics sidecar (Grok-maintained) |
| `_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json` | Finance corridors (Grok ingest copy) |
| `_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/aggs/agg-*.json` | Economics aggregate rows |
| `_ingest/bp-seal-2026-06-20/` | BP handoff (boarding-points, BP-COVERAGE-NEW) |
| `scripts/grok-econ-reseal/triage_pending_economics.py` | Re-run triage after corridor edits |
| `scripts/grok-econ-reseal/run_bp_pair_bind_lane.sh` | Grok orchestrator for BP-pair mint lane |
| `scripts/grok-bolt-yango/run_bp_seal_lane.sh` | Grok orchestrator for BP-seal lane |