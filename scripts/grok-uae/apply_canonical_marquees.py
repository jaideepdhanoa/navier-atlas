#!/usr/bin/env python3
"""Apply UAE canonical marquees + unified _map_scope for careem/bolt/yango/noon.

Reads handoff/uae-consolidation/CANONICAL-MARQUEES.json and related contracts.
Dry-run by default; pass --apply to write partner JSON + FEATURES_BY_TYPE label scrub.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from partner_scope_py import load_clusters  # noqa: E402

HANDOFF = ROOT / "handoff" / "uae-consolidation"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
FEATURES_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
ARCHIVE_PATH = ROOT / "handoff" / "archive" / "featured-wow-retired-2026-07-05.json"
REPORT_PATH = ROOT / "grok-routing-output" / "uae-canonical-marquees-apply-report.json"

UAE_PARTNERS = ("careem", "bolt", "yango", "noon")
STANDARD_KEYS = ("route_id", "from_label", "to_label", "cluster_id")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def to_standard(m: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_id": m.get("route_id"),
        "from_label": m["from_label"],
        "to_label": m["to_label"],
        "cluster_id": m.get("cluster_id") or "uae",
    }


def dedupe_marquees(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for item in items:
        key = item.get("route_id") or f"{item['from_label']}→{item['to_label']}"
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _norm_label(s: str) -> str:
    return " ".join((s or "").lower().split())


def load_routes_indexes() -> tuple[dict[str, dict], dict[frozenset[str], str], dict[tuple[str, str], str]]:
    """route_id → props; BP-pair → route_id; normalized labels → route_id."""
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    feats = routes if isinstance(routes, list) else routes.get("features", [])
    by_id: dict[str, dict] = {}
    by_bp_pair: dict[frozenset[str], str] = {}
    by_labels: dict[tuple[str, str], str] = {}
    for feat in feats:
        p = feat.get("properties") or feat
        rid = p.get("id")
        if not rid:
            continue
        by_id[rid] = p
        fn, tn = p.get("from"), p.get("to")
        if fn and tn:
            by_bp_pair.setdefault(frozenset((fn, tn)), rid)
        fl, tl = _norm_label(p.get("from_label", "")), _norm_label(p.get("to_label", ""))
        if fl and tl:
            for pair in ((fl, tl), (tl, fl)):
                by_labels.setdefault(pair, rid)
    return by_id, by_bp_pair, by_labels


def _hero_score(p: dict[str, Any]) -> float:
    dist = float(p.get("distance_nm") or 0)
    if dist < 2 or dist > 30:
        return -1.0
    sweet = 12.0
    score = 3.0 - abs(dist - sweet) * 0.15
    label = f"{p.get('from_label','')} {p.get('to_label','')}".lower()
    if any(w in label for w in ("island", "palm", "world", "nurai", "lulu", "yas", "marina")):
        score += 1.5
    if p.get("from_city_id") != p.get("to_city_id"):
        score += 0.8
    if p.get("_qa_land_flag"):
        return -1.0
    return score


def derive_marquees_from_geometry(
    city_ids: set[str],
    by_id: dict[str, dict],
    *,
    wow_max: int = 5,
    featured_max: int = 8,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Fallback: rank post-reseal inherited routes per city when canonical remap fails."""
    by_city: dict[str, list[dict[str, Any]]] = {c: [] for c in city_ids}
    for rid, p in by_id.items():
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if fc not in city_ids and tc not in city_ids:
            continue
        city = fc if fc in city_ids else tc
        by_city.setdefault(city, []).append(
            {
                "route_id": rid,
                "from_label": p.get("from_label", ""),
                "to_label": p.get("to_label", ""),
                "cluster_id": p.get("cluster_id") or "uae",
                "_hero_score": _hero_score(p),
                "_distance_nm": p.get("distance_nm"),
            }
        )
    wow: list[dict[str, Any]] = []
    featured: list[dict[str, Any]] = []
    for city in sorted(city_ids):
        ranked = sorted(by_city.get(city, []), key=lambda x: x["_hero_score"], reverse=True)
        ranked = [r for r in ranked if r["_hero_score"] >= 0]
        for r in ranked[:wow_max]:
            wow.append({k: r[k] for k in STANDARD_KEYS})
        for r in ranked[:featured_max]:
            featured.append({k: r[k] for k in STANDARD_KEYS})
    return dedupe_marquees(wow), dedupe_marquees(featured)


