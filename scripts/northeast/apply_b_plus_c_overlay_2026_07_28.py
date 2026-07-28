#!/usr/bin/env python3
"""B+C overlay (Jaideep 2026-07-28) on the usa-ny-harbor / usa-new-england markets.

B — re-anchor fares against Uber Black / premium substitutes
    (sources: northeast-program/census/UBER-BLACK-BENCHMARKS.md).
C — N45 (20-pax hybrid, $2.5M US/EU capex) on dense corridors where the N30
    cannot clear the ~3yr payback threshold; cheapest clearing hull wins.
Corridors that cannot clear ~3yr at a credible premium anchor on EITHER hull
are held (_economics_hold_reason) per the Northeast program rule.

Run AFTER build_usa_northeast_market_2026_07_28.py --apply:
    python3 apply_b_plus_c_overlay_2026_07_28.py /tmp/na --apply
"""
import json, sys

# route_id -> (new_fare, fare_basis, vessel_key or None=N30, hold_reason or None)
OVERLAY = {
  # --- usa-ny-harbor ---
  "rn-0e2b916d3b8d": (75, "Approved anchor 2026-07-28; sits between Uber Black E34th->LGA (~$48-100/vehicle, TaxiFareFinder 2026) and Blade heli $195-275/seat. N30 clears at 2.12yr.",
                      None, None),
  "rn-5c8ceecea4d9": (35, "Uber Black Pier 11 -> N Williamsburg $37.63/vehicle (TaxiFareFinder 2026); $35/seat is the credible ceiling.",
                      "n45", "HOLD (payback threshold): fails ~3yr on both hulls at the credible $35 anchor — N45 payback 4.84yr. Ceiling = whole Uber Black vehicle $37.63. Jaideep 2026-07-28 B+C."),
  "ics-bdacfbafa1":  (50, "Uber Black Pier 11 -> Paulus Hook $56.26/vehicle (TaxiFareFinder 2026); anchored $50/seat.",
                      "n45", None),
  # Quanta pair: stays range-gated (roadmap) until Navier locked Quanta hybrid pax/speed spec lands.
  # --- usa-new-england ---
  "rn-6e97c92755a8": (65, "Uber Black Long Wharf -> Hingham Shipyard $70.44/vehicle (TaxiFareFinder 2026); anchored $65/seat.",
                      "n45", None),
  "ics-3b05a4e262":  (70, "Uber Black Long Wharf -> Salem $77.53/vehicle (RideGuru 2026); anchored $70/seat.",
                      "n45", None),
  "ics-4df4cecf34":  (115, "Premium substitute band: Bay State fast ferry $92-107/seat incl. fuel surcharge; Cape Air BOS-PVC $119-259/seat; Uber Black ~$466/vehicle. Anchored $115/seat (ferry-premium, bottom of air band).",
                      "n45", "HOLD (payback threshold): N45 payback 6.80yr at $115. Clearing 3yr needs ~$174/seat — 1.7x the fast-ferry seat; not credibly anchored. Jaideep 2026-07-28 B+C."),
  "rn-b1104ed2e1eb": (25, "Uber Black Long Wharf -> Logan $29.56/vehicle (TaxiFareFinder 2026); today's harbor water taxi ~$20/seat. Anchored $25/seat.",
                      "n45", "HOLD (payback threshold): N45 payback 11.1yr at $25; clearing 3yr needs ~$46/seat vs a $29.56 whole Uber Black vehicle. Jaideep 2026-07-28 B+C."),
  "e__boston-new-england-usa__hyannis-terminal__nantucket-steamship-wharf":
                     (85, "Premium substitute band: Cape Air HYA-ACK $69-99/seat; Hy-Line fast ferry $52-61/seat. Anchored $85/seat (mid-air band).",
                      "n45", "HOLD (payback threshold, borderline): N45 payback 3.95yr at $85; clears 3.0yr only at ~$99-100/seat = very top of the sourced Cape Air band. Escalated to Jaideep as borderline. Jaideep 2026-07-28 B+C."),
  "ics-c7c6e76d27":  (60, "Premium substitute band: Cape Air to MVY ~$59/seat (Hyannis-origin proxy); Falmouth-Edgartown premium fast boat $35-45/seat; SSA $11 (subsidized, not the comparable). Anchored $60/seat.",
                      "n45", None),
  "rn-ba49e90cdbec": (55, "Seastreak NB -> Oak Bluffs $49/seat (2026, plus peak surcharges); anchored $55/seat premium.",
                      "n45", "HOLD (payback threshold): N45 payback 21.8yr at $55 — 27nm leg, low frequency; clearing 3yr needs ~$117/seat vs $49 Seastreak. Jaideep 2026-07-28 B+C."),
}
N45_CAPEX = 2_500_000  # Jaideep 2026-07-28: N45 $2.5M US/EU premium markets

def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else "/tmp/na"
    apply = "--apply" in sys.argv
    p = f"{repo}/finance/model/corridors.json"
    c = json.load(open(p))
    touched = 0
    for mk in ("usa-ny-harbor", "usa-new-england"):
        for cor in c["markets"][mk]["corridors"]:
            rid = cor.get("route_id")
            if rid not in OVERLAY:
                continue
            fare, basis, vk, hold = OVERLAY[rid]
            L = cor["L3_locals"]
            L["comparable_fare_usd_pax"] = fare
            L["_fare_anchor_basis"] = basis
            if vk:
                cor["vessel_key"] = vk
                L["capex_usd_override"] = N45_CAPEX
            if hold:
                cor["_economics_hold_reason"] = hold
            else:
                cor.pop("_economics_hold_reason", None)
            touched += 1
            print(f"{rid[:44]:46s} fare ${fare:>3} hull {vk or 'pioneer_ii(N30)':16s} {'HOLD' if hold else 'ACTIVE'}")
    print(f"touched {touched}/10 (Quanta pair untouched: range-gated pending locked spec)")
    if apply:
        json.dump(c, open(p, "w"), indent=1, ensure_ascii=False)
        print("APPLIED")

if __name__ == "__main__":
    main()
