#!/usr/bin/env python3
"""Mark remaining unlinked journeys/featured_routes as geometry-pending text chips."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTNERS_DC = ROOT / "data-clean" / "partners"
PARTNERS_PITCH = ROOT / "partner-pitch" / "partners"

SKIP_IF_LINKED = frozenset({"linked-grok-scoped", "linked-grok-node", "linked-model-link", "linked-property-geometry"})


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mark_item(item: dict) -> bool:
    if not isinstance(item, dict) or item.get("route_id"):
        return False
    if item.get("route_ids"):
        return False
    st = item.get("_link_status") or ""
    if st in SKIP_IF_LINKED or item.get("display") == "text_only":
        return False
    if st == "unlinked-intra-city":
        item["display"] = "text_only"
        return True
    item["display"] = "text_only"
    item["_link_status"] = "aspirational-no-built-route"
    item["_link_kind"] = item.get("_link_kind") or "aspirational-chip"
    item["_link_source"] = item.get("_link_source") or "grok/mark_unlinked_aspirational"
    item.setdefault("economics_status", "roadmap_excluded")
    item.setdefault("render", "roadmap-amber-dashed")
    return True


def _phase_chip_label(ph: dict) -> str:
    for uc in ph.get("use_cases") or []:
        if isinstance(uc, dict) and uc.get("label"):
            return uc["label"]
        if isinstance(uc, str) and uc.strip():
            return uc.strip()
    raw = ph.get("narrative") or ph.get("label") or "Roadmap corridor"
    return raw if len(raw) <= 120 else raw[:117] + "…"


def fill_empty_phase(ph: dict) -> bool:
    if ph.get("featured_routes"):
        return False
    ph["featured_routes"] = [{
        "label": _phase_chip_label(ph),
        "display": "text_only",
        "_link_status": "aspirational-no-built-route",
        "_link_kind": "aspirational-phase-chip",
        "_link_source": "grok/mark_unlinked_aspirational",
        "economics_status": "roadmap_excluded",
        "render": "roadmap-amber-dashed",
    }]
    return True


def walk(doc: dict) -> int:
    n = 0
    for j in doc.get("journeys_unlocked") or []:
        if mark_item(j):
            n += 1
    for ph in doc.get("phases") or []:
        if fill_empty_phase(ph):
            n += 1
        for fr in ph.get("featured_routes") or []:
            if mark_item(fr):
                n += 1
    for m in doc.get("markets") or []:
        for j in m.get("journeys_unlocked") or []:
            if mark_item(j):
                n += 1
        for ph in m.get("phases") or []:
            if fill_empty_phase(ph):
                n += 1
            for fr in ph.get("featured_routes") or []:
                if mark_item(fr):
                    n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", nargs="+", required=True)
    args = ap.parse_args()

    report = {"at": utc_now(), "partners": []}
    for slug in args.partner:
        path = PARTNERS_DC / f"{slug}.json"
        doc = json.loads(path.read_text())
        n = walk(doc)
        if args.apply and n:
            text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
            path.write_text(text)
            pitch = PARTNERS_PITCH / f"{slug}.json"
            if pitch.exists():
                pitch.write_text(text)
        report["partners"].append({"partner": slug, "marked": n})
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())