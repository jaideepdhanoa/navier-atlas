#!/usr/bin/env python3
"""Unify UAE finance corridor spine across partner market keys.

For uae-careem, bolt-uae, yango-uae, uae-noon, uae-luxury: derive one
deduped route_id spine (union of all partners, aligned to geometry rn-* where
possible) while preserving per-partner L3_locals / capture_rate / archetype overlays.

Drops cross-border Qatar/Bahrain routes from UAE finance keys.
"""
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
CORRIDORS_PATH = ROOT / "finance/model/corridors.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
REPORT_PATH = ROOT / "grok-routing-output/uae-finance-spine-unify-report.json"

UAE_KEYS = ("uae-careem", "bolt-uae", "yango-uae", "uae-noon", "uae-luxury")
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

CROSS_BORDER_RE = re.compile(
    r"qatar|bahrain|doha|manama",
    re.IGNORECASE,
)


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


def is_cross_border(c: dict) -> bool:
    blob = json.dumps(
        {
            "from": c.get("from"),
            "to": c.get("to"),
            "from_node_id": c.get("from_node_id"),
            "to_node_id": c.get("to_node_id"),
            "route_id": c.get("route_id"),
            "country": c.get("country"),
        }
    )
    if CROSS_BORDER_RE.search(blob):
        return True
    country = (c.get("country") or "").lower()
    return country not in ("", "united arab emirates", "uae")


def normalize_route_id(rid: str | None) -> str | None:
    if not rid:
        return None
    if rid.startswith("rn-"):
        return rid
    m = re.match(r"^(gcn-[a-f0-9]+)", rid)
    if m:
        return m.group(1)
    m = re.match(r"^(edge-[a-f0-9]+)", rid)
    if m:
        return m.group(1)
    return rid


def route_id_rank(rid: str | None) -> tuple[int, str]:
    if not rid:
        return (9, "")
    if rid.startswith("rn-"):
        return (0, rid)
    if rid.startswith("gcn-"):
        return (1, rid)
    if rid.startswith("edge-"):
        return (2, rid)
    if rid.startswith("e__"):
        return (3, rid)
    return (4, rid)


def load_geometry_route_index() -> dict[tuple[str, str], str]:
    """Map normalized endpoint labels -> geometry rn-* route_id."""
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


def pick_canonical_route_id(entries: list[tuple[str, dict]]) -> str | None:
    """Prefer careem rn-* then geometry rn-* then best-ranked id."""
    candidates: list[str] = []
    for key, c in entries:
        rid = c.get("route_id")
        if rid:
            candidates.append(rid)
        if key == "uae-careem" and rid and rid.startswith("rn-"):
            return rid

    rn_candidates = [r for r in candidates if r.startswith("rn-")]
    if rn_candidates:
        return sorted(rn_candidates, key=route_id_rank)[0]

    geom_idx = load_geometry_route_index()
    if entries:
        sig = corridor_signature(entries[0][1])
        geom_rid = geom_idx.get((sig[0], sig[1]))
        if geom_rid:
            return geom_rid

    if not candidates:
        return None
    return sorted(candidates, key=route_id_rank)[0]


def spine_metadata(entries: list[tuple[str, dict]], canonical_rid: str | None) -> dict:
    priority = ("uae-careem", "uae-luxury", "bolt-uae", "yango-uae", "uae-noon")
    by_key = {k: c for k, c in entries}
    for key in priority:
        if key in by_key:
            base = copy.deepcopy(by_key[key])
            break
    else:
        base = copy.deepcopy(entries[0][1])

    spine = {
        k: v
        for k, v in base.items()
        if k not in OVERLAY_FIELDS and k != "route_id"
    }
    spine["route_id"] = canonical_rid
    return spine


