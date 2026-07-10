#!/usr/bin/env bash
# Rebuild partner transparent sheets after country-reference opex seal.
# See finance/REBUILD-AFTER-COUNTRY-OPEX.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

MODE="${1:---dry-run}"
# Default: partners impacted by 2026-07-10 missing country-opex inventory
PARTNERS="${COUNTRY_OPEX_REBUILD_PARTNERS:-swing naver yango didi caribbean-mobility}"

echo "== country-opex rebuild =="
echo "root: $ROOT"
echo "mode: $MODE"
echo "partners: $PARTNERS"

echo ""
echo "== lint (report) =="
python3 finance/lint_country_opex.py --report-only || true

case "$MODE" in
  --dry-run)
    echo ""
    echo "Dry-run only. Would build:"
    for p in $PARTNERS; do
      echo "  python3 finance/build_transparent_sheet.py --partner $p --out finance/_refresh_${p}.xlsx"
    done
    echo "Then publish via finance/refresh_all_sheets.py --partners $(echo $PARTNERS | tr ' ' ',')"
    echo "Kakao intentionally excluded until South Korea country-ref is sealed."
    exit 0
    ;;
  --build)
    for p in $PARTNERS; do
      echo ""
      echo "== build $p =="
      # Prefer scoped corridors when present (partner_sheet_build)
      python3 - <<PY
import subprocess, sys
from pathlib import Path
sys.path.insert(0, "finance")
from partner_sheet_build import build_sheet_cmd
p = "$p"
out = Path("finance") / f"_refresh_{p}.xlsx"
cmd = build_sheet_cmd(p, out)
print(" ".join(cmd))
r = subprocess.run(cmd)
raise SystemExit(r.returncode)
PY
    done
    echo ""
    echo "Built local xlsx under finance/_refresh_*.xlsx — review Country opex tab banners before publish."
    exit 0
    ;;
  --publish)
    # Build first
    bash "$0" --build
    echo ""
    echo "== publish =="
    python3 finance/refresh_all_sheets.py --partners "$(echo $PARTNERS | tr ' ' ',')" --skip-master
    echo "Done. Clear partner _opex_country_status fallback notes if lint is clean."
    exit 0
    ;;
  --strict-check)
    fail=0
    for p in $PARTNERS; do
      echo "== strict $p =="
      if ! python3 finance/lint_country_opex.py --partner "$p"; then
        fail=1
      fi
    done
    exit $fail
    ;;
  *)
    echo "Usage: $0 --dry-run | --build | --publish | --strict-check"
    exit 2
    ;;
esac
