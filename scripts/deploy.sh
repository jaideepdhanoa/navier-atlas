#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Navier Atlas — production deploy  (DIVISION-OF-LABOR.md §3 / §4)
# Runs the mandatory pre-flight, then publishes index.html to Vercel prod.
# Claude Code owns this path; Tasklet seals the data. ABORTS if pre-flight fails.
#
#   VERCEL_TOKEN=… ./scripts/deploy.sh
#
# Required env:
#   VERCEL_TOKEN                  Vercel access token (NEVER commit; provided via env secret)
# Optional env (if the project isn't linked via .vercel/):
#   VERCEL_ORG_ID, VERCEL_PROJECT_ID   target the existing navier-atlas project non-interactively
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

: "${VERCEL_TOKEN:?VERCEL_TOKEN not set — provision it as an environment secret, never in git}"

# 1 · pre-flight deps (gitignored node_modules; install on first run)
if [ ! -d scripts/preflight/node_modules ]; then
  echo "→ installing pre-flight deps…"
  ( cd scripts/preflight && npm install --silent --no-audit --no-fund )
fi

# 2 · §3 pre-flight (hash match · exclusion grep · MapLibre smoke). Non-zero ⇒ abort the deploy.
echo "→ running deploy pre-flight…"
node scripts/preflight/preflight.mjs "$ROOT"

# 3 · publish to Vercel prod (static single-file site; index.html + assets at repo root)
echo "→ pre-flight clean; deploying to Vercel prod…"
URL="$(npx --yes vercel@54 deploy --prod --yes --token "$VERCEL_TOKEN")"
echo "✅ deployed: $URL"
echo "   (post to #tasklet-jaideep:  ✅ deployed $(git rev-parse --short HEAD) · routes rendering · pre-flight clean)"
