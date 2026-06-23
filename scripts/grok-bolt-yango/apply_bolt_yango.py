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
import sys
import unicodedata
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
    "bodrum": "bodrum-turkey",
    "cesme-izmir": "cesme-izmir-turkey",
    "antalya": "antalya-turkey",
}

HUB_STRIP = {"_provenance", "_held_markets", "_anchor_market", "capture_rate"}
HELD_MARKET_SLUGS = {
    "bolt-israel",
    "bolt-lebanon",
    "yango-israel",
}

# Pruned proposal pages — geometry may exist; do not splice into partner hub
PRUNED_MARKET_KEYS = frozenset(
    {
        "bolt-cyprus",
        "bolt-romania",
        "bolt-israel",
        "bolt-lebanon",
        "yango-senegal",
        "yango-mozambique",
        "yango-tunisia",
        "yango-pakistan",
        "yango-caspian-az",
        "yango-caspian-kz",
        "yango-israel",
    }
)


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def route_features(obj) -> list:
    return obj if isinstance(obj, list) else obj.get("features", [])


def route_props(r: dict) -> dict:
    return r.get("properties", r)


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_label(s: str | None) -> str:
    if not s:
        return ""
    s = _strip_accents(s.lower().strip())
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


_LABEL_STOP = frozenset(
    {
        "the", "and", "of", "lisbon", "portugal", "spain", "marina", "terminal",
        "fluvial", "pier", "port", "harbour", "harbor", "jetty", "city", "town",
    }
)


def _label_tokens(s: str | None) -> set[str]:
    return {t for t in norm_label(s).split() if t and t not in _LABEL_STOP}


