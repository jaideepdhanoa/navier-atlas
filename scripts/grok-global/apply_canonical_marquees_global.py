#!/usr/bin/env python3
"""Grok Pass 3 — apply global canonical marquees (cluster::city) to commercial partners.

Reads handoff/global-marquee-pass2/CANONICAL-MARQUEES.json. route_id binds directly
from sealed properties.id — no re-stamp. Label scrub + retire archive per handoff.
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

from partner_scope_py import (  # noqa: E402
    is_hub_partner,
    load_clusters,
    partner_cluster_ids,
    partner_scope_city_ids,
)

HANDOFF = ROOT / "handoff" / "global-marquee-pass2"
AUDIT_PATH = ROOT / "handoff" / "uae-consolidation" / "CROSS-PARTNER-INHERITANCE-AUDIT.json"
PARTNERS_DIR = ROOT / "data-clean" / "partners"
PITCH_DIR = ROOT / "partner-pitch" / "partners"
FEATURES_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
ARCHIVE_PATH = ROOT / "handoff" / "archive" / "featured-wow-retired-global-2026-07-06.json"
REPORT_PATH = ROOT / "grok-routing-output" / "global-canonical-marquees-apply-report.json"

COMMERCIAL_PARTNERS = (
    "airasia-move",
    "bolt",
    "cabify",
    "careem",
    "didi",
    "gojek",
    "grab",
    "grab-thailand",
    "indrive",
    "kakao-mobility",
    "line",
    "line-man-wongnai",
    "lyft",
    "noon",
    "ola",
    "rapido",
    "uber",
    "uber-india",
    "yango",
    "yassir",
)

STANDARD_KEYS = ("route_id", "from_label", "to_label", "cluster_id")
FLAT_UAE_PARTNERS = frozenset({"careem", "noon"})


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def to_standard(m: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_id": m.get("route_id"),
        "from_label": m["from_label"],
        "to_label": m["to_label"],
        "cluster_id": m.get("cluster_id"),
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


def load_routes_by_id() -> dict[str, dict]:
    routes = json.loads((ROOT / "data-clean" / "ROUTES.json").read_text())
    feats = routes if isinstance(routes, list) else routes.get("features", [])
    by_id: dict[str, dict] = {}
    for feat in feats:
        p = feat.get("properties") or feat
        rid = p.get("id")
        if rid:
            by_id[rid] = p
    return by_id


def inherited_route_ids(
    city_ids: set[str],
    cluster_ids: set[str],
    by_id: dict[str, dict],
) -> set[str]:
    out: set[str] = set()
    for rid, p in by_id.items():
        cid = p.get("cluster_id")
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if cid and cid in cluster_ids:
            out.add(rid)
        elif fc in city_ids or tc in city_ids:
            out.add(rid)
    return out


def filter_to_inherited(
    featured: list[dict[str, Any]],
    wow: list[dict[str, Any]],
    inherited: set[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    feat = [m for m in featured if m.get("route_id") in inherited]
    w = [m for m in wow if m.get("route_id") in inherited]
    dropped = (len(featured) - len(feat)) + (len(wow) - len(w))
    return feat, w, dropped


def bind_marquees(
    items: list[dict[str, Any]],
    by_id: dict[str, dict],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Verify route_id exists in sealed geometry — no re-stamp."""
    out: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    for item in items:
        rid = item.get("route_id")
        if rid and rid in by_id:
            out.append(item)
        else:
            dropped.append({"entry": item, "reason": "route_id_not_in_geometry"})
    return out, dropped


def load_contested_audit() -> dict[str, list[str]]:
    doc = json.loads(AUDIT_PATH.read_text())
    return doc.get("contested_clusters") or {}


def contested_for_partner(partner_id: str, contested: dict[str, list[str]]) -> set[str]:
    return {cid for cid, partners in contested.items() if partner_id in partners}


