#!/usr/bin/env python3
"""Apply arriving-seat distribution-capture demand anchors → airasia-move corridors."""
from __future__ import annotations

import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANCHORS = ROOT / "handoff/airasia-move-2026-06-27/AIRASIA-DEMAND-ANCHORS.json"
CORR_IN = ROOT / "finance/recal/corridors-airasia-move.json"
CORR_OUT = CORR_IN
REPORT = ROOT / "grok-routing-output/airasia-move-demand-apply-report.json"

# FLAG assumptions — documented for model pass (LB-254 distribution-capture)
HUB_MODEL = {
    "phuket-andaman": {"airport_pax_yr": 17_400_000, "airasia_share": 0.22, "load_factor": 0.85, "island_bound": 0.45, "attach": 0.28, "avg_fare_usd": 55},
    "koh-samui-gulf": {"airport_pax_yr": 2_500_000, "airasia_share": 0.18, "load_factor": 0.82, "island_bound": 0.55, "attach": 0.30, "avg_fare_usd": 50},
    "bali-nusa-gili": {"airport_pax_yr": 21_800_000, "airasia_share": 0.25, "load_factor": 0.86, "island_bound": 0.35, "attach": 0.30, "avg_fare_usd": 60},
    "lombok": {"airport_pax_yr": 3_500_000, "airasia_share": 0.20, "load_factor": 0.84, "island_bound": 0.40, "attach": 0.28, "avg_fare_usd": 50},
    "komodo-flores": {"airport_pax_yr": 1_000_000, "airasia_share": 0.30, "load_factor": 0.85, "island_bound": 0.85, "attach": 0.35, "avg_fare_usd": 65},
    "jakarta": {"airport_pax_yr": 50_000_000, "airasia_share": 0.15, "load_factor": 0.85, "island_bound": 0.02, "attach": 0.20, "avg_fare_usd": 40},
    "kota-kinabalu": {"airport_pax_yr": 9_000_000, "airasia_share": 0.35, "load_factor": 0.85, "island_bound": 0.40, "attach": 0.30, "avg_fare_usd": 50},
    "langkawi": {"airport_pax_yr": 3_500_000, "airasia_share": 0.40, "load_factor": 0.85, "island_bound": 0.50, "attach": 0.32, "avg_fare_usd": 48},
    "penang": {"airport_pax_yr": 8_000_000, "airasia_share": 0.30, "load_factor": 0.85, "island_bound": 0.15, "attach": 0.25, "avg_fare_usd": 45},
    "desaru": {"airport_pax_yr": 4_000_000, "airasia_share": 0.25, "load_factor": 0.84, "island_bound": 0.25, "attach": 0.28, "avg_fare_usd": 50},
    "manila": {"airport_pax_yr": 48_000_000, "airasia_share": 0.28, "load_factor": 0.85, "island_bound": 0.12, "attach": 0.32, "avg_fare_usd": 45},
    "cebu": {"airport_pax_yr": 12_000_000, "airasia_share": 0.32, "load_factor": 0.85, "island_bound": 0.35, "attach": 0.30, "avg_fare_usd": 42},
    "boracay": {"airport_pax_yr": 2_200_000, "airasia_share": 0.45, "load_factor": 0.86, "island_bound": 0.90, "attach": 0.38, "avg_fare_usd": 40},
    "palawan": {"airport_pax_yr": 2_800_000, "airasia_share": 0.38, "load_factor": 0.85, "island_bound": 0.75, "attach": 0.35, "avg_fare_usd": 48},
    "siargao": {"airport_pax_yr": 450_000, "airasia_share": 0.42, "load_factor": 0.84, "island_bound": 0.92, "attach": 0.36, "avg_fare_usd": 45},
    "singapore": {"airport_pax_yr": 68_000_000, "airasia_share": 0.12, "load_factor": 0.85, "island_bound": 0.06, "attach": 0.22, "avg_fare_usd": 55},
}

ROADMAP_ROUTE_IDS = {"rn-81f865bba3ac"}  # PP↔El Nido Quanta-LR — exclude from floor


