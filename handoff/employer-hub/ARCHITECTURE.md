# Employer hub architecture

## Product decisions (2026-08-11, updated 2026-08-14)

1. **Canonical URL:** `/employers/<id>` (e.g. `/employers/new-york`, `/employers/bay-area`)
2. **Aliases:** `/ny-employers`, `/bay-employers` (full static copies so cleanUrls work)
3. **Lines:** sequential water spines + transfer hubs (not radial spokes). Geography-first names.
4. **New water segments:** mid-channel hand geometry; no land chords
5. **LOI:** one Google Sheet tab; each row includes `hub` / `hub_id`
6. **Page story:** network + From→To trip planner lead; calculator secondary; LOI capture
7. **Seasonal:** opt-in per hub (`network.show_seasonal`) — NYC only today
8. **No page forks:** template in `employer-hub/template/`; cities are `hub.json` only

## Tasklet packages

- **Future cities playbook:** [`TASKLET-FUTURE-CITIES-HANDOFF.md`](./TASKLET-FUTURE-CITIES-HANDOFF.md) ← start here
- **Marina-standard map corrections (PR #352 v2) completion:** [`../employer-hub-v2/GROK-COMPLETION-map-corrections-2026-08-15.md`](../employer-hub-v2/GROK-COMPLETION-map-corrections-2026-08-15.md)
- Bay: `handoff/bay-employers/` (historical + LOI setup)
- NYC: `handoff/ny-employers/` (PR #349) — content/math only; not a page fork
- v2 network notes: `handoff/employer-hub-v2/` (spec + audits + completion)

## Render source of truth

`employer-hub/` — see `employer-hub/README.md`.
