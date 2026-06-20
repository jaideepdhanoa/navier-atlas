#!/usr/bin/env bash
# PR #56 — partner proposal use-case completeness + Phase 3 promotion gate
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
SEAL_TAG="${SEAL_TAG:-#79bi-partner-use-case-completeness}"

echo "→ JSON parse check (touched partner-pitch + handoff)"
python3 - <<'PY'
import json
from pathlib import Path

paths = list(Path("partner-pitch/partners").glob("*.json"))
paths += [
    Path("partner-pitch/schema/partner_proposal.schema.json"),
    Path("handoff/partner-map-model/partner-proposal-use-case-backfill-pr56-2026-06-20.json"),
    Path("handoff/partner-map-model/partner-coverage-phase-3-shared-registry-gap-queue-2026-06-20.json"),
]
for p in paths:
    if p.exists():
        json.loads(p.read_text())
        print(f"  ok {p}")
PY

echo "→ Use-case completeness audit"
python3 "$ROOT/scripts/audit_partner_proposal_use_cases.py"

echo "→ index.html script syntax"
node --check <(python3 - <<'PY'
import re
from pathlib import Path
html = Path("index.html").read_text()
m = re.search(r"<script>(.*?)</script>", html, re.S)
if not m:
    raise SystemExit("no inline script block found")
print(m.group(1))
PY
)

echo "→ Build-site smoke"
node "$ROOT/scripts/build-site.mjs" 2>&1 | tail -5

echo "→ Reseal (data-clean unchanged; stamp gate)"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — PR #56 partner proposal use-case completeness" \
  "partner-pitch/" \
  "index.html" \
  "handoff/partner-map-model/"

echo "✓ partner use-case completeness lane: $SEAL_TAG"