#!/usr/bin/env python3
"""Audit partner/market route bindings for Singapore-class mislinks.

Flags:
  - wrong_binding: clickable journey/featured route where geometry doesn't match authored from/to
  - cross_border_leak: intra-scoped market/chip containing foreign-corridor routes
  - mislinked_clickable: route_id set but fails render gates (hidden on map)
  - missing_route: route_id not in graph

Usage:
  python3 scripts/audit_market_route_bindings.py [--partner grab] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import relink_partner_journeys as r  # noqa: E402

PARTNERS_DIR = ROOT / "data-clean/partners"
REPORT_PATH = ROOT / "navier/handoff/journey-relink/market-binding-audit.json"

CROSS_BORDER_RE = re.compile(
    r"harbour bay|batam|bintan|bandar bentan|desaru|johor|sekupang|nongsa|"
    r"pasir gudang|riau islands|tanjung pinang|penang(?! hill)|langkawi|"
    r"koh lipe|manama|bahrain|soul beach abu dhabi",
    re.I,
)

# Markets that are explicitly cross-border — foreign endpoints expected
CROSS_BORDER_MARKETS = frozenset({
    "cross-border", "cross_border", "mena", "uae", "ksa-red-sea", "ksa-commercial",
    "brazil-latam", "mexico", "mediterranean", "cote-dazur", "istanbul",
    "riau", "borneo", "philippines-cross", "singapore-cross",
})


def walk_bindings(partner: dict, partner_id: str) -> list[dict]:
    rows: list[dict] = []

    def emit(obj: dict, *, market_id: str | None, scope: str | None, ctx: str, kind: str):
        if obj.get("route_id"):
            rows.append({
                "partner": partner_id,
                "market": market_id,
                "scope": scope,
                "kind": kind,
                "context": ctx,
                "label": obj.get("label"),
                "from": obj.get("from") or obj.get("from_label"),
                "to": obj.get("to") or obj.get("to_label"),
                "from_node_id": obj.get("from_node_id"),
                "to_node_id": obj.get("to_node_id"),
                "route_id": obj["route_id"],
                "distance_nm": obj.get("distance_nm"),
            })
        if obj.get("display") == "network_chip" and obj.get("route_ids"):
            for rid in obj["route_ids"]:
                rows.append({
                    "partner": partner_id,
                    "market": market_id,
                    "scope": scope,
                    "kind": "chip_leg",
                    "context": ctx,
                    "chip_label": obj.get("label"),
                    "route_id": rid,
                })

    def walk(obj, market_id: str | None, scope: str | None, ctx_parts: list[str]):
        if isinstance(obj, dict):
            label = obj.get("label") or (f"phase-{obj['n']}" if obj.get("n") else None)
            parts = ctx_parts + ([label] if label else [])
            ctx = " / ".join(parts[-4:])
            rs = obj.get("route_scope") or scope

            if obj.get("journeys_unlocked"):
                for j in obj["journeys_unlocked"]:
                    emit(j, market_id=market_id, scope=rs, ctx=ctx, kind="journey")
            if obj.get("featured_routes"):
                for fr in obj["featured_routes"]:
                    if fr.get("display") == "network_chip":
                        emit(fr, market_id=market_id, scope=rs, ctx=ctx, kind="chip")
                    else:
                        emit(fr, market_id=market_id, scope=rs, ctx=ctx, kind="featured")

            for ph in obj.get("phases") or []:
                pl = ph.get("label") or f"phase-{ph.get('n')}"
                for fr in ph.get("featured_routes") or []:
                    if fr.get("display") == "network_chip":
                        emit(fr, market_id=market_id, scope=ph.get("route_scope") or rs,
                             ctx=f"{ctx} / {pl}", kind="chip")
                    else:
                        emit(fr, market_id=market_id, scope=ph.get("route_scope") or rs,
                             ctx=f"{ctx} / {pl}", kind="featured")

            for m in obj.get("markets") or []:
                mid = m.get("id") or m.get("slug")
                walk(m, mid, None, parts + [m.get("label", mid)])

        elif isinstance(obj, list):
            for x in obj:
                walk(x, market_id, scope, ctx_parts)

    walk(partner, None, None, [partner_id])
    return rows


def is_domestic_scope(scope: str | None, market_id: str | None) -> bool:
    if market_id and market_id.lower() in CROSS_BORDER_MARKETS:
        return False
    if (scope or "").lower() in ("all", "regional", "cross", "cross-border"):
        return False
    return True


def audit_row(row: dict, routes: dict) -> list[dict]:
    issues: list[dict] = []
    rid = row["route_id"]
    rec = routes.get(rid)
    kind = row["kind"]

    if not rec:
        if kind in ("journey", "featured", "chip_leg"):
            issues.append({**row, "issue": "missing_route", "severity": "high"})
        return issues

    label_text = row.get("label") or row.get("chip_label") or ""
    from_l, to_l, full_label = r.item_labels({
        "label": label_text,
        "from": row.get("from"),
        "to": row.get("to"),
        "from_label": row.get("from"),
        "to_label": row.get("to"),
    })
    ep = f"{rec.from_label} {rec.to_label}"
    domestic = is_domestic_scope(row.get("scope"), row.get("market"))

    render_item = {
        "route_id": rid,
        "label": label_text,
        "from": row.get("from"),
        "to": row.get("to"),
        "from_node_id": row.get("from_node_id"),
        "to_node_id": row.get("to_node_id"),
        "distance_nm": row.get("distance_nm") or rec.distance_nm,
    }
    bucket = r.render_bucket(render_item, routes)

    base = {
        **row,
        "route_from": rec.from_label,
        "route_to": rec.to_label,
        "route_nm": rec.distance_nm,
        "render_bucket": bucket,
    }

    # Tier 1: wrong clickable binding (journey / featured only)
    if kind in ("journey", "featured") and from_l and to_l:
        if not r.directional_endpoints_match(from_l, to_l, rec):
            issues.append({
                **base,
                "issue": "wrong_binding",
                "severity": "critical",
                "parsed_from": from_l,
                "parsed_to": to_l,
            })
        elif bucket == "mislinked_dropped":
            issues.append({**base, "issue": "mislinked_clickable", "severity": "high"})

    # Tier 1b: journey with from/to but only label (hub cards)
    if kind == "journey" and not from_l and row.get("from"):
        from_l2, to_l2, _ = r.item_labels({"from": row["from"], "to": row.get("to"), "label": label_text})
        if from_l2 and to_l2 and not r.directional_endpoints_match(from_l2, to_l2, rec):
            issues.append({
                **base,
                "issue": "wrong_binding",
                "severity": "critical",
                "parsed_from": from_l2,
                "parsed_to": to_l2,
            })

    # Tier 2: cross-border geometry inside domestic scope
    if domestic and CROSS_BORDER_RE.search(ep):
        chip_domestic = row.get("chip_label") and not CROSS_BORDER_RE.search(row["chip_label"])
        journey_domestic = row.get("from") or row.get("to") or "domestic" in label_text.lower()
        if kind == "chip_leg" and chip_domestic:
            issues.append({**base, "issue": "cross_border_chip_leak", "severity": "high"})
        elif kind in ("journey", "featured") and journey_domestic:
            issues.append({**base, "issue": "cross_border_leak", "severity": "high"})

    # Tier 3: intra-city nodes but foreign route
    fn, tn = row.get("from_node_id"), row.get("to_node_id")
    if kind in ("journey", "featured") and fn and tn and fn == tn and domestic:
        if CROSS_BORDER_RE.search(ep):
            issues.append({**base, "issue": "intra_nodes_foreign_route", "severity": "high"})

    # Chip legs failing gates (informational unless cross-border)
    if kind == "chip_leg" and bucket == "mislinked_dropped" and not CROSS_BORDER_RE.search(ep):
        issues.append({**base, "issue": "chip_leg_mislinked", "severity": "low"})

    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="*", help="Limit to partner slug(s)")
    ap.add_argument("--json", action="store_true", help="Print full JSON to stdout")
    args = ap.parse_args()

    routes, _, _ = r.load_routes(r.ROOT)
    all_issues: list[dict] = []

    paths = sorted(PARTNERS_DIR.glob("*.json"))
    if args.partner:
        paths = [PARTNERS_DIR / f"{p}.json" for p in args.partner]

    for path in paths:
        if not path.exists() or path.suffix != ".json":
            continue
        partner_id = path.stem
        if partner_id.endswith(".bak-pre-marine-tam-split"):
            continue
        data = r.load_json(path)
        for row in walk_bindings(data, partner_id):
            all_issues.extend(audit_row(row, routes))

    # dedupe
    seen: set[tuple] = set()
    uniq: list[dict] = []
    for i in all_issues:
        key = (i["partner"], i.get("market"), i["route_id"], i["issue"],
               (i.get("label") or i.get("chip_label") or "")[:40])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(i)

    # prioritize actionable
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    uniq.sort(key=lambda x: (severity_order.get(x["severity"], 9), x["partner"], x.get("market") or ""))

    actionable = [i for i in uniq if i["severity"] in ("critical", "high")
                  and i["issue"] not in ("chip_leg_mislinked",)]

    by_partner = defaultdict(list)
    for i in actionable:
        by_partner[i["partner"]].append(i)

    summary = {
        "at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "total_issues": len(uniq),
        "actionable": len(actionable),
        "by_severity": dict(Counter(i["severity"] for i in uniq)),
        "by_issue": dict(Counter(i["issue"] for i in uniq)),
        "by_partner_actionable": {k: len(v) for k, v in sorted(by_partner.items(), key=lambda x: -len(x[1]))},
        "issues": uniq,
        "actionable_issues": actionable,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")

    print(f"Audit: {len(actionable)} actionable / {len(uniq)} total issues")
    print(f"Report: {REPORT_PATH}\n")
    print("=== Actionable by partner ===")
    for pid, items in sorted(by_partner.items(), key=lambda x: -len(x[1]))[:20]:
        crit = sum(1 for i in items if i["severity"] == "critical")
        print(f"  {pid}: {len(items)} ({crit} critical)")

    print("\n=== Critical wrong_binding (top 25) ===")
    crit = [i for i in actionable if i["issue"] == "wrong_binding"][:25]
    for i in crit:
        mkt = i.get("market") or "hub"
        lbl = (i.get("label") or i.get("from", ""))[:45]
        print(f"  [{i['partner']}/{mkt}] {lbl}")
        print(f"    authored: {i.get('parsed_from','?')} → {i.get('parsed_to','?')}")
        print(f"    bound:    {i['route_from']} → {i['route_to']} ({i['route_id']})")

    print("\n=== Cross-border chip leaks (top 15) ===")
    leaks = [i for i in actionable if i["issue"] == "cross_border_chip_leak"][:15]
    for i in leaks:
        print(f"  [{i['partner']}/{i.get('market') or 'hub'}] chip={i.get('chip_label','')[:40]}")
        print(f"    leg: {i['route_from']} → {i['route_to']}")

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()