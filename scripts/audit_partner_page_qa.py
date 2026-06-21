#!/usr/bin/env python3
"""
Partner page completeness + linkability QA gate.

Checks narrative, journeys, featured_routes, phase structure, and map-scope route
coverage. Writes per-partner ledgers and an aggregate report. Optionally appends
Tasklet flags to docs/NOTES-FOR-TASKLET.md.

Usage:
  python3 scripts/audit_partner_page_qa.py
  python3 scripts/audit_partner_page_qa.py --partner rapido careem noon
  python3 scripts/audit_partner_page_qa.py --write-tasklet-note
  python3 scripts/audit_partner_page_qa.py --fail-on-warn
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTNERS_PITCH = ROOT / "partner-pitch" / "partners"
PARTNERS_DC = ROOT / "data-clean" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"
NOTES = ROOT / "docs" / "NOTES-FOR-TASKLET.md"

MIN_JOURNEYS_SINGLE = 3
MIN_FEATURED_PER_ACTIVE_PHASE = 1
LINK_RATIO_PASS = 0.85
BP_BOUND_RATIO_UAE_REF = 0.60

HELD_OK = frozenset(
    {
        "held-null-with-reason",
        "held-null-not-in-gold",
        "held-null-not-in-spine",
        "held-null-no-spine-match",
        "roadmap-no-geometry",
        "unlinked-intra-city",
        "unlinked-no-route",
    }
)

REFERENCE_PARTNERS = frozenset({"noon", "grab", "rapido", "careem"})


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def build_gold_and_scope():
    routes = load_json(ROOT / "data-clean" / "ROUTES.json")
    gold = {f["properties"]["id"] for f in routes if f.get("properties", {}).get("id")}
    fbt = load_json(ROOT / "data-clean" / "FEATURES_BY_TYPE.json")

    city_ids = {
        f["properties"]["id"]
        for key in ("city", "priority_city")
        for f in fbt.get(key, [])
        if f.get("properties", {}).get("id")
    }
    node_index = {
        f["properties"]["id"]: f["properties"]
        for bucket in fbt
        for f in fbt.get(bucket, [])
        if f.get("properties", {}).get("id")
    }

    def city_id_of(nid: str | None) -> str | None:
        if not nid:
            return None
        if nid in city_ids:
            return nid
        p = node_index.get(nid)
        if p and p.get("parent_city_id") in city_ids:
            return p["parent_city_id"]
        pre = str(nid).split("__")[0]
        return pre if pre in city_ids else None

    return gold, city_id_of


def iter_featured_and_journeys(doc: dict):
    for j in doc.get("journeys_unlocked", []) or []:
        yield "journey", None, j
    for phase in doc.get("phases", []) or []:
        pn = phase.get("n")
        for fr in phase.get("featured_routes", []) or []:
            yield "featured", pn, fr
        for j in phase.get("journeys_unlocked", []) or []:
            yield "journey", pn, j
    for market in doc.get("markets", []) or []:
        mid = market.get("id")
        for j in market.get("journeys_unlocked", []) or []:
            yield "journey", mid, j
        for phase in market.get("phases", []) or []:
            pn = phase.get("n")
            for fr in phase.get("featured_routes", []) or []:
                yield "featured", f"{mid}/p{pn}", fr
        for fr in market.get("sealed_corridor_pool", []) or []:
            yield "sealed_pool", mid, fr


def is_linked(item: dict, gold: set[str]) -> bool:
    rid = item.get("route_id")
    rids = item.get("route_ids") or []
    if rid and rid in gold:
        return True
    if rids and any(x in gold for x in rids):
        return True
    status = item.get("_link_status") or ""
    if status in HELD_OK and (item.get("_hold_reason") or status.startswith("unlinked")):
        return True
    return False


def is_bp_bound(item: dict) -> bool:
    fn = str(item.get("from_node_id") or "")
    tn = str(item.get("to_node_id") or "")
    return fn.startswith("bp-") or tn.startswith("bp-")


def audit_partner(slug: str, doc: dict, gold: set[str], city_id_of) -> dict:
    flags: list[dict] = []
    tasklet: list[str] = []

    # Narrative completeness
    for field, path in (
        ("hero.title", ("hero", "title")),
        ("hero.subtitle", ("hero", "subtitle")),
        ("why_now", ("why_now",)),
        ("multimodal_fit", ("multimodal_fit",)),
    ):
        cur = doc
        for p in path:
            cur = cur.get(p) if isinstance(cur, dict) else None
        if not cur or not str(cur).strip():
            flags.append({"check": "narrative", "severity": "warn", "detail": f"missing {field}"})

    ctx = doc.get("partner_context") or {}
    if isinstance(ctx, dict):
        for k in ("their_ambition", "their_pressure", "where_navier_fits"):
            if not (ctx.get(k) or "").strip():
                flags.append({"check": "partner_context", "severity": "warn", "detail": f"missing {k}"})
    elif not str(ctx).strip():
        flags.append({"check": "partner_context", "severity": "warn", "detail": "missing partner_context"})

    journeys = [x for t, _, x in iter_featured_and_journeys(doc) if t == "journey" and isinstance(x, dict)]
    featured = [x for t, _, x in iter_featured_and_journeys(doc) if t in ("featured", "sealed_pool") and isinstance(x, dict)]

    layout = doc.get("layout") or "single"
    if layout != "hub" and len(journeys) < MIN_JOURNEYS_SINGLE:
        flags.append({
            "check": "journeys_count",
            "severity": "warn",
            "detail": f"{len(journeys)} journeys (min {MIN_JOURNEYS_SINGLE})",
        })

    journey_linked = 0
    for j in journeys:
        for req in ("from", "to", "today", "with_navier"):
            if not (j.get(req) or "").strip():
                flags.append({"check": "journey_fields", "severity": "error", "detail": f"journey missing {req}"})
        if is_linked(j, gold):
            journey_linked += 1
        else:
            flags.append({
                "check": "journey_unlinked",
                "severity": "warn",
                "detail": f"{j.get('from')} → {j.get('to')} ({j.get('_link_status')})",
            })
            tasklet.append(f"{slug}: journey needs geometry bind — {j.get('from')} → {j.get('to')}")

    featured_linked = 0
    bp_bound = 0
    for fr in featured:
        if fr.get("display") == "network_chip":
            rids = fr.get("route_ids") or []
            if rids and any(x in gold for x in rids):
                featured_linked += 1
            elif not rids:
                flags.append({"check": "network_chip_empty", "severity": "warn", "detail": fr.get("label")})
            continue
        if is_linked(fr, gold):
            featured_linked += 1
        else:
            flags.append({
                "check": "featured_unlinked",
                "severity": "warn",
                "detail": f"{fr.get('label')} ({fr.get('_link_status')})",
            })
        if is_bp_bound(fr):
            bp_bound += 1

    phases = doc.get("phases") or []
    for phase in phases:
        if phase.get("aspirational"):
            continue
        pn = phase.get("n")
        if not (phase.get("narrative") or "").strip():
            flags.append({"check": "phase_narrative", "severity": "warn", "detail": f"phase {pn} missing narrative"})
        if not (phase.get("rationale") or "").strip():
            flags.append({"check": "phase_rationale", "severity": "warn", "detail": f"phase {pn} missing rationale"})
        frs = [x for x in (phase.get("featured_routes") or []) if isinstance(x, dict)]
        if not phase.get("aspirational") and len(frs) < MIN_FEATURED_PER_ACTIVE_PHASE:
            flags.append({
                "check": "phase_featured",
                "severity": "warn",
                "detail": f"phase {pn} has {len(frs)} featured_routes",
            })

    # Map scope
    cities: set[str] = set()
    for phase in phases:
        for c in phase.get("cities") or []:
            cities.add(c)
    for market in doc.get("markets") or []:
        for c in market.get("anchor_cities") or market.get("cities") or []:
            cities.add(c)

    route_count = 0
    if cities:
        routes = load_json(ROOT / "data-clean" / "ROUTES.json")
        for f in routes:
            p = f.get("properties", {})
            if city_id_of(p.get("from")) in cities or city_id_of(p.get("to")) in cities:
                route_count += 1

    j_ratio = journey_linked / len(journeys) if journeys else 1.0
    f_ratio = featured_linked / len(featured) if featured else 1.0
    bp_ratio = bp_bound / len(featured) if featured else 0.0

    if j_ratio < LINK_RATIO_PASS:
        flags.append({"check": "journey_link_ratio", "severity": "warn", "detail": f"{j_ratio:.0%}"})
    if featured and f_ratio < LINK_RATIO_PASS:
        flags.append({"check": "featured_link_ratio", "severity": "warn", "detail": f"{f_ratio:.0%}"})

    if slug in {"noon", "careem"} and featured and bp_ratio < BP_BOUND_RATIO_UAE_REF:
        flags.append({
            "check": "bp_bound_ratio",
            "severity": "warn",
            "detail": f"{bp_ratio:.0%} BP-bound featured (target {BP_BOUND_RATIO_UAE_REF:.0%})",
        })
        tasklet.append(f"{slug}: increase BP-bound featured_routes to Noon reference bar")

    errors = sum(1 for f in flags if f["severity"] == "error")
    warns = sum(1 for f in flags if f["severity"] == "warn")

    if errors:
        verdict = "FAIL"
    elif warns and slug in REFERENCE_PARTNERS:
        verdict = "PASS_WITH_FLAGS"
    elif warns:
        verdict = "PASS_WITH_FLAGS"
    else:
        verdict = "PASS"

    return {
        "partner": slug,
        "verdict": verdict,
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "counts": {
            "journeys": len(journeys),
            "journeys_linked": journey_linked,
            "featured_routes": len(featured),
            "featured_linked": featured_linked,
            "bp_bound_featured": bp_bound,
            "map_routes_in_scope": route_count,
            "phases": len(phases),
        },
        "ratios": {
            "journey_link": round(j_ratio, 3),
            "featured_link": round(f_ratio, 3),
            "bp_bound": round(bp_ratio, 3),
        },
        "flags": flags,
        "tasklet_actions": tasklet,
        "errors": errors,
        "warnings": warns,
    }


def append_tasklet_note(aggregate: dict) -> None:
    if not NOTES.is_file():
        return
    tasklet_items = []
    for r in aggregate.get("partners", []):
        for t in r.get("tasklet_actions", []):
            tasklet_items.append(t)
    if not tasklet_items:
        return

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    block = [
        "",
        f"## {date} — Partner page QA flags (Grok audit_partner_page_qa)",
        "",
        f"**Ledger:** `handoff/partner-map-model/partner-page-qa-ledger.json`",
        "",
    ]
    for t in sorted(set(tasklet_items))[:25]:
        block.append(f"- {t}")
    if len(tasklet_items) > 25:
        block.append(f"- … +{len(tasklet_items) - 25} more in ledger")
    block.append("")

    text = NOTES.read_text()
    marker = f"## {date} — Partner page QA flags"
    if marker in text:
        return
    # Insert after header block (first ---)
    parts = text.split("---\n", 1)
    if len(parts) == 2:
        new_text = parts[0] + "---\n" + "\n".join(block) + parts[1]
    else:
        new_text = "\n".join(block) + text
    NOTES.write_text(new_text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="*", help="Limit to partner slug(s)")
    ap.add_argument("--write-tasklet-note", action="store_true")
    ap.add_argument("--fail-on-warn", action="store_true")
    args = ap.parse_args()

    gold, city_id_of = build_gold_and_scope()

    slugs = args.partner or sorted(
        p.stem for p in PARTNERS_PITCH.glob("*.json") if not p.name.startswith("_")
    )

    results: list[dict] = []
    for slug in slugs:
        path = PARTNERS_PITCH / f"{slug}.json"
        if not path.is_file():
            continue
        doc = load_json(path)
        rec = audit_partner(slug, doc, gold, city_id_of)
        results.append(rec)
        save_json(HANDOFF / f"partner-page-qa-{slug}.json", rec)

    aggregate = {
        "package": "partner-page-qa-ledger",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "partners": results,
        "summary": {
            "total": len(results),
            "pass": sum(1 for r in results if r["verdict"] == "PASS"),
            "pass_with_flags": sum(1 for r in results if r["verdict"] == "PASS_WITH_FLAGS"),
            "fail": sum(1 for r in results if r["verdict"] == "FAIL"),
            "tasklet_actions": sum(len(r.get("tasklet_actions", [])) for r in results),
        },
    }
    save_json(HANDOFF / "partner-page-qa-ledger.json", aggregate)

    print(f"Partner page QA — {aggregate['summary']['total']} partners")
    print(f"  PASS: {aggregate['summary']['pass']}")
    print(f"  PASS_WITH_FLAGS: {aggregate['summary']['pass_with_flags']}")
    print(f"  FAIL: {aggregate['summary']['fail']}")
    print(f"  Tasklet actions: {aggregate['summary']['tasklet_actions']}")

    for r in sorted(results, key=lambda x: x["partner"]):
        if r["verdict"] != "PASS":
            c = r["counts"]
            print(
                f"  {r['verdict']:16} {r['partner']:12} "
                f"journeys {c['journeys_linked']}/{c['journeys']} "
                f"featured {c['featured_linked']}/{c['featured_routes']} "
                f"map_routes {c['map_routes_in_scope']}"
            )

    if args.write_tasklet_note:
        append_tasklet_note(aggregate)

    if aggregate["summary"]["fail"]:
        return 1
    if args.fail_on_warn and aggregate["summary"]["pass_with_flags"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())