def registry_keys(partner: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for m in partner.get("markets") or []:
        if isinstance(m, dict):
            if m.get("slug"):
                keys.add(m["slug"])
            if m.get("id"):
                keys.add(m["id"])
    for fp in partner.get("network_footprint") or []:
        if isinstance(fp, dict) and fp.get("covered") is True:
            keys.add(fp.get("registry_key") or fp.get("id") or "")
        elif isinstance(fp, str):
            keys.add(fp)
    for k in partner.get("_map_scope", {}).get("registry_keys") or []:
        keys.add(k)
    return {k for k in keys if k}


def groups_for_partner(
    canonical: dict[str, Any],
    partner_id: str,
    scope_cities: set[str],
    contested_ids: set[str],
    reg_keys: set[str],
) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for group in (canonical.get("cities") or {}).values():
        cid = group.get("cluster_id") or ""
        city_id = group.get("city_id") or ""
        include = False
        if partner_id in FLAT_UAE_PARTNERS:
            include = city_id in scope_cities and cid.endswith("-uae")
        elif cid in contested_ids or city_id in contested_ids:
            include = True
        elif cid in reg_keys or city_id in reg_keys:
            include = True
        elif city_id in scope_cities:
            include = True
        if include:
            groups.append(group)
    return groups


def groups_for_market(
    canonical: dict[str, Any],
    market_key: str,
    anchor_cities: set[str],
) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for group in (canonical.get("cities") or {}).values():
        cid = group.get("cluster_id") or ""
        city_id = group.get("city_id") or ""
        if cid == market_key or city_id == market_key:
            groups.append(group)
        elif city_id in anchor_cities and (cid == market_key or cid == city_id):
            groups.append(group)
    return groups


def marquees_from_groups(groups: list[dict[str, Any]]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    featured: list[dict] = []
    wow: list[dict] = []
    featured_raw: list[dict] = []
    wow_raw: list[dict] = []
    for group in groups:
        for m in group.get("marquee_featured") or []:
            featured_raw.append(m)
            featured.append(to_standard(m))
        for m in group.get("marquee_wow") or []:
            wow_raw.append(m)
            wow.append(to_standard(m))
    return featured, wow, featured_raw, wow_raw


def apply_partner_marquees(
    partner: dict[str, Any],
    partner_id: str,
    featured: list[dict],
    wow: list[dict],
    contested_ids: set[str],
    cluster_by_id: dict[str, dict],
) -> tuple[dict[str, Any], dict[str, Any]]:
    doc = copy.deepcopy(partner)
    changes: dict[str, Any] = {"partner_id": partner_id, "actions": []}
    is_hub = is_hub_partner(doc)

    existing = doc.get("_map_scope") or {}
    scope = dict(existing)
    scope.update(
        {
            "_doc": "Global Pass 3 — inherit-all + canonical marquees (apply_canonical_marquees_global.py)",
            "generated": utc_now(),
            "inheritance_policy": "inherit_all_cluster_corridors",
            "contested_cluster_ids": sorted(contested_ids),
        }
    )
    if is_hub and existing.get("source") == "live_cluster_inheritance":
        scope["source"] = "live_cluster_inheritance"
    else:
        scope["source"] = "global_marquee_pass3"
        if is_hub:
            scope["cluster_city_ids"] = sorted(partner_scope_city_ids(doc, cluster_by_id))
    if not is_hub:
        scope.pop("cluster_city_ids", None)
    doc["_map_scope"] = scope
    changes["actions"].append(f"_map_scope.contested_cluster_ids → {len(contested_ids)}")

    doc["featured_routes"] = featured
    doc["wow_corridors"] = wow
    changes["actions"].append(f"featured_routes → {len(featured)}")
    changes["actions"].append(f"wow_corridors → {len(wow)}")

    if not is_hub:
        wnn = dict(doc.get("why_navier_now") or {})
        wnn["wow_corridors"] = [
            f"{w['from_label']} → {w['to_label']}" for w in wow if w.get("from_label") and w.get("to_label")
        ]
        doc["why_navier_now"] = wnn

    for pi, ph in enumerate(doc.get("phases") or []):
        if not isinstance(ph, dict):
            continue
        if ph.get("featured_routes"):
            ph["featured_routes"] = []
            changes["actions"].append(f"cleared phases[{pi}].featured_routes")
        ph["_fidelity_trim"] = {**(ph.get("_fidelity_trim") or {}), "intentional_null": True}

    doc["_global_canonical_marquees"] = {
        "applied_at": utc_now(),
        "source": "handoff/global-marquee-pass2/CANONICAL-MARQUEES.json",
        "marquee_source": "canonical_direct_bind",
        "featured_count": len(featured),
        "wow_count": len(wow),
        "contested_clusters": len(contested_ids),
    }
    return doc, changes


def market_inherited(
    market: dict[str, Any],
    contested_ids: set[str],
    city_to_cluster: dict[str, str],
    by_id: dict[str, dict],
) -> set[str]:
    mk = market.get("slug") or market.get("id") or ""
    city_ids = set(market.get("anchor_cities") or [])
    for ph in market.get("phases") or []:
        city_ids.update(ph.get("cities") or [])
    market_contested = {mk} if mk in contested_ids else set()
    cluster_ids = partner_cluster_ids(city_ids, city_to_cluster) | market_contested
    return inherited_route_ids(city_ids, cluster_ids, by_id)


def marquee_in_market_scope(
    item: dict[str, Any],
    market: dict[str, Any],
    by_id: dict[str, dict],
    market_inh: set[str],
) -> bool:
    rid = item.get("route_id")
    return bool(rid and rid in market_inh)


def is_leaf_market(market_key: str, canonical: dict[str, Any], contested_ids: set[str]) -> bool:
    """Only sync marquees onto leaf markets that map to a sealed cluster_id."""
    if market_key in contested_ids:
        return True
    for group in (canonical.get("cities") or {}).values():
        if group.get("cluster_id") == market_key or group.get("city_id") == market_key:
            return True
    return False


def apply_market_marquees(
    doc: dict[str, Any],
    canonical: dict[str, Any],
    by_id: dict[str, dict],
    contested_ids: set[str],
    city_to_cluster: dict[str, str],
    partner_inherited: set[str],
    changes: list[str],
) -> None:
    for m in doc.get("markets") or []:
        if not isinstance(m, dict):
            continue
        mk = m.get("slug") or m.get("id")
        if not mk:
            continue
        if not is_leaf_market(mk, canonical, contested_ids):
            if m.get("featured_routes"):
                m["featured_routes"] = []
                changes.append(f"cleared aggregate markets[{mk}].featured_routes")
            wnn = m.get("why_navier_now")
            if isinstance(wnn, dict) and wnn.get("wow_corridors"):
                wnn["wow_corridors"] = []
            continue
        anchors = set(m.get("anchor_cities") or [])
        for ph in m.get("phases") or []:
            anchors.update(ph.get("cities") or [])
        m_groups = groups_for_market(canonical, mk, anchors)
        if not m_groups:
            continue
        m_inh = market_inherited(m, contested_ids, city_to_cluster, by_id)
        feat, wow, feat_raw, wow_raw = marquees_from_groups(m_groups)
        feat, fd = bind_marquees(feat, by_id)
        wow, wd = bind_marquees(wow, by_id)
        feat = [
            x
            for x in feat
            if x.get("route_id") in partner_inherited and marquee_in_market_scope(x, m, by_id, m_inh)
        ]
        wow = [
            x
            for x in wow
            if x.get("route_id") in partner_inherited and marquee_in_market_scope(x, m, by_id, m_inh)
        ]
        feat = dedupe_marquees(feat)
        wow = dedupe_marquees(wow)
        if not feat and not wow:
            m["featured_routes"] = []
            wnn_clear = m.get("why_navier_now")
            if isinstance(wnn_clear, dict):
                wnn_clear["wow_corridors"] = []
            continue
        m["featured_routes"] = feat
        raw_wnn = m.get("why_navier_now")
        if isinstance(raw_wnn, dict):
            mwnn = dict(raw_wnn)
            mwnn["wow_corridors"] = wow
            m["why_navier_now"] = mwnn
        elif isinstance(raw_wnn, str) and wow:
            m["why_navier_now"] = {"narrative": raw_wnn, "wow_corridors": wow}
        else:
            m["wow_corridors"] = wow
        changes.append(f"markets[{mk}] featured={len(feat)} wow={len(wow)} dropped={len(fd)+len(wd)}")

    for m in doc.get("markets") or []:
        if not isinstance(m, dict):
            continue
        mk = m.get("slug") or m.get("id") or "?"
        for pi, ph in enumerate(m.get("phases") or []):
            if not isinstance(ph, dict):
                continue
            if ph.get("featured_routes"):
                ph["featured_routes"] = []
                changes.append(f"cleared markets[{mk}].phases[{pi}].featured_routes")
            ph["_fidelity_trim"] = {**(ph.get("_fidelity_trim") or {}), "intentional_null": True}


def apply_label_scrub(
    features: dict[str, Any],
    scrub: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, str]]]:
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--partner", nargs="*", choices=COMMERCIAL_PARTNERS)
    args = ap.parse_args()

    canonical = json.loads((HANDOFF / "CANONICAL-MARQUEES.json").read_text())
    retire_doc = json.loads((HANDOFF / "MARQUEE-RETIRE-LIST.json").read_text())
    scrub_doc = json.loads((HANDOFF / "LABEL-SCRUB.json").read_text())
    contested_audit = load_contested_audit()
    by_id = load_routes_by_id()
    _, cluster_by_id, city_to_cluster = load_clusters()

    targets = list(args.partner) if args.partner else list(COMMERCIAL_PARTNERS)
    report: dict[str, Any] = {
        "generated": utc_now(),
        "mode": "apply" if args.apply else "dry-run",
        "canonical_groups": len(canonical.get("cities") or {}),
        "partners": [],
        "label_scrub": None,
    }

    print(f"Global canonical marquees {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"  groups: {report['canonical_groups']}")

    for pid in targets:
        path = PARTNERS_DIR / f"{pid}.json"
        if not path.is_file():
            report["partners"].append({"partner_id": pid, "error": "missing"})
            continue

        partner = json.loads(path.read_text())
        scope_cities = partner_scope_city_ids(partner, cluster_by_id)
        contested_ids = contested_for_partner(pid, contested_audit)
        reg_keys = registry_keys(partner)
        groups = groups_for_partner(canonical, pid, scope_cities, contested_ids, reg_keys)

        featured, wow, feat_raw, wow_raw = marquees_from_groups(groups)
        featured, feat_dropped = bind_marquees(featured, by_id)
        wow, wow_dropped = bind_marquees(wow, by_id)

        cluster_ids = partner_cluster_ids(scope_cities, city_to_cluster) | contested_ids
        inherited = inherited_route_ids(scope_cities, cluster_ids, by_id)
        featured, wow, scope_dropped = filter_to_inherited(featured, wow, inherited)
        featured = dedupe_marquees(featured)
        wow = dedupe_marquees(wow)

        updated, changes = apply_partner_marquees(
            partner, pid, featured, wow, contested_ids, cluster_by_id
        )
        apply_market_marquees(
            updated,
            canonical,
            by_id,
            contested_ids,
            city_to_cluster,
            inherited,
            changes["actions"],
        )

        row = {
            **changes,
            "groups_matched": len(groups),
            "scope_cities": len(scope_cities),
            "featured_count": len(featured),
            "wow_count": len(wow),
            "featured_dropped": len(feat_dropped),
            "wow_dropped": len(wow_dropped),
            "scope_filtered": scope_dropped,
            "inherited_routes": len(inherited),
        }
        report["partners"].append(row)

        print(
            f"  {pid}: groups={len(groups)} featured={len(featured)} wow={len(wow)} "
            f"dropped={len(feat_dropped)+len(wow_dropped)}"
        )

        if args.apply:
            text = json.dumps(updated, indent=2) + "\n"
            path.write_text(text)
            pitch = PITCH_DIR / f"{pid}.json"
            if pitch.parent.is_dir():
                pitch.write_text(text)

    features = json.loads(FEATURES_PATH.read_text())
    scrubbed, scrub_changes = apply_label_scrub(features, scrub_doc)
    report["label_scrub"] = {"changes": len(scrub_changes), "samples": scrub_changes[:12]}
    print(f"\n  LABEL-SCRUB: {len(scrub_changes)} updates")

    if args.apply:
        if scrub_changes:
            FEATURES_PATH.write_text(json.dumps(scrubbed, indent=2) + "\n")
        archive = {
            "generated": retire_doc.get("generated", "2026-07-06"),
            "archived_at": utc_now(),
            "source": "handoff/global-marquee-pass2/MARQUEE-RETIRE-LIST.json",
            "total_entries": len(retire_doc.get("retired") or []),
            "retired": retire_doc.get("retired") or [],
        }
        ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        ARCHIVE_PATH.write_text(json.dumps(archive, indent=2) + "\n")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nReport → {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())