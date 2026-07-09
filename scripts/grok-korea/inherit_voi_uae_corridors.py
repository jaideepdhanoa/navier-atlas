#!/usr/bin/env python3
"""#208 follow-up: seed Voi UAE (Dubai) finance corridors from uae-noon / bolt-uae spine.

Finance-corridor inheritance: same Dubai/UAE route_id set as Dott/Careem/Noon;
only partner overlay (partner field / capture) differs. Null model_link on Voi
UAE sub-proposal until this lands.
"""
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "finance/model/corridors.json"
RECAL_VOI = ROOT / "finance/recal/corridors-voi.json"
RECEIPT = ROOT / "handoff/partner-map-model/VOI-UAE-FINANCE-INHERIT-2026-07-09.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    model = json.loads(MODEL.read_text())
    mkts = model.get("markets") or {}
    # Prefer noon (denser L3) else careem else bolt-uae
    src_key = next((k for k in ("uae-noon", "uae-careem", "bolt-uae") if k in mkts), None)
    if not src_key:
        print("✗ no UAE source market in model/corridors.json")
        return 2
    src = mkts[src_key]
    corridors = copy.deepcopy(src.get("corridors") or [])
    for c in corridors:
        # keep L3; mark inherit
        c["_finance_inherit"] = {
            "from_market": src_key,
            "at": utc_now(),
            "partner": "voi",
        }

    block = {
        "partner": "voi",
        "region": "UAE",
        "label": "Voi — UAE Dubai expansion (inherited UAE spine)",
        "fleet_basis": src.get("fleet_basis") or "network_sum",
        "fleet_rounding": src.get("fleet_rounding") or "ceil",
        "capture_rate": src.get("capture_rate") or 0.1,
        "_scope": "uae-voi-inherit",
        "_provenance": {
            "spec": "PR #208 Grok follow-up",
            "source_market": src_key,
            "at": utc_now(),
        },
        "corridors": corridors,
    }

    receipt = {
        "at": utc_now(),
        "source_market": src_key,
        "n_corridors": len(corridors),
        "with_l3_pax": sum(
            1
            for c in corridors
            if (c.get("L3_locals") or {}).get("corridor_annual_oneway_pax")
        ),
    }

    if not args.apply:
        print(json.dumps(receipt, indent=2))
        return 0

    mkts["uae-voi"] = block
    model["markets"] = mkts
    MODEL.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n")

    # Merge into recal corridors-voi.json (keep existing EU markets)
    if RECAL_VOI.exists():
        recal = json.loads(RECAL_VOI.read_text())
    else:
        recal = {
            "_doc": "Voi scoped corridors",
            "capture_rate": 0.1,
            "markets": {},
        }
    recal.setdefault("markets", {})["uae-voi"] = {
        "partner": "voi",
        "region": "UAE",
        "label": block["label"],
        "fleet_basis": block["fleet_basis"],
        "fleet_rounding": block["fleet_rounding"],
        "_scope": "uae-voi-inherit",
        "_partner_market_keys": ["uae-voi"],
        "_corridors_bound": len(corridors),
        "corridors": corridors,
        "_provenance": block["_provenance"],
    }
    recal["_built_at"] = utc_now()
    recal["_doc"] = "Voi corridors — EU markets + UAE Dubai inherit (#208)"
    RECAL_VOI.write_text(json.dumps(recal, indent=2, ensure_ascii=False) + "\n")

    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"wrote": [str(MODEL), str(RECAL_VOI), str(RECEIPT)], **receipt}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
