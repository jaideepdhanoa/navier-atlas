#!/usr/bin/env python3
"""Generate route-paired country-deck economics from canonical aggregate rows.

This is the only country-review deck economics path. It never borrows a route,
market, or country: unsupported values are emitted as null with a hold reason.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

VALUE_KEYS = (
    "annual_one_way_pax",
    "one_way_fare_usd",
    "annual_revenue_usd",
    "vessels_supported",
)


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def null_values() -> dict[str, None]:
    return {k: None for k in VALUE_KEYS}


def row_values(row: dict[str, Any]) -> dict[str, Any]:
    mid = row.get("mid") or {}
    return {
        "annual_one_way_pax": mid.get("pax_per_year"),
        "one_way_fare_usd": mid.get("navier_fare_usd"),
        "annual_revenue_usd": mid.get("market_revenue_yr"),
        "vessels_supported": mid.get("vessels_supported_10pct"),
    }


def is_supported(values: dict[str, Any]) -> bool:
    return all(values.get(k) is not None for k in VALUE_KEYS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--binding", required=True, type=Path)
    ap.add_argument("--aggregate", required=True, type=Path)
    ap.add_argument("--routes", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    binding = read_json(args.binding)
    aggregate = read_json(args.aggregate)
    routes = read_json(args.routes)

    route_ids = {
        (r.get("properties") or {}).get("id")
        for r in routes
        if isinstance(r, dict)
    }
    rows = aggregate.get("rows") or []
    row_by_route: dict[str, dict[str, Any]] = {}
    duplicates: set[str] = set()
    for row in rows:
        rid = row.get("route_id")
        if not rid:
            continue
        if rid in row_by_route:
            duplicates.add(rid)
        row_by_route[rid] = row
    if duplicates:
        raise SystemExit(f"duplicate aggregate route IDs: {sorted(duplicates)}")

    pair_values: list[dict[str, Any]] = []
    for pair in binding["city_route_pairs"]:
        rid = pair.get("route_id")
        base = {
            "pair_key": pair["pair_key"],
            "city_key": pair["city_key"],
            "city_label": pair["city_label"],
            "route_label": pair["route_label"],
            "route_id": rid,
        }
        if rid is None:
            pair_values.append({
                **base,
                "status": "held",
                "values": null_values(),
                "hold_reason": pair["hold_reason"],
            })
            continue
        if rid not in route_ids:
            raise SystemExit(f"{pair['pair_key']}: route ID absent from canonical ROUTES.json: {rid}")
        row = row_by_route.get(rid)
        if row is None:
            pair_values.append({
                **base,
                "status": "held",
                "values": null_values(),
                "hold_reason": pair.get("hold_reason") or "No route-level finance row is available.",
            })
            continue
        if row.get("country") != binding["country"]:
            raise SystemExit(
                f"{pair['pair_key']}: aggregate country {row.get('country')!r} "
                f"does not match {binding['country']!r}"
            )
        values = row_values(row)
        if not is_supported(values):
            pair_values.append({
                **base,
                "status": "held",
                "values": null_values(),
                "hold_reason": pair.get("hold_reason") or "Route-level demand, fare, or operating inputs are incomplete.",
            })
        else:
            pair_values.append({
                **base,
                "status": "supported",
                "values": values,
                "hold_reason": None,
            })

    total_spec = binding["country_total"]
    supported_ids = total_spec.get("supported_route_ids") or []
    if len(supported_ids) != len(set(supported_ids)):
        raise SystemExit("country_total.supported_route_ids contains duplicates")
    total_revenue = 0.0
    total_vessels = 0
    for rid in supported_ids:
        if rid not in route_ids:
            raise SystemExit(f"country total route absent from canonical ROUTES.json: {rid}")
        row = row_by_route.get(rid)
        if row is None:
            raise SystemExit(f"country total route absent from aggregate: {rid}")
        values = row_values(row)
        if not is_supported(values):
            raise SystemExit(f"country total route is not fully supported: {rid}")
        if row.get("country") != binding["country"]:
            raise SystemExit(f"country total route has wrong country: {rid}")
        total_revenue += float(values["annual_revenue_usd"])
        total_vessels += int(values["vessels_supported"])

    expected_revenue = total_spec.get("expected_annual_revenue_usd")
    expected_vessels = total_spec.get("expected_vessels_supported")
    if expected_revenue is None:
        if supported_ids:
            raise SystemExit("null expected country revenue requires an empty supported-route list")
        country_values = {
            "annual_revenue_usd": None,
            "vessels_supported": None,
            "supported_route_count": 0,
        }
        country_status = "held"
    else:
        if round(total_revenue, 2) != round(float(expected_revenue), 2):
            raise SystemExit(
                f"country revenue mismatch: generated {total_revenue} expected {expected_revenue}"
            )
        if total_vessels != int(expected_vessels):
            raise SystemExit(
                f"country vessel mismatch: generated {total_vessels} expected {expected_vessels}"
            )
        country_values = {
            "annual_revenue_usd": round(total_revenue, 2),
            "vessels_supported": total_vessels,
            "supported_route_count": len(supported_ids),
        }
        country_status = "supported"

    out = {
        "schema_version": "country-deck-economics-v2",
        "deck_key": binding["deck_key"],
        "partner_id": binding["partner_id"],
        "country": binding["country"],
        "generator": "deck-studio/decks/gen_deck_economics.py",
        "source_files": {
            "binding": str(args.binding),
            "aggregate": str(args.aggregate),
            "routes": str(args.routes),
        },
        "source_sha256": {
            "binding": sha256(args.binding),
            "aggregate": sha256(args.aggregate),
            "routes": sha256(args.routes),
        },
        "pairs": pair_values,
        "country_total": {
            "status": country_status,
            "values": country_values,
            "supported_route_ids": supported_ids,
            "hold_reason": total_spec.get("hold_reason") if country_status == "held" else None,
        },
        "checks": {
            "id_matching": "exact",
            "unsupported_values": "null",
            "borrowed_country_or_route_values": False,
            "published_total_reconciled": country_status == "supported",
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
