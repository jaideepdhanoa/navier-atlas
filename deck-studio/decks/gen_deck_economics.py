#!/usr/bin/env python3
"""
gen_deck_economics.py — deterministic deck VALUE generator (Grok-owned).

Produces every NUMBER a partner deck needs, pulled straight from the model engine
(finance/recal/agg-<partner>.json + finance/recal/growth-<partner>.json). No hand-typing,
no judgement. Pairs with deck-studio/decks/<partner>/economics-binding.json:
  binding  = WHERE  (object_ids per field)        <- already in repo
  this file = WHAT   (formatted value per field)   <- generated here
Grok joins value[slide][field] -> binding[slide][field].object_id -> style-preserving text op.

Emits, keyed to the binding's field names:
  - slide3_kpi      : the 4 network KPI cards  (+ six per-market cards for the slide-3 grid)
  - slide10_tam     : the 5 TAM-ladder rungs
  - economics_slides: per-market unit economics for every slide-7-family index
                      (revenue build, the 6-line flush-left OPEX, results)

Usage (run from repo root):
  python3 deck-studio/decks/gen_deck_economics.py <partner>
  python3 deck-studio/decks/gen_deck_economics.py grab --validate   # reproduce gold, write nothing

Sources (read-only, the ONLY origin of numbers):
  finance/recal/agg-<partner>.json        rows[] (per-corridor thin/mid/full), rollup
  finance/recal/growth-<partner>.json     grounded{} + estimated_total{} LB-254 ladder
  deck-studio/decks/<partner>/market-scope.json     ordered deck markets (scope source)
  deck-studio/decks/<partner>/economics-binding.json  which slides/fields exist
"""
import json, os, sys, datetime
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "finance"))
from partner_platform_rev import shows_platform_revenue  # noqa: E402

def P(*a): return os.path.join(ROOT, *a)

def money(x):
    return None if x is None else f"${x:,.0f}"
def pct(x):
    return None if x is None else f"{round(x*100)}%"
def f1(x):
    return None if x is None else f"{x:.1f}"

# ---- ladder formatting for headline KPIs / TAM rungs (M vs B autoscale) ----
def usd_compact(x):
    if x is None: return None
    a = abs(x)
    if a >= 1e9:  return f"${x/1e9:.1f}B"
    if a >= 1e6:  return f"${x/1e6:.0f}M"
    return f"${x:,.0f}"

# ---------- representative-corridor selection (deterministic) ----------
def representative_corridor(rows, market_key):
    """Deck slide-7-family shows ONE flagship corridor per market.
    Rule (fixed, no judgement): grounded corridors first, then by revenue_per_boat_yr desc.
    If no grounded corridor exists for the market, fall back to estimated, same sort.
    Returns the row dict or None."""
    cand = [r for r in rows if r.get("market") == market_key and not (r.get("is_dup") or r.get("status") == "duplicate")]
    if not cand:
        return None
    def keyf(r):
        grounded = 0 if r.get("status") == "grounded" else 1
        rev = (r.get("mid", {}) or {}).get("revenue_per_boat_yr") or 0
        return (grounded, -rev)
    cand.sort(key=keyf)
    return cand[0]

# ---------- per-slide econ field values from one corridor row ----------
def econ_fields(row):
    mid = row.get("mid", {}) or {}
    cc  = mid.get("cost_components", {}) or {}
    asmp = mid.get("assumptions", {}) or {}
    rev = mid.get("revenue_per_boat_yr")
    opex_total = mid.get("annual_opex")
    profit = mid.get("ebitda_per_boat_yr")
    dep = cc.get("depreciation_usd_yr")
    # capex derived from the model's OWN depreciation output (capex = dep * dep_years[20]);
    # this reproduces the region rule ($900K US/EU, $600K RoW) without re-encoding it.
    capex = round(dep * 20) if dep else None
    nm = row.get("nm")
    vessel = mid.get("vessel") or "N30 Pioneer II"
    pax_cap = asmp.get("pax_capacity")
    corridor = row.get("corridor")
    fare = mid.get("navier_fare_usd")
    margin = mid.get("margin")
    payback = mid.get("payback_years")
    co2 = mid.get("co2_saved_t_per_boat_yr")
    profitable = (profit or 0) > 0
    summary = None
    if rev is not None and opex_total is not None and profit is not None:
        summary = (f"{money(rev)} revenue  \u2212  {money(opex_total)} run cost  =  "
                   f"{money(profit)} profit / boat\u00b7yr  \u00b7  {pct(margin)} margin  \u00b7  "
                   f"{f1(payback) + ' yrs payback' if payback is not None else 'payback n/a'}")
    route_line = None
    if corridor:
        route_line = f"{corridor}  \u00b7  ~{round(nm)} nm  \u00b7  {vessel} ({pax_cap} seats)" if nm else f"{corridor}  \u00b7  {vessel} ({pax_cap} seats)"
    return {
        "title": (f"profitable from year one" if profitable else None),
        "route_line": route_line,
        "summary_line": summary,
        "trips_per_day": (str(mid.get("trips_per_day")) if mid.get("trips_per_day") is not None else None),
        "operating_days": (str(asmp.get("operating_days_yr")) if asmp.get("operating_days_yr") is not None else None),
        "revenue_legs": pct(asmp.get("revenue_leg_pct")),
        "seats_per_trip": f1(mid.get("pax_per_trip")),
        "paid_seats_yr": (f"{round(mid.get('pax_per_year')):,}" if mid.get("pax_per_year") is not None else None),
        "premium_fare": (f"{money(fare)} / seat" if fare is not None else None),
        "revenue_per_boat": money(rev),
        "opex_energy": money(cc.get("energy_usd_yr")),
        "opex_crew": money(cc.get("crew_usd_yr")),
        "opex_marina": money(cc.get("marina_overhead_usd_yr")),
        "opex_maintenance": money(cc.get("maintenance_usd_yr")),
        "opex_insurance": money(cc.get("insurance_usd_yr")),
        "opex_charging_berth": money(cc.get("charging_berth_usd_yr")),
        "opex_total": money(opex_total),
        "result_profit": money(profit),
        "result_margin": pct(margin),
        "result_capex": money(capex),
        "result_payback": (f"{f1(payback)} yrs" if payback is not None else None),
        "result_co2": (f"{f1(co2)} t" if co2 is not None else None),
    }

