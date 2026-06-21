#!/usr/bin/env python3
"""
Populate corridor_annual_oneway_pax on ola-mumbai / rapido-mumbai draft markets.

Tasklet captured M2M fare floors + load anchors but held annual demand null until
route counts were sealed. Split the PR #58 Mumbai market anchor (120k pax/yr) across
each market's sealed route_id rows — comparable_fare stays null (public floor only).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRIDORS = ROOT / "finance" / "model" / "corridors.json"
MARKET_ANCHOR_PAX = 120_000
DRAFT_KEYS = ("ola-mumbai", "rapido-mumbai")


def main() -> int:
    corr = json.loads(CORRIDORS.read_text())
    for mid in DRAFT_KEYS:
        mk = corr["markets"].get(mid)
        if not mk:
            print(f"skip {mid}: not in corridors.json")
            continue
        rows = [c for c in mk.get("corridors", []) if c.get("route_id")]
        if not rows:
            print(f"skip {mid}: no route_id rows")
            continue
        pax_each = max(5000, int(MARKET_ANCHOR_PAX / len(rows)))
        for c in rows:
            l3 = c.setdefault("L3_locals", {})
            if l3.get("corridor_annual_oneway_pax") is not None:
                continue
            l3["corridor_annual_oneway_pax"] = pax_each
            l3["demand_confidence"] = "med-low"
            rec = l3.setdefault("_demand_record", {})
            rec.update({
                "value": pax_each,
                "unit": "pax/yr one-way (addressable)",
                "source_tier": "T3",
                "confidence": "med-low",
                "basis": "addressable",
                "source": f"PR #58 Mumbai spine route-count split ({len(rows)} sealed rows × anchor {MARKET_ANCHOR_PAX:,} pax/yr)",
                "method": "Market anchor split after sealed route count captured; M2M fare floor unchanged.",
            })
            if l3.get("_status") == "DRAFT_ONLY_PUBLIC_FARE_FLOOR_DEMAND_NULL":
                l3["_status"] = "DRAFT_FARE_FLOOR_DEMAND_SPLIT"
        mk["finance_status"] = "draft_demand_split_route_count_captured"
        mk["_demand_split_at"] = "2026-06-20"
        print(f"{mid}: {len(rows)} corridors @ {pax_each} pax/yr each")

    meta = corr.setdefault("_meta", {})
    meta["mumbai_draft_demand_split"] = {"at": "2026-06-20", "markets": list(DRAFT_KEYS)}
    CORRIDORS.write_text(json.dumps(corr, indent=1, ensure_ascii=False) + "\n")
    print(f"patched {CORRIDORS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())