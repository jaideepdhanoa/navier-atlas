#!/usr/bin/env python3
"""Repair ferry-operator pages contaminated with HK template journeys — bind ICS/edge from cluster briefs."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
BRIEFS = ROOT / "data-clean" / "cluster_briefs"
CITY_BRIEFS = ROOT / "data-clean" / "city_briefs"
ARCHETYPE = ROOT / "handoff" / "partner-map-model" / "public-transit-authority-archetype.json"
REPORT = ROOT / "handoff" / "partner-map-model" / "ferry-flagship-repair-report.json"

FERRY_REPAIR: dict[str, dict] = {
    "norway-fjords": {
        "cluster": "norway",
        "cities": ["bergen-norway", "stavanger-norway", "geiranger-norway"],
        "phase_labels": [
            "Phase 1 — UNESCO fjord compliance (Geiranger)",
            "Phase 2 — Stavanger / Lysefjord hurtigbåt",
            "Phase 3 — Bergen marina belt",
        ],
    },
    "fullers360": {
        "city_brief": "auckland-new-zealand",
        "cities": ["auckland-new-zealand"],
        "phase_labels": [
            "Phase 1 — Waiheke & Devonport commuter",
            "Phase 2 — Hauraki Gulf islands",
        ],
        "city_route_filter": "auckland-new-zealand",
        "signature_route_ids": [
            "ics-09a1d1e6e5",
        ],
    },
    "transport-nsw": {
        "archetype": "transport-nsw",
        "cities": ["sydney-australia"],
        "city_route_filter": "sydney-australia",
        "phase_labels": [
            "Phase 1 — Manly & inner-harbour commuter",
            "Phase 2 — Parramatta River network",
            "Phase 3 — Olympic Park & eastern bays",
        ],
    },
    "thames-clippers": {
        "archetype": "thames-clippers",
        "cities": ["london-thames-uk"],
        "city_route_filter": "london-thames-uk",
        "phase_labels": [
            "Phase 1 — Central fast zero-wake pilot (Pioneer II)",
            "Phase 2 — Full-length + new developments (Pioneer II)",
            "Phase 3 — Royal Docks & Thamesmead",
        ],
    },
    "shun-tak": {
        "archetype": "hong-kong",
        "cities": ["hong-kong"],
        "city_route_filter": "hong-kong",
        "phase_labels": [
            "Phase 1 — Victoria Harbour premium pilot",
            "Phase 2 — Outlying islands network",
            "Phase 3 — PRD cross-border connectivity",
        ],
    },
    "maldives-government": {
        "cluster": "maldives",
        "cities": ["male-maldives"],
        "phase_labels": [
            "Phase 1 — Velana resort transfer pilot",
            "Phase 2 — North Malé atoll network",
            "Phase 3 — Regional gateway connectivity",
        ],
    },
    "bc-ferries": {
        "city_brief": "vancouver-canada",
        "cities": ["vancouver-canada"],
        "city_route_filter": "vancouver-canada",
        "phase_labels": [
            "Phase 1 — Downtown Vancouver ↔ Victoria fast passenger (Quanta-LR)",
            "Phase 2 — Gulf Islands + Nanaimo network (Pioneer II + Quanta-LR)",
            "Phase 3 — Coastal foiling passenger network",
        ],
    },
    "wsf": {
        "city_brief": "seattle-puget-sound-usa",
        "cities": ["seattle-puget-sound-usa"],
        "city_route_filter": "seattle-puget-sound-usa",
        "phase_labels": [
            "Phase 1 — Cross-Sound fast passenger pilot (Pioneer II)",
            "Phase 2 — San Juan Islands + South Sound (Quanta-LR)",
            "Phase 3 — Regional Sound network scale",
        ],
    },
    "hawaii": {
        "cluster": "hawaii-usa",
        "cities": [
            "oahu-honolulu-hawaii-usa",
            "maui-county-hawaii-usa",
            "kauai-hawaii-usa",
            "hawaii-island-hawaii-usa",
        ],
        "phase_labels": [
            "Phase 1 — Pulama Lānaʻi signature arrival",
            "Phase 2 — Maui County inter-island",
            "Phase 3 — Statewide inter-island network",
        ],
    },
    "nyc-ferry": {
        "archetype": "nyc-ferry",
        "cities": ["new-york-harbor-usa"],
        "city_route_filter": "new-york-harbor-usa",
        "phase_labels": [
            "Phase 1 — Rockaway long-range + East River wake pilot",
            "Phase 2 — Regional Hudson + harbor routes",
            "Phase 3 — Midtown & NJ Gold Coast",
            "Phase 4 — JFK / Jamaica Bay roadmap",
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_gold() -> tuple[set[str], dict[str, dict]]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    gold: set[str] = set()
    props: dict[str, dict] = {}
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id")
        if rid:
            gold.add(rid)
            props[rid] = p
    return gold, props


def split_label(label: str) -> tuple[str, str]:
    for sep in ("↔", "→", "->", "—", "–"):
        if sep in label:
            parts = label.split(sep, 1)
            return parts[0].strip(), parts[1].strip()
    return label, label


def card_from_route(rid: str, label: str, props: dict, gold: set[str]) -> dict | None:
    if rid not in gold:
        return None
    p = props[rid]
    fr_l, to_l = split_label(label)
    card = {
        "label": label,
        "from_node_id": p.get("from") or p.get("from_node"),
        "to_node_id": p.get("to") or p.get("to_node"),
        "distance_nm": p.get("distance_nm"),
        "platform": p.get("platform") or "Pioneer II",
        "route_id": rid,
        "route_ids": [rid],
        "_link_kind": "ferry-flagship",
        "_link_status": "linked-grok-scoped",
        "_link_source": "grok/repair_ferry_flagship_corridors",
        "economics_status": "economics_pending",
    }
    return card


def journey_from_route(rid: str, label: str, props: dict, gold: set[str], *, archetype: str) -> dict | None:
    card = card_from_route(rid, label, props, gold)
    if not card:
        return None
    fr_l, to_l = split_label(label)
    return {
        "from": fr_l,
        "to": to_l,
        "today": "Diesel ferry or excursion craft — slow, emissions-constrained where mandated.",
        "with_navier": "A fast, silent foiling run on the sealed corridor — zero-emission where the mandate requires it.",
        "distance_nm": card.get("distance_nm"),
        "platform": card.get("platform"),
        "archetype": archetype,
        "from_node_id": card["from_node_id"],
        "to_node_id": card["to_node_id"],
        "route_id": rid,
        "route_ids": [rid],
        "_link_kind": "ferry-flagship",
        "_link_status": "linked-grok-scoped",
        "_link_source": "grok/repair_ferry_flagship_corridors",
        "economics_status": "economics_pending",
    }


def city_gold_routes(city_id: str, gold: set[str], props: dict[str, dict]) -> list[dict]:
    sigs = []
    for rid, p in props.items():
        if rid not in gold:
            continue
        fr = p.get("from_city_id") or p.get("from")
        to = p.get("to_city_id") or p.get("to")
        if city_id not in (fr, to):
            continue
        if not str(rid).startswith(("ics-", "e__", "rn-", "edge")):
            continue
        sigs.append({"label": p.get("label") or rid, "route_id": rid})
    return sigs


def flatten_cluster_signatures(brief: dict) -> list[dict]:
    sigs: list[dict] = []
    for sig in brief.get("signature_routes") or []:
        rid = sig.get("route_id")
        rids = sig.get("route_ids") or []
        label = sig.get("label", "")
        if rid:
            sigs.append({"label": label, "route_id": rid})
        for r in rids:
            sigs.append({"label": label, "route_id": r})
    return sigs


def archetype_signatures(slug: str, gold: set[str]) -> list[dict]:
    doc = json.loads(ARCHETYPE.read_text())
    cfg = (doc.get("partners") or {}).get(slug) or {}
    sigs: list[dict] = []
    for specs in (cfg.get("supplement_routes") or {}).values():
        for spec in specs:
            if spec.get("economics_status") == "roadmap_excluded":
                continue
            rid = spec.get("route_id")
            if rid and rid in gold:
                sigs.append({"label": spec.get("label", rid), "route_id": rid})
    return sigs


def signature_routes(cfg: dict, gold: set[str], props: dict[str, dict]) -> list[dict]:
    if cfg.get("archetype"):
        sigs = archetype_signatures(cfg["archetype"], gold)
        city_filter = cfg.get("city_route_filter")
        if city_filter:
            seen = {s["route_id"] for s in sigs}
            for s in city_gold_routes(city_filter, gold, props):
                if s["route_id"] not in seen:
                    sigs.append(s)
        return sigs
    if cfg.get("cluster"):
        brief = json.loads((BRIEFS / f"{cfg['cluster']}.json").read_text())
        return flatten_cluster_signatures(brief)
    if cfg.get("city_brief"):
        sigs: list[dict] = []
        city_filter = cfg.get("city_route_filter")
        if city_filter:
            sigs.extend(city_gold_routes(city_filter, gold, props))
        seen = {s["route_id"] for s in sigs if s.get("route_id")}
        for rid in cfg.get("signature_route_ids") or []:
            if rid not in seen:
                sigs.append({"label": rid, "route_id": rid})
        return sigs
    return []


def repair_partner(slug: str, cfg: dict, gold: set[str], props: dict[str, dict]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    sigs = signature_routes(cfg, gold, props)
    journeys = []
    featured = []
    for sig in sigs:
        rid = sig.get("route_id")
        label = sig.get("label", rid or "")
        if not rid:
            continue
        j = journey_from_route(rid, label, props, gold, archetype="commute" if "ics-" in rid else "intercity")
        if j:
            journeys.append(j)
        fr = card_from_route(rid, label, props, gold)
        if fr:
            featured.append(fr)

    if not journeys:
        return {"partner": slug, "skipped": "no gold signatures"}

    doc["journeys_unlocked"] = journeys
    phases = doc.get("phases") or []
    labels = cfg.get("phase_labels") or []
    cities = cfg.get("cities") or []
    n_ph = max(len(phases), 1)
    chunk = max(1, (len(featured) + n_ph - 1) // n_ph) if featured else 0
    for i, ph in enumerate(phases):
        if cities:
            ph["cities"] = cities
        if i < len(labels):
            ph["label"] = labels[i]
        if featured:
            start = i * chunk
            ph["featured_routes"] = featured[start : start + chunk] if start < len(featured) else []
        else:
            ph["featured_routes"] = []

    doc.setdefault("_ferry_flagship_repair", {})["applied_at"] = utc_now()
    doc["_ferry_flagship_repair"]["journeys"] = len(journeys)
    doc["_ferry_flagship_repair"]["featured"] = len(featured)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "journeys": len(journeys), "featured": len(featured)}


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else list(FERRY_REPAIR)
    gold, props = load_gold()
    results = [repair_partner(s, FERRY_REPAIR[s], gold, props) for s in slugs if s in FERRY_REPAIR]
    out = {"at": utc_now(), "lane": "grok/repair_ferry_flagship_corridors", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())