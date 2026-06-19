#!/usr/bin/env python3
"""
Economics-only reseal: refresh growth_case + economics_url on fresh partners.
Geometry / markets untouched. Held: saudi-pif, red-sea-global.
"""
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INGEST = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal"

FRESH_PARTNERS = frozenset(
    {"grab", "careem", "bolt", "yango", "qatar", "jih-global", "constance", "four-seasons"}
)
HELD = frozenset({"saudi-pif", "red-sea-global"})


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def wire_economics_url(obj, url: str):
    if not url:
        return
    obj["economics_url"] = url
    gc = obj.get("growth_case") or {}
    rp = gc.get("revenue_potential") or {}
    for rung in rp.get("rungs") or []:
        if isinstance(rung, dict):
            rung["model_link"] = url
    pe = gc.get("phase_economics") or {}
    for phase in pe.get("phases") or []:
        if isinstance(phase, dict):
            phase.setdefault("model_link", url)


def merge_growth_case(current: dict, handoff: dict, url: str) -> dict:
    out = copy.deepcopy(current)
    if handoff.get("growth_case"):
        out["growth_case"] = copy.deepcopy(handoff["growth_case"])
    wire_economics_url(out, url)
    out["_econ_reseal"] = {
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "package": "econ-reseal-2026-06-19",
        "fresh": True,
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dc", default="data-clean")
    ap.add_argument("--ingest", default=str(INGEST))
    args = ap.parse_args()

    dc = ROOT / args.dc
    ingest = Path(args.ingest)
    url_map = load_json(ingest / "inputs/economics_url_map.json").get("economics_url", {})
    manifest = load_json(ingest / "inputs/seal-manifest.json")

    report = {"fresh": [], "skipped_held": list(HELD), "errors": []}
    for pid, spec in (manifest.get("partners") or {}).items():
        if not spec.get("fresh_this_reseal"):
            continue
        if pid not in FRESH_PARTNERS:
            continue
        handoff_path = ingest / "partners" / f"{pid}.json"
        live_path = dc / "partners" / f"{pid}.json"
        if not handoff_path.exists():
            report["errors"].append(f"missing handoff {handoff_path}")
            continue
        if not live_path.exists():
            report["errors"].append(f"missing live {live_path}")
            continue
        handoff = load_json(handoff_path)
        current = load_json(live_path)
        url = handoff.get("economics_url") or url_map.get(pid)
        merged = merge_growth_case(current, handoff, url)
        save_json(live_path, merged)
        rungs = len((merged.get("growth_case") or {}).get("revenue_potential", {}).get("rungs") or [])
        prov = (merged.get("growth_case") or {}).get("_provenance", {})
        report["fresh"].append(
            {
                "partner": pid,
                "economics_url": url,
                "ladder_rungs": rungs,
                "source_rollup": prov.get("source_rollup"),
                "sourced_corridors": prov.get("sourced_corridors"),
            }
        )

    out = ROOT / "grok-routing-output" / "econ-reseal-report.json"
    save_json(out, report)
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()