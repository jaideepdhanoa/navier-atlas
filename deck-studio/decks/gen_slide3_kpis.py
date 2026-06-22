#!/usr/bin/env python3
"""
gen_slide3_kpis.py — deterministic slide-3 / TAM-ladder KPI sidecar generator.

USAGE:  python3 gen_slide3_kpis.py <partner>
        e.g. python3 gen_slide3_kpis.py bolt

INPUTS  (read-only, never hand-edit values out of these):
  finance/recal/agg-<partner>.json     -> rows[], rollup.grounded_floor_by_market, rollup.n_corridors_total
  finance/recal/growth-<partner>.json  -> grounded{}, estimated_total{}  (LB-254 ladder)
  deck-studio/decks/<partner>/market-scope.json  -> ordered focus markets + labels + flags

OUTPUT:
  deck-studio/decks/<partner>/slide3-kpis-<partner>.json

RULES:
  - NEVER hard-code a numeric value. Every number is read from the source files above.
  - Scenario keys are fixed: "grounded" (headline) and "estimated_total" (upside). Do not invent others.
  - SAM/TAM/platform-rev are dicts -> always take ["mid"]. Never low/high on the headline card.
  - Markets, order, labels, and gulf_slide_only come ONLY from market-scope.json (single source of scope truth).
  - If a market in scope is missing from the source files -> emit null KPIs for it, DO NOT guess. (null beats wrong.)
"""
import json, sys, datetime
from collections import defaultdict

partner = sys.argv[1]
REC = "finance/recal"
DECK = f"deck-studio/decks/{partner}"
agg = json.load(open(f"{REC}/agg-{partner}.json"))
grw = json.load(open(f"{REC}/growth-{partner}.json"))
scope = json.load(open(f"{DECK}/market-scope.json"))   # {"markets":[{"key","label","tag","gulf_slide_only"}, ...]}

rows = agg["rows"]
gf = agg["rollup"]["grounded_floor_by_market"]

cc = defaultdict(int); pax = defaultdict(float)
for r in rows:
    cc[r["market"]] += 1
    m = r.get("mid") or r.get("thin") or {}            # mid scenario preferred, thin fallback
    pax[r["market"]] += (m.get("pax_per_year") or 0)

def usd_m(v): return round((v or 0)/1e6, 2)
def usd_b(v): return round((v or 0)/1e9, 2)

def card(key):
    g = gf.get(key)
    if g is None:
        return None                                     # null beats confidently-wrong
    py = pax[key]
    return {
        "routes_mapped": cc[key],
        "addressable_pool_usd_m": usd_m(g.get("transport_spend_pool_yr")),
        "navier_rev_grounded_floor_usd_m": usd_m(g.get("market_rev_yr")),
        "fleet_at_floor": g.get("fleet", 0),
        "modeled_riders_per_day_floor": round(py/365),
        "co2_saved_t_yr": round(g.get("co2_saved_t_yr", 0)),
    }

def ladder(scen):
    s = grw[scen]
    mid = lambda x: x.get("mid") if isinstance(x, dict) else x
    return {
        "addressable_transport_spend_usd_m": usd_m(s["M_today_transport_spend_yr"]),
        "SOM_floor_navier_rev_usd_m": usd_m(s["SOM_floor_navier_transport_rev_yr"]),
        "SAM_navier_rev_mid_usd_b": usd_b(mid(s["SAM_navier_transport_rev_yr"])),
        "TAM_journey_gmv_mid_usd_b": usd_b(mid(s["TAM_journey_gmv_yr"])),
        "partner_platform_rev_mid_usd_b": usd_b(mid(s["partner_platform_rev_yr"])),
        "effective_capture": round(s.get("_eff_capture_floor", 0), 3),
        "is_captive": s.get("_is_captive"),
    }

markets = {}
for m in scope["markets"]:
    markets[m["key"]] = {
        "label": m["label"], "tag": m.get("tag"),
        "gulf_slide_only": m.get("gulf_slide_only", False),
        "kpis": card(m["key"]),
    }

out = {
    "_partner": partner,
    "_generated": datetime.date.today().isoformat(),
    "_source": f"finance/recal/agg-{partner}.json + growth-{partner}.json (LB-254 ladder)",
    "_provenance_note": "Grounded-floor = demand x fare x capture (~10% contested). Modeled, not measured; "
                        "labelled grounded floor. SAM/TAM are the LB-254 capture-correct ladder rungs. "
                        "Show grounded as headline; estimated_total is the with-cascade upside.",
    "_units": "usd_m = $M/yr; usd_b = $B/yr; pool = annual transport-spend across mapped corridors",
    "network_headline": {
        "routes_mapped_total": agg["rollup"]["n_corridors_total"],
        "grounded": ladder("grounded"),
        "estimated_total": ladder("estimated_total"),
    },
    "slide3_market_cards": markets,
}
out_path = f"{DECK}/slide3-kpis-{partner}.json"
json.dump(out, open(out_path, "w"), indent=2)
print(f"wrote {out_path}")
