#!/usr/bin/env python3
"""Apply 80-20 inheritance candidate binds to partner network_footprint[].

Reads handoff/partner-map-model/partner-coverage-80-20-inheritance-review-2026-06-20.json
and promotes net-new inherited registry cities into live partner JSONs. Partners whose
footprint is entirely unbound (didi, indrive, ola) also receive baseline rows so LATAM /
Global South city geometry binds land on the map.

Additive only — never shrinks or removes footprint rows.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff" / "partner-map-model"
PARTNERS = ROOT / "data-clean" / "partners"
PITCH = ROOT / "partner-pitch" / "partners"

REVIEW_PATH = HANDOFF / "partner-coverage-80-20-inheritance-review-2026-06-20.json"
REGISTRY_PATH = HANDOFF / "global-inheritance-registry.json"
MAP_SCOPE_PATH = HANDOFF / "map-scope.json"

# Partners with no bound footprint rows get all artifact rows, not only net-new.
LATAM_BACKLOG_PARTNERS = frozenset({"didi", "indrive", "ola", "rapido"})


def load_json(p: Path) -> dict:
    return json.loads(p.read_text())


def save_json(p: Path, obj: dict) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def registry_index(registry: dict) -> dict[str, dict]:
    return {m["registry_key"]: m for m in registry.get("city_markets") or []}


def infer_render(row: dict) -> tuple[str, bool, str]:
    density = row.get("coverage_density") or ""
    routes = int(row.get("route_count_active") or 0)
    lane = row.get("promotion_lane") or ""

    if density == "marquee_economics_ready":
        return "geometry", True, "sub_proposal"
    if density == "full_display_geometry_no_economics" and routes > 0:
        return "geometry", True, "corridor_ready"
    if routes > 0:
        return "geometry", False, "corridor_ready"
    if density == "thin_brief_only_needs_route_grounding":
        return "cluster_dots", False, "corridor_ready"
    if lane.startswith("promote_new_display_and_marquee"):
        return "cluster_dots", False, "sub_proposal"
    return "cluster_dots", False, "corridor_ready"


def footprint_row_from_bind(row: dict, reg: dict[str, dict], covered_market_ids: set[str]) -> dict:
    rk = row["registry_city_id"]
    meta = reg.get(rk) or {}
    render, map_promote, tier = infer_render(row)
    country = row.get("country")
    region = meta.get("region") or "Global"
    entry_id = rk

    covered = False
    country_slug = (country or "").lower().replace(" ", "-")
    for mid in covered_market_ids:
        if mid in entry_id or (country_slug and country_slug in mid):
            covered = True
            break

    return {
        "id": entry_id,
        "registry_key": rk,
        "covered": covered,
        "tier": tier,
        "render": render,
        "map_promote": map_promote,
        "label": row.get("display") or meta.get("display") or rk,
        "country": country,
        "countries": [country] if country else [],
        "region": region,
        "_binding_source": "grok/apply_partner_8020_inheritance_bindings",
        "_evidence_tier": row.get("evidence_tier"),
        "_promotion_lane": row.get("promotion_lane"),
    }


def rows_for_partner(partner_id: str, all_rows: list[dict], bound_count: int) -> list[dict]:
    partner_rows = [r for r in all_rows if r.get("partner_id") == partner_id]
    if partner_id in LATAM_BACKLOG_PARTNERS and bound_count == 0:
        return partner_rows
    return [r for r in partner_rows if not r.get("already_in_partner_baseline")]


def upsert_footprint(partner: dict, row: dict) -> bool:
    fp = partner.setdefault("network_footprint", [])
    rk = row["registry_key"]
    existing = next(
        (x for x in fp if x.get("registry_key") == rk or x.get("id") == row["id"]),
        None,
    )
    if existing:
        before = deepcopy(existing)
        if not existing.get("registry_key"):
            existing.update(row)
            return existing != before
        return False
    fp.append(row)
    return True


def covered_market_ids(partner: dict) -> set[str]:
    ids: set[str] = set()
    for m in partner.get("markets") or []:
        if m.get("id"):
            ids.add(m["id"])
        if m.get("market_id"):
            ids.add(m["market_id"])
    return ids


def materialize_map_scope_from_handoff(partner_id: str, scope_all: dict) -> dict | None:
    block = scope_all.get(partner_id)
    if not block:
        return None
    return {
        "_doc": "LB-261 materialized from handoff/partner-map-model/map-scope.json",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "handoff/partner-map-model/map-scope.json",
        "registry_keys": sorted(set(block.get("registry_keys") or [])),
        "cluster_city_ids": sorted(set(block.get("sealed_cluster_cities") or [])),
    }


def rebuild_map_scope_from_footprint(
    partner: dict,
    reg: dict[str, dict],
    applied_city_ids: list[str],
) -> dict:
    existing = partner.get("_map_scope") or {}
    keys: set[str] = set(existing.get("registry_keys") or [])
    cities: set[str] = set(existing.get("cluster_city_ids") or [])

    for fp in partner.get("network_footprint") or []:
        if fp.get("render") == "held":
            continue
        rk = fp.get("registry_key")
        if not rk:
            continue
        keys.add(rk)
        meta = reg.get(rk)
        if meta:
            cities.add(rk)
            for cid in meta.get("cluster_ids") or []:
                keys.add(cid)

    for cid in applied_city_ids:
        cities.add(cid)
        keys.add(cid)

    return {
        "_doc": "LB-261 materialized from network_footprint after 80-20 inheritance apply",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "network_footprint + global-inheritance-registry",
        "registry_keys": sorted(keys),
        "cluster_city_ids": sorted(cities),
    }


def main() -> int:
    if not REVIEW_PATH.exists():
        print(f"✗ missing {REVIEW_PATH}", file=sys.stderr)
        return 1

    review = load_json(REVIEW_PATH)
    registry = load_json(REGISTRY_PATH) if REGISTRY_PATH.exists() else {"city_markets": []}
    reg = registry_index(registry)
    scope_all = load_json(MAP_SCOPE_PATH) if MAP_SCOPE_PATH.exists() else {}

    all_rows = review.get("candidate_inherited_binds") or []
    net_new = [r for r in all_rows if not r.get("already_in_partner_baseline")]

    partner_ids = sorted({r["partner_id"] for r in all_rows})
    report: dict = {
        "at": datetime.now(timezone.utc).isoformat(),
        "artifact": str(REVIEW_PATH.relative_to(ROOT)),
        "net_new_target": len(net_new),
        "partners": {},
        "skipped_no_partner_json": [],
        "skipped_duplicate_registry_keys": 0,
    }

    total_applied = 0

    for pid in partner_ids:
        pj = PARTNERS / f"{pid}.json"
        if not pj.exists():
            rows = rows_for_partner(pid, all_rows, 0)
            if rows:
                report["skipped_no_partner_json"].append(
                    {"partner_id": pid, "rows": len(rows), "net_new": sum(1 for r in rows if not r.get("already_in_partner_baseline"))}
                )
            continue

        partner = load_json(pj)
        bound_before = sum(1 for x in partner.get("network_footprint") or [] if x.get("registry_key"))
        fp_before = len(partner.get("network_footprint") or [])

        to_apply = rows_for_partner(pid, all_rows, bound_before)
        covered_ids = covered_market_ids(partner)
        applied = 0
        applied_city_ids: list[str] = []
        duplicates = 0

        for row in to_apply:
            fp_row = footprint_row_from_bind(row, reg, covered_ids)
            rk = fp_row["registry_key"]
            if any(x.get("registry_key") == rk for x in partner.get("network_footprint") or []):
                duplicates += 1
                continue
            if upsert_footprint(partner, fp_row):
                applied += 1
                applied_city_ids.append(rk)

        bound_after = sum(1 for x in partner.get("network_footprint") or [] if x.get("registry_key"))
        fp_after = len(partner.get("network_footprint") or [])

        map_scope_mode = None
        if pid == "grab" and pid in scope_all:
            partner["_map_scope"] = materialize_map_scope_from_handoff(pid, scope_all)
            map_scope_mode = "handoff_map_scope"
        elif applied > 0 or (pid in scope_all and not partner.get("_map_scope")):
            if pid in scope_all and pid not in ("bolt", "yango", "uber", "lyft"):
                handoff_scope = materialize_map_scope_from_handoff(pid, scope_all)
                if handoff_scope and handoff_scope.get("cluster_city_ids"):
                    partner["_map_scope"] = handoff_scope
                    map_scope_mode = "handoff_map_scope"
                else:
                    partner["_map_scope"] = rebuild_map_scope_from_footprint(partner, reg, applied_city_ids)
                    map_scope_mode = "footprint_rebuild"
            elif applied > 0:
                partner["_map_scope"] = rebuild_map_scope_from_footprint(partner, reg, applied_city_ids)
                map_scope_mode = "footprint_rebuild"

        save_json(pj, partner)
        if PITCH.parent.exists():
            save_json(PITCH / f"{pid}.json", partner)

        total_applied += applied
        report["partners"][pid] = {
            "candidates_considered": len(to_apply),
            "rows_applied": applied,
            "duplicates_skipped": duplicates,
            "footprint_before": fp_before,
            "footprint_after": fp_after,
            "bound_before": bound_before,
            "bound_after": bound_after,
            "map_scope": "yes" if partner.get("_map_scope") else "no",
            "map_scope_mode": map_scope_mode,
            "latam_backlog_mode": pid in LATAM_BACKLOG_PARTNERS and bound_before == 0,
        }
        print(
            f"  ✓ {pid}: +{applied} binds, footprint {fp_before}→{fp_after}, "
            f"bound {bound_before}→{bound_after}, map_scope={report['partners'][pid]['map_scope']}"
        )

    report["rows_applied_total"] = total_applied
    report["skipped_duplicate_registry_keys"] = sum(
        p.get("duplicates_skipped", 0) for p in report["partners"].values()
    )

    out = HANDOFF / "partner-8020-inheritance-apply-report-2026-06-20.json"
    save_json(out, report)
    print(f"\nApplied {total_applied} inherited binds across {len(report['partners'])} partners")
    if report["skipped_no_partner_json"]:
        skipped = sum(x["rows"] for x in report["skipped_no_partner_json"])
        print(f"Skipped {skipped} rows — no partner JSON for: "
              f"{', '.join(x['partner_id'] for x in report['skipped_no_partner_json'])}")
    print(f"Report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())