def main():
    if len(sys.argv) < 2:
        print("usage: gen_deck_economics.py <partner> [--validate]", file=sys.stderr); sys.exit(2)
    partner = sys.argv[1]
    validate = "--validate" in sys.argv

    agg = json.load(open(P("finance", "recal", f"agg-{partner}.json")))
    rows = agg.get("rows", [])

    if validate:
        # Reproduce gold: for each econ slide in the binding, find the row whose
        # revenue_per_boat matches the sample, then assert every formatted field matches.
        binding = json.load(open(P("deck-studio", "decks", partner, "economics-binding.json")))
        rev_index = {}
        for r in rows:
            v = (r.get("mid", {}) or {}).get("revenue_per_boat_yr")
            if v is not None:
                rev_index.setdefault(round(v), r)
        checks = passes = 0
        for s in binding.get("economics_slides", []):
            fld = s.get("fields", {})
            samp_rev = fld.get("revenue_per_boat", {}).get("sample_value")
            if not samp_rev: continue
            target = int(samp_rev.replace("$", "").replace(",", ""))
            row = rev_index.get(target)
            if not row:
                print(f"slide {s['slide_index']}: no row matches {samp_rev} (market changed) — skip"); continue
            got = econ_fields(row)
            for k in ["opex_energy","opex_crew","opex_marina","opex_maintenance","opex_total",
                      "result_profit","result_margin","result_payback","result_co2",
                      "trips_per_day","operating_days","revenue_legs","seats_per_trip","paid_seats_yr"]:
                if k in fld:
                    checks += 1
                    want = fld[k].get("sample_value")
                    if got.get(k) == want: passes += 1
                    else: print(f"  slide {s['slide_index']} {k}: gen={got.get(k)!r} gold={want!r}")
        print(f"VALIDATE {partner}: {passes}/{checks} field-formats reproduce gold")
        return

    scope = json.load(open(P("deck-studio", "decks", partner, "market-scope.json")))
    binding = json.load(open(P("deck-studio", "decks", partner, "economics-binding.json")))
    markets = scope["markets"]
    econ_slides = sorted([s["slide_index"] for s in binding.get("economics_slides", [])])

    # map econ slides (in index order) -> markets (in scope order)
    out_econ = {}
    for i, sidx in enumerate(econ_slides):
        if i < len(markets):
            mk = markets[i]
            row = representative_corridor(rows, mk["key"])
            if row is None:
                out_econ[str(sidx)] = {"status": "no_corridor_for_market_hold_null", "market": mk["label"], "fields": None}
            else:
                f = econ_fields(row)
                f["header_market"] = f"WHAT ONE BOAT EARNS \u00b7 {mk['label'].upper()}"
                if f.get("title"):
                    market_short = mk["label"].split(" \u2014 ")[0]
                    f["title"] = f"{market_short}: profitable from year one"
                out_econ[str(sidx)] = {"status": row.get("status"), "market": mk["label"],
                                       "corridor": row.get("corridor"), "route_id": row.get("route_id"),
                                       "fields": f}
        else:
            out_econ[str(sidx)] = {"status": "no_market_drop_slide", "market": None, "fields": None}

    # ---- slide-3 four network KPI cards + six per-market cards ----
    growth = json.load(open(P("finance", "recal", f"growth-{partner}.json")))
    def ladder(scn):
        d = growth.get(scn, {}) or {}
        return d
    g = ladder("grounded")
    rollup = agg.get("rollup", {}) or {}
    def mid(k):
        v = g.get(k); return v.get("mid") if isinstance(v, dict) else v
    pool = g.get("M_today_transport_spend_yr")
    som = g.get("SOM_floor_navier_transport_rev_yr")
    sam = mid("SAM_navier_transport_rev_yr")
    tam_marine = mid("marine_mobility_tam_yr")      # induced marine-transfer market (~4x SAM)
    journey_gmv = mid("TAM_journey_gmv_yr")          # + food/stays/experiences (~3x TAM)
    plat = mid("partner_platform_rev_yr")
    n_corr = rollup.get("n_corridors_total")

    slide3_cards = [
        {"value": (f"{n_corr}" if n_corr is not None else None),
         "meaning": "premium water corridors mapped from real demand"},
        {"value": usd_compact(pool), "meaning": "premium sea-transfer spend already moving on these lanes, per year"},
        {"value": (f"${som/1e6:.0f}M floor" if som else None), "meaning": "SOM floor — Navier fare, today's trips, ~10% capture"},
        {"value": usd_compact(tam_marine), "meaning": "marine-transfer TAM (induced market), mid of model band"},
    ]
    pj_path = P("partner-pitch", "partners", f"{partner}.json")
    partner_meta = json.load(open(pj_path)) if os.path.isfile(pj_path) else {}
    show_plat = shows_platform_revenue(partner_meta)
    slide10_rungs = [
        {"rung": "SOM", "value": usd_compact(som)},
        {"rung": "SAM", "value": usd_compact(sam)},
        {"rung": "TAM", "value": usd_compact(tam_marine)},
        {"rung": "Journey GMV", "value": usd_compact(journey_gmv)},
    ]
    if show_plat:
        slide10_rungs.append({"rung": "partner platform revenue", "value": usd_compact(plat)})

    # six per-market cards (slide-3 grid) — pax/day, pool, rev floor, fleet, co2
    gfm = rollup.get("grounded_floor_by_market", {}) or {}
    per_market = {}
    rows_by_mkt = defaultdict(list)
    for r in rows:
        rows_by_mkt[r.get("market")].append(r)
    for mk in markets:
        k = mk["key"]; m = gfm.get(k)
        if not m:
            per_market[k] = {"label": mk["label"], "gulf_slide_only": mk.get("gulf_slide_only", False), "kpis": None}
            continue
        pax_day = round(sum(((r.get("mid", {}) or {}).get("pax_per_year") or
                             (r.get("thin", {}) or {}).get("pax_per_year") or 0) for r in rows_by_mkt[k]) / 365)
        per_market[k] = {
            "label": mk["label"], "gulf_slide_only": mk.get("gulf_slide_only", False),
            "kpis": {
                "routes_mapped": sum(1 for r in rows_by_mkt[k]),
                "addressable_pool_usd_m": round((m.get("transport_spend_pool_yr") or 0)/1e6, 2),
                "navier_rev_floor_usd_m": round((m.get("market_rev_yr") or 0)/1e6, 2),
                "fleet_at_floor": m.get("fleet"),
                "modeled_riders_per_day_floor": pax_day,
                "co2_saved_t_yr": round(m.get("co2_saved_t_yr") or 0),
            },
        }

    out = {
        "_meta": {
            "doc": "Deterministic deck VALUE sidecar. Join field values onto economics-binding.json object_ids. "
                   "Every number is read from the model engine; none are hand-typed. "
                   "All figures are grounded-floor / modeled, not measured.",
            "partner": partner,
            "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sources": [f"finance/recal/agg-{partner}.json", f"finance/recal/growth-{partner}.json",
                        f"deck-studio/decks/{partner}/market-scope.json"],
            "representative_corridor_rule": "grounded first, then revenue_per_boat_yr desc",
            "capex_rule": "capex = model depreciation x 20yr dep-life (reproduces $900K US/EU, $600K RoW)",
            "opex_total_rule": "sum of the six flush-left OPEX lines (energy, crew, marina, maintenance, insurance, charging_berth)",
            "provenance_note": "grounded floor = demand x fare x ~10% capture; modeled, not a measured count",
        },
        "slide3_kpi": {"network_cards": slide3_cards, "per_market_cards": per_market},
        "slide10_tam": {"rungs": slide10_rungs},
        "economics_slides": out_econ,
    }
    outp = P("deck-studio", "decks", partner, f"deck-economics-values-{partner}.json")
    json.dump(out, open(outp, "w"), indent=2)
    print(f"wrote {outp}")
    filled = sum(1 for v in out_econ.values() if v.get("fields"))
    print(f"econ slides filled: {filled}/{len(econ_slides)} | per-market cards: {len(per_market)}")

if __name__ == "__main__":
    main()
