#!/usr/bin/env python3
"""Bind dubai-rta and abu-dhabi-itc featured routes / journeys to gold geometry (Noon-grade)."""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC_PARTNERS = ROOT / "data-clean" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "uae-authority-noon-upgrade-report.json"

# Narrative label substring (lower) → gold bind
DUBAI_RTA_BINDINGS: dict[str, dict] = {
    "dubai creek ↔ dubai marina": {
        "route_id": "rn-96ac70c9ebf8",
        "from_node_id": "bp-56d5f5bd8d",
        "to_node_id": "bp-c2602e6640",
        "distance_nm": 15.5,
    },
    "dubai marina / harbour ↔ palm jumeirah / dubai islands": {
        "route_id": "rn-42aa1791bb60",
        "from_node_id": "bp-56d5f5bd8d",
        "to_node_id": "bp-051c982570",
        "distance_nm": 2.1,
    },
    "dubai creek ↔ dubai harbour / bluewaters": {
        "route_id": "rn-b1ba183aa886",
        "from_node_id": "bp-548f2fc0b7",
        "to_node_id": "bp-56d5f5bd8d",
        "distance_nm": 11.9,
    },
    "abu dhabi waterfront ↔ sir bani yas island": {
        "route_id": "rn-08f29522c5f2",
        "from_node_id": "abu-dhabi-uae",
        "to_node_id": "bp-a40b35cc0543",
        "distance_nm": 50.6,
    },
}

ABU_DHABI_ITC_BINDINGS: dict[str, dict] = {
    "corniche / downtown ↔ saadiyat cultural district": {
        "route_id": "rn-d94bb048e34e",
        "from_node_id": "bp-3b66a8ce1d",
        "to_node_id": "bp-4602a2affc9f",
        "distance_nm": 10.7,
    },
    "downtown ↔ yas island (events)": {
        "route_id": "rn-961cdc919083",
        "from_node_id": "bp-3b66a8ce1d",
        "to_node_id": "bp-7d4da7d9980a",
        "distance_nm": 2.5,
    },
    "yas island ↔ saadiyat cultural district": {
        "route_id": "rn-d94bb048e34e",
        "from_node_id": "bp-7d4da7d9980a",
        "to_node_id": "bp-4602a2affc9f",
        "distance_nm": 10.7,
    },
    "ghantoot (mid-corridor) → dubai waterfront": {
        "route_id": "e__uae__1b860507c38f",
        "from_node_id": "abu-dhabi-uae",
        "to_node_id": "dubai-uae",
        "distance_nm": 60.0,
    },
    "ghantoot (mid-corridor) ↔ dubai waterfront": {
        "route_id": "e__uae__1b860507c38f",
        "from_node_id": "abu-dhabi-uae",
        "to_node_id": "dubai-uae",
        "distance_nm": 60.0,
    },
}

JOURNEY_BINDINGS: dict[str, dict[str, dict]] = {
    "dubai-rta": {
        "dubai creek|dubai marina": DUBAI_RTA_BINDINGS["dubai creek ↔ dubai marina"],
        "dubai marina / harbour|palm jumeirah / dubai islands": DUBAI_RTA_BINDINGS[
            "dubai marina / harbour ↔ palm jumeirah / dubai islands"
        ],
        "dubai creek|dubai harbour / bluewaters": DUBAI_RTA_BINDINGS["dubai creek ↔ dubai harbour / bluewaters"],
        "abu dhabi waterfront|sir bani yas island": DUBAI_RTA_BINDINGS["abu dhabi waterfront ↔ sir bani yas island"],
    },
    "abu-dhabi-itc": {
        "corniche / downtown|saadiyat cultural district": ABU_DHABI_ITC_BINDINGS[
            "corniche / downtown ↔ saadiyat cultural district"
        ],
        "downtown|yas island (events)": ABU_DHABI_ITC_BINDINGS["downtown ↔ yas island (events)"],
        "yas island|saadiyat cultural district": ABU_DHABI_ITC_BINDINGS["yas island ↔ saadiyat cultural district"],
        "ghantoot (mid-corridor)|dubai waterfront": ABU_DHABI_ITC_BINDINGS["ghantoot (mid-corridor) → dubai waterfront"],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_gold() -> set[str]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    return {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}


def norm(s: str) -> str:
    return (s or "").strip().lower()


def bind_item(item: dict, spec: dict, gold: set[str]) -> bool:
    rid = spec.get("route_id")
    if not rid or rid not in gold:
        return False
    item["route_id"] = rid
    item["route_ids"] = [rid]
    for k in ("from_node_id", "to_node_id", "distance_nm"):
        if spec.get(k) is not None:
            item[k] = spec[k]
    item["_link_kind"] = "bp-corridor-candidate"
    item["_link_status"] = "linked-authority-noon-mirror"
    item["_link_source"] = "grok/upgrade_uae_authority_from_noon"
    item.pop("_hold_reason", None)
    item.setdefault("economics_status", "economics_pending")
    return True


def upgrade_partner(slug: str, bindings: dict[str, dict], journey_map: dict[str, dict], gold: set[str]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    bound_fr = bound_j = 0
    for phase in doc.get("phases") or []:
        for fr in phase.get("featured_routes") or []:
            key = norm(fr.get("label", ""))
            spec = bindings.get(key)
            if spec and bind_item(fr, spec, gold):
                bound_fr += 1
    for j in doc.get("journeys_unlocked") or []:
        jkey = f"{norm(j.get('from',''))}|{norm(j.get('to',''))}"
        spec = journey_map.get(jkey)
        if spec and bind_item(j, spec, gold):
            bound_j += 1
    doc.setdefault("_authority_noon_upgrade", {})["applied_at"] = utc_now()
    doc["_authority_noon_upgrade"]["featured_bound"] = bound_fr
    doc["_authority_noon_upgrade"]["journeys_bound"] = bound_j
    for out in (path, DC_PARTNERS / f"{slug}.json"):
        out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "featured_bound": bound_fr, "journeys_bound": bound_j}


def main() -> int:
    gold = load_gold()
    results = {
        "at": utc_now(),
        "lane": "grok/upgrade_uae_authority_from_noon",
        "partners": [
            upgrade_partner("dubai-rta", DUBAI_RTA_BINDINGS, JOURNEY_BINDINGS["dubai-rta"], gold),
            upgrade_partner("abu-dhabi-itc", ABU_DHABI_ITC_BINDINGS, JOURNEY_BINDINGS["abu-dhabi-itc"], gold),
        ],
    }
    REPORT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())