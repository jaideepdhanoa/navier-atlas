# Tasklet → Grok handoff template (partner proposals)

**Use this checklist whenever Tasklet authors a new partner proposal or refreshes an existing one.**

## Division of labor (locked)

| Lane | Owner | Deliverables |
|------|-------|--------------|
| Research inputs | **Tasklet** | Corridors, demand anchors, modeled fares, country-reference rows, BP spec, narrative (`partner-pitch/partners/<id>.json`) |
| Geometry seal | **Grok** | BP mint, route_ids, render flags, partner journey linkage, 0-silent-drops QA |
| Economics cascade | **Grok** | `corridors.json` bind, demand apply, aggregate→growth→splice, sheet, sidecar |
| Deck generation | **Grok** | Deterministic model→deck (after economics bound) |

Tasklet **never** hand-types the `growth_case` ladder — it is always cascade-generated.

---

## What Tasklet delivers (seal-staging package)

Create `partner-pitch/seal-staging/<package-name>/` with:

```
seal-manifest.json          # partner ids, corridor counts, acceptance gates
GROK-PROMPT.md              # geometry mandate + hard gates for Grok
<partner-id>/
  <partner-id>-corridors.json       # enumerated legs, L3 locals, fares (route_id: null until seal)
  <partner-id>-demand-anchors.json  # sourced volumes + capture basis
  <partner-id>-boarding-point-spec.json
  <partner-id>-country-reference-row.json  # (optional) splice into country-reference.json
  README.md
```

Plus narrative at canonical path: `partner-pitch/partners/<partner-id>.json` with `economics_status: pending`.

### Required fields in corridor source

- `proposed_from_node_id` / `proposed_to_node_id` (or labels Grok can resolve)
- `approx_distance_nm`, `vessel`, `archetype`, `country`, `pool_basis`
- `L3_locals.comparable_fare_usd_pax` (modeled fare — flagged, not sealed)
- `capex_tier` on market block (`hospitality` → $1M, `commercial` → region rule)
- `capture_rate` on market block (e.g. 0.55 captive ABC — Grok applies via cascade)

### Hard gates Tasklet must satisfy before PR

- [ ] Every BP in spec appears in corridors or drop-ledger rationale
- [ ] Roadmap legs (>70nm Pioneer II) marked `tier: roadmap` / `render: roadmap-amber-dashed`
- [ ] Seasonal legs flagged `render: seasonal-amber`; `season_days` set or explicitly null with note
- [ ] No hand-typed `growth_case` rungs (stub only)
- [ ] `null` beats confidently-wrong on fares and demand

---

## What Grok runs (automatic)

From repo root:

```bash
# Full lane (geometry + economics + deploy) — ABC / Curaçao package:
./scripts/grok-tasklet-import/run_tasklet_proposal_lane.sh curacao-caribbean-2026-06-24

# Economics only (after geometry already sealed):
SKIP_GEOMETRY=1 ./scripts/grok-tasklet-import/run_tasklet_proposal_lane.sh <package>

# Single partner:
TASKLET_PACKAGE=<package> ./scripts/grok-tasklet-import/run_econ_cascade.sh <partner-id>
```

Pipeline steps (Phase B):

1. `bind_corridors_from_staging.py` — staging → `finance/model/corridors.json` with sealed `route_id`s
2. `build_scoped_corridors.py` — `finance/recal/corridors-<partner>.json`
3. `apply_demand_anchors.py` — `corridor_annual_oneway_pax` from demand anchors
4. `aggregate.py` → `growth.py` → `growth_frontend_block.py` → `splice_growth_into_partner.py`
5. `build_economics_sidecar.py` + `build_transparent_sheet.py`
6. Bind `economics_status` on partner JSON; reseal; deploy

Reports land in `grok-routing-output/tasklet-corridors-bind-report.json` and `grok-routing-output/<partner>-demand-apply-report.json`.

---

## Optional Tasklet follow-ups (non-blocking)

- Logo / deck image assets (see `deck-studio/docs/IMAGE-RULES.md`)
- Fare validation against operator quotes
- `season_days` precision for seasonal legs (Grok defaults Klein Curaçao → 120 days if null)
- Published Google Sheet URL once Jaideep approves sheet upload (`finance/economics_url_map.json`)

---

## Reference implementations

| Package | Partners | Notes |
|---------|----------|-------|
| `curacao-caribbean-2026-06-24` | `ocean-whisperer`, `caribbean` | $1M hospitality vs $900K commercial; capture 0.55; rising ladder |
| `grab-thailand` | `grab-thailand` | Demand apply pattern |
| `minor-hotels` | `minor-hotels` | Captive hospitality cascade |