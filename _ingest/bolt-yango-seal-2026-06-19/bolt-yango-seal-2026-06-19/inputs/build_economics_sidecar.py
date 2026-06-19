#!/usr/bin/env python3
"""
Build economics_by_route_id.json — the route-keyed unit-economics sidecar that
Claude's build joins onto Atlas route features (D0 styling / D1 corridor card / D2 roll-up).

Source of truth = the SAME engine the transparent Sheet uses (aggregate.py per-partner rows).
Route-ID resolution is ID-based only (exactness mandate): a record is emitted ONLY when its
corridor resolves to a real gold route_id — via the corridor's own route_id (present in gold)
or an exact unordered endpoint {from_node_id,to_node_id} match. No fuzzy matching. No guessing.

Usage:
  python3 build_economics_sidecar.py \
     --gold /tmp/v12/data-clean --aggdir /tmp --out /tmp/economics_by_route_id.json
"""
import json, os, sys, datetime
from collections import Counter

def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag)+1] if flag in sys.argv else default

GOLD   = arg("--gold", "/tmp/v12/data-clean")
AGGDIR = arg("--aggdir", "/tmp")
OUT    = arg("--out", "/tmp/economics_by_route_id.json")
PARTNERS = ["grab", "careem", "jih-global", "red-sea-global", "saudi-redsea-pif", "qatar"]

# Partner -> deck / model link surfaced on the card's "see the full model" CTA. null = honest blank.
DECK_URL = {
    "grab": "https://docs.google.com/spreadsheets/d/1ACYTZar0odZCASzKUwo1A4rXGsCsz6Luec6Cu3vQ20w/edit",
}

# ---- gold geometry: route_id set + unordered-endpoint index ----
R = json.load(open(os.path.join(GOLD, "ROUTES.json")))
feats = R["features"] if isinstance(R, dict) and "features" in R else R
gold_rids = set()
pair2id = {}
for f in feats:
    p = f["properties"]; rid = p.get("id")
    gold_rids.add(rid)
    a, b = p.get("from"), p.get("to")
    if a and b:
        pair2id.setdefault(frozenset((a, b)), rid)

# ---- corridors.json: per-corridor route-id resolution (ID-based only) ----
corr = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model", "corridors.json")))
resolved = {}            # (market, label) -> route_id
unresolved_detail = {}   # (market, label) -> reason
corr_country = {}        # (market, label) -> country  (corridors.json is source of truth;
                         # never trust the agg row's country — it can carry a stale template value,
                         # e.g. UAE corridors once shipped country="Singapore" from a copy-paste seed.)
for mid_k, mk in corr["markets"].items():
    partner = mk.get("partner", "grab")
    for c in mk["corridors"]:
        label = f"{c.get('from')} -> {c.get('to')}"
        key = (mid_k, label)
        corr_country[key] = c.get("country")
        rid = c.get("route_id")
        a, b = c.get("from_node_id"), c.get("to_node_id")
        is_asp = bool(c.get("aspirational"))
        if rid and rid in gold_rids:
            resolved[key] = rid
        elif a and b and frozenset((a, b)) in pair2id:
            resolved[key] = pair2id[frozenset((a, b))]
        else:
            # LB-169: intra-city aspirational chips have a==b at city-resolution (both bp-* in same city,
            # or both literal city slug). No edge exists between a city and itself in ROUTES.json by design,
            # so don't flag as a binding failure — label honestly as aspirational_intra_city.
            # LB-170: corridors carrying explicit `aspirational: true` and no built edge are aspirational
            # by design (declared, not a binding miss) — label inter-city honestly.
            if a and b and a == b:
                why = "aspirational_intra_city"
            elif is_asp:
                why = "aspirational_declared"
            else:
                why = "route_id_not_in_gold" if rid else (
                      "endpoints_city_level_not_pinned" if (a and b) else "no_endpoints")
            unresolved_detail[key] = {"partner": partner, "reason": why}

def num(x):
    return None if x is None else round(float(x), 2)

# Collect every route-pinned corridor; multiple corridor concepts can collapse onto one
# gold route line (shared boarding points / hub-spoke representation). Group by route_id so
# nothing is dropped: headline = highest market-rev corridor; the rest go in also_serves.
from collections import defaultdict as _dd
by_rid = _dd(list)
pending = []

