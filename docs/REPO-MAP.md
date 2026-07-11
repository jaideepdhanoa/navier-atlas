# navier-atlas — repo reference map (for the Grok-chat / Tasklet seat)

Source of truth: `github.com/jaideepdhanoa/navier-atlas` @ `main`. Everything below is a repo path.

## Handshake / operating docs (root + docs/)
- `DIVISION-OF-LABOR.md` — the seat contract (research vs build).
- `README-FOR-CLAUDE.md`, `PROMPT-FOR-CLAUDE.md`, `WORK-QUEUE-FOR-CLAUDE.md` — the **build seat's** brief +
  the queue **you** write for it.
- `CHANGES-FROM-TASKLET.md` / `docs/CHANGES-FROM-TASKLET.md` — what build changed back.
- `docs/NOTES-FOR-TASKLET.md` — the long-running shared notebook (large; skim by section).
- `docs/BRAND-VOICE-FOR-TASKLET.md` — partner-facing voice rules (plain English, no AI slop).
- `docs/playbooks/` — **the five playbooks + archetype + hospitality gold** (added by this migration).
- `docs/GROK-SPEC-*.md` — open specs handed to build (data-driven capture, OW greenfield rescope, …).

## Economics / model (YOUR primary lane) — `finance/`
- `finance/model/corridors.json` — **the durable global corridor network** (markets keyed `partner-geography`;
  per-corridor demand/fare in `L3_locals`). The single economic source of truth.
- `finance/model/aggregate.py` — grounded-floor + cascade engine (reads `corridors.json`).
- `finance/model/growth.py` — SOM floor → SAM → TAM journey-GMV → partner platform-rev ladder.
- `finance/model/country-reference.json` — per-country opex/energy/grid/crew/marina. Missing/incomplete exact
  country rows now fail closed; explicitly held corridors are excluded and disclosed. Run
  `scripts/validate_country_reference.py` before every cascade, sheet, sidecar, or deck seal.
- `finance/model/vessel-constants.json`, `growth-config.json` — scenario bands, hull constants, capex tiers.
- `finance/model/build_transparent_sheet.py` — the **second, independent** cost engine (must agree with the
  model — golden rule #7).
- `finance/recal/agg-<partner>.json`, `growth-<partner>.json` — per-partner aggregates/ladders.
- `finance/PARTNER-SHEET-IDS.json` — Google Sheet IDs for in-place updates (`fileIdToReplace`).
- `finance/model/build_master_sheet.py`, `splice_growth_into_partner.py`, `materialize_partner_economics.py`.

## Partner proposals — `partner-pitch/`
- `partner-pitch/partners/<partner>.json` — the proposal (hero, markets, journeys, phases, growth_case).
  Derivatives: `grab-thailand.json`, `line-man-wongnai-derivative.json`, `uber-india-derivative.json`, …
- `partner-pitch/partners/_growth-draft/<partner>.growth.json` — frontend phase-economics block.
- `partner-pitch/subproposals/build_scaffold.py` — re-gates hulls per leg (VESSEL-REGATE-LEDGER).
- `partner-pitch/*PARITY*`, `*CROSSWALK*` — worked parity examples (Bolt/Yango).

## Atlas render graph (BUILD's lane; you assemble inputs) 
- `atlas-external/boarding-points/<city>.json` — researched BPs (bare-slug city ids).
- `data-clean/` — sealed graph: `ROUTES.json`, `FEATURES_BY_TYPE.json`, `partners/<p>.json`,
  `economics_by_route_id.json` (the route-keyed sidecar).
- `_ingest/` — staged seal inputs.

## Decks — `deck-studio/` and `decks/`
- `deck-studio/decks/<deck_key>/` — `deck.config.json`, `slide-manifest.json`, `content-source.json`,
  `image-manifest.json`, `slide3-kpis-*.json`. (e.g. `grab-thailand/`, new `line-man-wongnai/`.)
- `deck-studio/assets/` + `ASSET-REGISTRY.json` — banked N30 plates + partner logos by market/role.
- `deck-studio/qa/partner_copy_lint.py` — the blocking no-jargon copy gate.
- `deck-studio/docs/PARTNER-COPY-RULES.md`, `SPEC-narrative-binding.md`.
- `decks/<partner>/assets/` — per-deck market backgrounds (e.g. `minor-hotels-v2/assets/econ-bg-bali-n30.jpg`).

## Handoff packages — `handoff/`
- `handoff/GROK-*.md`, `handoff/partner-map-model/<batch>/` — prompts + readiness queues + source maps + status.
- `handoff/grok-handback-*.md` — build's handbacks to you.

## Scripts / QA — `scripts/`, `tests/`
- `scripts/validate_partner_proposals.py --strict-narrative` — slide-2 readiness gate.
- `scripts/grok-tasklet-import` lane — import path between seats.

## Front-end app (build/deploy) — `app/`, `api/`, `index.html`, `vercel.json`, `DEPLOY.md`.
