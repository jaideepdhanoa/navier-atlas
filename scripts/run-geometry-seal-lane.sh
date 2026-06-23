#!/usr/bin/env bash
# Geometry seal lane — land QA, coastal re-solve, allowlist scrub, seal refresh.
#
#   ./scripts/run-geometry-seal-lane.sh --wave g1 --apply
#   ./scripts/run-geometry-seal-lane.sh --wave all --apply --strict
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

APPLY=0
WAVE="g0"
STRICT=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --strict) STRICT=1; shift ;;
    --wave)
      shift
      WAVE="${1:-g0}"
      shift
      ;;
    --wave=*)
      WAVE="${1#--wave=}"
      shift
      ;;
    g0|g1|g2|g3|g4|all)
      WAVE="$1"
      shift
      ;;
    *) shift ;;
  esac
done

PY_APPLY=()
if ((APPLY)); then PY_APPLY=(--apply); fi
AUDIT_AFTER=(python3 scripts/audit-route-geometry.py)
if ((STRICT)); then AUDIT_AFTER+=(--strict); fi

echo "→ geometry audit (before)"
python3 scripts/audit-route-geometry.py || true

run_g0() {
  echo "→ G0 instrument (triage report)"
  python3 scripts/audit-route-geometry.py
}

run_g1() {
  echo "→ G1 story channel mint (nudge-first)"
  python3 scripts/grok-geometry/mint_story_channels.py --story --nudge-only --max-land-km 5 "${PY_APPLY[@]}"
  echo "→ G1 story channel A* solve (remaining)"
  python3 scripts/grok-geometry/mint_story_channels.py --story --min-land-km 5 "${PY_APPLY[@]}"
  echo "→ G1 legacy coastal re-solve"
  python3 scripts/grok-geometry/fix_route_geometry.py --story "${PY_APPLY[@]}"
  echo "→ G1 story channel A* solve"
  python3 scripts/grok-geometry/solve_story_channels.py --story "${PY_APPLY[@]}"
  echo "→ G1 apply route-solutions.jsonl"
  if ((APPLY)); then
    python3 scripts/grok-geometry/apply_route_solutions.py
  fi
  echo "→ G1 scrub story routes from allowlist"
  python3 scripts/grok-geometry/scrub_story_allowlist.py "${PY_APPLY[@]}"
}

run_g2() {
  echo "→ G2 cluster + allowlisted coastal re-solve"
  python3 scripts/grok-geometry/fix_route_geometry.py --allowlisted "${PY_APPLY[@]}"
}

run_g3() {
  echo "→ G3 mesh burn-down (remaining QA failures)"
  python3 scripts/grok-geometry/fix_route_geometry.py --all "${PY_APPLY[@]}"
}

run_g4() {
  echo "→ G4 seal hash + geometry gate"
  if ((APPLY)); then
    python3 scripts/grok-econ-reseal/update_seal_hashes.py
    python3 scripts/grok-geometry/update_seal_geometry_gate.py --apply
  else
    python3 scripts/grok-geometry/update_seal_geometry_gate.py
  fi
}

case "$WAVE" in
  g0) run_g0 ;;
  g1) run_g1 ;;
  g2) run_g2 ;;
  g3) run_g3 ;;
  g4) run_g4 ;;
  all)
    run_g0
    run_g1
    run_g2
    run_g3
    run_g4
    ;;
  *)
    echo "unknown wave: $WAVE" >&2
    exit 2
    ;;
esac

echo "→ geometry audit (after)"
"${AUDIT_AFTER[@]}"

echo "✓ geometry seal lane complete (wave=$WAVE)"