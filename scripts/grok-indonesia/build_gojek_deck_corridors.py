#!/usr/bin/env python3
"""Build per-market scoped corridors for Gojek 10-market deck economics."""
from __future__ import annotations

import copy
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean" / "partners"
RECAL = ROOT / "finance" / "recal"
CORR_SRC = RECAL / "corridors-gojek.json"
OUT = RECAL / "corridors-gojek-deck.json"

STUB_CORRIDORS = {
    "rn-33fe0cc24a60": {
        "from": "Tambolaka Airport gateway (Waikabubak)",
        "to": "NIHI Sumba (private jetty + beach-landing)",
        "distance_nm": 35.0,
        "fare": 120,
        "pax": 8000,
    },
    "rn-c77ad1314ae3": {
        "from": "NIHI Sumba (private jetty + beach-landing)",
        "to": "Cap Karoso (Kerewe / Karoso SW coast)",
        "distance_nm": 18.0,
        "fare": 85,
        "pax": 5000,
    },
}

DECK_MARKETS = [
    "jakarta",
    "bali-nusa-gili",
    "lombok",
    "komodo-flores",
    "sumba",
    "riau-singapore",
    "singapore",
    "raja-ampat",
    "likupang",
    "lake-toba",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect_route_ids_by_market(doc: dict) -> dict[str, set[str]]:
    by_mkt: dict[str, set[str]] = defaultdict(set)

    def add(slug: str, rid: str | None) -> None:
        if slug and rid and isinstance(rid, str) and not rid.endswith("-shared"):
            by_mkt[slug].add(rid)

    for m in doc.get("markets") or []:
        slug = m.get("slug") or m.get("id")
        if slug not in DECK_MARKETS:
            continue
        for j in m.get("journeys_unlocked") or []:
            add(slug, j.get("route_id"))
            for x in j.get("route_ids") or []:
                add(slug, x)
        phases = m.get("phases") or []
        phase_iter = phases.values() if isinstance(phases, dict) else phases
        for ph in phase_iter:
            if not isinstance(ph, dict):
                continue
            for fr in ph.get("featured_routes") or []:
                add(slug, fr.get("route_id"))
                for x in fr.get("route_ids") or []:
                    add(slug, x)
        for gc in (m.get("growth_case") or {}).get("phases") or []:
            if not isinstance(gc, dict):
                continue
            for fr in gc.get("featured_routes") or []:
                add(slug, fr.get("route_id"))
    return by_mkt


def main() -> int:
    doc = json.loads((DC / "gojek.json").read_text())
    src = json.loads(CORR_SRC.read_text())
    gojek_block = src["markets"]["gojek"]
    all_corridors = {c["route_id"]: c for c in gojek_block.get("corridors") or [] if c.get("route_id")}

    def stub_corridor(rid: str) -> dict:
        spec = STUB_CORRIDORS[rid]
        fare = spec["fare"]
        pax = spec["pax"]
        return {
            "route_id": rid,
            "from": spec["from"],
            "to": spec["to"],
            "distance_nm": spec["distance_nm"],
            "vessel": "N30 Pioneer II",
            "archetype": "tourism",
            "country": "Indonesia",
            "pool_basis": "addressable",
            "L3_locals": {
                "comparable_fare_usd_pax": fare,
                "corridor_annual_oneway_pax": pax,
                "_demand_record": {
                    "value": pax,
                    "unit": "pax/yr one-way",
                    "source_tier": "T3",
                    "confidence": "med-low",
                    "source": "indonesia-frontier-seal",
                    "method": "gojek-deck/stub_until_sidecar",
                },
                "_fare_record": {
                    "value": fare,
                    "unit": "USD/pax/one-way",
                    "source_tier": "T3",
                    "confidence": "med",
                    "source": "indonesia-frontier-seal",
                    "method": "gojek-deck/stub_until_sidecar",
                },
                "demand_confidence": "med-low",
            },
            "_gojek_deck_stub": True,
            "_vessel_key": "pioneer_ii",
        }

    by_mkt = collect_route_ids_by_market(doc)
    out_markets = {}
    report = {"markets": {}, "unassigned_corridors": []}

    for slug in DECK_MARKETS:
        rids = sorted(by_mkt.get(slug) or [])
        corridors = []
        for rid in rids:
            if rid in all_corridors:
                corridors.append(copy.deepcopy(all_corridors[rid]))
            elif rid in STUB_CORRIDORS:
                corridors.append(stub_corridor(rid))
        out_markets[slug] = {
            "partner": "gojek",
            "region": "SEA",
            "label": next(
                (m.get("label") for m in doc.get("markets") or [] if (m.get("slug") or m.get("id")) == slug),
                slug,
            ),
            "fleet_basis": "network_sum",
            "fleet_rounding": "ceil",
            "_scope": "gojek-deck-10-market",
            "_route_ids_bound": len(corridors),
            "corridors": corridors,
        }
        report["markets"][slug] = {"route_ids": len(rids), "corridors": len(corridors)}

    assigned = {rid for s in DECK_MARKETS for rid in by_mkt.get(s, ())}
    for rid in sorted(all_corridors):
        if rid not in assigned:
            report["unassigned_corridors"].append(rid)

    out = {
        "_doc": "Gojek 10-market deck scope — per-market corridors for gen_deck_economics.py",
        "_source": str(CORR_SRC),
        "_built_at": utc_now(),
        "capture_rate": src.get("capture_rate", 0.1),
        "markets": out_markets,
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"out": str(OUT), **report}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())