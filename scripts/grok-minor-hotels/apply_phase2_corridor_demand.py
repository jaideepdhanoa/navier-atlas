#!/usr/bin/env python3
"""Patch Phase-2 Minor Hotels corridors (Thailand Gulf, Maldives, UAE wider) into scoped view."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORR_OUT = ROOT / "finance/recal/corridors-minor-hotels.json"
PARTNER = ROOT / "partner-pitch/partners/minor-hotels.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
REPORT = ROOT / "grok-routing-output/minor-hotels-phase2-demand-report.json"

# Modeled captive demand — Tier-2 hospitality (T4/T5; null beats wrong ceiling)
PHASE2_CLUSTERS: dict[str, dict] = {
    "thailand-gulf": {
        "market_key": "thailand-gulf",
        "label": "Minor Hotels — Thailand Gulf",
        "pool_usd_yr": 1_850_000,
        "fare_usd": 85.0,
        "capture": 0.85,
        "partner_market_id": "thailand_gulf",
    },
    "maldives": {
        "market_key": "maldives",
        "label": "Minor Hotels — Maldives",
        "pool_usd_yr": 2_400_000,
        "fare_usd": 120.0,
        "capture": 0.90,
        "partner_market_id": "maldives",
    },
    "uae-wider": {
        "market_key": "uae-wider",
        "label": "Minor Hotels — UAE wider",
        "pool_usd_yr": 1_200_000,
        "fare_usd": 150.0,
        "capture": 0.60,
        "partner_market_id": "uae_wider",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def route_props(routes: list, rid: str) -> dict | None:
    for r in routes:
        p = r.get("properties", r)
        if p.get("id") == rid:
            return p
    return None


def corridor_row(rid: str, props: dict, pax: int, fare: float, capture: float, note: str) -> dict:
    fc = props.get("from_city_id") or props.get("from")
    tc = props.get("to_city_id") or props.get("to")
    return {
        "route_id": rid,
        "from": props.get("label", rid).split("→")[0].strip() if "→" in props.get("label", "") else fc,
        "to": props.get("label", rid).split("→")[-1].strip() if "→" in props.get("label", "") else tc,
        "distance_nm": props.get("distance_nm", 0),
        "vessel": props.get("platform", "Pioneer II"),
        "archetype": "hospitality_developer",
        "from_node_id": fc,
        "to_node_id": tc,
        "country": "Multi",
        "captive": True,
        "captive_resort": True,
        "pool_basis": "addressable",
        "_minor_hotels_captive": True,
        "_minor_capture_target": capture,
        "L3_locals": {
            "comparable_fare_usd_pax": fare,
            "corridor_annual_oneway_pax": pax,
            "_fare_record": {
                "value": fare,
                "unit": "USD/pax/one-way",
                "source_tier": "T5",
                "confidence": "low-med",
                "source": note,
                "method": "minor-hotels phase2 captive floor",
            },
            "_demand_record": {
                "value": pax,
                "unit": "pax/yr one-way",
                "source_tier": "T4",
                "confidence": "low-med",
                "source": note,
                "method": "minor-hotels phase2 pool split",
            },
            "demand_confidence": "med",
        },
        "_minor_phase2_hardened": True,
    }


def main() -> int:
    partner = json.loads(PARTNER.read_text())
    routes = json.loads(ROUTES.read_text())
    corr = json.loads(CORR_OUT.read_text()) if CORR_OUT.exists() else {
        "_doc": "Scoped captive corridors for minor-hotels economics cascade",
        "capture_rate": 0.1,
        "markets": {},
    }

    report = {"at": now_iso(), "clusters": {}}

    for cluster_key, spec in PHASE2_CLUSTERS.items():
        pmid = spec["partner_market_id"]
        market = next((m for m in partner.get("markets", []) if m.get("id") == pmid), None)
        if not market:
            continue
        rids: list[str] = []
        for j in market.get("journeys_unlocked", []):
            rid = j.get("route_id")
            if rid and rid not in rids:
                rids.append(rid)
        if not rids:
            continue
        total_trips = int(round(spec["pool_usd_yr"] / max(spec["fare_usd"], 1)))
        base = total_trips // len(rids)
        rem = total_trips % len(rids)
        shares = [base + (1 if i < rem else 0) for i in range(len(rids))]

        corridors = []
        for rid, pax in zip(rids, shares):
            props = route_props(routes, rid)
            if not props:
                continue
            corridors.append(
                corridor_row(
                    rid,
                    props,
                    pax,
                    spec["fare_usd"],
                    spec["capture"],
                    f"{spec['label']} property-throughput floor (Phase-2)",
                )
            )

        mk = corr["markets"].setdefault(
            spec["market_key"],
            {
                "partner": "minor-hotels",
                "region": "Global",
                "label": spec["label"],
                "fleet_basis": "network_sum",
                "fleet_rounding": "ceil",
                "_minor_cluster": cluster_key,
                "_minor_economics_status": "phase2_modeled",
                "_grounded_floor_usd_yr": int(spec["pool_usd_yr"] * spec["capture"]),
                "corridors": [],
            },
        )
        existing = {c.get("route_id") for c in mk.get("corridors", [])}
        added = []
        for c in corridors:
            if c["route_id"] not in existing:
                mk["corridors"].append(c)
                added.append(c["route_id"])
        report["clusters"][cluster_key] = {
            "routes": len(rids),
            "added": added,
            "pool_usd_yr": spec["pool_usd_yr"],
        }

    corr["_phase2_demand_applied"] = True
    corr["_built_at"] = now_iso()
    CORR_OUT.write_text(json.dumps(corr, indent=1) + "\n")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())