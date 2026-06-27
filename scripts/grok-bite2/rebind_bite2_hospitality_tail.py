#!/usr/bin/env python3
"""Rebind cote-dazur / d-marin / discovery-land from cluster brief signatures (#115 tail)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff/partner-map-model/bite2-hospitality-tail-rebind.json"

PARTNER_SPECS = {
    "cote-dazur": {
        "cluster": "france",
        "journeys": [
            {
                "from": "Nice (Port)",
                "to": "Monaco (Port Hercule)",
                "today": "Helicopter or gridlocked Corniche road.",
                "with_navier": "Silent foiling hop — the iconic Riviera corridor.",
                "distance_nm": 6.5,
                "platform": "Pioneer II",
                "archetype": "luxury",
                "from_node_id": "cote-dazur-france",
                "to_node_id": "monaco-monaco",
                "route_id": "e__cote-dazur-france__port-de-nice__monaco-monaco__port-hercule",
            },
            {
                "from": "Cannes",
                "to": "Îles de Lérins (Sainte-Marguerite)",
                "today": "Diesel excursion boat.",
                "with_navier": "Quiet foiling island crossing.",
                "distance_nm": 3.0,
                "platform": "Pioneer II",
                "archetype": "tourism",
                "from_node_id": "cote-dazur-france",
                "to_node_id": "cote-dazur-france",
                "route_id": "ics-529325c5eb",
            },
        ],
        "phases": [
            {"cities": ["cote-dazur-france", "monaco-monaco"], "featured_route_id": "e__cote-dazur-france__port-de-nice__monaco-monaco__port-hercule"},
            {"cities": ["cote-dazur-france"], "featured_route_id": "ics-529325c5eb"},
            {"cities": ["cote-dazur-france"], "featured_route_id": "rn-147bf78ddf5b"},
        ],
    },
    "d-marin": {
        "cluster": "croatia",
        "journeys": [
            {
                "from": "Split",
                "to": "Hvar",
                "today": "Scheduled catamaran — sells out in summer.",
                "with_navier": "On-demand foiling crossing.",
                "distance_nm": 25.2,
                "platform": "Pioneer II",
                "archetype": "tourism",
                "from_node_id": "split-croatia",
                "to_node_id": "hvar-croatia",
                "route_id": "edge__hvar-croatia__split",
            },
            {
                "from": "Korčula",
                "to": "Dubrovnik",
                "today": "Ferry or charter yacht.",
                "with_navier": "Premium foiling link along southern Dalmatia.",
                "distance_nm": 46.3,
                "platform": "Pioneer II",
                "archetype": "tourism",
                "from_node_id": "korcula-croatia",
                "to_node_id": "dubrovnik-croatia",
                "route_id": "edge__korcula-croatia__dubrovnik",
            },
        ],
        "phases": [
            {"cities": ["split-croatia", "hvar-croatia"], "featured_route_id": "edge__hvar-croatia__split"},
            {"cities": ["korcula-croatia", "dubrovnik-croatia"], "featured_route_id": "edge__korcula-croatia__dubrovnik"},
            {"cities": ["split-croatia"], "featured_route_id": "rn-ae7179e3ce7b"},
        ],
    },
    "discovery-land": {
        "cluster": "florida-usa",
        "journeys": [
            {
                "from": "Nassau",
                "to": "Paradise Island / resort cay",
                "today": "Diesel tender — loud and weather-exposed.",
                "with_navier": "Signature silent foiling club arrival.",
                "distance_nm": 4.4,
                "platform": "Pioneer II",
                "archetype": "luxury",
                "from_node_id": "nassau-bahamas",
                "to_node_id": "nassau-bahamas",
                "route_id": "ics-3e84761396",
            },
            {
                "from": "Miami",
                "to": "Nassau",
                "today": "Private aviation + separate boat leg.",
                "with_navier": "Quanta-LR trunk linking Florida to the Bahamas clubs.",
                "distance_nm": 154.9,
                "platform": "Quanta-LR",
                "archetype": "intercity",
                "from_node_id": "miami-florida-usa",
                "to_node_id": "nassau-bahamas",
                "route_id": "edge__miami-florida-usa__nassau-bahamas",
            },
        ],
        "phases": [
            {"cities": ["nassau-bahamas"], "featured_route_id": "ics-3e84761396"},
            {"cities": ["miami-florida-usa", "nassau-bahamas"], "featured_route_id": "edge__miami-florida-usa__nassau-bahamas"},
            {"cities": ["nassau-bahamas"], "featured_route_id": "ics-582bb891bc"},
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_routes() -> dict[str, dict]:
    routes = json.loads((ROOT / "data-clean/ROUTES.json").read_text())
    return {f["properties"]["id"]: f["properties"] for f in routes if f.get("properties", {}).get("id")}


def journey_row(spec: dict, props: dict) -> dict:
    rid = spec["route_id"]
    return {
        **spec,
        "route_ids": [rid],
        "_link_kind": "hospitality-flagship",
        "_link_status": "linked-grok-bite2-tail",
        "_link_source": "grok/rebind_bite2_hospitality_tail",
        "economics_status": "economics_pending",
        "display": "geometry" if props.get("geometry") else "text_only",
        "distance_nm": props.get("distance_nm") or spec.get("distance_nm"),
    }


def featured_row(j: dict) -> dict:
    return {
        "label": f"{j['from']} ↔ {j['to']}",
        "from_node_id": j["from_node_id"],
        "to_node_id": j["to_node_id"],
        "distance_nm": j.get("distance_nm"),
        "platform": j.get("platform"),
        "route_id": j["route_id"],
        "route_ids": [j["route_id"]],
        "_link_kind": "hospitality-flagship",
        "_link_status": "linked-grok-bite2-tail",
        "_link_source": "grok/rebind_bite2_hospitality_tail",
        "economics_status": "economics_pending",
    }


def rebind_partner(slug: str, spec: dict, gold: dict[str, dict]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    journeys = []
    for js in spec["journeys"]:
        props = gold.get(js["route_id"], {})
        if js["route_id"] not in gold:
            return {"partner": slug, "error": f"missing route {js['route_id']}"}
        journeys.append(journey_row(js, props))
    doc["journeys_unlocked"] = journeys

    for i, ph in enumerate(doc.get("phases") or []):
        if i < len(spec["phases"]):
            ps = spec["phases"][i]
            ph["cities"] = ps["cities"]
            rid = ps["featured_route_id"]
            if rid not in gold:
                return {"partner": slug, "error": f"missing phase route {rid}"}
            js = next((s for s in spec["journeys"] if s["route_id"] == rid), None)
            if js:
                j = journey_row(js, gold[rid])
            else:
                p = gold[rid]
                j = {
                    "from": p.get("from", "origin"),
                    "to": p.get("to", "destination"),
                    "from_node_id": p.get("from_city_id") or p.get("from"),
                    "to_node_id": p.get("to_city_id") or p.get("to"),
                    "route_id": rid,
                    "route_ids": [rid],
                    "distance_nm": p.get("distance_nm"),
                    "platform": "Quanta-LR" if (p.get("distance_nm") or 0) > 70 else "Pioneer II",
                    "_link_kind": "hospitality-flagship",
                    "_link_status": "linked-grok-bite2-tail",
                    "_link_source": "grok/rebind_bite2_hospitality_tail",
                    "economics_status": "economics_pending",
                }
            ph["featured_routes"] = [featured_row(j)]

    doc["_bite2_hospitality_rebind"] = {"at": utc_now(), "cluster": spec["cluster"], "route_ids": [j["route_id"] for j in journeys]}
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "journeys": len(journeys), "route_ids": [j["route_id"] for j in journeys]}


def main() -> int:
    gold = load_routes()
    results = [rebind_partner(slug, spec, gold) for slug, spec in PARTNER_SPECS.items()]
    out = {"at": utc_now(), "results": results}
    REPORT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0 if all("error" not in r for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())