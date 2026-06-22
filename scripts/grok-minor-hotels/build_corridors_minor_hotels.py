#!/usr/bin/env python3
"""Build scoped captive corridors view for minor-hotels economics cascade."""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-minor-hotels"))
from minor_shared import (  # noqa: E402
    CORR_OUT,
    ROOT,
    TIER1_CLUSTERS,
    TIER1_CORRIDOR_ROUTES,
    load_economics_floor,
)

CORR_SRC = ROOT / "finance/model/corridors.json"
PARENT_MARKETS = {
    "phuket": "phuket",
    "bali": "bali",
    "palm-jumeirah": "uae-luxury",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def index_routes(src: dict) -> dict[str, tuple[str, dict]]:
    idx: dict[str, tuple[str, dict]] = {}
    for mkt, mk in src["markets"].items():
        for c in mk.get("corridors") or []:
            rid = c.get("route_id")
            if rid:
                idx[rid] = (mkt, c)
    return idx


def distribute_demand(total_trips: int, n: int) -> list[int]:
    if n <= 0:
        return []
    base = total_trips // n
    rem = total_trips % n
    out = [base] * n
    for i in range(rem):
        out[i] += 1
    return out


def patch_captive(corridor: dict, pax: int, fare: float, capture: float, note: str) -> dict:
    corridor = copy.deepcopy(corridor)
    l3 = corridor.setdefault("L3_locals", {})
    l3["comparable_fare_usd_pax"] = fare
    l3["corridor_annual_oneway_pax"] = pax
    l3["_demand_record"] = {
        "value": pax,
        "unit": "pax/yr one-way",
        "source_tier": "T2",
        "confidence": "med",
        "source": note,
        "method": "Minor Hotels captive property-throughput floor (Tasklet DRAFT)",
    }
    l3["_fare_record"] = {
        "value": fare,
        "unit": "USD/pax/one-way",
        "source_tier": "T2",
        "confidence": "med",
        "source": note,
        "method": "Minor Hotels captive fare anchor",
    }
    l3["demand_confidence"] = "med"
    corridor["captive"] = True
    corridor["captive_resort"] = True
    corridor["pool_basis"] = "addressable"
    corridor["_minor_hotels_captive"] = True
    corridor["_minor_capture_target"] = capture
    return corridor


def build_market(cluster_key: str, src: dict, route_idx: dict) -> dict:
    spec = TIER1_CLUSTERS[cluster_key]
    floor_doc = load_economics_floor(cluster_key)
    ga = floor_doc["global_assumptions"]
    pool = floor_doc["grounded_floor"]["transport_spend_pool_usd_yr_mid"]
    fare = ga["fare_usd_mid"]
    capture = ga["capture_mid"]
    total_trips = int(round(pool / max(fare, 1)))

    parent_key = PARENT_MARKETS[spec["market_key"]]
    route_ids = [r for r in TIER1_CORRIDOR_ROUTES[spec["market_key"]] if r in route_idx]
    # Exclude cross-border
    route_ids = [r for r in route_ids if "langkawi" not in r.lower()]

    shares = distribute_demand(total_trips, len(route_ids))
    corridors = []
    for rid, pax in zip(route_ids, shares):
        _, row = route_idx[rid]
        c = patch_captive(
            copy.deepcopy(row),
            pax,
            fare,
            capture,
            f"minor-hotels/{cluster_key} grounded floor",
        )
        c["route_id"] = rid
        corridors.append(c)

    return {
        "partner": "minor-hotels",
        "region": "Global",
        "label": f"Minor Hotels — {cluster_key}",
        "fleet_basis": "network_sum",
        "fleet_rounding": "ceil",
        "_market_note": (
            f"captive hospitality_developer cluster; LB-254 pool anchor; "
            f"floor=${floor_doc['grounded_floor']['grounded_som_floor_usd_yr_mid']:,.0f}/yr"
        ),
        "_minor_cluster": cluster_key,
        "_minor_economics_status": spec["status"],
        "_grounded_floor_usd_yr": floor_doc["grounded_floor"]["grounded_som_floor_usd_yr_mid"],
        "corridors": corridors,
    }


def main() -> int:
    src = json.loads(CORR_SRC.read_text())
    route_idx = index_routes(src)
    out = {
        "_doc": "Scoped captive corridors for minor-hotels economics cascade",
        "_source": "finance/model/corridors.json + handoff economics floors",
        "_built_at": now_iso(),
        "capture_rate": 0.1,
        "markets": {},
    }
    report = {"markets": {}, "missing_routes": []}

    for cluster_key in TIER1_CLUSTERS:
        spec = TIER1_CLUSTERS[cluster_key]
        mk = spec["market_key"]
        wanted = TIER1_CORRIDOR_ROUTES[mk]
        missing = [r for r in wanted if r not in route_idx]
        if missing:
            report["missing_routes"].extend(missing)
        market = build_market(cluster_key, src, route_idx)
        out["markets"][mk] = market
        report["markets"][mk] = {
            "corridors": len(market["corridors"]),
            "floor_usd_yr": market["_grounded_floor_usd_yr"],
            "status": spec["status"],
        }

    CORR_OUT.parent.mkdir(parents=True, exist_ok=True)
    CORR_OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"out": str(CORR_OUT), "report": report}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())