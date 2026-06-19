#!/usr/bin/env python3
"""Mint Portugal corridor BPs missing from gold (Porto Gaia, Algarve, Guadiana)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NEW_BPS = [
    {
        "id": "bp-porto-gaia",
        "name": "Vila Nova de Gaia (Cais de Gaia)",
        "shortName": "Cais de Gaia",
        "parent_city_id": "porto-douro-portugal",
        "lng": -8.6132,
        "lat": 41.1384,
        "bp_type": "ferry_terminal",
        "linked_locale": "Vila Nova de Gaia waterfront",
        "relevance": "P1",
        "operator": "Douro river cruise operators",
        "source": "https://ttsl.pt/",
    },
    {
        "id": "bp-lagos-marina",
        "name": "Marina de Lagos",
        "shortName": "Marina de Lagos",
        "parent_city_id": "lisbon-tagus-portugal",
        "lng": -8.6742,
        "lat": 37.1088,
        "bp_type": "marina",
        "linked_locale": "Lagos waterfront",
        "relevance": "P2",
        "operator": "Lagos marina operators",
        "source": "https://www.marinadelagos.com/",
    },
    {
        "id": "bp-ponta-da-piedade",
        "name": "Ponta da Piedade (sea caves jetty)",
        "shortName": "Ponta da Piedade",
        "parent_city_id": "lisbon-tagus-portugal",
        "lng": -8.6675,
        "lat": 37.0785,
        "bp_type": "public_pier",
        "linked_locale": "Ponta da Piedade grottoes",
        "relevance": "P2",
        "operator": "Lagos excursion boats",
        "source": "navier-coverage-2026-06-19",
    },
    {
        "id": "bp-vila-real-santo-antonio",
        "name": "Vila Real de Santo António (Guadiana)",
        "shortName": "Vila Real de Santo António",
        "parent_city_id": "lisbon-tagus-portugal",
        "lng": -7.4172,
        "lat": 37.1953,
        "bp_type": "ferry_terminal",
        "linked_locale": "Guadiana north bank",
        "relevance": "P2",
        "operator": "Guadiana cross-border ferry",
        "source": "navier-coverage-2026-06-19",
    },
    {
        "id": "bp-ayamonte-spain",
        "name": "Ayamonte (Spain, Guadiana)",
        "shortName": "Ayamonte",
        "parent_city_id": "lisbon-tagus-portugal",
        "lng": -7.4041,
        "lat": 37.2012,
        "bp_type": "ferry_terminal",
        "linked_locale": "Ayamonte waterfront",
        "relevance": "P2",
        "operator": "Guadiana cross-border ferry",
        "source": "navier-coverage-2026-06-19",
    },
]


def poi_feature(bp: dict) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [bp["lng"], bp["lat"]]},
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "name": bp["name"],
            "shortName": bp["shortName"],
            "parent_city_id": bp["parent_city_id"],
            "bp_type": bp["bp_type"],
            "bp_type_label": bp["bp_type"].replace("_", " ").title(),
            "relevance": bp["relevance"],
            "operator": bp.get("operator"),
            "coords_resolved": True,
            "confidence": "high",
            "precision": "web_research_canonical",
            "source": bp.get("source"),
            "linked_locale": bp.get("linked_locale"),
            "_gazetteer_source": "grok-portugal-corridor-patch-2026-06-19",
            "_tasklet_provenance": "grok-portugal-corridor-patch-2026-06-19",
            "last_enriched": now,
            "status": "operational",
        },
    }


def main():
    dc = ROOT / "data-clean"
    fbt_path = dc / "FEATURES_BY_TYPE.json"
    fbt = json.loads(fbt_path.read_text())
    pois = fbt.setdefault("poi", [])
    existing = {p.get("properties", p).get("id") for p in pois}
    added = []
    for bp in NEW_BPS:
        if bp["id"] in existing:
            continue
        pois.append(poi_feature(bp))
        added.append(bp["id"])
    fbt_path.write_text(json.dumps(fbt, indent=2) + "\n")
    print(json.dumps({"added": added, "total_pois": len(pois)}, indent=2))


if __name__ == "__main__":
    main()