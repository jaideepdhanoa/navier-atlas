#!/usr/bin/env bash
# Run Bite-2 ladder cascade for all partners in LADDER-CASCADE-WORKLIST.json
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-bite2"
WORKLIST="$ROOT/data-clean/_handoff/bite2/LADDER-CASCADE-WORKLIST.json"
REPORT="$ROOT/handoff/partner-map-model/bite2-cascade-report.json"
LANE="$SCRIPTS/run_partner_cascade.sh"
chmod +x "$LANE" "$SCRIPTS/run_bite2_batch.sh"

python3 - <<'PY' "$WORKLIST" "$REPORT" "$LANE"
import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

worklist = json.loads(Path(sys.argv[1]).read_text())
report_path = Path(sys.argv[2])
lane = sys.argv[3]
results = []
ok = fail = skip = 0

for pid in worklist["priority_order"]:
    item = next(x for x in worklist["worklist"] if x["partner"] == pid)
    lt = item["ladder_type"]
    print(f"\n######## {pid} ({lt}) ########", flush=True)
    try:
        r = subprocess.run([lane, pid, lt], cwd=Path(lane).parents[2], check=False)
        if r.returncode == 0:
            ok += 1
            status = "bound"
        elif r.returncode == 2:
            skip += 1
            status = "skipped_no_corridors"
        else:
            fail += 1
            status = "failed"
    except Exception as e:
        fail += 1
        status = f"error:{e}"
    # verify
    dc = Path(lane).parents[2] / f"data-clean/partners/{pid}.json"
    has_gc = False
    if dc.is_file():
        has_gc = bool(json.loads(dc.read_text()).get("growth_case"))
    results.append({"partner": pid, "ladder_type": lt, "status": status, "growth_case": has_gc})

out = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "ok": ok,
    "fail": fail,
    "skip": skip,
    "results": results,
}
report_path.write_text(json.dumps(out, indent=2) + "\n")
print(f"\n=== Bite-2 batch: ok={ok} fail={fail} skip={skip} ===")
print(f"report → {report_path}")
PY