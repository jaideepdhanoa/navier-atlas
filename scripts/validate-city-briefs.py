#!/usr/bin/env python3
"""
validate-city-briefs.py — completeness gate for partner-pitch city briefs.

Enforces the FP/UAE "gold" standard so partial briefs (empty "Why marine
mobility here" / "Use cases" sections, flat navier_fit, missing sources)
can never silently reach a partner deck again.

Usage:
    python3 scripts/validate-city-briefs.py [--strict] [path/to/city_briefs]

Exit code 1 if any brief fails (use in CI / pre-handoff gate).
"""
import json, glob, os, sys

DIR = sys.argv[-1] if not sys.argv[-1].startswith("--") and os.path.isdir(sys.argv[-1]) \
    else "partner-pitch/city_briefs"
STRICT = "--strict" in sys.argv

def check(d):
    f = []
    uc = d.get("use_cases")
    if not uc:
        f.append("no use_cases (renders empty 'Use cases')")
    elif any(isinstance(x, str) for x in uc):
        f.append("use_cases are bare strings — need {archetype,title,body,platform}")
    elif any(not (isinstance(x, dict) and x.get("body")) for x in uc):
        f.append("use_cases missing 'body'")

    nf = d.get("navier_fit")
    if not nf:
        f.append("no navier_fit (renders empty 'Why marine mobility here')")
    elif isinstance(nf, str):
        f.append("navier_fit is a flat string — need {pioneer_ii, quanta_lr}")
    elif not (nf.get("pioneer_ii") and nf.get("quanta_lr")):
        f.append("navier_fit missing pioneer_ii and/or quanta_lr")

    ds = d.get("demand_signals")
    if not ds:
        f.append("no demand_signals")
    elif len(ds) < 3:
        f.append(f"demand_signals thin ({len(ds)}; want >=3)")

    s = d.get("summary", "")
    if len(s) < 250:
        f.append(f"summary thin ({len(s)} chars; want >=250)")

    if not d.get("journeys"):
        f.append("no journeys")
    if not d.get("sources"):
        f.append("no sources (unverifiable)")
    return f

def main():
    files = [x for x in sorted(glob.glob(os.path.join(DIR, "*.json")))
             if not x.endswith("_index.json")]
    bad = {}
    for fp in files:
        try:
            d = json.load(open(fp))
        except Exception as e:
            bad[fp] = [f"invalid JSON: {e}"]
            continue
        iss = check(d)
        if iss:
            bad[fp] = iss
    print(f"Audited {len(files)} briefs — {len(bad)} incomplete, "
          f"{len(files)-len(bad)} at gold standard.\n")
    for fp in sorted(bad):
        print(f"  ✗ {os.path.basename(fp)}")
        for i in bad[fp]:
            print(f"      - {i}")
    if bad and STRICT:
        sys.exit(1)

if __name__ == "__main__":
    main()
