# Navier Atlas — collaboration repo

The shared, **sanitized** render surface for the Navier marine-mobility atlas
(live: https://navier-atlas.vercel.app). This repo is the single source of truth
for the *presentation layer* and the merge surface between **Tasklet** (data graph)
and **Claude** (render/UI).

> ⚠️ **Confidentiality.** This repo contains ONLY gate-passed, externally-safe
> artifacts. No principal names, deal terms, funding references, gate flags, internal
> scores, or pipeline internals. See `.gitignore`. Never commit anything that trips
> the externalization gate. When in doubt, leave it out.

## What's here
| Path | Owner | Purpose |
|---|---|---|
| `index.html` | Tasklet builds · Claude's render | Current gate-passed production bundle |
| `data-clean/` | Tasklet | Sanitized data Claude renders against (ROUTES, FEATURES_BY_TYPE, STORIES, VESSEL_SPECS) |
| `DIVISION-OF-LABOR.md` | shared | **The contract** — who owns what, render schema, merge protocol |
| `docs/route-demand-model.md` | Tasklet | How `traffic_weight` / `trip_purpose` are derived |
| `docs/POI-RENDERING.md` | shared | Boarding-point glyph spec |
| `PROMPT-FOR-CLAUDE.md` / `README-FOR-CLAUDE.md` | Tasklet | Onboarding for the Claude session |

## What is deliberately NOT here
`build.py`, `route_network.py`, `partition/`, `boarding-points/`, `route-demand-config.json`,
`humans.json`, dossiers, references, secrets — these are **Tasklet-internal** and stay in the
private working tree. The repo is the merge surface, not the pipeline.

## Branching
- `main` — released state (mirrors what's live). **Only Tasklet merges to `main`.**
- `claude/render` — Claude's working branch for front-end/render changes.
- `tasklet/data` — Tasklet's working branch for refreshed `data-clean/` + `index.html`.

## Golden rules
1. Claude edits the **front-end template / render code only** — never the data, never the pipeline, never deploys.
2. Tasklet runs **partition → both gates → `_dist/` deploy** and is the only side that ships to production.
3. The render contract in `DIVISION-OF-LABOR.md` is the frozen seam — changed only by mutual PR.
4. Every merge ships a `HANDOFF-*.md` changelog entry.
