#!/usr/bin/env python3
"""
Apply proposal fidelity audit TRIM recommendations only (RE-GROUND lane).

DROP is gated behind --allow-drop (requires per-item audit receipt).
Placeholder backfill is prohibited — empty carousel beats fake corridor.

Usage:
  python3 scripts/apply_proposal_fidelity_from_audit.py --partner careem --trim-only
  python3 scripts/apply_proposal_fidelity_from_audit.py --partner grab --allow-drop  # discouraged
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_proposal_fidelity import (  # noqa: E402
    corridor_label,
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
    corridor = it.get("corridor") or ""
    if " → " in corridor:
        fl, tl = corridor.split(" → ", 1)
        return {"from": fl.strip(), "to": tl.strip(), "route_id": it.get("route_id")}
    return {"label": corridor, "route_id": it.get("route_id")}


def apply_trim(item: dict, rec: dict) -> dict:
    out = copy.deepcopy(item)
    route_nm = rec.get("distance_route_nm")
    if route_nm is not None and rec.get("recommendation") == "TRIM":
        for flag in rec.get("flags") or []:
            if flag.get("check") == "distance_honesty":
                out["distance_nm"] = route_nm
                break
    out["_fidelity_trim"] = {"at": TS, "audit_rec": rec.get("recommendation")}
    out["_link_source"] = "grok/apply_proposal_fidelity_trim"
    for k in ("_inherit_source", "_inherit_at"):
        out.pop(k, None)
    return out


def filter_list(
    items: list,
    surface: str,
    phase,
    audit_idx: dict,
    *,
    allow_drop: bool,
) -> tuple[list, int, int]:
    kept: list = []
    dropped = 0
    trimmed = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        key = audit_key(surface, phase, item)
        rec = audit_idx.get(key)
        if rec and rec.get("recommendation") == "DROP":
            if allow_drop:
                dropped += 1
                continue
        if rec and rec.get("recommendation") == "TRIM":
            kept.append(apply_trim(item, rec))
            trimmed += 1
        else:
            kept.append(copy.deepcopy(item))
    return kept, dropped, trimmed


def cap_journeys(journeys: list) -> list:
    return journeys[:MAX_JOURNEYS]


def cap_featured(featured: list) -> list:
    return featured[:MAX_FEATURED_PER_PHASE]


def mark_intentional_null(phase: dict) -> None:
    if not phase.get("featured_routes"):
        phase["_fidelity_trim"] = {
            "at": TS,
            "intentional_null": True,
            "reason": "no_s_tier_featured_after_reground",
        }


def apply_doc(doc: dict, audit_idx: dict, *, allow_drop: bool) -> tuple[dict, dict]:
    doc = copy.deepcopy(doc)
    stats = {"dropped": 0, "trimmed": 0, "capped_journeys": 0, "capped_featured": 0, "intentional_null_phases": 0}

    ju, d, t = filter_list(doc.get("journeys_unlocked") or [], "journey", None, audit_idx, allow_drop=allow_drop)
    stats["dropped"] += d
    stats["trimmed"] += t
    before = len(ju)
    ju = cap_journeys(ju)
    stats["capped_journeys"] = before - len(ju)
    doc["journeys_unlocked"] = ju

    for phase in doc.get("phases") or []:
        pn = phase.get("n")
        fr, d, t = filter_list(phase.get("featured_routes") or [], "featured", pn, audit_idx, allow_drop=allow_drop)
        stats["dropped"] += d
        stats["trimmed"] += t
        before = len(fr)
        fr = cap_featured(fr)
        stats["capped_featured"] += before - len(fr)
        phase["featured_routes"] = fr
        if not fr:
            mark_intentional_null(phase)
            stats["intentional_null_phases"] += 1

    for market in doc.get("markets") or []:
        mid = market.get("id")
        ju, d, t = filter_list(market.get("journeys_unlocked") or [], "journey", f"market:{mid}", audit_idx, allow_drop=allow_drop)
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
                allow_drop=allow_drop,
            )
            stats["dropped"] += d
            stats["trimmed"] += t
            before = len(fr)
            fr = cap_featured(fr)
            stats["capped_featured"] += before - len(fr)
            phase["featured_routes"] = fr
            if not fr:
                mark_intentional_null(phase)
                stats["intentional_null_phases"] += 1

    doc["_fidelity_trim"] = {
        "at": TS,
        "source": "grok/apply_proposal_fidelity_trim",
        "allow_drop": allow_drop,
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
    ap.add_argument("--allow-drop", action="store_true", help="Apply DROP recommendations (discouraged)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.allow_drop:
        print("WARNING: --allow-drop enabled; prefer reground_proposal_surfaces.py", file=sys.stderr)

    for slug in args.partner:
        audit_idx = load_audit_index(slug)
        for path in partner_paths(slug):
            doc = json.loads(path.read_text())
            out, stats = apply_doc(doc, audit_idx, allow_drop=args.allow_drop)
            print(
                f"{slug} {path.relative_to(ROOT)}: dropped={stats['dropped']} trimmed={stats['trimmed']} "
                f"null_phases={stats['intentional_null_phases']}"
            )
            if not args.dry_run:
                path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())