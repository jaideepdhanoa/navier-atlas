#!/usr/bin/env python3
"""Wave 3 — bind hospitality flagship corridors from cluster briefs + scoped gold routes."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import load_classes, proposal_class  # noqa: E402

PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
BRIEFS = ROOT / "data-clean" / "cluster_briefs"
REPORT = ROOT / "handoff" / "partner-map-model" / "hospitality-flagship-bind-report.json"

CLUSTER_BY_PARTNER = {
    "maldives": "maldives",
    "constance": "maldives",
    "crown-champa": "maldives",
    "sun-siyam": "maldives",
    "universal-enterprises": "maldives",
    "villa-hotels": "maldives",
    "six-senses": "maldives",
    "soneva": "maldives",
    "aman": "maldives",
    "jih-global": "maldives",
    "indian-ocean-luxury": "seychelles",
    "discovery-land": "bahamas",
    "norway-fjords": "norway",
    "four-seasons": "maldives",
    "red-sea-global": "red-sea-global-ksa",
    "french-polynesia": "french-polynesia",
    "cote-dazur": "france",
    "d-marin": "croatia",
    "hawaii": "hawaii-usa",
    "saudi-pif": "red-sea-global-ksa",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_gold_routes() -> tuple[set[str], list[dict]]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    ids = set()
    props = []
    for f in routes:
        p = f.get("properties") or {}
        if p.get("id"):
            ids.add(p["id"])
            props.append(p)
    return ids, props


def norm(s: str) -> str:
    s = (s or "").lower()
    for ch in ("↔", "—", "–", "/", "(", ")", ",", "&"):
        s = s.replace(ch, " ")
    return " ".join(s.split())


def token_set(*parts: str) -> set[str]:
    blob = " ".join(p for p in parts if p)
    return {t for t in norm(blob).split() if len(t) > 2}


def route_matches_item(item: dict, props: dict) -> bool:
    fn, tn = item.get("from_node_id"), item.get("to_node_id")
    if not fn or not tn:
        return True
    cities = {
        props.get("from_city_id") or props.get("from"),
        props.get("to_city_id") or props.get("to"),
    }
    item_cities = set()
    for n in (fn, tn):
        item_cities.add(n.split("__")[0] if "__" in str(n) else n)
    return bool(cities & item_cities) or fn == props.get("from") or tn == props.get("to")


def bind_item(item: dict, rid: str, props: dict, gold: set[str]) -> bool:
    if rid not in gold or not route_matches_item(item, props):
        return False
    item["route_id"] = rid
    item["route_ids"] = [rid]
    if props.get("distance_nm") is not None:
        item["distance_nm"] = props["distance_nm"]
    if props.get("from") and not str(item.get("from_node_id", "")).startswith("bp-"):
        item["from_node_id"] = props["from"]
    if props.get("to") and not str(item.get("to_node_id", "")).startswith("bp-"):
        item["to_node_id"] = props["to"]
    item["_link_kind"] = "hospitality-flagship"
    item["_link_status"] = "linked-grok-scoped"
    item["_link_source"] = "grok/bind_hospitality_flagship_corridors"
    item.pop("_hold_reason", None)
    item.setdefault("economics_status", "economics_pending")
    return True


def signature_pool(cluster_id: str, gold: set[str]) -> list[tuple[str, str, dict]]:
    path = BRIEFS / f"{cluster_id}.json"
    if not path.exists():
        return []
    brief = json.loads(path.read_text())
    pool: list[tuple[str, str, dict]] = []
    for sig in brief.get("signature_routes") or []:
        label = sig.get("label", "")
        rid = sig.get("route_id")
        if rid and rid in gold:
            pool.append((label, rid, {"label": label}))
        for r in sig.get("route_ids") or []:
            if r in gold:
                pool.append((label, r, {"label": label}))
    return pool


def scoped_routes(cities: set[str], route_props: list[dict]) -> list[dict]:
    out = []
    for p in route_props:
        fr = p.get("from_city_id") or p.get("from")
        to = p.get("to_city_id") or p.get("to")
        if fr in cities or to in cities:
            out.append(p)
    return out


def partner_cities(doc: dict) -> set[str]:
    cities: set[str] = set()
    for ph in doc.get("phases") or []:
        cities.update(ph.get("cities") or [])
    for j in doc.get("journeys_unlocked") or []:
        for k in ("from_node_id", "to_node_id"):
            v = j.get(k)
            if v and not str(v).startswith("bp-"):
                cities.add(v.split("__")[0] if "__" in str(v) else v)
    return cities


def bind_partner(slug: str, gold: set[str], route_props: list[dict]) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    if proposal_class(slug, doc) != "hospitality":
        return {"partner": slug, "skipped": "not hospitality"}
    cluster = CLUSTER_BY_PARTNER.get(slug, slug)
    pool = signature_pool(cluster, gold)
    cities = partner_cities(doc)
    scoped = scoped_routes(cities, route_props) if cities else route_props[:200]
    bound_j = bound_f = 0
    used: set[str] = set()

    def best_match(item: dict) -> str | None:
        it = token_set(item.get("from", ""), item.get("to", ""), item.get("label", ""))
        best_rid = None
        best_score = 0.35
        for label, rid, _ in pool:
            if rid in used:
                continue
            score = len(it & token_set(label)) / max(len(it), 1)
            if score > best_score:
                best_score = score
                best_rid = rid
        if best_rid:
            return best_rid
        for p in scoped:
            rid = p.get("id")
            if not rid or rid in used:
                continue
            label = p.get("label") or f"{p.get('from')} {p.get('to')}"
            score = len(it & token_set(label)) / max(len(it), 1)
            if score > best_score:
                best_score = score
                best_rid = rid
        if not best_rid and "velana" in norm(item.get("from", "")):
            for label, rid, _ in pool:
                if rid in used:
                    continue
                if "velana" in norm(label) or "malé" in norm(label) or "male" in norm(label):
                    return rid
        return best_rid

    for j in doc.get("journeys_unlocked") or []:
        if not isinstance(j, dict):
            continue
        if j.get("route_id") in gold:
            continue
        rid = best_match(j)
        if not rid:
            continue
        props = next((p for p in route_props if p.get("id") == rid), {})
        if bind_item(j, rid, props, gold):
            used.add(rid)
            bound_j += 1

    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if not isinstance(fr, dict):
                continue
            if fr.get("route_id") in gold:
                continue
            rid = best_match(fr)
            if not rid:
                continue
            props = next((p for p in route_props if p.get("id") == rid), {})
            if bind_item(fr, rid, props, gold):
                used.add(rid)
                bound_f += 1

    doc.setdefault("_hospitality_flagship_bind", {})["applied_at"] = utc_now()
    doc["_hospitality_flagship_bind"]["journeys"] = bound_j
    doc["_hospitality_flagship_bind"]["featured"] = bound_f
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "cluster": cluster, "journeys_bound": bound_j, "featured_bound": bound_f}


def main() -> int:
    data = load_classes()
    slugs = sys.argv[1:] if len(sys.argv) > 1 else [
        p for p, c in data["by_partner"].items() if c == "hospitality"
    ]
    gold, route_props = load_gold_routes()
    results = [bind_partner(s, gold, route_props) for s in slugs]
    out = {"at": utc_now(), "lane": "grok/bind_hospitality_flagship_corridors", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())