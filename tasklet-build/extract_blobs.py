#!/usr/bin/env python3
"""Extract the 4 render blobs from the shipped index.html into _ingest/data-clean/.
Factored out of release.sh so the seal always reflects exactly what shipped.
Blobs are baked as `const NAME = <json>;` lines in template.html."""
import re, json, pathlib

HERE = pathlib.Path(__file__).parent
html = (HERE / "index.html").read_text()
DC = HERE.parent / "_ingest" / "data-clean"
DC.mkdir(parents=True, exist_ok=True)

# Map: JS const name -> output filename
WANT = {
    "FEATURES_BY_TYPE": "FEATURES_BY_TYPE.json",
    "ROUTES":           "ROUTES.json",
    "STORIES":          "STORIES.json",
    "VESSEL_SPECS":     "VESSEL_SPECS.json",
}

def grab(name):
    # match `const NAME = <json>;`  (json is an object or array, possibly large)
    m = re.search(r"const\s+" + re.escape(name) + r"\s*=\s*(\{.*?\}|\[.*?\]);", html, re.DOTALL)
    if not m:
        raise SystemExit(f"❌ extract_blobs: could not find const {name}")
    return m.group(1)

for name, fn in WANT.items():
    raw = grab(name)
    obj = json.loads(raw)          # validate it parses
    (DC / fn).write_text(json.dumps(obj, ensure_ascii=False))
    n = len(obj) if isinstance(obj, (list, dict)) else "?"
    print(f"  extracted {name} -> {fn} ({n} items)")
print("extract_blobs ✅")
