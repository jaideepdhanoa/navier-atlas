#!/usr/bin/env bash
# Phase-3 pilot postflight — LB-224 v2 two-tier gate (matches atlas-external/postflight.sh §2).
set -uo pipefail

WORK="${1:-}"
if [ -z "$WORK" ]; then
  echo "usage: postflight_pilot.sh <work-root>" >&2
  exit 2
fi

DC="$WORK/atlas-repo/data-clean"
TOOLS="$WORK/partner-pitch/_tools"
QA_TOOL="${QA_TOOL:-$TOOLS/qa_land_crossing.py}"
QA_OVERLAY="${QA_OVERLAY:-$TOOLS/uae_gulf_land.wkb}"

HARD=0
ROUTE_FLOOR="${ROUTE_FLOOR:-5421}"
SEAL_FRESH_MIN=120

ok()   { printf '  \033[32mOK\033[0m   %s\n' "$*"; }
warn() { printf '  \033[33mWARN\033[0m %s\n' "$*"; }
fail() { printf '  \033[31mFAIL\033[0m %s\n' "$*"; HARD=1; }

printf '=== POSTFLIGHT PILOT %s ===\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

ROUTES="$DC/ROUTES.json"
if [ -f "$ROUTES" ]; then
  RC=$(python3 -c "import json;d=json.load(open('$ROUTES'));print(len(d) if isinstance(d,list) else len(d.get('features',[])))")
  if [ "${RC:-0}" -ge "$ROUTE_FLOOR" ]; then ok "route count $RC ≥ floor $ROUTE_FLOOR"
  else fail "route REGRESSION: $RC < floor $ROUTE_FLOOR"; fi
else fail "missing $ROUTES"; fi

BASELINE="$DC/qa_baseline.json"
ALLOWLIST="$DC/route_water_allowlist.json"
PRIOR_SEAL="$DC/SEAL.prior.json"

