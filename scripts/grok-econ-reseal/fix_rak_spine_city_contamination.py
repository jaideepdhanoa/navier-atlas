#!/usr/bin/env python3
"""Fix RAK spine rows where Dubai/Ajman/Sharjah BPs were tagged ras-al-khaimah-uae."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff" / "partner-map-model"
DC = ROOT / "data-clean"
SPINE = HANDOFF / "uae-gulf-shared-corridor-spine.json"
LEDGERS = (
    HANDOFF / "rakta-route-seal-ledger-2026-06-21.json",
    HANDOFF / "rakta-held-null-route-ledger-2026-06-21.json",
)

DUBAI_HINTS = ("dubai", "deira", "ghubaiba", "sabkha", "port rashid", "cruise terminal", "dubai island", "dubai canal", "dubai offshore")
SHARJAH_HINTS = ("sharjah", "hamriyah", "dibba", "ajman", "al zorah", "uaq marine")


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def bp_city_index() -> dict[str, str]:
    fbt = load(DC / "FEATURES_BY_TYPE.json")
    out = {}
    for f in fbt.get("poi") or []:
        p = f.get("properties") or {}
        bid = p.get("id")
        if bid and p.get("parent_city_id"):
            out[bid] = p["parent_city_id"]
    return out


def label_city(from_lbl: str, to_lbl: str) -> tuple[str | None, str | None]:
    blob = f"{from_lbl} {to_lbl}".lower()
    fc = tc = None
    if any(h in from_lbl.lower() for h in DUBAI_HINTS):
        fc = "dubai-uae"
    elif any(h in from_lbl.lower() for h in SHARJAH_HINTS):
        fc = "sharjah-uae"
    if any(h in to_lbl.lower() for h in DUBAI_HINTS):
        tc = "dubai-uae"
    elif any(h in to_lbl.lower() for h in SHARJAH_HINTS):
        tc = "sharjah-uae"
    if not fc and not tc:
        if any(h in blob for h in DUBAI_HINTS):
            fc = tc = "dubai-uae"
        elif any(h in blob for h in SHARJAH_HINTS):
            fc = tc = "sharjah-uae"
    return fc, tc


def infer_city(
    from_bp: str | None,
    to_bp: str | None,
    from_lbl: str,
    to_lbl: str,
    bp_idx: dict,
    *,
    prefer_labels: bool = False,
) -> tuple[str | None, str | None]:
    lfc, ltc = label_city(from_lbl, to_lbl)
    if prefer_labels:
        fc, tc = lfc, ltc
    else:
        fc = bp_idx.get(from_bp) if from_bp else None
        tc = bp_idx.get(to_bp) if to_bp else None
        if not fc:
            fc = lfc
        if not tc:
            tc = ltc
    return fc, tc


def fix_row(row: dict, bp_idx: dict) -> bool:
    is_contamination = row.get("classification") == "held_exact_bind_required_city_label_contamination"
    fc, tc = infer_city(
        row.get("from_node_id"),
        row.get("to_node_id"),
        row.get("from_label", ""),
        row.get("to_label", ""),
        bp_idx,
        prefer_labels=is_contamination,
    )
    if not is_contamination and not fc and not tc:
        return False
    changed = False
    old_fc, old_tc = row.get("from_city_id"), row.get("to_city_id")
    if fc and fc != old_fc:
        row["from_city_id"] = fc
        changed = True
    if tc and tc != old_tc:
        row["to_city_id"] = tc
        changed = True
    if is_contamination and (changed or fc or tc):
        if fc == tc == "dubai-uae" or (fc == "dubai-uae" and tc == "ras-al-khaimah-uae") or (fc == "ras-al-khaimah-uae" and tc == "dubai-uae"):
            row["classification"] = "proposal_active_rak_dubai_inter_emirate"
            row["market_key"] = "inter_emirate_uae"
            row["guardrail"] = "Reclassified after BP parent_city_id fix — commercial-now candidate after seal"
        elif fc and tc and fc != tc:
            row["classification"] = "proposal_active_rak_dubai_inter_emirate"
            row["market_key"] = "inter_emirate_uae"
        else:
            row["classification"] = "proposal_active_rak_domestic"
        changed = True
    return changed


def refresh_ledger_summary(doc: dict, rows: list) -> None:
    from collections import Counter

    summary = doc.setdefault("summary", {})
    summary["by_classification"] = dict(Counter(r.get("classification") for r in rows))
    summary["total_geometry_present_spine_rows"] = sum(
        1 for r in rows if r.get("geometry_status_spine") == "geometry_present"
    )


def main() -> int:
    bp_idx = bp_city_index()
    fixed = 0
    for ledger_path in LEDGERS:
        if not ledger_path.exists():
            continue
        doc = load(ledger_path)
        rows = doc.get("routes") or doc.get("held_routes") or []
        for row in rows:
            if fix_row(row, bp_idx):
                fixed += 1
        refresh_ledger_summary(doc, rows)
        save(ledger_path, doc)

    if SPINE.exists():
        spine = load(SPINE)
        for row in spine.get("corridors") or []:
            if row.get("partner_id") == "rakta" or row.get("market_key") == "domestic_uae_intra_city":
                if fix_row(row, bp_idx):
                    fixed += 1
        spine.setdefault("_meta", {})["rak_contamination_fix_at"] = datetime.now(timezone.utc).isoformat()
        save(SPINE, spine)

    report = {"at": datetime.now(timezone.utc).isoformat(), "rows_fixed": fixed}
    save(HANDOFF / "rak-spine-contamination-fix-report.json", report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())