def hub_pool(slug: str) -> tuple[int, float]:
    m = HUB_MODEL[slug]
    seats = m["airport_pax_yr"] * m["airasia_share"] * m["load_factor"]
    oneway = int(seats * m["island_bound"] * m["attach"])
    return oneway, m["avg_fare_usd"]


def corridor_market_slug(c: dict) -> str | None:
    for key in ("_market_slug", "market_slug"):
        if c.get(key):
            return c[key]
    node = (c.get("from_node_id") or c.get("to_node_id") or "").lower()
    mapping = {
        "manila-philippines": "manila",
        "cebu-philippines": "cebu",
        "boracay-philippines": "boracay",
        "palawan-philippines": "palawan",
        "siargao-philippines": "siargao",
        "singapore": "singapore",
        "phuket-phang-nga-thailand": "phuket-andaman",
        "koh-samui-thailand": "koh-samui-gulf",
        "bali-indonesia": "bali-nusa-gili",
        "lombok-indonesia": "lombok",
        "komodo-flores-indonesia": "komodo-flores",
        "jakarta-indonesia": "jakarta",
        "sabah-kota-kinabalu-malaysia": "kota-kinabalu",
        "langkawi-malaysia": "langkawi",
        "penang-malaysia": "penang",
        "desaru-coast-malaysia": "desaru",
    }
    for k, v in mapping.items():
        if k in node:
            return v
    return None


def main() -> int:
    doc = json.loads(CORR_IN.read_text())
    partner = doc["markets"]["airasia-move"]
    corridors = partner["corridors"]
    by_slug: dict[str, list[dict]] = {}
    for c in corridors:
        slug = corridor_market_slug(c)
        if slug:
            by_slug.setdefault(slug, []).append(c)

    report = {"patched": [], "roadmap_held": [], "skipped": [], "hubs": {}}
    for slug, cs in by_slug.items():
        if slug not in HUB_MODEL:
            report["skipped"].append({"slug": slug, "n": len(cs), "reason": "no hub model"})
            continue
        pax_total, fare = hub_pool(slug)
        near = [c for c in cs if c.get("route_id") not in ROADMAP_ROUTE_IDS and (c.get("distance_nm") or 0) <= 70]
        roadmap = [c for c in cs if c.get("route_id") in ROADMAP_ROUTE_IDS or (c.get("distance_nm") or 0) > 70]
        share = max(1, len(near))
        pax_each = max(1, pax_total // share)
        report["hubs"][slug] = {"pool_oneway_pax_yr": pax_total, "fare_usd": fare, "corridors_near": len(near), "corridors_roadmap": len(roadmap)}
        for c in near:
            l3 = c.setdefault("L3_locals", {})
            l3["comparable_fare_usd_pax"] = fare
            l3["corridor_annual_oneway_pax"] = pax_each
            l3["_demand_record"] = {
                "value": pax_each,
                "unit": "premium-eligible one-way pax/yr",
                "basis": "arriving-seat distribution-capture",
                "confidence": "modeled_FLAG",
                "method": "hub_pool / n_near_corridors",
                "hub": slug,
            }
            l3["demand_confidence"] = "modeled_FLAG"
            c["_airasia_demand_hardened"] = True
            report["patched"].append({"slug": slug, "route_id": c.get("route_id"), "pax": pax_each, "fare": fare})
        for c in roadmap:
            c["_roadmap"] = True
            c["_in_grounded_floor"] = False
            c["vessel"] = c.get("vessel") or "Quanta-LR"
            l3 = c.setdefault("L3_locals", {})
            l3["corridor_annual_oneway_pax"] = 0
            l3["_demand_record"] = {"value": 0, "basis": "roadmap_quanta_lr", "note": "PP↔El Nido held out of floor"}
            report["roadmap_held"].append({"slug": slug, "route_id": c.get("route_id"), "nm": c.get("distance_nm")})

    doc["_airasia_demand_applied_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc["_anchor_ref"] = str(ANCHORS.relative_to(ROOT))
    CORR_OUT.write_text(json.dumps(doc, indent=2) + "\n")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"patched": len(report["patched"]), "roadmap_held": len(report["roadmap_held"]), "hubs": len(report["hubs"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())