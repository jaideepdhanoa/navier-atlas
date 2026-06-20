# Navier finance engine — vendored toolchain (Tasklet → Grok handoff)

This tree is the **complete, runnable** partner unit-economics cascade. It is stdlib-only
(Python 3, no third-party packages) and self-contained: every script reads its inputs by
relative path from this `finance/` directory. Vendored so Grok's CI can run the cascade
end-to-end going forward, per the Tasklet↔Grok division of labor.

> Supersedes the older partial copy under `_ingest/gold-delta-LB230-LB241/finance/model/`
> (which only had `aggregate.py` + `corridors.json`). Use this root-level `finance/` tree.

## Files

```
finance/
  model/
    aggregate.py            stage 1 — joins per-corridor L3 sourcing with per-country opex
    atom.py                 loaded by aggregate.py (importlib) — per-corridor economics atom
    growth.py               stage 2 — growth-case cascade (floor -> SAM/TAM ladder)
    growth_frontend_block.py stage 3 — front-end growth block for partner pages
    growth-config.json      growth parameters (read by growth.py)
    vessel-constants.json   N30 vessel + opex constants
    country-reference.json  per-country opex / fx / labor reference (39 rows)
    corridors.json          canonical corridor registry snapshot (see "Corridors" below)
  splice_growth_into_partner.py  stage 4 — splices growth_case into partner-pitch/partners/<p>.json
  build_economics_sidecar.py     gold sidecar builder (reads a gold ROUTES.json + agg-<p>.json)
  economics_url_map.json         deck/economics URL map (read by the sidecar builder)
  grab-growth-case.json          growth.py default-output fallback
  recal/                         output target for agg-*, growth-*, growth-frontend-* JSON
partner-pitch/
  subproposals/build_scaffold.py Gate C.1 vessel re-gate (Bolt subproposal scaffold)
```

## Run order (the locked cascade)

```bash
cd finance/model

# 1) aggregate  — pass --corridors to override the default registry (see Corridors)
python3 aggregate.py --partner <p> --json ../recal/agg-<p>.json \
    [--corridors /abs/or/rel/path/to/deduped-corridors.json]

# 2) growth     — output flag is --json (not --out)
python3 growth.py --agg ../recal/agg-<p>.json --partner <p> --json ../recal/growth-<p>.json

# 3) frontend block
python3 growth_frontend_block.py --partner <p> \
    --growth ../recal/growth-<p>.json --rollup ../recal/agg-<p>.json \
    --out ../recal/growth-frontend-<p>.json

# 4) splice into the partner page
cd ..
python3 splice_growth_into_partner.py --partner <p> \
    --growth recal/growth-<p>.json --frontend recal/growth-frontend-<p>.json \
    --partner-json partner-pitch/partners/<p>.json
```

`<p>` in {grab, bolt, yango, careem, ...}. Verified end-to-end for **yango** from a clean
minimal tree (all four stages green).

## Corridors (source-of-truth convention)

`finance/model/corridors.json` here is a **canonical registry snapshot**. For the PR #46
parity re-aggregate, the de-duped SE-Asia corridors live at
`_ingest/tasklet-parity-2026-06-20/corridors.json`. Grok should **diff the two** and pass the
de-duped file via `aggregate.py --corridors <path>`. If they are identical lineage, the bare
default is fine. `aggregate.py` reads `--corridors` if present, else `model/corridors.json`.

## Division of labor (unchanged)

- **Tasklet** — corridors, BP research, partner content, agg inputs; PRs to `main`.
- **Grok** — merge, mint/seal BPs, **run this finance cascade**, build sidecar, deploy.
