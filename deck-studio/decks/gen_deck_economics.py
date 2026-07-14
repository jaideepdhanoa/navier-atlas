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


def route_unit_economics(row: dict[str, Any]) -> dict[str, Any]:
    """Per-boat, route-level unit economics from the sourced `thin` block.

    This is the correct basis for a unit-economics slide (per-vessel run cost and
    payback), distinct from the market-level rollup used for the country total.
    """
    t = row.get("thin") or {}
    cc = t.get("cost_components") or {}
    return {
        "distance_nm": t.get("distance_nm"),
        "vessel": t.get("vessel"),
        "annual_one_way_pax_per_boat": t.get("pax_per_year"),
        "one_way_fare_usd": t.get("navier_fare_usd"),
        "revenue_per_boat_yr": t.get("revenue_per_boat_yr"),
        "opex_lines": {
            "energy_usd_yr": cc.get("energy_usd_yr"),
            "crew_usd_yr": cc.get("crew_usd_yr"),
            "marina_overhead_usd_yr": cc.get("marina_overhead_usd_yr"),
            "maintenance_usd_yr": cc.get("maintenance_usd_yr"),
            "insurance_usd_yr": cc.get("insurance_usd_yr"),
            "charging_berth_usd_yr": cc.get("charging_berth_usd_yr"),
        },
        "total_run_cost_yr": t.get("annual_opex"),
        "depreciation_usd_yr": t.get("depreciation"),
        "ebitda_per_boat_yr": t.get("ebitda_per_boat_yr"),
        "margin": t.get("margin"),
        "payback_years": t.get("payback_years"),
        "co2_saved_t_per_boat_yr": t.get("co2_saved_t_per_boat_yr"),
    }


ROUTE_LEVEL_KEYS = ("annual_one_way_pax_per_boat", "one_way_fare_usd", "revenue_per_boat_yr", "payback_years")


def route_is_supported(ue: dict[str, Any]) -> bool:
    return all(ue.get(k) is not None for k in ROUTE_LEVEL_KEYS)


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

    # ---- single representative unit-economics route ----
    er = binding["economics_route"]
    rid = er.get("route_id")
    econ_base = {
        "label": er.get("label"),
        "route_id": rid,
        "desc": er.get("desc"),
    }
    if rid is None:
        economics_route = {
            **econ_base,
            "status": "held",
            "unit_economics": None,
            "hold_reason": "Route ID and financial values remain blank pending local terminal, demand, and fare evidence.",
        }
    else:
        if rid not in route_ids:
            raise SystemExit(f"economics_route: route ID absent from canonical ROUTES.json: {rid}")
        row = row_by_route.get(rid)
        if row is None:
            economics_route = {**econ_base, "status": "held", "unit_economics": None,
                               "hold_reason": "No route-level finance row is available."}
        elif row.get("country") != binding["country"]:
            raise SystemExit(
                f"economics_route: aggregate country {row.get('country')!r} does not match {binding['country']!r}"
            )
        else:
            ue = route_unit_economics(row)
            if route_is_supported(ue):
                economics_route = {**econ_base, "status": "supported", "unit_economics": ue, "hold_reason": None}
            else:
                economics_route = {**econ_base, "status": "held", "unit_economics": None,
                                   "hold_reason": "Route-level demand, fare, or operating inputs are incomplete."}

    # ---- TAM ladder rungs bound from grounded aggregate fields (never invented) ----
    def resolve_field(root: Any, dotted: str) -> Any:
        cur = root
        for part in dotted.split("."):
            if isinstance(cur, dict):
                cur = cur.get(part)
            else:
                return None
        return cur

    tam_spec = binding.get("tam") or {}
    tam_rungs: list[dict[str, Any]] = []
    for rung in tam_spec.get("rungs") or []:
        field = rung.get("aggregate_field") or ""
        val = resolve_field(aggregate, field) if field else None
        expected = rung.get("value_usd")
        if expected is not None and val is not None and round(float(val), 2) != round(float(expected), 2):
            raise SystemExit(
                f"TAM rung '{rung.get('label')}' mismatch: aggregate {val} vs binding {expected}"
            )
        # Binding-supplied upper rungs (handoff ladder / labelled assumption bands) may set
        # value_usd without an aggregate field. Aggregate remains authoritative when present.
        if val is None and expected is not None:
            val = expected
        out_rung: dict[str, Any] = {
            "label": rung.get("label"),
            "value_usd": val,
            "note": rung.get("note"),
        }
        for opt in ("value_usd_low", "value_usd_high", "value_basis", "status"):
            if rung.get(opt) is not None:
                out_rung[opt] = rung.get(opt)
        tam_rungs.append(out_rung)
    tam_out = {
        "headline": tam_spec.get("headline"),
        "rungs": tam_rungs,
        "hold_reason": tam_spec.get("hold_reason"),
        "source": tam_spec.get("source"),
    }

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
        "schema_version": "country-deck-economics-v3",
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
        "economics_route": economics_route,
        "tam": tam_out,
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
