#!/usr/bin/env python3
"""
RE-GROUND bp_binding failures — clear wrong route_id (HOLD null), never DROP carousel text.

Reads latest PROPOSAL-FIDELITY-{partner}.json audit; for DROP+bp_binding items:
  - Clear route_id / route_ids
  - Set display=text_only, _link_status=unlinked-bp-hold
  - Record _fidelity_trim

Usage:
  python3 scripts/reground_bp_binding_holds.py --partner grab bolt rapido --apply
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
    audit_item,
    build_indexes,
    corridor_label,
    iter_proposal_items,
    resolve_route_id,
)

HANDOFF = ROOT / "handoff" / "partner-map-model"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
RECEIPT = HANDOFF / "BP-BINDING-HOLD-RECEIPT.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def audit_key(surface: str, phase, item: dict) -> tuple:
    return (surface, str(phase), corridor_label(item), resolve_route_id(item) or "")


def build_audit_index(slug: str) -> dict[tuple, dict]:
    path = HANDOFF / f"PROPOSAL-FIDELITY-{slug}.json"
    record = load_json(path)
    idx: dict[tuple, dict] = {}
    for it in record["items"]:
        corridor = it.get("corridor") or ""
        item_stub: dict = {"route_id": it.get("route_id")}
        if " → " in corridor:
            fl, tl = corridor.split(" → ", 1)
            item_stub["from_label"] = fl.strip()
            item_stub["to_label"] = tl.strip()
            item_stub["label"] = f"{fl.strip()} ↔ {tl.strip()}"
        else:
            item_stub["label"] = corridor
        idx[audit_key(it["surface"], it["phase"], item_stub)] = it
    return idx


def hold_item(item: dict, detail: str) -> dict:
    out = copy.deepcopy(item)
    out.pop("route_id", None)
    out.pop("route_ids", None)
    out["display"] = "text_only"
    out["_link_status"] = "unlinked-bp-hold"
    out["_link_source"] = "grok/reground_bp_binding_holds"
    out["_fidelity_trim"] = {"at": TS, "reason": "bp_binding_hold_null", "detail": detail[:120]}
    return out


def patch_list(items: list, surface: str, phase, audit_idx: dict, stats: dict) -> list:
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        key = audit_key(surface, phase, item)
        rec = audit_idx.get(key)
        if rec and rec.get("recommendation") == "DROP":
            flags = rec.get("flags") or []
            if any(f.get("check") == "bp_binding" for f in flags):
                detail = next(
                    (f.get("detail", "") for f in flags if f.get("check") == "bp_binding"),
                    "",
                )
                out.append(hold_item(item, detail))
                stats["held"] = stats.get("held", 0) + 1
                continue
        out.append(copy.deepcopy(item))
        stats["unchanged"] = stats.get("unchanged", 0) + 1
    return out


def apply_partner(slug: str, *, apply: bool) -> dict:
    path = ROOT / "data-clean" / "partners" / f"{slug}.json"
    doc = load_json(path)
    audit_idx = build_audit_index(slug)
    stats: dict[str, int] = {}

    doc["journeys_unlocked"] = patch_list(doc.get("journeys_unlocked") or [], "journey", None, audit_idx, stats)
    for phase in doc.get("phases") or []:
        phase["featured_routes"] = patch_list(
            phase.get("featured_routes") or [], "featured", phase.get("n"), audit_idx, stats
        )
    for market in doc.get("markets") or []:
        mid = market.get("id")
        market["journeys_unlocked"] = patch_list(
            market.get("journeys_unlocked") or [], "journey", f"market:{mid}", audit_idx, stats
        )
        for phase in market.get("phases") or []:
            pn = phase.get("n")
            phase["featured_routes"] = patch_list(
                phase.get("featured_routes") or [], "featured", f"{mid}/p{pn}", audit_idx, stats
            )

    doc["_bp_binding_hold"] = {"at": TS, "stats": stats}
    if apply:
        save_json(path, doc)
        pitch = ROOT / "partner-pitch" / "partners" / f"{slug}.json"
        if pitch.parent.exists():
            save_json(pitch, doc)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="+", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    receipt = {"at": TS, "partners": {}}
    for slug in args.partner:
        stats = apply_partner(slug, apply=args.apply)
        receipt["partners"][slug] = stats
        print(f"{slug}: {stats}")

    if args.apply:
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())