#!/usr/bin/env bash
# Grok Pass 4 — scope-key normalization + gates
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

GROK_GLOBAL="$ROOT/scripts/grok-global"
REPORT="$ROOT/grok-routing-output/global-inheritance-pass4-report.json"
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

echo "=== Grok Pass 4 — scope-key normalization ==="
echo "root: $ROOT"
echo "started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

run_step "apply_scope_key_normalization" python3 "$GROK_GLOBAL/apply_scope_key_normalization_pass4.py" --apply || true

run_step "validate_scope_resolution" python3 "$ROOT/scripts/validate_scope_resolution.py" --json --strict || true

run_step "validate_partner_inheritance" \
  python3 "$ROOT/scripts/validate_partner_inheritance.py" --json --strict --partner \
  airasia-move bolt cabify careem didi gojek grab grab-thailand indrive \
  kakao-mobility line line-man-wongnai lyft noon ola rapido uber uber-india yango yassir || true

run_step "update_seal_hashes" python3 "$ROOT/scripts/grok-econ-reseal/update_seal_hashes.py" || true

write_pass4_receipt() {
  python3 - <<'PY' "$REPORT" "$@"
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
    "lane": "global-inheritance-pass4",
    "steps": stats,
    "blockers": blockers,
    "lane_ok": len(blockers) == 0,
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
PY
}

if ((${#BLOCKERS[@]} > 0)); then
  write_pass4_receipt "${STATS[@]}" -- "${BLOCKERS[@]}"
else
  write_pass4_receipt "${STATS[@]}" --
fi

if ((${#BLOCKERS[@]} > 0)); then
  echo ""
  echo "⚠ Pass 4 completed with blockers:"
  printf '  - %s\n' "${BLOCKERS[@]}"
  exit 2
fi

echo ""
echo "✓ Grok Pass 4 complete"