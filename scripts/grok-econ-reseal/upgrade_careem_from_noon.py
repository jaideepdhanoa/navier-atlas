#!/usr/bin/env python3
"""
Upgrade Careem UAE proposal to Noon-grade BP-bound seals.

Noon is the reference partner for UAE geometry binding. Careem keeps super-app
narrative but inherits Noon's sealed featured_routes and journey route_ids where
the corridor semantics align. Null beats wrong — held-null items get explicit
_hold_reason for Tasklet.
"""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC_PARTNERS = ROOT / "data-clean" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "careem-noon-upgrade-report.json"

UAE_CITIES = frozenset(
    {
        "abu-dhabi-uae",
        "dubai-uae",
        "fujairah-uae",
        "ras-al-khaimah-uae",
        "sharjah-uae",
    }
)

# Careem journey (from,to) normalized → sealed route binding
JOURNEY_ROUTE_MAP: dict[tuple[str, str], dict] = {
    ("dubai marina / bluewaters", "downtown creek / festival city"): {
        "route_id": "rn-2e112eb57142",
        "route_ids": [
            "rn-2e112eb57142",
            "gcn-5f710d44d4-careem",
            "rn-656e8e7d6b4d",
            "gcn-1662e39eb7-careem",
        ],
        "from_node_id": "bp-56d5f5bd8d",
        "to_node_id": "bp-b3458dd3c6",
        "note": "Bluewaters/Festival City sealed legs; city-label card retained for narrative",
    },
    ("dubai", "the world / palm / offshore resorts"): {
        "route_id": "gcn-6a2841d6db-careem",
        "from_node_id": "bp-56d5f5bd8d",
        "to_node_id": "dubai-uae",
    },
    ("dubai", "abu dhabi (yas / saadiyat)"): {
        "route_id": "gcn-360882a646-careem",
        "route_ids": ["rn-80c408c085a6", "gcn-360882a646-careem"],
        "from_node_id": "dubai-uae",
        "to_node_id": "abu-dhabi-uae",
    },
    ("sharjah (al khan / khalid lagoon)", "dubai (marina / festival city)"): {
        "route_id": "gcn-8e3c2d581c-careem",
        "route_ids": ["gcn-8e3c2d581c-careem", "rn-12245df07550"],
        "from_node_id": "bp-f0fde14967",
        "to_node_id": "bp-56d5f5bd8d",
        "note": "Al Khan Lagoon mouth ↔ Dubai Harbour — Noon phase-2 seal",
    },
    ("fujairah east-coast cluster", "dibba · khor fakkan · kalba"): {
        "route_id": "gcn-8f0d49bbde-careem",
        "route_ids": ["rn-bc685bdb0da3", "gcn-8f0d49bbde-careem"],
        "from_node_id": "fujairah-uae",
        "to_node_id": "bp-82af5d5862",
    },
}


def norm_pair(a: str, b: str) -> tuple[str, str]:
    return (a.strip().lower(), b.strip().lower())


def load_gold_ids() -> set[str]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    return {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}


def noon_sealed_featured(noon: dict) -> list[dict]:
    """Collect Noon phase 1–2 BP-bound featured rows (active UAE only)."""
    rows: list[dict] = []
    for phase in noon.get("phases", []) or []:
        if phase.get("n") not in (1, 2):
            continue
        if phase.get("aspirational"):
            continue
        for fr in phase.get("featured_routes", []) or []:
            if not isinstance(fr, dict):
                continue
            rid = fr.get("route_id")
            if not rid:
                continue
            rows.append(copy.deepcopy(fr))
    return rows


def careem_featured_from_noon(fr: dict, gold_ids: set[str]) -> dict:
    """Adapt a Noon featured row for Careem super-app framing."""
    out = copy.deepcopy(fr)
    rid = out.get("route_id")
    if rid and rid not in gold_ids:
        out["route_id"] = None
        out["_link_status"] = "held-null-not-in-gold"
        return out
    out["_link_kind"] = "bp-corridor-candidate"
    out["_link_status"] = "linked-careem-noon-mirror"
    out["_link_source"] = "grok/upgrade_careem_from_noon"
    out.setdefault("platform", out.get("platform") or "N30 Pioneer II")
    out.setdefault("economics_status", "economics_pending")
    out["archetype"] = "super_app"
    return out


