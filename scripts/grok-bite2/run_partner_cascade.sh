#!/usr/bin/env bash
# Bite-2: bind growth_case for one partner (mobility or hospitality).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-bite2"
FINANCE="$ROOT/finance"
MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"
BY="$ROOT/scripts/grok-bolt-yango"
PARTNER="${1:-}"
LADDER_TYPE="${2:-mobility_ladder}"

if [[ -z "$PARTNER" ]]; then
  echo "Usage: $0 <partner-id> [mobility_ladder|hospitality_unit_econ]" >&2
  exit 1
fi

CORR="$RECAL/corridors-$PARTNER.json"
PJ="$ROOT/partner-pitch/partners/$PARTNER.json"
DC="$ROOT/data-clean/partners/$PARTNER.json"
MARKETS="$PARTNER"

step() { echo ""; echo "=== $PARTNER: $* ==="; }

step "0 build scoped corridors"
python3 "$SCRIPTS/build_partner_corridors.py" --partner "$PARTNER"
N=$(python3 -c "import json; d=json.load(open('$CORR')); print(len(d['markets']['$PARTNER']['corridors']))")
if [[ "$N" == "0" ]]; then
  echo "✗ no corridors for $PARTNER — skip" >&2
  exit 2
fi

step "1 aggregate.py"
python3 "$MODEL/aggregate.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --corridors "$CORR" \
  --json "$RECAL/agg-$PARTNER.json"

step "2 growth.py"
python3 "$MODEL/growth.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --agg "$RECAL/agg-$PARTNER.json" \
  --json "$RECAL/growth-$PARTNER.json"

step "3 growth_frontend_block.py"
mkdir -p "$GROWTH_DRAFT"
# Ensure partner-pitch copy exists for splice target
if [[ ! -f "$PJ" ]]; then
  cp "$DC" "$PJ"
fi
python3 "$MODEL/growth_frontend_block.py" \
  --partner "$PARTNER" \
  --partner-json "$PJ" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --rollup "$RECAL/agg-$PARTNER.json" \
  --out "$GROWTH_DRAFT/$PARTNER.growth.json"

step "4 splice growth_case"
python3 "$FINANCE/splice_growth_into_partner.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --frontend "$GROWTH_DRAFT/$PARTNER.growth.json" \
  --partner-json "$PJ"
cp "$PJ" "$DC"

step "5 economics sidecar refresh"
python3 "$BY/build_economics_sidecar.py" \
  --dc "$ROOT/data-clean" \
  --corridors "$CORR" \
  --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json" || true

step "6 bind economics_url if known"
python3 - <<PY
import json, sys
from pathlib import Path
ROOT = Path("$ROOT")
PARTNER = "$PARTNER"
url_map = json.loads((ROOT/"finance/economics_url_map.json").read_text()).get("economics_url", {})
url = url_map.get(PARTNER)
if not url:
    print(f"  (no economics_url for {PARTNER})")
    sys.exit(0)
for rel in [f"partner-pitch/partners/{PARTNER}.json", f"data-clean/partners/{PARTNER}.json"]:
    p = ROOT / rel
    if not p.is_file():
        continue
    doc = json.loads(p.read_text())
    doc["economics_url"] = url
    if doc.get("growth_case"):
        doc["growth_case"].setdefault("_provenance", {})["economics_url"] = url
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
print(f"  economics_url → {url}")
PY

echo "✓ $PARTNER growth_case bound ($N corridors)"