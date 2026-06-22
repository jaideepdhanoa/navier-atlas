#!/usr/bin/env python3
"""
Build economics_by_route_id.json including bolt + yango partners.
Wraps handoff build_economics_sidecar.py logic with bolt/yango PARTNERS extension.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INGEST = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal"
OPEX_INGEST = ROOT / "_ingest/sidecar-opex-refresh-2026-06-20"
AGG_DIR = OPEX_INGEST if OPEX_INGEST.exists() else INGEST / "inputs/aggs"

PARTNERS = [
    "grab",
    "careem",
    "jih-global",
    "red-sea-global",
    "saudi-redsea-pif",
    "saudi-pif",
    "qatar",
    "bolt",
    "yango",
    "uber",
    "french-polynesia",
    "constance",
    "four-seasons",
    "grab-thailand",
    "uber-india",
]

def load_deck_url(url_map_path: Path | None = None) -> dict:
    candidates = [
        url_map_path,
        OPEX_INGEST / "economics_url_map.json",
        INGEST / "inputs/economics_url_map.json",
    ]
    for path in candidates:
        if path and path.exists():
            return json.loads(path.read_text()).get("economics_url", {})
    return {
        "grab": "https://docs.google.com/spreadsheets/d/1ACYTZar0odZCASzKUwo1A4rXGsCsz6Luec6Cu3vQ20w/edit",
        "careem": "https://docs.google.com/spreadsheets/d/1ip3bYDedgxj_9ydksKH1OzeoXGMWT2LZzti1y5jsx-8/edit",
        "bolt": "https://docs.google.com/spreadsheets/d/1XkD0x-PfDyY34ZBy5jX2u1LqoibAd_xMiyO-Re2UWUk/edit",
        "yango": "https://docs.google.com/spreadsheets/d/1fvB_tc8IWUTlKMWjPcoJde_uPnGKVqoCxxsgd5IL1rM/edit",
        "qatar": "https://docs.google.com/spreadsheets/d/1v0Fo-QDKVIEiMzzYUbrugCUH1cBJdLKD9URG1R16S0Q/edit",
        "jih-global": "https://docs.google.com/spreadsheets/d/136mve2Z-c2FRZm2cZZ3of9jk85kpEkpzf-ZIC9dzXJU/edit",
        "constance": "https://docs.google.com/spreadsheets/d/1Lhz_6nh3HnCK8L7tzr4HhmNEtfnXx2smecYPNQSORl0/edit",
        "four-seasons": "https://docs.google.com/spreadsheets/d/1Flk6PfRgCNdSGlP49lf1KxXaoR4qdlLcs1O8YA72gcc/edit",
    }

COMMODITY_FARE_IDS = {
    "rn-347c44e1d360": 15.20,
    "ics-5038f54700": 15.20,
    "ics-66f63f2796": 15.20,
    "ics-5288f62780": 14.00,
}

MARKET_DISPLAY = {
    "singapore": "Singapore",
    "cross-border": "Cross-Border",
    "bali": "Bali",
    "phuket": "Phuket",
    "philippines": "Philippines",
    "vietnam": "Vietnam",
    "cambodia": "Cambodia",
    "borneo": "Borneo",
    "penang": "Penang",
    "jakarta": "Jakarta",
    "taiwan": "Taiwan",
    "saudi-redsea": "Saudi – Red Sea",
    "saudi-redsea-resort": "Saudi – Red Sea (Resort)",
    "uae-careem": "UAE (Careem)",
    "uae-luxury": "UAE (Luxury)",
    "maldives-jih": "Maldives (JIH)",
}


def mkt_disp(mid):
    return MARKET_DISPLAY.get(mid, (mid or "").replace("-", " ").title())


def num(x):
    return None if x is None else round(float(x), 2)


def corridor_block(row, corr_country):
    mid = row.get("mid", {})
    thin = row.get("thin", {})
    full = row.get("full", {})
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
            "vessels_10pct": [
                thin.get("vessels_supported_10pct"),
                mid.get("vessels_supported_10pct"),
                full.get("vessels_supported_10pct"),
            ],
        },
        "estimation_basis": row.get("est_basis"),
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
                "insurance_usd_yr": num((mid.get("cost_components") or {}).get("insurance_usd_yr")),
                "charging_berth_usd_yr": num((mid.get("cost_components") or {}).get("charging_berth_usd_yr")),
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
            "demand": (
                "sourced corridor demand pool"
                if row.get("status") == "grounded"
                else f"estimated ({row.get('est_basis')})"
            ),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--aggdir", default=str(AGG_DIR))
    ap.add_argument(
        "--corridors",
        default=str(INGEST / "inputs/corridors.json"),
        help="finance corridors.json (econ-reseal handoff)",
    )
    ap.add_argument("--out", default="data-clean/economics_by_route_id.json")
    ap.add_argument("--global", action="store_true", help="Build from agg-global.json (partner-independent physics)")
    ap.add_argument(
        "--url-map",
        default="",
        help="economics_url_map.json (default: sidecar-opex-refresh handoff)",
    )
    args = ap.parse_args()

    dc = ROOT / args.dc
    aggdir = Path(args.aggdir)
    out = ROOT / args.out
    deck_url = load_deck_url(Path(args.url_map) if args.url_map else None)

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from bolt_yango_routing_shared import (
        build_bp_index,
        mint_route_id,
        resolve_corridor_endpoints,
    )

    routes_obj = json.loads((dc / "ROUTES.json").read_text())
    feats = routes_obj["features"] if isinstance(routes_obj, dict) and "features" in routes_obj else routes_obj
    fbt = json.loads((dc / "FEATURES_BY_TYPE.json").read_text())
    bp_idx = build_bp_index(fbt)
    gold_rids = set()
    pair2id = {}
    bp_pair2id = {}
    for f in feats:
        p = f["properties"]
        rid = p.get("id")
        gold_rids.add(rid)
        a, b = p.get("from"), p.get("to")
        if a and b:
            pair2id.setdefault(frozenset((a, b)), rid)
        fn, tn = p.get("from_node"), p.get("to_node")
        if fn and tn:
            bp_pair2id.setdefault(frozenset((fn, tn)), rid)

    corr = json.loads(Path(args.corridors).read_text())
    resolved = {}
    unresolved_detail = {}
    corr_country = {}
    market_partner = {}
    for mid_k, mk in corr["markets"].items():
        partner = mk.get("partner", "grab")
        market_partner[mid_k] = partner
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
                from_bp, to_bp, _, _ = resolve_corridor_endpoints(c, bp_idx)
                if from_bp and to_bp:
                    bp_key = frozenset((from_bp, to_bp))
                    if bp_key in bp_pair2id:
                        resolved[key] = bp_pair2id[bp_key]
                    else:
                        minted = mint_route_id(from_bp, to_bp)
                        if minted in gold_rids:
                            resolved[key] = minted
            if key not in resolved:
                if a and b and a == b:
                    why = "aspirational_intra_city"
                elif is_asp:
                    why = "aspirational_declared"
                else:
                    why = "route_id_not_in_gold" if rid else (
                        "endpoints_city_level_not_pinned" if (a and b) else "no_endpoints"
                    )
                unresolved_detail[key] = {"partner": partner, "reason": why}

    by_rid = defaultdict(list)
    pending = []
    aliases = {"saudi-redsea": "saudi-redsea-pif", "grab-aggregate-results": "grab"}

    def ingest_rows(rows, source_partner=None):
        for row in rows:
            if row.get("status") == "duplicate" or row.get("is_dup"):
                continue
            market = row.get("market")
            label = row.get("corridor")
            key = (market, label)
            mid = row.get("mid", {})
            rid = resolved.get(key)
            if not rid and mid.get("route_id") in gold_rids:
                rid = mid.get("route_id")
            if not rid:
                pending.append(
                    {
                        "authored_for": source_partner or market_partner.get(market),
                        "market": market,
                        "corridor": label,
                        "status": row.get("status"),
                        "reason": unresolved_detail.get(key, {}).get("reason", "unresolved"),
                    }
                )
                continue
            authored = market_partner.get(market, source_partner)
            by_rid[rid].append((authored, market, row))

    global_path = aggdir / "agg-global.json"
    if getattr(args, "global") or global_path.exists():
        if not global_path.exists():
            raise SystemExit(f"--global requested but {global_path} missing")
        ingest_rows(json.loads(global_path.read_text()).get("rows", []))
    else:
        for partner in PARTNERS:
            p_resolved = aliases.get(partner, partner)
            candidates = [
                aggdir / f"agg-{p_resolved}.json",
                aggdir / f"{p_resolved}-aggregate.json",
                aggdir / f"agg-{partner}.json",
                aggdir / f"{partner}-aggregate.json",
            ]
            path = next((c for c in candidates if c.exists()), None)
            if not path:
                continue
            ingest_rows(json.loads(path.read_text()).get("rows", []), source_partner=partner)

    records = []
    for rid, items in by_rid.items():
        items_sorted = sorted(items, key=lambda pr: -((pr[2].get("mid", {}).get("market_revenue_yr")) or 0))
        head_authored, head_market, head_row = items_sorted[0]
        rec = {"route_id": rid, "registry_market_id": head_market}
        if head_authored:
            rec["authored_for"] = head_authored
        rec.update(corridor_block(head_row, corr_country))
        if len(items_sorted) > 1:
            rec["also_serves"] = [corridor_block(r, corr_country) for _, __, r in items_sorted[1:]]
        if rid in COMMODITY_FARE_IDS:
            rec["commodity_fare"] = True
            rec["fare_basis"] = "commodity_public_transit"
            rec["commodity_fare_usd"] = COMMODITY_FARE_IDS[rid]
        records.append(rec)

    records.sort(key=lambda r: (r.get("authored_for") or "", -(r["mid"]["market_rev_yr"] or 0)))

    payload = {
        "_meta": {
            "doc": "Route-keyed unit-economics sidecar for the Atlas front end.",
            "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "gold_routes_total": len(gold_rids),
            "records": len(records),
            "pending_route_pin": len(pending),
            "partners": PARTNERS,
            "aggdir": str(aggdir),
            "opex_stack": "6-line (energy, crew, marina, maintenance, insurance, charging/berth)",
            "resolution": "ID-based only (route_id in gold, or exact unordered endpoint match).",
        },
        "records": records,
        "_pending_route_pin": pending,
    }
    out.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"wrote {out}")
    print(f"records: {len(records)} | pending: {len(pending)}")
    print("by authored_for:", dict(Counter(r.get("authored_for") for r in records)))


if __name__ == "__main__":
    main()