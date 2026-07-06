#!/usr/bin/env bash
# Grok Pass 1 — global corridor inheritance (116 contested clusters, one batch)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

GROK_GLOBAL="$ROOT/scripts/grok-global"
REPORT="$ROOT/grok-routing-output/global-inheritance-pass1-report.json"
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

echo "=== Grok Pass 1 — global corridor inheritance ==="
echo "root: $ROOT"
echo "started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# 0. BP hygiene precondition
run_step "apply_bp_cleanup_register" python3 "$GROK_GLOBAL/apply_bp_cleanup_register.py" --apply || true

# 1. Global geometry reseal (116 clusters, contention order)
run_step "seal_global_corridor_consolidation" python3 "$GROK_GLOBAL/seal_global_corridor_consolidation.py" --apply || true

# 2. Finance spine unification (all multi-partner geographies)
run_step "unify_finance_spine_global" python3 "$GROK_GLOBAL/unify_finance_spine_global.py" --apply || true

# 3. Derive partner scopes + strip hand-curated corridor arrays
run_step "derive_partner_scopes_global" python3 "$GROK_GLOBAL/derive_partner_scopes_global.py" --apply || true

# 4. Emit slim sealed-corridor manifests for Tasklet Pass 2
run_step "emit_sealed_corridor_manifests" python3 "$GROK_GLOBAL/emit_sealed_corridor_manifests.py" --apply || true

# 5. Inheritance gates (global)
run_step "validate_partner_inheritance" python3 "$ROOT/scripts/validate_partner_inheritance.py" --json --strict || true
run_step "validate_finance_inheritance" python3 "$ROOT/scripts/validate_finance_inheritance.py" --json || true

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
    "lane": "global-inheritance-pass1",
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
  echo "⚠ Pass 1 completed with blockers:"
  printf '  - %s\n' "${BLOCKERS[@]}"
  exit 2
fi

echo ""
echo "✓ Grok Pass 1 complete — ready for Tasklet global marquee curation"