if [ -f "$QA_TOOL" ] && [ -f "$ROUTES" ]; then
  if ! python3 -c "import global_land_mask" 2>/dev/null; then
    warn "global_land_mask absent — installing for QA"
    pip install -q global-land-mask numpy shapely 2>/dev/null || true
  fi
  if command -v uv >/dev/null 2>&1; then
    QA_RUN=(uv run --quiet --with shapely,global-land-mask python3 "$QA_TOOL")
  else
    QA_RUN=(python3 "$QA_TOOL")
  fi
  # Report must be produced; exit code 1 only means flagged routes exist (Tier A/B decide).
  QA_LOG=$(mktemp)
  if ! "${QA_RUN[@]}" "$ROUTES" --threshold 0.05 --overlay "$QA_OVERLAY" --quiet \
      --out "$DC/qa_land_crossing_report.json" 2>"$QA_LOG"; then
    if [ ! -f "$DC/qa_land_crossing_report.json" ]; then
      fail "qa_land_crossing report not produced — $(tail -2 "$QA_LOG")"
    else
      ok "qa_land_crossing report produced (flagged routes present — Tier A/B gates apply)"
    fi
  else
    ok "qa_land_crossing clean (LB-224 v2 overlay)"
  fi
  rm -f "$QA_LOG"

  SUBSET_RES=$(python3 - "$ROUTES" "$DC/qa_land_crossing_report.json" "$PRIOR_SEAL" "$ALLOWLIST" <<'PY'
import json,sys,hashlib,os
routes_p, qa_p, prior_p, allow_p = sys.argv[1:5]
routes=json.load(open(routes_p))
def _rid(f):
    p=f.get("properties",f) if isinstance(f,dict) else {}
    return p.get("id") or p.get("route_id")
def _ghash(f):
    g=f.get("geometry",{}); return hashlib.sha256(json.dumps(g,sort_keys=True,separators=(",",":")).encode()).hexdigest()
feats = routes if isinstance(routes,list) else routes.get('features',[])
cur={_rid(f):_ghash(f) for f in feats}
prior={}
if os.path.exists(prior_p):
    ps=json.load(open(prior_p)).get("geom_hashes",{})
    prior=ps if isinstance(ps,dict) else {}
changed=set(rid for rid,h in cur.items() if prior.get(rid)!=h)
allow=set()
if os.path.exists(allow_p):
    try: allow=set(json.load(open(allow_p)).get("ids",[]))
    except Exception: allow=set()
qa=json.load(open(qa_p))
flagged=qa.get("flagged") or qa.get("offenders") or []
flagged_ids=set(r.get("id") for r in flagged if r.get("id"))
subset_hits=(changed & flagged_ids) - allow
print(f"subset_changed={len(changed)} subset_flagged={len(subset_hits)} prior_known={bool(prior)}")
for rid in sorted(subset_hits)[:10]: print("  -",rid)
sys.exit(0 if not subset_hits else 1)
PY
)
  SUBSET_EXIT=$?
  if [ $SUBSET_EXIT -eq 0 ]; then ok "Tier A subset: 0 NEW flags ($(echo "$SUBSET_RES"|head -1))"
  else fail "Tier A subset FLAGS:"; echo "$SUBSET_RES"; fi

  DELTA_RES=$(python3 - "$DC/qa_land_crossing_report.json" "$BASELINE" "$ALLOWLIST" <<'PY'
import json,sys,os
qa_p, base_p, allow_p = sys.argv[1:4]
qa=json.load(open(qa_p))
allow=set()
if os.path.exists(allow_p):
    try: allow=set(json.load(open(allow_p)).get("ids",[]))
    except Exception: allow=set()
flagged=qa.get("flagged") or qa.get("offenders") or []
flagged_ids=set(r.get("id") for r in flagged if r.get("id"))
effective=flagged_ids - allow
n_eff=len(effective)
if not os.path.exists(base_p):
    print(f"NO_BASELINE effective_flagged={n_eff}"); sys.exit(2)
base=json.load(open(base_p))
base_n=base.get("flagged_count",base.get("count",0))
print(f"effective_flagged={n_eff} baseline={base_n} delta={n_eff-base_n}")
sys.exit(0 if n_eff<=base_n else 1)
PY
)
  DELTA_EXIT=$?
  case $DELTA_EXIT in
    0) ok "Tier B delta within baseline ($DELTA_RES)";;
    2) fail "qa_baseline.json MISSING ($BASELINE)";;
    *) fail "Tier B delta REGRESSION: $DELTA_RES";;
  esac
else fail "QA tool or ROUTES missing"; fi

SEAL="$DC/SEAL.json"
if [ -f "$SEAL" ]; then
  AGE=$(python3 -c "import os,time;print(int((time.time()-os.path.getmtime('$SEAL'))/60))")
  if [ "${AGE:-999}" -le "$SEAL_FRESH_MIN" ]; then ok "SEAL.json fresh (${AGE} min)"
  else fail "SEAL.json STALE (${AGE} min)"; fi
  python3 -c "import json; s=json.load(open('$SEAL')); b=s.get('blobs',{}).get('ROUTES',{}); m=s.get('meta',{}); assert m.get('route_count')==b.get('count'), 'mismatch'" \
    && ok "meta.route_count == blobs.ROUTES.count" \
    || fail "meta.route_count mismatch blobs.ROUTES.count"
else fail "missing SEAL.json"; fi

for b in FEATURES_BY_TYPE.json ROUTES.json; do
  f="$DC/$b"
  if [ -f "$f" ] && [ "$(wc -c < "$f")" -gt 100 ]; then ok "blob $b ($(wc -c < "$f") bytes)"
  else fail "blob $b missing"; fi
done

RESEAL="$TOOLS/reseal_from_disk.py"
if [ -f "$RESEAL" ]; then
  python3 "$RESEAL" "$DC" --dry-run >/dev/null 2>&1 && ok "reseal_from_disk dry-run OK" \
    || fail "reseal_from_disk dry-run FAILED"
fi

printf '=== POSTFLIGHT %s ===\n' "$([ $HARD -eq 0 ] && echo PASS || echo FAIL)"
exit $HARD