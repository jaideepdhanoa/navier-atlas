#!/usr/bin/env python3
"""Apply PR #55 exact-binding + coastal inheritance footprint updates.

Reads handoff/partner-map-model/partner-market-coverage-targeted-exact-binding-batch-2026-06-20.json
and HANDOFF.md coastal inheritance rules. Additive only — never shrinks footprint.
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

# HANDOFF.md coastal inheritance — broad story → registry_key (additive binds)
INHERITANCE_BINDS: dict[str, dict[str, str]] = {
    "lyft": {"athens-cyclades": "bolt-greece"},
}

# map-scope.json registry keys → footprint rows (additive for partners lacking binds)
MAP_SCOPE_ADDITIONS: dict[str, list[dict]] = {
    "uber": [
        {"registry_key": "uae-careem", "label": "UAE", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "uae-luxury", "label": "UAE Luxury", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "qatar", "label": "Qatar", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "saudi-redsea", "label": "Saudi Red Sea", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "saudi-redsea-resort", "label": "Saudi Red Sea Resorts", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "bolt-egypt", "label": "Egypt", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "yango-egypt", "label": "Egypt (Yango)", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "yango-morocco", "label": "Morocco", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "yango-tunisia", "label": "Tunisia", "region": "MENA", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
        {"registry_key": "bolt-greece", "label": "Greece", "region": "Europe", "tier": "sub_proposal", "render": "cluster_dots", "map_promote": False},
        {"registry_key": "bolt-croatia", "label": "Croatia", "region": "Europe", "tier": "sub_proposal", "render": "cluster_dots", "map_promote": False},
        {"registry_key": "bolt-italy", "label": "Italy", "region": "Europe", "tier": "sub_proposal", "render": "cluster_dots", "map_promote": False},
        {"registry_key": "bolt-france-riviera", "label": "France Riviera", "region": "Europe", "tier": "sub_proposal", "render": "cluster_dots", "map_promote": False},
        {"registry_key": "bolt-cyprus", "label": "Cyprus", "region": "Europe", "tier": "sub_proposal", "render": "cluster_dots", "map_promote": False},
        {"registry_key": "yango-turkey", "label": "Turkey", "region": "Europe", "tier": "sub_proposal", "render": "geometry", "map_promote": True},
    ],
}


def load_json(p: Path) -> dict:
    return json.loads(p.read_text())


def save_json(p: Path, obj: dict) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def footprint_row(
    *,
    entry_id: str,
    registry_key: str,
    label: str,
    region: str,
    tier: str = "corridor_ready",
    render: str = "geometry",
    map_promote: bool = False,
    covered: bool = False,
) -> dict:
    return {
        "id": entry_id,
        "registry_key": registry_key,
        "covered": covered,
        "tier": tier,
        "render": render,
        "map_promote": map_promote,
        "label": label,
        "country": None,
        "countries": [],
        "region": region,
        "_binding_source": "grok/apply_partner_coverage_bindings",
    }


def upsert_footprint(partner: dict, row: dict) -> bool:
    fp = partner.setdefault("network_footprint", [])
    rid = row["registry_key"]
    existing = next((x for x in fp if x.get("registry_key") == rid or x.get("id") == row["id"]), None)
    if existing:
        before = deepcopy(existing)
        existing.update(row)
        return existing != before
    fp.append(row)
    return True


def apply_exact_batch(partner: dict, items: list[dict], partner_id: str) -> int:
    changed = 0
    for item in items:
        if item.get("partner_id") != partner_id:
            continue
        rk = item.get("registry_key")
        if not rk:
            continue
        row = footprint_row(
            entry_id=rk,
            registry_key=rk,
            label=item.get("display") or rk,
            region=item.get("region") or "Global",
            tier="corridor_ready",
            render="geometry",
            map_promote=True,
        )
        if upsert_footprint(partner, row):
            changed += 1
    return changed


def apply_inheritance(partner: dict, partner_id: str) -> int:
    binds = INHERITANCE_BINDS.get(partner_id, {})
    changed = 0
    for fp in partner.get("network_footprint") or []:
        fid = fp.get("id")
        if fid in binds and not fp.get("registry_key"):
            fp["registry_key"] = binds[fid]
            fp["render"] = "cluster_dots"
            fp["tier"] = "corridor_ready"
            fp["_binding_source"] = "grok/coastal-inheritance"
            changed += 1
    return changed


def apply_map_scope_additions(partner: dict, partner_id: str) -> int:
    additions = MAP_SCOPE_ADDITIONS.get(partner_id, [])
    changed = 0
    for spec in additions:
        rk = spec["registry_key"]
        row = footprint_row(
            entry_id=rk,
            registry_key=rk,
            label=spec["label"],
            region=spec["region"],
            tier=spec.get("tier", "sub_proposal"),
            render=spec.get("render", "geometry"),
            map_promote=spec.get("map_promote", False),
            covered=False,
        )
        if upsert_footprint(partner, row):
            changed += 1
    return changed


def materialize_map_scope(partner: dict, partner_id: str) -> bool:
    scope_path = HANDOFF / "map-scope.json"
    if not scope_path.exists():
        return False
    scope_all = load_json(scope_path)
    block = scope_all.get(partner_id)
    if not block:
        return False
    partner["_map_scope"] = {
        "_doc": "LB-261 materialized from handoff/partner-map-model/map-scope.json",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "handoff/partner-map-model/map-scope.json",
        "registry_keys": block.get("registry_keys") or [],
        "cluster_city_ids": sorted(set(block.get("sealed_cluster_cities") or [])),
    }
    return True


def main() -> int:
    batch_path = HANDOFF / "partner-market-coverage-targeted-exact-binding-batch-2026-06-20.json"
    if not batch_path.exists():
        print(f"✗ missing {batch_path}", file=sys.stderr)
        return 1
    batch = load_json(batch_path)
    exact = batch.get("exact_supported") or []

    targets = sorted({x["partner_id"] for x in exact} | set(INHERITANCE_BINDS) | set(MAP_SCOPE_ADDITIONS))
    report: dict[str, dict] = {}

    for pid in targets:
        pj = PARTNERS / f"{pid}.json"
        if not pj.exists():
            print(f"  skip {pid}: no partner JSON")
            continue
        partner = load_json(pj)
        before = len(partner.get("network_footprint") or [])
        bound_before = sum(1 for x in partner.get("network_footprint") or [] if x.get("registry_key"))

        n_exact = apply_exact_batch(partner, exact, pid)
        n_inherit = apply_inheritance(partner, pid)
        n_scope = apply_map_scope_additions(partner, pid)
        scope_ok = materialize_map_scope(partner, pid)

        after = len(partner.get("network_footprint") or [])
        bound_after = sum(1 for x in partner.get("network_footprint") or [] if x.get("registry_key"))

        save_json(pj, partner)
        if PITCH.parent.exists():
            save_json(PITCH / f"{pid}.json", partner)

        report[pid] = {
            "footprint_before": before,
            "footprint_after": after,
            "bound_before": bound_before,
            "bound_after": bound_after,
            "exact_applied": n_exact,
            "inheritance_applied": n_inherit,
            "map_scope_additions": n_scope,
            "map_scope_materialized": scope_ok,
        }
        print(f"  ✓ {pid}: footprint {before}→{after}, bound {bound_before}→{bound_after} "
              f"(exact={n_exact} inherit={n_inherit} scope_add={n_scope})")

    out = HANDOFF / "binding-apply-report.json"
    save_json(out, {"at": datetime.now(timezone.utc).isoformat(), "partners": report})
    print(f"Report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())