def bind_journey(j: dict, gold_ids: set[str]) -> bool:
    key = norm_pair(j.get("from", ""), j.get("to", ""))
    spec = JOURNEY_ROUTE_MAP.get(key)
    if not spec:
        return False
    rid = spec.get("route_id")
    if rid and rid not in gold_ids:
        j["route_id"] = None
        j["_link_status"] = "held-null-not-in-gold"
        j["_hold_reason"] = f"mapped route {rid} missing from gold"
        return False
    if rid:
        j["route_id"] = rid
    rids = [x for x in (spec.get("route_ids") or []) if x in gold_ids]
    if rids:
        j["route_ids"] = rids
    for k in ("from_node_id", "to_node_id"):
        if spec.get(k):
            j[k] = spec[k]
    j["_link_kind"] = "bp-corridor-candidate"
    j["_link_status"] = "linked-careem-noon-mirror"
    j["_link_source"] = "grok/upgrade_careem_from_noon"
    if spec.get("note"):
        j["_mirror_note"] = spec["note"]
    j.setdefault("economics_status", "economics_pending")
    return True


def merge_noon_featured_into_careem(careem: dict, noon_rows: list[dict], gold_ids: set[str]) -> int:
    """Append Noon sealed BP corridors to Careem phase 3 featured_routes (visible on page)."""
    added = 0
    phase3 = next((p for p in careem.get("phases", []) if p.get("n") == 3), None)
    if not phase3:
        return 0
    featured = phase3.setdefault("featured_routes", [])
    existing_rids = {
        fr.get("route_id")
        for fr in featured
        if isinstance(fr, dict) and fr.get("route_id")
    }
    for fr in noon_rows:
        adapted = careem_featured_from_noon(fr, gold_ids)
        rid = adapted.get("route_id")
        if rid and rid in existing_rids:
            continue
        featured.append(adapted)
        if rid:
            existing_rids.add(rid)
        added += 1
    return added


def _apply_spec_to_featured(fr: dict, spec: dict, gold_ids: set[str], tag: str) -> bool:
    rid = spec.get("route_id")
    if not rid or rid not in gold_ids:
        return False
    fr["route_id"] = rid
    rids = [x for x in (spec.get("route_ids") or []) if x in gold_ids]
    if rids:
        fr["route_ids"] = rids
    for k in ("from_node_id", "to_node_id"):
        if spec.get(k):
            fr[k] = spec[k]
    fr["_link_status"] = "linked-careem-noon-mirror"
    fr["_link_source"] = "grok/upgrade_careem_from_noon"
    return True


def upgrade_featured_in_phases(careem: dict, gold_ids: set[str]) -> list[str]:
    changes: list[str] = []
    label_specs = [
        (("sharjah", "dubai"), ("sharjah (al khan / khalid lagoon)", "dubai (marina / festival city)")),
        (("marina", "creek"), ("dubai marina / bluewaters", "downtown creek / festival city")),
        (("dubai", "abu dhabi"), ("dubai", "abu dhabi (yas / saadiyat)")),
        (("world", "palm"), ("dubai", "the world / palm / offshore resorts")),
        (("fujairah", "dibba"), ("fujairah east-coast cluster", "dibba · khor fakkan · kalba")),
    ]
    for phase in careem.get("phases", []) or []:
        if phase.get("aspirational") or phase.get("n") == 4:
            continue
        for fr in phase.get("featured_routes", []) or []:
            if not isinstance(fr, dict):
                continue
            label = fr.get("label", "").lower()
            if "quanta-lr" in label or "aspirational" in label:
                continue
            for tokens, key in label_specs:
                if all(t in label for t in tokens):
                    spec = JOURNEY_ROUTE_MAP.get(key)
                    if spec and _apply_spec_to_featured(fr, spec, gold_ids, key[0]):
                        changes.append(f"featured {fr.get('label')} → {spec['route_id']}")
                    break
    return changes


def main() -> int:
    gold_ids = load_gold_ids()
    noon = json.loads((PARTNERS / "noon.json").read_text())
    careem = json.loads((PARTNERS / "careem.json").read_text())

    noon_rows = noon_sealed_featured(noon)
    journey_changes: list[str] = []
    for j in careem.get("journeys_unlocked", []) or []:
        if bind_journey(j, gold_ids):
            journey_changes.append(f"{j.get('from')} → {j.get('to')} → {j.get('route_id')}")

    featured_changes = upgrade_featured_in_phases(careem, gold_ids)
    pool_added = merge_noon_featured_into_careem(careem, noon_rows, gold_ids)

    careem["_careem_noon_mirror"] = {
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "reference": "noon.json BP-bound UAE seals",
        "noon_sealed_rows_inherited": pool_added,
        "policy": "Careem narrative preserved; geometry binds mirror Noon",
    }

    report = {
        "at": datetime.now(timezone.utc).isoformat(),
        "journey_binds": journey_changes,
        "featured_binds": featured_changes,
        "sealed_pool_added": pool_added,
        "noon_reference_rows": len(noon_rows),
    }

    for path in (PARTNERS / "careem.json", DC_PARTNERS / "careem.json"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(careem, indent=2, ensure_ascii=False) + "\n")

    HANDOFF.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())