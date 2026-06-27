#!/usr/bin/env python3
"""QA gate for hospitality deck_type — render-complete checklist (#112)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: qa_hospitality_gate.py <deck-key>", file=sys.stderr)
        return 2
    deck = sys.argv[1]
    d = ROOT / "decks" / deck
    binding = load_json(d / "economics-binding.json")
    values_path = d / f"deck-economics-values-{deck}.json"
    checks: list[dict] = []

    if binding.get("deck_type") != "hospitality":
        checks.append({"name": "deck_type", "status": "fail", "details": binding.get("deck_type")})
    else:
        checks.append({"name": "deck_type", "status": "pass", "details": "hospitality"})

    ladder = (binding.get("economics_frame") or {}).get("ladder", "")
    if "NONE" in str(ladder).upper() or "no som" in str(ladder).lower():
        checks.append({"name": "no_ladder", "status": "pass", "details": "ladder deprecated"})
    else:
        checks.append({"name": "no_ladder", "status": "fail", "details": ladder[:80]})

    appendix = binding.get("appendix_cards") or []
    checks.append({
        "name": "appendix_cards_binding",
        "status": "pass" if len(appendix) >= 7 else "fail",
        "details": f"{len(appendix)} cards",
    })

    bgs = binding.get("appendix_backgrounds") or []
    page_fills = [b for b in bgs if "pageBackgroundFill" in (b.get("apply") or "")]
    checks.append({
        "name": "appendix_page_fill_backgrounds",
        "status": "pass" if len(page_fills) == len(appendix) else "fail",
        "details": f"{len(page_fills)}/{len(appendix)} page-fills",
    })

    for bg in page_fills:
        if not bg.get("source_url") or "googleusercontent" in str(bg.get("source_url", "")):
            checks.append({
                "name": f"stable_url_{bg.get('slide_index')}",
                "status": "fail",
                "details": bg.get("asset_ref"),
            })

    if values_path.is_file():
        values = load_json(values_path)
        if values.get("slide10_tam") is not None or values.get("slide3_kpi") is not None:
            checks.append({"name": "values_no_mobility_ladder", "status": "fail", "details": "ladder fields present"})
        else:
            checks.append({"name": "values_no_mobility_ladder", "status": "pass", "details": "appendix only"})
        vcards = values.get("appendix_cards") or {}
        filled = sum(1 for v in vcards.values() if v.get("fields"))
        checks.append({
            "name": "appendix_values_filled",
            "status": "pass" if filled == len(appendix) else "fail",
            "details": f"{filled}/{len(appendix)}",
        })
        frame = values.get("_meta", {}).get("economics_frame") or {}
        if frame.get("vessel_investment_usd") == 1_000_000:
            checks.append({"name": "vessel_frame_1m", "status": "pass", "details": "$1M/vessel"})
        co2_ok = all((v.get("fields") or {}).get("co2_avoided_tonnes_year") for v in vcards.values() if v.get("fields"))
        checks.append({"name": "co2_present", "status": "pass" if co2_ok else "fail", "details": str(co2_ok)})
    else:
        checks.append({"name": "values_file", "status": "fail", "details": "missing"})

    status = "fail" if any(c["status"] == "fail" for c in checks) else "pass"
    receipt = {
        "deck_key": deck,
        "deck_type": "hospitality",
        "status": status,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "held": ["minor-hotels appendix re-pull audit_pending", "live deck apply not run"],
    }
    out = d / "qa-receipts" / "hospitality-qa-gate.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())