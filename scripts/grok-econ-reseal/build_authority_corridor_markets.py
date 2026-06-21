#!/usr/bin/env python3
"""Patch corridors.json with RAKTA + Bahrain MOTC sealed authority routes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRIDORS = ROOT / "finance" / "model" / "corridors.json"
ROUTES = ROOT / "data-clean" / "ROUTES.json"
HANDOFF = ROOT / "handoff" / "partner-map-model"

ANCHORS = {
    "rakta": {
        "label": "RAKTA — Ras Al Khaimah authority network",
        "fare_usd": 35.0,
        "market_pax_yr": 240000,
        "archetype": "authority",
        "country": "United Arab Emirates",
        "region": "MENA",
    },
    "bahrain-motc": {
        "label": "Bahrain MOTC — Manama authority network",
        "fare_usd": 28.0,
        "market_pax_yr": 180000,
        "archetype": "authority",
        "country": "Bahrain",
        "region": "MENA",
    },
}


def routes_index() -> dict[str, dict]:
    raw = json.loads(ROUTES.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    return {f["properties"]["id"]: f["properties"] for f in feats if f.get("properties", {}).get("id")}


def sealed_ids(partner: str) -> list[str]:
    path = ROOT / "partner-pitch" / "partners" / f"{partner}.json"
    doc = json.loads(path.read_text())
    ids = []
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            rid = fr.get("route_id")
            if rid:
                ids.append(rid)
    return list(dict.fromkeys(ids))


def l3(fare: float, pax: int, archetype: str) -> dict:
    return {
        "comparable_fare_usd_pax": fare,
        "corridor_annual_oneway_pax": pax,
        "demand_confidence": "med-low",
        "_fare_record": {"value": fare, "source_tier": "T3", "confidence": "med-low", "method": "authority anchor split"},
        "_demand_record": {"value": pax, "basis": "addressable", "source_tier": "T3", "confidence": "med-low"},
    }


def main() -> int:
    by_id = routes_index()
    corr = json.loads(CORRIDORS.read_text())
    markets = corr.setdefault("markets", {})
    for partner, anchor in ANCHORS.items():
        rids = sealed_ids(partner)
        if not rids:
            continue
        pax_each = max(3000, int(anchor["market_pax_yr"] / len(rids)))
        rows = []
        for rid in rids:
            p = by_id.get(rid, {})
            nm = float(p.get("distance_nm") or 0)
            rows.append({
                "route_id": rid,
                "from": p.get("from_label", ""),
                "to": p.get("to_label", ""),
                "distance_nm": nm,
                "vessel": "Pioneer II" if nm <= 70 else "Quanta-LR",
                "archetype": anchor["archetype"],
                "from_node_id": p.get("from_city_id"),
                "to_node_id": p.get("to_city_id"),
                "country": anchor["country"],
                "pool_basis": "addressable",
                "_authority_sealed": True,
                "L3_locals": l3(anchor["fare_usd"], pax_each, anchor["archetype"]),
            })
        mid = f"gulf-authority-{partner}"
        markets[mid] = {
            "partner": partner,
            "region": anchor["region"],
            "label": anchor["label"],
            "fleet_basis": "network_sum",
            "fleet_rounding": "ceil",
            "_market_note": f"Authority finance cascade — {len(rows)} sealed featured routes",
            "corridors": rows,
        }
        print(f"  {mid}: {len(rows)} corridors")
    corr.setdefault("_meta", {})["authority_markets_at"] = "2026-06-21"
    CORRIDORS.write_text(json.dumps(corr, indent=1, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())