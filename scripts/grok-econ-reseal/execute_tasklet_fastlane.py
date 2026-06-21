#!/usr/bin/env python3
"""Grok fastlane — seal Tasklet authority + India consumer handoffs (PR #62/#63).

Seals RAKTA / Bahrain MOTC spine corridors into live route_ids where gold matches.
Marks Kolkata / Chennai consumer markets held-null until Atlas city IDs exist.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff" / "partner-map-model"
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"

BRIEF_MARKET_IDS = frozenset(
    {"kolkata_hooghly_waterfront", "chennai_ecr_cuddalore_puducherry_coast"}
)

SEALABLE = frozenset(
    {
        "proposal_active_rak_domestic",
        "proposal_active_rak_dubai_inter_emirate",
        "proposal_active_bahrain_domestic",
        "proposal_active_ksa_eastern_province_cross_border",
    }
)

ROADMAP_CLASS = frozenset(
    {
        "roadmap_quanta_lr_hold_until_ops_review",
        "roadmap_quanta_lr_not_commercial_now",
    }
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def load_pr58():
    spec = importlib.util.spec_from_file_location(
        "execute_pr58_india_gcc",
        ROOT / "scripts/grok-econ-reseal/execute_pr58_india_gcc.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def iter_bindable_cards(doc: dict):
    for j in doc.get("journeys_unlocked") or []:
        if isinstance(j, dict):
            yield j
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, dict):
                yield fr
    for m in doc.get("markets") or []:
        for j in m.get("journeys_unlocked") or []:
            if isinstance(j, dict):
                yield j
        for ph in m.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, dict):
                    yield fr


def ledger_index(ledger_path: Path) -> dict[str, dict]:
    ledger = load_json(ledger_path)
    return {r["spine_corridor_id"]: r for r in ledger.get("routes", []) if r.get("spine_corridor_id")}


def seal_authority_partner(
    slug: str,
    *,
    ledger_path: Path,
    pr58: Any,
    gold_ids: set[str],
    by_id: dict,
    by_bp: dict,
) -> dict[str, Any]:
    path = PARTNERS / f"{slug}.json"
    doc = load_json(path)
    idx = ledger_index(ledger_path)
    sealed_rows: list[dict] = []
    held_rows: list[dict] = []

    for card in iter_bindable_cards(doc):
        sid = card.get("_spine_corridor_id")
        if not sid:
            continue
        meta = idx.get(sid, {})
        classification = meta.get("classification", "")
        entry = {
            "label": card.get("label") or f"{card.get('from', '')} → {card.get('to', '')}",
            "from_node_id": card.get("from_node_id"),
            "to_node_id": card.get("to_node_id"),
            "distance_nm": card.get("distance_nm"),
            "source_corridor_id": sid,
        }

        if classification in ROADMAP_CLASS:
            card["_link_status"] = "roadmap-no-geometry"
            card["_hold_reason"] = meta.get("route_id_hold_reason") or "Quanta-LR roadmap — not commercial-now"
            card["render"] = "roadmap-amber-dashed"
            held_rows.append({**meta, "grok_verdict": "ROADMAP_HELD"})
            continue

        if classification not in SEALABLE:
            card["_link_status"] = "held-null-with-reason"
            card["_hold_reason"] = meta.get("route_id_hold_reason") or classification
            held_rows.append({**meta, "grok_verdict": "HELD_NULL_WITH_REASON"})
            continue

        rec = pr58.seal_route_entry(
            entry, gold_ids, by_id, by_bp, partner=slug, phase=None
        )
        sealed_rows.append(rec)
        if rec.get("verdict") == "SEALED_ROUTE_ID" and rec.get("route_id"):
            card["route_id"] = rec["route_id"]
            card["route_ids"] = [rec["route_id"]]
            card["_link_kind"] = "spine-corridor-seal"
            card["_link_status"] = "linked-grok-scoped"
            card["_link_source"] = "grok/execute_tasklet_fastlane"
            card["_hold_reason"] = None
            card["economics_status"] = "economics_pending"
            if rec.get("vessel_gate"):
                card["vessel_gate"] = rec["vessel_gate"]
        else:
            card["_link_status"] = "held-null-with-reason"
            card["_hold_reason"] = rec.get("reason", "exact seal failed")
            held_rows.append({**meta, "grok_verdict": "HELD_NULL_WITH_REASON", "grok_reason": rec.get("reason")})

    doc.setdefault("_tasklet_fastlane", {})
    doc["_tasklet_fastlane"].update({
        "lane": "grok/execute_tasklet_fastlane",
        "applied_at": utc_now(),
        "sealed": sum(1 for r in sealed_rows if r.get("verdict") == "SEALED_ROUTE_ID"),
        "held": len(held_rows) + sum(
            1 for r in sealed_rows if r.get("verdict") != "SEALED_ROUTE_ID"
        ),
    })
    doc["proposal_status"] = "grok_seal_pass_tasklet_fastlane"
    save_json(path, doc)
    save_json(DC / f"{slug}.json", doc)

    out_ledger = {
        "partner": slug,
        "lane": "grok/execute_tasklet_fastlane",
        "checked_at": utc_now(),
        "source_tasklet_ledger": str(ledger_path.relative_to(ROOT)),
        "summary": {
            "sealed": sum(1 for r in sealed_rows if r.get("verdict") == "SEALED_ROUTE_ID"),
            "held_null": len(held_rows)
            + sum(1 for r in sealed_rows if r.get("verdict") != "SEALED_ROUTE_ID"),
        },
        "sealed_routes": sealed_rows,
        "held_routes": held_rows,
    }
    save_json(HANDOFF / f"{slug}-grok-seal-ledger.json", out_ledger)
    return out_ledger["summary"]


def seal_india_consumer_partner(slug: str) -> dict[str, Any]:
    path = PARTNERS / f"{slug}.json"
    doc = load_json(path)
    held_rows: list[dict] = []
    brief_markets: list[dict] = []

    for m in doc.get("markets") or []:
        mid = m.get("id")
        if mid not in BRIEF_MARKET_IDS:
            continue
        m["scope_status"] = "brief_only_grok_mint_required"
        m["anchor_cities"] = []
        m["map_promote"] = False
        brief_markets.append({"id": mid, "label": m.get("label")})
        for card in iter_bindable_cards({"markets": [m]}):
            card.pop("route_id", None)
            card.pop("route_ids", None)
            card.pop("from_node_id", None)
            card.pop("to_node_id", None)
            card.pop("distance_nm", None)
            card["_link_status"] = "held-null-not-in-spine"
            card["_hold_reason"] = (
                "No Atlas city IDs or spine geometry for Kolkata/Chennai — "
                "brief-only until Grok mints registry nodes"
            )
            card["_bind_status"] = "brief_only_grok_mint_required"
            card["_market_candidate"] = mid
            held_rows.append({
                "partner": slug,
                "market_id": mid,
                "label": card.get("label") or f"{card.get('from', '')} → {card.get('to', '')}",
                "verdict": "HELD_NULL_WITH_REASON",
                "reason": card["_hold_reason"],
            })

    doc["brief_only_markets"] = brief_markets
    doc.setdefault("_tasklet_fastlane", {})
    doc["_tasklet_fastlane"].update({
        "lane": "grok/execute_tasklet_fastlane",
        "applied_at": utc_now(),
        "brief_markets": list(BRIEF_MARKET_IDS),
        "held_brief_cards": len(held_rows),
    })
    if slug in ("ola", "rapido"):
        doc["proposal_status"] = "grok_seal_pass_tasklet_fastlane"
    save_json(path, doc)
    save_json(DC / f"{slug}.json", doc)

    ledger = {
        "partner": slug,
        "lane": "grok/execute_tasklet_fastlane",
        "checked_at": utc_now(),
        "markets": list(BRIEF_MARKET_IDS),
        "summary": {"held_null": len(held_rows), "sealed": 0},
        "held_routes": held_rows,
    }
    save_json(HANDOFF / f"india-consumer-{slug}-brief-seal-ledger.json", ledger)
    return ledger["summary"]


def seal_uber_india_brief() -> dict[str, Any]:
    """Uber global JSON — seal India brief markets only (display markets unchanged)."""
    path = PARTNERS / "uber.json"
    doc = load_json(path)
    india_markets = [
        m for m in doc.get("markets") or []
        if m.get("id") in BRIEF_MARKET_IDS
        or m.get("region") == "South Asia"
        and m.get("id") in BRIEF_MARKET_IDS
    ]
    held = 0
    for m in doc.get("markets") or []:
        if m.get("id") not in BRIEF_MARKET_IDS:
            continue
        m["scope_status"] = "brief_only_grok_mint_required"
        m["anchor_cities"] = []
        m["map_promote"] = False
        for card in iter_bindable_cards({"markets": [m]}):
            card.pop("route_id", None)
            card.pop("route_ids", None)
            card.pop("distance_nm", None)
            card["_link_status"] = "held-null-not-in-spine"
            card["_hold_reason"] = "brief_only_grok_mint_required — no Kolkata/Chennai Atlas IDs"
            card["_bind_status"] = "brief_only_grok_mint_required"
            held += 1
    doc.setdefault("_tasklet_fastlane", {})
    doc["_tasklet_fastlane"]["india_brief_held"] = held
    save_json(path, doc)
    save_json(DC / f"uber.json", doc)
    return {"held_null": held, "sealed": 0}


def main() -> int:
    pr58 = load_pr58()
    gold_ids, by_id, by_bp = pr58.build_route_index()
    stats: dict[str, Any] = {"at": utc_now(), "partners": {}}

    for slug, ledger in (
        ("rakta", HANDOFF / "rakta-route-seal-ledger-2026-06-21.json"),
        ("bahrain-motc", HANDOFF / "bahrain-motc-route-seal-ledger-2026-06-21.json"),
    ):
        stats["partners"][slug] = seal_authority_partner(
            slug, ledger_path=ledger, pr58=pr58, gold_ids=gold_ids, by_id=by_id, by_bp=by_bp
        )

    for slug in ("ola", "rapido"):
        stats["partners"][slug] = seal_india_consumer_partner(slug)
    stats["partners"]["uber"] = seal_uber_india_brief()

    save_json(HANDOFF / "tasklet-fastlane-execution-report.json", stats)
    print(json.dumps(stats, indent=2))

    partners = "ola rapido uber rakta bahrain-motc"
    print(f"\n→ partner page lane ({partners})")
    import os

    env = {**os.environ, "PARTNERS": partners}
    rc = subprocess.run(
        [str(ROOT / "scripts/grok-econ-reseal/run_partner_page_lane.sh")],
        cwd=ROOT,
        env=env,
    )
    return rc.returncode


if __name__ == "__main__":
    sys.exit(main())