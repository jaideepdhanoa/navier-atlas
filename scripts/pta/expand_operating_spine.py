#!/usr/bin/env python3
"""Apply hub-spoke pair recommendations from PTA-PAIR-GAP-TABLE to dossiers."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GAP_TABLE = ROOT / "handoff/partner-map-model/PTA-PAIR-GAP-TABLE.json"
HANDOFF = ROOT / "handoff/partner-map-model"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pair_exists(pairs: list[dict], a: str, b: str) -> bool:
    key = frozenset({a, b})
    return any(frozenset({p["from"], p["to"]}) == key for p in pairs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", action="append", help="Limit to partner slug(s)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--all", action="store_true", help="All authorities with expand_hub_spoke action")
    args = ap.parse_args()

    gap = json.loads(GAP_TABLE.read_text())
    targets = []
    for row in gap["authorities"]:
        if row["expansion_action"] != "expand_hub_spoke":
            continue
        if args.partner and row["partner_id"] not in args.partner:
            continue
        if not args.all and not args.partner:
            continue
        targets.append(row)

    if not targets and not args.partner:
        print("No expansion targets (spine already complete)")
        return 0

    if args.partner and not targets:
        for slug in args.partner:
            row = next((r for r in gap["authorities"] if r["partner_id"] == slug), None)
            if row and row.get("recommended_pairs"):
                targets.append(row)

    report = {"generated_at": utc_now(), "applied": [], "skipped": []}

    for row in targets:
        slug = row["partner_id"]
        path = HANDOFF / f"PTA-DOSSIER-{slug}.json"
        if not path.is_file():
            report["skipped"].append({"partner": slug, "reason": "no dossier"})
            continue
        dossier = json.loads(path.read_text())
        pairs = dossier["domestic_network"].setdefault("domestic_pairs", [])
        added = []
        for rec in row.get("recommended_pairs", []):
            if pair_exists(pairs, rec["from"], rec["to"]):
                continue
            pairs.append({k: v for k, v in rec.items() if k not in ("source", "hub")})
            added.append(rec["pair_id"])

        if not added:
            report["skipped"].append({"partner": slug, "reason": "no new pairs"})
            continue

        dossier.setdefault("provenance", {})["spine_expanded_at"] = utc_now()
        dossier["provenance"]["spine_expanded_pairs"] = added
        report["applied"].append({"partner": slug, "added": added, "total_pairs": len(pairs)})

        if args.apply:
            path.write_text(json.dumps(dossier, indent=2, ensure_ascii=False) + "\n")
            print(f"  ✓ {slug}: +{len(added)} pairs → {len(pairs)} total")

    receipt = HANDOFF / "PTA-SPINE-EXPANSION-RECEIPT.json"
    if args.apply:
        receipt.write_text(json.dumps(report, indent=2) + "\n")

    print(json.dumps({"applied": len(report["applied"]), "skipped": len(report["skipped"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())