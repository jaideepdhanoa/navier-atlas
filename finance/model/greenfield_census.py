#!/usr/bin/env python3
"""Standardized greenfield WIDTH census (replaces Grab-global 4.9× template).

Methodology (locked, same structure as growth-config Grab census):

  g = 1 + (N_greenfield / N_sourced) × α_density

where:
  N_sourced    = undirected-unique grounded (non-dup) corridors in partner agg with a route_id
  N_greenfield = undirected-unique atlas ROUTES in partner geography that are:
                   · Pioneer-feasible (distance_nm ≤ max_nm, default 70)
                   · not already in the sourced route_id / endpoint-pair set
                   · not micro-local noise when edge_class ∈ exclude_edge_classes
                   · not render_hidden / quarantine
  α_density    = low/mid/high from growth-config (default 0.25/0.40/0.55)

Partner geography = city_ids (and optional cluster_ids) resolved from:
  finance/model/corridors.json markets for that partner
  + data-clean/partners/<p>.json markets[].anchor_cities + network_footprint keys

NULL-beats-guess:
  · N_sourced == 0  → greenfield OFF (factor 1.0), mode=off
  · N_greenfield == 0 → factor 1.0, mode=census_empty
  · Never invent corridors or demand

Usage:
  python3 greenfield_census.py --partner didi
  python3 greenfield_census.py --all
  python3 greenfield_census.py --partner didi --json finance/recal/greenfield-census/didi.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIN = HERE.parent
ROOT = FIN.parent
DC = ROOT / "data-clean"
RECAL = FIN / "recal"
CENSUS_DIR = RECAL / "greenfield-census"
CFG_PATH = HERE / "growth-config.json"
CORRIDORS_PATH = HERE / "corridors.json"
ROUTES_PATH = DC / "ROUTES.json"
MAX_NM_DEFAULT = 70.0
# Grab census spirit: tier1 market-making + tier2 spokes — exclude intra-hub micro "local".
INCLUDE_EDGE = {
    "regional",
    "inter-city",
    "intercity",
    "trunk",
    "island-hop",
    "island_hop",
    "ferry",
    "commuter",
    "hub-spoke",
    "hub_spoke",
    "cross-border",
    "cross_border",
}
# Always drop noise + dense local mesh (otherwise atlas density inflates width 10–50×).
EXCLUDE_EDGE = {"micro", "poi-link", "internal", "hidden", "local"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def undirected_pair(a: str | None, b: str | None) -> tuple[str, str] | None:
    if not a or not b:
        return None
    return (a, b) if a <= b else (b, a)


def alpha_from_config() -> dict:
    cfg = load_json(CFG_PATH)
    gf = cfg["multipliers"]["greenfield_corridor_factor"]
    alpha = (gf.get("_census") or {}).get("alpha_density") or {
        "low": 0.25,
        "mid": 0.40,
        "high": 0.55,
    }
    return {k: float(alpha[k]) for k in ("low", "mid", "high")}


# Grab census count_ratio was 9.7. Above that, linear α·ratio overstates width because
# atlas micro-mesh density >> economics-sourced density. Soften the tail (still measured).
GRAB_RATIO_REF = 9.7
TAIL_ALPHA_SCALE = 0.15


def _effective_ratio(ratio: float) -> float:
    if ratio <= GRAB_RATIO_REF:
        return ratio
    return GRAB_RATIO_REF + (ratio - GRAB_RATIO_REF) * TAIL_ALPHA_SCALE


def derive_factor(n_sourced: int, n_greenfield: int, alpha: dict) -> dict:
    if n_sourced <= 0:
        return {"low": 1.0, "mid": 1.0, "high": 1.0, "count_ratio": None, "ratio_effective": None}
    ratio = n_greenfield / n_sourced
    r_eff = _effective_ratio(ratio)
    return {
        "low": round(1.0 + r_eff * alpha["low"], 4),
        "mid": round(1.0 + r_eff * alpha["mid"], 4),
        "high": round(1.0 + r_eff * alpha["high"], 4),
        "count_ratio": round(ratio, 4),
        "ratio_effective": round(r_eff, 4),
        "tail_softened": ratio > GRAB_RATIO_REF,
    }


def partner_cities_and_clusters(partner: str) -> tuple[set[str], set[str]]:
    cities: set[str] = set()
    clusters: set[str] = set()
    if CORRIDORS_PATH.exists():
        corr = load_json(CORRIDORS_PATH)
        for mid, m in (corr.get("markets") or {}).items():
            p = (m.get("partner") or "").lower()
            if partner == "grab":
                if p not in ("", "grab"):
                    continue
            elif p != partner.lower():
                continue
            for c in m.get("corridors") or []:
                for k in ("from_node_id", "to_node_id", "from_city_id", "to_city_id"):
                    v = c.get(k)
                    if v and isinstance(v, str) and not v.startswith("bp-"):
                        cities.add(v)
                # from/to human labels never used as city ids
    # partner JSON footprint / markets
    for base in (DC / "partners" / f"{partner}.json", ROOT / "partner-pitch" / "partners" / f"{partner}.json"):
        if not base.exists():
            continue
        doc = load_json(base)
        for m in doc.get("markets") or []:
            if not isinstance(m, dict):
                continue
            for c in m.get("anchor_cities") or []:
                if isinstance(c, str):
                    cities.add(c)
            sk = m.get("scope_registry_key")
            if isinstance(sk, str):
                cities.add(sk)
            for sk in m.get("scope_registry_keys") or []:
                if isinstance(sk, str):
                    cities.add(sk)
        for fp in doc.get("network_footprint") or []:
            if isinstance(fp, str):
                cities.add(fp)
                continue
            if not isinstance(fp, dict):
                continue
            key = fp.get("registry_key") or fp.get("id")
            if key:
                cities.add(str(key))
                # country-level footprint keys are clusters sometimes
                if fp.get("covered") is True:
                    clusters.add(str(key))
    # CLUSTERS: if a footprint key is a cluster_id, expand members
    cl_path = DC / "CLUSTERS.json"
    if cl_path.exists() and clusters:
        cl = load_json(cl_path)
        by_id = {c.get("cluster_id"): c for c in (cl.get("clusters") or [])}
        for cid in list(clusters):
            c = by_id.get(cid)
            if c:
                for mid in c.get("member_city_ids") or []:
                    cities.add(mid)
    # also treat bare city-looking footprint keys as cities already in set
    return cities, clusters


def load_routes() -> list:
    raw = load_json(ROUTES_PATH)
    return raw if isinstance(raw, list) else raw.get("features") or []


def census_partner(
    partner: str,
    *,
    agg_path: Path | None = None,
    max_nm: float = MAX_NM_DEFAULT,
) -> dict:
    alpha = alpha_from_config()
    agg_path = agg_path or (RECAL / f"agg-{partner}.json")
    if not agg_path.exists():
        return {
            "partner": partner,
            "at": utc_now(),
            "status": "no_agg",
            "mode": "off",
            "derived_greenfield_factor": {
                "headline_tier1_plus_tier2": {"low": 1.0, "mid": 1.0, "high": 1.0}
            },
            "n_sourced": 0,
            "n_greenfield_headline": 0,
            "note": f"missing {agg_path}",
        }

    agg = load_json(agg_path)
    rows = agg.get("rows") or []
    sourced_rids: set[str] = set()
    sourced_pairs: set[tuple[str, str]] = set()
    n_sourced_rows = 0
    for r in rows:
        if r.get("is_dup") or r.get("status") == "duplicate":
            continue
        # grounded floor contributors only (width base = published floor set)
        if r.get("status") not in ("grounded", None) and r.get("_in_grounded_floor") is False:
            # keep estimated out of sourced floor
            if r.get("status") != "grounded":
                continue
        if r.get("status") and r.get("status") not in ("grounded",):
            # only grounded
            if r.get("status") != "grounded":
                continue
        mid = r.get("mid") or {}
        rid = r.get("route_id") or mid.get("route_id")
        # require vessels or grounded status
        if r.get("status") != "grounded" and mid.get("vessels_supported_10pct") is None:
            continue
        if r.get("status") != "grounded":
            continue
        n_sourced_rows += 1
        if rid:
            sourced_rids.add(rid)
        # try endpoints from corridors later
    # endpoint pairs from corridors.json for this partner's grounded routes
    if CORRIDORS_PATH.exists():
        corr = load_json(CORRIDORS_PATH)
        for mid, m in (corr.get("markets") or {}).items():
            p = (m.get("partner") or ("grab" if partner == "grab" else "")).lower()
            if partner == "grab":
                if p not in ("", "grab"):
                    continue
            elif p != partner.lower():
                continue
            for c in m.get("corridors") or []:
                rid = c.get("route_id")
                if rid and rid in sourced_rids:
                    pair = undirected_pair(
                        c.get("endpoint_boarding_points", {}).get("from")
                        or c.get("from_node_id"),
                        c.get("endpoint_boarding_points", {}).get("to")
                        or c.get("to_node_id"),
                    )
                    # also from/to labels as last resort skip
                    fa = (c.get("endpoint_boarding_points") or {}).get("from") or c.get("from_node_id")
                    ta = (c.get("endpoint_boarding_points") or {}).get("to") or c.get("to_node_id")
                    # BP ids preferred
                    bp_from = (c.get("endpoint_boarding_points") or {}).get("from")
                    bp_to = (c.get("endpoint_boarding_points") or {}).get("to")
                    pair = undirected_pair(bp_from, bp_to)
                    if pair:
                        sourced_pairs.add(pair)

    cities, clusters = partner_cities_and_clusters(partner)
    routes = load_routes()
    # Expand geography from sourced route city stamps (critical when corridors use labels)
    for feat in routes:
        p = feat.get("properties") or {}
        if p.get("id") in sourced_rids:
            for k in ("from_city_id", "to_city_id"):
                if p.get(k):
                    cities.add(p[k])
            if p.get("cluster_id"):
                clusters.add(p["cluster_id"])
    # Expand cluster members
    cl_path = DC / "CLUSTERS.json"
    if cl_path.exists() and clusters:
        cl = load_json(cl_path)
        by_id = {c.get("cluster_id"): c for c in (cl.get("clusters") or [])}
        for cid in list(clusters):
            c = by_id.get(cid)
            if c:
                for mid in c.get("member_city_ids") or []:
                    cities.add(mid)

    green_rids: list[str] = []
    green_pairs: set[tuple[str, str]] = set()
    n_atlas_in_geo = 0
    n_skipped_nm = 0
    n_skipped_sourced = 0
    n_skipped_edge = 0

    for feat in routes:
        p = feat.get("properties") or {}
        rid = p.get("id")
        if p.get("render_hidden") is True or p.get("_quarantine") is True:
            continue
        if p.get("relevance") == "hide":
            continue
        fc = p.get("from_city_id")
        tc = p.get("to_city_id")
        cl = p.get("cluster_id")
        # Prefer both endpoints in partner cities when both stamped (Grab geography fidelity).
        in_geo = False
        if cities and fc and tc:
            in_geo = fc in cities and tc in cities
        elif cities and (fc in cities or tc in cities):
            in_geo = True
        if not in_geo and clusters and cl in clusters:
            in_geo = True
        if not in_geo and not cities and not clusters:
            continue
        if not in_geo:
            continue
        n_atlas_in_geo += 1
        nm = p.get("distance_nm")
        try:
            nm_f = float(nm) if nm is not None else None
        except (TypeError, ValueError):
            nm_f = None
        if nm_f is not None and nm_f > max_nm:
            n_skipped_nm += 1
            continue
        if nm_f is not None and nm_f < 0.5:
            # sub-0.5nm hops are marina spurs / micro — exclude from width census
            n_skipped_edge += 1
            continue
        edge = (p.get("edge_class") or "").lower() or None
        if edge in EXCLUDE_EDGE:
            n_skipped_edge += 1
            continue
        # If edge_class is set and not in include list, skip (unknown classes opt-in only when empty)
        if edge and edge not in INCLUDE_EDGE and edge not in EXCLUDE_EDGE:
            # allow empty/unknown only when distance suggests market-making (>= 2nm)
            if nm_f is None or nm_f < 2.0:
                n_skipped_edge += 1
                continue
        fr = p.get("from") or p.get("from_node")
        to = p.get("to") or p.get("to_node")
        pair = undirected_pair(fr, to)
        if rid and rid in sourced_rids:
            n_skipped_sourced += 1
            continue
        if pair and pair in sourced_pairs:
            n_skipped_sourced += 1
            continue
        if pair and pair in green_pairs:
            continue
        if pair:
            green_pairs.add(pair)
        if rid:
            green_rids.append(rid)

    n_sourced = max(len(sourced_rids), n_sourced_rows)
    # prefer unique route ids count for sourced when available
    if sourced_rids:
        n_sourced = len(sourced_rids)
    n_greenfield = len(green_pairs) if green_pairs else len(set(green_rids))

    fac = derive_factor(n_sourced, n_greenfield, alpha)
    if n_sourced == 0:
        mode = "off"
        fac = {"low": 1.0, "mid": 1.0, "high": 1.0, "count_ratio": None}
        note = "No grounded sourced corridors — greenfield OFF (null-beats-guess)."
    elif n_greenfield == 0:
        mode = "census_empty"
        fac = {"low": 1.0, "mid": 1.0, "high": 1.0, "count_ratio": 0.0}
        note = "Grounded floor exists; no additional atlas corridors in partner geography."
    else:
        mode = "census"
        note = (
            "ID-based census: grounded agg route_ids = sourced; atlas ROUTES in partner "
            f"cities/clusters within {max_nm} nm, excluding sourced pairs = greenfield."
        )

    out = {
        "partner": partner,
        "at": utc_now(),
        "status": "ok",
        "mode": mode,
        "methodology": {
            "formula": "g = 1 + (N_greenfield / N_sourced) * alpha_density",
            "max_nm": max_nm,
            "alpha_density": alpha,
            "sourced_definition": "grounded non-dup agg rows with route_id",
            "greenfield_definition": (
                "atlas ROUTES in partner geography, undirected-unique, ≤max_nm, "
                "not in sourced route_id/endpoint set"
            ),
            "replaces": "growth-config Grab default n_sourced=35 n_greenfield=341 → 4.9 mid",
        },
        "n_sourced": n_sourced,
        "n_greenfield_headline": n_greenfield,
        "n_atlas_in_geography": n_atlas_in_geo,
        "n_skipped_over_nm": n_skipped_nm,
        "n_skipped_already_sourced": n_skipped_sourced,
        "n_skipped_edge_class": n_skipped_edge,
        "n_partner_cities": len(cities),
        "n_partner_clusters": len(clusters),
        "count_ratio": fac.get("count_ratio"),
        "ratio_effective": fac.get("ratio_effective"),
        "tail_softened": fac.get("tail_softened", False),
        "alpha_density": alpha,
        "derived_greenfield_factor": {"headline_tier1_plus_tier2": {
            "low": fac["low"], "mid": fac["mid"], "high": fac["high"]
        }},
        "sourced_route_ids_sample": sorted(sourced_rids)[:40],
        "greenfield_route_ids_sample": green_rids[:40],
        "note": note,
        "agg_path": str(agg_path),
    }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", help="output path for single partner")
    ap.add_argument("--max-nm", type=float, default=MAX_NM_DEFAULT)
    ap.add_argument("--outdir", default=str(CENSUS_DIR))
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    partners: list[str] = []
    if args.all:
        for p in sorted(RECAL.glob("agg-*.json")):
            name = p.stem[len("agg-") :]
            if name in ("unique-global", "global", "gojek-deck", "gojek-deck-merged"):
                continue
            partners.append(name)
    elif args.partner:
        partners = [args.partner]
    else:
        ap.error("need --partner or --all")

    index = {"at": utc_now(), "partners": {}, "methodology": "greenfield_census.py"}
    for partner in partners:
        doc = census_partner(partner, max_nm=args.max_nm)
        path = Path(args.json) if args.json and len(partners) == 1 else outdir / f"{partner}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        fac = doc["derived_greenfield_factor"]["headline_tier1_plus_tier2"]
        index["partners"][partner] = {
            "mode": doc.get("mode"),
            "n_sourced": doc.get("n_sourced"),
            "n_greenfield": doc.get("n_greenfield_headline"),
            "g_mid": fac.get("mid"),
            "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        }
        print(
            f"{partner:28} mode={doc.get('mode'):12} "
            f"sourced={doc.get('n_sourced'):4} green={doc.get('n_greenfield_headline'):5} "
            f"g_mid={fac.get('mid')}"
        )

    idx_path = outdir / "INDEX.json"
    idx_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(partners)} censuses → {outdir}")
    print(f"Index → {idx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
