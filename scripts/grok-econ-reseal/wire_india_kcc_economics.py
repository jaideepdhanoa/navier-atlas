#!/usr/bin/env python3
"""Wire pending economics stubs for india_kcc + extension routes."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff" / "partner-map-model"


def load(path: Path):
    return json.loads(path.read_text())


def stub_record(route_id: str, corridor: str, market: str, distance_nm: float, vessel: str, *, roadmap: bool = False) -> dict:
    return {
        "route_id": route_id,
        "registry_market_id": market,
        "authored_for": "rapido",
        "corridor": corridor,
        "market": market.replace("-", " ").title(),
        "country": "India",
        "distance_nm": distance_nm,
        "status": "roadmap" if roadmap else "pending",
        "demand_confidence": "low" if roadmap else "med-low",
        "fare_today_usd": None,
        "navier_fare_usd": None,
        "vessel": vessel,
        "estimation_basis": "india_kcc_pending_cascade",
        "assumptions": {"note": "Economics cascade pending — geometry sealed, fare/demand null per Tasklet guardrail"},
    }


def collect_route_ids() -> list[dict]:
    rows = []
    for name in ("india-kolkata-chennai-mint-report.json", "india-extension-mint-report.json"):
        p = HANDOFF / name
        if not p.exists():
            continue
        for m in load(p).get("minted", []):
            rows.append(m)
    return rows


def main() -> int:
    econ_path = DC / "economics_by_route_id.json"
    econ = load(econ_path)
    records = list(econ.get("records") or [])
    by_id = {r["route_id"]: r for r in records if r.get("route_id")}
    added = []
    for m in collect_route_ids():
        rid = m["route_id"]
        if rid in by_id:
            continue
        market = "india-kolkata" if m.get("from_city_id") == "kolkata-india" and m.get("key") != "chennai_puducherry" else "india-chennai"
        if "kolkata" in m.get("partner_market_id", ""):
            market = "india-kolkata-rapido"
        elif "chennai" in m.get("partner_market_id", ""):
            market = "india-chennai-rapido"
        corridor = f"{m.get('from_label', '')} -> {m.get('to_label', '')}"
        vessel = m.get("platform") or ("Quanta-LR" if (m.get("distance_nm") or 0) > 70 else "N30 Pioneer II")
        rec = stub_record(rid, corridor, market, m.get("distance_nm") or 0, vessel, roadmap=bool(m.get("roadmap")))
        records.append(rec)
        by_id[rid] = rec
        added.append(rid)

    econ["records"] = records
    meta = econ.setdefault("_meta", {})
    meta["india_kcc_wire_at"] = datetime.now(timezone.utc).isoformat()
    meta["records"] = len(records)
    meta["india_kcc_stubs_added"] = len(added)
    econ_path.write_text(json.dumps(econ, indent=1, ensure_ascii=False) + "\n")
    report = {"at": meta["india_kcc_wire_at"], "added": added, "count": len(added)}
    (HANDOFF / "india-kcc-economics-wire-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())