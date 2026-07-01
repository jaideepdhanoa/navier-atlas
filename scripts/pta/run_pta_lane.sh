#!/usr/bin/env bash
# PTA end-to-end lane: gap table → spine expand → seal → linkage → gates
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PARTNERS=()
APPLY=0
DEPLOY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --deploy) DEPLOY=1; APPLY=1; shift ;;
    --partner)
      shift
      while [[ $# -gt 0 && "$1" != --* ]]; do PARTNERS+=("$1"); shift; done
      ;;
    *) shift ;;
  esac
done

echo "→ PTA pair-gap table"
python3 scripts/pta/build_pair_gap_table.py --write

EXPAND_ARGS=(--all)
((APPLY)) && EXPAND_ARGS+=(--apply)
echo "→ expand operating spine (hub-spoke)"
python3 scripts/pta/expand_operating_spine.py "${EXPAND_ARGS[@]}"

if ((${#PARTNERS[@]} == 0)); then
  mapfile -t PARTNERS < <(python3 -c "
import json
from pathlib import Path
rows=json.loads(Path('handoff/partner-map-model/PTA-PAIR-GAP-TABLE.json').read_text())['authorities']
for r in sorted(rows, key=lambda x: x['partner_id']):
    print(r['partner_id'])
")
fi

for slug in "${PARTNERS[@]}"; do
  echo "→ author hand waypoints $slug"
  HW_ARGS=(--partner "$slug")
  ((APPLY)) && HW_ARGS+=(--apply)
  python3 scripts/pta/author_pta_hand_waypoints.py "${HW_ARGS[@]}" || true
  echo "→ seal $slug"
  SEAL_ARGS=(--partner "$slug")
  ((APPLY)) && SEAL_ARGS+=(--apply)
  python3 scripts/pta/seal_authority.py "${SEAL_ARGS[@]}" || true
  if ((APPLY)); then
    ./scripts/run-route-linkage-lane.sh --partner "$slug" --apply || true
    python3 scripts/audit_proposal_fidelity.py --partner "$slug" || true
  fi
done

if ((APPLY)); then
  echo "→ global gates"
  python3 scripts/audit_proposal_fidelity.py --all-partners --strict-deploy-gate
  python3 scripts/audit-route-geometry.py --strict-severe
  node scripts/audit-partner-route-linkage.mjs --strict --global
  python3 scripts/validate-seal-integrity.py --strict
  BUILD_PROFILE=public node scripts/build.mjs
  BUILD_PROFILE=public node scripts/build-site.mjs
fi

if ((DEPLOY)); then
  RELEASE=1 ./scripts/deploy.sh
fi

echo "✓ PTA lane complete"