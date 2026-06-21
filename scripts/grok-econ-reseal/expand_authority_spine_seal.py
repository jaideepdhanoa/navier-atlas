#!/usr/bin/env python3
"""Expand RAKTA/Bahrain phase-1 featured routes from sealable spine rows + re-seal."""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff" / "partner-map-model"
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"

SEALABLE = frozenset({
    "proposal_active_rak_domestic",
    "proposal_active_rak_dubai_inter_emirate",
    "proposal_active_rak_musandam_pioneer",
    "proposal_active_bahrain_domestic",
    "proposal_active_ksa_eastern_province_cross_border",
})
SKIP_CLASS = frozenset({
    "held_exact_bind_required_city_label_contamination",
    "held_exact_bind_required_musandam_khasab",
    "roadmap_quanta_lr_hold_until_ops_review",
    "roadmap_quanta_lr_not_commercial_now",
})

EXPAND = {
    "rakta": {
        "ledger": HANDOFF / "rakta-route-seal-ledger-2026-06-21.json",
        "phases": [
            {"n": 1, "max_add": 999, "classifications": {"proposal_active_rak_domestic"}},
            {"n": 2, "max_add": 999, "classifications": {"proposal_active_rak_dubai_inter_emirate"}},
        ],
    },
    "bahrain-motc": {
        "ledger": HANDOFF / "bahrain-motc-route-seal-ledger-2026-06-21.json",
        "phases": [
            {"n": 1, "max_add": 999, "classifications": {"proposal_active_bahrain_domestic"}},
            {"n": 2, "max_add": 999, "classifications": {"proposal_active_ksa_eastern_province_cross_border"}},
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def load_pr58():
    spec = importlib.util.spec_from_file_location(
        "execute_pr58_india_gcc",
        ROOT / "scripts/grok-econ-reseal/execute_pr58_india_gcc.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def card_from_spine(row: dict) -> dict:
    label = f"{row.get('from_label', '')} → {row.get('to_label', '')}"
    return {
        "label": label,
        "from_node_id": row.get("from_node_id"),
        "to_node_id": row.get("to_node_id"),
        "from_label": row.get("from_label"),
        "to_label": row.get("to_label"),
        "distance_nm": row.get("distance_nm_spine"),
        "platform": "N30 Pioneer II",
        "route_id": None,
        "route_ids": None,
        "_spine_corridor_id": row.get("spine_corridor_id"),
        "_link_status": "held-null-not-in-spine",
        "_hold_reason": "pending Grok spine expand seal",
        "render": "commercial-now candidate after Grok seal",
        "economics_status": "economics_pending",
    }


def expand_phase(phase: dict, ledger_rows: list, cfg_phase: dict, existing: set[str]) -> list[str]:
    candidates = []
    for row in ledger_rows:
        sid = row.get("spine_corridor_id")
        cls = row.get("classification", "")
        if sid in existing or cls in SKIP_CLASS or cls not in cfg_phase["classifications"]:
            continue
        if row.get("geometry_status_spine") != "geometry_present":
            continue
        candidates.append(row)
    candidates.sort(key=lambda r: r.get("distance_nm_spine") or 999)
    added = []
    for row in candidates[: cfg_phase["max_add"]]:
        phase.setdefault("featured_routes", []).append(card_from_spine(row))
        existing.add(row["spine_corridor_id"])
        added.append(row["spine_corridor_id"])
    return added


def expand_partner(slug: str, cfg: dict) -> dict:
    doc = load_json(PARTNERS / f"{slug}.json")
    ledger_rows = load_json(cfg["ledger"]).get("routes") or []
    existing = {
        fr.get("_spine_corridor_id")
        for ph in doc.get("phases") or []
        for fr in ph.get("featured_routes") or []
        if fr.get("_spine_corridor_id")
    }
    all_added: list[str] = []
    for cfg_phase in cfg["phases"]:
        phase = next((p for p in doc.get("phases") or [] if p.get("n") == cfg_phase["n"]), None)
        if not phase:
            continue
        all_added.extend(expand_phase(phase, ledger_rows, cfg_phase, existing))
    doc.setdefault("_authority_spine_expand", {})["applied_at"] = utc_now()
    doc["_authority_spine_expand"]["added"] = all_added
    save_json(PARTNERS / f"{slug}.json", doc)
    return {"partner": slug, "added": len(all_added), "spine_ids": all_added[:20], "spine_ids_total": len(all_added)}


def reseal_partner(slug: str, pr58: Any) -> dict:
    ledger_name = {
        "rakta": "rakta-route-seal-ledger-2026-06-21.json",
        "bahrain-motc": "bahrain-motc-route-seal-ledger-2026-06-21.json",
    }[slug]
    ledger_path = HANDOFF / ledger_name
    gold_ids, by_id, by_bp = pr58.build_route_index()
    doc = load_json(PARTNERS / f"{slug}.json")
    idx = {r["spine_corridor_id"]: r for r in load_json(ledger_path).get("routes", []) if r.get("spine_corridor_id")}
    sealed = held = 0
    for ph in doc.get("phases") or []:
        for card in ph.get("featured_routes") or []:
            sid = card.get("_spine_corridor_id")
            if not sid:
                continue
            meta = idx.get(sid, {})
            cls = meta.get("classification", "")
            if cls in SKIP_CLASS:
                card["_link_status"] = "roadmap-no-geometry" if "roadmap" in cls else "held-null-with-reason"
                card["_hold_reason"] = meta.get("guardrail") or cls
                held += 1
                continue
            if cls not in SEALABLE:
                held += 1
                continue
            rec = pr58.seal_route_entry(
                {
                    "label": card.get("label"),
                    "from_node_id": card.get("from_node_id") or meta.get("from_node_id"),
                    "to_node_id": card.get("to_node_id") or meta.get("to_node_id"),
                    "distance_nm": card.get("distance_nm") or meta.get("distance_nm_spine"),
                    "source_corridor_id": sid,
                },
                gold_ids, by_id, by_bp, partner=slug, phase=ph.get("n"),
            )
            if rec.get("verdict") == "SEALED_ROUTE_ID" and rec.get("route_id"):
                card["route_id"] = rec["route_id"]
                card["route_ids"] = [rec["route_id"]]
                card["_link_kind"] = "spine-corridor-seal"
                card["_link_status"] = "linked-grok-scoped"
                card["_link_source"] = "grok/expand_authority_spine_seal"
                card.pop("_hold_reason", None)
                card["vessel_gate"] = rec.get("vessel_gate")
                card["economics_status"] = "economics_pending"
                sealed += 1
            else:
                card["_link_status"] = "held-null-with-reason"
                card["_hold_reason"] = rec.get("reason", "seal failed")
                held += 1
    save_json(PARTNERS / f"{slug}.json", doc)
    save_json(DC / f"{slug}.json", doc)
    return {"partner": slug, "sealed": sealed, "held": held}


def main() -> int:
    pr58 = load_pr58()
    results = {"at": utc_now(), "expand": [], "reseal": []}
    for slug, cfg in EXPAND.items():
        results["expand"].append(expand_partner(slug, cfg))
        results["reseal"].append(reseal_partner(slug, pr58))
    save_json(HANDOFF / "authority-spine-expand-report.json", results)
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())