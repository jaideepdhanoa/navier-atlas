#!/usr/bin/env python3
"""
Apply proposal fidelity audit DROP/TRIM recommendations to partner JSON.

Reads handoff/partner-map-model/PROPOSAL-FIDELITY-{partner}.json and removes
DROP items, fixes distance on TRIM items, enforces caps (≤4 journeys, ≤3 featured/phase).

Usage:
  python3 scripts/apply_proposal_fidelity_from_audit.py --partner grab
  python3 scripts/apply_proposal_fidelity_from_audit.py --partner bolt rapido --dry-run
"""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_proposal_fidelity import (  # noqa: E402
    corridor_label,
    iter_proposal_items,
    resolve_route_id,
)

HANDOFF = ROOT / "handoff" / "partner-map-model"
MAX_JOURNEYS = 4
MAX_FEATURED_PER_PHASE = 3
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def audit_key(surface: str, phase, item: dict) -> tuple:
    return (surface, str(phase), corridor_label(item), resolve_route_id(item) or "")


def load_audit_index(partner: str) -> dict[tuple, dict]:
    path = HANDOFF / f"PROPOSAL-FIDELITY-{partner}.json"
    if not path.exists():
        raise SystemExit(f"missing audit: {path}")
    record = json.loads(path.read_text())
    return {audit_key(it["surface"], it["phase"], _item_from_audit(it)): it for it in record["items"]}


def _item_from_audit(it: dict) -> dict:
    """Minimal dict so corridor_label / resolve_route_id match audit pass."""
    corridor = it.get("corridor") or ""
    if " → " in corridor:
        fl, tl = corridor.split(" → ", 1)
        return {"from": fl.strip(), "to": tl.strip(), "route_id": it.get("route_id")}
    return {"label": corridor, "route_id": it.get("route_id")}


def should_drop(rec: dict | None) -> bool:
    if not rec:
        return False
    return rec.get("recommendation") == "DROP"


def apply_trim(item: dict, rec: dict) -> dict:
    out = copy.deepcopy(item)
    route_nm = rec.get("distance_route_nm")
    if route_nm is not None and rec.get("recommendation") == "TRIM":
        for flag in rec.get("flags") or []:
            if flag.get("check") == "distance_honesty":
                out["distance_nm"] = route_nm
                break
    out["_fidelity_trim"] = {"at": TS, "audit_rec": rec.get("recommendation")}
    out["_link_source"] = "grok/apply_proposal_fidelity_from_audit"
    for k in ("_inherit_source", "_inherit_at"):
        out.pop(k, None)
    return out


def filter_list(items: list, surface: str, phase, audit_idx: dict) -> tuple[list, int, int]:
    kept: list = []
    dropped = 0
    trimmed = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        key = audit_key(surface, phase, item)
        rec = audit_idx.get(key)
        if rec and should_drop(rec):
            dropped += 1
            continue
        if rec and rec.get("recommendation") == "TRIM":
            kept.append(apply_trim(item, rec))
            trimmed += 1
        else:
            out = copy.deepcopy(item)
            if rec:
                out["_link_source"] = out.get("_link_source") or "grok/apply_proposal_fidelity_from_audit"
            kept.append(out)
    return kept, dropped, trimmed


def cap_journeys(journeys: list) -> list:
    return journeys[:MAX_JOURNEYS]


def cap_featured(featured: list) -> list:
    return featured[:MAX_FEATURED_PER_PHASE]


def load_original_doc(path: Path) -> dict:
    rel = path.relative_to(ROOT).as_posix()
    try:
        raw = subprocess.check_output(["git", "show", f"HEAD:{rel}"], cwd=ROOT, stderr=subprocess.DEVNULL)
        return json.loads(raw)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return json.loads(path.read_text())


def keep_item(item: dict, surface: str, phase, audit_idx: dict) -> dict | None:
    rec = audit_idx.get(audit_key(surface, phase, item))
    if not rec or rec.get("recommendation") == "DROP":
        return None
    if rec.get("recommendation") == "TRIM":
        return apply_trim(item, rec)
    out = copy.deepcopy(item)
    out["_link_source"] = out.get("_link_source") or "grok/apply_proposal_fidelity_from_audit"
    return out


def build_keep_pool(original: dict, audit_idx: dict) -> dict[str, list[tuple[str, dict]]]:
    pool: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for kind, phase_key, item in iter_proposal_items(original):
        kept = keep_item(item, kind, phase_key, audit_idx)
        if kept:
            pool[str(phase_key)].append((kind, kept))
    return pool


def placeholder_featured(anchor_city: str | None, label: str = "Corridor seal pending — roadmap") -> dict:
    cid = anchor_city or "singapore"
    return {
        "label": label,
        "from_node_id": cid,
        "to_node_id": cid,
        "distance_nm": 0,
        "platform": "Pioneer II",
        "route_id": None,
        "display": "text_only",
        "_link_kind": "corridor-label",
        "_link_status": "unlinked-intra-city",
        "_link_source": "grok/apply_proposal_fidelity_from_audit/placeholder",
    }


def placeholder_journey(anchor_city: str | None) -> dict:
    cid = anchor_city or "singapore"
    return {
        "from": "Coastal corridor",
        "to": "Seal pending",
        "today": "Road or legacy ferry — no premium in-app water tier yet.",
        "with_navier": "Roadmap corridor — geometry and endpoint seal in progress.",
        "distance_nm": 0,
        "platform": "Pioneer II",
        "archetype": "tourism",
        "from_node_id": cid,
        "to_node_id": cid,
        "route_id": None,
        "display": "text_only",
        "_link_kind": "corridor-label",
        "_link_status": "unlinked-intra-city",
        "_link_source": "grok/apply_proposal_fidelity_from_audit/placeholder",
    }


