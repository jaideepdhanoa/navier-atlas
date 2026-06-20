#!/usr/bin/env bash
# PR #53 + #54 — partner map model: materialize footprint scope, ID aliases, build verify
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

SEAL_TAG="${SEAL_TAG:-#79bg-partner-map-model}"

echo "→ Materialize _map_scope from seal-scope handoff"
python3 "$ROOT/scripts/materialize_partner_map_scope.py" bolt yango

echo "→ ID alias fixes (crosswalk remaining_for_grok_id_alias_only)"
python3 - <<'PY'
import json
from pathlib import Path

ALIASES = {
    "dammam-khobar-ksa": "eastern-province-ksa",
    "redsea-egypt": "hurghada-el-gouna-egypt",
}

def fix_obj(o):
    if isinstance(o, dict):
        return {k: fix_obj(v) for k, v in o.items()}
    if isinstance(o, list):
        return [fix_obj(x) for x in o]
    if isinstance(o, str) and o in ALIASES:
        return ALIASES[o]
    return o

for slug in ("bolt", "yango"):
    p = Path(f"data-clean/partners/{slug}.json")
    d = json.loads(p.read_text())
    fixed = fix_obj(d)
    p.write_text(json.dumps(fixed, indent=2, ensure_ascii=False) + "\n")
    pp = Path(f"partner-pitch/partners/{slug}.json")
    if pp.parent.exists():
        pp.write_text(p.read_text())
    print(f"  ✓ {slug}: anchor aliases applied")
PY

echo "→ Build-site smoke (bolt hub scope)"
node "$ROOT/scripts/build-site.mjs" 2>&1 | grep -E "bolt|yango|ABORT|FATAL" | head -20

echo "✓ partner map lane: $SEAL_TAG"