def labels_match(a: str | None, b: str | None) -> bool:
    na, nb = norm_label(a), norm_label(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = _label_tokens(a), _label_tokens(b)
    if not ta or not tb:
        return False
    overlap = ta & tb
    need = min(2, min(len(ta), len(tb)))
    return len(overlap) >= max(1, need)


def crosswalk_node(nid: str | None) -> str | None:
    if not nid:
        return nid
    return ANCHOR_CROSSWALK.get(nid, nid)


class RouteIndexes:
    def __init__(self, routes: list):
        self.bp_pair: dict[tuple[str, str], str] = {}
        self.label_pair: dict[tuple[str, str], str] = {}
        self.inter_city: dict[tuple[str, str], str] = {}
        self.by_id: dict[str, dict] = {}
        for r in routes:
            p = route_props(r)
            rid = p.get("id") or p.get("route_id")
            if not rid:
                continue
            self.by_id[rid] = p
            fn, tn = p.get("from_node"), p.get("to_node")
            if fn and tn:
                self.bp_pair[(fn, tn)] = rid
                self.bp_pair[(tn, fn)] = rid
            fl, tl = p.get("from_label"), p.get("to_label")
            if fl and tl:
                key = (norm_label(fl), norm_label(tl))
                self.label_pair[key] = rid
                self.label_pair[(key[1], key[0])] = rid
            fc, tc = p.get("from_city_id"), p.get("to_city_id")
            if fc and tc and fc != tc:
                self.inter_city[(fc, tc)] = rid
                self.inter_city[(tc, fc)] = rid

    def match_labels(self, from_l: str | None, to_l: str | None) -> str | None:
        if not from_l or not to_l:
            return None
        nf, nt = norm_label(from_l), norm_label(to_l)
        hit = self.label_pair.get((nf, nt))
        if hit:
            return hit
        for (rf, rt), rid in self.label_pair.items():
            if labels_match(from_l, rf) and labels_match(to_l, rt):
                return rid
        return None


def build_corridor_index(corridors_doc: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for mkey, mval in (corridors_doc.get("markets") or {}).items():
        if isinstance(mval, dict) and mval.get("corridors"):
            out[mkey] = mval["corridors"]
    return out


def corridor_for_journey(corridors: list[dict], from_l: str, to_l: str) -> dict | None:
    for c in corridors or []:
        if labels_match(from_l, c.get("from")) and labels_match(to_l, c.get("to")):
            return c
    return None


def bind_route_item(
    obj: dict,
    market_key: str,
    indexes: RouteIndexes,
    corridor_idx: dict,
    economics_url: str | None,
    bp_idx: dict | None = None,
):
    """Bind one featured_route / journey_unlocked row."""
    if not isinstance(obj, dict) or obj.get("route_id"):
        return

    for key in ("from_node_id", "to_node_id", "from_node", "to_node"):
        if obj.get(key):
            obj[key] = crosswalk_node(obj[key])

    from_l = obj.get("from") or obj.get("from_label")
    to_l = obj.get("to") or obj.get("to_label")
    rid = indexes.match_labels(from_l, to_l)

    corr = corridor_for_journey(corridor_idx.get(market_key, []), from_l or "", to_l or "")
    if not rid and corr and corr.get("route_id"):
        rid = corr["route_id"]

    if not rid and corr and bp_idx:
        from bolt_yango_routing_shared import resolve_corridor_endpoints

        from_bp, to_bp, _, _ = resolve_corridor_endpoints(corr, bp_idx)
        if from_bp and to_bp:
            rid = indexes.bp_pair.get((from_bp, to_bp))

    if not rid:
        fn = obj.get("from_node_id") or obj.get("from_node")
        tn = obj.get("to_node_id") or obj.get("to_node")
        if fn and tn and fn != tn:
            rid = indexes.inter_city.get((fn, tn)) or indexes.bp_pair.get((fn, tn))

    if rid:
        obj["route_id"] = rid
        obj["_link_kind"] = "corridor-label" if from_l else "corridor-node"
        obj["_link_status"] = "linked"
    elif from_l and to_l:
        obj["_link_status"] = "unlinked-no-route"
    elif (obj.get("from_node_id") or obj.get("from_node")) == (obj.get("to_node_id") or obj.get("to_node")):
        obj["_link_status"] = "unlinked-intra-city"

    if economics_url and obj.get("route_id") and obj.get("model_link") is None:
        obj["model_link"] = economics_url


def bind_market_routes(
    market: dict,
    market_key: str,
    indexes: RouteIndexes,
    corridor_idx: dict,
    economics_url: str | None,
    bp_idx: dict | None = None,
):
    for j in market.get("journeys_unlocked") or []:
        bind_route_item(j, market_key, indexes, corridor_idx, economics_url, bp_idx)
    for ph in market.get("phases") or []:
        for key in ("cities",):
            if isinstance(ph.get(key), list):
                ph[key] = [crosswalk_node(c) or c for c in ph[key]]
        for fr in ph.get("featured_routes") or []:
            bind_route_item(fr, market_key, indexes, corridor_idx, economics_url, bp_idx)


def bind_route_refs(
    obj,
    indexes: RouteIndexes,
    corridor_idx: dict,
    economics_url: str | None,
    market_key: str | None = None,
    bp_idx: dict | None = None,
):
    """Recursively bind route_id on hub + market proposals."""
    if isinstance(obj, list):
        for item in obj:
            bind_route_refs(item, indexes, corridor_idx, economics_url, market_key, bp_idx)
        return
    if not isinstance(obj, dict):
        return

    mkey = market_key
    if obj.get("slug") and obj.get("journeys_unlocked") is not None:
        pid = obj.get("id") or obj.get("slug")
        prefix = "bolt" if any(k.startswith("bolt-") for k in corridor_idx if pid in k) else "yango"
        for candidate in (f"bolt-{pid}", f"yango-{pid}", pid):
            if candidate in corridor_idx:
                mkey = candidate
                break
        bind_market_routes(obj, mkey or f"{prefix}-{pid}", indexes, corridor_idx, economics_url, bp_idx)
        return

    for j in obj.get("journeys_unlocked") or []:
        bind_route_item(j, market_key or "", indexes, corridor_idx, economics_url, bp_idx)

    for v in obj.values():
        if isinstance(v, (dict, list)):
            bind_route_refs(v, indexes, corridor_idx, economics_url, market_key, bp_idx)


def sanitize_partner_text(obj):
    """Strip exclusion tokens from partner-facing copy."""
    if isinstance(obj, str):
        from bolt_yango_shared import scrub_field

        out = (
            obj.replace("on hold", "held pending sovereign coordination")
            .replace("On hold", "Held pending sovereign coordination")
        )
        return scrub_field(out) or out
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


def market_from_authored(
    authored: dict,
    economics_url: str,
    sealed_cities: set[str],
    market_key: str,
    indexes: RouteIndexes,
    corridor_idx: dict,
    bp_idx: dict | None = None,
) -> dict:
    m = sanitize_partner_text({k: v for k, v in authored.items() if k not in HUB_STRIP})
    if m.get("slug") and not m.get("id"):
        m["id"] = m["slug"]
    m["anchor_cities"] = normalize_anchors(m.get("anchor_cities") or [], sealed_cities)
    if market_key in HELD_MARKET_SLUGS:
        m["tier"] = "data-only"
        m["status"] = "held"
    bind_market_routes(m, market_key, indexes, corridor_idx, economics_url, bp_idx)
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


def apply_bolt(
    authored_all: dict,
    handoff_bolt: dict,
    economics_url: str,
    sealed_cities: set[str],
    indexes: RouteIndexes,
    corridor_idx: dict,
    bp_idx: dict | None = None,
    *,
    ingest_package: str = "bolt-yango-seal-2026-06-19",
) -> dict:
    bolt_markets = []
    for key in sorted(authored_all):
        if not key.startswith("bolt-") or key in PRUNED_MARKET_KEYS:
            continue
        m = market_from_authored(
            authored_all[key], economics_url, sealed_cities, key, indexes, corridor_idx, bp_idx
        )
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
        "package": ingest_package,
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "markets_spliced": len(bolt_markets),
        "pruned_skipped": sorted(PRUNED_MARKET_KEYS),
    }
    bind_route_refs(out, indexes, corridor_idx, economics_url, bp_idx=bp_idx)
    return out


def apply_yango(
    authored_all: dict,
    hub: dict,
    economics_url: str,
    sealed_cities: set[str],
    indexes: RouteIndexes,
    corridor_idx: dict,
    bp_idx: dict | None = None,
    *,
    ingest_package: str = "bolt-yango-seal-2026-06-19",
) -> dict:
    yango_markets = []
    for key in sorted(authored_all):
        if not key.startswith("yango-") or key in PRUNED_MARKET_KEYS:
            continue
        m = market_from_authored(
            authored_all[key], economics_url, sealed_cities, key, indexes, corridor_idx, bp_idx
        )
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
        "package": ingest_package,
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "markets_spliced": len(yango_markets),
        "held_markets": hub.get("_held_markets", []),
        "pruned_skipped": sorted(PRUNED_MARKET_KEYS),
    }
    bind_route_refs(out, indexes, corridor_idx, economics_url, bp_idx=bp_idx)
    return out


