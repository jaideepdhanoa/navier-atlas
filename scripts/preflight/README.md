# Deploy pre-flight

Implements `DIVISION-OF-LABOR.md` §3 — the three cheap checks Claude Code runs before every
`vercel deploy --prod`. Exit non-zero ⇒ **abort the deploy**.

```bash
cd scripts/preflight && npm install        # one-time (node_modules is gitignored)
node preflight.mjs <repo-root>             # full run (requires data-clean/SEAL.json)
node preflight.mjs <repo-root> --allow-unsealed   # non-prod smoke (bypasses §3.1 only)
```

Or via the wrapper, which also deploys on success:

```bash
VERCEL_TOKEN=… ./scripts/deploy.sh
```

## Checks

| # | Check | What it does | Abort when |
|---|---|---|---|
| §3.1 | **hash match** | sha256 of each `data-clean/<NAME>.json` vs `data-clean/SEAL.json` | mismatch, or `SEAL.json` missing (data altered after sealing / not sealed) |
| §3.2 | **exclusion grep** | every pattern in `docs/EXCLUSION-TOKENS.txt` (case-insensitive regex) vs the final `index.html` | any match (a leak introduced in the render template) |
| §3.3 | **MapLibre smoke** | runs the page's real layer code under a MapLibre stub, validates every layer with the official `@maplibre/maplibre-gl-style-spec`, and asserts the route line layers register & bind to `routes` | any layer rejected, or route line layers missing |

§3.3 is the guard against the **F-01 / F-12 class** (a layer silently dropped by an invalid `zoom`
expression). It already caught two such bugs: `city-hub-glow` and Tasklet's `priority-hub-glow`.

## Note on `SEAL.json`

§3.1 expects `data-clean/SEAL.json` (Tasklet-produced) shaped like:

```json
{ "blobs": { "ROUTES": { "sha256": "…", "count": 1354 },
             "FEATURES_BY_TYPE": { "sha256": "…" },
             "STORIES": { "sha256": "…" },
             "VESSEL_SPECS": { "sha256": "…" } } }
```

If Tasklet's actual schema differs, adjust the `§3.1` block in `preflight.mjs` (or tell Claude to).
Until `SEAL.json` ships, a prod deploy is blocked by design; `--allow-unsealed` is for local smoke only.
