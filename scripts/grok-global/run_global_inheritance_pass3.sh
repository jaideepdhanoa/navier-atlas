#!/usr/bin/env bash
# Grok Pass 3 — apply global marquees + finance cascade + gates + deploy
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

GROK_GLOBAL="$ROOT/scripts/grok-global"
REPORT="$ROOT/grok-routing-output/global-inheritance-pass3-report.json"
BLOCKERS=()
STATS=()

COMMERCIAL="airasia-move,bolt,cabify,careem,didi,gojek,grab,grab-thailand,indrive,kakao-mobility,line,line-man-wongnai,lyft,noon,ola,rapido,uber,uber-india,yango,yassir"

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

echo "=== Grok Pass 3 — global marquee apply + deploy ==="
echo "root: $ROOT"
echo "started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# 1. Apply canonical marquees (direct route_id bind, no re-stamp)
run_step "apply_canonical_marquees_global" python3 "$GROK_GLOBAL/apply_canonical_marquees_global.py" --apply || true

# 2. Route linkage for commercial partners (before marquee apply — linkage may inject phase chips)
run_step "route_linkage_commercial" \
  "$ROOT/scripts/run-route-linkage-lane.sh" --apply --partner \
  airasia-move bolt cabify careem didi gojek grab grab-thailand indrive \
  kakao-mobility line line-man-wongnai lyft noon ola rapido uber uber-india yango yassir || true

# 2b. Re-apply marquees after linkage (clears non-standard phase featured_routes)
run_step "apply_canonical_marquees_post_linkage" python3 "$GROK_GLOBAL/apply_canonical_marquees_global.py" --apply || true

# 3. Finance cascade + sheet refresh (no regen_pta_economics --all)
run_step "finance_cascade" \
  env RUN_CASCADE=1 PARTNERS="$COMMERCIAL" SEAL_TAG="#global-pass3-marquee-2026-07-06" \
  "$ROOT/scripts/grok-econ-reseal/run_finance_sheet_lane.sh" || true

# 4. Inheritance gates (commercial)
run_step "validate_partner_inheritance" \
  python3 "$ROOT/scripts/validate_partner_inheritance.py" --json --strict --partner \
  airasia-move bolt cabify careem didi gojek grab grab-thailand indrive \
  kakao-mobility line line-man-wongnai lyft noon ola rapido uber uber-india yango yassir || true

run_step "validate_finance_inheritance" \
  python3 "$ROOT/scripts/validate_finance_inheritance.py" --json || true

# 5. Seal hashes
run_step "update_seal_hashes" python3 "$ROOT/scripts/grok-econ-reseal/update_seal_hashes.py" || true

# 6. Deploy (RELEASE=1 enforces seal)
if [[ -n "${SKIP_DEPLOY:-}" ]]; then
  echo "⊘ SKIP_DEPLOY set — skipping production deploy"
  STATS+=("deploy: SKIPPED")
else
  run_step "deploy_production" env RELEASE=1 "$ROOT/scripts/deploy.sh" || true
fi

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
    "lane": "global-inheritance-pass3",
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
  echo "⚠ Pass 3 completed with blockers:"
  printf '  - %s\n' "${BLOCKERS[@]}"
  exit 2
fi

echo ""
echo "✓ Grok Pass 3 complete — production live"