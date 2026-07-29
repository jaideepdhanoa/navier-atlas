#!/usr/bin/env python3
"""NYC EDC candidate-links plate v2 — right clear-space (S11 text panel sits right).
Routes strictly from data-clean/ROUTES.json. Run: python3 <script> /tmp/na"""
import importlib.util, json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/na").resolve()
BASE = ROOT / "scripts/grok-egypt/render_mx_eg_exact_route_maps_2026_07_23.py"
spec = importlib.util.spec_from_file_location("base_renderer", BASE)
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
OUT = ROOT / "deck-studio/assets/nyc-edc/city-maps"
RECEIPT = Path(__file__).resolve().parent / "NYC-EDC-CANDIDATE-MAP-V2-RECEIPT-2026-07-29.json"

# Wrap base.bbox: after normal pad/min-span, extend EAST so routes sit in left ~58%
_orig_bbox = base.bbox
RIGHT_CLEAR = 0.30
def bbox_east(lines, pad, min_span):
    minx, miny, maxx, maxy = _orig_bbox(lines, pad, min_span)
    span_x = maxx - minx
    maxx += span_x * (RIGHT_CLEAR / (1 - RIGHT_CLEAR))
    return minx, miny, maxx, maxy
base.bbox = bbox_east

MAPS = {
  "edc-candidate-links": {
    "out": OUT / "edc-candidate-links-exact-route-map.png",
    "route_ids": [
      "rn-0e2b916d3b8d",   # E 34th St <-> LGA Marine Air Terminal
      "ics-bdacfbafa1",    # Pier 11 <-> Paulus Hook
      "rn-5c8ceecea4d9",   # Pier 11 <-> North Williamsburg (candidate)
    ],
    "pad": 0.05, "left_clear": 0.0, "min_span_deg": 0.02,
  },
}
def main():
    by_id = base.load_routes()
    OUT.mkdir(parents=True, exist_ok=True)
    results, fail = [], False
    for key, cfg in MAPS.items():
        r = base.render_one(key, cfg, by_id)
        results.append(r)
        n = len(r.get("route_ids_resolved") or [])
        print(key, r.get("status"), r.get("file") or r.get("reason"), "routes", n)
        if r.get("status") != "ok" or n != len(cfg["route_ids"]): fail = True
    RECEIPT.write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(),
      "renderer": "render_nyc_edc_candidate_map_v2_2026_07_29.py (east clear-space patch)",
      "results": results}, indent=1))
    print("FAIL" if fail else "ALL OK")
    return 1 if fail else 0
if __name__ == "__main__":
    raise SystemExit(main())
