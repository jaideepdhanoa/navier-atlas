#!/usr/bin/env bash
# Global Geometry Completion — WS-1..WS-7 + gates + deploy
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

GROK="$ROOT/scripts/grok-global"
REPORT="$ROOT/grok-routing-output/global-geometry-completion-report.json"
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

echo "=== Global Geometry Completion ==="
echo "root: $ROOT"
echo "started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# WS-1: Pass-4 + UAE market group
run_step "WS-1 pass4_scope" python3 "$GROK/apply_scope_key_normalization_pass4.py" --apply || true
run_step "WS-1 uae_market_group" python3 "$GROK/apply_uae_market_group.py" --apply || true

# WS-4: Global unstamp restamp (THE UNLOCK)
run_step "WS-4 unstamp_restamp" python3 "$GROK/apply_global_unstamp_restamp.py" --apply || true

# WS-5: Market groups
run_step "WS-5 market_groups" python3 "$GROK/apply_market_groups.py" --apply || true

# WS-3 + WS-6: Careem Gulf + cluster renames
run_step "WS-6 cluster_renames" python3 "$GROK/apply_cluster_renames.py" --apply || true
run_step "WS-3 careem_gulf_qlr" python3 "$GROK/apply_careem_gulf_qlr.py" --apply || true

# WS-7: UAE de-spaghetti
run_step "WS-7 uae_despaghetti" python3 "$GROK/apply_uae_despaghetti.py" --apply || true

# Re-apply marquees after geometry changes
run_step "marquees_reapply" python3 "$GROK/apply_canonical_marquees_global.py" --apply || true

# Gates
run_step "validate_scope_resolution" python3 "$ROOT/scripts/validate_scope_resolution.py" --strict || true
run_step "validate_partner_inheritance" \
  python3 "$ROOT/scripts/validate_partner_inheritance.py" --json --strict --partner \
  airasia-move bolt cabify careem didi gojek grab grab-thailand indrive \
  kakao-mobility line line-man-wongnai lyft noon ola rapido uber uber-india yango yassir || true
run_step "validate_finance_inheritance" python3 "$ROOT/scripts/validate_finance_inheritance.py" --json || true
run_step "update_seal_hashes" python3 "$ROOT/scripts/grok-econ-reseal/update_seal_hashes.py" || true

# Deploy
if [[ -n "${SKIP_DEPLOY:-}" ]]; then
  echo "⊘ SKIP_DEPLOY set"
  STATS+=("deploy: SKIPPED")
else
  run_step "deploy_production" env RELEASE=1 "$ROOT/scripts/deploy.sh" || true
fi

write_receipt() {
  python3 - <<'PY' "$REPORT" "$@"
import json, sys
from datetime import datetime, timezone
from pathlib import Path

report_path = Path(sys.argv[1])
stats = sys.argv[2:-1]
blockers = []
if sys.argv[-1] != "--":
    blockers = [sys.argv[-1]]
elif len(sys.argv) > 3:
    blockers = sys.argv[3:]

receipt = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "lane": "global-geometry-completion",
    "steps": list(stats),
    "blockers": blockers,
    "lane_ok": len(blockers) == 0,
    "prod_url": "https://navier-atlas.vercel.app",
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
PY
}

if ((${#BLOCKERS[@]} > 0)); then
  write_receipt "${STATS[@]}" -- "${BLOCKERS[@]}"
  echo ""
  echo "⚠ Global geometry completion completed with blockers:"
  printf '  - %s\n' "${BLOCKERS[@]}"
  exit 2
fi

write_receipt "${STATS[@]}" --
echo ""
echo "✓ Global geometry completion — https://navier-atlas.vercel.app"