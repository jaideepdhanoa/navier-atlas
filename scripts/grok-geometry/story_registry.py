#!/usr/bin/env python3
"""Collect all story-visible route_ids from partners + briefs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "data-clean" / "partners"
CITY_BRIEFS = ROOT / "data-clean" / "city_briefs"
CLUSTER_BRIEFS = ROOT / "data-clean" / "cluster_briefs"


def route_ids_of(o) -> list[str]:
    if not o or isinstance(o, str):
        return []
    out = []
    if o.get("route_id"):
        out.append(o["route_id"])
    for r in o.get("route_ids") or []:
        if r:
            out.append(r)
    return out


def scan_phases(phases, prefix: str, out: dict):
    for ph in phases or []:
        n = ph.get("n") or ph.get("phase")
        tag = f"{prefix}:phase:{n}" if n is not None else f"{prefix}:phase"
        for fr in ph.get("featured_routes") or []:
            for rid in route_ids_of(fr):
                out.setdefault(rid, set()).add(tag)
                out[rid].add("featured")


def collect_story_registry() -> dict[str, list[str]]:
    out: dict[str, set[str]] = {}

    def add(rid: str, tag: str):
        if rid:
            out.setdefault(rid, set()).add(tag)

    for path in sorted(PARTNERS.glob("*.json")):
        if path.name.startswith("_"):
            continue
        doc = json.loads(path.read_text())
        pid = doc.get("partner_id") or path.stem
        scan_phases(doc.get("phases"), pid, out)
        for j in doc.get("journeys_unlocked") or []:
            for rid in route_ids_of(j):
                add(rid, f"{pid}:journey")
        for m in doc.get("markets") or []:
            mslug = m.get("slug") or m.get("market_id") or m.get("id") or "market"
            scan_phases(m.get("phases"), f"{pid}/{mslug}", out)
            for fr in m.get("featured_routes") or []:
                for rid in route_ids_of(fr):
                    add(rid, f"{pid}/{mslug}:featured")
            for j in m.get("journeys_unlocked") or []:
                for rid in route_ids_of(j):
                    add(rid, f"{pid}/{mslug}:journey")
        md = doc.get("map_display") or {}
        for rid in md.get("promote_route_ids") or []:
            add(rid, f"{pid}:promoted")
        for rid in md.get("roadmap_route_ids") or []:
            add(rid, f"{pid}:roadmap")

    for brief_dir in (CITY_BRIEFS, CLUSTER_BRIEFS):
        if not brief_dir.is_dir():
            continue
        for path in brief_dir.glob("*.json"):
            doc = json.loads(path.read_text())
            for sr in doc.get("signature_routes") or []:
                for rid in route_ids_of(sr):
                    add(rid, f"signature:{path.stem}")

    return {k: sorted(v) for k, v in sorted(out.items())}