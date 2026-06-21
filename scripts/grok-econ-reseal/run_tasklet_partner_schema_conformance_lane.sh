#!/usr/bin/env bash
# PR #57 — partner proposal schema conformance + renderer shorthand tolerance
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
SEAL_TAG="${SEAL_TAG:-#79bj-partner-schema-conformance}"

echo "→ Schema parity (runtime vs docs)"
python3 - <<'PY'
import hashlib
from pathlib import Path

runtime = Path("partner-pitch/schema/partner_proposal.schema.json")
docs = Path("docs/schema/partner_proposal.schema.json")
assert runtime.exists(), runtime
assert docs.exists(), docs
rh = hashlib.sha256(runtime.read_bytes()).hexdigest()
dh = hashlib.sha256(docs.read_bytes()).hexdigest()
if rh != dh:
    raise SystemExit(f"schema drift: runtime={rh[:12]} docs={dh[:12]}")
print(f"  runtime/docs schemas match ({rh[:12]}…)")
PY

echo "→ JSON parse check"
python3 - <<'PY'
import json
from pathlib import Path
for p in [
    Path("partner-pitch/schema/partner_proposal.schema.json"),
    Path("docs/schema/partner_proposal.schema.json"),
    Path("handoff/partner-map-model/partner-proposal-schema-conformance-pr57-2026-06-20.json"),
]:
    json.loads(p.read_text())
    print(f"  ok {p}")
PY

echo "→ Full partner proposal schema validation"
python3 "$ROOT/scripts/validate_partner_proposals.py"

echo "→ PR #56 use-case completeness (regression)"
python3 "$ROOT/scripts/audit_partner_proposal_use_cases.py"

echo "→ Partner page completeness + linkability QA"
python3 "$ROOT/scripts/audit_partner_page_qa.py" --write-tasklet-note

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

echo "→ Reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — PR #57 partner proposal schema conformance" \
  "partner-pitch/" \
  "docs/schema/" \
  "index.html" \
  "handoff/partner-map-model/"

echo "✓ partner schema conformance lane: $SEAL_TAG"