#!/usr/bin/env python3
"""Mint khasab-oman city, fix Musandam BP registry, reclassify RAKTA spine rows."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import load_json, save_json  # noqa: E402

DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "rak-musandam-khasab-mint-report.json"

KHASAB_CITY = "khasab-oman"
KHASAB_BPS = ("bp-221faa3616", "bp-8f6140f2d4", "bp-b127c11245")
PIONEER_ROUTES = ("rn-e2e12eaca539", "rn-4ed5c172422a", "rn-73f3c87ca5bf")
ROADMAP_MUSANDAM = "edge__muscat-oman__ras-al-khaimah-uae-cross-border-via-khasab-top-up"

LEDGERS = (
    HANDOFF / "rakta-route-seal-ledger-2026-06-21.json",
    HANDOFF / "rakta-held-null-route-ledger-2026-06-21.json",
    HANDOFF / "rakta-grok-seal-ledger.json",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def city_feature() -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [56.247, 26.206]},
        "properties": {
            "id": KHASAB_CITY,
            "type": "city",
            "name": "Khasab / Musandam",
            "shortName": "Khasab",
            "fullName": "Khasab (Musandam, Oman)",
            "region": "Middle East",
            "country": "Oman",
            "platform_class": "dual-platform",
            "priority": 2,
            "tier_sort_key": 2,
            "coords_resolved": True,
            "coords_source": "grok_rak_musandam_khasab_mint_2026-06-21",
        },
    }


def ensure_city(fbt: dict) -> bool:
    cities = fbt.setdefault("city", [])
    if any(f.get("properties", {}).get("id") == KHASAB_CITY for f in cities):
        return False
    cities.append(city_feature())
    return True


def fix_bp_parents(fbt: dict) -> list[str]:
    changed = []
    for f in fbt.get("poi") or []:
        p = f.get("properties") or {}
        if p.get("id") in KHASAB_BPS and p.get("parent_city_id") != KHASAB_CITY:
            p["parent_city_id"] = KHASAB_CITY
            p["_khasab_registry_fix"] = "grok_rak_musandam_khasab_mint_2026-06-21"
            changed.append(p["id"])
    return changed


def fix_route_city_ids(routes: list) -> list[str]:
    changed = []
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id")
        if rid not in PIONEER_ROUTES:
            continue
        if p.get("from_city_id") != KHASAB_CITY or p.get("to_city_id") != KHASAB_CITY:
            p["from_city_id"] = KHASAB_CITY
            p["to_city_id"] = KHASAB_CITY
            p["trip_scope"] = "intra_city"
            p["_khasab_registry_fix"] = "grok_rak_musandam_khasab_mint_2026-06-21"
            changed.append(rid)
    return changed


def update_cluster() -> None:
    clusters = load_json(DC / "CLUSTERS.json")
    for cl in clusters.get("clusters") or []:
        if cl.get("cluster_id") != "oman":
            continue
        members = list(cl.get("member_city_ids") or [])
        if KHASAB_CITY not in members:
            members.append(KHASAB_CITY)
            cl["member_city_ids"] = members
            cl["members_present"] = len(members)
        break
    save_json(DC / "CLUSTERS.json", clusters)


def update_spine() -> None:
    spine = load_json(HANDOFF / "uae-gulf-shared-corridor-spine.json")
    for row in spine.get("corridors") or []:
        cid = row.get("corridor_id")
        if cid in PIONEER_ROUTES:
            row["from_city_id"] = KHASAB_CITY
            row["to_city_id"] = KHASAB_CITY
            row["country_or_cross_border_pair"] = f"{KHASAB_CITY} ↔ {KHASAB_CITY}"
            row["authority_or_platform_relevance"] = "N30 Pioneer II commercial-now"
        elif cid == ROADMAP_MUSANDAM:
            row["authority_or_platform_relevance"] = "Quanta-LR roadmap / amber-dashed"
    summary = spine.setdefault("summary_by_market", {}).setdefault("rak_musandam_candidate", {})
    summary["khasab_oman_registry"] = KHASAB_CITY
    summary["geometry_present"] = summary.get("geometry_present", 0)
    save_json(HANDOFF / "uae-gulf-shared-corridor-spine.json", spine)


def reclassify_ledger_row(row: dict) -> None:
    sid = row.get("spine_corridor_id")
    if sid in PIONEER_ROUTES:
        row["classification"] = "proposal_active_rak_musandam_pioneer"
        row["market_key"] = "rak_musandam"
        row["from_city_id"] = KHASAB_CITY
        row["to_city_id"] = KHASAB_CITY
        row["authority_relevance_spine"] = "N30 Pioneer II commercial-now"
        row["guardrail"] = "Khasab/Oman registry minted — seal for commercial-now display."
    elif sid == ROADMAP_MUSANDAM:
        row["classification"] = "roadmap_quanta_lr_hold_until_ops_review"
        row["guardrail"] = "Roadmap only; display amber-dashed, exclude from economics."


def update_ledgers() -> int:
    n = 0
    for path in LEDGERS:
        if not path.exists():
            continue
        doc = load_json(path)
        for row in doc.get("routes") or []:
            if row.get("spine_corridor_id") in (*PIONEER_ROUTES, ROADMAP_MUSANDAM):
                reclassify_ledger_row(row)
                n += 1
        if "summary" in doc and "by_classification" in doc["summary"]:
            bc = doc["summary"]["by_classification"]
            held = bc.pop("held_exact_bind_required_musandam_khasab", 0)
            if held:
                bc["proposal_active_rak_musandam_pioneer"] = bc.get("proposal_active_rak_musandam_pioneer", 0) + 3
                if ROADMAP_MUSANDAM:
                    bc.setdefault("roadmap_quanta_lr_hold_until_ops_review", 0)
        save_json(path, doc)
    return n


def update_crosswalk() -> None:
    path = ROOT / "partner-pitch" / "RAKTA-ANCHOR-CITY-CROSSWALK.json"
    doc = load_json(path)
    for row in doc.get("rows") or []:
        if row.get("anchor_city_id") == KHASAB_CITY:
            row["verdict"] = "OK"
            row["note"] = "Grok minted khasab-oman in data-clean; Musandam Pioneer II routes sealed."
    save_json(path, doc)


def update_scope() -> None:
    path = HANDOFF / "rakta-scope-2026-06-21.json"
    doc = load_json(path)
    for m in doc.get("markets") or []:
        if m.get("id") == "rak-musandam":
            m["status"] = "geometry_present_khasab_minted"
        if m.get("id") == "rak-other-uae":
            m["status"] = "grok_inter_emirate_mint_pending"
    save_json(path, doc)


def main() -> int:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    city_added = ensure_city(fbt)
    bps_fixed = fix_bp_parents(fbt)
    if city_added or bps_fixed:
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)

    routes = load_json(DC / "ROUTES.json")
    routes_fixed = fix_route_city_ids(routes)
    if routes_fixed:
        save_json(DC / "ROUTES.json", routes)

    update_cluster()
    update_spine()
    ledger_rows = update_ledgers()
    update_crosswalk()
    update_scope()

    report = {
        "at": utc_now(),
        "lane": "grok/mint_rak_musandam_khasab_geometry",
        "city_added": city_added,
        "bps_fixed": bps_fixed,
        "routes_fixed": routes_fixed,
        "ledger_rows": ledger_rows,
        "khasab_city_id": KHASAB_CITY,
        "pioneer_route_ids": list(PIONEER_ROUTES),
        "roadmap_excluded": ROADMAP_MUSANDAM,
    }
    save_json(REPORT, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())