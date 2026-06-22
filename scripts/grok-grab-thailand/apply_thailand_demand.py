#!/usr/bin/env python3
"""Apply Tasklet THAILAND-DEMAND-ANCHORS onto a scoped grab-thailand corridors view."""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff/partner-map-model"
CORR_SRC = ROOT / "finance/model/corridors.json"
CORR_OUT = ROOT / "finance/recal/corridors-grab-thailand.json"
REPORT = ROOT / "grok-routing-output/grab-thailand-demand-apply-report.json"

MARKETS = ("koh-samui", "phuket", "bangkok")

# cascade-ready corridor patches (closure manifest 2026-06-22)
PATCHES = [
    {
        "market": "koh-samui",
        "from": "Koh Samui (Bangrak)",
        "to": "Koh Phangan (Thong Sala)",
        "anchor": "THAILAND-DEMAND-ANCHORS-samui-gulf.json",
        "corridor_label": "Koh Samui (Bangrak/Maenam) -> Koh Phangan (Thong Sala)",
    },
    {
        "market": "phuket",
        "from": "Phuket",
        "to": "Phi Phi (Tonsai)",
        "anchor": "THAILAND-DEMAND-ANCHORS-phuket-andaman.json",
        "corridor_label": "Phuket (Rassada Pier) -> Koh Phi Phi (Tonsai)",
    },
    {
        "market": "bangkok",
        "from": "Sathorn (Central) Pier",
        "to": "Phra Arthit Pier",
        "anchor": "THAILAND-DEMAND-ANCHORS-bangkok.json",
        "corridor_label": "Chao Phraya river spine: Sathorn (CEN) <-> ICONSIAM (N2/1) <-> Phra Arthit (N13) corridor",
    },
]


def load_anchor(name: str) -> dict:
    return json.loads((HANDOFF / name).read_text())


def find_anchor_corridor(anchor: dict, label: str) -> dict | None:
    for c in anchor.get("corridors", []):
        if c.get("corridor") == label:
            return c
    return None


def apply_patch(corridor: dict, anchor_row: dict) -> bool:
    dr = anchor_row.get("derived_demand_record") or {}
    pax = dr.get("premium_eligible_oneway_per_year")
    fare = dr.get("fare_for_model_usd")
    if pax is None and fare is None:
        return False
    l3 = corridor.setdefault("L3_locals", {})
    if fare is not None:
        l3["comparable_fare_usd_pax"] = fare
        l3["_fare_record"] = {
            "value": fare,
            "unit": "USD/pax/one-way",
            "source": anchor_row.get("corridor"),
            "method": "THAILAND-DEMAND-ANCHORS hardened fare",
            "confidence": dr.get("confidence", "derived_pending_validation"),
            "notes": dr.get("fare_basis"),
        }
    if pax is not None:
        l3["corridor_annual_oneway_pax"] = pax
        l3["_demand_record"] = {
            "value": pax,
            "unit": "premium-eligible one-way pax/yr",
            "basis": "derived_demand_record",
            "confidence": dr.get("confidence", "derived_pending_validation"),
            "source": anchor_row.get("corridor"),
            "method": dr.get("method", "shown_math"),
            "detail": dr.get("calc"),
        }
        l3["demand_confidence"] = "derived_pending_validation"
    corridor["_thailand_demand_hardened"] = True
    corridor["_demand_anchor_file"] = anchor_row.get("_source_file")
    return True


def main() -> int:
    src = json.loads(CORR_SRC.read_text())
    out = {
        "_doc": "Scoped Thailand view for grab-thailand economics cascade",
        "_source": "finance/model/corridors.json",
        "_built_at": datetime.now(timezone.utc).isoformat(),
        "capture_rate": src.get("capture_rate", 0.1),
        "markets": {},
    }
    report = {"patched": [], "skipped": [], "markets": list(MARKETS)}

    for mid in MARKETS:
        mk = copy.deepcopy(src["markets"][mid])
        mk["partner"] = "grab-thailand"
        mk["_scope"] = "grab-thailand-derivative"
        out["markets"][mid] = mk

    for spec in PATCHES:
        anchor = load_anchor(spec["anchor"])
        row = find_anchor_corridor(anchor, spec["corridor_label"])
        if not row:
            report["skipped"].append({**spec, "reason": "anchor row not found"})
            continue
        row = {**row, "_source_file": spec["anchor"]}
        mk = out["markets"][spec["market"]]
        hit = False
        for c in mk["corridors"]:
            if c.get("from") == spec["from"] and c.get("to") == spec["to"]:
                if apply_patch(c, row):
                    report["patched"].append({
                        "market": spec["market"],
                        "corridor": f"{spec['from']} -> {spec['to']}",
                        "pax": (row.get("derived_demand_record") or {}).get("premium_eligible_oneway_per_year"),
                        "fare_usd": (row.get("derived_demand_record") or {}).get("fare_for_model_usd"),
                    })
                    hit = True
                break
        if not hit:
            report["skipped"].append({**spec, "reason": "corridor not found in scoped markets"})

    CORR_OUT.parent.mkdir(parents=True, exist_ok=True)
    CORR_OUT.write_text(json.dumps(out, indent=2) + "\n")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"corridors_out": str(CORR_OUT), "patched": len(report["patched"]), "skipped": len(report["skipped"])}, indent=2))
    return 0 if report["patched"] else 1


if __name__ == "__main__":
    raise SystemExit(main())