def build_spine(markets: dict) -> tuple[dict[tuple, dict], list[dict]]:
    grouped: dict[tuple, list[tuple[str, dict]]] = defaultdict(list)
    dropped_xb: list[dict] = []

    for key in UAE_KEYS:
        for c in markets[key].get("corridors", []):
            if is_cross_border(c):
                dropped_xb.append({"market": key, "route_id": c.get("route_id"), "from": c.get("from"), "to": c.get("to")})
                continue
            grouped[corridor_signature(c)].append((key, c))

    spine: dict[tuple, dict] = {}
    for sig, entries in grouped.items():
        canonical_rid = pick_canonical_route_id(entries)
        spine[sig] = {
            "signature": {
                "from": entries[0][1].get("from"),
                "to": entries[0][1].get("to"),
                "from_node_id": sig[2],
                "to_node_id": sig[3],
            },
            "route_id": canonical_rid,
            "metadata": spine_metadata(entries, canonical_rid),
            "sources": {k: c.get("route_id") for k, c in entries},
        }
    return spine, dropped_xb


def partner_overlay(partner_row: dict | None, spine_row: dict) -> dict:
    out = copy.deepcopy(spine_row["metadata"])
    if partner_row:
        for field in OVERLAY_FIELDS:
            if field in partner_row:
                out[field] = copy.deepcopy(partner_row[field])
    return out


def unify_markets(doc: dict) -> tuple[dict, dict]:
    markets = doc["markets"]
    spine, dropped_xb = build_spine(markets)
    report = {
        "generated_at": utc_now(),
        "uae_keys": list(UAE_KEYS),
        "spine_count": len(spine),
        "dropped_cross_border": dropped_xb,
        "per_partner_before": {},
        "per_partner_after": {},
        "route_id_alignment": [],
    }

    for key in UAE_KEYS:
        before = markets[key].get("corridors", [])
        report["per_partner_before"][key] = {
            "total": len(before),
            "with_route_id": sum(1 for c in before if c.get("route_id")),
            "cross_border": sum(1 for c in before if is_cross_border(c)),
        }

        partner_by_sig = {
            corridor_signature(c): c
            for c in before
            if not is_cross_border(c)
        }
        new_corridors = []
        for sig, spine_row in sorted(spine.items(), key=lambda x: (x[1]["signature"]["from"], x[1]["signature"]["to"])):
            row = partner_overlay(partner_by_sig.get(sig), spine_row)
            old_rid = partner_by_sig.get(sig, {}).get("route_id") if sig in partner_by_sig else None
            if old_rid and row.get("route_id") and old_rid != row["route_id"]:
                report["route_id_alignment"].append(
                    {
                        "market": key,
                        "from": row.get("from"),
                        "to": row.get("to"),
                        "old_route_id": old_rid,
                        "new_route_id": row.get("route_id"),
                    }
                )
            new_corridors.append(row)
        markets[key]["corridors"] = new_corridors
        report["per_partner_after"][key] = {
            "total": len(new_corridors),
            "with_route_id": sum(1 for c in new_corridors if c.get("route_id")),
            "null_route_id": sum(1 for c in new_corridors if not c.get("route_id")),
        }

    spine_sets = {
        key: sorted(c.get("route_id") for c in markets[key]["corridors"] if c.get("route_id"))
        for key in UAE_KEYS
    }
    report["spine_identical"] = len({tuple(v) for v in spine_sets.values()}) == 1
    report["common_route_ids"] = len(set(spine_sets[UAE_KEYS[0]]) & set(spine_sets[UAE_KEYS[1]]))
    return doc, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    doc = json.loads(CORRIDORS_PATH.read_text())
    updated, report = unify_markets(doc)

    if args.apply:
        CORRIDORS_PATH.write_text(json.dumps(updated, indent=2) + "\n")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

    print(
        f"\n{'✓' if args.apply else '·'} uae finance spine: "
        f"{report['spine_count']} corridors | "
        f"dropped_xb={len(report['dropped_cross_border'])} | "
        f"spine_identical={report['spine_identical']}"
    )
    return 0 if report["spine_identical"] else 2


if __name__ == "__main__":
    raise SystemExit(main())