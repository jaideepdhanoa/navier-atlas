#!/usr/bin/env python3
"""Fix RAKTA phase-2 inter-emirate cards, Musandam phase-3 seals, Quanta-LR display promote."""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC_PARTNERS = ROOT / "data-clean" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"
REPORT = HANDOFF / "rak-partner-corridor-fix-report.json"

PIONEER_MUSANDAM = (
    ("rn-e2e12eaca539", "bp-221faa3616", "bp-8f6140f2d4", "Khasab", "Khasab Cruise Terminal", 0.6),
    ("rn-4ed5c172422a", "bp-8f6140f2d4", "bp-b127c11245", "Khasab Cruise Terminal", "Gumda Fishing Harbour", 14.8),
    ("rn-73f3c87ca5bf", "bp-221faa3616", "bp-b127c11245", "Khasab", "Gumda Fishing Harbour", 14.9),
)

ROADMAP_QLR = (
    ("edge-0772", "ras-al-khaimah-uae", "muscat-oman", "Ras Al Khaimah", "Muscat", 263.5),
    ("edge-0773", "ras-al-khaimah-uae", "doha-qatar", "Ras Al Khaimah", "Doha", 240.7),
    ("edge-0774", "ras-al-khaimah-uae", "manama-bahrain", "Ras Al Khaimah", "Manama", 289.7),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_gold() -> set[str]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    return {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}


def card_template(
    label: str,
    route_id: str,
    *,
    from_node: str,
    to_node: str,
    from_label: str,
    to_label: str,
    distance_nm: float,
    platform: str = "N30 Pioneer II",
    render: str = "commercial-now candidate after Grok seal",
    economics_status: str = "economics_pending",
    spine_id: str | None = None,
) -> dict:
    return {
        "label": label,
        "from_node_id": from_node,
        "to_node_id": to_node,
        "from_label": from_label,
        "to_label": to_label,
        "distance_nm": distance_nm,
        "platform": platform,
        "route_id": route_id,
        "route_ids": [route_id],
        "_spine_corridor_id": spine_id or route_id,
        "_link_kind": "spine-corridor-seal",
        "_link_status": "linked-grok-scoped",
        "_link_source": "grok/fix_rak_partner_corridors",
        "render": render,
        "vessel_gate": "N30 Pioneer II commercial-now" if platform != "Quanta-LR" else "Quanta-LR review >150nm",
        "economics_status": economics_status,
    }


def inter_emirate_phase2_cards(gold: set[str], mint_report: dict | None) -> list[dict]:
    minted = {m["from_city_id"] + "|" + m["to_city_id"]: m for m in (mint_report or {}).get("minted", [])}
    specs = [
        ("rn-b9da9d38e29f", "bp-56d5f5bd8d", "bp-29c2c81221", "Dubai Harbour Marina", "Wynn Al Marjan Island arrival lagoon", 49.8),
        ("rn-14d3708d3bf1", "dubai-uae", "ras-al-khaimah-uae", "Dubai", "Ras Al Khaimah", 52.8),
        ("rn-8bc1e153cdc4", "ras-al-khaimah-uae", "bp-051c982570", "Ras Al Khaimah", "Dubai Islands Marina", 50.0),
    ]
    for key in ("ras-al-khaimah-uae|abu-dhabi-uae", "ras-al-khaimah-uae|sharjah-uae", "ras-al-khaimah-uae|fujairah-uae"):
        if key in minted:
            m = minted[key]
            specs.append((m["route_id"], m["from_city_id"], m["to_city_id"], m["from_label"], m["to_label"], m["distance_nm"]))

    out = []
    for rid, fn, tn, fl, tl, dist in specs:
        if rid not in gold:
            continue
        out.append(card_template(f"{fl} → {tl}", rid, from_node=fn, to_node=tn, from_label=fl, to_label=tl, distance_nm=dist))
    return out


def musandam_phase3_cards(gold: set[str]) -> list[dict]:
    cards = []
    for rid, fn, tn, fl, tl, dist in PIONEER_MUSANDAM:
        if rid not in gold:
            continue
        cards.append(
            card_template(
                f"{fl} → {tl}",
                rid,
                from_node=fn,
                to_node=tn,
                from_label=fl,
                to_label=tl,
                distance_nm=dist,
                platform="N30 Pioneer II",
                render="commercial-now Musandam Pioneer II",
            )
        )
    for rid, fn, tn, fl, tl, dist in ROADMAP_QLR:
        if rid not in gold:
            continue
        cards.append(
            card_template(
                f"{fl} → {tl}",
                rid,
                from_node=fn,
                to_node=tn,
                from_label=fl,
                to_label=tl,
                distance_nm=dist,
                platform="Quanta-LR",
                render="roadmap-amber-dashed",
                economics_status="roadmap_excluded",
            )
        )
    return cards


def apply_rakta_fixes(doc: dict, gold: set[str]) -> dict:
    mint_report = None
    mr = HANDOFF / "rak-other-uae-mint-report.json"
    if mr.exists():
        mint_report = json.loads(mr.read_text())

    changes: list[str] = []
    for phase in doc.get("phases") or []:
        n = phase.get("n")
        if n == 2:
            new_cards = inter_emirate_phase2_cards(gold, mint_report)
            if new_cards:
                phase["featured_routes"] = new_cards
                phase["cities"] = ["ras-al-khaimah-uae", "dubai-uae", "sharjah-uae", "fujairah-uae", "abu-dhabi-uae"]
                phase["rationale"] = "True inter-emirate corridors only — Dubai intra-city contamination removed; RAK↔Dubai and RAK↔other-UAE spines sealed."
                changes.append(f"phase2:{len(new_cards)} inter-emirate cards")
        elif n == 3:
            pioneer = [c for c in musandam_phase3_cards(gold) if c.get("platform") != "Quanta-LR"]
            roadmap = [c for c in musandam_phase3_cards(gold) if c.get("platform") == "Quanta-LR"]
            phase["featured_routes"] = pioneer + roadmap
            phase["cities"] = [
                "ras-al-khaimah-uae",
                "khasab-oman",
                "muscat-oman",
                "doha-qatar",
                "manama-bahrain",
            ]
            phase["rationale"] = "Musandam Pioneer II local routes sealed under khasab-oman; Quanta-LR Gulf legs amber-dashed, excluded from economics."
            changes.append(f"phase3:{len(pioneer)} pioneer + {len(roadmap)} roadmap")

    doc["end_state"] = {
        "headline": "Northern Gulf water network — RAK domestic, inter-emirate, Musandam, and Quanta-LR roadmap",
        "end_state_cities": [
            "ras-al-khaimah-uae",
            "dubai-uae",
            "sharjah-uae",
            "fujairah-uae",
            "abu-dhabi-uae",
            "khasab-oman",
            "muscat-oman",
            "doha-qatar",
            "manama-bahrain",
        ],
        "narrative": "Commercial-now N30 layers in RAK, Dubai, and northern emirates; Musandam/Khasab under Oman registry; long Gulf legs as visible amber roadmap only.",
    }
    doc["map_display"] = {
        "promote_roadmap": True,
        "roadmap_route_ids": [r[0] for r in ROADMAP_QLR],
        "roadmap_economics_excluded": True,
    }
    doc.setdefault("_grok_corridor_fix", {})["applied_at"] = utc_now()
    doc["_grok_corridor_fix"]["changes"] = changes
    return {"changes": changes}


def main() -> int:
    gold = load_gold()
    doc = json.loads((PARTNERS / "rakta.json").read_text())
    result = apply_rakta_fixes(doc, gold)
    for path in (PARTNERS / "rakta.json", DC_PARTNERS / "rakta.json"):
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    save = {"at": utc_now(), "partner": "rakta", **result}
    REPORT.write_text(json.dumps(save, indent=2) + "\n")
    print(json.dumps(save, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())