def journey_to_featured(j: dict) -> dict:
    corridor = corridor_label(j)
    label = corridor.replace(" → ", " ↔ ") if " → " in corridor else (j.get("label") or corridor)
    out = {
        "label": label,
        "from_node_id": j.get("from_node_id"),
        "to_node_id": j.get("to_node_id"),
        "distance_nm": j.get("distance_nm"),
        "platform": j.get("platform"),
        "route_id": j.get("route_id"),
        "route_ids": j.get("route_ids"),
        "_link_kind": j.get("_link_kind") or "promoted-from-journey",
        "_link_status": j.get("_link_status"),
        "_link_source": "grok/apply_proposal_fidelity_from_audit/backfill",
        "display": j.get("display"),
    }
    return {k: v for k, v in out.items() if v is not None}


def backfill_featured(phase: dict, phase_key: str, pool: dict[str, list[tuple[str, dict]]], stats: dict) -> None:
    if phase.get("featured_routes"):
        return
    entries = list(pool.get(phase_key, []))
    if "/" in phase_key and not phase_key.startswith("market:"):
        mid = phase_key.split("/")[0]
        entries.extend(pool.get(f"market:{mid}", []))
    elif phase_key.isdigit():
        entries.extend(pool.get("None", []))
    featured = [it for kind, it in entries if kind == "featured"]
    if featured:
        phase["featured_routes"] = cap_featured(featured)
        stats["backfilled_phases"] = stats.get("backfilled_phases", 0) + 1
        return
    cities = phase.get("cities") or []
    anchor = cities[0] if cities else None
    phase["featured_routes"] = [placeholder_featured(anchor)]
    stats["placeholder_phases"] = stats.get("placeholder_phases", 0) + 1


def backfill_market_journeys(market: dict, mid: str, pool: dict[str, list[tuple[str, dict]]], stats: dict) -> None:
    if market.get("journeys_unlocked"):
        return
    entries = pool.get(f"market:{mid}", [])
    journeys = [it for kind, it in entries if kind == "journey"]
    if journeys:
        market["journeys_unlocked"] = cap_journeys(journeys)
        stats["backfilled_markets"] = stats.get("backfilled_markets", 0) + 1
        return
    anchors = market.get("anchor_cities") or []
    market["journeys_unlocked"] = [placeholder_journey(anchors[0] if anchors else None)]
    stats["placeholder_markets"] = stats.get("placeholder_markets", 0) + 1


def apply_doc(doc: dict, audit_idx: dict, *, original: dict | None = None) -> tuple[dict, dict]:
    doc = copy.deepcopy(doc)
    pool = build_keep_pool(original or doc, audit_idx)
    stats = {"dropped": 0, "trimmed": 0, "capped_journeys": 0, "capped_featured": 0}

    ju, d, t = filter_list(doc.get("journeys_unlocked") or [], "journey", None, audit_idx)
    stats["dropped"] += d
    stats["trimmed"] += t
    before = len(ju)
    ju = cap_journeys(ju)
    stats["capped_journeys"] = before - len(ju)
    doc["journeys_unlocked"] = ju

    for phase in doc.get("phases") or []:
        pn = phase.get("n")
        fr, d, t = filter_list(phase.get("featured_routes") or [], "featured", pn, audit_idx)
        stats["dropped"] += d
        stats["trimmed"] += t
        before = len(fr)
        fr = cap_featured(fr)
        stats["capped_featured"] += before - len(fr)
        phase["featured_routes"] = fr
        backfill_featured(phase, str(pn), pool, stats)

    for market in doc.get("markets") or []:
        mid = market.get("id")
        ju, d, t = filter_list(market.get("journeys_unlocked") or [], "journey", f"market:{mid}", audit_idx)
        stats["dropped"] += d
        stats["trimmed"] += t
        before = len(ju)
        ju = cap_journeys(ju)
        stats["capped_journeys"] += before - len(ju)
        market["journeys_unlocked"] = ju

        for phase in market.get("phases") or []:
            pn = phase.get("n")
            fr, d, t = filter_list(
                phase.get("featured_routes") or [],
                "featured",
                f"{mid}/p{pn}",
                audit_idx,
            )
            stats["dropped"] += d
            stats["trimmed"] += t
            before = len(fr)
            fr = cap_featured(fr)
            stats["capped_featured"] += before - len(fr)
            phase["featured_routes"] = fr
            backfill_featured(phase, f"{mid}/p{pn}", pool, stats)
        backfill_market_journeys(market, mid, pool, stats)

    doc["_fidelity_trim"] = {
        "at": TS,
        "source": "grok/apply_proposal_fidelity_from_audit",
        "stats": stats,
    }
    return doc, stats


def partner_paths(partner: str) -> list[Path]:
    paths = [ROOT / "data-clean" / "partners" / f"{partner}.json"]
    pitch = ROOT / "partner-pitch" / "partners" / f"{partner}.json"
    if pitch.exists():
        paths.append(pitch)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="+", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for slug in args.partner:
        audit_idx = load_audit_index(slug)
        for path in partner_paths(slug):
            original = load_original_doc(path)
            doc = json.loads(path.read_text())
            out, stats = apply_doc(doc, audit_idx, original=original)
            print(
                f"{slug} {path.relative_to(ROOT)}: dropped={stats['dropped']} trimmed={stats['trimmed']} "
                f"capped_j={stats['capped_journeys']} capped_fr={stats['capped_featured']} "
                f"backfill_ph={stats.get('backfilled_phases', 0)} backfill_mkt={stats.get('backfilled_markets', 0)}"
            )
            if not args.dry_run:
                path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())