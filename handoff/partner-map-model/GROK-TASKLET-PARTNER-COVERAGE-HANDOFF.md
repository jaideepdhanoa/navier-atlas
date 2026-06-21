# Grok → Tasklet partner coverage handoff

**Date:** 2026-06-21 (Waves 0–9 complete)  
**Lane:** `scripts/grok-econ-reseal/run_partner_coverage_lane.sh`  
**Rollup:** `handoff/partner-map-model/partner-coverage-review-rollup.json`

---

## Final gate status (after Wave 9)

| Gate | After Waves 7–8 | After Wave 9 | Target | Status |
|------|-----------------|--------------|--------|--------|
| Page QA FAIL | 0 | **0** | 0 | ✅ |
| Page QA PASS | 38 | **49** | — | +11 |
| Page QA PASS_WITH_FLAGS (all) | 16 | **5** | — | −11 |
| Page QA PASS_WITH_FLAGS (hospitality) | 3 | **3** | ≤ 5 | ✅ |
| Page QA PASS_WITH_FLAGS (hub + authority) | 12 | **2** | split | −10 |
| Page QA flags — featured geometry | — | **2** | — | kakao, lyft |
| Page QA flags — journey only | — | **3** | — | aman, six-senses, discovery-land |
| Spine FAIL | 0 | **0** | 0 | ✅ |
| Spine PASS | 44 | **50** | — | +6 |
| Spine PASS_WITH_FLAGS | 10 | **4** | ≤ 10 | ✅ (4 remaining) |
| Geometry gap partners | 9 | **6** | ≤ 8 | ✅ |
| Thin-map partners | 0 | **0** | 0 | ✅ |
| Tasklet bind actions | 0 | **0** | 0 | ✅ |

**Sealed references:** RAKTA 46/46 featured geom; Bahrain MOTC **8/8** featured geom (phase-1 domestic stub added — narrative polish only).

---

## What Grok shipped in Wave 9

### 9A — Quick geometry wins

| Script | Partners | Result |
|--------|----------|--------|
| `promote_authority_featured_route_ids.py` | hong-kong, norway-fjords | HK +5 archetype, +2 route_ids promote |
| `relink_hub_market_featured.py` | indrive, kakao, lyft, uber | indrive +6 featured; kakao +5 featured; lyft +21 featured; uber +24 journeys |
| `bind_velana_hospitality_corridors.py` | soneva | Velana leg already bound |
| `relink_partner_journeys.py` | hub + authority subset | Cleared indrive, uber from flags |

**Clears from flags:** indrive, uber, didi, bahrain-motc, hong-kong, hawaii, bc-ferries, wsf, nyc-ferry, cabify.

### 9B — North America ferry repair

Extended `repair_ferry_flagship_corridors.py` for **bc-ferries**, **wsf**, **hawaii**, **nyc-ferry** (city brief / cluster / archetype signatures). Fixed phase featured distribution (clears stale HK/Lyft contamination on phase 3).

| Partner | Journeys geom | Featured geom |
|---------|---------------|---------------|
| bc-ferries | 22/22 | sealed |
| wsf | 31/31 | sealed |
| hawaii | 3/3 | 3/3 featured |
| nyc-ferry | 21/21 | sealed |
| norway-fjords | **4/4** | **4/4** |

**Lane note:** Do not full-relink norway-fjords after repair — scoped relink re-contaminates phase featured. Lane re-runs repair + promote post-relink.

### 9D — Narrative + phase stubs

| Script | Result |
|--------|--------|
| `fill_hub_phase_narratives.py` | didi +4, cabify +4 phase stubs |
| `stub_authority_empty_phase_featured.py` | bahrain-motc phase-1 domestic stub (`rn-063a88bc18d1`) |

### Rollup splits (new)

`audit_partner_coverage_rollup.py` now reports:
- `qa_pass_with_flags_featured_geometry`
- `qa_pass_with_flags_journey_only`
- `qa_pass_with_flags_cosmetic`
- `spine_pass_with_flags`

---

## Tasklet action queue (Wave 9E — your turn)

### P0 — Hospitality mint sign-off (only path for 3 journey flags + 4 geometry gaps)

| Partner | Featured geom | Journey geom | Action |
|---------|---------------|--------------|--------|
| **discovery-land** | **0/25** | 2/14 | Bahamas flagship corridor mint queue (`nassau-bahamas` / cluster brief) — **blocks geometry gate tail** |
| **aman** | 8/42 | 7/28 | Pick top **5** property flagship corridors; Grok will mirror to journeys after mint |
| **six-senses** | 6/42 | 5/28 | Same — top 5 property corridors per region |

After mint approval, Grok runs `bind_hospitality_flagship_corridors.py` + journey relink. **Do not** restructure `phases[]` or proposal class.

### P1 — Hub featured continuation (2 partners, Grok can continue after your market picks)

| Partner | Featured geom | Need | Notes |
|---------|---------------|------|-------|
| **lyft** | 44/56 (79%) | +4 to 85% | Market picks for remaining US metros if auto-bind misses |
| **kakao-mobility** | 20/26 (77%) | +3 to 85% | Jeju + Seoul Han River legs — confirm flagship picks |

Grok can run another `relink_hub_market_featured.py` pass once Tasklet confirms market priority order.

### P2 — Narrative polish (no structural edits)

1. Authority copy pass: **qatar**, **hong-kong**, **transport-nsw**, **thames-clippers**, **nyc-ferry**, **bc-ferries**, **wsf**, **hawaii**
2. **bahrain-motc** phase-1 stub narrative — refine KPI/regulator prose only (geometry sealed)
3. Hero QA: **discovery-land** (mint pending), **didi** (stubs in place)

### P3 — Economics polish

- India demand-fare: **adani-ports**, **reliance-industries** where no registry row
- Cascaded authority/hub cards: polish growth blocks only — **do not** overwrite `model_link` / `route_id`

### P4 — Optional (soneva)

- **soneva** 6/14 featured (43%) — one more Velana/resort mint clears geometry gap; page already **PASS**

---

## Remaining spine PASS_WITH_FLAGS (4) — all hospitality subset pack

| Partner | Spine geo ratio | Owner |
|---------|-----------------|-------|
| aman | 15/70 | Tasklet mint → Grok bind |
| six-senses | 11/70 | Tasklet mint → Grok bind |
| soneva | 11/26 | Tasklet mint (optional) |
| discovery-land | 2/39 | Tasklet Bahamas mint |

No authority/hub/ferry spine flags remain.

---

## Do-not-touch

- **rakta**, **bahrain-motc** — reference tier (stubs OK, no phase-tier restructure)
- Authority `cross_border_roadmap` — amber; `economics_status: roadmap_excluded`
- Hub `markets[]` topology
- Cascaded `model_link` = route_id join keys
- **norway-fjords** phase featured after repair — no full relink pass

---

## Commands

```bash
# Full lane (Waves 0–9)
./scripts/grok-econ-reseal/run_partner_coverage_lane.sh

# Wave 9 only (after Tasklet mints)
python3 scripts/grok-econ-reseal/bind_hospitality_flagship_corridors.py aman six-senses discovery-land
python3 scripts/relink_partner_journeys.py --apply --partner aman six-senses discovery-land
python3 scripts/grok-econ-reseal/relink_hub_market_featured.py lyft kakao-mobility

# Audits + rollup
python3 scripts/audit_partner_spine_parity.py --all
python3 scripts/audit_partner_page_qa.py
python3 scripts/grok-econ-reseal/audit_partner_coverage_rollup.py
```