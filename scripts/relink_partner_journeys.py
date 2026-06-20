#!/usr/bin/env python3
"""
Grok-led re-linker for partner journeys_unlocked + featured_routes.

City-brief-grade binding: scope candidates to market/phase cities, borrow sealed
signature_routes from city/cluster briefs, two-gate match (distance ±25%, endpoint
tokens). Null beats wrong — clears mis-linked route_ids before re-binding.

Precision lanes (all partners / phase carousels):
  A. network_chip — auto-fill route_ids[] from scoped legs matching bundle tokens
  B. brief inheritance — cluster labels (Bali ↔ Lombok ↔ Komodo) → brief signature_routes
  C. best-of-N — traffic_weight + economics tie-break when multiple routes pass gates
  D. gcn promote — visible gcn-*-{partner} over quarantined rn-* copies

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
        "islands", "palm", "jumeirah", "experience", "resort",
        "central", "downtown", "city", "gulf", "creek",
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
    traffic_weight: float | None = None


@dataclass
class GcnPromoIndex:
    """Maps quarantined rn-* (or endpoint pairs) to visible gcn-*-{partner}."""
    by_rn: dict[str, dict[str, str]] = field(default_factory=dict)
    by_endpoints: dict[tuple[str, str], dict[str, str]] = field(default_factory=dict)


@dataclass
class EconomicsIndex:
    all_ids: set[str] = field(default_factory=set)
    by_partner: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    corridor_by_route: dict[str, str] = field(default_factory=dict)
    corridor_by_partner_route: dict[tuple[str, str], str] = field(default_factory=dict)


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
    network_chip: int = 0
    brief_cluster: int = 0
    gcn_promoted: int = 0
    still_null: int = 0
    geometry_pending: int = 0


# Bundle label segment separators (Grab hub chips, resort meshes, etc.)
_BUNDLE_SPLIT = re.compile(r"\s*(?:↔|↔|<->|/|—|–|&|,|\+|\band\b)\s*", re.I)


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


def _route_rec_from_props(p: dict) -> RouteRec | None:
    rid = p.get("id")
    if not rid:
        return None
    tw = p.get("traffic_weight")
    return RouteRec(
        id=rid,
        from_label=p.get("from_label") or p.get("from") or "",
        to_label=p.get("to_label") or p.get("to") or "",
        from_city_id=p.get("from_city_id"),
        to_city_id=p.get("to_city_id"),
        from_node=p.get("from"),
        to_node=p.get("to"),
        distance_nm=p.get("distance_nm"),
        edge_class=p.get("edge_class"),
        traffic_weight=float(tw) if tw is not None else None,
    )


def load_routes(root: Path) -> tuple[dict[str, RouteRec], dict[str, list[str]], GcnPromoIndex]:
    raw = load_json(root / "data-clean/ROUTES.json")
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    by_id: dict[str, RouteRec] = {}
    by_city: dict[str, list[str]] = defaultdict(list)
    promo = GcnPromoIndex()
    visible_gcn: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)

    for f in feats:
        p = f.get("properties") or {}
        rec = _route_rec_from_props(p)
        if not rec:
            continue
        rid = rec.id
        key = (rec.from_node or "", rec.to_node or "")
        if route_visible(p):
            by_id[rid] = rec
            for cid in (rec.from_city_id, rec.to_city_id):
                if cid:
                    by_city[cid].append(rid)
            if rid.startswith("gcn-") and key[0] and key[1]:
                slug = rid.rsplit("-", 1)[-1] if "-" in rid else ""
                visible_gcn[key].append((slug, rid))

    # Map every rn-* (quarantined or visible) with a partner gcn twin on same endpoints.
    for f in feats:
        p = f.get("properties") or {}
        rid = p.get("id")
        if not rid or not rid.startswith("rn-"):
            continue
        key = (p.get("from") or "", p.get("to") or "")
        if not key[0] or not key[1]:
            continue
        for slug, gcn_id in visible_gcn.get(key, []):
            promo.by_rn.setdefault(rid, {})[slug] = gcn_id
            promo.by_endpoints.setdefault(key, {})[slug] = gcn_id

    return by_id, by_city, promo


def load_economics_index(root: Path) -> EconomicsIndex:
    path = root / "data-clean/economics_by_route_id.json"
    idx = EconomicsIndex()
    if not path.exists():
        return idx
    raw = load_json(path)
    for rec in raw.get("records") or []:
        rid = rec.get("route_id")
        if not rid:
            continue
        idx.all_ids.add(rid)
        partner = str(rec.get("partner") or "").lower()
        corridor = rec.get("corridor") or ""
        if corridor:
            idx.corridor_by_route[rid] = corridor
            if partner:
                idx.corridor_by_partner_route[(partner, rid)] = corridor
        if partner:
            idx.by_partner[partner].add(rid)
    return idx


def econ_corridor_score(
    item: dict,
    rid: str,
    partner_slug: str | None,
    econ: EconomicsIndex,
) -> float:
    """Lane C: economics corridor text as tie-break for generic long-haul labels."""
    slug = (partner_slug or "").lower()
    corridor = econ.corridor_by_partner_route.get((slug, rid)) or econ.corridor_by_route.get(rid)
    if not corridor:
        return 0.0
    from_l, to_l, label = item_labels(item)
    label_n = norm_label(label or f"{from_l} → {to_l}")
    corr_n = norm_label(corridor.replace("->", " ").replace("→", " "))
    if not label_n or not corr_n:
        return 0.0
    if label_n == corr_n or label_n in corr_n or corr_n in label_n:
        return 8.0
    anchors = [a for a in _anchor_tokens(label) if a in corr_n]
    if anchors:
        return 10.0 + len(anchors)
    lt = _tokens(label)
    ct = _tokens(corridor)
    overlap = lt & ct
    if len(overlap) >= max(2, min(len(lt), len(ct)) // 2):
        return 6.0
    return 0.0


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


def partner_route_ok(rid: str, partner_slug: str | None) -> bool:
    slug = (partner_slug or "").lower()
    if not slug:
        return True
    if rid.startswith("gcn-") and not rid.endswith(f"-{slug}"):
        return False
    return True


def promote_route_id(
    rid: str | None,
    partner_slug: str | None,
    promo: GcnPromoIndex,
    routes: dict[str, RouteRec],
) -> str | None:
    if not rid:
        return None
    slug = (partner_slug or "").lower()
    # Quarantined rn-* → visible partner gcn copy
    if slug and rid in promo.by_rn:
        gcn = promo.by_rn[rid].get(slug)
        if gcn and gcn in routes:
            return gcn
    # Visible rn-* → prefer partner gcn when minted for same endpoints
    if slug and rid.startswith("rn-") and rid in promo.by_rn:
        gcn = promo.by_rn[rid].get(slug)
        if gcn and gcn in routes:
            return gcn
    if rid in routes:
        return rid
    return None


def candidate_rank(
    rid: str,
    rec: RouteRec,
    match_score: float,
    partner_slug: str | None,
    econ: EconomicsIndex,
) -> tuple:
    """Lane C tie-break: economics > traffic_weight > match score > partner gcn."""
    slug = (partner_slug or "").lower()
    has_econ = rid in econ.all_ids or (slug and rid in econ.by_partner.get(slug, set()))
    tw = rec.traffic_weight if rec.traffic_weight is not None else -1.0
    partner_gcn = bool(slug and rid.endswith(f"-{slug}"))
    is_gcn = rid.startswith("gcn-")
    return (has_econ, tw, match_score, partner_gcn, is_gcn)


def pick_best_rid(
    candidates: list[tuple[str, float]],
    routes: dict[str, RouteRec],
    partner_slug: str | None,
    econ: EconomicsIndex,
    promo: GcnPromoIndex,
) -> str | None:
    if not candidates:
        return None
    ranked: list[tuple[tuple, str]] = []
    for rid, score in candidates:
        promoted = promote_route_id(rid, partner_slug, promo, routes) or rid
        rec = routes.get(promoted)
        if not rec:
            continue
        ranked.append((candidate_rank(promoted, rec, score, partner_slug, econ), promoted))
    if not ranked:
        return None
    return max(ranked, key=lambda x: x[0])[1]


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
    econ: EconomicsIndex | None = None,
    promo: GcnPromoIndex | None = None,
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

    passing: list[tuple[str, float]] = []
    for rid in dict.fromkeys(candidates):
        promoted = promote_route_id(rid, partner_slug, promo or GcnPromoIndex(), routes) or rid
        if promoted not in routes:
            continue
        rec = routes[promoted]
        if not route_in_scope(rec, scope):
            continue
        if not from_l or not to_l:
            continue
        trial = dict(item)
        if rec.distance_nm is not None:
            trial["distance_nm"] = rec.distance_nm
        if not passes_gates(trial, rec, label_text):
            continue
        sc = score_route_match(from_l, to_l, rec, item.get("distance_nm"), partner_slug)
        sc = max(sc, econ_corridor_score(item, promoted, partner_slug, econ or EconomicsIndex()))
        if sc <= 0.0:
            continue
        passing.append((promoted, sc))
    return pick_best_rid(passing, routes, partner_slug, econ or EconomicsIndex(), promo or GcnPromoIndex())


def find_scoped_route(
    item: dict,
    scope: set[str],
    routes: dict[str, RouteRec],
    routes_by_city: dict[str, list[str]],
    partner_slug: str | None = None,
    econ: EconomicsIndex | None = None,
    promo: GcnPromoIndex | None = None,
) -> str | None:
    from_l = item.get("from") or item.get("from_label")
    to_l = item.get("to") or item.get("to_label")
    label_text = item.get("label") or f"{from_l or ''} {to_l or ''}"
    label_nm = item.get("distance_nm")

    candidates: set[str] = set()
    for cid in scope:
        candidates.update(routes_by_city.get(cid, []))

    econ = econ or EconomicsIndex()
    passing: list[tuple[str, float]] = []
    for rid in candidates:
        promoted = promote_route_id(rid, partner_slug, promo or GcnPromoIndex(), routes) or rid
        if not partner_route_ok(promoted, partner_slug):
            continue
        rec = routes.get(promoted)
        if not rec or not route_in_scope(rec, scope):
            continue
        trial = dict(item)
        if rec.distance_nm is not None:
            trial["distance_nm"] = rec.distance_nm
        if not passes_gates(trial, rec, label_text):
            continue
        score_nm = rec.distance_nm if rec.distance_nm is not None else label_nm
        sc = score_route_match(from_l, to_l, rec, score_nm, partner_slug)
        sc = max(sc, econ_corridor_score(item, promoted, partner_slug, econ))
        if sc <= 0.0:
            continue
        passing.append((promoted, sc))
    best = pick_best_rid(passing, routes, partner_slug, econ, promo or GcnPromoIndex())
    return best if best else None


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


def bundle_segments(label: str | None) -> list[str]:
    if not label:
        return []
    parts = [p.strip() for p in _BUNDLE_SPLIT.split(label) if p.strip()]
    return parts or [label.strip()]


def bundle_tokens(label: str | None) -> set[str]:
    toks: set[str] = set()
    for seg in bundle_segments(label):
        toks |= _place_toks(seg)
        toks |= {t for t in _tokens(seg) if len(t) >= 4 and t not in _GEO_STOP}
    return toks


def resolve_place_to_cities(place: str, scope: set[str]) -> list[str]:
    place_n = norm_label(place)
    if not place_n:
        return []
    slug = crosswalk_node(place_n.replace(" ", "-")) or place_n.replace(" ", "-")
    out: list[str] = []
    for cid in scope:
        a = cid.lower()
        if place_n in a or slug in a:
            out.append(cid)
            continue
        for tok in _tokens(place):
            if len(tok) >= 3 and tok in a.replace("_", "-").split("-"):
                out.append(cid)
    return list(dict.fromkeys(out))


def route_matches_bundle(rec: RouteRec, tokens: set[str]) -> bool:
    if not tokens:
        return False
    ep = _place_toks(rec.from_label) | _place_toks(rec.to_label)
    ep |= {t for t in _tokens(rec.from_label + " " + rec.to_label) if len(t) >= 4}
    overlap = tokens & ep
    if len(overlap) >= 2:
        return True
    anchors = [t for t in tokens if len(t) >= 5 and t not in _COMMON_PLACE]
    if anchors and any(a in norm_label(rec.from_label + " " + rec.to_label) for a in anchors):
        return True
    return len(overlap) >= 1 and any(len(t) >= 6 for t in overlap)


def inherit_cluster_route_ids(
    item: dict,
    scope: set[str],
    brief_idx: BriefRouteIndex,
    routes: dict[str, RouteRec],
    partner_slug: str | None,
    promo: GcnPromoIndex,
    econ: EconomicsIndex,
) -> list[str]:
    """Lane B: multi-place cluster labels → constituent brief signature_routes."""
    label = item.get("label") or ""
    segments = bundle_segments(label)
    if len(segments) < 2:
        return []
    city_hits: set[str] = set()
    for seg in segments:
        city_hits.update(resolve_place_to_cities(seg, scope))
    if len(city_hits) < 2:
        return []

    candidates: list[tuple[str, float]] = []
    for city in city_hits:
        for _nl, br_rid in brief_idx.by_city.get(city, []):
            promoted = promote_route_id(br_rid, partner_slug, promo, routes) or br_rid
            if promoted not in routes:
                continue
            rec = routes[promoted]
            if not route_in_scope(rec, scope):
                continue
            sc = (rec.traffic_weight or 0.0) + (3.0 if promoted in econ.all_ids else 0.0)
            candidates.append((promoted, sc))

    if not candidates:
        return []
    by_rid: dict[str, float] = {}
    for rid, sc in candidates:
        by_rid[rid] = max(by_rid.get(rid, 0.0), sc)
    ranked = sorted(by_rid.items(), key=lambda x: -x[1])
    return [rid for rid, _ in ranked]


def expand_network_chip_route_ids(
    item: dict,
    scope: set[str],
    routes: dict[str, RouteRec],
    routes_by_city: dict[str, list[str]],
    partner_slug: str | None,
    promo: GcnPromoIndex,
    econ: EconomicsIndex,
) -> list[str]:
    """Lane A: network_chip bundle → all scoped legs matching label tokens."""
    label = item.get("label") or ""
    tokens = bundle_tokens(label)
    if not tokens:
        return []

    chip_nm = item.get("distance_nm")
    candidates: set[str] = set()
    for cid in scope:
        candidates.update(routes_by_city.get(cid, []))

    passing: list[tuple[str, float]] = []
    for rid in candidates:
        promoted = promote_route_id(rid, partner_slug, promo, routes) or rid
        rec = routes.get(promoted)
        if not rec or not route_in_scope(rec, scope):
            continue
        if not route_matches_bundle(rec, tokens):
            continue
        if chip_nm is not None and rec.distance_nm is not None:
            if abs(rec.distance_nm - chip_nm) / max(chip_nm, 1.0) > 0.5:
                continue
        tw = rec.traffic_weight or 0.0
        sc = tw + (2.0 if promoted in econ.all_ids else 0.0)
        passing.append((promoted, sc))

    if not passing:
        return []
    passing.sort(key=lambda x: -x[1])
    return list(dict.fromkeys(rid for rid, _ in passing))


def relink_network_chip(
    item: dict,
    scope: set[str],
    routes: dict[str, RouteRec],
    routes_by_city: dict[str, list[str]],
    brief_idx: BriefRouteIndex,
    stats: LinkStats,
    *,
    partner_slug: str | None = None,
    promo: GcnPromoIndex | None = None,
    econ: EconomicsIndex | None = None,
) -> None:
    promo = promo or GcnPromoIndex()
    econ = econ or EconomicsIndex()
    stats.total += 1

    old_ids = list(item.get("route_ids") or [])
    if item.get("route_id"):
        item["route_id"] = None
        stats.cleared_mislink += 1

    rids = inherit_cluster_route_ids(item, scope, brief_idx, routes, partner_slug, promo, econ)
    source = "brief-cluster"
    if not rids:
        rids = expand_network_chip_route_ids(
            item, scope, routes, routes_by_city, partner_slug, promo, econ
        )
        source = "network-chip"

    if rids:
        promoted_ids: list[str] = []
        for rid in rids:
            p = promote_route_id(rid, partner_slug, promo, routes) or rid
            if p in routes:
                if p != rid:
                    stats.gcn_promoted += 1
                promoted_ids.append(p)
        rids = list(dict.fromkeys(promoted_ids))
        item["route_ids"] = rids
        item["route_id"] = None
        item["_link_kind"] = "network-bundle"
        item["_link_status"] = f"linked-grok-{source}"
        item["_link_source"] = f"grok/relink_partner_journeys/{source}"
        stats.linked += 1
        if source == "brief-cluster":
            stats.brief_cluster += 1
        else:
            stats.network_chip += 1
    else:
        item["route_ids"] = None
        item["route_id"] = None
        fn = item.get("from_node_id") or item.get("from_node")
        tn = item.get("to_node_id") or item.get("to_node")
        if fn and tn and fn == tn:
            item["_link_status"] = "unlinked-intra-city"
            stats.geometry_pending += 1
        else:
            item["_link_status"] = "unlinked-no-bundle"
            stats.still_null += 1


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
    promo: GcnPromoIndex | None = None,
    econ: EconomicsIndex | None = None,
) -> None:
    if not isinstance(item, dict):
        return

    for key in ("from_node_id", "to_node_id", "from_node", "to_node"):
        if item.get(key):
            item[key] = crosswalk_node(item[key])

    if item.get("display") == "network_chip":
        relink_network_chip(
            item, scope, routes, routes_by_city, brief_idx, stats,
            partner_slug=partner_slug, promo=promo, econ=econ,
        )
        return

    stats.total += 1

    if is_geometry_pending(item) and item.get("display") == "text_only":
        stats.geometry_pending += 1
        return

    from_l, to_l, label_text = item_labels(item)
    old_rid = item.get("route_id")
    promo = promo or GcnPromoIndex()
    econ = econ or EconomicsIndex()

    # Lane D: promote existing rn-* to partner gcn before gate check
    if old_rid:
        promoted = promote_route_id(old_rid, partner_slug, promo, routes)
        if promoted and promoted != old_rid:
            old_rid = promoted
            item["route_id"] = promoted
            stats.gcn_promoted += 1

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

    rid = borrow_from_brief(item, scope, brief_idx, routes, partner_slug, econ, promo)
    if rid:
        source = "brief"
    if not rid:
        rid = find_scoped_route(item, scope, routes, routes_by_city, partner_slug, econ, promo)
        if rid:
            source = "scoped"
    if not rid:
        rid = find_node_pair_route(item, routes, routes_by_city, scope)
        if rid:
            rid = promote_route_id(rid, partner_slug, promo, routes) or rid
            source = "node"

    if rid:
        if rid != item.get("route_id"):
            promoted = promote_route_id(rid, partner_slug, promo, routes)
            if promoted and promoted != rid:
                stats.gcn_promoted += 1
                rid = promoted
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
    promo: GcnPromoIndex | None = None,
    econ: EconomicsIndex | None = None,
):
    if hub_scope_set is None:
        hub_scope_set = hub_scope(partner, city_ids, locale_parents)

    kw = {"partner_slug": partner_slug, "promo": promo, "econ": econ}

    for j in partner.get("journeys_unlocked") or []:
        relink_item(j, hub_scope_set, routes, routes_by_city, brief_idx, stats, **kw)

    for ph in partner.get("phases") or []:
        ph_scope = expand_scope(
            set(resolve_phase_cities(ph.get("cities"), city_ids)) or set(hub_scope_set)
        )
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, str):
                continue
            relink_item(fr, ph_scope, routes, routes_by_city, brief_idx, stats, **kw)

    for m in partner.get("markets") or []:
        m_scope = market_scope(m, city_ids, locale_parents) or hub_scope_set
        for j in m.get("journeys_unlocked") or []:
            relink_item(j, m_scope, routes, routes_by_city, brief_idx, stats, **kw)
        for ph in m.get("phases") or []:
            ph_scope = expand_scope(
                set(resolve_phase_cities(ph.get("cities"), city_ids)) or set(m_scope)
            )
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, str):
                    continue
                relink_item(fr, ph_scope, routes, routes_by_city, brief_idx, stats, **kw)


def render_bucket(item: dict, routes: dict[str, RouteRec]) -> str:
    if is_geometry_pending(item):
        return "geometry_pending"

    bundle_ids = [
        r for r in (item.get("route_ids") or [])
        if r and r in routes
    ]
    if item.get("display") == "network_chip" and bundle_ids:
        return "clickable_route_bundle"

    rid = item.get("route_id")
    if not rid:
        if bundle_ids:
            return "clickable_route_bundle"
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
    routes, routes_by_city, promo = load_routes(ROOT)
    brief_idx = load_brief_index(ROOT)
    econ = load_economics_index(ROOT)

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
        walk_partner(
            partner, slug, routes, routes_by_city, brief_idx, city_ids, locale_parents, stats,
            promo=promo, econ=econ,
        )
        all_stats.total += stats.total
        all_stats.linked += stats.linked
        all_stats.cleared_mislink += stats.cleared_mislink
        all_stats.borrowed_brief += stats.borrowed_brief
        all_stats.matched_scoped += stats.matched_scoped
        all_stats.matched_node += stats.matched_node
        all_stats.network_chip += stats.network_chip
        all_stats.brief_cluster += stats.brief_cluster
        all_stats.gcn_promoted += stats.gcn_promoted
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
                    "network_chip": stats.network_chip,
                    "brief_cluster": stats.brief_cluster,
                    "gcn_promoted": stats.gcn_promoted,
                },
            }

        save_json(path, partner)
        pitch = ROOT / "partner-pitch/partners" / f"{slug}.json"
        if pitch.parent.exists():
            save_json(pitch, partner)

        after = audit_partner(partner, slug, routes)
        for k, v in after.items():
            totals_after[k] += v
        bundle_after = after.get("clickable_route_bundle", 0)
        print(
            f"  ✓ {slug}: linked {stats.linked}/{stats.total} "
            f"(brief {stats.borrowed_brief}, scoped {stats.matched_scoped}, "
            f"chip {stats.network_chip}, cluster {stats.brief_cluster}, "
            f"gcn {stats.gcn_promoted}, cleared {stats.cleared_mislink}) "
            f"clickable {before.get('clickable_route',0)}→{after.get('clickable_route',0)} "
            f"bundle {before.get('clickable_route_bundle',0)}→{bundle_after} "
            f"mislink {before.get('mislinked_dropped',0)}→{after.get('mislinked_dropped',0)}"
        )

    print("\n=== Render buckets (journeys + featured_routes) ===")
    if args.apply:
        print("BEFORE:", dict(sorted(totals_before.items(), key=lambda x: -x[1])))
        print("AFTER: ", dict(sorted(totals_after.items(), key=lambda x: -x[1])))
        print(
            f"\nRelink: {all_stats.linked}/{all_stats.total} linked, "
            f"{all_stats.cleared_mislink} cleared, "
            f"{all_stats.borrowed_brief} from briefs, {all_stats.matched_scoped} scoped, "
            f"{all_stats.network_chip} network_chip, {all_stats.brief_cluster} brief_cluster, "
            f"{all_stats.gcn_promoted} gcn_promoted"
        )
    else:
        print(dict(sorted(totals_before.items(), key=lambda x: -x[1])))


if __name__ == "__main__":
    main()