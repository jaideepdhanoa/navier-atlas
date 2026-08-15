# Employer hubs (templated city microsites)

Public sales surfaces for employer water networks. **One template**, many cities.

## Decisions (2026-08-11)

| Topic | Choice |
|-------|--------|
| Canonical URL | `/employers/<id>` e.g. `/employers/new-york`, `/employers/bay-area` |
| Aliases | `/bay-employers`, `/ny-employers`, `/dc-employers` (full copies for cleanUrls) |
| Lines / EXEC | Same map treatment as Bay — every product line is a styled display line |
| New water segments | Grok owns water-clean hand geometry |
| LOI | One Google Sheet tab; rows include `hub` / `hub_id` |
| Migration | Extract template from Bay first; NYC is hub #2 |

## Layout

```
employer-hub/
  registry.json              # which hubs to build
  template/
    index.html               # shell + brand mark
    hub.css
    hub.js                   # map, calculator profiles, LOI
  hubs/
    bay-area/hub.json        # hub #1 (live)
    new-york/hub.json        # hub #2 (live)
    washington-dc/hub.json   # hub #3 (live)
    miami/hub.json           # hub #4 (live) — dual cluster Miami/FTL
    boston/hub.json          # hub #5 (live)
    seattle/hub.json         # hub #6 (live) — dual cluster Lake/Sound
    san-diego/hub.json       # hub #7 (live) — San Diego Bay
```

## Calculator profiles

- `bay_productivity` — net incremental + hours/CO₂ (Bay defaults → $4,500 / $75)
- `nyc_parking_toll` — $/rider vs parking+toll benchmark (NY defaults → $600 vs $759, $18,900)

## Build

```bash
node scripts/build-employer-hubs.mjs
# or full site:
node scripts/build-site.mjs
```

Emits `_dist/employers/<id>/` and each alias path with `index.html`, `hub.css`, `hub.js`, `hub-data.js`, `assets/hero.jpg`.

## Add a city

1. Create `hubs/<id>/hub.json` (copy Bay or NY shape).
2. Register in `registry.json` with `canonical_path` + `aliases`.
3. Resolve stop coords (sealed `bp_id`s) and line `water_path`s — **sequential spines**, mid-channel only.
4. Set transfer hubs, `trip_planner`, catchment, network-first `copy`.
5. Set `calculator.profile` + `worked_assert`.
6. Build + deploy.

**Full future-city playbook (Tasklet):**  
[`handoff/employer-hub/TASKLET-FUTURE-CITIES-HANDOFF.md`](../handoff/employer-hub/TASKLET-FUTURE-CITIES-HANDOFF.md)

Legacy one-off page: `bay-employers/index.html` is **deprecated** as source of truth (kept for reference until removed). Edits go in `employer-hub/`.
