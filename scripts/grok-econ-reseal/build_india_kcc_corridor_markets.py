#!/usr/bin/env python3
"""Add Kolkata/Chennai + extension corridors to finance/model/corridors.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRIDORS = ROOT / "finance" / "model" / "corridors.json"
ROUTES = ROOT / "data-clean" / "ROUTES.json"
HANDOFF = ROOT / "handoff" / "partner-map-model"

KCC_ANCHORS = {
    "kolkata": {"label": "India — Kolkata / Hooghly", "fare": 2.5, "pax": 8000000, "country": "India"},
    "chennai": {"label": "India — Chennai / ECR coast", "fare": 12.0, "pax": 1200000, "country": "India"},
}


def route_props() -> dict[str, dict]:
    raw = json.loads(ROUTES.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    return {f["properties"]["id"]: f["properties"] for f in feats if f.get("properties", {}).get("id")}


def collect_route_ids() -> dict[str, list[str]]:
    out = {"kolkata": [], "chennai": []}
    for name in ("india-kolkata-chennai-mint-report.json", "india-extension-mint-report.json"):
        p = HANDOFF / name
        if not p.exists():
            continue
        for m in json.loads(p.read_text()).get("minted", []):
            if m.get("roadmap"):
                continue
            cid = m.get("from_city_id") or ""
            rid = m.get("route_id")
            if not rid:
                continue
            if cid == "kolkata-india":
                out["kolkata"].append(rid)
            elif cid == "chennai-india":
                out["chennai"].append(rid)
    for k in out:
        out[k] = list(dict.fromkeys(out[k]))
    return out


def main() -> int:
    by_id = route_props()
    buckets = collect_route_ids()
    corr = json.loads(CORRIDORS.read_text())
    markets = corr.setdefault("markets", {})
    for partner in ("rapido", "ola", "uber-india"):
        for key, anchor in KCC_ANCHORS.items():
            rids = buckets[key]
            if not rids:
                continue
            pax_each = max(50000, int(anchor["pax"] / len(rids)))
            rows = []
            for rid in rids:
                p = by_id.get(rid, {})
                nm = float(p.get("distance_nm") or 0)
                rows.append({
                    "route_id": rid,
                    "from": p.get("from_label", ""),
                    "to": p.get("to_label", ""),
                    "distance_nm": nm,
                    "vessel": "Pioneer II" if nm <= 70 else "Quanta-LR",
                    "archetype": "ridehail",
                    "country": anchor["country"],
                    "pool_basis": "addressable",
                    "_india_kcc": True,
                    "L3_locals": {
                        "comparable_fare_usd_pax": anchor["fare"],
                        "corridor_annual_oneway_pax": pax_each,
                        "demand_confidence": "med-low",
                    },
                })
            mid = f"india-{key}-{partner}"
            markets[mid] = {
                "partner": partner,
                "region": "South Asia",
                "label": anchor["label"],
                "fleet_basis": "network_sum",
                "corridors": rows,
            }
            print(f"  {mid}: {len(rows)} corridors")
    CORRIDORS.write_text(json.dumps(corr, indent=1, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())