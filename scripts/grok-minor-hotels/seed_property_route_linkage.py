#!/usr/bin/env python3
"""Seed Minor Hotels journeys + phase featured_routes from property-touched atlas geometry.

Hospitality rule: every linked route must touch at least one Minor property
(gateway→property, property→property, or property-originated excursion).

Usage:
  python3 scripts/grok-minor-hotels/seed_property_route_linkage.py --apply
  python3 scripts/grok-minor-hotels/seed_property_route_linkage.py --apply --partner minor-hotels
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-minor-hotels"))

from minor_shared import PARTNER_DST, PARTNER_SRC, load_binds, load_json  # noqa: E402

ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
MAX_JOURNEYS_PER_MARKET = 12
INVENTORY_PATH = ROOT / "handoff/partner-map-model/minor-hotels-seal-2026-06-22/inputs/inventory/minor-hotels-property-inventory.json"

MARKET_CLUSTER_ALIASES: dict[str, list[str]] = {
    "thailand-gulf": ["thailand"],
    "med-europe": ["mediterranean-europe"],
    "mozambique": ["mozambique"],
    "americas-coastal": ["brazil", "americas", "americas-coastal"],
    "vietnam-coastal": ["vietnam"],
    "sri-lanka": ["sri-lanka"],
    "australia-coastal": ["australia"],
    "gulf-singletons": ["oman", "qatar", "seychelles", "malaysia"],
}

_PROPERTY_STOP = frozenset({
    "anantara", "avani", "resort", "resorts", "hotel", "hotels", "villas", "villa",
    "the", "by", "maldives", "private", "islands", "island", "collection", "suites",
    "coast", "beach", "and", "at", "de", "di", "del", "dubai", "bali", "thailand",
    "minor", "oaks", "tivoli", "elewana", "reserve", "plus", "beachfront", "jetty",
    "pier", "marina", "lagoon", "world", "view", "palms", "palm",
})

_GATEWAY_WORDS = frozenset({
    "airport", "velana", "seaplane", "marina", "harbour", "harbor", "pier", "port",
    "terminal", "doha", "phuket", "benoa", "sanur", "dubai", "harbour", "rassada",
})


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(s: str | None) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def property_needles(name: str) -> list[str]:
    toks = [t for t in norm(name).split() if len(t) > 3 and t not in _PROPERTY_STOP]
    return toks[:4] if toks else [t for t in norm(name).split() if len(t) > 2][:2]


def label_hits_property(label: str, property_name: str) -> bool:
    lab = norm(label)
    needles = property_needles(property_name)
    if not needles:
        return norm(property_name)[:12] in lab
    hits = sum(1 for n in needles if n in lab)
    return hits >= min(2, len(needles)) or (len(needles) == 1 and hits == 1)


def route_props(feat: dict) -> dict:
    return feat.get("properties", feat)


def load_routes() -> list[dict]:
    raw = load_json(ROUTES_PATH)
    return raw if isinstance(raw, list) else raw.get("features", [])


def load_inventory_properties() -> list[dict]:
    if not INVENTORY_PATH.exists():
        return []
    doc = load_json(INVENTORY_PATH)
    return [p for p in doc.get("properties") or [] if p.get("coastal_relevant")]


def properties_for_market(market: dict, binds: list[dict], inventory: list[dict]) -> list[dict]:
    cities = set(market.get("anchor_cities") or [])
    slug = market.get("slug") or market.get("id") or ""
    clusters = set(MARKET_CLUSTER_ALIASES.get(slug, [slug.replace("-", "_")]))
    out: list[dict] = []
    seen: set[str] = set()

    def add(row: dict) -> None:
        name = row.get("property_name") or ""
        if name and name not in seen:
            seen.add(name)
            out.append(row)

    for b in binds:
        key = b.get("atlas_registry_key")
        cluster = b.get("cluster") or b.get("atlas_cluster_id")
        if key and key in cities:
            add(b)
        elif cluster and cluster in clusters:
            add(b)

    for row in inventory:
        cluster = row.get("cluster") or ""
        if cluster in clusters:
            add({
                "property_name": row.get("property_name"),
                "route_archetype": row.get("navier_route_archetype"),
                "atlas_registry_key": None,
                "cluster": cluster,
            })
    return out


def route_touches_portfolio(route: dict, properties: list[dict]) -> tuple[bool, str | None, str | None]:
    p = route_props(route)
    fl = p.get("from_label") or p.get("label") or ""
    tl = p.get("to_label") or ""
    from_prop = to_prop = None
    for prop in properties:
        name = prop.get("property_name") or ""
        if label_hits_property(fl, name):
            from_prop = name
        if label_hits_property(tl, name):
            to_prop = name
    if from_prop or to_prop:
        return True, from_prop, to_prop
    if p.get("_minor_hotels_tier1_sealed") or p.get("_minor_route_class"):
        return True, None, None
    return False, None, None


def journey_from_route(route: dict, *, from_prop: str | None, to_prop: str | None) -> dict:
    p = route_props(route)
    rid = p.get("id")
    fl, tl = p.get("from_label") or p.get("from"), p.get("to_label") or p.get("to")
    if from_prop and to_prop and from_prop != to_prop:
        title_from, title_to = from_prop, to_prop
        rclass = "B"
    elif to_prop:
        title_from, title_to = fl or "Gateway", to_prop
        rclass = "A"
    elif from_prop:
        title_from, title_to = from_prop, tl or "Destination"
        rclass = "C"
    else:
        title_from, title_to = fl, tl
        rclass = p.get("_minor_route_class") or "A"
    return {
        "from": title_from,
        "to": title_to,
        "today": "A diesel resort speedboat or outsourced launch — weather-bound, loud, third-party-operated.",
        "with_navier": "A silent captive foiling transfer on Minor's branded electric fleet — resort-controlled schedule.",
        "distance_nm": p.get("distance_nm"),
        "platform": p.get("platform") or "Pioneer II",
        "archetype": "tourism",
        "_route_class": rclass,
        "from_node_id": p.get("from_city_id") or p.get("from"),
        "to_node_id": p.get("to_city_id") or p.get("to"),
        "from_bp_id": p.get("from"),
        "to_bp_id": p.get("to"),
        "route_id": rid,
        "render": "solid",
        "range_status": "now",
        "_link_status": "linked-property-geometry",
        "_link_source": "grok-minor-hotels/seed_property_route_linkage",
        "_link_kind": "property-corridor",
        "economics_status": "bound" if rid else "economics_pending",
        "_minor_property_from": from_prop,
        "_minor_property_to": to_prop,
    }


def aspirational_property_featured(prop: dict, ph: dict) -> dict:
    archetype = (prop.get("route_archetype") or prop.get("navier_route_archetype") or "gateway transfer").replace("→", "→")
    return {
        "label": f"{prop.get('property_name')} — {archetype}",
        "from_node_id": (ph.get("cities") or [None])[0],
        "to_node_id": (ph.get("cities") or [None])[0],
        "platform": "Pioneer II",
        "display": "text_only",
        "_link_status": "aspirational-no-built-route",
        "_link_kind": "property-backlog-chip",
        "_link_source": "grok-minor-hotels/seed_property_route_linkage",
        "economics_status": "roadmap_excluded",
        "render": "roadmap-amber-dashed",
    }


def featured_from_journey(j: dict) -> dict:
    label = f"{j.get('from', '')} ↔ {j.get('to', '')}".strip(" ↔")
    rid = j.get("route_id")
    row = {
        "label": label,
        "from_node_id": j.get("from_node_id"),
        "to_node_id": j.get("to_node_id"),
        "distance_nm": j.get("distance_nm"),
        "platform": j.get("platform", "Pioneer II"),
        "route_id": rid,
        "_link_kind": "property-phase-sync",
        "_link_status": j.get("_link_status"),
        "_link_source": "grok-minor-hotels/seed_property_route_linkage",
        "economics_status": j.get("economics_status", "economics_pending"),
    }
    if rid:
        row["route_ids"] = [rid]
    return row


def seed_market(market: dict, binds: list[dict], routes: list[dict], inventory: list[dict]) -> tuple[int, int]:
    properties = properties_for_market(market, binds, inventory)
    if not properties:
        return 0, 0
    cities = set(market.get("anchor_cities") or [])
    prior = [
        j for j in (market.get("journeys_unlocked") or [])
        if j.get("_link_source") != "grok-minor-hotels/seed_property_route_linkage"
    ]
    existing = {j.get("route_id") for j in prior if j.get("route_id")}
    journeys_added = 0
    new_journeys: list[dict] = list(prior)

    candidates: list[tuple[int, dict, str | None, str | None]] = []
    for feat in routes:
        p = route_props(feat)
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if cities and fc not in cities and tc not in cities:
            continue
        ok, fp, tp = route_touches_portfolio(feat, properties)
        if not ok or not p.get("id"):
            continue
        # Prefer inter-property (B) > gateway→property (A) > excursion (C)
        score = 3 if fp and tp and fp != tp else 2 if tp else 1
        candidates.append((score, feat, fp, tp))

    candidates.sort(key=lambda x: (-x[0], route_props(x[1]).get("distance_nm") or 999))
    seen_rids: set[str] = set(existing)

    for _score, feat, fp, tp in candidates:
        if journeys_added >= MAX_JOURNEYS_PER_MARKET:
            break
        rid = route_props(feat).get("id")
        if not rid or rid in seen_rids:
            continue
        j = journey_from_route(feat, from_prop=fp, to_prop=tp)
        new_journeys.append(j)
        seen_rids.add(rid)
        journeys_added += 1

    market["journeys_unlocked"] = new_journeys

    phases_added = 0
    pool = [j for j in new_journeys if j.get("route_id")]
    used: set[str] = set()
    prop_i = 0
    prop_list = properties
    for ph in market.get("phases") or []:
        if not isinstance(ph, dict) or ph.get("featured_routes"):
            continue
        frs: list[dict] = []
        for j in pool:
            if len(frs) >= 3:
                break
            rid = j.get("route_id")
            if not rid or rid in used:
                continue
            frs.append(featured_from_journey(j))
            used.add(rid)
            phases_added += 1
        while len(frs) < 1 and prop_i < len(prop_list):
            frs.append(aspirational_property_featured(prop_list[prop_i], ph))
            prop_i += 1
            phases_added += 1
        if frs:
            ph["featured_routes"] = frs

    return journeys_added, phases_added


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", default="minor-hotels")
    args = ap.parse_args()

    partner = load_json(PARTNER_SRC if PARTNER_SRC.exists() else PARTNER_DST)
    binds = load_binds()
    routes = load_routes()
    inventory = load_inventory_properties()

    total_j, total_p = 0, 0
    market_rows = []
    for market in partner.get("markets") or []:
        if not isinstance(market, dict):
            continue
        ja, pa = seed_market(market, binds, routes, inventory)
        total_j += ja
        total_p += pa
        if ja or pa:
            market_rows.append({"slug": market.get("slug"), "journeys_added": ja, "phases_filled": pa})

    report = {
        "at": utc_now(),
        "partner": args.partner,
        "journeys_added": total_j,
        "phases_filled": total_p,
        "markets": market_rows,
    }

    if args.apply and (total_j or total_p):
        text = json.dumps(partner, indent=2, ensure_ascii=False) + "\n"
        PARTNER_DST.write_text(text)
        if PARTNER_SRC.exists():
            PARTNER_SRC.write_text(text)

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())