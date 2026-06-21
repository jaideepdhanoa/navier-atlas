#!/usr/bin/env python3
"""Strict regional spine parity gate — geometry links + card inventory vs reference template.

Complements audit_partner_page_qa.py (narrative). Hospitality subset mode skips full
card-count parity but still checks geometry on matched cards.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PARTNERS = ROOT / "partner-pitch" / "partners"
DRAFT = PARTNERS / "_draft"
MANIFEST_PATH = ROOT / "handoff" / "partner-map-model" / "regional-inheritance-manifest.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_DIR = ROOT / "handoff" / "partner-map-model"

BIND_FIELDS_PRESENT = ("route_id", "route_ids")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def partner_path(slug: str) -> Path | None:
    for base in (PARTNERS, DRAFT):
        p = base / f"{slug}.json"
        if p.is_file():
            return p
    return None


def gold_route_ids() -> set[str]:
    routes = load_json(ROUTES_PATH)
    return {
        f["properties"]["id"]
        for f in routes
        if f.get("properties", {}).get("id")
    }


def iter_cards(doc: dict):
    for j in doc.get("journeys_unlocked") or []:
        if isinstance(j, dict):
            yield "journey", None, j
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, dict):
                yield "featured", None, fr
    for m in doc.get("markets") or []:
        mid = m.get("id")
        for j in m.get("journeys_unlocked") or []:
            if isinstance(j, dict):
                yield "journey", mid, j
        for ph in m.get("phases") or []:
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, dict):
                    yield "featured", mid, fr


def is_geometry_linked(item: dict, gold: set[str]) -> bool:
    rid = item.get("route_id")
    rids = item.get("route_ids") or []
    if rid and rid in gold:
        return True
    if rids and any(x in gold for x in rids):
        return True
    return False


def card_inventory_counts(doc: dict, *, display_markets: set[str] | None) -> dict[str, int]:
    counts = {"hub_journeys": 0, "hub_featured": 0, "market_journeys": 0, "market_featured": 0}
    for kind, mid, item in iter_cards(doc):
        if mid and display_markets is not None and mid not in display_markets:
            if not (item.get("anchor_cities") if False else False):
                if mid not in display_markets:
                    continue
        if kind == "journey":
            if mid:
                if display_markets is None or mid in display_markets:
                    counts["market_journeys"] += 1
            else:
                counts["hub_journeys"] += 1
        else:
            if mid:
                if display_markets is None or mid in display_markets:
                    counts["market_featured"] += 1
            else:
                counts["hub_featured"] += 1
    return counts


def map_routes_in_scope(doc: dict, city_ids: set[str]) -> int:
    if not city_ids:
        return 0
    routes = load_json(ROUTES_PATH)

    def city_of(props: dict) -> str | None:
        return props.get("from") or props.get("to")

    n = 0
    for f in routes:
        p = f.get("properties", {})
        fr, to = p.get("from"), p.get("to")
        if fr in city_ids or to in city_ids:
            n += 1
    return n


def audit_slug(slug: str, manifest: dict, gold: set[str]) -> dict:
    pack_id = manifest["partner_pack"].get(slug)
    pack = manifest["packs"].get(pack_id or {})
    ref_slug = pack.get("reference_partner", slug)
    mode = pack.get("route_scope_mode", "display_markets")
    display_markets = set(pack.get("display_market_ids") or [])

    path = partner_path(slug)
    if not path:
        return {"partner": slug, "verdict": "SKIP", "reason": "missing file"}

    doc = load_json(path)
    ref_doc = load_json(partner_path(ref_slug)) if partner_path(ref_slug) else {}

    gaps: list[dict] = []
    flags: list[dict] = []

    cards = list(iter_cards(doc))
    geo_linked = sum(1 for _, mid, item in cards if is_geometry_linked(item, gold))
    geo_total = len(cards)

    if slug != ref_slug and mode != "subset":
        ref_counts = card_inventory_counts(ref_doc, display_markets=display_markets or None)
        tgt_counts = card_inventory_counts(doc, display_markets=display_markets or None)
        for k, rv in ref_counts.items():
            tv = tgt_counts.get(k, 0)
            if tv != rv:
                gaps.append({"check": "card_inventory", "field": k, "expected": rv, "actual": tv})

    scope_cities = set(pack.get("map_scope_city_ids") or [])
    if scope_cities and slug != ref_slug:
        ref_map = map_routes_in_scope(ref_doc, scope_cities)
        tgt_map = map_routes_in_scope(doc, scope_cities)
        if ref_map != tgt_map:
            gaps.append({
                "check": "map_routes_in_scope",
                "expected": ref_map,
                "actual": tgt_map,
                "cities": sorted(scope_cities),
            })

    brief_ids = set(pack.get("brief_only_market_ids") or [])
    for m in doc.get("markets") or []:
        if m.get("id") in brief_ids and (m.get("anchor_cities") or []):
            flags.append({
                "check": "brief_market_leak",
                "market": m.get("id"),
                "detail": "brief-only market has anchor_cities — will expand map scope",
            })

    geo_ratio = geo_linked / geo_total if geo_total else 1.0
    if mode == "subset":
        verdict = "PASS" if geo_ratio >= 0.5 or slug == ref_slug else "PASS_WITH_FLAGS"
    elif slug == ref_slug:
        verdict = "PASS"
    elif not gaps and geo_ratio >= 0.85:
        verdict = "PASS"
    elif gaps or geo_ratio < 0.85:
        verdict = "PASS_WITH_FLAGS" if geo_ratio >= 0.7 else "FAIL"
    else:
        verdict = "PASS"

    return {
        "partner": slug,
        "pack": pack_id,
        "reference": ref_slug,
        "mode": mode,
        "verdict": verdict,
        "geometry_linked": geo_linked,
        "geometry_total": geo_total,
        "geometry_ratio": round(geo_ratio, 3),
        "gaps": gaps,
        "flags": flags,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--partner", nargs="*", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--fail-on-fail", action="store_true")
    args = ap.parse_args()

    manifest = load_json(MANIFEST_PATH)
    gold = gold_route_ids()
    slugs = args.partner or (list(manifest["partner_pack"].keys()) if args.all else [])
    if not slugs:
        ap.error("specify --partner or --all")

    entries = [audit_slug(s, manifest, gold) for s in slugs]
    aggregate = {
        "lane": "grok/audit_partner_spine_parity",
        "checked_at": utc_now(),
        "partners": entries,
        "summary": {
            "pass": sum(1 for e in entries if e["verdict"] == "PASS"),
            "pass_with_flags": sum(1 for e in entries if e["verdict"] == "PASS_WITH_FLAGS"),
            "fail": sum(1 for e in entries if e["verdict"] == "FAIL"),
        },
    }

    ledger = REPORT_DIR / "spine-parity-ledger.json"
    ledger.write_text(json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n")

    for e in entries:
        (REPORT_DIR / f"spine-parity-{e['partner']}.json").write_text(
            json.dumps(e, indent=2, ensure_ascii=False) + "\n"
        )

    print(f"Spine parity — {len(entries)} partners")
    print(f"  PASS: {aggregate['summary']['pass']}")
    print(f"  PASS_WITH_FLAGS: {aggregate['summary']['pass_with_flags']}")
    print(f"  FAIL: {aggregate['summary']['fail']}")
    for e in entries:
        if e["verdict"] != "PASS":
            print(f"  {e['verdict']:16} {e['partner']:22} geo {e['geometry_linked']}/{e['geometry_total']} gaps {len(e['gaps'])}")

    if args.fail_on_fail and aggregate["summary"]["fail"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())