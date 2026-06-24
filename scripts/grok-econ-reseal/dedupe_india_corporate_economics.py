#!/usr/bin/env python3
"""Differentiate Adani Ports vs Reliance Industries scoped corridor economics.

Same inherited India spine geometry; partner-specific demand haircuts/uplifts
so agg/TAM no longer byte-match.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FINANCE = ROOT / "finance"
MODEL = FINANCE / "model"
RECAL = FINANCE / "recal"
PARTNERS = ROOT / "partner-pitch" / "partners"
REPORT = ROOT / "grok-routing-output/india-corporate-dedupe-report.json"

PARTNER_SPECS: dict[str, dict] = {
    "adani-ports": {
        "capture_rate": 0.11,
        "market_multipliers": {
            "india-mumbai-rapido": 1.12,
            "india-kerala-rapido": 1.18,
            "india-chennai-rapido": 1.08,
            "india-kolkata-rapido": 1.05,
            "india-goa-rapido": 1.0,
            "india-andaman-rapido": 1.0,
        },
        "note": "Port-terminal operator uplift on harbour-adjacent markets (Mumbai, Kerala/Vizhinjam, eastern gateways).",
    },
    "reliance-industries": {
        "capture_rate": 0.09,
        "market_multipliers": {
            "india-goa-rapido": 1.15,
            "india-andaman-rapido": 1.10,
            "india-mumbai-rapido": 1.05,
            "india-kerala-rapido": 1.0,
            "india-kolkata-rapido": 0.75,
            "india-chennai-rapido": 0.75,
        },
        "note": "Consumer/leisure conglomerate: Goa + Andaman weighted; eastern markets held back pending sourced demand.",
    },
}

MARKET_LABELS = {
    "india-mumbai-rapido": "mumbai",
    "india-goa-rapido": "goa",
    "india-kerala-rapido": "kerala",
    "india-andaman-rapido": "andaman",
    "india-kolkata-rapido": "kolkata",
    "india-chennai-rapido": "chennai",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def patch_corridors(partner: str, spec: dict) -> dict:
    src = RECAL / f"corridors-{partner}.json"
    doc = json.loads(src.read_text())
    stats = {"partner": partner, "corridors_patched": 0, "markets": {}}
    for mkey, mult in spec["market_multipliers"].items():
        mk = doc["markets"].get(mkey)
        if not mk:
            continue
        n = 0
        for c in mk.get("corridors") or []:
            l3 = c.get("L3_locals") or {}
            pax = l3.get("corridor_annual_oneway_pax")
            if not isinstance(pax, (int, float)) or pax <= 0:
                continue
            new_pax = int(round(pax * mult))
            l3["corridor_annual_oneway_pax"] = new_pax
            dr = l3.get("_demand_record") or {}
            if dr:
                dr["value"] = new_pax
                dr["method"] = f"india_corporate_dedupe:{partner}"
                dr["source"] = spec["note"]
            c["L3_locals"] = l3
            c["_india_corporate_dedupe"] = {"partner": partner, "multiplier": mult}
            n += 1
        stats["markets"][mkey] = {"multiplier": mult, "corridors": n}
        stats["corridors_patched"] += n
    doc["capture_rate"] = spec["capture_rate"]
    doc["_india_corporate_dedupe_at"] = now_iso()
    doc["_india_corporate_dedupe_note"] = spec["note"]
    src.write_text(json.dumps(doc, indent=2) + "\n")
    return stats


def cascade_partner(partner: str) -> dict:
    markets = ",".join(MARKET_LABELS.values())
    corr = RECAL / f"corridors-{partner}.json"
    agg = RECAL / f"agg-{partner}.json"
    growth = RECAL / f"growth-{partner}.json"
    subprocess.run(
        [
            sys.executable,
            str(MODEL / "aggregate.py"),
            "--partner",
            partner,
            "--markets",
            markets,
            "--corridors",
            str(corr),
            "--json",
            str(agg),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(MODEL / "growth.py"),
            "--partner",
            partner,
            "--markets",
            markets,
            "--agg",
            str(agg),
            "--json",
            str(growth),
        ],
        check=True,
    )
    frontend = ROOT / "partner-pitch/partners/_growth-draft" / f"{partner}.growth.json"
    subprocess.run(
        [
            sys.executable,
            str(MODEL / "growth_frontend_block.py"),
            "--partner",
            partner,
            "--partner-json",
            str(PARTNERS / f"{partner}.json"),
            "--growth",
            str(growth),
            "--rollup",
            str(agg),
            "--out",
            str(frontend),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(FINANCE / "splice_growth_into_partner.py"),
            "--partner",
            partner,
            "--growth",
            str(growth),
            "--frontend",
            str(frontend),
            "--partner-json",
            str(PARTNERS / f"{partner}.json"),
        ],
        check=True,
    )
    agg_doc = json.loads(agg.read_text())
    floor = agg_doc.get("rollup", {}).get("grounded_floor", {})
    return {
        "market_rev_yr": floor.get("market_rev_yr"),
        "fleet": floor.get("fleet"),
        "n_corridors": agg_doc.get("rollup", {}).get("n_corridors_total"),
    }


def main() -> int:
    report = {"at": now_iso(), "partners": {}}
    for partner, spec in PARTNER_SPECS.items():
        report["partners"][partner] = {
            "patch": patch_corridors(partner, spec),
            "cascade": cascade_partner(partner),
        }
        dst = ROOT / "data-clean" / "partners" / f"{partner}.json"
        src = PARTNERS / f"{partner}.json"
        if src.exists():
            dst.write_text(src.read_text())
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    a = report["partners"]["adani-ports"]["cascade"]["market_rev_yr"]
    r = report["partners"]["reliance-industries"]["cascade"]["market_rev_yr"]
    return 0 if a != r else 1


if __name__ == "__main__":
    raise SystemExit(main())