for partner in PARTNERS:
    # LB-152: accept both naming conventions + partner aliases
    # (in-tree files use `{partner}-aggregate.json`; recal/ uses `agg-{partner}.json`)
    ALIASES = {
        "saudi-redsea": "saudi-redsea-pif",
        "grab-aggregate-results": "grab",
    }
    p_resolved = ALIASES.get(partner, partner)
    candidates = [
        os.path.join(AGGDIR, f"agg-{p_resolved}.json"),
        os.path.join(AGGDIR, f"{p_resolved}-aggregate.json"),
        os.path.join(AGGDIR, f"agg-{partner}.json"),
        os.path.join(AGGDIR, f"{partner}-aggregate.json"),
    ]
    path = next((c for c in candidates if os.path.exists(c)), candidates[0])
    if not os.path.exists(path):
        continue
    rows = json.load(open(path)).get("rows", [])
    for row in rows:
        if row.get("status") == "duplicate" or row.get("is_dup"):
            continue
        market = row.get("market"); label = row.get("corridor")
        key = (market, label)
        mid = row.get("mid", {})
        rid = resolved.get(key)
        if not rid and mid.get("route_id") in gold_rids:
            rid = mid.get("route_id")
        if not rid:
            pending.append({"partner": partner, "market": market, "corridor": label,
                            "status": row.get("status"),
                            "reason": unresolved_detail.get(key, {}).get("reason", "unresolved")})
            continue
        by_rid[rid].append((partner, row))

MARKET_DISPLAY = {
    "singapore":"Singapore", "cross-border":"Cross-Border", "bali":"Bali",
    "phuket":"Phuket", "philippines":"Philippines", "vietnam":"Vietnam",
    "cambodia":"Cambodia", "borneo":"Borneo", "penang":"Penang", "jakarta":"Jakarta",
    "taiwan":"Taiwan", "saudi-redsea":"Saudi \u2013 Red Sea",
    "saudi-redsea-resort":"Saudi \u2013 Red Sea (Resort)",
    "uae-careem":"UAE (Careem)", "uae-luxury":"UAE (Luxury)",
    "maldives-jih":"Maldives (JIH)",
}
def mkt_disp(mid): return MARKET_DISPLAY.get(mid, (mid or "").replace("-"," ").title())

def corridor_block(row):
    mid = row.get("mid", {}); thin = row.get("thin", {}); full = row.get("full", {})
    # country: corridors.json is authoritative; only fall back to the row when absent there.
    auth_country = corr_country.get((row.get("market"), row.get("corridor")))
    return {
        "corridor": row.get("corridor"),
        "market": mkt_disp(row.get("market")),
        "country": auth_country if auth_country is not None else row.get("country"),
        "distance_nm": row.get("nm"),
        "status": row.get("status"),
        "demand_confidence": row.get("demand_conf"),
        "fare_today_usd": mid.get("comparable_fare_usd"),
        "navier_fare_usd": mid.get("navier_fare_usd"),
        "vessel": mid.get("vessel"),
        "mid": {
            "rev_per_boat_yr": num(mid.get("revenue_per_boat_yr")),
            "margin": num(mid.get("margin")),
            "payback_years": num(mid.get("payback_years")),
            "co2_saved_t_per_boat_yr": num(mid.get("co2_saved_t_per_boat_yr")),
            "vessels_10pct": mid.get("vessels_supported_10pct"),
            "market_rev_yr": num(mid.get("market_revenue_yr")),
        },
        "band": {
            "payback_years": [num(thin.get("payback_years")), num(mid.get("payback_years")), num(full.get("payback_years"))],
            "vessels_10pct": [thin.get("vessels_supported_10pct"), mid.get("vessels_supported_10pct"), full.get("vessels_supported_10pct")],
        },
        "estimation_basis": row.get("est_basis"),
        # --- G51: operating assumptions surfaced from atom.py internals (not re-derived).
        # Render on the corridor card so it is explicit we are NOT assuming 100% occupancy
        # 365 days/yr: one-way/cycle time, trips/day derivation, operating days/yr
        # (= 365 x mechanical uptime x weather), revenue-leg factor, load factor, capacity.
        "assumptions": mid.get("assumptions"),
        "breakdown": {
            "revenue_build": {
                "comparable_fare_usd": mid.get("comparable_fare_usd"),
                "navier_fare_usd": mid.get("navier_fare_usd"),
                "pax_capacity": (mid.get("revenue_inputs") or {}).get("pax_capacity"),
                "load_factor": (mid.get("revenue_inputs") or {}).get("load_factor"),
                "pax_per_trip": mid.get("pax_per_trip"),
                "trips_per_day": mid.get("trips_per_day"),
                "trips_per_year": mid.get("trips_per_year"),
                "pax_per_year": mid.get("pax_per_year"),
                "revenue_per_boat_yr": num(mid.get("revenue_per_boat_yr")),
            },
            "run_cost": {
                "energy_usd_yr": num((mid.get("cost_components") or {}).get("energy_usd_yr")),
                "crew_usd_yr": num((mid.get("cost_components") or {}).get("crew_usd_yr")),
                "marina_overhead_usd_yr": num((mid.get("cost_components") or {}).get("marina_overhead_usd_yr")),
                "maintenance_usd_yr": num((mid.get("cost_components") or {}).get("maintenance_usd_yr")),
                "annual_opex_usd_yr": num(mid.get("annual_opex")),
                "depreciation_usd_yr": num((mid.get("cost_components") or {}).get("depreciation_usd_yr")),
            },
            "result": {
                "ebitda_per_boat_yr": num(mid.get("ebitda_per_boat_yr")),
                "margin": num(mid.get("margin")),
                "payback_years": num(mid.get("payback_years")),
                "co2_saved_t_per_boat_yr": num(mid.get("co2_saved_t_per_boat_yr")),
            },
        },
        "provenance": {
            "fare": "comparable premium water-transfer, per-seat (premium anchor; discount_factor=1.0)",
            "demand": ("sourced corridor demand pool" if row.get("status") == "grounded"
                       else f"estimated ({row.get('est_basis')})"),
        },
    }

