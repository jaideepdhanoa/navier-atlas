#!/usr/bin/env python3
"""Wire upper-Gulf + Ko Lanta modeled demand into scoped grab-thailand corridors."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORR_OUT = ROOT / "finance/recal/corridors-grab-thailand.json"
REPORT = ROOT / "grok-routing-output/grab-thailand-depth-demand-apply-report.json"

# Tier-modeled premium-eligible one-way pax/yr (T4/T5; null beats confidently-wrong ceiling)
TIER_A = 75000
TIER_B = 28000

DEPTH_CORRIDORS = [
    {
        "market": "eastern_seaboard",
        "route_id": "rn-dcbcbe8bfb4f",
        "from": "Bangkok (Chao Phraya / Gulf gateway)",
        "to": "Pattaya (Bali Hai Pier)",
        "distance_nm": 52.6,
        "from_node_id": "bangkok-thailand",
        "to_node_id": "pattaya-thailand",
        "pax": 148000,
        "fare": 52.0,
        "tier": "B",
        "note": "Premium slice of Bangkok-Pattaya leisure+EEC road flow; modeled pending operator validation.",
    },
    {
        "market": "eastern_seaboard",
        "route_id": "rn-4a3b9db3cda5",
        "from": "Pattaya (Bali Hai Pier)",
        "to": "Koh Samet (Na Dan Pier)",
        "distance_nm": 37.0,
        "from_node_id": "pattaya-thailand",
        "to_node_id": "koh-samet-thailand",
        "pax": TIER_B,
        "fare": 42.0,
        "tier": "B",
        "note": "Premium slice of Ban Phe-origin Samet day-trip flow rerouted from Pattaya.",
    },
    {
        "market": "eastern_seaboard",
        "route_id": "rn-3b647e2d663d",
        "from": "Ban Phe Pier",
        "to": "Koh Samet (Na Dan Pier)",
        "distance_nm": 3.3,
        "from_node_id": "koh-samet-thailand",
        "to_node_id": "koh-samet-thailand",
        "pax": 92000,
        "fare": 14.0,
        "tier": "A",
        "note": "Proven high-frequency Ban Phe speedboat gateway; premium upgrade of dense leg.",
    },
    {
        "market": "royal_coast",
        "route_id": "rn-9c2bce5bffd0",
        "from": "Hua Hin (pier)",
        "to": "Pattaya (Bali Hai Pier)",
        "distance_nm": 57.2,
        "from_node_id": "hua-hin-thailand",
        "to_node_id": "pattaya-thailand",
        "pax": 52000,
        "fare": 78.0,
        "tier": "A",
        "note": "East-West Ferry Project validated cross-Gulf demand; foiling premium tier.",
    },
    {
        "market": "royal_coast",
        "route_id": "rn-7512bdcf3d4c",
        "from": "Hua Hin (pier)",
        "to": "Cha-Am (pier)",
        "distance_nm": 13.4,
        "from_node_id": "hua-hin-thailand",
        "to_node_id": "cha-am-thailand",
        "pax": TIER_B,
        "fare": 24.0,
        "tier": "B",
        "note": "Royal-coast resort weekend hop; modeled premium slice.",
    },
    {
        "market": "bangkok",
        "route_id": "rn-01f164a3d43c",
        "from": "Bangkok (ICONSIAM / Chao Phraya)",
        "to": "Hua Hin (pier)",
        "distance_nm": 88.0,
        "from_node_id": "bangkok-thailand",
        "to_node_id": "hua-hin-thailand",
        "pax": 85000,
        "fare": 68.0,
        "tier": "A",
        "note": "Marquee river-coast gateway: Bangkok weekenders to royal-coast resorts; replaces 2.5–3hr Phetkasem drive.",
    },
]

KOLANTA_PATCHES = [
    {
        "route_id": "rn-ad9e938ccfc6",
        "from": "Ko Lanta (Saladan Pier)",
        "to": "Koh Phi Phi (Tonsai)",
        "distance_nm": 17.0,
        "from_node_id": "koh-lanta-thailand",
        "to_node_id": "koh-phi-phi-thailand",
        "pax": 62000,
        "fare": 28.0,
        "tier": "A",
    },
    {
        "route_id": "rn-eed847c3269d",
        "from": "Ko Lanta (Saladan Pier)",
        "to": "Krabi (Klong Jilad)",
        "distance_nm": 24.0,
        "from_node_id": "koh-lanta-thailand",
        "to_node_id": "krabi-thailand",
        "pax": TIER_B,
        "fare": 32.0,
        "tier": "B",
    },
    {
        "route_id": "rn-01a8c29df66a",
        "from": "Phuket (Rassada Pier)",
        "to": "Ko Lanta (Saladan Pier)",
        "distance_nm": 42.4,
        "from_node_id": "phuket-phang-nga-thailand",
        "to_node_id": "koh-lanta-thailand",
        "pax": 31000,
        "fare": 55.0,
        "tier": "B",
    },
]


def corridor_row(spec: dict) -> dict:
    pax, fare = spec["pax"], spec["fare"]
    return {
        "route_id": spec["route_id"],
        "from": spec["from"],
        "to": spec["to"],
        "distance_nm": spec["distance_nm"],
        "vessel": "Pioneer II",
        "archetype": "ridehail",
        "from_node_id": spec["from_node_id"],
        "to_node_id": spec["to_node_id"],
        "country": "Thailand",
        "L3_locals": {
            "comparable_fare_usd_pax": fare,
            "_fare_record": {
                "value": fare,
                "unit": "USD/pax/one-way",
                "source_tier": "T5",
                "confidence": "low-med",
                "source": spec.get("note", "MODELED premium foiling fare"),
                "method": "grab-thailand depth/kolanta demand pass",
            },
            "corridor_annual_oneway_pax": pax,
            "_demand_record": {
                "value": pax,
                "unit": "premium-eligible one-way pax/yr",
                "source_tier": "T4",
                "confidence": "low-med",
                "source": spec.get("note", "MODELED tier demand"),
                "method": f"tier-{spec.get('tier', 'B')} modeled haircut (depth/kolanta pass)",
            },
            "demand_confidence": "med",
        },
        "_thailand_depth_hardened": True,
        "_demand_pass": "grab-thailand-depth-2026-06-23",
    }


def main() -> int:
    doc = json.loads(CORR_OUT.read_text())
    report = {"depth_added": [], "kolanta_added": [], "at": datetime.now(timezone.utc).isoformat()}

    for spec in DEPTH_CORRIDORS:
        mid = spec["market"]
        mk = doc["markets"].setdefault(
            mid,
            {
                "region": "SEA",
                "label": mid.replace("_", " ").title(),
                "partner": "grab-thailand",
                "_scope": "grab-thailand-derivative",
                "fleet_basis": "network_sum",
                "fleet_rounding": "ceil",
                "corridors": [],
            },
        )
        mk["partner"] = "grab-thailand"
        mk["_scope"] = "grab-thailand-derivative"
        row = corridor_row(spec)
        existing = {c.get("route_id") for c in mk["corridors"]}
        if spec["route_id"] not in existing:
            mk["corridors"].append(row)
            report["depth_added"].append(spec["route_id"])

    phuket = doc["markets"]["phuket"]
    existing_ph = {c.get("route_id") for c in phuket["corridors"]}
    for spec in KOLANTA_PATCHES:
        if spec["route_id"] in existing_ph:
            for c in phuket["corridors"]:
                if c.get("route_id") == spec["route_id"]:
                    c.update(corridor_row(spec))
                    report["kolanta_added"].append({"route_id": spec["route_id"], "action": "patched"})
            continue
        phuket["corridors"].append(corridor_row(spec))
        report["kolanta_added"].append({"route_id": spec["route_id"], "action": "added"})

    doc["_built_at"] = datetime.now(timezone.utc).isoformat()
    doc["_depth_demand_applied"] = True
    CORR_OUT.write_text(json.dumps(doc, indent=2) + "\n")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())