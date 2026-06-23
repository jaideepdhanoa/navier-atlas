#!/usr/bin/env python3
"""Promote model_link → route_id on journeys and featured_routes when geometry exists in ROUTES.json."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTNERS_DC = ROOT / "data-clean" / "partners"
PARTNERS_PITCH = ROOT / "partner-pitch" / "partners"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"

# Known mis-bound model_link overrides (null beats wrong)
JOURNEY_OVERRIDES: dict[tuple[str, str, str, str], str] = {
    ("bolt", "croatia", "Split", "Dubrovnik"): "rn-40ab54f8a8b0",
}

# Phase featured label → route_id when journeys remain unlinked
FEATURED_LABEL_PIN: dict[tuple[str, str, int, str], str] = {
    ("bolt", "croatia", 2, "Split ↔ Dubrovnik"): "rn-40ab54f8a8b0",
    ("bolt", "croatia", 2, "Hvar ↔ Dubrovnik"): "ics-276cee72da",
    ("bolt", "croatia", 2, "Korcula ↔ Dubrovnik"): "rn-ebb2c7e82b38",
    ("bolt", "croatia", 3, "Dubrovnik ↔ Korcula"): "rn-ebb2c7e82b38",
    ("minor-hotels", "palm-jumeirah", 2, "Dubai Marina → Anantara The Palm"): "rn-b0d5e6498ee4",
    ("minor-hotels", "", 3, "Dubai Marina → Anantara The Palm"): "rn-b0d5e6498ee4",
    ("minor-hotels", "maldives", 1, "Velana → Dhigu / Veli"): "e__velana__kurumba-jetty",
    ("minor-hotels", "", 3, "Velana → Anantara Veli / Dhigu"): "e__velana__kurumba-jetty",
    ("minor-hotels", "palm-jumeirah", 3, "Palm West → Atlantis"): "rn-b49c885ed913",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_route_ids() -> set[str]:
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    return {f.get("properties", f).get("id") for f in feats if f.get("properties", f).get("id")}


def resolve_model_link(
    partner: str,
    market_slug: str,
    item: dict,
    route_ids: set[str],
) -> str | None:
    fr = item.get("from") or ""
    to = item.get("to") or item.get("label") or ""
    for key, rid in JOURNEY_OVERRIDES.items():
        p, m, kfrom, kto = key
        if p == partner and m == market_slug and kfrom in fr and kto in to:
            if rid in route_ids:
                return rid
    ml = item.get("model_link")
    if ml and ml in route_ids:
        return ml
    return None


def promote_item(item: dict, rid: str) -> bool:
    if not isinstance(item, dict) or item.get("route_id"):
        return False
    if item.get("display") == "text_only":
        return False
    item["route_id"] = rid
    item["route_ids"] = [rid]
    item["_link_status"] = item.get("_link_status") or "linked-model-link"
    item["_link_source"] = item.get("_link_source") or "grok/promote_model_link_route_ids"
    item["_link_kind"] = item.get("_link_kind") or "model-link-promote"
    return True


def walk_container(
    partner: str,
    market_slug: str,
    container: dict,
    route_ids: set[str],
) -> int:
    n = 0
    for j in container.get("journeys_unlocked") or []:
        rid = resolve_model_link(partner, market_slug, j, route_ids)
        if rid and promote_item(j, rid):
            n += 1
    for ph in container.get("phases") or []:
        pn = ph.get("n")
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, dict) and fr.get("route_id"):
                continue
            pin = FEATURED_LABEL_PIN.get((partner, market_slug, pn, fr.get("label", ""))) if isinstance(fr, dict) else None
            if not pin and market_slug == "":
                pin = FEATURED_LABEL_PIN.get((partner, "", pn, fr.get("label", ""))) if isinstance(fr, dict) else None
            if pin and pin in route_ids and isinstance(fr, dict):
                if promote_item(fr, pin):
                    n += 1
                    continue
            rid = resolve_model_link(partner, market_slug, fr, route_ids) if isinstance(fr, dict) else None
            if rid and promote_item(fr, rid):
                n += 1
    return n


def promote_partner(doc: dict, slug: str, route_ids: set[str]) -> int:
    n = walk_container(slug, "", doc, route_ids)
    for m in doc.get("markets") or []:
        if not isinstance(m, dict):
            continue
        n += walk_container(slug, m.get("slug") or "", m, route_ids)
    return n


def write_partner(slug: str, doc: dict) -> None:
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    (PARTNERS_DC / f"{slug}.json").write_text(text)
    pitch = PARTNERS_PITCH / f"{slug}.json"
    if pitch.exists():
        pitch.write_text(text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", nargs="*")
    args = ap.parse_args()

    route_ids = load_route_ids()
    files = sorted(PARTNERS_DC.glob("*.json"))
    if args.partner:
        want = set(args.partner)
        files = [f for f in files if f.stem in want]

    report = {"at": utc_now(), "partners": [], "total_promoted": 0}
    for path in files:
        slug = path.stem
        if slug.startswith("_"):
            continue
        doc = json.loads(path.read_text())
        n = promote_partner(doc, slug, route_ids)
        row = {"partner": slug, "promoted": n}
        if args.apply and n:
            write_partner(slug, doc)
        report["partners"].append(row)
        report["total_promoted"] += n

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())