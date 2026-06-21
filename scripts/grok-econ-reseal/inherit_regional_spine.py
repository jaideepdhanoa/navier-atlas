#!/usr/bin/env python3
"""Regional spine inheritance — scaffold, bind geometry, normalize corporate overlays.

Reads handoff/partner-map-model/regional-inheritance-manifest.json and optional
region spine JSON (_template block). Reference partner is the sealed card template;
derivatives inherit bind fields by canonical card keys.

Usage:
  python3 inherit_regional_spine.py --bind --all
  python3 inherit_regional_spine.py --bind --partner ola adani-ports
  python3 inherit_regional_spine.py --audit-only --all
  python3 inherit_regional_spine.py --normalize-corporate --partner adani-ports reliance-industries
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PARTNERS = ROOT / "partner-pitch" / "partners"
DRAFT = PARTNERS / "_draft"
HANDOFF = ROOT / "handoff" / "partner-map-model"
MANIFEST_PATH = ROOT / "handoff" / "partner-map-model" / "regional-inheritance-manifest.json"

BIND_FIELDS = (
    "route_id", "route_ids", "from_node_id", "to_node_id", "distance_nm",
    "platform", "vessel_gate", "_link_kind", "_link_status", "_link_source",
    "economics_status", "model_link", "display",
)

OVERLAY_TEXT_FIELDS = frozenset({"from", "to", "today", "with_navier", "label", "narrative", "rationale"})


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def norm(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def norm_label(s: str | None) -> str:
    """Looser label match — strips parentheticals and normalizes separators."""
    s = norm(s)
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[/|]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def journey_key(market: str | None, item: dict) -> tuple[str, str, str]:
    return (market or "hub", norm_label(item.get("from")), norm_label(item.get("to")))


def featured_label(item: dict) -> str:
    label = norm_label(item.get("label"))
    if label:
        return label
    return norm_label(f"{item.get('from', '')} {item.get('to', '')}")


def featured_key(market: str | None, phase_n: Any, item: dict) -> tuple[str, str, str]:
    return (market or "hub", str(phase_n), featured_label(item))


def find_journey_overlay(targets: list[dict], ref_j: dict) -> dict | None:
    rk = journey_key(None, ref_j)
    ref_rid = ref_j.get("route_id")
    for j in targets:
        if not isinstance(j, dict):
            continue
        if journey_key(None, j) == rk:
            return j
    if ref_rid:
        for j in targets:
            if not isinstance(j, dict):
                continue
            if j.get("route_id") == ref_rid:
                return j
            rids = j.get("route_ids") or []
            if ref_rid in rids:
                return j
    ref_from = norm_label(ref_j.get("from"))
    ref_to = norm_label(ref_j.get("to"))
    for j in targets:
        if not isinstance(j, dict):
            continue
        jf, jt = norm_label(j.get("from")), norm_label(j.get("to"))
        if ref_from and ref_to and ref_from[:10] in jf and ref_to[:10] in jt:
            return j
    return None


def partner_path(slug: str) -> Path | None:
    for base in (PARTNERS, DRAFT):
        p = base / f"{slug}.json"
        if p.is_file():
            return p
    return None


def iter_cards(doc: dict):
    for j in doc.get("journeys_unlocked") or []:
        if isinstance(j, dict):
            yield "journey", None, None, j
    for ph in doc.get("phases") or []:
        pn = ph.get("n")
        for j in ph.get("journeys_unlocked") or []:
            if isinstance(j, dict):
                yield "journey", None, pn, j
        for fr in ph.get("featured_routes") or []:
            if isinstance(fr, dict):
                yield "featured", None, pn, fr
    for m in doc.get("markets") or []:
        mid = m.get("id")
        for j in m.get("journeys_unlocked") or []:
            if isinstance(j, dict):
                yield "journey", mid, None, j
        for ph in m.get("phases") or []:
            pn = ph.get("n")
            for fr in ph.get("featured_routes") or []:
                if isinstance(fr, dict):
                    yield "featured", mid, pn, fr


def build_card_index(doc: dict) -> dict[tuple, dict]:
    idx: dict[tuple, dict] = {}
    for kind, mid, pn, item in iter_cards(doc):
        if kind == "journey":
            key = journey_key(mid, item)
        else:
            key = featured_key(mid, pn, item)
        idx[key] = item
    return idx


def merge_bind_fields(target: dict, ref: dict, *, source_tag: str) -> list[str]:
    notes: list[str] = []
    for field in BIND_FIELDS:
        if field in ref and ref.get(field) is not None:
            if target.get(field) != ref[field]:
                target[field] = copy.deepcopy(ref[field])
                notes.append(field)
    if notes:
        target["_inherit_source"] = source_tag
        target["_inherit_at"] = utc_now()
    return notes


def bind_partner(
    target_slug: str,
    *,
    manifest: dict,
    dry_run: bool = False,
) -> dict[str, Any]:
    pack_id = manifest["partner_pack"].get(target_slug)
    if not pack_id:
        return {"partner": target_slug, "status": "skipped", "reason": "no pack"}
    pack = manifest["packs"][pack_id]
    ref_slug = pack["reference_partner"]
    if target_slug == ref_slug:
        return {"partner": target_slug, "status": "reference", "pack": pack_id}

    ref_path = partner_path(ref_slug)
    tgt_path = partner_path(target_slug)
    if not ref_path or not tgt_path:
        return {"partner": target_slug, "status": "skipped", "reason": "missing file"}

    ref_doc = load_json(ref_path)
    tgt_doc = load_json(tgt_path)
    ref_idx = build_card_index(ref_doc)
    mode = pack.get("route_scope_mode", "display_markets")
    bound = 0
    missing = 0
    extras = 0

    for kind, mid, pn, item in iter_cards(tgt_doc):
        if kind == "journey":
            key = journey_key(mid, item)
        else:
            key = featured_key(mid, pn, item)
        ref_item = ref_idx.get(key)
        if ref_item:
            if not dry_run:
                merge_bind_fields(item, ref_item, source_tag=f"grok/inherit/{ref_slug}")
            bound += 1
        else:
            if mode == "subset":
                continue
            if mid and mid in (pack.get("brief_only_market_ids") or []):
                item.setdefault("_bind_status", "brief_only_no_reference_card")
                continue
            missing += 1

    for key in ref_idx:
        # keys in reference not in target
        found = False
        for kind, mid, pn, item in iter_cards(tgt_doc):
            k = journey_key(mid, item) if kind == "journey" else featured_key(mid, pn, item)
            if k == key:
                found = True
                break
        if not found and mode != "subset":
            extras += 0  # tracked in parity audit

    tgt_doc.setdefault("_regional_inheritance", {})
    tgt_doc["_regional_inheritance"].update({
        "pack": pack_id,
        "reference_partner": ref_slug,
        "applied_at": utc_now(),
        "mode": mode,
        "bound_cards": bound,
        "missing_reference_keys": missing,
    })

    if not dry_run:
        save_json(tgt_path, tgt_doc)
        dc = ROOT / "data-clean" / "partners" / f"{target_slug}.json"
        if dc.parent.exists():
            save_json(dc, tgt_doc)

    return {
        "partner": target_slug,
        "status": "bound",
        "pack": pack_id,
        "reference": ref_slug,
        "bound": bound,
        "missing_keys": missing,
    }


def sync_hub_to_reference(ref_doc: dict, tgt_doc: dict, *, ref_slug: str) -> None:
    ref_hub_list = [
        j for kind, mid, pn, j in iter_cards(ref_doc) if kind == "journey" and mid is None
    ]
    tgt_journey_pool = [
        j for j in (tgt_doc.get("journeys_unlocked") or []) if isinstance(j, dict)
    ]
    for kind, mid, pn, j in iter_cards(tgt_doc):
        if kind == "journey":
            tgt_journey_pool.append(j)
    new_hub = []
    for ref_j in ref_hub_list:
        overlay = find_journey_overlay(tgt_journey_pool, ref_j)
        merged = copy.deepcopy(overlay or ref_j)
        if overlay:
            for field in OVERLAY_TEXT_FIELDS:
                if overlay.get(field):
                    merged[field] = copy.deepcopy(overlay[field])
        merge_bind_fields(merged, ref_j, source_tag=f"grok/normalize/{ref_slug}")
        new_hub.append(merged)
    if ref_hub_list:
        tgt_doc["journeys_unlocked"] = new_hub

    ref_phases = [p for p in (ref_doc.get("phases") or []) if isinstance(p, dict)]
    tgt_phases = {p.get("n"): p for p in (tgt_doc.get("phases") or []) if isinstance(p, dict)}
    new_phases = []
    for ref_ph in ref_phases:
        pn = ref_ph.get("n")
        tgt_ph = tgt_phases.get(pn) or {}
        merged_ph = copy.deepcopy(ref_ph)
        for field in ("narrative", "rationale", "label", "timeline", "use_cases", "boats", "fleet_confidence"):
            if tgt_ph.get(field) is not None:
                merged_ph[field] = copy.deepcopy(tgt_ph[field])
        tgt_featured = {
            featured_label(fr): fr
            for fr in (tgt_ph.get("featured_routes") or [])
            if isinstance(fr, dict)
        }
        synced_featured = []
        for ref_fr in ref_ph.get("featured_routes") or []:
            if not isinstance(ref_fr, dict):
                continue
            card = copy.deepcopy(ref_fr)
            overlay_fr = tgt_featured.get(featured_label(ref_fr))
            if not overlay_fr:
                for tfr in tgt_featured.values():
                    if ref_fr.get("route_id") and tfr.get("route_id") == ref_fr.get("route_id"):
                        overlay_fr = tfr
                        break
                    ref_rids = set(ref_fr.get("route_ids") or [])
                    t_rids = set(tfr.get("route_ids") or [])
                    if ref_rids and t_rids and ref_rids & t_rids:
                        overlay_fr = tfr
                        break
            if overlay_fr:
                for field in OVERLAY_TEXT_FIELDS:
                    if overlay_fr.get(field):
                        card[field] = copy.deepcopy(overlay_fr[field])
            merge_bind_fields(card, ref_fr, source_tag=f"grok/normalize/{ref_slug}")
            synced_featured.append(card)
        merged_ph["featured_routes"] = synced_featured
        new_phases.append(merged_ph)
    if ref_phases:
        tgt_doc["phases"] = new_phases


def sync_market_phases_to_reference(
    ref_doc: dict, tgt_doc: dict, *, ref_slug: str, display_ids: set[str]
) -> None:
    ref_idx = build_card_index(ref_doc)
    for m in tgt_doc.get("markets") or []:
        mid = m.get("id")
        if mid not in display_ids:
            continue
        ref_m = next((x for x in (ref_doc.get("markets") or []) if x.get("id") == mid), None)
        ref_m_phases = {
            p.get("n"): p for p in (ref_m or {}).get("phases") or [] if isinstance(p, dict)
        }
        for ph in m.get("phases") or []:
            if not isinstance(ph, dict):
                continue
            ref_ph = ref_m_phases.get(ph.get("n"))
            if not ref_ph:
                continue
            tgt_featured = {
                featured_label(fr): fr
                for fr in (ph.get("featured_routes") or [])
                if isinstance(fr, dict)
            }
            synced = []
            for ref_fr in ref_ph.get("featured_routes") or []:
                if not isinstance(ref_fr, dict):
                    continue
                card = copy.deepcopy(ref_fr)
                overlay_fr = tgt_featured.get(featured_label(ref_fr))
                if overlay_fr:
                    for field in OVERLAY_TEXT_FIELDS:
                        if overlay_fr.get(field):
                            card[field] = copy.deepcopy(overlay_fr[field])
                merge_bind_fields(card, ref_fr, source_tag=f"grok/normalize/{ref_slug}")
                synced.append(card)
            ph["featured_routes"] = synced
        for kind, mid2, pn, item in iter_cards({"markets": [m]}):
            if kind != "featured":
                continue
            ref_item = ref_idx.get(featured_key(mid2, pn, item))
            if ref_item:
                merge_bind_fields(item, ref_item, source_tag=f"grok/normalize/{ref_slug}")


def normalize_to_reference(
    target_slug: str,
    *,
    manifest: dict,
    dry_run: bool = False,
    corporate_brief: bool = False,
) -> dict[str, Any]:
    pack_id = manifest["partner_pack"].get(target_slug)
    pack = manifest["packs"].get(pack_id or "", {})
    ref_slug = pack.get("reference_partner", "rapido")
    if target_slug == ref_slug:
        return {"partner": target_slug, "status": "reference", "pack": pack_id}
    ref_path = partner_path(ref_slug)
    tgt_path = partner_path(target_slug)
    if not ref_path or not tgt_path:
        return {"partner": target_slug, "status": "skipped"}

    ref_doc = load_json(ref_path)
    tgt_doc = load_json(tgt_path)
    brief_ids = set(pack.get("brief_only_market_ids") or []) if corporate_brief else set()
    display_ids = set(pack.get("display_market_ids") or [])

    sync_hub_to_reference(ref_doc, tgt_doc, ref_slug=ref_slug)
    if display_ids:
        sync_market_phases_to_reference(
            ref_doc, tgt_doc, ref_slug=ref_slug, display_ids=display_ids
        )

    brief_markets: list[dict] = []
    if corporate_brief and brief_ids:
        kept_markets = []
        for m in tgt_doc.get("markets") or []:
            if m.get("id") in brief_ids:
                m["scope_status"] = "brief_only_until_atlas_ids"
                m["anchor_cities"] = []
                m["map_promote"] = False
                brief_markets.append(m)
            else:
                kept_markets.append(m)
        tgt_doc["markets"] = kept_markets
        tgt_doc["brief_only_markets"] = [
            {"id": m.get("id"), "slug": m.get("slug"), "label": m.get("label")}
            for m in brief_markets
        ]
        tgt_doc["markets"].extend(brief_markets)

    tgt_doc.setdefault("_regional_inheritance", {})
    tgt_doc["_regional_inheritance"]["normalized_to_reference"] = utc_now()
    if not dry_run:
        save_json(tgt_path, tgt_doc)
        dc = ROOT / "data-clean" / "partners" / f"{target_slug}.json"
        if dc.is_file() or dc.parent.exists():
            save_json(dc, tgt_doc)

    return {
        "partner": target_slug,
        "status": "normalized",
        "reference": ref_slug,
        "brief_markets": list(brief_ids),
    }


def normalize_corporate_partner(
    target_slug: str,
    *,
    manifest: dict,
    dry_run: bool = False,
) -> dict[str, Any]:
    return normalize_to_reference(
        target_slug, manifest=manifest, dry_run=dry_run, corporate_brief=True
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bind", action="store_true")
    ap.add_argument("--audit-only", action="store_true")
    ap.add_argument("--normalize-corporate", action="store_true")
    ap.add_argument(
        "--normalize-mirror",
        action="store_true",
        help="Trim derivative hub inventory to pack reference (e.g. Careem→Noon)",
    )
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--partner", nargs="*", default=[])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = load_json(MANIFEST_PATH)
    slugs = args.partner or (list(manifest["partner_pack"].keys()) if args.all else [])
    if not slugs:
        ap.error("specify --partner or --all")

    results = []
    for slug in slugs:
        if args.normalize_corporate:
            results.append(normalize_corporate_partner(slug, manifest=manifest, dry_run=args.dry_run))
        elif args.normalize_mirror:
            results.append(normalize_to_reference(slug, manifest=manifest, dry_run=args.dry_run))
        if args.bind or args.audit_only:
            results.append(bind_partner(slug, manifest=manifest, dry_run=args.dry_run or args.audit_only))

    report = {
        "lane": "grok/inherit_regional_spine",
        "at": utc_now(),
        "dry_run": args.dry_run,
        "results": results,
    }
    out = ROOT / "handoff" / "partner-map-model" / "regional-inheritance-apply-report.json"
    save_json(out, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())