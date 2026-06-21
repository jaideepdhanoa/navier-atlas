#!/usr/bin/env python3
"""
Audit and align Noon ↔ Careem UAE proposals.

Noon is the BP-bound reference (PR #58 seal lane). Careem inherits the same
sealed corridor objects for matching UAE journey labels where geometry exists.
"""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "noon-careem-mirror-audit.json"

UAE_CITIES = frozenset(
    {
        "abu-dhabi-uae",
        "dubai-uae",
        "fujairah-uae",
        "ras-al-khaimah-uae",
        "sharjah-uae",
    }
)

JOURNEY_LABEL_KEYS = (
    ("dubai marina / bluewaters", "downtown creek / festival city"),
    ("dubai", "the world / palm / offshore resorts"),
    ("dubai", "abu dhabi (yas / saadiyat)"),
    ("sharjah (al khan / khalid lagoon)", "dubai (marina / festival city)"),
    ("fujairah east-coast cluster", "dibba · khor fakkan · kalba"),
)


def norm_pair(a: str, b: str) -> tuple[str, str]:
    return (a.strip().lower(), b.strip().lower())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def noon_featured_index(noon: dict) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for phase in noon.get("phases", []):
        for fr in phase.get("featured_routes", []) or []:
            if isinstance(fr, dict) and fr.get("label"):
                idx[fr["label"]] = fr
    return idx


def apply_noon_mirror_to_careem(careem: dict, noon: dict, gold_ids: set[str]) -> tuple[dict, list[str]]:
    changes: list[str] = []
    out = copy.deepcopy(careem)
    noon_by_label = noon_featured_index(noon)

    for phase in out.get("phases", []):
        cities = set(phase.get("cities") or [])
        if not cities & UAE_CITIES:
            continue
        for i, fr in enumerate(phase.get("featured_routes", []) or []):
            if not isinstance(fr, dict):
                continue
            ref = noon_by_label.get(fr.get("label", ""))
            if not ref:
                continue
            merged = copy.deepcopy(fr)
            for key in (
                "from_node_id",
                "to_node_id",
                "from_label",
                "to_label",
                "distance_nm",
                "platform",
                "route_id",
                "vessel_gate",
                "economics_status",
                "model_link",
            ):
                if ref.get(key) is not None:
                    merged[key] = ref[key]
            rid = merged.get("route_id")
            if rid and rid not in gold_ids:
                merged["route_id"] = None
                merged["_link_status"] = "held-null-not-in-gold"
            elif rid:
                merged["_link_kind"] = ref.get("_link_kind") or "bp-corridor-candidate"
                merged["_link_status"] = "linked-noon-mirror"
                merged["_link_source"] = "grok/audit_mirror_noon_careem"
                changes.append(f"careem featured '{merged.get('label')}' -> {rid}")
            phase["featured_routes"][i] = merged

    noon_journey_by_pair: dict[tuple[str, str], dict] = {}
    for j in noon.get("journeys_unlocked", []) or []:
        if isinstance(j, dict) and j.get("from") and j.get("to"):
            noon_journey_by_pair[norm_pair(j["from"], j["to"])] = j

    for j in out.get("journeys_unlocked", []) or []:
        if not isinstance(j, dict):
            continue
        key = norm_pair(j.get("from", ""), j.get("to", ""))
        ref = noon_journey_by_pair.get(key)
        if not ref:
            continue
        rid = ref.get("route_id")
        if rid and rid in gold_ids:
            j["route_id"] = rid
            j["from_node_id"] = ref.get("from_node_id") or j.get("from_node_id")
            j["to_node_id"] = ref.get("to_node_id") or j.get("to_node_id")
            j["_link_status"] = "linked-noon-mirror"
            j["_link_source"] = "grok/audit_mirror_noon_careem"
            j.setdefault("economics_status", ref.get("economics_status", "economics_pending"))
            changes.append(f"careem journey {j.get('from')} -> {j.get('to')} -> {rid}")

    out["_noon_mirror_audit"] = {
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "reference": "noon.json PR58 BP-bound featured_routes",
    }
    return out, changes


def audit(doc: dict, name: str, gold_ids: set[str]) -> dict:
    journeys = doc.get("journeys_unlocked", []) or []
    linked = 0
    broken: list[str] = []
    for j in journeys:
        rid = j.get("route_id")
        rids = j.get("route_ids") or []
        if rid and rid in gold_ids:
            linked += 1
        elif rid:
            broken.append(f"journey {j.get('from')}->{j.get('to')}: {rid}")
        elif rids and any(x in gold_ids for x in rids):
            linked += 1
        elif not rid and not rids:
            broken.append(f"unlinked {j.get('from')}->{j.get('to')} ({j.get('_link_status')})")

    fr_total = 0
    fr_linked = 0

    def walk(o):
        nonlocal fr_total, fr_linked
        if isinstance(o, dict):
            if "featured_routes" in o:
                for fr in o.get("featured_routes") or []:
                    if isinstance(fr, dict):
                        fr_total += 1
                        rid = fr.get("route_id")
                        rids = fr.get("route_ids") or []
                        if rid and rid in gold_ids:
                            fr_linked += 1
                        elif rids and any(x in gold_ids for x in rids):
                            fr_linked += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(doc)
    return {
        "partner": name,
        "journeys": len(journeys),
        "journeys_linked": linked,
        "journeys_broken": broken,
        "featured_routes": fr_total,
        "featured_linked": fr_linked,
    }


def main() -> int:
    routes = load_json(ROOT / "data-clean" / "ROUTES.json")
    if isinstance(routes, list):
        gold_ids = {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}
    else:
        gold_ids = set()

    noon = load_json(PARTNERS / "noon.json")
    careem = load_json(PARTNERS / "careem.json")

    before = {
        "noon": audit(noon, "noon", gold_ids),
        "careem": audit(careem, "careem", gold_ids),
    }

    careem_updated, changes = apply_noon_mirror_to_careem(careem, noon, gold_ids)
    save_json(PARTNERS / "careem.json", careem_updated)

    after = {
        "noon": audit(noon, "noon", gold_ids),
        "careem": audit(careem_updated, "careem", gold_ids),
    }

    report = {
        "at": datetime.now(timezone.utc).isoformat(),
        "before": before,
        "after": after,
        "careem_changes": changes,
        "verdict": "PASS" if after["careem"]["journeys_linked"] >= before["noon"]["journeys_linked"] - 1 else "REVIEW",
    }
    save_json(REPORT, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())