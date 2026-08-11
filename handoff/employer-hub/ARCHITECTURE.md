# Employer hub architecture (locked 2026-08-11)

## Product decisions

1. **Canonical URL:** `/employers/<id>` (e.g. `/employers/new-york`, `/employers/bay-area`)
2. **Aliases:** `/ny-employers`, `/bay-employers` (full static copies so cleanUrls work)
3. **Lines:** consistent with Bay — every product line (including LGA EXEC when present) is a map line
4. **New water segments:** Grok draws water-clean display geometry
5. **LOI:** one Google Sheet tab; each row includes `hub` / `hub_id`
6. **Build order:** extract template from Bay first; NYC is hub #2 on the same rails

## Tasklet packages

- Bay: `handoff/bay-employers/` (historical + LOI setup)
- NYC: `handoff/ny-employers/` (PR #349) — content/math only; not a page fork

## Render source of truth

`employer-hub/` — see `employer-hub/README.md`.
