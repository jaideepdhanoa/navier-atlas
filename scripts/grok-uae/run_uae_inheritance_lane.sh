#!/usr/bin/env bash
# UAE inheritance lane — geometry seal → marquees → finance spine → peru/senegal → gates → sync
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

GROK_UAE="$ROOT/scripts/grok-uae"
GROK_YANGO="$ROOT/scripts/grok-yango"
REPORT="$ROOT/grok-routing-output/uae-inheritance-lane-report.json"
BLOCKERS=()
STATS=()

run_step() {
  local label="$1"
  shift
  echo ""
  echo "→ $label"
  if "$@"; then
    STATS+=("$label: OK")
    return 0
  else
    local rc=$?
    BLOCKERS+=("$label failed (exit $rc)")
    STATS+=("$label: FAIL($rc)")
    return "$rc"
  fi
}

run_if_exists() {
  local script="$1"
  local label="$2"
  shift 2
  if [[ -f "$script" ]]; then
    run_step "$label" python3 "$script" "$@" || true
  else
    echo "⊘ skip $label — missing $script"
    BLOCKERS+=("missing: $script")
    STATS+=("$label: SKIPPED(missing)")
  fi
}

echo "=== UAE inheritance lane ==="
echo "root: $ROOT"
echo "started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# 1. UAE geometry consolidation
run_if_exists "$GROK_UAE/seal_uae_corridor_consolidation.py" "seal_uae_corridor_consolidation" --apply || true

# 2. Canonical marquees (optional)
run_if_exists "$GROK_UAE/apply_canonical_marquees.py" "apply_canonical_marquees" --apply || true

# 3. Finance spine unification
run_step "unify_uae_finance_spine" python3 "$GROK_UAE/unify_uae_finance_spine.py" --apply || true

# 4. Peru + Senegal Yango density seal
run_step "seal_yango_peru_senegal" python3 "$GROK_YANGO/seal_yango_peru_senegal.py" --apply || true

# 5. Inheritance gates
run_if_exists "$ROOT/scripts/validate_partner_inheritance.py" "validate_partner_inheritance" --partner careem bolt yango noon --strict || true
run_if_exists "$ROOT/scripts/validate_finance_inheritance.py" "validate_finance_inheritance" --geography uae || true

# 6. Partner map scope sync
if [[ -f "$ROOT/scripts/sync-partner-map-scope.mjs" ]]; then
  run_step "sync-partner-map-scope" node "$ROOT/scripts/sync-partner-map-scope.mjs" || true
else
  BLOCKERS+=("missing: scripts/sync-partner-map-scope.mjs")
fi

# 7. Reseal hashes
run_step "update_seal_hashes" python3 "$ROOT/scripts/grok-econ-reseal/update_seal_hashes.py" || true

python3 - <<'PY' "$REPORT" "${STATS[@]}" -- "${BLOCKERS[@]}"
import json, sys
from datetime import datetime, timezone
from pathlib import Path

report_path = Path(sys.argv[1])
stats = []
blockers = []
mode = "stats"
for arg in sys.argv[2:]:
    if arg == "--":
        mode = "blockers"
        continue
    if mode == "stats":
        stats.append(arg)
    else:
        blockers.append(arg)

receipt = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "lane": "uae-inheritance",
    "steps": stats,
    "blockers": blockers,
    "lane_ok": len(blockers) == 0,
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
PY

if ((${#BLOCKERS[@]:-0} > 0)); then
  echo ""
  echo "⚠ Lane completed with blockers:"
  printf '  - %s\n' "${BLOCKERS[@]}"
  exit 2
fi

echo ""
echo "✓ UAE inheritance lane complete"