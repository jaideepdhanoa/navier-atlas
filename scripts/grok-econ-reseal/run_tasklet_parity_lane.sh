#!/usr/bin/env bash
# Complete Tasklet PR #46 + PR #48 — full finance cascade on de-duped registry
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

HANDOFF="${TASKLET_HANDOFF:-$ROOT/_ingest/tasklet-parity-2026-06-20}"
FINANCE_MODEL="$ROOT/finance/model"
FINANCE="$ROOT/finance"
RECAL="$FINANCE/recal"
ACTIVE_CORR="$FINANCE_MODEL/corridors.json"
BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
SEAL_TAG="${SEAL_TAG:-#79az-tasklet-finance-cascade}"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"

if [[ ! -f "$HANDOFF/grab.json" ]]; then
  echo "✗ missing $HANDOFF/grab.json" >&2
  exit 1
fi
if [[ ! -f "$FINANCE_MODEL/vessel-constants.json" ]]; then
  echo "✗ missing finance engine — merge PR #48 first" >&2
  exit 1
fi

mkdir -p "$GROWTH_DRAFT" "$RECAL"

echo "→ Promote Grab use-cases + canonical corridors (SEA de-dup + penang/borneo + turkey split)"
cp "$HANDOFF/grab.json" "$ROOT/data-clean/partners/grab.json"
mkdir -p "$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs"
cp "$ACTIVE_CORR" "$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"

echo "→ §B.0 country-reference preflight (bolt + yango)"
python3 - <<'PY'
import json
from pathlib import Path
corr = json.loads(Path("finance/model/corridors.json").read_text())["markets"]
cref = set(json.loads(Path("finance/model/country-reference.json").read_text())["countries"])
for prefix in ("bolt", "yango"):
    need = {m["country"] for k, m in corr.items() if k.startswith(f"{prefix}-") and m.get("country")}
    miss = sorted(need - cref)
    print(f"  {prefix}: missing={miss or 'none ✅'}")
PY

echo "→ Bolt vessel re-gate (Gate C.1)"
python3 "$ROOT/partner-pitch/subproposals/build_scaffold.py" >/dev/null 2>&1 || true

echo "→ Full 4-stage finance cascade (grab / bolt / yango)"
for p in grab bolt yango; do
  echo "  [$p] aggregate"
  python3 "$FINANCE_MODEL/aggregate.py" --partner "$p" --json "$RECAL/agg-$p.json" --corridors "$ACTIVE_CORR"
  echo "  [$p] growth"
  python3 "$FINANCE_MODEL/growth.py" --partner "$p" --agg "$RECAL/agg-$p.json" --json "$RECAL/growth-$p.json"
  echo "  [$p] frontend_block"
  python3 "$FINANCE_MODEL/growth_frontend_block.py" --partner "$p" \
    --growth "$RECAL/growth-$p.json" --rollup "$RECAL/agg-$p.json" \
    --out "$GROWTH_DRAFT/$p.growth.json"
  echo "  [$p] splice → data-clean"
  cp "$ROOT/data-clean/partners/$p.json" "$ROOT/partner-pitch/partners/$p.json"
  python3 "$FINANCE/splice_growth_into_partner.py" --partner "$p" \
    --growth "$RECAL/growth-$p.json" --frontend "$GROWTH_DRAFT/$p.growth.json" \
    --partner-json "$ROOT/data-clean/partners/$p.json"
  cp "$ROOT/data-clean/partners/$p.json" "$ROOT/partner-pitch/partners/$p.json"
done

echo "→ Economics sidecar + triage"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json"

python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
grab = json.loads(Path("data-clean/partners/grab.json").read_text())
uc = empty = 0
for m in grab.get("markets", []):
    for ph in m.get("phases", []):
        for u in ph.get("use_cases", []) or []:
            uc += 1
            if not (u.get("summary") or "").strip():
                empty += 1
agg = json.loads(Path("finance/recal/agg-grab.json").read_text())
gf = agg.get("rollup", {}).get("grounded_floor", {})
print(f"grab use_cases: {uc} total, {empty} empty")
print(f"grab grounded_floor: ${gf.get('market_rev_yr', 0)/1e6:.1f}M")
for p in ("bolt", "yango", "grab"):
    part = json.loads(Path(f"data-clean/partners/{p}.json").read_text())
    gc = part.get("growth_case", {})
    rungs = (gc.get("revenue_potential") or {}).get("rungs") or []
    lt = len(gc.get("ladder_transitions") or [])
    chips = gc.get("_render_chip_flag") or gc.get("revenue_potential", {}).get("_render_chip_flag")
    print(f"{p}: rungs={len(rungs)} ladder_transitions={lt} marine_tam={'yes' if gc.get('marine_mobility_tam') else 'no'}")
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — PR #48 finance cascade + PR #46 Grab/Bolt/Yango TAM refresh" \
  "$HANDOFF/" "finance/"

echo "✓ tasklet parity lane: $SEAL_TAG"