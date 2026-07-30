#!/usr/bin/env python3
"""D9 Suffolk County / NYMTC deck plates (text-free, fail-closed).
  - suffolk-candidate-links: Pier11<->Sag Harbor + Pier11<->Montauk (long-range study candidates)
                             + East End locals (S11; right clear-space)
  - suffolk-horizon-today:   published Shelter Island lifeline crossings (South Ferry, North Ferry)
  - suffolk-horizon-tomorrow: today + Navier East End links (Sag Harbor<->North Haven,
                             Shelter Island Heights<->North Haven, Sag Harbor<->Montauk)
Routes strictly from data-clean/ROUTES.json. Run: python3 <script> /tmp/na"""
import importlib.util, json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/na").resolve()
BASE = ROOT / "scripts/grok-egypt/render_mx_eg_exact_route_maps_2026_07_23.py"
spec = importlib.util.spec_from_file_location("base_renderer", BASE)
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
OUT = ROOT / "deck-studio/assets/suffolk/city-maps"
RECEIPT = Path(__file__).resolve().parent / "SUFFOLK-DECK-MAPS-RECEIPT-2026-07-29.json"

P11_SAG = "rn-e2c8f0d3fe0d"     # Pier 11 <-> Long Wharf Sag Harbor (101.2 nm)
P11_MTK = "rn-1119113a9806"     # Pier 11 <-> Viking Fleet Dock Montauk (104.7 nm)
SOUTH_FERRY = "e__the-hamptons-east-end-usa__north-haven-south-ferry__shelter-island-south-ferry-dock"
NORTH_FERRY = "e__the-hamptons-east-end-usa__greenport-mitchell-park-marina__shelter-island-heights-north-ferry"
SAG_NH = "ics-1d6b5394c1"       # Sag Harbor <-> North Haven
SIH_NH = "ics-08828b9b14"       # Shelter Island Heights <-> North Haven
SAG_MTK = "ics-69383f7df3"      # Sag Harbor <-> Montauk

TODAY = [SOUTH_FERRY, NORTH_FERRY]
TOMORROW = TODAY + [SAG_NH, SIH_NH, SAG_MTK]

_orig_bbox = base.bbox
RIGHT_CLEAR = 0.30
def bbox_east(lines, pad, min_span):
    minx, miny, maxx, maxy = _orig_bbox(lines, pad, min_span)
    span_x = maxx - minx
    maxx += span_x * (RIGHT_CLEAR / (1 - RIGHT_CLEAR))
    return minx, miny, maxx, maxy

MAPS = {
  "suffolk-candidate-links": {
    "out": OUT / "suffolk-candidate-links-exact-route-map.png",
    "route_ids": [P11_SAG, P11_MTK, SAG_NH, SIH_NH, SAG_MTK],
    "pad": 0.06, "left_clear": 0.0, "min_span_deg": 0.05, "_east_clear": True,
  },
  "suffolk-horizon-today": {
    "out": OUT / "suffolk-horizon-today-exact-route-map.png",
    "route_ids": sorted(TODAY),
    "pad": 0.06, "left_clear": 0.0, "min_span_deg": 0.10,
  },
  "suffolk-horizon-tomorrow": {
    "out": OUT / "suffolk-horizon-tomorrow-exact-route-map.png",
    "route_ids": sorted(TOMORROW),
    "pad": 0.10, "left_clear": 0.0, "min_span_deg": 0.12,
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
      "renderer": "render_suffolk_deck_maps_2026_07_29.py (base: render_mx_eg_exact_route_maps_2026_07_23.py)",
      "today_route_ids": sorted(TODAY), "tomorrow_route_ids": sorted(TOMORROW),
      "results": results}, indent=1))
    print("FAIL" if fail else "ALL OK")
    return 1 if fail else 0
if __name__ == "__main__":
    raise SystemExit(main())