def remap_marquee_route_ids(
    items: list[dict[str, Any]],
    raw_items: list[dict[str, Any]],
    by_id: dict[str, dict],
    by_bp_pair: dict[frozenset[str], str],
    by_labels: dict[tuple[str, str], str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Rebind canonical marquee route_ids to post-reseal geometry (BP pair, then labels)."""
    out: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    for item, raw in zip(items, raw_items):
        row = dict(item)
        rid = row.get("route_id")
        if rid and rid in by_id:
            out.append(row)
            continue
        fn = raw.get("from_node_id")
        tn = raw.get("to_node_id")
        new_rid = by_bp_pair.get(frozenset((fn, tn))) if fn and tn else None
        if new_rid:
            row["route_id"] = new_rid
            row["_remapped_from"] = rid
            out.append(row)
            continue
        fl = _norm_label(row.get("from_label", ""))
        tl = _norm_label(row.get("to_label", ""))
        new_rid = by_labels.get((fl, tl)) if fl and tl else None
        if new_rid:
            row["route_id"] = new_rid
            row["_remapped_from"] = rid
            out.append(row)
            continue
        dropped.append({"entry": row, "reason": "no_geometry_match"})
    return out, dropped


def harvest_current(partner: dict[str, Any], partner_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def grab(container: list[Any] | None, kind: str, path: str, market: str | None = None) -> None:
        for e in container or []:
            if isinstance(e, str):
                rows.append({"partner": partner_id, "kind": kind, "market": market, "schema": "string", "text": e, "path": path})
            elif isinstance(e, dict):
                rows.append(
                    {
                        "partner": partner_id,
                        "kind": kind,
                        "market": market,
                        "schema": "dict",
                        "path": path,
                        "from_label": e.get("from_label"),
                        "to_label": e.get("to_label"),
                        "from_node_id": e.get("from_node_id"),
                        "to_node_id": e.get("to_node_id"),
                        "route_id": e.get("route_id"),
                        "raw": e,
                    }
                )

    def wow_of(obj: dict[str, Any] | None) -> list[Any] | None:
        if not isinstance(obj, dict):
            return None
        w = obj.get("why_navier_now")
        return w.get("wow_corridors") if isinstance(w, dict) else None

    grab(partner.get("featured_routes"), "featured", "featured_routes")
    grab(wow_of(partner), "wow", "why_navier_now.wow_corridors")
    grab(partner.get("wow_corridors"), "wow", "wow_corridors")
    for pi, ph in enumerate(partner.get("phases") or []):
        if isinstance(ph, dict):
            grab(ph.get("featured_routes"), "featured", f"phases[{pi}].featured_routes")
    for mi, m in enumerate(partner.get("markets") or []):
        if not isinstance(m, dict):
            continue
        mk = m.get("slug") or m.get("id") or str(mi)
        grab(m.get("featured_routes"), "featured", f"markets[{mk}].featured_routes", mk)
        grab(wow_of(m), "wow", f"markets[{mk}].why_navier_now.wow_corridors", mk)
        for pi, ph in enumerate(m.get("phases") or []):
            if isinstance(ph, dict):
                grab(ph.get("featured_routes"), "featured", f"markets[{mk}].phases[{pi}].featured_routes", mk)
    return rows


def canonical_for_cities(canonical: dict[str, Any], city_ids: set[str]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    featured: list[dict] = []
    wow: list[dict] = []
    featured_raw: list[dict] = []
    wow_raw: list[dict] = []
    for cid in sorted(city_ids):
        city = canonical.get("cities", {}).get(cid)
        if not city:
            continue
        for m in city.get("marquee_featured") or []:
            featured_raw.append(m)
            featured.append(to_standard(m))
        for m in city.get("marquee_wow") or []:
            wow_raw.append(m)
            wow.append(to_standard(m))
    return featured, wow, featured_raw, wow_raw


def uae_scope_cities(unified: list[str], partner: dict[str, Any]) -> set[str]:
    """Partner UAE cities ∩ unified UAE cluster membership."""
    uae_set = set(unified)
    from_scope = set()
    for c in partner.get("_map_scope", {}).get("cluster_city_ids") or []:
        if "uae" in c or c in uae_set:
            from_scope.add(c)
    end_state = partner.get("end_state")
    if isinstance(end_state, dict):
        for c in end_state.get("end_state_cities") or []:
            if c in uae_set:
                from_scope.add(c)
    for ph in partner.get("phases") or []:
        for c in ph.get("cities") or []:
            if c in uae_set:
                from_scope.add(c)
    for m in partner.get("markets") or []:
        for c in m.get("anchor_cities") or []:
            if c in uae_set:
                from_scope.add(c)
        for ph in m.get("phases") or []:
            for c in ph.get("cities") or []:
                if c in uae_set:
                    from_scope.add(c)
    if not from_scope:
        from_scope = uae_set
    return {c for c in from_scope if c in uae_set}


def apply_partner_marquees(
    partner: dict[str, Any],
    partner_id: str,
    featured: list[dict],
    wow: list[dict],
    unified_city_ids: list[str],
    *,
    marquee_source: str = "canonical_remapped",
) -> dict[str, Any]:
    doc = copy.deepcopy(partner)
    changes: dict[str, Any] = {"partner_id": partner_id, "actions": []}

    # Unified _map_scope
    scope = dict(doc.get("_map_scope") or {})
    scope.update(
        {
            "_doc": "UAE consolidation — unified cluster membership (apply_canonical_marquees.py)",
            "generated": utc_now(),
            "source": "uae_consolidation_canonical",
            "registry_keys": sorted(set(scope.get("registry_keys") or []) | {"uae"}),
            "cluster_city_ids": unified_city_ids,
            "inheritance_policy": "inherit_all_cluster_corridors",
        }
    )
    doc["_map_scope"] = scope
    changes["actions"].append(f"_map_scope.cluster_city_ids → {len(unified_city_ids)} UAE cities")

    # Root canonical presentation arrays
    doc["featured_routes"] = featured
    doc["wow_corridors"] = wow
    changes["actions"].append(f"featured_routes → {len(featured)} canonical entries")
    changes["actions"].append(f"wow_corridors → {len(wow)} canonical entries")

    is_hub = doc.get("layout") in ("hub", "network") and bool(doc.get("markets"))

    # Flat partners: schema expects why_navier_now.wow_corridors as strings
    if not is_hub:
        wnn = dict(doc.get("why_navier_now") or {})
        wnn["wow_corridors"] = [
            f"{w['from_label']} → {w['to_label']}" for w in wow if w.get("from_label") and w.get("to_label")
        ]
        doc["why_navier_now"] = wnn
        for pi, ph in enumerate(doc.get("phases") or []):
            if isinstance(ph, dict) and ph.get("featured_routes"):
                ph["featured_routes"] = []
                changes["actions"].append(f"cleared phases[{pi}].featured_routes")

    # Hub: UAE market phases cleared; other markets untouched
    for m in doc.get("markets") or []:
        if not isinstance(m, dict):
            continue
        mk = m.get("slug") or m.get("id")
        if mk != "uae":
            continue
        m["featured_routes"] = featured
        raw_wnn = m.get("why_navier_now")
        if isinstance(raw_wnn, dict):
            mwnn = dict(raw_wnn)
            mwnn["wow_corridors"] = wow
            m["why_navier_now"] = mwnn
        elif isinstance(raw_wnn, str):
            m["why_navier_now"] = {
                "narrative": raw_wnn,
                "wow_corridors": wow,
            }
        for pi, ph in enumerate(m.get("phases") or []):
            if isinstance(ph, dict) and ph.get("featured_routes"):
                ph["featured_routes"] = []
                changes["actions"].append(f"cleared markets[uae].phases[{pi}].featured_routes")
        changes["actions"].append("markets[uae] featured_routes + wow synced")

    doc["_uae_canonical_marquees"] = {
        "applied_at": utc_now(),
        "source": "handoff/uae-consolidation/CANONICAL-MARQUEES.json",
        "marquee_source": marquee_source,
        "featured_count": len(featured),
        "wow_count": len(wow),
        "unified_city_ids": unified_city_ids,
    }
    return doc, changes


def apply_label_scrub(features: dict[str, Any], scrub: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    applied = scrub.get("applied") or []
    scrub_map = {row["node_id"]: row["clean"] for row in applied}
    changes: list[dict[str, str]] = []
    out = copy.deepcopy(features)
    for layer in ("poi", "locale", "city", "priority_city"):
        for feat in out.get(layer) or []:
            props = feat.get("properties") or {}
            nid = props.get("id")
            if not nid or nid not in scrub_map:
                continue
            clean = scrub_map[nid]
            for field in ("name", "shortName", "fullName"):
                if field in props and props[field] != clean:
                    changes.append({"node_id": nid, "field": field, "from": props[field], "to": clean})
                    props[field] = clean
    return out, changes


def merge_archive(retire_doc: dict[str, Any], uae_retired: list[dict[str, Any]]) -> dict[str, Any]:
    existing = []
    if ARCHIVE_PATH.exists():
        existing_doc = json.loads(ARCHIVE_PATH.read_text())
        existing = existing_doc.get("retired") or []
    merged = existing + uae_retired
    return {
        "generated": retire_doc.get("generated", "2026-07-05"),
        "archived_at": utc_now(),
        "source": "handoff/uae-consolidation/MARQUEE-RETIRE-LIST.json + apply_canonical_marquees.py",
        "total_entries": len(merged),
        "retired": merged,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="Write files (default: dry-run)")
    ap.add_argument("--partner", nargs="*", choices=UAE_PARTNERS, help="Limit to partner(s)")
    args = ap.parse_args()

    canonical = json.loads((HANDOFF / "CANONICAL-MARQUEES.json").read_text())
    retire_doc = json.loads((HANDOFF / "MARQUEE-RETIRE-LIST.json").read_text())
    scrub_doc = json.loads((HANDOFF / "LABEL-SCRUB.json").read_text())
    routes_by_id, routes_by_bp, routes_by_labels = load_routes_indexes()

    _, cluster_by_id, _ = load_clusters()
    uae_cluster = cluster_by_id.get("uae") or {}
    unified_city_ids = sorted(uae_cluster.get("member_city_ids") or [])

    targets = list(args.partner) if args.partner else list(UAE_PARTNERS)
    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "unified_uae_city_ids": unified_city_ids,
        "partners": [],
        "label_scrub": None,
        "archive": None,
    }

    all_retired: list[dict[str, Any]] = []

    print(f"UAE canonical marquees {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"  unified UAE cities: {unified_city_ids}")

    for pid in targets:
        path = PARTNERS_DIR / f"{pid}.json"
        partner = json.loads(path.read_text())
        scope_cities = uae_scope_cities(unified_city_ids, partner)
        featured_std, wow_std, featured_raw, wow_raw = canonical_for_cities(canonical, scope_cities)
        featured, feat_dropped = remap_marquee_route_ids(
            featured_std, featured_raw, routes_by_id, routes_by_bp, routes_by_labels
        )
        wow, wow_dropped = remap_marquee_route_ids(
            wow_std, wow_raw, routes_by_id, routes_by_bp, routes_by_labels
        )
        featured = dedupe_marquees(featured)
        wow = dedupe_marquees(wow)
        marquee_source = "canonical_remapped"
        if not featured and not wow:
            wow, featured = derive_marquees_from_geometry(scope_cities, routes_by_id)
            marquee_source = "geometry_derived_fallback"
        current = harvest_current(partner, pid)
        retired_for_partner = [e for e in retire_doc.get("retired") or [] if e.get("partner") == pid]
        all_retired.extend(retired_for_partner)

        updated, changes = apply_partner_marquees(
            partner, pid, featured, wow, unified_city_ids, marquee_source=marquee_source
        )
        row = {
            **changes,
            "scope_cities": sorted(scope_cities),
            "featured_count": len(featured),
            "wow_count": len(wow),
            "featured_dropped": len(feat_dropped),
            "wow_dropped": len(wow_dropped),
            "marquee_source": marquee_source,
            "current_entries": len(current),
            "retire_list_entries": len(retired_for_partner),
        }
        report["partners"].append(row)

        print(f"\n  {pid}:")
        print(f"    scope cities: {sorted(scope_cities)}")
        print(f"    canonical featured/wow: {len(featured)}/{len(wow)}")
        print(f"    current entries harvested: {len(current)} · retire-list: {len(retired_for_partner)}")
        for act in changes["actions"]:
            print(f"    · {act}")

        if args.apply:
            path.write_text(json.dumps(updated, indent=2) + "\n")

    # Label scrub (global FEATURES_BY_TYPE)
    features = json.loads(FEATURES_PATH.read_text())
    scrubbed, scrub_changes = apply_label_scrub(features, scrub_doc)
    report["label_scrub"] = {"changes": len(scrub_changes), "samples": scrub_changes[:12]}
    print(f"\n  LABEL-SCRUB: {len(scrub_changes)} BP/locale label updates")
    for ch in scrub_changes[:6]:
        print(f"    {ch['node_id']}.{ch['field']}: {ch['from']!r} → {ch['to']!r}")

    archive_payload = merge_archive(retire_doc, all_retired)
    report["archive"] = {"path": str(ARCHIVE_PATH.relative_to(ROOT)), "total_entries": archive_payload["total_entries"]}
    print(f"\n  ARCHIVE: {archive_payload['total_entries']} total retired entries → {ARCHIVE_PATH.relative_to(ROOT)}")

    if args.apply:
        if scrub_changes:
            FEATURES_PATH.write_text(json.dumps(scrubbed, indent=2) + "\n")
        ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        ARCHIVE_PATH.write_text(json.dumps(archive_payload, indent=2) + "\n")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nReport → {REPORT_PATH.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())