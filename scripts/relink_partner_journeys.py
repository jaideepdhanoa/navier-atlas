#!/usr/bin/env python3
"""
Grok-led re-linker for partner journeys_unlocked + featured_routes.

City-brief-grade binding: scope candidates to market/phase cities, borrow sealed
signature_routes from city/cluster briefs, two-gate match (distance ±25%, endpoint
tokens). Null beats wrong — clears mis-linked route_ids before re-binding.

Usage:
  python3 scripts/relink_partner_journeys.py --audit
  python3 scripts/relink_partner_journeys.py --apply
  python3 scripts/relink_partner_journeys.py --apply --partner bolt yango
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Anchor shorthand → sealed city_id (Grok-maintained; extend as needed)
NODE_CROSSWALK: dict[str, str] = {
    "dubai": "dubai-uae",
    "abu-dhabi": "abu-dhabi-uae",
    "sharjah": "sharjah-uae",
    "fujairah": "fujairah-uae",
    "ras-al-khaimah": "ras-al-khaimah-uae",
    "doha": "doha-qatar",
    "palma-mallorca-spain": "mallorca-spain",
    "el-gouna-egypt": "hurghada-el-gouna-egypt",
    "hurghada-egypt": "hurghada-el-gouna-egypt",
    "redsea-egypt": "hurghada-el-gouna-egypt",
    "neom-ksa": "neom-sindalah-ksa",
    "amaala-ksa": "red-sea-global-ksa",
    "red-sea-global": "red-sea-global-ksa",
    "ksa-commercial": "jeddah-ksa",
    "dammam-khobar-ksa": "eastern-province-ksa",
    "bodrum": "bodrum-turkey",
    "cesme-izmir": "cesme-izmir-turkey",
    "antalya": "antalya-turkey",
    "istanbul": "istanbul-turkey",
    "cairo": "cairo-egypt",
    "lisbon-tagus": "lisbon-tagus-portugal",
    "porto": "porto-douro-portugal",
    "helsinki": "helsinki-finland",
    "tallinn": "tallinn-estonia",
    "dublin": "dublin-ireland",
    "lagos": "lagos-nigeria",
    "singapore": "singapore",
    "bangkok": "bangkok-thailand",
    "bali": "jakarta-indonesia",
    "jakarta": "jakarta-indonesia",
}

CITY_SEARCH_ALIASES: dict[str, list[str]] = {
    "red-sea-global-ksa": ["red-sea-global-ksa", "the-red-sea-archipelago-ksa"],
    "hurghada-el-gouna-egypt": ["hurghada-el-gouna-egypt", "sharm-el-sheikh-egypt"],
    "lisbon-tagus-portugal": ["lisbon-tagus-portugal", "porto-douro-portugal", "algarve-portugal"],
    "athens-saronic-greece": ["athens-saronic-greece", "mykonos-greece"],
}

# Keep marina/jetty/palm/etc. — they distinguish corridors; only drop filler grammar.
_LABEL_STOP = frozenset(
    {
        "the", "and", "of", "to", "from", "via", "with", "for", "into", "near", "off",
    }
)

_GEO_STOP = frozenset(
    {
        "the", "and", "to", "of", "at", "via", "from", "near", "off", "reach", "regional",
        "islands", "island", "bay", "coast", "point", "city", "pier", "jetty", "terminal",
        "harbour", "harbor", "marina", "waterfront", "resort", "resorts", "beach", "club",
        "ferry", "cruise", "water", "wharf", "dock", "cove", "north", "south", "east", "west",
        "central", "grand", "greater", "area", "district", "downtown", "cbd", "intl",
        "international", "airport", "seaplane",
    }
)

ROUTE_LINK_TOL = 0.25

# Tokens too generic to anchor a directional match on their own.
_COMMON_PLACE = frozenset(
    {
        "dubai", "abu", "dhabi", "harbour", "harbor", "marina", "beach", "island",
        "islands", "palm", "jumeirah", "corniche", "harbour", "experience", "resort",
        "central", "downtown", "city", "gulf", "creek", "harbor",
    }
)


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_label(s: str | None) -> str:
    if not s:
        return ""
    s = _strip_accents(s.lower().strip())
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _tokens(s: str | None, stops: frozenset[str] = _LABEL_STOP) -> set[str]:
    return {t for t in norm_label(s).split() if t and t not in stops}


def _place_toks(s: str | None) -> set[str]:
    return {w for w in re.split(r"[^a-z]+", norm_label(s)) if len(w) > 3 and w not in _GEO_STOP}


def _anchor_tokens(s: str | None) -> list[str]:
    return [
        t
        for t in sorted(_tokens(s), key=len, reverse=True)
        if len(t) >= 4 and t not in _COMMON_PLACE
    ]


def directional_endpoints_match(from_l: str | None, to_l: str | None, rec: RouteRec) -> bool:
    if not labels_match(from_l, rec.from_label) or not labels_match(to_l, rec.to_label):
        return False
    for side_l, side_r in ((from_l, rec.from_label), (to_l, rec.to_label)):
        anchors = _anchor_tokens(side_l)
        if not anchors:
            continue
        rl = norm_label(side_r)
        if not any(a in rl for a in anchors):
            return False
    return True


def labels_match(a: str | None, b: str | None) -> bool:
    na, nb = norm_label(a), norm_label(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    overlap = ta & tb
    need = min(2, min(len(ta), len(tb)))
    return len(overlap) >= max(1, need)


def crosswalk_node(nid: str | None) -> str | None:
    if not nid:
        return nid
    return NODE_CROSSWALK.get(nid, nid)


def expand_scope(city_ids: set[str]) -> set[str]:
    out: set[str] = set()
    for cid in city_ids:
        for alias in CITY_SEARCH_ALIASES.get(cid, [cid]):
            out.add(alias)
    return out


@dataclass
class RouteRec:
    id: str
    from_label: str
    to_label: str
    from_city_id: str | None
    to_city_id: str | None
    from_node: str | None
    to_node: str | None
    distance_nm: float | None
    edge_class: str | None


@dataclass
class BriefRouteIndex:
    by_label: dict[str, str] = field(default_factory=dict)
    by_city_label: dict[tuple[str, str], str] = field(default_factory=dict)
    by_city: dict[str, list[tuple[str, str]]] = field(default_factory=dict)


@dataclass
class LinkStats:
    total: int = 0
    linked: int = 0
    cleared_mislink: int = 0
    borrowed_brief: int = 0
    matched_scoped: int = 0
    matched_node: int = 0
    still_null: int = 0
    geometry_pending: int = 0


def route_visible(p: dict) -> bool:
    if p.get("_quarantine"):
        return False
    if str(p.get("relevance", "")).lower() == "hide":
        return False
    return True


def build_city_ids(features_by_type: dict) -> set[str]:
    out: set[str] = set()
    for t in ("city", "priority_city"):
        for f in features_by_type.get(t, []):
            pid = (f.get("properties") or {}).get("id")
            if pid:
                out.add(pid)
    return out


def build_locale_parents(features_by_type: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for f in features_by_type.get("locale", []):
        p = f.get("properties") or {}
        if p.get("id") and p.get("parent_city_id"):
            out[p["id"]] = p["parent_city_id"]
    return out


def city_id_of(node_id: str | None, city_ids: set[str], locale_parents: dict[str, str]) -> str | None:
    if not node_id:
        return None
    nid = crosswalk_node(node_id) or node_id
    if nid in city_ids:
        return nid
    if nid in locale_parents and locale_parents[nid] in city_ids:
        return locale_parents[nid]
    pre = nid.split("__", 1)[0]
    pre = crosswalk_node(pre) or pre
    if pre in city_ids:
        return pre
    return pre if pre in city_ids else None


def resolve_phase_cities(cities: list | None, city_ids: set[str]) -> list[str]:
    out: set[str] = set()
    for c in cities or []:
        c = crosswalk_node(c) or c
        if c in city_ids:
            out.add(c)
            continue
        x = str(c).lower()
        for cid in city_ids:
            a = cid.lower()
            if (
                a == x
                or a.startswith(x + "-")
                or a.startswith(x + "_")
                or x in a.split("-")
                or x in a.split("_")
            ):
                out.add(cid)
    return list(out)


def load_routes(root: Path) -> tuple[dict[str, RouteRec], dict[str, list[str]]]:
    raw = load_json(root / "data-clean/ROUTES.json")
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id: dict[str, RouteRec] = {}
    by_city: dict[str, list[str]] = defaultdict(list)
    for f in feats:
        p = f.get("properties") or {}
        if not route_visible(p):
            continue
        rid = p.get("id")
        if not rid:
            continue
        rec = RouteRec(
            id=rid,
            from_label=p.get("from_label") or p.get("from") or "",
            to_label=p.get("to_label") or p.get("to") or "",
            from_city_id=p.get("from_city_id"),
            to_city_id=p.get("to_city_id"),
            from_node=p.get("from"),
            to_node=p.get("to"),
            distance_nm=p.get("distance_nm"),
            edge_class=p.get("edge_class"),
        )
        by_id[rid] = rec
        for cid in (rec.from_city_id, rec.to_city_id):
            if cid:
                by_city[cid].append(rid)
    return by_id, by_city


def load_brief_index(root: Path) -> BriefRouteIndex:
    idx = BriefRouteIndex()
    for sub, key in (("city_briefs", "city_id"), ("cluster_briefs", "cluster_id")):
        d = root / "data-clean" / sub
        if not d.is_dir():
            continue
        for p in d.glob("*.json"):
            b = load_json(p)
            owner = b.get(key) or p.stem
            for sr in b.get("signature_routes") or []:
                if isinstance(sr, str):
                    continue
                lbl = sr.get("label")
                rid = sr.get("route_id")
                if not lbl or not rid:
                    continue
                nl = norm_label(lbl)
                idx.by_label[nl] = rid
                idx.by_city_label[(owner, nl)] = rid
                idx.by_city.setdefault(owner, []).append((nl, rid))
    return idx


def route_in_scope(rec: RouteRec, scope: set[str]) -> bool:
    return bool(
        (rec.from_city_id and rec.from_city_id in scope)
        or (rec.to_city_id and rec.to_city_id in scope)
    )


def distance_ok(label_nm: float | None, route_nm: float | None) -> bool:
    if label_nm is None or route_nm is None:
        return True
    return abs(route_nm - label_nm) / max(label_nm, 1.0) <= ROUTE_LINK_TOL


def endpoint_ok(label_text: str, rec: RouteRec) -> bool:
    lab = _place_toks(label_text)
    if not lab:
        return True
    ep = _place_toks(rec.from_label + " " + rec.to_label)
    if not ep:
        return True
    return bool(lab & ep)


def passes_gates(item: dict, rec: RouteRec, label_text: str) -> bool:
    return distance_ok(item.get("distance_nm"), rec.distance_nm) and endpoint_ok(label_text, rec)


def score_route_match(
    from_l: str | None,
    to_l: str | None,
    rec: RouteRec,
    label_nm: float | None,
    partner_slug: str | None = None,
) -> float:
    """Both endpoints must match in authored direction (from→to). No reverse scoring."""
    if not from_l or not to_l:
        return 0.0
    if not directional_endpoints_match(from_l, to_l, rec):
        return 0.0
    score = 10.0
    if label_nm is not None and rec.distance_nm is not None:
        delta = abs(rec.distance_nm - label_nm) / max(label_nm, 1.0)
        if delta > ROUTE_LINK_TOL:
            score -= min(6.0, delta * 4.0)
        else:
            score += 2.0 * (1.0 - delta)
    if partner_slug:
        slug = partner_slug.lower()
        if rec.id.endswith(f"-{slug}"):
            score += 3.0
        elif f"-{slug}" in rec.id:
            score += 2.0
    elif rec.id.startswith("rn-"):
        score += 0.5
    return score


def borrow_from_brief(
    item: dict,
    scope: set[str],
    brief_idx: BriefRouteIndex,
    routes: dict[str, RouteRec],
    partner_slug: str | None = None,
) -> str | None:
    from_l = item.get("from") or item.get("from_label") or ""
    to_l = item.get("to") or item.get("to_label") or ""
    label = item.get("label") or f"{from_l} → {to_l}"
    label_n = norm_label(label)
    label_text = f"{from_l} {to_l}"

    candidates: list[str] = []
    for city in scope:
        rid = brief_idx.by_city_label.get((city, label_n))
        if rid:
            candidates.append(rid)
        for nl, br_rid in brief_idx.by_city.get(city, []):
            if label_n == nl or label_n in nl or nl in label_n:
                candidates.append(br_rid)
    for nl, rid in brief_idx.by_label.items():
        if label_n == nl or label_n in nl or nl in label_n:
            candidates.append(rid)

    best: str | None = None
    best_score = 0.0
    for rid in dict.fromkeys(candidates):
        if rid not in routes:
            continue
        rec = routes[rid]
        if not route_in_scope(rec, scope):
            continue
        if not from_l or not to_l:
            continue
        sc = score_route_match(from_l, to_l, rec, item.get("distance_nm"), partner_slug)
        if sc < 8.0:
            continue
        trial = dict(item)
        if rec.distance_nm is not None:
            trial["distance_nm"] = rec.distance_nm
        if not passes_gates(trial, rec, label_text):
            continue
        if sc > best_score:
            best_score = sc
            best = rid
    return best


def find_scoped_route(
    item: dict,
    scope: set[str],
    routes: dict[str, RouteRec],
    routes_by_city: dict[str, list[str]],
    partner_slug: str | None = None,
) -> str | None:
    from_l = item.get("from") or item.get("from_label")
    to_l = item.get("to") or item.get("to_label")
    label_text = item.get("label") or f"{from_l or ''} {to_l or ''}"
    label_nm = item.get("distance_nm")

    candidates: set[str] = set()
    for cid in scope:
        candidates.update(routes_by_city.get(cid, []))

    best_id: str | None = None
    best_score = 0.0
    for rid in candidates:
        rec = routes.get(rid)
        if not rec or not route_in_scope(rec, scope):
            continue
        # Score against graph distance when endpoints match — authored label_nm may be rounded.
        score_nm = rec.distance_nm if rec.distance_nm is not None else label_nm
        sc = score_route_match(from_l, to_l, rec, score_nm, partner_slug)
        if sc <= best_score:
            continue
        trial = dict(item)
        if rec.distance_nm is not None:
            trial["distance_nm"] = rec.distance_nm
        if not passes_gates(trial, rec, label_text):
            continue
        best_score = sc
        best_id = rid
    return best_id if best_score >= 8.0 else None


def find_node_pair_route(
    item: dict,
    routes: dict[str, RouteRec],
    routes_by_city: dict[str, list[str]],
    scope: set[str],
) -> str | None:
    fn = crosswalk_node(item.get("from_node_id") or item.get("from_node"))
    tn = crosswalk_node(item.get("to_node_id") or item.get("to_node"))
    if not fn or not tn or fn == tn:
        return None
    label_text = item.get("label") or ""
    label_nm = item.get("distance_nm")
    best_id: str | None = None
    best_score = 0.0
    for cid in scope:
        for rid in routes_by_city.get(cid, []):
            rec = routes[rid]
            if {rec.from_node, rec.to_node} != {fn, tn} and {rec.from_city_id, rec.to_city_id} != {fn, tn}:
                # try city-level node match via city ids
                if not (
                    (rec.from_node == fn and rec.to_node == tn)
                    or (rec.from_node == tn and rec.to_node == fn)
                ):
                    continue
            sc = 3.0
            if label_nm is not None and rec.distance_nm is not None:
                delta = abs(rec.distance_nm - label_nm) / max(label_nm, 1.0)
                if delta > ROUTE_LINK_TOL:
                    continue
                sc += 1.0 - delta
            if not endpoint_ok(label_text, rec):
                continue
            if sc > best_score:
                best_score = sc
                best_id = rid
    return best_id


def item_labels(item: dict) -> tuple[str | None, str | None, str]:
    from_l = item.get("from") or item.get("from_label")
    to_l = item.get("to") or item.get("to_label")
    label = item.get("label") or (f"{from_l} → {to_l}" if from_l or to_l else "")
    return from_l, to_l, label


def is_geometry_pending(item: dict) -> bool:
    if item.get("display") == "text_only" or item.get("flag") == "network-chip-text-only":
        return True
    st = str(item.get("_link_status") or "")
    if "aspirational" in st.lower() or "null-geometry-pending" in st.lower():
        return True
    if item.get("flag") == "aspirational-no-built-route":
        return True
    return False


def relink_item(
    item: dict,
    scope: set[str],
    routes: dict[str, RouteRec],
    routes_by_city: dict[str, list[str]],
    brief_idx: BriefRouteIndex,
    stats: LinkStats,
    *,
    partner_slug: str | None = None,
    force: bool = True,
) -> None:
    if not isinstance(item, dict):
        return
    stats.total += 1

    for key in ("from_node_id", "to_node_id", "from_node", "to_node"):
        if item.get(key):
            item[key] = crosswalk_node(item[key])

    if is_geometry_pending(item) and item.get("display") == "text_only":
        stats.geometry_pending += 1
        return

    from_l, to_l, label_text = item_labels(item)
    old_rid = item.get("route_id")

    # Clear mis-linked or absent ids when force-relinking
    if old_rid:
        rec = routes.get(old_rid)
        if not rec or not passes_gates(item, rec, label_text):
            item["route_id"] = None
            if item.get("route_ids"):
                item["route_ids"] = None
            stats.cleared_mislink += 1
            old_rid = None

    if old_rid and not force:
        stats.linked += 1
        return

    rid: str | None = None
    source = ""

    rid = borrow_from_brief(item, scope, brief_idx, routes, partner_slug)
    if rid:
        source = "brief"
    if not rid:
        rid = find_scoped_route(item, scope, routes, routes_by_city, partner_slug)
        if rid:
            source = "scoped"
    if not rid:
        rid = find_node_pair_route(item, routes, routes_by_city, scope)
        if rid:
            source = "node"

    if rid:
        rec = routes[rid]
        if rec.distance_nm is not None:
            item["distance_nm"] = rec.distance_nm
        item["route_id"] = rid
        item["_link_kind"] = "corridor-label" if (from_l or item.get("label")) else "corridor-node"
        item["_link_status"] = f"linked-grok-{source}"
        item["_link_source"] = f"grok/relink_partner_journeys/{source}"
        stats.linked += 1
        if source == "brief":
            stats.borrowed_brief += 1
        elif source == "scoped":
            stats.matched_scoped += 1
        elif source == "node":
            stats.matched_node += 1
    else:
        item["route_id"] = None
        if from_l and to_l:
            fn = item.get("from_node_id") or item.get("from_node")
            tn = item.get("to_node_id") or item.get("to_node")
            if fn and tn and fn == tn:
                item["_link_status"] = "unlinked-intra-city"
                stats.geometry_pending += 1
            else:
                item["_link_status"] = "unlinked-no-route"
                stats.still_null += 1
        elif (item.get("from_node_id") or item.get("from_node")) == (
            item.get("to_node_id") or item.get("to_node")
        ):
            item["_link_status"] = "unlinked-intra-city"
            stats.geometry_pending += 1
        else:
            item["_link_status"] = "unlinked-no-route"
            stats.still_null += 1


def market_scope(
    market: dict,
    city_ids: set[str],
    locale_parents: dict[str, str],
) -> set[str]:
    scope: set[str] = set()
    for c in resolve_phase_cities(market.get("anchor_cities"), city_ids):
        scope.add(c)
    for ph in market.get("phases") or []:
        for c in resolve_phase_cities(ph.get("cities"), city_ids):
            scope.add(c)
    for j in market.get("journeys_unlocked") or []:
        for key in ("from_node_id", "to_node_id"):
            cid = city_id_of(j.get(key), city_ids, locale_parents)
            if cid:
                scope.add(cid)
    return expand_scope(scope)


def hub_scope(partner: dict, city_ids: set[str], locale_parents: dict[str, str]) -> set[str]:
    scope: set[str] = set()
    for ph in partner.get("phases") or []:
        for c in resolve_phase_cities(ph.get("cities"), city_ids):
            scope.add(c)
    for j in partner.get("journeys_unlocked") or []:
        for key in ("from_node_id", "to_node_id"):
            cid = city_id_of(j.get(key), city_ids, locale_parents)
            if cid:
                scope.add(cid)
    for m in partner.get("markets") or []:
        scope.update(market_scope(m, city_ids, locale_parents))
    return expand_scope(scope)


def walk_partner(
    partner: dict,
    partner_slug: str,
    routes: dict[str, RouteRec],
    routes_by_city: dict[str, list[str]],
    brief_idx: BriefRouteIndex,
    city_ids: set[str],
    locale_parents: dict[str, str],
    stats: LinkStats,
    *,
    hub_scope_set: set[str] | None = None,
):
    if hub_scope_set is None:
        hub_scope_set = hub_scope(partner, city_ids, locale_parents)

    for j in partner.get("journeys_unlocked") or []:
        relink_item(j, hub_scope_set, routes, routes_by_city, brief_idx, stats, partner_slug=partner_slug)

    for ph in partner.get("phases") or []:
        ph_scope = expand_scope(
            set(resolve_phase_cities(ph.get("cities"), city_ids)) or set(hub_scope_set)
        )
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, str):
                continue
            relink_item(fr, ph_scope, routes, routes_by_city, brief_idx, stats, partner_slug=partner_slug)

    for m in partner.get("markets") or []:
        m_scope = market_scope(m, city_ids, locale_parents) or hub_scope_set
        for j in m.get("journeys_unlocked") or []:
            relink_item(j, m_scope, routes, routes_by_city, brief_idx, stats, partner_slug=partner_slug)
        for ph in m.get("phases") or []:
            ph_scope = expand_scope(
                set(resolve_phase_cities(ph.get("cities"), city_ids)) or set(m_scope)
            )
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, str):
                    continue
                relink_item(fr, ph_scope, routes, routes_by_city, brief_idx, stats, partner_slug=partner_slug)


def render_bucket(item: dict, routes: dict[str, RouteRec]) -> str:
    if is_geometry_pending(item):
        return "geometry_pending"
    rid = item.get("route_id")
    if not rid:
        fn = item.get("from_node_id")
        tn = item.get("to_node_id")
        if fn and tn:
            return "clickable_city_fallback"
        return "no_link"
    rec = routes.get(rid)
    if not rec:
        return "route_id_not_in_graph"
    from_l, to_l, label_text = item_labels(item)
    if not passes_gates(item, rec, label_text):
        return "mislinked_dropped"
    return "clickable_route"


def audit_partner(partner: dict, partner_id: str, routes: dict[str, RouteRec]) -> dict:
    buckets: dict[str, int] = defaultdict(int)

    def count_item(item: dict):
        if isinstance(item, str):
            return
        buckets[render_bucket(item, routes)] += 1

    def walk(obj: dict):
        for j in obj.get("journeys_unlocked") or []:
            count_item(j)
        for ph in obj.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                count_item(fr)
        for m in obj.get("markets") or []:
            walk(m)

    walk(partner)
    return dict(buckets)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", nargs="*", help="Limit to partner slug(s)")
    args = ap.parse_args()
    if not args.audit and not args.apply:
        args.audit = True

    fbt = load_json(ROOT / "data-clean/FEATURES_BY_TYPE.json")
    city_ids = build_city_ids(fbt)
    locale_parents = build_locale_parents(fbt)
    routes, routes_by_city = load_routes(ROOT)
    brief_idx = load_brief_index(ROOT)

    partner_dir = ROOT / "data-clean/partners"
    slugs = args.partner or sorted(p.stem for p in partner_dir.glob("*.json"))

    totals_before: dict[str, int] = defaultdict(int)
    totals_after: dict[str, int] = defaultdict(int)
    all_stats = LinkStats()

    for slug in slugs:
        path = partner_dir / f"{slug}.json"
        if not path.exists():
            print(f"skip {slug}: missing", file=sys.stderr)
            continue
        partner = load_json(path)

        if args.audit:
            b = audit_partner(partner, slug, routes)
            for k, v in b.items():
                totals_before[k] += v
            continue

        before = audit_partner(partner, slug, routes)
        for k, v in before.items():
            totals_before[k] += v

        stats = LinkStats()
        walk_partner(partner, slug, routes, routes_by_city, brief_idx, city_ids, locale_parents, stats)
        all_stats.total += stats.total
        all_stats.linked += stats.linked
        all_stats.cleared_mislink += stats.cleared_mislink
        all_stats.borrowed_brief += stats.borrowed_brief
        all_stats.matched_scoped += stats.matched_scoped
        all_stats.matched_node += stats.matched_node
        all_stats.still_null += stats.still_null
        all_stats.geometry_pending += stats.geometry_pending

        partner.setdefault("_provenance", {})
        if isinstance(partner["_provenance"], dict):
            partner["_provenance"]["journey_relink"] = {
                "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "lane": "grok/relink_partner_journeys",
                "stats": {
                    "total": stats.total,
                    "linked": stats.linked,
                    "cleared_mislink": stats.cleared_mislink,
                    "borrowed_brief": stats.borrowed_brief,
                    "matched_scoped": stats.matched_scoped,
                },
            }

        save_json(path, partner)
        pitch = ROOT / "partner-pitch/partners" / f"{slug}.json"
        if pitch.parent.exists():
            save_json(pitch, partner)

        after = audit_partner(partner, slug, routes)
        for k, v in after.items():
            totals_after[k] += v
        print(
            f"  ✓ {slug}: linked {stats.linked}/{stats.total} "
            f"(brief {stats.borrowed_brief}, scoped {stats.matched_scoped}, "
            f"cleared {stats.cleared_mislink}) "
            f"clickable {before.get('clickable_route',0)}→{after.get('clickable_route',0)} "
            f"mislink {before.get('mislinked_dropped',0)}→{after.get('mislinked_dropped',0)}"
        )

    print("\n=== Render buckets (journeys + featured_routes) ===")
    if args.apply:
        print("BEFORE:", dict(sorted(totals_before.items(), key=lambda x: -x[1])))
        print("AFTER: ", dict(sorted(totals_after.items(), key=lambda x: -x[1])))
        print(
            f"\nRelink: {all_stats.linked}/{all_stats.total} linked, "
            f"{all_stats.cleared_mislink} cleared, "
            f"{all_stats.borrowed_brief} from briefs, {all_stats.matched_scoped} scoped"
        )
    else:
        print(dict(sorted(totals_before.items(), key=lambda x: -x[1])))


if __name__ == "__main__":
    main()