def binding_stats(partner_doc: dict) -> dict:
    linked = unlinked = intra = 0
    for m in partner_doc.get("markets") or []:
        for j in m.get("journeys_unlocked") or []:
            if j.get("route_id"):
                linked += 1
            elif j.get("_link_status") == "unlinked-intra-city":
                intra += 1
            else:
                unlinked += 1
        for ph in m.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                if fr.get("route_id"):
                    linked += 1
                elif fr.get("_link_status") == "unlinked-intra-city":
                    intra += 1
                else:
                    unlinked += 1
    return {"linked": linked, "unlinked": unlinked, "intra_city_pending_route": intra}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--ingest", default=str(INGEST))
    ap.add_argument(
        "--authored",
        default="",
        help="Path to authored markets JSON (default: ingest subproposals or inputs/)",
    )
    args = ap.parse_args()

    ingest = Path(args.ingest)
    dc = ROOT / args.dc
    partners = dc / "partners"

    if args.authored:
        authored_path = Path(args.authored)
    elif (ingest / "inputs/subproposals-enriched-2026-06-20.json").exists():
        authored_path = ingest / "inputs/subproposals-enriched-2026-06-20.json"
    else:
        authored_path = ingest / "subproposals/AUTHORED-ALL-33-markets.json"
    authored_all = load_json(authored_path)
    hub_ingest = ingest
    if not (ingest / "subproposals/AUTHORED-yango-hub.json").exists():
        hub_ingest = INGEST
    yango_hub = load_json(hub_ingest / "subproposals/AUTHORED-yango-hub.json")
    handoff_bolt = load_json(hub_ingest / "partners/bolt.json")
    econ_path = ingest / "inputs/economics_url_map.json"
    if not econ_path.exists():
        econ_path = INGEST / "inputs/economics_url_map.json"
    econ_map = load_json(econ_path)
    fbt = load_json(dc / "FEATURES_BY_TYPE.json")
    sealed_cities = {
        f["properties"]["id"]
        for k in ("city", "priority_city")
        for f in fbt.get(k, [])
        if f.get("properties", {}).get("id")
    }
    routes = route_features(load_json(dc / "ROUTES.json"))
    indexes = RouteIndexes(routes)
    econ_corr = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
    corridors_path = ingest / "inputs/corridors.json"
    if not corridors_path.exists() and econ_corr.exists():
        corridors_path = econ_corr
    corridor_idx = build_corridor_index(load_json(corridors_path)) if corridors_path.exists() else {}

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from bolt_yango_routing_shared import build_bp_index

    bp_idx = build_bp_index(fbt)

    bolt_url = econ_map.get("economics_url", {}).get("bolt", "")
    yango_url = econ_map.get("economics_url", {}).get("yango", "")

    pkg = authored_path.name
    bolt_out = apply_bolt(
        authored_all,
        handoff_bolt,
        bolt_url,
        sealed_cities,
        indexes,
        corridor_idx,
        bp_idx,
        ingest_package=pkg,
    )
    yango_out = apply_yango(
        authored_all,
        yango_hub,
        yango_url,
        sealed_cities,
        indexes,
        corridor_idx,
        bp_idx,
        ingest_package=pkg,
    )

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
        "routes_in_graph": len(indexes.by_id),
        "corridor_markets": len(corridor_idx),
        "binding_bolt": binding_stats(bolt_out),
        "binding_yango": binding_stats(yango_out),
        "turkey_anchors": TURKEY_ANCHORS,
        "markets_zero_anchors_after_crosswalk": unresolved,
        "note": "Corridor-label binding; intra-city routes require BP-pair geometry lane.",
    }
    out_path = ROOT / "grok-routing-output" / "bolt-yango-splice-report.json"
    save_json(out_path, report)
    print(json.dumps(report, indent=2))
    print(f"→ wrote {partners / 'bolt.json'} ({report['bolt_markets']} markets)")
    print(f"→ wrote {partners / 'yango.json'} ({report['yango_markets']} markets)")


if __name__ == "__main__":
    main()