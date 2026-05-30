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

# 2 · build the data asset from data-clean/ (Claude owns render+build; Tasklet delivers DATA only).
#     atlas-data.js sets the window.* globals index.html consumes. One generator ⇒ no clobber.
echo "→ building atlas-data.js from data-clean/…"
node scripts/build.mjs

# 3 · §3 pre-flight (seal hash · exclusion grep · MapLibre smoke · pitch-render presence).
#     Set RELEASE=1 for a prod cut to ENFORCE the seal (§3.1); non-zero ⇒ abort the deploy.
echo "→ running deploy pre-flight…"
node scripts/preflight/preflight.mjs "$ROOT" ${RELEASE:+--release}

# 4 · publish to Vercel prod (static site; index.html + atlas-data.js + assets at repo root,
#     governed by the .vercelignore allowlist)
echo "→ pre-flight clean; deploying to Vercel prod…"
URL="$(npx --yes vercel@54 deploy --prod --yes --token "$VERCEL_TOKEN")"
echo "✅ deployed: $URL"
echo "   (post to #tasklet-jaideep:  ✅ deployed $(git rev-parse --short HEAD) · routes rendering · pre-flight clean)"
