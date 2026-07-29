#!/usr/bin/env python3
"""D7 Steamship Authority deck plates (text-free, fail-closed).
  - ssa-candidate-links: Woods Hole<->Vineyard Haven + Hyannis<->Nantucket + New Bedford<->Oak Bluffs (S11; right clear-space)
  - ssa-horizon-today:   SSA published network (WH<->VH, WH<->OB, Hyannis<->Nantucket)
  - ssa-horizon-tomorrow: today + New Bedford<->Oak Bluffs study candidate
Routes strictly from data-clean/ROUTES.json. Run: python3 <script> /tmp/na"""
import importlib.util, json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/na").resolve()
BASE = ROOT / "scripts/grok-egypt/render_mx_eg_exact_route_maps_2026_07_23.py"
spec = importlib.util.spec_from_file_location("base_renderer", BASE)
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
OUT = ROOT / "deck-studio/assets/steamship/city-maps"
RECEIPT = Path(__file__).resolve().parent / "SSA-DECK-MAPS-RECEIPT-2026-07-29.json"

WH_VH = "ics-c7c6e76d27"
HY_NAN = "e__boston-new-england-usa__hyannis-terminal__nantucket-steamship-wharf"
NB_OB = "rn-ba49e90cdbec"
WH_OB = "rn-ssa-wh-oakbluffs"

TODAY = [WH_VH, WH_OB, HY_NAN]
TOMORROW = TODAY + [NB_OB]

_orig_bbox = base.bbox
RIGHT_CLEAR = 0.30
def bbox_east(lines, pad, min_span):
    minx, miny, maxx, maxy = _orig_bbox(lines, pad, min_span)
    span_x = maxx - minx
    maxx += span_x * (RIGHT_CLEAR / (1 - RIGHT_CLEAR))
    return minx, miny, maxx, maxy

MAPS = {
  "ssa-candidate-links": {
    "out": OUT / "ssa-candidate-links-exact-route-map.png",
    "route_ids": [WH_VH, HY_NAN, NB_OB],
    "pad": 0.06, "left_clear": 0.0, "min_span_deg": 0.05, "_east_clear": True,
  },
  "ssa-horizon-today": {
    "out": OUT / "ssa-horizon-today-exact-route-map.png",
    "route_ids": sorted(TODAY),
    "pad": 0.10, "left_clear": 0.0, "min_span_deg": 0.10,
  },
  "ssa-horizon-tomorrow": {
    "out": OUT / "ssa-horizon-tomorrow-exact-route-map.png",
    "route_ids": sorted(TOMORROW),
    "pad": 0.10, "left_clear": 0.0, "min_span_deg": 0.10,
  },
}
def main():
    by_id = base.load_routes()
    OUT.mkdir(parents=True, exist_ok=True)
    results, fail = [], False
    for key, cfg in MAPS.items():
        base.bbox = bbox_east if cfg.pop("_east_clear", False) else _orig_bbox
        r = base.render_one(key, cfg, by_id)
        results.append(r)
        n = len(r.get("route_ids_resolved") or [])
        print(key, r.get("status"), r.get("file") or r.get("reason"), "routes", n)
        if r.get("status") != "ok" or n != len(cfg["route_ids"]): fail = True
    base.bbox = _orig_bbox
    RECEIPT.write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(),
      "renderer": "render_ssa_deck_maps_2026_07_29.py (base: render_mx_eg_exact_route_maps_2026_07_23.py)",
      "today_route_ids": sorted(TODAY), "tomorrow_route_ids": sorted(TOMORROW),
      "results": results}, indent=1))
    print("FAIL" if fail else "ALL OK")
    return 1 if fail else 0
if __name__ == "__main__":
    raise SystemExit(main())
