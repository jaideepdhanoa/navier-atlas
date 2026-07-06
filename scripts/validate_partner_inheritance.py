#!/usr/bin/env python3
"""Gate: featured/wow corridors must be subsets of partner-inherited ROUTES.json geometry.

Contract: handoff/uae-consolidation/CORRIDOR-INHERITANCE-CONTRACT.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from partner_scope_py import (  # noqa: E402
    load_clusters,
    partner_cluster_ids,
    partner_scope_city_ids,
)

STANDARD_KEYS = frozenset({"route_id", "from_label", "to_label", "cluster_id"})
DATA_PARTNERS = ROOT / "data-clean" / "partners"
PITCH_PARTNERS = ROOT / "partner-pitch" / "partners"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
REPORT_PATH = ROOT / "grok-routing-output" / "partner-inheritance-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_routes_index() -> tuple[dict[str, dict], dict[frozenset[str], set[str]], dict[tuple[str, str], set[str]]]:
    routes = json.loads(ROUTES_PATH.read_text())
    by_route_id: dict[str, dict] = {}
    by_bp_pair: dict[frozenset[str], set[str]] = {}
    by_labels: dict[tuple[str, str], set[str]] = {}
    for feat in routes:
        p = feat.get("properties") or {}
        rid = p.get("id")
        if not rid:
            continue
        by_route_id[rid] = p
        fn, tn = p.get("from"), p.get("to")
        if fn and tn:
            by_bp_pair.setdefault(frozenset((fn, tn)), set()).add(rid)
        fl, tl = p.get("from_label"), p.get("to_label")
        if fl and tl:
            by_labels.setdefault((fl, tl), set()).add(rid)
            by_labels.setdefault((tl, fl), set()).add(rid)
    return by_route_id, by_bp_pair, by_labels


def inherited_route_ids(
    city_ids: set[str],
    cluster_ids: set[str],
    by_route_id: dict[str, dict],
) -> set[str]:
    out: set[str] = set()
    for rid, p in by_route_id.items():
        cid = p.get("cluster_id")
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if cid and cid in cluster_ids:
            out.add(rid)
        elif fc in city_ids or tc in city_ids:
            out.add(rid)
    return out


def wow_of(obj: dict[str, Any] | None) -> list[Any] | None:
    if not isinstance(obj, dict):
        return None
    w = obj.get("why_navier_now")
    return w.get("wow_corridors") if isinstance(w, dict) else None


def iter_marquee_entries(partner: dict[str, Any]) -> list[dict[str, Any]]:
    pid = partner.get("partner_id", "unknown")
    entries: list[dict[str, Any]] = []
    has_canonical = bool(partner.get("_uae_canonical_marquees"))
    is_hub = partner.get("layout") in ("hub", "network") and bool(partner.get("markets"))

    def add(container: list[Any] | None, kind: str, path: str) -> None:
        for i, e in enumerate(container or []):
            entries.append(
                {
                    "partner_id": pid,
                    "kind": kind,
                    "path": f"{path}[{i}]",
                    "entry": e,
                }
            )

    # Root canonical arrays (post-UAE consolidation)
    if partner.get("featured_routes") is not None:
        add(partner.get("featured_routes"), "featured", "featured_routes")
    if partner.get("wow_corridors") is not None:
        add(partner.get("wow_corridors"), "wow", "wow_corridors")
    elif not has_canonical:
        add(wow_of(partner), "wow", "why_navier_now.wow_corridors")

    if has_canonical and is_hub:
        for mi, m in enumerate(partner.get("markets") or []):
            if not isinstance(m, dict):
                continue
            mk = m.get("slug") or m.get("id") or m.get("market") or str(mi)
            if mk != "uae":
                continue
            add(m.get("featured_routes"), "featured", f"markets[{mk}].featured_routes")
            add(m.get("wow_corridors"), "wow", f"markets[{mk}].wow_corridors")
            w = wow_of(m)
            if w is not None:
                add(w, "wow", f"markets[{mk}].why_navier_now.wow_corridors")
            for pi, ph in enumerate(m.get("phases") or []):
                if isinstance(ph, dict):
                    add(ph.get("featured_routes"), "featured", f"markets[{mk}].phases[{pi}].featured_routes")
        return entries

    if not has_canonical:
        for pi, ph in enumerate(partner.get("phases") or []):
            if isinstance(ph, dict):
                add(ph.get("featured_routes"), "featured", f"phases[{pi}].featured_routes")
    for mi, m in enumerate(partner.get("markets") or []):
        if not isinstance(m, dict):
            continue
        mk = m.get("slug") or m.get("id") or m.get("market") or str(mi)
        add(m.get("featured_routes"), "featured", f"markets[{mk}].featured_routes")
        add(wow_of(m), "wow", f"markets[{mk}].why_navier_now.wow_corridors")
        for pi, ph in enumerate(m.get("phases") or []):
            if isinstance(ph, dict):
                add(ph.get("featured_routes"), "featured", f"markets[{mk}].phases[{pi}].featured_routes")
    return entries


def check_schema(entry: Any) -> list[str]:
    if isinstance(entry, str):
        return ["legacy_string_schema"]
    if not isinstance(entry, dict):
        return ["non_object_entry"]
    keys = set(entry.keys())
    missing = STANDARD_KEYS - keys
    extra = keys - STANDARD_KEYS
    errs: list[str] = []
    if missing:
        errs.append(f"missing_keys:{','.join(sorted(missing))}")
    if extra:
        errs.append(f"extra_keys:{','.join(sorted(extra))}")
    for req in STANDARD_KEYS:
        if req in entry and entry[req] is None and req != "route_id":
            errs.append(f"null_{req}")
    if "from_label" in entry and "to_label" in entry:
        if not str(entry.get("from_label") or "").strip():
            errs.append("empty_from_label")
        if not str(entry.get("to_label") or "").strip():
            errs.append("empty_to_label")
    return errs


def resolve_entry_route_ids(
    entry: Any,
    by_route_id: dict[str, dict],
    by_bp_pair: dict[frozenset[str], set[str]],
    by_labels: dict[tuple[str, str], set[str]],
) -> set[str] | None:
    if isinstance(entry, str):
        return None
    if not isinstance(entry, dict):
        return None
    rid = entry.get("route_id")
    if rid and rid in by_route_id:
        return {rid}
    fn = entry.get("from_node_id")
    tn = entry.get("to_node_id")
    if fn and tn:
        return set(by_bp_pair.get(frozenset((fn, tn)), set()))
    fl = entry.get("from_label")
    tl = entry.get("to_label")
    if fl and tl:
        return set(by_labels.get((fl, tl), set()))
    return set()


def partner_dirs(*, include_pitch: bool) -> list[Path]:
    dirs = [DATA_PARTNERS]
    if include_pitch and PITCH_PARTNERS.is_dir():
        dirs.append(PITCH_PARTNERS)
    return dirs


def validate_partner(
    partner: dict[str, Any],
    *,
    city_to_cluster: dict[str, str],
    cluster_by_id: dict[str, dict],
    by_route_id: dict[str, dict],
    by_bp_pair: dict[frozenset[str], set[str]],
    by_labels: dict[tuple[str, str], set[str]],
    strict_schema: bool,
) -> dict[str, Any]:
    pid = partner.get("partner_id", "unknown")
    city_ids = partner_scope_city_ids(partner, cluster_by_id)
    cluster_ids = partner_cluster_ids(city_ids, city_to_cluster)
    inherited = inherited_route_ids(city_ids, cluster_ids, by_route_id)

    schema_failures: list[dict[str, Any]] = []
    subset_failures: list[dict[str, Any]] = []
    entries_checked = 0

    for row in iter_marquee_entries(partner):
        entry = row["entry"]
        entries_checked += 1
        schema_errs = check_schema(entry)
        if schema_errs:
            schema_failures.append({**row, "errors": schema_errs})
            if strict_schema:
                continue
        rids = resolve_entry_route_ids(entry, by_route_id, by_bp_pair, by_labels)
        if rids is None:
            subset_failures.append({**row, "errors": ["unresolvable_entry"]})
            continue
        if not rids:
            subset_failures.append({**row, "errors": ["no_matching_route_id"]})
            continue
        outside = sorted(r for r in rids if r not in inherited)
        if outside:
            subset_failures.append(
                {
                    **row,
                    "errors": ["outside_inherited_set"],
                    "route_ids": sorted(rids),
                    "outside": outside,
                }
            )

    ok = not subset_failures and (not schema_failures if strict_schema else True)
    return {
        "partner_id": pid,
        "ok": ok,
        "scope_city_count": len(city_ids),
        "scope_cluster_ids": sorted(cluster_ids),
        "inherited_route_count": len(inherited),
        "entries_checked": entries_checked,
        "schema_failures": schema_failures,
        "subset_failures": subset_failures,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--partner", nargs="*", help="Limit to partner_id(s)")
    ap.add_argument("--strict", action="store_true", help="Fail on schema violations too")
    ap.add_argument("--json", action="store_true", help=f"Write report to {REPORT_PATH.relative_to(ROOT)}")
    ap.add_argument("--include-pitch", action="store_true", help="Also scan partner-pitch/partners/")
    args = ap.parse_args()

    _, cluster_by_id, city_to_cluster = load_clusters()
    by_route_id, by_bp_pair, by_labels = load_routes_index()

    partner_filter = set(args.partner) if args.partner else None
    results: list[dict[str, Any]] = []

    for pdir in partner_dirs(include_pitch=args.include_pitch):
        for path in sorted(pdir.glob("*.json")):
            if path.name.startswith("_"):
                continue
            doc = json.loads(path.read_text())
            pid = doc.get("partner_id", path.stem)
            if partner_filter and pid not in partner_filter:
                continue
            results.append(
                validate_partner(
                    doc,
                    city_to_cluster=city_to_cluster,
                    cluster_by_id=cluster_by_id,
                    by_route_id=by_route_id,
                    by_bp_pair=by_bp_pair,
                    by_labels=by_labels,
                    strict_schema=args.strict,
                )
            )

    failing = [r for r in results if not r["ok"]]
    schema_total = sum(len(r["schema_failures"]) for r in results)
    subset_total = sum(len(r["subset_failures"]) for r in results)

    print("Partner corridor inheritance gate")
    print(f"  partners checked: {len(results)}")
    print(f"  passing: {len(results) - len(failing)}")
    print(f"  failing: {len(failing)}")
    print(f"  schema issues: {schema_total}")
    print(f"  subset issues: {subset_total}")

    for r in failing:
        print(f"\n  ✗ {r['partner_id']}")
        print(
            f"    scope: {r['scope_city_count']} cities · "
            f"{r['inherited_route_count']} inherited routes · "
            f"{r['entries_checked']} marquee entries"
        )
        for sf in r["subset_failures"][:6]:
            print(f"    subset {sf['path']}: {', '.join(sf['errors'])}")
        if len(r["subset_failures"]) > 6:
            print(f"    ... +{len(r['subset_failures']) - 6} more subset failures")
        if args.strict:
            for sf in r["schema_failures"][:4]:
                print(f"    schema {sf['path']}: {', '.join(sf['errors'])}")
            if len(r["schema_failures"]) > 4:
                print(f"    ... +{len(r['schema_failures']) - 4} more schema failures")

    report = {
        "generated": utc_now(),
        "strict_schema": args.strict,
        "summary": {
            "partners_checked": len(results),
            "passing": len(results) - len(failing),
            "failing": len(failing),
            "schema_issues": schema_total,
            "subset_issues": subset_total,
        },
        "partners": results,
    }

    if args.json:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
        print(f"\nReport → {REPORT_PATH.relative_to(ROOT)}")

    if failing:
        return 1
    if args.strict and schema_total:
        return 1
    print("\n  ✅ all partners pass inheritance gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())