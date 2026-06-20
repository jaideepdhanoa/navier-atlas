#!/usr/bin/env bash
# Commit sealed gold to main, push to GitHub, deploy to Vercel prod.
# GitHub is the handoff channel for Tasklet — lanes call this by default.
#
# Usage:
#   ./scripts/publish-gold.sh "Gold #79at — description" [extra paths to git add...]
#
# Opt out (dry run / local iteration):
#   SKIP_PUBLISH=1 ./scripts/grok-econ-reseal/run_79at_lane.sh
#   SKIP_DEPLOY=1  — push only, no Vercel deploy
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "${SKIP_PUBLISH:-}" == "1" ]]; then
  echo "→ SKIP_PUBLISH=1 — skipping commit/push/deploy"
  exit 0
fi

MSG="${1:?usage: publish-gold.sh \"commit message\" [paths...]}"
shift || true

# Default paths every gold lane touches
PATHS=(
  data-clean/
  scripts/
  grok-routing-output/
  docs/NOTES-FOR-TASKLET.md
)
if [[ $# -gt 0 ]]; then
  PATHS+=("$@")
fi

git add "${PATHS[@]}"

if git diff --cached --quiet; then
  echo "→ nothing staged; skipping commit"
else
  git commit -m "$MSG"
fi

echo "→ pushing origin main (Tasklet handoff channel)"
git push origin main

if [[ "${SKIP_DEPLOY:-}" == "1" ]]; then
  echo "→ SKIP_DEPLOY=1 — push complete, deploy skipped"
  exit 0
fi

SHA="$(git rev-parse --short HEAD)"
echo "→ deploying $SHA to Vercel prod"
RELEASE=1 ./scripts/deploy.sh
echo "✅ published $SHA → https://navier-atlas.vercel.app (GitHub main + Vercel prod)"