# --- G61: commodity-fare tags (public-ferry anchor, not premium per-seat). LB-131.
COMMODITY_FARE_IDS = {
    "rn-347c44e1d360": 15.20,  # Samui (Bangrak) -> Don Sak
    "ics-5038f54700":  15.20,  # Samui (Lipa Noi) -> Donsak (Raja)
    "ics-66f63f2796":  15.20,  # Samui (Nathon) -> Donsak (Seatran)
    "ics-5288f62780":  14.00,  # Saigon (Bach Dang) -> Vung Tau
}

records = []
for rid, items in by_rid.items():
    # headline = highest market-rev (grounded preferred via the rev sort; null treated as 0)
    items_sorted = sorted(items, key=lambda pr: -((pr[1].get("mid", {}).get("market_revenue_yr")) or 0))
    head_partner, head_row = items_sorted[0]
    rec = {"route_id": rid, "partner": head_partner, "deck_url": DECK_URL.get(head_partner)}
    rec.update(corridor_block(head_row))
    if len(items_sorted) > 1:
        rec["also_serves"] = [corridor_block(r) for _, r in items_sorted[1:]]
    if rid in COMMODITY_FARE_IDS:
        rec["commodity_fare"] = True
        rec["fare_basis"] = "commodity_public_transit"
        rec["commodity_fare_usd"] = COMMODITY_FARE_IDS[rid]
    records.append(rec)

records.sort(key=lambda r: (r["partner"], -(r["mid"]["market_rev_yr"] or 0)))

out = {
    "_meta": {
        "doc": "Route-keyed unit-economics sidecar for the Atlas front end. Join onto route "
               "features by route_id. Presence of a record => has_economics=true. Show MID "
               "headline; band carries THIN/MID/FULL. Honor status (grounded vs estimated) and "
               "demand_confidence in styling. Never invent: absent record = no economics yet.",
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gold_routes_total": len(gold_rids),
        "records": len(records),
        "pending_route_pin": len(pending),
        "resolution": "ID-based only (route_id in gold, or exact unordered endpoint match). No fuzzy matching.",
    },
    "records": records,
    "_pending_route_pin": pending,
}
json.dump(out, open(OUT, "w"), indent=1)
print(f"wrote {OUT}")
print(f"records (route-pinned): {len(records)} | pending (no gold route): {len(pending)}")
print("by partner:", dict(Counter(r['partner'] for r in records)))
print("grounded:", sum(1 for r in records if r['status']=='grounded'),
      "| estimated:", sum(1 for r in records if r['status']=='estimated'))
