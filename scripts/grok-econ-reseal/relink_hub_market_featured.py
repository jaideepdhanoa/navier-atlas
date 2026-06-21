#!/usr/bin/env python3
"""Wave 8 — bind hub market featured_routes from scoped gold + journey mirrors."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import proposal_class  # noqa: E402

PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff" / "partner-map-model" / "hub-market-featured-relink-report.json"

DEFAULT_HUBS = ["gojek", "line", "didi", "lyft", "kakao-mobility"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower().strip())


def token_set(*parts: str) -> set[str]:
    blob = " ".join(p for p in parts if p).lower()
    for ch in ("↔", "—", "–", "/", "(", ")", ",", "&"):
        blob = blob.replace(ch, " ")
    return {t for t in blob.split() if len(t) > 2}


def load_gold() -> tuple[set[str], dict[str, dict], list[dict]]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    gold: set[str] = set()
    props: dict[str, dict] = {}
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id")
        if rid:
            gold.add(rid)
            props[rid] = p
    return gold, props, routes


def market_cities(market: dict) -> set[str]:
    cities: set[str] = set()
    cities.update(market.get("anchor_cities") or market.get("cities") or [])
    for ph in market.get("phases") or []:
        cities.update(ph.get("cities") or [])
    return cities


def scoped_pool(cities: set[str], routes: list, gold: set[str]) -> list[dict]:
    pool: list[dict] = []
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id")
        if not rid or rid not in gold:
            continue
        fr = p.get("from_city_id") or p.get("from")
        to = p.get("to_city_id") or p.get("to")
        if cities and not (fr in cities or to in cities):
            continue
        pool.append(p)
    return pool


def journey_index(market: dict) -> dict[tuple[str, str], dict]:
    idx: dict[tuple[str, str], dict] = {}
    for j in market.get("journeys_unlocked") or []:
        if not isinstance(j, dict):
            continue
        key = (norm(j.get("from", "")), norm(j.get("to", "")))
        if j.get("route_id"):
            idx[key] = j
    return idx


def bind_card(card: dict, rid: str, props: dict, gold: set[str]) -> bool:
    if rid not in gold:
        return False
    p = props.get(rid, {})
    card["route_id"] = rid
    card["route_ids"] = [rid]
    if p.get("from"):
        card["from_node_id"] = p["from"]
    if p.get("to"):
        card["to_node_id"] = p["to"]
    for k in ("distance_nm", "platform"):
        if p.get(k) is not None:
            card[k] = p[k]
    card["_link_kind"] = card.get("_link_kind", "hub-market-featured")
    card["_link_status"] = "linked-grok-scoped"
    card["_link_source"] = "grok/relink_hub_market_featured"
    card.pop("_hold_reason", None)
    card.setdefault("economics_status", "economics_pending")
    return True


def best_route(card: dict, pool: list[dict], gold: set[str], used: set[str]) -> str | None:
    label = card.get("label") or f"{card.get('from', '')} {card.get('to', '')}"
    ct = token_set(label, card.get("from", ""), card.get("to", ""))
    dist = card.get("distance_nm")
    best_rid = None
    best_score = 0.32
    for p in pool:
        rid = p.get("id")
        if not rid or rid in used:
            continue
        label_p = p.get("label") or ""
        score = len(ct & token_set(label_p)) / max(len(ct), 1)
        if card.get("from_node_id") and card.get("to_node_id"):
            ep = {p.get("from"), p.get("to"), p.get("from_node"), p.get("to_node")}
            if card["from_node_id"] in ep and card["to_node_id"] in ep:
                score = max(score, 0.9)
        if dist and p.get("distance_nm"):
            ratio = min(dist, p["distance_nm"]) / max(dist, p["distance_nm"])
            if ratio >= 0.6:
                score += 0.15
        if score > best_score:
            best_score = score
            best_rid = rid
    return best_rid


def relink_market(market: dict, routes: list, gold: set[str], props: dict[str, dict]) -> tuple[int, int]:
    cities = market_cities(market)
    pool = scoped_pool(cities, routes, gold)
    jidx = journey_index(market)
    bound_j = bound_f = 0
    used: set[str] = set()

    for j in market.get("journeys_unlocked") or []:
        if not isinstance(j, dict) or j.get("route_id") in gold:
            continue
        key = (norm(j.get("from", "")), norm(j.get("to", "")))
        mirror = jidx.get(key)
        if mirror and mirror is not j and mirror.get("route_id") in gold:
            if bind_card(j, mirror["route_id"], props, gold):
                used.add(mirror["route_id"])
                bound_j += 1
            continue
        rid = best_route(j, pool, gold, used)
        if rid and bind_card(j, rid, props, gold):
            used.add(rid)
            bound_j += 1

    for ph in market.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if not isinstance(fr, dict) or fr.get("route_id") in gold:
                continue
            label_key = (norm(fr.get("from", "")), norm(fr.get("to", "")))
            if not label_key[0]:
                parts = (fr.get("label") or "").split("↔")
                if len(parts) == 2:
                    label_key = (norm(parts[0]), norm(parts[1]))
            j = jidx.get(label_key)
            if j and j.get("route_id") in gold:
                if bind_card(fr, j["route_id"], props, gold):
                    bound_f += 1
                continue
            rid = best_route(fr, pool, gold, used)
            if rid and bind_card(fr, rid, props, gold):
                used.add(rid)
                bound_f += 1
    return bound_j, bound_f


def process(slug: str, gold: set[str], props: dict[str, dict], routes: list) -> dict:
    path = PARTNERS / f"{slug}.json"
    doc = json.loads(path.read_text())
    if proposal_class(slug, doc) != "hub":
        return {"partner": slug, "skipped": "not hub"}
    total_j = total_f = 0
    markets_out = []
    for m in doc.get("markets") or []:
        bj, bf = relink_market(m, routes, gold, props)
        total_j += bj
        total_f += bf
        if bj or bf:
            markets_out.append({"market": m.get("id"), "journeys": bj, "featured": bf})
    doc.setdefault("_hub_market_featured_relink", {})["applied_at"] = utc_now()
    doc["_hub_market_featured_relink"]["journeys"] = total_j
    doc["_hub_market_featured_relink"]["featured"] = total_f
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    dc = DC / f"{slug}.json"
    if dc.exists():
        dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return {"partner": slug, "markets": markets_out, "journeys_bound": total_j, "featured_bound": total_f}


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_HUBS
    gold, props, routes = load_gold()
    results = [process(s, gold, props, routes) for s in slugs]
    out = {"at": utc_now(), "lane": "grok/relink_hub_market_featured", "results": results}
    REPORT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())