#!/usr/bin/env python3
"""Promote Kolkata/Chennai markets from brief-only to sealed display on India partners."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"
MANIFEST = HANDOFF / "regional-inheritance-manifest.json"
MINT_REPORT = HANDOFF / "india-kolkata-chennai-mint-report.json"

MARKET_CITY = {
    "kolkata_hooghly_waterfront": "kolkata-india",
    "chennai_ecr_cuddalore_puducherry_coast": "chennai-india",
}

INDIA_PARTNERS = (
    "rapido",
    "ola",
    "uber-india",
    "adani-ports",
    "reliance-industries",
    "uber",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def norm_label(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[/|]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def journey_key(from_s: str | None, to_s: str | None) -> str:
    return f"{norm_label(from_s)}|{norm_label(to_s)}"


def build_bind_index(minted: list[dict]) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for m in minted:
        keys = [
            journey_key(m.get("journey_from"), m.get("journey_to")),
            journey_key(m.get("from_label"), m.get("to_label")),
        ]
        for k in keys:
            if k and k != "|":
                idx[k] = m
    return idx


def bind_card(card: dict, bind_idx: dict[str, dict], market_id: str) -> bool:
    candidates = [
        journey_key(card.get("from"), card.get("to")),
        journey_key(card.get("from"), card.get("to", "").split(" via")[0]),
    ]
    hit = None
    for k in candidates:
        if k in bind_idx:
            hit = bind_idx[k]
            break
    if not hit:
        # Fuzzy: match leading token of from/to
        cf, ct = norm_label(card.get("from")), norm_label(card.get("to"))
        for k, m in bind_idx.items():
            jf, jt = k.split("|", 1)
            if (cf.startswith(jf) or jf.startswith(cf)) and (ct.startswith(jt) or jt.startswith(ct) or jt in ct):
                hit = m
                break
    if not hit:
        return False
    card["route_id"] = hit["route_id"]
    card["route_ids"] = [hit["route_id"]]
    card["from_node_id"] = hit["from_bp"]
    card["to_node_id"] = hit["to_bp"]
    card["distance_nm"] = hit["distance_nm"]
    card["_bind_status"] = "sealed_grok_mint"
    card["_link_kind"] = "spine-corridor-seal"
    card["_link_status"] = "linked-grok-scoped"
    card["_link_source"] = "grok/seal_india_kolkata_chennai"
    card.pop("_hold_reason", None)
    card.pop("_route_id_rule", None)
    card["economics_status"] = "economics_pending"
    card["_market_candidate"] = market_id
    return True


def iter_cards(doc: dict, market_id: str | None = None):
    if market_id:
        markets = [m for m in doc.get("markets") or [] if m.get("id") == market_id]
    else:
        markets = doc.get("markets") or []
    for m in markets:
        mid = m.get("id")
        for j in m.get("journeys_unlocked") or []:
            yield mid, j
        for ph in m.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                yield mid, fr


def promote_market(m: dict, city_id: str) -> None:
    m["anchor_cities"] = [city_id]
    m["map_promote"] = True
    m["scope_status"] = "sealed_display_ready"
    m["proposal_status"] = "included_sealed_geometry"
    if not m.get("phases"):
        m["phases"] = [{
            "n": 1,
            "label": f"Phase 1 — {m.get('label', city_id)} beachhead",
            "boats": 4,
            "cities": [city_id],
            "route_scope": "intra",
            "featured_routes": [],
        }]


def clean_uber_india_copy(doc: dict) -> None:
    if doc.get("partner_id") != "uber-india":
        return
    doc["coverage_note"] = (
        "Six India consumer markets on sealed Atlas geometry: Mumbai, Goa, Kerala, Andaman, "
        "Kolkata/Hooghly and Chennai/ECR."
    )
    hero = doc.setdefault("hero", {})
    hero["subtitle"] = (
        "Six high-value India markets — all six on the map with sealed corridors "
        "and economics pending on new eastern/southeastern routes."
    )
    hero["what_we_do_together"] = (
        "An Uber-branded foiling water tier across Mumbai, Goa, Kerala backwaters, the Andaman islands, "
        "Kolkata's Hooghly waterfront and Chennai's ECR coast — booked in-app on sealed Atlas corridors."
    )
    nt = doc.setdefault("network_thesis", {})
    nt["headline"] = "One app. India's coastal and river markets. Uber's water layer."
    nt["coverage_note"] = (
        "Full India consumer scope: Mumbai, Goa, Kerala, Andaman, Kolkata/Hooghly and Chennai/ECR. "
        "Economics cascade pending on newly minted eastern/southeastern corridors."
    )
    nt["body"] = (
        "India is a coastline of harbours, tidal rivers, backwaters and island archipelagos — "
        "and no mobility platform owns the water. The same in-app foiling tier extends to Mumbai's harbour, "
        "Goa's coast, Kerala's backwaters, the Andaman islands, Kolkata's Hooghly and Chennai's ECR coast."
    )
    doc.pop("draft_status", None)
    wnn = doc.setdefault("why_navier_now", {})
    wnn.setdefault("wow_corridors", [])
    extras = [
        "Howrah ↔ Fairlie Hooghly commuter",
        "Chennai Port WQIV ↔ Cuddalore ECR coast",
    ]
    for e in extras:
        if e not in wnn["wow_corridors"]:
            wnn["wow_corridors"].append(e)
    ctx = doc.setdefault("partner_context", {})
    ctx["where_navier_fits"] = (
        "A foiling water tier in the Uber app across all six India consumer markets — "
        "same partner-supply model as global Uber, on sealed Atlas geometry."
    )


def update_manifest() -> None:
    manifest = load_json(MANIFEST)
    for pack_name in ("india_mobility", "india_corporate"):
        pack = manifest["packs"][pack_name]
        display = list(pack.get("display_market_ids") or [])
        brief = list(pack.get("brief_only_market_ids") or [])
        scope = list(pack.get("map_scope_city_ids") or [])
        for mid in ("kolkata_hooghly_waterfront", "chennai_ecr_cuddalore_puducherry_coast"):
            if mid in brief:
                brief.remove(mid)
            if mid not in display:
                display.append(mid)
        for cid in ("kolkata-india", "chennai-india"):
            if cid not in scope:
                scope.append(cid)
        pack["display_market_ids"] = display
        pack["brief_only_market_ids"] = brief
        pack["map_scope_city_ids"] = scope
    save_json(MANIFEST, manifest)


def seal_partner(slug: str, bind_idx: dict[str, dict]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = load_json(path)
    sealed = 0
    held = 0
    for mid, city_id in MARKET_CITY.items():
        markets = [m for m in doc.get("markets") or [] if m.get("id") == mid]
        if not markets:
            continue
        for m in markets:
            promote_market(m, city_id)
            for _, card in iter_cards(doc, mid):
                if bind_card(card, bind_idx, mid):
                    sealed += 1
                else:
                    card["_bind_status"] = "held_null_extension"
                    card["_link_status"] = "held-null-with-reason"
                    card["_hold_reason"] = "Extension/circuit route — no exact geometry minted yet"
                    card.pop("route_id", None)
                    card.pop("route_ids", None)
                    held += 1

    doc.pop("brief_only_markets", None)
    doc.setdefault("_india_kcc_seal", {})["applied_at"] = utc_now()
    doc["_india_kcc_seal"]["sealed_cards"] = sealed
    doc["_india_kcc_seal"]["held_cards"] = held
    clean_uber_india_copy(doc)
    save_json(path, doc)
    save_json(DC / f"{slug}.json", doc)
    return {"partner": slug, "sealed": sealed, "held": held}


def main() -> int:
    if not MINT_REPORT.exists():
        print(f"FATAL: run mint_india_kolkata_chennai_geometry.py first ({MINT_REPORT})")
        return 1
    report = load_json(MINT_REPORT)
    bind_idx = build_bind_index(report.get("minted") or [])
    update_manifest()
    results = [seal_partner(slug, bind_idx) for slug in INDIA_PARTNERS]
    out = {"at": utc_now(), "lane": "grok/seal_india_kolkata_chennai_partners", "partners": results}
    save_json(HANDOFF / "india-kolkata-chennai-seal-report.json", out)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())