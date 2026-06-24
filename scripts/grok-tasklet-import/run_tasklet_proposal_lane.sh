#!/usr/bin/env bash
# Full Tasklet proposal lane: geometry seal (Phase A) → economics cascade (Phase B) → reseal → deploy.
#
# Usage:
#   ./scripts/grok-tasklet-import/run_tasklet_proposal_lane.sh [seal-staging-package]
#   SKIP_GEOMETRY=1 ./scripts/grok-tasklet-import/run_tasklet_proposal_lane.sh   # Phase B only
#
# Trigger whenever Tasklet opens a PR with partner-pitch/seal-staging/<package>/ and
# partner-pitch/partners/<id>.json with economics_status pending.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

SCRIPTS="$ROOT/scripts/grok-tasklet-import"
PACKAGE="${1:-curacao-caribbean-2026-06-24}"
export TASKLET_PACKAGE="$PACKAGE"
SEAL_TAG="${SEAL_TAG:-#pr93-abc-econ}"
BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"

step() { echo ""; echo "=== $* ==="; }

if [[ "${SKIP_GEOMETRY:-0}" != "1" ]]; then
  step "Phase A — geometry seal (if package requires mint)"
  if [[ -x "$ROOT/scripts/run-abc-islands-seal-lane.sh" ]] && [[ "$PACKAGE" == *"curacao-caribbean"* ]]; then
    SEAL_TAG="${SEAL_TAG%-*}-seal" "$ROOT/scripts/run-abc-islands-seal-lane.sh" || true
  else
    echo "  (no geometry lane for package $PACKAGE — assuming geometry already sealed)"
  fi
else
  echo "SKIP_GEOMETRY=1 — Phase A skipped"
fi

step "Phase B — bind corridors + economics cascade (per partner in seal-manifest)"
PARTNERS=$(python3 - <<'PY' "$ROOT" "$PACKAGE"
import json, sys
from pathlib import Path
pkg = Path(sys.argv[1]) / "partner-pitch/seal-staging" / sys.argv[2]
m = json.loads((pkg / "seal-manifest.json").read_text())
print(" ".join(m.get("partners", {}).keys()))
PY
)

for p in $PARTNERS; do
  step "Phase B — $p"
  "$SCRIPTS/run_econ_cascade.sh" "$p"
done

step "Reseal hashes + sidecar refresh (canonical corridors)"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ROOT/finance/model/corridors.json" \
  --aggdir "$ROOT/finance/recal" \
  --url-map "$ROOT/finance/economics_url_map.json"

python3 "$ECON/update_seal_hashes.py" 2>/dev/null || true

step "Build + deploy"
BUILD_PROFILE=public node "$ROOT/scripts/build-site.mjs" --profile=public
RELEASE=1 BUILD_PROFILE=public "$ROOT/scripts/deploy.sh"

"$ROOT/scripts/publish-gold.sh" "Gold $SEAL_TAG — Tasklet proposal economics ($PACKAGE)" "$SCRIPTS/"
echo "✓ tasklet proposal lane complete ($PACKAGE / $SEAL_TAG)"