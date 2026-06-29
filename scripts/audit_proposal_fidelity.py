#!/usr/bin/env python3
"""
Proposal fidelity audit — BP exactness, distance honesty, phase-narrative fit,
cross-emirate sanity, geometry preview, inheritance debt.

Read-only diagnostic (Phase A1). Writes aggregate JSON + per-partner markdown trim lists.

Usage:
  python3 scripts/audit_proposal_fidelity.py
  python3 scripts/audit_proposal_fidelity.py --partner careem noon grab rapido bolt
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from relink_partner_journeys import (  # noqa: E402
    RouteRec,
    directional_endpoints_match,
    labels_match,
    norm_label,
)

PARTNERS_DC = ROOT / "data-clean" / "partners"
HANDOFF = ROOT / "handoff" / "partner-map-model"

REFERENCE_PARTNERS = frozenset({"careem", "noon", "grab", "rapido", "bolt"})
HUB_LAYOUTS = frozenset({"hub", "network"})
DISTANCE_TOL = 0.25
LAND_KM_FAIL = 0.4
CROSS_EMIRATE_NM = 40.0
_GEOMETRY_CACHE: dict[str, float | None] = {}

PHASE_BEACHHEAD_CITIES = frozenset({"dubai-uae", "sharjah-uae"})


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def haversine_nm(lng1: float, lat1: float, lng2: float, lat2: float) -> float:
    r = 3440.065
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def build_indexes():
    routes_raw = load_json(ROOT / "data-clean" / "ROUTES.json")
    gold = set()
    route_by_id: dict[str, dict] = {}
    for f in routes_raw:
        p = f.get("properties", {})
        rid = p.get("id")
        if rid:
            gold.add(rid)
            route_by_id[rid] = {"feature": f, "props": p}

    fbt = load_json(ROOT / "data-clean" / "FEATURES_BY_TYPE.json")
    node_props: dict[str, dict] = {}
    city_ids: set[str] = set()
    for bucket in fbt:
        for feat in fbt.get(bucket, []) or []:
            props = feat.get("properties", {})
            nid = props.get("id")
            if not nid:
                continue
            node_props[nid] = props
            if bucket in ("city", "priority_city"):
                city_ids.add(nid)

    def bp_label(nid: str | None) -> str:
        if not nid:
            return ""
        p = node_props.get(nid, {})
        return (p.get("label") or p.get("name") or nid).strip()

    def city_of(nid: str | None) -> str | None:
        if not nid:
            return None
        if nid in city_ids:
            return nid
        p = node_props.get(nid, {})
        pc = p.get("parent_city_id")
        if pc in city_ids:
            return pc
        pre = str(nid).split("__")[0]
        return pre if pre in city_ids else None

    def route_rec(rid: str) -> RouteRec | None:
        entry = route_by_id.get(rid)
        if not entry:
            return None
        p = entry["props"]
        fn, tn = p.get("from"), p.get("to")
        return RouteRec(
            id=rid,
            from_label=p.get("from_label") or bp_label(fn) or (fn or ""),
            to_label=p.get("to_label") or bp_label(tn) or (tn or ""),
            from_city_id=p.get("from_city_id") or city_of(fn),
            to_city_id=p.get("to_city_id") or city_of(tn),
            from_node=fn,
            to_node=tn,
            distance_nm=p.get("distance_nm"),
            edge_class=p.get("edge_class"),
        )

    return gold, route_by_id, route_rec, city_of, bp_label


def iter_proposal_items(doc: dict):
    for j in doc.get("journeys_unlocked", []) or []:
        if isinstance(j, dict):
            yield "journey", None, j
    for phase in doc.get("phases", []) or []:
        pn = phase.get("n")
        for fr in phase.get("featured_routes", []) or []:
            if isinstance(fr, dict):
                yield "featured", pn, fr
    for market in doc.get("markets", []) or []:
        mid = market.get("id")
        for j in market.get("journeys_unlocked", []) or []:
            if isinstance(j, dict):
                yield "journey", f"market:{mid}", j
        for phase in market.get("phases", []) or []:
            pn = phase.get("n")
            for fr in phase.get("featured_routes", []) or []:
                if isinstance(fr, dict):
                    yield "featured", f"{mid}/p{pn}", fr


def phase_meta(doc: dict, phase_key) -> dict | None:
    if isinstance(phase_key, int):
        for ph in doc.get("phases", []) or []:
            if ph.get("n") == phase_key:
                return ph
    if isinstance(phase_key, str) and phase_key.startswith("market:"):
        return None
    return None


def corridor_label(item: dict) -> str:
    fl = item.get("from") or item.get("from_label") or item.get("label", "").split("→")[0].strip()
    tl = item.get("to") or item.get("to_label") or ""
    if "→" in item.get("label", "") and not tl:
        parts = item["label"].split("→", 1)
        fl, tl = parts[0].strip(), parts[1].strip()
    return f"{fl} → {tl}".strip(" →")


def resolve_route_id(item: dict) -> str | None:
    rid = item.get("route_id")
    if rid:
        return rid
    rids = item.get("route_ids") or []
    return rids[0] if rids else None


def check_bp_binding(item: dict, rec: RouteRec | None) -> list[dict]:
    flags = []
    if not rec:
        rid = resolve_route_id(item)
        if rid:
            flags.append({"check": "bp_binding", "severity": "error", "detail": f"route_id {rid} missing from ROUTES.json"})
        return flags

    from_l = item.get("from") or item.get("from_label") or ""
    to_l = item.get("to") or item.get("to_label") or ""
    if item.get("label") and not from_l:
        lab = item["label"]
        for sep in ("→", "↔", "->"):
            if sep in lab:
                parts = lab.split(sep, 1)
                if len(parts) == 2:
                    from_l, to_l = parts[0].strip(), parts[1].strip()
                break

    if not directional_endpoints_match(from_l, to_l, rec):
        flags.append({
            "check": "bp_binding",
            "severity": "error",
            "detail": (
                f"labels ≠ route endpoints: "
                f"card '{from_l}' → '{to_l}' vs route '{rec.from_label}' → '{rec.to_label}'"
            ),
        })
    return flags


def check_distance_honesty(item: dict, rec: RouteRec | None) -> list[dict]:
    flags = []
    card_dist = item.get("distance_nm")
    if card_dist is None or not rec or rec.distance_nm is None:
        return flags
    try:
        card_f = float(card_dist)
        route_f = float(rec.distance_nm)
    except (TypeError, ValueError):
        return flags
    if route_f <= 0:
        return flags
    rel = abs(card_f - route_f) / route_f
    if rel > DISTANCE_TOL:
        flags.append({
            "check": "distance_honesty",
            "severity": "warn",
            "detail": f"card {card_f}nm vs route {route_f}nm ({rel:.0%} delta)",
        })
    return flags


def check_phase_narrative_fit(
    item: dict,
    phase_key,
    doc: dict,
    rec: RouteRec | None,
    city_of,
) -> list[dict]:
    flags = []
    if not isinstance(phase_key, int):
        return flags
    phase = phase_meta(doc, phase_key)
    if not phase:
        return flags

    label = (phase.get("label") or "").lower()
    narrative = (phase.get("narrative") or "").lower()

    route_cities: set[str] = set()
    if rec:
        if rec.from_city_id:
            route_cities.add(rec.from_city_id)
        if rec.to_city_id:
            route_cities.add(rec.to_city_id)
    else:
        for nid in (item.get("from_node_id"), item.get("to_node_id")):
            c = city_of(nid)
            if c:
                route_cities.add(c)

    if "dubai beachhead" in label or ("dubai" in narrative and phase_key == 1):
        outside = route_cities - PHASE_BEACHHEAD_CITIES
        if outside:
            flags.append({
                "check": "phase_narrative_fit",
                "severity": "error",
                "detail": f"Phase {phase_key} Dubai beachhead but route cities {sorted(outside)}",
            })

    if phase_key == 1 and rec and rec.distance_nm and float(rec.distance_nm) > CROSS_EMIRATE_NM:
        flags.append({
            "check": "phase_narrative_fit",
            "severity": "error",
            "detail": f"Phase 1 beachhead but {rec.distance_nm}nm leg",
        })

    return flags


def check_cross_emirate_sanity(item: dict, kind: str, phase_key, rec: RouteRec | None) -> list[dict]:
    flags = []
    if not rec or rec.from_city_id == rec.to_city_id:
        return flags
    if not rec.from_city_id or not rec.to_city_id:
        return flags
    if not rec.from_city_id.endswith("-uae") or not rec.to_city_id.endswith("-uae"):
        return flags
    dist = float(rec.distance_nm or 0)
    if dist < CROSS_EMIRATE_NM:
        return flags

    archetype = (item.get("archetype") or "").lower()
    commerce = archetype in ("commerce_logistics", "commute", "everyday")
    if kind == "journey" and phase_key is None and commerce:
        flags.append({
            "check": "cross_emirate_sanity",
            "severity": "warn",
            "detail": f"{dist}nm cross-emirate framed as everyday commerce",
        })
    return flags


def _route_land_km(route_by_id: dict, rid: str) -> float | None:
    if rid in _GEOMETRY_CACHE:
        return _GEOMETRY_CACHE[rid]
    entry = route_by_id.get(rid)
    if not entry:
        _GEOMETRY_CACHE[rid] = None
        return None
    p = entry["props"]
    land_f = None
    coords = (entry.get("feature") or {}).get("geometry", {}).get("coordinates") or []
    if len(coords) >= 2:
        try:
            sys.path.insert(0, str(ROOT / "scripts" / "grok-geometry"))
            from route_land_qa import evaluate_route  # noqa: WPS433

            ev = evaluate_route(coords, sea_nm=p.get("distance_nm"))
            land_f = float(ev.get("interior_land_km") or 0)
        except Exception:
            land_f = None
    if land_f is None:
        land = p.get("_geometry_land_km")
        if land is None:
            land = p.get("interior_land_km")
        if land is not None:
            try:
                land_f = float(land)
            except (TypeError, ValueError):
                land_f = None
    _GEOMETRY_CACHE[rid] = land_f
    return land_f


def check_geometry_preview(route_by_id: dict, rid: str | None) -> list[dict]:
    flags = []
    if not rid or rid not in route_by_id:
        return flags
    land_f = _route_land_km(route_by_id, rid)
    if land_f is None:
        return flags
    if land_f > LAND_KM_FAIL:
        flags.append({
            "check": "geometry_preview",
            "severity": "warn",
            "detail": f"interior_land_km={land_f:.2f} (threshold {LAND_KM_FAIL})",
        })
    return flags


def check_placeholder_surface(item: dict) -> list[dict]:
    src = str(item.get("_link_source") or "")
    if "placeholder" in src.lower():
        return [{
            "check": "placeholder_surface",
            "severity": "error",
            "detail": f"_link_source={src}",
        }]
    return []


def check_inheritance_debt(item: dict) -> list[dict]:
    src = item.get("_inherit_source") or ""
    if "grok/normalize/noon" in src or "grok/normalize" in src:
        return [{
            "check": "inheritance_debt",
            "severity": "warn",
            "detail": f"_inherit_source={src}",
        }]
    link_src = item.get("_link_source") or ""
    if "relink_partner_journeys" in link_src and item.get("_inherit_source"):
        return [{
            "check": "inheritance_debt",
            "severity": "info",
            "detail": f"inherited link via {link_src}",
        }]
    return []


def recommend_action(flags: list[dict], kind: str, phase_key) -> str:
    severities = {f["severity"] for f in flags}
    checks = {f["check"] for f in flags}

    if "bp_binding" in checks and "error" in severities:
        return "DROP"
    if "phase_narrative_fit" in checks and "error" in severities:
        return "DROP" if kind == "featured" else "DEFER"
    if "geometry_preview" in checks and kind == "featured":
        return "DEFER"
    if "distance_honesty" in checks and "bp_binding" in checks:
        return "DROP"
    if "cross_emirate_sanity" in checks and kind == "journey" and phase_key is None:
        return "DEFER"
    if "inheritance_debt" in checks and not checks - {"inheritance_debt", "geometry_preview"}:
        return "KEEP"
    if not flags:
        return "KEEP"
    if kind == "featured" and "geometry_preview" in checks:
        return "DEFER"
    if severities == {"warn"} or severities <= {"warn", "info"}:
        return "TRIM"
    return "REWRITE"


def audit_item(
    slug: str,
    kind: str,
    phase_key,
    item: dict,
    doc: dict,
    gold: set[str],
    route_by_id: dict,
    route_rec,
    city_of,
) -> dict:
    rid = resolve_route_id(item)
    rec = route_rec(rid) if rid else None

    flags: list[dict] = []
    if rid and rid not in gold:
        flags.append({"check": "route_missing", "severity": "error", "detail": f"{rid} not in gold"})

    flags.extend(check_bp_binding(item, rec))
    flags.extend(check_distance_honesty(item, rec))
    flags.extend(check_phase_narrative_fit(item, phase_key, doc, rec, city_of))
    flags.extend(check_cross_emirate_sanity(item, kind, phase_key, rec))
    flags.extend(check_geometry_preview(route_by_id, rid))
    flags.extend(check_placeholder_surface(item))
    flags.extend(check_inheritance_debt(item))

    action = recommend_action(flags, kind, phase_key)
    errors = sum(1 for f in flags if f["severity"] == "error")
    warns = sum(1 for f in flags if f["severity"] == "warn")

    return {
        "surface": kind,
        "phase": phase_key,
        "corridor": corridor_label(item),
        "route_id": rid,
        "route_endpoints": (
            f"{rec.from_label} → {rec.to_label}" if rec else None
        ),
        "distance_card_nm": item.get("distance_nm"),
        "distance_route_nm": rec.distance_nm if rec else None,
        "flags": flags,
        "errors": errors,
        "warnings": warns,
        "recommendation": action,
    }


def partner_verdict(items: list[dict]) -> str:
    drops = sum(1 for i in items if i["recommendation"] == "DROP")
    errors = sum(i["errors"] for i in items)
    keeps = sum(1 for i in items if i["recommendation"] == "KEEP")
    if drops >= len(items) // 2 or errors >= 3:
        return "REWRITE"
    if drops or errors:
        return "TRIM"
    if keeps == len(items):
        return "PASS"
    return "PASS_WITH_FLAGS"


def write_partner_md(slug: str, record: dict) -> None:
    lines = [
        f"# Proposal fidelity — {slug}",
        "",
        f"**Verdict:** {record['verdict']}",
        f"**Checked:** {record['checked_at']}",
        "",
        "## Summary",
        "",
        f"- Items audited: {record['counts']['items']}",
        f"- KEEP: {record['counts']['keep']}",
        f"- DROP: {record['counts']['drop']}",
        f"- DEFER: {record['counts']['defer']}",
        f"- TRIM/REWRITE: {record['counts']['trim']}",
        f"- BP-binding errors: {record['counts']['bp_errors']}",
        "",
        "## Trim list",
        "",
        "| Surface | Phase | Corridor | Route | Rec | Flags |",
        "|---------|-------|----------|-------|-----|-------|",
    ]
    for it in record["items"]:
        flag_txt = "; ".join(f"{f['check']}: {f['detail'][:60]}" for f in it["flags"][:2])
        if len(it["flags"]) > 2:
            flag_txt += f" (+{len(it['flags']) - 2})"
        lines.append(
            f"| {it['surface']} | {it['phase'] or '—'} | {it['corridor'][:50]} | "
            f"`{it['route_id'] or '—'}` | **{it['recommendation']}** | {flag_txt or '—'} |"
        )

    if slug == "careem":
        lines.extend([
            "",
            "## Careem Phase 1 target keep set (post-trim)",
            "",
            "**journeys_unlocked (≤4):**",
            "- Dubai Harbour Marina → Nikki Beach Resort Pearl Jumeirah Jetty (`rn-b1ba183aa886`)",
            "- Fujairah east-coast cluster → Dibba · Khor Fakkan · Kalba (`gcn-8f0d49bbde-careem` / `rn-bc685bdb0da3`)",
            "- Ushuaïa Dubai Harbour → Marina Mall / Breakwater Marina — **defer to Phase 2** (not hub journeys)",
            "",
            "**Phase 1 featured_routes (≤3, Dubai beachhead):**",
            "- KEEP: Dubai Harbour Marina → Nikki Beach (`rn-b1ba183aa886`)",
            "- KEEP: Vida Beach Resort UAQ → Sharjah Waterfront City marina (`rn-02a40748974d`) — Sharjah/Dubai adjacency",
            "- DROP: Yas Marina → Four Seasons (Abu Dhabi; not beachhead)",
            "- DROP: Fujairah → Khorfakkan (east coast; defer Phase 3)",
            "- DROP: RAK → Ghallilah (RAK; phase-narrative misfit + 5.2km land)",
            "",
            "**DROP from journeys_unlocked:**",
            "- Yas Marina → Four Seasons (`rn-f46231fb7baf` binds Bahrain BP pair)",
            "- RAK → Ghallilah (wrong endpoint pair on route)",
            "- Dubai Harbour → Nikki Beach (`gcn-6a2841d6db-careem` — Anantara World Islands leak)",
        ])

    path = HANDOFF / f"PROPOSAL-FIDELITY-{slug}.md"
    path.write_text("\n".join(lines) + "\n")


def audit_partner(slug: str, doc: dict, indexes) -> dict:
    gold, route_by_id, route_rec, city_of, _ = indexes
    items = []
    for kind, phase_key, item in iter_proposal_items(doc):
        if item.get("display") == "network_chip":
            continue
        items.append(
            audit_item(slug, kind, phase_key, item, doc, gold, route_by_id, route_rec, city_of)
        )

    counts = {
        "items": len(items),
        "keep": sum(1 for i in items if i["recommendation"] == "KEEP"),
        "drop": sum(1 for i in items if i["recommendation"] == "DROP"),
        "defer": sum(1 for i in items if i["recommendation"] == "DEFER"),
        "trim": sum(1 for i in items if i["recommendation"] in ("TRIM", "REWRITE")),
        "bp_errors": sum(1 for i in items if any(f["check"] == "bp_binding" for f in i["flags"])),
    }

    record = {
        "partner": slug,
        "verdict": partner_verdict(items),
        "layout": doc.get("layout"),
        "hub": is_hub_partner(doc),
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "counts": counts,
        "items": items,
    }
    return record


def journey_bp_errors(record: dict) -> int:
    """S-tier (journeys_unlocked) BP-binding failures only — preflight §3.7 gate."""
    return sum(
        1
        for it in record.get("items", [])
        if it.get("surface") == "journey"
        and any(f.get("check") == "bp_binding" for f in it.get("flags", []))
    )


def geometry_gate_errors(record: dict) -> int:
    """Featured/journey routes with interior_land_km > LAND_KM_FAIL — §3.7 hard gate."""
    return sum(
        1
        for it in record.get("items", [])
        if it.get("surface") in ("journey", "featured")
        and any(f.get("check") == "geometry_preview" for f in it.get("flags", []))
    )


def placeholder_gate_errors(record: dict) -> int:
    return sum(
        1
        for it in record.get("items", [])
        if any(f.get("check") == "placeholder_surface" for f in it.get("flags", []))
    )


def is_hub_partner(doc: dict) -> bool:
    return doc.get("layout") in HUB_LAYOUTS and bool(doc.get("markets"))


def resolve_audit_slugs(args) -> list[str]:
    if args.partner:
        return list(args.partner)
    if args.all_partners:
        return sorted(
            p.stem for p in PARTNERS_DC.glob("*.json") if not p.name.startswith("_")
        )
    if args.hub_partners:
        slugs: list[str] = []
        for path in sorted(PARTNERS_DC.glob("*.json")):
            if path.name.startswith("_"):
                continue
            doc = load_json(path)
            if is_hub_partner(doc):
                slugs.append(path.stem)
        for ref in sorted(REFERENCE_PARTNERS):
            if ref not in slugs:
                slugs.append(ref)
        return slugs
    return sorted(REFERENCE_PARTNERS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="*", help="Limit to partner slug(s)")
    ap.add_argument("--hub-partners", action="store_true", help="Audit all hub-layout partners (~29)")
    ap.add_argument("--all-partners", action="store_true", help="Audit all data-clean partners (62)")
    ap.add_argument(
        "--strict-journey-gate",
        action="store_true",
        help="Exit 1 if any audited partner has S-tier (journey) BP-binding errors",
    )
    ap.add_argument(
        "--strict-deploy-gate",
        action="store_true",
        help="Exit 1 on §3.7 hard gates: journey BP, geometry, placeholders, reference REWRITE",
    )
    args = ap.parse_args()

    indexes = build_indexes()
    slugs = resolve_audit_slugs(args)

    results = []
    for slug in slugs:
        path = PARTNERS_DC / f"{slug}.json"
        if not path.is_file():
            print(f"skip {slug}: no data-clean JSON")
            continue
        doc = load_json(path)
        rec = audit_partner(slug, doc, indexes)
        rec["journey_bp_errors"] = journey_bp_errors(rec)
        rec["geometry_gate_errors"] = geometry_gate_errors(rec)
        rec["placeholder_gate_errors"] = placeholder_gate_errors(rec)
        results.append(rec)
        write_partner_md(slug, rec)
        save_json(HANDOFF / f"PROPOSAL-FIDELITY-{slug}.json", rec)

    aggregate = {
        "package": "proposal-fidelity-audit",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "partners": [
            {k: v for k, v in r.items() if k != "items"}
            | {"items": len(r["items"]), "journey_bp_errors": r.get("journey_bp_errors", 0)}
            for r in results
        ],
        "detail_by_partner": {r["partner"]: r for r in results},
    }
    save_json(HANDOFF / "PROPOSAL-FIDELITY-AUDIT.json", aggregate)

    print(f"Proposal fidelity — {len(results)} partners")
    gate_fail = False
    gate_reasons: list[str] = []
    for r in results:
        c = r["counts"]
        jbe = r.get("journey_bp_errors", 0)
        gge = r.get("geometry_gate_errors", 0)
        pge = r.get("placeholder_gate_errors", 0)
        print(
            f"  {r['verdict']:16} {r['partner']:10} "
            f"items={c['items']} keep={c['keep']} drop={c['drop']} "
            f"defer={c['defer']} bp_err={c['bp_errors']} journey_bp={jbe}"
            + (f" geom={gge}" if gge else "")
            + (f" placeholder={pge}" if pge else "")
        )
        if args.strict_journey_gate and jbe > 0:
            gate_fail = True
            gate_reasons.append(f"{r['partner']}: {jbe} journey BP error(s)")
        if args.strict_deploy_gate:
            # Tiered §3.7: placeholder all partners; journey_bp hub-scope or reference-only
            # when --all-partners; REWRITE/PASS_WITH_FLAGS reference partners only.
            journey_gate = (not args.all_partners) or r["partner"] in REFERENCE_PARTNERS
            if jbe > 0 and journey_gate:
                gate_fail = True
                gate_reasons.append(f"{r['partner']}: journey_bp={jbe}")
            if gge > 0:
                gate_fail = True
                gate_reasons.append(f"{r['partner']}: geometry_gate={gge}")
            if pge > 0:
                gate_fail = True
                gate_reasons.append(f"{r['partner']}: placeholder={pge}")
            if r["partner"] in REFERENCE_PARTNERS and r["verdict"] == "REWRITE":
                gate_fail = True
                gate_reasons.append(f"{r['partner']}: REWRITE verdict")
            if r["partner"] in REFERENCE_PARTNERS and r["verdict"] == "PASS_WITH_FLAGS":
                gate_fail = True
                gate_reasons.append(f"{r['partner']}: PASS_WITH_FLAGS (trim flags remain)")

    if gate_fail:
        print("✗ deploy gate FAILED:")
        for reason in gate_reasons:
            print(f"    - {reason}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())