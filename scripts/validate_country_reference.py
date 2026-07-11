#!/usr/bin/env python3
"""Fail-closed country-reference gate for Navier corridor economics.

An active corridor must resolve its exact `country` string to a complete row in
country-reference.json. There is no default country. A corridor may be excluded
only with a non-empty `_economics_hold_reason`; held rows are reported and never
enter aggregate.py or build_transparent_sheet.py.
"""
import argparse, json, pathlib, sys

REQUIRED = (
    "captain_usd_yr",
    "energy_usd_kwh",
    "grid_co2_kg_kwh",
    "marina_overhead_usd_yr",
    "cost_index",
)
PSEUDO_COUNTRIES = {"CrossBorder", "USVI / BVI", "TBD", "Unknown", "Global"}

def value(node):
    return node.get("value") if isinstance(node, dict) else node

def main():
    ap = argparse.ArgumentParser()
    here = pathlib.Path(__file__).resolve().parent
    ap.add_argument("--corridors", default=str(here.parent / "finance/model/corridors.json"))
    ap.add_argument("--country-reference", default=str(here.parent / "finance/model/country-reference.json"))
    ap.add_argument("--partner", help="Validate one partner; omit for every market")
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args()

    corridors = json.load(open(args.corridors, encoding="utf-8"))["markets"]
    cref = json.load(open(args.country_reference, encoding="utf-8"))["countries"]
    errors, held, active = [], [], []

    for market, market_obj in corridors.items():
        partner = market_obj.get("partner", "grab")
        if args.partner and partner != args.partner:
            continue
        for idx, row in enumerate(market_obj.get("corridors", [])):
            rec = {
                "market": market,
                "partner": partner,
                "index": idx,
                "route_id": row.get("route_id"),
                "corridor": f"{row.get('from','')} -> {row.get('to','')}",
                "country": row.get("country"),
            }
            reason = row.get("_economics_hold_reason")
            if reason:
                rec["reason"] = reason
                held.append(rec)
                if not isinstance(reason, str) or len(reason.strip()) < 12:
                    errors.append({**rec, "error": "economics hold reason is not descriptive"})
                continue

            active.append(rec)
            country = row.get("country")
            if not country:
                errors.append({**rec, "error": "missing country"})
                continue
            if country in PSEUDO_COUNTRIES or "/" in country:
                errors.append({**rec, "error": "pseudo/composite country label; declare exact evidenced opex country"})
                continue
            country_row = cref.get(country)
            if not country_row:
                errors.append({**rec, "error": "missing exact country-reference row"})
                continue
            for field in REQUIRED:
                v = value(country_row.get(field))
                if not isinstance(v, (int, float)):
                    errors.append({**rec, "field": field, "error": "missing/non-numeric required country-reference value"})

    report = {
        "status": "PASS" if not errors else "FAIL",
        "partner": args.partner or "all",
        "active_corridors": len(active),
        "held_corridors": len(held),
        "held": held,
        "errors": errors,
        "rule": "exact country key + five numeric fields, or explicit economics hold; no fallback",
    }
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
