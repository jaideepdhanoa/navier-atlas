#!/usr/bin/env python3
"""
Splice Tasklet Bolt/Yango handoff into data-clean/partners/.
- AUTHORED-ALL-33-markets.json → full per-market sub-proposals (Grab parity)
- AUTHORED-yango-hub.json → Yango hub refresh
- handoff partners/bolt.json → Bolt hub + growth_case shell
- Bind route_id on featured_routes / journeys_unlocked where corridors exist
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INGEST = ROOT / "_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19"

TURKEY_ANCHORS = [
    "istanbul-turkey",
    "bodrum-turkey",
    "antalya-turkey",
    "cesme-izmir-turkey",
]

# Tasklet anchor shorthand → sealed city_id (where city exists on surface)
ANCHOR_CROSSWALK = {
    "dubai": "dubai-uae",
    "abu-dhabi": "abu-dhabi-uae",
    "sharjah": "sharjah-uae",
    "doha": "doha-qatar",
    "palma-mallorca-spain": "mallorca-spain",
    "el-gouna-egypt": "hurghada-el-gouna-egypt",
    "hurghada-egypt": "hurghada-el-gouna-egypt",
    "neom-ksa": "neom-sindalah-ksa",
    "amaala-ksa": "red-sea-global-ksa",
    "red-sea-global": "red-sea-global-ksa",
    "ksa-commercial": "jeddah-ksa",
}

HUB_STRIP = {"_provenance", "_held_markets", "_anchor_market", "capture_rate"}
HELD_MARKET_SLUGS = {
    "bolt-israel",
    "bolt-lebanon",
    "yango-israel",
}


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def route_features(obj) -> list:
    return obj if isinstance(obj, list) else obj.get("features", [])


def route_props(r: dict) -> dict:
    return r.get("properties", r)


def build_route_index(routes: list) -> dict[tuple[str, str], str]:
    """Map (from_node, to_node) and city pairs → route_id (first match)."""
    idx: dict[tuple[str, str], str] = {}
    for r in routes:
        p = route_props(r)
        rid = p.get("id") or p.get("route_id")
        if not rid:
            continue
        for a, b in (
            (p.get("from_node"), p.get("to_node")),
            (p.get("from"), p.get("to")),
            (p.get("from_city_id"), p.get("to_city_id")),
        ):
            if a and b:
                idx[(a, b)] = rid
                idx[(b, a)] = rid
    return idx


def bind_route_refs(obj, route_idx: dict, economics_url: str | None):
    """Recursively bind route_id on featured_routes / journeys_unlocked."""
    if isinstance(obj, list):
        for item in obj:
            bind_route_refs(item, route_idx, economics_url)
        return
    if not isinstance(obj, dict):
        return

    fn = obj.get("from_node_id") or obj.get("from_node")
    tn = obj.get("to_node_id") or obj.get("to_node")
    if fn and tn and obj.get("route_id") is None:
        rid = route_idx.get((fn, tn))
        if rid:
            obj["route_id"] = rid
            obj["_link_kind"] = "corridor"
            obj["_link_status"] = "linked-exact"

    if economics_url and obj.get("model_link") is None and "route_id" in obj:
        obj["model_link"] = economics_url

    for v in obj.values():
        if isinstance(v, (dict, list)):
            bind_route_refs(v, route_idx, economics_url)


def sanitize_partner_text(obj):
    """Strip exclusion tokens from partner-facing copy."""
    if isinstance(obj, str):
        return (
            obj.replace("on hold", "held pending sovereign coordination")
            .replace("On hold", "Held pending sovereign coordination")
        )
    if isinstance(obj, list):
        return [sanitize_partner_text(x) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize_partner_text(v) for k, v in obj.items()}
    return obj


def normalize_anchors(anchors: list[str], sealed: set[str]) -> list[str]:
    out = []
    for a in anchors or []:
        cid = ANCHOR_CROSSWALK.get(a, a)
        if cid in sealed:
            out.append(cid)
        elif a in sealed:
            out.append(a)
    return list(dict.fromkeys(out))


def market_from_authored(authored: dict, economics_url: str, sealed_cities: set[str], market_key: str) -> dict:
    m = sanitize_partner_text({k: v for k, v in authored.items() if k not in HUB_STRIP})
    if m.get("slug") and not m.get("id"):
        m["id"] = m["slug"]
    m["anchor_cities"] = normalize_anchors(m.get("anchor_cities") or [], sealed_cities)
    if market_key in HELD_MARKET_SLUGS:
        m["tier"] = "data-only"
        m["status"] = "held"
    bind_route_refs(m, ROUTE_IDX, economics_url)
    return m


def hub_fields(src: dict, *, strip_markets: bool = True) -> dict:
    skip = {"markets", "roll_up_markets", "_provenance", "_held_markets", "_anchor_market"}
    if not strip_markets:
        skip.discard("markets")
    out = {}
    for k, v in src.items():
        if k in skip:
            continue
        if k == "partner_context" and isinstance(v, str):
            out[k] = {"their_ambition": v, "their_pressure": "", "where_navier_fits": ""}
            continue
        if k == "network_thesis" and isinstance(v, str):
            out[k] = {"headline": "Yango water network", "body": v}
            continue
        out[k] = copy.deepcopy(v)
    return out


def apply_bolt(authored_all: dict, handoff_bolt: dict, economics_url: str, sealed_cities: set[str]) -> dict:
    bolt_markets = []
    for key in sorted(authored_all):
        if not key.startswith("bolt-"):
            continue
        m = market_from_authored(authored_all[key], economics_url, sealed_cities, key)
        bolt_markets.append(m)
    bolt_markets.sort(key=lambda x: (x.get("label") or x.get("id") or "").lower())

    out = sanitize_partner_text(hub_fields(handoff_bolt, strip_markets=True))
    out["markets"] = bolt_markets
    out.pop("roll_up_markets", None)
    out["economics_url"] = economics_url
    out["layout"] = "hub"
    out["network_thesis"]["stats"] = [
        {"label": "Markets", "value": str(len(bolt_markets)), "sub": "full per-market sub-proposals"},
        {"label": "Corridors", "value": "223", "sub": "shared network registry"},
        {"label": "Proof", "value": "~100 vessels", "sub": "live Maldives network"},
    ]
    out["_ingest"] = {
        "package": "bolt-yango-seal-2026-06-19",
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "markets_spliced": len(bolt_markets),
    }
    bind_route_refs(out, ROUTE_IDX, economics_url)
    return out


def apply_yango(authored_all: dict, hub: dict, economics_url: str, sealed_cities: set[str]) -> dict:
    yango_markets = []
    for key in sorted(authored_all):
        if not key.startswith("yango-"):
            continue
        m = market_from_authored(authored_all[key], economics_url, sealed_cities, key)
        if m.get("slug") == "turkey" or m.get("id") == "turkey":
            anchors = list(dict.fromkeys(TURKEY_ANCHORS + (m.get("anchor_cities") or [])))
            m["anchor_cities"] = [a for a in anchors if a in sealed_cities]
        yango_markets.append(m)
    yango_markets.sort(key=lambda x: (x.get("label") or x.get("id") or "").lower())

    out = sanitize_partner_text(hub_fields(hub, strip_markets=True))
    out["markets"] = yango_markets
    out["partner_id"] = "yango"
    out["display"] = "Yango"
    out["display_name"] = "Yango"
    out["layout"] = "hub"
    out["economics_url"] = economics_url
    out["category"] = "ridehail"
    out["archetype"] = "ridehail"
    # growth_case placeholders are GROK_BIND sentinels — omit until economics lane binds real numbers.
    gc = out.pop("growth_case", None)
    if gc and isinstance(gc, dict):
        out["_growth_case_pending"] = {
            "status": "awaiting_grok_bind",
            "economics_url": economics_url,
            "note": "Run build_economics_sidecar.py against Yango model; bind phase_economics + ladder.",
        }
    out["_ingest"] = {
        "package": "bolt-yango-seal-2026-06-19",
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "markets_spliced": len(yango_markets),
        "held_markets": hub.get("_held_markets", []),
    }
    bind_route_refs(out, ROUTE_IDX, economics_url)
    return out


def main():
    global ROUTE_IDX
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--ingest", default=str(INGEST))
    args = ap.parse_args()

    ingest = Path(args.ingest)
    dc = ROOT / args.dc
    partners = dc / "partners"

    authored_all = load_json(ingest / "subproposals/AUTHORED-ALL-33-markets.json")
    yango_hub = load_json(ingest / "subproposals/AUTHORED-yango-hub.json")
    handoff_bolt = load_json(ingest / "partners/bolt.json")
    econ_map = load_json(ingest / "inputs/economics_url_map.json")
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    sealed_cities = {
        f["properties"]["id"]
        for k in ("city", "priority_city")
        for f in fbt.get(k, [])
        if f.get("properties", {}).get("id")
    }
    routes = route_features(load_json(dc / "ROUTES.json"))
    ROUTE_IDX = build_route_index(routes)

    bolt_url = econ_map.get("economics_url", {}).get("bolt", "")
    yango_url = econ_map.get("economics_url", {}).get("yango", "")

    bolt_out = apply_bolt(authored_all, handoff_bolt, bolt_url, sealed_cities)
    yango_out = apply_yango(authored_all, yango_hub, yango_url, sealed_cities)

    save_json(partners / "bolt.json", bolt_out)
    save_json(partners / "yango.json", yango_out)

    unresolved = []
    for partner, markets in (("bolt", bolt_out["markets"]), ("yango", yango_out["markets"])):
        for m in markets:
            if not m.get("anchor_cities"):
                unresolved.append(f"{partner}/{m.get('id')}")

    report = {
        "date": "2026-06-19",
        "bolt_markets": len(bolt_out["markets"]),
        "yango_markets": len(yango_out["markets"]),
        "routes_indexed": len(ROUTE_IDX),
        "turkey_anchors": TURKEY_ANCHORS,
        "markets_zero_anchors_after_crosswalk": unresolved,
        "note": "BP coverage sealed; Yango growth_case bound in bind_yango_growth_case.py.",
    }
    out_path = ROOT / "grok-routing-output" / "bolt-yango-splice-report.json"
    save_json(out_path, report)
    print(json.dumps(report, indent=2))
    print(f"→ wrote {partners / 'bolt.json'} ({report['bolt_markets']} markets)")
    print(f"→ wrote {partners / 'yango.json'} ({report['yango_markets']} markets)")


if __name__ == "__main__":
    main()