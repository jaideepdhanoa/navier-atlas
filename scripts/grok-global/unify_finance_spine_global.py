#!/usr/bin/env python3
"""Generalize UAE finance spine unification to all multi-partner geographies."""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_finance_inheritance import (  # noqa: E402
    MARKET_GEO_OVERRIDES,
    market_to_geography,
    market_to_partner,
)

CORRIDORS_PATH = ROOT / "finance" / "model" / "corridors.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "grok-routing-output" / "global-finance-spine-unify-report.json"

OVERLAY_FIELDS = (
    "L3_locals",
    "archetype",
    "pool_basis",
    "pool_id",
    "capture_rate",
    "fleet_basis",
    "fleet_rounding",
    "aspirational",
    "_notes",
    "_inherited_from_gcn",
    "_cross_border_to",
    "_cross_border_from",
)

CROSS_BORDER_RE = re.compile(r"qatar|bahrain|doha|manama", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm_label(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s.strip().lower())


def corridor_signature(c: dict) -> tuple:
    return (
        norm_label(c.get("from")),
        norm_label(c.get("to")),
        c.get("from_node_id"),
        c.get("to_node_id"),
    )


def is_cross_border_uae(c: dict) -> bool:
    blob = json.dumps(c)
    return bool(CROSS_BORDER_RE.search(blob))


def route_id_rank(rid: str | None) -> tuple[int, str]:
    if not rid:
        return (9, "")
    if rid.startswith("rn-"):
        return (0, rid)
    if rid.startswith("gcn-"):
        return (1, rid)
    if rid.startswith("edge-"):
        return (2, rid)
    return (4, rid)


def load_geometry_route_index() -> dict[tuple[str, str], str]:
    raw = json.loads(ROUTES_PATH.read_text())
    routes = raw if isinstance(raw, list) else raw.get("features", [])
    idx: dict[tuple[str, str], str] = {}
    for r in routes:
        p = r.get("properties", r)
        rid = p.get("id")
        if not rid or not str(rid).startswith("rn-"):
            continue
        fl = norm_label(p.get("from") or p.get("from_label"))
        tl = norm_label(p.get("to") or p.get("to_label"))
        if fl and tl:
            idx[(fl, tl)] = rid
            idx[(tl, fl)] = rid
    return idx


def pick_canonical_route_id(entries: list[tuple[str, dict]], geom_idx: dict) -> str | None:
    candidates: list[str] = []
    for _, c in entries:
        rid = c.get("route_id")
        if rid:
            candidates.append(rid)

    rn_candidates = [r for r in candidates if r.startswith("rn-")]
    if rn_candidates:
        return sorted(rn_candidates, key=route_id_rank)[0]

    if entries:
        sig = corridor_signature(entries[0][1])
        geom_rid = geom_idx.get((sig[0], sig[1]))
        if geom_rid:
            return geom_rid

    if not candidates:
        return None
    return sorted(candidates, key=route_id_rank)[0]


def spine_metadata(entries: list[tuple[str, dict]], canonical_rid: str | None) -> dict:
    base = copy.deepcopy(entries[0][1])
    spine = {k: v for k, v in base.items() if k not in OVERLAY_FIELDS and k != "route_id"}
    spine["route_id"] = canonical_rid
    return spine


def partner_overlay(partner_row: dict | None, spine_row: dict) -> dict:
    out = copy.deepcopy(spine_row["metadata"])
    if partner_row:
        for field in OVERLAY_FIELDS:
            if field in partner_row:
                out[field] = copy.deepcopy(partner_row[field])
    return out


def unify_geography(
    geo: str,
    market_keys: list[str],
    markets: dict,
    geom_idx: dict,
) -> tuple[dict, dict]:
    grouped: dict[tuple, list[tuple[str, dict]]] = defaultdict(list)
    dropped_xb: list[dict] = []

    for key in market_keys:
        for c in markets[key].get("corridors", []):
            if geo == "uae" and is_cross_border_uae(c):
                dropped_xb.append(
                    {"market": key, "route_id": c.get("route_id"), "from": c.get("from"), "to": c.get("to")}
                )
                continue
            grouped[corridor_signature(c)].append((key, c))

    spine: dict[tuple, dict] = {}
    for sig, entries in grouped.items():
        canonical_rid = pick_canonical_route_id(entries, geom_idx)
        spine[sig] = {
            "route_id": canonical_rid,
            "metadata": spine_metadata(entries, canonical_rid),
            "sources": {k: c.get("route_id") for k, c in entries},
        }

    report = {
        "geography": geo,
        "market_keys": market_keys,
        "spine_count": len(spine),
        "dropped_cross_border": len(dropped_xb),
        "spine_identical": True,
        "per_market_after": {},
    }

    for key in market_keys:
        before = markets[key].get("corridors", [])
        partner_by_sig = {
            corridor_signature(c): c
            for c in before
            if not (geo == "uae" and is_cross_border_uae(c))
        }
        new_corridors = []
        for sig, spine_row in sorted(spine.items(), key=lambda x: (x[1]["metadata"].get("from", ""), x[1]["metadata"].get("to", ""))):
            row = partner_overlay(partner_by_sig.get(sig), spine_row)
            new_corridors.append(row)
        markets[key]["corridors"] = new_corridors
        report["per_market_after"][key] = {
            "total": len(new_corridors),
            "with_route_id": sum(1 for c in new_corridors if c.get("route_id")),
        }

    spine_sets = {
        key: tuple(sorted(c.get("route_id") for c in markets[key]["corridors"] if c.get("route_id")))
        for key in market_keys
    }
    report["spine_identical"] = len(set(spine_sets.values())) == 1
    return report, report["spine_identical"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    doc = json.loads(CORRIDORS_PATH.read_text())
    markets = doc.get("markets") or {}
    geom_idx = load_geometry_route_index()

    by_geo: dict[str, list[str]] = defaultdict(list)
    for key in markets:
        by_geo[market_to_geography(key)].append(key)

    reports: list[dict] = []
    all_ok = True
    for geo in sorted(by_geo):
        keys = sorted(by_geo[geo])
        partners = {market_to_partner(k) for k in keys}
        if len(partners) < 2:
            continue
        rep, ok = unify_geography(geo, keys, markets, geom_idx)
        reports.append(rep)
        all_ok = all_ok and ok
        print(
            f"  {geo}: keys={len(keys)} spine={rep['spine_count']} "
            f"identical={rep['spine_identical']}"
        )

    receipt = {
        "generated_at": utc_now(),
        "geographies_unified": len(reports),
        "all_spines_identical": all_ok,
        "geographies": reports,
    }

    if args.apply:
        CORRIDORS_PATH.write_text(json.dumps(doc, indent=2) + "\n")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"geographies": len(reports), "all_ok": all_ok}, indent=2))
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())