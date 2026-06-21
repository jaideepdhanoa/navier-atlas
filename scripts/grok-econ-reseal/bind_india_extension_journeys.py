#!/usr/bin/env python3
"""Bind extension mint report onto India partner held-null journey cards."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"
EXT_REPORT = HANDOFF / "india-extension-mint-report.json"
INDIA = ("rapido", "ola", "uber-india-derivative", "adani-ports", "reliance-industries", "uber")


def norm(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[/|]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def bind_index(minted: list[dict]) -> dict[str, dict]:
    idx = {}
    for m in minted:
        k = f"{norm(m.get('journey_from'))}|{norm(m.get('journey_to'))}"
        idx[k] = m
        # partial match keys
        if "ariyadaha" in k:
            idx["fairlie|ariyadaha via howrah   baghbazar   belur   kutighat"] = m
        if "heritage hooghly" in k:
            idx["millennium park   babughat   princep ghat|heritage hooghly leisure loop"] = m
        if "puducherry" in k:
            idx["chennai|puducherry   pondicherry"] = m
        if "kovalam" in k:
            idx["napier bridge|kovalam via buckingham canal"] = m
    return idx


def iter_cards(doc: dict):
    for m in doc.get("markets") or []:
        if not isinstance(m, dict):
            continue
        mid = m.get("id")
        for j in m.get("journeys_unlocked") or []:
            if isinstance(j, dict):
                yield mid, j
        for ph in m.get("phases") or []:
            if not isinstance(ph, dict):
                continue
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, dict):
                    yield mid, fr


def try_bind(card: dict, idx: dict[str, dict], market_id: str) -> bool:
    if card.get("_bind_status") not in ("held_null_extension", "brief_only_grok_mint_required", None):
        if card.get("route_id"):
            return False
    key = f"{norm(card.get('from'))}|{norm(card.get('to'))}"
    hit = idx.get(key)
    if not hit:
        cf, ct = norm(card.get("from")), norm(card.get("to"))
        for k, m in idx.items():
            jf, jt = k.split("|", 1)
            if (cf in jf or jf in cf) and (ct in jt or jt in ct or any(t in ct for t in jt.split()[:3])):
                hit = m
                break
    if not hit:
        return False
    card["route_id"] = hit["route_id"]
    card["route_ids"] = [hit["route_id"]]
    card["from_node_id"] = hit["from_bp"]
    card["to_node_id"] = hit["to_bp"]
    card["distance_nm"] = hit["distance_nm"]
    if hit.get("roadmap"):
        card["_bind_status"] = "roadmap_feasibility"
        card["_link_status"] = "roadmap-no-geometry"
        card["render"] = "roadmap-amber-dashed"
        card["_hold_reason"] = "Buckingham Canal water-metro — feasibility stage only"
    else:
        card["_bind_status"] = "sealed_grok_extension"
        card["_link_status"] = "linked-grok-scoped"
        card["_link_source"] = "grok/bind_india_extension_journeys"
        card.pop("_hold_reason", None)
    card["economics_status"] = "economics_pending"
    card["_market_candidate"] = market_id
    return True


def main() -> int:
    if not EXT_REPORT.exists():
        print("run mint_india_extension_routes.py first")
        return 1
    minted = load_json(EXT_REPORT).get("minted", [])
    idx = bind_index(minted)
    results = []
    for slug in INDIA:
        path = PARTNERS / f"{slug}.json"
        doc = load_json(path)
        bound = 0
        for mid, card in iter_cards(doc):
            if try_bind(card, idx, mid):
                bound += 1
        doc.setdefault("_india_extension_bind", {})["bound"] = bound
        doc["_india_extension_bind"]["at"] = datetime.now(timezone.utc).isoformat()
        save = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
        path.write_text(save)
        (DC / f"{slug}.json").write_text(save)
        results.append({"partner": slug, "bound": bound})
    out = {"at": datetime.now(timezone.utc).isoformat(), "partners": results}
    (HANDOFF / "india-extension-bind-report.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


def load_json(path: Path):
    return json.loads(path.read_text())


if __name__ == "__main__":
    raise SystemExit(main())