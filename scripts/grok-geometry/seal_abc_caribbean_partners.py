#!/usr/bin/env python3
"""Bind ABC seal routes on ocean-whisperer + caribbean partners; retire caribbean-mobility."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_routing_shared import load_json, route_features, save_json  # noqa: E402

MINT_REPORT = ROOT / "grok-routing-output/abc-islands-seal-report.json"
REPORT_PATH = ROOT / "grok-routing-output/abc-caribbean-partner-seal-report.json"
TAG = "abc_islands"
LUMP = "aruba-curacao-bonaire"
NEW_CITIES = ("aruba-aruba", "curacao-curacao", "bonaire-bonaire")

NODE_ALIASES = {
    "curacao-curacao__spanish-water-caracasbaai": "curacao-curacao__spanish-water-jan-thiel",
}

PARTNERS = {
    "ocean-whisperer": ROOT / "partner-pitch/partners/ocean-whisperer.json",
    "caribbean": ROOT / "partner-pitch/partners/caribbean.json",
}

# Shared geometry, scoped render — OW treats inter-island network legs as roadmap-only.
OW_ROADMAP_LEGS = {
    frozenset(
        {
            "curacao-curacao__spanish-water-jan-thiel",
            "bonaire-bonaire__kralendijk-town-pier",
        }
    ),
    frozenset(
        {
            "curacao-curacao__spanish-water-jan-thiel",
            "aruba-aruba__oranjestad-renaissance-marina",
        }
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_node(node: str | None) -> str | None:
    if not node:
        return node
    return NODE_ALIASES.get(node, node)


def build_route_index() -> dict[tuple[str, str], dict]:
    routes = route_features(load_json(ROOT / "data-clean/ROUTES.json"))
    idx: dict[tuple[str, str], dict] = {}
    for feat in routes:
        p = feat.get("properties", feat)
        fn, tn = p.get("from_node") or p.get("from"), p.get("to_node") or p.get("to")
        if fn and tn:
            idx[(fn, tn)] = p
            idx[(tn, fn)] = p
    return idx


def bind_journeys(partner: dict, route_idx: dict[tuple[str, str], dict], *, partner_id: str = "") -> dict:
    stats = {"bound": 0, "roadmap": 0, "seasonal": 0, "still_pending": 0}
    pending_statuses = {
        "PENDING_SEAL",
        "aspirational-no-built-route",
        "pending-seal",
    }

    def bind_one(j: dict) -> None:
        st = j.get("_link_status", "")
        if st not in pending_statuses and st != "linked-grok-scoped" and not j.get("route_id"):
            return
        fc = resolve_node(j.get("from_node_id"))
        tc = resolve_node(j.get("to_node_id"))
        if not fc or not tc:
            stats["still_pending"] += 1
            return
        props = route_idx.get((fc, tc))
        render = j.get("render") or ""
        if props:
            rid = props.get("id")
            tier = props.get("_tier") or ("roadmap" if props.get("_aspirational") else "grounded")
            if partner_id == "ocean-whisperer" and frozenset({fc, tc}) in OW_ROADMAP_LEGS:
                tier = "roadmap"
            j["route_id"] = rid
            j["route_ids"] = [rid]
            j["distance_nm"] = props.get("distance_nm", j.get("distance_nm"))
            j["_link_status"] = "linked-grok-scoped"
            j["_link_source"] = f"grok/{TAG}"
            j.pop("display", None)
            if tier == "roadmap":
                j["economics_status"] = "roadmap_excluded"
                j["render"] = "roadmap-amber-dashed"
                stats["roadmap"] += 1
            elif tier == "seasonal" or props.get("_seasonal"):
                j["economics_status"] = "economics_pending"
                j["render"] = "seasonal-amber"
                stats["seasonal"] += 1
            else:
                j["economics_status"] = "economics_pending"
                j["render"] = "solid"
                stats["bound"] += 1
        elif render in ("roadmap-amber-dashed",):
            j["route_id"] = None
            j["_link_status"] = "roadmap-quanta-lr"
            j["economics_status"] = "roadmap_excluded"
            stats["roadmap"] += 1
        else:
            stats["still_pending"] += 1

    for j in partner.get("journeys_unlocked", []):
        bind_one(j)
    for phase in partner.get("phases", []):
        for j in phase.get("featured_routes", []):
            bind_one(j)
    return stats


def retire_caribbean_mobility(apply: bool) -> dict:
    path = ROOT / "data-clean/partners/caribbean-mobility.json"
    pitch = ROOT / "partner-pitch/partners/caribbean-mobility.json"
    actions = {"retired": False}
    if not path.exists():
        return actions
    doc = load_json(path)
    doc["_status"] = "retired"
    doc["_superseded_by"] = "caribbean"
    doc["_retired_at"] = utc_now()
    doc["_retire_note"] = "Lumped aruba-curacao-bonaire market superseded by caribbean + ocean-whisperer ABC seal (PR #93)."
    if apply:
        save_json(path, doc)
        if pitch.exists():
            save_json(pitch, doc)
        actions["retired"] = True
    return actions


def replace_lump_refs(obj, stats: dict) -> None:
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if v == LUMP:
                obj[k] = list(NEW_CITIES)
                stats["list_expansions"] = stats.get("list_expansions", 0) + 1
            elif isinstance(v, str) and v == LUMP:
                obj[k] = "aruba-aruba"
                stats["str_replacements"] = stats.get("str_replacements", 0) + 1
            else:
                replace_lump_refs(v, stats)
    elif isinstance(obj, list):
        out = []
        changed = False
        for item in obj:
            if item == LUMP:
                out.extend(NEW_CITIES)
                changed = True
            else:
                replace_lump_refs(item, stats)
                out.append(item)
        if changed:
            obj[:] = out
            stats["list_expansions"] = stats.get("list_expansions", 0) + 1


def patch_inheritance_partners(apply: bool) -> dict:
    stats: dict = {}
    for rel in (
        "data-clean/partners/cabify.json",
        "data-clean/partners/didi.json",
        "data-clean/partners/lyft.json",
    ):
        path = ROOT / rel
        if not path.exists():
            continue
        doc = load_json(path)
        before = json.dumps(doc).count(LUMP)
        if not before:
            continue
        replace_lump_refs(doc, stats)
        if apply:
            save_json(path, doc)
        stats[rel] = before
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not MINT_REPORT.exists():
        print(f"FATAL: run mint_abc_islands_geometry.py first ({MINT_REPORT})")
        return 1

    route_idx = build_route_index()
    report = {
        "at": utc_now(),
        "lane": f"grok/{TAG}_partners",
        "apply": args.apply,
        "partners": {},
        "caribbean_mobility": retire_caribbean_mobility(False),
        "inheritance_patches": patch_inheritance_partners(False),
    }

    for pid, src in PARTNERS.items():
        partner = load_json(src)
        stats = bind_journeys(partner, route_idx, partner_id=pid)
        report["partners"][pid] = stats
        if args.apply:
            save_json(src, partner)
            dst = ROOT / f"data-clean/partners/{pid}.json"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    if args.apply:
        report["caribbean_mobility"] = retire_caribbean_mobility(True)
        report["inheritance_patches"] = patch_inheritance_partners(True)

    report["still_pending_total"] = sum(
        s.get("still_pending", 0) for s in report["partners"].values()
    )
    save_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))
    return 0 if report["still_pending_total"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())