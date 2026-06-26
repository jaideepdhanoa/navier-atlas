#!/usr/bin/env python3
"""Build finance/recal/corridors-<partner>.json for Bite-2 ladder cascade."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-tasklet-import"))
from tasklet_shared import CORRIDORS_SRC, RECAL, load_json, save_json  # noqa: E402

DC = ROOT / "data-clean" / "partners"
ECON = ROOT / "data-clean" / "economics_by_route_id.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect_route_ids(doc: dict) -> set[str]:
    ids: set[str] = set()

    def walk(o):
        if isinstance(o, dict):
            rid = o.get("route_id")
            if isinstance(rid, str) and rid:
                ids.add(rid)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(doc)
    return ids


def index_corridors(src: dict) -> dict[str, tuple[str, dict]]:
    idx: dict[str, tuple[str, dict]] = {}
    for mkt, mk in (src.get("markets") or {}).items():
        for c in mk.get("corridors") or []:
            rid = c.get("route_id")
            if rid and rid not in idx:
                idx[rid] = (mkt, c)
    return idx


def corridor_from_econ(rec: dict) -> dict:
    """Minimal L3 corridor row from economics_by_route_id record."""
    mid = rec.get("mid") or {}
    pool = mid.get("market_rev_yr") or 0
    fare = rec.get("navier_fare_usd") or rec.get("fare_today_usd") or 50
    pax = int(round(pool / max(fare, 1))) if pool else 0
    parts = (rec.get("corridor") or "unknown").split(" -> ", 1)
    from_l = parts[0].strip() if parts else "origin"
    to_l = parts[1].strip() if len(parts) > 1 else "destination"
    vessel = rec.get("vessel") or "Pioneer II"
    vkey = "pioneer_ii" if "pioneer" in vessel.lower() else "quanta_lr"
    return {
        "route_id": rec.get("route_id"),
        "from": from_l,
        "to": to_l,
        "distance_nm": rec.get("distance_nm") or 10,
        "vessel": vessel,
        "archetype": "intercity",
        "country": rec.get("country") or "CrossBorder",
        "pool_basis": "addressable",
        "L3_locals": {
            "comparable_fare_usd_pax": fare,
            "corridor_annual_oneway_pax": pax,
            "_demand_record": {
                "value": pax,
                "unit": "pax/yr one-way",
                "source_tier": "T3",
                "confidence": rec.get("demand_confidence") or "med",
                "source": "economics_by_route_id.json",
                "method": "bite2/econ_sidecar_inherit",
            },
            "_fare_record": {
                "value": fare,
                "unit": "USD/pax/one-way",
                "source_tier": "T3",
                "confidence": "med",
                "source": "economics_by_route_id.json",
                "method": "bite2/econ_sidecar_inherit",
            },
            "demand_confidence": rec.get("demand_confidence") or "med",
        },
        "_bite2_source": "economics_by_route_id",
        "_vessel_key": vkey,
    }


def build(partner: str) -> dict:
    src = load_json(CORRIDORS_SRC)
    partner_path = DC / f"{partner}.json"
    if not partner_path.is_file():
        raise FileNotFoundError(partner_path)
    doc = load_json(partner_path)
    rids = collect_route_ids(doc)
    idx = index_corridors(src)

    partner_markets = [
        k for k, mk in (src.get("markets") or {}).items() if mk.get("partner") == partner
    ]

    corridors: list[dict] = []
    seen: set[str] = set()

    for mkey in partner_markets:
        for c in src["markets"][mkey].get("corridors") or []:
            rid = c.get("route_id")
            if rid and rid in seen:
                continue
            if rid:
                seen.add(rid)
            corridors.append(copy.deepcopy(c))

    for rid in sorted(rids):
        if rid in seen:
            continue
        if rid in idx:
            _, c = idx[rid]
            corridors.append(copy.deepcopy(c))
            seen.add(rid)

    econ_by: dict[str, dict] = {}
    if ECON.is_file():
        edoc = load_json(ECON)
        for rec in edoc.get("records") or []:
            rid = rec.get("route_id")
            if rid and rid not in econ_by:
                econ_by[rid] = rec

    for rid in sorted(rids):
        if rid in seen:
            continue
        if rid in econ_by:
            corridors.append(corridor_from_econ(econ_by[rid]))
            seen.add(rid)

    market_block = {
        "partner": partner,
        "region": doc.get("region") or "Global",
        "label": f"{doc.get('display') or partner} — scoped cascade",
        "fleet_basis": "network_sum",
        "fleet_rounding": "ceil",
        "_scope": f"{partner}-bite2-cascade",
        "_partner_market_keys": partner_markets,
        "_route_ids_requested": len(rids),
        "_corridors_bound": len(corridors),
        "corridors": corridors,
    }
    if doc.get("archetype") in ("hospitality",) or doc.get("category", "").startswith("hospitality"):
        market_block["capex_tier"] = "hospitality"

    capture = 0.1
    for mkey in partner_markets:
        cr = (src["markets"][mkey].get("capture_rate"))
        if cr:
            capture = cr
            break

    return {
        "_doc": f"Scoped corridors view for {partner} Bite-2 economics cascade",
        "_source": str(CORRIDORS_SRC),
        "_built_at": utc_now(),
        "capture_rate": capture,
        "markets": {partner: market_block},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--partner", required=True)
    ap.add_argument("--out", help="output path (default finance/recal/corridors-<partner>.json)")
    args = ap.parse_args()
    out = Path(args.out) if args.out else RECAL / f"corridors-{args.partner}.json"
    scoped = build(args.partner)
    n = len(scoped["markets"][args.partner]["corridors"])
    save_json(out, scoped)
    print(f"✓ {out} ({n} corridors, markets={len(scoped['markets'][args.partner]['_partner_market_keys'])})")
    return 0 if n else 2


if __name__ == "__main__":
    raise SystemExit(main())